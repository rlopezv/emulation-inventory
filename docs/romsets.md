# Romsets

Asociación entre los sistemas de `docs/systems.md` y los DATs disponibles en `metadata/dat/`. Los identificadores canónicos usados aquí deben coincidir siempre con los definidos en `docs/systems.md`; este fichero no redefine sistemas, solo documenta sus fuentes de romset.

El nombre de DAT es relativo a la subcarpeta de su fuente (`No-Intro/`, `Non-Redump/`, `Redump/`, `TOSEC/`, `arcade/`, `libretro/`,`hyperspin/`,`custom/`, `WHDLoad/`).

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
- **XML (HyperList)** — XML propio del frontend HyperSpin, con las etiquetas `<menu><game name="...">`. No contiene hashes de verificación (no es un DAT de auditoría); vincula nombres de ROM con metadatos y elementos multimedia de la ruleta de juegos. Usado por los ficheros de `metadata/dat/hyperspin/`. Ver `docs/references.md#formatos-de-preservación-y-organización`.
- **[TODO]** — formato aún no definido para los DATs de `metadata/dat/custom/` (carpeta reservada, todavía sin contenido).

`tools/scripts/build-dat-index-nointro.ps1` procesa DAT **XML (Logiqx)** con `cloneofid` (No-Intro/Non-Redump). `tools/scripts/build-dat-index-redump.ps1` procesa DAT **XML (Logiqx, sin cloneofid)** (Redump), agrupando por nombre base. `tools/scripts/build-dat-index-tosec.ps1` procesa DAT **XML (Logiqx, TOSEC)**, agrupando por nombre base con detección de región por código de 2 letras. Los sistemas en **ClrMamePro (texto)** quedan pendientes de un tratamiento específico. Los DAT en **XML (HyperList)** y el formato pendiente de `custom/` no tienen script de indexado todavía.

## Consolas

