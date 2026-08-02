# Batocera

Batocera es un sistema operativo y Custom Firmware (CFW) de código abierto y distribución limpia basado en una versión reducida y altamente optimizada de Linux (Buildroot). Diseñado específicamente para convertir ordenadores, mini-PCs y placas de computación reducida en estaciones de emulación dedicadas, destaca en la escena actual por su filosofía plug-and-play. Utiliza una versión avanzada de EmulationStation como frontend y se ejecuta por completo desde la memoria RAM tras el arranque, incorporando controladores gráficos propietarios preinstalados, soporte nativo para miles de controladores por Bluetooth y una arquitectura modular que automatiza la configuración de RetroArch y emuladores independientes (standalone).

## Dispositivos aplicables

- Raspberry Pi (3B+, 4, 5, Zero 2 W y variantes de cómputo)
- Ordenadores x86_64 (Mini PCs estilo Intel NUC, portátiles antiguos, PCs de sobremesa convencionales y consolas de mano tipo Steam Deck o ASUS ROG Ally)
- Placas secundarias y TV Boxes (ODROID, Khadas, Rockchip y dispositivos seleccionados de Orange Pi)

Esta guía se centra en la instalación en Raspberry Pi 3B+ (dispositivo del inventario en `docs/devices.md`).

## Tipo de instalación

Imagen flasheada a SD / unidad externa (`.img.gz`). Instalación limpia de bajo nivel escribiendo directamente en una tarjeta MicroSD, un pendrive USB o un disco duro externo/SSD. El flasheo inicial es destructivo y reescribe todas las particiones del soporte elegido.

## Requisitos previos

- Tarjeta MicroSD de primera marca: mínimo 32GB o 64GB (SanDisk Ultra o Samsung EVO) para Raspberry Pi 3B+. En PC, se prefiere un SSD por bus USB 3.0.
- Software de flasheo: BalenaEtcher (muy recomendado por el equipo de desarrollo), Rufus, Raspberry Pi Imager o `dd` en WSL/Linux.
- Alimentación estable (crítico en Raspberry Pi): usar una fuente de alimentación oficial de 5V y 2.5A para la Raspberry Pi 3B+. Las caídas de tensión por cargadores de móvil genéricos provocan corrupción de datos inmediata en las tablas de la MicroSD.

## Descarga

- Sitio web oficial: <https://batocera.org>
- Nota técnica: es un requisito inamovible descargar la variante exacta para la arquitectura del procesador (ej. elegir la imagen de la sección Raspberry Pi 3 / 3B+ / 3A+). Flashear una compilación errónea impide que el cargador de arranque (bootloader) de Broadcom inicialice el kernel de Linux.

## Preparación de almacenamiento

El esquema de particiones de Batocera divide de forma estricta los archivos del sistema de los datos del usuario:

- **Partición BATOCERA (Sistema)**: el software de flasheo crea una partición inicial de unos 6GB en formato FAT32 destinada exclusivamente al kernel de Linux, los controladores y los archivos de arranque. No requiere manipulación manual.
- **Partición SHARE (Datos del usuario)**: durante el primer arranque, el sistema utiliza automáticamente todo el espacio restante de la tarjeta para crear una segunda partición lógica llamada `SHARE`.
- Configuración del formato: por defecto se crea en formato Linux EXT4 (incompatible con Windows nativo sin herramientas secundarias). Batocera permite cambiar este formato a exFAT desde sus opciones internas.
- Integración con pipeline propio: es posible leer la partición `SHARE` directamente en formato EXT4 desde WSL para pre-cargar la estructura oficial de carpetas de ROMs (ej. `/roms/nes/`, `/roms/snes/`, `/roms/megadrive/`, `/roms/psx/`) en minúsculas estrictas.

## Instalación

1. Inserta la MicroSD en el lector de tarjetas del ordenador.
2. Inicia el software de flasheo (ej. BalenaEtcher) y selecciona el archivo `.img.gz` descargado (no requiere descompresión previa).
3. Elige la MicroSD destino y haz clic en Flash/Escribir. Al finalizar, Windows mostrará errores de partición no reconocida debido a que no lee EXT4 de forma nativa; ignora las alertas y expulsa la tarjeta de forma segura.

## Primer arranque

1. Introduce la MicroSD flasheada en la ranura de la Raspberry Pi 3B+. Desconecta cualquier disco USB secundario en este inicio.
2. Conecta el cable HDMI a la pantalla y, por último, el cable de alimentación.
3. El sistema ejecuta un script automático de inicialización en modo texto que expande la partición `SHARE` para ocupar el 100% de la capacidad física de la MicroSD y genera todo el árbol de directorios de juegos. La placa se reinicia automáticamente y carga la interfaz gráfica enriquecida de EmulationStation.

## Configuración post-instalación

- **Volcado de ROMsets y BIOS**: extrayendo la tarjeta y leyéndola en WSL, o mediante red local (Samba) introduciendo la dirección `\\BATOCERA` en el explorador de Windows si la consola está conectada por Wi-Fi/Ethernet. Transfiere los juegos a sus respectivas carpetas. Es obligatorio copiar las BIOS validadas en el directorio raíz `/share/bios/`.
- **Indexación de metadatos (`gamelist.xml`)**: el frontend lee la base de datos de juegos a través de `gamelist.xml`, situado en la raíz de cada carpeta de consola. Los archivos multimedia se alojan por defecto en `/share/roms/[sistema]/images/` para carátulas y `/share/roms/[sistema]/videos/` para los clips de vídeo.
- Ventaja de pipeline propio: es posible generar `gamelist.xml` de forma nativa a partir de DATs propios estructurados, inyectando las carátulas locales directamente desde el ordenador y evitando el lento proceso de scraping interno de la placa.

## Notas

- **Tratamiento de ROMsets Arcade (límite en Pi 3B+)**: a diferencia de las versiones para PC, la Raspberry Pi 3B+ tiene limitaciones severas de hardware. Para lograr los 60 FPS estables en placas recreativas de Capcom (CPS1/2/3) y Neo-Geo, el estándar recomendado es FinalBurn Neo (romset en formato Non-Merged). Para arcade generales complejos, MAME 2003-Plus (romset `0.78-plus`). Evitar procesar conjuntos de MAME modernos, ya que el rendimiento cae drásticamente. Incluir la BIOS `neogeo.zip` adaptada a esa era en la raíz de la carpeta arcade.
- **Optimización del formato de consolas en disco**: al contar con emuladores modernos actualizados y núcleos de RetroArch estables, el formato de compresión CHD (v5) es la directriz mandatoria para cualquier sistema basado en discos compactos (PS1, Sega CD, Saturn, Dreamcast). Reduce el peso de las ISOs a la mitad, estabiliza la tasa de fotogramas por segundo y elimina los cuellos de botella al leer múltiples pistas musicales desde la MicroSD.
- **Gestión 1G1R de la interfaz**: aunque EmulationStation en Batocera está muy optimizado, el hardware de la Raspberry Pi 3B+ tiene limitaciones de memoria RAM (1GB compartido con la GPU). Cargar carpetas saturadas con miles de archivos duplicados de distintas regiones o betas provoca tirones visuales severos (stuttering) al hacer scroll rápido por los menús tridimensionales. Es una directriz técnica obligatoria aplicar un filtro 1G1R estricto antes de transferir los juegos, limitando los conjuntos a los títulos esenciales por plataforma para mantener el frontend fluido y rápido.
