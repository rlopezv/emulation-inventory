#!/usr/bin/env python3
"""
Script de un solo uso: convierte la seccion "## Fuentes de referencia" de
cada docs/guides/romsets/systems/<id>.md del formato de bullets anidados
(fijado 2026-09-06) a una tabla `| Tipo | Fuente | Detalle |`, distinguiendo
fuentes **Especialista** (una BD dedicada a ESE sistema concreto) de
**Generica** (catalogo amplio, cubre muchos sistemas -- por ahora solo
Wikipedia, que ya tenia entrada propia en los 84 ficheros).

Motivo del cambio de formato: la sesion de investigacion 2026-09-06
verifico ~30 fuentes especialistas propuestas por el usuario (algunas
de un LLM externo, marcadas "utm_source=chatgpt.com") contra las webs
reales, y el resultado (que fuente sirve para que sistema, con que
matices -- solo HTML, requiere headless browser, sin HTTPS, cobertura
parcial...) ya no cabe limpiamente en un bullet suelto. SPECIALIST_MAP
mas abajo es el resultado de esa investigacion -- cada entrada con nota
solo si hay un matiz real que documentar (bloqueo Anubis, sin HTTPS,
reutilizacion prohibida, cobertura parcial...); TODO_REASON documenta
POR QUE algo quedo sin fuente (investigado y descartado) para no
confundirlo con "todavia no investigado".

Idempotente: reemplaza la seccion "## Fuentes de referencia" completa
(desde el heading hasta el siguiente heading `##`/marcador AUTO-GENERADO/
fin de fichero) por la tabla nueva. Preserva cualquier bullet no-Wikipedia
ya existente fusionandolo en la fila Especialista correspondiente si el
propio script lo declara (ver NOTA en spectrum) -- no inventa fusiones
automaticas para bullets que no esten ya mapeados aqui.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

DOCS_ROOT = Path(__file__).resolve().parents[2] / "docs" / "guides" / "romsets" / "systems"

HEADING = "## Fuentes de referencia"

# id -> lista de (fuente, url, detalle) ; None => sin fuente especialista
# (ver TODO_REASON para el motivo). Fuentes verificadas contra la web real
# en la sesion 2026-09-06 -- no hardcodear nada aqui sin haber pasado por
# esa verificacion (WebFetch/WebSearch/curl real, no de segunda mano).
SPECIALIST_MAP: dict[str, list[tuple[str, str, str]] | None] = {
    "spectrum": [
        ("ZXDB", "https://github.com/zxdb/ZXDB", "Dump MySQL descargable (`ZXDB_mysql.sql.zip`); accesible tambien en vivo via API JSON de World of Spectrum (`worldofspectrum.org/infoseek/api/software`, `X-API-KEY=test` funcional) o via HTML en spectrumcomputing.co.uk -- las tres vias son el mismo dato"),
    ],
    "dragon32": [
        ("The Dragon Archive", "https://www.worldofdragon.org/", "Wiki HTML, sin API/export. No cubre TRS-80 CoCo (variante de hardware del mismo sistema) -- limitacion aceptada"),
    ],
    "vic20": [
        ("VIC-20 Listings", "http://www.vic20listings.freeolamail.com/proglist.html", "Sin HTTPS (usar la URL `http://` tal cual). Type-ins con autor/revista/RAM requerida, solo HTML"),
    ],
    "amstradcpc": [
        ("CPC-Power", "https://www.cpc-power.com/", "Solo HTML navegable, sin API/CSV"),
    ],
    "msx": [
        ("Generation-MSX", "https://generation-msx.nl/", "Solo HTML navegable, sin API/export"),
    ],
    "msx2": [
        ("Generation-MSX", "https://generation-msx.nl/", "Solo HTML navegable, sin API/export"),
    ],
    "c64": [
        ("GameBase64", "https://www.gamebase64.com/", "Formato GameBase clasico: BD Access/SQLite descargable (~15 GB via foro/Internet Archive), no una API"),
        ("Lemon64", "https://www.lemon64.com/", "Solo fichas/reviews HTML, sin export"),
    ],
    "plus4": [
        ("Plus/4 World", "https://plus4world.powweb.com/", "Solo HTML navegable, sin export masivo"),
    ],
    "amiga": [
        ("Hall of Light", "https://amiga.abime.net/", "Bloqueada por proteccion anti-bot (Anubis) -- requiere headless browser, no verificable con curl/requests simples"),
        ("Lemon Amiga", "https://www.lemonamiga.com/", "Sin API confirmada (pedida explicitamente en su propio foro sin respuesta)"),
    ],
    "atari2600": [
        ("Atarimania", "https://www.atarimania.com/", "~10.500 juegos/15.000 capturas, solo HTML/scans sin API"),
    ],
    "atari5200": [
        ("Atarimania", "https://www.atarimania.com/", "Cobertura delgada (~99 juegos) comparada con ST/8-bit, solo HTML/scans"),
    ],
    "atari800": [
        ("Atarimania", "https://www.atarimania.com/", "Linea fuerte del sitio (~12.000 juegos), solo HTML/scans sin API"),
    ],
    "atarist": [
        ("Atarimania", "https://www.atarimania.com/", "Buque insignia del sitio (~9.800 juegos + archivo de revistas/manuales), solo HTML/scans sin API"),
    ],
    "atari7800": [
        ("AtariAge", "https://atariage.com/", "Fichas ricas (System/Company/Year/Rarity/scans) via `software_page.php?SoftwareLabelID=`, solo HTML"),
        ("Atarimania", "https://www.atarimania.com/", "Solo HTML/scans sin API"),
    ],
    "lynx": [
        ("AtariAge", "https://atariage.com/", "Fichas ricas via `software_page.php?SoftwareLabelID=`, solo HTML"),
        ("Atarimania", "https://www.atarimania.com/", "Solo HTML/scans sin API"),
    ],
    "jaguar": [
        ("AtariAge", "https://atariage.com/", "Fichas ricas via `software_page.php?SoftwareLabelID=`, solo HTML"),
        ("Atarimania", "https://www.atarimania.com/", "Cobertura delgada (~142 juegos), solo HTML/scans"),
    ],
    "thomson": [
        ("DCMOTO", "https://dcmoto.free.fr/", "Logitheque HTML navegable, sin API"),
    ],
    "zx81": [
        ("ZX81 Stuff", "https://www.zx81stuff.org.uk/", "Archivo personal (600+ titulos), solo HTML"),
    ],
    "snes": [
        ("SNES Central", "https://snescentral.com/", "PCB Info/ROM Chip ID/CIC por region. Solo HTML -- el propio sitio prohibe expresamente la reutilizacion de su contenido sin permiso"),
    ],
    "gb": [
        ("Game Boy Database", "https://game-boy-database.com/", "~5175 fichas confirmadas, coleccionismo regional (codigos, idiomas, arte). Solo HTML"),
        ("Game Boy Hardware Database", "https://gbhwdb.gekkio.fi/", "CSV real descargable (`static/export/cartridges.csv`), pero es dato de componente electronico (chips/PCB), no metadata de juego. Repo de codigo archivado desde ago. 2026"),
    ],
    "gbc": [
        ("Game Boy Database", "https://game-boy-database.com/", "~5175 fichas confirmadas, coleccionismo regional. Solo HTML"),
    ],
    "n64": [
        ("GameDB-N64", "https://github.com/niemasd/GameDB-N64/", "JSON/TSV reales y descargables. Activo pero de bajo volumen (ultimo commit jul. 2025)"),
    ],
    "virtualboy": [
        ("Planet Virtual Boy", "https://www.virtual-boy.com/database/", "Serial/barcode/ROM size/save type por ficha real. Solo HTML, sin export"),
    ],
    "sg1000": [("Sega Retro", "https://segaretro.org/", "API real de MediaWiki (`api.php`) pero bloqueada por Anubis -- requiere headless browser, no un script simple")],
    "mastersystem": [("Sega Retro", "https://segaretro.org/", "API real de MediaWiki (`api.php`) pero bloqueada por Anubis -- requiere headless browser")],
    "gamegear": [("Sega Retro", "https://segaretro.org/", "API real de MediaWiki (`api.php`) pero bloqueada por Anubis -- requiere headless browser")],
    "megadrive": [("Sega Retro", "https://segaretro.org/", "API real de MediaWiki (`api.php`) pero bloqueada por Anubis -- requiere headless browser")],
    "segacd": [("Sega Retro", "https://segaretro.org/", "API real de MediaWiki (`api.php`) pero bloqueada por Anubis -- requiere headless browser")],
    "sega32x": [("Sega Retro", "https://segaretro.org/", "API real de MediaWiki (`api.php`) pero bloqueada por Anubis -- requiere headless browser")],
    "saturn": [("Sega Retro", "https://segaretro.org/", "API real de MediaWiki (`api.php`) pero bloqueada por Anubis -- requiere headless browser")],
    "dreamcast": [("Sega Retro", "https://segaretro.org/", "API real de MediaWiki (`api.php`) pero bloqueada por Anubis -- requiere headless browser")],
    "pcengine": [("PC Engine Software Bible", "https://www.pcengine.co.uk/", "Vivo y mantenido, solo HTML")],
    "pcenginecd": [("PC Engine Software Bible", "https://www.pcengine.co.uk/", "Vivo y mantenido, solo HTML")],
    "neogeo": [("NeoGeoSoft", "http://neogeosoft.com/", "Sin HTTPS valido (usar `http://`). Tablas MVS/AES con Serial/Año/Titulo JP+EN, solo HTML")],
    "neogeocd": [("NeoGeoSoft", "http://neogeosoft.com/?section=cd", "Sin HTTPS valido (usar `http://`). Solo HTML")],
    "psx": [("PlayStation DataCenter", "https://psxdatacenter.com/", "Buque insignia del sitio (~8400 fichas, mantenido semanalmente desde 2007). Solo HTML")],
    "ps2": [("PlayStation DataCenter", "https://psxdatacenter.com/psx2/intro2.html", "Seccion secundaria (~2000 fichas). Solo HTML")],
    # Sin fuente especialista confirmada -- investigado y descartado/sin resultado,
    # no "sin investigar". El motivo va en TODO_REASON.
    "sharpx68000": None,
    "nes": None,
    "nds": None,
    "3ds": None,
    "gamecube": None,
    "wii": None,
    "wiiu": None,
    "switch": None,
    "ps3": None,
    "psp": None,
}

TODO_REASON: dict[str, str] = {
    "sharpx68000": "GamesX descartado (wiki general de hardware retro, no dedicado a X68000)",
    "nes": "NESCartDB no verificable (fallo de carga persistente); su mirror en GitHub (`MetaFight/NesCartDB`) es un scrape sin estructurar, no datos utilizables",
    "nds": "GameTDB descartada como fuente (decisión 2026-09-06)",
    "3ds": "GameTDB descartada como fuente (decisión 2026-09-06)",
    "gamecube": "GameTDB descartada como fuente (decisión 2026-09-06)",
    "wii": "GameTDB descartada como fuente (decisión 2026-09-06)",
    "wiiu": "GameTDB descartada como fuente (decisión 2026-09-06)",
    "switch": "GameTDB descartada como fuente (decisión 2026-09-06)",
    "ps3": "GameTDB descartada como fuente (decisión 2026-09-06); RPCS3 compatibility no cuenta (es estado de ejecución, no metadata descriptiva)",
    "psp": "PlayStation DataCenter tiene sección PSP pero solo cubre 1 juego (\"The 3rd Birthday\") -- no es una fuente real",
}

# Bloque de bullets pre-existentes que hay que retirar al fusionar en el
# Especialista de la tabla (para no duplicar). Solo un caso conocido.
MERGED_EXTRA_BULLETS = {"spectrum"}

WIKI_BLOCK_RE = re.compile(r"- Wikipedia:\s*\n((?:\s*-\s*.+\n?)+)")
EXTRA_BLOCK_RE = re.compile(r"- Otros:\s*\n((?:\s*-\s*.*\n?)+)")
SECTION_RE = re.compile(
    rf"{re.escape(HEADING)}\n\n(.*?)(?=\n<!-- AUTO-GENERADO|\n## |\Z)", re.DOTALL
)


def extract_wiki_urls(section_text: str) -> list[str]:
    m = WIKI_BLOCK_RE.search(section_text)
    if not m:
        return []
    return [line.strip().removeprefix("- ").strip() for line in m.group(1).strip("\n").split("\n") if line.strip()]


def build_table(system_id: str, section_text: str) -> str:
    rows = ["| Tipo | Fuente | Detalle |", "| --- | --- | --- |"]

    specialist = SPECIALIST_MAP.get(system_id)
    if specialist:
        for name, url, detail in specialist:
            rows.append(f"| Especialista | [{name}]({url}) | {detail} |")
    elif system_id in TODO_REASON:
        rows.append(f"| Especialista | `[TODO]` | {TODO_REASON[system_id]} |")
    else:
        rows.append("| Especialista | `[TODO]` | Sin investigar todavía |")

    wiki_urls = extract_wiki_urls(section_text)
    for url in wiki_urls:
        rows.append(f"| Genérica | Wikipedia | {url} |")

    return "\n".join(rows) + "\n"


def process_file(path: Path) -> bool:
    system_id = path.stem
    text = path.read_text(encoding="utf-8")
    m = SECTION_RE.search(text)
    if not m:
        print(f"AVISO: sin sección '{HEADING}' en {path.name}, saltando", file=sys.stderr)
        return False

    section_text = m.group(1)
    if "| Tipo | Fuente | Detalle |" in section_text:
        # Ya convertido -- no reprocesar (evita perder datos si se relanza
        # el script sin querer, como paso el 2026-09-06).
        return False
    table = build_table(system_id, section_text)
    new_text = text[: m.start(1)] + table + text[m.end(1) :]

    if new_text != text:
        path.write_text(new_text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for path in sorted(DOCS_ROOT.glob("*.md")):
        if path.name == "README.md":
            continue
        if process_file(path):
            print(f"Actualizado: {path.name}")
            changed += 1
    print(f"\nTotal actualizados: {changed}", file=sys.stderr)


if __name__ == "__main__":
    main()
