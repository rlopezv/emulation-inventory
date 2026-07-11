# Romsets

Asociación entre los sistemas de `docs/systems.md` y los DATs disponibles en `metadata/dat/`. Los identificadores canónicos usados aquí deben coincidir siempre con los definidos en `docs/systems.md`; este fichero no redefine sistemas, solo documenta sus fuentes de romset.

El nombre de DAT es relativo a la subcarpeta de su fuente (`No-Intro/`, `Non-Redump/`, `Redump/`, `TOSEC/`, `arcade/`, `libretro/`).

Para sistemas ópticos existen dos flujos de verificación según el formato del romset:

| Formato | Fuente de verificación | Herramienta |
| --- | --- | --- |
| ISO / BIN·CUE | DAT Redump o Non-Redump | CLRMamePro, RomVault |
| CHD nativo MAME | Software list XML (`metadata/software-list/`) | MAME `-verifysoftlist`, RomVault |

## Formato de DAT

La columna **Formato** indica el formato de fichero del DAT, necesario para saber qué parser aplica:

- **XML (Logiqx)** — XML con esquema Logiqx/clrmamepro (`<datafile><game name="...">`). Usado por No-Intro, Non-Redump, MAME y FBNeo. Sigue la convención de región entre paréntesis (`(USA)`, `(Japan)`, etc.) y expone relación parent/clone vía `cloneofid`.
- **XML (Logiqx, sin cloneofid)** — mismo esquema XML y misma convención de región, pero los `<game>` de Redump **no incluyen atributos `id`/`cloneofid`**. No permite resolver relación parent/clone automáticamente; la agrupación de familias 1G1R se hace por nombre base exacto, y las equivalencias de título entre regiones (ej. nombre japonés vs. occidental) solo pueden añadirse a mano vía el fichero de alias.
- **XML (Logiqx, TOSEC)** — mismo esquema XML, sin `id`/`cloneofid` (igual que Redump), pero con convención de nombre TOSEC: `Título (Fecha)(Publisher)(Región)[flags]`, donde la región usa **códigos de 2 letras** (`ES`, `FR`, `US`...) en vez de nombres completos, y el primer grupo entre paréntesis suele ser una fecha, no la región. Usado por `metadata/dat/TOSEC/`.
- **ClrMamePro (texto)** — formato de texto plano `clrmamepro ( ... ) game ( ... )`, no XML. Usado por todos los DAT de `metadata/dat/libretro/`. No sigue la convención de región No-Intro (el paréntesis suele ser fabricante/marca) y requiere un parser distinto.

`tools/scripts/build-dat-index-nointro.ps1` procesa DAT **XML (Logiqx)** con `cloneofid` (No-Intro/Non-Redump). `tools/scripts/build-dat-index-redump.ps1` procesa DAT **XML (Logiqx, sin cloneofid)** (Redump), agrupando por nombre base. `tools/scripts/build-dat-index-tosec.ps1` procesa DAT **XML (Logiqx, TOSEC)**, agrupando por nombre base con detección de región por código de 2 letras. Los sistemas en **ClrMamePro (texto)** quedan pendientes de un tratamiento específico.

## Consolas

