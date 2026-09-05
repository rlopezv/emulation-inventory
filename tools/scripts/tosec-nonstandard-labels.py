#!/usr/bin/env python3
"""
Escanea uno o varios DAT TOSEC y clasifica cada etiqueta entre parentesis/
corchetes contra el vocabulario OFICIAL de TOSEC (region, idioma, video,
copyright, estado de desarrollo, flags de dump — ver docs/references.md#tosec),
sacando una tabla de frecuencia de las etiquetas que NO encajan en ese
vocabulario.

Motivacion (ver docs/session-context.md, sesion 2026-09-02/03): el
`DATParentInferrer` de Igir (ver docs/guides/tools/1g1r-filtering.md#igir)
solo sabe despojar el vocabulario OFICIAL de TOSEC al agrupar padres/clones
para el 1G1R — cualquier etiqueta de escena/comunidad no oficial (`[k-file]`
en Atari 8-bit, `[CPM Version]`/`[master disk N]`/`[gunstick]` en Amstrad
CPC, confirmadas en pruebas reales) hace que Igir NO fusione variantes que
en la practica son el mismo contenido, dejando "clones sueltos" en el 1G1R
final. Este script identifica esas etiquetas de forma proactiva, sistema
por sistema, ANTES de correr Igir, en vez de descubrirlas por sorpresa
comparando resultados a mano.

Uso:
    python tools/scripts/tosec-nonstandard-labels.py "sources/tosec/out/Atari 8bit - Games - [ATR] (TOSEC-v2025-01-15_CM).dat"
    python tools/scripts/tosec-nonstandard-labels.py sources/tosec/out/*.dat --top 20

Salida: tabla de frecuencia de corchetes y parentesis no reconocidos, por
DAT. No modifica nada — es solo diagnostico, el siguiente paso (limpiar
antes de pasar por Igir) queda para quien use el resultado.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree as ET

# Vocabulario oficial de TOSEC (docs/references.md#tosec), mismo que usa
# Igir en datParentInferrer.ts — mantener sincronizado si TOSEC/Igir amplian
# alguna lista.
REGION_CODES = set(
    "AE AL AS AT AU BA BE BG BR CA CH CL CN CS CY CZ DE DK EE EG ES EU FI FR "
    "GB GR HK HR HU ID IE IL IN IR IS IT JO JP KR LT LU LV MN MX MY NL NO NP "
    "NZ OM PE PH PL PT QA RO RU SE SG SI SK TH TR TW US VN YU ZA".split()
)
LANG_CODES = set(
    "ar bg bs cs cy da de el en eo es et fa fi fr ga gu he hi hr hu is it ja "
    "ko lt lv ms nl no pl pt ro ru sk sl sq sr sv th tr ur vi yi zh".split()
)
VIDEO_CODES = set("CGA EGA HGC MCGA MDA NTSC NTSC-PAL PAL PAL-60 PAL-NTSC SVGA VGA XGA".split())
COPYRIGHT_CODES = set("CW CW-R FW GW GW-R LW PD SW SW-R".split())
DEVELOPMENT_CODES = set("alpha beta preview pre-release proto".split())
DEMO_CODES = set("demo demo-kiosk demo-playable demo-rolling demo-slideshow".split())

DATE_RE = re.compile(r"^[0-9x]{4}(-[0-9x]{2}(-[0-9x]{2})?)?$")
MULTILANG_RE = re.compile(r"^M[0-9]+$", re.I)
# Descriptores de medio legitimos (no son "etiquetas de calidad de volcado",
# son contenido fisicamente distinto — Disk 1 != Disk 2) — no se cuentan
# como no-estandar aunque tampoco esten en el vocabulario TOSEC oficial.
MEDIA_PART_RE = re.compile(
    r"^(disk|disc|tape|part)\s*[0-9]+(\s*of\s*[0-9]+)?(\s*side\s*[a-f])?$|^side\s*[a-f]$", re.I
)
DUMP_FLAG_RE = re.compile(r"^(cr|f|h|m|p|t|tr|o|u|v|b|a|!)([0-9]+| .*)?$", re.I)


def classify_paren(content: str, position: int) -> str | None:
    c = content.strip()
    cl = c.lower()
    if DATE_RE.match(c) or MEDIA_PART_RE.match(c):
        return None
    if c in REGION_CODES or cl in LANG_CODES or c in VIDEO_CODES or c in COPYRIGHT_CODES:
        return None
    if cl in DEVELOPMENT_CODES or cl in DEMO_CODES or MULTILANG_RE.match(c):
        return None
    if position < 2:
        # Asumido fecha/publisher (texto libre esperado en esas posiciones,
        # ya cubierto por DATE_RE arriba para la fecha) - no se marca.
        return None
    return c


def classify_bracket(content: str) -> str | None:
    c = content.strip()
    if DUMP_FLAG_RE.match(c):
        return None
    return c


def scan_dat(path: Path) -> tuple[Counter, Counter, int]:
    names = [g.get("name") for g in ET.parse(path).getroot().findall("game") if g.get("name")]
    parens: Counter = Counter()
    brackets: Counter = Counter()
    for n in names:
        for i, p in enumerate(re.findall(r"\(([^()]*)\)", n)):
            label = classify_paren(p, i)
            if label:
                parens[label] += 1
        for b in re.findall(r"\[([^\]]*)\]", n):
            label = classify_bracket(b)
            if label:
                brackets[label] += 1
    return parens, brackets, len(names)


def main() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except AttributeError:
        pass

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("dats", nargs="+", type=Path, help="Uno o varios DAT TOSEC (Logiqx)")
    parser.add_argument("--top", type=int, default=15, help="Cuantas etiquetas mostrar por tabla (por defecto 15)")
    args = parser.parse_args()

    for path in args.dats:
        if not path.is_file():
            print(f"AVISO: no existe {path}, saltando", file=sys.stderr)
            continue
        parens, brackets, total_games = scan_dat(path)
        print(f"\n{'=' * 10} {path.name} ({total_games} entradas) {'=' * 10}")
        print(f"\nCorchetes [] no reconocidos (no son flags oficiales de dump):")
        if not brackets:
            print("  (ninguno)")
        for tok, count in brackets.most_common(args.top):
            print(f"  [{tok}]: {count}")
        print(f"\nParéntesis () no reconocidos (no son fecha/región/idioma/vídeo/copyright/desarrollo, ni Disk/Side):")
        if not parens:
            print("  (ninguno)")
        for tok, count in parens.most_common(args.top):
            print(f"  ({tok}): {count}")


if __name__ == "__main__":
    main()
