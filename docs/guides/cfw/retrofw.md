# RetroFW

RetroFW es un Custom Firmware (CFW) ligero y de código abierto basado en una distribución compacta de Linux para consolas portátiles retro equipadas con procesadores MIPS (como el JZ4760). Utiliza un frontend modular y directo (habitualmente GMenu2X o variantes minimalistas de SimpleMenu) diseñado para maximizar la memoria RAM disponible. Destaca por revivir hardware antiguo gracias a la optimización de sus emuladores en formato empaquetado `.opk`, logrando ejecutar de forma fluida sistemas desde los 8 bits hasta los 16 bits avanzados y PlayStation 1 de forma nativa.

## Dispositivos aplicables

- PowKiddy LDK (modelos Landscape y Vertical)
- Retrogame RS97 (en todas sus revisiones de placa interna: v1.0, v2.1, v3.0, etc.)
- Anbernic RG99
- PowKiddy RS-07 (consola portátil estilo mini recreativa)
- Anbernic RG300 (modelos antiguos, según `docs/software.md`)

## Tipo de instalación

Imagen flasheada a SD (`.img`), instalación limpia de fábrica en la MicroSD de sistema. Dependiendo del dispositivo, el almacenamiento se gestiona mediante una única tarjeta física con particiones divididas o mediante una configuración manual para leer datos desde una ranura secundaria.

## Requisitos previos

- Tarjeta MicroSD única: se recomienda encarecidamente una de 16GB, 32GB o como máximo 64GB (SanDisk o Samsung).
- Nota técnica: el controlador de almacenamiento de estos procesadores antiguos (MIPS) tiene serios problemas de estabilidad y tiempos de acceso eternos si se utilizan tarjetas de 128GB o superiores.
- Software de flasheo: Rufus o BalenaEtcher para entornos de escritorio, o `dd` en WSL/Linux.
- Herramienta de particionado (opcional): MiniTool Partition Wizard o gparted en Linux/WSL para expandir la partición de datos manualmente si el script de inicio falla.

## Descarga

- Repositorio oficial de la escena: las imágenes oficiales estables y los paquetes de emuladores actualizados se centralizan en el GitHub del proyecto — <https://github.com/retrofw/retrofw.github.io>
- Nota crítica: descargar el archivo `.img` correspondiente al nombre en clave de la placa (ej. `RetroFW-LDK-vX.X.img` para la PowKiddy LDK o `RetroFW-RS97-vX.X.img` para la RS97). Flashear una imagen incorrecta rompe el mapeo de los botones físicos o invierte los colores de la pantalla.

## Preparación de almacenamiento

- **SD de sistema (única)**: no requiere preparación ni formateo previo. El programa de flasheo crea la estructura Linux necesaria: una partición de arranque oculta y una partición visible en formato FAT32 etiquetada comúnmente como `retrofw` o `main`, destinada a las ROMs y aplicaciones.
- Integración con pipeline propio: a diferencia de los CFW modernos, RetroFW no autogenera un árbol de carpetas con nombres estándares en su primer arranque. Exige rutas de directorio muy particulares que dependen de cómo estén configurados los archivos de enlace de los emuladores nativos; hay que inyectar la estructura creando carpetas en la raíz como `/roms/GB/`, `/roms/MD/`, `/roms/GBA/` y `/roms/ARCADE/`.

## Instalación

1. Inserta la MicroSD en el lector de tarjetas del ordenador.
2. Ejecuta el software de flasheo (ej. Rufus) y carga la imagen `.img` de RetroFW correspondiente al dispositivo.
3. Selecciona la MicroSD destino y haz clic en Escribir. Una vez finalizado el flasheo, extrae la tarjeta.

## Primer arranque

1. Inserta la tarjeta MicroSD flasheada en la ranura única de la consola.
2. Enciende el dispositivo. El sistema ejecuta un script en segundo plano para inicializar el kernel de Linux.
3. **Nota de optimización y advertencia**: a partir de la versión v2.2 de RetroFW, el sistema autogenera y expande el diseño de particiones correcto de forma nativa en este primer inicio. Sin embargo, si se utilizan compilaciones heredadas o el proceso falla en revisiones antiguas de la placa RS97 dejando solo unos pocos megabytes libres, hay que introducir la tarjeta en el ordenador y usar `gparted` o MiniTool en WSL para expandir manualmente la partición de datos FAT32 hasta el límite físico de la MicroSD.

## Configuración post-instalación

- **Volcado de emuladores (`.opk`)**: en RetroFW, los emuladores se instalan como aplicaciones autónomas. Hay que arrastrar los archivos `.opk` de los emuladores descargados dentro de la carpeta `/apps/` de la MicroSD para que el frontend GMenu2X los reconozca.
- **Estructura de ROMs**: transfiere las colecciones de juegos validadas a las subcarpetas creadas dentro de `/roms/`. Las BIOS obligatorias (como `scph1001.bin` para PS1) deben colocarse dentro de la carpeta oculta de configuración de cada emulador nativo (ej. `/home/retrofw/.pcsx4all/bios/`), nunca en la raíz de las ROMs.
- **Tratamiento de carátulas (previews)**: GMenu2X busca las imágenes en formato `.png` de tamaño ultra-reducido (generalmente un ancho máximo de 160 o 320 píxeles para evitar saturar la memoria RAM) dentro de una carpeta llamada `previews` dentro del directorio del emulador. Su nomenclatura debe coincidir byte por byte con el nombre del archivo de la ROM.

## Notas

- **Tratamiento estricto de ROMsets Arcade**: debido al hardware MIPS, el entorno arcade nativo de RetroFW está completamente fragmentado y congelado en el tiempo. Hay que filtrar y compilar subsets independientes utilizando archivos DAT muy específicos según el emulador de destino:
  - `mame4all` / `fba-a320` / `fbasdl`: ligados de forma inamovible al romset clásico MAME 0.37b5 (familia `mame2000`). Es obligatorio procesar este DAT para los juegos de arcade generales.
  - `gngeo`: emulador nativo optimizado exclusivamente para Neo-Geo SNK. Requiere las ROMs del set MAME antiguo y el archivo de BIOS `neogeo.zip` adaptado a esa misma versión dentro de la carpeta de ROMs.
  - `xmame 2.0` (Alpha): versión experimental para ciertos títulos arcade que no rinden en `mame4all`. Utiliza una estructura de romset mixta entre MAME 0.52 y MAME 0.60.
- **Optimización para PlayStation 1**: el emulador nativo PCSX4All integrado en RetroFW está optimizado para leer el formato comprimido CHD (v5). Convertir las ISOs/BIN de PS1 a CHD reduce drásticamente los tiempos de lectura del bus MicroSD y garantiza que juegos pesados funcionen a 60 FPS estables con frameskip automático.
- **Gestión 1G1R obligatoria**: la memoria RAM libre en estos dispositivos suele oscilar entre 32MB y 64MB. Cargar una carpeta con más de 1000 ROMs (como un full-set americano de NES o Genesis) congela el frontend GMenu2X al intentar renderizar la lista. Pasar los DATs por un filtro 1G1R estricto con herramientas como retool para dejar subsets de no más de 200-300 juegos esenciales por sistema es una necesidad técnica crítica en este firmware.
