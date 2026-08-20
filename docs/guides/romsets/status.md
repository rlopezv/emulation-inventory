# Estado del pipeline de romsets

Snapshot del progreso **actual** por sistema a través de las 10 fases de [workflow.md](workflow.md), condensado en 5 hitos. A diferencia de [bitacora.md](bitacora.md) (registro cronológico de qué se hizo en cada sesión), este fichero es una foto del estado presente — se sobreescribe, no se acumula.

## Cómo se generó este snapshot

Derivado del propio filesystem del repo (no autodeclarado), cruzando `docs/romsets.md` contra:

- **DAT generado** — ¿existe `metadata/dat-index/<id>.json` con contenido real (no vacío)? Cubre las fases 1-2 (obtención + conversión si hizo falta).
- **Romset curado** — ¿existe un DAT curado (fullset **y** 1G1R) en `data/dats/<categoría>/{fullset,1g1r}/` con nombre correspondiente al `DAT` de `docs/romsets.md`? Cubre las fases 3-5 (auditoría, limpieza, 1G1R). Generado con Retool en el caso de No-Intro/Redump — ver `docs/guides/tools/1g1r-filtering.md`.
- **Formato final** — ¿el romset físico está en el formato de despliegue definitivo (CHD/CSO/RVZ/etc. según aplique)? Cubre la fase 7. **No verificable desde este repo** (los ficheros de ROM en sí no viven aquí, `data/roms/` solo aloja `gamelist.xml`+`media/`, no las ROMs) — columna informativa que el usuario debe rellenar a mano.
- **En data/roms** — ¿`data/roms/<categoría>/<id>/gamelist.xml` tiene contenido real (no la plantilla vacía de 45 bytes)? Cubre la fase 8.
- **Media** — ¿`data/roms/<categoría>/<id>/media/` tiene ficheros reales, no solo `.gitkeep`? Cubre las fases 9-10.

**Leyenda:** ✅ Completo · ⚠️ Parcial · ⬜ Pendiente · ➖ No aplica (sin DAT por diseño, ver `docs/romsets.md`) · `[TODO]` no verificable desde el repo.

**Snapshot tomado:** 2026-08-17. Desactualizable en cuanto avance el pipeline — no hay automatización todavía que lo regenere (ver "Pendiente" al final).

## Consolas

| Identificador | DAT generado | Romset curado | Formato final | En data/roms | Media | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| `gameandwatch` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `atari2600` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Recuperado hoy (gap de manifiesto incompleto, ya cerrado); 18 títulos solo en `full+aftermarket` vs `pc/`, 84 divergencias de clonelist — catálogo con mucha escena aftermarket histórica |
| `atari5200` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Recuperado hoy (gap de manifiesto incompleto, ya cerrado) |
| `atari7800` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Recuperado hoy (gap de manifiesto incompleto, ya cerrado) |
| `astrocade` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Recuperado hoy (gap de manifiesto incompleto, ya cerrado) |
| `vectrex` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Recuperado hoy; DAT `(Aftermarket)` venía vacío (0 juegos), omitido automáticamente sin afectar al resultado |
| `odyssey2` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Recuperado hoy (gap de manifiesto incompleto, ya cerrado) |
| `intellivision` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Recuperado hoy (gap de manifiesto incompleto, ya cerrado) |
| `channelf` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `megaduck` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `nes` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `fds` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `satellaview` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `sufami` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `sgb` | ➖ | ➖ | [TODO] | ⬜ | ⬜ | Sin DAT propio por diseño (usa ROMs de `gb`/`gbc`) |
| `snes` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `gb` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `gbc` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `gba` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `virtualboy` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `n64` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `64dd` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `pokemini` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `nds` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `dsiware` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `3ds` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `3dseshop` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `newn3ds` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Recuperado hoy (gap de manifiesto incompleto, ya cerrado) |
| `gamecube` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `wii` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `wiiu` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | DAT indexado pero sin curar en `data/dats/console/` todavía |
| `switch` | ➖ | ➖ | [TODO] | ⬜ | ⬜ | Sin DAT de verificación estándar |
| `sg1000` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `mastersystem` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `megadrive` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `sega32x` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `gamegear` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `segacd` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy:** tenía romset curado antes del reseteo de `sources/`; `sources/dats/redump/` se borró y no se ha repoblado (sin `update-sources.ps1` equivalente para Redump), así que no entró en la tanda de Retool de hoy |
| `saturn` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `dreamcast` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `psx` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `ps2` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `ps3` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | DAT indexado pero sin curar en `data/dats/console/` todavía |
| `psp` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `pspminis` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Recuperado hoy (gap de manifiesto incompleto, ya cerrado) |
| `psn` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Recuperado hoy (gap de manifiesto incompleto, ya cerrado) |
| `psvita` | ➖ | ➖ | [TODO] | ⬜ | ⬜ | Sin DAT standalone identificado |
| `lynx` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `jaguar` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `jaguarcd` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `pcengine` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `pcenginecd` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `3do` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `cdi` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `amigacdtv` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `amigacd32` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `ngp` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `ngpc` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `wswan` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `wswanc` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `supervision` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `xbox` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `xbox360` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | DAT indexado pero sin curar en `data/dats/console/` todavía |
| `gx4000` | ✅ | ⬜ | [TODO] | ⚠️ | ⬜ | Único sistema con `gamelist.xml` real (no plantilla). Índice generado con el TOSEC anterior; `docs/romsets.md` ya no le asigna fuente (caso excepcional, tratamiento manual pendiente) — no pasó ni pasará por el pipeline Retool de `data/dats/console/` (pensado para No-Intro/Redump) |
| `neogeocd` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | **Regresión de hoy** — mismo motivo que `segacd` |
| `neogeo` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Fuente libretro (ClrMamePro texto); sin script de indexado todavía — mismo caso que la sección Arcade |

