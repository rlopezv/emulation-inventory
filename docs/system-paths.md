# System Paths

Rutas por defecto de ROMs, BIOS, saves, states, media y gamelist por distribución. Documento de referencia operativa para configurar, migrar y auditar colecciones.

## Convenciones

- `{sistema}` — identificador canónico del sistema según `docs/systems.md` o convención propia del CFW
- `TF1` — tarjeta SD principal (sistema); `TF2` — tarjeta SD secundaria (contenido)
- `SD` — SD única cuando el dispositivo solo tiene una ranura
- `[TODO]` — ruta no verificada o pendiente de confirmación
- Si una sección no incluye fila `Screenshots` o no separa `Media (imágenes)` de `Media (vídeos)`, es porque ese CFW no gestiona esos elementos de forma independiente (los agrupa en una sola carpeta `Media` o no ofrece captura de pantalla dedicada), no un olvido de documentación.

---

## Linux Handheld

### ROCKNIX

**Hardware:** RK3326, RK3566 — RG353P/V, RGARC-S, RG40XXV/H, RGB10, OGA, RK2020

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | TF2 | `/storage/roms/{sistema}/` |
| BIOS | TF2 | `/storage/bios/` |
| Saves | TF2 | `/storage/saves/{sistema}/` |
| States | TF2 | `/storage/states/{sistema}/` |
| Screenshots | TF2 | `/storage/screenshots/` |
| Media (imágenes) | TF2 | `/storage/roms/{sistema}/media/` |
| Media (vídeos) | TF2 | `/storage/roms/{sistema}/media/` |
| Gamelist | TF2 | `/storage/roms/{sistema}/gamelist.xml` |

> TF1 contiene el sistema operativo. TF2 es la tarjeta de contenido. En dispositivos de una sola SD, todo va en la misma tarjeta bajo `/storage/`.

---

### KNULLI

**Hardware:** H700 (RG35XX Plus/H/SP, RG34XX/SP), A133 (V10), A133P (V90S)

Derivado de Batocera. Estructura idéntica a Batocera oficial.

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | TF1 | `/userdata/roms/{sistema}/` |
| BIOS | TF1 | `/userdata/bios/` |
| Saves | TF1 | `/userdata/saves/{sistema}/` |
| States | TF1 | `/userdata/states/{sistema}/` |
| Screenshots | TF1 | `/userdata/screenshots/` |
| Media (imágenes) | TF1 | `/userdata/roms/{sistema}/images/` |
| Media (vídeos) | TF1 | `/userdata/roms/{sistema}/videos/` |
| Gamelist | TF1 | `/userdata/gamelists/{sistema}/gamelist.xml` |

> En dispositivos H700 con una sola SD, TF1 es la única tarjeta.

---

### muOS

**Hardware:** H700 — RG28XX

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | TF1 | `/mnt/mmc/ROMS/{sistema}/` |
| ROMs | TF2 | `/mnt/sdcard/ROMS/{sistema}/` |
| BIOS | TF1 | [TODO] |
| Saves | TF1 | [TODO] |
| States | TF1 | [TODO] |
| Media (artwork) | TF1 | [TODO] |
| Media (preview) | TF1 | [TODO] |
| Gamelist | — | No aplica (muOS usa catálogo propio) |

> muOS no usa `gamelist.xml`. Los metadatos se gestionan mediante su propio sistema de catálogo.

---

### AmberELEC

**Hardware:** RK3326 — RG351M, RG351V, RG351MP

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | TF2 | `/storage/roms/{sistema}/` |
| BIOS | TF2 | `/storage/roms/bios/` |
| Saves | TF2 | `/storage/roms/savestates/` |
| States | TF2 | `/storage/roms/savestates/` |
| Screenshots | TF2 | `/storage/roms/screenshots/` |
| Media | TF2 | `/storage/roms/{sistema}/media/` |
| Gamelist | TF2 | `/storage/roms/{sistema}/gamelist.xml` |

