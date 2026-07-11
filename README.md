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
| `docs/software.md` | Catálogo de CFW, OS retro, frontends, launchers y herramientas |
| `docs/distributions.md` | Relación entre dispositivos, software recomendado e instalación real |
| `docs/system-paths.md` | Rutas de ROMs, BIOS, saves, states y media por CFW (pendiente) |

## Arcade y juegos

| Fichero | Propósito |
| --- | --- |
| `docs/arcade/` | Referencia de emulación arcade y colecciones Bartop Curated por sistema |
| `docs/handheld-stick.md` | Rendimiento de juegos exigentes en hardware limitado (RK3566) |

## Referencia

| Fichero | Propósito |
| --- | --- |
| `docs/references.md` | Referencia técnica de romsets, DATs, herramientas y conceptos |
| `decisions/` | Decisiones de diseño del repositorio (ADRs) |
| `metadata/dat/arcade/` | DATs de FinalBurn Neo y MAME (2000–2016) |
| `metadata/dat/No-Intro/` | DATs de No-Intro por sistema |
| `metadata/dat/Non-Redump/` | DATs de Non-Redump por sistema |
| `metadata/dat/libretro/` | DATs de libretro-database |
| `metadata/mame/` | DATs y XMLs internos de MAME |
| `metadata/software-list/` | Software lists XML de MAME |

## Herramientas colaborativas

| Carpeta | Propósito |
| --- | --- |
| `prompts/` | Prompts reutilizables para curación y validación |
| `.claude/` | Configuración y skills para Claude Code |
| `tools/` | Scripts de validación y mantenimiento (pendiente) |
| `references/` | Fuentes auxiliares y documentación de soporte |

---

## Prompts disponibles

| Prompt | Propósito |
| --- | --- |
| `prompts/arcade_games.md` | Curar una colección Bartop para un sistema dado |
| `prompts/review-distributions.md` | Revisar y validar `distributions.md` |
| `prompts/validate-cross-references.md` | Validar consistencia entre documentos |
| `prompts/generate-system-paths.md` | Generación futura de `system-paths.md` |

---

## Estado

| Documento | Estado |
| --- | --- |
| `docs/devices.md` | Estable |
| `docs/systems.md` | Estable |
| `docs/software.md` | Estable |
| `docs/distributions.md` | Estable |
| `docs/arcade/arcade.md` | Activo |
| `docs/games.md` | Activo |
| `docs/handheld-stick.md` | Activo |
| `docs/references.md` | Activo |
| `docs/system-paths.md` | Pendiente de definición |

---

## Instrucciones para Claude Code

Las reglas editoriales y el mapa completo de archivos están en `CLAUDE.md`.
