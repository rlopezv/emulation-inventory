# Scripts

Scripts del pipeline de romsets: indexado de DATs, construcción/promoción de sets completos, filtrado y generación de documentación. La mayoría son PowerShell (`pwsh tools/scripts/<script>.ps1`, entorno Windows nativo); algunos tienen además un equivalente Python (`python tools/scripts/<script>.py`, pensado para ejecutarse desde el devcontainer — ver `.devcontainer/`). Ambos caminos son válidos, ninguno sustituye al otro; el `.py` se valida contrastando su salida contra el `.ps1` correspondiente antes de darlo por bueno. Ver la cabecera de cada fichero para parámetros y ejemplos de uso completos.

## Sincronización de fuentes de trabajo (`sources/`)

`metadata/dat/<Fuente>/` es el archivo crudo (todo lo que se descarga, tal cual). `sources/dats/<fuente>/` es la copia de trabajo curada que leen los scripts de indexado — solo los sistemas realmente usados, sin duplicados por timestamp. Ejecutar antes de (re)indexar tras una descarga nueva.

| Script | Propósito |
| --- | --- |
| `update-sources.ps1` / `update-sources.py` | Sincroniza `sources/dats/no-intro/{pc,full,aftermarket}/` desde `metadata/dat/No-Intro/{pc,full,aftermarket}/`, según el manifiesto `config/nointro-systems.json` (id canónico → nombre base del DAT). Copia el fichero más reciente que coincida por sistema/pack, y avisa de sistemas sin descarga o de ficheros huérfanos en `sources/` que ya no están en el manifiesto. Equivalentes verificados: misma salida para el manifiesto completo. |

## Indexado de DAT (`metadata/dat-index/`)

| Script | Propósito |
| --- | --- |
| `build-dat-index-nointro.ps1` / `build-dat-index-nointro.py` | Genera `metadata/dat-index/<id>.json` a partir de DAT No-Intro (`sources/dats/no-intro/{full,aftermarket,pc}/`, resueltos por nombre base vía `config/nointro-systems.json`) o Non-Redump (nombre de fichero exacto en `metadata/dat/Non-Redump/`); agrupa familias 1G1R por relación parent/clone. Fuente del árbol seleccionable con `-SourceMode`/`--source-mode`: `FullAftermarket` (por defecto, `full`+`aftermarket` combinados vía `cloneofid`), `Pc` (árbol completo desde `pc/`, vía `cloneof` por nombre) o `Merged` (`FullAftermarket` completado con lo detectado solo en `pc/`). Genera además, si hay pack `pc/`, un informe de contraste bidireccional (`debug/<id>-pc-contrast.json`) y, si hay clonelist de retool, un informe de divergencias (`debug/<id>-clonelist-diff.json`). Equivalentes verificados por contenido (conjunto de familias) en 33 de 34 sistemas; NES tiene una discrepancia residual conocida (ver `docs/session-context.md`) causada por una ambigüedad pre-existente del algoritmo de fusión de alias manual ante colisiones de nombre canónico, no por la portabilidad en sí. |
| `build-dat-index-redump.ps1` / `build-dat-index-redump.py` | Igual que el anterior pero para DAT Redump (sin `cloneofid`); agrupa por clonelist o, si no existe, por nombre base exacto. Redump sigue la misma convención de nombrado que No-Intro (verificado: 99.6% cobertura de región, 98.8% coincidencia con metadata de retool en PSX), así que comparte el mismo diseño de `languages`/`members[]`/`revision`/`version`/`isAlt` y validación posterior contra `retool-clonelists-metadata` (`debug/<id>-language-diff.json`). Pendiente: tratamiento de multi-disco (`(Disc N)`) como caso distinto de revisión/alt — sin campo dedicado todavía. |
| `build-dat-index-tosec.ps1` | Igual que los anteriores pero para DAT TOSEC (sin `cloneofid`, convención de nombre con código de región de 2 letras). |
| `build-dat-index-1g1r.ps1` | Genera el índice a partir de los DAT ya curados 1G1R de `data/dats/console/1g1r/` (generados externamente con retool); no necesita agrupar por parent/clone, retool ya lo resolvió. |
| `inspect-dat-index.ps1` | Muestra un resumen de validación de un `metadata/dat-index/<id>.json` (total de familias, entradas sin región, distribución de categorías, muestra de alias). |
| `filter-by-title-type.ps1` | Limpia un índice dejando solo familias con `<game_id>` de un prefijo de Title ID permitido (uso: catálogos digitales Nintendo 3DS/DSi). |
| `filter-cross-system-duplicates.ps1` | Limpia un índice eliminando familias ya cubiertas por otro sistema relacionado (uso: `3dseshop` vs `3ds`). |
| `find-1g1r-duplicates.ps1` | Detecta nombres de familia duplicados dentro de un índice 1G1R generado por `build-dat-index-1g1r.ps1`. |

