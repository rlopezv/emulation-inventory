# Emulation Docs

Documentación normalizada de un ecosistema personal de emulación multi-dispositivo.

El objetivo es mantener una base de conocimiento útil para:

- Decidir qué CFW o frontend utilizar en cada dispositivo.
- Seleccionar los mejores romsets para cada hardware.
- Mantener un registro de lo instalado y lo recomendado.
- Curar colecciones de juegos optimizadas para bartop o handheld.

Funciona como espacio de trabajo colaborativo con Claude Code.

---

## Documentos principales

| Fichero | Propósito |
| --- | --- |
| `docs/devices.md` | Inventario de hardware (handhelds, SBCs, tablets) |
| `docs/systems.md` | Catálogo de sistemas emulados e identificadores canónicos |
| `docs/romsets.md` | Asociación romset-DAT por sistema |
| `docs/software.md` | Catálogo de CFW, OS retro, frontends y launchers (software instalado en dispositivo) |
| `docs/tools.md` | Catálogo de herramientas de PC para gestión de romsets/DATs |
| `docs/distributions.md` | Relación entre dispositivos, software recomendado e instalación real |
| `docs/system-paths.md` | Rutas de ROMs, BIOS, saves, states y media por CFW |

## Guías

| Carpeta | Propósito |
| --- | --- |
| `docs/guides/cfw/` | Guías de instalación paso a paso por CFW/OS |
| `docs/guides/apps/` | Guías de configuración de frontends y emuladores standalone Android |
| `docs/guides/romsets/` | Workflows de preparación de romsets (cartucho/plano, óptico→CHD, arcade) |
| `docs/hardware/` | Guías de referencia de hardware auxiliar (flashcarts, etc.) |

## Arcade y juegos

| Fichero | Propósito |
| --- | --- |
| `docs/arcade/` | Referencia de emulación arcade y colecciones Bartop Curated por sistema |
| `docs/handheld-stick.md` | Rendimiento de juegos exigentes en hardware limitado (RK3566) |

## Referencia

| Fichero | Propósito |
| --- | --- |
| `docs/references.md` | Referencia técnica de romsets, DATs y conceptos |
| `decisions/` | Decisiones de diseño del repositorio (ADRs) |
| `metadata/dat/` | DATs por fuente: No-Intro, Redump, Non-Redump, TOSEC, arcade, libretro, etc. |
| `metadata/dat-index/` | Índice JSON por sistema, generado a partir de `metadata/dat/` |
| `metadata/sources/` | DATs fuente sin procesar, previos a retool |
| `metadata/mame/` | DATs y XMLs internos de MAME |
| `metadata/software-list/` | Software lists XML de MAME |
| `data/dats/` | Romsets curados por sistema (fullset y 1G1R), generados con retool |
| `data/roms/` | Estructura final de ROMs lista para desplegar en dispositivos |

## Herramientas colaborativas

| Carpeta | Propósito |
| --- | --- |
| `prompts/` | Prompts reutilizables para curación y validación |
| `.claude/` | Configuración y skills para Claude Code |
| `tools/` | Scripts PowerShell de validación y mantenimiento (indexado de DATs, construcción de romsets) |
| `references/` | Fuentes auxiliares y documentación de soporte (carpeta reservada) |

---

## Prompts disponibles

| Prompt | Propósito |
| --- | --- |
| `prompts/arcade_games.md` | Curar una colección Bartop para un sistema dado |
| `prompts/device_research.md` | Investigar specs de hardware de un dispositivo para `devices.md` |
| `prompts/distribution_research.md` | Investigar recomendación de CFW/frontend de un dispositivo para `distributions.md` |
| `prompts/review-distributions.md` | Revisar y validar `distributions.md` |
| `prompts/validate-cross-references.md` | Validar consistencia entre documentos |
| `prompts/generate-system-paths.md` | Histórico: proceso original de diseño de `system-paths.md` |

---

## Estado

| Documento | Estado |
| --- | --- |
| `docs/devices.md` | Estable |
| `docs/systems.md` | Estable |
| `docs/romsets.md` | Estable |
| `docs/software.md` | Estable |
| `docs/tools.md` | Estable |
| `docs/distributions.md` | Estable |
| `docs/system-paths.md` | Activo |
| `docs/arcade/arcade.md` | Activo |
| `docs/handheld-stick.md` | Activo |
| `docs/references.md` | Activo |

---

## Instrucciones para Claude Code

Las reglas editoriales y el mapa completo de archivos están en `CLAUDE.md`.
