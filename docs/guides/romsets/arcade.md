# Preparación de romsets — Arcade

[TODO: descripción breve]

Aplica a MAME/FBNeo (ver `docs/romsets.md` y `docs/references.md`).

## Elección de tipo de set

Split / Non-Merged / Merged (ver `docs/references.md#romsets-arcade`).

## Fuente

[TODO]

## Verificación contra DAT MAME/FBNeo

Mismo problema que en sistemas ópticos: si el CHD o el `.zip` de arcade tienen nombre incorrecto, hay que curar por hash contra el DAT oficial de MAME en lugar de confiar en el nombre de archivo (ver detalle de herramientas en [optical-chd.md](optical-chd.md): RomVault, JRomManager, SabreTools Rebuild).

**Estructura exigida por MAME:** la ROM principal va en un `.zip` (ej. `kinst.zip`) y el `.chd` debe ir dentro de una subcarpeta con el mismo nombre exacto que ese zip (ej. `/kinst/kinst.chd`). Tanto RomVault como JRomManager crean automáticamente esta subcarpeta y mueven el CHD mal nombrado a su sitio correcto en cuanto se carga el DAT de la versión de MAME usada.

## BIOS y samples

[TODO]

## Organización en data/roms

[TODO]

## Notas

[TODO]
