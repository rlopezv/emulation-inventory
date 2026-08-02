# Guías de preparación de romsets

Flujos de trabajo para preparar romsets antes de distribuirlos en `data/roms/`. Cada guía es un scaffold pendiente de contenido.

| Flujo | Alcance | Guía |
| --- | --- | --- |
| Cartucho / plano | Consolas de cartucho, handhelds y microcomputers verificados con DAT No-Intro | [cartridge.md](cartridge.md) |
| Óptico → CHD | Sistemas ópticos (PSX, Saturn, Dreamcast, PC Engine CD, Sega CD, etc.) verificados con DAT Non-Redump y convertidos con CHDMan | [optical-chd.md](optical-chd.md) |
| Arcade | MAME/FBNeo, elección de tipo de set (split/merged/non-merged), BIOS y samples | [arcade.md](arcade.md) |
| Workflow end-to-end | Flujo completo DAT → auditoría → 1G1R → parcheo → compresión → gamelist, encadenando las herramientas de `docs/software.md` | [workflow.md](workflow.md) |
| Pipeline propio (tools/scripts) | Estado actual del pipeline de scripts del repo (DAT → dat-index → docs, ROMs físicas) y roadmap de ampliaciones propuestas | [custom-pipeline.md](custom-pipeline.md) |

## Curación por sistema

Información de referencia específica por sistema (catálogo oficial vs. prototipos/homebrew, casos especiales) que no encaja en las tablas de `docs/romsets.md`: ver [systems/](systems/README.md).
