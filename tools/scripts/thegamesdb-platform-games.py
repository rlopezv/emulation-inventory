#!/usr/bin/env python3
"""
Consulta ad-hoc de la API oficial de TheGamesDB (https://api.thegamesdb.net/,
Swagger vigente -- la wiki historica en wiki.thegamesdb.net esta obsoleta)
para obtener el listado de juegos de una plataforma. Mismo patron que
`launchbox-platform-games.py`, pero aqui la plataforma se resuelve por
NOMBRE contra la API en tiempo real en vez de un mapeo hardcodeado: no
hay forma de verificar de antemano el `id`/nombre exacto de cada
plataforma en TheGamesDB sin tener ya una API key (ver
docs/guides/tools/api-credentials.md), asi que no se inventa aqui --
usar --list-platforms para verificarlo la primera vez que se use un
sistema nuevo, y luego --platform-id (mas rapido, evita una llamada
extra) para las siguientes.

**No probado contra la API real todavia** (escrito sin API key
disponible en el momento de creacion, 2026-09-06) -- construido contra
el esquema documentado en Swagger (openapi/thegamesdb-*-api-openapi.yml
de github.com/api-evangelist/thegamesdb) y el formato de respuesta ya
conocido de la comunidad (data/pages/remaining_monthly_allowance). Antes
de confiar en la salida, validar una vez que la clave este disponible:
si el formato de respuesta real difiere de lo aqui asumido, ajustar
`_unwrap_games()`/`_unwrap_platforms()`.

Uso:
    python thegamesdb-platform-games.py --api-key XXXX --list-platforms
    python thegamesdb-platform-games.py --api-key XXXX --platform-name "Sinclair ZX Spectrum" --output spectrum.csv
    python thegamesdb-platform-games.py --api-key XXXX --platform-id 4913 --output spectrum.csv

La API key tambien se puede pasar por variable de entorno
THEGAMESDB_API_KEY en vez de --api-key.
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

API_BASE = "https://api.thegamesdb.net/v1"

# Campos de juego pedidos por defecto (ver lista completa de `fields`
# soportados en thegamesdb-games-api-openapi.yml); "developers" no esta
# entre los campos documentados de /Games/ByPlatformID -- si se necesita,
# habria que resolverlo aparte via la API de Developers por id.
DEFAULT_FIELDS = "overview,genres,publishers,platform,rating"

CSV_COLUMNS = ["id", "game_title", "release_date", "platform", "overview", "genres", "publishers", "rating"]


def api_key_from_args(args: argparse.Namespace) -> str:
    key = args.api_key or os.environ.get("THEGAMESDB_API_KEY")
    if not key:
        sys.exit("Falta la API key: pasar --api-key o definir THEGAMESDB_API_KEY (ver docs/guides/tools/api-credentials.md)")
    return key


def api_get(path: str, params: dict) -> dict:
    url = f"{API_BASE}{path}?{urllib.parse.urlencode(params)}"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _unwrap_platforms(payload: dict) -> dict:
    # Forma documentada: {"data": {"count": N, "platforms": {"<id>": {...}, ...}}}
    return payload.get("data", {}).get("platforms", {})


def _unwrap_games(payload: dict) -> tuple[list[dict], str | None]:
    data = payload.get("data", {})
    games = data.get("games", [])
    next_url = payload.get("pages", {}).get("next")
    return games, next_url


def list_platforms(apikey: str) -> None:
    payload = api_get("/Platforms", {"apikey": apikey})
    platforms = _unwrap_platforms(payload)
    for pid, info in sorted(platforms.items(), key=lambda kv: info_name(kv[1])):
        print(f"{pid}\t{info_name(info)}")


def info_name(info: dict) -> str:
    return info.get("name", "")


def resolve_platform_id(apikey: str, name: str) -> str:
    payload = api_get("/Platforms/ByPlatformName", {"apikey": apikey, "name": name})
    platforms = _unwrap_platforms(payload)
    if not platforms:
        sys.exit(
            f"Ninguna plataforma coincide con '{name}' en TheGamesDB. "
            "Usa --list-platforms para ver los nombres reales."
        )
    if len(platforms) > 1:
        opciones = ", ".join(f"{pid}={info_name(v)}" for pid, v in platforms.items())
        sys.exit(f"Varias plataformas coinciden con '{name}': {opciones}. Usa --platform-id con el id exacto.")
    (pid, _info), = platforms.items()
    return pid


def fetch_all_games(apikey: str, platform_id: str, fields: str) -> list[dict]:
    games: list[dict] = []
    params = {"apikey": apikey, "id": platform_id, "fields": fields, "page": 1}
    while True:
        payload = api_get("/Games/ByPlatformID", params)
        page_games, next_url = _unwrap_games(payload)
        games.extend(page_games)
        if not next_url:
            break
        params["page"] += 1
        time.sleep(0.5)  # cortesia -- ver limite mensual en docs/guides/tools/api-credentials.md
    return games


def write_csv(games: list[dict], output: Path | None) -> None:
    stream = open(output, "w", newline="", encoding="utf-8") if output else sys.stdout
    try:
        writer = csv.writer(stream)
        writer.writerow(CSV_COLUMNS)
        for g in games:
            writer.writerow([g.get(col, "") for col in CSV_COLUMNS])
    finally:
        if output:
            stream.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--api-key", help="API key de TheGamesDB (o variable de entorno THEGAMESDB_API_KEY)")
    parser.add_argument("--list-platforms", action="store_true", help="Lista id+nombre de todas las plataformas y sale")
    parser.add_argument("--platform-name", help="Nombre exacto de la plataforma en TheGamesDB (resuelto vía API)")
    parser.add_argument("--platform-id", help="Id numérico de la plataforma (evita la llamada de resolución por nombre)")
    parser.add_argument("--fields", default=DEFAULT_FIELDS, help=f"Campos a pedir (por defecto: {DEFAULT_FIELDS})")
    parser.add_argument("--output", type=Path, help="Fichero CSV de salida (por defecto: stdout)")
    args = parser.parse_args()

    apikey = api_key_from_args(args)

    if args.list_platforms:
        list_platforms(apikey)
        return

    if not args.platform_name and not args.platform_id:
        parser.error("--platform-name o --platform-id es obligatorio salvo con --list-platforms")

    platform_id = args.platform_id or resolve_platform_id(apikey, args.platform_name)
    games = fetch_all_games(apikey, platform_id, args.fields)
    write_csv(games, args.output)
    print(f"{len(games)} juegos para la plataforma id={platform_id}", file=sys.stderr)


if __name__ == "__main__":
    main()
