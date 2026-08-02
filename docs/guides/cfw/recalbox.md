# Recalbox

Recalbox es un sistema operativo y Custom Firmware (CFW) de código abierto, distribución limpia y rendimiento optimizado basado en Linux (Buildroot). Está diseñado específicamente para transformar placas de computación reducida, mini-PCs y ordenadores antiguos en estaciones de emulación y centros multimedia listos para usar (out-of-the-box). Utiliza una versión personalizada y muy fluida de EmulationStation como frontend principal y destaca por incluir controladores Bluetooth optimizados para mandos modernos de PS4/PS5/Xbox, modos de rebobinado automático (Rewind), soporte integrado para Kodi Media Center y el exclusivo sistema Recalbox RGB Dual para salida nativa en monitores CRT.

## Dispositivos aplicables

- Raspberry Pi (modelos 5, 4B, 400, 3B/3B+, Zero 2 W)
- Ordenadores de arquitectura x86_64 (Mini PCs, PCs de sobremesa de 64 bits)
- Dispositivos portátiles (Anbernic RG351P/M/V, Odroid Go Advance/Super)

Esta guía se centra en la instalación en Raspberry Pi 5 (4GB) (dispositivo del inventario en `docs/devices.md`).

## Tipo de instalación

Imagen flasheada a SD / unidad NVMe / USB (`.img.xz`). Instalación limpia de fábrica escribiendo directamente en una tarjeta MicroSD, un pendrive USB o un disco SSD/NVMe conectado por el bus PCIe de la Raspberry Pi 5. El flasheo inicial elimina todas las particiones del soporte elegido.

## Requisitos previos

- Tarjeta MicroSD o unidad SSD de primera marca: mínimo 64GB, 128GB o 256GB (SanDisk Ultra/Extreme o Samsung EVO Select). En Raspberry Pi 5, la instalación en un SSD NVMe mediante un HAT PCIe multiplica por diez la velocidad de transferencia.
- Software de flasheo: Raspberry Pi Imager (altamente recomendado por su compatibilidad nativa con la Pi 5), BalenaEtcher o `dd` en WSL/Linux.
- Alimentación oficial USB-C PD (crítico): la Raspberry Pi 5 exige obligatoriamente una fuente de 5V y 5A (25W) con Power Delivery (PD). Usar fuentes genéricas de 5V/3A de móviles limita la energía del puerto USB, provocando congelamientos aleatorios del sistema y corrupción inmediata en los datos de la MicroSD.

## Descarga

- Sitio web oficial: <https://www.recalbox.com/>
- Nota técnica: es indispensable descargar la variante exacta para la placa destino (ej. seleccionar la sección Raspberry Pi 5). Flashear una compilación de Raspberry Pi 4 impide que el cargador de arranque inicialice el procesador de la Pi 5.

## Preparación de almacenamiento

El esquema de particiones de Recalbox divide de forma estricta los archivos del sistema de los datos de los romsets:

- **Partición RECALBOX (Sistema)**: el software de flasheo crea una partición inicial de unos 4GB en formato FAT32 destinada exclusivamente al kernel de Linux, los controladores del sistema y los archivos de configuración de arranque. No requiere manipulación manual previa.
- **Partición SHARE (Datos del usuario)**: durante el primer arranque, el sistema utiliza automáticamente todo el espacio restante de la tarjeta o SSD para crear una segunda partición lógica llamada `SHARE`.
- Configuración del formato: por defecto se crea en formato exFAT de forma nativa, lo que permite extraer la MicroSD de la consola y conectarla directamente a cualquier PC con Windows/WSL para gestionar terabytes de datos sin lidiar con los problemas de permisos de EXT4.
- Integración con pipeline propio: es posible escribir la estructura oficial de carpetas de ROMs en minúsculas estrictas (ej. `/roms/nes/`, `/roms/snes/`, `/roms/megadrive/`, `/roms/psx/`) directamente antes de conectar la tarjeta por primera vez a la consola.

## Instalación

