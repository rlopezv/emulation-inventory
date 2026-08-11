# Preparación de romsets — Óptico → CHD

[TODO: descripción breve]

Aplica a sistemas ópticos verificados con DAT Redump (o Non-Redump para protos/betas cuando no hay DAT Redump; ver `docs/romsets.md`).

## Fuente

[TODO]

## Verificación contra DAT Redump

Cuando un CHD tiene el nombre de archivo incorrecto o metadatos alterados, no se puede confiar en el nombre: hay que leer el hash interno (SHA-1) del CHD y de la ROM asociada, cruzarlo contra el DAT oficial (Redump o Non-Redump) y renombrar/reestructurar la colección a partir de esa firma real, no del nombre de fichero.

**RomVault** — opción más precisa para CHDs. Usa internamente la lógica de `chdman` para leer la cabecera y descomprimir/verificar el SHA-1 real oculto dentro del CHD, busca el juego correcto en el DAT y renombra/mueve automáticamente a la sintaxis oficial.

**JRomManager** — soporte nativo para esquemas Merged/Non-Merged/Split con cálculo de SHA-1 profundo. Detecta archivos "huérfanos" o mal nombrados, los empareja contra el DAT y aplica la función `Fix` para renombrar tanto el contenedor de la ROM como el CHD.

**SabreTools (Rebuild)** — reconstrucción vía CLI: apunta a la carpeta desorganizada como origen y a un DAT limpio; lee los hashes sin importar el nombre de archivo y genera un romset nuevo, correctamente renombrado, en la carpeta de destino.

[TODO: no se ha podido confirmar la sintaxis exacta del comando de rebuild/sort de SabreTools ni hasta qué algoritmo de hash llega (se citaba SHA-512, sin confirmar) — consultar la página "Sort" de su wiki oficial antes de dar el comando por definitivo]

**verifydump** — cruza el CHD contra los `.cue` oficiales de Redump para validar que la estructura interna del volcado es correcta al 100%, antes de organizarlo. **No es específico de PS1/PS2/Saturn/Dreamcast** — es aplicable a cualquier sistema óptico de Redump, ya que Redump nunca distribuye CHD oficialmente para ningún sistema (siempre `.bin`/`.cue` o `.iso`); ver detalle completo, mecanismo exacto y optimización con RAM disk en [romset-audit.md](../tools/romset-audit.md#validación-de-chd-por-hash-verifydump).

### Caso especial — GameCube / Wii (RVZ en vez de CHD)

GameCube y Wii no usan CHD: el contenedor moderno es **RVZ**, creado por el propio equipo de Dolphin, por lo que la comunidad no recurre a gestores externos tipo RomVault/JRomManager sino a las herramientas oficiales de Dolphin. RVZ es lossless si se configura correctamente: comprime el disco pero conserva los hashes MD5/SHA-1 como si fuera la ISO original descomprimida, lo que permite que herramientas como JRomManager auditen directamente archivos RVZ configurando el DAT de Redump correspondiente.

**DolphinTool (CLI)** — equivalente a `chdman` para la infraestructura Nintendo. Subcomando confirmado **`header`** (no `read-id`, corregido): `dolphin-tool header -i archivo.rvz` devuelve, entre otros datos, el `Game ID` (código único de 6 caracteres, ej. `GALE01` para Super Smash Bros. Melee — ejemplo real de la documentación oficial), nombre interno, revisión, región y país. El subcomando `verify` calcula además CRC32/MD5/SHA1 tanto de ISO como de RVZ, con verificación bit-exacta confirmada contra el original. Con esto se puede automatizar el renombrado masivo en Bash/PowerShell contra una base de datos limpia de Redump.

**Interfaz nativa de Dolphin (por lotes)** — existe la opción **"Convert Selected Files"** (clic derecho, requiere Dolphin ≥5.0-12188) para convertir varios ISO/RVZ a la vez. **No confirmado que renombre automáticamente** a partir del nombre/región leído — un hilo del foro oficial de Dolphin pide precisamente esta función como *feature request* ("Batch ISO Renaming"), lo que sugiere que no viene implementada de forma nativa; para renombrado automático, usar el subcomando `header` de DolphinTool en un script propio en su lugar.

**Dolphin RVZ/ISO Conversion Scripts (ElektroStudios)** — scripts de automatización de la comunidad que envuelven DolphinTool para convertir en lote de forma bidireccional (ISO ⇄ RVZ), configurable en formato/nivel de compresión y tamaño de bloque. [TODO: la documentación del proyecto no menciona ningún porcentaje de ahorro de espacio concreto — no citar cifras sin confirmar]

**Paso previo obligatorio — retool** — igual que con sistemas de CD, filtrar primero el DAT de Redump de GameCube/Wii con retool para generar la lista 1G1R antes de dejar que Dolphin identifique y renombre solo los RVZ que pasaron el filtro; evita duplicar gigabytes de datos comprimidos innecesariamente.

## Conversión a CHD

[TODO]

## Organización en data/roms

[TODO]

## Generación de gamelist.xml y media

[TODO]

## Notas

[TODO]
