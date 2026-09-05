# EmulationStation

EmulationStation es un frontend gráfico de código abierto, multiplataforma y de alto rendimiento diseñado para actuar como la interfaz visual central en sistemas de emulación dedicados. Escrito en C++ utilizando la API gráfica OpenGL/OpenGL ES, destaca por su arquitectura modular basada en temas enriquecidos que admiten carátulas en alta resolución, clips de vídeo, música de fondo y efectos tridimensionales. Su núcleo opera leyendo e indexando bases de datos en texto estructurado XML, lo que le permite organizar catálogos masivos de juegos ordenándolos por metadatos avanzados (año, género, desarrollador, número de jugadores) y lanzar emuladores o núcleos de RetroArch mediante argumentos dinámicos en segundo plano.

## Contexto de uso

Embebido en CFW (viene incluido, sin instalación propia).

## CFWs / plataformas donde se usa

- KNULLI (Anbernic series RG35XX Plus/H/SP/CubeXX, PowKiddy V10)
- ROCKNIX / JELOS (PowKiddy RGB10 Max 3/X55, Anbernic RG353P/V/M)
- AmberELEC / 351ELEC (Anbernic RG351M/V/MP)
- dArkOS (PowKiddy RGB20, RGB10 Max 2)
- Batocera / Recalbox (Raspberry Pi 3/4/5, mini PCs x86_64, ordenadores de sobremesa)
- EmuELEC (TV Boxes Amlogic, Super Console X, Game Sticks)

## Descarga

No aplica: viene integrado en el CFW.

## Instalación

No aplica: viene integrado en el CFW.

## Estructura de carpetas y ROMs

La flexibilidad de EmulationStation se cimenta en su archivo de configuración maestro llamado `es_systems.cfg`, el cual mapea los sistemas del frontend con los directorios de disco:

- **La raíz estándar**: se organiza en una partición dedicada a los datos del usuario (etiquetada como `SHARE`, `STORAGE` o `EEROMS` según el CFW) dentro de una carpeta central llamada `/roms/`. Las subcarpetas utilizan nombres cortos en minúsculas estrictas para identificar los sistemas (ej. `/roms/nes/`, `/roms/snes/`, `/roms/megadrive/`, `/roms/gba/`, `/roms/psx/`, `/roms/arcade/`).
- **Mapeo del pipeline**: un script propio debe clonar exactamente esta estructura de rutas en minúsculas en el disco duro o tarjeta SD antes de inyectar los metadatos, evitando alterar la nomenclatura para que el motor de escaneo de EmulationStation localice los binarios.

Ejemplo práctico de configuración de sistema (`es_systems.cfg`):

```xml
<systemList>
  <system>
    <name>snes</name>
    <fullname>Super Nintendo Entertainment System</fullname>
    <path>/storage/roms/snes</path>
    <extension>.sfc .smc .SFC .SMC</extension>
    <command>retroarch -L /usr/lib/libretro/snes9x_libretro.so %ROM%</command>
    <platform>snes</platform>
    <theme>snes</theme>
  </system>
</systemList>
```

## Metadatos y scraping

A diferencia de los frontends minimalistas, EmulationStation depende al 100% de un archivo indexador plano en formato XML llamado estrictamente `gamelist.xml`, el cual debe residir en la raíz de la carpeta de cada consola (ej. `/roms/snes/gamelist.xml`).

- **El archivo `gamelist.xml`**: registra de forma minuciosa la ficha técnica de cada juego y vincula las rutas locales de sus recursos multimedia.
- **Ubicación de imágenes y vídeos**: los archivos gráficos se guardan por defecto en subcarpetas dentro del directorio del sistema, típicamente llamadas `/roms/[sistema]/images/` para carátulas y `/roms/[sistema]/videos/` para fragmentos de vídeo.
- Ventaja de pipeline propio (crítica): no usar el raspador por Wi-Fi integrado en la consola (es extremadamente lento). Un script propio puede generar el archivo `gamelist.xml` de forma nativa a la velocidad del procesador del PC cruzando bases de datos DAT: lee la ROM, calcula su hash, inyecta los datos de texto en las etiquetas del XML y escribe la ruta local de la carátula precargada de forma instantánea.

Ejemplo práctico de indexador XML (`gamelist.xml`):

