# Flashcarts retro — Guía de referencia

Resumen del estado de cada cartucho, organización de los romsets en mi PC
(carpeta `_SD`) y enlaces al software necesario.

> **Regla de oro común a los clones (EDGB y FlashGear):** nunca actualizar el
> firmware. Son clones de EverDrive y una actualización oficial de Krikzz puede
> dejarlos inservibles (brick). Dejarlos con el firmware que traen de fábrica.

---

## 1. EZ-Flash Omega (base) — Game Boy Advance (+ GB/GBC/NES por emulación)

Cartucho principal para GBA. Reproduce GBA de forma nativa; GB/GBC/NES por
emulación interna (Goomba Color). Versión **base** (no Definitive Edition).

**Características**
- Sistemas: GBA (`.gba`) nativo; GB (`.gb`), GBC (`.gbc`), NES (`.nes`) emulados.
- Carga ROMs en crudo (sin parchear).
- Guardado por SRAM: **esperar ~5 segundos tras guardar antes de apagar**.
- Límite del kernel: **512 archivos / 256 carpetas por directorio**.
- Nombres de archivo: **menos de 100 caracteres**.
- SD: FAT32 (≤32 GB) o exFAT (>32 GB), clúster **32 KB**.

**Cómo ha quedado mi romset (`_SD`)**
- ROMs descomprimidas desde los zips originales.
- Duplicados regionales apartados en `_Duplicados` (no copiados a la SD).
- Nombres limpios: eliminado todo lo posterior al primer paréntesis.
- Organizadas en **carpetas por letra** (`#`, `A`–`Z`), holgadamente bajo el
  límite de 512.
- En la SD, una carpeta por sistema (`GBA`, `GB`, `GBC`).

**Buenas prácticas para no corromper la SD**
- Contar hasta 5 tras guardar dentro del juego antes de apagar / volver al menú.
- En GB/GBC (emulador): guardar normal → **L+R** → esperar ~5 s → salir. **No usar "Exit".**
- Insertar la SD antes de encender; no extraer el cartucho con la consola encendida.
- Respaldar la carpeta `SAVER` al PC periódicamente.
- Mantener el kernel al día y usar tarjeta de marca.

**Software / referencia**
- Descargas oficiales (kernel, cheats, thumbnails): https://www.ezflashomega.com/pages/EZ-Flash-Omega-Downloads.html
- Kernel comunitario veikkos (backup automático de saves): https://github.com/veikkos/omega-kernel/releases/
- Guía / troubleshooting oficial: https://www.ezflashomega.com/pages/EZ-Flash-Troubleshooting-And-Quick-Start-Guide.html

---

## 2. EZ-Flash Junior — Game Boy / Game Boy Color (hardware real)

Cartucho dedicado a GB/GBC, ejecutados en hardware real (sin emulación).

**Estado del firmware: flasheado a FW4 / Kernel 1.04e** (versión estable, con el
manejo de ficheros mejorado: hasta 7000 archivos por carpeta y nombres de 254
caracteres). Se hizo el downgrade desde la RC de FW5/K1.05e que traía.

**Características**
- Sistemas: Game Boy (`.gb`) y Game Boy Color (`.gbc`).
- SD: **FAT32, clúster 32 KB**. Tarjeta de 4 GB o más, de marca y rápida.
- Con FW4/K1.04e: sin el antiguo límite de 100 archivos por carpeta.

**Cómo ha quedado mi romset (`_SD`)**
- ROMs descomprimidas `.gb` / `.gbc`.
- Duplicados regionales apartados en `_Duplicados`.
- Nombres limpios (sin paréntesis): además evita los "File System Error" por
  caracteres especiales.
- Organización por letras reutilizable (cabe de sobra bajo el límite de 7000).
- En la SD: `ezgb.dat` (kernel) + carpetas de ROMs + `SAVER` (se crea sola).

