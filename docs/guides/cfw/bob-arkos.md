# BOB (Best of the Best) — variante ArkOS

BOB (Best of the Best) en su variante ArkOS es una compilación masiva, optimizada y pre-configurada por la comunidad que utiliza como núcleo el sistema operativo ArkOS (Ubuntu/Debian Linux de 64 bits). A diferencia de una instalación limpia de ArkOS, esta variante destaca por incluir un entorno llave en mano con configuraciones avanzadas para la asignación de emuladores independientes (standalone), scripts de optimización para la tasa de refresco, temas visuales de EmulationStation diseñados para pantallas de baja resolución y un árbol de directorios optimizado listo para recibir conjuntos masivos de ROMs de 8, 16, 32 y 64 bits.

## Dispositivos aplicables

- Anbernic RG351P / RG351M (pantallas con relación de aspecto 3:2)
- Anbernic RG351V (consola vertical con pantalla 4:3)
- Anbernic RG351MP (consola horizontal metálica con pantalla 4:3)
- PowKiddy RGB10 Max (pantalla panorámica de 5 pulgadas)

## Tipo de instalación

Imagen flasheada a SD (`.img`), instalación limpia de bajo nivel. El sistema opera por defecto bajo una configuración de tarjeta única, pero permite bifurcar el almacenamiento a un esquema de doble tarjeta (SD1 sistema, SD2 ROMs) mediante scripts integrados en su panel de herramientas.

## Requisitos previos

- Tarjeta MicroSD de alta capacidad: al ser una distribución que incluye múltiples recursos y configuraciones complejas, se recomienda un tamaño mínimo de 64GB, 128GB o 256GB (SanDisk Ultra o Samsung EVO Select).
- Software de flasheo: Rufus (muy recomendado para las particiones extendidas de ArkOS), BalenaEtcher o `dd` en WSL/Linux.
- Herramienta de particionado externa: MiniTool Partition Wizard o gparted en WSL para corregir o extender la partición de datos si el expansor automático del kernel falla.

## Descarga

- Repositorios de la escena: debido a su naturaleza pre-configurada y empaquetada, las imágenes de BOB variante ArkOS se distribuyen a través de canales comunitarios específicos (hilos de preservación retro, canales de Telegram de la escena y servidores espejo compartidos) — [TODO: URL exacta / fuente].
- Descargar siempre el archivo comprimido específico para el procesador y pantalla del dispositivo (ej. la imagen para la RG351V es diferente a la de la RG351P debido a la resolución nativa del panel).

## Preparación de almacenamiento

- **SD de sistema (única)**: no requiere formateo manual previo; el flasheo crea la estructura Linux necesaria: una partición de arranque BOOT (FAT32), la partición del sistema operativo raíz `rootfs` (EXT4) y una partición destinada a los datos visibles del usuario.
- **Nomenclatura estricta de carpetas**: al estar basado en el núcleo de ArkOS, el sistema utiliza nombres específicos en minúsculas para sus directorios de juegos dentro de la ruta `/roms/`. Hay que inyectar las colecciones respetando exactamente las rutas nativas, tales como `/roms/nes/`, `/roms/snes/`, `/roms/megadrive/`, `/roms/gba/` y `/roms/psx/`.

## Instalación

1. Inserta la MicroSD en el lector de tarjetas del ordenador.
2. Descomprime la imagen descargada de BOB hasta obtener el archivo ejecutable `.img`.
3. Abre la herramienta de flasheo (ej. Rufus), selecciona el archivo `.img` y elige la MicroSD como unidad de destino. Haz clic en Escribir/Iniciar. Al finalizar, ignora los mensajes de error de Windows relativos al formato de particiones adicionales y expulsa la tarjeta de forma segura.

## Primer arranque

1. Inserta la MicroSD flasheada en la ranura principal de la consola (TF1/INT). Si se planea usar doble tarjeta, mantén la ranura TF2 vacía en este paso.
2. Enciende el dispositivo. El kernel de ArkOS ejecuta un script automatizado de inicialización en segundo plano que expande la partición de las ROMs para ocupar el 100% de la capacidad restante de la tarjeta. El sistema se reinicia automáticamente.
3. (Opcional para doble tarjeta): para volcar los ROMsets en una tarjeta secundaria, ve al menú de la consola en `Options -> Advanced -> Switch to SD2 for ROMs`. El sistema se apaga. Inserta la SD2 formateada en exFAT en la ranura TF2, vuelve a encender la consola y el sistema genera el árbol de carpetas en ella de forma instantánea.

## Configuración post-instalación

- **Volcado de ROMsets y BIOS**: transfiere las colecciones de juegos organizadas a las carpetas correspondientes en la partición de datos. Es un requisito inamovible copiar los archivos de BIOS obligatorios dentro de la carpeta centralizada `/roms/bios/` en la raíz de la partición de juegos para garantizar el arranque de sistemas avanzados.
- **Indexación multimedia (`gamelist.xml`)**: el frontend EmulationStation lee la base de datos de juegos a través de `gamelist.xml`, situado en la raíz de cada carpeta de consola. Los archivos multimedia se alojan por defecto en `/roms/[sistema]/images/` para carátulas y `/roms/[sistema]/videos/` para los clips de vídeo.
- Ventaja de pipeline propio: es posible generar `gamelist.xml` de forma nativa a partir de DATs propios estructurados, enlazando las imágenes locales sin depender del lento proceso de scraping interno de la consola.

## Notas

- **Tratamiento de ROMsets Arcade optimizados**: BOB variante ArkOS viene pre-configurado para priorizar FinalBurn Neo (romset en formato Non-Merged) en títulos arcade clásicos y de lucha. Para juegos arcade generales complejos, utiliza el núcleo MAME 2003-Plus (romset `0.78-plus`). Es mandatorio procesar las colecciones con los archivos DAT estrictos de estas versiones para evitar pantallas en negro o fallos en el mapeo de los controles.
- **Optimización del formato de consolas en disco**: al contar con núcleos independientes optimizados de 64 bits para sistemas basados en CD/DVD (como DuckStation o Flycast), el formato de compresión CHD (v5) es el estándar obligatorio para PS1, Sega CD, Saturn y Dreamcast. Convertir las colecciones a CHD reduce el peso de la biblioteca a la mitad, alivia el bus de lectura de la MicroSD y acelera la carga. Para juegos de PSP, soporta perfectamente el formato CSO.
- **Gestión 1G1R y rendimiento del frontend**: debido a que BOB utiliza temas pesados y configuraciones avanzadas en EmulationStation, cargar carpetas saturadas con miles de archivos duplicados de distintas regiones provoca retrasos severos (lag) al navegar por los menús o al arrancar la consola. Aplicar un filtro 1G1R limpio (con herramientas como retool) antes de transferir los juegos garantiza que la interfaz de EmulationStation mantenga una navegación fluida a 60 FPS estables.
- **Apagado seguro del sistema**: al ser una distribución basada en Ubuntu Linux completa, nunca se debe apagar la consola manteniendo pulsado el botón físico de Power de forma brusca. Hazlo siempre desde el menú de EmulationStation (`Start -> Quit -> Shutdown System`) para salvaguardar la integridad de las tablas de particiones, evitar la corrupción de la base de datos de juegos y proteger los archivos de guardado rápido (savestates).
