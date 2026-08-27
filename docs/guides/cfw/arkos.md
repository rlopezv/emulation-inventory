# ArkOS

ArkOS (Another Retro Kernel Operating System) es un Custom Firmware (CFW) de 64 bits altamente flexible y de rendimiento extremo basado en una distribución ligera de Ubuntu/Debian Linux. Utiliza una versión optimizada de EmulationStation como frontend y destaca en la comunidad por dar un acceso casi total al sistema operativo subyacente. Permite alternar entre emuladores nativos independientes (como standalone RetroArch o versiones optimizadas de PPSSPP) para exprimir cada fotograma por segundo en sistemas complejos como PSP, Dreamcast y Nintendo 64.

## Dispositivos aplicables

- Anbernic RG351 (P, M, V, MP)
- Anbernic RG353 (P, V, M, VS)
- Powkiddy (RGB10Max3, RGB20S, RK2023)
- R36S / R35S y otros clones basados en el chip Rockchip RK3326/RK3566

## Tipo de instalación

Imagen flasheada a SD (`.img`) que destruye las particiones previas. Permite configurar una única tarjeta (sistema + ROMs) o habilitar una configuración avanzada de doble tarjeta (SD1 sistema, SD2 ROMs) mediante los scripts de su panel de control.

## Requisitos previos

- Tarjetas MicroSD compatibles: una de 16GB o 32GB de calidad para el sistema (SD1); una de 64GB a 512GB de alta velocidad para juegos (SD2).
- Nota crítica: el kernel de ArkOS es extremadamente sensible a las tarjetas MicroSD falsas o de baja calidad, provocando corrupción del sistema de archivos al apagar la consola.
- Software de flasheo: Rufus (muy recomendado para Windows), BalenaEtcher o `dd` en WSL/Linux.
- Acceso a Internet (opcional pero recomendado): conexión Wi-Fi en la consola para actualizar scripts del sistema.

## Descarga

- Repositorio oficial: <https://github.com/christianhaitian/arkos/releases>
- ArkOS no centraliza todo en GitHub Releases; su distribución oficial se gestiona también a través de enlaces directos estructurados por dispositivo en su Wiki oficial — [TODO: URL de la wiki].
- Nota técnica: descargar la variante exacta para el chip. Una imagen de RG351P no funcionará en una RG351V debido a la configuración de los controladores del panel de la pantalla.
- **Clones no oficiales (kernel porting)**: `github.com/lcdyk0517/arkos4clone` — herramientas de porting de kernel para ejecutar ArkOS/dArkOS en dispositivos clon basados en RK3326 sin soporte oficial (scripts de build, herramienta de análisis de DTB, mapeo de botones/pantalla). Repositorio hermano para fixes de compatibilidad de juegos por separado. **El mecanismo de instalación es distinto al flujo estándar de este documento** — si en el futuro se aborda un dispositivo concreto que lo necesite, requiere su propia guía, no encaja como nota dentro de esta.

## Preparación de almacenamiento

ArkOS es compatible con una enorme variedad de sistemas de archivos debido a su base Ubuntu:

- **SD1 (Sistema)**: el software de flasheo crea automáticamente tres particiones: BOOT (FAT32), rootfs (EXT4, el núcleo de Linux) y una partición temporal de almacenamiento.
- **SD2 (ROMs — ranura TF2)**: se recomienda formatear en exFAT de forma nativa para mantener compatibilidad plug-and-play con entornos Windows/WSL.
- Integración con pipeline propio: al igual que con AmberELEC, no es obligatorio crear las carpetas a mano. Sin embargo, ArkOS utiliza nombres de carpetas ligeramente diferentes para ciertos sistemas (ej. `mastersystem` en lugar de `ms`, o `megadrive` en lugar de `genesis`); un script debe mapear estas rutas antes de volcar las ROMs.

## Instalación

1. Inserta la SD1 en el ordenador.
2. Abre la herramienta de flasheo (ej. Rufus). Selecciona el archivo `.img` descomprimido de ArkOS.
3. Desactiva cualquier opción de formateo automático adicional y haz clic en Empezar/Escribir.
4. Una vez finalizado, extrae la tarjeta.

## Primer arranque

1. Introduce la SD1 en la ranura TF1.
2. Deja la ranura TF2 (SD2) completamente vacía en este paso.
3. Enciende la consola. ArkOS expande el sistema operativo automáticamente en la SD1 y crea una carpeta de juegos por defecto en ella. El proceso tarda unos minutos y la consola se reinicia sola.
4. Una vez cargue la interfaz, ve a `Options -> Advanced -> Switch to SD2 for ROMs` (si se va a usar doble tarjeta). El sistema se apaga.
5. Inserta la SD2 formateada en exFAT en la ranura TF2 y vuelve a encender la consola. ArkOS detecta la tarjeta y puebla la SD2 con toda la estructura oficial de directorios en segundos.

## Configuración post-instalación

- **Volcado de datos**: transfiere los ROMsets curados a las carpetas generadas en la SD2. Las BIOS de los sistemas deben ir en la carpeta raíz `/roms/bios/`.
- **Metadatos de EmulationStation**: usa la misma estructura estricta del archivo indexador `gamelist.xml` en la raíz de la carpeta de cada consola. Las rutas por defecto para multimedia que lee ArkOS son `/roms/[sistema]/images/` para carátulas y `/roms/[sistema]/videos/` para vídeos.
- Ventaja de pipeline propio: es posible automatizar la creación de `gamelist.xml` inyectando directamente los metadatos de año, género y número de jugadores extraídos de listados propios transformados, evitando raspar los juegos en la propia consola.

## Notas

- **Tratamiento de ROMsets Arcade**: ArkOS es sumamente flexible con el Arcade. Soporta MAME 2003-Plus (romset `0.78-plus`) para un rendimiento equilibrado en chips económicos, y núcleos modernos de FinalBurn Neo en formato Non-Merged. Lo ideal es generar los dos subsets independientes utilizando sus respectivos archivos DAT oficiales.
- **Formatos avanzados de consolas**: ArkOS incluye soporte nativo y optimizado para CHD (v5) en todos los sistemas de disco de 8, 16, 32 y 64 bits (incluyendo los núcleos de Panasonic 3DO, Amiga CD32 y PC-FX). Para juegos de Nintendo GameCube/Wii (en dispositivos como la RG353M), maneja perfectamente el formato RVZ.
- **Apagado seguro**: al estar basado en Ubuntu Linux, nunca apagar la consola manteniendo pulsado el botón físico de Power (salvo congelamiento total). Hazlo siempre desde el menú de EmulationStation (`Start -> Quit -> Shutdown System`) para evitar que el script corrompa la base de datos de juegos o las tablas de `gamelist.xml`.