## Arcade

| Identificador | DAT generado | Romset curado | Formato final | En data/roms | Media | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| `mame` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Sin script de indexado para arcade todavía |
| `fbneo` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | |
| `neogeo` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Ver también fila en Consolas |
| `cps1` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Subconjunto de `fbneo`/`mame`, sin DAT propio |
| `cps2` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Subconjunto de `fbneo`/`mame`, sin DAT propio |
| `cps3` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | |
| `naomi` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Subconjunto de `fbneo`/`mame`, sin DAT propio |
| `atomiswave` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | |
| `daphne` | ➖ | ➖ | [TODO] | ⬜ | ⬜ | Sin DAT estándar |
| `naomi2` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | |

## Microcomputers

| Identificador | DAT generado | Romset curado | Formato final | En data/roms | Media | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| `c64` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Curado, pero cayó físicamente en `data/dats/console/` (Retool no distingue categoría) en vez de `data/dats/micro/` — revisar si mover o dejarlo así |
| `c128` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Fuente ya fijada (TOSEC), pendiente extender `build-dat-index-tosec.ps1` |
| `amiga` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Fuente ya fijada (WHDLoad, DAT ya descargado en `metadata/dat/WHDLoad/`), pendiente crear indexador nuevo |
| `spectrum` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Fuente ya fijada (TOSEC), pendiente extender `build-dat-index-tosec.ps1` |
| `zx81` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Ídem |
| `msx` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Curado, mismo caso que `c64`: cayó en `data/dats/console/` en vez de `data/dats/micro/` |
| `msx2` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | Curado, mismo caso que `c64`: cayó en `data/dats/console/` en vez de `data/dats/micro/` |
| `amstradcpc` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Fuente ya fijada (TOSEC), pendiente extender `build-dat-index-tosec.ps1` |
| `atarist` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Ídem |
| `sharpx68000` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Ídem |
| `dragon32` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Ídem |
| `vic20` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Sistema añadido esta sesión, fuente ya fijada (TOSEC), sin indexar todavía |
| `atari800` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Sistema añadido esta sesión, fuente ya fijada (TOSEC), sin indexar todavía |
| `thomson` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Sistema añadido esta sesión, fuente ya fijada (TOSEC), sin indexar todavía |

## Engines / Ports

| Identificador | DAT generado | Romset curado | Formato final | En data/roms | Media | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| `scummvm` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Sin script de indexado para DAT libretro (ClrMamePro texto) todavía |
| `dos` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | |
| `doom` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | |
| `quake` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | |
| `quake2` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | |
| `cavestory` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | |
| `openbor` | ➖ | ➖ | [TODO] | ⬜ | ⬜ | Sin DAT estándar |
| `ports` | ➖ | ➖ | [TODO] | ⬜ | ⬜ | Sin DAT estándar |

