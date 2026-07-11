# Curacion por sistema

Ficheros de curacion con informacion de referencia especifica por sistema (catalogo oficial vs. prototipos/homebrew, casos especiales de fuente, etc.) que no encaja como fila de tabla en `docs/romsets.md`.

Cada fichero puede combinar contenido curado a mano con una seccion auto-generada (entre `<!-- AUTO-GENERADO INICIO -->` / `<!-- AUTO-GENERADO FIN -->`) con el listado de familias de `metadata/dat-index/<id>.json`, regenerable con `tools/scripts/generate-romset-docs.ps1`.

Esta carpeta complementa, no sustituye:
- `docs/romsets.md` -- asociacion sistema -> DAT (fuente, formato, alternativa).
- `metadata/dat-index/<id>.json` -- indice generado a partir del DAT real.

| Sistema | Fichero |
| --- | --- |
| `3do` | [3do.md](3do.md) |
| `3ds` | [3ds.md](3ds.md) |
| `3dseshop` | [3dseshop.md](3dseshop.md) |
| `64dd` | [64dd.md](64dd.md) |
| `amigacd32` | [amigacd32.md](amigacd32.md) |
| `amigacdtv` | [amigacdtv.md](amigacdtv.md) |
| `cdi` | [cdi.md](cdi.md) |
| `dreamcast` | [dreamcast.md](dreamcast.md) |
| `dsiware` | [dsiware.md](dsiware.md) |
| `fds` | [fds.md](fds.md) |
| `gamecube` | [gamecube.md](gamecube.md) |
| `gamegear` | [gamegear.md](gamegear.md) |
| `gb` | [gb.md](gb.md) |
| `gba` | [gba.md](gba.md) |
| `gbc` | [gbc.md](gbc.md) |
| `gx4000` | [gx4000.md](gx4000.md) |
| `jaguar` | [jaguar.md](jaguar.md) |
| `jaguarcd` | [jaguarcd.md](jaguarcd.md) |
| `lynx` | [lynx.md](lynx.md) |
| `mastersystem` | [mastersystem.md](mastersystem.md) |
| `megadrive` | [megadrive.md](megadrive.md) |
| `n64` | [n64.md](n64.md) |
| `nds` | [nds.md](nds.md) |
| `neogeocd` | [neogeocd.md](neogeocd.md) |
| `nes` | [nes.md](nes.md) |
| `ngp` | [ngp.md](ngp.md) |
| `ngpc` | [ngpc.md](ngpc.md) |
| `pcengine` | [pcengine.md](pcengine.md) |
| `pcenginecd` | [pcenginecd.md](pcenginecd.md) |
| `pokemini` | [pokemini.md](pokemini.md) |
| `ps2` | [ps2.md](ps2.md) |
| `ps3` | [ps3.md](ps3.md) |
| `psp` | [psp.md](psp.md) |
| `psx` | [psx.md](psx.md) |
| `satellaview` | [satellaview.md](satellaview.md) |
| `saturn` | [saturn.md](saturn.md) |
| `sega32x` | [sega32x.md](sega32x.md) |
| `segacd` | [segacd.md](segacd.md) |
| `sg1000` | [sg1000.md](sg1000.md) |
| `snes` | [snes.md](snes.md) |
| `sufami` | [sufami.md](sufami.md) |
| `supervision` | [supervision.md](supervision.md) |
| `virtualboy` | [virtualboy.md](virtualboy.md) |
| `wii` | [wii.md](wii.md) |
| `wiiu` | [wiiu.md](wiiu.md) |
| `wswan` | [wswan.md](wswan.md) |
| `wswanc` | [wswanc.md](wswanc.md) |
| `xbox` | [xbox.md](xbox.md) |
| `xbox360` | [xbox360.md](xbox360.md) |
