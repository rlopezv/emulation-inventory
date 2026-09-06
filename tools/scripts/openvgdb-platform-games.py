#!/usr/bin/env python3
"""
Consulta ad-hoc de OpenVGDB (github.com/OpenVGDB/OpenVGDB), base de datos
SQLite descargable sin API/credencial -- mismo patron que
`launchbox-platform-games.py`: fichero local, sin rate limit.

**Importante -- fuente parada, no viva:** la ultima release (v29.0) es de
noviembre de 2021 (confirmado via GitHub API, no de 2026 pese a que una
busqueda superficial puede sugerir lo contrario por el dia "11" del mes).
Cubre 43 sistemas (3DO..MSX2, verificado contra la base real 2026-09-06)
sin nada posterior a esa fecha -- util como snapshot legado, sobre todo
por incluir HASHES (CRC/MD5/SHA1) junto con cada ROM, cosa que ninguna de
las otras fuentes de referencia de este repo hace salvo RetroAchievements
(ver `retroachievements-platform-games.py`). No usar como fuente de
lanzamientos recientes de ningun sistema.

Descarga (una sola vez, manual): https://github.com/OpenVGDB/OpenVGDB/releases/latest
-- descomprimir el .zip, pasar la ruta al .sqlite resultante con --db.

Uso:
    python openvgdb-platform-games.py --db ruta/a/openvgdb.sqlite --list-systems
    python openvgdb-platform-games.py --db ruta/a/openvgdb.sqlite --system spectrum --output c64.csv
    python openvgdb-platform-games.py --db ruta/a/openvgdb.sqlite --system-id 41 --output c64.csv
"""

from __future__ import annotations

import argparse
import csv
import sqlite3
import sys
from pathlib import Path

# Identificador canonico (docs/systems.md) -> systemName de OpenVGDB.
# Verificado 1:1 contra la base real (v29.0, 2026-09-06), incluyendo
# CONTEO REAL de filas en ROMs/RELEASES por sistema, no solo presencia en
# la tabla SYSTEMS -- "Arcade" (id 2, cubierto aparte en docs/arcade/) y
# "NEC SuperGrafx" (id 17, sin id canonico propio en docs/systems.md)
# quedan sin mapeo por no tener id en systems.md; "3DO Interactive
# Multiplayer" (id 1), "Atari Jaguar CD" (id 8), "NEC PC-FX" (id 16) y
# "Commodore 64" (id 41) SI aparecen en SYSTEMS pero tienen 0 filas reales
# en ROMs/RELEASES (confirmado por consulta directa) -- son entradas
# placeholder sin datos, no un id de sistema valido para este script pese
# a estar en la tabla; se marcan None con el motivo real, no se ocultan.
PLATFORM_MAP: dict[str, str | None] = {
    "3do": None,  # placeholder en SYSTEMS, 0 filas reales en ROMs/RELEASES
    "atari2600": "Atari 2600",
    "atari5200": "Atari 5200",
    "atari7800": "Atari 7800",
    "lynx": "Atari Lynx",
    "jaguar": "Atari Jaguar",
    "jaguarcd": None,  # placeholder en SYSTEMS, 0 filas reales en ROMs/RELEASES
    "wswan": "Bandai WonderSwan",
    "wswanc": "Bandai WonderSwan Color",
    "coleco": "Coleco ColecoVision",
    "vectrex": "GCE Vectrex",
    "intellivision": "Intellivision",
    "pcengine": "NEC PC Engine/TurboGrafx-16",
    "pcenginecd": "NEC PC Engine CD/TurboGrafx-CD",
    "fds": "Nintendo Famicom Disk System",
    "gb": "Nintendo Game Boy",
    "gba": "Nintendo Game Boy Advance",
    "gbc": "Nintendo Game Boy Color",
    "gamecube": "Nintendo GameCube",
    "n64": "Nintendo 64",
    "nds": "Nintendo DS",
    "nes": "Nintendo Entertainment System",
    "snes": "Nintendo Super Nintendo Entertainment System",
    "virtualboy": "Nintendo Virtual Boy",
    "wii": "Nintendo Wii",
    "sega32x": "Sega 32X",
    "gamegear": "Sega Game Gear",
    "mastersystem": "Sega Master System",
    "segacd": "Sega CD/Mega-CD",
    "megadrive": "Sega Genesis/Mega Drive",
    "saturn": "Sega Saturn",
    "sg1000": "Sega SG-1000",
    "ngp": "SNK Neo Geo Pocket",
    "ngpc": "SNK Neo Geo Pocket Color",
    "psx": "Sony PlayStation",
    "psp": "Sony PlayStation Portable",
    "odyssey2": "Magnavox Odyssey2",
    "c64": None,  # placeholder en SYSTEMS, 0 filas reales en ROMs/RELEASES
    "msx": "Microsoft MSX",
    "msx2": "Microsoft MSX2",
    "pcfx": None,  # placeholder en SYSTEMS, 0 filas reales en ROMs/RELEASES
}

