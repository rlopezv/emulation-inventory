# Filtrado 1G1R

Generación del set 1G1R (una ROM por juego, según prioridad de región/idioma) a partir del DAT completo ya auditado (fase 3) y limpiado de categorías no deseadas (fase 4). No modifica el romset físico directamente — genera un **DAT curado** que luego se usa para filtrar/reconstruir el romset con la herramienta de auditoría de la fase 3.

Corresponde a la fase 5 de [docs/guides/romsets/workflow.md](../romsets/workflow.md).

**Relación con el pipeline propio:** retool produce los DAT curados en `data/dats/<sistema>/1g1r/` (incluyendo la cuarentena `japan/`); `build-dat-index-1g1r.ps1` (documentado en [docs/guides/romsets/custom-pipeline.md](../romsets/custom-pipeline.md)) indexa después ese DAT curado a `dat-index/<id>.json`. Esta guía cubre el uso de retool en sí.

## retool

**Fuente:** github.com/unexpectedpanda/retool, sitio de documentación en unexpectedpanda.github.io/retool.

**Estado: sin mantenimiento activo** — el propio repositorio lo indica explícitamente ("Retool is no longer maintained", ver issue #337), confirmado también desde el README de `retool-clonelists-metadata`. Sigue siendo funcional y es la herramienta de referencia de este repo. Ya reflejado en `docs/tools.md` (Estado: Mantenimiento).

**Requisitos:** Windows 10+, Ubuntu 20+ o macOS 15+; las versiones sin compilar (desde código fuente) requieren Python 3.10+.

**Uso básico confirmado:**

```bash
retool PATH_TO_DAT_FILE
```

Importa el DAT original (No-Intro o Redump), lo procesa y genera un DAT nuevo filtrado, **preservando el original intacto**. Ver todas las opciones disponibles:

```bash
retool.py -h
```

**Flags principales confirmados** (lista ampliada, cruzada contra la propia `--help` de retool tal como la documenta `fresh1g1r/config/*/filters.py` — ver `docs/dat-sources.md#fresh1g1r`, fuente de referencia real de uso en producción, no solo teórica):

- `-l <idiomas>` — filtra por lista de idiomas; un título que no soporte ninguno de la lista se elimina.
- `-d` — desactiva el filtrado 1G1R (ignora las listas de clones y trata cada título como único); útil si se quiere conservar todo de una región/idioma concreto sin reducir a 1G1R. No compatible con `--legacy`.
- `-c` — prioriza títulos con RetroAchievements (usa hashes de CHD/RVZ para imágenes de disco).
- `-n` — usa nombres locales si están disponibles (ej. caracteres japoneses en vez de romanizados).
- `-o` — prioriza versiones de producción más antiguas en vez de las más nuevas.
- `-r` — prioriza región sobre idioma (fuerza el orden de región estricto sin importar soporte de idioma).
- `-y` — prioriza versiones licenciadas frente a no licenciadas/aftermarket/homebrew.
- `-z` — prioriza títulos extraídos de relanzamientos modernos frente al lanzamiento original.
- `--compilations <i|k|o>` — tratamiento de recopilaciones: `i` prioriza siempre el título individual, `k` conserva ambos, `o` optimiza para menos duplicados.
- `--nooverrides` — desactiva los overrides globales y de sistema.
- `--output <carpeta>` — carpeta de salida para el/los DAT 1G1R generado(s). No compatible con `--replace`.
- `--regionsplit` — divide el resultado en varios DAT, uno por región. No compatible con `--legacy`.
- `--exclude <códigos>` — exclusiones de tipos de título no deseados, un código de letra por tipo (ver tabla abajo).
- `--labelmia` — marca los ficheros MIA con atributo `mia="yes"` (no usar si se es suscriptor de DATVault).
- `--labelretro` — marca títulos con RetroAchievements con atributo `retroachievements="yes"`.
- `--listnames` — genera además un `.txt` con solo los nombres de los títulos conservados.
- `--machine` — exporta cada título con la etiqueta `<machine>` (estándar MAME) en vez de `<game>`.
- `--originalheader` — usa las cabeceras del DAT de entrada original en el DAT de salida.
- `--replace` — sustituye el DAT de entrada por la versión de Retool. No compatible con `--output`.
- `--report` — genera además un informe de los títulos conservados, eliminados y marcados como clon.
- `--reprocess` — permite reprocesar DAT que Retool ya haya procesado antes.
- `--config <fichero>` — config de usuario alternativa a la de por defecto.
- `--clonelist <fichero>` — clonelist alternativa a la de por defecto.
- `--legacy` — exporta en formato Parent-Clone clásico. No compatible con `-d`.
- `--metadata <fichero>` / `--mia <fichero>` / `--ra <fichero>` — ficheros alternativos a los de por defecto.
- `--singlecpu` — desactiva el uso multiprocesador (fuerza un solo núcleo).
- `--trace <regex>` — traza un título a través del proceso de Retool, para depuración.
- `--warnings` / `--warningpause` — reporta avisos de clonelist durante el procesado; `--warningpause` además pausa al encontrar uno.

**Códigos de `--exclude`** (uno o varios concatenados, ej. `--exclude AaBbcdDefkmMopPruv`):

| Código | Excluye |
| --- | --- |
| `a` | Aplicaciones (categoría "Applications", o `(Program)`/`(Test Program)`/`Check Program`/`Sample Program` en el nombre) |
| `A` | Audio (categoría "Audio") |
| `b` | Volcados defectuosos (`[b]` en el nombre) |
| `B` | BIOS y otros chips (categoría "Console", o `[BIOS]`/`(Enhancement Chip)` en el nombre) |
| `c` | Coverdiscs (categoría "Coverdiscs") |
| `d` | Demos, kioscos y muestras (categoría "Demos", o texto de demo/kiosco/muestra en el nombre) |
| `D` | Add-ons (categoría "Add-Ons") |
| `e` | Educativos (categoría "Educational") |
| `f` | Corregidos (`[f]` en el nombre — volcados fijados/corregidos) |
| `k` | MIA (ROMs declaradas como missing in action en las clonelist o en el DAT) |
| `m` | Manuales (`(Manual)` en el nombre) |
| `M` | Multimedia (categoría "Multimedia") |
| `o` | Discos bonus (categoría "Bonus Discs") |
| `p` | Pirata (`(Pirate)` en el nombre) |
| `P` | Preproducción (categoría "Preproduction", o `(Alpha)`/`(Beta)`/`(Proto)` etc.) |
| `r` | Promocional (categoría "Promotional", o `(Promo)`/`EPK`/`Press Kit`) |
| `u` | No licenciados (`(Unl)`/`(Aftermarket)`/`(Pirate)` en el nombre) |
| `v` | Vídeo (categoría "Video") |

**Prioridad de región/idioma (2.x):** a diferencia de versiones antiguas (1.x), que seleccionaban el clon de mayor revisión dentro de la región de mayor prioridad sin más, la versión 2.0 tiene en cuenta también el idioma asociado a la región prioritaria — ejemplo documentado: con prioridad `USA > Europe`, si el título USA no tiene versión en inglés pero sí uno en Europe, puede seleccionar el de Europe por ser el que cumple el idioma esperado de la región prioritaria (inglés), no solo por posición en la lista de prioridad.

**Salida:** DAT compatible con RomVault, ClrMamePro e igir; evita duplicados y admite nombres localizados.

**Esquema de DAT aceptado — importante:** retool no interpreta el atributo `id`/`cloneofid` (esquema Standard de `full/`/`aftermarket/`); necesita el esquema Parent-Clone (`cloneof="<nombre del padre>"` por nombre completo, sin `id`, como `pc/`). Si se quiere alimentar a retool con un DAT propio en esquema Standard (ej. `full`+`aftermarket` fusionados, o cualquier otro sin pack Parent-Clone oficial), `tools/scripts/convert-cloneofid-to-parent-clone.ps1` convierte de un esquema a otro (fusionando varios ficheros de entrada, namespaceando `id` por origen) — ver `tools/scripts/README.md`.

### Mecanismo de las clonelist (confirmado en la documentación oficial)

**Selección automática:** retool identifica el DAT cargado leyendo las etiquetas `<name>`/`<url>` de su cabecera, y busca en la carpeta `clonelists/` (ver [dat-generation.md](dat-generation.md#redump)) un fichero cuyo nombre coincida con el sistema y el grupo de origen (ej. `Apple - Macintosh (Redump).json`) — de ahí que el nombre del fichero deba ser exacto, no orientativo.

**Estructura interna — array `variants`:** cuando retool no detecta automáticamente que varios títulos están relacionados (nombres muy distintos entre regiones, compilaciones, supersets), la clonelist permite agruparlos manualmente. El array `variants` permite:

- Agrupar títulos con nombres distintos bajo el mismo grupo.
- Mover títulos a un grupo distinto del que retool les asignaría por defecto.
- Agrupar supersets/compilaciones junto a los títulos individuales que contienen.
- Fijar prioridades explícitas para forzar qué título selecciona el 1G1R.
- Asignar categorías y nombres locales (idioma nativo).
- Marcar títulos para ignorar.
- Aplicar todo lo anterior de forma condicional mediante filtros por región, idioma, coincidencia de expresión regular contra el nombre completo, o el orden de región configurado por el usuario.

Detalle completo y guía de contribución en unexpectedpanda.github.io/retool (secciones "Create and edit clone lists" y "How Retool works").

### Otras carpetas del repositorio de metadatos

Copia local completa en `metadata/dat/retool/` (sustituye a la antigua `metadata/dat/clonelist/`, que solo tenía `clonelists/` y quedaba desactualizada). Además de `clonelists/` y `retroachievements/` (ver [dat-generation.md](dat-generation.md#redump)), `retool-clonelists-metadata` incluye:

- **`metadata/`** — metadatos generados automáticamente desde Redump y No-Intro; no editable a mano (para corregir un error hay que reportarlo a Redump/No-Intro directamente, no al repositorio).
- **`mias/`** — listas MIA ("Missing In Action": juegos confirmados que existieron pero de los que no hay volcado verificado todavía), obtenidas semanalmente de servidores externos.
- **`scripts/`** — herramientas de mantenimiento propias del repositorio (`clone_list_clean.py`, `clone_list_validate.py`, `get_mia.py`, `get_ra.py` + `clone-list-schema.json`), no el motor de Retool en sí.
- **`config/internal-config.json`** — configuración interna que usa retool [TODO: no presente en la copia local actual, confirmar si forma parte de este repositorio o de retool en sí].

## DATROMTool

**Fuente:** github.com/andrebrait/DATROMTool. Se declara a sí mismo sucesor de `1g1r-romset-generator` (mismo autor) — pero verificado: `1g1r-romset-generator` no está archivado y sigue recibiendo commits (último push 2026-02-05), no es un proyecto muerto sustituido del todo, ver sección propia más abajo.

**Capacidades confirmadas:**

- Parsing de DAT en formato Logiqx XML.
- Extracción de metadatos desde la convención de nombrado No-Intro (región, idioma, versión, estado de pre-lanzamiento) — ver `docs/references.md#no-intro`.
- Detección de inconsistencias en los datos de región/idioma extraídos.
- Conversión entre XML Logiqx, JSON y YAML.
- Matching de ROMs por hash (SHA-256, SHA-1, MD5) o por tamaño+CRC.
- Lectura/escritura de Zip, 7z, TAR (con GZip/BZip2/LZMA/XZ) y lectura de RAR (v4 y v5).

[TODO: no se ha podido confirmar la sintaxis exacta de línea de comandos ni los flags específicos de filtrado 1G1R (región/idioma/exclusiones) — el repositorio no expone esta información de forma directa en su página principal, consultar el `README`/`--help` de la herramienta al usarla]

## 1g1r-romset-generator

**Fuente:** github.com/andrebrait/1g1r-romset-generator. Predecesor declarado de DATROMTool (mismo autor) pero **activo por derecho propio** — verificado: no archivado, último push 2026-02-05. Utilidad de un solo fichero Python 3, sin dependencias externas.

**Capacidades confirmadas:**

- Genera sets 1G1R a partir de DAT No-Intro.
- Filtro de región: `-r USA,EUR,JPN` (códigos de 3 letras, más de 20 soportados).
- Filtro de idioma: `-l en,es,ru` (ISO 639-1), como criterio secundario tras la región.
- Exclusión por tipo: BIOS, prototipos, betas, demos, muestras, piratas, homebrew, ROM sin licencia.
- Sistema de puntuación que prioriza calidad del dump, lanzamientos publicados (no proto/beta), coincidencia región/idioma y preferencia de revisión.
- Salida: copia, mueve, o crea enlaces simbólicos/hardlinks del resultado 1G1R.

Alternativa más ligera a DATROMTool cuando no hace falta el resto de capacidades de este (conversión de formatos, parsing multi-fuente) — solo generación 1G1R sobre No-Intro.

## Igir

**Fuente:** igir.io, github.com/emmercm/igir. CLI en JavaScript/Node.js, sin instalación previa (`npx igir@latest`); alternativa moderna a retool para entornos de automatización (scripts, Docker, NAS).

**Capacidades confirmadas:**

- Agnóstico de fuente de DAT — soporta No-Intro, Redump, TOSEC y MAME (incluye reconstrucción de un set MAME a la versión exacta indicada, `--dat "MAME 0.258.dat"`).
- Filtrado 1G1R con prioridades configurables por línea de comandos: `--prefer-region`, `--prefer-language`, `--prefer-verified`, `--prefer-good`, `--prefer-parent`.
- Gestiona tanto ROMs planas como imágenes de disco pesadas (`.iso`, `.chd`, `.cue`) — extrae, renombra y mueve.
- También cubre detección de cabeceras headered/headerless (ver `docs/references.md#caso-especial--headered-vs-headerless-nes-snes-atari-7800-atari-lynx-fds`), relevante si el 1G1R se aplica sobre un romset con esa variante.

**Ejemplo de comando confirmado:**

```bash
igir copy --dat "*.dat" --input "**/*.zip" --output 1G1R --dir-dat-name --single --prefer-language EN --prefer-region USA,WORLD,EUR,JPN
```

## Scripts propios (sin herramienta de terceros)

Alternativa de control total: parsear directamente el DAT Logiqx XML (o el `dat-index/<id>.json` ya generado por el pipeline propio, ver [custom-pipeline.md](../romsets/custom-pipeline.md)) y aplicar la lógica de región/idioma a mano, cruzando contra `metadata/dat/retool/clonelists/*.json` cuando el sistema no tenga `cloneofid` nativo (caso Redump). Útil cuando ninguna herramienta de terceros cubre bien un sistema concreto, a costa de mantener la lógica de filtrado propia. Fuente confirmada de esos ficheros de clonelist: github.com/unexpectedpanda/retool-clonelists-metadata (ver detalle en [dat-generation.md](dat-generation.md#redump)) — es el mismo repositorio que alimenta a retool, así que reutilizarlo aquí mantiene la lógica de agrupado consistente entre ambos métodos.

[TODO: no existe ninguna herramienta de terceros consolidada llamada "PyRomVault" — verificado que no aparece en ninguna búsqueda; si se busca algo ya hecho en Python en vez de script propio desde cero, existen proyectos como `romlm` (pack/unpack/sort/dedupe) o `pyrsc` (Python ROMs Set Cleaner, quita clones/bootlegs), sin confirmar si cubren 1G1R con la misma profundidad que retool/Igir]

## Notas

El DAT 1G1R generado en esta fase no sustituye al DAT completo obtenido en la fase 1 — se conservan ambos: el completo para poder recuperar cualquier título descartado más adelante, y el 1G1R como el que realmente se usa para filtrar/reconstruir el romset de despliegue.

Ver `docs/references.md#1g1r` para los conceptos de reglas regionales, exclusiones y la cuarentena de exclusivos regionales (`japan/`) que aplica este repo cuando 1G1R descarta un título que solo existe en una región no prioritaria.
