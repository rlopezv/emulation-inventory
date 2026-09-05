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

- `-l` — filtra por idiomas. **Corregido tras verificación real (retool 2.4.9 CLI): no lleva lista inline** (`-l es,en,ja` no es sintaxis válida) — es un flag booleano; los idiomas a aceptar se activan descomentándolos en `config/user-config.yaml`, sección `language order:` (ej. `- English`, `- Spanish`, `- Japanese`). Un título que no soporte ninguno de los idiomas activos se elimina.
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
- `--report` — genera además un informe **de texto** (`.txt`) de los títulos conservados, eliminados y marcados como clon — no es un DAT reutilizable, solo lectura humana.
- `--removesdat` — **confirmado por verificación real**: genera además un DAT propio (`(Removed titles) (<N>).dat`, formato idéntico al DAT principal) con los títulos que esta pasada concreta eliminó — es el mecanismo real para obtener un DAT de "descartados" reutilizable (ej. una cuarentena de idioma), no `--report`.
- `--reprocess` — permite reprocesar DAT que Retool ya haya procesado antes.
- `--config <fichero>` — config de usuario alternativa a la de por defecto.
- `--clonelist <fichero>` — clonelist alternativa a la de por defecto.
- `--legacy` — exporta en formato Parent-Clone clásico. No compatible con `-d`.
- `--metadata <fichero>` / `--mia <fichero>` / `--ra <fichero>` — ficheros alternativos a los de por defecto.
- `--singlecpu` — desactiva el uso multiprocesador (fuerza un solo núcleo).
- `--trace <regex>` — traza un título a través del proceso de Retool, para depuración.
- `--warnings` / `--warningpause` — reporta avisos de clonelist durante el procesado; `--warningpause` además pausa al encontrar uno.

**Códigos de `--exclude`** (uno o varios concatenados, ej. `--exclude aAbBDemMov`). **Tabla corregida contra la salida real de `retool --help` (2.4.9)** — dos códigos estaban mal documentados en una versión anterior de esta tabla (`f` y `u`, ver nota):

| Código | Excluye |
| --- | --- |
| `a` | Aplicaciones (categoría "Applications", o `(Program)`/`(Test Program)`/`Check Program`/`Sample Program` en el nombre) |
| `A` | Audio (categoría "Audio", puede incluir bandas sonoras de juegos) |
| `b` | Volcados defectuosos (`[b]` en el nombre) |
| `B` | BIOS y otros chips (categoría "Console", o `[BIOS]`/`(Enhancement Chip)` en el nombre) |
| `c` | Coverdiscs (discos de portada de revista) |
| `d` | Demos, kioscos y muestras (categoría "Demos", o texto de demo/kiosco/muestra en el nombre) |
| `D` | Add-ons (expansiones y material adicional) |
| `e` | Educativos (categoría "Educational") |
| `f` | **Aftermarket** (juegos homebrew/no licenciados publicados tras el fin de vida oficial de la plataforma) — corregido, no es "corregidos"/fixed dumps como decía una versión anterior de esta tabla |
| `g` | Juegos (`Games`) — permite excluir el propio contenido "juego" cuando se quiere quedar solo con auxiliares (BIOS, aplicaciones...), caso de uso poco habitual en este pipeline |
| `k` | Títulos con ROM MIA (missing in action, declarados en la clonelist o el DAT) |
| `m` | Manuales (`(Manual)` en el nombre) |
| `M` | Multimedia (categoría "Multimedia", puede incluir juegos) |
| `o` | Discos bonus (categoría "Bonus Discs") |
| `p` | Pirata (`(Pirate)` en el nombre) |
| `P` | Preproducción (alfas, betas, prototipos) |
| `r` | Promocional |
| `u` | **Solo "Unlicensed" (`(Unl)`)** — corregido: no cubre Aftermarket (código `f` propio) ni Pirata (código `p` propio) pese a lo que decía una versión anterior de esta tabla |
| `v` | Vídeo (categoría "Video") |

**Prioridad de región/idioma (2.x):** a diferencia de versiones antiguas (1.x), que seleccionaban el clon de mayor revisión dentro de la región de mayor prioridad sin más, la versión 2.0 tiene en cuenta también el idioma asociado a la región prioritaria — ejemplo documentado: con prioridad `USA > Europe`, si el título USA no tiene versión en inglés pero sí uno en Europe, puede seleccionar el de Europe por ser el que cumple el idioma esperado de la región prioritaria (inglés), no solo por posición en la lista de prioridad.

