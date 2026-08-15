#!/usr/bin/env python3
"""
Equivalente Python de update-sources.ps1 (pensado para ejecutarse desde el
devcontainer). Misma logica, mismo manifiesto (config/nointro-systems.json),
misma salida esperada; ver la cabecera de update-sources.ps1 para la
descripcion completa del proposito y el patron de nombres de fichero.

Uso:
    python tools/scripts/update-sources.py
    python tools/scripts/update-sources.py --system-id nes
"""

import argparse
import json
import re
import shutil
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent

MANIFEST_PATH = SCRIPT_DIR / "config" / "nointro-systems.json"
RAW_ROOT = REPO_ROOT / "metadata" / "dat" / "No-Intro"
DEST_ROOT = REPO_ROOT / "sources" / "dats" / "no-intro"

# pack -> tag insertado en el nombre de fichero (o None si no lleva tag)
PACKS = {
    "pc": "Parent-Clone",
    "full": None,
    "aftermarket": "Aftermarket",
}

TIMESTAMP = r"\d{8}-\d{6}"


def get_dat_pattern(base_name: str, tag: str | None) -> re.Pattern:
    escaped_base = re.escape(base_name)
    if tag:
        return re.compile(rf"^{escaped_base} \({re.escape(tag)}\) \({TIMESTAMP}\)\.dat$")
    return re.compile(rf"^{escaped_base} \({TIMESTAMP}\)\.dat$")


def find_latest_match(folder: Path, pattern: re.Pattern) -> Path | None:
    if not folder.is_dir():
        return None
    candidates = sorted(
        (p for p in folder.iterdir() if p.is_file() and pattern.match(p.name)),
        key=lambda p: p.name,
        reverse=True,
    )
    return candidates[0] if candidates else None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--system-id", dest="system_id", default=None)
    args = parser.parse_args()

    manifest: dict[str, str] = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["systems"]

    ids = [args.system_id] if args.system_id else list(manifest.keys())

    missing: list[str] = []
    copied_count = 0

    for system_id in ids:
        if system_id not in manifest:
            print(f"ADVERTENCIA: Sistema no encontrado en el manifiesto: {system_id}")
            continue
        base_name = manifest[system_id]
        found_any = False

        for pack_name, tag in PACKS.items():
            pattern = get_dat_pattern(base_name, tag)
            src_folder = RAW_ROOT / pack_name
            match = find_latest_match(src_folder, pattern)
            if not match:
                continue

            found_any = True
            dest_folder = DEST_ROOT / pack_name
            dest_folder.mkdir(parents=True, exist_ok=True)
            dest_path = dest_folder / match.name

            # Elimina versiones anteriores del mismo sistema/pack antes de copiar la nueva
            for existing in dest_folder.iterdir():
                if existing.is_file() and existing.name != match.name and pattern.match(existing.name):
                    existing.unlink()

            if not dest_path.exists():
                shutil.copy2(match, dest_path)
                copied_count += 1
                print(f"Copiado [{pack_name}]: {match.name}")

        if not found_any:
            missing.append(system_id)

    if missing:
        print(f"ADVERTENCIA: Sistemas del manifiesto sin ningun DAT encontrado en metadata/dat/No-Intro/: {', '.join(missing)}")

    # Ficheros huerfanos en sources/: ya no corresponden a ningun sistema del manifiesto
    expected_base_names = set(manifest.values())
    for pack_name, tag in PACKS.items():
        dest_folder = DEST_ROOT / pack_name
        if not dest_folder.is_dir():
            continue
        suffix_pattern = (
            rf" \({re.escape(tag)}\) \({TIMESTAMP}\)\.dat$" if tag else rf" \({TIMESTAMP}\)\.dat$"
        )
        suffix_re = re.compile(suffix_pattern)
        for existing in dest_folder.iterdir():
            if not existing.is_file():
                continue
            stripped_base = suffix_re.sub("", existing.name)
            if stripped_base not in expected_base_names:
                print(f"ADVERTENCIA: Huerfano en sources/ [{pack_name}]: {existing.name} (ya no esta en el manifiesto)")

    print(f"Sincronizacion completa. {copied_count} fichero(s) nuevo(s) copiado(s).")


if __name__ == "__main__":
    main()
