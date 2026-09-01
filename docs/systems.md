# Sistemas

Catálogo de sistemas emulados con sus identificadores canónicos y parámetros técnicos de referencia. Es la fuente de verdad para identificadores de sistema: cualquier referencia a un sistema en otros documentos debe usar el identificador canónico definido aquí.

Los identificadores canónicos corresponden a los nombres de carpeta usados habitualmente en ES-DE, Batocera y distribuciones compatibles. No deben renombrarse sin actualizar todas las referencias cruzadas.

## DATs de referencia

Los DATs usados para verificación y curación de romsets están en `metadata/dat/`:

| Carpeta | Contenido |
| --- | --- |
| `metadata/dat/No-Intro/` | DATs de No-Intro para consolas y handhelds |
| `metadata/dat/Non-Redump/` | DATs de Non-Redump para sistemas ópticos (contenido que Redump no cubre oficialmente: prototipos, betas, demos) |
| `metadata/dat/Redump/` | DATs de Redump (redump.org) para el catálogo retail real de sistemas ópticos |
| `metadata/dat/arcade/` | DATs de FinalBurn Neo y MAME (2000, 2003, 2003-plus, 2010, 2015, 2016) |
| `metadata/dat/hyperspin/` | DATs de Hyperspin |
| `metadata/dat/libretro/` | DATs de libretro-database |
| `metadata/dat/TOSEC/` | DATs de TOSEC (tosecdev.org), sobre todo microcomputadoras y sistemas de nicho |
| `metadata/dat/custom/` | DATs propios |

La asociación entre sistemas y DATs concretos se documenta en `docs/romsets.md`.

---

## Convenciones

### Identificador canónico

Nombre de carpeta normalizado usado en frontends compatibles con EmulationStation. Se escribe en minúsculas, sin espacios. Ejemplos: `nes`, `megadrive`, `psx`, `mame`.

### Cores RetroArch habituales

Nombre interno del core tal como aparece en RetroArch (`nombre_del_core`). Los cores marcados con `*` tienen soporte limitado o son experimentales.

### Columnas

| Columna | Descripción |
| --- | --- |
| Nombre del sistema | Nombre internacional más reconocido del sistema |
| Año | Año de lanzamiento comercial |
| Identificador canónico | Nombre de carpeta normalizado para frontends compatibles con EmulationStation |
| Nombres regionales/comerciales | Variantes de nombre por región o mercado |
| Aspect Ratio | Relación de aspecto de la señal de vídeo nativa |
| Resolución nativa típica | Resolución de salida más habitual del hardware original |
| Orientación | Orientación típica de la pantalla o señal de vídeo |
| Cores RetroArch habituales | Cores recomendados para RetroArch; `*` indica soporte limitado |
| Emuladores standalone habituales | Emuladores independientes más utilizados |

---

## Consolas

