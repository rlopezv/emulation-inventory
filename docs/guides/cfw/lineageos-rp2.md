# LineageOS (Retroid Pocket 2)

LineageOS para la Retroid Pocket 2 es una distribución limpia de Custom ROM basada en Android (comúnmente Android 8.1 Oreo o versiones optimizadas de la comunidad) desarrollada para reemplazar por completo el sistema operativo de fábrica (Android 6.0). Destaca técnicamente por eliminar todo el bloatware del fabricante, liberar memoria RAM crítica (esencial en este hardware de 1GB), mejorar la latencia de entrada de los controles físicos mediante parches de kernel nativos y ofrecer soporte moderno para APIs de gráficos actualizadas, lo que permite ejecutar emuladores independientes (standalone) avanzados con una tasa de FPS mucho más estable.

## Dispositivos aplicables

- Retroid Pocket 2 (modelo original equipado con el procesador MediaTek MT6580 y 1GB de RAM)
- Nota crítica: no es compatible con la Retroid Pocket 2+ (Plus) ni la Retroid Pocket 2S, las cuales utilizan procesadores Unisoc totalmente diferentes. Flashear esta ROM en esos modelos provoca un brick irreversible de hardware.

## Tipo de instalación

Flasheo por herramienta de fabricante (SP Flash Tool). Instalación profunda a nivel de firmware mediante una conexión por cable USB a un ordenador. Requiere poner el dispositivo en modo de descarga forzada para reescribir todas las particiones de la memoria flash NAND interna (eMMC), borrando por completo el sistema operativo de fábrica.

## Requisitos previos

- Ordenador con Windows o WSL: necesario para ejecutar las herramientas de flasheo de MediaTek.
- Cable de datos USB-C de alta calidad: conexión directa a un puerto de la placa base (evitar hubs USB).
- Controladores MediaTek Preloader (MTK VCOM Drivers): indispensables para que el ordenador reconozca la consola apagada en modo de flasheo.
- Tarjeta MicroSD de alta velocidad: de 64GB a 256GB (SanDisk Ultra o Samsung EVO) destinada exclusivamente al almacenamiento de ROMs y recursos multimedia.

## Descarga

- Repositorio y guías de la comunidad: al ser un desarrollo de la escena, los archivos se descargan desde hilos oficiales y espejos autorizados distribuidos en Discord o en guías consolidadas de la comunidad Retroid — <https://retrogamecorps.com/2021/03/21/lineageos-android-8-1-on-retroid-pocket-2/>
- Paquete requerido: descargar el archivo comprimido que contiene la ROM completa junto con el agente de arranque y los archivos de dispersión (ej. `RP2-LineageOS-vX.X-Full-Flash.zip`).

## Preparación de almacenamiento

El ecosistema de Android gestiona el almacenamiento de forma totalmente diferente a los sistemas Linux ligeros:

- **Memoria interna (eMMC)**: no requiere preparación manual. El flasheo mediante la herramienta del fabricante borra, crea y formatea las particiones del sistema de forma automática.
- **Tarjeta MicroSD (almacenamiento de ROMs)**: debe formatearse en el ordenador obligatoriamente en exFAT o FAT32.
- Nota de Android: al introducir la tarjeta por primera vez, Android pregunta si se desea usarla como "Almacenamiento portátil" o "Almacenamiento interno extendido". Seleccionar siempre Almacenamiento portátil; esto permite extraer la tarjeta e introducirla en el PC/WSL para gestionar los ROMsets sin restricciones de cifrado de Android.
- Estructura de carpetas: Android y los frontends modernos leen cualquier ruta. Para un pipeline propio, inyectar una estructura limpia y estándar en la raíz como `/ROMS/NES/`, `/ROMS/SNES/`, `/ROMS/Arcade/` o `/ROMS/PSX/` es la solución de organización idónea.

## Instalación

