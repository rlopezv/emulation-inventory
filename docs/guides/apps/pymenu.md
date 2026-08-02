# pyMenu

pyMenu es un frontend minimalista, ligero y de código abierto escrito en Python utilizando la librería gráfica Pygame. Fue desarrollado originalmente por la scene para ofrecer una alternativa de lanzamiento ágil, limpia y estructurada en dispositivos portátiles retro de recursos extremadamente críticos. A diferencia de las interfaces gráficas modernas que escanean directorios dinámicamente, pyMenu funciona como un lanzador de accesos directos estáticos que interpreta scripts en tiempo real y gestiona su menú mediante archivos de texto plano, garantizando tiempos de arranque instantáneos y una tasa de refresco fluida en microprocesadores de generaciones previas.

## Contexto de uso

Embebido en CFW / Standalone ligero.

## CFWs / plataformas donde se usa

- MiyooCFW clásico / BittBoy CFW (consolas de la familia BittBoy, PocketGo original y PowKiddy Q90/V90 en sus compilaciones tempranas de la scene)
- Dingux / OpenDingux (como lanzador secundario ligero en dispositivos basados en chips Ingenic)
- Distribuciones personalizadas en Raspberry Pi Zero (proyectos modulares DIY de llaveros de emulación que buscan el mínimo consumo de CPU)

## Descarga

Depende del CFW: en las compilaciones que lo adoptan como lanzador por defecto viene integrado (no aplica descarga aparte). En otros casos, los scripts fuente basados en `.py` y sus archivos de configuración se descargan directamente desde los repositorios de la scene de MiyooCFW en GitHub para instalarlo como lanzador secundario sobre un sistema ya existente.

## Instalación

Depende del CFW:

- **Embebido**: no aplica de forma externa; el sistema operativo de la consola se encarga de inicializar el intérprete de Python y arrancar el script principal de pyMenu automáticamente al encender el dispositivo.
- **Standalone**: hay que copiar manualmente los scripts `.py`, el intérprete de Python (si no está ya presente en el sistema base) y los archivos de configuración a la ruta que espera el CFW, y registrar pyMenu como lanzador (según el mecanismo de arranque del CFW destino). [TODO: pasos exactos por CFW, ya que varían.]

## Estructura de carpetas y ROMs

pyMenu no gestiona romsets de forma dinámica ni escanea carpetas. Su arquitectura depende en su totalidad de una indexación manual basada en texto plano:

- **El archivo de configuración maestro**: el frontend lee la lista de elementos disponibles a través de un archivo de texto plano de configuración, comúnmente llamado `config.ini` o `menu.cfg`, ubicado en la carpeta del sistema (ej. `/main/pymenu/`).
- **Asignación de entradas fijas**: dentro de este archivo, cada juego, emulador o aplicación debe declararse de forma individual como una sección fija, especificando la ruta exacta del ejecutable y sus argumentos de lanzamiento.
- **Mapeo del pipeline**: un script propio no puede limitarse a volcar carpetas de juegos. Para dar soporte a pyMenu, debe encargarse de escribir o editar de forma automatizada este archivo `.ini` maestro, generando una entrada de texto por cada título que haya pasado los filtros.

Ejemplo práctico de configuración estática (`config.ini`):

```ini
# Configuración global del frontend
[General]
skin = default
font = /mnt/pymenu/fonts/retro.ttf
fontsize = 14

# Entrada fija para arrancar un emulador independiente (método recomendado)
[PlayStation 1]
exec = /mnt/apps/pcsx4all.opk
args =
icon = /mnt/pymenu/skins/default/icons/ps1.png

# Entrada fija para arrancar un juego directo (acceso directo a ROM)
[Super Mario World]
exec = /mnt/apps/pocketsnes.opk
args = /mnt/roms/snes/smw.sfc
icon = /mnt/pymenu/skins/default/icons/smw.png

# Entrada fija para un port o juego nativo
[Cave Story]
exec = /mnt/apps/cavestory.opk
args =
icon = /mnt/pymenu/skins/default/icons/cavestory.png
```

## Metadatos y scraping

pyMenu no soporta archivos indexadores de metadatos complejos (`gamelist.xml`) ni descripciones:

- **Tratamiento de iconos/carátulas**: asocia cada entrada fija del archivo `.ini` a una imagen en formato `.png` o `.bmp` asignada explícitamente en la línea `icon =`.
- **Nomenclatura libre**: dado que la ruta de la carátula se escribe manualmente en el archivo de configuración, el nombre de la imagen no tiene por qué coincidir con el de la ROM; basta con que la ruta declarada en el `.ini` sea exacta.
- **Acción crítica de pipeline (por RAM)**: las imágenes se cargan directamente en la memoria caché de vídeo de Pygame sin reescalado dinámico. Hay que procesar estas imágenes multimedia reescalándolas de forma masiva a resoluciones cuadradas muy bajas (habitualmente 32x32 o 64x64 píxeles para iconos de menú, o un máximo de 160x120 si el tema tiene ventana de previsualización).

## Temas y personalización

La estética de la interfaz es completamente personalizable modificando las hojas de estilo del script y los recursos gráficos locales:

- **Estructura del tema**: un tema de pyMenu consta de una imagen de fondo fija en formato BMP/PNG, iconos transparentes para las categorías y fuentes del sistema.
- **Posicionamiento por coordenadas**: las coordenadas donde se dibuja el texto de los accesos directos y la ventana de previsualización del icono están fijadas mediante variables numéricas de píxeles en el código de Python de la interfaz. Modificar la relación de aspecto de las imágenes por fuera de estas coordenadas provoca que el icono se renderice cortado o tape las líneas de texto del menú.

## Notas

- **Límite crítico de entradas por pantalla (filtro 1G1R ultra-agresivo)**: al renderizar cada entrada de forma individual mediante código de Pygame en tiempo real, intentar meter más de 50-100 entradas de texto en una sola sección congela el frontend por completo o satura los 32MB de RAM de la consola. Es técnicamente obligatorio aplicar un filtro 1G1R ultra-estricto para seleccionar únicamente una decena de títulos indispensables por sistema si se van a estructurar accesos directos por juego, descartando por completo full-sets o listas masivas.
- **Propósito real del frontend**: en la scene de dispositivos modestos, pyMenu se utiliza principalmente como un lanzador limpio de emuladores independientes (una sección para RetroArch, otra para PCSX4All, otra para PicoDrive). El usuario arranca el emulador desde pyMenu y es el propio emulador nativo el que se encarga de abrir su explorador interno para buscar las carpetas físicas de ROMs en la tarjeta SD.
- **Apagado seguro obligatorio**: aunque pyMenu es una interfaz ligera, estas consolas de bajo coste carecen de un circuito de apagado por software y cortan la corriente directamente mediante un interruptor físico de hardware. Para evitar la corrupción de bloques de la MicroSD o de los archivos de configuración del `.ini`, se recomienda cerrar siempre los emuladores abiertos y regresar a pyMenu antes de mover el interruptor físico.
