# GarlicOS

GarlicOS es un Custom Firmware (CFW) de código abierto y alto rendimiento diseñado específicamente para exprimir al máximo el hardware de las consolas portátiles Anbernic de primera generación. Destaca en la escena de la emulación por introducir un sistema operativo ligero basado en hilos independientes que permite funciones premium como el cambio instantáneo de juego mediante puntos de guardado automático en frío (similar al funcionamiento de OnionOS y FunKey OS), un arranque ultra-rápido en menos de 5 segundos directamente al menú principal y un consumo de batería optimizado en modo de suspensión profunda. Su interfaz gráfica prescinde de frontends pesados como EmulationStation en favor de un menú visual basado en texto y temas personalizables en bloques.

## Dispositivos aplicables

- Anbernic RG35XX (Original)

## Tipo de instalación

Imagen flasheada a SD (`.img`), instalación limpia de fábrica. Admite e integra de forma nativa configuraciones de tarjeta única o esquemas avanzados de doble tarjeta (SD1 sistema, SD2 ROMs).

## Requisitos previos

- Tarjetas MicroSD compatibles: una de 16GB o 32GB de buena calidad para el sistema operativo (SD1); una secundaria opcional de 64GB a 128GB de alta velocidad para juegos (SD2).
- Nota técnica: evitar tarjetas de 256GB o superiores; la controladora de la RG35XX original sufre retrasos severos en los tiempos de acceso al indexar directorios masivos de gran tamaño.
- Software de flasheo: Rufus (altamente recomendado para GarlicOS) o BalenaEtcher.
- Herramienta de particionado: MiniTool Partition Wizard o `gparted` en WSL/Linux. Obligatoria para expandir las particiones si se usa el esquema de una sola tarjeta.

## Descarga

- Sitio web oficial del desarrollador: la imagen oficial estable consolidada y sus actualizaciones menores se descargan de la web oficial del creador Black-Seraph — <https://www.patreon.com/posts/garlicos-for-76561333>
- Archivos requeridos: descargar la imagen base comprimida (ej. `garlicos-rg35xx-v1.4.9.7z`). Asegúrate de usar la versión estable 1.x para el modelo original.

## Preparación de almacenamiento

El esquema de almacenamiento de GarlicOS es uno de los más estrictos y particulares:

- **SD1 (Sistema)**: el software de flasheo crea automáticamente cuatro particiones lógicas en formato Linux y FAT32 (incluyendo las particiones ocultas del kernel y una partición visible llamada `ROMS` si se usa una configuración de tarjeta única).
- **SD2 (ROMs — ranura TF2 / segundo slot)**: debe formatearse obligatoriamente en FAT32 con un tamaño de clúster de 32 KB para garantizar la velocidad de los puntos de guardado automático.
- **Nomenclatura corta de carpetas (muy crítica)**: GarlicOS utiliza abreviaturas estrictas y en MAYÚSCULAS para nombrar los directorios de las consolas en la raíz de la partición de juegos. Hay que mapear los volcados hacia rutas exactas como `/FC/` (NES), `/SFC/` (SNES), `/MD/` (Mega Drive), `/GBA/`, `/GBC/` o `/PS/` (PlayStation 1). Si se usan nombres largos como `/snes/` o `/sfc/` en minúsculas, el menú los ignora por completo.

## Instalación

1. Inserta la SD1 en el ordenador.
2. Descomprime el archivo `.7z` de GarlicOS hasta obtener el archivo ejecutable `.img`.
3. Abre la herramienta de flasheo (ej. Rufus), selecciona el archivo `.img` y elige como unidad destino la MicroSD. Haz clic en Escribir/Iniciar.
4. **Paso de redimensionamiento (solo para configuración de tarjeta única)**: al finalizar el flasheo, abre MiniTool Partition Wizard o gparted en WSL. La última partición (etiquetada como `ROMS`) mide apenas unos megabytes; hay que expandirla manualmente hasta el final del espacio libre no asignado de la tarjeta para poder meter los juegos. Si se usa el método de doble tarjeta, este paso se puede omitir.

