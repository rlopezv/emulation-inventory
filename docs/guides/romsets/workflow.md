# Preparación de romsets — Workflow end-to-end

[TODO: descripción breve]

Flujo completo de procesamiento de un romset desde el DAT de origen hasta su despliegue en `data/roms/`, encadenando las herramientas documentadas en `docs/software.md` y `docs/tools.md`. Complementa los flujos por tipo de fuente ([cartridge.md](cartridge.md), [optical-chd.md](optical-chd.md), [arcade.md](arcade.md)) indicando qué herramienta concreta se usa en cada paso; el detalle de uso de cada herramienta (comandos, parámetros) vive en las guías de [docs/guides/tools/](../tools/README.md).

## 1. Obtención del DAT

Punto de partida de todo el flujo: sin el DAT correcto no se puede auditar, filtrar ni renombrar nada. La fuente y el DAT concreto por sistema están fijados en `docs/romsets.md`; aquí se documenta dónde conseguirlos y con qué herramienta. Detalle de uso: [dat-generation.md](../tools/dat-generation.md).

**No-Intro** (cartuchos, handhelds, la mayoría de microcomputers) — descarga manual desde el portal **DAT-o-MATIC** (datomatic.no-intro.org), la fuente oficial del grupo. Elegir el esquema Parent-Clone (P/C) si se va a aplicar 1G1R después (ver paso 5). Requiere cuenta gratuita del portal.

**Redump** (sistemas ópticos: PSX, PS2, Saturn, Dreamcast, GameCube, Wii, PC Engine CD, Sega CD, 3DO, Jaguar CD, Amiga CD32/CDTV, Neo Geo CD) — descarga manual desde **redump.org**, sección Datfiles de cada sistema.

**Non-Redump** — usar solo como fuente alternativa cuando `docs/romsets.md` lo indica (prototipos/betas no aceptados por Redump, o sistemas sin DAT Redump todavía como PS3/PSP/Xbox 360). Repositorio comunitario en GitHub (ver enlace por sistema en `docs/romsets.md`).

**TOSEC** — descarga del set completo (todas las plataformas en un único paquete) desde **tosec.org**; extraer solo el/los DAT del sistema necesario. Útil para microcomputers sin cobertura No-Intro (ej. `gx4000`).

**MAME / FBNeo (arcade)** — el DAT de MAME se genera localmente con `mame -listxml > mame.xml` desde el propio ejecutable (no se descarga como fichero suelto); FBNeo se obtiene del repositorio oficial en GitHub o se genera igual que MAME con el volcado XML integrado del emulador. Ver `docs/references.md#dats` para el detalle de qué sistemas cubre cada uno.

**libretro (ClrMamePro texto)** — DATs mantenidos en el repositorio `libretro-database` de GitHub; usados para sistemas sin cobertura adecuada en las fuentes anteriores (ej. `spectrum`, `zx81`, `scummvm`, `dos`). Formato de texto plano, no XML — requiere parser distinto (ver `docs/romsets.md#formato-de-dat`).

Una vez descargado, el DAT se coloca en `metadata/dat/<Fuente>/` (o `metadata/sources/` si es un DAT crudo previo a retool) para que `tools/scripts/build-dat-index-*.ps1` pueda indexarlo — ver [custom-pipeline.md](custom-pipeline.md).

## 2. Conversión de DAT

Conversión, fusión o división del propio fichero DAT entre formatos (XML Logiqx, ClrMamePro texto, TOSEC), cuando la fuente original no entrega el formato necesario para el resto del flujo. No es un paso obligatorio en todos los sistemas. Detalle de uso: [dat-conversion.md](../tools/dat-conversion.md).

**Herramienta:** SabreTools (CLI) o SabreToolsStudio (interfaz gráfica sobre SabreTools).

## 3. Auditoría contra DAT

Verificación del romset físico contra el DAT (nombre, hash, completitud del set). Detalle de uso: [romset-audit.md](../tools/romset-audit.md).

