#!/usr/bin/env python3
"""
Equivalente Python de build-dat-index-redump.ps1 (pensado para ejecutarse
desde el devcontainer). Misma logica, misma salida esperada; ver la
cabecera de build-dat-index-redump.ps1 para la descripcion completa del
proposito (agrupacion por clonelist ya que Redump no tiene cloneofid,
languages/members[]/revision/version/isAlt por-clon, validacion posterior
opcional contra retool-clonelists-metadata).

Nota sobre "misma salida esperada": el contenido es equivalente, verificado
comparando recuentos y muestras contra el .ps1; el JSON en si NO es
byte-identico (ver build-dat-index-nointro.py sobre orden ordinal vs
cultural al ordenar cadenas).

Uso:
    python tools/scripts/build-dat-index-redump.py
    python tools/scripts/build-dat-index-redump.py --system-id psx
"""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
REPO_ROOT = SCRIPT_DIR.parent.parent

DAT_ROOT = REPO_ROOT / "metadata" / "dat"
OUTPUT_ROOT = REPO_ROOT / "metadata" / "dat-index"
ALIAS_ROOT = OUTPUT_ROOT / "aliases"
DEBUG_ROOT = OUTPUT_ROOT / "debug"
CLONELIST_ROOT = DAT_ROOT / "retool" / "clonelists"
METADATA_ROOT = DAT_ROOT / "retool" / "metadata"

# Exclusiones GLOBALES: patrones de revista/cheats/demo que se repiten
# entre varios sistemas Redump (van pegados al titulo, no como tag entre
# parentesis, por lo que el descarte por tag no los detecta).
GLOBAL_TITLE_EXCLUSIONS = [
    r"\bDemo\b", "Not for Sale", "Non-Sell", "Action Replay", "GameShark",
    "CodeBreaker", "Xploder", "Famitsu", r"\bPreview\b", r"\bPromotion\b",
    r"\bKiosk\b", r"\bTrial\b", r"\bSample\b", r"\bBeta\b",
]


def join_title_exclusions(specific: list[str]) -> str:
    return "|".join(GLOBAL_TITLE_EXCLUSIONS + specific)


# Exclusiones especificas de PSX: series retail que requieren periferico
# especifico para jugarse (ej. Kids Station), y marcas de revista/cheats
# propias de PSX (ver GLOBAL_TITLE_EXCLUSIONS para las comunes).
PSX_SPECIFIC_EXCLUSIONS = join_title_exclusions([
    "Interactive CD Sampler", "PlayStation Underground", "Jampack",
    r"Official.*PlayStation Magazine", r"PSi\d?", "OPSM", "GSi", "M6 PlayStation",
    "Planet PSX", "Pocket PowerStation", "PlayStation Zone", "PlayMag", "Joypad Demo",
    "Screen Attack", "Gratis! Demo Disc", "Taikenban", "体験版", "店頭体験版",
    "Plus Yuu", "Import Player", "PS-X-Change",
    "Equalizer Game Wizard", "Power Play for PlayStation", "Gamebuster",
    "HMV CodeBuster", "GT Circuit Breaker", "Best Cheats in the World",
    "Hackerz", "EQ One", "Dance-UK", "Official UK PlayStation Best Games Ever",
    "Kids Station", "Tech PlayStation", "Dengeki PlayStation",
    "Memory Card Data Base", "Interactive Drive", "Lawson Special",
])

# Exclusiones especificas de Amiga CD32: marcas de revista/coverdisc
# propias de este sistema.
AMIGA_CD32_SPECIFIC_EXCLUSIONS = join_title_exclusions([
    "CD32 Gamer", "Amiga CD32 Gamer", "CD Exchange", "Amiga CD32 Magazine",
])

# Exclusiones especificas de Xbox: marcas de revista/coverdisc propias.
XBOX_SPECIFIC_EXCLUSIONS = join_title_exclusions([
    "Official Xbox Magazine", "Official Xbox Best Ever Games",
    "Official Xbox Starter Pack", "Official Xbox 50 Best Games",
    "Official Xbox Live Disc", r"Best Xbox.*Game Disc",
    "Xbox Playable Starter Pack", "Dance-UK",
])

# Resto de sistemas Redump: solo exclusiones globales (sin marcas
# especificas identificadas todavia). Ampliar si se detectan casos.
DEFAULT_TITLE_EXCLUSIONS = join_title_exclusions([])

