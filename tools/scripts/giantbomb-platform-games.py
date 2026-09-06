#!/usr/bin/env python3
"""
Consulta ad-hoc de la API oficial de GiantBomb (https://www.giantbomb.com/api/,
alta de credencial en docs/guides/tools/api-credentials.md) para obtener el
listado de juegos de una plataforma. Mismo patron que
`thegamesdb-platform-games.py`: la plataforma se resuelve por NOMBRE en
tiempo real contra la API (GET /platforms/?filter=name:<nombre>) para
obtener su `id` NUMERICO propio -- GiantBomb identifica cada recurso por
un `guid` (string, ej. "3030-121") ademas de ese `id`, y el filtrado de
juegos por plataforma usa el `id` numerico, no el guid (confirmado via
foro oficial y wrappers de terceros, ver tools/scripts/README.md) -- no
hay forma de verificarlo de antemano sin tener ya una API key, asi que
no se hardcodea ningun mapeo aqui. --list-platforms/--platform-name
resuelven por nombre; --platform-id acepta el id ya conocido.

**No probado contra la API real todavia** (escrito sin API key
disponible, 2026-09-06) -- construido contra el esquema Swagger
documentado (openapi/giantbomb-*-api-openapi.yml de
github.com/api-evangelist/giantbomb) y ejemplos de uso reales de
`filter=platforms:<id>` confirmados en el foro oficial de GiantBomb.
Antes de confiar en la salida, validar una vez que la clave este
disponible: el formato de la respuesta real (envoltorio "results", tipos
de "error"/"status_code") no se ha comprobado contra JSON real, solo
contra la documentacion.

Uso:
    python giantbomb-platform-games.py --api-key XXXX --list-platforms
    python giantbomb-platform-games.py --api-key XXXX --platform-name "PlayStation 3" --output ps3.csv
    python giantbomb-platform-games.py --api-key XXXX --platform-id 35 --output ps3.csv

La API key tambien se puede pasar por variable de entorno
GIANTBOMB_API_KEY en vez de --api-key.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://www.giantbomb.com/api"

# GiantBomb pide explicitamente identificar al cliente con un User-Agent
# real en vez del generico de la libreria (documentado en su FAQ/foro).
USER_AGENT = "emulation-docs-repo/1.0 (ad-hoc reference script)"

# field_list por defecto -- limitar campos ahorra cuota, ver
# docs/guides/tools/api-credentials.md para el limite (200 peticiones/
# recurso/hora). "id" y "guid" no hacen falta pedirlos aparte para
# /games/, siempre vienen incluidos.
DEFAULT_FIELDS = "name,original_release_date,deck,genres,platforms"

CSV_COLUMNS = ["id", "guid", "name", "original_release_date", "deck", "genres"]

RESULTS_PER_PAGE = 100  # maximo permitido por la API


def api_key_from_args(args: argparse.Namespace) -> str:
    key = args.api_key or os.environ.get("GIANTBOMB_API_KEY")
    if not key:
        sys.exit("Falta la API key: pasar --api-key o definir GIANTBOMB_API_KEY (ver docs/guides/tools/api-credentials.md)")
    return key


def api_get(path: str, params: dict) -> dict:
    params = {**params, "format": "json"}
    url = f"{API_BASE}{path}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _check_status(payload: dict) -> None:
    # Documentado: status_code == 1 es "OK"; el resto son distintos
    # tipos de error (invalid api key, not found, rate limit...).
    if payload.get("status_code") != 1:
        sys.exit(f"Error de la API de GiantBomb: {payload.get('error')} (status_code={payload.get('status_code')})")


def list_platforms(apikey: str) -> None:
    payload = api_get("/platforms/", {"api_key": apikey, "field_list": "id,name", "limit": RESULTS_PER_PAGE})
    _check_status(payload)
    for p in sorted(payload.get("results", []), key=lambda p: p.get("name", "")):
        print(f"{p.get('id')}\t{p.get('name')}")


def resolve_platform_id(apikey: str, name: str) -> int:
    payload = api_get("/platforms/", {"api_key": apikey, "filter": f"name:{name}", "field_list": "id,name"})
    _check_status(payload)
    results = payload.get("results", [])
    if not results:
        sys.exit(f"Ninguna plataforma coincide con '{name}' en GiantBomb. Usa --list-platforms para ver los nombres reales.")
    if len(results) > 1:
        opciones = ", ".join(f"{p['id']}={p['name']}" for p in results)
        sys.exit(f"Varias plataformas coinciden con '{name}': {opciones}. Usa --platform-id con el id exacto.")
    return results[0]["id"]


def fetch_all_games(apikey: str, platform_id: int, fields: str) -> list[dict]:
    games: list[dict] = []
    offset = 0
    while True:
        payload = api_get(
            "/games/",
            {
                "api_key": apikey,
                "filter": f"platforms:{platform_id}",
                "field_list": fields,
                "limit": RESULTS_PER_PAGE,
                "offset": offset,
                "sort": "name:asc",
            },
        )
        _check_status(payload)
        results = payload.get("results", [])
        games.extend(results)
        total = payload.get("number_of_total_results", len(games))
        offset += len(results)
        if not results or offset >= total:
            break
        time.sleep(1)  # cortesia -- ver limite en docs/guides/tools/api-credentials.md
    return games


def flatten(game: dict) -> dict:
    genres = game.get("genres") or []
    return {
        "id": game.get("id", ""),
        "guid": game.get("guid", ""),
        "name": game.get("name", ""),
        "original_release_date": game.get("original_release_date", ""),
        "deck": game.get("deck", ""),
        "genres": "; ".join(g.get("name", "") for g in genres),
    }


def write_csv(games: list[dict], output: Path | None) -> None:
    stream = open(output, "w", newline="", encoding="utf-8") if output else sys.stdout
    try:
        writer = csv.writer(stream)
        writer.writerow(CSV_COLUMNS)
        for g in games:
            row = flatten(g)
            writer.writerow([row[col] for col in CSV_COLUMNS])
    finally:
        if output:
            stream.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--api-key", help="API key de GiantBomb (o variable de entorno GIANTBOMB_API_KEY)")
    parser.add_argument("--list-platforms", action="store_true", help="Lista id+nombre de todas las plataformas y sale")
    parser.add_argument("--platform-name", help="Nombre exacto de la plataforma en GiantBomb (resuelto vía API)")
    parser.add_argument("--platform-id", type=int, help="Id numérico de la plataforma (evita la llamada de resolución por nombre)")
    parser.add_argument("--fields", default=DEFAULT_FIELDS, help=f"field_list a pedir (por defecto: {DEFAULT_FIELDS})")
    parser.add_argument("--output", type=Path, help="Fichero CSV de salida (por defecto: stdout)")
    args = parser.parse_args()

    apikey = api_key_from_args(args)

    if args.list_platforms:
        list_platforms(apikey)
        return

    if not args.platform_name and args.platform_id is None:
        parser.error("--platform-name o --platform-id es obligatorio salvo con --list-platforms")

    platform_id = args.platform_id if args.platform_id is not None else resolve_platform_id(apikey, args.platform_name)
    games = fetch_all_games(apikey, platform_id, args.fields)
    write_csv(games, args.output)
    print(f"{len(games)} juegos para la plataforma id={platform_id}", file=sys.stderr)


if __name__ == "__main__":
    main()
