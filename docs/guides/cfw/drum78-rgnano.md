# DrUm78 RGNano

DrUm78 RGNano es un Custom Firmware (CFW) de código abierto que adapta y mejora de forma masiva el sistema operativo FunKey-OS (Linux ultra-ligero) específicamente para el hardware minúsculo de Anbernic. Su principal logro técnico es desbloquear una tasa de refresco nativa de 60 Hz eliminando por completo el efecto de parpadeo (screen tearing) del firmware de fábrica. Utiliza el frontend RetroFE con un lanzador optimizado que suprime el reloj analógico inicial stock, integra soporte completo para listas de favoritos independientes y ejecuta emuladores empaquetados en formato `.opk` y núcleos de PicoArch/Libretro a velocidad completa.

## Dispositivos aplicables

- Anbernic RG Nano (consola micro-vertical con chasis de aluminio y pantalla de 1.54 pulgadas)

## Tipo de instalación

Imagen flasheada a SD (`.img`), instalación limpia de fábrica. El sistema opera bajo un esquema de tarjeta única que divide automáticamente el almacenamiento para alojar el sistema y el espacio del usuario.

## Requisitos previos

- Tarjeta MicroSD de calidad: se recomienda encarecidamente 32GB o 64GB de primera marca (SanDisk Ultra o Samsung EVO).
- Nota técnica: evitar tarjetas de 128GB o superiores. El bus físico de la RG Nano no aprovecha esa capacidad y puede elevar drásticamente el consumo de batería y la temperatura del dispositivo.
- Software de flasheo: Rufus (óptimo para Windows), BalenaEtcher (Mac/Windows) o `dd` en WSL/Linux.
- Lector de tarjetas MicroSD USB 3.0 para asegurar la correcta validación de bloques durante el flasheo.

## Descarga

- Repositorio de lanzamientos (GitHub del desarrollador): <https://github.com/DrUm78/FunKey-OS/releases>
- Portal específico de RGNano (según `docs/software.md`): <https://rgnano.com/custom-firmware/>
- Nota de archivo: descargar exclusivamente el archivo completo de imagen que contenga el sufijo `RG_Nano` en su nombre y termine en extensión `.img` (ej. `FunKey-DrUm78-RG_Nano-vX.X.img`). No usar el archivo con extensión `.fwu`, destinado únicamente a actualizaciones menores del sistema sobre instalaciones preexistentes.

## Preparación de almacenamiento

- **SD de sistema (única)**: no requiere formateo ni manipulación previa de particiones; el flasheo destruye el mapa de sectores previo para configurar el kernel.
- Integración con pipeline propio: el sistema utiliza la estructura de rutas heredada de FunKey-OS y monta las particiones visibles bajo la ruta nativa Linux `/mnt/`. Hay que inyectar o mapear las colecciones de juegos respetando nombres de directorios del sistema en minúsculas estrictas dentro de la partición de datos visible, tales como `/gba/`, `/gbc/`, `/nes/`, `/snes/` y `/gg/`.

## Instalación

1. Conecta la tarjeta MicroSD al lector del PC.
2. Inicia el software de flasheo (ej. Rufus). Selecciona la MicroSD destino y carga el archivo `.img` de DrUm78 RGNano.
3. Haz clic en Escribir/Iniciar. Al finalizar con éxito, ignora las alertas de Windows indicando que las particiones no tienen formato y expulsa la tarjeta de forma segura.

## Primer arranque

1. Inserta la MicroSD flasheada en la ranura única de la Anbernic RG Nano.
2. Enciende la consola. El firmware ejecuta un script en modo texto en segundo plano que redimensiona y expande automáticamente la partición de datos para ocupar el 100% del espacio restante de la MicroSD. La consola se reinicia automáticamente.
3. Al finalizar el reinicio, el sistema carga directamente el menú gráfico de RetroFE mostrando los sistemas vacíos listos para recibir metadatos.

## Configuración post-instalación

- **Volcado de ROMsets y BIOS**: conecta la consola encendida al PC mediante USB-C y selecciona el modo de transferencia de archivos (MTP/almacenamiento masivo), o extrae la MicroSD. Copia los juegos organizados en las subcarpetas del sistema. Es obligatorio colocar los archivos de BIOS de consolas de disco o de sistemas avanzados dentro del directorio `/bios/` configurado por el emulador.
- **Tratamiento de carátulas (previews)**: el frontend RetroFE exige imágenes en formato `.png` guardadas estrictamente dentro de una subcarpeta `previews` dentro del directorio de cada consola. Los nombres deben coincidir de forma exacta con la ROM.
- **Acción crítica de pipeline**: la pantalla de la RG Nano tiene una resolución física y cuadrada de 240x240 píxeles. Es necesario procesar las carátulas 3D u originales de forma masiva reescalándolas con un filtro de alta calidad Lanczos a un tamaño estricto de 240x240 píxeles y reduciendo la profundidad de color a 8 bits. Introducir carátulas HD convencionales satura de inmediato la memoria de vídeo del procesador, provocando ralentizaciones drásticas en el menú.

## Notas

- **Tratamiento de ROMsets Arcade**: al igual que FunKey-OS, el soporte arcade nativo de este firmware depende de núcleos empaquetados muy optimizados. Hay que filtrar y compilar subsets utilizando los DATs de MAME 0.37b5 (MAME 2000) o FinalBurn Alpha 0.2.97.44. Colocar siempre la BIOS `neogeo.zip` correspondiente a esa era dentro de la misma ruta de las ROMs arcade.
- **Optimización extrema para PlayStation 1**: la tasa de 60 Hz reales lograda por DrUm78 permite que los títulos de PS1 funcionen con una fluidez sorprendente a pesar del tamaño de la pantalla. Es obligatorio procesar las colecciones de PlayStation utilizando la conversión a CHD (v5); reduce el espacio a la mitad, estabiliza los fotogramas y evita la escritura constante de archivos en caché de la MicroSD.
- **Búsqueda en subcarpetas**: a partir de las versiones actualizadas de DrUm78, el motor de análisis del frontend permite el escaneo de ROMs organizadas dentro de subcarpetas en la tarjeta (útil para organizar sets masivos de sistemas de 8 bits por orden alfabético).
- **Apagado de sistema**: aunque el dispositivo es de bajo coste, DrUm78 ha mapeado un script de apagado seguro por software para proteger la integridad de las tablas de datos de la MicroSD. Se recomienda no cortar la energía directamente con el botón físico de hardware; en su lugar, usar la combinación de botones configurada en el CFW o apagar la consola directamente desde el menú principal de RetroFE.
