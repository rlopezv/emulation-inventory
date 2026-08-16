# Guías de preparación de romsets

Flujos de trabajo para preparar romsets antes de distribuirlos en `data/roms/`. Cada guía es un scaffold pendiente de contenido.

| Flujo | Alcance | Guía |
| --- | --- | --- |
| Cartucho / plano | Consolas de cartucho y handhelds verificados con DAT No-Intro | [cartridge.md](cartridge.md) |
| Microcomputers | Commodore 64/128, Amiga, ZX Spectrum/81, MSX/MSX2, Amstrad CPC, Atari ST, Sharp X68000...; diversidad de medio (cinta/disco/cartucho) y minoría de fuentes distintas a No-Intro | [microcomputers.md](microcomputers.md) |
| Óptico → CHD | Sistemas ópticos (PSX, Saturn, Dreamcast, PC Engine CD, Sega CD, etc.) verificados con DAT Redump (Non-Redump para protos/betas) y convertidos con CHDMan | [optical-chd.md](optical-chd.md) |
| Arcade | MAME/FBNeo, elección de tipo de set (split/merged/non-merged), BIOS y samples | [arcade.md](arcade.md) |
| Workflow end-to-end | Flujo completo DAT → auditoría → 1G1R → parcheo → compresión → gamelist, encadenando las herramientas de `docs/software.md` | [workflow.md](workflow.md) |
| Pipeline propio (tools/scripts) | Estado actual del pipeline de scripts del repo (DAT → dat-index → docs, ROMs físicas) y roadmap de ampliaciones propuestas | [custom-pipeline.md](custom-pipeline.md) |
| Bitácora de procesado | Registro cronológico de sesiones reales de trabajo, no prescriptivo — base empírica para detectar qué automatizar | [bitacora.md](bitacora.md) |

## Clasificación de sistemas por flujo

Qué guía de la tabla de arriba aplica a cada identificador canónico de `docs/systems.md`. Es la base para añadir, en cada guía, un apartado de "formato de ROM recomendado" sin ambigüedad sobre a qué sistemas aplica.

### Consolas / handhelds

