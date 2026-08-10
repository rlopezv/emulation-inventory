# Limpieza de romset

Eliminación de clones, contenido no deseado (mahjong, casino, contenido maduro) y duplicados cross-sistema, sobre el romset físico ya auditado (fase 3). No es un filtrado 1G1R completo (eso es la fase 5) — aquí se trata de recortar categorías enteras no deseadas, no de quedarse con una sola región por juego.

Corresponde a la fase 4 de [docs/guides/romsets/workflow.md](../romsets/workflow.md).

**Relación con el pipeline propio:** `filter-by-title-type.ps1` y `filter-cross-system-duplicates.ps1` (documentados en [docs/guides/romsets/custom-pipeline.md](../romsets/custom-pipeline.md)) hacen una limpieza equivalente pero sobre `dat-index/<id>.json` (metadatos), antes de tocar ficheros físicos. Esta guía cubre la limpieza posterior sobre el romset físico con herramientas de terceros.

## ROMSorter

**Fuente:** github.com/drakewill-CRL/ROMSorter. Aplicación de escritorio (no CLI), requiere .NET 6, Windows x64 principalmente (el componente "Librarian" sí es multiplataforma).

**Funciones confirmadas** (interfaz de botones, no scriptable):

- **Zip/Unzip all files** — comprime cada carpeta de ROMs a un ZIP individual (recomprime lo existente, extrae RAR/7z/TAR antes de comprimir) o descomprime todo.
- **Catalog Files / Verify Catalog** — genera un catálogo de nombres+hashes sin necesidad de leer los ficheros completos cada vez, y lo usa después para verificar integridad rápidamente.
- **Rename Single-File games** — renombra ROMs identificadas usando ficheros `.DAT`, compatible con TOSEC.
- **1G1R Sort** — selección 1 Game 1 ROM según prioridad de región (relevante también para la fase 5, pero disponible aquí como atajo si no se necesita el control fino de retool).
- **Everdrive Sort** — organiza en subcarpetas por letra inicial, pensado para flashcarts con límite de ficheros por carpeta.
- Conversión BIN/CUE e ISO → CHD (requiere `chdman` en el sistema).

[TODO: no se ha identificado en la documentación disponible una función específica de "limpieza" por categoría (mahjong/casino/adulto) — parece más orientado a organización/1G1R que a exclusión de categorías; para eso ver Simple Arcade Multifilter más abajo]

## Simple Arcade Multifilter (SAM)

**Fuente:** github.com/markwkidd/ahk-retroarch-playlist-helpers (script AutoHotKey). Pensado específicamente para sets arcade (MAME, FB Alpha).

**Entradas requeridas** (deben coincidir exactamente con la versión del romset a filtrar):

- **`catver.ini`** — fichero de categorización por género/tipo.
- **DAT XML** — metadatos del set. Ambos se obtienen de los repositorios correspondientes a la versión de MAME en uso (2000, 2003, 2010, 2014, 2016) o de FB Alpha.

**Flujo de uso confirmado (2 pasos):**

1. **Configuración** — indicar carpeta de ROMs de origen, DAT, `catver.ini` y carpeta de destino.
2. **Filtrado** — seleccionar categorías a incluir (`OR`) o excluir (`NOT`) mediante checkboxes; tres filtros adicionales disponibles: incluir BIOS, excluir clones, excluir juegos marcados como "Mature" (contenido maduro).

**Salida:** una carpeta nueva con el romset ya filtrado y organizado, incluyendo los BIOS asociados copiados según los criterios elegidos — lista para usar directamente en RetroArch/MAME.

## Notas

El resultado de esta fase alimenta la fase 5 (filtrado 1G1R, [1g1r-filtering.md](1g1r-filtering.md)): conviene limpiar categorías no deseadas (mahjong, casino, adulto, BIOS sueltas) antes de aplicar 1G1R, para no perder tiempo procesando contenido que se va a descartar de todos modos.

A diferencia de la fase 3 (auditoría), estas herramientas sí modifican o reorganizan ficheros directamente — hacer una copia de seguridad del romset auditado antes de ejecutar cualquiera de las dos, especialmente la primera vez.
