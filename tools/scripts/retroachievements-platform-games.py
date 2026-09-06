#!/usr/bin/env python3
"""
Consulta ad-hoc de la API oficial de RetroAchievements
(https://api-docs.retroachievements.org/, alta de credencial en
docs/guides/tools/api-credentials.md) para obtener el listado de juegos
de un sistema -- a diferencia de MobyGames/TheGamesDB/GiantBomb/IGDB,
esta fuente conecta con algo ya usado en el repo: `rahashes` y
`unofficial-ra-dats` (ver docs/dat-sources.md) usan hashes de
RetroAchievements para verificacion, y este mismo endpoint puede devolver
los hashes MD5 de cada juego (`--include-hashes`), asi que sirve tanto de
listado de referencia como de fuente de hashes en vivo.

Cobertura limitada: solo sistemas que RetroAchievements soporta con
logros (no es un catalogo generico como los otros cuatro).

La plataforma se resuelve por NOMBRE en tiempo real contra
`API_GetConsoleIDs.php` (--console-name) para obtener su `ID` numerico
-- no se hardcodea un mapeo id-canonico->consola aqui, no hay forma de
verificarlo de antemano sin tener ya una API key. --list-consoles vuelca
todas para resolverlo a mano la primera vez.

**No probado contra la API real todavia** (escrito sin API key
disponible, 2026-09-06) -- construido contra la documentacion oficial
(api-docs.retroachievements.org). Antes de confiar en la salida,
validar una vez que la clave este disponible.

Uso:
    python retroachievements-platform-games.py --api-key XXXX --username USER --list-consoles
    python retroachievements-platform-games.py --api-key XXXX --username USER --console-name "Sinclair ZX Spectrum" --output spectrum.csv
    python retroachievements-platform-games.py --api-key XXXX --username USER --console-id 41 --include-hashes --output spectrum.csv

La API key y el usuario tambien se aceptan por variables de entorno
RA_API_KEY / RA_USERNAME en vez de --api-key/--username (RetroAchievements
exige ambos para autenticar, no solo la clave).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

API_BASE = "https://retroachievements.org/API"

CSV_COLUMNS = ["ID", "Title", "NumAchievements", "Points", "DateModified", "Hashes"]


def credentials_from_args(args: argparse.Namespace) -> tuple[str, str]:
    api_key = args.api_key or os.environ.get("RA_API_KEY")
    username = args.username or os.environ.get("RA_USERNAME")
    if not api_key or not username:
        sys.exit(
            "Faltan credenciales: pasar --api-key/--username o definir "
            "RA_API_KEY/RA_USERNAME (ver docs/guides/tools/api-credentials.md)"
        )
    return api_key, username


def api_get(endpoint: str, username: str, api_key: str, params: dict) -> list | dict:
    # RetroAchievements exige usuario + clave en cada peticion (parametros
    # "z"=usuario, "y"=clave), no solo la clave sola.
    query = {"z": username, "y": api_key, **params}
    url = f"{API_BASE}/{endpoint}?{urllib.parse.urlencode(query)}"
    with urllib.request.urlopen(url) as resp:
        return json.loads(resp.read().decode("utf-8"))


def list_consoles(username: str, api_key: str) -> None:
    consoles = api_get("API_GetConsoleIDs.php", username, api_key, {"g": 1})
    for c in sorted(consoles, key=lambda c: c.get("Name", "")):
        print(f"{c.get('ID')}\t{c.get('Name')}")


def resolve_console_id(username: str, api_key: str, name: str) -> int:
    consoles = api_get("API_GetConsoleIDs.php", username, api_key, {"g": 1})
    exact = [c for c in consoles if c.get("Name", "").lower() == name.lower()]
    if not exact:
        sys.exit(f"Ninguna consola coincide con '{name}' en RetroAchievements. Usa --list-consoles para ver los nombres reales.")
    if len(exact) > 1:
        opciones = ", ".join(f"{c['ID']}={c['Name']}" for c in exact)
        sys.exit(f"Varias consolas con el mismo nombre '{name}': {opciones}. Usa --console-id con el id exacto.")
    return exact[0]["ID"]


def fetch_games(username: str, api_key: str, console_id: int, only_with_achievements: bool, include_hashes: bool) -> list[dict]:
    params = {
        "i": console_id,
        "f": 1 if only_with_achievements else 0,
        "h": 1 if include_hashes else 0,
    }
    return api_get("API_GetGameList.php", username, api_key, params)


def write_csv(games: list[dict], output: Path | None) -> None:
    stream = open(output, "w", newline="", encoding="utf-8") if output else sys.stdout
    try:
        writer = csv.writer(stream)
        writer.writerow(CSV_COLUMNS)
        for g in games:
            hashes = g.get("Hashes") or []
            writer.writerow([g.get(col, "") if col != "Hashes" else "; ".join(hashes) for col in CSV_COLUMNS])
    finally:
        if output:
            stream.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--api-key", help="Web API key de RetroAchievements (o variable de entorno RA_API_KEY)")
    parser.add_argument("--username", help="Usuario de RetroAchievements dueño de la key (o variable de entorno RA_USERNAME)")
    parser.add_argument("--list-consoles", action="store_true", help="Lista id+nombre de todas las consolas y sale")
    parser.add_argument("--console-name", help="Nombre exacto de la consola en RetroAchievements (resuelto vía API)")
    parser.add_argument("--console-id", type=int, help="Id numérico de la consola (evita la llamada de resolución por nombre)")
    parser.add_argument("--only-with-achievements", action="store_true", help="Solo juegos con logros publicados (parámetro f=1)")
    parser.add_argument("--include-hashes", action="store_true", help="Incluye los hashes MD5 compatibles de cada juego (parámetro h=1)")
    parser.add_argument("--output", type=Path, help="Fichero CSV de salida (por defecto: stdout)")
    args = parser.parse_args()

    api_key, username = credentials_from_args(args)

    if args.list_consoles:
        list_consoles(username, api_key)
        return

    if not args.console_name and args.console_id is None:
        parser.error("--console-name o --console-id es obligatorio salvo con --list-consoles")

    console_id = args.console_id if args.console_id is not None else resolve_console_id(username, api_key, args.console_name)
    games = fetch_games(username, api_key, console_id, args.only_with_achievements, args.include_hashes)
    write_csv(games, args.output)
    print(f"{len(games)} juegos para la consola id={console_id}", file=sys.stderr)


if __name__ == "__main__":
    main()
