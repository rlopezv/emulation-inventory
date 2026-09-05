#!/usr/bin/env python3
"""
Compara una colección física de ROMs/discos contra los 3 DAT que produce
`retool-1g1r-pipeline.py` (FULLSET, FINAL 1G1R, cuarentena de idioma) y,
opcionalmente, organiza la colección en tres carpetas de salida
(fullset/1g1r/japan) a partir de esa comparación.

Motivación (ver docs/session-context.md, sesión 2026-09-02): comparar por
nombre exacto contra una colección grande deja de ser práctico a partir de
cierto tamaño — Redump renombra títulos entre versiones del DAT (añade tags
de idioma, cambia guion/espaciado, sube de revisión), y esas discrepancias
de nombre se confunden con huecos reales de la colección si solo se compara
1:1. Por eso esta herramienta hace DOS pasadas:

    1. Coincidencia EXACTA (nombre completo, sin extensión).
    2. Coincidencia NORMALIZADA (misma base de título + primer grupo entre
       paréntesis, que se asume la región — el resto de tags se ignora).
       Un match que solo aparece aquí es "probablemente lo tienes, pero con
       nombre distinto" - no se asume automáticamente igual sin revisión.

Uso, solo informe (por defecto):
    python tools/scripts/check-collection-vs-1g1r.py \\
        --collection "F:\\roms\\console\\dreamcast" \\
        --pipeline-output private/retool-pipeline-test/dreamcast

Uso, organizando la colección en tres carpetas de salida (copia por defecto,
--copy-mode move/symlink/hardlink como alternativa; solo mueve/copia los
matches EXACTOS salvo que se pase --include-fuzzy):
    python tools/scripts/check-collection-vs-1g1r.py \\
        --collection "F:\\roms\\console\\dreamcast" \\
        --pipeline-output private/retool-pipeline-test/dreamcast \\
        --output-fullset "F:\\organizado\\dreamcast\\fullset" \\
        --output-1g1r "F:\\organizado\\dreamcast\\1g1r" \\
        --output-japan "F:\\organizado\\dreamcast\\japan" \\
        --copy-mode hardlink

`--pipeline-output` asume la estructura que deja `retool-1g1r-pipeline.py`
(step1/ = FULLSET, step4/ = FINAL + "Removed titles" = cuarentena). Para
usar DAT de otro origen, pasar --fullset-dat/--final-dat/--quarantine-dat
directamente en vez de --pipeline-output.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import sys
from pathlib import Path
from xml.etree import ElementTree as ET

PAREN_RE = re.compile(r"\(([^()]*)\)")
NORMALIZE_RE = re.compile(r"[\s\-~_.,!']+")
DISC_TAG_RE = re.compile(r"(?i)^(disc|disk|cd|side)\s*\S+$")


def names_of(dat_path: Path) -> set[str]:
    root = ET.parse(dat_path).getroot()
    return {g.get("name") for g in root.findall("game") if g.get("name")}


def normalized_key(name: str) -> str:
    """Título base + primer grupo entre paréntesis (asumido región) +
    cualquier tag de disco/lado (`Disc N`/`Disk N`/`CD N`/`Side N`, buscado
    en el resto de grupos) — el resto de tags (idioma/revisión/rerelease...)
    se ignora. El tag de disco se mantiene aparte para no confundir
    "mismo juego, disco distinto" con "mismo juego, nombre renombrado" (bug
    real detectado en `dreamcast`: sin esto, los 3 discos de un juego
    multi-disco colapsaban sobre la misma clave). Case-insensitive,
    guiones/espacios/puntuación colapsados."""
    base = name.split("(", 1)[0]
    groups = PAREN_RE.findall(name)
    region = groups[0] if groups else ""
    disc_tag = next((g for g in groups[1:] if DISC_TAG_RE.match(g.strip())), "")
    key = f"{base} {region} {disc_tag}".lower()
    return NORMALIZE_RE.sub(" ", key).strip()


def find_step_dat(step_dir: Path, exclude_removed: bool = True) -> Path:
    dats = sorted(step_dir.glob("*.dat"))
    if exclude_removed:
        dats = [d for d in dats if "Removed titles" not in d.name]
    if not dats:
        raise FileNotFoundError(f"Ningun .dat en {step_dir}")
    return dats[0]


def find_removed_dat(step_dir: Path) -> Path:
    dats = [d for d in step_dir.glob("*.dat") if "Removed titles" in d.name]
    if not dats:
        raise FileNotFoundError(f"Ningun DAT 'Removed titles' en {step_dir}")
    return dats[0]


def compare(collection_names: set[str], dat_names: set[str]) -> dict:
    exact = collection_names & dat_names
    dat_norm = {normalized_key(n): n for n in dat_names}
    fuzzy_only = {}
    for cname in collection_names - exact:
        key = normalized_key(cname)
        if key in dat_norm and dat_norm[key] not in exact:
            fuzzy_only[cname] = dat_norm[key]
    missing = dat_names - exact - set(fuzzy_only.values())
    extra = collection_names - exact - set(fuzzy_only.keys())
    return {
        "total_dat": len(dat_names),
        "exact_matches": sorted(exact),
        "fuzzy_matches": fuzzy_only,  # {nombre_fichero: nombre_dat}
        "missing": sorted(missing),
        "extra": sorted(extra),  # ficheros de la colección que no encajan en este DAT
    }


def classify_extra(extra_names: list[str], raw_dat_names: set[str] | None) -> dict:
    """De los ficheros "extra" de una capa (no encajan ahí), separa los que
    SÍ están en el DAT Redump/No-Intro sin filtrar (`--raw-dat`) — es decir,
    títulos reales que el paso 1 excluyó a propósito (demo/proto/aftermarket/
    unlicensed/...) — de los que no aparecen en absoluto en el catálogo
    conocido (fichero desconocido/mal nombrado/de otra fuente)."""
    if raw_dat_names is None:
        return {"excluded": None, "unknown": None}
    raw_norm = {normalized_key(n) for n in raw_dat_names}
    excluded, unknown = [], []
    for name in extra_names:
        if name in raw_dat_names or normalized_key(name) in raw_norm:
            excluded.append(name)
        else:
            unknown.append(name)
    return {"excluded": sorted(excluded), "unknown": sorted(unknown)}


def report_tier(label: str, result: dict, raw_dat_names: set[str] | None = None) -> None:
    print(f"\n== {label} ({result['total_dat']} títulos) ==")
    print(f"  Coincidencia exacta:      {len(result['exact_matches'])}")
    print(f"  Coincidencia normalizada (revisar nombre): {len(result['fuzzy_matches'])}")
    print(f"  Sin coincidencia (falta): {len(result['missing'])}")
    print(f"  Sobran en la colección (no encajan en este DAT): {len(result['extra'])}")
    if result["fuzzy_matches"]:
        print("  -- Renombrados probables (fichero -> nombre DAT) --")
        for fname, dname in sorted(result["fuzzy_matches"].items()):
            print(f"     {fname}  ->  {dname}")
    if result["missing"]:
        print("  -- Faltan de verdad --")
        for n in result["missing"][:30]:
            print(f"     {n}")
        if len(result["missing"]) > 30:
            print(f"     ... y {len(result['missing']) - 30} más")
    if result["extra"]:
        classified = classify_extra(result["extra"], raw_dat_names)
        if raw_dat_names is None:
            print("  -- Sobran, sin clasificar (pasa --raw-dat para separar excluidos/desconocidos) --")
            for n in result["extra"][:30]:
                print(f"     {n}")
            if len(result["extra"]) > 30:
                print(f"     ... y {len(result['extra']) - 30} más")
        else:
            print(f"  -- Excluidos a propósito (están en el Redump/No-Intro sin filtrar, el paso 1 los sacó): {len(classified['excluded'])} --")
            for n in classified["excluded"][:30]:
                print(f"     {n}")
            if len(classified["excluded"]) > 30:
                print(f"     ... y {len(classified['excluded']) - 30} más")
            print(f"  -- Desconocidos (no están ni en el catálogo sin filtrar): {len(classified['unknown'])} --")
            for n in classified["unknown"][:30]:
                print(f"     {n}")
            if len(classified["unknown"]) > 30:
                print(f"     ... y {len(classified['unknown']) - 30} más")


def organize(
    collection_files: dict[str, Path],
    result: dict,
    output_dir: Path,
    copy_mode: str,
    include_fuzzy: bool,
) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    names_to_copy = list(result["exact_matches"])
    if include_fuzzy:
        names_to_copy += list(result["fuzzy_matches"].keys())
    for name in names_to_copy:
        src = collection_files[name]
        dst = output_dir / src.name
        if dst.exists():
            continue
        if copy_mode == "copy":
            shutil.copy2(src, dst)
        elif copy_mode == "move":
            shutil.move(str(src), str(dst))
        elif copy_mode == "symlink":
            dst.symlink_to(src.resolve())
        elif copy_mode == "hardlink":
            import os
            os.link(src, dst)
    print(f"  Organizados {len(names_to_copy)} ficheros en {output_dir} ({copy_mode})")


def build_excluded_report(result_fullset: dict, raw_dat_names: set[str] | None, collection_files: dict[str, Path]) -> list[dict]:
    """CSV de los ficheros "sobrantes" de FULLSET, clasificados vía
    `classify_extra` en excluidos a propósito (categoría filtrada por el
    paso 1: demo/proto/aftermarket/unlicensed/multimedia...) vs desconocidos
    de verdad (ni siquiera están en el Redump/No-Intro sin filtrar). Solo
    tiene sentido para la capa FULLSET (las demás capas tienen "extra" =
    variantes descartadas por el propio 1G1R, una categoría distinta, no
    "excluido por tipo")."""
    classified = classify_extra(result_fullset["extra"], raw_dat_names)
    rows = []
    for category, names in (("excluded", classified["excluded"] or []), ("unknown", classified["unknown"] or [])):
        for name in names:
            filename = collection_files[name].name if name in collection_files else f"{name} (nombre no resuelto)"
            rows.append({"category": category, "filename": filename})
    return rows


def write_excluded_report(rows: list[dict], report_path: Path) -> None:
    with report_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["category", "filename"])
        writer.writeheader()
        writer.writerows(rows)
    excluded_n = sum(1 for r in rows if r["category"] == "excluded")
    unknown_n = sum(1 for r in rows if r["category"] == "unknown")
    print(f"\nInforme de sobrantes ({excluded_n} excluidos, {unknown_n} desconocidos) escrito en: {report_path}")


def build_rename_plan(all_results: dict[str, dict], collection_files: dict[str, Path]) -> list[dict]:
    """De los matches "normalizados" (renombrado probable) de todas las
    capas ya comparadas, construye una lista de renombrados propuestos
    (fichero real -> nombre exacto que espera el DAT), deduplicada."""
    seen: dict[str, str] = {}  # current_filename -> proposed_filename
    rows = []
    for tier, result in all_results.items():
        for current_stem, dat_name in result["fuzzy_matches"].items():
            current_path = collection_files[current_stem]
            proposed_name = dat_name + current_path.suffix
            if current_path.name in seen and seen[current_path.name] != proposed_name:
                # Mismo fichero, propuestas distintas segun la capa (raro,
                # pero posible si dos DAT distintos normalizan igual) -
                # se deja constancia de ambas para revision manual, no se
                # elige una a ciegas.
                rows.append({
                    "tier": tier, "current_filename": current_path.name,
                    "proposed_filename": proposed_name,
                    "note": "CONFLICTO: propuesta distinta ya vista en otra capa, revisar a mano",
                })
                continue
            if current_path.name in seen:
                continue
            seen[current_path.name] = proposed_name
            rows.append({
                "tier": tier, "current_filename": current_path.name,
                "proposed_filename": proposed_name, "note": "",
            })
    return rows


def build_missing_report(all_results: dict[str, dict], ext: str | None) -> list[dict]:
    """Lista de "compra pendiente" por capa: títulos que ni siquiera tienen
    match normalizado, deduplicada por (tier, título) — un mismo título
    puede aparecer en más de una capa (ej. falta en FULLSET implica que
    también falta en 1G1R FINAL/cuarentena) y se listan todas las capas
    donde falta, no solo la primera."""
    rows = []
    for tier, result in all_results.items():
        for name in result["missing"]:
            expected_filename = f"{name}.{ext.lstrip('.')}" if ext else name
            rows.append({"tier": tier, "title": name, "expected_filename": expected_filename})
    return rows


def write_missing_report(rows: list[dict], report_path: Path) -> None:
    with report_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["tier", "title", "expected_filename"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nInforme de faltantes ({len(rows)} filas, puede repetir título entre capas) escrito en: {report_path}")


def write_rename_plan(rows: list[dict], plan_path: Path) -> None:
    with plan_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["tier", "current_filename", "proposed_filename", "note"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"\nPlan de renombrado ({len(rows)} filas) escrito en: {plan_path}")
    print("Revisa el CSV (sobre todo filas con 'note' no vacío) antes de aplicarlo con --apply-renames.")


def apply_rename_plan(plan_path: Path, collection: Path) -> None:
    with plan_path.open(encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    applied, skipped = 0, 0
    for row in rows:
        if row.get("note"):
            print(f"  SALTADO (tiene nota, revisar a mano): {row['current_filename']}")
            skipped += 1
            continue
        src = collection / row["current_filename"]
        dst = collection / row["proposed_filename"]
        if not src.is_file():
            print(f"  SALTADO (ya no existe): {row['current_filename']}")
            skipped += 1
            continue
        if dst.exists():
            print(f"  SALTADO (destino ya existe): {row['proposed_filename']}")
            skipped += 1
            continue
        src.rename(dst)
        applied += 1
    print(f"\nRenombrados aplicados: {applied}. Saltados: {skipped}.")


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass  # Python <3.7 o stream sin reconfigure; se queda con el encoding por defecto

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--collection", required=True, type=Path, help="Carpeta con la colección real (ROMs/discos)")
    parser.add_argument("--raw-dat", type=Path, default=None, help="DAT Redump/No-Intro SIN filtrar (antes del paso 1 de retool) — permite distinguir, entre los ficheros que sobran en FULLSET, los excluidos a propósito (demo/proto/aftermarket/unlicensed...) de los realmente desconocidos")
    parser.add_argument("--ext", default=None, help="Filtrar por extensión (ej. chd); por defecto usa todos los ficheros de la carpeta")
    parser.add_argument("--pipeline-output", type=Path, default=None, help="Carpeta de salida de retool-1g1r-pipeline.py (usa step1/ y step4/ automáticamente)")
    parser.add_argument("--fullset-dat", type=Path, default=None, help="DAT FULLSET explícito (alternativa a --pipeline-output)")
    parser.add_argument("--final-dat", type=Path, default=None, help="DAT FINAL 1G1R explícito")
    parser.add_argument("--quarantine-dat", type=Path, default=None, help="DAT de cuarentena explícito (opcional)")
    parser.add_argument("--output-fullset", type=Path, default=None, help="Si se indica, organiza los matches de FULLSET aquí")
    parser.add_argument("--output-1g1r", type=Path, default=None, help="Si se indica, organiza los matches de FINAL 1G1R aquí")
    parser.add_argument("--output-japan", type=Path, default=None, help="Si se indica, organiza los matches de cuarentena aquí")
    parser.add_argument("--copy-mode", choices=["copy", "move", "symlink", "hardlink"], default="copy")
    parser.add_argument("--include-fuzzy", action="store_true", help="Al organizar, incluir también los matches normalizados (renombrados probables), no solo los exactos")
    parser.add_argument("--json", type=Path, default=None, help="Volcar el informe completo también como JSON en esta ruta")
    parser.add_argument("--rename-plan", type=Path, default=None, help="Escribe un CSV (tier,current_filename,proposed_filename,note) con los renombrados propuestos a partir de los matches normalizados de todas las capas comparadas — no renombra nada todavía, es para revisar antes de aplicar")
    parser.add_argument("--missing-report", type=Path, default=None, help="Escribe un CSV (tier,title,expected_filename) con los títulos que faltan de verdad en cada capa comparada — lista de compra pendiente, usa --ext para que expected_filename incluya la extensión")
    parser.add_argument("--excluded-report", type=Path, default=None, help="Escribe un CSV (category,filename) con los ficheros que sobran en FULLSET, clasificados en 'excluded' (categoría filtrada a propósito por el paso 1) y 'unknown' (ni siquiera están en el catálogo sin filtrar) — requiere --raw-dat, si no se pasa el CSV sale vacío")
    parser.add_argument("--apply-renames", type=Path, default=None, help="Aplica un CSV ya generado (y revisado) por --rename-plan: renombra los ficheros en --collection. No hace comparación, solo renombra")
    args = parser.parse_args()

    if args.apply_renames:
        apply_rename_plan(args.apply_renames, args.collection)
        return

    if args.pipeline_output:
        fullset_dat = find_step_dat(args.pipeline_output / "step1")
        step4 = args.pipeline_output / "step4"
        final_dat = find_step_dat(step4)
        try:
            quarantine_dat = find_removed_dat(step4)
        except FileNotFoundError:
            quarantine_dat = None
    else:
        fullset_dat = args.fullset_dat
        final_dat = args.final_dat
        quarantine_dat = args.quarantine_dat

    if not fullset_dat or not fullset_dat.is_file():
        sys.exit("Falta --pipeline-output o --fullset-dat (fichero no encontrado)")

    collection_files = {}
    for f in args.collection.iterdir():
        if not f.is_file():
            continue
        if args.ext and f.suffix.lower().lstrip(".") != args.ext.lower().lstrip("."):
            continue
        collection_files[f.stem] = f
    collection_names = set(collection_files.keys())

    print(f"Colección: {len(collection_names)} ficheros en {args.collection}")

    raw_dat_names = names_of(args.raw_dat) if args.raw_dat else None

    fullset_names = names_of(fullset_dat)
    result_fullset = compare(collection_names, fullset_names)
    report_tier(f"FULLSET ({fullset_dat.name})", result_fullset, raw_dat_names)

    results = {"fullset": result_fullset}

    if final_dat and final_dat.is_file():
        final_names = names_of(final_dat)
        result_final = compare(collection_names, final_names)
        report_tier(f"1G1R FINAL ({final_dat.name})", result_final)
        results["1g1r"] = result_final

        if args.output_1g1r:
            organize(collection_files, result_final, args.output_1g1r, args.copy_mode, args.include_fuzzy)

    if quarantine_dat and quarantine_dat.is_file():
        quarantine_names = names_of(quarantine_dat)
        result_quarantine = compare(collection_names, quarantine_names)
        report_tier(f"Cuarentena / Japan ({quarantine_dat.name})", result_quarantine)
        results["japan"] = result_quarantine

        if args.output_japan:
            organize(collection_files, result_quarantine, args.output_japan, args.copy_mode, args.include_fuzzy)

    if args.output_fullset:
        organize(collection_files, result_fullset, args.output_fullset, args.copy_mode, args.include_fuzzy)

    if args.rename_plan:
        rows = build_rename_plan(results, collection_files)
        write_rename_plan(rows, args.rename_plan)

    if args.missing_report:
        rows = build_missing_report(results, args.ext)
        write_missing_report(rows, args.missing_report)

    if args.excluded_report:
        if raw_dat_names is None:
            print("\nAviso: --excluded-report sin --raw-dat no puede clasificar nada; escribiendo CSV vacío.")
        rows = build_excluded_report(result_fullset, raw_dat_names, collection_files)
        write_excluded_report(rows, args.excluded_report)

    if args.json:
        args.json.write_text(json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nInforme completo en: {args.json}")


if __name__ == "__main__":
    main()