# id -> {"dat": "<nombre de fichero>.dat", "clonelist": "<nombre en metadata/dat/retool/clonelists/>.json" (opcional), "title_exclusions": "<regex>" (opcional)}
DAT_MAP = {
    "gamecube": {"dat": "Nintendo - GameCube - Datfile (2019) (2026-06-13 18-14-01).dat", "clonelist": "Nintendo - GameCube (Redump).json", "title_exclusions": DEFAULT_TITLE_EXCLUSIONS},
    "wii": {"dat": "Nintendo - Wii - Datfile (3780) (2026-06-15 03-13-28).dat", "clonelist": "Nintendo - Wii (Redump).json", "title_exclusions": DEFAULT_TITLE_EXCLUSIONS},
    "segacd": {"dat": "Sega - Mega CD & Sega CD - Datfile (549) (2026-05-28 18-06-58).dat", "clonelist": "Sega - Mega CD & Sega CD (Redump).json", "title_exclusions": DEFAULT_TITLE_EXCLUSIONS},
    "saturn": {"dat": "Sega - Saturn - Datfile (2457) (2026-06-14 12-36-08).dat", "clonelist": "Sega - Saturn (Redump).json", "title_exclusions": DEFAULT_TITLE_EXCLUSIONS},
    "dreamcast": {"dat": "Sega - Dreamcast - Datfile (1516) (2026-06-14 18-25-41).dat", "clonelist": "Sega - Dreamcast (Redump).json", "title_exclusions": DEFAULT_TITLE_EXCLUSIONS},
    "psx": {"dat": "Sony - PlayStation - Datfile (10914) (2026-06-15 11-55-46).dat", "clonelist": "Sony - PlayStation (Redump).json", "title_exclusions": PSX_SPECIFIC_EXCLUSIONS},
    "ps2": {"dat": "Sony - PlayStation 2 - Datfile (11774) (2026-06-15 03-41-38).dat", "clonelist": "Sony - PlayStation 2 (Redump).json", "title_exclusions": DEFAULT_TITLE_EXCLUSIONS},
    "jaguarcd": {"dat": "Atari - Jaguar CD Interactive Multimedia System - Datfile (38) (2026-04-03 15-50-49).dat", "title_exclusions": DEFAULT_TITLE_EXCLUSIONS},
    "pcenginecd": {"dat": "NEC - PC Engine CD & TurboGrafx CD - Datfile (551) (2026-06-14 14-24-19).dat", "clonelist": "NEC - PC Engine CD & TurboGrafx CD (Redump).json", "title_exclusions": DEFAULT_TITLE_EXCLUSIONS},
    "3do": {"dat": "Panasonic - 3DO Interactive Multiplayer - Datfile (672) (2026-06-09 14-48-47).dat", "clonelist": "Panasonic - 3DO Interactive Multiplayer (Redump).json", "title_exclusions": DEFAULT_TITLE_EXCLUSIONS},
    "amigacdtv": {"dat": "Commodore - Amiga CDTV - Datfile (61) (2026-05-16 20-58-08).dat", "clonelist": "Commodore - Amiga CD (Redump).json", "title_exclusions": DEFAULT_TITLE_EXCLUSIONS},
    "amigacd32": {"dat": "Commodore - Amiga CD32 - Datfile (207) (2026-05-08 20-54-04).dat", "clonelist": "Commodore - Amiga CD32 (Redump).json", "title_exclusions": AMIGA_CD32_SPECIFIC_EXCLUSIONS},
    "xbox": {"dat": "Microsoft - Xbox - Datfile (2683) (2026-06-14 23-43-27).dat", "clonelist": "Microsoft - Xbox (Redump).json", "title_exclusions": XBOX_SPECIFIC_EXCLUSIONS},
    "neogeocd": {"dat": "SNK - Neo Geo CD - Datfile (111) (2026-05-06 12-21-03).dat", "title_exclusions": DEFAULT_TITLE_EXCLUSIONS},
}

# Tokens de region reconocidos por la convencion No-Intro/Redump (lista cerrada).
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

# Idioma por defecto SOLO para regiones con un idioma dominante razonable -
# mismo mapa ya validado en build-dat-index-nointro.py.
REGION_LANGUAGE_DEFAULTS = {
    "Argentina": "Es", "Australia": "En", "Austria": "De", "Brazil": "Pt",
    "Bulgaria": "Bg", "Canada": "En", "Chile": "Es", "China": "Zh",
    "Colombia": "Es", "Croatia": "Hr", "Czechia": "Cs", "Denmark": "Da",
    "Egypt": "Ar", "Europe": "En", "Finland": "Fi", "France": "Fr", "Germany": "De",
    "Greece": "El", "Hong Kong": "Zh", "Hungary": "Hu", "India": "En",
    "Indonesia": "Id", "Iran": "Fa", "Iraq": "Ar", "Ireland": "En",
    "Israel": "He", "Italy": "It", "Japan": "Ja", "Korea": "Ko",
    "Latin America": "Es", "Mexico": "Es", "Netherlands": "Nl",
    "New Zealand": "En", "Norway": "No", "Peru": "Es", "Poland": "Pl",
    "Portugal": "Pt", "Romania": "Ro", "Russia": "Ru", "Saudi Arabia": "Ar",
    "Slovakia": "Sk", "South Africa": "En", "Spain": "Es", "Sweden": "Sv",
    "Taiwan": "Zh", "Turkey": "Tr", "UAE": "Ar", "United Kingdom": "En",
    "USA": "En", "Vietnam": "Vi", "World": "En", "Unknown": "En",
}

