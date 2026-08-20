# Bitácora de procesado de romsets

Registro cronológico de sesiones reales de trabajo procesando romsets — no es documentación prescriptiva (eso es [workflow.md](workflow.md) y las guías de [docs/guides/tools/](../tools/README.md)), es el rastro de **qué se hizo de verdad, en qué orden y con qué comandos concretos**, para poder destilarlo después en scripts propios (ver roadmap en [custom-pipeline.md](custom-pipeline.md)).

**Reseteada el 2026-08-17:** se limpiaron las entradas anteriores al reiniciar el proceso de generación de DAT para romsets — las decisiones de fuente/formato que salieron de esas sesiones siguen vigentes en `docs/romsets.md` (no se pierden), solo se vacía el registro cronológico para volver a llevar la traza desde cero.

## Cómo usar esta bitácora

- Las entradas se agrupan por **tipo de romset**, los mismos cuatro de [cartridge.md](cartridge.md), [microcomputers.md](microcomputers.md), [optical-chd.md](optical-chd.md) y [arcade.md](arcade.md) — así una sesión se compara contra sesiones del mismo tipo, no contra todo el histórico mezclado (el proceso real difiere bastante entre, por ejemplo, cartucho y óptico).
- Dentro de cada tipo, una entrada por sesión de trabajo, en orden cronológico (más reciente arriba).
- Cada entrada sigue la plantilla de abajo — no hace falta rellenar todos los campos si no aplican.
- Cuando un mismo paso se repite igual en 2-3 sesiones seguidas **dentro del mismo tipo**, es la señal de que ese paso ya está maduro para automatizarse — anotarlo en "Candidato a automatizar" y trasladarlo al roadmap de [custom-pipeline.md](custom-pipeline.md) cuando se decida abordarlo. Si se repite igual **entre tipos distintos**, es candidato a automatización más genérica (aplicable a todo el pipeline, no solo a un tipo de fuente).
- Enlazar a la fase/guía correspondiente (`../tools/dat-generation.md`, etc.) en vez de repetir el detalle de uso de cada herramienta — aquí solo va la traza real (qué se ejecutó, con qué parámetros, qué pasó).

## Plantilla de entrada

Cada entrada mapea directamente a las 10 fases de [workflow.md](workflow.md), para que las sesiones sean comparables fase a fase entre sí. Marcar `—` en las fases que no aplicaron a esta sesión (ej. fase 2 si el DAT ya venía en el formato correcto), no borrar la línea — así queda constancia de que se consideró y no de que se olvidó.

```markdown
### AAAA-MM-DD — <Sistema/consola>

**Objetivo:** qué se quería conseguir en esta sesión.

**Fases seguidas** (ver [dat-generation.md](../tools/dat-generation.md) / [dat-conversion.md](../tools/dat-conversion.md) / etc. para el detalle de cada herramienta):

1. Obtención del DAT — comando/acción exacta, o `—` si no aplicó.
2. Conversión de DAT — 
3. Auditoría contra DAT — 
4. Limpieza de romset — 
5. Filtrado 1G1R — 
6. Parcheo — 
7. Compresión/conversión de formato — 
8. Organización en data/roms — 
9. Generación de gamelist.xml — 
10. Obtención de media — 

**Resultado:** qué salió (romset final, nº de juegos, tamaño, etc.).

**Problemas / decisiones tomadas:** cualquier desvío del proceso estándar, y por qué.

**Candidato a automatizar:** qué fase(s) de esta sesión fueron mecánicas e idénticas a sesiones anteriores.
```

## Cartucho / plano

<!-- Añadir entradas nuevas justo debajo de esta línea, la más reciente primero -->

### 2026-08-20 — `strip-retool-tag.ps1` mejorado: conserva recuento y evita colisión con "Removed titles"

**Objetivo:** tras regenerar los 44 sistemas con Retool (fix de idioma + orden de regiones), limpiar el nombre de los ~389 ficheros resultantes en `data/dats/{console,micro,arcade}/{1g1r,fullset}/` quitando el tag `(Retool <fecha>) [flags]` que añade Retool.

**Problema encontrado con la versión anterior del script:** el `.dat` principal y el `.dat` de auditoría `(Removed titles)` del mismo sistema colapsaban al mismo nombre tras quitar todo lo posterior a `(Retool ...)` — ambos son `.dat`, la única diferencia estaba justo en la parte que se eliminaba. Al ejecutar de verdad, el segundo se omitía por colisión (`Test-Path` ya ocupado) y se quedaba con el nombre feo original; `-WhatIf` no lo reflejaba porque no simula colisiones entre renombrados de la misma pasada.