**Salida:** DAT compatible con RomVault, ClrMamePro e igir; evita duplicados y admite nombres localizados.

**Esquema de DAT aceptado — importante:** retool no interpreta el atributo `id`/`cloneofid` (esquema Standard de `full/`/`aftermarket/`); necesita el esquema Parent-Clone (`cloneof="<nombre del padre>"` por nombre completo, sin `id`, como `pc/`). Si se quiere alimentar a retool con un DAT propio en esquema Standard (ej. `full`+`aftermarket` fusionados, o cualquier otro sin pack Parent-Clone oficial), `tools/scripts/convert-cloneofid-to-parent-clone.ps1` convierte de un esquema a otro (fusionando varios ficheros de entrada, namespaceando `id` por origen) — ver `tools/scripts/README.md`.

### Pipeline recomendado — varias pasadas encadenadas con `--reprocess`

`--reprocess` permite dar a retool, como entrada, un DAT que el propio retool ya ha generado antes — esto habilita encadenar pasadas sucesivas en vez de intentar resolver categorías, región/compilaciones e idioma en una única ejecución.

**Automatizado en `tools/scripts/retool-1g1r-pipeline.py`** — ejecuta los 4 pasos de abajo con una sola invocación (ver la cabecera del script y `tools/scripts/README.md#filtrado-1g1r-retool` para configuración/parámetros exactos). Descripción del flujo, para quien quiera ejecutarlo a mano o entender qué hace el script:

**Entrada — importante, corregido tras una verificación previa contaminada:** el DAT de entrada es el **Parent-Clone oficial de DAT-o-MATIC tal cual** (ej. `sources/no-intro/<Sistema> (Parent-Clone) (*).dat`), **sin pasar por ningún conversor propio**. Un intento anterior de esta guía usaba `tools/scripts/convert-cloneofid-to-parent-clone.py` para inyectar `<release region=... language=.../>` antes de dársela a retool, asumiendo que retool necesitaba ese atributo — **falso, confirmado leyendo el código fuente de retool** (`modules/dat/process_dat.py`): región e idioma se derivan exclusivamente del **nombre del título** (`TitleTools.regions()`/`languages_title`, vía `self.full_name`) más, si existe, un metadata JSON propio de retool indexado por nombre exacto (`languages_online`, ver más abajo) — el atributo `<release language="...">` que inyectaba el conversor **no lo lee nadie** en el código real. La única conversión estructural real que sigue haciendo falta (y que ya trae hecha el pack `Parent-Clone` oficial) es `cloneof` por nombre en vez de `id`/`cloneofid` numérico.

**Metadata/clonelist propios de retool — usar la copia local, no dejar que el contenedor los descargue:** retool resuelve `clonelists/`, `metadata/`, `mias/` y `retroachievements/` como carpetas relativas a su propia instalación (`/opt/retool/<carpeta>` en el devcontainer). Si estas carpetas no existen, retool las descarga interactivamente (620 ficheros, ~90s) de `unexpectedpanda/retool-clonelists-metadata` — para evitarlo y para que el resultado sea reproducible, montar la copia local ya clonada como volumen de solo lectura en esas 4 rutas en vez de dejar que el contenedor descargue la suya. La copia curada de nivel superior en `sources/retool-clonelists-metadata/` **no cubre todos los sistemas todavía** (ej. Mega Drive falta ahí) — usar `sources/retool-clonelists-metadata/input/` (el clon git completo) hasta que la curación esté más avanzada.

Pasos (**verificados end-to-end en el devcontainer**, retool 2.4.9 real, sobre `megadrive`, DAT oficial sin modificar + clonelist/metadata local montada, sin red):

