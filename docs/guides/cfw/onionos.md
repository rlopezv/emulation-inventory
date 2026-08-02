# OnionOS

OnionOS es un Custom Firmware (CFW) de código abierto y rendimiento extremo que actúa como una capa de optimización masiva sobre el sistema operativo Linux subyacente de Miyoo. Destaca en la escena de la emulación por su velocidad y por incorporar características revolucionarias como el Game Switcher (un selector que permite alternar instantáneamente entre juegos guardando y cargando el estado en frío en menos de dos segundos), modos de suspensión profunda con consumo cero de batería, y una suite de emuladores nativos basados en núcleos de RetroArch altamente optimizados para maximizar la memoria RAM del dispositivo.

## Dispositivos aplicables

- Miyoo Mini (v1, v2, v3, v4)
- Miyoo Mini Plus (Miyoo Mini +)

## Tipo de instalación

Extracción a SD existente. No requiere el flasheo de imágenes `.img` ni destruye particiones. La instalación se realiza formateando la tarjeta MicroSD e introduciendo directamente una estructura de carpetas comprimidas que el cargador de arranque de la consola lee e inicializa de forma nativa.

## Requisitos previos

- Tarjeta MicroSD de primera marca: se recomienda 32GB, 64GB o 128GB (SanDisk Ultra o Samsung EVO).
- Nota de estabilidad: OnionOS realiza lecturas y escrituras constantes en la SD debido a sus sistemas de guardado automático instantáneo; usar tarjetas genéricas provoca corrupción irreversible de datos.
- Formateador de almacenamiento: herramientas como GUIFormat (Windows) para asegurar el sistema de archivos FAT32.
- Descompresor de archivos: 7-Zip o `unzip` en la terminal de WSL.

## Descarga

- Repositorio oficial: los paquetes consolidados de instalación se descargan directamente desde el sitio oficial del proyecto — <https://onionui.github.io/>
- Nota técnica: descargar siempre el archivo completo para instalaciones limpias (ej. `Onion-vX.X.X.zip`). El mismo archivo es universal y sirve tanto para el modelo clásico como para el modelo Plus.

## Preparación de almacenamiento

El esquema de almacenamiento de OnionOS es riguroso respecto a la nomenclatura y el formato físico:

- **SD de juegos y sistema (única)**: debe estar formateada obligatoriamente en FAT32 con un tamaño de clúster de 32 KB (para tarjetas de hasta 64GB) o 64 KB (para tarjetas de 128GB) para optimizar la velocidad de carga del Game Switcher.
- **Nomenclatura estricta de carpetas (muy crítica)**: OnionOS organiza las ROMs dentro de una carpeta principal en la raíz llamada `/Roms/`. Utiliza nombres descriptivos y estrictamente en MAYÚSCULAS para las subcarpetas de las consolas. Hay que mapear los volcados hacia rutas exactas como `/Roms/FC/` (NES), `/Roms/SFC/` (SNES), `/Roms/MD/` (Mega Drive), `/Roms/GBA/` o `/Roms/PS/` (PlayStation 1). Si la carpeta se escribe en minúsculas, el sistema la ignora.

## Instalación

1. Inserta la MicroSD en el ordenador y asegúrate de que esté formateada en FAT32 con el tamaño de clúster correcto.
2. Descomprime el archivo `.zip` de OnionOS descargado.
3. Copia todos los archivos y carpetas ocultas extraídos (como `.tmp_update`, `Bios`, `Emu`, `Roms`, `Themes`, etc.) directamente en la raíz de la tarjeta MicroSD.

## Primer arranque

1. Inserta la MicroSD con los archivos en la Miyoo Mini / Mini Plus.
2. Enciende la consola. OnionOS detecta los archivos de instalación e inicia un asistente visual automático en pantalla (el instalador de Onion).
3. Selecciona los sistemas y emuladores a activar utilizando la cruceta de la consola y presiona Start para confirmar. El sistema compila las rutas en segundos y carga la interfaz principal de OnionOS. La tarjeta conserva su espacio físico original al instante.

## Configuración post-instalación

- **Volcado de datos**: transfiere las colecciones de juegos en las subcarpetas en mayúsculas dentro de `/Roms/`. Es obligatorio copiar los archivos de BIOS que lo requieran dentro de la carpeta centralizada `/Bios/` en la raíz de la tarjeta para permitir el arranque de núcleos avanzados.
- **Tratamiento de carátulas (Imgs)**: OnionOS no lee archivos XML indexadores planos (`gamelist.xml`). Lee las carátulas por correspondencia directa de nombres planos en formato `.png` ubicadas estrictamente dentro de una subcarpeta llamada `Imgs` (con la primera letra en mayúscula) dentro de la carpeta de cada consola (ej. `/Roms/SFC/Imgs/`). El archivo de imagen debe llamarse exactamente igual que la ROM.
- **Acción de pipeline propio (optimización de tamaño)**: la pantalla de la Miyoo Mini tiene una resolución física de 640x480 píxeles. Hay que procesar las imágenes multimedia reescalándolas de forma masiva a un ancho máximo estricto de 256 píxeles (manteniendo la relación de aspecto) y guardarlas en formato PNG de 8 bits (indexado). Esto ahorra megabytes críticos y garantiza un scroll ultra-fluido a 60 FPS en el menú de carátulas de Onion.

## Notas

- **Tratamiento de ROMsets Arcade eficientes**: al contar con solo 128MB de RAM, los emuladores arcade nativos están ajustados al límite. El estándar absoluto recomendado para arcade general es MAME 2003-Plus (romset `0.78-plus`). Para sistemas CPS1, CPS2, CPS3 y Neo-Geo, usa FinalBurn Neo (romset en formato Non-Merged). Hay que procesar los DATs exactos de estas dos variantes e incluir la BIOS `neogeo.zip` correcta para evitar cuelgues del sistema.
- **Optimización del formato de PlayStation 1**: OnionOS ejecuta PS1 de forma perfecta mediante el núcleo optimizado PCSX-ReARMed. Para maximizar el rendimiento y el espacio, es directriz mandatoria realizar la conversión masiva de las ISOs/BIN al formato comprimido CHD (v5). OnionOS gestiona los CHDs de forma nativa, lo que reduce el peso a la mitad y alivia el bus de lectura de la MicroSD al cargar pistas de audio integradas.
- **Gestión 1G1R de la interfaz**: dado que OnionOS escanea los directorios físicos en tiempo real al abrir una carpeta, tener directorios con más de 1000 archivos provoca un pequeño retraso (lag) de un par de segundos al entrar al sistema. Aplicar un filtro 1G1R estricto (con herramientas como retool) para dejar subsets limpios de títulos esenciales garantiza una respuesta instantánea de la interfaz y un menú impecable.