**Fix:** reescrito `tools/scripts/strip-retool-tag.ps1` para conservar el recuento de títulos entre paréntesis (`(510)`, `(1,297)`...) y el marcador `(Removed titles)` cuando aplica, en vez de descartar todo el bloque tras `(Retool ...)`. Resultado: `<sistema> (<fecha versión DAT>) (<recuento>).dat` para el principal, `<sistema> (<fecha>) (Removed titles) (<recuento>).dat` para el de auditoría, `<sistema> (<fecha>).txt` para el informe — sin colisión posible, cada uno tiene un nombre distinto. Verificado con `-WhatIf` sobre los 389 ficheros: 0 `OMITIDO` antes de ejecutar el renombrado real.

**Resultado:** 389 ficheros renombrados en una pasada sobre `data/dats/` (recursivo, confirmado que ya lo era). Registrado también que las variantes `(-d)` (deduplicado) viven en `fullset/`, separadas de `1g1r/`, así que no hay colisión cruzada entre ambas carpetas.

**Candidato a automatizar:** ninguno — ya es el script versionado, no queda nada suelto en el scratchpad para este paso.

### 2026-08-19 — Sega Mega Drive (`megadrive`): diagnóstico y fix de títulos base desaparecidos del 1G1R

**Objetivo:** averiguar por qué `Golden Axe`, `Columns`, `Streets of Rage`, `ToeJam & Earl`, `Sonic & Knuckles`, `Super Hang-On`, `Revenge of Shinobi`, `Shadow Dancer`, `Super Volleyball` y `World Cup Italia '90` desaparecían enteros del 1G1R de Retool pese a estar en el `fullset` y tener idioma correcto.

**Fases seguidas** (ver [dat-generation.md](../tools/dat-generation.md)):

1. Obtención del DAT — ya generado (`sources/dats/no-intro/fullset/Sega - Mega Drive - Genesis (Parent-Clone)...dat`).
2. Conversión de DAT — `—`
3. Auditoría contra DAT — diagnóstico con la función "Trace a title through Retool's process" de la GUI (checkbox + campo de regex, `Golden Axe`), apuntando al DAT de Mega Drive.
4. Limpieza de romset — `—`
5. Filtrado 1G1R — **causa raíz encontrada y corregida**: ver detalle abajo.
6. Parcheo — `—`
7. Compresión/conversión de formato — `—`
8. Organización en data/roms — `—`
9. Generación de gamelist.xml — `—`
10. Obtención de media — `—`

**Resultado:** causa raíz confirmada con traza real de `Golden Axe` — en `Stage: Compilations`, Retool prefiere la copia de un juego embebida en una recopilación multijuego (`10 Super Jogos (Brazil)`, `Mega Games 2 (Europe)`, `6-Pak (USA)`) sobre el cartucho individual cuando la región de esa recopilación tiene mayor prioridad interna que la región del cartucho individual en "Filter by this region order" (Global settings → Regions). El usuario solo tenía `Spain, Europe, UK, World, USA, Japan` en esa lista; `Brazil` no estaba añadida pero aun así tenía prioridad interna mejor que `World`, así que ganaba la recopilación brasileña y `Golden Axe` quedaba oculto dentro de ella (no como entrada propia en el 1G1R). **Fix:** mover todas las "Available regions" restantes a la lista ordenada, por debajo de las 6 de interés real. Reprocesados los 44 sistemas con este ajuste. Verificado con `grep` sobre el 1G1R regenerado de `megadrive` (1297 juegos): los 10 títulos de la lista ya aparecen; `6-Pak` deja de aparecer como recopilación porque ya no hace falta (sus juegos ganan todos por separado) — comportamiento correcto, no regresión.

**Problemas / decisiones tomadas:** el checkbox "Trace a title" tiene un campo de regex justo debajo que no era visible a primera vista — hay que apuntar además al DAT correcto (se probó primero por error sobre Master System). Detalle completo del hallazgo en `docs/session-context.md`.

**Candidato a automatizar:** ninguno — es un ajuste de configuración de Retool (GUI externa), no de nuestros scripts. Documentado como regla operativa permanente para toda futura pasada por Retool.

### 2026-08-17 — Fairchild Channel F (`channelf`) y Mega Duck (`megaduck`)