## Primer arranque

1. Introduce la SD1 flasheada en la ranura principal de la consola (TF1/INT). Deja la ranura TF2 completamente vacía.
2. Enciende la consola. GarlicOS inicia en frío en menos de 5 segundos mostrando el menú principal limpio.
3. Si se va a usar una configuración de doble tarjeta, apaga la consola manteniendo presionado el botón de Power por un par de segundos. Inserta la SD2 formateada en FAT32 (con la estructura de carpetas cortas pre-cargada) en la ranura TF2 y enciende el dispositivo. El sistema detecta la segunda ranura de forma transparente e indexa los juegos de inmediato.

## Configuración post-instalación

- **Volcado de ROMsets y BIOS**: transfiere las colecciones de juegos validadas a las carpetas cortas de la SD2. Es un requisito inamovible copiar los archivos de BIOS obligatorios dentro de una carpeta centralizada llamada `/BIOS/` (estrictamente en mayúsculas) ubicada en la raíz de la partición de juegos.
- **Tratamiento de carátulas (Imgs)**: GarlicOS no soporta archivos indexadores XML planos (`gamelist.xml`). El menú lee las carátulas por correspondencia directa de nombres planos en formato `.png` ubicadas estrictamente dentro de una subcarpeta llamada `Imgs` (con la primera letra en mayúscula) dentro de la carpeta de cada consola (ej. `/SFC/Imgs/`). El archivo de imagen debe llamarse exactamente igual que la ROM.
- **Acción crítica de pipeline (para evitar cuelgues)**: la pantalla de la RG35XX tiene una resolución de 640x480 píxeles. GarlicOS procesa las imágenes en memoria RAM en tiempo real al hacer scroll rápido. Hay que procesar las portadas reescalándolas de forma masiva a un ancho máximo estricto de 320 píxeles (o un alto máximo de 480 píxeles) y guardándolas en formato PNG de 8 bits (indexado). Introducir carátulas HD o PNG transparentes de 32 bits satura de inmediato la memoria de vídeo del procesador, provocando que los nombres de los juegos desaparezcan de la pantalla o que la consola se congele al navegar por los menús.

## Notas

- **Tratamiento de ROMsets Arcade eficientes**: debido a que la RG35XX original cuenta con un procesador Actions ATM7039S modesto de 32 bits, los núcleos arcade modernos de RetroArch sufren ralentizaciones severas. El estándar absoluto recomendado por la comunidad es compilar un subset arcade basado estrictamente en el archivo DAT oficial de MAME 2003-Plus (romset `0.78-plus`) para arcade general, y núcleos optimizados de FinalBurn Neo en formato Non-Merged para las placas de Capcom y Neo-Geo. Es obligatorio incluir el archivo de BIOS `neogeo.zip` adaptado a esa misma era en la raíz de la carpeta arcade para garantizar la compatibilidad.
- **Optimización del formato de consolas en disco**: el emulador de PlayStation 1 integrado rinde a 60 FPS estables. Para maximizar el rendimiento y el espacio, es directriz mandatoria realizar la conversión masiva de las ISOs/BIN al formato comprimido CHD (v5). GarlicOS lee los CHDs de forma nativa, lo que reduce el peso a la mitad en la tarjeta y alivia el bus de lectura de la MicroSD al cargar pistas de audio.
- **Gestión 1G1R de la interfaz**: dado que GarlicOS lee la tarjeta SD a pelo en cada scroll en tiempo real, tener carpetas saturadas con más de 1000 archivos provoca que el listado tarde varios segundos en abrirse al entrar al sistema. Aplicar un filtro 1G1R estricto (con herramientas como retool) para dejar subsets limpios de títulos esenciales garantiza una respuesta instantánea de la interfaz y un menú impecable.
