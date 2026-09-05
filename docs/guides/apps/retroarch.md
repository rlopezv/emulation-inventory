# RetroArch

Frontend/backend de ejecución de núcleos libretro: motor unificado que carga "cores" (`.so`/`.dll` por sistema) bajo una única configuración de mando, guardado y shaders. Invocado desde EmulationStation, SimpleMenu u otros frontends por línea de comandos (`retroarch -L <core.so> <rom>`).

## Contexto de uso

| Contexto | Dónde aplica |
| --- | --- |
| Embebido en CFW | Backend de ejecución preinstalado en prácticamente todos los CFW Linux Handheld / OS Retro de este catálogo (ROCKNIX, KNULLI, ArkOS/dArkOS, Batocera, Recalbox, EmuELEC, AmberELEC...); el frontend del CFW solo lo invoca |
| Standalone instalable | Android y PC, cuando no se usa dentro de un CFW dedicado |

## CFWs / plataformas donde se usa

Backend de ejecución en la práctica totalidad de los CFW Linux Handheld y OS Retro cubiertos por `docs/software.md`. En Android es la vía recomendada para sistemas multiconsola de 8/16 bits (ver `android-emuladores.md`); en PC/Windows es el motor central de RetroBat.

## Descarga

| Plataforma | Fuente |
| --- | --- |
| Android | APK AArch64 directo del buildbot oficial (`buildbot.libretro.com/stable`), preferido sobre Google Play — mismo criterio que `android-emuladores.md` |
| Windows/Linux/macOS | <https://www.retroarch.com/> |
| Handheld/SBC | No aplica: viene integrado en el CFW |

## Instalación

| Contexto | Pasos |
| --- | --- |
| Embebido en CFW | No aplica, ya viene configurado |
| Standalone (Android/PC) | Instalación estándar del ejecutable/APK → primer arranque: `Online Updater > Core Downloader` (núcleos) y opcionalmente `Update Assets` / `Update Overlays` |

## Estructura de carpetas

| Carpeta | Contenido |
| --- | --- |
| `system/` | BIOS única compartida por todos los núcleos (a diferencia de los emuladores standalone Android, que la piden por app) |
| `config/remaps/<core>/` | Remaps de controles por núcleo (`<core>.rmp`) o por juego (`<contenido>.rmp`) |
| `overlays/` | Overlays de pantalla — bezels decorativos y overlays de teclado virtual (ver secciones abajo) |
| `saves/` / `states/` | Partidas guardadas nativas / save states de RetroArch |

## Microordenadores: mapeo de controles por juego

A diferencia de una consola, la mayoría de estos sistemas no tiene una convención de controles válida para todo su catálogo — cada juego puede esperar el joystick en un puerto distinto, teclas de acción adicionales (pausa, selección de arma, menú), o directamente no soportar joystick y exigir teclado. RetroArch expone dos mecanismos distintos según el núcleo, guardados por juego en `config/<core>/<juego>.opt` y `config/remaps/<core>/<juego>.rmp`:

- **Override de opciones de núcleo por juego** (`.opt`): guardado con `Quick Menu > Options > Save Game Options` tras ajustar las opciones del núcleo para ese juego en concreto.
- **Remap estándar de RetroArch** (`.rmp`, ver sección "Cuando el juego exige teclado"): mecanismo genérico RetroPad→dispositivo/tecla, usado como excepción puntual en núcleos donde la base ya funciona sola.

Todas las opciones y valores citados en esta sección están tomados de la documentación oficial de cada núcleo en `docs.libretro.com/library/<núcleo>/` (enlace en cada tabla) — no de una librería de configuración concreta, cuyo origen (core de RetroArch vs. emulador standalone) no se puede dar por hecho solo por la ruta donde vive.

### Arranque automático y joystick por núcleo

