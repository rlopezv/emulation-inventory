#!/usr/bin/env python3
"""
Equivalente Python de build-dat-index-nointro.ps1 (pensado para ejecutarse
desde el devcontainer). Misma logica, mismo manifiesto
(config/nointro-systems.json), misma salida esperada; ver la cabecera de
build-dat-index-nointro.ps1 para la descripcion completa del proposito, el
diseno full+aftermarket+pc/clonelist y los tres --source-mode.

Nota sobre "misma salida esperada": el contenido (familias, alias, regiones,
categorias, contraste, divergencias) es equivalente, verificado comparando
recuentos y muestras contra el .ps1; el JSON en si NO es byte-identico -
Python usa orden ordinal Unicode al ordenar cadenas (sorted()) y PowerShell
usa comparacion sensible a cultura (Sort-Object), lo que puede reordenar
ligeramente entradas con acentos/caracteres no ASCII.

Uso:
    python tools/scripts/build-dat-index-nointro.py
    python tools/scripts/build-dat-index-nointro.py --system-id nes
    python tools/scripts/build-dat-index-nointro.py --system-id nes --source-mode pc
    python tools/scripts/build-dat-index-nointro.py --system-id nes --source-mode merged
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
SOURCES_ROOT = REPO_ROOT / "sources" / "dats" / "no-intro"
OUTPUT_ROOT = REPO_ROOT / "metadata" / "dat-index"
ALIAS_ROOT = OUTPUT_ROOT / "aliases"
DEBUG_ROOT = OUTPUT_ROOT / "debug"
CLONELIST_ROOT = DAT_ROOT / "retool" / "clonelists"
METADATA_ROOT = DAT_ROOT / "retool" / "metadata"

MANIFEST_PATH = SCRIPT_DIR / "config" / "nointro-systems.json"

# Non-Redump: fuera del manifiesto de No-Intro (formato/paquete distinto),
# se mantienen con nombre de fichero exacto en metadata/dat/Non-Redump/.
NON_REDUMP_MAP = {
    "wiiu": "Non-Redump - Nintendo - Wii U (20260312-235110).dat",
    "ps3": "Non-Redump - Sony - PlayStation 3 (20250908-072347).dat",
    "psp": "Non-Redump - Sony - PlayStation Portable (20260421-200314).dat",
    "cdi": "Non-Redump - Philips - CD-i (20260429-044928).dat",
    "xbox360": "Non-Redump - Microsoft - Xbox 360 (20251219-035655).dat",
}

TIMESTAMP = r"\d{8}-\d{6}"

SOURCE_MODE_LABELS = {"fullaftermarket": "FullAftermarket", "pc": "Pc", "merged": "Merged"}

# Tokens de region reconocidos por la convencion No-Intro (lista cerrada).
# Auditada contra todos los DAT de No-Intro/Non-Redump (ver historial de
# build-dat-index-nointro): "United Kingdom" es el token real, no "UK".
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

# Idioma por defecto SOLO para regiones con un idioma dominante razonable
# (fallback de ultimo recurso, cuando la deteccion por nombre no dio idioma
# - ver get_language_for_regions). Region ausente de este mapa = sin
# default, no se inventa dato (ver CLAUDE.md "Do not invent data"): "Asia",
# "Belgium" (Fr/Nl oficiales), "Bangladesh", "Scandinavia", "Switzerland"
# (De/Fr/It oficiales) quedan fuera por ambiguedad real de idioma dominante.
# "Unknown" y "Europe" SI tienen default (En) - decision explicita del
# usuario: mejor asumir ingles que dejar el campo vacio.
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

# Tags que descartan la entrada por completo (proto/demo/no final).
DISCARD_TAGS = [
    "Proto", "Demo", "Special Demo", "Trial", "Beta", "Sample", "Kiosk",
    "Test Program", "Program", "BIOS", "DLC", "Update", "System Application",
    "System Module", "E3 Video", "Nintendo 3DS Conference", "Shared Data Archive",
    "Not For Sale",
]

# Tags que se conservan pero marcan la entrada como no oficial.
FLAG_TAGS = ["Aftermarket", "Compilation", "Unl", "Pirate", "NP"]

PAREN_GROUP_RE = re.compile(r"\(([^()]*)\)")
ALL_GROUP_RE = re.compile(r"[(\[]([^)\]]*)[)\]]")
STRIP_GROUP_RE = re.compile(r"\s*[(\[][^)\]]*[)\]]")
TRAILING_NUMBER_RE = re.compile(r"\s+\d+$")
CLONELIST_STRIP_LAST_GROUP_RE = re.compile(r"\s*\([^()]*\)$")
LANGUAGE_CODE_RE = re.compile(r"^[A-Z][a-z]$")
REVISION_RE = re.compile(r"\(Rev ([^)]+)\)", re.IGNORECASE)
VERSION_RE = re.compile(r"\(v([\d.]+[A-Za-z]?)\)", re.IGNORECASE)
ALT_RE = re.compile(r"\(Alt(?:\s*\d*)?\)", re.IGNORECASE)


def resolve_nointro_dat(base_name: str, pack: str, tag: str | None = None) -> Path | None:
    """Busca <base_name>[ <tag>] (<timestamp>).dat en el pack indicado
    (full/aftermarket/pc). Devuelve la ruta del fichero mas reciente que
    coincida, o None si el pack no tiene fichero para ese sistema."""
    suffix = f" ({tag})" if tag else ""
    escaped_base = re.escape(f"{base_name}{suffix}")
    pattern = re.compile(rf"^{escaped_base} \({TIMESTAMP}\)\.dat$")
    folder = SOURCES_ROOT / pack
    if not folder.is_dir():
        return None
    candidates = sorted(
        (p for p in folder.iterdir() if p.is_file() and pattern.match(p.name)),
        key=lambda p: p.name,
        reverse=True,
    )
    return candidates[0] if candidates else None


def resolve_retool_data_path(base_name: str, root: Path) -> Path | None:
    """El base_name del manifiesto incluye a veces un tag de formato que los
    ficheros de retool-clonelists-metadata no llevan (ej. "Atari - Atari
    Lynx (LYX)" -> "Atari - Atari Lynx (No-Intro).json"). Se prueba primero
    el nombre exacto y, si no existe, se reintenta quitando el ultimo grupo
    entre parentesis. Reutilizable para clonelists/ y metadata/ (mismo
    patron de nombre "<Sistema> (No-Intro).json" en ambas carpetas)."""
    candidates = [base_name]
    stripped = CLONELIST_STRIP_LAST_GROUP_RE.sub("", base_name)
    if stripped != base_name:
        candidates.append(stripped)
    for candidate in candidates:
        path = root / f"{candidate} (No-Intro).json"
        if path.is_file():
            return path
    return None


def resolve_clonelist_path(base_name: str) -> Path | None:
    return resolve_retool_data_path(base_name, CLONELIST_ROOT)


def resolve_metadata_path(base_name: str) -> Path | None:
    return resolve_retool_data_path(base_name, METADATA_ROOT)


def get_clonelist_map(path: Path | None) -> dict[str, str]:
    """searchTerm (nombre base tal como aparece en el DAT) -> group (nombre
    canonico curado por retool-clonelists-metadata)."""
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
    """nombre completo del <game> -> lista de codigos de idioma ("En","Fr"...)
    curados por retool-clonelists-metadata (metadata/dat/retool/metadata/).
    OPCIONAL y usado DESPUES del calculo propio (resolve_languages, cadena
    nombre+region) - no rellena el campo languages, solo sirve para
    detectar divergencias entre lo calculado y lo curado (ver paso 9 de
    build_system_index, debug/<id>-language-diff.json)."""
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


def get_paren_groups(name: str) -> list[str]:
    return PAREN_GROUP_RE.findall(name)


def get_revision(name: str) -> str | None:
    """Tag oficial de No-Intro para revisiones corregidas: "(Rev 1)",
    "(Rev A)". Devuelve la etiqueta cruda (ej. "1", "A"), o None si no hay
    tag."""
    match = REVISION_RE.search(name)
    return match.group(1) if match else None


def get_version(name: str) -> str | None:
    """Convencion de aftermarket/homebrew: "(v1.1)", "(v2.100)". Devuelve
    el numero crudo (ej. "1.1"), o None si no hay tag. Distinta de revision
    (No-Intro oficial) - no se mezclan, cada familia suele usar solo una."""
    match = VERSION_RE.search(name)
    return match.group(1) if match else None


def test_is_alt(name: str) -> bool:
    """Dump alternativo del mismo contenido: "(Alt)", "(Alt 2)". A
    despriorizar/excluir por defecto en una seleccion 1G1R."""
    return bool(ALT_RE.search(name))


def get_regions(name: str) -> list[str]:
    # Recorre los grupos entre parentesis en orden y usa el primero que
    # contenga al menos un token de region reconocido (no asume que sea
    # necesariamente el primer grupo del nombre; ej. "Zanac (AI) (Japan)").
    for group in get_paren_groups(name):
        tokens = [t.strip() for t in re.split(r"[,+]", group)]
        matched = [t for t in tokens if t in KNOWN_REGIONS]
        if matched:
            return matched
    return []


def get_languages(name: str) -> list[str]:
    # Convencion No-Intro: "Nombre (Region) (Idiomas) (...) (Revision)" - el
    # grupo de idiomas es una lista separada por comas de codigos de 2 letras
    # ("En","Fr","Es"...) que aparece INMEDIATAMENTE despues del grupo de
    # region reconocido. Se usa la posicion relativa a la region (no solo el
    # patron de 2 letras) para evitar falsos positivos - verificado: existen
    # grupos de 2 letras coincidentes con el patron pero que NO son idioma
    # cuando aparecen fuera de esa posicion (ej. "(Ge)" antes de la region en
    # un titulo de NES, no despues). Fuente primaria de la cadena de relleno
    # (ver resolve_languages) - get_language_map (retool) ya no rellena, es
    # una capa de validacion posterior (ver build_system_index paso 9).
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


def get_language_for_regions(regions: list[str]) -> list[str]:
    """Ultimo recurso: primera region (en el orden ya devuelto por
    get_regions/el mapa curado) que tenga un default razonable."""
    for region in regions:
        if region in REGION_LANGUAGE_DEFAULTS:
            return [REGION_LANGUAGE_DEFAULTS[region]]
    return []


def resolve_languages(full_name: str, regions: list[str]) -> tuple[list[str], str]:
    """Cadena de relleno propia (SIN retool-clonelists-metadata - ver
    build_system_index paso 9 para el papel de retool ahora, capa de
    validacion posterior, no de relleno): 1) deteccion por nombre
    (get_languages), 2) default por region (get_language_for_regions, solo
    regiones no ambiguas). Devuelve (languages, source) - source deja
    trazable que un idioma "region-default" es una inferencia, no un dato
    verificado."""
    by_name = get_languages(full_name)
    if by_name:
        return by_name, "name"
    by_region = get_language_for_regions(regions)
    if by_region:
        return by_region, "region-default"
    return [], "none"


def get_base_name(name: str) -> str:
    return STRIP_GROUP_RE.sub("", name).strip()


def get_all_groups(name: str) -> list[str]:
    return ALL_GROUP_RE.findall(name)


def test_tag_match(group: str, tag_list: list[str]) -> bool:
    normalized = TRAILING_NUMBER_RE.sub("", group).strip()
    return any(tag.lower() == normalized.lower() for tag in tag_list)


def get_discard_reason(name: str, roms: list[ET.Element]) -> str | None:
    """Devuelve el tag/motivo de descarte, o None si la entrada se conserva."""
    for group in get_all_groups(name):
        if test_tag_match(group, DISCARD_TAGS):
            return TRAILING_NUMBER_RE.sub("", group).strip()
    if any(rom.get("status") == "baddump" for rom in roms):
        return "baddump"
    return None


def get_category(name: str) -> str:
    for group in get_all_groups(name):
        if test_tag_match(group, FLAG_TAGS):
            return TRAILING_NUMBER_RE.sub("", group).strip()
    return "Oficial"


def get_root_id(key: str, lookup: dict, memo: dict[str, str]) -> str:
    if key in memo:
        return memo[key]
    visited: set[str] = set()
    current = key
    while True:
        if current in visited:
            break  # ciclo: cortamos aqui
        visited.add(current)
        node = lookup.get(current)
        clone_of = node.get("clone_of_id") if node else None
        if not node or not clone_of or clone_of not in lookup:
            break
        current = clone_of
    memo[key] = current
    return current


def write_json_file(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def parse_games(path: Path) -> list[ET.Element]:
    return ET.parse(path).getroot().findall("game")


def add_games_to_lookup(
    lookup: dict, discarded_log: list, accepted_log: list[str],
    path: Path | None, origin: str, system_id: str,
) -> None:
    """Parsea un DAT Logiqx (full/aftermarket) y anade sus <game> aceptados
    a lookup, namespaceando id/cloneofid por origin ("full"/"aftermarket")
    porque cada pack numera sus id desde 0001 por su cuenta (colision
    confirmada entre packs del mismo sistema: no son ids globales)."""
    if not path:
        return
    games = parse_games(path)
    if not games:
        print(f"ADVERTENCIA: Sin elementos <game> en '{system_id}' ({origin}): {path}")
        return
    for game in games:
        full_name = game.get("name")
        game_id = game.get("id")
        if not full_name or not game_id:
            continue

        reason = get_discard_reason(full_name, game.findall("rom"))
        if reason:
            discarded_log.append({"name": full_name, "reason": reason, "origin": origin})
            continue
        accepted_log.append(full_name)

        key = f"{origin}:{game_id}"
        clone_of_id = game.get("cloneofid")
        clone_of_key = f"{origin}:{clone_of_id}" if clone_of_id else None
        regions = get_regions(full_name)
        languages, language_source = resolve_languages(full_name, regions)
        lookup[key] = {
            "id": key,
            "clone_of_id": clone_of_key,
            "full_name": full_name,
            "base_name": get_base_name(full_name),
            "origin": origin,
            "regions": regions,
            "languages": languages,
            "language_source": language_source,
            "category": get_category(full_name),
            "revision": get_revision(full_name),
            "version": get_version(full_name),
            "is_alt": test_is_alt(full_name),
        }


def add_pc_games_to_lookup(
    lookup: dict, discarded_log: list, accepted_log: list[str],
    path: Path | None, system_id: str,
) -> None:
    """Parsea el pack pc/ (Parent-Clone): cloneof="<nombre completo del
    padre>", sin atributo id. Se usa el propio nombre completo como clave
    (unico dentro del DAT por construccion de No-Intro), asi get_root_id
    funciona sin cambios sobre este lookup igual que sobre el de
    full+aftermarket. Usado en --source-mode pc y merged."""
    if not path:
        return
    games = parse_games(path)
    if not games:
        print(f"ADVERTENCIA: Sin elementos <game> en '{system_id}' (pc): {path}")
        return
    for game in games:
        full_name = game.get("name")
        if not full_name:
            continue

        reason = get_discard_reason(full_name, game.findall("rom"))
        if reason:
            discarded_log.append({"name": full_name, "reason": reason, "origin": "pc"})
            continue
        accepted_log.append(full_name)

        regions = get_regions(full_name)
        languages, language_source = resolve_languages(full_name, regions)
        lookup[full_name] = {
            "id": full_name,
            "clone_of_id": game.get("cloneof") or None,
            "full_name": full_name,
            "base_name": get_base_name(full_name),
            "origin": "pc",
            "regions": regions,
            "languages": languages,
            "language_source": language_source,
            "category": get_category(full_name),
            "revision": get_revision(full_name),
            "version": get_version(full_name),
            "is_alt": test_is_alt(full_name),
        }


def new_empty_family(canonical_name: str) -> dict:
    return {
        "canonical_name": canonical_name,
        "alias_names": set(),
        "regions": set(),
        "languages": set(),
        "categories": set(),
        # Detalle por-clon (necesario para 1G1R por idioma+region: el
        # agregado de arriba solo dice QUE existe tal region/idioma en la
        # familia, no QUE clon concreto lo tiene).
        "members": [],
    }


def add_node_to_family(family: dict, node: dict) -> None:
    if node["base_name"] != family["canonical_name"]:
        family["alias_names"].add(node["base_name"])
    family["regions"].update(node["regions"])
    family["languages"].update(node["languages"])
    family["categories"].add(node["category"])
    family["members"].append({
        "name": node["full_name"],
        "origin": node["origin"],
        "regions": sorted(node["regions"]),
        "languages": sorted(node["languages"]),
        "languageSource": node["language_source"],
        "category": node["category"],
        "revision": node["revision"],
        "version": node["version"],
        "isAlt": node["is_alt"],
    })


def build_families(lookup: dict) -> tuple[dict, dict[str, str]]:
    """Resuelve la raiz de familia (parent/clone) de cada nodo via
    get_root_id (generico: solo necesita id/clone_of_id, sirve igual para
    el lookup namespaceado full+aftermarket que para el de pc/ por nombre)."""
    memo: dict[str, str] = {}
    families: dict[str, dict] = {}
    canonical_by_node_id: dict[str, str] = {}

    for node in lookup.values():
        if not node["base_name"]:
            continue
        root_id = get_root_id(node["id"], lookup, memo)
        canonical_name = lookup[root_id]["base_name"]
        canonical_by_node_id[node["id"]] = canonical_name

        if root_id not in families:
            families[root_id] = new_empty_family(canonical_name)
        add_node_to_family(families[root_id], node)

    return families, canonical_by_node_id


def resolve_dat_paths(system_id: str, entry: dict) -> tuple[Path, Path | None, Path | None] | None:
    """Devuelve (full_path, aftermarket_path, pc_path), o None si no se
    pudo resolver el DAT base."""
    if entry["source"] == "No-Intro":
        base_name = entry["base_name"]
        full_path = resolve_nointro_dat(base_name, "full")
        if not full_path:
            print(
                f"ADVERTENCIA: DAT no encontrado para '{system_id}' (No-Intro, base '{base_name}') "
                "en sources/dats/no-intro/full/. ¿Falta ejecutar update-sources.py?"
            )
            return None
        aftermarket_path = resolve_nointro_dat(base_name, "aftermarket", "Aftermarket")
        pc_path = resolve_nointro_dat(base_name, "pc", "Parent-Clone")
        return full_path, aftermarket_path, pc_path

    full_path = DAT_ROOT / entry["source"] / entry["dat"]
    if not full_path.is_file():
        print(f"ADVERTENCIA: DAT no encontrado para '{system_id}': {full_path}")
        return None
    return full_path, None, None


def build_system_index(system_id: str, entry: dict, source_mode: str) -> None:
    is_no_intro = entry["source"] == "No-Intro"
    resolved = resolve_dat_paths(system_id, entry)
    if resolved is None:
        return
    full_path, aftermarket_path, pc_path = resolved

    # 0) Mapa de idiomas curado por retool-clonelists-metadata: YA NO es
    # fuente de relleno (ver resolve_languages, cadena propia por
    # nombre+region). Se usa mas abajo (paso 9) como capa de validacion
    # posterior - divergencias entre lo calculado y lo que dice retool.
    language_map: dict[str, list[str]] = {}
    language_map_path: Path | None = None
    if is_no_intro:
        language_map_path = resolve_metadata_path(entry["base_name"])
        language_map = get_language_map(language_map_path)

    # 1) Parsear full+aftermarket (namespaceado por origen) y pc (nombre
    # completo como clave). Se parsean ambos siempre -salvo pc/ si no
    # existe para el sistema- porque el contraste informativo (paso 7) los
    # necesita sin importar el modo.
    fam_lookup: dict = {}
    fam_discarded: list = []
    fam_accepted: list[str] = []
    add_games_to_lookup(fam_lookup, fam_discarded, fam_accepted, full_path, "full", system_id)
    add_games_to_lookup(fam_lookup, fam_discarded, fam_accepted, aftermarket_path, "aftermarket", system_id)

    pc_lookup: dict = {}
    pc_discarded: list = []
    pc_accepted: list[str] = []
    if pc_path:
        add_pc_games_to_lookup(pc_lookup, pc_discarded, pc_accepted, pc_path, system_id)

    # --source-mode pc/merged requieren pc/; si el sistema no tiene pack
    # pc/ se degrada a fullaftermarket avisando.
    effective_mode = source_mode
    if effective_mode in ("pc", "merged") and not pc_path:
        print(
            f"ADVERTENCIA: Modo '{effective_mode}' pedido para '{system_id}' pero no hay pack pc/ "
            "disponible - se usa fullaftermarket"
        )
        effective_mode = "fullaftermarket"

    if effective_mode == "pc":
        if not pc_lookup:
            print(f"ADVERTENCIA: Sin elementos <game> validos en '{system_id}' (pc): {pc_path}")
            return
        lookup, discarded_log, accepted_log = pc_lookup, pc_discarded, pc_accepted
    else:
        if not fam_lookup:
            print(f"ADVERTENCIA: Sin elementos <game> validos en '{system_id}': {full_path}")
            return
        lookup, discarded_log, accepted_log = fam_lookup, fam_discarded, fam_accepted

    # 2) Resolver familias sobre la fuente activa.
    families, canonical_by_node_id = build_families(lookup)

    # 2b) --source-mode merged: completar el arbol full+aftermarket con las
    # familias que solo existen en pc/ (mismo criterio que el contraste del
    # paso 7 - onlyInPc), usando los datos de pc/ para esas entradas.
    merged_count = 0
    if effective_mode == "merged" and pc_lookup:
        fam_accepted_set = set(fam_accepted)
        pc_families, pc_canonical_by_node_id = build_families(pc_lookup)
        family_by_canonical = {f["canonical_name"]: f for f in families.values()}

        for pc_node in pc_lookup.values():
            if pc_node["full_name"] in fam_accepted_set:
                continue  # ya cubierto por full+aftermarket

            pc_canonical = pc_canonical_by_node_id[pc_node["id"]]
            if pc_canonical not in family_by_canonical:
                new_key = f"pc:{pc_canonical}"
                families[new_key] = new_empty_family(pc_canonical)
                family_by_canonical[pc_canonical] = families[new_key]
            add_node_to_family(family_by_canonical[pc_canonical], pc_node)
            canonical_by_node_id[pc_node["id"]] = pc_canonical
            accepted_log.append(pc_node["full_name"])
            merged_count += 1

    # 3) Cargar fichero de alias manual (si existe) y fusionar
    alias_path = ALIAS_ROOT / f"{system_id}.json"
    manual_aliases = []
    if alias_path.is_file():
        existing = json.loads(alias_path.read_text(encoding="utf-8"))
        manual_aliases = existing.get("aliases", [])

    # Nota: dos raices cloneofid distintas pueden compartir canonical_name
    # por coincidencia de titulo entre juegos NO relacionados (frecuente con
    # titulos genericos: "Baseball", "Tetris"...) sin que eso sea un
    # problema - son entradas legitimamente distintas en el indice final,
    # que si admite "name" repetido.
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

            # Si ese alias era el canonico de OTRA familia auto-detectada, fusionamos esa familia tambien.
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

    # 4) Salida del indice principal, ordenada por nombre canonico
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
        "source": entry["source"],
        "sourceMode": SOURCE_MODE_LABELS[effective_mode],
        "dat": pc_path.name if effective_mode == "pc" else full_path.name,
        "datAftermarket": aftermarket_path.name if effective_mode != "pc" and aftermarket_path else None,
        "datPc": pc_path.name if effective_mode in ("pc", "merged") and pc_path else None,
        "generated": date.today().isoformat(),
        "games": games_out,
    }
    write_json_file(OUTPUT_ROOT / f"{system_id}.json", output)

    # 5) Persistir el fichero de alias fusionado (auto + manual)
    aliases_out = [
        {"canonical": f["canonical_name"], "aliases": sorted(f["alias_names"])}
        for f in sorted(families.values(), key=lambda f: f["canonical_name"])
        if f["alias_names"]
    ]
    write_json_file(alias_path, {"system": system_id, "aliases": aliases_out})

    # 6) Fichero de depuracion: descartados (con motivo) y aceptados
    write_json_file(
        DEBUG_ROOT / f"{system_id}.json",
        {
            "system": system_id,
            "discarded": sorted(discarded_log, key=lambda d: d["name"]),
            "accepted": sorted(accepted_log),
        },
    )

    # 7) Informe de contraste bidireccional entre full+aftermarket y pc/,
    # calculado siempre sobre los datos "pristinos" (fam_accepted/
    # pc_accepted), sin importar --source-mode.
    pc_note = "sin pc/"
    if pc_path:
        fam_accepted_set = set(fam_accepted)
        pc_accepted_set = set(pc_accepted)
        only_in_pc = sorted(pc_accepted_set - fam_accepted_set)
        only_in_full_aftermarket = sorted(fam_accepted_set - pc_accepted_set)
        if only_in_pc or only_in_full_aftermarket:
            write_json_file(
                DEBUG_ROOT / f"{system_id}-pc-contrast.json",
                {
                    "system": system_id,
                    "pc": pc_path.name,
                    "onlyInPc": only_in_pc,
                    "onlyInFullAftermarket": only_in_full_aftermarket,
                },
            )
        pc_note = f"pc contraste: {len(only_in_pc)} solo-pc / {len(only_in_full_aftermarket)} solo-full+aftermarket"
        if effective_mode == "merged":
            pc_note += f" ({merged_count} fusionados)"

    # 8) Validacion cruzada contra el clonelist de retool-clonelists-metadata
    clonelist_note = "sin clonelist"
    if is_no_intro:
        clonelist_path = resolve_clonelist_path(entry["base_name"])
        clonelist_map = get_clonelist_map(clonelist_path)
        if clonelist_map:
            diffs = []
            for node in lookup.values():
                if node["base_name"] not in clonelist_map:
                    continue
                clonelist_group = clonelist_map[node["base_name"]]
                cloneofid_group = canonical_by_node_id[node["id"]]
                if clonelist_group != cloneofid_group:
                    diffs.append({
                        "baseName": node["base_name"],
                        "cloneofidFamily": cloneofid_group,
                        "clonelistGroup": clonelist_group,
                    })
            if diffs:
                write_json_file(
                    DEBUG_ROOT / f"{system_id}-clonelist-diff.json",
                    {
                        "system": system_id,
                        "clonelist": clonelist_path.name,
                        "diffs": sorted(diffs, key=lambda d: d["baseName"]),
                    },
                )
            clonelist_note = f"clonelist: {len(diffs)} divergencias"

    # 9) Validacion de idioma contra retool-clonelists-metadata: capa
    # OPCIONAL y POSTERIOR al calculo propio (resolve_languages, paso 1) -
    # retool ya NO rellena el campo languages, solo sirve para detectar
    # divergencias entre lo calculado (nombre + default por region) y lo
    # que dice retool, por cada clon individual (mas granular que el
    # clonelist-diff del paso 8, que compara por base_name de familia).
    language_note = "sin metadata idioma"
    if language_map:
        lang_diffs = []
        for node in lookup.values():
            if node["full_name"] not in language_map:
                continue
            retool_languages = sorted(language_map[node["full_name"]])
            # "nolang" es un marcador especial de retool ("sin contenido de
            # texto", no un codigo de idioma real - 17266 casos en todo
            # retool-clonelists-metadata, no es raro: juegos genuinamente sin
            # texto). Nuestro algoritmo nunca puede "acertarlo" porque no hay
            # ninguna senal textual de "sin idioma" en el nombre - se excluye
            # de la comparacion, no es una divergencia real.
            if "nolang" in retool_languages:
                continue
            computed_languages = sorted(node["languages"])
            if retool_languages != computed_languages:
                lang_diffs.append({
                    "name": node["full_name"],
                    "computedLanguages": computed_languages,
                    "computedSource": node["language_source"],
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

    mode_label = SOURCE_MODE_LABELS[effective_mode]
    print(
        f"Generado: {system_id}.json [{mode_label}] ({len(games_out)} familias, {len(discarded_log)} descartados) "
        f"+ aliases/{system_id}.json ({len(aliases_out)} con alias) [{pc_note}] [{clonelist_note}] [{language_note}]"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--system-id", dest="system_id", default=None)
    parser.add_argument(
        "--source-mode",
        dest="source_mode",
        choices=["fullaftermarket", "pc", "merged"],
        default="fullaftermarket",
    )
    args = parser.parse_args()

    manifest: dict[str, str] = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))["systems"]

    dat_map: dict[str, dict] = {}
    for system_id, base_name in manifest.items():
        dat_map[system_id] = {"source": "No-Intro", "base_name": base_name}
    for system_id, dat_name in NON_REDUMP_MAP.items():
        dat_map[system_id] = {"source": "Non-Redump", "dat": dat_name}

    ids = [args.system_id] if args.system_id else list(dat_map.keys())

    for system_id in ids:
        if system_id not in dat_map:
            print(f"ADVERTENCIA: Sistema no mapeado: {system_id}")
            continue
        build_system_index(system_id, dat_map[system_id], args.source_mode)


if __name__ == "__main__":
    main()
