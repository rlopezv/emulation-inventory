# Dispositivos

Inventario de hardware de emulación del ecosistema personal. Cubre handhelds, SBCs, tablets y bartops. Es la fuente de verdad para dispositivos: todo dispositivo referenciado en otros documentos debe existir aquí.

## Convenciones

### Fiabilidad

Confianza en los datos documentados, no calidad del hardware.

* Muy alta — datos verificados en múltiples fuentes fiables
* Alta — datos bien documentados con alta confianza
* Media-Alta — datos mayoritariamente fiables con alguna incertidumbre menor
* Media — datos parciales o con fuentes contradictorias
* Baja — datos escasos, especulativos o sin verificar

### Orientación

* SBC — placa sin pantalla, uso como servidor de emulación o conectado a TV
* Horizontal — pantalla apaisada, posición de juego estándar
* Vertical — pantalla en portrait
* Clamshell horizontal — formato concha con pantalla horizontal
* Horizontal tablet — tablet con pantalla apaisada
* Dual-screen clamshell — formato consola con dos pantallas
* Arcade tabletop horizontal — formato tabletop/bartop de pantalla fija
* Mini arcade tabletop fija / horizontal — formato bartop miniatura

### SD

Configuración normalizada de almacenamiento:

* `TF1` — única ranura microSD
* `TF1 + TF2` — dos ranuras microSD
* `TF Interna` — microSD fija interna sin ranura accesible externamente
* `TF Interna + TF1` — microSD fija interna + ranura microSD externa
* `TF Interna (XX GB) + TF1` — microSD interna fija con tamaño conocido + ranura microSD externa
* `Interna (XX GB)` — almacenamiento eMMC/UFS sin ranura externa
* `Interna (XX GB) + TF1` — almacenamiento eMMC/UFS + ranura microSD

### Columnas

| Columna | Descripción |
| --- | --- |
| Marca | Fabricante o marca comercial del dispositivo |
| Modelo | Nombre de modelo del dispositivo |
| Procesador | SoC o CPU principal con núcleos y frecuencia |
| Memoria | RAM disponible |
| Pantalla | Tamaño de pantalla en pulgadas |
| Resolución | Resolución nativa de la pantalla |
| Aspect Ratio | Relación de aspecto de la pantalla |
| Orientación | Posición de uso y factor de forma del dispositivo |
| Año salida | Año de lanzamiento comercial |
| Fiabilidad | Confianza en los datos documentados (ver convención) |
| SD | Configuración de ranuras de almacenamiento externo |
| Imagen | Nombre del archivo de imagen en `docs/imgs/` |

---