| Nombre del sistema | Año | Identificador canónico | Nombres regionales/comerciales | Aspect Ratio | Resolución nativa típica | Orientación | Cores RetroArch habituales | Emuladores standalone habituales |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Fairchild Channel F | 1976 | `channelf` | Fairchild Video Entertainment System (VES, nombre de lanzamiento original), SABA Videoplay, Luxor Video Entertainment System/Computer, Adman Grandstand Video Entertainment Computer | [TODO] (4:3 inferido por salida TV estándar de la época, no confirmado como spec propia del hardware) | 128×64 (VRAM); ~102×58 visible con overscan | Horizontal | `freechaf` | MAME/MESS (sin standalone dedicado conocido) |
| Atari 2600 | 1977 | `atari2600` | Atari VCS | 4:3 | 160×192 (NTSC) típico | Horizontal | `stella` | Stella |
| Bally Astrocade | 1978 | `astrocade` | Bally Home Library Computer | 4:3 | 160×102 típico | Horizontal | `mame` | MAME |
| Magnavox Odyssey 2 | 1978 | `odyssey2` | Philips Videopac G7000 | 4:3 | 160×200 típico | Horizontal | `o2em` | O2EM |
| Mattel Intellivision | 1979 | `intellivision` | Mattel Electronics Intellivision | 4:3 | 159×192 (NTSC) típico | Horizontal | `freeintv` | FreeIntv |
| Nintendo Game & Watch | 1980 | `gameandwatch` | Game & Watch | Variable | Variable | Horizontal/Vertical | `gw`, `mame` | MAME |
| Atari 5200 | 1982 | `atari5200` | Atari 5200 SuperSystem | 4:3 | 320×192 típico | Horizontal | `atari800` | Atari800 |
| GCE Vectrex | 1982 | `vectrex` | Vectrex | 4:3 aprox. | Vector (sin resolución de trama) | Horizontal | `vecx` | VecX |
| ColecoVision | 1982 | `coleco` | CBS ColecoVision (Europa) | 4:3 | 256×192 | Horizontal | `gearcoleco`, `bluemsx` | ColEm |
| Emerson Arcadia 2001 | 1982 | `arcadia2001` | Bandai Arcadia, Leisure Vision, Interton VC 4000... (30+ clones) | [TODO] | [TODO] (128×104 o 128×208, fuentes contradictorias) | Horizontal | `mame` (driver `arcadia`) | MAME |
| Atari 7800 | 1986 | `atari7800` | Atari 7800 ProSystem | 4:3 | 320×200 típico | Horizontal | `prosystem`, `stella` | ProSystem |
| Nintendo Entertainment System | 1983 | `nes` | Famicom | 4:3 | 256×240 | Horizontal | `fceumm`, `nestopia`, `mesen` | Mesen |
| Sega SG-1000 | 1983 | `sg1000` | — | 4:3 | 256×192 | Horizontal | `genesis-plus-gx`, `smsplus-gx`, `gearsystem` | Gearsystem |
| Sega Master System | 1985 | `mastersystem` | Sega Mark III | 4:3 | 256×192 | Horizontal | `genesis-plus-gx`, `smsplus-gx`, `gearsystem` | Gearsystem |
| Famicom Disk System | 1986 | `fds` | FDS | 4:3 | 256×240 | Horizontal | `fceumm`, `nestopia`, `mesen` | Mesen |
| PC Engine | 1987 | `pcengine` | TurboGrafx-16 | 4:3 | 256×239 típico | Horizontal | `mednafen_pce_fast`, `beetle_pce_fast` | Mednafen |
| PC Engine CD | 1988 | `pcenginecd` | TurboGrafx-CD | 4:3 | 256×239 típico | Horizontal | `mednafen_pce_fast`, `beetle_pce_fast` | Mednafen |
| Sega Mega Drive | 1988 | `megadrive` | Genesis | 4:3 | 320×224 típico | Horizontal | `genesis-plus-gx`, `picodrive`, `blastem` | BlastEm, Kega Fusion |
| Nintendo Game Boy | 1989 | `gb` | Game Boy DMG | 10:9 | 160×144 | Horizontal | `gambatte`, `sameboy`, `mgba` | SameBoy, BGB |
| Atari Lynx | 1989 | `lynx` | — | 5:3 | 160×102 | Horizontal/Vertical | `handy`, `beetle_lynx` | Mednafen |
| Sega Game Gear | 1990 | `gamegear` | — | 10:9 | 160×144 | Horizontal | `genesis-plus-gx`, `smsplus-gx`, `gearsystem` | Gearsystem |
| Super Nintendo Entertainment System | 1990 | `snes` | Super Famicom | 4:3 | 256×224 típico | Horizontal | `snes9x`, `bsnes`, `mesen-s` | bsnes, Snes9x |
| Neo Geo AES | 1990 | `neogeo` | Neo Geo Home System | 4:3 | 320×224 | Horizontal | `fbneo`, `mame` | FinalBurn Neo, MAME |
| Neo Geo CD | 1994 | `neogeocd` | Neo-Geo CD, NGCD | 4:3 | 320×224 | Horizontal | `fbneo`, `mame` | FinalBurn Neo, MAME |
| Amstrad GX4000 | 1990 | `gx4000` | — | 4:3 | 320×200 típico | Horizontal | `cap32`, `mame` | Caprice32 |
| Amiga CDTV | 1991 | `amigacdtv` | Commodore CDTV | 4:3 | Variable (320×256 PAL típico) | Horizontal | `puae` | FS-UAE, WinUAE |
| Philips CD-i | 1991 | `cdi` | CD-i | 4:3 | Variable (384×280 típico) | Horizontal | `mame`, `same_cdi` | CD-i Emulator, MAME |
| Sega CD | 1991 | `segacd` | Mega-CD | 4:3 | 320×224 típico | Horizontal | `genesis-plus-gx`, `picodrive` | Kega Fusion, BlastEm |
| Mega Duck | 1993 | `megaduck` | Cougar Boy (USA), Creatronic/Videojet (Europa) | 10:9 (calculado, mismo formato de píxel que Game Boy) | 160×144 | Horizontal | `sameduck` | [TODO] (Super Junior SameDuck existe como fork de SameBoy, madurez/mantenimiento sin verificar) |
| Panasonic 3DO | 1993 | `3do` | 3DO Interactive Multiplayer | 4:3 | 320×240 típico | Horizontal | `opera` | 4DO |
| Atari Jaguar | 1993 | `jaguar` | — | 4:3 | Variable (320×240 típico) | Horizontal | `virtualjaguar` | BigPEmu |
| Amiga CD32 | 1993 | `amigacd32` | Commodore CD32 | 4:3 | Variable (320×256 PAL típico) | Horizontal | `puae` | FS-UAE, WinUAE |
| Sony PlayStation | 1994 | `psx` | PlayStation, PS1 | 4:3 | Variable (320×240 típico) | Horizontal | `pcsx_rearmed`, `swanstation`, `duckstation`, `beetle_psx_hw` | DuckStation, Mednafen |
| Sega Saturn | 1994 | `saturn` | — | 4:3 | Variable (320×224 típico) | Horizontal | `beetle_saturn`, `yabasanshiro` | Yaba Sanshiro, Mednafen, Kronos |
| Sega 32X | 1994 | `sega32x` | Genesis 32X, Mega Drive 32X, Super 32X | 4:3 | 320×224 típico | Horizontal | `picodrive` | Kega Fusion |
| Super Game Boy | 1994 | `sgb` | SGB | 10:9 | 160×144 | Horizontal | `same_boy` | SameBoy |
| Atari Jaguar CD | 1995 | `jaguarcd` | — | 4:3 | Variable (320×240 típico) | Horizontal | `virtualjaguar` | BigPEmu |
| Satellaview | 1995 | `satellaview` | BS-X | 4:3 | 256×224 típico | Horizontal | `snes9x`, `bsnes` | bsnes |
| Sufami Turbo | 1996 | `sufami` | — | 4:3 | 256×224 típico | Horizontal | `snes9x`, `bsnes` | bsnes |
| Nintendo 64 | 1996 | `n64` | N64 | 4:3 | Variable (320×240 típico) | Horizontal | `mupen64plus-next`, `parallel-n64` | Mupen64Plus, Project64, simple64 |
| Nintendo 64DD | 1999 | `64dd` | 64DD | 4:3 | Variable (320×240 típico) | Horizontal | `mupen64plus-next`, `parallel-n64` | Mupen64Plus, simple64 |
| Neo Geo Pocket | 1998 | `ngp` | — | 20:19 aprox. | 160×152 | Horizontal | `mednafen_ngp`, `race` | Mednafen |
| Nintendo Game Boy Color | 1998 | `gbc` | Game Boy Colour | 10:9 | 160×144 | Horizontal | `gambatte`, `sameboy`, `mgba` | SameBoy, BGB |
| Sega Dreamcast | 1998 | `dreamcast` | — | 4:3 | 640×480 | Horizontal | `flycast` | Flycast, Redream, Demul |
| Neo Geo Pocket Color | 1999 | `ngpc` | Neo Geo Pocket Colour | 20:19 aprox. | 160×152 | Horizontal | `mednafen_ngp`, `race` | Mednafen |
| Watara Supervision | 1992 | `supervision` | QuickShot Supervision | 1:1 | 160×160 | Horizontal | `potator` | MAME |
| Sony PlayStation 2 | 2000 | `ps2` | PS2 | 4:3 | Variable (640×448 típico) | Horizontal | `lrpcsx2`* | PCSX2 |
| Pokémon Mini | 2001 | `pokemini` | Pokémon mini | 3:2 | 96×64 | Horizontal | `pokemini` | PokeMini |
| Nintendo Game Boy Advance | 2001 | `gba` | GBA | 3:2 | 240×160 | Horizontal | `mgba`, `gpsp`, `vba-next` | mGBA, VBA-M |
| Nintendo GameCube | 2001 | `gamecube` | GameCube | 4:3 | 640×480 típico | Horizontal | `dolphin` | Dolphin |
| Nintendo DS | 2004 | `nds` | DS, NDS | 4:3 | 256×192 cada pantalla | Dual-screen | `melonds`, `desmume` | melonDS, DeSmuME |
| Nintendo DSi | 2008 (JP) / 2009 (NA/EU/AU) | `ndsi` | Nintendo DSi | 4:3 (por pantalla) | 256×192 cada pantalla | Dual-screen | `melonds` (modo DSi) | melonDS |
| DSiWare | 2008 | `dsiware` | Nintendo DSi (Digital) | 4:3 | 256×192 cada pantalla | Dual-screen | `melonds` | melonDS |
| Sony PlayStation Portable | 2004 | `psp` | PSP | 16:9 | 480×272 | Horizontal | `ppsspp` | PPSSPP |
| PlayStation Minis | 2009 | `pspminis` | PSP minis, PSN Minis | 16:9 | 480×272 | Horizontal | `ppsspp` | PPSSPP |
| PlayStation Network (PSP) | 2008 | `psn` | PSN, PSP Digital | 16:9 | 480×272 | Horizontal | `ppsspp` | PPSSPP |
| Microsoft Xbox | 2001 | `xbox` | Xbox | 4:3 / 16:9 | 480p típico | Horizontal | — | xemu |
| Microsoft Xbox 360 | 2005 | `xbox360` | Xbox 360 | 16:9 | 1280×720 típico | Horizontal | — | Xenia |
| Nintendo Wii | 2006 | `wii` | Wii | 4:3 / 16:9 | 640×480 típico | Horizontal | `dolphin` | Dolphin |
| Sony PlayStation 3 | 2006 | `ps3` | PS3 | 16:9 | 1280×720 típico | Horizontal | — | RPCS3 |
| Nintendo 3DS | 2011 | `3ds` | 3DS | 5:3 aprox. | 400×240 superior; 320×240 inferior | Dual-screen | — | Lime3DS, Citra |
| Nintendo 3DS eShop | 2011 | `3dseshop` | Nintendo 3DS (Digital) | 5:3 aprox. | 400×240 superior; 320×240 inferior | Dual-screen | — | Lime3DS, Citra |
| New Nintendo 3DS | 2014 | `newn3ds` | New 3DS, N3DS | 5:3 aprox. | 400×240 superior; 320×240 inferior | Dual-screen | — | Lime3DS, Citra |
| Sony PlayStation Vita | 2011 | `psvita` | PS Vita | 16:9 | 960×544 | Horizontal | `vitaquake2`* | Vita3K |
| Nintendo Wii U | 2012 | `wiiu` | Wii U | 16:9 | 1280×720 típico | Horizontal | `cemu` | Cemu |
| Nintendo Switch | 2017 | `switch` | Switch | 16:9 | 1280×720 portátil; 1920×1080 dock | Horizontal | — | Ryujinx, Sudachi, Suyu |
| Nintendo Virtual Boy | 1995 | `virtualboy` | Virtual Boy | 12:7 aprox. | 384×224 | Horizontal | `beetle_vb` | Mednafen |
| WonderSwan | 1999 | `wswan` | WonderSwan Mono | 14:9 aprox. | 224×144 | Horizontal/Vertical | `mednafen_wswan` | Mednafen |
| WonderSwan Color | 2000 | `wswanc` | SwanCrystal | 14:9 aprox. | 224×144 | Horizontal/Vertical | `mednafen_wswan` | Mednafen |

