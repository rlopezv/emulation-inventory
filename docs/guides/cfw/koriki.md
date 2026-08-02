# Koriki

Koriki es un Custom Firmware (CFW) de código abierto y alto rendimiento diseñado originalmente como una capa de optimización para el frontend SimpleMenu sobre sistemas portátiles económicos. Destaca técnicamente por sustituir el entorno gráfico pesado por un servidor de pantalla optimizado y controladores que reducen la latencia de entrada (input lag). Su arquitectura permite exprimir los procesadores ARM de doble núcleo modestos, logrando ejecutar de forma fluida juegos de consolas de 8 y 16 bits avanzados, Arcade y PlayStation 1 utilizando núcleos dedicados de RetroArch optimizados para el consumo mínimo de memoria caché.

## Dispositivos aplicables

- Miyoo Mini (v1, v2, v3, v4)
- Miyoo Mini Plus (Miyoo Mini +)
- Anbernic RG35XX original (variante base, según `docs/software.md`)
- Nota: existen adaptaciones comunitarias de la rama principal de Koriki para consolas de chasis vertical y horizontal basadas en el procesador SigmaStar SSD202D.
- Variante **Koriki ED**: adaptación de Koriki a la familia H700, compatible con Anbernic RG35XX Plus, RG35XXH, RG28XX y RG34XX (según `docs/software.md`).

## Tipo de instalación

Extracción a SD existente. No requiere el flasheo tradicional de imágenes `.img` ni la destrucción de particiones. La instalación se realiza preparando la tarjeta MicroSD e introduciendo un conjunto de archivos comprimidos directamente en la raíz, conviviendo de forma nativa con el cargador de arranque (bootloader) de la consola.

## Requisitos previos

- Tarjeta MicroSD de primera marca: se recomienda 32GB, 64GB o 128GB (SanDisk Ultra o Samsung EVO).
- Nota de estabilidad: la controladora de lectura de la Miyoo Mini es propensa a corromper datos si la tarjeta es genérica o si se extrae mientras la consola escribe archivos de guardado rápido.
- Formateador de almacenamiento: herramientas como GUIFormat (Windows) o utilidades de particionado nativas en WSL/Linux para asegurar un sistema de archivos compatible.
- Descompresor de archivos: 7-Zip o `unzip` en la terminal de WSL.

## Descarga

- Repositorio oficial de la escena: los paquetes de instalación consolidados se descargan directamente desde el repositorio principal de desarrollo — <https://github.com/Rparadise-Team/Koriki/releases>
- Nota técnica: descargar el archivo ejecutable o comprimido que corresponda exactamente al modelo de la pantalla (el modelo Plus y el clásico tienen resoluciones y controladores de panel diferentes, ej. `Koriki-MiyooMiniPlus-vX.X.X.zip`).

## Preparación de almacenamiento

- **SD de juegos y sistema (única)**: la tarjeta MicroSD debe estar formateada obligatoriamente en FAT32 con un tamaño de clúster de 32 KB o 64 KB para optimizar los tiempos de acceso de lectura del kernel de Koriki.
- Integración con pipeline propio: el paquete comprimido de Koriki ya incluye la raíz de los directorios del sistema de archivos. Las ROMs se organizan dentro de una carpeta principal en la raíz llamada `/Roms/`. Hay que mapear los volcados respetando estrictamente los nombres de carpetas estándares del CFW, tales como `/Roms/FC/` (NES), `/Roms/SFC/` (SNES), `/Roms/MD/` (Mega Drive), `/Roms/GBA/` y `/Roms/PS/`.

## Instalación

1. Inserta la MicroSD en el ordenador y asegúrate de que esté formateada correctamente en FAT32.
2. Descomprime el archivo `.zip` de Koriki descargado.
3. Copia todo el contenido extraído (las carpetas `Bios`, `Emu`, `Roms`, `Themes`, y los archivos de arranque del sistema) directamente en la raíz de la tarjeta MicroSD. No dejes los archivos dentro de carpetas secundarias.

## Primer arranque

1. Inserta la MicroSD con los archivos en la ranura de la Miyoo Mini / Mini Plus.
2. Enciende la consola. El cargador de arranque de Miyoo detecta los archivos de Koriki e inicia un script automático de carga (se muestra el logotipo personalizado del CFW en pantalla).
3. El sistema inicializa los archivos de RetroArch de forma transparente y carga directamente la interfaz fluida de SimpleMenu. Al ser una instalación por extracción directa, la tarjeta conserva su tamaño físico original al instante sin requerir redimensionamientos extras.

## Configuración post-instalación

- **Volcado de datos optimizado**: transfiere las colecciones de juegos en las subcarpetas dentro de `/Roms/`. Es un requisito crítico copiar los archivos de BIOS obligatorios en la carpeta centralizada `/Bios/` en la raíz de la tarjeta para habilitar el arranque de núcleos avanzados (como PS1 o GBA).
- **Tratamiento de carátulas (previews)**: al utilizar SimpleMenu como frontend principal, la interfaz busca imágenes estáticas en formato `.png` guardadas estrictamente dentro de una subcarpeta `.previews` dentro de la carpeta de cada consola (ej. `/Roms/SFC/.previews/`). Los nombres de las carátulas deben coincidir byte por byte con el nombre de la ROM.
- Ventaja de pipeline propio: dado que SimpleMenu lee metadatos por correspondencia de nombres planos, no requiere indexadores XML pesados, lo que agiliza la inyección masiva de portadas directamente desde el ordenador.

## Notas

- **Tratamiento de ROMsets Arcade**: los núcleos de RetroArch en Koriki para la Miyoo Mini rinden al máximo utilizando el conjunto MAME 2003-Plus (romset `mame2003-plus` / versión 0.78-plus) para arcade general, y FinalBurn Neo (formato Non-Merged) para las placas de Capcom y Neo-Geo. Hay que procesar los DATs exactos de estas dos variantes para evitar bloqueos del sistema o fallos de asignación de memoria RAM (la consola cuenta con solo 128MB de RAM).
- **Optimización del formato de consolas en disco**: al igual que en la mayoría de firmwares ligeros, el formato comprimido CHD (v5) es el estándar obligatorio para juegos de PS1 y Sega CD en Koriki. Realizar la conversión masiva a CHD ahorra hasta un 40% de espacio en la MicroSD y alivia el bus de lectura de la consola, eliminando la ralentización al cargar pistas de audio de pistas múltiples.
- **Gestión 1G1R y rendimiento del menú**: aunque SimpleMenu es un frontend sumamente ágil, las listas kilométricas de más de 2000 juegos por carpeta saturan la memoria caché del sistema en la Miyoo Mini. Es altamente recomendable aplicar un filtro 1G1R estricto (con herramientas como retool) para limitar los subsets a un máximo de 300 títulos esenciales por sistema, garantizando un scroll fluido a 60 FPS sin tirones visuales al buscar los juegos.
- **Comunidad de referencia (Brothers of Metal)**: para este ecosistema, la comunidad hispana Brothers of Metal (BoM) es un referente absoluto en la curación de contenidos. Sus packs y compilaciones comunitarias son muy valorados porque incluyen romsets ya organizados con la estructura de carpetas nativa, portadas pre-reescaladas a las dimensiones de la pantalla y una cuidada selección de traducciones al castellano y hacks listos para jugar.