> TF1 contiene el sistema. TF2 es la tarjeta de contenido.

---

### ArkOS

**Hardware:** RK3326 — OGA, RK2020

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | TF2 | `/roms/{sistema}/` |
| BIOS | TF2 | `/roms/bios/` |
| Saves | TF2 | `/roms/savestates/` |
| States | TF2 | `/roms/savestates/` |
| Screenshots | TF2 | `/roms/screenshots/` |
| Media | TF2 | `/roms/{sistema}/media/` |
| Gamelist | TF2 | `/roms/{sistema}/gamelist.xml` |

> TF1 contiene el sistema. TF2 es la tarjeta de contenido montada en `/roms/`.

---

### dArkOS

**Hardware:** RK3326 — RGB20, RGB10 Max 2

Sucesor de ArkOS. Estructura idéntica a ArkOS.

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | TF2 | `/roms/{sistema}/` |
| BIOS | TF2 | `/roms/bios/` |
| Saves | TF2 | `/roms/savestates/` |
| States | TF2 | `/roms/savestates/` |
| Screenshots | TF2 | `/roms/screenshots/` |
| Media | TF2 | `/roms/{sistema}/media/` |
| Gamelist | TF2 | `/roms/{sistema}/gamelist.xml` |

---

### Adam Image

**Hardware:** JZ4770/OpenDingux — RG350, RG350M/P, RG280M/V, RG300X, PocketGo2

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | TF2 | `/media/sdcard/roms/{sistema}/` |
| BIOS | TF1 | [TODO] |
| Saves | TF1 | [TODO] |
| States | TF1 | [TODO] |
| Media | TF1 | [TODO] |
| Gamelist | TF1 | [TODO] |

> TF1 contiene el sistema y los datos de usuario. TF2 es la tarjeta de ROMs.

---

### RetroFW

**Hardware:** JZ4760B — LDK Landscape, LDK Vertical, RS97, RS-07

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | SD | `/media/sdcard/roms/{sistema}/` |
| BIOS | SD | `/home/retrofw/bios/` |
| Saves | SD | `/home/retrofw/saves/` |
| States | SD | `/home/retrofw/saves/` |
| Media | — | No aplica (SimpleMenu usa imágenes locales opcionales) |
| Gamelist | — | No aplica |

---

### CrossMix-OS

**Hardware:** A133P — TrimUI Smart Pro, TrimUI Brick

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | SD | `/mnt/SDCARD/Roms/{sistema}/` |
| BIOS | SD | `/mnt/SDCARD/Bios/` |
| Saves | SD | `/mnt/SDCARD/Saves/` |
| States | SD | `/mnt/SDCARD/States/` |
| Media | SD | `/mnt/SDCARD/Roms/{sistema}/Imgs/` |
| Gamelist | SD | `/mnt/SDCARD/Roms/{sistema}/gamelist.xml` |

---

### Onion OS

**Hardware:** SSD202D — Miyoo Mini, Miyoo Mini Plus

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | SD | `/mnt/SDCARD/Roms/{sistema}/` |
| BIOS | SD | `/mnt/SDCARD/BIOS/` |
| Saves | SD | `/mnt/SDCARD/Saves/{sistema}/` |
| States | SD | `/mnt/SDCARD/Saves/{sistema}/` |
| Media | SD | `/mnt/SDCARD/Roms/{sistema}/Imgs/` |
| Gamelist | SD | `/mnt/SDCARD/Roms/{sistema}/gamelist.xml` |

---

### Koriki BOM

**Hardware:** SSD202D (Miyoo Mini/Plus, Miyoo Mini Flip), RG35XX Original, RK3566 (Miyoo Flip)

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | SD | `/mnt/SDCARD/Roms/{sistema}/` |
| BIOS | SD | `/mnt/SDCARD/Bios/` |
| Saves | SD | `/mnt/SDCARD/Saves/{sistema}/` |
| States | SD | `/mnt/SDCARD/Saves/{sistema}/` |
| Media | SD | `/mnt/SDCARD/Roms/{sistema}/Imgs/` |
| Gamelist | SD | [TODO] |

