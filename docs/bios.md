# BIOS

Catálogo de ficheros BIOS/firmware requeridos por sistema para que el emulador/core arranque. No redefine sistemas (`docs/systems.md`, `docs/arcade/arcade.md`) ni la ruta de destino de la carpeta `bios/` por CFW (`docs/system-paths.md#bios`) — solo documenta qué ficheros hacen falta, si son obligatorios y qué emulador/core los requiere.

**No se enlaza a fuentes de descarga.** La BIOS es firmware con copyright: cada usuario debe volcarla de su propio hardware o adquirirla legalmente. Los nombres de fichero son sensibles a mayúsculas/minúsculas en varios cores — se transcriben tal cual los espera el emulador, sin normalizar.

## Consolas

| Identificador canónico | Fichero(s) BIOS | Obligatoria/Opcional | Emulador/core que la requiere | Notas |
| --- | --- | --- | --- | --- |
| `psx` | `scph5501.bin` (USA), `scph5502.bin` (Europa), `scph5500.bin` (Japón) | Obligatoria | `lr-duckstation` / `lr-swanstation` | Estándar de la scene moderna: BIOS PSone (modelo tardío), libre de región, compatible con el 100% de los CHD. `scph5502.bin` crítica si el 1G1R prioriza región PAL |
| `segacd` | `bios_CD_U.bin` (USA), `bios_CD_E.bin` (Europa), `bios_CD_J.bin` (Japón) | Obligatoria | `lr-genesis-plus-gx` | El core selecciona la BIOS según la región del `.CHD` a arrancar; mantener las tres |
| `saturn` | `sega_101.bin` (Japón), `mpr-17933.bin` (USA/Europa) | Obligatoria | `lr-beetle-saturn` / `lr-yabasanshiro` | `sega_101.bin` necesaria para el catálogo masivo de lucha japonés |
| `dreamcast` | `dc_boot.bin`, `dc_flash.bin` | Obligatoria | `lr-flycast` | **Ruta especial:** subcarpeta `bios/dc/` (no sueltos en `bios/`). `dc_flash.bin` es la memoria flash de la consola (hora/idioma) |
| `3do` | `fz10.bin` | Obligatoria | `lr-opera` | Modelo Panasonic FZ-10, considerada la más estable y libre de región |
| `neogeocd` | `neocd_f.bin` | Obligatoria/recomendada | `lr-neocd` | BIOS de carga rápida — esencial para saltar las pantallas de carga originales del CD |
| `pcenginecd` | System Card (nombre común en la escena `syscard3.pce`, **nombre exacto no verificado en fuente oficial**) | Obligatoria | `lr-mednafen_pce`/`lr-beetle_pce_fast` | Documentación oficial de Mednafen confirma el requisito (opción `pce.cdbios`) solo para el modo CD; no aplica a `pcengine` HuCard/cartucho |
| `nds` | `bios7.bin` (ARM7, 16 KB), `bios9.bin` (ARM9, 4 KB), `firmware.bin` (128/256/512 KB según modelo origen) | Obligatoria | `lr-melonds` | melonDS no tiene HLE de BIOS: exige volcados reales de una DS/DS Lite física. El `firmware.bin` no es sintetizable por el emulador; uno volcado de una DSi/3DS solo sirve para arranque directo de juego, no para el menú de firmware (no es "bootable") |
| `dsiware` | Todo lo de `nds` + `bios7i.bin`, `bios9i.bin` (64 KB c/u), firmware DSi (128 KB), `nand.bin` (dump de NAND, ~240 MB) | Obligatoria | `lr-melonds` (modo DSi) | **Requisito muy alto, poco viable sin hardware DSi real**: el NAND solo se obtiene volcando una DSi física (`fwTool`/`dsbf_dump.nds`), no existe generación sintética. Documentar como bloqueante hasta que el usuario confirme que dispone de una DSi para el volcado |
| `ndsi` | Mismos ficheros que `dsiware` (`bios7i.bin`, `bios9i.bin`, firmware DSi, `nand.bin`) | Obligatoria | `lr-melonds` (modo DSi) | Cartuchos físicos DSi-enhanced/exclusivos, mismo requisito de NAND que `dsiware` — ver esa fila |
| `pspminis` / `psn` | — | No requiere | `PPSSPP`/`lr-ppsspp` | PPSSPP reimplementa el kernel PSP por HLE completo (`flash0:/kd/*.prx` en C++); no necesita ni acepta un dump de firmware real |
| `3ds` / `3dseshop` / `newn3ds` | `boot9.bin`, `boot11.bin` (boot ROM ARM9/11), `aes_keys.txt` (claves AES volcadas de una 3DS real), `movable.sed` | Mixta: opcional para la mayoría de catálogo `.3DS`/`.CCI` desencriptado; **obligatoria `aes_keys.txt`** para contenido cifrado (CIA cifradas, catálogo eShop de `3dseshop`) | Citra / Lime3DS / Azahar | Matiz exacto de obligatoriedad de `boot9.bin`/`boot11.bin` en modo normal **no verificado** contra fuente oficial (solo guías de terceros) — tratar con cautela hasta confirmar |
| `psvita` | Firmware oficial de Sony PS Vita (paquete completo v3.60/3.65, no fichero suelto) | Obligatoria (para la mayoría del catálogo comercial) | `Vita3K` | No es una BIOS clásica en fichero: se instala desde dentro del propio Vita3K (`File > Install Firmware`) para poder emular en LLE los módulos de sistema que algunos juegos requieren |
| `astrocade` | `astro.bin` (dentro de `astrocde.zip`, set MAME) | Obligatoria | MAME (driver `astrocde`) | Se gestiona como el resto de sets BIOS de MAME (ver sección Arcade) pese a ser un sistema de cartucho doméstico |
| `odyssey2` | `o2rom.bin` | Obligatoria | `lr-o2em` | Opcionales para variantes Videopac+ si se emulan: `c52.bin`, `g7400.bin`, `jopac.bin` |
| `intellivision` | `exec.bin` (Executive ROM), `grom.bin` (Graphics ROM) | Obligatorias ambas | `lr-freeintv` | |
| `channelf` | `sl31253.bin` + `sl31254.bin` (o pack combinado `channelf.zip`) | Obligatoria | `lr-freechaf` | |
| `coleco` | `colecovision.rom` (MD5 `2c66f5911e5b42b8ebe113403548eee7`, fallback `coleco.rom`) | Obligatoria | `lr-gearcoleco` | `lr-bluemsx` no necesita fichero de BIOS específico de Coleco, pero sí la carpeta `Databases`/`Machines` completa de blueMSX |
| `atari5200` | `5200.rom` | Obligatoria | `lr-atari800` | |
| `atari7800` | `7800 BIOS (U).rom` + `prosystem.dat` | BIOS opcional (HLE); `prosystem.dat` recomendado | `lr-prosystem` | La BIOS la marca "Optional" la doc oficial; el efecto exacto en compatibilidad al omitirla es saber de la escena, no confirmado textualmente en fuente oficial. `prosystem.dat` es distinto de la BIOS: es la base de hashes `.bin` de No-Intro que el core usa para identificar el mapper/tipo de cartucho de cada ROM headerless — necesario porque la fuente elegida para `atari7800` es `.BIN` (headerless, sin esa información en el propio fichero) en vez de `.A78` (headered). Va en la misma carpeta `system`/BIOS que el resto (ver `docs/system-paths.md#bios`) |
| `mastersystem` | `bios_U.sms` (USA), `bios_E.sms` (Europa), `bios_J.sms` (Japón) | Opcional (HLE, logo Sega) | `lr-genesis-plus-gx` | Regionales, no un `bios.sms` genérico |
| `fds` | `disksys.rom` | Obligatoria | `lr-fceumm` / `lr-nestopia` | Famicom Disk System, distinto del `nes` de cartucho estándar |
| `megadrive` | `bios_MD.bin` (Startup ROM) | Opcional (HLE) | `lr-genesis-plus-gx` | |
| `gb` | `gb_bios.bin` | Opcional (boot logo) | `lr-gambatte` | Requiere activar la opción de core "Use official bootloader"; nombre no verificado para el core alternativo `lr-sameboy` |
| `gamegear` | `bios.gg` | Opcional (HLE) | `lr-genesis-plus-gx` | |
| `lynx` | `lynxboot.img` | **Obligatoria** | `lr-handy` / `lr-beetle_lynx` | A diferencia de la mayoría de handhelds de esta tabla, aquí es obligatoria en ambos cores alternativos |
| `sega32x` | Nombres tipo `32X_G_BIOS.BIN`/`32X_M_BIOS.BIN`/`32X_S_BIOS.BIN` (**no confirmados en fuente oficial**, solo fuentes comunitarias) | Opcional (HLE confirmado; nombres exactos `[TODO]`) | `lr-picodrive` | Además de la BIOS de Mega Drive |
| `satellaview` | `BS-X.bin` | Opcional (solo para entorno BS-X) | `lr-snes9x` | Add-on de `snes` |
| `sufami` | `STBIOS.bin` | Opcional (solo para Sufami Turbo) | `lr-snes9x` | Add-on de `snes` |
| `64dd` | `IPL.n64` (`lr-mupen64plus_next`) o `64DD_IPL.bin` (`lr-parallel_n64`) — mismo contenido (mismo MD5), nombre distinto por core | Marcada "opcional" en el `.info` del core, pero de facto necesaria para que el 64DD funcione | `lr-mupen64plus_next` / `lr-parallel_n64` | |
| `gbc` | `gbc_bios.bin` | Opcional (boot logo) | `lr-gambatte` | Distinto del `gb_bios.bin` de Game Boy original |
| `pokemini` | `bios.min` | Opcional | `lr-pokemini` | |
| `gba` | `gba_bios.bin` | Opcional | `lr-mgba` | Requiere activar "Use BIOS file if found"; nombre no verificado para el core alternativo `lr-vba_next` |
| `ps2` | Dump según modelo, ej. `SCPH-70004_BIOS_V12_EUR_200.BIN` + `.rom0`/`.rom1`/`.nvm`/`.mec` con el mismo nombre base | Obligatoria | `PCSX2` (standalone) / `lr-lrps2` | "PCSX2 cannot play games without a BIOS, and no open-source alternative exists" (doc oficial). Alternativa HLE real solo en el core **Play!** (`lr-play`), emulador distinto, no una opción de PCSX2 |
| `gamecube` | `IPL.bin` (por región: `USA`/`EUR`/`JAP`) | Opcional (HLE) | `Dolphin` | Dolphin hace HLE del boot ROM; el `IPL.bin` real solo hace falta para el arranque con animación auténtica o títulos con uso intensivo de fuentes del sistema (ej. Star Fox Assault) |
| `wii` | Dump de NAND (nombre no estandarizado; incluye claves extraídas vía `keys.bin`/OTP) | Opcional, solo casos avanzados | `Dolphin` | Dolphin incluye las claves de Wii internamente; el NAND real solo hace falta para Wii Shop Channel/funciones de red, no para jugar |
| `wiiu` | `keys.txt` (clave común de Wii U + claves por juego si aplica) | Opcional según formato: obligatoria solo en `.wud`/`.wux`; **no** hace falta con `.wua` (formato recomendado por Cemu) | `Cemu` | |
| `switch` | `prod.keys` (+ `title.keys` para parches/DLC) + firmware oficial instalado como paquete NCA (no BIOS única) | Obligatoria (ambos, y deben coincidir de versión) | Ryujinx/Sudachi/Suyu/Eden/Citron (forks post-cierre de Yuzu 2024) | Sin fuente "oficial viva" tras la retirada legal de Yuzu/Ryujinx en 2024; nombre `prod.keys` consistente entre todos los forks activos |
| `xbox` | `mcpx_1.0.bin` (MCPX Boot ROM) + BIOS de consola modificada/debug (comúnmente `complex_4627v1.0.bin` o `bios.bin` — **xemu no arranca con BIOS retail sin modificar**) + imagen de HDD | Obligatoria (los tres) | `xemu` | Único caso de esta tabla con 3 componentes distintos obligatorios. El proyecto no distribuye ninguno por motivos legales |
| `xbox360` | — | No requiere | `Xenia` | HLE completo del kernel (`xboxkrnl`/`XAM`), no ejecuta firmware real |
| `ps3` | `PS3UPDAT.PUP` (firmware oficial completo de Sony) | Obligatoria | `RPCS3` | No es un fichero suelto en `system/`: se instala desde dentro del propio RPCS3 (`File > Install Firmware`) |
| `cdi` | `cdimono1.zip` (contiene `cdi200.rom`/`cdi220.rom`/`cdi220b.rom` + ROMs de servo/slave); variantes `cdi910.zip`/`cdimono2.zip` según hardware CD-i concreto | Obligatoria | MAME (`cdimono1`/`cdi910`/`cdimono2`) | Confirmado en código fuente MAME (`ROM_SYSTEM_BIOS`) |
| `jaguarcd` | BIOS CD embebida en el core; opcional sustituir por `[BIOS] Atari Jaguar CD (World).j64` real | Opcional (HLE por defecto) | `lr-virtualjaguar` | A diferencia del resto de la familia Jaguar, aquí sí existe un fichero BIOS real opcional documentado |
| `amigacdtv` | `kick34005.CDTV` (Kickstart 1.3 rev 34.005, ROM extendida CDTV v1.00) | Obligatoria (hay un Kickstart AROS no oficial como fallback parcial) | `lr-puae` | Distinta de las Kickstart de Amiga 500/1200 ya listadas en Microcomputers |
| `amigacd32` | `kick40060.CD32` (combinado) o par `kick40060.CD32` + `kick40060.CD32.ext` (Kickstart 3.1 rev 40.060 + ROM extendida) | Obligatoria (mismo fallback AROS no oficial) | `lr-puae` | |

