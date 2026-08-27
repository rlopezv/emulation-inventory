# Prompt - Investigar tema y bezels para un dispositivo con CFW instalado

Voy a darte el nombre de un dispositivo ya presente en `docs/devices.md`, con su CFW/frontend ya elegido en `docs/distributions.md` (EmulationStation o alguno de sus forks: KNULLI, ROCKNIX, ArkOS, dArkOS, Batocera, AmberELEC, etc.).

Tu tarea es investigar qué **tema visual** de EmulationStation y qué **pack de bezels/overlays** de RetroArch son compatibles de verdad con ese dispositivo y ese CFW concreto, y devolver una recomendación lista para usar.

## Por qué existe este prompt

Una sesión de investigación real (agosto 2026) partió de una tabla de temas/bezels aportada por el usuario desde otra fuente (sin verificar) y, al contrastar cada fila contra el repositorio real, **casi todas resultaron incorrectas**: un tema atribuido al autor equivocado, temas anunciados como compatibles con 3 CFW distintos cuando el README solo confirmaba uno, formatos de pantalla mal descritos (un tema "1:1 nativo" resultó tener el 1:1 marcado "in process", sin terminar), un pack de bezels con el nombre de repositorio distinto al dado, y una ruta de instalación de ArkOS que ningún documento oficial confirma. Este prompt existe para no repetir ese patrón: **nunca aceptar una lista de temas/bezels de terceros tal cual**, verificar siempre contra la fuente primaria.

## Paso 1 — Determinar los requisitos reales del dispositivo

Antes de buscar nada, fija estos datos desde `docs/devices.md` y `docs/distributions.md` (no los preguntes al usuario si ya están documentados):

1. **Relación de aspecto y resolución de pantalla** (columna `Aspect Ratio`/`Resolución` de `devices.md`) — 4:3, 3:2, 1:1, 16:9, 16:10, dual-screen, etc. Esto filtra qué temas/bezels encajan de verdad; un tema pensado para pantalla cuadrada 1:1 se ve roto en una pantalla 4:3 y viceversa.
2. **Orientación** (columna `Orientación`) — horizontal, vertical, giratoria: puede excluir según diseño del tema.
3. **CFW/frontend real** (columna `Software recomendado`/`Frontend recomendado` de `distributions.md`) — el nombre exacto (KNULLI, ROCKNIX, ArkOS, dArkOS, Batocera, AmberELEC, RetroBat...). **Importante:** estos forks de EmulationStation NO comparten automáticamente compatibilidad de temas entre sí, aunque estén emparentados (ej. KNULLI deriva de ROCKNIX, pero un tema "compatible con ROCKNIX" no está confirmado compatible con KNULLI solo por eso) — cada uno se verifica por separado contra lo que diga el README.

## Paso 2 — Buscar candidatos

Busca temas EmulationStation y packs de bezels/overlays candidatos (GitHub, foros de la comunidad del CFW en cuestión, wiki oficial del CFW si enlaza temas recomendados). Anota nombre + URL de repo + autor de cada candidato — sin dar nada por bueno todavía.

## Paso 3 — Verificar cada candidato contra su fuente primaria (obligatorio, no opcional)

Para cada tema/pack candidato, **abre el repositorio real y lee su README** (no un resumen de terceros, no una tabla ya hecha que alguien te pase). Confirma explícitamente:

1. **La URL exacta existe y contiene lo que dice contener** — el nombre del autor/usuario de GitHub dado puede estar equivocado; si no encuentras coincidencia exacta, dilo explícitamente en vez de aproximar a la URL "más parecida".
2. **Compatibilidad de CFW declarada por el propio README** — lista exacta de CFW/frontends que el autor dice soportar. Si el CFW objetivo no aparece en esa lista, es "no confirmado", no "probablemente compatible por parentesco".
3. **Relación de aspecto / resolución objetivo declarada por el propio README** — algunos temas soportan varias (ej. "4:3, 1:1 y 16:9"), otros solo una, y a veces un formato aparece como "in process"/sin terminar aunque se anuncie en el título. Cita el texto exacto si hay ambigüedad.
4. **Estado de mantenimiento** — fecha del último commit/push. Marca como legacy/posiblemente abandonado si no hay actividad reciente (más de ~1-2 años, según contexto).
5. **Si el "pack" agrupa varios repos separados** (ej. un autor con 3 repos distintos para consolas/arcade realista/arcade fanart bajo el mismo tema) — desambigua cuál es el que corresponde a lo que se busca, no los trates como una unidad.

## Paso 4 — Verificar la ruta de instalación contra la documentación oficial del CFW

No asumas rutas por analogía con otro CFW de la misma familia. Busca la **wiki/documentación oficial** del CFW concreto (ej. `knulli.org`, wiki de `christianhaitian/arkos`) y confirma:

- Ruta de instalación de temas.
- Ruta de instalación de bezels/overlays (y si el propio CFW gestiona el bezel automáticamente desde EmulationStation, o si hace falta configurarlo aparte dentro de RetroArch — esto varía y algunas guías de terceros lo indican mal).

Si no encuentras una página oficial que dé la ruta exacta, dilo con `[TODO]` en vez de dar una ruta de una guía comunitaria como si fuera oficial — puedes citar la comunitaria como aproximación, marcada como tal.

## Reglas

1. No inventes ni des por buena ninguna afirmación de compatibilidad, formato o ruta que no hayas visto tú mismo en la fuente primaria (README del repo, wiki oficial del CFW).
2. Si te doy una tabla o lista ya elaborada (mía o de otra fuente) como punto de partida, trátala como lista de candidatos a verificar, nunca como resultado ya válido.
3. Usa `[TODO]` explícito para cualquier dato que no puedas confirmar, en vez de aproximar o dejarlo implícito.
4. Cuando corrijas un dato de la lista de partida, dilo explícitamente ("la tabla decía X, el README real dice Y") en vez de sustituirlo en silencio.
5. Devuelve el resultado como una recomendación acotada al dispositivo+CFW concreto: nombre del tema, URL del repo, ruta de instalación citando su fuente; mismo formato para el pack de bezels si aplica.
