#!/usr/bin/env python3
"""
Consulta ad-hoc de la base de datos local de LaunchBox Games Database
(`LaunchBox.Metadata.db`, SQLite generado por LaunchBox a partir de su
`Metadata.zip` -- https://gamesdb.launchbox-app.com/) para obtener el
listado de juegos de un sistema, como alternativa a scrapear la web (sin
API oficial) o parsear el XML de 500 MB a mano.

Uso:
    python launchbox-platform-games.py --list-platforms
    python launchbox-platform-games.py --system spectrum --output spectrum.csv
    python launchbox-platform-games.py --system psx --exclude-nonjuego

Requiere tener LaunchBox instalado (o al menos su base de datos local
sincronizada) -- ruta por defecto configurable con --db si no coincide
con la del usuario.
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

DEFAULT_DB = Path(r"F:\tools\LaunchBox\Metadata\LaunchBox.Metadata.db")

# Identificador canonico (docs/systems.md) -> nombre de Platform en LaunchBox.
# Verificado contra `select Name from Platforms` sobre la base real
# (sesion 2026-09-06). None = sin plataforma equivalente confirmada en
# LaunchBox (revisar --list-platforms antes de asumir que no existe).
PLATFORM_MAP: dict[str, str | None] = {
    "3do": "3DO Interactive Multiplayer",
    "3ds": "Nintendo 3DS",
    "64dd": "Nintendo 64DD",
    "amiga": "Commodore Amiga",
    "amigacd32": "Commodore Amiga CD32",
    "amigacdtv": "Commodore CDTV",
    "amstradcpc": "Amstrad CPC",
    "arcadia2001": "Emerson Arcadia 2001",
    "astrocade": "Bally Astrocade",
    "atari2600": "Atari 2600",
    "atari5200": "Atari 5200",
    "atari7800": "Atari 7800",
    "atari800": "Atari 800",
    "atarist": "Atari ST",
    "c128": "Commodore 128",
    "c64": "Commodore 64",
    "cdi": "Philips CD-i",
    "channelf": "Fairchild Channel F",
    "coleco": "ColecoVision",
    "dragon32": "Dragon 32/64",
    "dreamcast": "Sega Dreamcast",
    "dsiware": None,  # LaunchBox no distingue DSiWare de "Nintendo DS"
    "fds": "Nintendo Famicom Disk System",
    "gameandwatch": "Nintendo Game & Watch",
    "gamecube": "Nintendo GameCube",
    "gamegear": "Sega Game Gear",
    "gb": "Nintendo Game Boy",
    "gba": "Nintendo Game Boy Advance",
    "gbc": "Nintendo Game Boy Color",
    "gx4000": "Amstrad GX4000",
    "intellivision": "Mattel Intellivision",
    "jaguar": "Atari Jaguar",
    "jaguarcd": "Atari Jaguar CD",
    "lynx": "Atari Lynx",
    "mastersystem": "Sega Master System",
    "megadrive": "Sega Genesis",
    "megaduck": "Mega Duck",
    "msx": "Microsoft MSX",
    "msx2": "Microsoft MSX2",
    "n64": "Nintendo 64",
    "nds": "Nintendo DS",
    "ndsi": None,  # sin plataforma propia en LaunchBox, ver dsiware
    "neogeo": "SNK Neo Geo AES",
    "neogeocd": "SNK Neo Geo CD",
    "nes": "Nintendo Entertainment System",
    "newn3ds": None,  # sin plataforma propia en LaunchBox, ver 3ds
    "ngp": "SNK Neo Geo Pocket",
    "ngpc": "SNK Neo Geo Pocket Color",
    "odyssey2": "Magnavox Odyssey 2",
    "pcengine": "NEC TurboGrafx-16",
    "pcenginecd": "NEC TurboGrafx-CD",
    "plus4": "Commodore Plus 4",
    "pokemini": "Nintendo Pokemon Mini",
    "ps2": "Sony Playstation 2",
    "ps3": "Sony Playstation 3",
    "psn": None,  # no es una plataforma fisica, sin equivalente en LaunchBox
    "psp": "Sony PSP",
    "pspminis": "Sony PSP Minis",
    "psvita": "Sony Playstation Vita",
    "psx": "Sony Playstation",
    "satellaview": "Nintendo Satellaview",
    "saturn": "Sega Saturn",
    "sega32x": "Sega 32X",
    "segacd": "Sega CD",
    "sg1000": "Sega SG-1000",
    "sgb": None,  # Super Game Boy no tiene plataforma propia en LaunchBox
    "sharpx68000": "Sharp X68000",
    "snes": "Super Nintendo Entertainment System",
    "spectrum": "Sinclair ZX Spectrum",
    "sufami": None,  # Sufami Turbo no tiene plataforma propia en LaunchBox
    "supervision": "Watara Supervision",
    "switch": "Nintendo Switch",
    "thomson": None,  # sin plataforma confirmada en LaunchBox
    "vectrex": "GCE Vectrex",
    "vic20": "Commodore VIC-20",
    "virtualboy": "Nintendo Virtual Boy",
    "wii": "Nintendo Wii",
    "wiiu": "Nintendo Wii U",
    "wswan": "WonderSwan",
    "wswanc": "WonderSwan Color",
    "xbox": "Microsoft Xbox",
    "xbox360": "Microsoft Xbox 360",
    "zx81": "Sinclair ZX-81",
}

FIELDS = [
    "DatabaseID",
    "Name",
    "ReleaseYear",
    "ReleaseDate",
    "ReleaseType",
    "Genres",
    "Developer",
    "Publisher",
]


def connect(db_path: Path) -> sqlite3.Connection:
    if not db_path.is_file():
        sys.exit(f"No se encuentra la base de datos de LaunchBox en: {db_path}")
    return sqlite3.connect(str(db_path))


def list_platforms(con: sqlite3.Connection) -> None:
    cur = con.execute("SELECT Name FROM Platforms ORDER BY Name")
    for (name,) in cur.fetchall():
        print(name)


def resolve_platform_name(system_id: str) -> str:
    if system_id not in PLATFORM_MAP:
        sys.exit(
            f"Sistema '{system_id}' no está en PLATFORM_MAP. "
            "Comprueba el id contra docs/systems.md y añádelo al mapeo, "
            "verificando el nombre real con --list-platforms."
        )
    name = PLATFORM_MAP[system_id]
    if name is None:
        sys.exit(
            f"Sistema '{system_id}' no tiene plataforma equivalente confirmada "
            "en LaunchBox (ver comentario junto a la entrada en PLATFORM_MAP)."
        )
    return name


def fetch_games(
    con: sqlite3.Connection, platform_name: str, exclude_nonjuego: bool
) -> list[sqlite3.Row]:
    con.row_factory = sqlite3.Row
    query = f"SELECT {', '.join(FIELDS)} FROM Games WHERE Platform = ?"
    params: list[str] = [platform_name]
    if exclude_nonjuego:
        # "Released"/None se mantienen; se excluye lo que no es juego
        # comercial original -- coherente con el criterio ya aplicado a
        # No-Intro/Redump/TOSEC en este repo (fullset != homebrew/hacks).
        query += " AND (ReleaseType IS NULL OR ReleaseType NOT IN (?, ?, ?))"
        params += ["Homebrew", "ROM Hack", "Unlicensed"]
    query += " ORDER BY Name"
    return con.execute(query, params).fetchall()


def write_csv(rows: list[sqlite3.Row], output: Path | None) -> None:
    stream = open(output, "w", newline="", encoding="utf-8") if output else sys.stdout
    try:
        writer = csv.writer(stream)
        writer.writerow(FIELDS)
        for row in rows:
            writer.writerow([row[f] for f in FIELDS])
    finally:
        if output:
            stream.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB, help="Ruta a LaunchBox.Metadata.db")
    parser.add_argument("--system", help="Identificador canónico (docs/systems.md)")
    parser.add_argument("--list-platforms", action="store_true", help="Lista todas las Platform de LaunchBox y sale")
    parser.add_argument("--exclude-nonjuego", action="store_true", help="Excluye Homebrew/ROM Hack/Unlicensed")
    parser.add_argument("--output", type=Path, help="Fichero CSV de salida (por defecto: stdout)")
    args = parser.parse_args()

    con = connect(args.db)

    if args.list_platforms:
        list_platforms(con)
        return

    if not args.system:
        parser.error("--system es obligatorio salvo con --list-platforms")

    platform_name = resolve_platform_name(args.system)
    rows = fetch_games(con, platform_name, args.exclude_nonjuego)
    write_csv(rows, args.output)
    print(f"{len(rows)} juegos para '{platform_name}' ({args.system})", file=sys.stderr)


if __name__ == "__main__":
    main()
