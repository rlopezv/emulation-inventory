# Simple30

Simple30 es un Custom Firmware (CFW) optimizado y de código abierto diseñado para reemplazar la interfaz de fábrica en dispositivos portátiles económicos basados en procesadores Allwinner de cuatro núcleos de generaciones previas. Destaca técnicamente por integrar una versión aligerada y modificada de SimpleMenu como frontend por defecto en lugar de entornos pesados, priorizando la tasa de refresco a 60 Hz limpios, la asignación directa de núcleos optimizados de RetroArch y la reducción drástica del tiempo de arranque del sistema operativo.

## Dispositivos aplicables

- PocketGo S30 (consola portátil horizontal con diseño inspirado en el mando de Super Nintendo)

## Tipo de instalación

Imagen flasheada a SD (`.img`), instalación limpia de fábrica. Funciona bajo un esquema de tarjeta única que aloja tanto las particiones ocultas del sistema Linux como la partición accesible para las ROMs y recursos del usuario.

## Requisitos previos

- Tarjeta MicroSD estándar de marca: se recomienda 32GB, 64GB o como máximo 128GB (SanDisk Ultra o Samsung EVO).
- Nota de rendimiento: el controlador SD integrado en la PocketGo S30 presenta problemas de estabilidad y cuellos de botella severos si se utilizan tarjetas de 256GB o superiores, ralentizando el escaneo de los menús.
- Software de flasheo: Rufus (altamente recomendado para esta imagen), BalenaEtcher o `dd` en WSL/Linux.
- Herramienta de particionado (opcional): MiniTool Partition Wizard o gparted en WSL/Linux para asegurar el redimensionamiento correcto si el script inicial falla.

## Descarga

- Repositorio de la comunidad: al ser una compilación nacida de la escena y optimizada por desarrolladores independientes, la imagen estable se distribuye en GitHub — <https://github.com/retrogamecorps/Simple30>
- Descargar siempre la última compilación limpia en formato de imagen (ej. `Simple30-PocketGoS30-vX.X.img`).

## Preparación de almacenamiento

- **SD de sistema (única)**: no requiere formateo manual previo; el flasheo reestructura la tarjeta MicroSD con las particiones lógicas del kernel y la partición visible del usuario.
- **Nomenclatura estricta de carpetas**: Simple30 utiliza la nomenclatura nativa de SimpleMenu para la ruta de los juegos, alojada en una partición visible en formato FAT32 o exFAT. Hay que inyectar la estructura creando carpetas en la raíz del almacenamiento respetando mayúsculas y nombres de sistemas específicos como `/roms/NES/`, `/roms/SNES/`, `/roms/GBA/`, `/roms/MAME/` y `/roms/PSX/`.

## Instalación

1. Inserta la MicroSD en el lector de tarjetas del ordenador.
2. Ejecuta el software de flasheo (ej. Rufus) y carga el archivo de imagen `.img` de Simple30.
3. Selecciona la unidad correspondiente a la tarjeta y haz clic en Escribir/Iniciar. Al finalizar, ignora los mensajes de error de Windows relativos al formato de particiones adicionales y expulsa la tarjeta de forma segura.

## Primer arranque

1. Inserta la MicroSD flasheada en la ranura única de la PocketGo S30.
2. Enciende la consola. El sistema ejecuta un script automático de inicialización en segundo plano que redimensiona la partición de datos visible para ocupar el 100% de la capacidad restante de la tarjeta. La consola se reinicia automáticamente.
3. Al finalizar, el dispositivo carga directamente la interfaz de Simple30 indexando los sistemas (aparecerán vacíos hasta que se vuelquen las colecciones).

## Configuración post-instalación

- **Volcado de datos**: transfiere los ROMsets validados a las carpetas correspondientes dentro de `/roms/`. Las BIOS obligatorias para consolas basadas en discos u ordenadores deben copiarse estrictamente en la subcarpeta centralizada `/roms/bios/` o en la ruta de sistema interna asignada por RetroArch.
- **Tratamiento de carátulas (previews)**: al utilizar SimpleMenu como frontend, el sistema no depende de archivos `gamelist.xml` planos. Busca imágenes estáticas en formato `.png` guardadas estrictamente dentro de una subcarpeta oculta `.previews` dentro de la carpeta de cada consola (ej. `/roms/SNES/.previews/`). Los nombres de las portadas deben coincidir byte por byte con el nombre del archivo de la ROM.
- Ventaja de pipeline propio: es posible procesar estas imágenes de forma masiva reduciendo su resolución a un ancho máximo optimizado para la pantalla de la S30 (generalmente reescaladas a un máximo de 640x480 o 320x240 píxeles según la tasa de compresión), evitando retrasos visuales al navegar a gran velocidad por las listas.

## Notas

- **Tratamiento de ROMsets Arcade**: los núcleos de RetroArch incluidos en Simple30 para la PocketGo S30 están ajustados para emular de forma óptima subsets basados en el archivo DAT oficial de MAME 2003-Plus (romset `0.78-plus`) para arcade general, y FinalBurn Neo (formato Non-Merged) para placas de lucha CPS y Neo-Geo. Es crítico filtrar los juegos con estas variantes exactas para evitar pantallas en negro.
- **Optimización para PlayStation 1**: el hardware de la PocketGo S30 ejecuta PS1 a velocidad completa de forma nativa. Para garantizar un rendimiento óptimo, es directriz mandatoria realizar la conversión masiva de las ISOs/BIN al formato comprimido CHD (v5). Simple30 gestiona los CHDs a la perfección, aliviando el bus de lectura de la MicroSD y ahorrando hasta un 40% de espacio de almacenamiento.
- **Gestión 1G1R crucial**: aunque Simple30 aligera enormemente el rendimiento del frontend, el hardware de la consola sigue teniendo limitaciones de memoria RAM. Cargar carpetas saturadas con miles de ROMs (como sets completos con clones e idiomas duplicados) provoca que el listado tarde varios segundos en abrirse. Aplicar un filtro 1G1R estricto (con herramientas como retool) para dejar subsets limpios de títulos esenciales optimiza los tiempos de indexación y ofrece una navegación inmediata a 60 FPS estables.
