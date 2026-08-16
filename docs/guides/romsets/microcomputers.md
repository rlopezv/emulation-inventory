# Preparación de romsets — Microcomputers

Flujo de preparación para microcomputers clásicos (Commodore 64/128, Amiga, ZX Spectrum/81, MSX/MSX2, Amstrad CPC, Atari ST, Sharp X68000...). Sigue el mismo orden de fases que [docs/guides/romsets/workflow.md](workflow.md); aquí se resume qué cambia frente a [cartridge.md](cartridge.md), del que se separó por dos motivos reales (ver `docs/romsets.md` sección Microcomputers):

- **Diversidad de medio** — a diferencia de consolas de cartucho, un mismo sistema puede necesitar imágenes de cinta (`.tzx`/`.tap`), disco (`.dsk`/`.d64`/`.adf`) o cartucho según el título, cada uno con su propio formato de contenedor.
- **Fuente por sistema, en revisión sistema-a-sistema (ver `docs/session-context.md`)** — a diferencia de `cartridge.md`, aquí no hay una fuente principal única para todo el bucket: para `c64`, `msx` y `msx2` se confirmó No-Intro como fuente principal del formato de cartucho dominante (`.CRT`/`.ROM`), con TOSEC como fuente alternativa para el catálogo de disco/cinta que No-Intro no cubre. Para `spectrum` y `zx81` se confirmó TOSEC como fuente principal (No-Intro no tiene cobertura madura de estos sistemas), con libretro-database como alternativa. `c128`, `amiga`, `amstradcpc`, `atarist`, `dragon32` y `sharpx68000` siguen con TOSEC como fuente principal fijada en sesiones previas, pendientes de la misma revisión cruzada formato-disponible × emulador-soporta antes de confirmarla como definitiva — ver tabla de formatos más abajo para el estado actual de cada uno.

## Fuente

