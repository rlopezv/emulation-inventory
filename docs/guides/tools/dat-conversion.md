# Conversión de DAT

Conversión, fusión y división del propio fichero DAT (no de romsets) entre formatos — Logiqx XML, ClrMamePro texto, RomCenter, SabreDAT JSON/XML — cuando la fuente original no entrega el formato necesario para el resto del flujo. No es un paso obligatorio en todos los sistemas: solo aplica cuando el DAT obtenido en la fase 1 no está ya en el formato que espera la herramienta de auditoría/filtrado de las fases siguientes.

Corresponde a la fase 2 de [docs/guides/romsets/workflow.md](../romsets/workflow.md).

## SabreTools (CLI)

**Fuente:** github.com/SabreTools/SabreTools. Herramienta de referencia para manipulación masiva de DAT — la misma usada para la generación manual desde directorio en [dat-generation.md](dat-generation.md#generación-manual-desde-directorio-dat-from-dir).

**Confirmado en la wiki oficial:** el comando de conversión/manipulación es `--update` (alias `-ud`).

### Conversión de formato

```bash
SabreTools --update --output-type=xml --output-dir=OutDir Path\To\DatFile.dat
```

El flag `-ot=`/`--output-type=` admite múltiples instancias (se puede pedir varios formatos de salida a la vez de la misma pasada). Formatos de salida soportados: Logiqx XML, ClrMamePro, RomCenter, SabreDAT JSON, SabreDAT XML, Separated Value (CSV/TSV).

Ejemplo — convertir una carpeta completa de DATs a ClrMamePro, excluyendo los atributos de relación padre/clon:

```bash
SabreTools --update --output-type=cmp --exclude-of=romof --exclude-of=sampleof --exclude-of=cloneof Path\To\Dats
```

### Fusión (merge)

`--merge` — todos los DAT de entrada se combinan en un único fichero de salida.

### División (split)

Comando `-sp`/`--split`, con varios criterios disponibles:

- **Por extensión** (`-es`/`--extension`) — separa en dos DAT según listas de extensiones (`-exta=`/`-extb=`).
- **Por hash** (`-hs`/`--hash`) — usa el orden de preferencia Nodump > SHA-512 > SHA-384 > SHA-256 > SHA-1 > MD5 > CRC.
- **Por tamaño de archivo** (`-szs`/`--size`, con `-rad=`/`--radix=` para el umbral).
- **Por tamaño total del juego** (`-tis`/`--total-size`, con `-cs=`/`--chunk-size=`).
- **Por tipo de archivo** (`-ts`/`--type`) — separa ROMs de discos.

[TODO: la wiki indica que la división jerárquica por niveles ("Currently is not fully implemented") no está completa — verificar estado actual antes de depender de ella]

Además, específico para relación Parent-Clone:

- `-ds`/`--dat-split` — elimina archivos redundantes entre padres e hijos según los atributos `romof`/`cloneof`.
- `-dm`/`--dat-merged` — genera sets fusionados (Merged).
- `-dnm`/`--dat-non-merged` — genera sets no fusionados (Non-Merged).

(Ver `docs/references.md#romsets-arcade` para el significado de Split/Merged/Non-Merged aplicado al romset físico, no solo al DAT.)

### Filtrado por tipo de título

Excluye entradas del DAT por nombre — confirmado como alternativa a retool para fuentes que retool no soporta (TOSEC, MAME...), ver `docs/session-context.md`. Mismo comando `update` (`ud`), flag `-fi=`/`--filter=`:

```bash
sabretools update -ot=Logiqx -fi='machine.name!=<regex>' -out=OutDir Path\To\DatFile.dat
```

`type.key!=valor` excluye lo que SÍ coincide con `valor` (el `!` significa "no coincidente" — el resultado se queda con lo que NO matchea). Claves habituales: `machine.name`, `game.name`, `machine.category`, `item.romof`. Acepta regex completa (C#), no solo coincidencia exacta.

**Dos comportamientos reales a tener en cuenta (verificados, no documentados así en la wiki oficial):**

1. **Varios `-fi=` se combinan en AND, no en OR.** Pedir "excluir demo" + "excluir proto" en dos flags separados **no excluye nada** (un ítem tendría que matchear las dos condiciones a la vez). Para excluir varias etiquetas hace falta **una sola regex con alternancia**: `-fi='machine.name!=.*(demo|proto).*'`.
2. **Una regex de substring sin anclar da falsos positivos reales.** `.*proto.*` eliminó *"4th Protocol, The"* (contiene "proto" como substring). Hay que anclar al paréntesis/corchete completo de la convención de nombrado real de la fuente (ver más abajo para TOSEC) — no basta con "contiene la palabra".

#### Caso confirmado: excluir demos/preproducción/bad dumps de TOSEC

Para DAT que siguen la convención de nombrado real de TOSEC (`docs/references.md#tosec` — **no** la convención simplificada que había antes en ese documento, corregida contra la especificación oficial en esta misma sesión), la regex validada contra los 30 DAT reales del catálogo (`sources/tosec/out/*.dat`, ver `docs/session-context.md`) es:

```bash
sabretools update -ot=Logiqx \
  -fi='machine.name!=.*(\((demo|demo-kiosk|demo-playable|demo-rolling|demo-slideshow|alpha|beta|preview|pre-release|proto)\)|\[b\]).*' \
  -out=process/out/<sistema>/dat \
  "sources/tosec/out/<fichero>.dat"
```

Cubre tres campos reales de la convención TOSEC: `(demo)` (5 variantes), `(estado de desarrollo)` (`alpha`/`beta`/`preview`/`pre-release`/`proto`) y el flag de dump `[b]` (bad dump). **No** cubre Applications/Audio/BIOS/Bonus discs/Coverdiscs/Educational/Manuals/Multimedia/Video ni Unlicensed/Aftermarket/Pirate/MIA/Add-ons/Promotional — TOSEC publica esas categorías como DAT separados por categoría (no mezclados en el DAT de "Games"), y "Unlicensed"/"Aftermarket"/"Pirate" no son valores reales del campo "estado de copyright" de TOSEC (`CW`/`CW-R`/`FW`/`GW`/`GW-R`/`LW`/`PD`/`SW`/`SW-R`) — son conceptos de No-Intro/Redump, no aplican aquí.

Resultado real (30 DAT, 17 sistemas TOSEC): **221.127 → 211.976 juegos (9.151 excluidos, ~4,1%)**. Verificado 0 residuales y sin falsos positivos en varios sistemas (`amstradcpc`, `amiga`, `atarist`), no solo en la primera prueba. `zx81` no excluyó nada (catálogo simple, plausible).

**Convención de destino**: el resultado filtrado va en `process/out/<sistema>/<tipo>/` (`tipo` = `dat`/`auxiliar`/`config`, mismo espacio que `dat_processing`) — distinto de `process/<clave>/<tipo>/<source_id>/` (extracción cruda sin filtrar, la que genera `dat-processing extract`). Este segundo nivel (`process/out/`) todavía se genera a mano por CLI, sin módulo Python propio en `tools/application`.

## SabreToolsStudio (GUI)

**Fuente:** github.com/Eggmansworld/SabreToolsStudio. Interfaz gráfica portátil sobre SabreTools, sin instalación, para Windows y Linux.

Siete funciones principales confirmadas: creación de DAT desde carpeta (múltiples algoritmos de hash), reconstrucción de colecciones (TorrentZip, Zstandard Zip, TAR), verificación contra DAT con generación de fixdats, actualización de DAT (conversión de formato, fusión con deduplicación, filtros 1G1R), división de DAT (por extensión/tamaño/tipo), estadísticas (CSV/HTML/TSV) y construcción visual de scripts por lotes.

**Estado:** actividad limitada en el repositorio (14 commits, sin releases publicadas) — funcional pero sin garantía de mantenimiento activo. Preferir SabreTools (CLI) para automatización o si esta GUI da problemas.

## Alternativas

### DatUtil (Logiqx)

**Fuente:** logiqx.com/Tools/DatUtil/DatUtil.php. Herramienta clásica del propio creador del formato Logiqx XML; confirmado que convierte, depura y compara DAT entre gestores (ClrMamePro, RomCenter), no solo hacia RomCenter como se documentó inicialmente en [dat-generation.md](dat-generation.md) (sección HyperList, donde se descartó como vía hacia HyperList — sigue siendo válida como conversor DAT en general, que es lo que cubre esta fase).

Formatos válidos confirmados: `listinfo`, `listxml`, `romcenter2`, `delimited`, `titlelist`, `sublist`.

```bash
datutil -f romcenter list.xml
```

Convierte `list.xml` (Logiqx) a formato RomCenter. Cambiar `-f` por el formato de salida deseado de la lista anterior.

### JRomManager

**Fuente:** ver también [romset-audit.md](romset-audit.md) — es la herramienta principal de auditoría (fase 3), pero también exporta DAT en varios formatos desde el menú emergente del visor de perfiles: **Logiqx**, **MAME**, **Software List** y **Software Lists**.

**Nota de comportamiento:** por defecto usa "explicit merging" (separa solo según el atributo `merge`), a diferencia de ClrMamePro que separa en cuanto una ROM del set padre comparte CRC con un hijo, aunque no tenga atributo `merge`; para replicar el comportamiento de ClrMamePro, activar la opción "implicit merge" en la configuración del perfil.

## Notas

El DAT convertido se coloca junto al original en `metadata/dat/<Fuente>/` (o se sobrescribe si el objetivo es solo cambiar de formato, conservando una copia del original hasta confirmar que el nuevo audita correctamente — ver `Notas` en [dat-generation.md](dat-generation.md)).

No confundir esta fase con el **filtrado 1G1R** (fase 5, [1g1r-filtering.md](1g1r-filtering.md)): SabreTools puede aplicar filtros 1G1R durante una actualización de DAT, pero la herramienta de referencia del repo para ese paso es retool, no SabreTools — usar SabreTools aquí solo para conversión/fusión/división de formato, no como sustituto de retool.
