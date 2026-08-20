# CLAUDE.md

## Project

This repository documents a personal multi-device emulation ecosystem covering handhelds, SBCs, tablets and bartops.

The goal is to maintain a useful knowledge base for:

- Deciding which CFW or frontend to use on each device.
- Selecting the best romsets per hardware.
- Tracking what is installed vs. recommended.
- Curating game collections optimized for bartop or handheld use.

This is a collaborative workspace designed to be used with Claude Code.

The documentation is written in Spanish and uses Markdown tables as the main format.

## File map

### Core documentation

| File | Purpose |
| --- | --- |
| `docs/devices.md` | Hardware inventory |
| `docs/systems.md` | Emulated systems catalog and canonical identifiers |
| `docs/romsets.md` | Romset-to-DAT association per system (source, format, alternate source, completeness, storage) |
| `docs/software.md` | CFW, OS, frontend and launcher catalog (device-installed software) |
| `docs/tools.md` | PC-side tool catalog for romset/DAT management (scraping, validation, conversion, patching) |
| `docs/distributions.md` | Device-to-software recommendation and installation audit |
| `docs/system-paths.md` | ROM, BIOS, saves, states and media paths by CFW |
| `docs/bios.md` | Required BIOS/firmware files per system: exact filename(s), mandatory/optional, emulator/core that needs it, special subfolder if any. Does not define where the `bios/` folder itself lives per CFW (see `docs/system-paths.md`) nor link to download sources |
| `docs/guides/cfw/` | Step-by-step installation guides per CFW/OS marked Recomendado/Verificado in distributions.md (see `docs/guides/cfw/README.md`) |
| `docs/guides/apps/` | Configuration guides for frontends (EmulationStation, SimpleMenu, ES-DE, Daijishō, Pegasus) and Android standalone emulators, running on top of an already-installed CFW/OS (see `docs/guides/apps/README.md`) |
| `docs/guides/romsets/` | Romset preparation workflows by source type: cartridge/flat, microcomputers, optical→CHD, arcade (see `docs/guides/romsets/README.md`) |
| `docs/guides/tools/` | Per-task usage guides (commands, parameters) for the tools catalogued in `docs/tools.md`: DAT generation/conversion, romset audit/cleaning, 1G1R filtering, patching, format conversion, gamelist and media generation. Each phase of `docs/guides/romsets/workflow.md` links here for detail (see `docs/guides/tools/README.md`) |
| `docs/guides/bios.md` | How-to guide for the catalog in `docs/bios.md`: dumping your own BIOS from real hardware, verifying it (hash), organizing/renaming it per system, and deploying it to the path defined in `docs/system-paths.md#bios` |
| `docs/hardware/` | Reference guides for supporting hardware (flashcarts, etc.) |

### Arcade and games

| File | Purpose |
| --- | --- |
| `docs/arcade/` | Arcade reference and Bartop Curated catalogs by system (see `docs/arcade/README.md`) |
| `docs/handheld-stick.md` | Performance ratings for demanding games on limited hardware (RK3566) |

### Reference and decisions

