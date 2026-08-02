# Adam Image

Adam Image es un Custom Firmware (CFW) minimalista y optimizado basado en OpenDingux (Linux) para consolas portátiles retro con pantallas de resolución 320x240 o 480x320. Utiliza el frontend SimpleMenu y destaca por ofrecer arranque directo a la lista de sistemas, emuladores nativos altamente optimizados y soporte para RetroArch en núcleos de consolas domésticas.

En la comunidad hispanohablante (foros y canales de Telegram de creadores como eduardofilo), el proyecto se conoce bajo el concepto "Adán y Eva": la Imagen Adán es el firmware de sistema (SD1) y la Imagen Eva es un volcado complementario para la SD2.

## Dispositivos aplicables

- Anbernic RG350 (Original, M, P)
- Anbernic RG280 (V, M)
- Anbernic RG300X
- PlayGo / PocketGo V2 (y clones basados en el procesador JZ4770)

## Tipo de instalación

Imagen flasheada a SD1 (sistema) + SD2 secundaria formateada en FAT32 sin flashear (ROMs y datos).

## Requisitos previos

- Dos tarjetas MicroSD de calidad (se recomienda encarecidamente la configuración de doble tarjeta):
  - SD1 (Sistema — ranura TF1): 8GB o 16GB (SanDisk o Samsung).
  - SD2 (ROMs y datos — ranura TF2): 64GB, 128GB o 256GB, formateada en FAT32.
- Software de flasheo: BalenaEtcher o Rufus (Windows) o `dd` (WSL/Linux).
- Lector de tarjetas SD rápido y estable.

## Descarga

- Repositorio oficial: última versión estable (`.img`) — <https://github.com/eduardofilo/RG350_adam_image/releases>
- Pack de emuladores adicionales (opcional): archivos `.opk` nativos actualizados si se desea reemplazar alguna variante del sistema.
- Imagen Eva (opcional, comunidad hispanohablante): volcado complementario para la SD2 con estructura de carpetas, carátulas raspadas, configuración y romset filtrado ya listos, como alternativa a partir de una SD2 vacía — [TODO: URL exacta / fuente].

## Preparación de almacenamiento

Adam Image utiliza un sistema de dos tarjetas para independizar los archivos del sistema operativo de las colecciones de juegos:

- **SD1 (TF1)**: no requiere formateo previo; el flasheo destruye las particiones existentes para crear la estructura Linux del sistema.
- **SD2 (TF2)**: dos vías posibles:
  - Vacía y formateada en FAT32 (o exFAT con parches de kernel modernos, aunque FAT32 garantiza 100% de compatibilidad con los scripts internos de OpenDingux); el sistema genera automáticamente la estructura de carpetas en el primer arranque (ver nota de automatización más abajo).
  - Flasheada con la Imagen Eva (ver Descarga): SD2 pre-poblada con estructura, carátulas, configuración y romset ya listos, sin pasos adicionales de organización.

Nota de automatización: si se usa una SD2 vacía, en el primer arranque el sistema crea automáticamente en su raíz un árbol de directorios vacío (`/roms/apps`, `/roms/NES`, `/roms/MAME`, etc.).

## Instalación

1. Inserta la SD1 en el ordenador.
2. Abre la herramienta de flasheo (ej. BalenaEtcher), selecciona la imagen descargada (`adam_vX.X.img`) y elige como destino la MicroSD de sistema. Flashea.
3. **Paso crítico para portátiles chinas**: tras el flasheo, se monta una partición pequeña llamada `BOOT`. Entra en ella y ejecuta el script correspondiente al modelo exacto de la consola (ej. `select_kernel.bat` o el script de terminal equivalente) para renombrar el archivo del kernel específico de la pantalla (320x240 frente a 480x320). Si se omite este paso, la consola arranca con la pantalla en negro.

## Primer arranque

1. Introduce la SD1 en la ranura TF1 (normalmente la interna o superior) de la consola.
2. Introduce la SD2 (vacía) en la ranura TF2.
3. Enciende la consola; el sistema se expande automáticamente y tarda un par de minutos en configurar las particiones.
4. Al cargar la interfaz de SimpleMenu por primera vez, apaga la consola de forma segura (botón Power o menú del sistema).
5. Extrae la SD2. Al conectarla al PC/WSL, el sistema ya habrá generado la estructura exacta de carpetas de ROMs.

## Configuración post-instalación

- **Volcado de ROMs curadas**: copia los subsets de juegos en las carpetas correspondientes generadas en la SD2.
- **Metadatos y carátulas**: SimpleMenu busca las imágenes en formato `.png` dentro de una subcarpeta `.previews` dentro de la carpeta de cada sistema (ej. `/roms/SNES/.previews/`). Los nombres de las imágenes deben coincidir exactamente con el nombre de la ROM.

## Notas

- Los emuladores arcade integrados en Adam Image (no vía RetroArch) están ligados a versiones concretas de romset: FinalBurn Alpha `0.2.97.44` en formato Split/Non-Merged para CPS y Neo-Geo, y MAME `0.78` (familia `mame2003`/`mame2003-plus`) para el resto de arcade (ver `docs/arcade/arcade.md`). Un romset "completo" genérico no es directamente compatible con estos emuladores; hace falta preparar el subset en la versión y formato correctos para este CFW.
- Para consolas domésticas (Mega Drive, NES, SNES, Game Gear) usa sets No-Intro estándar (ver `docs/romsets.md`).
