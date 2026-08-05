# plumOS (GKD Pixel 2)

plumOS es un firmware personalizado (Stock Mod) optimizado para la GKD Pixel 2, desarrollado originalmente por la comunidad de modding japonesa *game-de-it*. Utiliza como cimiento el sistema operativo de fábrica (Stock OS) para heredar su estabilidad energética y compatibilidad de pantalla, pero lo modifica profundamente para limpiar los menús, acelerar drásticamente los tiempos de respuesta y añadir soporte completo para emuladores ultra-ligeros y logros retro (*RetroAchievements*).

## Dispositivos aplicables

- GKD Pixel 2 (RK3326S)

## Tipo de instalación

- **Flasheo completo en tarjeta microSD única (TF1)**: se sustituye íntegramente la instalación previa escribiendo una imagen de disco consolidada en la tarjeta de memoria del dispositivo.

## Requisitos previos

- Una tarjeta microSD de calidad (ej. SanDisk o Samsung) de al menos 64 GB o 128 GB.
- Un ordenador con lector de tarjetas microSD.
- Un software de flasheo de imágenes como [BalenaEtcher](https://balena.io) o Rufus.
- Un software gestor de particiones como **MiniTool Partition Wizard** o **DiskGenius** (indispensable para expandir el volumen en Windows).
- Un descompresor compatible con archivos fragmentados (ej. [7-Zip](https://7-zip.org) o WinRAR).

## Descarga

Las compilaciones oficiales optimizadas para este dispositivo se descargan desde el repositorio oficial del proyecto: [github.com/game-de-it/plumOS-pixel2](https://github.com/game-de-it/plumOS-pixel2).

*Nota: La imagen de instalación suele venir distribuida en tres archivos fragmentados con extensiones secuenciales (ej. `plumOS.7z.001`, `plumOS.7z.002`, `plumOS.7z.003`). Debes descargar todos los fragmentos y guardarlos en una misma carpeta antes de iniciar la extracción.*

## Preparación de almacenamiento

1. **Copia de seguridad obligatoria**: respalda tus carpetas de `Roms` y `Bios` almacenadas en tu tarjeta SD actual.
2. **Consolidar y extraer la imagen**: abre exclusivamente el primer archivo fragmentado (`.001`) utilizando 7-Zip. El descompresor unificará de forma automática todas las partes y generará un único archivo ejecutable de imagen con extensión `.img`.

## Instalación

1. Inserta la nueva tarjeta microSD en el lector de tarjetas de tu ordenador.
2. Abre tu software de flasheo preferido ([BalenaEtcher](https://balena.io) o Rufus).
3. Selecciona la imagen `.img` unificada de plumOS como archivo de origen.
4. Elige tu tarjeta microSD como disco de destino y ejecuta el proceso de **Flashear / Escribir**.
5. **Expandir partición ROMS (Obligatorio en Windows)**: al finalizar el flasheo, el almacenamiento se dividirá en varias particiones (como `EMUELEC` y `ROMS`). Abre un gestor como [MiniTool Partition Wizard](https://partitionwizard.com), localiza la partición nombrada `ROMS`, utiliza la herramienta de **Extender / Expandir** para abarcar todo el espacio libre restante de la tarjeta microSD y aplica los cambios.

## Primer arranque

1. Introduce la tarjeta microSD modificada en la ranura **TF1** de la GKD Pixel 2.
2. Enciende el dispositivo presionando el botón de Power.
3. La consola ejecutará scripts automáticos para estructurar el árbol de directorios y los archivos de configuración en el primer inicio. Permite que el proceso finalice sin pulsar ningún botón hasta que cargue la interfaz principal limpia de EmulationStation.

## Configuración post-instalación

- **Estructura de emulación**: puedes conectar la tarjeta a tu PC para transferir tus juegos. El sistema generará y respetará las carpetas estándar de almacenamiento dentro de la partición expandida `ROMS`.
- **Integración de Motores Retro**: incluye de manera nativa emuladores optimizados como *picoarch* y soporte integrado para el motor de juegos retro *Pyxel* (permitiendo la ejecución directa de archivos `.py` y `.pyxapp`).
- **Acceso Remoto por Terminal**: si utilizas un adaptador Wi-Fi USB compatible, el sistema permite la administración inalámbrica. Puedes abrir una sesión SSH en tu ordenador utilizando los siguientes parámetros predeterminados:
  - **Usuario**: `root`
  - **Contraseña**: configurada o modificable a través del archivo de parámetros de red del sistema.
- **Ecualizador de audio nativo**: el sistema arranca con un ecualizador de sonido ajustado por software que mitiga la distorsión típica de los altavoces de fábrica a volúmenes altos.

## Notas

- **Arranque y suspensión rápidos**: destaca por ofrecer el modo de espera (*sleep mode*) más ágil y eficiente en consumo energético entre las modificaciones basadas en stock.
- **Configuración limpia de RetroArch**: viene preconfigurado con ajustes que priorizan la reducción de la latencia de entrada (*input lag*) y desactiva filtros pesados de EmulationStation que ralentizan el menú.
- **Idioma predeterminado**: los menús generales de las aplicaciones se han cambiado al inglés (corrigiendo el sistema de fábrica), aunque algunas herramientas secundarias internas pueden conservar textos en chino.
- **Limitación conocida**: al igual que otros Stock Mods, el tiempo de arranque completo inicial en frío se mantiene cerca de los 30 segundos.
- Alternativas para el mismo dispositivo: `RogueOS` (mejor soporte PortMaster y apps multimedia), `twigUI` (interfaz minimalista tipo spruceOS), `KNULLI (Scarab)` (ver `docs/guides/cfw/knulli.md`). Ver comparativa completa en `docs/distributions.md`.
