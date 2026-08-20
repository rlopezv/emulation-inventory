# Guía de BIOS/firmware

Cómo obtener, verificar, organizar y desplegar la BIOS/firmware que necesita cada sistema. Complementa dos ficheros de referencia que no repite:

- `docs/bios.md` — **qué** fichero(s) hace falta por sistema, si son obligatorios u opcionales, y cualquier subcarpeta especial.
- `docs/system-paths.md#bios` — **dónde** vive la carpeta `bios/` según el CFW instalado.

## Principio general

La BIOS es firmware con copyright de su fabricante original. La única vía legítima es volcarla de hardware propio, o instalarla mediante un canal oficial que el propio fabricante ofrece gratis a quien ya posee la consola (ej. el firmware de PS3/Vita, distribuido oficialmente por Sony para actualizar consolas reales). Esta guía no enlaza a ninguna fuente de descarga de BIOS — solo nombra las herramientas de volcado/verificación, que sí son de libre distribución.

## Proceso de volcado por familia

| Familia | Método | Herramienta habitual |
| --- | --- | --- |
| Consolas Sony ópticas (`psx`/`ps2`) | Volcado directo desde la consola real con un dispositivo de modding/soft-mod, o extracción del firmware de una imagen de sistema ya en posesión del usuario | Herramientas específicas por consola/modelo, `[TODO]` — no verificado en esta sesión cuál es el estándar actual de la escena |
| `ps3` | Descarga **oficial y gratuita** desde el soporte de Sony (`PS3UPDAT.PUP`, mismo fichero que actualizaría una PS3 real) e instalación desde dentro de RPCS3 (`File > Install Firmware`) | RPCS3 (proceso integrado) |
| `psvita` | Instalación del paquete de firmware oficial desde dentro del propio emulador | Vita3K (proceso integrado, `File > Install Firmware`) |
| GameCube/Wii (`gamecube`/`wii`) | Volcado de `IPL.bin` y/o NAND desde una consola real | Herramientas de dumping de Dolphin (menú propio) — ver wiki oficial de Dolphin para el procedimiento exacto, `[TODO]` no detallado aquí |
| `nds`/`dsiware` | Volcado de `bios7.bin`/`bios9.bin`/`firmware.bin` (DS) y adicionalmente `bios7i.bin`/`bios9i.bin`/NAND (DSi) desde hardware real | `fwTool`/`dsbf_dump.nds` (mencionadas en la FAQ oficial de melonDS) |
| `3ds`/`3dseshop`/`newn3ds` | Volcado de `boot9.bin`/`boot11.bin`/`aes_keys.txt`/`movable.sed` desde una 3DS real con acceso homebrew | GodMode9 (herramienta estándar de la escena 3DS para dumping) |
| `switch` | Extracción de `prod.keys` desde una Switch real con acceso a payload injection, e instalación del firmware oficial como paquete de ficheros | Lockpick_RCM (extracción de claves) |
| `xbox` | Volcado de `mcpx_1.0.bin` y BIOS de consola desde hardware modded | `[TODO]` — no investigado en esta sesión, requiere hardware con modchip o exploit de software |
| `wiiu` | Extracción de la clave común (`keys.txt`) desde una Wii U real con acceso homebrew | `[TODO]` — no investigado en esta sesión |
| Microcomputers (`amiga`/`atarist`/`sharpx68000`/etc.) | La ROM Kickstart/TOS/system suele adquirirse mediante licencias de reedición legal del fabricante actual de la marca (ej. paquetes "Amiga Forever" para Kickstart), o volcarse de hardware propio | `[TODO]` — no investigado en esta sesión qué canal de adquisición legal usa cada uno hoy |

**Nota:** esta tabla es una primera pasada, con varios `[TODO]` explícitos donde no se investigó el método exacto — no inventar el nombre de una herramienta de dumping sin confirmarlo en fuente oficial del proyecto correspondiente antes de rellenar los huecos.

## Verificación

Antes de dar una BIOS por buena, comprobar que el fichero coincide con el nombre y (si se conoce) el hash documentado en `docs/bios.md`. Varias de las investigaciones de esta sesión ya trajeron hashes MD5 puntuales como referencia (ej. `disksys.rom` MD5 `ca30b50f880eb660a320674ed365ef7a`, `gb_bios.bin` MD5 `32fbbd84168d3482956eb3c5051637f5`) pero **`docs/bios.md` no incluye todavía una columna de hash sistemática** — decisión pendiente del usuario sobre si merece la pena añadirla (ver `docs/session-context.md`).

Herramienta genérica: cualquier utilidad de checksum (`certutil -hashfile` en Windows, `sha1sum`/`md5sum` en Linux/WSL) contra el hash publicado por el propio proyecto del emulador en su documentación oficial — no contra hashes de foros/packs no verificados.

## Organización y renombrado

- Respetar el nombre de fichero **exacto** documentado en `docs/bios.md`, incluida la caja de mayúsculas/minúsculas (ej. `kick34005.A500`, no `kick34005.a500`) — varios cores son sensibles a esto en Linux (case-sensitive), aunque en Windows pase desapercibido.
- Respetar las subcarpetas especiales ya señaladas en `docs/bios.md` (`bios/dc/` para Dreamcast/NAOMI/Atomiswave, `bios/keropi/` para Sharp X68000).
- Los "RetroArch BIOS Pack" descargados de packs comunitarios suelen traer ficheros duplicados o con nombres en mayúsculas distintos del esperado — revisar y renombrar antes de copiar a la tarjeta.

## Despliegue

Una vez verificada y renombrada, la BIOS se copia a la ruta que le corresponda según el CFW instalado — ver `docs/system-paths.md#bios` para la tabla CFW × ruta. Las subcarpetas especiales (`dc/`, `keropi/`) van dentro de esa ruta base, no la sustituyen.

## Automatización futura (no implementada)

Idea de tooling anotada en `docs/bios.md` y `docs/session-context.md`: un normalizador propio (`tools/scripts/`) que verifique el hash MD5 conocido de cada fichero de un pack BIOS descargado, lo renombre al nombre exacto esperado y lo mueva a la subcarpeta correspondiente automáticamente. Pendiente de evaluar como script nuevo — no implementado todavía.