DISCARD_TAGS = [
    "Proto", "Demo", "Special Demo", "Trial", "Beta", "Sample", "Kiosk",
    "Test Program", "Program", "BIOS", "DLC", "Update", "System Application",
    "System Module", "E3 Video", "Nintendo 3DS Conference", "Shared Data Archive",
]
FLAG_TAGS = ["Aftermarket", "Compilation", "Unl", "Pirate"]

PAREN_GROUP_RE = re.compile(r"\(([^()]*)\)")
ALL_GROUP_RE = re.compile(r"[(\[]([^)\]]*)[)\]]")
STRIP_GROUP_RE = re.compile(r"\s*[(\[][^)\]]*[)\]]")
TRAILING_NUMBER_RE = re.compile(r"\s+\d+$")
LANGUAGE_CODE_RE = re.compile(r"^[A-Z][a-z]$")
REVISION_RE = re.compile(r"\(Rev ([^)]+)\)", re.IGNORECASE)
VERSION_RE = re.compile(r"\(v([\d.]+[A-Za-z]?)\)", re.IGNORECASE)
ALT_RE = re.compile(r"\(Alt(?:\s*\d*)?\)", re.IGNORECASE)


def get_paren_groups(name: str) -> list[str]:
    return PAREN_GROUP_RE.findall(name)


def get_regions(name: str) -> list[str]:
    for group in get_paren_groups(name):
        tokens = [t.strip() for t in re.split(r"[,+]", group)]
        matched = [t for t in tokens if t in KNOWN_REGIONS]
        if matched:
            return matched
    return []


def get_language_for_regions(regions: list[str]) -> list[str]:
    for region in regions:
        if region in REGION_LANGUAGE_DEFAULTS:
            return [REGION_LANGUAGE_DEFAULTS[region]]
    return []


def get_languages(name: str) -> list[str]:
    """Misma convencion que No-Intro (docs/references.md#redump): el
    grupo de idiomas es una lista separada por comas de codigos de 2
    letras que aparece INMEDIATAMENTE despues del grupo de region
    reconocido."""
    groups = get_paren_groups(name)
    for i, group in enumerate(groups):
        tokens = [t.strip() for t in re.split(r"[,+]", group)]
        is_region_group = any(t in KNOWN_REGIONS for t in tokens)
        if not is_region_group or i + 1 >= len(groups):
            continue
        next_tokens = [t.strip() for t in groups[i + 1].split(",")]
        if next_tokens and all(LANGUAGE_CODE_RE.match(t) for t in next_tokens):
            return next_tokens
    return []


def resolve_languages(full_name: str, regions: list[str]) -> tuple[list[str], str]:
    """Cadena de relleno propia (SIN retool-clonelists-metadata - ver
    build_system_index para el papel de retool ahora, capa de validacion
    posterior, no de relleno): 1) deteccion por nombre, 2) default por
    region."""
    by_name = get_languages(full_name)
    if by_name:
        return by_name, "name"
    by_region = get_language_for_regions(regions)
    if by_region:
        return by_region, "region-default"
    return [], "none"


def get_revision(name: str) -> str | None:
    match = REVISION_RE.search(name)
    return match.group(1) if match else None


def get_version(name: str) -> str | None:
    match = VERSION_RE.search(name)
    return match.group(1) if match else None


def test_is_alt(name: str) -> bool:
    return bool(ALT_RE.search(name))


def get_base_name(name: str) -> str:
    return STRIP_GROUP_RE.sub("", name).strip()


def get_all_groups(name: str) -> list[str]:
    return ALL_GROUP_RE.findall(name)


def test_tag_match(group: str, tag_list: list[str]) -> bool:
    normalized = TRAILING_NUMBER_RE.sub("", group).strip()
    return any(tag.lower() == normalized.lower() for tag in tag_list)