CSV_COLUMNS = [
    "releaseTitleName",
    "releaseDeveloper",
    "releasePublisher",
    "releaseGenre",
    "releaseDate",
    "romFileName",
    "romHashCRC",
    "romHashMD5",
    "romHashSHA1",
]


def connect(db_path: Path) -> sqlite3.Connection:
    if not db_path.is_file():
        sys.exit(
            f"No se encuentra la base de datos en: {db_path}\n"
            "Descargar de https://github.com/OpenVGDB/OpenVGDB/releases/latest y pasar --db a la ruta del .sqlite."
        )
    return sqlite3.connect(str(db_path))


def list_systems(con: sqlite3.Connection) -> None:
    cur = con.execute("SELECT systemID, systemName FROM SYSTEMS ORDER BY systemName")
    for sid, name in cur.fetchall():
        print(f"{sid}\t{name}")


def resolve_system_id(con: sqlite3.Connection, system_id: str) -> int:
    if system_id not in PLATFORM_MAP:
        sys.exit(
            f"Sistema '{system_id}' no está en PLATFORM_MAP. "
            "Comprueba el id contra docs/systems.md y añádelo, verificando el nombre real con --list-systems."
        )
    name = PLATFORM_MAP[system_id]
    if name is None:
        sys.exit(f"Sistema '{system_id}' no tiene systemID equivalente en OpenVGDB (ver comentario en PLATFORM_MAP).")
    row = con.execute("SELECT systemID FROM SYSTEMS WHERE systemName = ?", (name,)).fetchone()
    if row is None:
        sys.exit(f"'{name}' no se encuentra en la tabla SYSTEMS de esta base -- ¿versión distinta a la verificada (v29.0)?")
    return row[0]


def fetch_games(con: sqlite3.Connection, system_id: int) -> list[sqlite3.Row]:
    con.row_factory = sqlite3.Row
    query = f"""
        SELECT {', '.join(CSV_COLUMNS)}
        FROM RELEASES
        JOIN ROMs ON RELEASES.romID = ROMs.romID
        WHERE ROMs.systemID = ?
        ORDER BY releaseTitleName
    """
    return con.execute(query, (system_id,)).fetchall()


def write_csv(rows: list[sqlite3.Row], output: Path | None) -> None:
    stream = open(output, "w", newline="", encoding="utf-8") if output else sys.stdout
    try:
        writer = csv.writer(stream)
        writer.writerow(CSV_COLUMNS)
        for row in rows:
            writer.writerow([row[c] for c in CSV_COLUMNS])
    finally:
        if output:
            stream.close()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--db", type=Path, required=True, help="Ruta al openvgdb.sqlite descargado")
    parser.add_argument("--system", help="Identificador canónico (docs/systems.md)")
    parser.add_argument("--system-id", type=int, help="systemID numérico de OpenVGDB (evita el mapeo)")
    parser.add_argument("--list-systems", action="store_true", help="Lista todos los systemID+nombre y sale")
    parser.add_argument("--output", type=Path, help="Fichero CSV de salida (por defecto: stdout)")
    args = parser.parse_args()

    con = connect(args.db)

    if args.list_systems:
        list_systems(con)
        return

    if not args.system and args.system_id is None:
        parser.error("--system o --system-id es obligatorio salvo con --list-systems")

    system_id = args.system_id if args.system_id is not None else resolve_system_id(con, args.system)
    rows = fetch_games(con, system_id)
    write_csv(rows, args.output)
    print(f"{len(rows)} juegos para systemID={system_id}", file=sys.stderr)


if __name__ == "__main__":
    main()