**Sin BIOS confirmado (verificado, no `[TODO]` por omisión):** `atari2600`, `gameandwatch`, `vectrex`, `nes`, `sg1000`, `pcengine` (HuCard, distinto de `pcenginecd` de arriba), `snes`, `jaguar` (boot ROM embebida en el propio core, distinto de `jaguarcd`), `n64`, `ngp`, `ngpc`, `xbox360`, `psp`/`pspminis`/`psn` (PPSSPP no la necesita, HLE completo confirmado también para el catálogo físico UMD), `megaduck` (aportado por el usuario). **Indicios de que no, sin confirmación explícita en fuente primaria:** `supervision`, `wswan`, `wswanc`, `virtualboy` — no tratar como definitivo si aparece un caso real que lo contradiga.

## Arcade

En MAME/FBNeo la BIOS suele venir **embebida en el propio romset**, como set padre/compartido, no como fichero suelto en `bios/`:

- **`neogeo` (MVS/AES)** — `neogeo.zip` no va en la carpeta de sistema: se coloca **junto a las ROMs de juego** de Neo Geo (`lr-fbneo` / `lr-mame`). Contiene las BIOS regionales de la MVS (recreativa) y la AES (consola doméstica), incluyendo la Universe BIOS (Uni-BIOS) si se usa esa variante.
- **`cps1`** — sin BIOS compartida; cada set es autocontenido (confirmado en el driver `cps1.cpp` de MAME).
- **`cps2`** — **`qsound.zip`** (contiene `dl-1425.bin`, programa del DSP QSound) obligatoria para el sonido; nombre distinto de la clave de descifrado por juego (mecanismo aparte, no es un BIOS compartido).
- **`cps3`** — sin BIOS compartida para el uso normal: cada cartucho lleva su propio boot ROM cifrado con clave propia. `cps3boot.zip` no es una BIOS de sistema, es un romset bootleg independiente usado para reprogramar cartuchos de seguridad muertos.
- **`atomiswave`** — `awbios.zip` en `bios/dc/` (misma ruta que Dreamcast/NAOMI), opcional pero recomendada en `lr-flycast` (arranca en HLE sin ella).
- **`naomi`** (placa original) — `naomi.zip` en `bios/dc/`, opcional pero recomendada. El core libretro usa el mismo `naomi.zip` para NAOMI y NAOMI 2 (a diferencia de MAME, que sí distingue `naomi2.zip` aparte). Casos especiales con BIOS propia por juego: `hod2bios.zip`, `f355bios.zip`, `f355dlx.zip`, `airlbios.zip`.
- **`dreamcast`/`naomi2`** — ver fila `naomi` arriba para `lr-flycast`; MAME sí usa `naomi2.zip` como set separado.
- El resto de sistemas arcade de MAME tienen decenas de sets BIOS compartidos adicionales (ej. `decocass.zip`) — quedan fuera de esta tabla por volumen; se gestionan como parte normal de la auditoría del romset (`docs/guides/romsets/arcade.md`).

