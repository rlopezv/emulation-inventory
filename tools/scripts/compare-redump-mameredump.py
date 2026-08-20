#!/usr/bin/env python3
"""
Compara, sistema a sistema, el DAT oficial de Redump (metadata/dat/Redump/,
esquema Logiqx <game name="..."><rom .../></game>, sin cloneofid) contra el
DAT equivalente de metadata/dat/MAMERedump/full/ (esquema estilo MAME,
<machine name="..."><disk name="....chd" sha1="..."/></machine>, con el SHA1
real del CHD -- ver github.com/MetalSlug/MAMERedump y la entrada
correspondiente en docs/session-context.md).

Objetivo: detectar discrepancias de COBERTURA (titulos presentes en una
fuente y ausentes en la otra) entre el CUE/BIN oficial de Redump y el CHD
publicado por MAMERedump para el mismo catalogo. No compara hashes byte a
byte (no son comparables: Redump da SHA1 de pistas .cue/.bin, MAMERedump da
SHA1 del .chd ya comprimido/convertido) -- la comparacion es por el nombre
completo del titulo (`name`/`description`), que ambas fuentes mantienen con
la misma convencion de nombrado de Redump.

Sistemas cubiertos: los que en docs/romsets.md tienen Fuente=Redump Y tienen
DAT equivalente en MAMERedump/full/, listados en
config/redump-mameredump-systems.json ('xbox' queda fuera a proposito: Redump
lo cubre pero MAMERedump no publica CHD para el).

Salida: por sistema, metadata/dat-index/debug/<id>-redump-mameredump-diff.json
con las dos listas (solo en Redump / solo en MAMERedump), mas un resumen por
consola. No modifica ningun DAT ni bloquea nada -- es puramente informativo,
mismo patron que el informe de contraste pc/ de build-dat-index-nointro.py.

Uso:
    python tools/scripts/compare-redump-mameredump.py
    python tools/scripts/compare-redump-mameredump.py --system-id psx
"""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent

MANIFEST_PATH = SCRIPT_DIR / "config" / "redump-mameredump-systems.json"
REDUMP_ROOT = REPO_ROOT / "metadata" / "dat" / "Redump"
MAMEREDUMP_ROOT = REPO_ROOT / "metadata" / "dat" / "MAMERedump" / "full"
DEBUG_ROOT = REPO_ROOT / "metadata" / "dat-index" / "debug"

# Redump: "<base> - Datfile (<count>) (<fecha-hora>).dat"
REDUMP_SUFFIX = r" - Datfile \(\d+\) \([^)]+\)\.dat$"
# MAMERedump: "<base> (<count>).dat"
MAMEREDUMP_SUFFIX = r" \(\d+\)\.dat$"


def find_dat(folder: Path, base_name: str, suffix_pattern: str) -> Path | None:
    if not folder.is_dir():
        return None
    pattern = re.compile(rf"^{re.escape(base_name)}{suffix_pattern}")
    candidates = sorted(
        (p for p in folder.iterdir() if p.is_file() and pattern.match(p.name)),
        key=lambda p: p.name,
        reverse=True,
    )
    return candidates[0] if candidates else None


def get_redump_titles(path: Path) -> set[str]:
    tree = ET.parse(path)
    return {game.get("name", "") for game in tree.getroot().findall("game") if game.get("name")}


DEMO_SYNONYMS = re.compile(r"\((?:Otameshi-ban|Taikenban|Otameshiban)\)", re.IGNORECASE)
PAREN_COMMA_LIST = re.compile(r"\(([^()]*,[^()]*)\)")

# Tags de prelanzamiento/prueba (con o sin fecha entre parentesis pegada,
# ej. "(Beta) (1996-11-02)") -- MAMERedump parece catalogar solo volcados
# comerciales finales (+ Unl/Pirata/Aftermarket), no cada build de prueba
# que si recoge Redump. Mismo patron que discardTags de build-dat-index-*.
PRERELEASE_TAGS = re.compile(
    r"\((?:Beta|Proto|Prototype|Demo|Sample|Alpha|Preview|Trial|Kiosk)\b[^)]*\)",
    re.IGNORECASE,
)


def is_prerelease(name: str) -> bool:
    return bool(PRERELEASE_TAGS.search(name))


def loose_key(name: str) -> str:
    """Clave laxa para filtrar ruido de convencion de nombrado entre Redump y
    MAMERedump (mismo disco, nombre reescrito): unifica sinonimos de 'demo'
    japones->ingles, colapsa listas separadas por coma dentro de un mismo
    parentesis (region secundaria, idiomas) a su primer elemento, quita
    guiones (romanizacion distinta de titulos japoneses, ej. 'Yuushatachi'
    vs 'Yuusha-tachi') y normaliza espacios/mayusculas. Es una heuristica
    para revision VISUAL de patrones, no una prueba de que dos discos sean
    el mismo -- confirmar a mano antes de dar una divergencia por resuelta.
    """
    key = DEMO_SYNONYMS.sub("(Demo)", name)
    key = PAREN_COMMA_LIST.sub(lambda m: f"({m.group(1).split(',')[0].strip()})", key)
    key = key.replace("-", "")
    key = re.sub(r"\s+", " ", key).strip().lower()
    return key