| Núcleo | Sistema(s) | Opción confirmada | Qué hace | Pendiente de verificar | Fuente |
| --- | --- | --- | --- | --- | --- |
| `vice_x64sc` / `vice_x128` / `vice_xvic` / `vice_xplus4` | `c64`, `c128`, `vic20`, `plus4` | `vice_autostart` (activo por defecto) + `vice_joyport` (`1`/`2`) | Simula `LOAD`+`RUN` automáticamente; fija el puerto de joystick | Si VIC-20/Plus4 (un solo puerto físico) necesitan forzar un valor distinto al de C64 — sin confirmar | <https://docs.libretro.com/library/vice/> |
| `fuse` | `spectrum` | `fuse_fast_load` (Off/On, On por defecto); `fuse_joypad_*` (mapeo de cada botón a una tecla) | Acelera la carga de cinta; permite jugar sin joystick estándar | Valor exacto para fijar Kempston como dispositivo por defecto desde el `.opt` (la documentación solo describe la selección manual desde `Quick Menu > Controls`, no un valor numérico) | <https://docs.libretro.com/library/fuse/> |
| `cap32` | `amstradcpc` | `cap32_autorun` (enabled/disabled, enabled por defecto) | Adivina y ejecuta el comando de arranque del disco, sin escribir `RUN"disco` | Si falla (discos CP/M o catálogo no estándar): `cap32_combokey` (`select`/`y`/`b`/`disabled`, `select` por defecto) elige qué botón abre el teclado virtual para escribirlo a mano | <https://docs.libretro.com/library/caprice32/> |
| `atari800` | `atari800` | `atari800_cassboot` (autoarranque de cinta), `atari800_internalbasic` (Off/On) | Autoarranca cinta; desactivar el BASIC interno es necesario para algunos cartuchos/discos | — | <https://docs.libretro.com/library/atari800/> |
| `px68k` | `sharpx68000` | `px68k_ramsize`, `px68k_joytype1`/`px68k_joytype2` (`Default (2 Buttons)` / `CPSF-MD (8 Buttons)` / `CPSF-SFC (8 Buttons)` / Cyberstick) | RAM y tipo de mando emulado; más botones para juegos de lucha | Opción de velocidad de disco: no encontrada | <https://docs.libretro.com/library/px68k/> ; <https://github.com/libretro/px68k-libretro/blob/master/libretro_core_options.h> |
| `theodore` | `thomson` | `theodore_autorun` (disabled/enabled, disabled por defecto); `theodore_rom` (`Auto`/`TO8`/`TO8D`/`TO9`/`TO9+`/`MO5`/`MO6`/`PC128`/`TO7`/`TO7/70`) | Autoarranca cinta/disco; fija el modelo Thomson cuando la autodetección falla | — | <https://docs.libretro.com/library/theodore/> |
| `81` | `zx81` | Tipo de dispositivo "Cursor Joystick" (seleccionable desde `Quick Menu > Controls`); opciones `Joypad ... Mapping` para asignar `NEW LINE` u otra tecla directamente a cualquier botón del RetroPad | La cruceta mapea a las teclas de cursor del ZX81 sin remap manual — el ZX81 no tuvo nunca interfaz Kempston, así que esa opción no existe en este núcleo. `NEW LINE` (el Enter del ZX81) se asigna a un botón por opción de núcleo, sin necesitar teclado físico ni `.rmp` | — | <https://docs.libretro.com/library/eightyone/> |
| `fmsx` | `msx`, `msx2` | `fmsx_mode` (`MSX2+`/`MSX1`/`MSX2`); dispositivo `Joystick + Emulated Keyboard` (seleccionable desde `Quick Menu > Controls`) | Fija el modelo MSX correcto; el dispositivo combinado permite joystick + teclas emuladas desde el mando sin overlay aparte | — | <https://docs.libretro.com/library/fmsx/> |
| `bluemsx` | `msx`, `msx2` | Ninguna necesaria para el arranque básico; dispositivos `RetroKeyboard` / `RetroPad Keyboard Map` disponibles si hace falta teclado | El joystick estándar MSX funciona de fábrica sin tocar opciones | — | <https://docs.libretro.com/library/bluemsx/> |
| `hatari` | `atarist` | `hatari_fastfdc` (disco rápido), `hatari_fastboot` (parcheo TOS para arranque rápido) | Acelera el acceso a disquete y el arranque del sistema | — | <https://docs.libretro.com/library/hatari/> |
| `puae` | `amiga` | `puae_floppy_speed` (`100`/`200`/`400`/`800`/`0`, entero plano sin `%`); `puae_use_whdload*` | Acelera la carga de disquete (0 = turbo, sin rotación emulada); arranque directo de juegos instalados vía WHDLoad | — | <https://docs.libretro.com/library/puae/> |
| `dosbox-pure` | `dos` | Menú propio del núcleo (elegir ejecutable con cruceta + `A`) | No requiere opciones de texto — resuelto por el propio núcleo | — | <https://docs.libretro.com/library/dosbox_pure/> |
| `xroar` | `dragon32` | Sin core libretro estándar confirmado | En Batocera, Dragon 32/64/Alpha se resuelve con MAME (standalone o core libretro `mame`); XRoar aparece ahí como emulador **standalone** aparte, no como core. No asumir que existe un `xroar` libretro en un CFW concreto sin comprobarlo primero contra la lista de sistemas/emuladores de ese CFW | Confirmar, CFW por CFW, si expone `xroar` como core o solo como standalone — la vía RetroArch de facto para este sistema parece ser el core `mame` | Sin página en `docs.libretro.com` (404 comprobado); <https://wiki.batocera.org/systems:dragon64> |

