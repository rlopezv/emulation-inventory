# KNULLI

KNULLI es un Custom Firmware (CFW) de código abierto, alto rendimiento y distribución limpia basado en el ecosistema de Batocera Linux. Está diseñado específicamente para exprimir los procesadores ARM de 64 bits modernos (como los SoC de la familia Allwinner H700). Utiliza una versión altamente optimizada de EmulationStation como frontend y destaca en la escena actual por ofrecer características premium nativas como soporte avanzado para shaders con aceleración por hardware, shaders automáticos según relación de aspecto, juego en red (Netplay), sincronización en la nube para guardados, logros de RetroAchievements integrados y soporte total para sistemas de archivos modernos.

## Dispositivos aplicables

- Anbernic RG35XX Plus
- Anbernic RG35XX H (modelo horizontal)
- Anbernic RG35XX SP (modelo plegable flip)
- Anbernic RG28XX / RG34XX / RG34XX SP
- Anbernic RG40XX V / RG40XX H
- Anbernic RG CubeXX
- PowKiddy V10 / PowKiddy V90S

## Tipo de instalación

Imagen flasheada a SD (`.img.gz`), instalación limpia de fábrica. Soporta de forma nativa e integrada tanto configuraciones de tarjeta única (sistema + ROMs) como esquemas avanzados de doble tarjeta (SD1 sistema, SD2 ROMs).

## Requisitos previos

- Tarjetas MicroSD compatibles: una de 16GB o 32GB de calidad para el sistema operativo (SD1); una secundaria opcional de 64GB a 512GB de alta velocidad para juegos (SD2).
- Software de flasheo: BalenaEtcher (muy recomendado), Rufus, o `dd` en WSL/Linux.
- Conexión Wi-Fi integrada en el dispositivo para habilitar las funciones en red y raspado del sistema.

## Descarga

- Repositorio oficial: las imágenes oficiales estables y de desarrollo se distribuyen de forma centralizada en el GitHub oficial del proyecto — <https://github.com/knulli-cfw/distribution/releases>
- Nota técnica: es indispensable descargar el archivo `.img.gz` correspondiente a la familia del procesador o modelo específico de la consola (ej. `knulli-anbernic-rg35xx-h700-vX.X.X.img.gz`), ya que los controladores del panel de la pantalla y el mapeo de botones varían entre revisiones de hardware.

## Preparación de almacenamiento

- **SD1 (Sistema)**: el software de flasheo crea la estructura Linux necesaria: una partición de arranque START (FAT32) y una partición principal de almacenamiento del sistema operativo (EXT4). No requiere formateo manual previo.
- **SD2 (ROMs — ranura TF2 / segundo slot)**: KNULLI rompe con el estándar clásico y utiliza por defecto el sistema de archivos Linux EXT4 para la partición de datos por motivos de rendimiento y permisos. Sin embargo, permite alternar a exFAT o FAT32 desde su menú de opciones para facilitar la lectura plug-and-play en entornos Windows/WSL.

## Instalación

1. Inserta la SD1 en el lector de tarjetas del ordenador.
2. Inicia el software de flasheo (ej. BalenaEtcher). Selecciona el archivo `.img.gz` descargado de KNULLI (no es necesario descomprimirlo previamente si se usa Etcher).
3. Elige la MicroSD destino y haz clic en Flash/Escribir. Al finalizar, Windows mostrará errores de partición no reconocida; ignóralos por completo y expulsa la tarjeta de forma segura.

## Primer arranque

1. Introduce la SD1 flasheada en la ranura principal de la consola (TF1/INT). Deja la ranura TF2 completamente vacía.
2. Enciende la consola. KNULLI inicia un script automático de redimensionamiento de particiones en modo texto. El sistema expande el almacenamiento interno y se reinicia automáticamente.
3. Una vez cargue EmulationStation, si se va a utilizar una configuración de doble tarjeta, presiona `Start -> System Settings -> Storage Device` y cámbialo a `Second SD Card`. El sistema pedirá reiniciar.
4. Apaga la consola, inserta la SD2 formateada (preferiblemente en exFAT para trabajar desde el PC) en la ranura TF2 y enciende el dispositivo. El sistema puebla automáticamente todo el árbol de directorios de ROMs en la segunda tarjeta de forma instantánea.

## Configuración post-instalación

- **Volcado de datos**: transfiere los juegos organizados a las carpetas autogeneradas en la SD2 (ej. `/roms/snes/`, `/roms/megadrive/`). Los archivos de BIOS obligatorios deben copiarse estrictamente en el directorio raíz `/roms/bios/` para que los emuladores arranquen.
- **Indexación de metadatos**: EmulationStation lee la base de datos de juegos a través de `gamelist.xml`, situado en la raíz de cada carpeta de consola. Los archivos multimedia se alojan por defecto en `/roms/[sistema]/images/` para carátulas y `/roms/[sistema]/videos/` para los clips de vídeo.
- Nota de rendimiento: el sistema lee de forma directa y nativa estos archivos XML planos. Inyectar metadatos locales y portadas limpias desde el ordenador evita usar el lento raspador por Wi-Fi de la consola.

## Notas

- **Tratamiento de ROMsets Arcade modernos**: gracias al procesador ARM de 64 bits de estas portátiles, KNULLI ejecuta núcleos muy actuales. El estándar absoluto recomendado por la comunidad para sistemas arcade y placas dedicadas (CPS1, CPS2, CPS3 y Neo-Geo) es FinalBurn Neo (romset en formato Non-Merged). Para juegos arcade generales, el núcleo más equilibrado es MAME 2003-Plus (romset `0.78-plus`). Es mandatorio utilizar los archivos DAT oficiales de estas dos versiones para evitar fallos de inicialización o cuelgues del backend.
- **Optimización de consolas de disco**: al estar basado en Batocera, soporta de forma nativa y óptima el formato de compresión CHD (v5) en emuladores de PS1, Saturn, Dreamcast, Sega CD, PC-FX y 3DO. Convertir las colecciones a CHD reduce el peso de la biblioteca a la mitad, alivia el bus de la MicroSD y acelera la carga. Para PSP y PlayStation 2, soporta perfectamente el formato CSO.
- **Gestión 1G1R de la interfaz**: aunque las consolas aplicables tienen procesadores solventes, el frontend EmulationStation puede ralentizar su tiempo de carga inicial si se saturan las carpetas con miles de archivos duplicados. Aplicar un filtro 1G1R antes de transferir los archivos purga la interfaz de clones de distintas regiones y betas, ofreciendo menús limpios y una navegación fluida a 60 FPS estables.
- **Apagado seguro obligatorio**: al ser una distribución completa de Linux de 64 bits, nunca se debe apagar la consola presionando el botón físico de Power directamente de forma brusca. Hazlo siempre desde el menú de EmulationStation (`Start -> Quit -> Shutdown System`) para salvaguardar la integridad del sistema de archivos, evitar corrupciones en la partición y proteger los archivos de guardado rápido (savestates).
