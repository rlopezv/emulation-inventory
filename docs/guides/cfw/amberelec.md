# AmberELEC

AmberELEC (anteriormente conocido como 351ELEC) es un Custom Firmware (CFW) de código abierto y alto rendimiento basado en Linux (EmuELEC/JeOS) para consolas portátiles con procesadores Rockchip de 64 bits. Utiliza EmulationStation como frontend y está profundamente optimizado para exprimir al máximo la aceleración por hardware del chip, ofreciendo integración con RetroArch, juego en red (Netplay), logros (RetroAchievements) y escalado de vídeo a nivel de píxel perfecto.

## Dispositivos aplicables

- Anbernic RG351 (P, M, V, MP)
- Anbernic RG552 (soporte oficial a través de compilaciones específicas de 64 bits)
- Anbernic RG353 (P, V, M) — nota: solo las variantes compatibles con chips RK3566 en compilaciones de la comunidad

## Tipo de instalación

Imagen flasheada a SD (`.img.gz`) que destruye las particiones previas. Admite configuración de una sola tarjeta (sistema + ROMs) o de doble tarjeta (SD1 sistema, SD2 ROMs).

## Requisitos previos

- Tarjeta MicroSD de alta velocidad: 16GB/32GB para el sistema (SD1) y opcionalmente 64GB a 512GB para almacenamiento de juegos (SD2).
- Software de flasheo: BalenaEtcher, Rufus, o `dd` en WSL/Linux.
- Formateador de almacenamiento: herramientas como GUIFormat (para asegurar formato FAT32/exFAT en Windows) si se prepara la SD2 manualmente.

## Descarga

- Repositorio oficial: imágenes estables de lanzamiento (`.img.gz`) correspondientes al modelo exacto del dispositivo — <https://github.com/AmberELEC/AmberELEC/releases>
- Nota técnica: descargar el archivo correcto para la arquitectura (ej. `AmberELEC-RG351P.img.gz` para pantallas 3:2 o `AmberELEC-RG351V.img.gz` para pantallas 4:3).

## Preparación de almacenamiento

A diferencia de OpenDingux (Adam Image), AmberELEC cuenta con soporte avanzado para múltiples sistemas de archivos modernos en la tarjeta de juegos (SD2):

- **SD1 (Sistema)**: no requiere preparación previa; el flasheo reestructura la tarjeta con una partición de arranque EMUELEC (FAT32) y una partición de almacenamiento del sistema (EXT4).
- **SD2 (ROMs — ranura TF2)**: se recomienda formatear en exFAT o ext4 (si se usa Linux nativo) para admitir archivos de gran tamaño (superiores a 4GB, vital para juegos de PSP, Dreamcast o PS2).
- Integración con pipeline propio: no es necesario crear las carpetas a mano; un script puede pre-cargar la SD2 con la estructura oficial de carpetas de AmberELEC antes del primer arranque, instalando los archivos de configuración base.

## Instalación

1. Conecta la SD1 al PC.
2. Usa la herramienta de flasheo para escribir el archivo `.img.gz` descargado directamente en la tarjeta (no es necesario descomprimirlo si se usa BalenaEtcher).
3. Una vez finalizado el flasheo, extrae la tarjeta de forma segura.

## Primer arranque

1. Introduce la SD1 en la ranura TF1 de la consola.
2. (Opcional) Si se usa configuración de doble tarjeta, introduce la SD2 completamente vacía en la ranura TF2.
3. Enciende la consola. AmberELEC ejecuta un script automatizado que expande la partición de almacenamiento, crea el sistema de archivos del usuario y genera todo el árbol oficial de carpetas de ROMs en la SD2 automáticamente. La consola se reinicia al finalizar.

## Configuración post-instalación

- **Volcado de ROMsets y BIOS**: copia las colecciones de juegos en las carpetas generadas (ej. `/roms/snes/`, `/roms/psx/`). Es obligatorio añadir las BIOS del sistema en `/roms/bios/` para que funcionen plataformas como PS1, Dreamcast, GBA y sistemas Arcade.
- **Metadatos y raspado (scraping)**: EmulationStation lee los metadatos a través de `gamelist.xml`, ubicado dentro de la carpeta de cada sistema. Las carátulas y vídeos se almacenan por defecto en `/roms/[sistema]/images/` y `/roms/[sistema]/videos/`.
- Ventaja de pipeline propio: es posible generar `gamelist.xml` a partir de DATs propios estructurados, enlazando imágenes locales sin depender del raspador interno por Wi-Fi de la consola, mucho más lento.

## Notas

- **Tratamiento de ROMsets Arcade**: a diferencia de Adam Image, los núcleos de RetroArch en AmberELEC son mucho más modernos. Usa por defecto FinalBurn Neo (FBNeo v1.0.0.3 o superior) en formato Non-Merged para CPS1, CPS2, CPS3 y Neo-Geo. Para MAME, el estándar óptimo de rendimiento en estos chips es MAME 2003-Plus (romset `mame2003-plus`) o MAME 2010 (0.139). Es crítico usar los DATs exactos de estas versiones para evitar pantallas en negro.
- **Ecosistema de consolas en disco**: al contar con núcleos actualizados de DuckStation y Flycast, AmberELEC soporta los formatos de compresión más eficientes de la comunidad de preservación: CHD (v5) para PS1, Sega CD, Saturn y Dreamcast, y CSO para PSP.
- **Soporte 1G1R**: procesar los sets con herramientas como retool antes de transferirlos a la SD2 limpia el menú de EmulationStation de clones molestos, mejorando drásticamente el tiempo de carga del frontend al arrancar la consola.