1. **Parent-Clone oficial → `FULLSET`** (solo catálogo oficial, sin 1G1R todavía): `-d --exclude aAbBcDdefmMopPruv` — excluye aplicaciones/audio/bad dumps/BIOS/coverdiscs/add-ons/demos/educativos/**aftermarket (`f`)**/manuales/multimedia/bonus discs/**pirata (`p`)**/**preproducción — alfas, betas, prototipos (`P`)**/promocional/**no licenciado (`u`)**/vídeo. **Verificado:** 3498 → 1757 títulos (398 aftermarket, 133 unlicensed, 870 preproducción, 205 demos, 66 pirata, 35 apps, 31 BIOS, 3 bad dumps eliminados).
2. **`FULLSET` → `1G1R-BASE`** (1G1R por región, sin tocar idioma): `--reprocess --compilations k`, sin `-l` todavía. La lista de regiones (`config/user-config.yaml`, `region order:`) **ya viene completa por defecto en la CLI 2.4.9** (todas las regiones conocidas listadas, `Unknown` incluida al final) — no hace falta tocarla a mano como sí hacía falta en la GUI de sesiones anteriores; si se usa un `--config` propio, mantener esa cobertura completa es igualmente obligatorio. **Verificado:** 1757 → 1002 títulos, y los 9 títulos que en sesiones anteriores desaparecían por el bug de regiones incompletas (Golden Axe, Columns, Streets of Rage, ToeJam & Earl, Sonic & Knuckles, Super Hang-On, Revenge of Shinobi, Shadow Dancer, Super Volleyball) sobreviven como individuales — comprobado por nombre en el DAT de salida. (`World Cup Italia '90` sí "desaparece" de esta lista, pero no es un bug: el clonelist lo agrupa correctamente como retitulado regional de `World Championship Soccer`, misma familia.)
3. **`1G1R-BASE` → `1G1R-INTERMEDIATE`** (recorte al superconjunto de idiomas de interés): `--reprocess -l`, con `English`/`Spanish`/`Spanish (Latin American)`/`Spanish (Mexican)`/`Japanese` descomentados en `language order:` (y el resto de idiomas, como alemán, dejados comentados = fuera desde ya, sin cuarentena). **Verificado:** 1002 → 965 títulos.
4. **`1G1R-INTERMEDIATE` → `1G1R-FULL` + cuarentena** (separar japonés): `--reprocess -l --removesdat`, esta vez recomentando `Japanese` en `language order:` (dejando solo English/Spanish activos). **Verificado:** **836 conservados** (`1G1R-FULL`) + **129 en el DAT de descartes** generado por `--removesdat` (`(Removed titles) (129) (-l).dat`), confirmado por contenido: solo títulos `(Japan)` (`16t`, `A Ressha de Ikou MD`, `Aa Harimanada`...).

**Aftermarket aparte:** mismo pipeline (pasos 1-2, y 3-4 si también interesa cuarentenar algún idioma dentro del aftermarket) partiendo únicamente del subconjunto aftermarket del Parent-Clone (`--exclude` sin `f`, filtrando lo demás) — nunca mezclado con el catálogo oficial en la misma pasada.

**Notas operativas de ejecución no interactiva (CLI en devcontainer/CI):** con la copia local de clonelist/metadata montada (ver arriba), retool no pregunta por ellos; la única descarga que puede seguir pidiendo es `config/internal-config.json` la primera vez que se usa una carpeta de `config/` nueva (fichero pequeño, propio de retool, no relacionado con clonelist/metadata) — hay que encauzar `echo y |` delante del comando o el proceso muere con `EOFError`. Además, la primera invocación de retool en una carpeta de `config/` nueva **solo hace ese bootstrap** (crea `config/user-config.yaml` y sale sin procesar el DAT aunque se le pida) — hay que volver a invocarlo una segunda vez para que procese de verdad; `retool-1g1r-pipeline.py` ya maneja este reintento automáticamente. Para no repetir el bootstrap en absoluto entre ejecuciones futuras, montar `config/` de retool como volumen persistente propio (`--retool-config-dir` en el script, o `-v .../retool-config:/opt/retool/config` a mano) en vez de dejar que cada contenedor efímero lo regenere desde cero.

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

**Capacidades confirmadas (contra el `--help` real del script, no solo el README — el README tiene huecos sobre comportamiento por defecto y formato de entrada):**

