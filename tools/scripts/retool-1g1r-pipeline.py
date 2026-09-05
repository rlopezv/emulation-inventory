#!/usr/bin/env python3
"""
Pipeline de 4 pasadas de Retool (ver docs/guides/tools/1g1r-filtering.md,
seccion "Pipeline recomendado") para llegar a un 1G1R final mas una
cuarentena de idioma, a partir de un DAT Parent-Clone oficial (ej. el pack
`pc/` de DAT-o-MATIC, ya en sources/no-intro/).

Solo Python (sin equivalente .ps1): Retool no tiene binario para Windows
nativo, requiere el devcontainer (imagen `emulation-devcontainer`, ver
.devcontainer/Dockerfile) - mismo motivo que compare-redump-mameredump.py
es Python-only.

Pasos (cada uno reprocesa la salida del anterior via --reprocess):
    1. FULLSET       -d --exclude <codigos>              (solo catalogo oficial)
    2. 1G1R-BASE     --compilations k                     (1G1R por region)
    3. INTERMEDIATE  -l <idiomas finales + cuarentena>     (superconjunto)
    4. FINAL+CUARENTENA -l <solo idiomas finales> --removesdat

El DAT de entrada NO se modifica ni se le inyecta region/language: Retool
deriva ambos del propio nombre del titulo (ver modules/dat/process_dat.py
del propio retool) - no hace falta (ni sirve de nada) un conversor propio
mas alla de lo que ya provee el pack Parent-Clone oficial.

Uso:
    python tools/scripts/retool-1g1r-pipeline.py \\
        --dat "sources/no-intro/Sega - Mega Drive - Genesis (Parent-Clone) (20260810-205824).dat" \\
        --output private/megadrive-1g1r \\
        --keep-languages "English,Spanish,Spanish (Latin American),Spanish (Mexican)" \\
        --quarantine-languages "Japanese"

Requisitos: Docker Desktop corriendo y la imagen `emulation-devcontainer`
ya construida (`docker build -t emulation-devcontainer .devcontainer/`).
La primera vez que se usa un --retool-config-dir nuevo, Retool necesita
red para bootstrapear config/internal-config.json (unica descarga; el
clonelist/metadata NO se descarga si --clonelist-dir ya los trae, ver
--clonelist-dir).
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DEFAULT_IMAGE = "emulation-devcontainer:latest"
DEFAULT_CLONELIST_DIR = REPO_ROOT / "sources" / "retool-clonelists-metadata" / "input"
DEFAULT_EXCLUDE = "aAbBcDdefmMopPruv"  # todo lo no-oficial: ver tabla en 1g1r-filtering.md
DEFAULT_COMPILATIONS = "k"

# Lista cerrada de nombres de idioma tal como los espera Retool en
# `language order:` (config/user-config.yaml) - copiada de la plantilla que
# el propio Retool genera en el primer arranque. Si Retool actualiza esta
# lista en una version futura, el bootstrap (paso 0) la vuelve a generar y
# esta lista puede quedar desfasada - no es una fuente de verdad propia,
# solo un espejo para poder reescribir el bloque sin depender del orden.
KNOWN_LANGUAGE_ORDER = [
    "English", "Afrikaans", "Albanian", "Arabic", "Basque", "Bulgarian",
    "Catalan", "Chinese (Simplified)", "Chinese (Traditional)", "Cornish",
    "Croatian", "Czech", "Danish", "Dutch", "Estonian", "Finnish", "French",
    "French (Canadian)", "Gaelic", "German", "Greek", "Hebrew", "Hindi",
    "Hungarian", "Icelandic", "Indonesian", "Italian", "Japanese", "Korean",
    "Latin", "Latvian", "Lithuanian", "Norwegian", "Polish", "Portuguese",
    "Portuguese (Brazilian)", "Romanian", "Russian", "Serbian", "Slovak",
    "Slovenian", "Spanish", "Spanish (Latin American)", "Spanish (Mexican)",
    "Swedish", "Tamil", "Thai", "Turkish", "Ukrainian", "Vietnamese",
]


def run_docker(
    image: str,
    dat_mount: tuple[Path, str] | None,
    input_dir: Path | None,
    output_dir: Path,
    config_dir: Path,
    clonelist_dir: Path,
    workdir: str,
    retool_args: list[str],
) -> None:
    """Lanza `docker run --rm` con los montajes estandar y ejecuta retool."""
    cmd = ["docker", "run", "--rm", "-i"]

    if dat_mount is not None:
        host_path, container_path = dat_mount
        cmd += ["-v", f"{host_path}:{container_path}:ro"]
    if input_dir is not None:
        cmd += ["-v", f"{input_dir}:/work-in:ro"]

    cmd += [
        "-v", f"{output_dir}:/work-out",
        "-v", f"{config_dir}:/opt/retool/config",
        "-v", f"{clonelist_dir / 'clonelists'}:/opt/retool/clonelists:ro",
        "-v", f"{clonelist_dir / 'metadata'}:/opt/retool/metadata:ro",
        "-v", f"{clonelist_dir / 'mias'}:/opt/retool/mias:ro",
        "-v", f"{clonelist_dir / 'retroachievements'}:/opt/retool/retroachievements:ro",
        image,
        "sh", "-c",
        f"cd {workdir} && retool " + " ".join(retool_args),
    ]

    print(f"\n$ {' '.join(cmd)}\n", file=sys.stderr)
    subprocess.run(cmd, input=b"y\n", check=True)


def latest_dat(folder: Path) -> Path | None:
    dats = sorted(folder.glob("*.dat"))
    if not dats:
        return None
    if len(dats) > 1:
        # --removesdat/--report generan mas de un fichero; el DAT principal
        # (no "Removed titles") es siempre el que hay que encadenar.
        dats = [d for d in dats if "Removed titles" not in d.name]
    return dats[0]


def run_retool_step(
    image: str,
    dat_mount: tuple[Path, str] | None,
    input_dir: Path | None,
    output_dir: Path,
    config_dir: Path,
    clonelist_dir: Path,
    workdir: str,
    retool_args: list[str],
    step_output_dir: Path,
) -> Path:
    """Ejecuta un paso de Retool y devuelve el DAT resultante.

    En un config_dir recien creado, la PRIMERA invocacion de Retool en toda
    su vida solo hace bootstrap de config/internal-config.json y
    config/user-config.yaml (confirmado empiricamente): no procesa el DAT
    todavia, aunque se le pida. Por eso se reintenta una vez mas si no
    aparece ningun .dat de salida - la segunda invocacion, con la config ya
    en disco, si procesa. Pasadas ejecuciones futuras con el mismo
    --retool-config-dir no pagan este coste, solo la primera vez jamas."""
    for attempt in (1, 2):
        run_docker(image, dat_mount, input_dir, output_dir, config_dir, clonelist_dir, workdir, retool_args)
        result = latest_dat(step_output_dir)
        if result is not None:
            return result
        if attempt == 1:
            print("(bootstrap de config/ en la primera invocacion - reintentando)", file=sys.stderr)
    raise RuntimeError(f"Retool no genero ningun .dat en {step_output_dir} tras 2 intentos")


def write_language_config(config_dir: Path, keep_languages: set[str]) -> None:
    """Reescribe el bloque `language order:` de user-config.yaml, dejando
    descomentados unicamente los idiomas en keep_languages. No toca el
    resto del fichero (region order, compilations, excludes...)."""
    config_path = config_dir / "user-config.yaml"
    lines = config_path.read_text(encoding="utf-8").splitlines()

    start = next(i for i, l in enumerate(lines) if l.strip() == "language order:")
    end = next(i for i in range(start + 1, len(lines)) if lines[i].strip() == "" or lines[i].startswith("# ==="))

    new_block = []
    for lang in KNOWN_LANGUAGE_ORDER:
        prefix = "- " if lang in keep_languages else "# - "
        new_block.append(f"{prefix}{lang}")

    lines[start + 1:end] = new_block
    config_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--dat", required=True, type=Path, help="DAT Parent-Clone oficial de entrada (sin modificar)")
    parser.add_argument("--output", required=True, type=Path, help="Carpeta donde crear step1/../step4")
    parser.add_argument("--keep-languages", required=True, help="Idiomas finales separados por coma (nombres tal como los usa Retool, ej. 'English,Spanish')")
    parser.add_argument("--quarantine-languages", default="", help="Idiomas a cuarentenar por separado (coma); vacio = sin cuarentena, el resultado de la pasada 2 ya es el final")
    parser.add_argument("--exclude", default=DEFAULT_EXCLUDE, help=f"Codigos --exclude para la fase 1 (por defecto: {DEFAULT_EXCLUDE}, todo lo no-oficial)")
    parser.add_argument("--compilations", default=DEFAULT_COMPILATIONS, choices=["i", "k", "o"], help="Modo --compilations para la fase 2 (por defecto: k)")
    parser.add_argument("--image", default=DEFAULT_IMAGE, help="Imagen Docker con Retool instalado")
    parser.add_argument("--clonelist-dir", default=DEFAULT_CLONELIST_DIR, type=Path, help="Carpeta con clonelists/metadata/mias/retroachievements de retool-clonelists-metadata (input/ = clon git completo, recomendado)")
    parser.add_argument("--retool-config-dir", type=Path, default=None, help="Carpeta persistente para config/ de Retool (por defecto: <output>/_retool-config, se reutiliza entre pasadas de esta ejecucion; pasar la misma ruta en ejecuciones futuras evita el bootstrap de red repetido)")
    args = parser.parse_args()

    dat_path = args.dat.resolve()
    output_dir = args.output.resolve()
    clonelist_dir = args.clonelist_dir.resolve()
    config_dir = (args.retool_config_dir or (output_dir / "_retool-config")).resolve()

    if not dat_path.is_file():
        sys.exit(f"No existe el DAT de entrada: {dat_path}")
    for sub in ("clonelists", "metadata", "mias", "retroachievements"):
        if not (clonelist_dir / sub).is_dir():
            sys.exit(f"Falta {clonelist_dir / sub} - pasa --clonelist-dir a una copia con esa estructura (ver sources/retool-clonelists-metadata/input/)")

    keep = {s.strip() for s in args.keep_languages.split(",") if s.strip()}
    quarantine = {s.strip() for s in args.quarantine_languages.split(",") if s.strip()}
    unknown = (keep | quarantine) - set(KNOWN_LANGUAGE_ORDER)
    if unknown:
        sys.exit(f"Idioma(s) no reconocido(s) por KNOWN_LANGUAGE_ORDER: {sorted(unknown)} - revisar nombre exacto en config/user-config.yaml de un Retool ya arrancado")

    output_dir.mkdir(parents=True, exist_ok=True)
    config_dir.mkdir(parents=True, exist_ok=True)

    step1_dir = output_dir / "step1"
    step2_dir = output_dir / "step2"
    step3_dir = output_dir / "step3"
    step4_dir = output_dir / "step4"

    # --- Paso 1: FULLSET (solo catalogo oficial) ---
    print("== Paso 1/4: FULLSET (excluyendo no-oficial) ==", file=sys.stderr)
    fullset_dat = run_retool_step(
        args.image, (dat_path, f"/dat-in/{dat_path.name}"), None, output_dir, config_dir, clonelist_dir,
        workdir="/work-out",
        retool_args=["-d", "--exclude", args.exclude, "--output", "/work-out/step1", f'"/dat-in/{dat_path.name}"'],
        step_output_dir=step1_dir,
    )

    # --- Paso 2: 1G1R-BASE (region + compilaciones, sin idioma) ---
    print("== Paso 2/4: 1G1R-BASE (region + compilaciones) ==", file=sys.stderr)
    base_dat = run_retool_step(
        args.image, None, step1_dir, output_dir, config_dir, clonelist_dir,
        workdir="/work-in",
        retool_args=["--reprocess", "--compilations", args.compilations, "--output", "/work-out/step2", f'"{fullset_dat.name}"'],
        step_output_dir=step2_dir,
    )

    if not quarantine:
        # Sin cuarentena: recorte de idioma directo (si se pidio alguno) y fin.
        if keep:
            print("== Paso 3/3: recorte de idioma final (sin cuarentena) ==", file=sys.stderr)
            write_language_config(config_dir, keep)
            final_dat = run_retool_step(
                args.image, None, step2_dir, output_dir, config_dir, clonelist_dir,
                workdir="/work-in",
                retool_args=["--reprocess", "-l", "--output", "/work-out/step4", f'"{base_dat.name}"'],
                step_output_dir=step4_dir,
            )
            print(f"\nListo. 1G1R final en: {final_dat}", file=sys.stderr)
        else:
            print(f"\nListo. 1G1R final (sin filtro de idioma) en: {base_dat}", file=sys.stderr)
        return

    # --- Paso 3: INTERMEDIATE (superconjunto: keep + quarantine) ---
    print("== Paso 3/4: INTERMEDIATE (idiomas finales + cuarentena) ==", file=sys.stderr)
    write_language_config(config_dir, keep | quarantine)
    intermediate_dat = run_retool_step(
        args.image, None, step2_dir, output_dir, config_dir, clonelist_dir,
        workdir="/work-in",
        retool_args=["--reprocess", "-l", "--output", "/work-out/step3", f'"{base_dat.name}"'],
        step_output_dir=step3_dir,
    )

    # --- Paso 4: FINAL + CUARENTENA (solo keep, --removesdat) ---
    print("== Paso 4/4: FINAL + cuarentena (--removesdat) ==", file=sys.stderr)
    write_language_config(config_dir, keep)
    run_docker(
        args.image, None, step3_dir, output_dir, config_dir, clonelist_dir,
        workdir="/work-in",
        retool_args=["--reprocess", "-l", "--removesdat", "--output", "/work-out/step4", f'"{intermediate_dat.name}"'],
    )

    final_dats = sorted(step4_dir.glob("*.dat"))
    final = next(d for d in final_dats if "Removed titles" not in d.name)
    removed = next(d for d in final_dats if "Removed titles" in d.name)
    print(f"\nListo.\n  1G1R final:  {final}\n  Cuarentena:  {removed}", file=sys.stderr)


if __name__ == "__main__":
    main()