## Arcade

| Nombre del sistema | Año | Identificador canónico | Nombres regionales/comerciales | Aspect Ratio | Resolución nativa típica | Orientación | Cores RetroArch habituales | Emuladores standalone habituales |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| MAME | 1997 | `mame` | Multiple Arcade Machine Emulator | Variable | Variable | Horizontal/Vertical | `mame`, `mame2003-plus`, `mame2010` | MAME |
| FinalBurn Neo | 2019 | `fbneo` | FBNeo, Final Burn Neo | Variable | Variable | Horizontal/Vertical | `fbneo` | FinalBurn Neo |
| Neo Geo MVS | 1990 | `neogeo` | Multi Video System (MVS) | 4:3 | 320×224 | Horizontal | `fbneo`, `mame` | FinalBurn Neo, MAME |
| Capcom Play System I | 1988 | `cps1` | CPS-1 | 4:3 | 384×224 | Horizontal | `fbneo`, `mame` | FinalBurn Neo, MAME |
| Capcom Play System II | 1993 | `cps2` | CPS-2 | 4:3 | 384×224 | Horizontal | `fbneo`, `mame` | FinalBurn Neo, MAME |
| Capcom Play System III | 1996 | `cps3` | CPS-3 | 4:3 | 384×224 | Horizontal | `fbneo`, `mame` | FinalBurn Neo, MAME |
| Sega NAOMI | 1998 | `naomi` | New Arcade Operation Machine Idea | 4:3 | 640×480 | Horizontal | `flycast` | Flycast |
| Sammy Atomiswave | 2003 | `atomiswave` | Atomiswave | 4:3 | 640×480 | Horizontal | `flycast` | Flycast |
| LaserDisc Arcade | 1983 | `daphne` | Daphne, Dragon's Lair Hardware | Variable | Variable | Horizontal | — | Daphne, Hypseus Singe |
| Sega NAOMI 2 | 2000 | `naomi2` | NAOMI 2 | 4:3 | 640×480 | Horizontal | — | Flycast |

