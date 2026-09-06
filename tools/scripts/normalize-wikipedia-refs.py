#!/usr/bin/env python3
"""
Script de un solo uso: normaliza TODAS las secciones "Fuentes de
referencia" de docs/guides/romsets/systems/*.md al formato canonico
fijado el 2026-09-06 (heading + "- Wikipedia:" + sub-lista anidada, una
URL por linea, incluso si solo hay una):

    ## Fuentes de referencia

    - Wikipedia:
      - https://en.wikipedia.org/wiki/...

Antes de esta normalizacion convivian tres formatos en el corpus:
1. Heading + "- Wikipedia: <url>" plano, una URL por linea (58 ficheros,
   generados por `add-wikipedia-refs.ps1`).
2. Heading + "- Wikipedia:" + sub-lista anidada (14 ficheros generados por
   `add-wikipedia-refs.py`, ya en el formato nuevo).
3. "- Wikipedia:" + sub-lista anidada SIN el heading `##` (4 ficheros
   editados a mano: atari5200/atari7800/atarist/c64).

No toca las lineas `[TODO]` (se quedan planas, no hay URL que anidar) ni
reescribe ninguna URL — solo reestructura el formato, preservando cada
URL/fragmento (`#Commercial_games` etc.) tal cual estaba.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parents[2] / "docs" / "guides" / "romsets" / "systems"

HEADING = "## Fuentes de referencia"

# Caso 1: heading seguido de una o mas lineas planas "- Wikipedia: <url>"
# (no TODO) -> convertir a "- Wikipedia:" + sub-lista anidada.
FLAT_WITH_HEADING_RE = re.compile(
    rf"{re.escape(HEADING)}\n\n((?:- Wikipedia: (?!\[TODO\]).+\n?)+)"
)

# Caso 3: "- Wikipedia:" (plano o ya anidado) que NO tiene el heading
# inmediatamente encima -> anteponer el heading, sin tocar el resto.
BARE_BLOCK_RE = re.compile(r"(?<!Fuentes de referencia\n\n)- Wikipedia:\n(?:  - .+\n?)+")


def normalize_flat_to_nested(match: re.Match) -> str:
    flat_lines = match.group(1).strip("\n").split("\n")
    urls = [line.removeprefix("- Wikipedia: ").strip() for line in flat_lines]
    nested = "\n".join(f"  - {u}" for u in urls)
    return f"{HEADING}\n\n- Wikipedia:\n{nested}\n"


def normalize_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    text = FLAT_WITH_HEADING_RE.sub(normalize_flat_to_nested, text)

    def add_heading(match: re.Match) -> str:
        return f"{HEADING}\n\n{match.group(0)}"

    text = BARE_BLOCK_RE.sub(add_heading, text)

    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(DOCS_ROOT.glob("*.md")):
        if path.name == "README.md":
            continue
        if normalize_file(path):
            print(f"Normalizado: {path.name}")
            changed += 1
    print(f"\nTotal normalizados: {changed}", file=sys.stderr)


if __name__ == "__main__":
    main()
