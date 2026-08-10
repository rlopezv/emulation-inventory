# Herramientas

Catálogo de herramientas de PC para gestión, validación, conversión y scraping de romsets/DATs. Distinto de `docs/software.md`, que cubre software instalado *en un dispositivo* (CFW, OS, frontends, launchers); estas herramientas no se instalan en los handhelds/SBC del inventario, sino que se usan en el ordenador para preparar las colecciones antes de desplegarlas en `data/roms/`.

## Convenciones

### Categoría

* Configuración
* Scraping
* Validación
* Gestión
* Librerías
* Volcado
* Conversión
* Ports
* Servicios
* Parcheo

### Estado

* Activo
* Mantenimiento
* Histórico
* Descontinuado
* Experimental

### Columnas

| Columna | Descripción |
| --- | --- |
| Nombre | Nombre del proyecto o herramienta |
| Variante | Rama o edición específica dentro del mismo proyecto |
| Tipo | Siempre `Tool` para este catálogo |
| Categoría | Función principal de la herramienta (ver convención) |
| Familia | Proyecto base o linaje técnico del que deriva |
| Frontend | Interfaz de usuario, si aplica |
| Requiere gamelist | Si necesita `gamelist.xml` para operar |
| Media soportada | Tipos de recursos visuales que puede generar o consumir |
| Página / repo | URL del proyecto o repositorio oficial |
| Plataforma principal | Arquitectura o entorno de ejecución principal |
| Dispositivos principales | Sistemas/formatos a los que se aplica habitualmente |
| Estado | Estado de desarrollo y mantenimiento actual |
| Notas | Observaciones relevantes sobre uso o posicionamiento |

---

## Herramientas y utilidades