## Microcomputers

| Nombre del sistema | Año | Identificador canónico | Nombres regionales/comerciales | Aspect Ratio | Resolución nativa típica | Orientación | Cores RetroArch habituales | Emuladores standalone habituales |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| Atari 8-bit Family | 1979 | `atari800` | Atari 400, 800, XL, XE | 4:3 | Variable (320×192 típico) | Horizontal | `atari800` | Atari800 |
| Commodore VIC-20 | 1980 | `vic20` | VC-20 (Alemania), VIC-1001 (Japón) | 4:3 | Variable (176×184 típico) | Horizontal | `vice_xvic` | VICE |
| Sinclair ZX81 | 1981 | `zx81` | Timex Sinclair 1000 | 4:3 | 256×192 típico | Horizontal | `81`, `mame` | EightyOne, MAME |
| Dragon 32 / Dragon 64 | 1982 | `dragon32` | Dragon 64, Tano Dragon | 4:3 | 256×192 típico | Horizontal | `xroar`, `mame` | XRoar, MAME |
| Commodore 64 | 1982 | `c64` | C64 | 4:3 | Variable (320×200 típico) | Horizontal | `vice_x64sc`, `vice_x128`, `vice_xplus4` | VICE |
| ZX Spectrum | 1982 | `spectrum` | Sinclair ZX Spectrum | 4:3 | 256×192 | Horizontal | `fuse` | Fuse |
| MSX | 1983 | `msx` | — | 4:3 | Variable (256×192 típico) | Horizontal | `fmsx`, `bluemsx` | openMSX, blueMSX |
| Commodore Plus/4 | 1984 | `plus4` | Commodore 16, Commodore 116, Plus/4 | 4:3 | Variable (320×200 típico) | Horizontal | `vice_xplus4` | VICE |
| Amstrad CPC | 1984 | `amstradcpc` | CPC 464, CPC 664, CPC 6128 | 4:3 | Variable (320×200 típico) | Horizontal | `cap32` | Caprice32, Arnold |
| Thomson MO5 / TO8 | 1984 | `thomson` | MO5, MO6, TO7, TO8, TO8D, TO9, TO9+ | 4:3 | 320×200 (MO5) | Horizontal | `theodore` | Theodore |
| Commodore 128 | 1985 | `c128` | C128 | 4:3 | Variable (320×200 típico) | Horizontal | `vice_x128` | VICE |
| Atari ST | 1985 | `atarist` | Atari 520ST, 1040ST | 4:3 | Variable (320×200 típico) | Horizontal | `hatari` | Hatari |
| Commodore Amiga | 1985 | `amiga` | Amiga 500, Amiga 1200 | 4:3 | Variable (320×256 PAL típico) | Horizontal | `puae` | FS-UAE, WinUAE |
| MSX2 | 1985 | `msx2` | — | 4:3 | Variable (256×212 típico) | Horizontal | `fmsx`, `bluemsx` | openMSX, blueMSX |
| Sharp X68000 | 1987 | `sharpx68000` | X68000 | 4:3 | Variable (512×512 / 768×512 típico) | Horizontal | `px68k` | XM6 TypeG |