| Identificador canónico | Flujo | Notas |
| --- | --- | --- |
| `atari2600` | Cartucho / plano | |
| `astrocade` | Cartucho / plano | |
| `odyssey2` | Cartucho / plano | |
| `intellivision` | Cartucho / plano | |
| `gameandwatch` | Cartucho / plano | Fuente libretro (ClrMamePro texto), no No-Intro |
| `atari5200` | Cartucho / plano | |
| `vectrex` | Cartucho / plano | |
| `atari7800` | Cartucho / plano | |
| `nes` | Cartucho / plano | |
| `sg1000` | Cartucho / plano | |
| `mastersystem` | Cartucho / plano | |
| `fds` | Cartucho / plano | |
| `pcengine` | Cartucho / plano | |
| `pcenginecd` | Óptico | CHD |
| `megadrive` | Cartucho / plano | |
| `gb` | Cartucho / plano | |
| `lynx` | Cartucho / plano | |
| `gamegear` | Cartucho / plano | |
| `snes` | Cartucho / plano | |
| `neogeo` | Arcade | AES (cartucho doméstico) y MVS comparten romset; mismo DAT que la sección Arcade — ver `docs/romsets.md` |
| `neogeocd` | Óptico | CHD |
| `gx4000` | Caso especial | Fuente TOSEC, set predominantemente homebrew mal mantenido (catálogo comercial original muy reducido); requiere curación/proceso manual, no encaja limpio en Cartucho/plano ni Microcomputers |
| `amigacdtv` | Óptico | CHD |
| `cdi` | Óptico | CHD; solo DAT Non-Redump hoy (pendiente Redump) |
| `segacd` | Óptico | CHD |
| `3do` | Óptico | CHD |
| `jaguar` | Cartucho / plano | |
| `amigacd32` | Óptico | CHD |
| `psx` | Óptico | CHD |
| `saturn` | Óptico | CHD |
| `sega32x` | Cartucho / plano | |
| `sgb` | Caso especial | Sin DAT propio; requiere procesar el No-Intro de `gb`/`gbc` para extraer los títulos con soporte Super Game Boy (cartuchos con función especial en modo SGB) |
| `jaguarcd` | Óptico | CHD |
| `satellaview` | Cartucho / plano | |
| `sufami` | Cartucho / plano | |
| `n64` | Cartucho / plano | |
| `64dd` | Cartucho / plano | |
| `ngp` | Cartucho / plano | |
| `gbc` | Cartucho / plano | Subconjunto "dual-mode"/DMG-compatible (cartucho gris): juegos de GBC pensados para funcionar también en Game Boy original monocromo; no requiere tratamiento distinto de DAT, es una propiedad del título dentro del mismo No-Intro |
| `dreamcast` | Óptico | CHD |
| `ngpc` | Cartucho / plano | |
| `supervision` | Cartucho / plano | |
| `ps2` | Óptico | CHD |
| `pokemini` | Cartucho / plano | |
| `gba` | Cartucho / plano | |
| `gamecube` | Óptico | No usa CHD — usa RVZ (ver caso especial ya documentado en `optical-chd.md`) |
| `nds` | Cartucho / plano | |
| `dsiware` | Cartucho / plano | Digital, sin medio físico |
| `psp` | Óptico | UMD físico; fuente Redump (`metadata/dat/Redump/Sony - PlayStation Portable - Datfile (3500)...dat`), **todavía no mapeado en `build-dat-index-redump.ps1`** (gap pendiente, ver `docs/session-context.md`); formato de juego recomendado CSO (comprimido, más eficiente), manteniendo el romset fuente en ISO |
| `pspminis` | Cartucho / plano | Digital PSN, DAT No-Intro propio |
| `psn` | Cartucho / plano | Digital PSN, DAT No-Intro propio |
| `xbox` | Óptico | No usa CHD — XISO |
| `xbox360` | Óptico | Solo DAT Non-Redump hoy (pendiente Redump) |
| `wii` | Óptico | No usa CHD — usa RVZ (igual que `gamecube`) |
| `ps3` | Óptico | Solo DAT Non-Redump hoy (pendiente Redump) |
| `3ds` | Cartucho / plano | Cartucho físico; DAT No-Intro `Nintendo - Nintendo 3DS (Decrypted)`. Formato de juego recomendado: `.3DS` (Desencriptado) o `.CCI` (comprimido, CSO para 3DS) |
| `3dseshop` | Cartucho / plano | Digital eShop; DAT No-Intro `Nintendo - Nintendo 3DS (Digital) (CDN)` — existen además `(Digital) (Updates)` y `(Digital) (DLC)` sin mapear todavía como fila propia en `docs/romsets.md` |
| `newn3ds` | Cartucho / plano | |
| `psvita` | Cartucho / plano | Solo cubierto el catálogo digital (No-Intro `Sony - PlayStation Vita (PSN) (Content)`/`(Updates)`); sin DAT del catálogo físico en tarjeta. Formatos soportados por Vita3K: `.ZIP` (NoNpDrm comprimido) y `.PKG` (con clave de licencia) |
| `wiiu` | Óptico | Solo DAT Non-Redump hoy (pendiente Redump) |
| `switch` | Sin clasificar | Sin DAT de verificación estándar |
| `virtualboy` | Cartucho / plano | |
| `wswan` | Cartucho / plano | |
| `wswanc` | Cartucho / plano | |

### Arcade

`docs/systems.md#arcade`: `mame`, `fbneo`, `neogeo` (MVS, mismo id que en Consolas), `cps1`, `cps2`, `cps3`, `naomi`, `atomiswave`, `daphne`, `naomi2`, `chihiro`, `triforce` — todos Arcade. `naomi`, `atomiswave`, `chihiro` y `triforce` usan medio GD-ROM/DVD internamente pero se tratan como Arcade (vía MAME/FBNeo/Dolphin), no como Óptico, porque su flujo de romset real pasa por esas herramientas y no por Redump/CHDMan.

### Microcomputers

`docs/systems.md#microcomputers`: `zx81`, `dragon32`, `c64`, `spectrum`, `msx`, `amstradcpc`, `c128`, `atarist`, `amiga`, `msx2`, `sharpx68000` — todos Microcomputers.

### Engines / Ports

`docs/systems.md#engines--ports`: `scummvm`, `openbor`, `ports`, `dos`, `doom`, `quake`, `quake2`, `cavestory`. `docs/romsets.md` ya les dedica su propia sección ("Engines / Ports"), pero **no existe todavía ninguna guía para ellos en la tabla de flujos de arriba** — no encajan en Cartucho/Microcomputers/Óptico/Arcade (la mayoría no tiene romset convencional). Pendiente decidir si merece guía propia.

## Curación por sistema

Información de referencia específica por sistema (catálogo oficial vs. prototipos/homebrew, casos especiales) que no encaja en las tablas de `docs/romsets.md`: ver [systems/](systems/README.md).