- Genera sets 1G1R a partir de un DAT (No-Intro u otro Logiqx) + una carpeta de ROMs reales (`-i`), emparejando por escaneo de hash (por defecto) o solo por nombre de fichero (`--no-scan`, requiere `-e/--extension` para saber qué extensión asumir).
- Filtro de región: `-r USA,EUR,JPN` (lista separada por comas). Idioma (`-l en,es,ru`) es **criterio secundario de prioridad, no un filtro** — no descarta por idioma salvo que se añada `--only-selected-lang`. `--all-regions`/`--all-regions-with-lang` permiten aceptar una región no listada si la preferida no está disponible.
- Exclusión por tipo, un flag por categoría: `--no-bios`, `--no-program`, `--no-enhancement-chip`, `--no-proto`, `--no-beta`, `--no-demo`, `--no-sample`, `--no-pirate`, `--no-aftermarket`, `--no-homebrew`, `--no-promo`, `--no-unlicensed`; `--no-all` aplica todos los anteriores **excepto** `--no-unlicensed` (hay que añadirlo aparte si se quiere excluir también lo no licenciado).
- Sistema de puntuación configurable: `-w/--language-weight` (peso de idioma frente a región, por defecto 3), `--prioritize-languages`, `--early-revisions`/`--early-versions`, `--prefer-parents`, `--prefer-prereleases`, y listas `--prefer`/`--avoid`/`--exclude`/`--exclude-after` por palabra o fichero de texto (`file:ruta.txt`).
- **`--input-order`** — prioriza los títulos por el orden en que aparecen en el DAT, ignorando región/idioma/revisión. Es la opción relevante para encadenar con retool (ver flujo completo abajo): **no existe un flag para desactivar el 1G1R en sí** (va integrado en el sistema de puntuación), pero si el DAT de entrada ya viene reducido a un título por familia (como el 1G1R-FULL de retool), no hay nada que puntuar — `--input-order` se limita a coger ese único candidato.
- Salida (`-o`): copia (por defecto), `--move`, `--symlink`/`--hardlink` (`--relative` para symlinks relativos), `--group-by-first-letter` para organizar en subcarpetas.
- `--header-file`/carpeta `headers/` para reconocer ROMs headered al escanear (ver `docs/references.md#caso-especial--headered-vs-headerless-nes-snes-atari-7800-atari-lynx-fds`).
- **Sin confirmar todavía** (ni `--help` ni el README lo aclaran): si acepta ROMs en `.zip` o solo sin comprimir, y si `-i` admite subcarpetas o debe ser una carpeta plana — probar con una muestra pequeña antes de confiar en ello para una colección real.

### Flujo completo: de DAT completo a romset físico organizado

Encadenando `retool-1g1r-pipeline.py` (decide **qué** título gana por familia — región, idioma, compilaciones, clonelist) con `1g1r-romset-generator` (empareja esa decisión contra **ficheros reales** y los organiza en disco):

1. **`tools/scripts/retool-1g1r-pipeline.py`** sobre el DAT Parent-Clone/Redump oficial → produce el DAT `1G1R-FULL` (y opcionalmente la cuarentena de idioma) — ver sección de arriba.
2. **`1g1r-romset-generator`** usando ese `1G1R-FULL` como `-d`, con `--input-order` (no hay nada que puntuar, retool ya decidió) y `-i`/`-o` apuntando a tu colección real:

   ```bash
   python3 generate.py \
     -d "<1G1R-FULL generado por retool>" \
     -i <carpeta con la colección completa, sin filtrar> \
     -o <carpeta de salida 1G1R> \
     --input-order \
     --move
   ```

   No hace falta repetir ningún `--no-*`: el DAT que produce el paso 1 de retool ya viene sin BIOS/protos/betas/demos/aftermarket/pirata/unlicensed, así que no hay nada de eso que `1g1r-romset-generator` tenga que volver a excluir.
3. Repetir el paso 2 con el DAT de cuarentena (`Removed titles`) apuntando a una carpeta de salida distinta, si se quiere tener también esos títulos organizados aparte para revisión manual, en vez de descartados sin más.

Alternativa más ligera a DATROMTool cuando no hace falta el resto de capacidades de este (conversión de formatos, parsing multi-fuente) — solo generación 1G1R sobre No-Intro.

## Igir

**Fuente:** igir.io, github.com/emmercm/igir. CLI en JavaScript/Node.js. **Instalar con `npm install -g igir@<versión>` dentro del devcontainer, no `npx igir@latest`** — confirmado que `npx` no completa la instalación del paquete nativo `dolphin-tool` (falla con `Cannot find module './addon-dolphin-tool/build/Release/dolphin-tool.node'`), incluso en Node 22; `npm install -g` sobre Debian bookworm (base del devcontainer) sí funciona. Ya integrado en `.devcontainer/Dockerfile` (`ARG IGIR_VERSION`, junto a Node.js vía NodeSource — la imagen base no trae Node). Requiere Node.js ≥22 (`igir@5.4.0` lo declara como *engine*).