**Flasheo (referencia, ya hecho)**
- Tarjeta de marca verificada (H2testw/F3), FAT32 32 KB.
- `ezgb.dat` (SHA1 `43c76dc2b206907a68a1b3d320324d2d4438b7f3`) + `Update_FW4.gb` en la raíz.
- Consola con pilas nuevas o enchufada. Ejecutar `Update_FW4.gb` como un juego,
  pulsar A, esperar el parpadeo (~10 s), apagar cuando lo pida (**no reset**).
- Guardar copia de los archivos de kernel/firmware en el PC por si hay que recuperar.

**Software / referencia**
- Descargas oficiales: https://www.ezflashjr.com/pages/Downloads.html
- Descargas (web alternativa EZ-Flash): https://www.ezflash.cn/download/
- H2testw / verificación de tarjetas: https://zadig.akeo.ie/ *(para Zadig)* — para H2testw buscar "H2testw" o usar F3 en Linux/Mac.

> Nota: la SD de la Junior debe ser de marca y rápida, sobre todo para flashear
> (una tarjeta lenta puede colgar el cartucho en LOADING/OSINIT).

---

## 3. EDGB — Clon de EverDrive-GB (Game Boy / Game Boy Color)

Cartucho con carcasa humo y sticker genérico "GAME COLOR / Made in China"
(grabado trasero `V2.2 06.06.2019`). Clon de una versión antigua del
EverDrive-GB.

**Características**
- Sistemas: Game Boy (`.gb`) y Game Boy Color (`.gbc`).
- Guarda directamente en la SD (sin save states, sin RTC).
- Compatible con ROM only, MBC1, MBC2, MBC3, MBC5 hasta 8 MB.
- Tarjeta formateada en **FAT32**.

**Cómo ha quedado mi romset (`_SD`)**
- ROMs descomprimidas `.gb` / `.gbc`.
- Duplicados regionales apartados en `_Duplicados` (no se copian a la SD).
- Nombres limpios: eliminado todo lo posterior al primer paréntesis.
- En la SD: ROMs + carpeta `SAVE` (se crea sola al guardar). No copiar `_Duplicados`.

**Software / referencia**
- No requiere software propio: copiar ROMs a la SD y listo.
- Ficha de referencia del clon: https://www.thegeekghost.com/2020/08/02/game-color-edgb-flash-cart/
- Base de datos de flashcarts GB: https://gameboy.github.io/wiki/flashcarts

> ⚠️ No actualizar el firmware (corre OS v1 de EverDrive-GB modificado, no actualizable).

---

## 4. FlashGear Pro (GG) — Clon de EverDrive para Sega Game Gear / Master System

Clon de EverDrive de Game Gear comprado en AliExpress (versión tipo `Pro v9`).
La microSD va **dentro de la carcasa** (hay que abrir el tornillo trasero para
acceder a ella; ranura push-push interna: empujar y soltar, no tirar).

**Características**
- Sistemas: Game Gear (`.gg`) y Master System (`.sms`).
- Menú estilo EverDrive, lectura desde SD.
- Tarjeta formateada en **FAT32**.
- Algunas unidades llevan pila interna para el guardado.

**Cómo ha quedado mi romset (`_SD`)**
- ROMs descomprimidas.
- Duplicados regionales apartados en `_Duplicados`.
- Nombres limpios: eliminado todo lo posterior al primer paréntesis.
- Separadas por sistema en subcarpetas:
  - `_SD\GG`  → roms `.gg`
  - `_SD\SMS` → roms `.sms`
- En la SD: carpetas `GG` y `SMS` + carpeta `SAVE` existente (no tocar).

**Síntoma típico a recordar**
- Si arranca directo a un juego sin pasar por el menú = la SD no se está
  leyendo (formato o tarjeta). Solución: SD en FAT32 y/o tarjeta de marca.
  Si nada se lee, probar otra SD; algún caso se ha resuelto reasentando la pila interna.

**Software / referencia**
- No requiere software propio: copiar ROMs a la SD.
- Hilo de referencia/diagnóstico (FR): https://www.gamopat-forum.com/t118843-flashgear-pro-pour-game-gear
- Vídeo de referencia: https://www.youtube.com/watch?v=Hro7nRmc43s