## Validación cruzada entre fuentes

| Script | Propósito |
| --- | --- |
| `compare-redump-mameredump.py` | Compara, por título completo (no por hash — no son comparables entre sí), el DAT oficial de Redump (`metadata/dat/Redump/`) contra el equivalente de `metadata/dat/MAMERedump/full/` (DAT estilo MAME con el SHA1 real del CHD, `github.com/MetalSlug/MAMERedump`) para los sistemas listados en `config/redump-mameredump-systems.json`. Soporta tanto el esquema `<machine>/<disk .chd>` (la mayoría) como `<game>/<rom>` estándar (GameCube/Wii, que usan `.rvz` en vez de CHD). Genera `metadata/dat-index/debug/<id>-redump-mameredump-diff.json` por sistema (títulos solo en Redump / solo en MAMERedump); puramente informativo, no bloquea nada ni modifica ningún DAT. `xbox` queda fuera del manifiesto a propósito: Redump lo cubre pero MAMERedump no publica CHD para él. |

## Conversión de esquema DAT

| Script | Propósito |
| --- | --- |
| `convert-cloneofid-to-parent-clone.ps1` / `convert-cloneofid-to-parent-clone.py` | Conversor genérico e independiente (no usa `dat-index` ni el manifiesto de sistemas): recibe uno o varios DAT Logiqx en esquema Standard (`id`/`cloneofid`, ej. `full`+`aftermarket` de No-Intro) y devuelve un único DAT fusionado en esquema Parent-Clone (`cloneof` por nombre completo, sin `id`), que es el que acepta un consumidor tipo RomCenter/Retool (no interpretan `id`/`cloneofid`). No aplica curación propia (no descarta Proto/Demo/Beta/etc., eso es trabajo de Retool aguas abajo); namespacea los `id` por fichero de origen para fusionar varias entradas sin colisión. El árbol de clones que produce es el mismo que ya trae el DAT de origen (`id`/`cloneofid` asignados por No-Intro) — el script solo traduce de esquema, no recalcula parentesco. |
| `generate-parent-clone-fullset.ps1` / `generate-parent-clone-fullset.py` | Driver de lote sobre el anterior: aplica `convert-cloneofid-to-parent-clone.ps1`/`.py` a `full`+`aftermarket` de **todos** los sistemas del manifiesto `config/nointro-systems.json` (o uno solo con `-SystemId`/`--system-id`), generando el DAT Parent-Clone de cada uno en `sources/dats/no-intro/fullset/` — la entrada real de Retool. Paso siguiente a `update-sources.ps1` en el flujo real, no un sustituto: primero `update-sources.ps1` sincroniza `sources/dats/no-intro/{pc,full,aftermarket}/` desde `metadata/dat/No-Intro/`, después este script convierte `full`+`aftermarket` al esquema que Retool necesita. |

## Filtrado 1G1R (Retool)