Contenido real de cada `.opt` (solo las líneas confirmadas arriba, tal como las documenta `docs.libretro.com`; el resto de opciones de cada núcleo se deja en su valor por defecto):

#### `vice_x64sc` / `vice_x128` / `vice_xvic` / `vice_xplus4` (`c64`, `c128`, `vic20`, `plus4`)

```ini
# config/vice_x64sc/<juego>.opt (mismo patrón para vice_x128 / vice_xvic / vice_xplus4)
vice_autostart = "enabled"
vice_joyport = "2"
```

#### `fuse` (`spectrum`)

```ini
# config/fuse/<juego>.opt
fuse_fast_load = "On"
```

Selección de Kempston como dispositivo: `Quick Menu > Controls > Port 1 Controls > Device Type > Kempston Joystick` (sin equivalente confirmado como línea de `.opt`).

#### `cap32` (`amstradcpc`)

```ini
# config/cap32/<juego>.opt
cap32_autorun = "enabled"
cap32_combokey = "select"
```

#### `atari800` (`atari800`)

```ini
# config/atari800/<juego>.opt
atari800_cassboot = "enabled"
atari800_internalbasic = "Off"
```

#### `px68k` (`sharpx68000`)

```ini
# config/px68k/<juego>.opt
px68k_ramsize = "12MB"
px68k_joytype1 = "CPSF-MD (8 Buttons)"
```

#### `theodore` (`thomson`)

```ini
# config/theodore/<juego>.opt
theodore_autorun = "enabled"
theodore_rom = "Auto"
```

#### `hatari` (`atarist`)

```ini
# config/hatari/<juego>.opt
hatari_fastfdc = "true"
hatari_fastboot = "true"
```

#### `puae` (`amiga`)

```ini
# config/puae/<juego>.opt
puae_floppy_speed = "400"
puae_use_whdload = "hdfs"
```

#### `fmsx` (`msx`, `msx2`)

```ini
# config/fmsx/<juego>.opt
fmsx_mode = "MSX2+"
```

Dispositivo combinado joystick+teclado: `Quick Menu > Controls > Port 1 Controls > Device Type > Joystick + Emulated Keyboard`.

Sin bloque de ejemplo para `bluemsx`, `81`, `dosbox-pure` y `xroar` — no por olvido, sino porque no hay ninguna opción confirmada que valga la pena escribir en su `.opt`: `bluemsx` y `81` funcionan sin configuración adicional (joystick de fábrica / dispositivo Cursor automático), `dosbox-pure` se resuelve desde su propio menú en pantalla (no por texto), y de `xroar` no hay ningún core libretro confirmado — ver nota de la tabla de arriba.