**Hallazgo clave, confirmado leyendo el código fuente (`src/modules/dats/datParentInferrer.ts`), no solo la doc — esto es lo que distingue a Igir de retool y `1g1r-romset-generator` para fuentes sin `cloneof`/`cloneofid` (TOSEC, o un DAT Standard de No-Intro):**

Igir trae un módulo, `DATParentInferrer`, que **infiere las relaciones padre/clon él solo** cuando el DAT no las declara — no necesita un clonelist externo (a diferencia de retool) ni se limita a tratar cada entrada como su propia familia (lo que hace `1g1r-romset-generator` al carecer de `cloneof`, avisando explícitamente "A Parent/Clone XML DAT is required"). El algoritmo:

1. Si el DAT ya trae parent/clone, no toca nada (salvo `--dat-ignore-parent-clone`, que fuerza la re-inferencia igualmente).
2. Si no, agrupa por nombre **despojado** de región/idioma y de un catálogo extenso de variantes conocidas — con reglas **específicas para la convención de nombrado de TOSEC** (`TOSEC_REGION_REGEX`, `TOSEC_LANGUAGE_REGEX`, `TOSEC_DEMO_REGEX`, `TOSEC_COPYRIGHT_REGEX`, `TOSEC_DEVELOPMENT_REGEX`, `TOSEC_DUMP_FLAGS_REGEX` — este último cubre exactamente los flags `[cr|f|h|m|p|t|tr|o|u|v|b|a|!]` de la especificación oficial, ver `docs/references.md#tosec`), además de las reglas genéricas de No-Intro/GoodTools/consola específica.
3. Si tras despojar todo hay un "juego retail limpio" con ese nombre base, ese es el padre (gane o no en orden de aparición); si no, el primero visto en el DAT hace de padre por defecto.

**Capacidades confirmadas (contra el `--help` real de `igir@5.4.0`):**

- Agnóstico de fuente de DAT — soporta No-Intro, Redump, TOSEC y MAME (incluye reconstrucción de un set MAME a la versión exacta indicada, `--dat "MAME 0.258.dat"`).
- Filtrado 1G1R (`--single`/`-s`) con prioridades configurables, aplicadas en orden: `--prefer-game-regex`/`--prefer-rom-regex`, `--prefer-verified`, `--prefer-good`, `-l/--prefer-language`, `-r/--prefer-region`, `--prefer-revision older|newer`, `--prefer-retail`, `--prefer-parent`.
- Filtros de exclusión por categoría (independientes de `--single`): `--no-bios`, `--no-device`, `--no-unlicensed`, `--no-debug`, `--no-demo`, `--no-beta`, `--no-sample`, `--no-prototype`, `--no-program`, `--no-aftermarket`, `--no-homebrew`, `--no-unverified`, `--no-bad`; `--only-retail` activa todos los anteriores de golpe. Cada uno tiene su opuesto `--only-*`.
- Regiones/idiomas soportados por `--prefer-region`/`--filter-region` son una lista cerrada de códigos, mezcla de 2 y 3 letras (`USA`, `UK`, `GER`, `EUR`, `JPN`, `WORLD`... — no siempre coincide con el código de 2 letras que usa TOSEC en el nombre, ej. `DE`→`GER`, revisar la lista exacta en `--help` antes de asumir un código).
- Gestiona tanto ROMs planas como imágenes de disco pesadas (`.iso`, `.chd`, `.cue`) — extrae, renombra y mueve.
- También cubre detección de cabeceras headered/headerless (ver `docs/references.md#caso-especial--headered-vs-headerless-nes-snes-atari-7800-atari-lynx-fds`), relevante si el 1G1R se aplica sobre un romset con esa variante.
- **Comando `dir2dat` integrado** ("Generate a DAT from all input files") — permite generar el DAT del propio resultado 1G1R sin depender de SabreTools: `igir dir2dat --input <carpeta 1G1R> --dir2dat-output <carpeta>`. Útil como referencia versionable de "esto es exactamente lo que hay en mi 1G1R", ya sin relación padre/clon que resolver (cada entrada es única).

**Ejemplo de comando confirmado (genérico):**

```bash
igir copy --dat "*.dat" --input "**/*.zip" --output 1G1R --dir-dat-name --single --prefer-language EN --prefer-region USA,WORLD,EUR,JPN
```

### Verificado end-to-end contra TOSEC real (2026-09-02) — `atari800`, categoría `[ATR]`