**Herramienta principal:** JRomManager — auditoría rápida y multiplataforma de colecciones masivas.

**Alternativas:** ClrMamePro, RomCenter, RomVault.

**CHD con nombres o metadatos incorrectos:** no confiar en el nombre de archivo — curar por hash (SHA-1) contra el DAT oficial con RomVault, JRomManager o SabreTools Rebuild; `verifydump` para validar CHDs Redump contra su `.cue` oficial. Detalle completo en [optical-chd.md](optical-chd.md) (discos ópticos) y [arcade.md](arcade.md) (estructura de subcarpeta MAME).

## 4. Limpieza de romset

Eliminación de clones, contenido no deseado (mahjong, casino, contenido maduro en arcade) y duplicados cross-sistema, sobre el romset físico ya auditado. Detalle de uso: [romset-cleaning.md](../tools/romset-cleaning.md).

**Herramientas:** ROMSorter, Simple Arcade Multifilter (SAM, arcade).

**Relación con el pipeline propio:** `filter-by-title-type.ps1` y `filter-cross-system-duplicates.ps1` hacen una limpieza equivalente pero sobre `dat-index/<id>.json` (metadatos), antes de tocar ficheros físicos — ver [custom-pipeline.md](custom-pipeline.md).

## 5. Filtrado 1G1R

Generación del set 1G1R (una ROM por juego, según prioridad de región/idioma) a partir del romset completo ya auditado. Detalle de uso: [1g1r-filtering.md](../tools/1g1r-filtering.md).

**Herramienta principal:** retool.

**Alternativa:** DATROMTool.

**Relación con el pipeline propio:** retool produce los DAT curados en `data/dats/<sistema>/1g1r/`; `build-dat-index-1g1r.ps1` indexa después ese DAT curado — ver [custom-pipeline.md](custom-pipeline.md).

## 6. Parcheo (traducciones, hacks, bugfixes)

Aplicación de parches IPS/BPS/xdelta sobre una ROM limpia ya auditada. Detalle de uso: [patching.md](../tools/patching.md).

**Herramientas:** Lunar IPS (LIPS), Flips (Floating IPS), DeltaPatcher (xdelta).

## 7. Compresión / conversión de formato

Conversión al formato final de despliegue: CHD (discos ópticos, MAME), CSO/DAX (PSP/PS2), RVZ/ISO optimizada (GameCube/Wii). Detalle de uso: [conversion-compression.md](../tools/conversion-compression.md).

**Herramientas:** CHDMan, Maxcso, NKit, DolphinTool.

## 8. Organización en data/roms

Copia del romset ya procesado a `data/roms/`, la estructura final de despliegue a dispositivos.

**Pipeline propio:** `build-complete-romset.ps1` (staging) + `promote-complete-romset.ps1` (promoción, dry-run por defecto) — ver [custom-pipeline.md](custom-pipeline.md). No tiene guía propia en `docs/guides/tools/`.

## 9. Generación de gamelist.xml

Generación de `gamelist.xml` para el romset ya organizado en `data/roms/`. Detalle de uso: [gamelist-generation.md](../tools/gamelist-generation.md).

**Herramientas:** Skraper, SkyScraper, ES Scraper, SimpleScraper, gamelist-utils (conversión entre formatos).

No confundir con `generate-romset-docs.ps1`, que genera documentación en `docs/guides/romsets/systems/<id>.md` a partir de `dat-index/<id>.json`, no `gamelist.xml` — ver [custom-pipeline.md](custom-pipeline.md).

## 10. Obtención de media

Descarga de imágenes y vídeos asociados al romset, normalmente en el mismo paso que la fase 9 pero documentada aquí como tarea propia. Detalle de uso: [media-scraping.md](../tools/media-scraping.md).

**Herramientas:** Skraper, SkyScraper.

## Notas

[TODO]
