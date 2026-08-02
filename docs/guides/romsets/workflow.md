# Preparación de romsets — Workflow end-to-end

[TODO: descripción breve]

Flujo completo de procesamiento de un romset desde el DAT de origen hasta su despliegue en `data/roms/`, encadenando las herramientas documentadas en `docs/software.md`. Complementa los flujos por tipo de fuente ([cartridge.md](cartridge.md), [optical-chd.md](optical-chd.md), [arcade.md](arcade.md)) detallando qué herramienta concreta se usa en cada paso.

## 1. Obtención del DAT

[TODO]

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