Prueba real en el devcontainer (`emulation-devcontainer` con Igir ya instalado) contra `sources/tosec/out/Atari 8bit - Games - [ATR] (TOSEC-v2025-01-15_CM).dat` (5822 entradas, sin `cloneof` — DAT TOSEC plano) y una colección física real de 5759 ficheros `.atr`:

```bash
igir copy report --dat atari800.dat --input "[ATR]/" --output output/ --single --prefer-region USA,UK,GER,EUR
```

**Resultado:**

- 5822 entradas del DAT → **4146 familias** tras la inferencia automática de `DATParentInferrer` (sin clonelist propio de TOSEC, que no existe) — es decir, agrupó ~1676 entradas como clones de otra.
- De esas 4146, **4080 encontradas y copiadas** de la colección real (3557/3622 son "retail releases" según la propia clasificación de Igir, el resto BASIC listings/homebrew que TOSEC también cataloga).
- Sin errores ni colapsos incorrectos detectados al revisar el resultado a mano: `007 - The Living Daylights (1987)(Domark)(GB)` y su variante `[k-file]` se mantuvieron **separados** (el tag `[k-file]` no está en la lista de variantes que el inferidor sabe despojar, así que no se arriesga a fusionarlos); `0 Grad Nord` de 1985 (Ariolasoft) y de 1990 (Secret Games) — mismo nombre, juegos distintos — tampoco se confundieron.

**Conclusión de esta sesión de pruebas — comparación de las tres herramientas para 1G1R:**

| | retool | 1g1r-romset-generator | Igir |
| --- | --- | --- | --- |
| DAT con `cloneof` (No-Intro/Redump con Parent-Clone) | ✅ nativo | ✅ nativo | ✅ nativo |
| DAT sin `cloneof` (TOSEC, Standard) | ❌ necesita clonelist externo (no existe para TOSEC) | ❌ se niega salvo confirmación manual, y no agrupa nada aunque continúes | **✅ infiere el agrupado él solo**, con reglas propias para TOSEC |
| Genera un DAT de salida | ✅ | ❌ (opera sobre ficheros físicos) | ✅ (`dir2dat`, además de operar sobre ficheros físicos) |

**Para TOSEC específicamente, Igir es la herramienta correcta para el 1G1R real** — retool y `1g1r-romset-generator` quedaban bloqueados exactamente en el punto que motivó `docs/session-context.md` a apuntar "falta el clonelist propio para TOSEC/MAME" como pendiente; con Igir ese pendiente queda resuelto sin necesidad de construir ese clonelist a mano.

## Scripts propios (sin herramienta de terceros)

Alternativa de control total: parsear directamente el DAT Logiqx XML (o el `dat-index/<id>.json` ya generado por el pipeline propio, ver [custom-pipeline.md](../romsets/custom-pipeline.md)) y aplicar la lógica de región/idioma a mano, cruzando contra `metadata/dat/retool/clonelists/*.json` cuando el sistema no tenga `cloneofid` nativo (caso Redump). Útil cuando ninguna herramienta de terceros cubre bien un sistema concreto, a costa de mantener la lógica de filtrado propia. Fuente confirmada de esos ficheros de clonelist: github.com/unexpectedpanda/retool-clonelists-metadata (ver detalle en [dat-generation.md](dat-generation.md#redump)) — es el mismo repositorio que alimenta a retool, así que reutilizarlo aquí mantiene la lógica de agrupado consistente entre ambos métodos.

[TODO: no existe ninguna herramienta de terceros consolidada llamada "PyRomVault" — verificado que no aparece en ninguna búsqueda; si se busca algo ya hecho en Python en vez de script propio desde cero, existen proyectos como `romlm` (pack/unpack/sort/dedupe) o `pyrsc` (Python ROMs Set Cleaner, quita clones/bootlegs), sin confirmar si cubren 1G1R con la misma profundidad que retool/Igir]

## Notas

El DAT 1G1R generado en esta fase no sustituye al DAT completo obtenido en la fase 1 — se conservan ambos: el completo para poder recuperar cualquier título descartado más adelante, y el 1G1R como el que realmente se usa para filtrar/reconstruir el romset de despliegue.

Ver `docs/references.md#1g1r` para los conceptos de reglas regionales, exclusiones y la cuarentena de exclusivos regionales (`japan/`) que aplica este repo cuando 1G1R descarta un título que solo existe en una región no prioritaria.
