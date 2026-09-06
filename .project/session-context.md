# Contexto de sesión activo

Fichero versionado (viaja con git a cualquier entorno: Windows nativo, WSL, devcontainer) con el estado de trabajo pendiente entre sesiones. Es nuestro estado de trabajo interno — no se referencia desde `docs/` ni desde ningún otro documento del proyecto.

Complementa dos cosas que **no** viajan igual:

- `CLAUDE.md` — reglas estables del proyecto, cambia poco.
- La memoria local de Claude Code (`~/.claude/projects/<id>/memory/`) — se deriva de la ruta absoluta del repo, así que es específica de cada entorno y no se copia entre ellos de forma fiable.

Actualizar al cerrar una sesión con trabajo pendiente; **limpiar la entrada cuando se resuelve** — este fichero es una lista de tareas abiertas, no un changelog de lo ya hecho (eso ya vive en `docs/` como fuente de verdad, o en el historial de git).

## Pendiente ahora mismo

1. **Repoblar `sources/dats/redump/`** — sin mecanismo de sincronización (`update-sources.ps1` no cubre Redump). 15 sistemas Redump perdieron su romset curado tras un reseteo de `sources/`. Decidir: repoblar a mano desde `metadata/dat/Redump/`, o crear un script análogo a `update-sources.ps1` para Redump.
2. **`psp` sin mapear en `build-dat-index-redump.ps1`** — el DAT real ya está localizado (`Sony - PlayStation Portable - Datfile (3500)...dat`), falta añadirlo al indexador.
3. **Extender `build-dat-index-tosec.ps1`** a los 17 sistemas TOSEC de microcomputers (hoy solo mapea `gx4000`) — necesita soporte de array de DAT para fusionar los 12 sub-DAT de género de `c64 [D64]`.
4. **Extender `build-dat-index-nointro.ps1`** para `c64`/`msx`/`msx2` como fuente primaria (antes no mapeados porque la fuente primaria no era No-Intro).
5. **Indexador nuevo para WHDLoad** (`amiga`) — mismo formato ClrMamePro que libretro, pero esquema de campos distinto (sin convención región/idioma tipo No-Intro/TOSEC).
5b. **Revisar `docs/romsets.md` tras curar los 17 sistemas con scaffold pendiente** (`coleco`, `arcadia2001`, `ndsi`, `c128`, `plus4`, `spectrum`, `zx81`, `amstradcpc`, `atarist`, `sharpx68000`, `dragon32`, `vic20`, `atari800`, `thomson`, `amiga`) — la columna `Fuente` de esa tabla documenta la fuente cruda (TOSEC/No-Intro/WHDLoad); una vez generado el DAT curado (1G1R/retool) para cada uno, comprobar si esa columna sigue reflejando la fuente real usada por el pipeline (ver precedente en `astrocade`: la `Fuente` del índice generado pasó de `1G1R (retool)` a `No-Intro`).
6. **Rama `nointro-sources-restructure`** creada desde `develop`, sin mergear todavía.
7. **Matching por nombre de colecciones reales vs. `dat-index`** — en curso, acumulando datos empíricos (varios sistemas ya probados). Decisión pendiente del algoritmo final: normalizar nombre, matching por hash real vía MAMERedump, o combinación de ambos. A petición del usuario, seguir acumulando datos antes de diseñarlo.
8. **1G1R real de TOSEC** (agrupar variantes regionales, no solo excluir demos/protos/bad dumps) — TOSEC no tiene clonelist ni `cloneof` nativo. Pista sin explorar: ZX-Pokemaster (matching por hash MD5 contra una base tipo ZXDB), sin confirmar si existe equivalente de esa base de hashes para otros microcomputers.
9. **Filtrado por placa/categoría en arcade** (`docs/guides/romsets/workflow.md`, fase de procesado de DAT) — dato ya disponible (`catver.ini` de `antopisa-mame-supportfiles`), nada implementado todavía.
10. **`sistema_index.yaml`** se regenera a mano (`dat-processing reindex`), sin hook automático al tocar una YAML de `dat_sources`.
11. **`rahashes.yaml` sin resolver por sistema** — 5 patrones de ruta sin convención de nombres propia; aparcado a propósito (fichero auxiliar, no prioritario).
12. **Fragmentación residual del 1G1R de Igir en TOSEC** — diagnóstico ya hecho (`tools/scripts/tosec-nonstandard-labels.py`, detecta etiquetas de escena no oficiales por sistema). Falta decidir el mecanismo real de limpieza antes de la pasada de Igir.
13. **Igir**: pasar `--report-output` explícito la próxima vez (el CSV de `igir report` no se localizó en la última prueba); `igir dir2dat` sobre un 1G1R real sin probar todavía.
14. **`docs/bios.md`**: puntos "no verificado" pendientes de confirmar en fuente primaria — nombre exacto de la System Card de `pcenginecd`, hito de integración de `triforce` en Dolphin (si sigue aplicando). Normalizador de packs BIOS comunitarios (idea de tooling, no implementada). Decisión pendiente: añadir columna de hash MD5/SHA1 a `bios.md` para un futuro normalizador.
15. **Artefactos de prueba** en `private/retool-pipeline-test/` (no versionado) — libres de borrar si no hace falta conservarlos.

