# RogueOS

RogueOS es una modificación profunda (Stock Mod) del sistema operativo de fábrica de la GKD Pixel 2, desarrollada por Ninoh-FOX. Al partir de la base de fábrica en vez de reemplazarla por completo, aprovecha los drivers nativos de pantalla y energía del dispositivo.

## Dispositivos aplicables

- GKD Pixel 2 (RK3326S)

## Tipo de instalación

- **Flasheo completo en tarjeta microSD única (TF1)**: se sustituye íntegramente el contenido de la tarjeta original mediante una imagen de disco externa, borrando los datos previos.

## Requisitos previos

- Una tarjeta microSD de calidad (ej. SanDisk o Samsung) de al menos 64 GB o 128 GB.
- Un ordenador con lector de tarjetas microSD.
- Un software de flasheo de imágenes de disco como [BalenaEtcher](https://balena.io) o [Rufus](https://rufus.ie).
- Un software gestor de particiones como **MiniTool Partition Wizard** o **DiskGenius** (imprescindible en sistemas Windows para expandir el almacenamiento tras el flasheo).
- Una aplicación descompresora compatible con archivos divididos (ej. [7-Zip](https://7-zip.org) o WinRAR).

## Descarga

Las imágenes oficiales actualizadas y los parches de rendimiento se descargan directamente desde el repositorio oficial del proyecto: [github.com/Ninoh-FOX/PIXEL2-ROGUE-OS/releases](https://github.com/Ninoh-FOX/PIXEL2-ROGUE-OS/releases).

*Nota: La distribución suele venir dividida en múltiples archivos comprimidos (ej. `RogueOS.zip`, `RogueOS.z01`, `RogueOS.z02`) que deben ubicarse en la misma carpeta antes de iniciar la extracción.*

## Preparación de almacenamiento

1. **Respaldar el sistema original**: realiza una copia de seguridad completa del contenido de tu MicroSD de fábrica, prestando especial atención a tus carpetas personales de `Roms` y `Bios`.
2. **Extraer la imagen**: abre el archivo principal `.zip` con un descompresor como 7-Zip para unificar los fragmentos descargados. Obtendrás un único archivo ejecutable con extensión `.img`.

## Instalación

1. Introduce la tarjeta MicroSD de destino en el ordenador.
2. Abre tu software de flasheo ([BalenaEtcher](https://balena.io) o Rufus).
3. Selecciona el archivo de imagen `.img` extraído previamente.
4. Elige tu tarjeta MicroSD como unidad de destino y ejecuta la acción de **Flashear / Escribir**.
5. **Expandir partición de juegos (Obligatorio en Windows)**: una vez finalizado el flasheo, abre un gestor de discos como [MiniTool Partition Wizard](https://partitionwizard.com). Localiza la partición de nombre `ROMS` y utiliza la función **Extender / Expandir** para que ocupe todo el espacio no asignado restante de la tarjeta microSD. Confirma los cambios aplicando los comandos.

## Primer arranque

1. Introduce la MicroSD recién configurada en la ranura **TF1** de la GKD Pixel 2.
2. Enciende la consola manteniendo pulsado el botón de encendido.
3. El sistema operativo ejecutará un script automatizado de inicialización interna de manera transparente durante este primer encendido. No toques ningún botón ni apagues la consola hasta que aparezca la interfaz principal de EmulationStation.

## Configuración post-instalación

- **Transferencia de juegos y BIOS**: puedes extraer de nuevo la tarjeta microSD para transferir tu contenido guardado a las carpetas correspondientes dentro de la partición expandida `ROMS`.
- **Acceso por SSH y Red**: si deseas conectarte a la consola mediante Wi-Fi local para gestionar archivos o configuraciones avanzadas, puedes abrir una terminal SSH en tu PC usando las siguientes credenciales de fábrica:
  - **Host**: Dirección IP asignada a la GKD Pixel 2.
  - **Usuario**: `root`.
  - **Contraseña**: `rogue`.
- **Lanzamientos nativos (PortMaster)**: accede a la sección de aplicaciones del frontend para ejecutar las herramientas de red que actualizarán el catálogo directo de PortMaster de forma nativa.
- **Mapeo de comandos rápidos (Atajos de RetroArch)**:
  - `Menú`: Abre el menú de configuración interna de RetroArch.
  - `Select + Start`: Cierra el juego de forma segura regresando al menú principal.
  - `Select + X`: Captura de pantalla directa.
  - `Select + R1 / L1`: Guardar estado / Cargar estado de forma rápida.

## Notas

- **PortMaster integrado**: permite ejecutar de forma nativa ports ligeros de PC (ej. Celeste, Stardew Valley).
- **Gestión de energía**: avisos por vibración al 10% y 5% de batería, apagado automático seguro al 1% para evitar corrupción de la SD.
- **Mejoras multimedia**: RetroArch actualizado y reproductores de música optimizados que funcionan con la pantalla apagada.
- **Desventaja conocida**: mantiene el tiempo de arranque de fábrica, en torno a los 30 segundos.
- Alternativas para el mismo dispositivo: `plumOS-GKD` (arranque/sleep más rápidos), `twigUI` (interfaz minimalista tipo spruceOS), `KNULLI (Scarab)` (ver `docs/guides/cfw/knulli.md`). Ver comparativa completa en `docs/distributions.md`.