| Identificador canónico | Fuente | Formato | DAT | Fuente alternativa | DAT alternativo | Completitud | Almacenamiento | Notas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `gameandwatch` | libretro | ClrMamePro (texto) | `Handheld Electronic Game.dat` | — | — | [TODO] | [TODO] | Cubre "Handheld Electronic Game" en general (Nintendo, Mattel, VTech, Tiger...), no solo Nintendo Game & Watch; fuera del alcance de build-dat-index-nointro.ps1 por formato |
| `atari2600` | No-Intro | XML (Logiqx) | `Atari - Atari 2600 (*).dat` | — | — | [TODO] | [TODO] | |
| `atari5200` | No-Intro | XML (Logiqx) | `Atari - Atari 5200 (*).dat` | — | — | [TODO] | [TODO] | Requiere BIOS `5200.rom` |
| `atari7800` | No-Intro | XML (Logiqx) | `Atari - Atari 7800 (BIN) (*).dat` | — | — | [TODO] | [TODO] | BIN = headerless; también disponible variante A78 (headered, 128 bytes) — ver `docs/references.md#caso-especial--headered-vs-headerless-nes-snes-atari-7800-atari-lynx-fds` |
| `astrocade` | No-Intro | XML (Logiqx) | `Bally - Astrocade (*).dat` | — | — | [TODO] | [TODO] | |
| `vectrex` | No-Intro | XML (Logiqx) | `GCE - Vectrex (*).dat` | — | — | [TODO] | [TODO] | |
| `coleco` | No-Intro | XML (Logiqx) | `Coleco - ColecoVision (*).dat` | TOSEC | `Coleco - ColecoVision (*).dat` | [TODO] | [TODO] | |
| `arcadia2001` | No-Intro | XML (Logiqx) | `Emerson - Arcadia 2001 (*).dat` | TOSEC | `Emerson Arcadia 2001 (*).dat` | [TODO] | [TODO] | Sin BIOS (cartucho puro, confirmado en MAME: "BIOS Requirement: Not required") |
| `odyssey2` | No-Intro | XML (Logiqx) | `Magnavox - Odyssey 2 (*).dat` | — | — | [TODO] | [TODO] | |
| `intellivision` | No-Intro | XML (Logiqx) | `Mattel - Intellivision (*).dat` | — | — | [TODO] | [TODO] | Requiere BIOS `grom.bin`, `exec.bin` |
| `channelf` | No-Intro | XML (Logiqx) | `Fairchild - Channel F (*).dat` | — | — | [TODO] | [TODO] | 37 juegos, catálogo limpio `.bin`. Requiere BIOS `sl31253.bin`+`sl31254.bin` (o pack combinado `channelf.zip`) — ver `docs/bios.md` |
| `megaduck` | No-Intro | XML (Logiqx) | `Welback - Mega Duck (*).dat` | — | — | [TODO] | [TODO] | 25 juegos, catálogo limpio `.bin`. Sin BIOS requerida. Si un juego se queda en pantalla negra, cambiar la extensión a `.md1`/`.md2` según el tamaño del cartucho suele resolver el mapeo de memoria en el core `sameduck` |
| `nes` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo Entertainment System (Headered) (*).dat` | — | — | [TODO] | [TODO] | Headered (iNES, 16 bytes); también disponible versión Headerless — ver `docs/references.md#caso-especial--headered-vs-headerless-nes-snes-atari-7800-atari-lynx-fds`. Motivo: sin cabecera, el Mapper del cartucho solo puede inferirse por base de datos de hashes (fiable para el catálogo oficial licenciado, no siempre para cartuchos homebrew/pirata/no oficiales con mappers no estándar); la cabecera lo garantiza en todos los casos. Comparado el DAT real: Headered tiene 4502 entradas, Headerless 4506 (4 más: 3 multicarts pirata + BIOS Game Genie) — la diferencia de cobertura no es la causa |
| `fds` | No-Intro | XML (Logiqx) | `Nintendo - Family Computer Disk System (FDS) (*).dat` | — | — | [TODO] | [TODO] | FDS = formato de imagen de disco raw estándar; también disponible variante QD (QuickDisk, distinto del caso headered/headerless — ver `metadata/dat/No-Intro/`) |
| `satellaview` | No-Intro | XML (Logiqx) | `Nintendo - Satellaview (*).dat` | — | — | [TODO] | [TODO] | |
| `sufami` | No-Intro | XML (Logiqx) | `Nintendo - Sufami Turbo (*).dat` | — | — | [TODO] | [TODO] | |
| `sgb` | — | — | — | — | — | [TODO] | [TODO] | Sin DAT específico; usa ROMs de `gb`/`gbc` ejecutadas en modo Super Game Boy |
| `snes` | No-Intro | XML (Logiqx) | `Nintendo - Super Nintendo Entertainment System (*).dat` | — | — | [TODO] | [TODO] | Sin etiqueta en el nombre = headerless (`.sfc`); No-Intro no publica variante Headered/SMC por separado en el catálogo actual — ver `docs/references.md#caso-especial--headered-vs-headerless-nes-snes-atari-7800-atari-lynx-fds` |
| `gb` | No-Intro | XML (Logiqx) | `Nintendo - Game Boy (*).dat` | — | — | [TODO] | [TODO] | |
| `gbc` | No-Intro | XML (Logiqx) | `Nintendo - Game Boy Color (*).dat` | — | — | [TODO] | [TODO] | |
| `gba` | No-Intro | XML (Logiqx) | `Nintendo - Game Boy Advance (*).dat` | — | — | [TODO] | [TODO] | |
| `virtualboy` | No-Intro | XML (Logiqx) | `Nintendo - Virtual Boy (*).dat` | — | — | [TODO] | [TODO] | |
| `n64` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo 64 (BigEndian) (*).dat` | — | — | [TODO] | [TODO] | BigEndian (`.z64`, formato nativo del cartucho); también disponible ByteSwapped (`.v64`) — ver `docs/references.md#caso-especial--nintendo-64-orden-de-bytes-byte-order` |
| `64dd` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo 64DD (*).dat` | — | — | [TODO] | [TODO] | |
| `pokemini` | No-Intro | XML (Logiqx) | `Nintendo - Pokemon Mini (*).dat` | — | — | [TODO] | [TODO] | |
| `nds` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo DS (Decrypted) (*).dat` | — | — | [TODO] | [TODO] | También disponible Encrypted |
| `ndsi` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo DSi (*).dat` | — | — | [TODO] | [TODO] | Cartuchos físicos DSi-enhanced/exclusivos, DAT separado de `nds` (cabecera extendida, Modcrypt) y de `dsiware` (digital) |
| `dsiware` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo DSi (Digital) (CDN) (Decrypted) (*).dat` | — | — | [TODO] | [TODO] | Decrypted es la variante elegida (formato definitivo); también disponible Encrypted. El DAT anterior sin dividir (`Nintendo - Nintendo DSi (Digital) (*).dat`, 2022) está desactualizado |
| `3ds` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo 3DS (Decrypted) (*).dat` | — | — | [TODO] | [TODO] | Cartuchos físicos. También disponible variante Encrypted |
| `3dseshop` | No-Intro | XML (Logiqx) | `Nintendo - Nintendo 3DS (Digital) (CDN) (*).dat` | — | — | [TODO] | [TODO] | Exclusivos de eShop. Virtual Console 3DS pendiente: DAT no descargado en metadata/dat/ |
| `newn3ds` | No-Intro | XML (Logiqx) | `Nintendo - New Nintendo 3DS (Decrypted) (*).dat` | — | — | [TODO] | [TODO] | Catálogo físico exclusivo de New Nintendo 3DS; también disponible variante Encrypted |
| `gamecube` | Redump | XML (Logiqx, sin cloneofid) | `Nintendo - GameCube - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Nintendo - Nintendo GameCube (*).dat` | [TODO] | [TODO] | Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Nintendo - GameCube (*).dat` |
| `wii` | Redump | XML (Logiqx, sin cloneofid) | `Nintendo - Wii - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Nintendo - Wii (*).dat` | [TODO] | [TODO] | Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Nintendo - Wii (*).dat` |
| `wiiu` | Non-Redump | XML (Logiqx) | `Non-Redump - Nintendo - Wii U (*).dat` | — | — | [TODO] | [TODO] | Pendiente DAT Redump |
| `switch` | — | — | — | — | — | — | [TODO] | Sin DAT de verificación estándar |
| `sg1000` | No-Intro | XML (Logiqx) | `Sega - SG-1000 - SC-3000 (*).dat` | — | — | [TODO] | [TODO] | Incluye SC-3000 |
| `mastersystem` | No-Intro | XML (Logiqx) | `Sega - Master System - Mark III (*).dat` | — | — | [TODO] | [TODO] | |
| `megadrive` | No-Intro | XML (Logiqx) | `Sega - Mega Drive - Genesis (*).dat` | — | — | [TODO] | [TODO] | |
| `sega32x` | No-Intro | XML (Logiqx) | `Sega - 32X (*).dat` | — | — | [TODO] | [TODO] | |
| `gamegear` | No-Intro | XML (Logiqx) | `Sega - Game Gear (*).dat` | — | — | [TODO] | [TODO] | |
| `segacd` | Redump | XML (Logiqx, sin cloneofid) | `Sega - Mega CD & Sega CD - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Sega - Sega Mega CD + Sega CD (*).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/megacd.xml`. Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Sega - Mega CD & Sega CD (*).dat` |
| `saturn` | Redump | XML (Logiqx, sin cloneofid) | `Sega - Saturn - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Sega - Sega Saturn (*).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/saturn.xml`. Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Sega - Saturn (*).dat` |
| `dreamcast` | Redump | XML (Logiqx, sin cloneofid) | `Sega - Dreamcast - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Sega - Dreamcast (*).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/dc.xml`. Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Sega - Dreamcast (*).dat` |
| `psx` | Redump | XML (Logiqx, sin cloneofid) | `Sony - PlayStation - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Sony - PlayStation (*).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/psx.xml`. Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Sony - PlayStation (*).dat` |
| `ps2` | Redump | XML (Logiqx, sin cloneofid) | `Sony - PlayStation 2 - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Sony - PlayStation 2 (*).dat` | [TODO] | [TODO] | Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Sony - PlayStation 2 (*).dat` |
| `ps3` | Non-Redump | XML (Logiqx) | `Non-Redump - Sony - PlayStation 3 (*).dat` | — | — | [TODO] | [TODO] | Pendiente DAT Redump |
| `psp` | Redump | XML (Logiqx) | `Sony - PlayStation Portable - Datfile (*) (*).dat` | — | — | [TODO] | [TODO] | Corregido el prefijo (era `Redump - Sony - ...`, no coincide con el nombre real descargado). Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Sony - PlayStation Portable (*).dat` |
| `pspminis` | No-Intro | XML (Logiqx) | `Sony - PlayStation Portable (PSN) (Minis) (Decrypted) (*).dat` | — | — | [TODO] | [TODO] | Contenido digital PSN, subconjunto independiente del catálogo retail de `psp` |
| `psn` | No-Intro | XML (Logiqx) | `Sony - PlayStation Portable (PSN) (Decrypted) (*).dat` | — | — | [TODO] | [TODO] | Catálogo digital PSN completo de PSP (distinto de `psp` físico UMD y de `pspminis`) |
| `psvita` | — | — | — | — | — | [TODO] | [TODO] | Sin DAT standalone identificado |
| `lynx` | No-Intro | XML (Logiqx) | `Atari - Atari Lynx (LYX) (*).dat` | — | — | [TODO] | [TODO] | LYX = headerless, catálogo comercial completo (127 entradas); LNX = headered (64 bytes), solo cubre 12 (mayormente Unl/Pirate) — ver `docs/references.md#caso-especial--headered-vs-headerless-nes-snes-atari-7800-atari-lynx-fds`; también disponible variante BLL (no cubierta ahí) |
| `jaguar` | No-Intro | XML (Logiqx) | `Atari - Atari Jaguar (J64) (*).dat` | — | — | [TODO] | [TODO] | Formato del romset real del usuario. ABS/COF vacíos, JAG solo 1 entrada, ROM tiene el mismo catálogo de juegos que J64 (J64 añade 5 BIOS ya descartados) |
| `jaguarcd` | Redump | XML (Logiqx, sin cloneofid) | `Atari - Jaguar CD Interactive Multimedia System - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Atari - Atari Jaguar CD (*).dat` | [TODO] | [TODO] | Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Atari - Jaguar CD Interactive Multimedia System (*).dat` |
| `pcengine` | No-Intro | XML (Logiqx) | `NEC - PC Engine - TurboGrafx-16 (*).dat` | — | — | [TODO] | [TODO] | |
| `pcenginecd` | Redump | XML (Logiqx, sin cloneofid) | `NEC - PC Engine CD & TurboGrafx CD - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - NEC - PC Engine CD + TurboGrafx CD (*).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/pcecd.xml`. Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/NEC - PC Engine CD & TurboGrafx CD (*).dat` |
| `3do` | Redump | XML (Logiqx, sin cloneofid) | `Panasonic - 3DO Interactive Multiplayer - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Panasonic - 3DO Interactive Multiplayer (*).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/3do.xml`. Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Panasonic - 3DO Interactive Multiplayer (*).dat` |
| `cdi` | Non-Redump | XML (Logiqx) | `Non-Redump - Philips - CD-i (*).dat` | — | — | [TODO] | [TODO] | CHD: `metadata/software-list/cdi.xml`. Pendiente DAT Redump |
| `amigacdtv` | Redump | XML (Logiqx, sin cloneofid) | `Commodore - Amiga CDTV - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Commodore - Amiga CDTV (*).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/cdtv.xml`. Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Commodore - Amiga CDTV (*).dat` |
| `amigacd32` | Redump | XML (Logiqx, sin cloneofid) | `Commodore - Amiga CD32 - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Commodore - Amiga CD32 (*).dat` | [TODO] | [TODO] | CHD: `metadata/software-list/cd32.xml`. Non-Redump solo cubre protos/betas. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/Commodore - Amiga CD32 (*).dat` |
| `ngp` | No-Intro | XML (Logiqx) | `SNK - NeoGeo Pocket (*).dat` | — | — | [TODO] | [TODO] | |
| `ngpc` | No-Intro | XML (Logiqx) | `SNK - NeoGeo Pocket Color (*).dat` | — | — | [TODO] | [TODO] | |
| `wswan` | No-Intro | XML (Logiqx) | `Bandai - WonderSwan (*).dat` | — | — | [TODO] | [TODO] | |
| `wswanc` | No-Intro | XML (Logiqx) | `Bandai - WonderSwan Color (*).dat` | — | — | [TODO] | [TODO] | |
| `supervision` | No-Intro | XML (Logiqx) | `Watara - Supervision (*).dat` | — | — | [TODO] | [TODO] | |
| `xbox` | Redump | XML (Logiqx, sin cloneofid) | `Microsoft - Xbox - Datfile (*) (*).dat` | Non-Redump | `Non-Redump - Microsoft - Xbox (*).dat` | [TODO] | [TODO] | Non-Redump solo cubre protos/betas |
| `xbox360` | Non-Redump | XML (Logiqx) | `Non-Redump - Microsoft - Xbox 360 (*).dat` | — | — | [TODO] | [TODO] | Pendiente DAT Redump |
| `gx4000` | — | — | — | — | — | [TODO] | [TODO] | Es un caso excepcional que requiere tratamiento manual |
| `neogeocd` | Redump | XML (Logiqx, sin cloneofid) | `SNK - Neo Geo CD - Datfile (*) (*).dat` | — | `metadata/software-list/neocd.xml` | [TODO] | [TODO] | DAT alternativo es software list de MAME (CHD), no un DAT de romset. Contraste de hash SHA1 disponible vía MAMERedump: `metadata/dat/MAMERedump/full/SNK - Neo Geo CD (*).dat` |

## Arcade

Caso especial dentro de este fichero: a diferencia de Consolas/Microcomputers, un mismo sistema arcade suele tener **varios romsets utilizables en paralelo** (una versión de MAME/FBNeo por cada core/emulador objetivo, no una sola fuente "actual"). La tabla principal fija la fuente/DAT recomendado por sistema; el desglose completo de versiones vive en la tabla `Versiones de romset` de más abajo.

| Identificador canónico | Fuente | Formato | DAT | Completitud | Almacenamiento | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| `mame` | MAME | XML (Logiqx) | Ver tabla `Versiones de romset` | [TODO] | [TODO] | Sin versión "actual" única — el romset a usar depende del core/emulador objetivo |
| `fbneo` | FBN | XML (Logiqx) | `FinalBurn Neo v1.0.0.03.dat` (recomendada) | [TODO] | [TODO] | Resto de versiones (v1.0.0.00, v1.0.0.02) y variantes legacy (PiFBA, fbalpha2012) en tabla `Versiones de romset` |
| `neogeo` | libretro | ClrMamePro (texto) | `SNK - Neo Geo.dat` | [TODO] | [TODO] | AES y MVS comparten romset. DAT propio, no subconjunto de `mame`/`fbneo` — variantes filtradas por FBN/GnGeo en tabla `Versiones de romset` |
| `cps1` | FBN / MAME | — | — | [TODO] | [TODO] | Sin DAT propio — subconjunto filtrado por driver `cps1.cpp` del romset completo `mame`/`fbneo` |
| `cps2` | FBN / MAME | — | — | [TODO] | [TODO] | Sin DAT propio — subconjunto filtrado por driver `cps2.cpp` del romset completo `mame`/`fbneo` |
| `cps3` | Non-Redump | XML (Logiqx) | `Non-Redump - Capcom - Play System III (*).dat` | [TODO] | [TODO] | DAT propio (cartuchos CPS-3 volcables individualmente, a diferencia de CPS-1/CPS-2) |
| `naomi` | MAME + MAMERedump | XML (Logiqx) | Subconjunto `mame` (cartucho) + `Arcade - Sega - Naomi (34).dat` (verificación CHD/SHA1) | [TODO] | [TODO] | Core/emulador recomendado: flycast. Discos (GD-ROM→CHD) vía MAMERedump, cartuchos vía driver `naomi.cpp` de `mame` |
| `atomiswave` | libretro | ClrMamePro (texto) | `Atomiswave.dat` | [TODO] | [TODO] | DAT propio, no subconjunto de `mame`/`fbneo`. Core/emulador recomendado: flycast |
| `naomi2` | MAME (≥0.260) + MAMERedump | XML (Logiqx) | Subconjunto `mame` + `Arcade - Sega - Naomi 2 (13).dat` (verificación CHD/SHA1) | [TODO] | [TODO] | Igual que `naomi`, requiere MAME 0.260 o superior. Core/emulador recomendado: flycast |
| `daphne` | — | — | — | — | — | Caso excepcional que requiere tratamiento manual: framefiles + vídeo (`.m2v`/`.ogg`/`.txt` de sincronización), sin ROMs verificables por hash estándar |

### Versiones de romset — `mame` / `fbneo` / `neogeo`

Desglose de versiones utilizables por sistema. Un mismo core/emulador de `docs/arcade/arcade.md` exige exactamente una versión de romset; usar la que no corresponde produce roms no reconocidas o pantalla negra.

| Identificador canónico | Core/emulador (`arcade.md`) | Versión romset | Ubicación local del DAT | Notas |
| --- | --- | --- | --- | --- |
| `mame` | `mame2000` | MAME 0.37b5 | `metadata/dat/arcade/mame2000/MAME 0.37b5 XML.dat` | Alt.: `retropie-dat-master/mame4all/`, `.../lr-imame4all/` (mismo core, nombre histórico `imame4all`) |
| `mame` | `mame2003` | MAME 0.78 | `metadata/dat/arcade/mame2003/mame2003.xml` | Alt.: `retropie-dat-master/lr-mame2003/` (incluye variantes `lite`/`no-clones-no-neogeo`) |
| `mame` | `mame2003-plus` | MAME 0.78 + backports | `metadata/dat/arcade/mame2003-plus/mame2003-plus.xml` | Alt.: `retropie-dat-master/lr-mame2003-plus/` |
| `mame` | `mame2010` | MAME 0.139u1 | `metadata/dat/arcade/mame2010/mame2010.xml` | Alt.: `retropie-dat-master/lr-mame2010/` |
| `mame` | `mame2015` | MAME 0.160 | `metadata/dat/arcade/mame2015/mame2014.xml` | Nombre de fichero real no coincide con la versión (`mame2014.xml`). Alt.: `retropie-dat-master/lr-mame2015/` (zip) |
| `mame` | `mame2016` | MAME 0.174 | `metadata/dat/arcade/mame2016/MAME 0.174 Arcade XML.dat` | Alt.: `retropie-dat-master/lr-mame2016/` (zip, incluye variante "Home") |
| `mame` | `AdvanceMame` (1.2 a 5.0) | MAME 0.106 | `retropie-dat-master/advmame1.2/` | — |
| `mame` | `AdvanceMame 0.94` | MAME 0.94 | `retropie-dat-master/advmame.94/` | — |
| `fbneo` | `fbneo` | v1.0.0.00 | `metadata/dat/arcade/FinalBurn Neo v1.0.0.00.dat` | — |
| `fbneo` | `fbneo` | v1.0.0.02 | `metadata/dat/arcade/FinalBurn Neo v1.0.0.02.dat` | — |
| `fbneo` | `fbneo` (recomendada) | v1.0.0.03 | `metadata/dat/arcade/FinalBurn Neo v1.0.0.03.dat` | Incluye `.csv` adicional. Alt.: `retropie-dat-master/lr-fbneo/...(Arcade only).dat` |
| `fbneo` | `PiFBA` | FBA2X 7.3 | `retropie-dat-master/pifba/` | Legacy, predecesor de `fbalpha2012` |
| `fbneo` | `fbalpha2012` | FBA 0.2.97.29/30 | `retropie-dat-master/lr-fbalpha2012/` | Legacy |
| `neogeo` | `fbneo` (Neogeo only) | v1.0.0.03 | `retropie-dat-master/lr-fbneo/...(Neogeo only).dat` | Subconjunto ya filtrado por el propio fichero |
| `neogeo` | `fbalpha2012_neogeo` | FBA 0.2.97.29 | `retropie-dat-master/lr-fbalpha2012/fba-lr-neogeo-only.xml` | Legacy |
| `neogeo` | `GnGeo_2020-02-16` | MAME 0.128 / FBA 0.2.97.39 | — | Sin DAT local descargado |
| `neogeo` | `GnGeo 0.8.4 (Pandora)` | GnGeo 0.8.4 | `retropie-dat-master/gngeopi/` | Histórico |

## Microcomputers

| Identificador canónico | Fuente | Formato | DAT | Fuente alternativa | DAT alternativo | Completitud | Almacenamiento | Notas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `c64` | No-Intro | XML (Logiqx) | `Commodore - Commodore 64 (*).dat` | TOSEC | `Commodore C64 - Games - [D64] (TOSEC-v*).dat` (12 sub-DAT por género, fusionar con `SabreTools --merge` antes de auditar — ver `docs/guides/tools/dat-conversion.md`) | [TODO] | [TODO] | Elegido No-Intro/CRT como fuente primaria por usabilidad real en el dispositivo objetivo: cartucho `.crt` con autostart instantáneo, sin teclado virtual ni mapeo de disquetera, catálogo oficial limpio (ideal para 1G1R). TOSEC/D64 queda como fuente alternativa para el catálogo histórico masivo en disquete, que incluye volcados crackeados que No-Intro excluye por diseño |
| `c128` | TOSEC | XML (Logiqx, TOSEC) | `Commodore C128 - Games - [D64] (TOSEC-v*).dat` | — | — | [TODO] | [TODO] | Resuelto — sí tiene cobertura TOSEC, sin dividir por género a diferencia de `c64` |
| `plus4` | TOSEC | XML (Logiqx, TOSEC) | `Commodore C16, C116 & Plus-4 - Games - [PRG] (TOSEC-v*).dat` | [TODO] | [TODO] | [TODO] | [TODO] | Sistema dado de alta esta sesión (antes solo aparecía como core `vice_xplus4` sin fila propia). No verificado si No-Intro tiene cobertura de cartucho para esta familia — pendiente de la misma revisión formato-disponible × emulador-soporta que el resto de microcomputers (ver `docs/guides/romsets/microcomputers.md`) |
| `amiga` | WHDLoad (Retroplay) | ClrMamePro (texto) | `Commodore - Amiga - WHDLoad.dat` | TOSEC | `Commodore Amiga - Games - [ADF] (TOSEC-v*).dat` | [TODO] | [TODO] | Elegido WHDLoad como fuente primaria por usabilidad: cada juego es un `.lha` único con carga instantánea (sin pantallas de disquetera, sin cambio de disco entre volúmenes), catalogado con checksums CRC32/MD5/SHA1 por `github.com/MrV2K/WHDLoad-Database` (basado en los DAT oficiales de Retroplay, ver `docs/references.md`). No-Intro descartado como fuente: su único DAT de Amiga es 100% `.IPF`/`.ROM` (5760+37 entradas), no `.ADF`, y requiere la librería externa CAPSimg sin aportar ventaja de usabilidad. TOSEC/`.ADF` queda como fuente alternativa para quien prefiera el disquete original (sub-DAT adicionales sin fusionar por defecto: Public Domain, SPS, Save Disks, Unofficial Addons & Patches); libretro (`Commodore - Amiga.dat`) queda como alternativa secundaria de `.ADF` |
| `spectrum` | TOSEC | XML (Logiqx, TOSEC) | `Sinclair ZX Spectrum - Games - [TAP] (TOSEC-v*).dat` | libretro | `Sinclair - ZX Spectrum.dat` | [TODO] | [TODO] | Cambiado de libretro a TOSEC como fuente principal, mismo motivo que el resto de microcomputers (cracks/preservación); libretro queda como alternativa. Formato principal `.TAP` (no `.TZX`): soporta Fast Loading en el core `lr-fuse` (estándar en portátiles chinas), precarga en RAM en segundos frente a los minutos de carga real de `.TZX` — muchos cores en portátiles fallan al aplicar Fast Loading sobre `.TZX`. `.TZX` sigue disponible como DAT TOSEC (preservación perfecta: esquemas anticopia, cargas turbo) pero se recomienda evitarlo salvo necesidad específica. Otros formatos alternativos TOSEC disponibles: `[SNA]`, `[Z80]`, `[DSK]`, `[SZX]`, entre otros |
| `zx81` | TOSEC | XML (Logiqx, TOSEC) | `Sinclair ZX81 - Games - [P] (TOSEC-v*).dat` | libretro | `Sinclair - ZX 81.dat` | [TODO] | [TODO] | Cambiado de libretro a TOSEC como fuente principal, mismo motivo; libretro queda como alternativa. `.P` es el formato nativo de programa ZX81, con autostart instantáneo en el core `lr-eightyone`; también disponibles `[TZX]` (desaconsejado en portátiles — emulación de cinta tosca, obliga a teclado virtual y `LOAD ""` tokenizado), `[Z81]` (snapshot nativo de EightyOne, no medio real, no es alternativa de romset) y `[Multipart]` (empaquetado de varios `.P`, no un formato distinto) |
| `msx` | No-Intro | XML (Logiqx) | `Microsoft - MSX (*).dat` | TOSEC | `MSX MSX - Games - [DSK] (TOSEC-v*).dat` | [TODO] | [TODO] | Elegido No-Intro/`.ROM` como fuente primaria: cartucho con autostart instantáneo (catálogo Konami: Nemesis, Penguin Adventure...), catálogo limpio ideal para 1G1R. TOSEC/`.DSK` como fuente alternativa, imprescindible para el catálogo avanzado en disco (RPGs/aventuras japonesas y de la escena NL/ES, exclusivos de disquete). Descartar `.CAS` (cinta, emulación inestable) y `.MX1`/`.MX2` (extensiones obsoletas de emuladores DOS de los 90) |
| `msx2` | No-Intro | XML (Logiqx) | `Microsoft - MSX2 (*).dat` | TOSEC | `MSX MSX2 - Games - [DSK] (TOSEC-v*).dat` | [TODO] | [TODO] | Mismo criterio que `msx`; `.DSK` especialmente crítico en MSX2/MSX2+, donde recae la mayoría del catálogo avanzado |
| `amstradcpc` | TOSEC | XML (Logiqx, TOSEC) | `Amstrad CPC - Games - [DSK] (TOSEC-v*).dat` | libretro | `Amstrad - CPC.dat` | [TODO] | [TODO] | Se mantiene TOSEC como fuente principal (no hay swap a No-Intro como en `c64`/`msx`/`msx2`: No-Intro solo publica `Amstrad - CPC (Flux)` — volcados de flujo magnético HxC/RAW, preservación técnica no reproducible directamente — y un `(Misc)` residual de 1 entrada). `.DSK` con autostart nativo en `lr-caprice32`, dominante absoluto en portátiles; `.CDT` (cinta) desaconsejado — Fast Loading poco fiable en los cores de portátiles, a diferencia de Spectrum. `.CPR` (cartucho) solo aplica a GX4000/CPC Plus, no a CPC 6128 estándar |
| `atarist` | TOSEC | XML (Logiqx, TOSEC) | `Atari ST - Games - [ST] (TOSEC-v*).dat` | — | — | [TODO] | [TODO] | Se mantiene TOSEC como fuente principal, sin swap a No-Intro: el DAT No-Intro local (`Atari - Atari ST (*).dat`) es 100% `.IPF` (546 entradas), formato de preservación de protecciones que requiere la librería externa CAPSimg y no aporta ventaja de usabilidad frente a `.ST`; el catálogo de cartucho de Atari ST fue residual. `.ST` es volcado directo de disquete con autostart nativo en Hatari; TOSEC es la única fuente que cataloga tanto los originales de tienda como los discos-menú históricos de la demoscene/piratería (The Automation, Medway Boys, D-Bug). `.MSA` es equivalente a `.ST` pero sin DAT TOSEC propio (no existe `Games - [MSA]`). Se descartan `.STX`/`.IPF` pese a tener DAT TOSEC: requieren la librería externa CAPSimg y son notablemente más pesados de emular (audio entrecortado, ralentización) |
| `sharpx68000` | TOSEC | XML (Logiqx, TOSEC) | `Sharp X68000 - Games - [DIM] (TOSEC-v*).dat` | Non-Redump | `Non-Redump - Sharp - X68000 (*).dat` | [TODO] | [TODO] | Cambiado de Non-Redump a TOSEC `[DIM]` para que la fuente coincida con el formato de ROM recomendado (`.DIM`, ver `docs/guides/romsets/microcomputers.md`); Non-Redump queda como alternativa. No-Intro solo cubre la variante Flux, descartado (mismo motivo que `amiga`/`atarist`). `[HFE]`/`[RAW]`/`[SCP]` confirmados **no usables**: ningún emulador recomendado (px68k, XM6 TypeG) los soporta. `.HDF` (disco duro virtual, formato de mayor usabilidad para juegos multi-disco, soportado por px68k) **sin DAT TOSEC disponible** — pendiente localizar una fuente equivalente al caso `amiga`/WHDLoad si se quiere cubrir con verificación |
| `dragon32` | TOSEC | XML (Logiqx, TOSEC) | `Dragon Data Dragon - Games - [CAS] (TOSEC-v*).dat` | — | — | [TODO] | [TODO] | Única fuente posible: No-Intro no tiene cobertura de Dragon Data. `.CAS` es el formato más masivo (564 entradas) con autostart nativo en XRoar; `.VDK` (disquete) alternativa para catálogo avanzado de Dragon 64, también nativo. `.PAK` (cartucho) con **riesgo real**: muchos volcados están pensados para el TRS-80 CoCo (plataforma hermana, no intercambiable) y pueden provocar error de dirección de memoria si se mezclan; `.BIN` suelto tampoco recomendable, sin la cabecera que indica al emulador dónde inyectar el código en RAM |
| `vic20` | TOSEC | XML (Logiqx, TOSEC) | `Commodore VIC20 - Games - [PRG] - Singlepart (TOSEC-v*).dat` | TOSEC | `Commodore VIC20 - Games - [TAP] (TOSEC-v*).dat` | [TODO] | [TODO] | No-Intro tiene DAT (293 entradas) pero nombra los cartuchos por dirección de memoria de mapeo (`.a0`/`.60`/`.70`/`.b0`...), no listo para usar sin conversión — descartado como primaria (mismo criterio que `amiga`/`atarist`: formato "limpio" pero poco práctico). `.PRG` elegido por catálogo (1652 entradas, el mayor de TOSEC) y autostart en `lr-vice`, mismo core que `c64`/`c128`. `.TAP` alternativa (849 entradas) |
| `atari800` | TOSEC | XML (Logiqx, TOSEC) | `Atari 8bit - Games - [XEX] (TOSEC-v*).dat` | TOSEC | `Atari 8bit - Games - [ATR] (TOSEC-v*).dat` | [TODO] | [TODO] | No-Intro solo tiene 39 entradas (set mínimo, mayoría `.bin` cartucho), insuficiente como fuente principal — descartado. `.XEX` (ejecutable directo, 3072 entradas) elegido por carga instantánea; `.ATR` (imagen de disquete, 5822 entradas, catálogo completo) como alternativa. Evitar `.CAS` (cinta, carga lenta) |
| `thomson` | TOSEC | XML (Logiqx, TOSEC) | `Thomson MO5 - Games - [K7] (TOSEC-v*).dat` | TOSEC | `Thomson TO8, TO8D, TO9, TO9+ - Games - [FD] (TOSEC-v*).dat` | [TODO] | [TODO] | Sin DAT No-Intro para esta familia. TOSEC divide el catálogo por modelo concreto (MO5/MO6/TO7/TO8-TO8D-TO9-TO9+), unificados aquí bajo un único id porque el core `theodore` cubre toda la familia. `.K7` (cinta, MO5, 656 entradas) elegido por ser el catálogo mayor; `.FD`/`.SAP` (disco, familia TO8, 171/114 entradas) como alternativa para el catálogo más avanzado |

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
