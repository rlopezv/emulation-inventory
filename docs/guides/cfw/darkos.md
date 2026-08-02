# dArkOS

dArkOS es una distribución y bifurcación (fork) altamente optimizada de ArkOS, diseñada específicamente para corregir problemas de visualización, maximizar la tasa de refresco y exprimir el rendimiento de la GPU en dispositivos con pantallas de relación de aspecto 4:3 y 16:9 de generaciones anteriores de Rockchip. Utiliza un frontend EmulationStation modificado para un bajo consumo de memoria RAM y mantiene la flexibilidad de Ubuntu/Debian, permitiendo la ejecución de núcleos nativos independientes para sistemas complejos de 32 y 64 bits.

## Dispositivos aplicables

- PowKiddy RGB20 (modelo vertical clásico)
- PowKiddy RGB10 Max / RGB10 Max 2 (modelos horizontales de pantalla grande)
- Odroid Go Advance (OGA), Anbernic RG351MP, RG353M, RG353V, RG353VS, RG503 (según `docs/software.md`)
- Nota: comprobar las revisiones de placa específicas de la comunidad en los modelos Max, ya que dArkOS incluye controladores corregidos para los paneles táctiles y módulos Wi-Fi integrados de estos terminales.

## Tipo de instalación

Imagen flasheada a SD (`.img`), instalación limpia de fábrica. Soporta de forma nativa configuraciones de tarjeta única o el ecosistema de doble tarjeta (SD1 sistema, SD2 ROMs).

## Requisitos previos

- Tarjeta MicroSD de alta calidad: una de 16GB o 32GB (Clase 10 o superior) para el sistema operativo (SD1) y una secundaria de 64GB a 256GB para el almacenamiento de datos (SD2).
- Software de flasheo: Rufus (recomendado para Windows), BalenaEtcher o `dd` en WSL/Linux.
- Alimentación estable: al menos un 50% de batería en el dispositivo antes de iniciar el flasheo por primera vez.

## Descarga

- Repositorio de la comunidad: al ser una variante modificada, las imágenes estables de dArkOS se distribuyen a través de hilos comunitarios específicos de preservación o repositorios dedicados en GitHub gestionados por desarrolladores independientes de la escena de PowKiddy — <https://github.com/christianhaitian/dArkOS>
- Descargar siempre el archivo de imagen comprimido específico para el nombre del modelo (ej. `dArkOS-RGB10MAX2.img`).

## Preparación de almacenamiento

- **SD1 (Sistema)**: el software de flasheo crea las particiones necesarias en formato Linux (rootfs en EXT4 y la partición BOOT en FAT32). No requiere formateo previo.
- **SD2 (ROMs — ranura TF2)**: debe formatearse obligatoriamente en exFAT.
- Integración con pipeline propio: dArkOS comparte la nomenclatura de rutas de ArkOS. Si se inyecta la estructura de carpetas antes del primer arranque mediante script, hay que crear la carpeta raíz `/roms/` y directorios específicos como `/roms/mastersystem/` o `/roms/pcengine/` para evitar conflictos en el escaneo del frontend.

## Instalación

1. Inserta la SD1 en el lector de tarjetas del PC.
2. Inicia el software de flasheo (ej. Rufus) y selecciona el archivo de imagen `.img` descomprimido de dArkOS.
3. Selecciona la unidad correspondiente a la MicroSD y haz clic en Escribir/Iniciar. Ignora cualquier aviso de Windows solicitando formatear particiones adicionales tras el proceso.

## Primer arranque

1. Introduce únicamente la SD1 flasheada en la ranura principal de la consola (TF1/INT). Mantén la ranura SD2 vacía.
2. Enciende el dispositivo. El sistema ejecuta un script de inicialización automático en modo texto que expande las particiones en la SD1. El terminal se reinicia automáticamente tras completar este paso.
3. Una vez cargue EmulationStation, entra al menú de configuración: `Options -> Advanced -> Switch to SD2 for ROMs`. El sistema prepara el cambio y se apaga solo.
4. Inserta la SD2 en la ranura secundaria (TF2/EXT) y enciende la consola. El sistema puebla automáticamente la estructura de directorios en la segunda tarjeta si no existía previamente.

## Configuración post-instalación

- **Transferencia de ROMsets y BIOS**: vuelca los conjuntos de juegos validados en sus carpetas correspondientes en la SD2. Las BIOS de sistemas que las requieran deben copiarse obligatoriamente en `/roms/bios/`.
- **Indexación multimedia**: el frontend lee la lista de juegos mediante `gamelist.xml`, situado en la raíz de cada carpeta de consola. Los archivos multimedia se alojan en `/roms/[sistema]/images/` para portadas y `/roms/[sistema]/videos/` para clips de vídeo.
- Uso de pipeline propio: es posible escribir `gamelist.xml` de forma nativa a partir de DATs propios, permitiendo que la interfaz de dArkOS muestre carátulas personalizadas al instante sin ralentizar el rendimiento por procesos de scraping internos.

## Notas

- **Optimización del formato Arcade**: dArkOS ejecuta por defecto núcleos altamente optimizados de FinalBurn Neo y MAME 2003-Plus. Para evitar cierres inesperados, procesar los romsets arcade en formato Non-Merged utilizando los archivos DAT estrictos de estas dos variantes antes de transferirlos a la SD2.
- **Tratamiento de consolas en disco**: al igual que su sistema base, soporta nativamente el formato de compresión CHD (v5) para sistemas de 16, 32 y 64 bits (PS1, Saturn, Sega CD, PC-FX). Usar CHDs en las pantallas grandes de los modelos RGB10 Max estabiliza la velocidad de lectura del bus de la tarjeta SD.
- **Gestión 1G1R**: dArkOS se beneficia enormemente del filtrado 1 Game 1 ROM. El uso de listados limpios generados con herramientas como retool reduce drásticamente el uso de memoria caché de EmulationStation, crítico en la PowKiddy RGB20 por su ajustada memoria RAM.