| Marca | Modelo | Procesador | Memoria | Pantalla | Resolución | Aspect Ratio | Orientación | Año salida | Fiabilidad | SD | Imagen |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Raspberry Pi | 3B+ | Broadcom BCM2837B0 (4x Cortex-A53 1.4 GHz) | 1 GB | — | 1920x1080 | 16:9 | SBC | 2018 | Muy alta | TF1 | docs/imgs/RPi3B+.png |
| Raspberry Pi | 5 (4GB) | Broadcom BCM2712 (4x Cortex-A76 2.4 GHz) | 4 GB | — | 1920x1080 | 16:9 | SBC | 2023 | Muy alta | TF1 | docs/imgs/RPi5.png |
| Teclast | T50 | Unisoc Tiger T616 | 8 GB | 11" | 2000x1200 | 5:3 | Horizontal tablet | 2022 | Alta | Interna (128 GB) + TF1 | docs/imgs/TeclastT50.png |
| Xiaomi | Redmi Pad 2 | MediaTek Helio G100 Ultra | 4 GB | 11" | 2560x1600 aprox | 16:10 | Horizontal tablet | 2025 | Media-alta | Interna (128 GB) + TF1 | docs/imgs/XiaomiRedmiPad2.png |
| PowKiddy | A13 | Rockchip RK3128 | 256 MB | 10.1" | 1024x600 | 16:9 aprox. | Mini bartop plegable / horizontal | 2020 aprox. | Media-Alta | TF1 | docs/imgs/PowKiddyA13.png |
| PocketGo | Bitboy | Allwinner F1C100S/F1C500S | 32 MB | 2.4" | 320x240 | 4:3 | Horizontal | 2018 | Media | TF1 | docs/imgs/Bitboy.png |
| PowKiddy | LDK Landscape | Ingenic JZ4760B | 128 MB | 2.6" | 320x240 | 4:3 | Horizontal | 2019 | Media | TF1 | docs/imgs/LDKLandscape.png |
| PocketGo | Pocket Go | Allwinner F1C100S/F1C500S | 32 MB | 2.4" | 320x240 | 4:3 | Horizontal | 2019 | Media | TF1 | docs/imgs/PocketGo.png |
| PowKiddy | LDK Vertical | Ingenic JZ4760B | 128 MB | 2.6" | 320x240 | 4:3 | Vertical | 2019 | Media | TF1 | docs/imgs/LDKVertical.png |
| Anbernic | RG350 | Ingenic JZ4770 | 512 MB | 3.5" | 320x240 | 4:3 | Horizontal | 2019 | Alta | TF1 + TF2 | docs/imgs/RG350.png |
| Retrogame | RS97 | Ingenic JZ4760B | 128 MB | 3.0" | 480x320 | 3:2 | Horizontal | 2017 | Baja | TF Interna + TF1 | docs/imgs/RS97.png |
| PocketGo | PocketGo2 V1 | Ingenic JZ4770 | 512 MB | 3.5" | 320x240 | 4:3 | Horizontal | 2019 | Media | TF1 + TF2 | docs/imgs/PocketGo2V1.png |
| Retroflag | GPi Case (2019) | Broadcom BCM2835 (1x ARM11 @ 1.0 GHz) | 512 MB LPDDR2 | 2.8" | 320x240 | 4:3 | Vertical | 2019 | Muy alta | TF1 | docs/imgs/RetroflagGPiCase.png |
| PowKiddy | Q90 | Allwinner F1C100S/F1C500S | 32 MB | 3.0" | 320x240 | 4:3 | Horizontal | 2020 | Media | TF1 | docs/imgs/Q90.png |
| Hardkernel | Odroid-Go-Advance | Rockchip RK3326 | 1 GB | 3.5" | 480x320 | 3:2 | Horizontal | 2020 | Alta | TF1 | docs/imgs/OdroidGoAdvance.png |
| PowKiddy | V90 | Allwinner F1C100S/F1C500S | 32 MB | 2.8" | 320x240 | 4:3 | Clamshell horizontal | 2020 | Media | TF1 | docs/imgs/V90.png |
| Anbernic | RG99 | Ingenic JZ4725B | 32 MB | 2.8" | 960x480 | 2:1 | Vertical | 2018/2019 aprox. | Media | TF1 | docs/imgs/RG99.png |
| RK2020 | RK2020 | Rockchip RK3326 | 1 GB | 3.5" | 480x320 | 3:2 | Horizontal | 2020 | Media | TF1 | docs/imgs/RK2020.png |
| PowKiddy | RGB10 | Rockchip RK3326 | 1 GB | 3.5" | 480x320 | 3:2 | Horizontal | 2020 | Alta | TF1 | docs/imgs/RGB10.png |
| Anbernic | RG280M | Ingenic JZ4770 | 512 MB | 2.8" | 480x320 | 3:2 | Horizontal | 2020 | Alta | TF1 + TF2 | docs/imgs/RG280M.png |
| Anbernic | RG350M | Ingenic JZ4770 | 512 MB | 3.5" | 640x480 | 4:3 | Horizontal | 2020 | Alta | TF1 + TF2 | docs/imgs/RG350M.png |
| PowKiddy | RGB20 | Rockchip RK3326 | 1 GB | 3.5" | 480x320 | 3:2 | Vertical | 2020 | Media | TF1 + TF2 | docs/imgs/RGB20.png |
| PocketGo | S30 | Actions ATM7051 | 512 MB | 3.5" | 480x320 | 3:2 | Horizontal | 2020/2021 | Media | TF1 | docs/imgs/S30.png |
| Anbernic | RG280V | Ingenic JZ4770 | 512 MB | 2.8" | 480x320 | 3:2 | Vertical | 2020 | Alta | TF1 + TF2 | docs/imgs/RG280V.png |
| Anbernic | RG350P | Ingenic JZ4770 | 512 MB | 3.5" | 320x240 | 4:3 | Horizontal | 2020 | Alta | TF1 + TF2 | docs/imgs/RG350P.png |
| Anbernic | RG351M | Rockchip RK3326 | 1 GB | 3.5" | 480x320 | 3:2 | Horizontal | 2021 | Alta | TF1 | docs/imgs/RG351M.png |
| Anbernic | RG351V | Rockchip RK3326 | 1 GB | 3.5" | 640x480 | 4:3 | Vertical | 2021 | Alta | TF1 + TF2 | docs/imgs/RG351V.png |
| Anbernic | RG300X | Ingenic JZ4770 | 512 MB | 3.0" | 640x480 | 4:3 | Horizontal | 2021 | Alta | TF1 + TF2 | docs/imgs/RG300X.png |
| PowKiddy | Q20 Mini | Allwinner F1C100S/F1C500S | 32 MB | 2.4" | 320x240 | 4:3 | Horizontal | 2021 | Media | TF1 | docs/imgs/Q20Mini.png |
| Anbernic | RG351MP | Rockchip RK3326 | 1 GB | 3.5" | 640x480 | 4:3 | Horizontal | 2021 | Alta | TF1 + TF2 | docs/imgs/RG351MP.png |
| PowKiddy | RGB10 Max 2 | Rockchip RK3326 | 1 GB | 5.0" | 854x480 | 16:9 aprox. | Horizontal | 2021 | Alta | TF1 | docs/imgs/RGB10Max2.png |
| Miyoo | Miyoo Mini | SigmaStar SSD202D | 128 MB | 2.8" | 640x480 | 4:3 | Vertical | 2021 | Media | TF1 | docs/imgs/MiyooMini.png |
| Anbernic | RG353P | Rockchip RK3566 | 2 GB | 3.5" | 640x480 | 4:3 | Horizontal | 2022 | Alta | TF1 + TF2 | docs/imgs/RG353P.png |
| Anbernic | RG353V | Rockchip RK3566 | 2 GB | 3.5" | 640x480 | 4:3 | Vertical | 2022 | Alta | TF1 + TF2 | docs/imgs/RG353V.png |
| Anbernic | RG35XX | Actions ATM7039S | 256 MB | 3.5" | 640x480 | 4:3 | Vertical | 2022 | Alta | TF1 + TF2 | docs/imgs/RG35XX.png |
| Miyoo | Miyoo Mini Plus | SigmaStar SSD202D | 128 MB | 3.5" | 640x480 | 4:3 | Vertical | 2023 | Alta | TF1 | docs/imgs/MiyooMiniPlus.png |
| Anbernic | RG35XX Plus | Allwinner H700 | 1 GB | 3.5" | 640x480 | 4:3 | Vertical | 2023 | Alta | TF1 + TF2 | docs/imgs/RG35XXPlus.png |
| Data Frog | SF2000 | HCSEMI B210 / MIPS | 128 MB | 3.0" aprox. | 320x240 | 4:3 | Horizontal | 2023 | Media | TF1 | docs/imgs/SF2000.png |
| Anbernic | RGNano | ARM Cortex-A7 / FunKey-class SoC | 64 MB | 1.54" | 240x240 | 1:1 | Mini vertical | 2023 | Media | TF1 | docs/imgs/RGNano.png |
| TrimUI | TRIMUI Smart Pro | Allwinner A133P | 1 GB | 4.96" | 1280x720 | 16:9 | Horizontal | 2023 | Alta | TF1 | docs/imgs/TrimUISmartPro.png |
| TrimUI | Model S | Allwinner F1C200S (ARM9 628 MHz) | 64 MB | 2.0" | 320x240 | 4:3 | Horizontal | 2022 | Media | TF1 | docs/imgs/ModelS.png |
| PowKiddy | A30 | Allwinner F1C200S (ARM9 mononúcleo) | 64 MB LPDDR2 | 2.8" | 320x240 | 4:3 | Horizontal | 2021 | Baja | TF1 | docs/imgs/PowkiddyA30.png |
| Anbernic | RG35XXH | Allwinner H700 | 1 GB | 3.5" | 640x480 | 4:3 | Horizontal | 2024 | Alta | TF1 + TF2 | docs/imgs/RG35XXH.png |
| Anbernic | RGARC-S | Rockchip RK3566 | 1 GB | 4.0" | 640x480 | 4:3 | Horizontal | 2023 | Alta | TF1 + TF2 | docs/imgs/RGARCS.png |
| Miyoo | A30 | Allwinner A33 | 512 MB | 2.8" | 640x480 | 4:3 | Horizontal | 2024 | Media | TF1 | docs/imgs/MiyooA30.png |
| Anbernic | RG28XX | Allwinner H700 | 1 GB | 2.8" | 640x480 | 4:3 | Horizontal | 2024 | Alta | TF1 + TF2 | docs/imgs/RG28XX.png |
| Anbernic | RG35XXSP | Allwinner H700 | 1 GB | 3.5" | 640x480 | 4:3 | Clamshell horizontal | 2024 | Alta | TF1 + TF2 | docs/imgs/RG35XXSP.png |
| Anbernic | RG34XX | Allwinner H700 | 1 GB | 3.4" | 640x480 | 4:3 | Vertical | 2024 | Alta | TF1 + TF2 | docs/imgs/RG34XX.png |
| Anbernic | RG34XXSP | Allwinner H700 | 1 GB | 3.4" | 640x480 | 4:3 | Clamshell horizontal | 2024 | Alta | TF1 + TF2 | docs/imgs/RG34XXSP.png |
| PowKiddy | RS-07 | Ingenic JZ4760B | 128 MB | 4.3" | 480x272 aprox. | 16:9 | Arcade tabletop horizontal | 2020 aprox. | Alta | TF Interna | docs/imgs/PowKiddyRS-07.png |
| PowKiddy | RS-12 | SoC ARM genérico 32-bit single-core | 32 MB | 3.0" | 320x240 | 4:3 | Arcade tabletop horizontal | 2020/2021 aprox. | Media | TF1 | docs/imgs/PowKiddyRS-12.png |
| PowKiddy | V10 | Rockchip RK3326 | 1 GB | 3.5" | 480x320 | 3:2 | Vertical | 2024 | Media | TF1 | docs/imgs/V10.png |
| Anbernic | RG40XXV | Allwinner H700 | 1 GB | 4.0" | 640x480 | 4:3 | Vertical | 2024 | Alta | TF1 + TF2 | docs/imgs/RG40XXV.png |
| GKD | Bubble | Rockchip RK3566 | 1 GB | 3.5" IPS laminada | 640x480 | 4:3 | Horizontal | 2024 | Alta | TF1 + TF2 | docs/imgs/GKDBubble.png |
| Anbernic | RG40XXH | Allwinner H700 | 1 GB | 4.0" | 640x480 | 4:3 | Horizontal | 2024 | Alta | TF1 + TF2 | docs/imgs/RG40XXH.png |
| TrimUI | TRIMUI Brick | Allwinner A133 Plus | 1 GB | 3.2" | 1024x768 | 4:3 | Vertical | 2024 | Alta | TF1 | docs/imgs/TrimUIBrick.png |
| PowKiddy | V90S | Allwinner A133 Plus | 1 GB | 3.5" | 640x480 | 4:3 | Clamshell horizontal | 2025 | Alta | TF1 | docs/imgs/V90S.png |