## Decisiones ya cerradas (no reinvestigar)

- **Fuentes de idioma/región descartadas**: LaunchBox.Metadata.db (sin campo `Language`, solo `Region` en alternate titles, sin clave de cruce fiable); API de RetroAchievements (ningún endpoint expone región/idioma).
- **Default de idioma para región `Asia`**: evaluado y rechazado — la detección de caracteres Han es inviable (catálogo No-Intro es 100% ASCII) y el default reducido (`Asia`+`Pirate/Unl/Bootleg`→`En`) tiene ~26% de error esperado.
- **Herramientas de DAT→DAT genérico evaluadas para TOSEC/MAME**: Igir descartado (opera sobre ROMs físicas, no genera DAT filtrado); DATROMTool sin releases publicadas; RomCenter solo Windows sin CLI multiplataforma. Flujo confirmado: SabreTools (`--dfd`) para generar DAT fresco + `retool --clonelist` propio.
- **Retool — regla operativa permanente**: en "Global settings → Regions", mover siempre todas las "Available regions" a la lista ordenada (ninguna en el panel izquierdo) — una región fuera de la lista no se excluye ni va al fondo, puede ganar a una región sí ordenada y esconder un título base conocido dentro de una recopilación multijuego.
- **Retool depende del atributo XML `<release language="...">`, no del nombre del título**, para el filtro de idioma — y del `<url>` de la cabecera del DAT para localizar el clonelist correcto.

## Notas de entorno

- **Devcontainer** (`.devcontainer/`): Python 3.12 + Claude Code, alternativa al PowerShell nativo para el pipeline propio (`tools/scripts/`), no sustituto — varias herramientas de la scene catalogadas en `docs/tools.md` son Windows-only y se siguen usando en el host. Build propio (`.devcontainer/Dockerfile`) con `retool`+`SabreTools` ya instalados.
- **Credenciales del devcontainer:** vía `.devcontainer/.env` (gitignored, nunca versionado) con `CLAUDE_CODE_OAUTH_TOKEN` generado con `claude setup-token`. Si se abre el devcontainer en una máquina nueva, recrear ese `.env` a mano — no viaja con git a propósito.
- **Rendimiento en Windows + Docker Desktop:** si el repo vive en el filesystem de Windows (`C:\Users\...`) y se abre en devcontainer, el bind-mount cruzado Windows↔WSL2 es notablemente más lento que si el repo vive directamente dentro del filesystem de WSL2. Al clonar en una máquina nueva, mejor clonar directamente dentro de WSL2 si se va a usar el devcontainer con frecuencia.
