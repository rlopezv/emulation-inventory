# SimpleMenu

SimpleMenu es un frontend de código abierto, ultraligero y de rendimiento extremo diseñado específicamente para consolas portátiles y dispositivos embebidos con recursos de hardware limitados. Escrito en C utilizando la librería SDL2, prescinde por completo de los motores gráficos pesados e indexadores de bases de datos complejos en favor de una arquitectura basada en listas de texto plano, transiciones directas y carga instantánea. Destaca en la scene por ofrecer una interfaz limpia que optimiza el uso de la memoria RAM, maximiza la autonomía de la batería y arranca los emuladores nativos de forma directa mediante argumentos de línea de comandos.

## Contexto de uso

Embebido en CFW (viene incluido, sin instalación propia).

## CFWs / plataformas donde se usa

- Adam Image (Anbernic serie RG350, RG280V, RG300X, PocketGo 2)
- Simple30 (PocketGo S30)
- Miyoo Stock/Custom Mod (dispositivos basados en chips Allwinner/Ingenic que buscan menús de texto plano rápidos)

Nota: se han excluido de esta lista Rogue CFW y dArkOS, que en `docs/software.md` (y en el caso de dArkOS también en `darkos.md`) figuran con GMenu2X y EmulationStation respectivamente, no SimpleMenu.

## Descarga

No aplica: viene integrado en el CFW.

## Instalación

No aplica: viene integrado en el CFW.

## Estructura de carpetas y ROMs

La flexibilidad de SimpleMenu radica en sus archivos de configuración llamados `section.ini` (o archivos `.ini` por consola). Estos archivos definen de forma estricta las rutas físicas de las ROMs y las extensiones legibles:

- **La raíz estándar**: aunque cada CFW puede renombrar la carpeta de juegos (ej. `/roms/` o `/Roms/`), la estructura interna que exige SimpleMenu se organiza por directorios con las siglas oficiales de los sistemas (ej. `/roms/NES/`, `/roms/SNES/`, `/roms/GBA/`, `/roms/MAME/`, `/roms/PSX/`).
- **Mapeo del pipeline**: un script propio debe leer los archivos `.ini` del frontend (ubicados comúnmente en la partición de sistema en carpetas como `/.simplemenu/sections/`) para extraer la clave `roms =` y saber exactamente a qué carpeta física del disco hay que volcar los juegos según el CFW destino.

Ejemplo práctico de configuración estática (`sections.ini`) — un pipeline propio debe ser capaz de interpretar o reescribir bloques estructurados como este para mapear correctamente las rutas de los emuladores nativos en el sistema:

```ini
[Console]
execs = /media/data/apps/pocketsnes.opk
roms = /media/sdcard/roms/SNES
extensions = sfc,smc,fig
launcher =
architecture = mips

[Arcade]
execs = /media/data/apps/fba-sdl.opk
roms = /media/sdcard/roms/MAME
extensions = zip,7z
launcher =
architecture = mips
```

## Metadatos y scraping

SimpleMenu rompe con la arquitectura clásica de archivos indexadores planos como `gamelist.xml`. No procesa metadatos basados en texto (descripciones, año, género, número de jugadores) dentro de las listas de juegos para no saturar la caché:

- **Tratamiento de carátulas (previews)**: el frontend lee las imágenes multimedia por correspondencia directa de nombres planos en formato `.png` o `.jpg`.
- **Ubicación de imágenes**: las portadas deben guardarse obligatoriamente dentro de una subcarpeta llamada estrictamente `.previews` (con punto inicial, lo que la convierte en una carpeta oculta en Linux) situada en la raíz de la carpeta de cada consola (ejemplo: `/roms/SNES/.previews/`).
- **Nomenclatura estricta**: el archivo de imagen debe llamarse exactamente igual que la ROM, incluyendo mayúsculas, minúsculas y caracteres especiales, variando únicamente la extensión (ej. `Super Mario World (USA).sfc` requiere `Super Mario World (USA).png`).
- Ventaja de pipeline propio: no es necesario generar XMLs. Basta con crear la carpeta `.previews`, descargar las portadas por scraping y renombrarlas en espejo con los archivos de las ROMs. Para pantallas de 320x240 (como la RG280V), reescalar las imágenes masivamente a un ancho máximo de 320 píxeles agiliza el renderizado del menú.

## Temas y personalización

La interfaz visual se controla mediante archivos de texto plano de configuración de temas (`theme.ini`) estructurados por capas de píxeles:

- **Componentes del tema**: un tema de SimpleMenu consta de imágenes de fondo fijas para el menú general, logotipos en formato PNG transparente para las cabeceras de cada consola (system art) y fuentes tipográficas TrueType (`.ttf`).
- **Coordenadas fijas**: en el archivo `theme.ini`, los creadores definen las coordenadas exactas de pantalla (X, Y, Ancho, Alto) donde el frontend debe pintar la lista de texto de los juegos y la ventana de la carátula `.previews`. Si un pipeline de imágenes altera drásticamente la relación de aspecto de la portada, esta podría verse estirada o cortada según las directrices fijadas en el tema activo.

## Notas

- **Tratamiento de ROMsets Arcade modestos**: al ejecutarse principalmente en sistemas con procesadores de baja potencia (como los Ingenic JZ4770 de Adam Image), los emuladores arcade nativos enlazados a SimpleMenu exigen conjuntos muy antiguos. Hay que filtrar y compilar subsets utilizando exclusivamente los archivos DAT oficiales de MAME 0.78 (`mame2003`) para arcade general y FinalBurn Alpha 0.2.97.44 para CPS y Neo-Geo. La BIOS `neogeo.zip` debe residir en el mismo directorio que los juegos.
- **Optimización para sistemas basados en disco**: el formato de compresión CHD (v5) es el estándar mandatorio para sistemas como PS1 o Sega CD gestionados por SimpleMenu. Los emuladores independientes embebidos (como PCSX4All) leen los archivos CHD de forma impecable, reduciendo el peso de la biblioteca a la mitad y evitando que el frontend sufra retrasos al leer listas kilométricas de archivos `.bin`/`.cue` duplicados.
- **Gestión 1G1R obligatoria por límite de caché**: SimpleMenu lee la estructura de archivos físicos de la tarjeta SD en tiempo real al entrar a un sistema y la almacena en una caché indexada volátil. Si una carpeta contiene más de 1200-1500 archivos sueltos (como un full-set de NES sin filtrar), el frontend se congela por completo al arrancar, muestra una pantalla en negro o sufre desbordamiento de memoria RAM. Es técnicamente obligatorio aplicar un filtro 1G1R estricto (con herramientas como retool) para limitar los subsets a un máximo de 300-400 títulos esenciales por plataforma, garantizando un scroll fluido a 60 FPS estables.
- **Refresco manual de listas**: si el usuario añade o elimina un juego introduciendo la tarjeta en el PC, en algunas versiones de SimpleMenu integradas es necesario forzar la actualización de la lista de archivos presionando la combinación de botones configurada por el CFW (comúnmente el botón Select o una opción de recarga en el menú de opciones interno) para que limpie la caché física previa y lea los nuevos nombres.