**Objetivo:** dar de alta los DAT No-Intro de los dos sistemas de cartucho añadidos esta sesión, tras resetear `sources/` para empezar limpios.

**Fases seguidas** (ver [dat-generation.md](../tools/dat-generation.md#no-intro-dat-o-matic)):

1. Obtención del DAT — ya estaba descargado en `metadata/dat/No-Intro/{full,aftermarket,pc}/`; añadidas las entradas `channelf`→`Fairchild - Channel F` y `megaduck`→`Welback - Mega Duck` a `tools/scripts/config/nointro-systems.json`, y sincronizado a `sources/dats/no-intro/{pc,full,aftermarket}/` con `update-sources.ps1`.
2. Conversión de DAT — `—` (Logiqx XML, formato esperado).
3. Auditoría contra DAT — `—` (pendiente; lo generado hoy es el índice `metadata/dat-index/<id>.json`, no una auditoría de romset físico).
4. Limpieza de romset — `—`
5. Filtrado 1G1R — `—`
6. Parcheo — `—`
7. Compresión/conversión de formato — `—`
8. Organización en data/roms — `—`
9. Generación de gamelist.xml — `—`
10. Obtención de media — `—`

**Resultado:** `build-dat-index-nointro.ps1 -SystemId <id>` generado para ambos: `channelf` (29 familias, 3 descartados, 2 con alias), `megaduck` (26 familias, 0 descartados, 0 con alias). Contraste `pc/` vs `full+aftermarket`: 0 divergencias en los dos.

**Problemas / decisiones tomadas:** ninguno — primer indexado de ambos sistemas, sin sorpresas.

**Candidato a automatizar:** ninguno todavía, muestra muy pequeña (2 sistemas).

## Microcomputers

<!-- Añadir entradas nuevas justo debajo de esta línea, la más reciente primero -->

### 2026-08-17 — Commodore 64 (`c64`), MSX (`msx`) y MSX2 (`msx2`)

**Objetivo:** dar de alta los DAT No-Intro de los tres microcomputers con fuente No-Intro fijada esta sesión (swap desde TOSEC), tras resetear `sources/` para empezar limpios.

**Fases seguidas** (ver [dat-generation.md](../tools/dat-generation.md#no-intro-dat-o-matic)):

1. Obtención del DAT — ya estaba descargado en `metadata/dat/No-Intro/{full,aftermarket,pc}/`; añadidas las entradas `c64`→`Commodore - Commodore 64`, `msx`→`Microsoft - MSX`, `msx2`→`Microsoft - MSX2` a `tools/scripts/config/nointro-systems.json`, y sincronizado a `sources/dats/no-intro/{pc,full,aftermarket}/` con `update-sources.ps1`.
2. Conversión de DAT — `—` (Logiqx XML, formato esperado).
3. Auditoría contra DAT — `—` (pendiente; lo generado hoy es el índice `metadata/dat-index/<id>.json`, no una auditoría de romset físico).
4. Limpieza de romset — `—`
5. Filtrado 1G1R — `—`
6. Parcheo — `—`
7. Compresión/conversión de formato — `—`
8. Organización en data/roms — `—`
9. Generación de gamelist.xml — `—`
10. Obtención de media — `—`

**Resultado:** `build-dat-index-nointro.ps1 -SystemId <id>` generado para los tres: `c64` (255 familias, 95 descartados, 0 con alias), `msx` (577 familias, 53 descartados, 7 con alias, 12 divergencias de clonelist), `msx2` (153 familias, 6 descartados, 2 con alias, 3 divergencias de clonelist). Contraste `pc/` vs `full+aftermarket`: 0 divergencias en los tres.

**Problemas / decisiones tomadas:** ninguno — primer indexado de los tres sistemas tras el swap de fuente TOSEC→No-Intro decidido esta misma sesión.

**Candidato a automatizar:** el flujo "añadir al manifiesto → `update-sources.ps1` → `build-dat-index-nointro.ps1 -SystemId`" ya se ha repetido igual para 5 sistemas seguidos (esta entrada + la de Cartucho/plano) — buen candidato a un script único que encadene los tres pasos por sistema en vez de ejecutarlos sueltos.

## Óptico → CHD

<!-- Añadir entradas nuevas justo debajo de esta línea, la más reciente primero -->

## Arcade

<!-- Añadir entradas nuevas justo debajo de esta línea, la más reciente primero -->
