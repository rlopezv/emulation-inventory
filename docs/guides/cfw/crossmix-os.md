# CrossMix-OS

CrossMix-OS es un Custom Firmware (CFW) y una suite de optimización masiva de código abierto diseñada para consolas portátiles basadas en el procesador Allwinner A133P. A diferencia de los CFW tradicionales, no reemplaza el kernel de fábrica, sino que reconstruye y mejora por completo el entorno de usuario sobre el sistema original. Utiliza una interfaz personalizada fluida y destaca por incluir emuladores actualizados con soporte avanzado para RetroArch de 64 bits, optimizaciones de rendimiento independientes (como standalone PPSSPP), gestión automatizada de herramientas de sistema y soporte nativo para carátulas animadas y metadatos dinámicos.

## Dispositivos aplicables

- TrimUI Smart Pro (consola portátil horizontal con pantalla de 4.96 pulgadas)
- TrimUI Brick (variante vertical de la misma arquitectura de hardware)

## Tipo de instalación

Extracción a SD existente. No requiere flasheo ni destrucción de particiones: se formatea la tarjeta MicroSD y se introduce directamente un paquete de archivos comprimidos (`.zip`) que el sistema lee e inicializa de forma nativa al encender la consola.

## Requisitos previos

- Tarjeta MicroSD de alto rendimiento: se recomienda 64GB, 128GB o 256GB (SanDisk Ultra/Extreme o Samsung EVO Select). El procesador Allwinner A133P maneja de forma óptima tarjetas de gran capacidad.
- Formateador de almacenamiento: herramientas como GUIFormat (Windows) o los comandos de particionado nativos en WSL/Linux para asegurar un sistema de archivos compatible.
- Descompresor de archivos: 7-Zip, WinRAR o `unzip` en la terminal de Linux.

## Descarga

- Repositorio oficial: los paquetes de instalación consolidados se descargan directamente desde el repositorio principal de desarrollo — <https://github.com/cizia64/CrossMix-OS>
- Nota técnica: descargar siempre el archivo comprimido completo de la última versión estable (ej. `CrossMix-OS-vX.X.X.zip`). No requiere descargas de parches de kernel independientes para la TrimUI Smart Pro.

## Preparación de almacenamiento

- **SD de juegos y sistema (única)**: CrossMix-OS exige que la tarjeta esté formateada obligatoriamente en FAT32 (para máxima compatibilidad de scripts) o en exFAT (muy recomendado por su soporte para archivos de más de 4GB en sistemas como PSP o Dreamcast).
- Integración con pipeline propio: el paquete `.zip` ya viene con la estructura base de carpetas de emuladores creada dentro de un directorio raíz llamado `/Roms/`. Es posible volcar directamente las colecciones respetando nombres de directorios modernos y estándar como `/Roms/FC/` (NES), `/Roms/SFC/` (SNES), `/Roms/MD/` (Mega Drive), `/Roms/PS/` (PlayStation 1) o `/Roms/PSP/`.

## Instalación

1. Inserta la MicroSD en el ordenador y asegúrate de que esté formateada en FAT32 o exFAT.
2. Descomprime el archivo `.zip` de CrossMix-OS descargado.
3. Copia todo el contenido extraído (las carpetas `Emus`, `Roms`, `Themes`, `Apps`, etc.) directamente en la raíz de la tarjeta MicroSD. Asegúrate de que estas carpetas queden en la raíz del almacenamiento y no dentro de una subcarpeta contenedora.

## Primer arranque

1. Inserta la MicroSD con los archivos extraídos en la ranura única de la consola TrimUI.
2. Enciende el dispositivo. CrossMix-OS detecta la nueva estructura e inicia un script automático de configuración en pantalla (aparece el logotipo animado del CFW). El sistema carga todos los módulos de RetroArch y optimiza el frontend.
3. Una vez finalizado, la consola muestra el menú principal renovado con todos los sistemas disponibles. No requiere reinicios manuales ni herramientas de particionado externas, ya que la tarjeta conserva su tamaño físico original.

## Configuración post-instalación

- **Volcado masivo de ROMsets**: copia los conjuntos de juegos validados en las subcarpetas dentro de `/Roms/`. Es fundamental añadir los archivos de BIOS obligatorios en la ruta centralizada `/Roms/BIOS/` para garantizar la compatibilidad de núcleos como PS1, Saturn o GBA.
- **Indexación de metadatos**: el sistema TrimUI utiliza `gamelist.xml` situado en la raíz de cada carpeta de ROMs. Las carátulas oficiales (imágenes estáticas o animadas) deben guardarse estrictamente en `/Roms/[Sistema]/Imgs/`.
- Ventaja de pipeline propio: es posible generar `gamelist.xml` de forma automática combinando la información de DATs propios y asignando las rutas locales de imágenes descargadas, evitando usar el raspador Wi-Fi interno de la consola.

## Notas

- **Tratamiento de ROMsets Arcade modernos**: gracias a la solvencia del procesador A133P, CrossMix-OS ejecuta núcleos modernos y actualizados. El estándar recomendado por la comunidad para sistemas de placas recreativas (CPS1, CPS2, CPS3 y Neo-Geo) es FinalBurn Neo (romset en formato Non-Merged). Para juegos arcade generales, implementa núcleos eficientes como MAME 2003-Plus (romset `0.78-plus`). Es necesario procesar las colecciones con los archivos DAT exactos de estas versiones para evitar pantallas en negro.
- **Optimización del formato de almacenamiento**: debido a la gran pantalla de la TrimUI Smart Pro, los sistemas basados en discos ópticos son muy demandados. CrossMix-OS ofrece soporte nativo total para el formato comprimido CHD (v5) en emuladores de PS1, Saturn, Dreamcast, Sega CD y PC-FX. Se recomienda automatizar la conversión masiva a CHD, descartando archivos `.bin`/`.cue` sueltos, para agilizar la lectura en el bus SD y ahorrar hasta un 40% de espacio. Para PlayStation 2 y PSP, usar el formato CSO optimizado.
- **Gestión 1G1R y rendimiento del frontend**: aunque el frontend de TrimUI es ligero, cargar carpetas con más de 2000-3000 archivos de golpe puede provocar pequeños tirones (stuttering) visuales al hacer scroll rápido por las listas de juegos. Pasar los conjuntos de ROMs por un filtro 1G1R inteligente (como retool) para seleccionar únicamente los títulos esenciales e idiomas preferidos (ej. España/Europa) optimiza los tiempos de indexación y ofrece una navegación limpia y fluida.