---

### MinUI

**Hardware:** F1C200S — TrimUI Smart

MinUI usa una convención propia con etiquetas (`{tag}`) entre paréntesis en lugar de nombres de carpeta estándar.

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | SD | `/mnt/SDCARD/Roms/{Sistema} ({tag})/` |
| BIOS | SD | `/mnt/SDCARD/Bios/{tag}/` |
| Saves | SD | `/mnt/SDCARD/Saves/{tag}/` |
| States | SD | `/mnt/SDCARD/Saves/{tag}/` |
| Media | — | No aplica (MinUI no usa scraped media) |
| Gamelist | — | No aplica |

> Ejemplo: `/mnt/SDCARD/Roms/Game Boy Advance (GBA)/`. Las etiquetas `{tag}` son las convenciones internas de MinUI: FC, SFC, GBA, GB, GBC, MD, PS, etc.

---

### spruceOS

**Hardware:** A33 — Miyoo A30

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | SD | `/mnt/SDCARD/Roms/{sistema}/` |
| BIOS | SD | `/mnt/SDCARD/Bios/` |
| Saves | SD | `/mnt/SDCARD/Saves/` |
| States | SD | `/mnt/SDCARD/Saves/` |
| Media | SD | `/mnt/SDCARD/Roms/{sistema}/Imgs/` |
| Gamelist | SD | [TODO] |

---

### BOB (Best of the Best) — Bittboy/PowKiddy

**Hardware:** F1C100S — PocketGo Bitboy, PocketGo Pocket Go, PowKiddy Q90/V90/Q20 Mini

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | SD | [TODO] |
| BIOS | SD | [TODO] |
| Saves | SD | [TODO] |
| States | SD | [TODO] |
| Media | — | [TODO] |
| Gamelist | — | [TODO] |

---

### DrUm78 RGNano

**Hardware:** Cortex-A7 — Anbernic RGNano

Doble interfaz: RetroFE es el lanzador de juegos por defecto (rutas de esta sección); GMenu2X está disponible como interfaz secundaria para utilidades del sistema y reproductor de MP3/vídeo, sin gestionar rutas de ROMs propias.

| Tipo | SD | Ruta |
| --- | --- | --- |
| ROMs | SD | `/mnt/{sistema}/` |
| BIOS | SD | `/mnt/bios/` |
| Saves | SD | [TODO] |
| States | SD | [TODO] |
| Media | SD | `/mnt/{sistema}/previews/` |
| Gamelist | — | No aplica (RetroFE escanea carpetas y empareja `previews/` por nombre de ROM) |

---

## OS Retro (SBC / PC)

### Batocera

**Hardware:** Raspberry Pi 3B+, SBC compatibles

Acceso a los archivos vía red: `\\BATOCERA\share` o SSH en `/userdata/`.

| Tipo | Ruta |
| --- | --- |
| ROMs | `/userdata/roms/{sistema}/` |
| BIOS | `/userdata/bios/` |
| Saves | `/userdata/saves/{sistema}/` |
| States | `/userdata/states/{sistema}/` |
| Screenshots | `/userdata/screenshots/` |
| Media (imágenes) | `/userdata/roms/{sistema}/images/` |
| Media (vídeos) | `/userdata/roms/{sistema}/videos/` |
| Gamelist | `/userdata/gamelists/{sistema}/gamelist.xml` |

---

### Recalbox

**Hardware:** Raspberry Pi 5, SBC compatibles

Acceso a los archivos vía red: `\\RECALBOX\share` o SSH en `/recalbox/share/`.