## Microcomputers

**Sin BIOS confirmado:** `c64`/`c128`/`vic20` (VICE incluye las ROM de sistema internamente, igual que el resto de la familia VICE), `thomson` (confirmado en la documentación oficial del core: "The Theodore core does not feature BIOS use").

| Identificador canónico | Fichero(s) BIOS | Obligatoria/Opcional | Emulador/core que la requiere | Notas |
| --- | --- | --- | --- | --- |
| `amiga` | `kick34005.A500` (Kickstart 1.3, A500), `kick40068.A1200` (Kickstart 3.1, A1200), `kick40063.A600` (Kickstart 3.1, A600) | Obligatoria | `lr-puae` | Nombre de fichero exacto, con mayúsculas del sufijo (`.A500`/`.A1200`/`.A600`). `kick34005.A500` cubre ~80% del catálogo `.ADF`; `kick40068.A1200` obligatoria para juegos AGA avanzados y packs `.LHA` de WHDLoad |
| `atarist` | `tos102.img` (TOS 1.02, ST básico), `tos206.img` (TOS 2.06, STE avanzado) | Obligatoria | `lr-hatari` | Acepta otras versiones de TOS; estas dos son las más estables/dominantes en la scene |
| `sharpx68000` | `iplrom.dat` (ROM de arranque), `cgrom.dat` (fuentes de caracteres japoneses) | Obligatoria | `lr-px68k` | **Ruta especial:** subcarpeta `bios/keropi/` (no sueltos en `bios/`) |
| `msx` / `msx2` | Carpetas `Databases/` y `Machines/` completas (no ficheros sueltos) | Obligatoria | `lr-bluemsx` | `Databases/` = hashes de cartuchos en XML; `Machines/` = configuraciones de hardware MSX/MSX2/MSX2+/Turbo-R. Sin ellas, pantalla negra especialmente al cargar `.DSK` |
| `dragon32` | `d32.rom` (Dragon 32), `d64.rom` (Dragon 64) | Opcional (HLE) | `lr-xroar` | XRoar tiene emulación de BIOS de alto nivel y arranca cinta sin ROM real; se recomienda añadirlas para compatibilidad completa, `d64.rom` necesaria para habilitar `.VDK` |
| `atari800` | `ATARIOSA.ROM` (400/800 PAL), `ATARIOSB.ROM` (400/800 NTSC), `ATARIXL.ROM` (XL/XE), `ATARIBAS.ROM` (intérprete BASIC) | Obligatorias (según modelo a emular) | `lr-atari800` | Mismo core que `atari5200`, que además requiere `5200.rom` propio (ver fila de Consolas) |

## Notas operativas

- **Verificación/normalización de packs comunitarios (idea de tooling, no implementada):** los "RetroArch BIOS Pack" de internet suelen traer ficheros duplicados o con nombres en mayúsculas (ej. `SCPH5501.BIN`). Un normalizador propio (verificar hash MD5 conocido → renombrar al nombre exacto esperado → mover a la subcarpeta correspondiente, `dc/`/`keropi/`/etc.) sería útil para `tools/scripts/`, pendiente de evaluar como script nuevo — no se han documentado aquí los hashes MD5 exactos por no estar verificados contra fuente propia.