def get_mameredump_titles(path: Path) -> set[str]:
    # La mayoria de DAT de MAMERedump/full/ usan <machine>/<disk .chd> (esquema
    # MAME), pero los sistemas que no usan CHD como formato de destino (ej.
    # GameCube/Wii, que usan .rvz de Dolphin) vienen en <game>/<rom> estandar
    # Logiqx -- se comprueba cual de los dos esquemas trae el fichero.
    root = ET.parse(path).getroot()
    machines = root.findall("machine")
    if machines:
        return {m.get("name", "") for m in machines if m.get("name")}
    return {g.get("name", "") for g in root.findall("game") if g.get("name")}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--system-id", dest="system_id", default=None)
    args = parser.parse_args()

    manifest: dict[str, str] = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["systems"]
    ids = [args.system_id] if args.system_id else list(manifest.keys())

    DEBUG_ROOT.mkdir(parents=True, exist_ok=True)
    summary: list[tuple[str, int, int, int, int]] = []

    for system_id in ids:
        if system_id not in manifest:
            print(f"ADVERTENCIA: Sistema no encontrado en el manifiesto: {system_id}")
            continue
        base_name = manifest[system_id]

        redump_path = find_dat(REDUMP_ROOT, base_name, REDUMP_SUFFIX)
        mameredump_path = find_dat(MAMEREDUMP_ROOT, base_name, MAMEREDUMP_SUFFIX)

        if not redump_path:
            print(f"ADVERTENCIA: {system_id}: sin DAT Redump encontrado para '{base_name}'")
            continue
        if not mameredump_path:
            print(f"ADVERTENCIA: {system_id}: sin DAT MAMERedump encontrado para '{base_name}'")
            continue

        redump_titles = get_redump_titles(redump_path)
        mameredump_titles = get_mameredump_titles(mameredump_path)

        only_redump = sorted(redump_titles - mameredump_titles)
        only_mameredump = sorted(mameredump_titles - redump_titles)

        # Segunda pasada: clave laxa, para separar ruido de convencion de
        # nombrado de divergencias que parecen reales de verdad.
        mameredump_loose = {loose_key(t) for t in mameredump_titles}
        redump_loose = {loose_key(t) for t in redump_titles}
        only_redump_real = sorted(t for t in only_redump if loose_key(t) not in mameredump_loose)
        only_mameredump_real = sorted(t for t in only_mameredump if loose_key(t) not in redump_loose)

        # Tercera pasada: de lo que sigue divergiendo tras la clave laxa,
        # separar prelanzamientos (Beta/Proto/Demo/...) del resto -- la
        # hipotesis es que MAMERedump no cataloga prelanzamientos en absoluto.
        only_redump_commercial = [t for t in only_redump_real if not is_prerelease(t)]
        only_redump_prerelease = [t for t in only_redump_real if is_prerelease(t)]
        only_mameredump_commercial = [t for t in only_mameredump_real if not is_prerelease(t)]
        only_mameredump_prerelease = [t for t in only_mameredump_real if is_prerelease(t)]

        output = {
            "system": system_id,
            "redump": redump_path.name,
            "mameRedump": mameredump_path.name,
            "redumpCount": len(redump_titles),
            "mameRedumpCount": len(mameredump_titles),
            "onlyInRedump": only_redump,
            "onlyInMameRedump": only_mameredump,
            "onlyInRedumpAfterLooseMatch": only_redump_real,
            "onlyInMameRedumpAfterLooseMatch": only_mameredump_real,
            "onlyInRedumpCommercialOnly": only_redump_commercial,
            "onlyInRedumpPrerelease": only_redump_prerelease,
            "onlyInMameRedumpCommercialOnly": only_mameredump_commercial,
            "onlyInMameRedumpPrerelease": only_mameredump_prerelease,
        }
        out_path = DEBUG_ROOT / f"{system_id}-redump-mameredump-diff.json"
        out_path.write_text(json.dumps(output, ensure_ascii=False, indent=2), encoding="utf-8")

        summary.append((
            system_id, len(redump_titles), len(mameredump_titles),
            len(only_redump), len(only_mameredump),
            len(only_redump_real), len(only_mameredump_real),
            len(only_redump_commercial), len(only_mameredump_commercial),
        ))
        print(
            f"{system_id}: Redump={len(redump_titles)} MAMERedump={len(mameredump_titles)} "
            f"| exacto R={len(only_redump)} M={len(only_mameredump)} "
            f"| laxo R={len(only_redump_real)} M={len(only_mameredump_real)} "
            f"| solo comercial R={len(only_redump_commercial)} M={len(only_mameredump_commercial)} "
            f"-> {out_path.relative_to(REPO_ROOT)}"
        )

    if summary:
        print("\n=== RESUMEN ===")
        header = (
            f"{'Sistema':15} {'Redump':>8} {'MAME':>6} "
            f"{'ExactoR':>8} {'ExactoM':>8} {'LaxoR':>7} {'LaxoM':>7} {'ComR':>6} {'ComM':>6}"
        )
        print(header)
        for system_id, r, m, only_r, only_m, real_r, real_m, com_r, com_m in summary:
            print(f"{system_id:15} {r:>8} {m:>6} {only_r:>8} {only_m:>8} {real_r:>7} {real_m:>7} {com_r:>6} {com_m:>6}")


if __name__ == "__main__":
    main()
