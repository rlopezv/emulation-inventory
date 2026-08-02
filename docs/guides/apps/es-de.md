# ES-DE (EmulationStation Desktop Edition)

ES-DE es un frontend gráfico multiplataforma e independiente (standalone) de código abierto que traslada la potencia, modularidad y estética avanzada de EmulationStation a dispositivos móviles y consolas portátiles dedicadas. Desarrollado en C++ utilizando SDL2 y OpenGL, destaca en la escena actual por su estricto cumplimiento de estándares de nombres de carpetas y su potente motor de renderizado de temas tridimensionales. Su núcleo opera mediante un sistema de indexación secuencial basado en archivos XML planos, permitiendo organizar catálogos masivos y lanzar emuladores independientes (standalone) de Android o núcleos de RetroArch mediante llamadas directas de actividad (Android Intents) con una latencia de transición mínima.

## Contexto de uso

Standalone instalable (APK Android / ejecutable PC). Centrado en su ecosistema Android.

## CFWs / plataformas donde se usa

- Android (gama media/alta): dispositivos que ejecutan Custom ROMs como GammaOS Next, LineageOS o el sistema operativo Android de fábrica.
- Hardware portátil compatible: Retroid Pocket (4/4 Pro/Classic), AYN Odin (1/2/2 Mini), Anbernic (RG Cube, RG556, RG406H/V) y smartphones o tablets equipados con mandos telescópicos de gama alta.
- PC/Linux (versión de escritorio): también es la base de referencia de RetroDECK, Bazzite y ChimeraOS.

## Descarga

- Sitio oficial: <https://es-de.org/>
- Amazon Appstore: al ser una aplicación comercial de pago en plataformas móviles, su distribución oficial en Android se centraliza de forma automatizada en la tienda de aplicaciones de Amazon.
- Patreon oficial del desarrollador: se puede obtener el paquete de instalación portátil directo `.apk` para actualizaciones manuales o dispositivos sin servicios de Google suscribiéndose al Patreon oficial de Leon Styhre (creador de ES-DE).

## Instalación

1. Descarga el archivo ejecutable `.apk` en el dispositivo Android a través de la Amazon Appstore o mediante transferencia directa por cable USB.
2. Abre el explorador de archivos de la consola, ejecuta el archivo `.apk` y concede el permiso para "Instalar aplicaciones de orígenes desconocidos" en los ajustes de seguridad de Android.
3. **Configuración del directorio base (paso crítico)**: al abrir ES-DE por primera vez, la aplicación pide crear y seleccionar un directorio central en el almacenamiento del dispositivo o en la MicroSD (generalmente llamado `/ES-DE/`). Esta carpeta aloja los archivos de configuración, los temas visuales y las bases de datos de metadatos XML.

## Estructura de carpetas y ROMs

La arquitectura de ES-DE es la más rígida y estricta de este inventario, ya que se cimenta en un archivo maestro inamovible llamado `es_systems.xml`:

- **La raíz estándar**: exige obligatoriamente una carpeta principal llamada `ROMs` (respetando mayúsculas y minúsculas según la configuración del sistema) en la raíz de la tarjeta MicroSD portátil exFAT. Las subcarpetas utilizan nombres cortos y estrictamente fijos en minúsculas para identificar los sistemas (ej. `/ROMs/nes/`, `/ROMs/snes/`, `/ROMs/megadrive/`, `/ROMs/gba/`, `/ROMs/psx/`). Si se renombra una carpeta (por ejemplo, `/ROMs/SNES/` en mayúsculas), el frontend ignora el directorio por completo.
- **Mapeo del pipeline**: un script propio debe clonar de forma exacta la nomenclatura corta oficial de ES-DE en la tarjeta antes de volcar las ROMs, garantizando que el escáner secuencial del frontend detecte los juegos al arrancar.

## Metadatos y scraping

Siguiendo la herencia de la versión de escritorio, ES-DE en Android depende al 100% de un archivo indexador plano en formato XML llamado estrictamente `gamelist.xml`, el cual debe residir en la raíz de la carpeta de cada consola (ej. `/ROMs/snes/gamelist.xml`).