| File | Purpose |
| --- | --- |
| `docs/references.md` | Technical reference for romsets, DATs, tools and concepts |
| `docs/session-context.md` | Versioned, cross-environment record of pending/in-progress work (unlike local Claude Code memory, which is tied to the absolute repo path and doesn't transfer between Windows/WSL/devcontainer or machines) — update when closing a session with unfinished work |
| `decisions/` | Architecture decision records (ADRs) for the repository |
| `metadata/` | Raw archive of everything downloaded per source (`metadata/dat/<Fuente>/`: No-Intro, TOSEC, MAME, libretro, etc.), kept as-is regardless of what the pipeline actually uses; MAME DATs and software-list XMLs also live here |
| `metadata/dat-index/` | Per-system JSON index built from `sources/dats/` by `tools/scripts/build-dat-index-*.ps1` |
| `sources/` | Curated working copy of DATs actually used by the pipeline (only the systems/packs in use, no timestamp-dated duplicates), synced from `metadata/` by `tools/scripts/update-sources.ps1`; gitignored |
| `data/dats/` | Curated DATs per system, produced externally with retool: `fullset` (complete curated set) and `1g1r` (1G1R-filtered, with a `japan/` quarantine subfolder for region-excluded titles pending review); gitignored — working files regenerated from `sources/`, not a versioned source of truth |
| `data/roms/` | Final ROM folder structure staged for deployment to devices (gamelist.xml, media, per-system layout); gitignored — same reasoning as `data/dats/` |

### Collaborative tools

| Folder | Purpose |
| --- | --- |
| `prompts/` | Reusable prompts for curation and validation tasks |
| `.claude/` | Claude Code configuration and skills |
| `tools/` | Validation and maintenance scripts (PowerShell: DAT indexing, romset build, filtering — see `tools/scripts/README.md`) |
| `references/` | Auxiliary sources and support documentation |

## Source of truth

1. `docs/devices.md` is the source of truth for hardware.
2. `docs/systems.md` is the source of truth for emulated systems and canonical identifiers.
3. `docs/software.md` is the source of truth for software, CFW, OS, frontends and launchers.
3b. `docs/tools.md` is the source of truth for PC-side romset/DAT management tools.
4. `docs/arcade/arcade.md` is the source of truth for arcade cores, standalone emulators and arcade romset families.
5. `docs/distributions.md` must not redefine hardware, systems or software.
6. `docs/system-paths.md` must not redefine devices, systems or software.
7. `docs/romsets.md` must not redefine systems; canonical identifiers must always match `docs/systems.md`.

## Language

All documentation must be written in Spanish.

Use concise, technical Spanish.

## General editing rules

- Preserve existing Markdown table structure unless explicitly asked to change it.
- Do not invent data.
- Use `[TODO]` when data is unknown or unverified.
- Do not remove rows unless explicitly instructed.
- Do not silently rename canonical identifiers.
- Prefer consistency over completeness.
- Avoid adding external sources directly into final tables unless requested.
- Keep notes short and operational.
- **Ask and propose before making any edit.** Plan approval is not authorization to execute without pausing for confirmation.

## devices.md rules

`docs/devices.md` is an inventory of hardware.

Expected columns:

```markdown
| Marca | Modelo | Procesador | Memoria | Pantalla | Resolución | Aspect Ratio | Orientación | Año salida | Fiabilidad | SD | Imagen |
```

Rules:

- Fiabilidad means confidence in documented data, not hardware quality.
- Use `[TODO]` for unknown hardware data.
- Do not add software recommendations here.

## systems.md rules

`docs/systems.md` is a catalog of emulated systems.

Expected columns:

```markdown
| Nombre del sistema | Año | Identificador canónico | Nombres regionales/comerciales | Aspect Ratio | Resolución nativa típica | Orientación | Cores RetroArch habituales | Emuladores standalone habituales |
```

Rules:

- Use the most internationally recognized system name.
- Keep canonical identifiers stable.
- Do not mix frontend folder names with canonical identifiers unless explicitly requested.
- Romset information (source: No-Intro / Redump / Non-Redump / MAME / TOSEC, DAT format, DAT version, alternate source, completeness, storage location) is documented in `docs/romsets.md`, not in this file. Canonical identifiers used there must always match this file.

## romsets.md rules

`docs/romsets.md` associates each system from `docs/systems.md` with its DAT source(s) in `metadata/dat/`.

Expected columns per section (Consolas / Arcade / Microcomputers / Engines-Ports):

```markdown
| Identificador canónico | Fuente | Formato | DAT | Fuente alternativa | DAT alternativo | Completitud | Almacenamiento | Notas |
```

Normalized `Formato` values:

```text
XML (Logiqx)
XML (Logiqx, sin cloneofid)
XML (Logiqx, TOSEC)
ClrMamePro (texto)
```

Rules:

- Canonical identifiers must always match `docs/systems.md`; do not define new systems here.
- Do not redefine hardware, software, or distribution recommendations here.
- `Fuente alternativa` / `DAT alternativo` document a secondary source for the same system (e.g. Non-Redump for prototypes/betas when the primary source is Redump, or a software-list XML for CHD verification), not a competing primary recommendation.
- Exception: the Arcade section omits `Fuente alternativa` / `DAT alternativo` (alternate sources are rare there), and Engines/Ports uses a reduced header (`Identificador canónico | Fuente | Formato | DAT | Notas`, no `Fuente alternativa`, `DAT alternativo`, `Completitud` or `Almacenamiento`) since these systems rarely track storage/completeness the same way. Consolas and Microcomputers use the full column set shown above — alternate sources turned out not to be rare for Microcomputers (libretro-database covers several as a documented alternative alongside TOSEC).
- `tools/scripts/build-dat-index-nointro.ps1` (No-Intro/Non-Redump, with `cloneofid`), `tools/scripts/build-dat-index-redump.ps1` (Redump, no `cloneofid`) and `tools/scripts/build-dat-index-tosec.ps1` (TOSEC, no `cloneofid`, 2-letter region codes) read their per-system DAT mapping from hardcoded tables mirroring this file; update the relevant one(s) when this file's Fuente/DAT changes for a system already covered by those scripts.

## software.md rules

`docs/software.md` catalogs software installed *on a device* (CFW, OS Retro, Android CFW, Stock Mod, Frontend, Launcher). PC-side romset/DAT management tools belong in `docs/tools.md`, not here.

Expected main columns:

```markdown
| Nombre | Variante | Tipo | Familia | Frontend | Requiere gamelist | Media soportada | Página / repo | Plataforma principal | Dispositivos principales | Estado | Notas |
```

Normalized `Tipo` values:

```text
CFW
OS Retro
Android CFW
Stock Mod
Frontend
Launcher
Histórico
```

Normalized `Estado` values:

```text
Activo
Mantenimiento
Histórico
Descontinuado
Experimental
```

## tools.md rules

`docs/tools.md` catalogs PC-side tools for romset/DAT management: scraping, validation, conversion, dumping, patching. Not installed on any device from `docs/devices.md` — do not reference these rows from `distributions.md`.

Expected columns:

```markdown
| Nombre | Variante | Tipo | Categoría | Familia | Frontend | Requiere gamelist | Media soportada | Página / repo | Plataforma disponible | Dispositivos principales | Nivel de usuario requerido | Estado | Notas |
```

`Tipo` is always `Tool`. Normalized `Categoría` values:

```text
Configuración
Scraping
Validación
Gestión
Librerías
Volcado
Conversión
Ports
Servicios
Parcheo
```

Normalized `Nivel de usuario requerido` values:

```text
Básico
Intermedio
Avanzado
```

- **Básico** — GUI simple, sin configuración previa ni conocimiento del dominio para un uso correcto.
- **Intermedio** — GUI con configuración no trivial, o CLI sencilla con pocos flags.
- **Avanzado** — CLI con sintaxis/flags compleja, requiere compilar desde código fuente, o conocimiento técnico profundo del dominio (formatos, hashes, estructura interna) para usarla correctamente.

Normalized `Estado` values: same list as `software.md` rules.

## distributions.md rules

`docs/distributions.md` relates devices with recommended software and real installation status.

It must use a single main table.

Expected columns:

```markdown
| Dispositivo | Familia | Tipo | Software recomendado | Alternativas | Frontend recomendado | Instalación real | Frontend real | Estado instalación | Contenido recomendado | Estado recomendación | Notas |
```

Normalized `Tipo` values:

```text
CFW
OS Retro
OS Handheld
Android CFW
Stock Mod
Frontend
```

- **CFW** — firmware para un dispositivo o familia de hardware concreta (GarlicOS, muOS, MiyooCFW, Adam Image, MinUI, CrossMix-OS…)
- **OS Retro** — sistema operativo retro de propósito general para SBC o PC (Batocera, Recalbox, RetroPie, Lakka…)
- **OS Handheld** — sistema operativo retro de propósito general para múltiples handhelds (ROCKNIX, ArkOS, AmberELEC, KNULLI, The Retro Arena…)
- **Android CFW** — ROM Android personalizada orientada a emulación (GammaOS, 351Droid…)
- **Stock Mod** — modificación del firmware de fábrica sin reemplazarlo
- **Frontend** — aplicación de lanzador/interfaz sobre un OS existente (ES-DE, Daijishō, Pegasus…)

Rules:

- Every device present in `docs/devices.md` must have its own row, except generic family placeholders that do not represent a concrete model (e.g. `Genérico | TV Box S905 (Super Console X / Stick)`).
- `Familia` is used only for grouping and filtering.
- Do not replace concrete devices with family summaries.
- Real installation is an audit field.
- Real installation does not automatically replace the recommended software.
- Do not include `gamelist.xml` reuse as a column.
- Do not include task lists or executive summaries.
- Use `[TODO]` or `Desconocido` instead of inventing installation state.

Recommendation criteria, in order:

1. Technical compatibility with the device or hardware family.
2. Community recommendation, adoption and consensus.
3. Maturity, stability and maintenance.
4. Coherence with the documentation ecosystem.
5. Ease of maintaining a clear, documentable and migratable collection structure.
6. Operational simplicity.
7. Known explicit user preferences.

Normalized recommendation states:

```text
Recomendado
Válido
Alternativo
Legado
Experimental
No recomendado
[TODO]
```

Normalized installation states:

```text
Verificado
Pendiente
No instalado
Desconocido
No aplica
```

## arcade/ rules

`docs/arcade/arcade.md` is the reference for arcade emulation.

It contains:

- RetroArch cores with associated romset versions, recommended use and target hardware.
- Standalone emulators with associated romset versions and target hardware.
- Romset catalog table with checkbox availability tracking (`[ ]` not available, `[x]` available).

Rules:

- Do not duplicate core or emulator entries that are already in `docs/software.md`.
- The romset catalog checkboxes reflect the user's actual collection.
- Cores and emulators are organized by performance profile and target hardware.
- Core names used in `docs/distributions.md` must match entries in this file.
- Curated catalogs per system live in `docs/arcade/arcade-{system}.md` files. See `docs/arcade/README.md` for the full list.
- Use the `prompts/arcade_games.md` prompt when generating new curated catalogs.
- Curated catalog columns: `Juego | Género | Tier | Arcade | Rot | Ctrl | Players | Notas`
- Normalized values: Tier S/A/B, Arcade S/A, Rot H/V/HV, Ctrl 2B/3B/6B/LG/WHEEL, Players 1P–4P/4P+ (usar `4P+` cuando el juego admite más de 4 jugadores vía multitap; detallar el máximo real en Notas).

## handheld-stick.md rules

`docs/handheld-stick.md` documents game performance on hardware at or beyond its limits.

Current focus: RK3566 devices running ROCKNIX.

Rules:

- Organized by system.
- Include Stick class (A/B/C) and Perf rating (S/A/B/C) per game.
- Only include games that are at or above the expected capability threshold of the target hardware.

## system-paths.md rules

`docs/system-paths.md` documents ROM, BIOS, save, state, media and `gamelist.xml` locations by firmware/frontend.

This file is a CFW × system matrix: for each CFW, the expected paths for each file type.

Structure is defined (see the file's own conventions section). Extend it following the existing per-CFW table format.

## bios.md rules

`docs/bios.md` catalogs required BIOS/firmware files per system: which file(s), whether mandatory or optional, which emulator/core needs it, and any special subfolder convention. It documents *what* is needed, not *where* the `bios/` folder lives per CFW (that is `docs/system-paths.md`'s job) nor system/hardware definitions (`docs/systems.md`/`docs/arcade/arcade.md`).

Sections mirror `docs/romsets.md`: Consolas / Arcade / Microcomputers.

Expected columns (Consolas / Microcomputers):

```markdown
| Identificador canónico | Fichero(s) BIOS | Obligatoria/Opcional | Emulador/core que la requiere | Notas |
```

Rules:

- Canonical identifiers must always match `docs/systems.md` (Consolas/Microcomputers) or `docs/arcade/arcade.md` (Arcade); do not define new systems here.
- **Obligatoria** — the emulator does not boot without it. **Opcional** — HLE fallback exists (boots without it, worse compatibility) or only some titles need it.
- Arcade uses a different model: in MAME/FBNeo the BIOS is usually embedded in the romset itself as a parent/shared set (e.g. `neogeo.zip`), not a standalone file in `system/`. Document this per-family in prose, not as an exhaustive per-game table of every shared MAME BIOS set.
- Never link to a BIOS download source. BIOS is copyrighted firmware — the user must dump it from their own hardware or acquire it legally. `[TODO]` is fine when the exact filename/hash is unconfirmed.
- Exact filenames matter and are case-sensitive on some CFW/cores — do not normalize casing when transcribing (e.g. `kick34005.A500`, not `kick34005.a500`).

## Prompts

Reusable prompts are in `prompts/`. When a task matches one of these, apply its rules before generating output.

| Prompt | Purpose |
| --- | --- |
| `prompts/arcade_games.md` | Curate a Bartop Collection for a given system |
| `prompts/device_research.md` | Research a device's hardware specs and produce a `devices.md`-ready row |
| `prompts/distribution_research.md` | Research a device's recommended CFW/frontend and produce a `distributions.md`-ready row |
| `prompts/review-distributions.md` | Review and validate `distributions.md` |
| `prompts/validate-cross-references.md` | Validate cross-document consistency |
| `prompts/generate-system-paths.md` | Historical: original prompt to design `system-paths.md` structure, now already defined |

## Important known facts

- Steam Deck is out of scope because the user does not intend to use it.
- The user has a LaunchBox BigBox license.
- The user has installed GammaOS on the GKD Bubble.
- Koriki must remain visible as a relevant alternative where applicable, especially Miyoo Mini, Miyoo Mini Plus and RG35XX original.
- RG35XX original must not be treated as the same family case as modern H700 devices.

## Validation checklist

Before finishing any edit:

- Check that all Markdown tables remain valid.
- Check that every `docs/devices.md` device appears in `docs/distributions.md`.
- Check that software names used in `docs/distributions.md` exist in `docs/software.md`, unless marked `[TODO]` or explained.
- Check that system identifiers match `docs/systems.md`.
- Check that core names used in `docs/distributions.md` match `docs/arcade/arcade.md`.
- Check that identifiers used in `docs/romsets.md` match `docs/systems.md`.
- Check that identifiers used in `docs/bios.md` match `docs/systems.md`/`docs/arcade/arcade.md`.
- Check that `[TODO]` is used instead of guessed data.
- Check that no executive summary or task list is added to `docs/distributions.md`.
