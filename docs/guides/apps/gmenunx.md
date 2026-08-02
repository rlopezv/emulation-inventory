# GMenuNX

GMenuNX es un frontend gráfico de código abierto, ultraligero y de rendimiento extremo diseñado específicamente para consolas portátiles retro con hardware y memoria RAM severamente limitados. Escrito en C utilizando la librería SDL, prescinde por completo de animaciones pesadas, escalado tridimensional o indexadores de bases de datos XML complejas. Su arquitectura se cimenta en un carrusel de pestañas fijas que lanzan emuladores nativos en formato de paquetes `.opk` o binarios independientes mediante la lectura secuencial de archivos de enlace de texto plano (`.lnk`), optimizando al máximo los ciclos de la CPU y la memoria caché del sistema.

## Contexto de uso

Embebido en CFW (viene incluido, sin instalación propia).

## CFWs / plataformas donde se usa

- RetroFW (PowKiddy LDK, Retrogame RS97, Anbernic RG99, PowKiddy RS-07)
- BOB (Best of the Best) (PowKiddy V90, Q90, Q20 Mini, PocketGo, BitBoy, PowKiddy A13)
- MiyooCFW clásico (consolas basadas en la placa base Allwinner F1C100S / F1C200S)

Nota: `docs/software.md` registra el Frontend de RetroFW como GMenu2X y el de MiyooCFW/BOB (Bittboy/PowKiddy) como SimpleMenu, mientras que esta guía y las propias `retrofw.md`/`bob.md` (redactadas con la misma fuente) indican GMenuNX. Se mantiene la discrepancia sin resolver — podrían ser nombres distintos de forks relacionados según versión del CFW.

## Descarga

No aplica: viene integrado en el CFW.

## Instalación

No aplica: viene integrado en el CFW.

## Estructura de carpetas y ROMs

GMenuNX no cuenta con un escáner dinámico automático de directorios. No detecta juegos metidos a pelo en la tarjeta SD ni autogenera listas leyendo carpetas. Su arquitectura es 100% estática y depende de archivos de texto planos con la extensión `.lnk` (enlaces) almacenados en subcarpetas de secciones dentro de la partición de sistema (ejemplo: `/home/retrofw/.gmenunx/sections/emulators/` o `/gmenu2x/sections/games/`).

- **La raíz de las ROMs**: aunque el frontend no lea las carpetas directamente, los emuladores nativos que lanza sí exigen una ruta. Un pipeline propio debe organizar los juegos en la partición visible utilizando nomenclaturas abreviadas en mayúsculas según las plantillas del CFW de destino (ejemplo: `/roms/FC/` para NES, `/roms/SFC/` para SNES, `/roms/MD/` para Mega Drive, `/roms/PS/` para PS1).
- **Mapeo del pipeline (muy crítico)**: un script propio no puede limitarse a copiar archivos de juegos. Para dar soporte a GMenuNX, debe encargarse de escribir de forma automatizada un archivo de texto `.lnk` individual por cada juego o emulador que deba aparecer en el menú de la consola.

Ejemplo práctico de archivo de enlace estático (`.lnk`), donde el nombre del archivo será el título en el menú (ej. `Super Mario World.lnk`):

```text
title=Super Mario World
icon=/gmenu2x/skins/default/icons/snes.png
exec=/mnt/apps/pocketsnes.opk
params=/mnt/roms/SFC/Super Mario World (USA).sfc
wrapper=false
selector=false
```

## Metadatos y scraping

GMenuNX no soporta archivos indexadores complejos (`gamelist.xml`) ni descripciones de texto, años o géneros:

- **Tratamiento de carátulas (previews)**: la interfaz asocia cada juego o emulador mediante una imagen fija en formato `.png` o `.bmp` que se define de forma explícita en la línea `icon =` del archivo `.lnk`.
- **Nomenclatura libre**: dado que la ruta de la carátula se escribe a mano dentro de cada archivo de enlace, el nombre físico de la imagen no tiene por qué coincidir obligatoriamente con el de la ROM; basta con que la ruta declarada sea exacta.
- **Control de resolución en el pipeline (crítico por RAM)**: GMenuNX carga los iconos/carátulas directamente en la memoria RAM de la consola sin reescalado dinámico por hardware. El tamaño óptimo estricto es de 160x120 píxeles (para carátulas dentro de ventanas de previsualización) o resoluciones cuadradas ultra-bajas como 32x32 o 64x64 píxeles si actúan como iconos de selección. Hay que reescalar masivamente todas las imágenes multimedia y reducir su profundidad de color a 8 bits (indexado). Introducir carátulas HD convencionales provoca un desbordamiento de memoria inmediato (Out of Memory Crash) congelando el frontend.

## Temas y personalización

La estética visual de las pestañas se controla mediante el archivo de texto plano de personalización del aspecto (`skin.ini`) ubicado en el directorio de temas del frontend:

- **Variables de la interfaz**: los archivos de skin definen el color del texto de la lista, la fuente tipográfica TrueType (`.ttf`) usada y las imágenes BMP/PNG de fondo fijas para las pestañas superiores y el pie de página.
- **Posicionamiento fijo**: las coordenadas donde se dibuja la lista textual de enlaces y el recuadro donde se renderiza el archivo gráfico del icono están fijadas mediante variables de píxeles rígidas en el código de la skin. Modificar la relación de aspecto de las imágenes por fuera de estas coordenadas provoca que la carátula se dibuje cortada o tape las líneas de selección.

## Notas

- **Límite de entradas por pestaña (filtro 1G1R ultra-agresivo)**: al renderizar cada enlace estático `.lnk` mediante código secuencial en tiempo real, e intentar cargar simultáneamente sus iconos en la ajustada RAM libre del hardware (usualmente entre 32MB y 64MB en dispositivos MIPS/Allwinner modestos), meter más de 100-150 archivos `.lnk` en una sola sección congela la consola por completo al encenderse o provoca un scroll injugable con ralentizaciones severas. Es técnicamente obligatorio aplicar un filtro 1G1R ultra-estricto para compilar listas muy reducidas de 20-30 títulos esenciales absolutos por plataforma si se van a crear accesos directos por juego.
- **Método alternativo (modo selector)**: si se quiere llevar cientos de juegos sin un filtro 1G1R tan agresivo, la directriz de ingeniería es cambiar la lógica de generación del archivo `.lnk`: en lugar de escribir un `.lnk` por juego, escribir un único archivo `.lnk` por emulador activando la casilla `selector=true` y declarando la ruta de la carpeta de ROMs. Esto hace que GMenuNX muestre solo el icono del emulador y, al hacer clic, delegue la carga en el explorador de archivos básico integrado del propio emulador nativo (el archivo `.opk`), que consume menos memoria RAM.
- **Apagado seguro obligatorio**: las consolas portátiles baratas que integran GMenuNX carecen de circuitos de apagado por software. Mover el interruptor físico de hardware corta la corriente de la batería directamente. Para evitar corrupciones catastróficas en la partición de sistema FAT32 o en las tablas de configuración de los archivos `.lnk` modificados por un pipeline propio, hay que regresar siempre al menú de GMenuNX, cerrar las aplicaciones y apagar el dispositivo mediante la opción de apagado por software del menú del frontend antes de cortar la energía física.
