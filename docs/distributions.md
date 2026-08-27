# Distribuciones

Matriz dispositivo × software que relaciona cada dispositivo del inventario con el software recomendado y el estado real de instalación. Es el documento operativo central del ecosistema: permite decidir qué instalar, auditar qué hay instalado y planificar migraciones.

Cada fila corresponde exactamente a un dispositivo de `docs/devices.md`. Las columnas de recomendación y las de instalación real son independientes: la instalación real no reemplaza la recomendación, solo la complementa.

## Convenciones

### Tipo

Tipo del software recomendado.

* CFW — firmware para un dispositivo o familia de hardware concreta (GarlicOS, muOS, MiyooCFW, Adam Image, MinUI, CrossMix-OS…)
* OS Retro — sistema operativo retro de propósito general para SBC o PC (Batocera, Recalbox, RetroPie, Lakka…)
* OS Handheld — sistema operativo retro de propósito general para múltiples handhelds (ROCKNIX, ArkOS, AmberELEC, KNULLI, The Retro Arena…)
* Android CFW — ROM Android personalizada orientada a emulación (GammaOS, 351Droid…)
* Stock Mod — modificación del firmware de fábrica sin reemplazarlo
* Frontend — aplicación de lanzador/interfaz sobre un OS existente (ES-DE, Daijishō, Pegasus…)

### Estado instalación

Estado verificado de la instalación real en el dispositivo.

* Verificado — instalación confirmada y documentada
* Pendiente — instalación prevista pero no ejecutada
* No instalado — dispositivo sin instalar
* Desconocido — estado no verificado
* No aplica — dispositivo que no requiere instalación de CFW

### Estado recomendación

Solidez de la recomendación para el dispositivo.

* Recomendado — opción principal clara y bien soportada
* Válido — opción funcional aunque no sea la principal
* Alternativo — alternativa razonable en contextos específicos
* Legado — recomendación histórica, superada por opciones más modernas
* Experimental — soporte no estable o en desarrollo
* No recomendado — opción desaconsejada para este dispositivo

### Columnas

| Columna | Descripción |
| --- | --- |
| Dispositivo | Nombre del dispositivo tal como aparece en `devices.md` |
| Familia | Familia de SoC o hardware para agrupación y filtrado |
| Tipo | Categoría del software recomendado |
| Software recomendado | CFW, OS o frontend recomendado como opción principal |
| Alternativas | Opciones secundarias válidas, separadas por `/` |
| Frontend recomendado | Interfaz de usuario expuesta por el software recomendado |
| Instalación real | Software realmente instalado en el dispositivo |
| Frontend real | Interfaz de usuario de la instalación real |
| Estado instalación | Estado verificado de la instalación real |
| Contenido recomendado | Estrategia de distribución de contenido en tarjetas SD |
| Estado recomendación | Solidez de la recomendación para este dispositivo |
| Notas | Observaciones operativas, versiones o advertencias |

---

