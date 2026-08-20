#!/usr/bin/env python3
"""
Equivalente Python de generate-parent-clone-fullset.ps1 (pensado para
ejecutarse desde el devcontainer). Misma logica, misma salida esperada; ver
la cabecera de generate-parent-clone-fullset.ps1 para la descripcion
completa del proposito (driver de lote sobre convert-cloneofid-to-parent-
clone.py para todo el manifiesto nointro-systems.json).

Uso:
    python tools/scripts/generate-parent-clone-fullset.py
    python tools/scripts/generate-parent-clone-fullset.py --system-id megadrive
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def latest_match(folder: Path, pattern: re.Pattern) -> Path | None:
    if not folder.is_dir():
        return None
    candidates = [p for p in folder.iterdir() if p.is_file() and pattern.match(p.name)]
    if not candidates:
        return None
    return sorted(candidates, key=lambda p: p.name, reverse=True)[0]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--system-id", dest="system_id", default=None)
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    repo_root = script_dir.parent.parent

    manifest_path = script_dir / "config" / "nointro-systems.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))["systems"]

    full_root = repo_root / "sources" / "dats" / "no-intro" / "full"
    aftermarket_root = repo_root / "sources" / "dats" / "no-intro" / "aftermarket"
    out_root = repo_root / "sources" / "dats" / "no-intro" / "fullset"
    out_root.mkdir(parents=True, exist_ok=True)

    converter = script_dir / "convert-cloneofid-to-parent-clone.py"

    ids = [args.system_id] if args.system_id else list(manifest.keys())

    results: list[dict] = []

    for system_id in ids:
        if system_id not in manifest:
            print(f"AVISO: sistema no encontrado en el manifiesto: {system_id}", file=sys.stderr)
            continue
        base_name = manifest[system_id]
        escaped = re.escape(base_name)

        full_pattern = re.compile(rf"^{escaped} \(\d{{8}}-\d{{6}}\)\.dat$")
        after_pattern = re.compile(rf"^{escaped} \(Aftermarket\) \(\d{{8}}-\d{{6}}\)\.dat$")

        full_match = latest_match(full_root, full_pattern)
        after_match = latest_match(aftermarket_root, after_pattern)

        if not full_match:
            print(f"AVISO: {system_id} : sin full/, saltado", file=sys.stderr)
            results.append({"id": system_id, "status": "sin full/"})
            continue

        inputs = [str(full_match)]
        if after_match:
            inputs.append(str(after_match))

        ts_match = re.search(r"\((\d{8}-\d{6})\)\.dat$", full_match.name)
        ts = ts_match.group(1) if ts_match else datetime.now().strftime("%Y%m%d-%H%M%S")

        out_name = f"{base_name} (Parent-Clone) ({ts}).dat"
        out_path = out_root / out_name

        cmd = [
            sys.executable, str(converter),
            "--input", *inputs,
            "--output", str(out_path),
            "--name", base_name,
            "--url", "https://www.no-intro.org",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            print(f"AVISO: {system_id} : ERROR - {proc.stderr.strip()}", file=sys.stderr)
            results.append({"id": system_id, "status": f"ERROR: {proc.stderr.strip()}"})
            continue

        game_count = out_path.read_text(encoding="utf-8").count("<game ")
        print(f"OK  {system_id} -> {out_name} ({game_count} games)")
        results.append({"id": system_id, "status": "OK", "games": game_count, "inputs": len(inputs)})

    print("\n=== RESUMEN ===")
    for r in results:
        print(r)


if __name__ == "__main__":
    main()