1. Instala los controladores MTK VCOM en el ordenador. Reinicia el equipo para asegurar que los controladores firmados se carguen correctamente.
2. Descomprime SP Flash Tool y el paquete de la ROM LineageOS. Abre el ejecutable de la herramienta y carga el archivo de dispersión (`MT6580_Android_scatter.txt`) incluido en la carpeta de la ROM.
3. Cambia el modo de flasheo en la pestaña desplegable de la herramienta de `Download Only` a `Firmware Upgrade` (paso crítico para asegurar que se reescriban las tablas de particiones correctamente).
4. Haz clic en el botón `Download` en la herramienta de PC. Con la Retroid Pocket 2 completamente apagada, conéctala al ordenador mediante el cable USB-C. La herramienta detecta el dispositivo mediante el Preloader, la barra de progreso cambia a color rojo, luego amarillo, e inicia el volcado del firmware. Mantén el dispositivo conectado hasta que aparezca el círculo verde de confirmación.

## Primer arranque

1. Desconecta el cable USB de la Retroid Pocket 2.
2. Mantén pulsado el botón de encendido hasta que la pantalla inicial se ilumine. El primer arranque bajo LineageOS puede demorarse entre 3 y 5 minutos debido a que Android debe compilar el entorno de ejecución ART en caché.
3. Una vez cargue el asistente de configuración inicial de Android, completa los pasos básicos (idioma, Wi-Fi y cuenta de Google opcional). El sistema carga el escritorio limpio de LineageOS.

## Configuración post-instalación

- **Configuración del frontend**: al ser Android, se recomienda encarecidamente instalar un frontend optimizado como Daijishō, Pegasus o Beacon desde la Play Store o mediante la inyección directa de archivos APK por USB.
- **Asignación de rutas**: abre el frontend instalado y dirígelo a las carpetas correspondientes dentro de la tarjeta MicroSD portátil (ej. `/storage/XXXX-XXXX/ROMS/SNES/`). El frontend indexará los archivos.
- **Tratamiento de metadatos**: a diferencia de los CFW de Linux, los frontends de Android no dependen de un archivo centralizado `gamelist.xml` local en cada directorio. Realizan un raspado digital (scraping) interno indexando las ROMs directamente en una base de datos SQLite interna de la aplicación de Android. No requiere inyectar imágenes sueltas en carpetas secundarias de la SD.

## Notas

- **Tratamiento de ROMsets Arcade estrictos**: debido a las severas limitaciones del procesador MediaTek MT6580 (arquitectura ARM de 32 bits de cuatro núcleos de baja potencia), los núcleos modernos de RetroArch como FinalBurn Neo sufren ralentizaciones críticas. La directriz obligatoria es compilar un subset arcade basado estrictamente en el archivo DAT oficial de MAME 0.78 (núcleo `mame2003` o `mame2003-plus`). No usar romsets arcade modernos ni formatos combinados de MAME actuales.
- **Optimización máxima para consolas de disco**: para sistemas como PlayStation 1, la emulación mediante el emulador independiente ePSXe o el núcleo PCSX ReARMed en Android rinde de forma óptima con el formato comprimido CHD (v5). Es necesario automatizar esta conversión masiva para reducir los tiempos de acceso del bus eMMC/SD, ahorrar hasta un 40% de espacio y garantizar los 60 FPS estables.
- **Gestión de la RAM y filtro 1G1R obligatorio**: la Retroid Pocket 2 original cuenta únicamente con 1GB de memoria RAM física. Los frontends avanzados de Android como Daijishō devoran una cantidad masiva de RAM al indexar las listas de juegos si estas contienen miles de títulos. Si se intenta cargar un full-set completo de NES o Genesis (con más de 2000-3000 juegos), el frontend se cierra por falta de memoria (Out of Memory / OOM Crash) o ralentiza el sistema operativo de forma crítica. Es técnicamente obligatorio aplicar un filtro 1G1R estricto (con herramientas como retool) para limitar los subsets a no más de 250 títulos selectos por consola, garantizando que el frontend mantenga el sistema estable y fluido.
