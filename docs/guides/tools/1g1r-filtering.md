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

**Flags principales confirmados:**

- `-l <idiomas>` — filtra por lista de idiomas; un título que no soporte ninguno de la lista se elimina.
- `-d` — desactiva el filtrado 1G1R (ignora las listas de clones y trata cada título como único); útil si se quiere conservar todo de una región/idioma concreto sin reducir a 1G1R.
- `--output <carpeta>` — carpeta de salida para el/los DAT 1G1R generado(s).
- `--regionsplit` — divide el resultado en varios DAT, uno por región.
- `--exclude` — exclusiones de tipos de título no deseados (demos, aplicaciones, etc. — complementario a la limpieza ya hecha en fase 4).

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

**Fuente:** github.com/andrebrait/DATROMTool. Sucesor moderno inspirado en SabreTools y retool; releva al antiguo proyecto `1g1r-romset-generator`.

**Capacidades confirmadas:**

- Parsing de DAT en formato Logiqx XML.
- Extracción de metadatos desde la convención de nombrado No-Intro (región, idioma, versión, estado de pre-lanzamiento) — ver `docs/references.md#no-intro`.
- Detección de inconsistencias en los datos de región/idioma extraídos.
- Conversión entre XML Logiqx, JSON y YAML.
- Matching de ROMs por hash (SHA-256, SHA-1, MD5) o por tamaño+CRC.
- Lectura/escritura de Zip, 7z, TAR (con GZip/BZip2/LZMA/XZ) y lectura de RAR (v4 y v5).

[TODO: no se ha podido confirmar la sintaxis exacta de línea de comandos ni los flags específicos de filtrado 1G1R (región/idioma/exclusiones) — el repositorio no expone esta información de forma directa en su página principal, consultar el `README`/`--help` de la herramienta al usarla]

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
