# MinUI

MinUI es un Custom Firmware (CFW) de código abierto y diseño ultra-minimalista enfocado exclusivamente en la velocidad, la eficiencia de la batería y la eliminación de cualquier distracción visual. A diferencia de los frontends pesados, MinUI prescinde por completo de carátulas, vídeos, música de fondo y metadatos complejos; utiliza una interfaz de texto plano fluida basada en listas que carga de forma instantánea. Su arquitectura se centra en lanzar emuladores nativos altamente optimizados (a través de núcleos Libretro/RetroArch personalizados de bajo consumo) que se ejecutan a velocidad completa con menús unificados de guardado y configuración.

## Dispositivos aplicables

- TrimUI Model S (TrimUI Smart clásica de tamaño llavero)
- Anbernic RG35XX (Original / Plus / H / SP / 28XX)
- Miyoo Mini / Miyoo Mini Plus
- Nota: debido a su popularidad, el desarrollador original (shauninman) y la comunidad mantienen ramas específicas adaptadas a múltiples SoC portátiles económicos, garantizando la misma experiencia unificada de texto en todas las pantallas.

## Tipo de instalación

Extracción a SD existente. No requiere el flasheo tradicional de imágenes `.img` ni destruye las particiones físicas de la tarjeta. La instalación se realiza preparando el almacenamiento e introduciendo directamente una estructura de archivos comprimidos en la raíz, coexistiendo de forma nativa con el arranque básico del dispositivo.

## Requisitos previos

- Tarjeta MicroSD fiable: se recomienda 32GB, 64GB o como máximo 128GB (SanDisk Ultra o Samsung EVO). Al no gestionar elementos multimedia pesados, un tamaño reducido es más que suficiente para miles de juegos de 8 y 16 bits.
- Formateador de almacenamiento: herramientas como GUIFormat (Windows) o utilidades nativas en WSL/Linux para asegurar un sistema de archivos compatible.
- Descompresor de archivos: 7-Zip, WinRAR o `unzip` en la terminal de WSL.

## Descarga

- Repositorio oficial de la escena: los paquetes de instalación consolidados se descargan de forma centralizada desde el repositorio principal de desarrollo — <https://github.com/shauninman/MinUI/releases>
- Nota técnica: descargar siempre el archivo comprimido completo que corresponda a la arquitectura o marca de la consola (ej. `MinUI-TrimUI-vX.X.X.zip` o el pack multi-dispositivo unificado).

## Preparación de almacenamiento

- **SD de juegos y sistema (única)**: la tarjeta MicroSD debe estar formateada obligatoriamente en FAT32 con un tamaño de clúster de 32 KB para asegurar que los scripts de texto del firmware se lean con la menor latencia posible.
- **Nomenclatura estricta de carpetas**: MinUI destaca porque no utiliza las abreviaturas estándar de las consolas para sus carpetas. Exige nombres de directorios descriptivos en inglés y en mayúscula inicial estricta dentro de una carpeta raíz llamada `/Roms/`. Hay que mapear los volcados hacia rutas exactas como `/Roms/Game Boy/`, `/Roms/Game Boy Advance/`, `/Roms/Nintendo Entertainment System/`, `/Roms/Super Nintendo Entertainment System/` o `/Roms/PlayStation/`. Si se usa una abreviatura (como `/snes/`), el menú ignora la carpeta por completo.

## Instalación

1. Inserta la MicroSD en el ordenador y asegúrate de que esté formateada correctamente en FAT32.
2. Descomprime el archivo `.zip` de MinUI descargado.
3. Copia todo el contenido extraído (incluyendo la carpeta `MinUI.zip` sin descomprimir que viene dentro del pack, y los archivos de arranque del sistema como `dboot.bin` o carpetas de sistema según la consola) directamente en la raíz de la tarjeta MicroSD.

## Primer arranque

1. Inserta la MicroSD con los archivos en la ranura principal de la consola aplicable.
2. Enciende el dispositivo. El cargador de arranque nativo detecta los archivos de MinUI e inicia un script automático de instalación (se muestra una pantalla de carga de texto minimalista instalando componentes).
3. El sistema inicializa los entornos de ejecución en segundos y carga directamente el menú principal de texto limpio de MinUI. Al ser una instalación por extracción directa, la tarjeta conserva su tamaño físico original de inmediato.

## Configuración post-instalación

- **Volcado de datos**: transfiere las colecciones de juegos en las subcarpetas con nombres largos dentro de `/Roms/`. Es un requisito obligatorio copiar los archivos de BIOS que lo requieran dentro de una subcarpeta llamada `Bios` con mayúscula inicial dentro de la carpeta del propio sistema (ejemplo: `/Roms/PlayStation/Bios/scph1001.bin`).
- **Tratamiento de carátulas (cero multimedia)**: MinUI no soporta carátulas ni listas indexadas en archivos XML planos (`gamelist.xml`). El frontend lee de forma directa la estructura física de archivos de la tarjeta SD en tiempo real, por lo que no es necesario realizar ningún tipo de raspado multimedia (scraping). El nombre físico del archivo de la ROM (limpio de tags de región si se prefiere) será exactamente el texto que se muestre en el menú de la consola.

## Notas

- **Soporte de emuladores de expansión (Extras)**: el paquete base de MinUI es extremadamente recortado (incluye solo consolas clásicas de 8 y 16 bits). Para añadir sistemas avanzados como Sega CD, PC Engine, Arcade o Pokémon Mini, hay que descargar el paquete oficial de extensiones (`MinUI-Extras.zip`) y arrastrar sus carpetas dentro de la raíz de la SD para sumar los nuevos núcleos Libretro optimizados.
- **Tratamiento de ROMsets Arcade**: el soporte arcade de MinUI es muy restrictivo y está simplificado al máximo. Utiliza un núcleo optimizado basado en versiones tempranas de FinalBurn o MAME. Hay que compilar subsets arcade limpios utilizando los DATs de MAME 0.37b5 o versiones Non-Merged de FinalBurn para garantizar que arranquen en esta interfaz sin menús avanzados de configuración de botones. Las ROMs deben ir en la carpeta `/Roms/Arcade/`.
- **Optimización total para PlayStation 1**: a pesar de su enfoque minimalista, el emulador de PS1 integrado es de rendimiento extremo. Es directriz obligatoria realizar la conversión masiva de las ISOs/BIN a formato comprimido CHD (v5). MinUI lee los CHDs de forma impecable, lo que reduce el espacio a la mitad en la tarjeta y acelera la carga en procesadores de bajo consumo.
- **Gestión 1G1R y organización de menús**: dado que MinUI lee la tarjeta SD a pelo en cada scroll, tener carpetas con más de 1000 archivos sueltos ralentiza la navegación por las listas de texto. Es técnicamente necesario aplicar un filtro 1G1R estricto (con herramientas como retool) para dejar subsets limpios de títulos esenciales. Además, el firmware permite organizar los juegos en subcarpetas alfabéticas o carpetas personalizadas (ej. `/Roms/Super Nintendo Entertainment System/Traducidos/`) para fragmentar los listados largos y mantener el menú impecable.
