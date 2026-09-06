#!/usr/bin/env python3
"""
Reparacion puntual: build-fuentes-referencia-table.py se relanzo por error
una segunda vez sobre su propia salida (2026-09-06), y al no encontrar el
bullet "- Wikipedia:" original dentro de una tabla ya convertida, borro la
fila Generica/Wikipedia en los 84 ficheros. Este script la restaura:

- Para los ficheros ya versionados en git: recupera la URL exacta desde
  `git show HEAD:<path>` (el contenido committeado, formato plano
  "- Wikipedia: <url>", anterior a la normalizacion a formato anidado
  hecha en esta misma sesion sin commitear).
- Para los ficheros nuevos (todavia sin commit, `git status` los marca
  `??`): no hay HEAD del que recuperar. Solo se restauran los que se
  conocen con certeza absoluta (RECOVERED_KNOWN, por haber sido vistos
  directamente en esta conversacion o generados deterministamente por
  `add-wikipedia-refs.py`). El resto queda en `[TODO]` con nota explicita
  del motivo -- no se inventa una URL de reemplazo.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
DOCS_ROOT = REPO_ROOT / "docs" / "guides" / "romsets" / "systems"

# Ficheros nuevos sin HEAD cuya URL de Wikipedia se conoce con certeza:
# generada deterministamente por add-wikipedia-refs.py (title_to_url) o
# vista directamente en esta conversacion antes de la perdida.
RECOVERED_KNOWN: dict[str, list[str]] = {
    "amiga": [
        "https://en.wikipedia.org/wiki/List_of_Amiga_games",
        "https://en.wikipedia.org/wiki/List_of_Amiga_games_(A%E2%80%93H)",
        "https://en.wikipedia.org/wiki/List_of_Amiga_games_(I%E2%80%93O)",
        "https://en.wikipedia.org/wiki/List_of_Amiga_games_(P%E2%80%93Z)",
    ],
    "coleco": ["https://en.wikipedia.org/wiki/List_of_ColecoVision_games"],
    "msx": ["https://en.wikipedia.org/wiki/List_of_MSX_games"],
    "msx2": ["https://en.wikipedia.org/wiki/List_of_MSX_games"],
    "plus4": ["https://en.wikipedia.org/wiki/List_of_Commodore_16_games"],
    "sharpx68000": ["https://en.wikipedia.org/wiki/List_of_X68000_games"],
    "spectrum": ["https://en.wikipedia.org/wiki/List_of_ZX_Spectrum_games"],
    "switch": ["https://en.wikipedia.org/wiki/List_of_Nintendo_Switch_games"],
    "vic20": ["https://en.wikipedia.org/wiki/List_of_VIC-20_games"],
    "zx81": ["https://en.wikipedia.org/wiki/List_of_ZX81_games"],
    # Vistos directamente (Read) en esta conversacion antes de la perdida.
    "c128": ["https://en.wikipedia.org/w/index.php?title=List_of_Commodore_128_games"],
    "thomson": ["https://en.wikipedia.org/wiki/List_of_Thomson_computers#Video_Games"],
    "gameandwatch": ["https://en.wikipedia.org/wiki/List_of_Game_%26_Watch_games"],
    "intellivision": ["https://en.wikipedia.org/wiki/List_of_Intellivision_games"],
    "odyssey2": ["https://en.wikipedia.org/wiki/List_of_Magnavox_Odyssey_2_games"],
    "vectrex": ["https://en.wikipedia.org/wiki/List_of_Vectrex_games"],
}

# psn: confirmado TODO real (sin articulo de lista especifico, ver
# add-wikipedia-refs.py TODO_NOTE) -- no es una perdida, es el estado
# correcto que ya tenia antes del error del script.
TODO_REAL_NOTE = (
    "`[TODO]` No existe artículo \"List of ... games\" específico para este sistema en Wikipedia "
    "(verificado contra Category:Lists_of_video_games_by_platform, sesión 2026-09-06)"
)
CONFIRMED_TODO = {"psn"}

# Ficheros nuevos sin HEAD y sin URL recuperable con certeza -- quedan en
# [TODO] con nota del motivo. No adivinar el articulo de Wikipedia.
UNRECOVERABLE = {
    "amstradcpc",
    "arcadia2001",
    "atari800",
    "atarist",
    "c64",
    "channelf",
    "dragon32",
    "megaduck",
    "ndsi",
    "psvita",
    "astrocade",
    "atari2600",
    "atari5200",
    "atari7800",
    "newn3ds",
}

WIKI_LINE_RE = re.compile(r"^- Wikipedia:\s*(.*)$", re.MULTILINE)
WIKI_NESTED_RE = re.compile(r"- Wikipedia:\s*\n((?:\s*-\s*.+\n?)+)")


def urls_from_head(system_id: str) -> list[str] | None:
    rel_path = f"docs/guides/romsets/systems/{system_id}.md"
    result = subprocess.run(
        ["git", "show", f"HEAD:{rel_path}"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    if result.returncode != 0:
        return None  # no existe en HEAD (fichero nuevo, ?? en git status)

    head_text = result.stdout
    nested = WIKI_NESTED_RE.search(head_text)
    if nested:
        urls = [line.strip().removeprefix("- ").strip() for line in nested.group(1).strip("\n").split("\n")]
        return [u for u in urls if u]

    flat = WIKI_LINE_RE.search(head_text)
    if flat and flat.group(1).strip():
        return [flat.group(1).strip()]

    return None


def insert_generica_rows(text: str, urls: list[str]) -> str:
    # Inserta las filas "| Genérica | Wikipedia | <url> |" justo despues de
    # la ultima fila de la tabla ya presente (Especialista o Generica).
    lines = text.split("\n")
    table_end_idx = None
    for i, line in enumerate(lines):
        if line.startswith("| Especialista") or line.startswith("| Genérica"):
            table_end_idx = i
    if table_end_idx is None:
        raise ValueError("No se encontró la tabla ya convertida")
    new_rows = [f"| Genérica | Wikipedia | {url} |" for url in urls]
    lines[table_end_idx + 1 : table_end_idx + 1] = new_rows
    return "\n".join(lines)


def process_file(path: Path) -> str:
    system_id = path.stem
    text = path.read_text(encoding="utf-8")

    if "| Genérica | Wikipedia |" in text:
        return "ya-tiene-generica"

    urls = urls_from_head(system_id)
    source = "HEAD"
    if urls is None:
        urls = RECOVERED_KNOWN.get(system_id)
        source = "conocido"

    if urls is None:
        todo_row = None
        if system_id in CONFIRMED_TODO:
            todo_row = f"| Genérica | Wikipedia | {TODO_REAL_NOTE} |"
        elif system_id in UNRECOVERABLE:
            todo_row = "| Genérica | Wikipedia | `[TODO]` URL perdida por error del script de conversión (2026-09-06); pendiente de volver a documentar |"
        if todo_row:
            lines = text.split("\n")
            table_end_idx = max(
                i for i, line in enumerate(lines) if line.startswith("| Especialista") or line.startswith("| Genérica")
            )
            lines.insert(table_end_idx + 1, todo_row)
            path.write_text("\n".join(lines), encoding="utf-8")
            return "todo-explicito"
        return "SIN-COBERTURA-EN-SCRIPT"

    new_text = insert_generica_rows(text, urls)
    path.write_text(new_text, encoding="utf-8")
    return f"recuperado-de-{source}"


def main() -> None:
    counts: dict[str, int] = {}
    for path in sorted(DOCS_ROOT.glob("*.md")):
        if path.name == "README.md":
            continue
        status = process_file(path)
        counts[status] = counts.get(status, 0) + 1
        print(f"{path.name}: {status}")
    print("\nResumen:", counts, file=sys.stderr)


if __name__ == "__main__":
    main()