## Engines / Ports

| Nombre del sistema | Año | Identificador canónico | Nombres regionales/comerciales | Aspect Ratio | Resolución nativa típica | Orientación | Cores RetroArch habituales | Emuladores standalone habituales |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- |
| ScummVM | 2001 | `scummvm` | Script Creation Utility for Maniac Mansion Virtual Machine | Variable | Variable | Horizontal | `scummvm` | ScummVM |
| OpenBOR | 2004 | `openbor` | Open Beats of Rage, Beats of Rage Engine | Variable | Variable | Horizontal | `openbor` | OpenBOR |
| PortMaster | 2021 | `ports` | Ports, Native Ports | Variable | Variable | Horizontal | — | PortMaster |
| DOSBox | 2002 | `dos` | DOS, MS-DOS, PC DOS, DOSBox | Variable | Variable (320×200 típico) | Horizontal | `dosbox-pure`, `dosbox-svn` | DOSBox, DOSBox-X, DOSBox Staging |
| Doom | 1993 | `doom` | Doom Engine, id Tech 1 | 4:3 | 320×200 típico | Horizontal | `prboom`, `boom3`* | PrBoom+, GZDoom, Chocolate Doom |
| Quake | 1996 | `quake` | Quake Engine, id Tech 2 | 4:3 | Variable (320×240 típico) | Horizontal | `tyrquake` | Quakespasm, vkQuake |
| Quake II | 1997 | `quake2` | Quake II Engine, id Tech 2 | 4:3 | Variable | Horizontal | `vitaquake2`* | Yamagi Quake II |
| Cave Story | 2004 | `cavestory` | Doukutsu Monogatari | 4:3 | 320×240 típico | Horizontal | `nxengine` | NXEngine-evo |

