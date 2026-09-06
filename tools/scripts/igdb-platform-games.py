#!/usr/bin/env python3
"""
Consulta ad-hoc de la API oficial de IGDB (https://api.igdb.com/v4/,
alta de credencial en docs/guides/tools/api-credentials.md) para obtener
el listado de juegos de una plataforma.

Por que un script propio en vez de depender del modulo `igdb` de
SkyScraper (ya catalogado en docs/tools.md): SkyScraper hace scraping
por EMPAREJAMIENTO contra una romset ya presente en disco (nombre de
fichero -> busqueda), asi que solo sirve una vez que ya tienes los
ficheros. Este script consulta el catalogo completo de una plataforma
de forma independiente -- util como fuente de referencia (que juegos
existen para un sistema) ANTES de tener la romset, igual que
`thegamesdb-platform-games.py`/`giantbomb-platform-games.py`.

Mismo patron que esos dos: la plataforma se resuelve por NOMBRE en
tiempo real contra la API (POST /v4/platforms, Apicalypse) para obtener
su `id` numerico -- no se hardcodea ningun mapeo aqui, no hay forma de
verificarlo de antemano sin tener ya credenciales.

**No probado contra la API real todavia** (escrito sin credenciales
disponibles, 2026-09-06) -- construido contra el esquema confirmado via
`src/modules/dats/datParentInferrer.ts`-adyacente (documentacion propia
de IGDB v4, api-docs.igdb.com) y ejemplos reales de consultas Apicalypse
ya usados en la comunidad. Antes de confiar en la salida, validar una
vez que las credenciales esten disponibles.

Autenticacion: credenciales de app de Twitch (IGDB es propiedad de
Twitch/Amazon) -- registrar una app en la consola de desarrolladores de
Twitch para obtener `client_id`/`client_secret`, canjeados aqui mismo
por un token OAuth de aplicacion (grant_type=client_credentials, el
token no caduca en cuestion de minutos como uno de usuario, pero si a
las ~60 dias -- el script lo pide de nuevo en cada ejecucion, no lo
cachea).

Uso:
    python igdb-platform-games.py --client-id XXXX --client-secret YYYY --list-platforms
    python igdb-platform-games.py --client-id XXXX --client-secret YYYY --platform-name "ZX Spectrum" --output spectrum.csv
    python igdb-platform-games.py --client-id XXXX --client-secret YYYY --platform-id 26 --output spectrum.csv

Client-id/secret tambien aceptados por variables de entorno
IGDB_CLIENT_ID / IGDB_CLIENT_SECRET en vez de --client-id/--client-secret.
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

TWITCH_TOKEN_URL = "https://id.twitch.tv/oauth2/token"
API_BASE = "https://api.igdb.com/v4"

# Campos por defecto para /games -- "name" siempre viene; el resto es lo
# util para un listado de referencia. "platforms" se pide para poder
# comprobar de vuelta que el filtro funciono como se esperaba.
DEFAULT_GAME_FIELDS = "name,first_release_date,summary,genres.name,platforms"

CSV_COLUMNS = ["id", "name", "first_release_date", "summary", "genres"]

PAGE_SIZE = 500  # limite maximo de Apicalypse por peticion


def credentials_from_args(args: argparse.Namespace) -> tuple[str, str]:
    client_id = args.client_id or os.environ.get("IGDB_CLIENT_ID")
    client_secret = args.client_secret or os.environ.get("IGDB_CLIENT_SECRET")
    if not client_id or not client_secret:
        sys.exit(
            "Faltan credenciales: pasar --client-id/--client-secret o definir "
            "IGDB_CLIENT_ID/IGDB_CLIENT_SECRET (ver docs/guides/tools/api-credentials.md)"
        )
    return client_id, client_secret


def get_access_token(client_id: str, client_secret: str) -> str:
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }
    url = f"{TWITCH_TOKEN_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, method="POST")
    with urllib.request.urlopen(req) as resp:
        payload = json.loads(resp.read().decode("utf-8"))
    return payload["access_token"]


def apicalypse(client_id: str, access_token: str, endpoint: str, query: str) -> list[dict]:
    url = f"{API_BASE}/{endpoint}"
    req = urllib.request.Request(
        url,
        data=query.encode("utf-8"),
        method="POST",
        headers={
            "Client-ID": client_id,
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "text/plain",
        },
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode("utf-8"))


def list_platforms(client_id: str, access_token: str) -> None:
    results = apicalypse(client_id, access_token, "platforms", f"fields id,name; limit {PAGE_SIZE}; sort name asc;")
    for p in results:
        print(f"{p.get('id')}\t{p.get('name')}")


def resolve_platform_id(client_id: str, access_token: str, name: str) -> int:
    # Apicalypse no tiene un operador "igual, insensible a mayusculas"
    # directo para texto -- se usa `search`, que es una busqueda difusa
    # de IGDB, así que se exige coincidencia exacta de nombre en el
    # resultado antes de aceptarlo (evita falsos positivos).
    query = f'search "{name}"; fields id,name; limit 10;'
    results = apicalypse(client_id, access_token, "platforms", query)
    exact = [p for p in results if p.get("name", "").lower() == name.lower()]
    if not exact:
        opciones = ", ".join(f"{p['id']}={p['name']}" for p in results) or "(ninguna)"
        sys.exit(
            f"Ninguna plataforma coincide EXACTAMENTE con '{name}' en IGDB. "
            f"Candidatas por búsqueda difusa: {opciones}. Usa --list-platforms o --platform-id."
        )
    if len(exact) > 1:
        opciones = ", ".join(f"{p['id']}={p['name']}" for p in exact)
        sys.exit(f"Varias plataformas con el mismo nombre '{name}': {opciones}. Usa --platform-id con el id exacto.")
    return exact[0]["id"]


def fetch_all_games(client_id: str, access_token: str, platform_id: int, fields: str) -> list[dict]:
    games: list[dict] = []
    offset = 0
    while True:
        query = f"fields {fields}; where platforms = ({platform_id}); sort name asc; limit {PAGE_SIZE}; offset {offset};"
        page = apicalypse(client_id, access_token, "games", query)
        games.extend(page)
        if len(page) < PAGE_SIZE:
            break
        offset += PAGE_SIZE
        time.sleep(0.3)  # limite documentado: 4 peticiones/segundo por app
    return games


def flatten(game: dict) -> dict:
    genres = game.get("genres") or []
    return {
        "id": game.get("id", ""),
        "name": game.get("name", ""),
        "first_release_date": game.get("first_release_date", ""),
        "summary": game.get("summary", ""),
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
    parser.add_argument("--client-id", help="Client ID de la app de Twitch (o variable de entorno IGDB_CLIENT_ID)")
    parser.add_argument("--client-secret", help="Client secret de la app de Twitch (o variable de entorno IGDB_CLIENT_SECRET)")
    parser.add_argument("--list-platforms", action="store_true", help="Lista id+nombre de todas las plataformas y sale")
    parser.add_argument("--platform-name", help="Nombre exacto de la plataforma en IGDB (resuelto vía API)")
    parser.add_argument("--platform-id", type=int, help="Id numérico de la plataforma (evita la llamada de resolución por nombre)")
    parser.add_argument("--fields", default=DEFAULT_GAME_FIELDS, help=f"Campos Apicalypse a pedir (por defecto: {DEFAULT_GAME_FIELDS})")
    parser.add_argument("--output", type=Path, help="Fichero CSV de salida (por defecto: stdout)")
    args = parser.parse_args()

    client_id, client_secret = credentials_from_args(args)
    access_token = get_access_token(client_id, client_secret)

    if args.list_platforms:
        list_platforms(client_id, access_token)
        return

    if not args.platform_name and args.platform_id is None:
        parser.error("--platform-name o --platform-id es obligatorio salvo con --list-platforms")

    platform_id = args.platform_id if args.platform_id is not None else resolve_platform_id(client_id, access_token, args.platform_name)
    games = fetch_all_games(client_id, access_token, platform_id, args.fields)
    write_csv(games, args.output)
    print(f"{len(games)} juegos para la plataforma id={platform_id}", file=sys.stderr)


if __name__ == "__main__":
    main()
