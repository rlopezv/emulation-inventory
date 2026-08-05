# Scripts

Scripts PowerShell del pipeline de romsets: indexado de DATs, construcción/promoción de sets completos, filtrado y generación de documentación. Todos se ejecutan con `pwsh tools/scripts/<script>.ps1` desde la raíz del repo; ver la cabecera de cada fichero para parámetros y ejemplos de uso completos.

## Indexado de DAT (`metadata/dat-index/`)

| Script | Propósito |
| --- | --- |
| `build-dat-index-nointro.ps1` | Genera `metadata/dat-index/<id>.json` a partir de DAT No-Intro/Non-Redump (con `cloneofid`), agrupando familias 1G1R por relación parent/clone. |
| `build-dat-index-redump.ps1` | Igual que el anterior pero para DAT Redump (sin `cloneofid`); agrupa por clonelist o, si no existe, por nombre base exacto. |
| `build-dat-index-tosec.ps1` | Igual que los anteriores pero para DAT TOSEC (sin `cloneofid`, convención de nombre con código de región de 2 letras). |
| `build-dat-index-1g1r.ps1` | Genera el índice a partir de los DAT ya curados 1G1R de `data/dats/console/1g1r/` (generados externamente con retool); no necesita agrupar por parent/clone, retool ya lo resolvió. |
| `inspect-dat-index.ps1` | Muestra un resumen de validación de un `metadata/dat-index/<id>.json` (total de familias, entradas sin región, distribución de categorías, muestra de alias). |
| `filter-by-title-type.ps1` | Limpia un índice dejando solo familias con `<game_id>` de un prefijo de Title ID permitido (uso: catálogos digitales Nintendo 3DS/DSi). |
| `filter-cross-system-duplicates.ps1` | Limpia un índice eliminando familias ya cubiertas por otro sistema relacionado (uso: `3dseshop` vs `3ds`). |
| `find-1g1r-duplicates.ps1` | Detecta nombres de familia duplicados dentro de un índice 1G1R generado por `build-dat-index-1g1r.ps1`. |

## Construcción de romsets (`data/roms/`, colección física)

| Script | Propósito |
| --- | --- |
| `create-roms-structure.ps1` | Crea la estructura de carpetas destino en `data/roms/` (arcade/console/micro por identificador canónico), con stub de `gamelist.xml` y carpeta `media/`. |
| `build-complete-romset.ps1` | Construye un romset "completo" de un sistema aplanando raíz + subcarpetas válidas (jpn/unl/pack/etc.) más `_extra/`, excluyendo carpetas de trabajo (`_SD`, `duplicates`, `raw`). |
| `promote-complete-romset.ps1` | Promociona el romset "completo" generado por el script anterior a la carpeta final, sustituyendo el contenido previo (modo simulación por defecto; requiere `-Execute`). |
| `strip-retool-tag.ps1` | Renombra ficheros quitando el sufijo `(Retool ...)` que retool añade tras el nombre base. |

## Documentación

| Script | Propósito |
| --- | --- |
| `generate-romset-docs.ps1` | Genera/actualiza la sección auto-generada de cada `docs/guides/romsets/systems/<id>.md` a partir del índice correspondiente, y regenera la tabla índice de `systems/README.md`. |

## Scripts de un solo uso

| Script | Propósito |
| --- | --- |
| `add-wikipedia-refs.ps1` | Inserta la sección "Fuentes de referencia" con enlace de Wikipedia en cada `docs/guides/romsets/systems/<id>.md`. Ya ejecutado; no forma parte del pipeline habitual. |
| `fix-wikipedia-refs-blank-line.ps1` | Corrige la falta de línea en blanco tras la inserción de `add-wikipedia-refs.ps1`. Ya ejecutado. |
| `test-wiki-match-gamegear.ps1` | Prueba de emparejamiento de títulos de Wikipedia contra `metadata/dat-index/gamegear.json`; script exploratorio, no reutilizable directamente. |