| Script | Propósito |
| --- | --- |
| `check-collection-vs-1g1r.py` | **Solo Python.** Compara una colección real de ROMs/discos contra los 3 DAT de `retool-1g1r-pipeline.py` (FULLSET, 1G1R FINAL, cuarentena) en dos pasadas: coincidencia exacta por nombre, y coincidencia normalizada (título base + región + tag de disco/lado si aplica, ignorando idioma/revisión/rerelease) para separar "de verdad no lo tienes" de "lo tienes pero Redump lo renombró" — este segundo caso es frecuente en colecciones grandes y sin esta distinción se confunde con huecos reales. Puede además: organizar los matches en carpetas `fullset/1g1r/japan` (`--output-fullset`/`--output-1g1r`/`--output-japan`, copy/move/symlink/hardlink); generar un CSV de renombrado propuesto (`--rename-plan`) a partir de los matches normalizados, **para revisar a mano antes de aplicarlo** con `--apply-renames` (nunca renombra ni sobrescribe sin ese paso explícito; filas con conflicto — mismo fichero, propuestas distintas entre capas — se marcan y se saltan); generar un CSV de faltantes reales (`--missing-report`, columnas `tier,title,expected_filename` — usa `--ext` para que el nombre esperado incluya extensión) por cada capa comparada, pensado como lista de descarga pendiente directamente accionable; y, con `--raw-dat` (el DAT Redump/No-Intro sin filtrar, antes del paso 1 de retool), separar los ficheros "sobrantes" de FULLSET en **excluidos a propósito** (demo/proto/aftermarket/unlicensed/multimedia — están en el catálogo completo pero el paso 1 los saca por diseño) frente a **desconocidos de verdad** (ni siquiera están en el catálogo sin filtrar — fichero mal nombrado, región no catalogada por Redump, u otra fuente); volcable a CSV con `--excluded-report` (columnas `category,filename`). |
| `tosec-nonstandard-labels.py` | **Solo Python.** Escanea uno o varios DAT TOSEC y clasifica cada etiqueta entre paréntesis/corchetes contra el vocabulario **oficial** de TOSEC (región/idioma/vídeo/copyright/estado de desarrollo/flags de dump, ver `docs/references.md#tosec`), sacando la frecuencia de las que NO encajan — diagnóstico previo a Igir, ver nota en `1g1r-filtering.md#igir`: el `DATParentInferrer` de Igir solo despoja el vocabulario oficial al agrupar 1G1R, así que una etiqueta de escena no oficial (`[k-file]` en `atari800`, `[CPM Version]`/`[master disk N]`/`[gunstick]` en `amstradcpc`, ambas confirmadas con este script) impide que Igir fusione variantes que en la práctica son el mismo contenido. Solo diagnóstico, no modifica nada — cada etiqueta que saca hay que revisarla a mano (algunas son ruido legítimo: requisito de hardware como `(130XE)`/`(OS-B)`, no duplicados). |
| `retool-1g1r-pipeline.py` | **Solo Python** (Retool no tiene binario Windows nativo, requiere el devcontainer — mismo motivo que `compare-redump-mameredump.py`). Automatiza el pipeline de 4 pasadas encadenadas con `--reprocess` documentado en `docs/guides/tools/1g1r-filtering.md#pipeline-recomendado--varias-pasadas-encadenadas-con---reprocess`: FULLSET (excluye todo lo no-oficial) → 1G1R-BASE (región+compilaciones) → INTERMEDIATE (superconjunto de idiomas) → FINAL + cuarentena (`--removesdat`). Recibe el DAT Parent-Clone oficial **sin modificar** (ej. `sources/no-intro/<Sistema> (Parent-Clone) (*).dat`) — no inyecta `region`/`language` propios: Retool los deriva del nombre del título por sí solo (confirmado leyendo `modules/dat/process_dat.py` del propio Retool), así que un conversor previo no aporta nada ahí. Ver la cabecera del fichero para el detalle completo de parámetros. **Configuración necesaria antes de usarlo** (ver más abajo). |

**Configuración que requiere `retool-1g1r-pipeline.py`, no incluida en el repo:**

1. **Docker Desktop corriendo** y la imagen `emulation-devcontainer` ya construida: `docker build -t emulation-devcontainer .devcontainer/` (contiene Retool + SabreTools, ver `.devcontainer/Dockerfile`).
2. **Copia local de `retool-clonelists-metadata`** con subcarpetas `clonelists/`, `metadata/`, `mias/`, `retroachievements/` — el valor por defecto de `--clonelist-dir` apunta a `sources/retool-clonelists-metadata/input/` (el clon git completo de `unexpectedpanda/retool-clonelists-metadata`, no la copia curada de nivel superior de `sources/retool-clonelists-metadata/`, que hoy no cubre todos los sistemas — ver `docs/dat-sources.md`). Si esa carpeta no existe todavía en tu entorno, clonar `https://github.com/unexpectedpanda/retool-clonelists-metadata` ahí o pasar `--clonelist-dir` a donde la tengas.
3. **DAT de entrada**: el Parent-Clone oficial de DAT-o-MATIC tal cual, sin pasar por ningún conversor propio (`sources/no-intro/<Sistema> (Parent-Clone) (*).dat`, sincronizado por `update-sources.ps1`/`.py`).
4. **Nombres de idioma exactos**: `--keep-languages`/`--quarantine-languages` deben usar los nombres tal como los espera Retool en `language order:` (ej. `Spanish (Latin American)`, no `es`) — la lista cerrada vive en `KNOWN_LANGUAGE_ORDER` dentro del propio script, copiada de la plantilla que genera Retool en su primer arranque; si una versión futura de Retool cambia esa lista, hay que actualizarla ahí a mano.
5. **Opcional, recomendado:** `--retool-config-dir` apuntando a una carpeta persistente propia (no la temporal por defecto dentro de `--output`) si vas a procesar varios sistemas — evita repetir el bootstrap de `config/internal-config.json` (única llamada de red del pipeline; el clonelist/metadata no se descarga porque ya viene montado desde el punto 2).

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