> ⚠️ No actualizar el firmware (clon de EverDrive; el update oficial de Krikzz puede brickearlo).

---

## 5. Neo Geo Pocket Flash Masta USB — Neo Geo Pocket / NGP Color

**Caso especial: no usa SD ni carpetas.** Se conecta por micro USB al PC y se
flashean las ROMs a la memoria del cartucho con software propio.

**Características**
- Sistemas: Neo Geo Pocket y NGP Color (`.ngp` / `.ngc`).
- Capacidad: **1 ROM de 32 Mbit**, o **2 ROMs de 16 Mbit** cada una.
- Selección del juego activo mediante un **interruptor físico** del cartucho.
- Los juegos cargan como un cartucho real (sin menús ni tiempos de carga).
- El software también permite respaldar la partida guardada.

**Cómo ha quedado mi romset**
- No hay `_SD` ni organización por carpetas para este cartucho.
- Solo necesito mis ROMs `.ngp` / `.ngc` sueltas y descomprimidas, listas para
  seleccionarlas en el software de flasheo.

### Instalación del software en Windows

1. **Descargar el software Flash Masta** desde la página oficial de descargas:
   - https://www.flashmasta.com/software-downloads/
2. **Instalar el driver USB con Zadig.** El cartucho necesita un driver para que
   Windows lo reconozca:
   - Descargar Zadig: https://zadig.akeo.ie/
   - Conectar el Flash Masta al PC por micro USB.
   - Abrir Zadig, seleccionar el dispositivo Flash Masta en la lista y asignarle
     el driver (WinUSB / libusb) que indique la documentación.
3. **Instalar y abrir el software Flash Masta** descargado en el paso 1.

> Nota: el cartucho no incluye instrucciones físicas; la guía está en la web.
> Algún material de ayuda de la marca puede mostrar la variante de WonderSwan,
> pero el procedimiento es equivalente.

### Cómo pasar ROMs

1. Conectar el Flash Masta al PC con el cable micro USB.
2. Abrir el software Flash Masta.
3. Elegir la ranura/slot a escribir (recordar el límite: 1×32 Mbit o 2×16 Mbit).
4. Seleccionar el archivo de ROM (`.ngp` / `.ngc`) y flashearlo
   (el proceso es rápido, ~10 segundos).
5. Para usar dos juegos, repetir en el segundo slot con una ROM de ≤16 Mbit.
6. En la consola, usar el **interruptor físico** del cartucho para elegir qué
   slot/juego se ejecuta.
7. (Opcional) Usar la función de backup del software para respaldar la partida
   guardada antes de sobrescribir un slot.

**Software / referencia**
- Descargas oficiales (software): https://www.flashmasta.com/software-downloads/
- Zadig (driver USB): https://zadig.akeo.ie/
- Web del fabricante: https://www.flashmasta.com/
- Guía de montaje / primer vistazo: https://www.igorkromin.net/index.php/2018/07/01/assembly-and-first-look-at-the-flash-masta-usb-game-cart-for-neo-geo-pocket/

---

## Recordatorios generales

- **Zips originales = fuente de la verdad.** Todo el trabajo se hace sobre copias
  en `_SD`; los zips no se tocan.
- **FAT32** para EDGB, FlashGear y Junior; Omega admite exFAT en >32 GB. Clúster
  **32 KB**. Tarjetas de **marca** (SanDisk, Samsung, Kioxia, Netac…), evitar genéricas.
- **Verificar tarjetas nuevas** con H2testw/F3 antes de usarlas para flashear.
- **Esperar tras guardar** en la Omega (~5 s) y salir bien en GB/GBC (L+R, no "Exit").
- **Respaldar las carpetas de saves** (`SAVER` / `SAVE`) al PC de vez en cuando.
- **No copiar `_Duplicados`** a ninguna tarjeta: es solo la criba de trabajo.
- **No actualizar firmware** en los clones (EDGB y FlashGear). En los EZ-Flash sí
  se puede/recomienda mantener el kernel oficial al día.