```xml
<?xml version="1.0" encoding="utf-8"?>
<gameList>
  <game>
    <path>./Super Mario World (USA).sfc</path>
    <name>Super Mario World</name>
    <desc>El legendario juego de plataformas de fontaneros lanzado para el cerebro de la bestia.</desc>
    <image>./images/Super Mario World (USA).png</image>
    <video>./videos/Super Mario World (USA).mp4</video>
    <releasedate>19910813T000000</releasedate>
    <developer>Nintendo</developer>
    <publisher>Nintendo</publisher>
    <genre>Platform</genre>
    <players>2</players>
  </game>
</gameList>
```

## Temas y personalización

El aspecto visual completo se gestiona interpretando hojas de estilo XML ubicadas en el directorio de temas del sistema (ej. `/etc/emulationstation/themes/` o `/share/themes/`):

- **Variables del tema**: los archivos `theme.xml` definen cómo se pintan en pantalla los elementos. Organizan la tipografía (`.ttf`), la lista de selección de juegos, la ventana del vídeo y el encuadre de la carátula mediante etiquetas de tamaño y posición relativas (valores flotantes entre 0.0 y 1.0 respecto al total de la pantalla).
- **Control de resolución en el pipeline**: en sistemas embebidos modestos (como las portátiles de la familia H700 de KNULLI o EmuELEC), cargar imágenes en alta resolución (4K/1080p) colapsa los hilos de renderizado de la GPU de la consola, provocando tirones severos (stuttering) o bloqueos de la interfaz por falta de RAM. Es directriz obligatoria reescalar masivamente todas las carátulas a una resolución optimizada de 480p (ancho máximo de 640 píxeles o alto máximo de 480 píxeles) en formato PNG de 8 bits antes de transferirlas, garantizando un scroll fluido a 60 FPS estables.

## Notas

- **Tratamiento de ROMsets Arcade modernos**: en los CFWs modernos que incorporan EmulationStation (KNULLI, ROCKNIX, Batocera), los núcleos de RetroArch están actualizados. El estándar absoluto para sistemas arcade y placas dedicadas (CPS1/2/3 y Neo-Geo) debe basarse en el archivo DAT oficial de FinalBurn Neo (romset en formato Non-Merged). Para el resto del catálogo recreativo general, implementa el núcleo equilibrado MAME 2003-Plus (romset `0.78-plus`). Inyectar la BIOS `neogeo.zip` correspondiente a cada era en la raíz de sus carpetas arcade.
- **Optimización de consolas de disco pesadas**: el formato de compresión CHD (v5) es el estándar mandatorio para cualquier sistema basado en discos compactos (PS1, Saturn, Sega CD, Dreamcast, Panasonic 3DO, PC-FX) mapeado por EmulationStation. Reduce el peso de las ISOs a la mitad, estabiliza los fotogramas del frontend al saltarse pistas redundantes y optimiza el bus de transferencia de datos de la MicroSD. Para PSP y PlayStation 2 (en sistemas compatibles), usar el formato comprimido CSO.
- **Gestión 1G1R de la interfaz**: aunque EmulationStation en arquitecturas de 64 bits es un motor ágil, leer un directorio físico que contenga más de 2000-3000 archivos sueltos (como un full-set completo con clones, betas, demos e idiomas duplicados) ralentiza drásticamente el tiempo de arranque inicial de la consola y la carga de imágenes en el menú. Es una excelente práctica de ingeniería aplicar un filtro 1G1R estricto (con herramientas como retool) antes de transferir los juegos, limitando las listas a los títulos esenciales e idiomas preferidos por región, lo que garantiza una indexación inmediata y una interfaz limpia y fluida.
- **Temas y bezels — muy dependientes del dispositivo concreto**: los temas (resolución objetivo, relación de aspecto, si la pantalla es cuadrada/vertical/dual) siguen sin un tratamiento genérico válido para todos los dispositivos — pendiente de abordar por dispositivo/familia cuando se llegue a ese punto. Los bezels (marco decorativo alrededor de la imagen del juego en RetroArch, dimensionado a la resolución/aspect ratio exactos de la pantalla física) ya están cubiertos en `docs/guides/apps/retroarch.md#overlays-y-bezels`: por qué dependen del panel físico, qué ajustes de RetroArch entran en juego (`Overlay Auto Scale`, `Aspect Ratio: Core Provided`) y dónde buscar un pack para un dispositivo+CFW concreto.