| Tipo | Ruta |
| --- | --- |
| ROMs | `/recalbox/share/roms/{sistema}/` |
| BIOS | `/recalbox/share/bios/` |
| Saves | `/recalbox/share/saves/{sistema}/` |
| States | `/recalbox/share/states/{sistema}/` |
| Screenshots | `/recalbox/share/screenshots/` |
| Media | `/recalbox/share/roms/{sistema}/media/` |
| Gamelist | `/recalbox/share/roms/{sistema}/gamelist.xml` |

---

## Android CFW

### GammaOS Core + ES-DE

**Hardware:** GKD Bubble

GammaOS Core es la base Android. ES-DE se instala como aplicación encima. Las rutas de BIOS dependen del emulador individual.

| Tipo | Ruta |
| --- | --- |
| ROMs | `/storage/emulated/0/ROMs/{sistema}/` |
| BIOS | Por emulador (ver configuración individual) |
| Saves | Por emulador |
| States | Por emulador |
| Media (ES-DE) | `/storage/emulated/0/ES-DE/downloaded_media/{sistema}/` |
| Gamelist (ES-DE) | `/storage/emulated/0/ES-DE/gamelists/{sistema}/gamelist.xml` |

---

### GammaOS Next + ES-DE

**Hardware:** RGDS

GammaOS Next es la base Android. ES-DE se instala como aplicación encima. Las rutas de BIOS dependen del emulador individual.

| Tipo | Ruta |
| --- | --- |
| ROMs | `/storage/emulated/0/ROMs/{sistema}/` |
| BIOS | Por emulador (ver configuración individual) |
| Saves | Por emulador |
| States | Por emulador |
| Media (ES-DE) | `/storage/emulated/0/ES-DE/downloaded_media/{sistema}/` |
| Gamelist (ES-DE) | `/storage/emulated/0/ES-DE/gamelists/{sistema}/gamelist.xml` |

---

## Frontends (Android / Windows)

### ES-DE Android

**Hardware:** Teclast T50, Xiaomi Redmi Pad 2, AYN Odin 2, RGVita

| Tipo | Ruta |
| --- | --- |
| ROMs | `/storage/emulated/0/ROMs/{sistema}/` |
| BIOS | Por emulador |
| Saves | Por emulador |
| States | Por emulador |
| Media | `/storage/emulated/0/ES-DE/downloaded_media/{sistema}/` |
| Gamelist | `/storage/emulated/0/ES-DE/gamelists/{sistema}/gamelist.xml` |

---

### ES-DE Portable (Windows)

**Hardware:** GPD Win

Instalación portable en `C:\`. Las rutas son relativas a la carpeta de instalación de ES-DE.

| Tipo | Ruta |
| --- | --- |
| ROMs | `C:\ROMs\{sistema}\` |
| BIOS | Por emulador |
| Saves | Por emulador |
| States | Por emulador |
| Media | `ES-DE\downloaded_media\{sistema}\` |
| Gamelist | `ES-DE\gamelists\{sistema}\gamelist.xml` |

> Ruta de ROMs configurable en `es_settings.xml`. La ruta de media y gamelists es relativa a la carpeta de datos de ES-DE (`%AppData%\ES-DE\` en instalación estándar, o carpeta portable en instalación portable).

---

### LineageOS / RetroidOS

**Hardware:** MT6580 — Retroid Pocket 2

Base Android estándar; sin frontend propio (usar Pegasus, ver `docs/guides/apps/pegasus.md`).

| Tipo | Ruta |
| --- | --- |
| ROMs | [TODO] |
| BIOS | Por emulador |
| Saves | Por emulador |
| States | Por emulador |
| Media | [TODO] |
| Gamelist | [TODO] |

---

## Pendiente de documentar

| Distribución | Estado |
| --- | --- |
| BOB A13 (Batocera RK3128) | [TODO] — estructura probable similar a Batocera |
| GarlicOS | [TODO] — estructura TF1 sistema / TF2 ROMs |
| Koriki ED (H700) | [TODO] — variante H700 de Koriki |
| Simple30 | [TODO] — SimpleMenu sobre PocketGo S30 |