1. Inserta la MicroSD o SSD en el lector del ordenador.
2. Inicia Raspberry Pi Imager. Haz clic en Elegir Dispositivo y selecciona Raspberry Pi 5. En Escribir Sistema Operativo, desplázate hasta Emulación y Juegos -> Recalbox -> selecciona la variante para la placa.
3. Elige el soporte de almacenamiento destino y haz clic en Siguiente/Escribir. Al finalizar la verificación de bloques, expulsa la tarjeta de forma segura.

## Primer arranque

1. Introduce la MicroSD flasheada en la ranura de la Raspberry Pi 5.
2. Conecta el cable Micro-HDMI a la salida principal (puerto HDMI 0, el más cercano a la entrada USB-C de alimentación) y, por último, el cable de corriente oficial de 5A.
3. El sistema ejecuta un script automático de inicialización en modo texto que expande la partición `SHARE` para ocupar el 100% de la capacidad física del soporte y genera todo el árbol de directorios de juegos. La placa se reinicia automáticamente y carga la interfaz gráfica enriquecida de EmulationStation mostrando la música de fondo oficial.

## Configuración post-instalación

- **Volcado de ROMsets y BIOS**: extrayendo la tarjeta y leyéndola en el ordenador (gracias a su partición exFAT nativa), o mediante red local (Samba) introduciendo la dirección `\\RECALBOX` en el explorador de Windows si la placa está conectada por Wi-Fi o Ethernet. Transfiere los juegos a sus respectivas carpetas. Es obligatorio copiar las BIOS validadas en el directorio raíz `/share/bios/`.
- **Indexación de metadatos (`gamelist.xml`)**: el frontend lee la base de datos de juegos a través de `gamelist.xml`, situado en la raíz de cada carpeta de consola. Los archivos multimedia se alojan por defecto en `/share/roms/[sistema]/images/` para carátulas y `/share/roms/[sistema]/videos/` para los clips de vídeo.
- Ventaja de pipeline propio: es posible generar `gamelist.xml` de forma nativa a partir de DATs propios estructurados, enlazando las imágenes locales sin depender del raspador interno de la consola, mucho más lento y propenso a saturar la memoria caché del sistema.

## Notas

- **Tratamiento de ROMsets Arcade modernos (rendimiento extremo)**: gracias a la potencia bruta del procesador Broadcom BCM2712 de la Raspberry Pi 5, Recalbox puede ejecutar de forma sobrada los emuladores arcade más exigentes del mercado. El estándar absoluto recomendado por la comunidad para sistemas de placas recreativas (CPS1, CPS2, CPS3, Neo-Geo) es FinalBurn Neo (romset en formato Non-Merged). Para arcade generales complejos o títulos poligonales pesados de los 90, usa el núcleo MAME actualizado (evitar núcleos obsoletos como MAME 2003 en Pi 5). Incluir la BIOS `neogeo.zip` de la versión correspondiente en la raíz de la carpeta arcade.
- **Optimización del formato de consolas en disco**: al contar con emuladores independientes modernos de 64 bits (como DuckStation o Flycast), el formato de compresión CHD (v5) es el estándar mandatorio para cualquier sistema basado en discos compactos (PS1, Sega CD, Saturn, Dreamcast, Panasonic 3DO, PC-FX). Reduce el peso de las ISOs a la mitad, alivia el bus de lectura de la MicroSD y aprovecha la alta velocidad de los núcleos de la Pi 5 para eliminar los cuellos de botella al leer múltiples pistas musicales desde el soporte físico. Para PSP, usar el formato CSO.
- **Gestión 1G1R de la interfaz**: aunque la Raspberry Pi 5 cuenta con 4GB de memoria RAM física y gestiona EmulationStation a 60 FPS estables sin inmutarse, cargar carpetas saturadas con miles de archivos duplicados de distintas regiones, betas o prototipos arruina la experiencia de usuario al navegar por los menús visuales. Es una excelente práctica aplicar un filtro 1G1R estricto antes de transferir los juegos, limitando los conjuntos a los títulos esenciales e idiomas prioritarios (ej. España/Europa) por plataforma para mantener una biblioteca limpia, elegante y de carga instantánea.
