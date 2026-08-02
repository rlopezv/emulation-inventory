# Preparación de romsets — Óptico → CHD

[TODO: descripción breve]

Aplica a sistemas ópticos verificados con DAT Redump (o Non-Redump para protos/betas cuando no hay DAT Redump; ver `docs/romsets.md`).

## Fuente

[TODO]

## Verificación contra DAT Non-Redump

Cuando un CHD tiene el nombre de archivo incorrecto o metadatos alterados, no se puede confiar en el nombre: hay que leer el hash interno (SHA-1) del CHD y de la ROM asociada, cruzarlo contra el DAT oficial (Redump o Non-Redump) y renombrar/reestructurar la colección a partir de esa firma real, no del nombre de fichero.

**RomVault** — opción más precisa para CHDs. Usa internamente la lógica de `chdman` para leer la cabecera y descomprimir/verificar el SHA-1 real oculto dentro del CHD, busca el juego correcto en el DAT y renombra/mueve automáticamente a la sintaxis oficial.

**JRomManager** — soporte nativo para esquemas Merged/Non-Merged/Split con cálculo de SHA-1 profundo. Detecta archivos "huérfanos" o mal nombrados, los empareja contra el DAT y aplica la función `Fix` para renombrar tanto el contenedor de la ROM como el CHD.

**SabreTools (Rebuild)** — reconstrucción vía CLI: apunta a la carpeta desorganizada como origen y a un DAT limpio; lee los hashes (hasta SHA-512) sin importar el nombre de archivo y genera un romset nuevo, correctamente renombrado, en la carpeta de destino.

```bash
SabreTools.exe --rebuild --dat="redump.dat" --input="Carpeta_Con_Nombres_Mal" --output="Carpeta_Curada"
```

**verifydump** — específico para CHDs procedentes de discos Redump (PS1, PS2, Saturn, Dreamcast). Cruza el CHD contra los `.cue` oficiales de Redump para validar que la estructura interna del volcado es correcta al 100%, antes de organizarlo.

### Caso especial — GameCube / Wii (RVZ en vez de CHD)

GameCube y Wii no usan CHD: el contenedor moderno es **RVZ**, creado por el propio equipo de Dolphin, por lo que la comunidad no recurre a gestores externos tipo RomVault/JRomManager sino a las herramientas oficiales de Dolphin. RVZ es lossless si se configura correctamente: comprime el disco pero conserva los hashes MD5/SHA-1 como si fuera la ISO original descomprimida, lo que permite que herramientas como JRomManager auditen directamente archivos RVZ configurando el DAT de Redump correspondiente.

**DolphinTool (CLI)** — equivalente a `chdman` para la infraestructura Nintendo. Permite verificar la integridad de las imágenes vía script y extraer el GameID (código único de 6 caracteres, ej. `GALE01` para Super Smash Bros. Melee) para automatizar el renombrado masivo en Bash/PowerShell contra una base de datos limpia de Redump.

**Interfaz nativa de Dolphin (por lotes)** — el propio emulador es el gestor más potente para este formato: al añadir una carpeta con RVZ mal nombrados, ignora el nombre de archivo, lee la cabecera real, calcula el hash y extrae nombre, región e ID oficiales. Seleccionando todos los juegos y usando exportar/convertir en lote, Dolphin regrava los RVZ en una carpeta limpia con nomenclatura `[Nombre de Juego] ([Región])`.

**Dolphin RVZ/ISO Conversion Scripts (ElektroStudios)** — scripts de automatización de la comunidad que envuelven DolphinTool para convertir en lote de forma bidireccional (ISO ⇄ RVZ) y limpiar datos residuales del disco, ahorrando hasta un 90% de espacio antes del renombrado.

**Paso previo obligatorio — retool** — igual que con sistemas de CD, filtrar primero el DAT de Redump de GameCube/Wii con retool para generar la lista 1G1R antes de dejar que Dolphin identifique y renombre solo los RVZ que pasaron el filtro; evita duplicar gigabytes de datos comprimidos innecesariamente.

## Conversión a CHD

[TODO]

## Organización en data/roms

[TODO]

## Generación de gamelist.xml y media

[TODO]

## Notas

[TODO]