Para los sistemas con No-Intro como fuente principal, mismo flujo que en [cartridge.md](cartridge.md#fuente) — ver [dat-generation.md](../tools/dat-generation.md#no-intro-dat-o-matic).

Para las excepciones:

- **libretro-database** (`spectrum`, `zx81`) — ver [dat-generation.md](../tools/dat-generation.md#libretro-database-clrmamepro-texto). Formato ClrMamePro texto, no XML Logiqx — requiere parser distinto en la fase de auditoría.
- **Non-Redump** (`sharpx68000`) — ver [dat-generation.md](../tools/dat-generation.md#non-redump).
- **TOSEC** — no aparece como fuente principal de ningún microcomputer ya fijado en `docs/romsets.md` a día de hoy, pero sigue siendo la alternativa de referencia para microcomputers sin cobertura No-Intro/libretro adecuada (ver [dat-generation.md](../tools/dat-generation.md#tosec-the-old-school-emulation-center)) — su filosofía de acumulación (acepta volcados defectuosos, hacks, sin `cloneofid`) complica el filtrado 1G1R si se acaba usando.

## Formato de ROM recomendado por sistema

Sistemas clasificados como Microcomputers en [docs/guides/romsets/README.md](README.md#clasificación-de-sistemas-por-flujo). **Caso excepcional frente a Cartucho/plano y Óptico:** ahí un sistema tiene un formato único; aquí, según el medio real de publicación de cada título (cinta/disco/cartucho), puede hacer falta más de un DAT/formato simultáneo para cubrir el catálogo completo — un título publicado solo en cinta no aparece en el DAT de disco aunque ambos existan para el mismo sistema. TOSEC refleja esto publicando un DAT por formato de medio (tag entre corchetes en el nombre de fichero, ej. `[D64]`, `[TZX]`, `[ROM]`); el DAT ya fijado en `docs/romsets.md` es el formato principal/mayoritario, no necesariamente el único necesario.

Solo se contabiliza la categoría **Games** de cada DAT TOSEC (se descarta Applications/Demos/Educational/etc., fuera del alcance de un romset de juegos). Columna "DAT alternativo disponible": si ya existe el `Games - [Tag]` correspondiente en `metadata/dat/TOSEC/`, solo falta indexarlo (bloqueo 100% en `build-dat-index-tosec.ps1`, que hoy solo mapea `gx4000`); `[TODO]` si no se ha encontrado ese DAT localmente y no se ha confirmado si TOSEC lo publica.

| Identificador canónico | Formato principal | DAT | Formatos alternativos de riesgo | DAT alternativo disponible |
| --- | --- | --- | --- | --- |
| `zx81` | `.P` (programa nativo) | TOSEC `[P]` | `.TZX` (cinta, **desaconsejado** en portátiles — emulación tosca, exige teclado virtual y `LOAD ""` tokenizado) | Sí — `Games - [TZX]` ya descargado; `[Z81]` también existe pero es snapshot de EightyOne (no medio real, no cuenta como alternativa), `[Multipart]` es empaquetado de `.P`, no formato distinto |
| `dragon32` | `.CAS` (cinta) | TOSEC `[CAS]` | `.VDK` (disquete, juegos avanzados/tardíos exclusivos de Dragon 64) | Sí — `Games - [VDK]` ya descargado. `.PAK` (cartucho) **riesgo real**: muchos volcados son en realidad para TRS-80 CoCo (plataforma hermana no intercambiable), pueden causar error de memoria — no usar sin verificar; `.BIN` suelto tampoco recomendable, sin cabecera de dirección de carga |
| `c64` | `.CRT` (cartucho) | No-Intro `Commodore - Commodore 64 (*).dat` | `.D64` (disquete, catálogo histórico masivo, incluye crackeados) | Sí — TOSEC `Games - [D64]` (12 sub-DAT por género, fusionar con SabreTools), ya fijado como fuente alternativa en `docs/romsets.md` |
| `c128` | `.D64` (disco) | TOSEC `[D64]` (sin dividir por género, a diferencia de `c64`) | Sin variante CRT: No-Intro no publica DAT de Commodore 128 | — |
| `spectrum` | `.TAP` (cinta, Fast Loading) | TOSEC `[TAP]` (alt. libretro `Sinclair - ZX Spectrum.dat`) | `.Z80`/`.SNA` (snapshot, arranque instantáneo en partida — arcade rápidos tipo Jetpac/Manic Miner), `.DSK` (solo exclusivos Spectrum +3, incómodo sin teclado físico), `.TZX` (preservación perfecta, desaconsejado en portátiles por incompatibilidad de Fast Loading en muchos cores) | Sí — `Games - [Z80]`/`[SNA]`/`[DSK]`/`[TZX]` ya descargados |
| `msx` / `msx2` | `.ROM` (cartucho) | No-Intro `Microsoft - MSX(2) (*).dat` | `.DSK` (aventuras conversacionales, RPGs, Compile, MSX2/MSX2+ exclusivos) | Sí — TOSEC `Games - [DSK]`, ya fijado como fuente alternativa en `docs/romsets.md`. Descartar `.CAS` (cinta inestable, sin Fast Loading fiable) y `.MX1`/`.MX2` (obsoletas, no reconocidas por cores modernos) |
| `amstradcpc` | `.DSK` (disco) | TOSEC `[DSK]` (alt. libretro `Amstrad - CPC.dat`; No-Intro descartado — solo tiene `(Flux)`/`(Misc)`, sin set reproducible directo) | `.CDT` (cinta, **desaconsejado** en portátiles — Fast Loading poco fiable, a diferencia de Spectrum), `.CPR` (cartucho, **solo GX4000/CPC Plus**, no CPC 6128 estándar) | Sí — `Games - [CDT]`/`[CPR]` ya descargados, pero ninguno recomendado como alternativa real para CPC 6128 en portátil |
| `atarist` | `.ST` (disco) | TOSEC `[ST]` | `.MSA` (equivalente a `.ST`, mismo nivel de compatibilidad) | No — no existe `Games - [MSA]` en `metadata/dat/TOSEC/` (confirmado, TOSEC no lo publica como DAT separado); `.STX`/`.IPF` sí tienen DAT pero **desaconsejados**: requieren la librería externa CAPSimg y son más pesados de emular (audio entrecortado, ralentización) |
| `amiga` | `.LHA` (WHDLoad) | WHDLoad `Commodore - Amiga - WHDLoad.dat` (`github.com/MrV2K/WHDLoad-Database`, basado en Retroplay) | `.ADF` (disquete original, TOSEC/libretro) | Sí — TOSEC `Games - [ADF]`, ya fijado como fuente alternativa en `docs/romsets.md`. `.IPF` (solo `Unofficial IPF` en TOSEC) **desaconsejado**: requiere CAPSimg. `.HDF` no tiene DAT TOSEC ni forma parte del DAT WHDLoad (que empaqueta uniformemente en `.lha`) |
| `sharpx68000` | `.DIM`/`.XDF` (disquete 5.25", catálogo general) | TOSEC `[DIM]` (fuente cambiada de Non-Redump en `docs/romsets.md`, que queda como alternativa) | `.HDF` (disco duro virtual, dominante para juegos masivos multi-disco tipo Akumajou Dracula/Star Cruiser — soportado por px68k, evita menús de "inserta Disco 3") | No — `.HDF` no tiene DAT TOSEC (`Games`), pendiente localizar fuente equivalente al caso `amiga`/WHDLoad. `.HDM`/`.2HD` **descartados**: aunque existen como DAT TOSEC, causan Boot Fail en el core estándar de RetroArch — convertir a `.DIM` si aparecen |

**`c64`/`c128` — emulador y formatos adicionales verificados (investigación cruzada TOSEC-disponible × soporte real del emulador, ver `docs/session-context.md`):** core RetroArch `lr-vice` (`x64sc` para `c64`, `x128` para `c128`), standalone VICE. `.CRT` elegido como formato principal por autostart instantáneo (sin teclado virtual ni mapeo de disquetera) frente a `.D64`, dominante en catálogo pero con carga más lenta y sin ese autostart nativo. Además de `.D64`/`.TAP` ya indicados, VICE (standalone y core) también carga nativamente `.D71`, `.D81`, `.G64`, `.P00`, `.PRG`, `.T64` — todos con DAT TOSEC `Games` ya descargado por género — y `.BIN` (confianza media-alta, sin confirmación oficial explícita). `.NIB`/`.NBZ` solo cargan vía el core RetroArch (auto-convierte a G64 internamente); en VICE standalone requieren conversión previa con `nibtools`. Quedan descartados como no usables (archivadores/formatos de transporte de la escena, no imágenes cargables): `.ARC`, `.ARK`, `.DFI`, `.DMP`, `.LNX`, `.SDA`, `.SFX`, `.Z64` (este último es un disco partido en segmentos Zipcode para transferencia a unidad 1541 real, no un formato de imagen).

**`spectrum` — emulador verificado:** core RetroArch `lr-fuse` (estándar en portátiles chinas — detecta el modelo automáticamente según el archivo, 48K/128K/+2/+3; teclado virtual asignado al botón Select para introducir comandos de carga/joystick); standalone FBZX o Fuse (solo en hardware muy limitado, sin reescalado de shaders ni savestates unificados de RetroArch). Contenedor recomendado: `.TAP`/`.Z80` comprimidos en `.ZIP` individual, leído nativamente por los CFW de las portátiles (OnionOS, ArkOS...) sin gasto extra de espacio.

**`zx81` — emulador verificado:** core RetroArch `lr-eightyone` (`81`) — único core con soporte real en portátiles chinas (preconfigurado en ArkOS, AmberELEC, Batocera/Knulli), autostart instantáneo de `.P`, redirige las teclas de dirección originales del ZX81 a la cruceta. No existe alternativa standalone viable/preconfigurada en las consolas actuales — monopolio de `lr-eightyone` por la baja demanda del sistema. Contenedor recomendado: `.P` comprimido en `.ZIP` individual (los juegos pesan 1-16 KB, el peso es irrelevante; el `.ZIP` es solo por limpieza de la tarjeta y compatibilidad con scrapers como SkyScraper).

**`msx`/`msx2` — emulador verificado:** core RetroArch `lr-bluemsx` (estándar por defecto en ArkOS, AmberELEC, OnionOS; alta precisión en MSX/MSX2/MSX2+). **Alerta técnica crítica:** requiere copiar las subcarpetas `Databases`/`Machines` de blueMSX a `system/` de RetroArch, o falla en pantalla negra (especialmente con `.DSK`). Alternativa ligera para hardware muy limitado: `lr-fmsx` (menor consumo de CPU, pero peor compatibilidad con MSX2 avanzado en disquete y mapeo de botones menos intuitivo). Contenedor recomendado: `.ROM`/`.DSK` comprimidos en `.ZIP` individual.

**`amstradcpc` — emulador verificado:** core RetroArch `lr-caprice32` (estándar por defecto en OnionOS, ArkOS, AmberELEC; ultra optimizado para CPU de bajo consumo, autostart rápido de `.DSK`, buen mapeo de botones de disparo). Alternativa para hardware muy antiguo/gama extremadamente baja: `lr-crocods` (más ligero, pero peor compatibilidad con volcados modernos de la escena española y teclado virtual más tosco). Contenedor recomendado: `.DSK` comprimido en `.ZIP` individual.

**`atarist` — emulador verificado:** core RetroArch `lr-hatari` (estándar por defecto, autostart rápido, mapea el ratón del Atari ST al stick analógico derecho o la cruceta). **Nota técnica obligatoria:** requiere las BIOS TOS (`tos102.img`, `tos104.img`...) en `system/` de RetroArch, o se queda en pantalla en blanco — mismo patrón que Amiga/MSX con sus ficheros de sistema. Contenedor recomendado: `.ST`/`.MSA` comprimidos en `.ZIP`/`.7Z` individual.

**`amiga` — emulador verificado:** core RetroArch `lr-puae` (Portable UAE) — estándar por defecto en ArkOS, OnionOS, Knulli; detecta automáticamente el chipset requerido (AGA de Amiga 1200 vs. ECS/OCS de Amiga 500), lee `.ADF`/`.ZIP`/`.M3U` y `.LHA` de WHDLoad de forma nativa, mapea el ratón en los sticks, buen teclado virtual. **Nota técnica obligatoria:** requiere las ROM Kickstart oficiales (`kick34005.A500`, `kick40068.A1200`...) con su nombre exacto en `system/` de RetroArch. Alternativa standalone: Amiberry (Raspberry Pi y portátiles con interfaz directa fuera de RetroArch; muy preciso con WHDLoad, pero configuración compleja sin teclado/ratón físico). Advertencia de organización: no dejar discos sueltos de un mismo juego multi-disco como `.ADF` independientes en la raíz (`Juego Disk 1.adf`, `Juego Disk 2.adf`...) — duplica la entrada en el frontend; usar `.M3U` o el `.LHA` WHDLoad ya unificado.

**`sharpx68000` — emulador verificado:** core RetroArch `lr-px68k` (estándar por defecto en ArkOS, AmberELEC, Batocera/Knulli; optimizado para ARM moderno, lee `.ZIP`, soporta `.HDF`, simula las dos disqueteras físicas FDD0/FDD1). **Nota técnica obligatoria:** requiere `cgrom.dat` e `iplrom.dat` (BIOS del sistema) en `system/keropi/` de RetroArch, o se queda en pantalla negra. Advertencia de organización: no dejar disquetes sueltos de un mismo juego multi-disco como `.DIM` independientes en la raíz — mismo problema que Amiga.

**`dragon32` — emulador verificado:** core RetroArch `lr-xroar` (estándar por defecto en ArkOS, AmberELEC, Batocera/Knulli; muy ligero, mejor soporte de autostart del mercado para `.CAS`, mapea el joystick clásico de Dragon a la cruceta automáticamente). Tiene emulación de BIOS de alto nivel (HLE, arranca cinta sin ROM real), pero se recomienda añadir las ROM oficiales `d32.rom`/`d64.rom` en `system/` de RetroArch para compatibilidad completa, especialmente con `.VDK`.

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
