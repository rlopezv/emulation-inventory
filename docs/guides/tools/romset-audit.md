# Auditoría de romset contra DAT

Verificación del romset físico (nombre, hash, completitud del set) contra el DAT ya obtenido/convertido en las fases 1-2. No modifica el romset por sí sola en modo auditoría pura — identifica qué falta, qué sobra y qué tiene un hash incorrecto; la corrección (renombrado, reconstrucción) es un paso posterior opcional de cada herramienta.

Corresponde a la fase 3 de [docs/guides/romsets/workflow.md](../romsets/workflow.md). Para CHD con nombre o metadatos poco fiables, curar por hash (SHA-1) en vez de por nombre de fichero — ver [Validación de CHD por hash](#validación-de-chd-por-hash-verifydump) más abajo.

## JRomManager

**Fuente:** optyfr.github.io/JRomManager (Java, multiplataforma).

**Flujo básico confirmado** (wiki oficial, sección Scanner):

1. Crear/cargar un perfil y añadir el DAT correspondiente.
2. En la pestaña **Folders**: indicar la carpeta destino de ROMs (obligatoria) y opcionalmente carpetas fuente adicionales (admite arrastrar y soltar).
3. Configurar opciones de escaneo: **Calculate All SHA1** (calcula SHA1 de cada fichero encontrado en los archivos comprimidos — más lento porque implica descomprimir), **Enable Multithreading** (usa todos los núcleos disponibles), **Create missing sets** (si está desactivado, solo se pueden corregir sets ya existentes, no crear los que faltan del todo).
4. Elegir el modo de fusión: **Split**, **Non-Merged** o **Merged** (Scan/Fix/Rebuild disponibles para los tres, con gestión de colisiones de nombre).
5. Filtrado opcional por sistema, clones, discos, samples, tipo de mueble o año — si se cambia el filtro, hay que re-escanear antes de aplicar cualquier corrección.
6. Lanzar el scan; el resultado se puede exportar como reporte.

[TODO: no se pudo confirmar el detalle exacto de los reportes generados (Missing/Have/Duplicados) por limitaciones de acceso a esa sección del wiki]

## ClrMamePro

**Fuente:** mamedev.emulab.it/clrmamepro (Windows).

Combina dos componentes: un **Scanner** que audita la colección, y un **Rebuilder** que reconstruye los ficheros según las reglas del romset (merge/split/non-merged).

**Flujo básico confirmado:**

1. Cargar o crear un perfil: **"Add DatFile"** → seleccionar el `.dat` → Open.
2. Configurar la pestaña **Scanner** (carpeta de ROMs a auditar).
3. Opcionalmente, pestaña **Rebuilder** — solo necesaria si se quiere reconstruir automáticamente lo que el Scanner marque como faltante/incorrecto.
4. Para Software Lists específicamente, pestaña **Misc** → **"Create rompath for new dat"**, apuntando a la carpeta raíz donde están todas las carpetas de Software Lists.
5. El Scanner genera un fichero de reporte en su carpeta de escaneo con los problemas detectados; si la corrección automática está activada, los problemas ya corregidos no aparecen en el reporte final (solo quedan los pendientes).

También soporta modo batch (`Profile Batchrun`) con las mismas tres pestañas (Scanner/Rebuilder/Misc) para automatizar la auditoría de varios perfiles sin intervención manual.

## RomVault

**Fuente:** romvault.com / wiki.romvault.com.

**Niveles de escaneo confirmados** (wiki oficial, "Scanning / Fixing Levels"):

| Nivel | Escaneo | Descripción |
| --- | --- | --- |
| 1 — Quick Scan | Solo ficheros modificados desde el último escaneo; lee cabeceras, no descomprime | Útil mientras aún no se ha decidido la ubicación definitiva del romset |
| 2 — Normal Scan (por defecto) | Ficheros modificados, descomprime y calcula hash completo (CRC/MD5/SHA1) | Recomendado en casi todas las situaciones |
| 3 — Complete Rescan | Todos los ficheros, descompresión y hash completo | Solo si se sospecha corrupción de datos |

**Niveles de reparación (Fix), en paralelo a los de escaneo:**

| Nivel | Reparación | Descripción |
| --- | --- | --- |
| 1 — Quick Fix | Compara solo tamaño y CRC | Solo válido si el romset se escaneó con Nivel 1 |
| 2 — Normal Fix (por defecto) | Compara CRC/MD5/SHA1 completo | Recomendado para la mayoría de casos, evita colisiones de hash |
| 3 — Complete Rebuild | Descomprime y recomprime todos los ficheros | Generalmente innecesario en uso normal |

[TODO: no se pudo confirmar el flujo exacto de configuración inicial de un DatRoot (páginas "Windows Setup"/"quick_start" de la wiki no existen todavía) — consultar directamente la sección "Organizing DATs" de la wiki al usarlo]

## RomCenter

**Fuente:** romcenter.com (Windows).

Audita visualmente por colores: marca cada set en **verde** (correcto), **naranja** (corregible) o **rojo** (roto/incompleto), y permite aplicar las correcciones por lotes controlados.

**Flujo básico:** importar el DAT correspondiente → escanear la carpeta de ROMs → opcionalmente hacer primero una pasada de solo-renombrado (alinea nombres sin tocar el contenido) antes de aplicar reparaciones dirigidas sobre alternativas ya conocidas como válidas.

[TODO: no se ha podido confirmar el detalle paso a paso con la misma precisión que RomVault/ClrMamePro/JRomManager — verificar contra la documentación oficial o el propio programa antes de tratarlo como definitivo]

## Validación de CHD por hash (verifydump)

**Fuente:** github.com/j68k/verifydump. Cruza CHDs (o RVZ) contra el `.cue` oficial de Redump para validar la estructura interna del volcado, útil cuando el nombre de archivo no es fiable — ver también [optical-chd.md](../romsets/optical-chd.md).

**Sintaxis confirmada:**

```bash
verifydump "Datfile.zip" "C:\Games\SystemName"
```

- **Input:** el Datfile (puede ir comprimido en `.zip`) y la ruta con los CHD/RVZ a verificar.
- **Dependencias externas** (deben estar en el `PATH`): `chdman` y `binmerge` para `.chd`; `DolphinTool` para `.rvz`.
- **Salida:** reporte por fichero (`Dump verified correct and complete` o el error correspondiente) y resumen final (`Successfully verified N dumps`).
- **Flags útiles:** `--verbose` (detalle paso a paso), `--extra-cue-source` (`.cue` de referencia adicional, ver más abajo), `--allow-cue-file-mismatches` (ignora discrepancias de metadatos no soportados por CHD).

**Mecanismo exacto:** `verifydump` descomprime el CHD/RVZ de vuelta a `.bin`/`.cue` (con `chdman`+`binmerge`, o `DolphinTool`) y compara ese `.cue` regenerado contra un `.cue` de referencia (pasado con `--extra-cue-source`), ignorando metadatos que el contenedor comprimido no conserva — no compara el CHD directamente contra el Datfile.

**Aplicable a cualquier sistema óptico de Redump, no solo a "los que usan CHD":** Redump nunca distribuye CHD oficialmente para ningún sistema — su formato de distribución siempre es `.bin`/`.cue` o `.iso`; el CHD es siempre una conversión posterior (fase 7, [conversion-compression.md](conversion-compression.md)). Como la verificación se apoya en el `.cue`, no en un DAT "en formato CHD", la técnica es genérica para todo el catálogo óptico de Redump — el `.cue` oficial se descarga aparte, en la sección **Cuesheets** de Redump (ver [dat-generation.md](dat-generation.md#redump)).

**Optimización de rendimiento — RAM disk para el directorio temporal:** confirmado en la propia documentación oficial de `verifydump`, que lo recomienda explícitamente si se va a verificar la colección con mucha frecuencia. La herramienta usa el directorio temporal del sistema (variable `TEMP`), no un flag propio — para desviarlo a RAM:

1. Crear un disco virtual en RAM con **ImDisk Virtual Disk Driver** (ltr-data.se, gratuito y de código abierto):

   ```powershell
   imdisk -a -s 2G -m Z: -p "/fs:ntfs /q /y"
   ```

2. Apuntar la variable `TEMP` de la sesión a esa unidad antes de ejecutar `verifydump`:

   ```powershell
   $Env:TEMP = "Z:\"
   ```

3. Al descomprimir el CHD/RVZ para verificarlo, todo el trabajo temporal ocurre en RAM en vez de en el SSD/HDD — más velocidad y sin desgaste del disco físico. El contenido se pierde al apagar o desmontar el disco virtual, lo cual es intencional (son solo ficheros intermedios de verificación).

### Identificación rápida de CHD/RVZ sin descomprimir (RAHasher)

**Fuente:** github.com/nixxou/RAHasher. Alternativa mucho más ligera que `verifydump` para un caso de uso distinto: **identificar** qué juego es un CHD/RVZ mal nombrado, no verificar bit a bit que el volcado es perfecto.

**Confirmado técnicamente:** RAHasher descomprime el CHD/RVZ **en memoria, sobre la marcha** — no genera `.bin`/`.cue`/`.iso` intermedios en disco, por lo que no necesita `chdman`, `binmerge` ni `DolphinTool` como dependencias externas. Para Wii, además re-encripta las particiones (AES-128) y recalcula sus hashes H0/H1/H2 internos, de modo que ve el disco exactamente igual que el original sin descifrar.

```bash
RAHasher.exe ? "Animal Crossing - Let's Go to the City (Europe).rvz"
```

El `?` deja que RAHasher detecte el sistema automáticamente a partir de la cabecera del RVZ/CHD. Con el hash resultante, cruzar contra `retroachievements/<Sistema>.json` de `retool-clonelists-metadata` (ver [dat-generation.md](dat-generation.md#redump)) para identificar el título exacto.

**Limitación confirmada:** para RVZ, solo soporta el códec de compresión **Zstd** (el que usa RVZ por defecto) — imágenes comprimidas con LZMA/LZMA2/bzip2 se rechazan explícitamente en vez de calcular un hash incorrecto en silencio.

**No sustituye a `verifydump`:** el hash de RetroAchievements cubre solo una parte del disco (ej. el ejecutable de arranque en PS1), no el volcado completo — válido para identificar/renombrar rápido, no para certificar que el CHD es una copia perfecta y completa del original. Para eso, seguir usando `verifydump` contra el `.cue` oficial de Redump.

## Notas

El resultado de la auditoría (fase 3) alimenta directamente la fase 4 (limpieza de romset, [romset-cleaning.md](romset-cleaning.md)) y la fase 5 (filtrado 1G1R, [1g1r-filtering.md](1g1r-filtering.md)): no tiene sentido aplicar ninguna de las dos sobre un romset que todavía no se sabe si está completo o corrupto.

Todas las herramientas de esta fase distinguen entre **auditar** (solo reportar) y **corregir/reconstruir** (mover, renombrar o recomprimir ficheros); conviene ejecutar siempre primero en modo solo-reporte antes de activar cualquier corrección automática, especialmente la primera vez que se audita una colección nueva.
