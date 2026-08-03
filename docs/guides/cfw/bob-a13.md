# BOB A13 (Batocera v35b)

BOB A13 es una compilación comunitaria especial de Batocera (v35b) para el procesador Rockchip RK3128, distinta de las variantes de BOB (Best of the Best) basadas en MiyooCFW (F1C100S) o ArkOS. No comparte código ni frontend con esas otras variantes pese al nombre compartido.

## Dispositivos aplicables

- PowKiddy A13 (mini bartop plegable, RK3128)

## Tipo de instalación

Reemplazo completo del sistema operativo original (Firmware personalizado / Custom Firmware) mediante tarjeta MicroSD dedicada.

## Requisitos previos

- Consola PowKiddy A13 con batería cargada.
- Tarjeta MicroSD de calidad (SanDisk o Samsung recomendadas) de al menos 16GB o superior (según el volumen de ROMs).
- Lector de tarjetas MicroSD para PC.
- Herramienta para flashear imágenes de disco (BalenaEtcher o Rufus).
- Herramienta para gestionar particiones (MiniTool Partition Wizard o similar, opcional).

## Descarga

- Imagen del sistema: [TODO] — enlace de descarga de la comunidad BOB A13 / archivo de Batocera v35b RK3128.
- Herramienta de flasheo: BalenaEtcher o Rufus.

## Preparación de almacenamiento

1. Inserta la tarjeta MicroSD en tu PC.
2. Si la tarjeta contiene sistemas anteriores, se recomienda realizar un formateo rápido en formato FAT32 o exFAT para limpiar tablas de particiones corruptas.
3. Asegúrate de respaldar cualquier archivo previo, ya que el proceso de instalación borrará por completo la tarjeta.

## Instalación

1. Abre tu herramienta de flasheo (ej. BalenaEtcher).
2. Selecciona el archivo de la imagen descargada (`.img` o `.img.gz`).
3. Elige la tarjeta MicroSD de destino (verifica bien la letra de la unidad para evitar borrar otros discos).
4. Haz clic en Flash! / Empezar y espera a que el proceso de escritura y verificación termine.
5. Si tu sistema operativo (Windows) te muestra avisos de "Formatear disco" al terminar, ignóralos y cancela todos.

## Primer arranque

1. Introduce la MicroSD flasheada en la ranura correspondiente de la PowKiddy A13 (con la consola apagada).
2. Enciende el dispositivo.
3. El primer arranque tardará unos minutos más de lo habitual debido a que Batocera expandirá automáticamente la partición de usuario para ocupar todo el espacio restante de la MicroSD.
4. Una vez terminado el proceso, la consola iniciará directamente en la interfaz de EmulationStation.

## Configuración post-instalación

- **Mapeo de controles**: si los botones del panel arcade no responden correctamente, mantén presionado cualquier botón para abrir el menú de configuración de mandos y mapea la palanca y los botones A/B/X/Y/L/R/Start/Select.
- **Transferencia de ROMs y BIOS**: apaga la consola, extrae la MicroSD y conéctala al PC. Verás una nueva partición accesible llamada `SHARE`. Copia tus juegos en las carpetas correspondientes dentro del directorio `/roms/`.
- **Idioma del sistema**: accede al menú principal con `Start -> System Settings -> Language` y selecciona Español. El sistema te pedirá reiniciar para aplicar los cambios.

## Notas

- No confundir con BOB (Best of the Best) para F1C100S (`bob.md`) ni con la variante ArkOS (`bob-arkos.md`); v35b es una compilación específica para RK3128, base de la imagen BOB A13.
- Al estar basado en Batocera v35b para RK3128, la consola utiliza EmulationStation como frontend y RetroArch para la mayoría de los emuladores, a diferencia de los menús basados en GMenu2X/GMenuNX de las variantes MiyooCFW.
