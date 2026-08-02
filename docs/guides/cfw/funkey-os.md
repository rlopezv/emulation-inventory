# FunKey OS

FunKey OS es un sistema operativo y Custom Firmware (CFW) de código abierto embebido, ultraligero y basado en Linux, desarrollado desde cero utilizando la infraestructura de compilación Buildroot. Está optimizado específicamente para procesadores ARM de arquitectura compacta (como el Allwinner V3s) y destaca por su sistema de gestión de energía instantáneo, el cual permite pausar y guardar el estado del juego automáticamente al cerrar la tapa de la consola y apagar el dispositivo en menos de un segundo. Utiliza el frontend RetroFE adaptado para resoluciones cuadradas, cargando emuladores nativos altamente optimizados en formato de paquetes `.opk`.

## Dispositivos aplicables

- FunKey S (la microconsola plegable original estilo Game Boy Advance SP de llavero)
- PowKiddy Q36 Mini (variante horizontal de microconsola de llavero que utiliza la misma placa base)
- Nota: este firmware sirve como núcleo de desarrollo para derivaciones de otros fabricantes basados en la misma CPU y pantalla.

## Tipo de instalación

Imagen flasheada a SD (`.img`). El sistema opera bajo una configuración de tarjeta única en la que el flasheo gestiona de forma transparente las particiones del sistema y el espacio de almacenamiento del usuario.

## Requisitos previos

- Tarjeta MicroSD estándar de marca: se recomienda 16GB, 32GB o como máximo 64GB (SanDisk Ultra o Samsung EVO).
- Nota de ingeniería: el bus de datos del procesador Allwinner V3s está diseñado para un bajo consumo; usar tarjetas de 128GB o superiores provoca retardos severos en la inicialización del sistema y aumenta la degradación de bloques de la tarjeta.
- Software de flasheo: Rufus o BalenaEtcher para Windows/macOS, o `dd` en WSL/Linux.
- Cable de datos Micro-USB o USB-C (según el dispositivo aplicable) de buena calidad para la posterior transferencia de datos desde el ordenador.

## Descarga

- Repositorio de lanzamientos oficial: las imágenes de fábrica consolidadas y las actualizaciones se distribuyen directamente a través del GitHub oficial del equipo de desarrollo — <https://github.com/FunKey-Project/FunKey-OS>
- Nota técnica: descargar siempre el archivo comprimido que contenga la imagen del sistema operativo completo terminada en `.img` (ej. `FunKey-OS-vX.X.X.img`). No usar el archivo de actualización `.fwu` si se va a realizar una instalación limpia desde cero.

## Preparación de almacenamiento

- **SD de sistema (única)**: no requiere formateo ni manipulación previa de particiones; el flasheo destruye las tablas antiguas para escribir la partición de arranque Linux y la partición visible del usuario.
- Integración con pipeline propio: FunKey OS monta la partición de las ROMs de manera visible para el usuario bajo un esquema de rutas muy estricto en minúsculas. Hay que inyectar o mapear las colecciones de juegos respetando exactamente los nombres de directorios nativos del sistema en la raíz de la tarjeta, tales como `/nes/`, `/snes/`, `/megadrive/`, `/gba/`, `/gbc/`, `/ps1/` y `/lynx/`.

## Instalación

1. Conecta la tarjeta MicroSD al lector del ordenador.
2. Inicia el software de flasheo (ej. Rufus). Selecciona la unidad destino de la MicroSD y carga la imagen `.img` descomprimida de FunKey OS.
3. Haz clic en Escribir/Iniciar. Al finalizar la operación, expulsa la tarjeta de forma segura e ignora cualquier aviso de Windows referente al formateo de particiones adicionales.

## Primer arranque

1. Inserta la MicroSD flasheada en la ranura interna de la consola.
2. Enciende el dispositivo. En este primer inicio, el kernel de FunKey OS ejecuta un script automatizado en segundo plano que redimensiona y expande automáticamente la partición de datos visible para que ocupe el 100% de la capacidad física de la MicroSD.
3. El dispositivo completa la inicialización y carga la interfaz gráfica de RetroFE mostrando los sistemas listos para usar. No requiere ninguna interacción ni comandos adicionales por parte del usuario.

## Configuración post-instalación

- **Volcado de archivos**: conecta la consola encendida al PC mediante el cable USB. El sistema monta la partición de juegos en el ordenador automáticamente como si fuera un pendrive. Copia las colecciones de juegos en las subcarpetas del sistema correspondientes. Es obligatorio ubicar los archivos de BIOS en el directorio raíz `/bios/` configurado por el sistema.
- **Tratamiento de carátulas (previews)**: el frontend busca imágenes en formato `.png` guardadas estrictamente dentro de una subcarpeta `previews` dentro de la carpeta de cada consola. Los nombres de los archivos multimedia deben coincidir byte por byte con el nombre del archivo de la ROM.
- **Acción crítica de pipeline**: la pantalla del dispositivo tiene una resolución física y cuadrada de 240x240 píxeles. Es necesario procesar las imágenes multimedia de forma masiva reescalándolas con un filtro de alta calidad Lanczos a un tamaño estricto de 240x240 píxeles y reduciendo la profundidad de color a 8 bits. Introducir imágenes HD convencionales satura instantáneamente la memoria RAM del procesador (64MB), provocando bloqueos del frontend o ralentizaciones severas al navegar por los menús.

## Notas

- **Tratamiento de ROMsets Arcade**: al igual que sus derivados, el entorno arcade nativo de FunKey OS está ligado a emuladores empaquetados muy optimizados. Hay que filtrar y compilar subsets utilizando los DATs de MAME 0.37b5 (MAME 2000) o FinalBurn Alpha 0.2.97.44. Es obligatorio incluir el archivo de BIOS `neogeo.zip` correspondiente a esa era dentro de la misma ruta de las ROMs de arcade para garantizar la compatibilidad.
- **Optimización del formato de consolas en disco**: el emulador de PlayStation 1 integrado en FunKey OS (PCSX4All) está altamente optimizado para leer el formato comprimido CHD (v5). Es obligatorio procesar la colección de PS1 utilizando la conversión masiva a CHD, descartando los archivos `.bin`/`.cue` sueltos, para agilizar la transferencia por USB, reducir el espacio ocupado a la mitad y estabilizar la tasa de FPS en el microdispositivo.
- **Mapeo de funciones de la tapa**: la característica estrella de FunKey OS es su script de suspensión. Al cerrar la tapa de la FunKey S, el sistema genera de forma transparente un punto de guardado inmediato (savestate) y corta la energía. Al abrir la tapa, el dispositivo arranca en frío e inyecta el estado de guardado en menos de 3 segundos, devolviendo al usuario exactamente al punto donde se quedó.
- **Apagado de sistema**: aunque el interruptor físico o el cierre de la tapa gestionan la suspensión de forma segura, el sistema cuenta con un script de apagado completo por software accesible desde el menú de opciones de RetroFE (`Menu -> Power -> Shutdown`). Se recomienda usar este método si se va a almacenar la consola por un largo período para proteger las tablas de asignación de la partición FAT32.
