# Pegasus

Pegasus es un frontend gráfico multiplataforma, de código abierto, independiente (standalone) y de rendimiento extremo diseñado para gestionar colecciones de juegos masivas. Desarrollado en C++ sobre el framework Qt, destaca técnicamente por separar por completo la lógica del programa de la interfaz visual: los temas se programan directamente utilizando QML (Qt Modeling Language) y JavaScript, permitiendo carátulas dinámicas en 3D, animaciones a 60 FPS reales y el uso de vídeo sin impacto en la CPU. Su núcleo prescinde de bases de datos XML en favor de un sistema propietario de archivos de texto plano indexados de lectura secuencial ultrarrápida.

## Contexto de uso

Standalone instalable (APK Android / ejecutable PC).

## CFWs / plataformas donde se usa

- Android (gama media/alta): Custom ROMs como GammaOS Next, GammaOS Core o LineageOS en dispositivos tipo Retroid Pocket (4/4 Pro), AYN Odin (1/2), Anbernic RG Cube o RG556.
- PCs de sobremesa y portátiles (Windows/Linux/macOS): sistemas dedicados x86_64, ordenadores gaming y consolas portátiles de PC (Steam Deck, ASUS ROG Ally, Lenovo Legion Go).
- Sistemas embebidos avanzados: placas reducidas de 64 bits tipo Raspberry Pi 4/5 ejecutando distribuciones limpias de Linux.

## Descarga

- Sitio y repositorio oficial: <https://pegasus-frontend.org/>

## Instalación

- **En Android**: descarga el archivo de instalación portátil `.apk`, habilita "Instalar aplicaciones de orígenes desconocidos" en los ajustes de seguridad del dispositivo y ejecuta el archivo para instalar el frontend.
- **En PC (Windows)**: descarga el ejecutable portátil de 64 bits o el instalador `.msi`. No requiere dependencias adicionales.
- **En Linux / Steam Deck**: se puede instalar de forma directa como paquete Flatpak desde la tienda de aplicaciones Discover en modo escritorio.

## Estructura de carpetas y ROMs

Pegasus ofrece una flexibilidad total, pero depende de la declaración de directorios mediante un archivo central de metadatos:

- **La raíz estándar**: es plenamente compatible con el esquema de carpetas clásico en minúsculas en una tarjeta MicroSD o disco duro externo exFAT (ej. `/roms/nes/`, `/roms/snes/`, `/roms/megadrive/`, `/roms/psx/`).
- **Mapeo del pipeline**: Pegasus detecta los sistemas leyendo un archivo de texto indexador en cada subcarpeta de juegos. Un script propio debe inyectar este archivo de metadatos directamente en la raíz de cada directorio físico de consola junto a las ROMs.

## Metadatos y scraping

Pegasus no es compatible con archivos XML (`gamelist.xml`) ni bases de datos tradicionales. Utiliza un formato de texto plano propietario y estricto llamado obligatoriamente `metadata.txt` (o `metadata.pegasus.txt`), que debe residir en la raíz de la carpeta de cada consola (ej. `/roms/snes/metadata.txt`).

- **El archivo de metadatos**: estructura la ficha técnica del juego utilizando indentaciones limpias mediante espacios o tabuladores y asigna las palabras clave de los recursos multimedia.
- Ventaja de pipeline propio (crítica): escribir este formato en Python es extremadamente sencillo mediante cadenas de texto y bucles f-string. Un script puede parsear los archivos DAT XML de origen, limpiar clones (1G1R) y volcar este archivo de texto secuencial de forma nativa en segundos, ahorrando el lento scraping por Wi-Fi o internet en el frontend.

Ejemplo práctico de indexador Pegasus (`metadata.txt`):

```text
collection: Super Nintendo Entertainment System
shortname: snes
extensions: sfc, smc
launch: retroarch -L /cores/snes9x_libretro.so %ROM%

game: Super Mario World
file: Super Mario World (USA).sfc
developer: Nintendo
publisher: Nintendo
release: 1991-08-13
players: 2
genres: Platform
description: El legendario juego de plataformas de fontaneros lanzado para el cerebro de la bestia.
assets.boxart: ./media/boxart/Super Mario World (USA).png
assets.video: ./media/video/Super Mario World (USA).mp4
```

## Temas y personalización

Gracias a la implementación del motor gráfico QML (Qt), Pegasus cuenta con los temas visuales más dinámicos y estilizados de la escena retro:

- **Tratamiento de carátulas (assets)**: los nombres de las etiquetas de imágenes en `metadata.txt` pueden personalizarse según el tema elegido (ej. `assets.boxart`, `assets.screenshot`, `assets.clearlogo`). Las imágenes y vídeos se guardan por defecto en subcarpetas dedicadas dentro del directorio de la consola (ej. `/roms/snes/media/boxart/`).
- **Control de rendimiento en el pipeline**: al procesar código QML pesado, si se inyectan imágenes en alta resolución (4K/1080p), la memoria de vídeo de los dispositivos de gama media sufre tirones severos (stuttering) al recargar los assets dinámicos en las transiciones 3D. Es directriz técnica obligatoria reescalar masivamente todas las carátulas a una resolución optimizada de 480p (ancho máximo de 640 píxeles o alto máximo de 480 píxeles) en formato PNG de 8 bits (indexado), lo que garantiza que las animaciones QML de Pegasus mantengan sus 60 FPS estables.

## Notas

- **Tratamiento de ROMsets Arcade modernos**: al ejecutarse en PCs y entornos de Android de 64 bits de alto rendimiento, los emuladores vinculados a Pegasus están completamente actualizados. El estándar para sistemas arcade y placas dedicadas (CPS1/2/3 y Neo-Geo) debe basarse en el archivo DAT oficial de FinalBurn Neo (romset en formato Non-Merged). Para arcade generales complejos, usar el núcleo MAME actualizado. Incluir la BIOS `neogeo.zip` correspondiente en la raíz de sus carpetas arcade.
- **Optimización de consolas de disco avanzadas**: el formato de compresión CHD (v5) es el estándar mandatorio para cualquier sistema basado en discos compactos (PS1, Saturn, Sega CD, Dreamcast, PS2) mapeado por Pegasus. Reduce el peso de las ISOs a la mitad y acelera los hilos de carga de los emuladores independientes (standalone) tipo DuckStation o AetherSX2 integrados en la consola. Para PSP, usar el formato comprimido CSO.
- **Gestión 1G1R del frontend**: aunque la carga secuencial de `metadata.txt` de Pegasus es la más rápida de la escena (capaz de leer catálogos de 10.000 juegos en menos de un segundo), tener carpetas saturadas con clones, betas, demos e idiomas duplicados destruye la elegancia visual de los temas basados en cuadrículas (grid themes). Es una excelente práctica de ingeniería aplicar un filtro 1G1R estricto (con herramientas como retool) antes de transferir los juegos, limitando las listas a los títulos esenciales e idiomas preferidos por región para mantener una biblioteca limpia, fluida y premium.
