# Preparación de romsets — Óptico → CHD

[TODO: descripción breve]

Aplica a sistemas ópticos verificados con DAT Redump (o Non-Redump para protos/betas cuando no hay DAT Redump; ver `docs/romsets.md`).

## Fuente

Patrón general de la fuente (Redump / Non-Redump / MAMERedump, qué rol cumple cada una) documentado en [sources.md](sources.md#redump-patrón-general-y-alternativas) — aquí solo la vista aplicada a este flujo.

La mayoría de sistemas ópticos sigue el patrón completo (Redump como principal, Non-Redump como alternativa solo para protos/betas): `psx`, `saturn`, `segacd`, `dreamcast`, `3do`, `amigacdtv`, `amigacd32`, `jaguarcd`, `pcenginecd`, `xbox`, `gamecube`, `wii`. Desviaciones del patrón:

- **Solo Non-Redump, sin Redump todavía** — `ps3`, `xbox360`, `wiiu`, `cdi`: no es que Non-Redump sea la fuente elegida por algún motivo, es que Redump no publica DAT de estos sistemas a día de hoy; Non-Redump cubre el hueco entero, no solo protos/betas.
- **Solo Redump, sin Non-Redump** — `psp`: cubierto solo por Redump, sin fuente alternativa anotada en `docs/romsets.md`.
- **Redump + alternativa distinta de Non-Redump** — `neogeocd`: la alternativa es un software-list XML de MAME (`metadata/software-list/neocd.xml`), no un DAT Non-Redump — sirve para verificación de CHD, no como fuente de romset alternativa.

## Formato de ROM recomendado por sistema

Sistemas clasificados como Óptico en [docs/guides/romsets/README.md](README.md#clasificación-de-sistemas-por-flujo). Redump nunca distribuye CHD directamente (siempre `.bin`/`.cue` o `.iso`); cuando el formato de emulación recomendado es CHD, la verificación real del CHD ya convertido pasa por el software-list XML de MAME (`metadata/software-list/`), no por el DAT Redump — el DAT Redump solo verifica el `.bin`/`.cue`/`.iso` de origen antes de convertir.

**Fuente alternativa de verificación con SHA1 de CHD real** (cobertura parcial, no sustituye a la software-list de MAME): `sources/unofficial-ra-dats/input/DATs/RetroAchievements (No Subfolders)/RA - <Sistema>.dat` (ver `docs/dat-sources.md#unofficial-ra-dats`) trae `<disk name="*.chd" sha1="...">` con el hash real del CHD, cruzado por título contra Redump. Solo cubre juegos con set de logros de RetroAchievements — `saturn` 205/2457 títulos del catálogo Redump completo, `dreamcast` 173/1516, `segacd` 100/549, `psx` 892 (catálogo Redump bastante mayor). Útil para verificar por hash un CHD concreto sin tener que generar/consultar la software-list de MAME, pero no cubre el catálogo completo.

| Identificador canónico | Formato recomendado | Verificación del formato final | Notas |
| --- | --- | --- | --- |
| `psx` | CHD | `metadata/software-list/psx.xml` | |
| `saturn` | CHD | `metadata/software-list/saturn.xml` | |
| `segacd` | CHD | `metadata/software-list/megacd.xml` | |
| `pcenginecd` | CHD | `metadata/software-list/pcecd.xml` | |
| `dreamcast` | CHD | `metadata/software-list/dc.xml` | |
| `3do` | CHD | `metadata/software-list/3do.xml` | |
| `neogeocd` | CHD | `metadata/software-list/neocd.xml` | |
| `amigacdtv` | CHD | `metadata/software-list/cdtv.xml` | |
| `amigacd32` | CHD | `metadata/software-list/cd32.xml` | |
| `ps2` | CHD | Sin software-list de MAME conocida; verificación directa contra DAT Redump (bin/cue) | Soportado de forma nativa por PCSX2 |
| `gamecube` | RVZ (no CHD) | DAT Redump (iso) | Ver caso especial más abajo |
| `wii` | RVZ (no CHD) | DAT Redump (iso) | Ver caso especial más abajo |
| `xbox` | XISO (no CHD) | DAT Redump (iso) | |
| `jaguarcd` | CDI / CUE / `bigpimg` (no CHD) | DAT Redump (bin/cue) | Formatos nativos de BigPEmu |
| `psp` | CSO (comprimido), manteniendo también el ISO fuente | Fuente Redump (`Sony - PlayStation Portable - Datfile (3500)...dat`) | UMD físico, no usa CHD; DAT Redump todavía sin mapear en `build-dat-index-redump.ps1` (ver `docs/session-context.md`) |
| `cdi` | BIN/CUE (no CHD) | `metadata/software-list/cdi.xml` existe, pero el uso real de CHD para este sistema no está confirmado — evitar dar por buena una justificación técnica concreta ("base de datos firmada") sin verificar | Solo DAT Non-Redump hoy |
| `xbox360` | Juego extraído (`default.xex`), evitar `.iso` salvo que ya se disponga de ella y se quiera conservar (no CHD) | Solo DAT Non-Redump hoy | Xenia; el extraído elimina espacio inútil, arranca directo desde `default.xex` y encaja mejor con frontends que el `.iso` |
| `ps3` | Sin formato único: físico → carpeta extraída con `PS3_GAME`; digital → `.pkg` instalado (no CHD) | Solo DAT Non-Redump hoy | RPCS3; es lo más natural para cada origen y evita conversiones innecesarias |
| `wiiu` | WUA (comprimido, no CHD) | Solo DAT Non-Redump hoy | Cemu; un solo archivo que puede integrar juego+update+DLC, cómodo para frontends y almacenamiento — el más claro de los tres casos |

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
