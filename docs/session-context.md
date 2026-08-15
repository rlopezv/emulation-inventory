# Contexto de sesión activo

Fichero versionado (viaja con git a cualquier entorno: Windows nativo, WSL, devcontainer) con el estado de trabajo pendiente entre sesiones.

Complementa dos cosas que **no** viajan igual:

- `CLAUDE.md` — reglas estables del proyecto, cambia poco.
- La memoria local de Claude Code (`~/.claude/projects/<id>/memory/`) — se deriva de la ruta absoluta del repo, así que es específica de cada entorno (Windows nativo, WSL, devcontainer cuentan como entornos distintos aunque sea el mismo repo) y no se copia entre ellos de forma fiable.

Este fichero es la capa que sí viaja: decisiones de diseño a medias, tareas pendientes concretas, o cualquier estado que deba sobrevivir a un cambio de máquina o entorno. Actualizarlo al cerrar una sesión con trabajo pendiente; limpiar la entrada cuando se resuelve.

## Pendiente ahora mismo

### Reestructuración de fuentes No-Intro (metadata/ crudo vs sources/ curado)

**Contexto:** `metadata/dat/No-Intro/` se reestructuró en tres packs reales de descarga: `pc/` (Parent-Clone), `full/` (Standard) y `aftermarket/`. Se creó `sources/dats/no-intro/` (raíz, gitignored) como copia de trabajo curada, sincronizada desde `metadata/` por `tools/scripts/update-sources.ps1` / `.py` (verificados con salida idéntica), a partir del manifiesto `tools/scripts/config/nointro-systems.json`.

**Hallazgo técnico:** el DAT Parent-Clone (`pc/`) usa un esquema de agrupación distinto al Standard (`full/`): `cloneof="<nombre del padre>"` por nombre, en vez de `id`/`cloneofid` numéricos. `build-dat-index-nointro.ps1` solo sabe interpretar el segundo esquema; por eso indexa desde `full/`, y `pc/` se sincroniza pero no se consume todavía.

**Diseño objetivo (no implementado):** los tres packs se combinan, no se elige uno:
- `full/` = fuente de los títulos NO aftermarket.
- `aftermarket/` = fuente de los títulos aftermarket.
- `pc/` = conjunto de referencia completo (oficiales + aftermarket, con relaciones de parentesco ya resueltas) — usado para **contrastar** que `full + aftermarket` no deja huecos de cobertura, no para sustituirlos.

**Siguiente paso pausado a propósito:** antes de escribir `build-dat-index-nointro.py` (puerto Python del indexado, siguiendo el patrón ya usado en `update-sources.py`), decidir bien cómo implementar esa combinación full+aftermarket+contraste-con-pc.

**Limpieza pendiente:** borrar a mano `tools/scripts/config/nointro-systems.psd1` (obsoleto, sustituido por el `.json`; no se pudo borrar por permisos de sesión en su momento).

**Rama de trabajo:** `nointro-sources-restructure` (creada desde `develop`, sin mergear todavía).

## Notas de entorno

- **Devcontainer** (`.devcontainer/`): Python 3.12 + Claude Code, pensado como alternativa al PowerShell nativo para el pipeline propio (`tools/scripts/`), no como sustituto — muchas herramientas de la scene catalogadas en `docs/tools.md` son Windows-only y se siguen usando en el host.
- **Credenciales del devcontainer:** vía `.devcontainer/.env` (gitignored, nunca versionado) con `CLAUDE_CODE_OAUTH_TOKEN` generado con `claude setup-token`. Si se abre el devcontainer en una máquina nueva, recrear ese `.env` a mano (mismo token u otro nuevo) — no viaja con git a propósito.
- **Rendimiento en Windows + Docker Desktop:** si el repo vive en el filesystem de Windows (`C:\Users\...`) y se abre en devcontainer, el bind-mount cruzado Windows↔WSL2 es notablemente más lento que si el repo vive directamente dentro del filesystem de WSL2. Al clonar en una máquina nueva, mejor clonar directamente dentro de WSL2 si se va a usar el devcontainer con frecuencia.
