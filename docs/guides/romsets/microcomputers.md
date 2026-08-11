# Preparación de romsets — Microcomputers

Flujo de preparación para microcomputers clásicos (Commodore 64/128, Amiga, ZX Spectrum/81, MSX/MSX2, Amstrad CPC, Atari ST, Sharp X68000...). Sigue el mismo orden de fases que [docs/guides/romsets/workflow.md](workflow.md); aquí se resume qué cambia frente a [cartridge.md](cartridge.md), del que se separó por dos motivos reales (ver `docs/romsets.md` sección Microcomputers):

- **Diversidad de medio** — a diferencia de consolas de cartucho, un mismo sistema puede necesitar imágenes de cinta (`.tzx`/`.tap`), disco (`.dsk`/`.d64`/`.adf`) o cartucho según el título, cada uno con su propio formato de contenedor.
- **Minoría real de sistemas con fuente distinta a No-Intro** — la mayoría de microcomputers (`c64`, `amiga`, `msx`, `msx2`, `amstradcpc`, `atarist`) sí usan No-Intro como fuente principal, igual que en `cartridge.md`. Las excepciones confirmadas en `docs/romsets.md`: `spectrum`/`zx81` vía libretro (ClrMamePro texto — No-Intro solo cubre +3 en el caso de Spectrum) y `sharpx68000` vía Non-Redump (No-Intro solo cubre la variante Flux).

## Fuente

Para los sistemas con No-Intro como fuente principal, mismo flujo que en [cartridge.md](cartridge.md#fuente) — ver [dat-generation.md](../tools/dat-generation.md#no-intro-dat-o-matic).

Para las excepciones:

- **libretro-database** (`spectrum`, `zx81`) — ver [dat-generation.md](../tools/dat-generation.md#libretro-database-clrmamepro-texto). Formato ClrMamePro texto, no XML Logiqx — requiere parser distinto en la fase de auditoría.
- **Non-Redump** (`sharpx68000`) — ver [dat-generation.md](../tools/dat-generation.md#non-redump).
- **TOSEC** — no aparece como fuente principal de ningún microcomputer ya fijado en `docs/romsets.md` a día de hoy, pero sigue siendo la alternativa de referencia para microcomputers sin cobertura No-Intro/libretro adecuada (ver [dat-generation.md](../tools/dat-generation.md#tosec-the-old-school-emulation-center)) — su filosofía de acumulación (acepta volcados defectuosos, hacks, sin `cloneofid`) complica el filtrado 1G1R si se acaba usando.

## Herramientas específicas por sistema

Además de las herramientas genéricas ya cubiertas en `docs/guides/tools/` (romset-cleaning.md: ROMSorter/SAM; romset-audit.md: JRomManager/ClrMamePro/RomVault/RomCenter), existen herramientas de nicho por sistema, útiles sobre todo en la fase 4 (limpieza) y en la gestión de imágenes de disco/cinta. Todas verificadas y catalogadas en `docs/tools.md`:

- **Multisistema** — GoodMerge / goodMergePy (agrupan clones/variantes en un único archivo), Universal ROM Cleaner (limpieza genérica por atributos entre paréntesis/corchetes, no específica de TOSEC pese al nombre con el que a veces circula).
- **ZX Spectrum** — ZX-Pokemaster (organiza/renombra el catálogo TOSEC, **archivado/sin mantenimiento**), zx-spectrum-tosec-util (convierte TOSEC a la estructura de la consola retro "The Spectrum"), ZX-Blockeditor (edición de bloques de datos en `.tap`/`.tzx`/`.dsk`/etc.).
- **MSX** — DiskManager (gestión de imágenes `.dsk`).
- **Commodore 64** — DirMaster (edición de imágenes `.d64`/`.d81`).
- **Amstrad CPC** — ManageDsk (fusión/catálogo de imágenes `.dsk`).

**Descartadas tras verificar — no usar sin volver a confirmar:** "MSX Rom Database" (generation-msx.nl es una enciclopedia MSX, sin evidencia de la base de datos de mappers descrita), "CPCDiskAnalyse" (no existe con ese nombre; alternativas reales: `Dsktools`, `CPCDiskXP`, `muckypaws/AmstradDSKExplorer`), "ST-Ghost" (no es una herramienta independiente — `.STG`/"Ghost disk" es una función del emulador SSE, fork de Steem), "Hatari / Steem DB Tools" (sin evidencia de que exista), "AGLaunch" con repo `kgw77/AGLaunch` (la herramienta es real pero ese repositorio da 404 — sin fuente confirmada).

**Nota sobre conversión de cinta a audio (ZX Spectrum, no catalogado en `tools.md` por ser tangencial a la gestión de romsets):** OTLA está muerto (Google Code Archive, cerrado); alternativas activas: `raydac/zxtap-to-wav`, `semack/ZxTape2Wav.Net`.

## Verificación contra DAT

Fase 3 — ver [romset-audit.md](../tools/romset-audit.md). Para `spectrum`/`zx81` (ClrMamePro texto), confirmar que la herramienta usada soporta ese formato directamente (ClrMamePro, RomCenter) o via conversión previa (fase 2, [dat-conversion.md](../tools/dat-conversion.md)) si se prefiere JRomManager/RomVault con Logiqx XML.

## Filtrado 1G1R

Fase 5 — ver [1g1r-filtering.md](../tools/1g1r-filtering.md). Para los sistemas con No-Intro (mayoría), mismo flujo que `cartridge.md` con esquema Parent-Clone. Para `sharpx68000` (Non-Redump) y cualquier caso que acabe en TOSEC, aplica la misma cautela ya documentada en esas secciones de `dat-generation.md`: `cloneofid` no siempre fiable, revisar agrupado antes de dar el 1G1R por bueno.

## Organización en data/roms

Fase 8 — particularidad frente a `cartridge.md`: la estructura debe reflejar el tipo de medio real del título (cinta/disco/cartucho), no asumir un único contenedor por sistema. Ver el pipeline propio en [custom-pipeline.md](custom-pipeline.md).

[TODO: no se ha detallado aún cómo se organiza en `data/roms/` un sistema con medios mixtos (ej. Amstrad CPC con títulos en cinta y disco a la vez) — verificar convención esperada por el frontend objetivo antes de dar esto por definido]

## Generación de gamelist.xml y media

Fases 9-10 — ver [gamelist-generation.md](../tools/gamelist-generation.md) y [media-scraping.md](../tools/media-scraping.md). Sin particularidades específicas de microcomputer frente a otros tipos de fuente.

## Notas

Antes de asumir la fuente de un sistema nuevo no cubierto todavía en `docs/romsets.md`, revisar primero si No-Intro lo cubre (caso general) antes de recurrir a TOSEC/libretro — la experiencia de los sistemas ya documentados es que No-Intro cubre más microcomputers de los que se podría asumir a priori.
