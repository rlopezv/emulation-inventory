# muOS

muOS es un Custom Firmware (CFW) de 64 bits de código abierto, diseño minimalista y rendimiento extremo basado en una distribución Linux ultraligera construida desde cero. Destaca en la escena actual por ofrecer los tiempos de arranque y apagado más rápidos del mercado (menos de 6 segundos), un consumo mínimo de recursos de hardware y una modularidad total. Prescinde de interfaces pesadas como EmulationStation en favor de un menú principal fluido basado en texto y temas personalizables en bloques. Ejecuta emuladores nativos e independientes (standalone) optimizados y núcleos de RetroArch con asignación directa de núcleos por carpeta, permitiendo al usuario elegir el motor de emulación con un solo clic.

## Dispositivos aplicables

- Anbernic RG35XX Plus
- Anbernic RG35XX H (modelo horizontal)
- Anbernic RG35XX SP (modelo plegable)
- Anbernic RG28XX
- Anbernic RG40XX V / RG40XX H
- Nota: muOS se ha convertido en el sistema de referencia para la familia de procesadores Allwinner H700 de Anbernic debido a su excelente gestión de la batería en modo suspensión.

## Tipo de instalación

Imagen flasheada a SD (`.zip` que contiene un archivo `.img`), instalación limpia de fábrica. Admite configuraciones de una sola tarjeta (sistema + ROMs) o un ecosistema de doble tarjeta (SD1 sistema, SD2 ROMs) configurable sobre la marcha.

## Requisitos previos

- Tarjeta MicroSD fiable: una de 16GB o 32GB de calidad para el sistema operativo (SD1) y una opcional de 64GB a 512GB de alta velocidad para juegos (SD2).
- Software de flasheo: Rufus (muy recomendado para la estructura de particiones de muOS), BalenaEtcher o `dd` en WSL/Linux.
- Formateador de almacenamiento: herramientas como GUIFormat para la preparación de la SD2 si es necesario.

## Descarga

- Sitio web y repositorio oficial: las imágenes oficiales estables y sus actualizaciones se centralizan en la web oficial del proyecto — <https://muos.dev/> (con espejos de descarga alojados en servidores seguros o GitHub).
- Nota de descarga: descargar la última versión consolidada (ej. muOS Beans o versiones superiores). La imagen está unificada para toda la familia de dispositivos H700 de Anbernic, por lo que el mismo archivo sirve para varios modelos.

## Preparación de almacenamiento

- **SD1 (Sistema)**: el software de flasheo crea de forma transparente tres particiones lógicas en formato Linux (incluyendo el sistema de archivos raíz y una partición visible en FAT32/exFAT para datos locales si se usa tarjeta única). No requiere preparación manual.
- **SD2 (ROMs — ranura TF2)**: se recomienda formatear la tarjeta secundaria obligatoriamente en exFAT para asegurar compatibilidad total en entornos Windows/WSL y admitir archivos de gran tamaño.
- **Estructura abierta de carpetas**: muOS es el firmware más flexible con las rutas. No impone nombres de carpetas específicos; el explorador de muOS lee cualquier carpeta creada. No obstante, para mantener el orden del pipeline propio, lo idóneo es inyectar una estructura limpia y estándar en la raíz de la SD2 como `/ROMS/NES/`, `/ROMS/SNES/`, `/ROMS/MD/` o `/ROMS/PSX/`.

## Instalación

1. Inserta la SD1 en el lector de tarjetas del ordenador.
2. Abre la herramienta de flasheo (ej. Rufus) y selecciona el archivo `.img` extraído del zip de muOS.
3. Selecciona la MicroSD destino y haz clic en Escribir/Iniciar. Al finalizar la operación, expulsa la tarjeta de forma segura.

## Primer arranque

1. Introduce únicamente la SD1 flasheada en la ranura principal de la consola (TF1/INT). Deja la ranura TF2 vacía.
2. Enciende la consola. muOS ejecuta un script automatizado en pantalla que expande las particiones internas. El proceso tarda menos de dos minutos y la consola muestra el menú principal.
3. Apaga la consola de forma segura desde el menú (`Configuration -> Shutdown`).
4. Inserta la SD2 formateada en exFAT en la ranura secundaria (TF2/EXT) y vuelve a encender la consola. El sistema detecta la tarjeta de forma automática. No requiere activar casillas de cambio de tarjeta en los menús, ya que muOS lee ambas ranuras simultáneamente en su explorador de contenido (Content Explorer).

## Configuración post-instalación

- **Volcado de ROMsets y BIOS**: transfiere las colecciones de juegos organizadas a las carpetas en la SD2. Las BIOS del sistema son obligatorias para el arranque de núcleos avanzados y deben guardarse estrictamente en la carpeta centralizada `/MUOS/bios/` ubicada en la tarjeta de sistema (SD1) o en la raíz de la SD2 si se prefiere unificarlo.
- **Tratamiento de carátulas (boxart simplificado)**: muOS no utiliza archivos indexadores XML pesados (`gamelist.xml`); lee las carátulas por correspondencia directa de nombres planos en formato `.png` o `.jpg`. Las portadas deben guardarse de forma centralizada en la partición de juegos bajo la ruta `/MUOS/info/catalogue/[Nombre_de_la_carpeta_de_tus_roms]/`. El archivo de imagen debe llamarse exactamente igual que la ROM.

## Notas

- **Tratamiento de ROMsets Arcade modulares**: al basarse en RetroArch de 64 bits, muOS soporta los núcleos más modernos de FinalBurn Neo (romset Non-Merged). Para MAME, permite alternar sobre la marcha entre MAME 2003-Plus (`0.78-plus`) y MAME 2010. Lo particular de muOS es que se puede hacer clic derecho sobre la carpeta Arcade en la consola, seleccionar "Assign Core" y elegir qué emulador abrirá todos los archivos de esa carpeta, simplificando la gestión de subsets mixtos.
- **Optimización de formatos de disco**: soporta de forma nativa el formato comprimido CHD (v5) para sistemas de 16, 32 y 64 bits (PS1, Saturn, Dreamcast, Sega CD, PC-FX, 3DO) y RVZ para emuladores experimentales aplicables. Se recomienda automatizar la conversión masiva a CHD para reducir el peso de las ISOs a la mitad y optimizar el bus de lectura de la MicroSD.
- **Velocidad vs metadatos (filtro 1G1R recomendado)**: dado que muOS lee las carpetas de la tarjeta SD en tiempo real al navegar por los menús (lo que garantiza que nunca haga falta "actualizar la lista de juegos" al meter una ROM nueva), tener carpetas saturadas con más de 3000 archivos puede provocar un pequeño retraso al abrir el directorio por primera vez. Aplicar un filtro 1G1R limpio (con herramientas como retool) para dejar subsets de títulos esenciales garantiza que la navegación por texto plano mantenga su tasa de refresco nativa a 60 FPS estables y una velocidad de carga instantánea.
