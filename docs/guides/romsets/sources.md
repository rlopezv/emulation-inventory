# Fuentes de DAT — comportamiento por fuente, independiente del flujo de consumo

Las guías de flujo ([cartridge.md](cartridge.md), [microcomputers.md](microcomputers.md), [optical-chd.md](optical-chd.md), [arcade.md](arcade.md)) organizan la preparación de romsets por **tipo de consumo** (cartucho, microcomputer, óptico, arcade). Las fuentes de DAT (No-Intro, Redump, TOSEC...) no respetan esa frontera — TOSEC, por ejemplo, es la fuente principal o alternativa de la mayoría de microcomputers, pero también de algunas consolas de cartucho (`coleco`, `arcadia2001`, ver `docs/romsets.md` sección Consolas). Este fichero documenta el comportamiento de cada fuente en sí, aplicable a cualquier sistema que la use sin importar en qué guía de flujo esté clasificado ese sistema.

`docs/dat-sources.md` cataloga las fuentes por método de obtención (dónde descargarlas, formato exacto, layout). Este fichero es complementario: documenta el comportamiento de cara a **elegir qué usar para emulación**, no cómo obtenerlas.

## No-Intro: variantes por sistema

No-Intro publica en general un único DAT/formato por sistema (a diferencia de TOSEC) — pero en varios sistemas concretos publica **más de una variante del mismo contenido**, distinguibles solo por metadata técnica (orden de bytes, cabecera, cifrado), no por medio real distinto. Elegir la variante equivocada frente al romset real produce un hash que no coincide, aunque el contenido del juego sea idéntico al esperado.

Patrones recurrentes:

