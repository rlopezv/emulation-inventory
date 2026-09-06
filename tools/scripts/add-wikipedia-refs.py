#!/usr/bin/env python3
"""
Inserta (o rellena, si ya existe vacia) la seccion "## Fuentes de
referencia" de docs/guides/romsets/systems/<id>.md, calculando el encoding
de la URL de Wikipedia en vez de escribirlo a mano — motivo del script:
el encoding manual (espacios -> "_", "&" -> "%26", guion en-dash "-" ->
"%E2%80%93"...) es donde se producian los errores de formato repetidos.

Uso: editar WIKI_MAP mas abajo (id -> lista de titulos de articulo tal
cual aparecen en Wikipedia, o la constante TODO para "sin articulo
encontrado") y ejecutar sin argumentos. Idempotente: si la seccion ya
existe (vacia o no), la reemplaza; si no existe, la inserta tras el
titulo `# <id> -- Curacion`, antes de `<!-- AUTO-GENERADO INICIO -->`
(o al final del fichero si no hay marcador).

Verificar los titulos contra https://en.wikipedia.org/wiki/Category:Lists_of_video_games_by_platform
antes de anadirlos aqui — no inventar articulos que no esten confirmados
en esa categoria (ver docs/session-context.md, sesion 2026-09-06).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import quote

DOCS_ROOT = Path(__file__).resolve().parents[2] / "docs" / "guides" / "romsets" / "systems"

TODO = "TODO"

# id -> lista de titulos de articulo (orden = orden de los bullets), o TODO
# si no existe articulo de lista especifico confirmado contra la categoria.
WIKI_MAP: dict[str, list[str] | str] = {
    "amiga": ["List of Amiga games", "List of Amiga games (A–H)", "List of Amiga games (I–O)", "List of Amiga games (P–Z)"],
    "coleco": ["List of ColecoVision games"],
    "gameandwatch": ["List of Game & Watch games"],
    "intellivision": ["List of Intellivision games"],
    "msx": ["List of MSX games"],
    "msx2": ["List of MSX games"],
    "odyssey2": ["List of Magnavox Odyssey 2 games"],
    "plus4": ["List of Commodore 16 games"],
    "sharpx68000": ["List of X68000 games"],
    "spectrum": ["List of ZX Spectrum games"],
    "switch": ["List of Nintendo Switch games"],
    "vectrex": ["List of Vectrex games"],
    "vic20": ["List of VIC-20 games"],
    "zx81": ["List of ZX81 games"],
    "c128": TODO,
    "dragon32": TODO,
    "megaduck": TODO,
    "ndsi": TODO,
    "newn3ds": TODO,
    "psn": TODO,
    "psvita": TODO,
    "thomson": TODO,
}

TODO_NOTE = (
    "[TODO] No existe artículo \"List of ... games\" específico para este sistema en Wikipedia "
    "(verificado contra Category:Lists_of_video_games_by_platform, sesión 2026-09-06)"
)


def title_to_url(title: str) -> str:
    """Replica el esquema real de URL de Wikipedia: espacios -> "_",
    resto de caracteres percent-encoded salvo paréntesis y guión medio."""
    slug = title.replace(" ", "_")
    return "https://en.wikipedia.org/wiki/" + quote(slug, safe="()-")


def build_block(entry: list[str] | str) -> str:
    # Formato canonico (fijado 2026-09-06): heading + "- Wikipedia:" +
    # sub-lista anidada, una URL por linea, incluso si solo hay una.
    # TODO se queda en una sola linea plana, no hay URL que anidar.
    if entry == TODO:
        body = f"- Wikipedia: {TODO_NOTE}"
    else:
        urls = "\n".join(f"  - {title_to_url(t)}" for t in entry)
        body = "- Wikipedia:\n" + urls
    return "## Fuentes de referencia\n\n" + body + "\n"


def apply_to_file(system_id: str, entry: list[str] | str) -> None:
    path = DOCS_ROOT / f"{system_id}.md"
    if not path.is_file():
        print(f"AVISO: no existe {path}, saltando", file=sys.stderr)
        return

    text = path.read_text(encoding="utf-8")
    block = build_block(entry)

    # Caso 1: ya existe la seccion (vacia, plana o ya anidada) -> reemplazar
    # todo el bloque hasta la siguiente linea en blanco (o fin de fichero).
    # DOTALL para que "- Wikipedia:" con sub-lista anidada en lineas
    # siguientes se consuma entero, no solo su primera linea.
    section_re = re.compile(
        r"## Fuentes de referencia\n\n- Wikipedia:.*?(?=\n\n|\Z)", re.DOTALL
    )
    if section_re.search(text):
        new_text = section_re.sub(block, text, count=1)
    else:
        # Caso 2: no existe -> insertar tras la primera linea (titulo),
        # dejando una linea en blanco antes y despues.
        lines = text.split("\n", 1)
        if len(lines) == 1:
            new_text = lines[0] + "\n\n" + block
        else:
            title_line, rest = lines
            rest = rest.lstrip("\n")
            new_text = f"{title_line}\n\n{block}\n{rest}"

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        print(f"Actualizado: {path.relative_to(DOCS_ROOT.parents[3])}")
    else:
        print(f"Sin cambios: {path.name}")


def main() -> None:
    for system_id, entry in WIKI_MAP.items():
        apply_to_file(system_id, entry)


if __name__ == "__main__":
    main()
