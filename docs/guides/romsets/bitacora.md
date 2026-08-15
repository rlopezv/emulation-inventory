# Bitácora de procesado de romsets

Registro cronológico de sesiones reales de trabajo procesando romsets — no es documentación prescriptiva (eso es [workflow.md](workflow.md) y las guías de [docs/guides/tools/](../tools/README.md)), es el rastro de **qué se hizo de verdad, en qué orden y con qué comandos concretos**, para poder destilarlo después en scripts propios (ver roadmap en [custom-pipeline.md](custom-pipeline.md)).

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

### 2026-08-15 — Sistemas de cartucho (varios)

**Objetivo:** obtener los DAT No-Intro Parent-Clone para los sistemas de cartucho de interés, incluyendo cobertura aftermarket.

**Fases seguidas** (ver [dat-generation.md](../tools/dat-generation.md#no-intro-dat-o-matic)):

1. Obtención del DAT — descarga masiva de **dos paquetes** desde DAT-o-MATIC (sección Download → Daily), ninguno requiere cuenta/login:
   - **No-Intro Love Pack (PC)** — catálogo licenciado/comercial, variante Parent-Clone.
   - **No-Intro Love Pack (DAT) (Aftermarket)** — catálogo aftermarket (juegos no licenciados publicados después del último juego oficial de la plataforma), para tratar homebrew tardío.

   De ambos paquetes, descomprimidos y seleccionados solo los `.dat` de los sistemas de interés del catálogo completo (no se procesan los demás).
2. Conversión de DAT — `—` (el DAT ya viene en Logiqx XML, formato esperado).
3. Auditoría contra DAT — `—` (pendiente, no realizada en esta sesión).
4. Limpieza de romset — `—`
5. Filtrado 1G1R — `—`
6. Parcheo — `—`
7. Compresión/conversión de formato — `—`
8. Organización en data/roms — `—`
9. Generación de gamelist.xml — `—`
10. Obtención de media — `—`

**Resultado:** DATs No-Intro Parent-Clone (licenciado + aftermarket) obtenidos para los sistemas de cartucho de interés.

**Problemas / decisiones tomadas:** confirmado que "(PC)" en el nombre del pack indica Parent-Clone directamente (sin necesidad de una opción separada). Corregido en `dat-generation.md`: en la sección Daily hay **varios paquetes distintos** según catálogo (al menos PC/licenciado y Aftermarket, con posibles otras variantes como "Standard" plano sin confirmar del todo) — no un único paquete unificado como se dejó escrito en una revisión anterior de esta misma sesión. Dos sistemas de cartucho quedan fuera de ambos packs por no tener cobertura No-Intro en absoluto: `gx4000` (usa TOSEC) y `sgb` (sin DAT propio, usa ROMs de `gb`/`gbc`) — ambos ya estaban bien documentados en `docs/romsets.md` antes de esta sesión.

**Caso especial anotado — Neo Geo AES (`neogeo`):** aunque es nominalmente cartucho, se deja **fuera de este flujo** (no se procesó con el Love Pack de No-Intro) — AES y MVS comparten romset, y se tratará dentro de la fase de Arcade con el DAT de FBNeo/MAME correspondiente, ya documentado así en `docs/romsets.md`. No repetir el trabajo dos veces cuando llegue la sesión de arcade.

**Candidato a automatizar:** la descarga de ambos Love Packs es idéntica cada vez que se actualiza el catálogo (mismos paquetes, sin login, mismos pasos) — buen candidato a script de descarga+extracción selectiva una vez se repita en 2-3 sesiones más.

## Microcomputers

<!-- Añadir entradas nuevas justo debajo de esta línea, la más reciente primero -->

### 2026-08-15 — Microcomputers (TOSEC en vez de No-Intro)

**Objetivo:** obtener DATs para los microcomputers de interés, decidiendo entre No-Intro (fuente ya documentada) y TOSEC (ya descargado el pack completo).

**Fases seguidas** (ver [dat-generation.md](../tools/dat-generation.md#tosec-the-old-school-emulation-center) y [microcomputers.md](microcomputers.md)):

1. Obtención del DAT — descargado previamente **TOSEC - DAT Pack - Complete (4743) (TOSEC-v2025-03-13)** desde tosecdev.org, ya extraído en `metadata/dat/TOSEC/`. Decisión: usar TOSEC en vez de No-Intro/libretro para `c64`, `amiga`, `msx`, `msx2`, `amstradcpc`, `atarist`, `spectrum` y `zx81` — motivo: mucho software de microcomputer solo sobrevive en volcados crackeados, que No-Intro excluye por filosofía de "solo volcado limpio"; TOSEC los acepta deliberadamente. `sharpx68000` se queda en Non-Redump, sin cambiar por ahora. De paso, se resolvieron dos huecos que estaban sin fuente identificada: `c128` y `dragon32` sí tienen cobertura TOSEC.
2. Conversión de DAT — `—` (ya viene en Logiqx XML variante TOSEC).
3. Auditoría contra DAT — `—` (pendiente).
4. Limpieza de romset — `—`
5. Filtrado 1G1R — `—`
6. Parcheo — `—`
7. Compresión/conversión de formato — `—`
8. Organización en data/roms — `—`
9. Generación de gamelist.xml — `—`
10. Obtención de media — `—`

**Resultado:** fuente y variante de formato decidida para los 9 sistemas de microcomputer; `docs/romsets.md` actualizado con la decisión y el motivo.

**Problemas / decisiones tomadas:** el catálogo TOSEC es mucho más masivo y granular de lo esperado — no es "un DAT por sistema" sino decenas por sistema, cruzando categoría (Games/Applications/Demos/...) y formato de medio (`[D64]`, `[ADF]`, `[ROM]`, etc.). Caso especial `c64`: la categoría Games está además dividida en 12 sub-DAT por género, que hay que fusionar con `SabreTools --merge` antes de poder auditar contra un único DAT — ver [dat-conversion.md](../tools/dat-conversion.md). El resto de sistemas no tiene esa división por género.

**Candidato a automatizar:** la fusión por `SabreTools --merge` de los 12 sub-DAT de género de `c64` es mecánica y se repetirá cada vez que se actualice el pack TOSEC — buen candidato a script una vez esté probado manualmente al menos una vez.

## Óptico → CHD

<!-- Añadir entradas nuevas justo debajo de esta línea, la más reciente primero -->

### 2026-08-15 — Sistemas ópticos (varios)

**Objetivo:** obtener los DAT Redump para los sistemas ópticos de interés, junto con sus ficheros auxiliares.

**Fases seguidas** (ver [dat-generation.md](../tools/dat-generation.md#redump)):

1. Obtención del DAT — descargado desde **redump.org/downloads/**, sección pública Downloads, sin necesidad de cuenta. Junto al DAT de cada sistema, descargados también los **`.cue`** y los **`.sbi`** correspondientes.
2. Conversión de DAT — `—` (Logiqx XML, formato esperado).
3. Auditoría contra DAT — `—` (pendiente, no realizada en esta sesión; los `.cue`/`.sbi` obtenidos aquí son justo lo que hace falta para esa fase después, vía verifydump).
4. Limpieza de romset — `—`
5. Filtrado 1G1R — `—`
6. Parcheo — `—`
7. Compresión/conversión de formato — `—`
8. Organización en data/roms — `—`
9. Generación de gamelist.xml — `—`
10. Obtención de media — `—`

**Resultado:** DATs Redump + `.cue` + `.sbi` obtenidos para los sistemas ópticos de interés.

**Problemas / decisiones tomadas:** ninguno — coincide exactamente con lo ya documentado en `dat-generation.md#redump` (Cuesheets y SBI files como descargas aparte del DAT, en la misma página).

**Candidato a automatizar:** igual que con No-Intro, la descarga por sistema desde Redump es mecánica y repetible — candidato a script una vez se repita en más sesiones. A diferencia de No-Intro, aquí hace falta descargar 3 ficheros por sistema (DAT + `.cue` + `.sbi`) en vez de 1.

## Arcade

<!-- Añadir entradas nuevas justo debajo de esta línea, la más reciente primero -->

### 2026-08-15 — Arcade (MAME + FBNeo)

**Objetivo:** obtener los DAT de MAME y FBNeo para el romset arcade, incluyendo Neo Geo AES/MVS (ver nota en la entrada de Cartucho de esta misma fecha).

**Fases seguidas** (ver [dat-generation.md](../tools/dat-generation.md#mame--fbneo-ecosistema-arcade)):

1. Obtención del DAT — tres fuentes:
   - **MAME** — descargado desde **progettosnaps.net/dats/MAME/** (no generado en local con `mame -listxml`).
   - **FBNeo** — obtenido de **libretro-database**, carpeta `metadat/fbneo-split/` (fichero `FinalBurn Neo (ClrMame Pro XML, Arcade only).dat`).
   - **retropie-dat** (github.com/HerbFargus/retropie-dat) — descargado también el contenido completo del repositorio (carpetas por core: `lr-mame2003-plus`, `lr-mame2010`, `lr-fbneo`, etc.), para tener a mano el DAT de versiones de core más antiguas si hace falta auditar contra hardware que corre un core legacy en vez del más reciente.
2. Conversión de DAT — `—` (MAME XML y ClrMamePro texto respectivamente, formatos ya esperados por la fase de auditoría).
3. Auditoría contra DAT — `—` (pendiente, no realizada en esta sesión).
4. Limpieza de romset — `—`
5. Filtrado 1G1R — `—`
6. Parcheo — `—`
7. Compresión/conversión de formato — `—`
8. Organización en data/roms — `—`
9. Generación de gamelist.xml — `—`
10. Obtención de media — `—`

**Resultado:** DAT de MAME (Progetto-Snaps), DAT de FBNeo (libretro-database) y colección de DAT por versión de core (retropie-dat) obtenidos.

**Problemas / decisiones tomadas:** ninguno — las tres fuentes coinciden con lo ya documentado en `dat-generation.md` (Progetto-Snaps y libretro-database ya estaban; retropie-dat se añadió a la guía a raíz de esta sesión, con nota de mantenimiento limitado). Confirmado el uso real de Progetto-Snaps como alternativa a la generación local de MAME, no solo una opción teórica.

**Candidato a automatizar:** la descarga desde Progetto-Snaps, `libretro-database` y `retropie-dat` son las tres mecánicas — buenas candidatas a script una vez se repitan en más sesiones (ej. tras cada actualización de versión de MAME/FBNeo).