## Resumen

- **Consolas (66 sistemas):** los **44 sistemas No-Intro del manifiesto** (`tools/scripts/config/nointro-systems.json`) están completos: DAT generado + romset curado (fullset+1G1R) en `data/dats/console/`, incluidos los 15 recuperados hoy tras cerrar el gap de manifiesto incompleto (`channelf`, `megaduck`, `atari2600`, `atari5200`, `atari7800`, `astrocade`, `vectrex`, `odyssey2`, `intellivision`, `newn3ds`, `pspminis`, `psn`, más `c64`/`msx`/`msx2` que son Microcomputers pero cayeron aquí). **Regresión real de hoy: 15 sistemas Redump perdieron su romset curado** (`segacd`, `saturn`, `dreamcast`, `psx`, `ps2`, `gamecube`, `wii`, `xbox`, `jaguarcd`, `pcenginecd`, `3do`, `cdi`, `amigacdtv`, `amigacd32`, `neogeocd`) — tenían DAT curado antes del reseteo de `sources/`, pero `sources/dats/redump/` se borró y no se ha repoblado (no existe un `update-sources.ps1` equivalente para Redump), así que no pudieron pasar por la tanda de Retool de hoy. `wiiu`/`ps3`/`xbox360` (Non-Redump) siguen igual que antes: DAT indexado, sin curar. `gx4000` es el único con `gamelist.xml` real (parcial, sin media). `neogeo` sin indexar (formato libretro). 6 sin DAT por diseño (`sgb`, `switch`, `psvita`).
- **Arcade (10 sistemas):** 0 indexados — sin script de indexado para arcade todavía (gap ya conocido, ver `docs/session-context.md`).
- **Microcomputers (14 sistemas):** `c64`/`msx`/`msx2` curados (ver nota de ubicación en `data/dats/console/` en vez de `data/dats/micro/`, arriba). El resto (`c128`, `amiga`, `spectrum`, `zx81`, `amstradcpc`, `atarist`, `sharpx68000`, `dragon32`, `vic20`, `atari800`, `thomson`) sigue sin indexar pese a tener fuente ya fijada en `docs/romsets.md` — el trabajo real pendiente es extender `build-dat-index-tosec.ps1` y crear el indexador de WHDLoad.
- **Engines/Ports (8 sistemas):** 0 indexados, sin script de indexado para DAT libretro todavía.
- **`data/roms/` (gamelist + media):** prácticamente en blanco en todo el repo — de las 67 carpetas creadas (52 originales + 15 scaffold nuevas: `channelf`/`megaduck`/`atari2600`/`atari5200`/`atari7800`/`astrocade`/`vectrex`/`odyssey2`/`intellivision`/`newn3ds`/`pspminis`/`psn` en `console/`, `vic20`/`atari800`/`thomson` en `micro/`), 66 son plantilla vacía (`gamelist.xml` de 45 bytes, `media/*/.gitkeep` sin ficheros reales); solo `gx4000` tiene contenido real, y solo en `gamelist.xml` (sin media todavía). Ya no quedan huecos de scaffold para ningún sistema con fuente ya fijada en `docs/romsets.md`.
- **Formato final:** no verificable desde este repo (las ROMs no viven aquí) — columna a rellenar manualmente por el usuario si se quiere llevar este dato en el mismo fichero.

## Pendiente crítico — recuperar Redump

Los 15 sistemas Redump listados arriba como "regresión de hoy" necesitan que `sources/dats/redump/` se repueble antes de poder pasar por Retool otra vez. No hay script `update-sources.ps1` equivalente para Redump (solo existe para No-Intro) — hace falta decidir si se copian a mano desde `metadata/dat/Redump/` o si se crea un script de sincronización análogo al de No-Intro.

## Pendiente

- Automatizar la regeneración de este snapshot (script en `tools/scripts/`, ej. `report-romset-status.ps1`) en vez de mantenerlo a mano — candidato claro dado que la lógica de cruce (dat-index existe/no vacío, fullset+1g1r existe, gamelist.xml no es la plantilla, media tiene ficheros reales) es enteramente mecánica.
- Columna "Formato final" requiere que el usuario indique manualmente el estado, ya que no hay visibilidad de las ROMs reales desde este repo.
