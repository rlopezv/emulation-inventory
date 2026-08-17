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
| `atari2600` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `atari5200` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `atari7800` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `astrocade` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `vectrex` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `odyssey2` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `intellivision` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `channelf` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Sistema añadido esta sesión, todavía sin indexar |
| `megaduck` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Sistema añadido esta sesión, todavía sin indexar |
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
| `newn3ds` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `gamecube` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `wii` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `wiiu` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | DAT indexado pero sin curar en `data/dats/console/` todavía |
| `switch` | ➖ | ➖ | [TODO] | ⬜ | ⬜ | Sin DAT de verificación estándar |
| `sg1000` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `mastersystem` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `megadrive` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `sega32x` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `gamegear` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `segacd` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `saturn` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `dreamcast` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `psx` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `ps2` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `ps3` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | DAT indexado pero sin curar en `data/dats/console/` todavía |
| `psp` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `pspminis` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `psn` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `psvita` | ➖ | ➖ | [TODO] | ⬜ | ⬜ | Sin DAT standalone identificado |
| `lynx` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `jaguar` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `jaguarcd` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `pcengine` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `pcenginecd` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `3do` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `cdi` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `amigacdtv` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `amigacd32` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `ngp` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `ngpc` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `wswan` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `wswanc` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `supervision` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `xbox` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
| `xbox360` | ✅ | ⬜ | [TODO] | ⬜ | ⬜ | DAT indexado pero sin curar en `data/dats/console/` todavía |
| `gx4000` | ✅ | ⬜ | [TODO] | ⚠️ | ⬜ | Único sistema con `gamelist.xml` real (no plantilla). Fuente TOSEC, no pasó por el pipeline Retool de `data/dats/console/` (pensado para No-Intro/Redump) |
| `neogeocd` | ✅ | ✅ | [TODO] | ⬜ | ⬜ | |
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
| `chihiro` | ➖ | ➖ | [TODO] | ⬜ | ⬜ | Sin DAT estándar; emulación sin viabilidad práctica en MAME (ver `docs/bios.md`) |
| `triforce` | ➖ | ➖ | [TODO] | ⬜ | ⬜ | Sin DAT estándar; emulación recién madurada en Dolphin (ver `docs/bios.md`) |

## Microcomputers

| Identificador | DAT generado | Romset curado | Formato final | En data/roms | Media | Notas |
| --- | --- | --- | --- | --- | --- | --- |
| `c64` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Fuente ya fijada (No-Intro), pendiente extender `build-dat-index-nointro.ps1` |
| `c128` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Fuente ya fijada (TOSEC), pendiente extender `build-dat-index-tosec.ps1` |
| `amiga` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Fuente ya fijada (WHDLoad, DAT ya descargado en `metadata/dat/WHDLoad/`), pendiente crear indexador nuevo |
| `spectrum` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Fuente ya fijada (TOSEC), pendiente extender `build-dat-index-tosec.ps1` |
| `zx81` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Ídem |
| `msx` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Fuente ya fijada (No-Intro), pendiente extender `build-dat-index-nointro.ps1` |
| `msx2` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Ídem |
| `amstradcpc` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Fuente ya fijada (TOSEC), pendiente extender `build-dat-index-tosec.ps1` |
| `atarist` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Ídem |
| `vic20` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Sistema añadido esta sesión, fuente ya fijada (TOSEC), sin indexar todavía |
| `atari800` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Sistema añadido esta sesión, fuente ya fijada (TOSEC), sin indexar todavía |
| `thomson` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Sistema añadido esta sesión, fuente ya fijada (TOSEC), sin indexar todavía |
| `sharpx68000` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Ídem |
| `dragon32` | ⬜ | ⬜ | [TODO] | ⬜ | ⬜ | Ídem |

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

- **Consolas (66 sistemas, incluye `channelf`/`megaduck` añadidos después del snapshot original):** 55 con DAT generado y romset curado (fullset+1G1R en `data/dats/console/`); 3 con DAT generado pero sin curar (`wiiu`, `ps3`, `xbox360`); `gx4000` es el único con `gamelist.xml` real (parcial, sin media); `neogeo`, `channelf`, `megaduck` sin indexar. 6 sin DAT por diseño (`sgb`, `switch`, `psvita`) o fuera de alcance de indexación actual.
- **Arcade (12 sistemas):** 0 indexados — sin script de indexado para arcade todavía (gap ya conocido, ver `docs/session-context.md`).
- **Microcomputers (14 sistemas, incluye `vic20`/`atari800`/`thomson` añadidos después del snapshot original):** 0 indexados pese a tener fuente ya fijada en `docs/romsets.md` — el trabajo real pendiente es extender `build-dat-index-tosec.ps1`/`build-dat-index-nointro.ps1` y crear el indexador de WHDLoad.
- **Engines/Ports (8 sistemas):** 0 indexados, sin script de indexado para DAT libretro todavía.
- **`data/roms/` (gamelist + media):** prácticamente en blanco en todo el repo — 51 de 52 carpetas creadas son plantilla vacía (`gamelist.xml` de 45 bytes, `media/*/. gitkeep` sin ficheros reales); solo `gx4000` tiene contenido real, y solo en `gamelist.xml` (sin media todavía).
- **Formato final:** no verificable desde este repo (las ROMs no viven aquí) — columna a rellenar manualmente por el usuario si se quiere llevar este dato en el mismo fichero.

## Pendiente

- Automatizar la regeneración de este snapshot (script en `tools/scripts/`, ej. `report-romset-status.ps1`) en vez de mantenerlo a mano — candidato claro dado que la lógica de cruce (dat-index existe/no vacío, fullset+1g1r existe, gamelist.xml no es la plantilla, media tiene ficheros reales) es enteramente mecánica.
- Columna "Formato final" requiere que el usuario indique manualmente el estado, ya que no hay visibilidad de las ROMs reales desde este repo.