| Identificador canónico | Fuente | Formato | DAT | Fuente alternativa | DAT alternativo | Completitud | Almacenamiento | Notas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `gameandwatch` | libretro | ClrMamePro (texto) | `Handheld Electronic Game.dat` | — | — | [TODO] | [TODO] | Cubre "Handheld Electronic Game" en general (Nintendo, Mattel, VTech, Tiger...), no solo Nintendo Game & Watch; fuera del alcance de build-dat-index-nointro.ps1 por formato |
| `nes` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo Entertainment System (Headered) (20260504-103615).dat` | — | — | [TODO] | [TODO] | También disponible versión Headerless |
| `fds` | No-Intro | XML (Logiqx) | `Nintendo - Family Computer Disk System (FDS) (20260317-004812).dat` | — | — | [TODO] | [TODO] | |
| `satellaview` | No-Intro | XML (Logiqx) | `Nintendo - Satellaview (20260322-134432).dat` | — | — | [TODO] | [TODO] | |
| `sufami` | No-Intro | XML (Logiqx) | `Nintendo - Sufami Turbo (20240622-035607).dat` | — | — | [TODO] | [TODO] | |
| `sgb` | — | — | — | — | — | [TODO] | [TODO] | Sin DAT específico; usa ROMs de `gb`/`gbc` ejecutadas en modo Super Game Boy |
| `snes` | No-Intro | XML (Logiqx) | `Nintendo - Super Nintendo Entertainment System (20260505-202641).dat` | — | — | [TODO] | [TODO] | |
| `gb` | No-Intro | XML (Logiqx) | `Nintendo - Game Boy (20260501-055403).dat` | — | — | [TODO] | [TODO] | |
| `gbc` | No-Intro | XML (Logiqx) | `Nintendo - Game Boy Color (20260505-192202).dat` | — | — | [TODO] | [TODO] | |
| `gba` | No-Intro | XML (Logiqx) | `Nintendo - Game Boy Advance (20260503-202332).dat` | — | — | [TODO] | [TODO] | |
| `virtualboy` | No-Intro | XML (Logiqx) | `Nintendo - Virtual Boy (20260428-015207).dat` | — | — | [TODO] | [TODO] | |
| `n64` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo 64 (BigEndian) (20260505-135821).dat` | — | — | [TODO] | [TODO] | También disponible ByteSwapped |
| `64dd` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo 64DD (20260221-121754).dat` | — | — | [TODO] | [TODO] | |
| `pokemini` | No-Intro | XML (Logiqx) | `Nintendo - Pokemon Mini (20250407-153358).dat` | — | — | [TODO] | [TODO] | |
| `nds` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo DS (Decrypted) (20260504-004312).dat` | — | — | [TODO] | [TODO] | También disponible Encrypted |
| `dsiware` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo DSi (Digital) (20220506-190731).dat` | — | — | [TODO] | [TODO] | También disponibles variantes Encrypted/Decrypted (20260502) y CDN |
| `3ds` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo 3DS (Decrypted) (20260505-085920).dat` | — | — | [TODO] | [TODO] | Cartuchos físicos. También disponible variante Encrypted |
| `3dseshop` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo 3DS (Digital) (CDN) (20260306-063611).dat` | — | — | [TODO] | [TODO] | Exclusivos de eShop. Virtual Console 3DS pendiente: DAT no descargado en metadata/dat/ |
| `gamecube` | Redump | XML (Logiqx, sin cloneofid) | `Nintendo - GameCube - Datfile (2019) (2026-06-13 18-14-01).dat` | Non-Redump | `Non-Redump - Nintendo - Nintendo GameCube (20260429-160048).dat` | [TODO] | [TODO] | Non-Redump solo cubre protos/betas |
| `wii` | Redump | XML (Logiqx, sin cloneofid) | `Nintendo - Wii - Datfile (3780) (2026-06-15 03-13-28).dat` | Non-Redump | `Non-Redump - Nintendo - Wii (20260412-111452).dat` | [TODO] | [TODO] | Non-Redump solo cubre protos/betas |
| `wiiu` | Non-Redump | XML (Logiqx) | `Non-Redump - Nintendo - Wii U (20260312-235110).dat` | — | — | [TODO] | [TODO] | Pendiente DAT Redump |
| `switch` | — | — | — | — | — | — | [TODO] | Sin DAT de verificación estándar |
| `sg1000` | No-Intro | XML (Logiqx) | `Sega - SG-1000 - SC-3000 (20231205-110448).dat` | — | — | [TODO] | [TODO] | Incluye SC-3000 |
| `mastersystem` | No-Intro | XML (Logiqx) | `Sega - Master System - Mark III (20260428-025956).dat` | — | — | [TODO] | [TODO] | |
| `megadrive` | No-Intro | XML (Logiqx) | `Sega - Mega Drive - Genesis (20260504-203329).dat` | — | — | [TODO] | [TODO] | |
| `sega32x` | No-Intro | XML (Logiqx) | `Sega - 32X (20260317-140429).dat` | — | — | [TODO] | [TODO] | |
| `gamegear` | No-Intro | XML (Logiqx) | `Sega - Game Gear (20260422-014958).dat` | — | — | [TODO] | [TODO] | |
| `segacd` | Redump | XML (Logiqx, sin cloneofid) | `Sega - Mega CD & Sega CD - Datfile (549) (2026-05-28 18-06-58).dat` | Non-Redump | `Non-Redump - Sega - Sega Mega CD + Sega CD (20260413-193714).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/megacd.xml`. Non-Redump solo cubre protos/betas |
| `saturn` | Redump | XML (Logiqx, sin cloneofid) | `Sega - Saturn - Datfile (2457) (2026-06-14 12-36-08).dat` | Non-Redump | `Non-Redump - Sega - Sega Saturn (20260306-190347).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/saturn.xml`. Non-Redump solo cubre protos/betas |
| `dreamcast` | Redump | XML (Logiqx, sin cloneofid) | `Sega - Dreamcast - Datfile (1516) (2026-06-14 18-25-41).dat` | Non-Redump | `Non-Redump - Sega - Dreamcast (20260411-182542).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/dc.xml`. Non-Redump solo cubre protos/betas |
| `psx` | Redump | XML (Logiqx, sin cloneofid) | `Sony - PlayStation - Datfile (10914) (2026-06-15 11-55-46).dat` | Non-Redump | `Non-Redump - Sony - PlayStation (20260430-121343).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/psx.xml`. Non-Redump solo cubre protos/betas |
| `ps2` | Redump | XML (Logiqx, sin cloneofid) | `Sony - PlayStation 2 - Datfile (11774) (2026-06-15 03-41-38).dat` | Non-Redump | `Non-Redump - Sony - PlayStation 2 (20260415-170406).dat` | [TODO] | [TODO] | Non-Redump solo cubre protos/betas |
| `ps3` | Non-Redump | XML (Logiqx) | `Non-Redump - Sony - PlayStation 3 (20250908-072347).dat` | — | — | [TODO] | [TODO] | Pendiente DAT Redump |
| `psp` | Non-Redump | XML (Logiqx) | `Non-Redump - Sony - PlayStation Portable (20260421-200314).dat` | — | — | [TODO] | [TODO] | Pendiente DAT Redump |
| `psvita` | — | — | — | — | — | [TODO] | [TODO] | Sin DAT standalone identificado |
| `lynx` | No-Intro | XML (Logiqx) | `Atari - Atari Lynx (LYX) (20251222-090626).dat` | — | — | [TODO] | [TODO] | Catálogo comercial completo (127 entradas); variante LNX solo cubre 12 (mayormente Unl/Pirate), también disponible variante BLL |
| `jaguar` | No-Intro | XML (Logiqx) | `Atari - Atari Jaguar (J64) (20250208-164242).dat` | — | — | [TODO] | [TODO] | Formato del romset real del usuario. ABS/COF vacíos, JAG solo 1 entrada, ROM tiene el mismo catálogo de juegos que J64 (J64 añade 5 BIOS ya descartados) |
| `jaguarcd` | Redump | XML (Logiqx, sin cloneofid) | `Atari - Jaguar CD Interactive Multimedia System - Datfile (38) (2026-04-03 15-50-49).dat` | Non-Redump | `Non-Redump - Atari - Atari Jaguar CD (20260410-142305).dat` | [TODO] | [TODO] | Non-Redump solo cubre protos/betas |
| `pcengine` | No-Intro | XML (Logiqx) | `NEC - PC Engine - TurboGrafx-16 (20260124-120557).dat` | — | — | [TODO] | [TODO] | |
| `pcenginecd` | Redump | XML (Logiqx, sin cloneofid) | `NEC - PC Engine CD & TurboGrafx CD - Datfile (551) (2026-06-14 14-24-19).dat` | Non-Redump | `Non-Redump - NEC - PC Engine CD + TurboGrafx CD (20260413-192151).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/pcecd.xml`. Non-Redump solo cubre protos/betas |
| `3do` | Redump | XML (Logiqx, sin cloneofid) | `Panasonic - 3DO Interactive Multiplayer - Datfile (672) (2026-06-09 14-48-47).dat` | Non-Redump | `Non-Redump - Panasonic - 3DO Interactive Multiplayer (20250115-113934).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/3do.xml`. Non-Redump solo cubre protos/betas |
| `cdi` | Non-Redump | XML (Logiqx) | `Non-Redump - Philips - CD-i (20260429-044928).dat` | — | — | [TODO] | [TODO] | CHD: `metadata/software-list/cdi.xml`. Pendiente DAT Redump |
| `amigacdtv` | Redump | XML (Logiqx, sin cloneofid) | `Commodore - Amiga CDTV - Datfile (61) (2026-05-16 20-58-08).dat` | Non-Redump | `Non-Redump - Commodore - Amiga CDTV (20260409-113749).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/cdtv.xml`. Non-Redump solo cubre protos/betas |
| `amigacd32` | Redump | XML (Logiqx, sin cloneofid) | `Commodore - Amiga CD32 - Datfile (207) (2026-05-08 20-54-04).dat` | Non-Redump | `Non-Redump - Commodore - Amiga CD32 (20260428-090239).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/cd32.xml`. Non-Redump solo cubre protos/betas |
| `ngp` | No-Intro | XML (Logiqx) | `SNK - NeoGeo Pocket (20250904-215533).dat` | — | — | [TODO] | [TODO] | |
| `ngpc` | No-Intro | XML (Logiqx) | `SNK - NeoGeo Pocket Color (20240506-123728).dat` | — | — | [TODO] | [TODO] | |
| `wswan` | No-Intro | XML (Logiqx) | `Bandai - WonderSwan (20260124-123054).dat` | — | — | [TODO] | [TODO] | |
| `wswanc` | No-Intro | XML (Logiqx) | `Bandai - WonderSwan Color (20260415-165647).dat` | — | — | [TODO] | [TODO] | |
| `supervision` | No-Intro | XML (Logiqx) | `Watara - Supervision (20250625-093232).dat` | — | — | [TODO] | [TODO] | |
| `xbox` | Redump | XML (Logiqx, sin cloneofid) | `Microsoft - Xbox - Datfile (2683) (2026-06-14 23-43-27).dat` | Non-Redump | `Non-Redump - Microsoft - Xbox (20251215-001810).dat` | [TODO] | [TODO] | Non-Redump solo cubre protos/betas |
| `xbox360` | Non-Redump | XML (Logiqx) | `Non-Redump - Microsoft - Xbox 360 (20251219-035655).dat` | — | — | [TODO] | [TODO] | Pendiente DAT Redump |
| `gx4000` | TOSEC | XML (Logiqx, TOSEC) | `Amstrad GX4000 - Games (TOSEC-v2025-01-15_CM).dat` | — | — | [TODO] | [TODO] | Set predominantemente homebrew (2018-2024); catálogo comercial original de GX4000 es muy reducido |
| `neogeocd` | Redump | XML (Logiqx, sin cloneofid) | `SNK - Neo Geo CD - Datfile (111) (2026-05-06 12-21-03).dat` | — | `metadata/software-list/neocd.xml` | [TODO] | [TODO] | DAT alternativo es software list de MAME (CHD), no un DAT de romset |

## Arcade

| Identificador canónico | Fuente | Formato | DAT | Completitud | Almacenamiento | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| `mame` | MAME | XML (Logiqx) | Ver `metadata/dat/arcade/` | [TODO] | [TODO] | Versiones disponibles: 2000, 2003, 2003-plus, 2010, 2015, 2016 |
| `fbneo` | FBN | XML (Logiqx) | `FinalBurn Neo v1.0.0.03.dat` | [TODO] | [TODO] | También disponibles v1.0.0.00 y v1.0.0.02 |
| `neogeo` | libretro / FBN | ClrMamePro (texto) | `SNK - Neo Geo.dat` | [TODO] | [TODO] | AES y MVS comparten romset; usar FBN DAT para validación arcade |
| `cps1` | FBN / MAME | — | — | [TODO] | [TODO] | Subconjunto de fbneo / mame |
| `cps2` | FBN / MAME | — | — | [TODO] | [TODO] | Subconjunto de fbneo / mame |
| `cps3` | FBN / MAME | XML (Logiqx) | `Non-Redump - Capcom - Play System III (20250421-145612).dat` | [TODO] | [TODO] | También subconjunto de fbneo / mame |
| `naomi` | FBN / MAME | — | — | [TODO] | [TODO] | Subconjunto de fbneo / mame |
| `atomiswave` | FBN / libretro | ClrMamePro (texto) | `Atomiswave.dat` | [TODO] | [TODO] | DAT en subcarpeta libretro |
| `daphne` | — | — | — | — | — | Sin DAT estándar |
| `naomi2` | — | — | — | — | — | Sin DAT estándar |
| `chihiro` | — | — | — | — | — | Sin DAT estándar |
| `triforce` | — | — | — | — | — | Sin DAT estándar |

## Microcomputers

| Identificador canónico | Fuente | Formato | DAT | Completitud | Almacenamiento | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| `c64` | No-Intro | XML (Logiqx) | `Commodore - Commodore 64 (20260410-230500).dat` | [TODO] | [TODO] | |
| `c128` | — | — | — | [TODO] | [TODO] | Sin DAT específico identificado |
| `amiga` | No-Intro | XML (Logiqx) | `Commodore - Amiga (20240604-172503).dat` | [TODO] | [TODO] | |
| `spectrum` | libretro | ClrMamePro (texto) | `Sinclair - ZX Spectrum.dat` | [TODO] | [TODO] | No-Intro solo cubre +3; libretro DAT para uso general |
| `zx81` | libretro | ClrMamePro (texto) | `Sinclair - ZX 81.dat` | [TODO] | [TODO] | |
| `msx` | No-Intro | XML (Logiqx) | `Microsoft - MSX (20260202-122913).dat` | [TODO] | [TODO] | |
| `msx2` | No-Intro | XML (Logiqx) | `Microsoft - MSX2 (20260124-112728).dat` | [TODO] | [TODO] | |
| `amstradcpc` | No-Intro | XML (Logiqx) | `Amstrad - CPC (Misc) (20230406-091045).dat` | [TODO] | [TODO] | También disponible variante Flux |
| `atarist` | No-Intro | XML (Logiqx) | `Atari - Atari ST (20260222-121844).dat` | [TODO] | [TODO] | |
| `sharpx68000` | Non-Redump | XML (Logiqx) | `Non-Redump - Sharp - X68000 (20260426-004349).dat` | [TODO] | [TODO] | No-Intro solo cubre Flux |
| `dragon32` | — | — | — | [TODO] | [TODO] | Sin DAT identificado |

## Engines / Ports

| Identificador canónico | Fuente | Formato | DAT | Notas |
| --- | --- | --- | --- | --- |
| `scummvm` | libretro | ClrMamePro (texto) | `ScummVM.dat` | Sin romset convencional; archivos de juego individuales |
| `dos` | libretro | ClrMamePro (texto) | `DOS.dat` | |
| `doom` | libretro | ClrMamePro (texto) | `DOOM.dat` | |
| `quake` | libretro | ClrMamePro (texto) | `Quake.dat` | |
| `quake2` | libretro | ClrMamePro (texto) | `Quake II.dat` | |
| `cavestory` | libretro | ClrMamePro (texto) | `Cave Story.dat` | |
| `openbor` | — | — | — | Sin DAT estándar |
| `ports` | — | — | — | Sin DAT estándar |
