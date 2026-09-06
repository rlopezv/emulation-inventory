#!/usr/bin/env python3
"""
Consulta ad-hoc de la API en vivo de World of Spectrum
(worldofspectrum.org/infoseek/api/), especialista de ZX Spectrum.

**Importante -- no es una fuente independiente de ZXDB**: el World of
Spectrum actual (relanzado en 2020 por Lee Fogarty) usa ZXDB como backend
-- mismo dato que expone el dump MySQL de github.com/zxdb/ZXDB, pero
accesible aqui como API REST JSON en vivo, sin necesidad de levantar un
servidor MySQL para consumir el dump. Confirmado contra la API real
(2026-09-06): funciona con `X-API-KEY=test` sin registro visible,
24368 registros totales (10894 solo en entry_group=games).

**Limite duro de paginacion confirmado**: el parametro `limit` se
respeta hasta 10, valores mayores (probado 500 y 5000) se recortan a 10
igualmente -- traer el catalogo completo exige recorrer por `offset` de
10 en 10 (miles de peticiones), no una descarga en bloque. Usar
`--entry-group games` para acotar (10894 en vez de 24368) o `--title`
para una busqueda concreta en vez de `--all`.

Uso:
    python worldofspectrum-games.py --title "Manic Miner"
    python worldofspectrum-games.py --entry-group games --limit 10 --output muestra.csv
    python worldofspectrum-games.py --entry-group games --all --output spectrum_full.csv

La API key es opcional (por defecto "test", ya confirmado funcional);
--api-key para sustituirla si en el futuro deja de servir sin registro.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://worldofspectrum.org/infoseek/api"
PAGE_SIZE = 10  # tope duro confirmado del lado del servidor, no configurable

CSV_COLUMNS = [
    "id",
    "title",
    "entry_type_text",
    "entry_group",
    "no_players",
    "availability_text",
    "publishers",
    "features",
    "controls",
]


def api_get(endpoint: str, api_key: str, params: dict) -> dict:
    query = {"X-API-KEY": api_key, **params}
    url = f"{API_BASE}/{endpoint}?{urllib.parse.urlencode(query)}"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode("utf-8"))


def flatten(title: dict) -> dict:
    return {
        "id": title.get("id", ""),
        "title": title.get("title", ""),
        "entry_type_text": title.get("entry_type_text", ""),
        "entry_group": title.get("entry_group", ""),
        "no_players": title.get("no_players", ""),
        "availability_text": title.get("availability_text", ""),
        "publishers": "; ".join(p.get("name", "") for p in title.get("publishers") or []),
        "features": "; ".join(f.get("feature", "") for f in title.get("features") or []),
        "controls": "; ".join(c.get("control", c.get("name", "")) for c in title.get("controls") or []),
    }


def fetch_titles(api_key: str, filters: dict, fetch_all: bool, limit: int) -> list[dict]:
    titles: list[dict] = []
    offset = 0
    page_size = min(limit, PAGE_SIZE) if not fetch_all else PAGE_SIZE
    while True:
        params = {**filters, "limit": page_size, "offset": offset}
        payload = api_get("software", api_key, params)
        page = payload.get("titles", [])
        titles.extend(page)
        if not fetch_all:
            titles = titles[:limit]
            break
        offset += len(page)
        total = int(payload.get("totalRecords", offset))
        if not page or offset >= total:
            break
        time.sleep(0.3)  # cortesia -- sin rate limit documentado, pero es un servidor comunitario
    return titles


def write_csv(titles: list[dict], output: Path | None) -> None:
    stream = open(output, "w", newline="", encoding="utf-8") if output else sys.stdout
    try:
        writer = csv.writer(stream)
        writer.writerow(CSV_COLUMNS)
        for t in titles:
            row = flatten(t)
            writer.writerow([row[c] for c in CSV_COLUMNS])
    finally:
        if output:
            stream.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--api-key", default="test", help='API key (por defecto "test", confirmado funcional)')
    parser.add_argument("--title", help="Búsqueda por título (admite coincidencia parcial)")
    parser.add_argument(
        "--entry-group",
        choices=["games", "text-adventures", "simulators", "educational", "utilities", "demos", "miscellaneous", "compilations"],
        help="Filtra por grupo de entrada",
    )
    parser.add_argument("--limit", type=int, default=10, help="Número de resultados si no se usa --all (por defecto 10)")
    parser.add_argument("--all", action="store_true", help="Recorre TODO el filtro por paginación (miles de peticiones si no se acota con --title/--entry-group)")
    parser.add_argument("--output", type=Path, help="Fichero CSV de salida (por defecto: stdout)")
    args = parser.parse_args()

    filters = {}
    if args.title:
        filters["title"] = args.title
    if args.entry_group:
        filters["entry_group"] = args.entry_group

    titles = fetch_titles(args.api_key, filters, args.all, args.limit)
    write_csv(titles, args.output)
    print(f"{len(titles)} títulos obtenidos", file=sys.stderr)


if __name__ == "__main__":
    main()