- **Headered vs. Headerless** — bloque de bytes añadido por copiadores/adaptadores de época o por convención de emulador (mapper, mirroring, tamaño de RAM...), no parte del volcado original del cartucho. Afecta a NES (iNES/NES 2.0, 16 bytes), SNES (SMC, 512 bytes — `.smc` con cabecera / `.sfc` sin cabecera, predominante en el set actual), Famicom Disk System (fwNES/FDS, 16 bytes), Atari 7800 (A78, 128 bytes) y Atari Lynx (LNX, 64 bytes — `.lnx` con cabecera / `.lyx` sin cabecera). Tabla completa en `docs/references.md#caso-especial--headered-vs-headerless-nes-snes-atari-7800-atari-lynx-fds`.
- **Byte order** — mismo contenido, distinto orden de bytes del volcado. Solo confirmado en N64: `.z64` Big Endian (formato nativo del cartucho, el que usa No-Intro como estándar de auditoría), `.v64` Byte Swapped (formato histórico tipo Doctor V64), `.n64` Little Endian (variante menos común). Detalle en `docs/references.md#caso-especial--nintendo-64-orden-de-bytes-byte-order`.
- **Variantes digitales (Decrypted/Encrypted/CDN)** — para catálogo distribuido digitalmente (eShop, PSN), No-Intro publica DAT separados según el estado de cifrado: `Decrypted` (contenido descifrado, forma habitual de uso en emulación), `Encrypted` (tal como se distribuyó originalmente) y `(Digital) (CDN)` (extraído directamente del Content Delivery Network de la tienda, sin pasar por una consola real). Afecta a `nds`, `dsiware`, `3ds`, `3dseshop`, `newn3ds`, `pspminis`, `psn`, `psvita`. El formato recomendado en [cartridge.md](cartridge.md#formato-de-rom-recomendado-por-sistema) es Decrypted/CDN salvo excepción señalada ahí.

El criterio de elección aplicado sistema a sistema (formato recomendado, DAT alternativo) sigue en la tabla "Formato de ROM recomendado por sistema" de [cartridge.md](cartridge.md#formato-de-rom-recomendado-por-sistema) — esta sección documenta el patrón general de la fuente (por qué existen varias variantes y qué las distingue), no repite la elección fila a fila.

### Standard / Parent-Clone / Aftermarket — variantes del propio paquete DAT-o-MATIC

Además de las variantes por sistema de arriba, DAT-o-MATIC exporta el **mismo catálogo** con tres esquemas de empaquetado distintos, no intercambiables entre sí (ver [dat-generation.md](../tools/dat-generation.md#no-intro-dat-o-matic) para el flujo completo de obtención):

- **Standard** — listado plano, sin relación de parentesco entre versiones/regiones de un mismo juego. Sirve para comprobar la integridad de un set completo, pero **no es suficiente para 1G1R** (ver [1g1r-filtering.md](../tools/1g1r-filtering.md)): sin `cloneofid` no hay forma de agrupar automáticamente las variantes de un mismo título.
- **Parent-Clone (P/C)** — el mismo catálogo con el atributo `cloneofid` inyectado, resolviendo qué versión es el "padre" y cuáles son "clones" (regiones/revisiones). Es el esquema que exige [1g1r-filtering.md](../tools/1g1r-filtering.md) para poder aplicar retool/Igir; **obligatorio** marcar "Default parent if there is no p/c info" al generarlo (si no, los juegos exclusivos de una sola región sin clones quedan huérfanos y el gestor de ROMs los puede omitir del filtrado).
- **Aftermarket** — catálogo aparte, no incluido en ningún pack (PC)/Standard: juegos no licenciados publicados *después* del último título licenciado oficial de esa plataforma (homebrew tardío, distinto de "Unlicensed" en general — es más bien un indicador del final de vida útil comercial de la consola). Hay que descargarlo explícitamente si interesa ese contenido.

**Diseño de fullset todavía pendiente de implementar** (ver `docs/session-context.md` y el histórico de decisión): un fullset real = `Standard`/`full` (títulos no-aftermarket) + `Aftermarket` sumados; `Parent-Clone` no sustituye esa suma, se usa además **para contrastarla** — comparar `full + aftermarket` contra `Parent-Clone` sirve para detectar huecos de cobertura entre packs (títulos que aparecen en uno pero no en el otro), no solo para obtener las relaciones de parentesco. `Parent-Clone` agrupa por `cloneof` como nombre exacto del padre (sin `id`/`cloneofid` numérico), un esquema de agrupación distinto al de `Standard`/`full` — cualquier indexado automático tiene que detectar cuál de los dos esquemas trae el DAT antes de procesarlo, no asumir siempre el mismo.

## Redump: patrón general y alternativas

A diferencia de TOSEC, Redump publica **un único DAT por sistema** (formato `XML (Logiqx, sin cloneofid)` — sin relación parent/clone automática, ver `docs/romsets.md`). Lo que sí se repite de forma prácticamente idéntica en unos 15 sistemas ópticos (`gamecube`, `wii`, `segacd`, `saturn`, `dreamcast`, `psx`, `ps2`, `jaguarcd`, `pcenginecd`, `3do`, `amigacdtv`, `amigacd32`, `xbox`, `neogeocd`...) es la combinación de tres fuentes distintas alrededor del mismo sistema — hoy repetida casi con las mismas palabras en la columna Notas de cada fila de `docs/romsets.md`:

- **Redump** (fuente principal) — solo admite volcados perfectos verificados comparando copias de múltiples usuarios; no cubre prototipos, betas ni contenido nunca publicado comercialmente, por diseño (política del grupo, no una carencia a resolver).
- **Non-Redump** (fuente alternativa) — cubre exactamente lo que Redump excluye por diseño: prototipos, betas, contenido en tránsito de validación. No es una alternativa completa al catálogo comercial, solo tapa ese hueco concreto — no sustituye a Redump como fuente principal en ningún sistema donde ambas coexisten.
- **MAMERedump** (contraste, no elección de fuente) — DAT `metadata/dat/MAMERedump/full/...dat` con hash SHA1, usado para contrastar el CHD ya generado a partir del romset Redump/Non-Redump. No es una fuente de romset alternativa donde elegir, sirve para verificar la conversión ISO/BIN·CUE → CHD (fase 7), no para decidir qué DAT auditar antes de convertir (fase 3).

Auxiliares de verificación publicados por Redump junto al DAT principal — cuesheets `.cue` y subcanal `.sbi` anti-LibCrypt (`redump-cuesheets`/`redump-sbi` en `docs/dat-sources.md`) — tienen su estructura interna por sistema (subcarpeta = slug de Redump) todavía sin declarar en ese fichero. No son un romset alternativo: son ficheros de soporte para la fase de verificación de las imágenes ya generadas, no para elegir qué auditar.

El criterio de elección aplicado sistema a sistema (cuándo aplica Non-Redump, dónde hay CHD de por medio) sigue en `docs/romsets.md` (secciones Consolas/Arcade) y [optical-chd.md](optical-chd.md) — esta sección documenta el patrón general de la fuente, no repite la elección fila a fila.

## TOSEC: varios romsets por sistema, criterio de elección

Las guías de flujo fijan un único formato/DAT por sistema como principal (ver la tabla "Formato de ROM recomendado por sistema" de [microcomputers.md](microcomputers.md#formato-de-rom-recomendado-por-sistema) o la fila correspondiente en [cartridge.md](cartridge.md#formato-de-rom-recomendado-por-sistema)). Lo que falta ahí es la razón completa: **TOSEC publica un DAT `Games` independiente por cada formato de contenedor del sistema** (tag entre corchetes en el nombre, ej. `[DSK]`, `[CDT]`, `[TZX]`...), no un único romset — esas tablas solo listan el principal y 1-2 alternativas de riesgo, no el catálogo completo. Antes de fijar un formato hace falta decidir, para cada uno de los publicados: ¿es un medio real distribuible (disco/cinta/cartucho) o un formato de preservación/transporte que no representa un medio jugable en sí? Y si es medio real, ¿lo carga el core/emulador que vamos a usar?

Cuatro categorías recurrentes, no exclusivas de un sistema:

- **Medio real, cargable directamente** — disco/cinta/cartucho tal como se distribuía, y el emulador objetivo lo lee sin conversión. Candidato a formato principal o alternativa real.
- **Medio real, pero desaconsejado** — existe y es cargable, pero con un problema práctico conocido (Fast Loading poco fiable en portátiles, requiere librería externa pesada, riesgo de incompatibilidad de plataforma hermana...).
- **No es un medio real** — snapshot de memoria (equivalente a un savestate), no algo que existiera como producto distribuido; no hay "romset" que preservar ahí en el sentido de TOSEC, es un volcado de estado de un emulador concreto en un instante dado.
- **Formato de preservación/transporte, no cargable por software** — pensado para hardware real (sustitutos físicos de disquetera tipo HxC) o para preservar la señal analógica de carga (audio de cinta), no una estructura de datos que un core de emulación consuma.

### Amstrad CPC

Listado completo de TOSEC (`tosecdev.org`, categoría Games, 11 formatos):

| Formato | Categoría | ¿Usable en `lr-caprice32`? | Notas |
| --- | --- | --- | --- |
| `[DSK]` | Medio real | Sí — **elegido como principal** | Disquete, universal (Caprice32/Arnold/WinAPE/CPCEmu), autostart nativo |
| `[CDT]` | Medio real, desaconsejado | Sí | Cinta (variante CPC del TZX); Fast Loading poco fiable en cores de portátiles, igual que TZX en Spectrum |
| `[CPR]` | Medio real, uso acotado | Sí, solo CPC Plus/GX4000 | ROM de cartucho — no aplica a CPC 464/664/6128 estándar |
| `[TZX]` | Medio real, desaconsejado | `[TODO]` | Formato de cinta de Spectrum reutilizado para preservación de protecciones de carga en CPC; sin confirmar si `lr-caprice32` lo carga igual que `.CDT` o si hace falta convertir primero |
| `[SNA]` | No es medio real | `[TODO]` | Snapshot de memoria en un instante — no un producto distribuido, más cercano a un savestate que a un romset; dudoso como entrada de catálogo general |
| `[ROM]` | Medio real, uso acotado | `[TODO]` | ROM de expansión/firmware, distinto de `[CPR]` — nicho, sin confirmar su papel real en juegos publicados (más propio de utilidades/tarjetas de expansión) |
| `[BIN]` | Medio real, desaconsejado | `[TODO]` | Volcado binario crudo sin cabecera de carga — mismo riesgo ya documentado para el `.BIN` suelto de `dragon32`: el emulador no sabe dónde inyectarlo en RAM sin metadata adicional |
| `[RAW]` | Preservación, no cargable | No | Volcado de bajo nivel del disquete (flujo crudo) — formato de preservación, no una imagen que un emulador cargue directamente, mismo caso que `[RAW]`/`[SCP]` ya descartados para `sharpx68000` |
| `[HXCSTREAM]` | Preservación para hardware real | No | Formato de flujo del **HxC Floppy Emulator**, un sustituto físico de disquetera para el Amstrad CPC real — pensado para hardware, no para emulación software |
| `[MP3]` | Preservación de audio | No | Grabación de audio de la señal de carga de cinta — preserva el sonido, no una estructura de datos que un core cargue |
| `[WAV]` | Preservación de audio | No | Igual que `[MP3]`, sin compresión (mayor fidelidad, mismo uso) |

De los 11, solo 3 son medio real sin reservas (`[DSK]`, `[CDT]`, `[CPR]`) — ya reflejados en la tabla de `microcomputers.md`. `[TZX]`/`[SNA]`/`[ROM]`/`[BIN]` quedan con soporte de `lr-caprice32` sin confirmar (`[TODO]`); `[RAW]`/`[HXCSTREAM]`/`[MP3]`/`[WAV]` quedan descartados como no aplicables a emulación software, no por falta de investigación sino porque no son ese tipo de formato.

### Atari 8-bit

Listado completo de TOSEC (`tosecdev.org`, categoría Games, 8 formatos):

| Formato | Categoría | ¿Usable en `lr-atari800`? | Notas |
| --- | --- | --- | --- |
| `[XEX]` | Medio real | Sí — **elegido como principal** | Ejecutable Atari (con cabecera de carga propia), autostart instantáneo sin pasar por disquetera |
| `[ATR]` | Medio real | Sí — alternativa fijada (catálogo completo) | Imagen de disquete estándar, formato más extendido para Atari 8-bit |
| `[ATX]` | Medio real, preservación avanzada | `[TODO]` | Imagen de disquete con preservación de esquemas de protección de copia (timing de sectores real) — análogo a `.IPF`/`.STX` en Amiga/Atari ST; sin confirmar si `lr-atari800` lo carga o si requiere el ATR equivalente ya "crackeado" |
| `[XFD]` | Medio real | `[TODO]` | Imagen de disquete alternativa a `.ATR` (sin la cabecera de 16 bytes de `.ATR`), formato menos extendido — sin confirmar soporte directo en el core |
| `[CAS]` | Medio real, desaconsejado | Sí | Cinta — ya descartada en `microcomputers.md` por carga lenta, mismo criterio que `dragon32`/`amstradcpc` |
| `[BIN]` | Medio real, uso acotado | `[TODO]` | Volcado de cartucho ROM — a diferencia del `.BIN` "crudo sin cabecera" de `dragon32`/`amstradcpc`, el cartucho Atari 8-bit sí tiene un formato de volcado bien definido; sin confirmar si `lr-atari800` distingue el tamaño/tipo de cartucho automáticamente o requiere configuración manual |
| `[BAS]` | No es medio real distribuible como juego | No | Listado de programa BASIC (tokenizado o fuente) — formato de "revista tipo tecleo" (type-in), no la distribución de un juego ya compilado; fuera de alcance de un romset de juegos |
| `[RAW]` | Preservación, no cargable | No | Volcado de bajo nivel del disquete — mismo caso ya establecido para `[RAW]` en `amstradcpc`/`sharpx68000`, formato de preservación, no imagen cargable directamente |

De los 8, `[XEX]`/`[ATR]` son los dos ya fijados (principal/alternativa). `[ATX]`/`[XFD]`/`[BIN]` quedan con soporte de `lr-atari800` sin confirmar; `[BAS]`/`[RAW]` descartados por no ser el tipo de formato adecuado (listado de programa y preservación de bajo nivel, respectivamente), no por falta de soporte del core.

### Atari ST

Listado completo de TOSEC (`tosecdev.org`, categoría Games, 10 formatos — no existe `[MSA]` como DAT separado pese a mencionarse como equivalente a `.ST` en `microcomputers.md`):

| Formato | Categoría | ¿Usable en `lr-hatari`? | Notas |
| --- | --- | --- | --- |
| `[ST]` | Medio real | Sí — **elegido como principal** | Imagen de disquete de sector plano, formato más extendido y universal (Hatari, Steem, PaCifiST...) |
| `[DIM]` | Medio real | `[TODO]` | Imagen de disquete alternativa (histórica de PaCifiST) — sin confirmar soporte directo en `lr-hatari` |
| `[STX]` | Medio real, desaconsejado | Sí, pero pesado | Formato Pasti — preserva esquemas de protección de copia; ya desaconsejado (requiere CAPSimg, más pesado de emular: audio entrecortado, ralentización) |
| `[IPF]` | Medio real, desaconsejado | Sí, pero pesado | Mismo caso que `[STX]` — preservación de protecciones, requiere CAPSimg, ya desaconsejado |
| `[PRG]` | Medio real, ejecutable directo | `[TODO]` | Ejecutable GEM independiente (sin disco completo) — análogo al `.XEX` de Atari 8-bit; sin confirmar si `lr-hatari` lo arranca de forma autónoma o solo dentro de una imagen de disco |
| `[TOS]` | Medio real, ejecutable directo | `[TODO]` | Ejecutable independiente sin interfaz GEM (a diferencia de `.PRG`) — misma incertidumbre que `[PRG]` sobre autostart directo en `lr-hatari` |
| `[STT]` | Sin confirmar qué es | `[TODO]` | No se ha confirmado si es un formato de disco real, un snapshot, o un formato propio del emulador Steem — pendiente de verificar contra la especificación TOSEC antes de clasificarlo |
| `[HFE]` | Preservación para hardware real | No | Formato de flujo del **HxC Floppy Emulator**, mismo caso que `[HXCSTREAM]` en `amstradcpc` — sustituto físico de disquetera, no emulación software |
| `[SCP]` | Preservación para hardware real | No | Formato del **SuperCard Pro**, dispositivo de captura/reproducción de flujo magnético real (como KryoFlux) — hardware, no software; además el paquete pesa 2,8 GB, coherente con ser volcado de flujo crudo |
| `[RAW]` | Preservación, no cargable | No | Volcado de bajo nivel del disquete — mismo caso ya establecido en `amstradcpc`/`sharpx68000`/`atari800` |

De los 10, solo `[ST]` está confirmado sin reservas; `[STX]`/`[IPF]` son medio real pero ya desaconsejados por peso; `[DIM]`/`[PRG]`/`[TOS]`/`[STT]` quedan pendientes de verificar (soporte de core, o incluso qué es exactamente en el caso de `[STT]`); `[HFE]`/`[SCP]`/`[RAW]` descartados por ser formatos de hardware real o preservación de bajo nivel, no emulación software.

### Commodore Amiga

Caso distinto a los anteriores: la categoría Games de TOSEC para Amiga publica **un único formato**, `[ADF]` — no hay `[CDT]`/`[TZX]`-equivalentes de cinta ni variantes de preservación de bajo nivel bajo Games. El resto de formatos de Amiga que sí existen en TOSEC quedan fuera de la categoría Games estándar:

| Formato | Categoría | ¿Usable en `lr-puae`? | Notas |
| --- | --- | --- | --- |
| `[ADF]` | Medio real | Sí — fuente alternativa ya fijada (`.LHA`/WHDLoad es la principal) | Disquete original, único formato de la categoría Games |
| `.IPF` | Medio real, desaconsejado | Sí, pero pesado | **No está en la categoría Games** — viene de un DAT aparte, "Unofficial IPF"; preserva protecciones de copia, requiere CAPSimg (mismo caso que `[STX]`/`[IPF]` de Atari ST) |
| `.HDF` | Sin DAT TOSEC | — | Disco duro virtual — no tiene DAT propio en TOSEC ni forma parte del DAT WHDLoad (que empaqueta uniformemente en `.lha`); sin fuente de verificación por hash para este formato |

Amiga confirma que la premisa "TOSEC publica un DAT por formato de contenedor" no es universal — depende de cuántas variantes de medio distinto tenga cada sistema en la práctica, no es un patrón fijo de N formatos por sistema.

### Commodore 128

Listado completo de TOSEC (`tosecdev.org`, categoría Games, 14 formatos + 1 subcategoría CP/M — reutiliza en gran parte lo ya investigado para `c64`/VICE):

| Formato | Categoría | ¿Usable en `lr-vice` (`x128`)? | Notas |
| --- | --- | --- | --- |
| `[D64]` | Medio real | Sí — **elegido como principal** | Disquete, mismo formato/core que `c64` (`lr-vice`) |
| `[D71]` | Medio real | Sí | Disquete de doble cara nativo del C128, ya confirmado cargable en VICE junto al resto de formatos D71/D81/G64/P00/PRG/T64 |
| `[D81]` | Medio real | Sí | Disquete 3.5" (unidad 1581) |
| `[G64]` | Medio real | Sí | Imagen de disquete a nivel de flujo GCR, cargable nativamente |
| `[PRG]` | Medio real | Sí | Programa/cartucho suelto |
| `[T64]` | Medio real | Sí | Contenedor de cinta tipo archivo |
| `[TAP]` | Medio real | Sí | Imagen de cinta real (a diferencia de `.T64`, volcado directo de la señal) |
| `[NIB]` | Medio real, requiere conversión en standalone | Sí (vía core); no directo en VICE standalone | El core RetroArch autoconvierte a G64 internamente; VICE standalone requiere `nibtools` primero |
| `[NBZ]` | Medio real, requiere conversión en standalone | Sí (vía core); no directo en VICE standalone | Mismo caso que `[NIB]` (versión comprimida) |
| `[ARC]` | Archivador de la escena, no imagen | No | Formato de compresión/transporte, no un disco cargable directamente |
| `[ARK]` | Archivador de la escena, no imagen | No | Mismo caso que `[ARC]` |
| `[LNX]` | Archivador de la escena, no imagen | No | "Lynx" (archivador C64/C128, sin relación con la consola Atari Lynx) — empaqueta varios ficheros, no una imagen de disco |
| `[SDA]` | Archivador de la escena, no imagen | No | Self-Dissolving Archive — autoextraíble, no cargable directamente |
| `[SFX]` | Archivador de la escena, no imagen | No | Self-Extracting archive — mismo caso que `[SDA]` |
| `Games - CPM - [D71]` | Subcategoría distinta, no "juegos" en sentido nativo | `[TODO]` | Software para el **modo CP/M** del C128 (sistema operativo de terceros, no el modo nativo BASIC/KERNAL) — categoría separada dentro de Games, no un formato de contenedor más; fuera de alcance de un romset de juegos C128 estándar salvo que se quiera cubrir software CP/M específicamente |

De los 14 formatos de contenedor, 7 son medio real directamente cargable (`D64`/`D71`/`D81`/`G64`/`PRG`/`T64`/`TAP`), 2 requieren conversión previa en VICE standalone aunque el core los soporte (`NIB`/`NBZ`), y 5 son archivadores de la escena sin equivalencia a imagen de disco (`ARC`/`ARK`/`LNX`/`SDA`/`SFX`) — mismo patrón de descarte que en `c64` (más abajo). La subcategoría CP/M queda aparte, no es un formato de contenedor sino un tipo de software distinto.

### Commodore Plus/4

Sistema dado de alta en `docs/systems.md` en esta misma sesión (`plus4` — Commodore 16, Commodore 116 y Plus/4, misma familia de hardware TED, un único core VICE `vice_xplus4`; antes solo aparecía citado como core dentro de la fila de `c64`). Listado TOSEC (`tosecdev.org`, categoría Games, 3 formatos — mucho más simple que la familia C64/C128):

| Formato | Categoría | ¿Usable en `lr-vice` (`xplus4`)? | Notas |
| --- | --- | --- | --- |
| `[PRG]` | Medio real | `[TODO]` — **candidato a principal** | Programa/cartucho suelto, mismo formato que ya usa `vic20` como principal; sin confirmar autostart directo en `xplus4` |
| `[D64]` | Medio real | `[TODO]` | Disquete — mismo formato de contenedor que `c64`/`c128`, presumible compatibilidad con `lr-vice` pero sin confirmar para el perfil `xplus4` en concreto |
| `[TAP]` | Medio real | `[TODO]` | Cinta — mismo criterio de "desaconsejado en portátiles" que el resto de cintas del catálogo, pendiente de confirmar si aplica igual aquí |

A diferencia del resto de sistemas de esta sección, `plus4` todavía no tiene la revisión formato×emulador confirmada (por eso los tres `[TODO]`) — solo se ha catalogado la existencia del sistema y de sus 3 DAT TOSEC. `.PRG` se marca como candidato a principal por analogía directa con `vic20` (mismo tipo de formato, mismo fabricante, catálogo de cartucho), no por verificación propia todavía.

### Commodore 64

A diferencia de `c128`, TOSEC divide el catálogo de `c64` en **12 sub-DAT por género** (Adventure/Arcade/Board/Boulder Dash/Cards/Gambling/Misc/Racing/Shoot'em Up/Simulation/Sports/Strategy, ver `docs/romsets.md` — hay que fusionarlos con `SabreTools --merge` antes de auditar), y dentro de cada género republica de nuevo **todo el catálogo de formatos de contenedor**, no solo uno. Unión de formatos distintos vistos en los 12 géneros (22 en total — más que `c128`, que no tiene `REU`/`ARC`/`DMP` como paquete separado del mismo tamaño):

| Formato | Categoría | ¿Usable en `lr-vice` (`x64sc`)? | Notas |
| --- | --- | --- | --- |
| `[CRT]` | Medio real | Sí — **elegido como principal** | Cartucho, autostart instantáneo sin teclado virtual ni mapeo de disquetera |
| `[D64]` | Medio real | Sí — alternativa ya fijada | Disquete, catálogo histórico masivo (incluye crackeados) |
| `[D71]` | Medio real | Sí | Disquete doble cara — mismo caso que `c128` |
| `[D81]` | Medio real | Sí | Disquete 3.5" |
| `[G64]` | Medio real | Sí | Imagen a nivel de flujo GCR |
| `[P00]` | Medio real | Sí | Contenedor PC64 (fichero único con cabecera de nombre largo) |
| `[PRG]` | Medio real | Sí | Programa/cartucho suelto |
| `[T64]` | Medio real | Sí | Contenedor de cinta tipo archivo |
| `[TAP]` | Medio real | Sí | Cinta, volcado directo de la señal |
| `[BIN]` | Medio real | Sí (confianza media-alta) | Sin confirmación oficial explícita del proyecto VICE, pero uso extendido en la comunidad |
| `[NIB]` | Medio real, requiere conversión en standalone | Sí (vía core); no directo en VICE standalone | Autoconvertido a G64 por el core; VICE standalone requiere `nibtools` |
| `[NBZ]` | Medio real, requiere conversión en standalone | Sí (vía core); no directo en VICE standalone | Mismo caso que `[NIB]`, versión comprimida |
| `[REU]` | Medio real, periférico específico | `[TODO]` | Software/dato para la **RAM Expansion Unit** (cartucho de expansión de memoria) — requiere emular el periférico REU en VICE, no es un disco/cinta estándar; sin confirmar cuántos títulos del catálogo realmente lo necesitan |
| `[ARC]` | Archivador de la escena, no imagen | No | Formato de compresión/transporte |
| `[ARK]` | Archivador de la escena, no imagen | No | Mismo caso que `[ARC]` |
| `[LNX]` | Archivador de la escena, no imagen | No | "Lynx" (archivador C64, sin relación con la consola Atari Lynx) |
| `[LBR]` | Archivador de la escena, no imagen | No | Formato "Library" (empaquetado de varios ficheros, origen CP/M reutilizado en C64) |
| `[SDA]` | Archivador de la escena, no imagen | No | Self-Dissolving Archive |
| `[SFX]` | Archivador de la escena, no imagen | No | Self-Extracting archive |
| `[DFI]` | Preservación, no cargable | No | Volcado de disco a bajo nivel, formato de preservación (no imagen directa) |
| `[DMP]` | Preservación, no cargable | No | Volcado de memoria/disco a bajo nivel, mismo caso que `[DFI]` |
| `[Z64]` | Formato de transporte, no imagen | No | Disco partido en segmentos Zipcode para transferencia a una unidad 1541 real — no es una imagen cargable en emulación |

De los 22, 9 son medio real directamente cargable (`CRT`/`D64`/`D71`/`D81`/`G64`/`P00`/`PRG`/`T64`/`TAP`) más `BIN` con confianza media-alta, 2 requieren conversión previa en VICE standalone (`NIB`/`NBZ`), 1 es un periférico específico sin confirmar cobertura (`REU`), y 9 quedan descartados por ser archivadores/formatos de transporte/preservación de bajo nivel, no imágenes cargables (`ARC`/`ARK`/`LNX`/`LBR`/`SDA`/`SFX`/`DFI`/`DMP`/`Z64`).

### Commodore VIC-20

Listado completo de TOSEC (`tosecdev.org`, categoría Games): 6 formatos de contenedor, con `[CRT]` y `[PRG]` publicados además en dos variantes **Singlepart**/**Multipart** cada uno (8 paquetes en total). La distinción Singlepart/Multipart no es un formato de contenedor distinto — es una división por **complejidad de carga**: Singlepart es un único fichero autocontenido; Multipart son juegos que necesitan varios ficheros cargados juntos (típicamente programas que exceden el banco de memoria de un cartucho/programa simple), más delicados de auditar/organizar en un romset porque un solo `.zip` de TOSEC no basta para saber automáticamente qué ficheros van juntos.

| Formato | Categoría | ¿Usable en `lr-vice` (`xvic`)? | Notas |
| --- | --- | --- | --- |
| `[PRG]` Singlepart | Medio real | Sí — **elegido como principal** | Programa/cartucho suelto, catálogo más grande de TOSEC para este sistema (1652 entradas) |
| `[TAP]` | Medio real | Sí — alternativa ya fijada | Cinta (849 entradas) |
| `[D64]` | Medio real | Sí | Disquete, mismo mecanismo que `c64`/`c128` (mismo core `lr-vice`) |
| `[T64]` | Medio real | Sí | Contenedor de cinta tipo archivo, mismo caso que `c64` |
| `[CRT]` Singlepart | Medio real | `[TODO]` | Cartucho — formato "más limpio" que `.PRG` en teoría (como en `c64`), pero no elegido como principal aquí por tener catálogo menor; sin confirmar soporte directo en `xvic` |
| `[BIN]` | Medio real, uso acotado | `[TODO]` | Volcado de cartucho sin cabecera — mismo riesgo ya documentado para `.BIN` en otros sistemas (dirección de carga no especificada) |
| `[CRT]` Multipart | Medio real, complejidad de organización | `[TODO]` | Mismo formato que `[CRT]` Singlepart, pero requiere gestionar varios ficheros como una sola entrada lógica — sin confirmar cómo lo espera `lr-vice` (M3U, carpeta, orden de carga) |
| `[PRG]` Multipart | Medio real, complejidad de organización | `[TODO]` | Mismo caso que `[CRT]` Multipart, para programas sueltos que exceden un único fichero |

De los 6 formatos base, 4 son medio real directamente usable sin reservas (`PRG` Singlepart ya elegido, `TAP` ya alternativa, `D64`, `T64`); `CRT` y `BIN` quedan con soporte en `xvic` sin confirmar; las variantes Multipart de `CRT`/`PRG` añaden una complejidad de organización (varios ficheros por juego) que no se ha investigado todavía, no solo una duda de soporte de core.

### Dragon 32/64

Listado completo de TOSEC (`tosecdev.org`): 6 formatos en la categoría Games, más un DAT de **Firmware** separado (BIOS/ROM del sistema, fuera de alcance de un romset de juegos — eso es competencia de `docs/bios.md`, no de esta guía).

| Formato | Categoría | ¿Usable en XRoar (standalone)? | Notas |
| --- | --- | --- | --- |
| `[CAS]` | Medio real | Sí — **elegido como principal** | Cinta, catálogo más masivo (564 entradas), autostart nativo |
| `[VDK]` | Medio real | Sí — alternativa ya fijada | Disquete, catálogo avanzado de Dragon 64, también nativo en XRoar |
| `[DSK]` | Medio real | `[TODO]` | Otro formato de imagen de disquete distinto de `.VDK` — sin confirmar si es un contenedor alternativo equivalente o un formato de una controladora de disco distinta; sin confirmar soporte directo en XRoar |
| `[PAK]` | Medio real, riesgo real | Sí, con cautela | Cartucho — **riesgo ya documentado**: muchos volcados están pensados para TRS-80 CoCo (plataforma hermana no intercambiable), pueden causar error de dirección de memoria si se mezclan sin verificar |
| `[BIN]` | Medio real, desaconsejado | `[TODO]` | Volcado binario suelto, sin la cabecera que indica al emulador dónde inyectar el código en RAM — mismo riesgo ya documentado |
| `[SNA]` | No es medio real | `[TODO]` | Snapshot de memoria en un instante — no un producto distribuido, mismo caso que `[SNA]` en `amstradcpc` |
| `[WAV]` | Preservación de audio | No | Grabación de audio de la señal de carga de cinta — mismo caso que `[WAV]`/`[MP3]` en `amstradcpc`, no es una estructura de datos que el core cargue |
| `Firmware` | Fuera de alcance (no es Games) | — | BIOS/ROM del sistema — corresponde a `docs/bios.md`, no a esta guía de romsets |

De los 6 formatos de Games, 2 están confirmados (`CAS` principal, `VDK` alternativa) y 1 más con riesgo ya conocido pero usable (`PAK`); `DSK`/`BIN`/`SNA` quedan pendientes de verificar; `WAV` descartado por ser preservación de audio, no estructura cargable.

### MSX

Listado completo de TOSEC (`tosecdev.org`, categoría Games, 5 formatos — más simple que otros sistemas, sin variantes de preservación de bajo nivel tipo `RAW`/`SCP`):

| Formato | Categoría | ¿Usable en `lr-bluemsx`? | Notas |
| --- | --- | --- | --- |
| `[ROM]` | Medio real | Sí — **elegido como principal** (fuente No-Intro, no TOSEC) | Cartucho, autostart instantáneo, catálogo Konami limpio |
| `[DSK]` | Medio real | Sí — alternativa ya fijada | Disquete, catálogo avanzado (RPGs/aventuras japonesas y de la escena NL/ES) |
| `[CAS]` | Medio real, desaconsejado | Sí, pero ya descartado | Cinta — ya descartada por emulación inestable/sin Fast Loading fiable |
| `[WAV]` | Preservación de audio | No | Grabación de audio de la señal de carga de cinta, mismo caso que en `amstradcpc`/`dragon32` |
| `[WV]` | Preservación de audio | No | WavPack — versión comprimida sin pérdida del mismo audio de carga que `[WAV]`, mismo uso |

De los 5, solo `[ROM]`/`[DSK]` son la pareja principal/alternativa ya fijada (con la particularidad de que `[ROM]` viene de No-Intro, no de TOSEC); `[CAS]` es medio real pero ya descartado por motivos de fiabilidad; `[WAV]`/`[WV]` quedan fuera por ser preservación de audio, no estructura cargable — mismo patrón que Amstrad CPC/Dragon 32.

### MSX2

Listado real confirmado (distinto del de MSX1 — comparte `[CAS]`/`[DSK]`/`[ROM]`, pero cambia `[WAV]`/`[WV]` por `[HFE]`/`[SCP]`, 5 formatos):

| Formato | Categoría | ¿Usable en `lr-bluemsx`? | Notas |
| --- | --- | --- | --- |
| `[DSK]` | Medio real | Sí — alternativa ya fijada | Disquete, catálogo avanzado — mismo criterio que MSX1, aquí es "especialmente crítico" (mayoría del catálogo avanzado de MSX2/MSX2+) |
| `[ROM]` | Medio real | Sí | Cartucho — aquí sí existe como DAT TOSEC propio (a diferencia de MSX1, donde `[ROM]` principal viene de No-Intro); `[TODO]` si conviene usar este TOSEC `[ROM]` en vez de/junto al de No-Intro, o si son el mismo catálogo |
| `[CAS]` | Medio real, desaconsejado | Sí, pero desaconsejado | Cinta — mismo criterio que MSX1 (emulación inestable, sin Fast Loading fiable) |
| `[HFE]` | Preservación para hardware real | No | Formato de flujo del HxC Floppy Emulator — mismo caso que en `amstradcpc`/`atarist`, sustituto físico de disquetera, no emulación software |
| `[SCP]` | Preservación para hardware real | No | Formato del SuperCard Pro — mismo caso que en `atarist`, hardware de captura de flujo real, no software |

De los 5, `[DSK]` es la alternativa ya fijada; `[ROM]` es medio real usable pero con una pregunta abierta (relación con el `[ROM]` de No-Intro que usa MSX1); `[CAS]` desaconsejado por el mismo motivo que en MSX1; `[HFE]`/`[SCP]` descartados por ser formatos de hardware real, mismo patrón que en `amstradcpc`/`atarist`.

### Sharp X68000

Listado completo de TOSEC (`tosecdev.org`, categoría Games, 4 formatos):

| Formato | Categoría | ¿Usable en `lr-px68k`? | Notas |
| --- | --- | --- | --- |
| `[DIM]` | Medio real | Sí — **elegido como principal** (fuente cambiada de Non-Redump en `docs/romsets.md`, que queda como alternativa) | Disquete 5.25", catálogo general — ver `docs/guides/romsets/microcomputers.md#formato-de-rom-recomendado-por-sistema` |
| `[HFE]` | Preservación para hardware real | No | Formato de flujo del HxC Floppy Emulator — mismo caso ya establecido en `amstradcpc`/`atarist`/`msx2`, sustituto físico de disquetera, no emulación software |
| `[RAW]` | Preservación, no cargable | No | Volcado de bajo nivel del disquete — mismo caso ya establecido en `amstradcpc`/`atari800`/`atarist`, formato de preservación, no imagen cargable directamente |
| `[SCP]` | Preservación para hardware real | No | Formato del SuperCard Pro — mismo caso ya establecido en `atarist`, hardware de captura de flujo real, no software |

De los 4, solo `[DIM]` es medio real usable, ya confirmado como principal; `[HFE]`/`[RAW]`/`[SCP]` descartados por ser formatos de hardware real o preservación de bajo nivel, mismo patrón ya visto en varios sistemas de esta guía. `.HDF` (disco duro virtual, dominante para juegos multi-disco) sigue sin DAT TOSEC localizado — pendiente igual que en `docs/guides/romsets/microcomputers.md`.

### Sinclair ZX Spectrum

Listado completo de TOSEC (`tosecdev.org`, categoría Games, 23 formatos — el catálogo más fragmentado de esta guía, reflejo de la enorme escena de clones/interfaces de terceros del Spectrum):

| Formato | Categoría | ¿Usable en `lr-fuse`? | Notas |
| --- | --- | --- | --- |
| `[TAP]` | Medio real | Sí — **elegido como principal** | Cinta, Fast Loading — ver `docs/guides/romsets/microcomputers.md#formato-de-rom-recomendado-por-sistema` |
| `[Z80]` | No es medio real, uso deliberado | Sí — alternativa ya fijada | Snapshot de memoria, pero usado deliberadamente como alternativa para arranque instantáneo en juegos de partida rápida (Jetpac, Manic Miner) |
| `[SNA]` | No es medio real, uso deliberado | Sí — alternativa ya fijada | Mismo caso que `[Z80]`, snapshot equivalente |
| `[DSK]` | Medio real | Sí — alternativa ya fijada | Disco, solo exclusivos Spectrum +3, incómodo sin teclado físico |
| `[TZX]` | Medio real, desaconsejado | Sí, pero desaconsejado | Cinta de preservación perfecta — ya desaconsejado por incompatibilidad de Fast Loading en muchos cores de portátiles |
| `[TRD]` | Medio real | `[TODO]` | Imagen de disco TR-DOS (interfaz Beta disk, popular en la escena rusa/clones del Este) — sin confirmar soporte directo en `lr-fuse` frente a conversión previa |
| `[SCL]` | Medio real, formato contenedor de TR-DOS | `[TODO]` | Archivo contenedor de ficheros TR-DOS, representación alternativa a `[TRD]` — mismo ecosistema, sin confirmar soporte directo |
| `[MGT]` | Medio real | `[TODO]` | Imagen de disco de la interfaz +D/DISCiPLE — sin confirmar soporte directo en `lr-fuse` |
| `[MDR]` | Medio real | `[TODO]` | Volcado de cartucho Sinclair Microdrive (cinta en bucle continuo dentro de cartucho) — periférico específico, sin confirmar cuántos títulos del catálogo lo usan ni soporte de core |
| `[FDI]` | Medio real | `[TODO]` | Formato de imagen de disco genérico (Full Disk Image) — sin confirmar soporte directo en `lr-fuse` |
| `[UDI]` | Medio real, preservación avanzada | `[TODO]` | Ultra Disk Image, preserva detalles de bajo nivel del disco (sectores débiles) manteniéndose cargable — análogo a `.ATX`/`.IPF` en otros sistemas; sin confirmar soporte en `lr-fuse` |
| `[IPF]` | Medio real, desaconsejado | `[TODO]` | Preservación de protecciones de copia — mismo caso que `[IPF]` en `atarist`/`amiga`, requiere CAPSimg, previsiblemente desaconsejado también aquí |
| `[DCK]` | Medio real, uso acotado | `[TODO]` | Volcado de cartucho ROM para la Interfaz 2 — nicho, pocos juegos se distribuyeron en este formato |
| `[ROM]` | Medio real, uso acotado | `[TODO]` | Volcado de cartucho/ROM — mismo caso de nicho que `[DCK]`, sin confirmar diferencia práctica entre ambos |
| `[CSW]` | Medio real, señal de cinta comprimida | `[TODO]` | Compressed Square Wave — captura la señal de audio de carga en forma de onda comprimida sin pérdida; a diferencia de `[WAV]`/`[MP3]` en otros sistemas, algunos emuladores (Fuse) sí lo cargan directamente como si fuera una cinta — sin confirmar en `lr-fuse` concretamente |
| `[D40]` | Medio real | `[TODO]` | Imagen de disco de 40 pistas — sin confirmar controladora/interfaz de origen ni soporte de core |
| `[D80]` | Medio real | `[TODO]` | Imagen de disco de 80 pistas — mismo caso que `[D40]` con doble densidad de pistas |
| `[SZX]` | No es medio real | `[TODO]` | "ZX-State", formato de snapshot moderno sucesor de `.Z80`/`.SNA` (más completo, preserva más estado de hardware) — mismo tipo de formato que esos dos, no un producto distribuido |
| `[SP]` | No es medio real | `[TODO]` | Formato de snapshot alternativo, mismo tipo que `[Z80]`/`[SNA]`/`[SZX]` |
| `[SLT]` | Sin confirmar qué es | `[TODO]` | No se ha confirmado si es un formato de disco/snapshot independiente o un fichero auxiliar de datos vinculado a `.Z80` para juegos +3 basados en disco — pendiente de verificar contra la especificación TOSEC antes de clasificarlo |
| `[SPG]` | Sin confirmar qué es | `[TODO]` | Sin identificar — pendiente de verificar contra la especificación TOSEC antes de clasificarlo |
| `[$B]` | Sin confirmar qué es | `[TODO]` | Nombre de tag atípico (no es una extensión de fichero convencional) — pendiente de verificar contra la especificación TOSEC antes de clasificarlo |
| `[Multipart]` | Empaquetado, no formato de contenedor | — | Agrupación de varios ficheros de un mismo juego que requieren carga secuencial — mismo caso que `[Multipart]` en `vic20`/`zx81`, no es un tipo de medio distinto |

De los 23, 5 son la combinación principal/alternativas ya fijada (`[TAP]` principal, `[Z80]`/`[SNA]`/`[DSK]`/`[TZX]` alternativas); el resto —la mayoría de los formatos de disco/cartucho/snapshot alternativos, y 3 formatos sin identificar (`[SLT]`, `[SPG]`, `[$B]`)— queda pendiente de la revisión formato×soporte de `lr-fuse` que ya se hizo para otros sistemas de esta guía; ninguno se ha investigado todavía en detalle.

### Sinclair ZX81

Listado completo de TOSEC (`tosecdev.org`, categoría Games, 4 formatos — catálogo simple, ya con la elección principal/alternativa fijada en `docs/guides/romsets/microcomputers.md`):

| Formato | Categoría | ¿Usable en `lr-eightyone`? | Notas |
| --- | --- | --- | --- |
| `[P]` | Medio real | Sí — **elegido como principal** | Programa nativo, autostart instantáneo |
| `[TZX]` | Medio real, desaconsejado | Sí, pero desaconsejado | Cinta — desaconsejada en portátiles, emulación tosca, exige teclado virtual y `LOAD ""` tokenizado |
| `[Z81]` | No es medio real | No cuenta como alternativa | Snapshot del emulador EightyOne — no un producto distribuido, no cuenta como formato alternativo real |
| `[Multipart]` | Empaquetado, no formato de contenedor | — | Empaquetado de varios `.P` que requieren carga secuencial — mismo caso que `[Multipart]` en `vic20`/`spectrum`, no es un tipo de medio distinto |

De los 4, ya está resuelto sin pendientes: `[P]` principal, `[TZX]` alternativa desaconsejada, `[Z81]` descartado por ser snapshot y `[Multipart]` por ser empaquetado, no formato.

### Thomson TO8/TO8D/TO9/TO9+ (y familia MO5/MO6/TO7)

Listado TOSEC de la familia TO8/TO8D/TO9/TO9+ (`tosecdev.org`, categoría Games, 4 formatos — el DAT de cinta principal usado en `docs/guides/romsets/microcomputers.md`, `Thomson MO5 - Games - [K7]`, pertenece a un DAT distinto de la subfamilia MO5, no al listado TO8 de aquí; TOSEC divide por modelo concreto pero el proyecto los unifica bajo `thomson` porque el core `lr-theodore` cubre toda la familia):

| Formato | Categoría | ¿Usable en `lr-theodore`? | Notas |
| --- | --- | --- | --- |
| `[K7]` | Medio real | Sí — principal para la subfamilia MO5, ya fijado | Cinta — mismo formato de contenedor que el DAT MO5 ya usado como principal en `docs/guides/romsets/microcomputers.md` |
| `[FD]` | Medio real | Sí — alternativa ya fijada (subfamilia TO8) | Disco, catálogo avanzado de la subfamilia TO8/TO8D/TO9/TO9+ |
| `[SAP]` | Medio real | Sí — alternativa ya fijada (subfamilia TO8) | Otro formato de disco de la misma subfamilia — coexiste con `[FD]` como alternativa, ver tabla de formato recomendado en `microcomputers.md` |
| `[QD]` | Medio real, periférico específico | `[TODO]` | Volcado de QuickDisk (unidad de disco de cinta continua, periférico específico de la gama TO8/TO9) — sin confirmar cuántos títulos del catálogo lo requieren ni soporte directo en `lr-theodore` |

De los 4, `[K7]`/`[FD]`/`[SAP]` ya están cubiertos por la elección principal/alternativa existente en `docs/guides/romsets/microcomputers.md`; `[QD]` queda pendiente de investigar por ser un periférico específico de disco poco común.

### Coleco ColecoVision

Caso más simple del catálogo: la categoría Games de TOSEC publica **un único DAT sin variantes de formato** (`Coleco ColecoVision - Games`, sin sufijo `[XXX]`) — sistema puramente de cartucho, sin la diversidad de medio (disco/cinta) del resto de sistemas de esta sección. Confirmado contra el manifiesto ya existente (`config/system_names/tosec.json`). `coleco` está clasificado como Cartucho/plano en `docs/guides/romsets/README.md`, no como Microcomputer — TOSEC es aquí fuente alternativa a No-Intro, no principal (ver `cartridge.md`).

| Formato | Categoría | ¿Usable? | Notas |
| --- | --- | --- | --- |
| (sin sufijo) | Medio real | Sí — único DAT disponible | Volcado de cartucho unificado; `[TODO]` confirmar core preferido entre `gearcoleco`/`bluemsx` (`docs/systems.md` lista ambos, sin standalone ColEm evaluado todavía para este flujo) |

No hay elección de formato que hacer aquí — a diferencia del resto de sistemas de esta sección, la pregunta relevante para ColecoVision no es "qué formato TOSEC elegir" sino "qué core preferir" (`gearcoleco` vs `bluemsx`), todavía sin resolver.

### Emerson Arcadia 2001

Mismo caso que ColecoVision: la categoría Games de TOSEC publica **un único DAT sin variantes de formato** (`Emerson Arcadia 2001 - Games`, sin sufijo `[XXX]`) — sistema puramente de cartucho. `arcadia2001` está clasificado como Cartucho/plano en `docs/guides/romsets/README.md`, no como Microcomputer — TOSEC es aquí fuente alternativa a No-Intro, no principal (ver `cartridge.md`).

| Formato | Categoría | ¿Usable? | Notas |
| --- | --- | --- | --- |
| (sin sufijo) | Medio real | Sí — único DAT disponible | Volcado de cartucho unificado; `[TODO]` core/emulador preferido — sin core RetroArch confirmado en `docs/systems.md` para este sistema, standalone a verificar |

Igual que ColecoVision, no hay elección de formato TOSEC que hacer — la pregunta pendiente aquí es directamente qué emulador usar, sin resolver todavía (a diferencia de ColecoVision, ni siquiera hay dos candidatos de core identificados).
