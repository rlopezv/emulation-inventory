# twigUI

twigUI es una distribución ligera y minimalista optimizada para la GKD Pixel 2, basada en el ecosistema y la filosofía de diseño de *spruceOS* (originalmente creado para la Miyoo Mini). Reemplaza por completo el entorno pesado de EmulationStation por un frontend de texto y menús rápidos, priorizando el rendimiento, la simplicidad visual y la optimización de la batería en pantallas pequeñas.

## Dispositivos aplicables

- GKD Pixel 2 (RK3326S)

## Tipo de instalación

- **Instalación limpia sobre tarjeta microSD única (TF1)**: se flashea una imagen base limpia en la tarjeta de memoria, reemplazando por completo el sistema operativo de fábrica.

## Requisitos previos

- Una tarjeta microSD de calidad (ej. SanDisk o Samsung) de al menos 64 GB o 128 GB.
- Un ordenador con lector de tarjetas microSD.
- Un software de flasheo de imágenes de disco como [BalenaEtcher](https://balena.io) o [Rufus](https://rufus.ie).
- Un software gestor de particiones como **MiniTool Partition Wizard** o **DiskGenius** (imprescindible en sistemas Windows para expandir la partición de almacenamiento de juegos).
- Un descompresor de archivos como [7-Zip](https://7-zip.org) o WinRAR.

## Descarga

Las imágenes oficiales y las actualizaciones del frontend optimizado se descargan directamente desde el repositorio del proyecto: [github.com/spruceUI/twigUI](https://github.com/spruceUI/twigUI).

## Preparación de almacenamiento

1. **Copia de seguridad**: respalda por completo tus carpetas de `Roms` y `Bios` desde tu tarjeta actual antes de proceder.
2. **Extracción del firmware**: descarga el archivo comprimido oficial y descomprímelo con 7-Zip para obtener el archivo de imagen ejecutable con extensión `.img`.

## Instalación

1. Conecta la tarjeta microSD de destino a tu ordenador.
2. Ejecuta tu software de flasheo preferido ([BalenaEtcher](https://balena.io) o Rufus).
3. Selecciona la imagen `.img` de twigUI descargada y selecciona tu tarjeta microSD como destino. Haz clic en **Flashear / Escribir**.
4. **Expansión de la partición de juegos (Obligatorio en Windows)**: al finalizar el proceso, abre un gestor de discos avanzado como [MiniTool Partition Wizard](https://partitionwizard.com). Localiza la partición de almacenamiento reservada para el usuario (etiquetada habitualmente como `ROMS` o `SDCARD`), selecciona la opción **Extender / Expandir** para asignarle todo el espacio libre restante en la tarjeta y aplica los cambios.

## Primer arranque

1. Introduce la microSD con twigUI en la ranura **TF1** de la consola.
2. Enciende el dispositivo manteniendo presionado el botón de encendido.
3. El sistema realizará una carga inicial automatizada y una reorganización de directorios internos. **No apagues la consola** ni presiones ningún botón hasta que visualices el menú principal minimalista de twigUI basado en texto.

## Configuración post-instalación

- **Estructura de carpetas**: vuelve a conectar la tarjeta al ordenador si deseas transferir tus juegos. twigUI utiliza la nomenclatura estándar de directorios de spruceOS para las carpetas de juegos (`/Roms/GBA`, `/Roms/PSX`, etc.).
- **Gestión de carátulas (Opcional)**: el sistema soporta visualización de imágenes sencillas en miniatura al lado del texto. Coloca las carátulas dentro de una carpeta llamada `Imgs` dentro del directorio de cada emulador.
- **Acceso Remoto**: si configuras la red mediante el adaptador Wi-Fi USB, puedes conectarte vía SSH mediante los comandos de terminal utilizando las credenciales nativas del sistema:
  - **Usuario**: `root`
  - **Contraseña**: `spruce`
- **Atajos de control rápidos**:
  - `Botón Menú (Corta pulsación)`: Regresa instantáneamente al lanzador o cierra el emulador actual.
  - `Botón Menú + Flecha Arriba / Abajo`: Sube o baja el brillo de la pantalla directamente desde cualquier juego.
  - `Select + Start (Dos pulsaciones)`: Atajo universal de RetroArch para salir de manera segura.

## Notas

- **Interfaz Minimalista**: diseñado específicamente para la pantalla compacta de la Pixel 2; elimina los menús de carga lentos y pesados de los frontends tradicionales.
- **Eficiencia en Carga**: permite apagar la retroiluminación de la pantalla por completo mientras el dispositivo permanece conectado al cargador físico.
- **Apagado por inactividad**: incluye scripts que apagan la consola de forma segura tras un periodo de inactividad programado, protegiendo la salud de la batería.
- **Limitación conocida**: no incluye de forma nativa la capa estética ni los carruseles visuales de EmulationStation de los sistemas basados en stock.
- Alternativas para el mismo dispositivo: `RogueOS` (mejor soporte PortMaster y apps multimedia), `plumOS-GKD` (enfoque en audio mejorado y cores ligeros), `KNULLI (Scarab)` (ver `docs/guides/cfw/knulli.md`). Ver comparativa completa en `docs/distributions.md`.