| Miyoo | Miyoo Mini Flip | SigmaStar SSD202D / dual-core Cortex-A7 1.2 GHz | 128 MB | 2.8" IPS | 750x560 | 4:3 aprox. | Clamshell horizontal | 2025/2026 | Media-Alta | TF1 | docs/imgs/MiyooMiniFlip.png |
| Miyoo | Miyoo Flip | Rockchip RK3566 | 1 GB | 3.5" | 640x480 | 4:3 | Clamshell horizontal | 2025 | Media | TF1 + TF2 | docs/imgs/MiyooFlip.png |
| Anbernic | RGDS | Rockchip RK3568 | 3 GB | 2x4.0" | 640x480 cada pantalla | 4:3 | Dual-screen clamshell | 2025 | Alta | TF1 + TF2 | docs/imgs/RGDS.png |
| GKD | Pixel 2 | Rockchip RK3326S (4x Cortex-A35 @ 1.5 GHz) | 1 GB DDR3 | 2.4" | 640x480 | 4:3 | Vertical | 2025 | Muy alta | TF1 | docs/imgs/GKDPixel2.png |
| AYN | Odin 2 Portal (Base) | Snapdragon 8 Gen 2 | 8 GB | 7.0" AMOLED | 1920x1080 | 16:9 | Horizontal | 2024/2025 | Alta | Interna (128 GB) + TF1 | docs/imgs/OdinPortal.png |
| PowKiddy | X18 | MediaTek MT8163 (4x Cortex-A53 @ 1.3 GHz) | 2 GB | 5.5" | 1280x720 | 16:9 | Clamshell horizontal | 2018/2019 | Media-Alta | Interna (16 GB) + TF1 | docs/imgs/X18.png |
| GPD | Win | Intel Atom x7-Z8750 | 4 GB | 5.5" | 1280x720 | 16:9 | Clamshell horizontal | 2016 | Muy alta | Interna (64 GB) + TF1 | docs/imgs/GPDWin.png |
| Anbernic | RGVita (Base) | Unisoc Tiger T618 | 3 GB | 5.46" IPS INCELL táctil | 1280x720 | 16:9 | Horizontal | 2026 | Alta | Interna (64 GB) + TF1 | docs/imgs/RGVita.png |
| GKD | 350H | Ingenic X1830 (2x MIPS 1.5 GHz) | 128 MB | 3.5" | 320x240 | 4:3 | Horizontal | 2019 | Media-Alta | Interna (16 GB) + TF1 | docs/imgs/GKD350H.png |
| Retroid | Pocket 2 | MediaTek MT6580 (4x 1.3 GHz) | 1 GB | 3.5" | 640x480 | 4:3 | Horizontal | 2020 | Alta | Interna (8 GB) + TF1 | docs/imgs/RetroidPocket2.png |
| Anbernic | RG CubeXX | Allwinner H700 (4x Cortex-A53 1.5 GHz) | 1 GB LPDDR4 | 3.95" IPS OCA | 720x720 | 1:1 | Horizontal | 2024 | Alta | TF1 + TF2 | docs/imgs/RGCubeXX.png |
| Genérico | TV Box S905 (Super Console X / Stick) | Amlogic S905X (4x Cortex-A53 @ 1.5 GHz) | 1 GB DDR3 | — | 1920x1080 | 16:9 | SBC | 2020 | Media-Baja | Interna (8 GB) + TF1 | docs/imgs/SuperConsoleX.png |