def get_discard_reason(name: str, roms: list[ET.Element], title_exclusion_regex: str | None) -> str | None:
    for group in get_all_groups(name):
        if test_tag_match(group, DISCARD_TAGS):
            return TRAILING_NUMBER_RE.sub("", group).strip()
    if title_exclusion_regex and re.search(title_exclusion_regex, name):
        return "revista/cheats"
    if any(rom.get("status") == "baddump" for rom in roms):
        return "baddump"
    return None


def get_category(name: str) -> str:
    for group in get_all_groups(name):
        if test_tag_match(group, FLAG_TAGS):
            return TRAILING_NUMBER_RE.sub("", group).strip()
    return "Oficial"


def get_clonelist_map(path: Path | None) -> dict[str, str]:
    result: dict[str, str] = {}
    if not path or not path.is_file():
        return result
    data = json.loads(path.read_text(encoding="utf-8"))
    for variant in data.get("variants", []):
        group = variant.get("group")
        for title in variant.get("titles", []):
            search_term = title.get("searchTerm")
            if search_term:
                result[search_term] = group
    return result


def get_language_map(path: Path | None) -> dict[str, list[str]]:
    """OPCIONAL y usado DESPUES del calculo propio - no rellena languages,
    solo sirve para detectar divergencias (ver debug/<id>-language-diff.json
    en build_system_index)."""
    result: dict[str, list[str]] = {}
    if not path or not path.is_file():
        return result
    data = json.loads(path.read_text(encoding="utf-8"))
    for name, entry in data.items():
        if not isinstance(entry, dict):
            continue
        languages = entry.get("languages")
        if languages:
            result[name] = languages
    return result


