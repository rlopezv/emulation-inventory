# Preparación de romsets — Arcade

[TODO: descripción breve]

Aplica a MAME/FBNeo (ver `docs/romsets.md` y `docs/references.md`).

## Elección de tipo de set

Split / Non-Merged / Merged (ver `docs/references.md#romsets-arcade`).

## Fuente

Ver detalle completo de obtención en [dat-generation.md](../tools/dat-generation.md#mame--fbneo-ecosistema-arcade) y [MAME Software Lists](../tools/dat-generation.md#mame-software-lists-softwarelist) (para sistemas domésticos emulados dentro de MAME). Resumen: MAME se genera localmente (`mame -listxml`), FBNeo se obtiene vía `libretro-database/metadat/fbneo-split/`.

## Formato / contenedor recomendado por sistema

Sistemas clasificados como Arcade en [docs/guides/romsets/README.md](README.md#clasificación-de-sistemas-por-flujo). A diferencia de Óptico→CHD, aquí "formato" no es una elección (no hay ISO/BIN·CUE de origen que convertir) sino el tipo de contenedor que exige cada placa — ver detalle de cores/standalone asociados en `docs/arcade/arcade.md`.

| Identificador canónico | Contenedor | Notas |
| --- | --- | --- |
| `mame` | ZIP (Split/Non-Merged/Merged, ver arriba) | + `.chd` para juegos con disco, en subcarpeta con el nombre del set (ver "Verificación" más abajo) |
| `fbneo` | ZIP (mismo esquema que MAME) | + `.chd` para juegos con disco |
| `neogeo` | ZIP | BIOS compartida `neogeo.zip` en la raíz (AES y MVS comparten romset) |
| `cps1` | ZIP | Subconjunto de fbneo/mame |
| `cps2` | ZIP | Subconjunto de fbneo/mame |
| `cps3` | ZIP | Subconjunto de fbneo/mame |
| `naomi` | ZIP + `.chd` (o `.gdi`/`.lst`) | BIOS `naomi.zip` en la carpeta `system` de RetroArch, no junto a los juegos — ver `docs/arcade/arcade.md` |
| `atomiswave` | ZIP + `.chd` (o `.gdi`/`.lst`) | BIOS `awbios.zip`, misma carpeta `system` |
| `daphne` | Vídeo `.m2v`/`.ogg` + fichero de sincronización | No usa ROMs estándar — ver `docs/arcade/arcade.md` (fila Daphne / Hypseus Singe) |
| `naomi2` | [TODO] | Fuente: DAT MAME `0.260` o superior. Core/emulador recomendado: flycast (mismo que `naomi`). Contenedor sin confirmar todavía (probable ZIP + `.chd`, mismo linaje de hardware que `naomi`, sin verificar) |

## Verificación contra DAT MAME/FBNeo

Mismo problema que en sistemas ópticos: si el CHD o el `.zip` de arcade tienen nombre incorrecto, hay que curar por hash contra el DAT oficial de MAME en lugar de confiar en el nombre de archivo (ver detalle de herramientas en [optical-chd.md](optical-chd.md): RomVault, JRomManager, SabreTools Rebuild).

**Estructura exigida por MAME:** la ROM principal va en un `.zip` (ej. `kinst.zip`) y el `.chd` debe ir dentro de una subcarpeta con el mismo nombre exacto que ese zip (ej. `/kinst/kinst.chd`). Tanto RomVault como JRomManager crean automáticamente esta subcarpeta y mueven el CHD mal nombrado a su sitio correcto en cuanto se carga el DAT de la versión de MAME usada.

## BIOS y samples

**Confirmado en la documentación oficial de MAME:** algunas placas arcade comparten hardware base (ej. Neo Geo) — los datos de arranque/autotest de esa placa no se guardan como parte del romset de cada juego, sino como un fichero de BIOS aparte del propio sistema (ej. `neogeo.zip`). Ver también `docs/references.md#bios` y `docs/references.md#samples`.

**Estructura de carpetas confirmada:**

- **BIOS** — el `.zip` de BIOS va en la misma carpeta raíz que los ROMs de los juegos (no en subcarpeta propia).
- **Samples** — subcarpeta `samples/`, un `.zip` por juego que los necesite.
- **Artwork** (si se usa) — subcarpeta `artwork/`, también un `.zip` por juego.

**Parent/Clone y BIOS compartida:** cada placa con BIOS compartida define un set padre; los drivers de los juegos referencian ese padre, y el emulador fusiona el contenido del ZIP padre en tiempo de carga (relevante para sets `Merged`, ver `docs/references.md#romsets-arcade`).

## Organización en data/roms

[TODO: pendiente de detallar la estructura concreta esperada por sistema arcade dentro de `data/roms/` — ver estructura general ya documentada en `docs/guides/romsets/custom-pipeline.md` (`build-complete-romset.ps1`/`promote-complete-romset.ps1`) para el mecanismo genérico del repo, sin detalle específico de arcade todavía]

## Notas

[TODO]
