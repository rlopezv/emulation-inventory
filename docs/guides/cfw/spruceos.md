# spruceOS

spruceOS es un Custom Firmware (CFW) y una suite de optimización masiva de código abierto diseñada para reemplazar el sistema operativo deficiente de fábrica en las consolas portátiles ultra-compactas de Miyoo. Técnicamente, no sobreescribe el gestor de arranque (bootloader) interno, sino que reconstruye por completo el entorno de usuario sobre el sistema operativo Linux subyacente. Utiliza una interfaz minimalista de alto rendimiento basada en listas y destaca por incluir núcleos de RetroArch actualizados y optimizados para hardware de bajos recursos, habilitando funciones avanzadas como el guardado automático instantáneo, juego en red (Netplay) y una gestión fluida de carátulas sin ralentizar el bus de datos de la tarjeta.

## Dispositivos aplicables

- Miyoo A30 (consola micro-horizontal con joysticks analógicos y pantalla de 2.8 pulgadas)
- Miyoo Flip
- Miyoo Mini Flip
- TrimUI Brick
- TrimUI Smart Pro

(Miyoo Flip, Miyoo Mini Flip y la familia TrimUI según `docs/software.md`; no descritos en la información aportada.)

## Tipo de instalación

Extracción a SD existente. No requiere flasheo tradicional de imágenes `.img` ni destruye las particiones físicas de la tarjeta. La instalación se realiza preparando el almacenamiento e introduciendo directamente una estructura de archivos comprimidos en la raíz, que el cargador de la consola lee e inicializa nativamente al encender el dispositivo.

## Requisitos previos

- Tarjeta MicroSD de primera marca: se recomienda 32GB, 64GB o como máximo 128GB (SanDisk Ultra o Samsung EVO).
- Nota de estabilidad: la Miyoo A30 es sumamente sensible a las tarjetas de memoria genéricas o de mala calidad, las cuales provocan fallos de arranque (bootloops) y corrupción de guardados rápidos.
- Formateador de almacenamiento: herramientas como GUIFormat (Windows) o utilidades de particionado nativas en WSL/Linux para asegurar un sistema de archivos compatible.
- Descompresor de archivos: 7-Zip, WinRAR o `unzip` en la terminal de WSL.

## Descarga

- Repositorio oficial de la escena: los paquetes de instalación consolidados se descargan de forma centralizada desde el repositorio de desarrollo en GitHub, liderado de forma muy activa por la comunidad — <https://github.com/spruceUI/spruceOS/releases>
- Nota técnica: descargar siempre el archivo comprimido `.zip` completo de la última versión estable (ej. `spruce-vX.X.X.zip`). No requiere archivos ni parches de kernel independientes.

## Preparación de almacenamiento

- **SD de juegos y sistema (única)**: la tarjeta MicroSD debe estar formateada obligatoriamente en FAT32 con un tamaño de clúster de 32 KB para optimizar los tiempos de acceso de lectura de los emuladores nativos.
- **Estructura de carpetas**: el paquete de spruceOS ya incluye la raíz con los directorios necesarios. Las ROMs se organizan dentro de una carpeta principal llamada `/Roms/`. Hay que mapear los volcados respetando estrictamente las abreviaturas estándar de las carpetas del CFW, tales como `/Roms/FC/` (NES), `/Roms/SFC/` (SNES), `/Roms/MD/` (Mega Drive), `/Roms/GBA/` y `/Roms/PS/`.

## Instalación

1. Inserta la MicroSD en el ordenador y asegúrate de que esté formateada correctamente en FAT32 (32 KB).
2. Descomprime el archivo `.zip` de spruceOS descargado.
3. Copia todo el contenido extraído (las carpetas `Apps`, `Bios`, `Emu`, `Roms`, `Themes`, etc.) directamente en la raíz de la tarjeta MicroSD. Asegúrate de que queden en la raíz del almacenamiento y no dentro de una subcarpeta contenedora.

## Primer arranque

1. Inserta la MicroSD con los archivos en la ranura de la Miyoo A30.
2. Enciende la consola. El sistema operativo detecta los archivos de spruceOS e inicia un script automático de inicialización y carga (se muestra el logotipo personalizado del CFW en pantalla).
3. El sistema configura los entornos de RetroArch de forma transparente y carga directamente la interfaz principal en segundos. Al ser una instalación por extracción directa, la tarjeta conserva su tamaño físico original al instante sin requerir particionados adicionales.

## Configuración post-instalación

- **Volcado de datos**: transfiere las colecciones de juegos en las subcarpetas correspondientes dentro de `/Roms/`. Es fundamental copiar los archivos de BIOS obligatorios en la carpeta centralizada `/Bios/` en la raíz de la tarjeta para garantizar el arranque de sistemas avanzados (como PS1 o GBA).
- **Tratamiento de carátulas (Imgs)**: el frontend de spruceOS no utiliza archivos XML indexadores planos (`gamelist.xml`). Lee las carátulas por correspondencia directa de nombres planos en formato `.png` ubicadas estrictamente dentro de una subcarpeta llamada `Imgs` (con la primera letra en mayúscula) dentro de la carpeta de cada consola (ej. `/Roms/SFC/Imgs/`). El archivo de imagen debe llamarse exactamente igual que la ROM.
- Ventaja de pipeline propio: es posible automatizar esta inyección masiva creando los directorios correspondientes según el nombre de la carpeta del sistema. Dado que la pantalla de la A30 es pequeña, reescalar las imágenes de carátulas de forma masiva a un ancho máximo de 640x480 o 320x240 píxeles agiliza la navegación.

## Notas

- **Tratamiento de ROMsets Arcade eficientes**: debido a la potencia medida del procesador Allwinner A33, spruceOS rinde de forma óptima utilizando el conjunto MAME 2003-Plus (romset `mame2003-plus` / versión 0.78-plus) para arcade general, y núcleos ajustados de FinalBurn Neo en formato Non-Merged para las placas de Capcom y Neo-Geo. Hay que procesar los DATs exactos de estas versiones para evitar cuelgues del backend o pantallas en negro.
- **Optimización del formato de consolas en disco**: el formato comprimido CHD (v5) es el estándar recomendado para juegos de PS1 y Sega CD en spruceOS. Es necesario realizar la conversión masiva a CHD, descartando los archivos `.bin`/`.cue` sueltos, para reducir el peso a la mitad, estabilizar los fotogramas por segundo y evitar la degradación de bloques de la MicroSD debido a la lectura constante de datos musicales en múltiples pistas.
- **Gestión 1G1R de la interfaz**: aunque el frontend de spruceOS es sumamente ágil, tener carpetas saturadas con más de 1500 archivos puede provocar ralentizaciones o pequeños tirones (stuttering) visuales al hacer scroll rápido por las listas de juegos, ya que el sistema escanea los directorios físicos en tiempo real. Aplicar un filtro 1G1R estricto (con herramientas como retool) para dejar subsets limpios de títulos esenciales garantiza una navegación fluida a 60 FPS estables.