def write_json_file(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def new_empty_family(canonical_name: str) -> dict:
    return {
        "canonical_name": canonical_name,
        "alias_names": set(),
        "regions": set(),
        "languages": set(),
        "categories": set(),
        "members": [],
    }


def build_system_index(system_id: str, entry: dict) -> None:
    dat_path = DAT_ROOT / "Redump" / entry["dat"]
    if not dat_path.is_file():
        print(f"ADVERTENCIA: DAT no encontrado para '{system_id}': {dat_path}")
        return

    games = ET.parse(dat_path).getroot().findall("game")
    if not games:
        print(f"ADVERTENCIA: Sin elementos <game> en '{system_id}': {dat_path}")
        return

    clonelist_name = entry.get("clonelist")
    clonelist_path = CLONELIST_ROOT / clonelist_name if clonelist_name else None
    clonelist_map = get_clonelist_map(clonelist_path)
    clonelist_hits = 0

    # Mismo nombre de fichero que el clonelist, en metadata/ en vez de
    # clonelists/ (mismo patron, verificado sobre todos los sistemas
    # mapeados en DAT_MAP). Solo validacion posterior, ver paso final.
    language_map_path = METADATA_ROOT / clonelist_name if clonelist_name else None
    language_map = get_language_map(language_map_path)

    families: dict[str, dict] = {}
    discarded_log: list[dict] = []
    accepted_log: list[str] = []

    for game in games:
        full_name = game.get("name")
        if not full_name:
            continue

        reason = get_discard_reason(full_name, game.findall("rom"), entry.get("title_exclusions"))
        if reason:
            discarded_log.append({"name": full_name, "reason": reason})
            continue
        accepted_log.append(full_name)

        base_name = get_base_name(full_name)
        if not base_name:
            continue

        regions = get_regions(full_name)
        languages, language_source = resolve_languages(full_name, regions)
        category = get_category(full_name)

        canonical_key = base_name
        if base_name in clonelist_map:
            canonical_key = clonelist_map[base_name]
            clonelist_hits += 1

        if canonical_key not in families:
            families[canonical_key] = new_empty_family(canonical_key)
        family = families[canonical_key]
        if base_name != family["canonical_name"]:
            family["alias_names"].add(base_name)
        family["regions"].update(regions)
        family["languages"].update(languages)
        family["categories"].add(category)
        family["members"].append({
            "name": full_name,
            "origin": "redump",
            "regions": sorted(regions),
            "languages": sorted(languages),
            "languageSource": language_source,
            "category": category,
            "revision": get_revision(full_name),
            "version": get_version(full_name),
            "isAlt": test_is_alt(full_name),
        })

    # Fichero de alias manual: fusion igual que build-dat-index-nointro.py.
    alias_path = ALIAS_ROOT / f"{system_id}.json"
    manual_aliases = []
    if alias_path.is_file():
        existing = json.loads(alias_path.read_text(encoding="utf-8"))
        manual_aliases = existing.get("aliases", [])

    family_by_canonical = {f["canonical_name"]: f for f in families.values()}

    for manual_entry in manual_aliases:
        canonical = manual_entry.get("canonical")
        if canonical not in family_by_canonical:
            print(
                f"ADVERTENCIA: Alias manual en '{system_id}' referencia un nombre canonico no "
                f"encontrado en el DAT: '{canonical}' (se ignora)"
            )
            continue
        target_family = family_by_canonical[canonical]
        for alias_name in manual_entry.get("aliases", []):
            if alias_name == canonical:
                continue
            target_family["alias_names"].add(alias_name)

            if alias_name in family_by_canonical and family_by_canonical[alias_name] is not target_family:
                other_family = family_by_canonical[alias_name]
                target_family["alias_names"].update(other_family["alias_names"])
                target_family["regions"].update(other_family["regions"])
                target_family["languages"].update(other_family["languages"])
                target_family["categories"].update(other_family["categories"])
                target_family["members"].extend(other_family["members"])
                target_family["alias_names"].add(alias_name)
                family_by_canonical[alias_name] = target_family
                for key in [k for k, v in families.items() if v is other_family]:
                    del families[key]

    games_out = []
    for family in sorted(families.values(), key=lambda f: f["canonical_name"]):
        categories = family["categories"]
        final_category = "Oficial" if "Oficial" in categories else ", ".join(sorted(categories))
        games_out.append({
            "name": family["canonical_name"],
            "aliases": sorted(family["alias_names"]),
            "regions": sorted(family["regions"]),
            "languages": sorted(family["languages"]),
            "properties": {"category": final_category},
            "members": sorted(family["members"], key=lambda m: m["name"]),
        })

    output = {
        "system": system_id,
        "source": "Redump",
        "dat": entry["dat"],
        "generated": date.today().isoformat(),
        "games": games_out,
    }
    write_json_file(OUTPUT_ROOT / f"{system_id}.json", output)

    aliases_out = [
        {"canonical": f["canonical_name"], "aliases": sorted(f["alias_names"])}
        for f in sorted(families.values(), key=lambda f: f["canonical_name"])
        if f["alias_names"]
    ]
    write_json_file(alias_path, {"system": system_id, "aliases": aliases_out})

    write_json_file(
        DEBUG_ROOT / f"{system_id}.json",
        {
            "system": system_id,
            "discarded": sorted(discarded_log, key=lambda d: d["name"]),
            "accepted": sorted(accepted_log),
        },
    )

    if clonelist_path:
        coverage = round(100 * clonelist_hits / len(accepted_log), 1) if accepted_log else 0
        clonelist_note = f"clonelist: {clonelist_hits}/{len(accepted_log)} aceptados ({coverage}%)"
    else:
        clonelist_note = "sin clonelist"

    # Validacion de idioma contra retool-clonelists-metadata: capa OPCIONAL
    # y POSTERIOR al calculo propio - "nolang" es un marcador especial de
    # retool ("sin contenido de texto", no un idioma real), se excluye de
    # la comparacion (ver mismo criterio en build-dat-index-nointro.py).
    language_note = "sin metadata idioma"
    if language_map:
        lang_diffs = []
        for family in families.values():
            for member in family["members"]:
                if member["name"] not in language_map:
                    continue
                retool_languages = sorted(language_map[member["name"]])
                if "nolang" in retool_languages:
                    continue
                computed_languages = sorted(member["languages"])
                if retool_languages != computed_languages:
                    lang_diffs.append({
                        "name": member["name"],
                        "computedLanguages": computed_languages,
                        "computedSource": member["languageSource"],
                        "retoolLanguages": retool_languages,
                    })
        if lang_diffs:
            write_json_file(
                DEBUG_ROOT / f"{system_id}-language-diff.json",
                {
                    "system": system_id,
                    "metadata": language_map_path.name if language_map_path else None,
                    "diffs": sorted(lang_diffs, key=lambda d: d["name"]),
                },
            )
        language_note = f"idioma: {len(lang_diffs)} divergencias"

    print(
        f"Generado: {system_id}.json ({len(games_out)} familias, {len(discarded_log)} descartados) "
        f"+ aliases/{system_id}.json ({len(aliases_out)} con alias) [{clonelist_note}] [{language_note}]"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--system-id", dest="system_id", default=None)
    args = parser.parse_args()

    ids = [args.system_id] if args.system_id else list(DAT_MAP.keys())

    for system_id in ids:
        if system_id not in DAT_MAP:
            print(f"ADVERTENCIA: Sistema no mapeado: {system_id}")
            continue
        build_system_index(system_id, DAT_MAP[system_id])


if __name__ == "__main__":
    main()
