#!/usr/bin/env python3
"""
Equivalente Python de convert-cloneofid-to-parent-clone.ps1 (pensado para
ejecutarse desde el devcontainer). Misma logica, misma salida esperada; ver
la cabecera de convert-cloneofid-to-parent-clone.ps1 para la descripcion
completa del proposito (conversor generico e independiente, id/cloneofid ->
cloneof por nombre, para alimentar a Retool).

Uso:
    python tools/scripts/convert-cloneofid-to-parent-clone.py --input full.dat aftermarket.dat --output "salida (Parent-Clone).dat"
    python tools/scripts/convert-cloneofid-to-parent-clone.py --input full.dat --output salida.dat --name "Mi Sistema"
"""

from __future__ import annotations

import argparse
import re
from datetime import datetime
from pathlib import Path
from xml.etree import ElementTree as ET
from xml.sax.saxutils import escape as xml_escape

# Mismo detector de tokens de region que build-dat-index-nointro.py (lista
# cerrada, auditada contra los DAT de No-Intro/Non-Redump).
KNOWN_REGIONS = [
    "Argentina", "Asia", "Australia", "Austria", "Bangladesh", "Belgium",
    "Brazil", "Bulgaria", "Canada", "Chile", "China", "Colombia", "Croatia",
    "Czechia", "Denmark", "Egypt", "Europe", "Finland", "France", "Germany",
    "Greece", "Hong Kong", "Hungary", "India", "Indonesia", "Iran", "Iraq",
    "Ireland", "Israel", "Italy", "Japan", "Korea", "Latin America",
    "Mexico", "Netherlands", "New Zealand", "Norway", "Peru", "Poland",
    "Portugal", "Romania", "Russia", "Saudi Arabia", "Scandinavia",
    "Slovakia", "South Africa", "Spain", "Sweden", "Switzerland", "Taiwan",
    "Turkey", "UAE", "United Kingdom", "USA", "Vietnam", "World", "Unknown",
]

PAREN_GROUP_RE = re.compile(r"\(([^()]*)\)")
ROM_ATTRS = ("name", "size", "crc", "md5", "sha1", "status")


def get_first_region(game_name: str) -> str:
    for group in PAREN_GROUP_RE.findall(game_name):
        tokens = [t.strip() for t in re.split(r"[,+]", group)]
        matched = [t for t in tokens if t in KNOWN_REGIONS]
        if matched:
            return matched[0]
    return "Unknown"


def get_root_key(key: str, lookup: dict, memo: dict[str, str]) -> str:
    """Cadena cloneofid hasta la raiz, memoizada, a prueba de ciclos."""
    if key in memo:
        return memo[key]
    visited: set[str] = set()
    current = key
    while True:
        if current in visited:
            break  # ciclo: cortamos aqui
        visited.add(current)
        node = lookup.get(current)
        clone_of = node.get("clone_of_key") if node else None
        if not node or not clone_of or clone_of not in lookup:
            break
        current = clone_of
    memo[key] = current
    return current


def parse_input(path: Path, lookup: dict) -> None:
    if not path.is_file():
        raise SystemExit(f"No existe el fichero de entrada: {path}")
    origin = path.stem
    games = ET.parse(path).getroot().findall("game")
    if not games:
        print(f"ADVERTENCIA: Sin elementos <game> en '{path}' - se omite")
        return

    for game in games:
        full_name = game.get("name")
        if not full_name:
            continue

        game_id = game.get("id")
        local_key = game_id if game_id else f"name:{full_name}"
        key = f"{origin}:{local_key}"
        clone_of_id = game.get("cloneofid")
        clone_of_key = f"{origin}:{clone_of_id}" if game_id and clone_of_id else None

        lookup[key] = {
            "key": key,
            "clone_of_key": clone_of_key,
            "full_name": full_name,
            "roms": game.findall("rom"),
            "region": get_first_region(full_name),
        }


def rom_to_xml(rom: ET.Element) -> str:
    attrs = []
    for attr_name in ROM_ATTRS:
        value = rom.get(attr_name)
        if value:
            attrs.append(f'{attr_name}="{xml_escape(value)}"')
    return f"\t\t<rom {' '.join(attrs)}/>"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", dest="input_dats", nargs="+", required=True, metavar="DAT")
    parser.add_argument("--output", dest="output_dat", required=True)
    parser.add_argument("--name", dest="name", default=None)
    parser.add_argument("--url", dest="url", default="https://www.no-intro.org")
    args = parser.parse_args()

    input_paths = [Path(p) for p in args.input_dats]
    origin_names = [p.stem for p in input_paths]

    # 1) Parsear todos los ficheros de entrada, namespaceando por nombre
    # base del fichero para evitar colision de id entre ficheros distintos.
    lookup: dict[str, dict] = {}
    for path in input_paths:
        parse_input(path, lookup)

    if not lookup:
        raise SystemExit("Ningun <game> valido en los ficheros de entrada indicados.")

    # 2) Resolver raiz de cada <game> (por nombre completo del <game> raiz,
    # NO por nombre base - pc/ oficial tampoco colapsa variantes regionales).
    memo: dict[str, str] = {}
    root_name_by_key: dict[str, str] = {}
    for node in lookup.values():
        root_key = get_root_key(node["key"], lookup, memo)
        root_name_by_key[node["key"]] = lookup[root_key]["full_name"]

    # 3) Construir el XML de salida en esquema Parent-Clone.
    header_name = args.name or (" + ".join(origin_names) + " (Parent-Clone, generado)")
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")

    lines = [
        '<?xml version="1.0"?>',
        '<datafile xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="https://datomatic.no-intro.org/stuff https://datomatic.no-intro.org/stuff/schema_nointro_datfile_v4.xsd">',
        "\t<header>",
        f"\t\t<name>{xml_escape(header_name)}</name>",
        f"\t\t<description>{xml_escape(header_name)}</description>",
        f"\t\t<version>{timestamp}</version>",
        f"\t\t<date>{timestamp}</date>",
        f"\t\t<url>{xml_escape(args.url)}</url>",
        f"\t\t<homepage>Generado por convert-cloneofid-to-parent-clone.py a partir de: "
        f"{xml_escape(', '.join(origin_names))}</homepage>",
        "\t</header>",
    ]

    for node in sorted(lookup.values(), key=lambda n: n["full_name"]):
        name_escaped = xml_escape(node["full_name"])
        root_name = root_name_by_key[node["key"]]
        is_root = root_name == node["full_name"]

        if is_root:
            lines.append(f'\t<game name="{name_escaped}">')
        else:
            lines.append(f'\t<game name="{name_escaped}" cloneof="{xml_escape(root_name)}">')
        lines.append(f"\t\t<description>{name_escaped}</description>")
        lines.append(f'\t\t<release name="{name_escaped}" region="{node["region"]}"/>')
        for rom in node["roms"]:
            lines.append(rom_to_xml(rom))
        lines.append("\t</game>")

    lines.append("</datafile>")

    output_path = Path(args.output_dat)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    root_count = len(set(root_name_by_key.values()))
    print(
        f"Generado: {output_path} ({len(lookup)} juegos, {root_count} familias) "
        f"desde {len(input_paths)} fichero(s): {', '.join(origin_names)}"
    )


if __name__ == "__main__":
    main()
