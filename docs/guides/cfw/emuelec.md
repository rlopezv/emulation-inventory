# EmuELEC

EmuELEC es un Custom Firmware (CFW) de código abierto y alto rendimiento basado en CoreELEC/Lakka (Linux embebido) diseñado específicamente para SoC de la marca Amlogic. Utiliza una bifurcación optimizada de EmulationStation como frontend principal y destaca en la escena por ser el software preinstalado en la inmensa mayoría de consolas arcade domésticas y TV Boxes modificadas. Su arquitectura está orientada a exprimir al máximo los chips de bajo coste mediante controladores gráficos optimizados (Mali) y un sistema híbrido que ejecuta núcleos de RetroArch de 32 y 64 bits de forma transparente para lograr la máxima tasa de FPS posible.

## Dispositivos aplicables

- TV Box Amlogic S905/S912 (genérico)
- Super Console X (y todas sus variantes: Pro, King, Cube, etc.)
- Game Sticks (basados en procesadores Amlogic compatibles como S905Y2/X3)

## Tipo de instalación

Imagen flasheada a SD (`.img.gz`). Instalación limpia que reemplaza el arranque nativo del dispositivo, o convive con Android en modo Dual Boot mediante el lector de tarjetas.

## Requisitos previos

- Tarjeta MicroSD de alta velocidad: se recomienda 32GB a 256GB de primera marca (SanDisk Ultra o Samsung EVO). Las TV Boxes con SoC Amlogic tienen lectoras integradas que sufren con tarjetas genéricas.
- Software de flasheo: Rufus o BalenaEtcher para entornos de escritorio, o `dd` en WSL/Linux.
- El archivo DTB (Device Tree Blob) correcto: indispensable para que el kernel de Linux reconozca los componentes exactos (RAM, Wi-Fi, Ethernet) del modelo de TV Box.

## Descarga

- Repositorio oficial de la escena: las imágenes estables de fábrica y las actualizaciones se descargan de forma centralizada desde el GitHub oficial del proyecto — <https://github.com/EmuELEC/EmuELEC>
- Nota de descarga: descargar el archivo de imagen general para tarjetas SD (`EmuELEC-Amlogic.aarch64-vX.X-Generic.img.gz`). No usar los archivos de actualización `.tar`.

## Preparación de almacenamiento

- **SD de sistema y ROMs (híbrida)**: el flasheo destruye la tabla de particiones antigua para crear dos particiones lógicas: `EMUELEC` (FAT32, donde reside el sistema de arranque y los archivos DTB) y `STORAGE` (EXT4, la partición oculta del sistema Linux).
- **Partición EEROMS (la zona de juegos)**: durante el primer arranque, el sistema crea una tercera partición visible llamada `EEROMS` (formateada automáticamente en FAT32 o exFAT según la versión de EmuELEC).
- Integración con pipeline propio: EmuELEC exige nombres de carpetas en minúsculas estrictas para los sistemas (ej. `/roms/snes/`, `/roms/megadrive/`, `/roms/nes/`). Si se precargan los datos con un script propio, hay que clonar la estructura oficial de rutas de EmulationStation para evitar carpetas huérfanas.

## Instalación

1. Inserta la MicroSD en el ordenador.
2. Abre la herramienta de flasheo (ej. Rufus) y escribe la imagen `.img.gz` de EmuELEC en la tarjeta.
3. **Paso crítico de configuración (el archivo DTB)**: una vez finalizado el flasheo, se monta la partición visible llamada `EMUELEC`. Entra en ella y abre la carpeta `device_trees`. Busca el archivo `.dtb` que corresponda exactamente al procesador y memoria RAM de la TV Box (ej. `gxl_p212_2g.dtb` para un S905X con 2GB de RAM). Copia ese archivo, pégalo en la raíz de la partición `EMUELEC` y renómbralo exactamente como `dtb.img` (reemplazando el archivo genérico existente). Si se omite este paso, la TV Box no arranca.

## Primer arranque

1. Introduce la MicroSD con el archivo `dtb.img` configurado en la ranura de la TV Box / Super Console X.
2. **Forzar el arranque desde SD (método del palillo)**: con la TV Box completamente apagada y desconectada de la corriente, introduce un palillo o clip dentro del puerto AV (donde suele estar oculto el botón físico de Reset). Mantén presionado el botón de reset, conecta el cable de alimentación y no lo sueltes hasta que aparezca el logotipo oficial de EmuELEC en pantalla. Este paso solo es necesario la primera vez, para indicarle al chip Amlogic que priorice el arranque por MicroSD frente a la memoria interna de Android.
3. El sistema expande las particiones automáticamente, crea la partición de almacenamiento de juegos `EEROMS` y se reinicia mostrando la interfaz de EmulationStation.

## Configuración post-instalación

- **Volcado de ROMsets y BIOS**: extrae la tarjeta MicroSD de la TV Box e introdúcela en el PC. Aparece la nueva partición `EEROMS`. Vuelca los conjuntos de juegos validados en sus carpetas correspondientes. Es un requisito inamovible copiar los archivos de BIOS obligatorios en la ruta centralizada `/bios/` en la raíz de la partición de juegos.
- **Indexación multimedia (`gamelist.xml`)**: EmuELEC lee la base de datos de juegos a través de `gamelist.xml`, situado en la raíz de cada carpeta de consola. Las carátulas y vídeos se alojan por defecto en `/roms/[sistema]/images/` y `/roms/[sistema]/videos/`.
- Ventaja de pipeline propio: es posible generar `gamelist.xml` de forma nativa a partir de DATs propios estructurados, enlazando las imágenes locales sin depender del raspador interno de la consola, mucho más lento y propenso a saturar la memoria caché del sistema.

## Notas

- **Tratamiento de ROMsets Arcade (estricto)**: debido a que EmuELEC suele ejecutarse en procesadores Amlogic de bajo coste (como los clásicos S905X), los núcleos arcade modernos de RetroArch sufren ralentizaciones drásticas. El estándar absoluto recomendado por la comunidad es compilar un subset arcade basado estrictamente en el archivo DAT oficial de MAME 2003-Plus (romset `0.78-plus`) para arcade general, y núcleos optimizados de FinalBurn Neo en formato Non-Merged para las placas de Capcom y Neo-Geo. Es imperativo incluir la BIOS `neogeo.zip` adaptada a esa era para evitar pantallas en negro.
- **Optimización del formato de consolas en disco**: al estar basado en la infraestructura moderna de RetroArch, soporta de forma nativa el formato de compresión CHD (v5) en todos los sistemas basados en discos ópticos (PS1, Sega CD, Saturn, Dreamcast, PC-FX y 3DO). Convertir las colecciones a CHD reduce el peso de la biblioteca a la mitad y alivia el bus de lectura de la MicroSD. Para PlayStation Portable (PSP), soporta perfectamente el formato CSO.
- **Gestión 1G1R y resolución de carátulas (muy crítica)**: las TV Boxes y consolas baratas como la Super Console X sufren de serios problemas de gestión de memoria al renderizar interfaces gráficas pesadas. Cargar carpetas saturadas con miles de ROMs clonadas provoca retrasos severos (lag) al navegar por los menús. Además, introducir carátulas HD o 4K provoca que EmulationStation se cierre por falta de memoria RAM.
