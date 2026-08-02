# Daijishō

Daijishō es un frontend gráfico de código abierto, independiente (standalone) y de alto rendimiento diseñado exclusivamente para el ecosistema Android. Destaca en la escena de la emulación por su interfaz moderna basada en hilos lógicos que separan la navegación por pestañas de los procesos de sincronización. Su arquitectura se centra en la automatización: asocia de forma nativa cientos de plataformas con sus respectivos emuladores independientes (standalone) o núcleos de RetroArch mediante argumentos de llamada de actividad (Intent arguments), e indexa colecciones masivas de juegos directamente en una base de datos interna SQLite protegida del sistema.

## Contexto de uso

Standalone instalable (APK Android).

## CFWs / plataformas donde se usa

- Android (gama entrada/media/alta): Custom ROMs como GammaOS Next, GammaOS Core, LineageOS o el sistema operativo de fábrica de dispositivos de emulación dedicados.
- Hardware portátil compatible: Retroid Pocket (2/3/3+/4/4 Pro/Flip), AYN Odin (1/2/2 Mini), Anbernic (RG405M, RG405V, RG505, RG556, RG Cube) y smartphones o tablets Android modificados para juego retro.

## Descarga

- Google Play Store: disponible de forma directa para su instalación automática en dispositivos con acceso a los servicios de Google.
- Repositorio/sitio oficial: para dispositivos con Custom ROMs sin servicios de Google (versiones Lite de GammaOS), el archivo oficial de instalación masiva `.apk` se descarga de <https://daijisho.com/> (o el repositorio activo de mantenimiento de la scene).

## Instalación

1. Descarga el archivo ejecutable `.apk` en el dispositivo Android o transfiérelo mediante cable USB.
2. Abre el explorador de archivos de Android, ejecuta el `.apk` y concede el permiso para "Instalar aplicaciones de orígenes desconocidos" si el sistema operativo lo solicita.
3. Establece Daijishō como el lanzador de escritorio por defecto (Default Home App) en los ajustes de Android para que la consola arranque directamente en el menú de juegos al encenderse.

## Estructura de carpetas y ROMs

Daijishō ofrece una flexibilidad total respecto al almacenamiento físico debido a que no impone nombres específicos para los directorios en el disco:

- **La raíz estándar**: es plenamente compatible con el esquema de carpetas clásico en minúsculas en una tarjeta MicroSD externa formateada en exFAT (ej. `/ROMS/nes/`, `/ROMS/snes/`, `/ROMS/psx/`).
- **Mapeo del pipeline**: al no depender de archivos indexadores locales en las carpetas, un script propio puede volcar los juegos en la estructura limpia que se prefiera. La vinculación de rutas se realiza dentro de la interfaz de la aplicación agregando el directorio de forma explícita en cada plataforma (`Paths -> Add More`), permitiendo que el frontend indexe el almacenamiento portátil de forma secuencial.

## Metadatos y scraping

Daijishō no lee archivos XML planos locales (`gamelist.xml`) ni archivos de texto (`metadata.txt`) dentro de las carpetas de las ROMs:

- **Bases de datos SQLite**: el frontend analiza el nombre físico del archivo de la ROM, realiza un raspado digital (scraping) interno en línea contra bases de datos como PocketGit o LaunchBox y guarda toda la ficha técnica (descripción, año, género) en una base de datos indexada SQLite interna de la aplicación dentro de la memoria eMMC de la consola.
- Ventaja de pipeline propio (tratamiento de portadas): aunque el raspado de texto se delega al frontend, Daijishō permite inyectar carátulas de forma local. Las imágenes deben llamarse exactamente igual que la ROM (formato `.png` o `.jpg`). En lugar de meterlas en subcarpetas de la MicroSD, un script puede preparar una carpeta centralizada; al configurar Daijishō, se puede dirigir el apartado de portadas de la plataforma a esa ruta local para que la base de datos asocie el archivo gráfico al instante, ahorrando horas de descarga por Wi-Fi.

## Temas y personalización

El aspecto estético se controla mediante paquetes de temas centralizados que modifican el fondo de pantalla de cada consola (wallpaper packs):

- **Formatos admitidos**: los temas se distribuyen en archivos comprimidos que contienen imágenes fijas o en bucle y se descargan directamente desde el menú interno de la aplicación.
- **Control de rendimiento en el pipeline**: Daijishō renderiza las listas de juegos en forma de carrusel visual continuo. Si se utilizan tarjetas MicroSD saturadas o si el backend del frontend intenta cargar portadas en alta resolución (1080p/4K), la memoria RAM de dispositivos modestos (gama Core con 1GB/2GB) sufre tirones severos (stuttering) o congelamientos de la interfaz. Es directriz técnica obligatoria reescalar todas las carátulas locales a una resolución óptima de 480p (ancho máximo de 640 píxeles) antes de transferirlas para garantizar un scroll fluido a 60 FPS estables.

## Notas

- **Tratamiento de ROMsets Arcade de 64 bits**: al ejecutarse sobre núcleos modernos de Android, los emuladores vinculados son plenamente actuales. El estándar absoluto para sistemas arcade y placas dedicadas (CPS1/2/3 y Neo-Geo) debe basarse en el archivo DAT oficial de FinalBurn Neo (romset en formato Non-Merged). Para el resto del catálogo arcade general, implementa el núcleo MAME 2003-Plus (romset `0.78-plus`). Incluir la BIOS `neogeo.zip` correspondiente en la raíz de sus carpetas arcade.
- **Optimización de consolas de disco pesadas**: el formato de compresión CHD (v5) es el estándar mandatorio para cualquier sistema basado en discos compactos (PS1, Saturn, Sega CD, Dreamcast, PS2) mapeado por Daijishō. Aligerar el peso de las ISOs a la mitad optimiza drásticamente los hilos de carga de emuladores independientes avanzados de Android como DuckStation o AetherSX2. Para PSP, usar el formato comprimido CSO.
- **Gestión obligatoria de la RAM (filtro 1G1R)**: esta es la directriz más crítica en Android. Daijishō devora una cantidad masiva de memoria RAM al indexar y mantener en caché las listas si estas contienen miles de títulos. Si se intenta cargar un full-set completo con clones, betas, demos e idiomas duplicados (ej. más de 3000 juegos de NES), el frontend sufre cierres inesperados por falta de memoria (Out of Memory / OOM Crash) o ralentiza la navegación de forma crítica en consolas económicas. Es técnicamente obligatorio aplicar un filtro 1G1R estricto (con herramientas como retool) antes de transferir los juegos para dejar subsets limpios de títulos esenciales por plataforma, manteniendo el entorno de Android estable y fluido.