- **El archivo `gamelist.xml`**: registra la ficha técnica pormenorizada de cada juego y vincula las rutas físicas de sus recursos multimedia.
- **Ubicación de imágenes y vídeos**: los archivos gráficos se guardan por defecto en la ruta centralizada `/ES-DE/downloaded_media/[sistema]/` (en el almacenamiento interno de la consola) o se pueden configurar de forma relativa dentro de la subcarpeta de la consola (ej. `/ROMs/snes/media/images/`).
- Ventaja de pipeline propio: no usar el raspador interno por Wi-Fi de Android. Un script propio puede escribir este archivo `gamelist.xml` de forma automatizada a gran velocidad cruzando bases de datos DAT: lee la ROM, inyecta los datos de texto en las etiquetas del XML y mapea la ruta local de la carátula de forma instantánea.

Ejemplo práctico de indexador para ES-DE (`gamelist.xml`):

```xml
<?xml version="1.0" encoding="utf-8"?>
<gameList>
  <game>
    <path>./Super Mario World (USA).sfc</path>
    <name>Super Mario World</name>
    <desc>El legendario juego de plataformas de fontaneros lanzado para el cerebro de la bestia.</desc>
    <image>./media/images/Super Mario World (USA).png</image>
    <video>./media/videos/Super Mario World (USA).mp4</video>
    <releasedate>19910813T000000</releasedate>
    <developer>Nintendo</developer>
    <publisher>Nintendo</publisher>
    <genre>Platform</genre>
    <players>2</players>
  </game>
</gameList>
```

## Temas y personalización

ES-DE cuenta con el ecosistema de temas más avanzado de Android, interpretando hojas de estilo complejas basadas en XML:

- **Instalación de temas**: los packs de temas visuales se descargan en formato comprimido y deben extraerse estrictamente dentro de la ruta `/ES-DE/themes/` en la memoria de la consola.
- **Control de rendimiento en el pipeline**: los temas modernos de ES-DE (como Art Book Next o Linear) renderizan carátulas y vídeos de forma simultánea con efectos de difuminado y sombras por hardware. Si se inyectan portadas en alta resolución (1080p/4K), el bus de memoria de Android sufre tirones severos (stuttering) o retrasos al hacer scroll rápido. Es directriz técnica obligatoria reescalar masivamente todas las carátulas locales a una resolución óptima de 480p (ancho máximo de 640 píxeles) en formato PNG de 8 bits (indexado), garantizando una navegación limpia a 60 FPS estables.

## Notas

- **Tratamiento de ROMsets Arcade modernos**: al ejecutarse sobre hardware potente de 64 bits en Android, los emuladores vinculados a ES-DE están completamente actualizados. El estándar absoluto para sistemas de placas recreativas (CPS1/2/3 y Neo-Geo) debe basarse en el archivo DAT oficial de FinalBurn Neo (romset en formato Non-Merged). Para juegos arcade generales complejos, implementa el núcleo MAME actualizado. Incluir la BIOS `neogeo.zip` correspondiente en la raíz de sus carpetas arcade.
- **Optimización total para consolas en disco**: al contar con emuladores independientes modernos y actualizados (como DuckStation, AetherSX2 o Flycast), ES-DE ofrece soporte nativo perfecto para el formato comprimido CHD (v5) en sistemas basados en discos ópticos (PS1, Sega CD, Saturn y Dreamcast). Es recomendable automatizar la conversión masiva a CHD para reducir el peso de las ISOs a la mitad, aliviar el bus de lectura de la MicroSD y eliminar los tirones de audio. Para PSP, usar el formato CSO.
- **Gestión de RAM y filtro 1G1R obligatorio**: aunque las consolas portátiles Android actuales cuentan con más recursos (3GB a 8GB de RAM), el motor de ES-DE indexa y parsea todos los archivos `gamelist.xml` de golpe en cada arranque de la aplicación. Cargar carpetas saturadas con miles de clones, betas, demos e idiomas duplicados provoca que el frontend tarde varios minutos en iniciarse, devore la memoria RAM del sistema o sufra cierres inesperados por falta de memoria (Out of Memory Crash). Es técnicamente obligatorio aplicar un filtro 1G1R estricto (con herramientas como retool) antes de transferir los juegos para dejar subsets limpios de títulos esenciales por plataforma, manteniendo el entorno de ES-DE en Android optimizado, ágil y de carga instantánea.
