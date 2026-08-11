# Compresión / conversión de formato

Conversión al formato final de despliegue: CHD (discos ópticos, MAME), CSO/DAX (PSP/PS2), RVZ/GCZ (GameCube/Wii). Se aplica después del parcheo (fase 6) y antes de organizar en `data/roms/` (fase 8) — comprimir antes de auditar/parchear complicaría innecesariamente esos pasos.

Corresponde a la fase 7 de [docs/guides/romsets/workflow.md](../romsets/workflow.md).

## CHDMan

**Fuente:** incluido con MAME (mamedev.org). Conversión y gestión de imágenes CHD para discos ópticos y discos duros de arcade.

**Sintaxis confirmada:**

```bash
# Discos CD (PS1, Saturn, Dreamcast, PC Engine CD, Sega CD...)
chdman createcd -i "juego.cue" -o "juego.chd"

# Discos DVD (PS2, GameCube vía CHD, etc.)
chdman createdvd -i "juego.iso" -o "juego.chd"
```

**Formatos de entrada admitidos por `createcd`:** CUE, GDI, ISO, TOC.

**`createdvd` vs `createcd`:** para sistemas DVD, `createdvd` suele comprimir un 7-10% mejor y rinde mejor en juego; usa compresión `zstd` por defecto — comprobar que el emulador/core objetivo la soporta antes de asumir compatibilidad, no todos los `libretro` core la soportan.

**Caso especial LibCrypt (PS1 PAL):** el proceso de creación del CHD no procesa el fichero `.sbi` — hay que conservarlo en la misma carpeta que el `.chd` resultante para que la protección LibCrypt funcione (ver también `docs/guides/romsets/optical-chd.md`).

**Conversión por lotes (Windows, ejemplo confirmado):**

```batch
for /r %i in (*.cue, *.gdi, *.iso, *.toc) do chdman createcd -i "%i" -o "%~ni.chd"
```

## Maxcso

**Fuente:** github.com/unknownbrackets/maxcso. Compresor de alta velocidad ISO→CSO/DAX para PSP/PS2, multinúcleo.

**Uso básico confirmado:**

```bash
maxcso input.iso -o output.cso
```

Admite arrastrar el ISO directamente sobre `maxcso.exe` en Windows, y varios ficheros de entrada en una sola llamada.

**Nivel de compresión:** siempre usa nivel 9 (máximo); `--fast` da el resultado más rápido equivalente a nivel 9 de otras herramientas.

**Flags principales confirmados:**

- `--threads=N` — número de hilos para I/O y compresión.
- `--format=VER` — versión de contenedor: `cso1`, `cso2`, `zso`, `dax`.
- `--block=N` — tamaño de bloque (por defecto depende del tamaño del ISO).
- `--use-zopfli`, `--use-zlib`, `--use-7zdeflate`, `--use-lz4` — algoritmo de compresión a probar.
- `--decompress` — vuelca de vuelta a ISO sin comprimir.
- `--crc` — solo calcula y muestra CRC32, sin generar salida.
- `--quiet` — sin mensajes de estado.

**Ejemplo de máxima compresión (lento, citado en la documentación):**

```bash
maxcso.exe --use-zopfli --block=16384 input.iso
```

## NKit

**Fuente:** github.com/Nanook/NKit. Optimiza/restaura ISO de GameCube/Wii al tamaño mínimo, preservando compatibilidad con Dolphin.

**Formatos de salida confirmados:** `iso` (crudo) y `gcz` (comprimido) — el propio NKit es el formato más pequeño para GameCube/Wii disponible, aunque solo GameCube tiene soporte por hardware real (Wii vía NKit solo es reproducible en Dolphin, no en hardware).

**Uso confirmado (parcial):** soporta arrastrar ficheros sobre la app para agruparlos y procesarlos; parámetros configurables por sistema con prefijo (`-wii:dat Wii*.dat`, `-gamecube:dat GC*.dat`).

```bash
nkit *.iso -task convert -wii:convert wbfs
```

[TODO: no se ha encontrado un ejemplo de comando concreto para la conversión específica a/desde el propio formato NKit comprimido (`.nkit.iso`/`.nkit.gcz`) — el ejemplo confirmado de arriba es para WBFS, no para NKit en sí; consultar la página "Processing Tasks" del wiki oficial o el fichero `nkit.yaml` de configuración antes de automatizar este paso]

**Nota de compatibilidad:** existe una herramienta separada, `nkit2iso` (github.com/DonMikone/nkit2iso), específica para revertir `.nkit.iso`/`.nkit.gcz` a ISO plano verificado por CRC — más simple que el propio NKit si solo se necesita la conversión inversa.

## DolphinTool (ISO/RVZ/GCZ)

**Fuente:** incluida con Dolphin (dolphin-emu.org). Utilidad CLI oficial del propio emulador para convertir y verificar imágenes de GameCube/Wii.

**Sintaxis confirmada del subcomando `convert`:**

```bash
dolphin-tool convert -i entrada.iso -o salida.rvz -f rvz -b 131072 -c zstd -l 5
```

- `-f FORMAT` — formato de contenedor: `iso`, `gcz`, `wia`, `rvz` (por defecto `rvz`).
- `-b BLOCK_SIZE` — tamaño de bloque para GCZ/WIA/RVZ; 131072 (128 KiB) recomendado para RVZ.
- `-c COMPRESSION` — método de compresión para WIA/RVZ: `none`, `zstd`, `bzip`, `lzma`, `lzma2`; `zstd` recomendado para RVZ.
- `-l COMPRESSION_LEVEL` — nivel de compresión.
- `-s` — elimina datos basura ("junk data") como parte de la conversión.

**Conversión inversa (RVZ → ISO), ejemplo confirmado:**

```bash
dolphin-tool convert -f iso -i juego.rvz -o juego.iso
```

Para extracción de metadatos por hash (`read-id`, GameID de 6 caracteres), ver `docs/guides/romsets/optical-chd.md` y la sección "Extracción de metadatos" del roadmap en [custom-pipeline.md](../romsets/custom-pipeline.md).

## Notas

El formato final depende del emulador/core objetivo, no de una preferencia genérica — comprobar en `docs/system-paths.md`/`docs/software.md` qué formato espera cada CFW/frontend antes de comprimir en masa; deshacer una compresión ya aplicada a todo un romset es costoso.

Extracción de metadatos por hash en formatos comprimidos (CHD/RVZ) — ver sección "Extracción de metadatos" del roadmap en [custom-pipeline.md](../romsets/custom-pipeline.md); detalle del caso GameCube/Wii en `docs/guides/romsets/optical-chd.md`.
