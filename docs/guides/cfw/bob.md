# BOB (Best of the Best)

BOB (Best of the Best) es un Custom Firmware (CFW) y una compilación comunitaria altamente optimizada basada en el sistema operativo subyacente MiyooCFW (Linux ligero). Está diseñado específicamente para revitalizar y exprimir el rendimiento de consolas portátiles de bajo coste basadas en el procesador Allwinner F1C100S. Utiliza un frontend GMenu2X personalizado y destaca por incluir emuladores configurados al límite con marcos de salto (frameskip) optimizados, parches de rendimiento y un árbol de directorios pre-estructurado para simplificar la gestión de colecciones de 8 y 16 bits.

## Dispositivos aplicables

- PowKiddy V90 (modelo plegable estilo Game Boy Advance SP)
- PowKiddy Q90 (modelo horizontal estilo Nintendo Switch Lite)
- PowKiddy Q20 Mini (modelo vertical ultra-compacto)
- PocketGo / BitBoy (versiones originales con pantalla de 2.4 pulgadas)

## Tipo de instalación

Imagen flasheada a SD (`.img`), configuración de tarjeta única que aloja tanto el sistema operativo Linux como las particiones lógicas para juegos y recursos.

## Requisitos previos

- Tarjeta MicroSD de marca reputada: se recomienda encarecidamente 16GB, 32GB o como máximo 64GB (SanDisk Ultra o Samsung EVO).
- Nota crítica: al igual que en RetroFW, el bus de memoria y el controlador del procesador Allwinner sufren graves ralentizaciones y retrasos en los tiempos de acceso al intentar leer tarjetas de 128GB o superiores.
- Software de flasheo: Rufus (altamente recomendado para este firmware), BalenaEtcher o `dd` en WSL/Linux.
- Herramienta de particionado en Windows/WSL: MiniTool Partition Wizard o gparted. Indispensable, ya que el redimensionamiento automático suele fallar en las controladoras de estas consolas chinas.

## Descarga

- Repositorio de la comunidad: al ser una compilación cocinada por la comunidad, los enlaces oficiales de las imágenes consolidadas de BOB (como BOB v1.0 o actualizaciones v2.0 Beta) se distribuyen a través de hilos dedicados de preservación, canales comunitarios de Telegram y repositorios espejo (mirrors) en GitHub gestionados por desarrolladores de la escena de MiyooCFW — [TODO: URL exacta / fuente].
- Descargar el archivo comprimido correspondiente al formato general de la consola (los modelos V90/Q90 comparten el mismo kernel).

## Preparación de almacenamiento

- **SD de sistema (única)**: no requiere formateo manual previo. El flasheo destruye la tabla de particiones antigua para escribir el mapa de sectores lógicos de Linux.
- Integración con pipeline propio: BOB destaca porque, a diferencia de los firmwares limpios, ya incluye un árbol de carpetas pre-configurado. No obstante, utiliza nomenclaturas heredadas de sistemas clásicos orientadas a los nombres de los emuladores nativos; hay que mapear los volcados hacia rutas exactas en la partición de datos como `/roms/FC/` (Famicom/NES), `/roms/SFC/` (Super Famicom/SNES), `/roms/MD/` (Mega Drive) y `/roms/PCE/` (PC Engine).

## Instalación

1. Conecta la tarjeta MicroSD al lector del ordenador.
2. Ejecuta el software de flasheo (ej. Rufus) y carga la imagen `.img` descomprimida de BOB.
3. Selecciona la unidad correcta de la tarjeta y haz clic en Escribir/Iniciar. Al finalizar, Windows mostrará alertas de "Partición no legible"; ignóralas y no las formatees bajo ningún concepto.

## Primer arranque

1. Inserta la MicroSD flasheada en la ranura única de la consola.
2. Enciende el dispositivo. El sistema carga el kernel de Linux y arranca directamente en la interfaz visual de GMenu2X.
3. **Paso de redimensionamiento obligatorio**: en el 90% de las imágenes de BOB, la partición visible de las ROMs viene limitada de fábrica al tamaño mínimo de la imagen original (unos 4GB u 8GB). Si la tarjeta es de 32GB o 64GB, hay que apagar la consola, volver a meter la MicroSD en el PC y abrir gparted en WSL o MiniTool en Windows para extender manualmente el tamaño de la partición FAT32 (etiquetada como `main` o `roms`) hasta el final del espacio libre no asignado.

## Configuración post-instalación

- **Inyección de colecciones**: transfiere los ROMsets validados a las carpetas específicas de la partición de datos. Si un emulador nativo requiere BIOS (como `gba_bios.bin` para Game Boy Advance), esta debe colocarse obligatoriamente en el directorio interno del emulador asignado por el CFW (ej. `/gmenu2x/roms/bios/` o dentro de la subcarpeta oculta de configuración de la aplicación en `/home/`).
- **Tratamiento de carátulas (previews)**: GMenu2X en BOB busca imágenes en formato `.png` de baja resolución (tamaño óptimo estricto de 160x120 o ancho máximo de 320x240 píxeles) alojadas en una subcarpeta llamada `previews` dentro de la ruta de cada emulador. Los nombres de las imágenes deben ser 100% idénticos al de la ROM.

## Notas

- **Tratamiento de ROMsets Arcade**: al compartir la base de MiyooCFW, los emuladores arcade integrados en BOB están limitados por la baja potencia del hardware. Hay que procesar exclusivamente el archivo DAT oficial de MAME 0.37b5 (romset de la familia `mame2000`) para la carpeta general de arcade. Para el sistema de lucha Neo-Geo, se usa el emulador optimizado independiente, que requiere su propio juego de ROMs emparejadas con la BIOS `neogeo.zip` de esa misma era.
- **Optimización para PlayStation 1 (límite técnico)**: el procesador Allwinner F1C100S no tiene potencia suficiente para emular PS1 de forma perfecta al 100%. Sin embargo, BOB incluye un núcleo PCSX4All con un código de frameskip muy agresivo. Para maximizar los FPS, es directriz obligatoria convertir las ISOs/BIN de PS1 al formato comprimido CHD (v5), lo que reduce el cuello de botella en la velocidad de lectura de la MicroSD y estabiliza el rendimiento de los juegos compatibles.
- **Gestión 1G1R crítica (apagado seguro)**: estas consolas portátiles de bajo coste carecen de un circuito de apagado por software; el interruptor físico corta la corriente de la batería directamente. Si el sistema está leyendo o escribiendo datos en la MicroSD cuando se mueve el interruptor, la tarjeta se corrompe de inmediato de forma irreversible. Al tener la consola solo 32MB de RAM libre, cargar carpetas masivas con miles de juegos satura el frontend GMenuNX y provoca escritura constante de archivos de intercambio (swap) en la tarjeta. Es técnicamente obligatorio usar un filtro 1G1R estricto (con herramientas como retool) para limitar los conjuntos a no más de 150-200 títulos esenciales por consola, reduciendo al mínimo la actividad de lectura/escritura en disco.
