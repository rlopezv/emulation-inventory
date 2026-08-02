# ROCKNIX

ROCKNIX (Rockchip Linux) es un Custom Firmware (CFW) de código abierto, distribución limpia y rendimiento extremo basado en una infraestructura JeOS (Just Enough Operating System). Es la continuación oficial y comunitaria del aclamado proyecto JELOS. Destaca en la escena actual por incorporar los últimos kernels de Linux estables y soporte de controladores gráficos Mainline (Mesa/Panfrost), lo que desbloquea un rendimiento optimizado en emuladores de 64 bits de alta demanda como Vulkan para PSP, Dreamcast y Nintendo 64. Utiliza EmulationStation como frontend principal con soporte completo para scripts personalizados, juego en red (Netplay) y RetroAchievements nativos.

## Dispositivos aplicables

- PowKiddy RGB10 / RGB10 Max 3 / RGB20S / RK2023
- Anbernic RG353P / RG353V / RG353M / RG353VS
- Anbernic RG ARC-S / RG ARC-D
- PowKiddy X55
- Anbernic RGDS (según `docs/software.md`)

## Tipo de instalación

Imagen flasheada a SD (`.img.tar` o `.img.gz`), instalación limpia de fábrica. Admite de forma nativa e integrada tanto configuraciones de tarjeta única (sistema + ROMs) como esquemas de doble tarjeta (SD1 sistema, SD2 ROMs).

## Requisitos previos

- Tarjetas MicroSD compatibles: una de 16GB o 32GB de calidad para el sistema operativo (SD1); una secundaria opcional de 64GB a 512GB de alta velocidad para juegos (SD2).
- Software de flasheo: BalenaEtcher, Rufus, o `dd` en WSL/Linux.
- Conexión a Internet: Wi-Fi integrado o mediante dongle USB en los dispositivos aplicables para actualizar los binarios internos del sistema.

## Descarga

- Repositorio oficial de la escena: las imágenes oficiales estables y de desarrollo se distribuyen de forma centralizada en el GitHub oficial del proyecto — <https://github.com/ROCKNIX/distribution/releases>
- Nota técnica: es indispensable descargar el archivo correspondiente al SoC o modelo exacto de la consola (ej. `ROCKNIX-RK3566.aarch64-vX.X.img.tar` para la familia RG353 o PowKiddy X55). Flashear una compilación de otra arquitectura impide el arranque del kernel.

## Preparación de almacenamiento

- **SD1 (Sistema)**: el software de flasheo crea el mapa de particiones Linux necesario: una partición de arranque BOOT (FAT32) y una partición de almacenamiento del sistema operativo (EXT4). No requiere formateo manual previo.
- **SD2 (ROMs — ranura TF2 / segundo slot)**: ROCKNIX ofrece compatibilidad total con sistemas de archivos avanzados. Se recomienda formatear la tarjeta secundaria en exFAT de forma nativa para trabajar de manera plug-and-play en entornos Windows/WSL, aunque también soporta ext4 y Btrfs para usuarios puros de Linux.
- Integración con pipeline propio: ROCKNIX autogenera toda la estructura si la tarjeta está vacía, pero si se precarga la SD2 antes del primer arranque con un script propio, hay que usar los nombres de carpetas estándar en minúsculas exigidos por EmulationStation (ej. `/roms/snes/`, `/roms/megadrive/`, `/roms/psx/`).

## Instalación

1. Inserta la SD1 en el lector de tarjetas del ordenador.
2. Inicia el software de flasheo (ej. BalenaEtcher). Selecciona el archivo de la imagen descargada de ROCKNIX.
3. Elige la MicroSD destino y haz clic en Flash/Escribir. Al finalizar, Windows mostrará errores de partición no reconocida; ignóralos por completo y expulsa la tarjeta de forma segura.

## Primer arranque

1. Introduce únicamente la SD1 flasheada en la ranura principal de la consola (TF1/INT). Deja la ranura TF2 completamente vacía.
2. Enciende la consola. ROCKNIX inicia un script automático de redimensionamiento de particiones en modo texto. El sistema expande el almacenamiento interno y se reinicia automáticamente.
3. Una vez cargue EmulationStation, si se va a utilizar una configuración de doble tarjeta, presiona `Start -> System Settings -> Storage Device` y cámbialo a `MAIN` (o la etiqueta de la segunda SD). El sistema pedirá reiniciar.
4. Apaga la consola, inserta la SD2 formateada en la ranura TF2 y enciende el dispositivo. El sistema puebla automáticamente todo el árbol de directorios de ROMs en la segunda tarjeta de forma instantánea si no existía previamente.

## Configuración post-instalación

- **Volcado de datos**: transfiere los juegos organizados a las carpetas generadas en la SD2. Los archivos de BIOS obligatorios deben copiarse estrictamente en el directorio raíz `/roms/bios/` para que los emuladores arranquen.
- **Indexación de metadatos**: EmulationStation lee la base de datos de juegos a través de `gamelist.xml`, situado en la raíz de cada carpeta de consola. Los archivos multimedia se alojan por defecto en `/roms/[sistema]/images/` para carátulas y `/roms/[sistema]/videos/` para los clips de vídeo.
- Ventaja de pipeline propio: es posible generar `gamelist.xml` de forma nativa basándose en DATs propios estructurados, enlazando las imágenes locales sin depender del raspador interno por Wi-Fi de la consola, mucho más lento.

## Notas

- **Tratamiento de ROMsets Arcade actualizados**: al incorporar kernels mainline modernos y un entorno de 64 bits completo, ROCKNIX ejecuta los emuladores arcade más recientes. El estándar recomendado por la comunidad para sistemas arcade y placas dedicadas (CPS1, CPS2, CPS3 y Neo-Geo) es FinalBurn Neo (romset en formato Non-Merged). Para juegos arcade generales, el núcleo más equilibrado y eficiente para los chips RK3566 es MAME 2003-Plus (romset `0.78-plus`). Es necesario procesar las colecciones con los archivos DAT exactos de estas versiones para evitar pantallas en negro.
- **Optimización del formato de consolas en disco**: al estar profundamente optimizado para emuladores independientes (standalone) y RetroArch, soporta de forma nativa el formato de compresión CHD (v5) en todos los sistemas basados en discos ópticos (PS1, Saturn, Dreamcast, Sega CD, PC-FX y 3DO). Convertir las colecciones a CHD reduce el peso de la biblioteca a la mitad y alivia el bus de la MicroSD. Para PlayStation Portable, soporta perfectamente el formato CSO.
- **Gestión 1G1R de la interfaz**: aunque las consolas aplicables tienen procesadores solventes de 64 bits, el frontend EmulationStation puede ralentizar su tiempo de carga inicial si se saturan las carpetas con miles de archivos duplicados. Aplicar un filtro 1G1R antes de transferir los archivos purga la interfaz de clones de distintas regiones y betas, ofreciendo menús limpios y una navegación fluida a 60 FPS estables.
- **Apagado seguro obligatorio**: al ser una distribución completa de Linux moderna, nunca se debe apagar la consola presionando el botón físico de Power directamente de forma brusca. Hazlo siempre desde el menú de EmulationStation (`Start -> Quit -> Shutdown System`) para salvaguardar la integridad del sistema de archivos, evitar corrupciones en la partición y proteger los archivos de guardado rápido (savestates).