| Dispositivo | Familia | Tipo | Software recomendado | Alternativas | Frontend recomendado | Instalación real | Frontend real | Estado instalación | Contenido recomendado | Estado recomendación | Notas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Raspberry Pi 3B+ | BCM2837B0 | OS Retro | Batocera (v37) | Recalbox / Lakka / RetroPie | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + emuladores; ROMs en red/USB | Recomendado | v37 es la versión más adecuada para BCM2837B0. |
| Raspberry Pi 5 4GB | BCM2712 | OS Retro | Recalbox (10.0.5) | Lakka / Batocera (43.1) | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + emuladores; ROMs en red/USB | Recomendado | Soporte nativo para BCM2712. |
| Teclast T50 | Unisoc T616 | Frontend | ES-DE Android | Daijishō / Pegasus | ES-DE | [TODO] | [TODO] | Desconocido | Interna: apps + emuladores; TF1: ROMs | Recomendado | ES-DE si se reutilizan gamelists y media EmulationStation. |
| Xiaomi Redmi Pad 2 | Helio G100 Ultra | Frontend | ES-DE Android | Daijishō / Pegasus | ES-DE | [TODO] | [TODO] | Desconocido | Interna: apps + emuladores; TF1: ROMs | Recomendado | Para colecciones ES reutilizables, ES-DE; para setup Android puro, Daijishō. |
| PowKiddy A13 | RK3128 | OS Retro | BOB A13 | Batocera (v35b) | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves; backup obligatorio | Recomendado | v35b es una compilación especial para RK3128; base de la imagen BOB. |
| PocketGo Bitboy | F1C100S | CFW | BOB | MiyooCFW / Stock mod | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Hardware muy limitado; evitar frontends pesados. |
| PowKiddy LDK Landscape | JZ4760B | CFW | RetroFW | OpenDingux | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Familia Ingenic antigua; no tratar como Batocera. |
| PocketGo Pocket Go | F1C100S | CFW | BOB | MiyooCFW / Stock mod | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Hardware muy limitado; evitar frontends pesados. |
| PowKiddy LDK Vertical | JZ4760B | CFW | RetroFW | OpenDingux | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Igual que LDK Landscape. |
| Anbernic RG350 | JZ4770 | CFW | Adam Image | Rogue CFW | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Familia JZ4770/OpenDingux. |
| Retrogame RS97 | JZ4760B | CFW | RetroFW | OpenDingux | SimpleMenu | [TODO] | [TODO] | Desconocido | TF Interna: sistema; TF1: ROMs, BIOS, saves | Recomendado | RetroFW es la línea natural. |
| PocketGo PocketGo2 V1 | JZ4770 | CFW | Adam Image | Rogue CFW / Stock OpenDingux | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Familia JZ4770/OpenDingux. |
| Retroflag GPi Case (2019) | Raspberry Pi Zero | OS Retro | Recalbox | RetroPie / Batocera | EmulationStation | [TODO] | [TODO] | Pendiente | TF1: sistema + ROMs, BIOS, saves | Recomendado | Requiere la imagen/build específica de Recalbox y RetroPie con soporte para la pantalla de 2.8" del GPi Case y el script 'Safe Shutdown' de Retroflag para el interruptor físico (no es la imagen genérica de Raspberry Pi). Limitado a emulación clásica hasta PS1 (con frameskip). Funciona con 3 pilas AA. |
| PowKiddy Q90 | F1C100S | CFW | BOB | MiyooCFW / Stock mod | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Hardware muy limitado; evitar frontends pesados. |
| Hardkernel Odroid-Go-Advance | RK3326 | OS Handheld | ArkOS | ROCKNIX | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | RK3326/OGA. |
| PowKiddy V90 | F1C100S | CFW | BOB | MiyooCFW / Stock mod | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Hardware muy limitado; evitar frontends pesados. |
| Anbernic RG99 | JZ4725B | CFW | RetroFW | OpenDingux | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Hardware legacy muy limitado; solo sistemas 8-bit básicos. |
| RK2020 RK2020 | RK3326 | OS Handheld | ArkOS | ROCKNIX | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | RK3326 clásico. |
| PowKiddy RGB10 | RK3326 | OS Handheld | ROCKNIX | ArkOS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | ROCKNIX/ArkOS según preferencia. |
| Anbernic RG280M | JZ4770 | CFW | Adam Image | Rogue CFW | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Adam Image como base práctica. TF2 en FAT32. |
| Anbernic RG350M | JZ4770 | CFW | Adam Image | Rogue CFW | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Adam Image como base práctica. TF2 en FAT32. |
| PowKiddy RGB20 | RK3326 | OS Handheld | dArkOS | ArkOS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Imagen oficial OGA 1.1/RGB10/RGB20; ArkOS histórico. |
| PocketGo S30 | ATM7051 | CFW | Simple30 | SimplerS30 / Stock mod | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Simple30/SimplerS30 son específicos para S30. |
| Anbernic RG280V | JZ4770 | CFW | Adam Image | Rogue CFW | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Adam Image como base práctica. TF2 en FAT32. |
| Anbernic RG350P | JZ4770 | CFW | Adam Image | Rogue CFW | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Adam Image como base práctica. TF2 en FAT32. |
| Anbernic RG351M | RK3326 | OS Handheld | AmberELEC | ROCKNIX / BOB ArkOS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Imagen: AmberELEC-RG351P.aarch64.img.gz. |
| Anbernic RG351V | RK3326 | OS Handheld | AmberELEC | ROCKNIX / BOB ArkOS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Imagen: AmberELEC-RG351V.aarch64.img.gz. |
| Anbernic RG300X | JZ4770 | CFW | Adam Image | Rogue CFW | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Adam Image como base práctica. TF2 en FAT32. |
| PowKiddy Q20 Mini | F1C100S | CFW | BOB | MiyooCFW / Stock mod | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Hardware muy limitado; evitar frontends pesados. |
| Anbernic RG351MP | RK3326 | OS Handheld | AmberELEC | ROCKNIX / BOB ArkOS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Imagen: AmberELEC-RG351MP.aarch64.img.gz. |
| PowKiddy RGB10 Max 2 | RK3326 | OS Handheld | dArkOS | BOB ArkOS / RetroOZ | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | BOB ArkOS imagen RGB10Max; RetroOZ histórico. |
| Miyoo Miyoo Mini | SSD202D | CFW | Koriki BOM (v1.6.x) | Onion OS (v4.3.x+) / MinUI | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Koriki recomendado; Onion OS como alternativa consolidada. |
| Anbernic RG353P | RK3566 | OS Handheld | ROCKNIX | GammaOS Core | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Dual boot Android/Linux; preferencia por lado Linux con ROCKNIX. |
| Anbernic RG353V | RK3566 | OS Handheld | ROCKNIX | GammaOS Core | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Dual boot Android/Linux; preferencia por lado Linux con ROCKNIX. |
| Anbernic RG35XX (Original) | ATM7039S | CFW | Koriki BOM | GarlicOS | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | No confundir con familia H700; GarlicOS como alternativa clásica. |
| Miyoo Miyoo Mini Plus | SSD202D | CFW | Koriki BOM (v1.6.x) | Onion OS (v4.3.x+) / MinUI | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Koriki recomendado; Onion OS como alternativa consolidada. |
| Anbernic RG35XX Plus | H700 | OS Handheld | KNULLI | muOS / Koriki ED | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Familia H700/XX moderna. |
| Data Frog SF2000 | HCSEMI B210 | Stock Mod | SF2000 Multicore / Tadpole | Stock mod | Stock UI | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs; backup obligatorio | Válido | Más workflow que CFW completo. |
| Anbernic RGNano | Cortex-A7 | CFW | DrUm78 RGNano (v2.x+) | Stock Anbernic | RetroFE | DrUm78 RGNano | RetroFE | Verificado | TF1: sistema + ROMs | Recomendado | RetroFE es el lanzador de juegos por defecto; GMenu2X disponible como interfaz secundaria para utilidades del sistema y reproductor MP3/vídeo. RetroArch Quick Menu para emulación. |
| TrimUI TRIMUI Smart Pro | A133P | CFW | CrossMix-OS | KNULLI | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | CrossMix como opción principal. |
| TrimUI TRIMUI Brick | A133 Plus | CFW | CrossMix-OS | spruceOS / KNULLI | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | CrossMix como opción principal; spruceOS alternativa destacada. |
| TrimUI Model S | F1C200S | CFW | MinUI | Tomato OS | MinUI | MinUI | MinUI | Verificado | TF1: sistema + ROMs, BIOS, saves | Recomendado | MinUI preferido; Tomato OS alternativa específica para Model S. |
| PowKiddy A30 | F1C200S | CFW | MinUI | Modified Stock OS | MinUI | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Experimental | Comparte SoC F1C200S con TrimUI Model S; adaptación de MinUI para F1C200S por Shaun Inman. Alternativa es el TrimUI OS de fábrica modificado con GMenu2X. Soporte de comunidad muy escaso — [TODO] validar fiabilidad de estos datos antes de confiar en ellos para instalación real. |
| Anbernic RG35XXH | H700 | OS Handheld | KNULLI | muOS / Koriki ED | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Igual que RG35XX Plus. |
| Anbernic RGARC-S | RK3566 | OS Handheld | ROCKNIX | Stock Linux | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | ROCKNIX especialmente interesante en ARC. |
| Miyoo A30 | A33 | CFW | spruceOS | MinUI | spruceOS UI | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | spruceOS es la línea fuerte reciente. |
| Anbernic RG28XX | H700 | OS Handheld | muOS | KNULLI | muOS UI | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | ROCKNIX sin soporte para RG28XX. |
| Anbernic RG35XXSP | H700 | OS Handheld | KNULLI | muOS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | ROCKNIX sin soporte para RG35XXSP. |
| Anbernic RG34XX | H700 | OS Handheld | KNULLI | muOS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | ROCKNIX sin soporte para RG34XX. |
| Anbernic RG34XXSP | H700 | OS Handheld | KNULLI | muOS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | ROCKNIX sin soporte para RG34XXSP. |
| PowKiddy RS-07 | JZ4760B | CFW | RetroFW | Stock mod | SimpleMenu | [TODO] | [TODO] | Desconocido | TF Interna: sistema + ROMs, BIOS, saves; clonar SD original | Recomendado | Familia JZ4760B; The Retro Arena sin soporte. |
| PowKiddy RS-12 | ARM 32-bit | Stock Mod | Modified Stock OS | — | Stock UI | Modified Stock OS | Stock UI | Verificado | TF1: sistema + ROMs | Válido | Dispositivo cerrado; se juega con el firmware de fábrica. |
| PowKiddy V10 | RK3326 | OS Handheld | KNULLI (Scarab) | ROCKNIX | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Scarab es la build específica de KNULLI para V10. |
| GKD Pixel 2 | RK3326 | Stock Mod | RogueOS | plumOS-GKD / twigUI / KNULLI (Scarab) | EmulationStation | [TODO] | [TODO] | Pendiente | TF1: sistema + ROMs, BIOS, saves | Recomendado | Basado en el SoC RK3326S. RogueOS (Ninoh-FOX) destaca por PortMaster integrado y gestión de batería (vibración 10%/5%, apagado seguro al 1%), a costa de arranque de fábrica (~30s). plumOS-GKD (game-de-it) prioriza arranque/sleep más rápidos. twigUI es un port de spruceOS que sustituye EmulationStation por una interfaz de texto minimalista. KNULLI (Scarab) añade Syncthing y scraping premium pero aún tiene fallos de juventud en audio y algunos adaptadores Wi-Fi USB en este hardware. |
| Anbernic RG40XXV | H700 | OS Handheld | KNULLI | muOS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | ROCKNIX sin soporte. Existe LOAD"" con estética ZX Spectrum. |
| GKD Bubble | RK3566 | Android CFW | GammaOS Core | plumOS-GKD | ES-DE | GammaOS Core | ES-DE | Verificado | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | GammaOS Core verificado; ES-DE instalado como frontend. |
| Anbernic RG40XXH | H700 | OS Handheld | KNULLI | muOS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | ROCKNIX sin soporte para RG40XXH. |
| PowKiddy V90S | A133 Plus | OS Handheld | KNULLI (Scarab) | plumOS / spruceOS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Scarab es la build específica de KNULLI para V90S; spruceOS como alternativa en desarrollo. |
| Miyoo Miyoo Mini Flip | SSD202D | CFW | Koriki BOM (v1.6.x) | spruceOS | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves | Recomendado | Depende de madurez de builds. |
| Miyoo Miyoo Flip | RK3566 | CFW | Koriki BOM (v1.6.x) | spruceOS | SimpleMenu | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | Depende de madurez de builds. |
| Anbernic RGDS | RK3568 | Android CFW | GammaOS Next | ROCKNIX | ES-DE | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | GammaOS Next con ES-DE como frontend; ROCKNIX como alternativa Linux. |
| AYN Odin 2 Portal (Base) | Snapdragon 8 Gen 2 | Frontend | ES-DE Android | Daijishō / Pegasus | ES-DE | [TODO] | [TODO] | Desconocido | Interna: apps + emuladores; TF1: ROMs | Recomendado | Android; ES-DE para colecciones ES compatibles. |
| PowKiddy X18 | MT8176 | Frontend | Daijishō | ES-DE Android / Pegasus | Daijishō | [TODO] | [TODO] | Desconocido | Interna: apps + emuladores; TF1: ROMs | Recomendado | Android 7.0; usar frontend Android, no CFW Linux. |
| GPD Win | Intel Atom x7 | Frontend | ES-DE (Portable) | RetroBat / LaunchBox/BigBox | ES-DE | ES-DE (Portable) | ES-DE | Verificado | Interna: sistema + emuladores; TF1: ROMs, BIOS, carátulas | Recomendado | Usar versión portable (.zip); LaunchBox/BigBox problemático por consumo de RAM/GPU; activar X-Input con el interruptor físico antes de abrir ES-DE. |
| Anbernic RGVita (Base) | Unisoc T618 | Android CFW | GammaOS Next | ES-DE Android / Daijishō / Pegasus / RGLauncher stock | GammaOS Next (launcher propio) | [TODO] | [TODO] | Desconocido | Interna: apps + emuladores; TF1: ROMs | Recomendado | Android 12. GammaOS Next ya lanzado y confirmado compatible (README oficial del proyecto) — sustituye a la recomendación anterior de Android stock + ES-DE, que pasa a alternativa. |
| GKD 350H | X1830 | Stock Mod | Modified Stock OS | — | Stock UI | Modified Stock OS | Stock UI | Verificado | Interna: sistema + ROMs; TF1: ROMs | Válido | Dispositivo cerrado; no existe CFW para X1830. OpenDingux de fábrica es la única opción. |
| Retroid Pocket 2 | MT6580 | Android CFW | LineageOS (Android 8.1 v2) | Stock Android 8.1 / RetroidOS | Pegasus | Stock Android 6.0 | RetroidOS | Verificado | Interna: sistema + apps + emuladores; TF1: ROMs | Recomendado | LineageOS limpia el sistema y mejora rendimiento; Pegasus como frontend sobre Android. L2/R2 físicos; salida Micro HDMI. |
| Anbernic RG CubeXX | H700 | OS Handheld | KNULLI | muOS / Modified Stock OS | EmulationStation | [TODO] | [TODO] | Desconocido | TF1: sistema; TF2: ROMs, BIOS, saves | Recomendado | KNULLI es ideal aquí porque su interfaz escala perfectamente en pantallas cuadradas 1:1. muOS funciona pero requiere temas adaptados. |
| Anbernic RG Slide | Unisoc T820 | Android CFW | GammaOS Next | ES-DE Android / Daijishō / RGLauncher stock | GammaOS Next (launcher propio) | [TODO] | [TODO] | Desconocido | Interna: apps + emuladores; TF1: ROMs | Recomendado | Build específica desde v1.2.0 (pública feb. 2026). Alternativa: quedarse en Android stock + ES-DE si no se quiere sustituir el SO. |
| Anbernic RG Rotate | Unisoc T618 | Android CFW | GammaOS Nano | GammaOS Next (modo completo) / ES-DE Android / RGLauncher stock | Android Launcher (UI Nano) | [TODO] | [TODO] | Desconocido | Interna: apps + emuladores; TF1: ROMs | Recomendado | Desde v1.4.0, GammaOS Nano es la UI ligera por defecto para este modelo, con ajustes propios del mecanismo giratorio (rotar/dormir/lanzar app/reloj); el modo Next completo está disponible a un switch dentro de la misma instalación. Coherente con RGVita (mismo SoC T618). |
| MagicX Zero 40 | A133 Plus | Android CFW | GammaOS Nano | Firmware stock (Dawn Launcher) | Android Launcher (UI Nano) | [TODO] | [TODO] | Desconocido | TF1: sistema + ROMs, BIOS, saves; TF2: media/backup | Recomendado | GammaOS Nano es el único CFW confirmado para el Zero 40 (v1.4.1, agosto 2026); no existe port de MinUI/Moss ni de GammaOS Core/Next "completo" para este modelo concreto (solo para el Mini Zero 28, dispositivo distinto). Mismo SoC (A133 Plus) que TrimUI Brick/PowKiddy V90S, pero su firmware stock es Android, no Linux/Tina — por eso sigue la rama Android CFW (GammaOS) en vez de CrossMix-OS/KNULLI/spruceOS. |
| MagicX Mini Zero 28 | A133 Plus | CFW | MinUI (Moss) | GammaOS Nano / muOS (en desarrollo) | MinUI | [TODO] | [TODO] | Desconocido | TF1/INT: Moss + MinUI; TF2/EXT: ROMs, saves | Recomendado | MinUI sobre Moss-zero28 (Tina Linux) es la alternativa Linux recomendada: soporte comunitario (Shaun Inman) desde enero 2025, interfaz minimalista de listas de texto y suspensión/apagado automático fiables. MagicX no ofrece firmware Linux oficial; Moss es la base que arranca desde TF1/INT, con MinUI y las ROMs en TF2/EXT. GammaOS Nano queda como alternativa Android (ver Zero 40, mismo SoC). El equipo de muOS trabaja en un port para esta arquitectura (interfaz más rica, PortMaster) pero no está publicado aún — no confirmado en software.md. |