### Fuentes externas para consultar controles por juego

Para cuando falta la ficha del juego en la librería de configuración propia, estos catálogos comunitarios documentan los controles reales por título — más fiables que asumir una convención genérica:

| Sistema | Fuente | Qué aporta |
| --- | --- | --- |
| `spectrum` | World of Spectrum / ZXDB (spectrumcomputing.co.uk) | Ficha por juego con controles reales. Convención orientativa cuando no hay ficha: `Q`/`A`/`O`/`P` como direcciones, `Space` o `M` como disparo — confirmar siempre contra la ficha, no asumir |
| `amstradcpc` | CPC-Power (cpc-power.com) | Ficha por juego, en ocasiones con escaneo de las instrucciones originales de cinta/disco. Convención orientativa: cursores del teclado, o `Caps Lock`/`Ctrl`/`Copy`/`CLR` + `Space` |
| `c64` / `c128` / `vic20` / `plus4` | Lemon64 | Comunidad de referencia C64. El joystick es casi universal en este catálogo — si un juego no responde, revisar antes el puerto (`vice_joyport`) que las teclas |
| `msx` / `msx2` | Generation-MSX | Enciclopedia de software MSX. Convención orientativa: flechas de dirección + `Space` (botón 1) + `Graph`/`Code`/`M` (botón 2) |

Las convenciones orientativas de esta tabla son puntos de partida, no garantías — confirmar contra la ficha del juego concreto antes de darlas por buenas.

## Cuando el juego exige teclado: teclado virtual

Para lo que no se resuelve con el mapeo por juego de la sección anterior (juegos que exigen teclado directo, listados de revista, utilidades del propio sistema operativo), RetroArch ofrece varios mecanismos, combinables entre sí:

| Mecanismo | Ruta de menú | Qué hace |
| --- | --- | --- |
| Game Focus | `Settings > Input > Hotkey Binds > Game Focus` (tecla por defecto `Scroll Lock`) | Desactiva los hotkeys globales mientras el núcleo lee el teclado directamente, para que una tecla del juego no abra el menú por error |
| Remapeo RetroPad → teclado | `Settings > Input > Port 1 Controls`, o `Quick Menu > Controls` tras cargar contenido | Asigna un input emulado a cada botón del mando desde la propia interfaz; guardable como `Save Core Remap File` (`config/remaps/<core>/<core>.rmp`) o `Save Game Remap File` (`config/remaps/<core>/<contenido>.rmp`). El `.rmp` resultante guarda índices abstractos del input expuesto por ese núcleo, no códigos de tecla legibles — no se escribe a mano. Orden de carga: `retroarch.cfg` → override de núcleo → de directorio → de juego (el más específico gana) |
| Teclado virtual propio del núcleo | Depende del núcleo — detalle por núcleo abajo | Overlay de teclado renderizado por el propio núcleo sobre la pantalla emulada, independiente de los overlays de RetroArch |
| Overlay de teclado RetroArch | `Settings > On-Screen Overlay` | Mismo mecanismo que los overlays/bezels decorativos (ver sección siguiente) pero con zonas táctiles que envían teclas en vez de marco visual. Útil en dispositivos táctiles; **no es una solución adecuada para handhelds sin pantalla táctil** — sus zonas de entrada no están diseñadas para recorrerse con D-Pad/joystick |

Para un handheld sin pantalla táctil (R36T/R36S y similares), la estrategia correcta es el teclado virtual propio del núcleo o el mapper del núcleo — no el overlay genérico de RetroArch.

### Teclado virtual por núcleo

