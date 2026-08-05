# Preparación de romsets — Workflow end-to-end

[TODO: descripción breve]

Flujo completo de procesamiento de un romset desde el DAT de origen hasta su despliegue en `data/roms/`, encadenando las herramientas documentadas en `docs/software.md`. Complementa los flujos por tipo de fuente ([cartridge.md](cartridge.md), [optical-chd.md](optical-chd.md), [arcade.md](arcade.md)) detallando qué herramienta concreta se usa en cada paso.

## 1. Obtención del DAT

Punto de partida de todo el flujo: sin el DAT correcto no se puede auditar, filtrar ni renombrar nada. La fuente y el DAT concreto por sistema están fijados en `docs/romsets.md`; aquí se documenta dónde conseguirlos y con qué herramienta.

**No-Intro** (cartuchos, handhelds, la mayoría de microcomputers) — descarga manual desde el portal **DAT-o-MATIC** (datomatic.no-intro.org), la fuente oficial del grupo. Elegir el esquema Parent-Clone (P/C) si se va a aplicar 1G1R después (ver paso 3). Requiere cuenta gratuita del portal.

**Redump** (sistemas ópticos: PSX, PS2, Saturn, Dreamcast, GameCube, Wii, PC Engine CD, Sega CD, 3DO, Jaguar CD, Amiga CD32/CDTV, Neo Geo CD) — descarga manual desde **redump.org**, sección Datfiles de cada sistema.

**Non-Redump** — usar solo como fuente alternativa cuando `docs/romsets.md` lo indica (prototipos/betas no aceptados por Redump, o sistemas sin DAT Redump todavía como PS3/PSP/Xbox 360). Repositorio comunitario en GitHub (ver enlace por sistema en `docs/romsets.md`).

**TOSEC** — descarga del set completo (todas las plataformas en un único paquete) desde **tosec.org**; extraer solo el/los DAT del sistema necesario. Útil para microcomputers sin cobertura No-Intro (ej. `gx4000`).

**MAME / FBNeo (arcade)** — el DAT de MAME se genera localmente con `mame -listxml > mame.xml` desde el propio ejecutable (no se descarga como fichero suelto); FBNeo se obtiene del repositorio oficial en GitHub o se genera igual que MAME con el volcado XML integrado del emulador. Ver `docs/references.md#dats` para el detalle de qué sistemas cubre cada uno.

**libretro (ClrMamePro texto)** — DATs mantenidos en el repositorio `libretro-database` de GitHub; usados para sistemas sin cobertura adecuada en las fuentes anteriores (ej. `spectrum`, `zx81`, `scummvm`, `dos`). Formato de texto plano, no XML — requiere parser distinto (ver `docs/romsets.md#formato-de-dat`).

Herramienta de manipulación de DAT en sí (convertir, mezclar, dividir ficheros DAT, no romsets): **SabreTools** (CLI) o **SabreToolsStudio** (interfaz gráfica).

Una vez descargado, el DAT se coloca en `metadata/dat/<Fuente>/` (o `metadata/sources/` si es un DAT crudo previo a retool) para que `tools/scripts/build-dat-index-*.ps1` pueda indexarlo — ver `docs/guides/romsets/custom-pipeline.md`.

## 2. Auditoría contra DAT

**Herramienta principal:** JRomManager — auditoría rápida y multiplataforma de colecciones masivas.

**Alternativas:** ClrMamePro, RomCenter, RomVault.

**Manipulación pura de DAT** (conversión, mezcla, división de archivos DAT en sí, no de romsets): SabreTools (CLI) o SabreToolsStudio (interfaz gráfica sobre SabreTools).

**CHD con nombres o metadatos incorrectos:** no confiar en el nombre de archivo — curar por hash (SHA-1) contra el DAT oficial con RomVault, JRomManager o SabreTools Rebuild; `verifydump` para validar CHDs Redump contra su `.cue` oficial. Detalle completo en [optical-chd.md](optical-chd.md) (discos ópticos) y [arcade.md](arcade.md) (estructura de subcarpeta MAME).

[TODO: pasos concretos]

## 3. Filtrado 1G1R

**Herramienta principal:** retool.

**Alternativa:** DATROMTool.

[TODO: pasos concretos]

## 4. Parcheo (traducciones, hacks, bugfixes)

[TODO: Lunar IPS / Flips / DeltaPatcher]

## 5. Compresión / conversión de formato

[TODO: CHDMan / Maxcso / NKit]

## 6. Organización en data/roms

[TODO]

## 7. Generación de gamelist.xml y media

[TODO]

## Notas

[TODO]