---

## Romsets

La asociación entre estos sistemas y los DATs de `metadata/dat/` (fuente, formato, DAT alternativo, completitud, almacenamiento) se documenta en `docs/romsets.md`, no en este fichero.

## Información de sistemas

| Identificador | Sistema | Referencia de Control (Wikipedia) |
| --- | --- | --- |
| `3do` | 3DO Interactive Multiplayer | https://en.wikipedia.org/wiki/3DO_Interactive_Multiplayer |
| `3ds` | Nintendo 3DS | https://en.wikipedia.org/wiki/Nintendo_3DS |
| `3dseshop` | Nintendo 3DS eShop | https://en.wikipedia.org/wiki/Nintendo_eShop |
| `64dd` | Nintendo 64DD | https://en.wikipedia.org/wiki/Nintendo_64DD |
| `amigacd32` | Amiga CD32 | https://en.wikipedia.org/wiki/Amiga_CD32 |
| `amigacdtv` | Commodore CDTV | https://en.wikipedia.org/wiki/Commodore_CDTV |
| `cdi` | Philips CD-i | https://en.wikipedia.org/wiki/CD-i |
| `dreamcast` | Sega Dreamcast | https://en.wikipedia.org/wiki/Dreamcast |
| `dsiware` | DSiWare | https://en.wikipedia.org/wiki/DSiWare |
| `fds` | Family Computer Disk System | https://en.wikipedia.org/wiki/Family_Computer_Disk_System |
| `gamecube` | Nintendo GameCube | https://en.wikipedia.org/wiki/GameCube |
| `gamegear` | Sega Game Gear | https://en.wikipedia.org/wiki/Game_Gear |
| `gb` | Nintendo Game Boy | https://en.wikipedia.org/wiki/Game_Boy |
| `gba` | Game Boy Advance | https://en.wikipedia.org/wiki/Game_Boy_Advance |
| `gbc` | Game Boy Color | https://en.wikipedia.org/wiki/Game_Boy_Color |
| `gx4000` | Amstrad GX4000 | https://en.wikipedia.org/wiki/Amstrad_GX4000 |
| `jaguar` | Atari Jaguar | https://en.wikipedia.org/wiki/Atari_Jaguar |
| `jaguarcd` | Atari Jaguar CD | https://en.wikipedia.org/wiki/Atari_Jaguar_CD |
| `lynx` | Atari Lynx | https://en.wikipedia.org/wiki/Atari_Lynx |
| `mastersystem` | Sega Master System | https://en.wikipedia.org/wiki/Master_System |
| `megadrive` | Sega Mega Drive / Genesis | https://en.wikipedia.org/wiki/Sega_Genesis |
| `n64` | Nintendo 64 | https://en.wikipedia.org/wiki/Nintendo_64 |
| `nds` | Nintendo DS | https://en.wikipedia.org/wiki/Nintendo_DS |
| `neogeocd` | Neo Geo CD | https://en.wikipedia.org/wiki/Neo_Geo_CD |
| `nes` | Nintendo Entertainment System | https://en.wikipedia.org/wiki/Nintendo_Entertainment_System |
| `ngp` | Neo Geo Pocket | https://en.wikipedia.org/wiki/Neo_Geo_Pocket |
| `ngpc` | Neo Geo Pocket Color | https://en.wikipedia.org/wiki/Neo_Geo_Pocket_Color |
| `pcengine` | PC Engine / TurboGrafx-16 | https://en.wikipedia.org/wiki/TurboGrafx-16 |
| `pcenginecd` | PC Engine CD / TurboGrafx-CD | https://en.wikipedia.org/wiki/TurboGrafx-CD |
| `pokemini` | Pokémon Mini | https://en.wikipedia.org/wiki/Pok%C3%A9mon_Mini |
| `ps2` | PlayStation 2 | https://en.wikipedia.org/wiki/PlayStation_2 |
| `ps3` | PlayStation 3 | https://en.wikipedia.org/wiki/PlayStation_3 |
| `psp` | PlayStation Portable | https://en.wikipedia.org/wiki/PlayStation_Portable |
| `psx` | PlayStation | https://en.wikipedia.org/wiki/PlayStation_(console) |
| `satellaview` | Satellaview | https://en.wikipedia.org/wiki/Satellaview |
| `saturn` | Sega Saturn | https://en.wikipedia.org/wiki/Sega_Saturn |
| `sega32x` | Sega 32X | https://en.wikipedia.org/wiki/32X |
| `segacd` | Sega CD | https://en.wikipedia.org/wiki/Sega_CD |
| `sg1000` | Sega SG-1000 | https://en.wikipedia.org/wiki/SG-1000 |
| `snes` | Super Nintendo Entertainment System | https://en.wikipedia.org/wiki/Super_Nintendo_Entertainment_System |
| `sufami` | Sufami Turbo | https://en.wikipedia.org/wiki/Sufami_Turbo |
| `supervision` | Watara Supervision | https://en.wikipedia.org/wiki/Watara_Supervision |
| `virtualboy` | Nintendo Virtual Boy | https://en.wikipedia.org/wiki/Virtual_Boy |
| `wii` | Nintendo Wii | https://en.wikipedia.org/wiki/Wii |
| `wiiu` | Nintendo Wii U | https://en.wikipedia.org/wiki/Wii_U |
| `wswan` | WonderSwan | https://en.wikipedia.org/wiki/WonderSwan |
| `wswanc` | WonderSwan Color | https://en.wikipedia.org/wiki/WonderSwan_Color |
| `xbox` | Microsoft Xbox | https://en.wikipedia.org/wiki/Xbox_(console) |
| `xbox360` | Microsoft Xbox 360 | https://en.wikipedia.org/wiki/Xbox_360 |