| Núcleo | Sistema(s) | Abrir teclado | Detalle / limitaciones |
| --- | --- | --- | --- |
| `puae` | `amiga` | `Select` (por defecto, sin configurar nada) | Posición en pantalla no configurable (se superpone al juego). Botón/tecla alternativo asignable vía `puae_mapper_vkbd` ("Toggle Virtual Keyboard"), sin asignar por defecto (`"---"`) |
| `vice_x64sc` / `vice_x128` / `vice_xvic` / `vice_xplus4` | `c64`, `c128`, `vic20`, `plus4` | `Select` (pulsación corta) alterna, por defecto | Dentro del teclado: `B`/`Enter` pulsa la tecla, `A` alterna transparencia, `Y` (corto) alterna ShiftLock, `X` = Space, `Start` = Return, tecla `JOY` cambia el puerto de joystick emulado. Botón/tecla alternativo asignable vía `vice_mapper_vkbd`, sin asignar por defecto (`"---"`) |
| `hatari` | `atarist` | `Y` alterna, `X` muestra/oculta | `R3` = Space; `B` = fuego/clic izquierdo y pulsa la tecla virtual; `R` cambia de página del teclado |
| `fuse` | `spectrum` | `Select` | `A`/`X`/`Y` = fuego del joystick, `B` = arriba, `L1` = RETURN, `R1` = SPACE |
| `cap32` | `amstradcpc` | `Select` (también asignable a `B` o `Y`, únicas opciones) | D-Pad + `Select` mueve el cursor sobre el teclado; personalizable en `Quick Menu > Controls > AMSTRAD KEYBOARD` |
| `dosbox-pure` | `dos` | `L3` (pulsar stick izquierdo) | `L2`/`R2` cambian la velocidad del cursor; `Controller Mapper` (menú de inicio del core o botón "PAD MAPPER" del teclado virtual) permite remapear hasta 4 funciones por botón entre teclado/ratón/joystick |
| `bluemsx` | `msx`, `msx2` | Sin overlay propio — usar `RetroKeyboard` (passthrough completo de teclado físico) o `RetroPad Keyboard Map`, seleccionable en `Port Controls` | Limitación conocida: no se puede tener overlay de teclado y RetroPad activos simultáneamente en la misma partida |
| `fmsx` | `msx`, `msx2` | Sin overlay dedicado — el dispositivo `Joystick + Emulated Keyboard` (`Quick Menu > Controls`) da acceso a teclado emulado junto al joystick | Mecanismo distinto al de un botón que "abre" un overlay: aquí se elige de entrada un tipo de dispositivo combinado |
| `atari800` | `atari800` | No hace falta teclado virtual para lo básico | `Select`, `Start` y `Option` (los botones físicos de la consola Atari) ya vienen mapeados de fábrica a los botones `Select`/`Start`/`L` del RetroPad — no hay que remapearlos a mano. La documentación oficial recomienda además usar el tipo de dispositivo "Atari Joystick" en vez de RetroPad genérico |
| `81` | `zx81` | Teclado virtual propio del núcleo, además de mapeo directo por opción | El dispositivo "Cursor Joystick" ya resuelve el movimiento; `NEW LINE` y el resto de teclas se asignan directamente a botones del RetroPad vía las opciones `Joypad ... Mapping`, sin depender del teclado virtual ni de un `.rmp` |
| `xroar` | `dragon32` | No aplica sin confirmar core | Ver nota en la tabla de arranque automático — sin core libretro estándar confirmado, la vía RetroArch de facto parece ser `mame` |
| `theodore` | `thomson` | Botón dedicado para mostrar/ocultar | Navegable íntegramente con mando: D-Pad selecciona la tecla, `B` la pulsa. `theodore_vkb_transparency` ajusta la transparencia del overlay |
| `px68k` | `sharpx68000` | Sin teclado virtual general (limitación conocida, no pendiente de investigar más) | `L2` abre el menú interno del emulador, no un VKBD. `px68k_joy1_select` remapea el botón Select a una tecla concreta (entre ellas `OPT1`/`OPT2`) — sirve para juegos que solo necesitan una tecla especial. Para teclado extensivo: dispositivo `RetroKeyboard` o una solución externa específica del frontend/dispositivo |

