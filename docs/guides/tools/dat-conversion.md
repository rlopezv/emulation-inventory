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