| Nombre            | Variante | Tipo | Categoría     | Familia           | Frontend | Requiere gamelist | Media soportada   | Página / repo                                     | Plataforma principal | Dispositivos principales                      | Estado | Notas                                                            |
| ----------------- | -------- | ---- | ------------- | ----------------- | -------- | ----------------- | ----------------- | ------------------------------------------------- | -------------------- | --------------------------------------------- | ------ | ---------------------------------------------------------------- |
| EmuDeck           | —        | Tool | Configuración | EmuDeck           | —        | No                | No                | https://www.emudeck.com/                          | Linux / Windows      | Steam Deck, PC, handheld PC                   | Activo | Automatiza instalación y configuración de emuladores y frontends |
| Skraper           | —        | Tool | Scraping      | Skraper           | —        | Sí                | Imágenes + vídeos | https://www.skraper.net/                          | Windows              | Multiplataforma                               | Activo | Generación de gamelist.xml, imágenes, vídeos y metadatos         |
| SkyScraper        | —        | Tool | Scraping      | SkyScraper        | —        | Sí                | Imágenes + vídeos | https://github.com/muldjord/skyscraper            | Linux                | Batocera, RetroPie, Linux                     | Activo | Scraper muy utilizado en sistemas Linux                          |
| ClrMamePro        | —        | Tool | Validación    | ClrMamePro        | —        | No                | No                | https://mamedev.emulab.it/clrmamepro/             | Windows              | Arcade, No-Intro, Redump                      | Activo | Referencia para validación y reconstrucción de romsets           |
| RomCenter         | —        | Tool | Validación    | RomCenter         | —        | No                | No                | https://www.romcenter.com/                        | Windows              | Arcade, No-Intro, Redump                      | Activo | Alternativa más accesible a ClrMamePro                           |
| RomVault          | —        | Tool | Validación    | RomVault          | —        | No                | No                | https://www.romvault.com/                         | Windows              | Arcade, No-Intro, Redump                      | Activo | Validación y reconstrucción de colecciones                       |
| JRomManager       | —        | Tool | Validación    | JRomManager       | —        | No                | No                | https://github.com/optyfr/JRomManager             | Java                 | Multiplataforma                               | Activo | Gestión de romsets basada en DAT                                 |
| retool            | —        | Tool | Gestión       | retool            | —        | No                | No                | https://github.com/unexpectedpanda/retool         | Multiplataforma      | Multiplataforma                               | Mantenimiento | Filtra, recorta y convierte DAT oficiales de No-Intro y Redump en listas 1G1R; genera los DAT curados de `data/dats/console/` (`fullset` y `1g1r`) y el mapeo de variantes regionales en `metadata/dat/clonelist/*.json`; el propio repositorio declara "no longer maintained" (ver issue #337), sigue funcional pero sin desarrollo activo |
| Igir              | —        | Tool | Gestión       | Igir              | —        | No                | No                | https://igir.io                                   | Node.js (CLI, `npx`) | No-Intro, Redump, TOSEC, MAME                 | Activo | Alternativa moderna a retool para automatización (scripts, Docker, NAS); filtra 1G1R con prioridades configurables por CLI (`--prefer-region`, `--prefer-language`, `--prefer-verified`); gestiona también imágenes de disco (`.iso`, `.chd`, `.cue`) y detección de cabeceras headered/headerless |
| ROMSorter         | —        | Tool | Gestión       | ROMSorter         | —        | No                | No                | https://github.com/drakewill-CRL/ROMSorter        | Multiplataforma (CLI) | Multiplataforma                               | Activo | Escanea directorios de ROMs, calcula hashes (MD5, SHA-1, CRC32) y las organiza en carpetas según DAT; prioriza velocidad y bajo consumo |
| Don's MAME Lister | —        | Tool | Gestión       | Don's MAME Lister | —        | No                | No                | http://r0man0.free.fr/index.php/download-mame-xml-lists-and-generator/ | Windows              | Arcade, MAME                                  | Histórico | Filtra DAT o listas XML de MAME por categorías específicas (año, fabricante, género, controles, resolución) para generar sub-DATs personalizados |
| Simple Arcade Multifilter (SAM) | — | Tool | Gestión | SAM         | —        | No                | No                | https://github.com/markwkidd/ahk-retroarch-playlist-helpers/blob/master/Simple%20Arcade%20Multifilter.ahk | AutoHotkey (script) | Arcade, MAME                                  | Mantenimiento | Script AutoHotkey que aplica filtros masivos sobre sets arcade (elimina clones, mahjong, casino, contenido maduro) para dejar un set jugable limpio |
| datlib            | —        | Tool | Librerías     | datlib            | —        | No                | No                | https://pypi.org/project/datlib/                  | Python               | No-Intro, Redump                              | [TODO] | Librería Python para leer y procesar archivos DAT (No-Intro, Redump); base habitual para scripts personalizados de renombrado y automatización |
| SabreTools        | —        | Tool | Gestión       | SabreTools        | —        | No                | No                | https://github.com/SabreTools/SabreTools          | Multiplataforma (CLI) | No-Intro, Redump, MAME                       | Activo | Herramienta CLI líder para manipular, dividir, fusionar y convertir archivos DAT masivamente |
| SabreToolsStudio  | —        | Tool | Gestión       | SabreTools        | —        | No                | No                | https://github.com/Eggmansworld/SabreToolsStudio  | Windows / Linux      | No-Intro, Redump, MAME                       | Activo | Interfaz gráfica portátil construida sobre SabreTools; compila, verifica y mezcla archivos DAT de forma visual |
| MPF (Media Preservation Frontend) | — | Tool | Volcado | SabreTools | —        | No                | No                | https://github.com/SabreTools/MPF                 | Windows              | Discos ópticos (Redump)                       | Activo | Frontend para identificar y volcar discos ópticos con precisión, orquestando herramientas de volcado como Redumper |
| Redumper          | —        | Tool | Volcado       | Redumper          | —        | No                | No                | https://github.com/superg/redumper                | Multiplataforma (CLI) | Discos ópticos (Redump)                       | Activo | Herramienta de volcado de discos ópticos de alta precisión, usada como backend por MPF |
| verifydump        | —        | Tool | Validación    | verifydump        | —        | No                | No                | https://github.com/j68k/verifydump                | Multiplataforma (CLI) | Discos ópticos (Redump)                       | Activo | Cruza CHDs contra los `.cue` oficiales de Redump para validar la estructura interna del volcado, útil cuando el nombre del archivo no es fiable |
| binmerge          | —        | Tool | Conversión    | binmerge          | —        | No                | No                | https://github.com/putnam/binmerge                | Multiplataforma (CLI) | Discos ópticos (Redump)                       | Activo | Fusiona los múltiples `.bin` por pista de un dump Redump en un único `.bin` (o los divide de vuelta), regenerando el `.cue`; paso previo habitual antes de convertir a CHD |
| DATROMTool        | —        | Tool | Gestión       | DATROMTool         | —        | No                | No                | https://github.com/andrebrait/DATROMTool          | Multiplataforma (CLI) | No-Intro, Redump                              | Activo | Sucesor moderno inspirado en SabreTools; orientado a automatizar tratamiento de metadatos y colecciones 1G1R |
| RomM              | —        | Tool | Gestión       | RomM              | —        | No                | Imágenes + vídeos | https://romm.app/                                 | Docker / Linux / NAS | Colecciones multi-sistema                     | Activo | Gestión web de ROMs, scraping y catálogo centralizado            |
| CHDMan            | —        | Tool | Conversión    | MAME Tools        | —        | No                | No                | https://www.mamedev.org/                          | Multiplataforma      | CHD, MAME, Redump                             | Activo | Conversión y gestión de imágenes CHD                             |
| Maxcso            | —        | Tool | Conversión    | Maxcso            | —        | No                | No                | https://github.com/unknownbrackets/maxcso         | Multiplataforma (CLI) | PSP, PS2                                     | Activo | Compresor de alta velocidad de ISO a formato CSO/DAX; usa múltiples núcleos |
| NKit              | —        | Tool | Conversión    | NKit              | —        | No                | No                | https://github.com/Nanook/NKit                    | Windows              | GameCube, Wii                                 | Mantenimiento | Optimiza y restaura imágenes ISO de GameCube/Wii al tamaño mínimo conservando compatibilidad con Dolphin |
| DolphinTool       | —        | Tool | Conversión    | Dolphin           | —        | No                | No                | https://dolphin-emu.org/                          | Multiplataforma (CLI) | GameCube, Wii                                 | Activo | Utilidad CLI incluida y distribuida con Dolphin; convierte y verifica imágenes ISO/RVZ/GCZ de GameCube y Wii |
| Dolphin RVZ/ISO Conversion Scripts | — | Tool | Conversión | ElektroStudios | — | No | No | https://github.com/ElektroStudios/Dolphin_Emulator_RVZ_ISO_GameCube_Wii_Conversion_Scripts | Windows (script) | GameCube, Wii | Activo | Scripts de la comunidad que usan DolphinTool para automatizar la conversión masiva bidireccional ISO ⇄ RVZ y limpiar datos residuales del disco |
| PortMaster        | —        | Tool | Ports         | PortMaster        | —        | No                | Limitado          | https://portmaster.games/                         | Linux Handheld       | ROCKNIX, ArkOS, AmberELEC, muOS y compatibles | Activo | Instalación y gestión de ports nativos                           |
| RetroAchievements | —        | Tool | Servicios     | RetroAchievements | —        | No                | No                | https://retroachievements.org/                    | Multiplataforma      | Sistemas compatibles                          | Activo | Plataforma de logros para emulación                              |
| Tadpole           | —        | Tool | Configuración | Tadpole           | —        | No                | No                | https://github.com/EricGoldsteinNz/tadpole        | Windows              | Data Frog SF2000                              | Activo | Configuración y personalización de SF2000                        |
| SF2000 Multicore  | —        | Tool | Configuración | SF2000 Multicore  | —        | No                | No                | https://github.com/madcock/sf2000_multicore_cores | Data Frog SF2000     | SF2000                                        | Activo | Añade soporte multicore a SF2000                                 |
| Pandory Tool      | —        | Tool | Configuración | Pandory           | —        | No                | No                | https://github.com/TeamPandory/pandorytool        | Android / Linux      | Pandora Box compatibles                       | Activo | Configuración y desbloqueo de Pandora Box                        |
| ES Scraper | — | Tool | Scraping | EmulationStation | — | Sí | Imágenes + vídeos | [TODO] | Multiplataforma | EmulationStation, ES-DE y derivados | Activo | Scraper integrado utilizado por numerosas distribuciones basadas en EmulationStation |
| SimpleScraper | — | Tool | Scraping | SimpleScraper | — | Sí | Imágenes | [TODO] | Windows | EmulationStation y derivados | Mantenimiento | Alternativa ligera a Skraper para generación básica de metadatos e imágenes |
| gamelist-utils | — | Tool | Gestión | gamelist-utils | — | Sí | Imágenes + vídeos | https://github.com/JayCanuck/gamelist-utils | Node.js (TypeScript) | Multiplataforma | Activo | Copia, filtra, transforma y optimiza romsets junto a su gamelist.xml y media; soporta conversión entre EmulationStation, RetroArch, SimpleMenu, muOS y Onion; procesamiento por lotes con `--multi` |
| Lunar IPS (LIPS) | — | Tool | Parcheo | Lunar IPS | — | No | No | https://fusoya.eludevisibility.org/lips/ | Windows | Sistemas de 8 y 16 bits (NES, SNES, Genesis) | Histórico | Programa clásico y ligero para aplicar o crear parches en formato IPS |
| Flips (Floating IPS) | — | Tool | Parcheo | Flips | — | No | No | https://github.com/Alcaro/Flips | Multiplataforma | Sistemas de 8 y 16 bits | Activo | Alternativa moderna a Lunar IPS; genera parches IPS más pequeños y limpios; soporta también formato BPS |
| DeltaPatcher | — | Tool | Parcheo | xdelta | — | No | No | https://github.com/marco-calautti/DeltaPatcher | Windows | N64, PlayStation en adelante | Activo | Interfaz gráfica para xdelta; parcheo de juegos pesados donde el formato IPS no es viable por límite de tamaño |
| RDBEd | — | Tool | Gestión | RDBEd | — | No | No | https://github.com/schellingb/RDBEd | Windows / Linux / macOS (Mono) | RetroArch RDB | Activo | Editor open-source de bases de datos RetroArch (`.rdb`); lee/escribe `.rdb` y DAT (ClrMamePro); exporta a DAT (`File > Export DAT`) y vuelca `.rdb` a texto legible (`Tools > Dump RDB File`) |
| Rom Info Tools | — | Tool | Conversión | Rom Info Tools | HyperSpin | Sí | No | https://hyperspin-fe.com/files/file/18409-rom-info-tools/ | Windows | gamelist.xml, HyperList, No-Intro DAT, mameinfo/mamehistory | [TODO] | Convierte entre formatos de base de datos compatibles (gamelist.xml, nointrodat.dat, hyperspin.xml, mamelist.xml, mameinfo.dat, mamehistory.dat, retrofe_include.txt); genera DAT estilo No-Intro o HyperSpin desde una carpeta de ROMs, extrae/fusiona información y renombra ROMs |
| HyperSpin Database Creator | — | Tool | Gestión | HyperSpin Database Creator | HyperSpin | No | No | https://github.com/swhook52/HyperSpinDatabaseCreator | [TODO] | HyperSpin | [TODO] | Cruza el XML maestro de HyperSpin contra una carpeta de ROMs y genera un `*_custom.xml` con solo los juegos presentes; el XML original queda intacto |
| Don's HyperSpin List Generator | — | Tool | Validación | Don's HyperSpin Tools | HyperSpin | No | No | https://hyperspin-fe.com/files/file/5602-dons-hyperspin-tools/ | Windows | HyperSpin | Activo | Recorta el XML maestro de HyperSpin a solo las ROMs presentes localmente; auditor integrado de wheels/artwork/temas faltantes y detector de nombres mal escritos entre carpeta y lista |
| DATUtil | — | Tool | Conversión | DATUtil (Logiqx) | — | No | No | http://www.logiqx.com/Tools/DatUtil/DatUtil.php | Windows | No-Intro, Redump, ClrMamePro, RomCenter | [TODO] | Herramienta CLI de Logiqx (creador del formato Logiqx XML) para convertir, depurar y comparar DAT entre formatos (`listinfo`, `listxml`, `romcenter2`, `delimited`, `titlelist`, `sublist`) |
| DATVault | — | Tool | Servicios | RomVault | — | No | No | https://wiki.romvault.com/doku.php?id=what_is_datvault | Multiplataforma | No-Intro, Redump, MAME, MAME Software Lists | Activo | Servicio/API integrado en RomVault (≥3.4) que actualiza los DAT con un clic desde sus propios servidores; gratuito solo para el DAT oficial `mame -listxml`, el resto del repositorio requiere clave de pago vía Patreon |