**No existe un remap "universal" válido para todos los núcleos a la vez** — cada `.rmp` vive dentro de la carpeta de su núcleo (`config/remaps/<core>/`), no hay un fichero compartido entre núcleos. Además, un `.rmp` no almacena códigos de tecla legibles tipo `RETROK_F11`: guarda índices abstractos del input que expone ese core/dispositivo concreto (ej. `input_player1_btn_l2 = "10"`), que varían de un núcleo a otro — no hay una línea universal que se pueda documentar a mano; se genera desde la propia interfaz (`Quick Menu > Controls > Port 1 Controls`, ajustar el botón, `Save Core Remap File` o `Save Game Remap File`), dejando que RetroArch escriba el fichero.

En `vice` y `puae` este `.rmp` ni siquiera hace falta para el teclado virtual: `Select` ya lo abre por defecto sin configurar nada, y la opción `vice_mapper_vkbd`/`puae_mapper_vkbd` ("Toggle Virtual Keyboard", sin asignar por defecto — `"---"`) asigna la acción **directamente** a otro botón del RetroPad (ej. `L2`) desde el propio `.opt` del núcleo, sin ningún paso intermedio de remapeo de teclado.

## Overlays y bezels

| Acción | Ruta | Qué hace |
| --- | --- | --- |
| Elegir overlay | `Settings > On-Screen Overlay > Overlay Preset` | Carga el par `.cfg`+`.png` (`overlays/`) |
| Descarga de packs oficiales | `Online Updater > Update Overlays` | — |
| Opacidad | `Settings > On-Screen Overlay > Overlay Opacity` | `0.00`–`1.00`, por defecto `0.15` — no depende del dispositivo |
| Auto Scale | `Settings > On-Screen Overlay > Overlay Auto Scale` | Reescala el overlay a la resolución actual; ayuda con paneles de tamaño distinto pero mismo aspect ratio, no corrige un overlay pensado para un aspect ratio distinto |
| Ocultar con mando conectado | `Settings > On-Screen Overlay > Hide Overlay when Gamepad is Connected` | Relevante sobre todo para overlays de teclado táctil (ver sección de microordenadores) |
| Alcance de la configuración | Mismo mecanismo de overrides que los remaps | Global (`retroarch.cfg`) o por núcleo/directorio/juego |

**Por qué esto es dependiente del dispositivo:** el fichero `.cfg` de un overlay define las coordenadas del hueco transparente (y del marco decorativo alrededor) para una resolución y aspect ratio de panel concretos — un pack hecho para 640×480 (el caso típico de Miyoo Mini+/A30) no encaja automáticamente en un panel de otra resolución o proporción, aunque `Overlay Auto Scale` esté activado. Además, para que el hueco coincida con el área real de renderizado, `Video > Scaling > Aspect Ratio` debe estar en `Core Provided` (no forzado a otro valor) y `Keep Aspect Ratio` activado — de lo contrario el overlay se desalinea aunque el pack sea el correcto para ese panel.

En la práctica, esto significa que casi nunca hay "el" pack de overlays válido para un sistema — hay que localizar (o encargar investigar) uno pensado para la resolución/aspect ratio exactos del dispositivo. Concepto general (qué es un overlay/bezel, ajuste al área efectiva según modo de escalado): `docs/references.md#overlays--bezels`. Búsqueda de un pack compatible con un dispositivo+CFW concreto: `prompts/theme_bezel_research.md`.

## Ópticos (CHD)

| Sistemas | Formato |
| --- | --- |
| PS1, Saturn, Sega CD, Dreamcast, 3DO, PC-FX | CHD (v5) — mandatorio, todos los núcleos relevantes lo leen nativo |
| PSP, PS2 (sistemas compatibles) | CSO |

Flujo de conversión: `docs/guides/romsets/optical-chd.md`.

## Arcade

| Placas | Romset recomendado |
| --- | --- |
| CPS1/2/3, Neo-Geo | DAT oficial FinalBurn Neo, Non-Merged |
| Resto del catálogo recreativo general | MAME 2003-Plus, `0.78-plus` |

Mismo criterio que `emulationstation.md`.
