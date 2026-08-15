# Generación / obtención de DAT

Punto de partida del flujo: obtener el DAT correcto por sistema antes de auditar, filtrar o renombrar nada. La fuente concreta por sistema está fijada en `docs/romsets.md` — esa tabla es la fuente de verdad y esta guía **no la redefine**. La sección "Cómo elegir la fuente" de aquí abajo explica el criterio general detrás de esas decisiones, útil sobre todo para un sistema nuevo aún no documentado en `docs/romsets.md` o para entender por qué se eligió una fuente en concreto. El resto de la guía cubre cómo obtener o generar cada fuente con cada herramienta, no cuál usar.

Corresponde a la fase 1 de [docs/guides/romsets/workflow.md](../romsets/workflow.md). Formato de fichero de cada fuente detallado en `docs/references.md#formatos`.

## Cómo elegir la fuente

Orden de prioridad general, de mayor a menor fiabilidad de preservación (verificación por hash, comunidad, mantenimiento activo). Para un sistema ya fijado en `docs/romsets.md`, esa tabla manda; este árbol es para sistemas sin decisión tomada todavía o para entender el criterio.

1. **¿Es arcade (placa recreativa)?** → [MAME / FBNeo](#mame--fbneo-ecosistema-arcade). MAME para máxima fidelidad si el hardware objetivo lo soporta; FBNeo para dispositivos de baja potencia (ARM, handhelds).
2. **¿Es un sistema doméstico (consola/microordenador) emulado dentro de la arquitectura de MAME** (ej. Sega CD, PC Engine CD, Neo Geo CD, ciertos microordenadores)**?** → [MAME Software Lists](#mame-software-lists-softwarelist), no el DAT arcade principal — combinando ambos solo si el sistema requiere BIOS/dispositivo adicional (ver limitaciones de esa sección).
3. **¿Es consola de cartucho, handheld o la mayoría de microcomputers?** → [No-Intro](#no-intro-dat-o-matic). Es la fuente con mayor cobertura y mejor definida (esquema Parent-Clone nativo, imprescindible para 1G1R).
4. **¿Es sistema óptico (CD/DVD/GD-ROM)?** → [Redump](#redump) como fuente primaria (máxima exactitud byte a byte). Completar con [Non-Redump](#non-redump) solo para prototipos/betas que Redump rechaza, o sistemas sin cobertura Redump todavía (PS3, PSP, Xbox 360).
5. **¿No tiene cobertura adecuada en ninguna de las anteriores?** (microordenadores huérfanos, homebrew, sistemas muy antiguos) → [TOSEC](#tosec-the-old-school-emulation-center) primero (más exhaustivo pero sin filtrado 1G1R nativo); [libretro-database](#libretro-database-clrmamepro-texto) si tampoco hay cobertura TOSEC adecuada (`spectrum`, `zx81`, `scummvm`, `dos`...); para contenido de nicho fuera de todo lo anterior (pinball, tragamonedas, visual novels, Touhou, RPG Maker, iPod Clickwheel Games...), la colección curada `Eggmansworld/Datfiles` (ver `docs/references.md#preservación-y-gestión-de-dat`) — sin garantía de mantenimiento activo equivalente a las fuentes anteriores.
6. **¿Ninguna fuente de preservación cubre el sistema, pero ya existe una colección propia organizada?** → último recurso: [Generación manual desde directorio](#generación-manual-desde-directorio-dat-from-dir) (SabreTools DFD/D2D) sobre los ficheros reales, o los backups de [gamelist.xml](#gamelistxml-dat-de-respaldo) / [HyperList](#hyperlist-xml) si solo se dispone de esos XML.

**Motivo del orden:** las fuentes 3-4 (No-Intro/Redump) son las únicas con esquema Parent-Clone nativo o agrupado fiable para 1G1R y con mantenimiento activo garantizado por comunidades dedicadas; TOSEC prioriza exhaustividad sobre curación (acepta volcados defectuosos, hacks, etc. — ver sus limitaciones); libretro-database y la generación manual son de último recurso porque no aportan garantía de volcado legítimo, solo coincidencia de hash con lo que ya hay en disco.

## No-Intro (DAT-o-MATIC)

**Fuente:** DAT-o-MATIC, datomatic.no-intro.org. El portal permite descargar paquetes diarios sin registro, pero requiere una cuenta gratuita para personalizar exportaciones avanzadas (imprescindible para entornos 1G1R).

### Opción A: Personalizada por Sistema (Recomendado para 1G1R)

Requiere iniciar sesión con tu cuenta de usuario.

1. Ir a la sección **Download** del menú principal.
2. En la pantalla de descargas, seleccionar el sistema deseado en el menú desplegable (esquina superior izquierda).
3. Configurar el esquema de exportación según el objetivo del romset:
   - **Standard:** Genera un listado plano. Útil si solo deseas comprobar la integridad de un set completo sin importar las regiones.
   - **Parent-Clone (P/C):** **Obligatorio.** Activa las relaciones de parentesco inyectando el atributo `cloneofid` (ver `docs/references.md#logiqx-xml-dat`). Es el requisito previo fundamental para usar herramientas de filtrado posterior en la Fase 5 (como Retool).
4. **Parámetro crítico de preservación:** Al elegir la opción *Parent-Clone*, asegúrate de marcar la casilla **"Default parent if there is no p/c info"**. Esto garantiza que los juegos exclusivos de una única región (que carecen de clones) queden correctamente estructurados como padres y no sean omitidos por los gestores de ROMs durante el filtrado.
5. Hacer clic en el botón de descarga para obtener el archivo. Al descomprimirlo, el fichero interno tendrá la estructura estandarizada **Logiqx XML**.

### Opción B: Descarga masiva por lotes (Daily Packs)

Ideal para actualizar todos los sistemas de golpe sin necesidad de iniciar sesión.

1. Ir directamente a la sección **Download** del menú principal.
2. En las pestañas internas de la zona central, hacer clic en la opción **Daily**.
3. Elegir el paquete según necesidad — no requieren cuenta/login. Variantes confirmadas en uso real:
   - **No-Intro Love Pack (PC)** — variante **Parent-Clone** (el nombre del pack ya lo indica con "(PC)"), catálogo licenciado/comercial estándar.
   - **No-Intro Love Pack (DAT) (Aftermarket)** — catálogo **aftermarket**: juegos no licenciados publicados *después* del último juego licenciado oficial de esa plataforma (homebrew indie tardío, no confundir con "Unlicensed" en general — es un barómetro del final de vida útil de la consola). Necesario aparte del pack (PC) si interesa este contenido, no viene incluido en él.
   - Puede haber más variantes en la misma sección (ej. "Standard" plano, sin relación P/C) — confirmar en el propio portal cuáles están disponibles en cada visita, ya que no se ha hecho un barrido exhaustivo de todas.
4. Descomprimir el lote completo y extraer únicamente el `.dat` del sistema que necesites (ver "Notas" al final de esta guía para dónde colocarlo).

**Caso confirmado:** para sistemas de cartucho, seleccionar dentro del ZIP solo los sistemas de interés del catálogo completo — no hace falta procesar los que no interesan. Dos excepciones a tener en cuenta que **no** están cubiertas por ningún pack de No-Intro: `gx4000` (usa TOSEC, ver más abajo) y `sgb` (no tiene DAT propio — usa las mismas ROMs de `gb`/`gbc`, ejecutadas en modo Super Game Boy).

### Patrón de nombres de ficheros (No-Intro)

Los archivos descargados siguen convenciones de nombres estrictas que dependen del método de obtención:

- **Descargas individuales (Parent-Clone):** El portal genera de forma dinámica un archivo comprimido que sigue la estructura:
  `[Compañía] - [Nombre del Sistema] (Parent-Clone) ([YYYYMMDD-HHMMSS]).dat`
  *Ejemplo:* `Nintendo - Super Nintendo Entertainment System (Parent-Clone) (20260810-184522).dat`
- **Descarga del paquete diario (Daily Pack):** El contenedor principal se descarga bajo el nombre:
  `No-Intro Love Pack (PC) ([YYYYMMDD]).7z`
  *Ejemplo:* `No-Intro Love Pack (PC) (20260810).7z`
- **DATs extraídos del Daily Pack:** Al descomprimir el paquete diario, los archivos `.dat` individuales de su interior adoptan el nombre limpio oficial del proyecto sin marcas de tiempo:
  `[Compañía] - [Nombre del Sistema].dat`
  *Ejemplo:* `Nintendo - Game Boy Advance.dat`

**Nota técnica para automatización:** los gestores de ROMs avanzados (como RomVault o ClrMamePro) ignoran el nombre físico del archivo `.dat` en el disco. Validan el sistema leyendo directamente la cabecera interna del XML (`<header><name>`).

## Redump

**Fuente:** redump.org. La descarga de las bases de datos de verificación se realiza directamente desde la sección pública **Downloads** del menú principal. No requiere registro ni cuenta de usuario.

### Pasos de obtención (Redump)

1. Acceder al apartado global de **Downloads** en el menú superior del portal oficial de Redump.
2. Localizar el bloque central denominado **Datfiles**. Evita buscar sistema por sistema en el catálogo general del menú lateral, ya que allí se listan volcados individuales de discos y no el índice maestro.
3. Hacer clic sobre el nombre del sistema que deseas auditar. El portal descargará automáticamente un archivo comprimido (habitualmente en formato `.zip` o `.7z`) que contiene el listado de verificación en formato **Logiqx XML**.
4. **Descarga de ficheros de soporte auxiliares (Opcional pero crítico para el workflow):** En la misma página de descargas, desplázate hacia los bloques inferiores para obtener los recursos necesarios para sistemas basados en CD-ROM:
   - **Cuesheets:** Listados de pistas de audio/datos necesarios para sistemas como *Sega CD, PC Engine CD o PlayStation*.
   - **SBI files:** Firmas de datos de subcanal (subchannel data) imprescindibles para sortear la protección anticopia *LibCrypt* de los sistemas *PlayStation (PS1) europeos (PAL)*.

### Patrón de nombres de ficheros (Redump)

Los contenedores y archivos extraídos de Redump siguen un estricto patrón cronológico invertido:

- **Fichero comprimido descargado (DAT):** Adopta el nombre oficial del sistema seguido de la fecha de su última modificación en el servidor:
  `[Nombre del Sistema] ([YYYY-MM-DD]).zip`
  *Ejemplo:* `Sony - PlayStation (2026-07-22).zip`
- **DAT extraído en el disco duro:** Al descomprimir el archivo, mantiene la misma nomenclatura pero con la extensión técnica del formato:
  `[Nombre del Sistema] ([YYYY-MM-DD]).dat`
  *Ejemplo:* `Sony - PlayStation (2026-07-22).dat`
- **Paquetes de Cuesheets y SBI:** Los recopilatorios globales de archivos auxiliares se descargan bajo la estructura:
  `[Nombre del Sistema] - Cuesheets ([YYYY-MM-DD]).zip`
  `[Nombre del Sistema] - SBI files ([YYYY-MM-DD]).zip`

### Limitaciones técnicas de preservación (1G1R)

- **Ausencia de Atributo de Clones:** A diferencia de No-Intro, las bases de datos de Redump se exportan de forma nativa **sin la etiqueta `cloneofid`** (ver `docs/references.md#logiqx-xml-dat`). Redump trata cada edición física, revisión de disco o variante regional como una entidad única e independiente de preservación bit a bit.
- **Resolución del Romset:** Debido a esta carencia estructural, el agrupado y filtrado para obtener un set **1G1R (1 Game 1 ROM)** no se puede resolver analizando únicamente este archivo `.dat`. El gestor de ROMs o la herramienta de filtrado (como *Retool*) debe alimentarse de un diccionario externo de clonación secundario, procesando las relaciones mediante bases de datos de mapeo en formato JSON (`metadata/dat/retool/clonelists/*.json`) o aplicando algoritmos de concordancia basados en el nombre base del juego. **Fuente confirmada de esos ficheros:** github.com/unexpectedpanda/retool-clonelists-metadata (del mismo autor que retool), copia local completa en `metadata/dat/retool/` — carpeta `clonelists/` (ej. `Apple - Macintosh (Redump).json`), generadas automáticamente a partir de las bases de datos de Redump y No-Intro. El mismo repositorio incluye además `metadata/` (metadatos adicionales por juego, ej. idiomas), `mias/` (listas Missing In Action) y una carpeta `retroachievements/` (un JSON por sistema, con entradas `name`/`crc`/`md5`/`sha1` de los hashes verificados por RetroAchievements), más `scripts/` con las herramientas de mantenimiento propias del repositorio (validación/limpieza de clonelists, obtención de MIA/RA). **Corrección importante para este contexto (Redump/CHD):** ese hash **no es un hash del CHD ni del disco completo** — para sistemas ópticos, RetroAchievements usa un método propio (para PS1: localizar el ejecutable principal vía `SYSTEM.CNF`, concatenar su ruta+nombre con su contenido, y hashear eso), documentado explícitamente como que "nunca coincidirá con un hash de fichero completo". Comparar el CRC/MD5/SHA1 del DAT de Redump contra `retroachievements/*.json` **no sirve** para sistemas de disco; hace falta **RAHasher** para calcular el hash real comparable (ver [romset-audit.md](romset-audit.md#identificación-rápida-de-chdrvz-sin-descomprimir-rahasher)). Para sistemas de cartucho (No-Intro), el hash de RA sí suele coincidir con el hash estándar del fichero — ahí la comparación directa contra el DAT sí es válida.
- **Auditoría de archivos auxiliares (.cue/.sbi):** Los gestores de ROMs avanzados (como *RomVault* o *ClrMamePro*) pueden configurarse para validar la integridad y presencia de las hojas de ruta `.cue` y las firmas `.sbi` asociadas. Si la base de datos de Redump los incluye en su estructura, el gestor marcará una ROM como "Incompleta" si faltan estos metadatos periféricos, aunque los archivos `.bin` o `.iso` de datos sean correctos.
- **Control de versiones local:** Antes de sobrescribir el archivo en tu directorio local `metadata/dat/redump/`, extrae la cadena de fecha `[YYYY-MM-DD]` del nuevo archivo y compárala con la versión que ya tienes almacenada para verificar de forma rápida si el catálogo del sistema ha recibido actualizaciones o correcciones de hashes.

## Non-Redump

**Aclaración de alcance:** ni No-Intro ni Redump alojan ROMs, solo el DAT de verificación (hashes); los ficheros de juego en sí debe obtenerlos el usuario por su cuenta (plataformas comunitarias tipo Internet Archive, foros especializados). Esta sección cubre exclusivamente de dónde sacar el **DAT** Non-Redump, no las ROMs.

**Fuente primaria:** el propio portal **DAT-o-MATIC** de No-Intro (mismo login y mismo flujo de exportación ya descritos arriba en la sección No-Intro). DAT-o-MATIC agrupa bajo la categoría **"Non-Redump"** los sistemas cuyo volcado todavía no está verificado al estándar Redump (ej. Dreamcast, PlayStation 2, NAOMI, Apple-Bandai Pippin, Sharp Zaurus, BD-Video, DVD-Video). No es un repositorio GitHub aparte: basta con filtrar por esa categoría en el mismo desplegable de sistema del portal.

**Fuente secundaria** (huecos que DAT-o-MATIC no cubre, ej. PS3/Xbox 360): wiki de RomVault, sección `supported_dats` (`wiki.romvault.com/doku.php?id=supported_dats`), que documenta dos variantes relevantes:

- **`Non-Redump-Custom`** — juegos de PS3 y Xbox 360 de fuentes scene/P2P no presentes en la colección Redump.
- **`DeDupe-NoIntro`** — DAT Non-Redump de No-Intro con las imágenes ya presentes en Redump eliminadas, para evitar duplicados al combinar ambas colecciones.

### Patrón de nombres de ficheros (Non-Redump)

Sigue la misma convención que el resto de DAT-o-MATIC (ver "Patrón de nombres de ficheros" en la sección No-Intro), con la etiqueta `Non-Redump` insertada. Para los DAT de RomVault, consultar el nombre exacto en la propia wiki al momento de la descarga — no verificado aquí.

### Limitaciones técnicas de preservación (Non-Redump)

- **Tratamiento de clones:** al tratarse de sistemas sin volcado verificado, es habitual que no incluyan metadatos de parentesco (`cloneofid`) fiables. El filtrado 1G1R debe abordarse con cautela adicional en la fase 5.
- **Estabilidad de hashes:** al no estar verificados al estándar Redump, los hashes de estos sistemas pueden cambiar entre revisiones del DAT si se descubren volcados más limpios — comprobar la fecha de versión antes de dar por definitivo un audit ya realizado.

## TOSEC (The Old School Emulation Center)

**Fuente:** tosecdev.org (sitio oficial del proyecto TOSEC). El catálogo de verificación se distribuye de forma centralizada a través de la sección Downloads, o espejos comunitarios (Archive.org).

### Pasos de obtención (TOSEC)

1. Acceder a la sección de descargas oficial de TOSEC y localizar la versión del paquete maestro más reciente (ej. `TOSEC-vYYYY-MM-DD.zip`).
2. **Descarga en bloque:** El proyecto **no ofrece descargas individuales por sistema** en su web principal. Es obligatorio descargar el paquete acumulativo completo que contiene las bases de datos de todas las plataformas soportadas.
3. Descomprimir el archivo maestro en un directorio temporal.
4. Navegar por la estructura de carpetas interna, localizar el sistema microordenador o consola clásica que se desea auditar, y extraer únicamente sus archivos `.dat` hacia tu ruta local de metadatos.

### Patrón de nombres de ficheros (TOSEC)

TOSEC utiliza una convención de nomenclatura corporativa sumamente estricta y detallada que identifica de inmediato las variantes del sistema:

- **Archivo del paquete maestro:** `TOSEC-v[Año]-[Mes]-[Día].zip`
  *Ejemplo:* `TOSEC-v2026-04-20.zip`
- **DATs individuales internos:** Siguen el patrón de categorización del proyecto:
  `[Nombre del Sistema] - [Categoría] (TOSEC-v[Versión]).dat`
  *Ejemplos:* 
    - `Amstrad GX4000 - Games (TOSEC-v2026-04-20).dat`
    - `Commodore Amiga - Applications (TOSEC-v2026-04-20).dat`

### Limitaciones técnicas de preservación (TOSEC)

- **Filosofía de acumulación vs. Limpieza:** A diferencia de No-Intro, TOSEC busca preservar **absolutamente todo el espectro digital histórico**. Esto significa que sus DATs validarán alegremente volcados defectuosos (`[b]`), hacks de la época (`[h]`), intros de grupos de crackers (`[t]`) y copias corruptas. 
- **Incompatibilidad 1G1R nativa:** El formato Logiqx variante TOSEC carece de etiquetas de clonación (`cloneofid`) y utiliza códigos de región rígidos de dos letras (ver `docs/references.md#tosec`). Limpiar un set de TOSEC para dejar "un juego por región" es inviable mediante herramientas automatizadas estándar; requiere un filtrado manual exhaustivo o expresiones regulares complejas debido a la masiva cantidad de variantes de un mismo programa.
- **Ámbito de aplicación:** Se debe restringir su uso exclusivamente a microordenadores clásicos (Spectrum, Amstrad, Commodore) o sistemas huérfanos donde la cobertura de No-Intro sea deficiente o inexistente.

## MAME / FBNeo (Ecosistema Arcade)

A diferencia de los sistemas domésticos, el entorno Arcade no depende de listados comunitarios tradicionales para su validación principal. El archivo de verificación se genera o se extrae en sincronía matemática estricta con la compilación exacta del emulador que se va a utilizar para garantizar que las ROMs contengan los chips y placas base correctos.

### 1. MAME (Generación Local y Fuentes)

**Fuente Primaria:** El propio ejecutable oficial de MAME instalado en tu sistema. No se recomienda descargar un `.dat` genérico de internet si se dispone del emulador, ya que la más mínima variación de versión provocará errores de auditoría masivos debido a que MAME renombra, une o divide chips internos continuamente entre lanzamientos.

#### Pasos de obtención (Local)

1. Abrir la terminal de comandos (CMD, PowerShell o Bash) y situarse en el directorio raíz donde se encuentre instalado el emulador, o asegurarse de tener el ejecutable mapeado en las variables de entorno del sistema (`PATH`).
2. Ejecutar el comando nativo de volcado estructural para exportar la base de datos completa de máquinas soportadas por esa *build* específica:
   ```bash
   mame -listxml > mame.xml
   ```
3. Mover el archivo resultante `mame.xml` a tu directorio local de metadatos `metadata/dat/mame/`.

#### Fuentes alternativas en internet (si no se dispone del ejecutable)

- **Progetto-Snaps** — progettosnaps.net. Sitio de referencia de la comunidad Arcade; publica DATs de MAME completos, diffs entre versiones y DATs de Software List (SL), con historial desde versiones muy antiguas hasta la actual. Confirmado en uso real (sesión de bitácora) como fuente efectiva, no solo teórica.
- **renameSET.dat** — progettosnaps.net/renameset/. Registro histórico de renombrados de sets entre versiones de MAME (mapeo de identificadores mID); útil para sincronizar una colección tras una actualización de MAME que renombra sets existentes.
- **retropie-dat** — github.com/HerbFargus/retropie-dat. DAT de MAME/AdvMAME/FBA organizados por carpeta de **core exacto** (`lr-mame2003-plus`, `lr-mame2010`, `lr-fbneo`, `lr-fbalpha2012`, `gngeopi`...) — útil específicamente cuando el hardware objetivo corre un core antiguo/legacy y hace falta el DAT de esa versión concreta, no la más reciente. Mantenimiento limitado (20 commits, actividad reciente no confirmada) — ver `docs/references.md#preservación-y-gestión-de-dat`.

[TODO: verificar — se ha citado también un "MAME Clean DAT" (variante depurada del DAT completo, sin dispositivos huérfanos/drivers vacíos); no aparece entre las variantes listadas al comprobar directamente `progettosnaps.net/dats/MAME/`, pendiente de confirmar si existe con otro nombre o en otra sección del sitio]

#### Patrón de nombres de ficheros (MAME)

Al generarse de forma manual, se recomienda renombrarlo forzando la versión exacta del ejecutable para mantener el control de versiones en el workflow:

`mame_[v0.XXX].xml`

*Ejemplo:* `mame_v0.268.xml`

### 2. FBNeo (FinalBurn Neo)

**Fuente:** `metadat/fbneo-split/` dentro del repositorio **libretro-database** (ver sección [libretro-database](#libretro-database-clrmamepro-texto) más abajo) — confirmado que contiene el fichero `FinalBurn Neo (ClrMame Pro XML, Arcade only).dat`. No es el repositorio oficial de FBNeo, sino la importación que mantiene el equipo de Libretro.

**Aclaración técnica sobre el flag de volcado:** a diferencia de MAME, la versión por línea de comandos de FBNeo no tiene un flag equivalente a `-listxml` confirmado — de ahí que la vía práctica sea esta importación ya generada, no un volcado local.

#### Pasos de obtención (FBNeo)

1. Clonar o descargar `libretro-database` (ver [libretro-database](#libretro-database-clrmamepro-texto) más abajo para el comando de `git clone`).
2. Localizar el fichero en `metadat/fbneo-split/FinalBurn Neo (ClrMame Pro XML, Arcade only).dat`.

**Vías descartadas tras verificación:**

- **Repositorio oficial en GitHub** (`github.com/finalburnneo/FBNeo`) — comprobado que **no existe** una carpeta `dats/` en la raíz del repositorio (las carpetas reales son `.github`, `fbahelpfilesrc`, `projectfiles`, `src`, `tools`).
**Confirmado contra la wiki oficial de FBNeo** (`finalburnneo/FBNeo/wiki/menu_misc`): la interfaz gráfica de Windows (`fbneo.exe`) tiene la pestaña **Misc** con dos opciones — **"Generate dat file"** (una categoría concreta: arcade, o un sistema doméstico específico como Megadrive, PC-Engine, Sega Master System, MSX-1, ZX Spectrum...) y **"Generate all dats"** (todos a la vez). Formato de salida: ClrMamePro (XML). Detalle completo en `docs/arcade/arcade.md#anexo-procedimiento-para-generar-archivos-dat-personalizados`.

### Limitaciones técnicas de preservación (Arcade)

- **Sincronización Obligatoria de Versiones:** La regla de oro en Arcade dicta que **la versión del DAT debe coincidir con la versión del set de ROMs y la versión del emulador**. Si utilizas un DAT generado con MAME v0.268 para auditar un romset antiguo (ej. MAME v0.232), el gestor te indicará miles de archivos corruptos o faltantes, ya que las estructuras internas cambian para mejorar la fidelidad de la emulación.
- **Complejidad Estructural de Clones (Sets Divididos):** La jerarquía en este archivo XML cambia la etiqueta `<game>` por **`<machine>`**. Un clon en Arcade no es solo una variante regional; depende del juego "Padre" (Parent) para funcionar. En entornos *Split* (divididos), borrar o aislar incorrectamente un archivo Padre romperá de inmediato todos sus Clones, ya que estos carecen de las ROMs de la placa base común para arrancar.

## MAME Software Lists (`<softwarelist>`)

**Aclaración de alcance:** las Software Lists son catálogos integrados dentro del propio código de MAME para dar soporte a sistemas domésticos (consolas y microordenadores antiguos). No se descargan de internet de forma aislada; se vuelcan directamente desde el ejecutable del emulador para verificar cartuchos, disquetes, cintas o imágenes de disco (CHD) que se ejecutan a través de la arquitectura de MAME. Detalle del formato en `docs/references.md#software-lists`.

### Pasos de obtención (Software Lists)

#### Opción A: descarga directa (si no se dispone de MAME instalado)

- **Progetto-Snaps** — progettosnaps.net/dats/MAME/. Confirmado que ofrece **"SL" (Software List) DATs** como conjunto de datos separado del DAT arcade principal, disponible desde MAME v0.162 en adelante. Confirmado que se distribuye como paquete único comprimido (`SL_Dats_[versión].7z`).

  [TODO: verificar si al descomprimir ese paquete único aparecen ficheros `.dat` ya separados por sistema doméstico, o hay que filtrarlos manualmente — no se pudo confirmar sin descargar y descomprimir el archivo]

- **DATVault** — confirmado: es una **API integrada en RomVault (≥3.4)**, no un portal de descarga aparte (documentado en `wiki.romvault.com/doku.php?id=supported_dats` y `?id=what_is_datvault`). El propio programa RomVault se conecta a los servidores de DATVault para actualizar los DAT con un clic. Confirmadas tres variantes de Software Lists: **`MAME-SL`** (XML de la carpeta `hash` de la versión estable actual de MAME, incluye ROMs y CHDs), **`MAME-SL-Daily`** (desde los binarios diarios de MAME) y **`MAME-SL-CHD-Daily`** (solo CHD de los binarios diarios); también hay variantes "Merged"/"Split" que combinan todas las Software Lists en un único DAT. El acceso al DAT oficial `mame -listxml` es gratuito; el resto del repositorio (incluidas estas variantes SL) requiere clave de pago vía Patreon de RomVault.

#### Opción B: generación local

El volcado completo genera un XML masivo que engloba decenas de sistemas domésticos. **Confirmado en la documentación oficial de MAME:** el flag es `-listsoftware` (alias `-lsoft`), acepta opcionalmente un patrón/nombre de sistema para filtrar, y sin patrón vuelca todas las listas soportadas.

1. Abrir la terminal de comandos (CMD, PowerShell o Bash) y situarse en la raíz del directorio de instalación de MAME.
2. Volcado completo (todas las Software Lists soportadas por la build):
   ```bash
   mame -listsoftware > mame_softwarelists.xml
   ```
3. Mover el archivo resultante a tu directorio local de metadatos `metadata/dat/mame_sl/`.

**Extracción individual (recomendado si solo vas a auditar un sistema):** la documentación oficial de MAME sitúa el nombre del sistema **antes** del flag, no después:

```bash
mame megacd -listsoftware > mame_megacd.xml
```

*(Ejemplo documentado oficialmente: `mame coco3 -listsoftware`.)*

### Patrón de nombres de ficheros (Software Lists)

Al tratarse de una exportación manual controlada por el usuario, la nomenclatura en disco es libre, pero se recomienda estructurarla bajo la versión del emulador para evitar colisiones:

- **Volcado global:** `mame_softwarelists_[v0.XXX].xml`
  *Ejemplo:* `mame_softwarelists_v0.268.xml`
- **Volcado individual por sistema:** `mame_sl_[nombre_sistema]_[v0.XXX].xml`
  *Ejemplo:* `mame_sl_megacd_v0.268.xml`

### Limitaciones técnicas de preservación (Software Lists)

- **Estructura jerárquica distinta:** a diferencia del Logiqx (`<game>`) o del MAME Arcade (`<machine>`), las Software Lists usan la etiqueta raíz `<softwarelist>` y encapsulan cada juego bajo `<software name="...">` (ver `docs/references.md#etiquetas-sw-list-dat`); un parser propio para la fase de auditoría necesita este mapeo de etiquetas distinto.
- **Dependencia de CHD en sistemas ópticos:** en sistemas domésticos de CD-ROM emulados en MAME, el XML valida que el CHD coincida con el hash SHA-1 esperado por el driver (elemento `diskarea/disk`, ver `docs/references.md#etiquetas-sw-list-dat`).
- **Romsets de soporte (BIOS/dispositivos):** algunos sistemas de las Software Lists requieren volcados de BIOS o periféricos de expansión para arrancar, que no se listan dentro de la propia Software List sino en el DAT de MAME Arcade principal (`-listxml`); para auditar el set completo hace falta combinar ambos volcados. Sistemas citados con esta dependencia, **pendientes de verificar caso por caso contra el código fuente de MAME**: CD-ROM — `megacd`/`segacd` (BIOS regional de Sega), `pcecd` (PC Engine CD), `cdimono1` (Philips CD-i), `neocdz` (Neo-Geo CD); microordenadores — `amiga` (Kickstart de Commodore Amiga), `atari_xlxe` (Atari de 8 bits), `apple2`; consolas con coprocesador de cartucho — `snes` (juegos con Super FX/ST010, cuyas ROMs matemáticas están definidas como dispositivos en el DAT Arcade principal).

[TODO: la lista anterior no se ha verificado driver por driver contra el código fuente de MAME ni contra `docs/systems.md` — confirmar antes de tratarla como definitiva]

- **Sincronización estricta:** igual que con el set de recreativas, el catálogo de las Software Lists cambia con cada actualización de MAME — usar un listado de una versión distinta a la de los archivos provoca errores masivos en el gestor de ROMs.

## libretro-database (ClrMamePro texto)

**Fuente:** repositorio oficial del ecosistema RetroArch en GitHub, `github.com/libretro/libretro-database`. Su uso principal es servir como fuente de verificación para microordenadores clásicos, aventuras gráficas y entornos huérfanos que carecen de soporte o normalización en No-Intro o Redump.

### Pasos de obtención (libretro-database)

Para trabajar de forma ágil en entornos locales o de automatización, se recomienda clonar la biblioteca completa debido al peso ligero de sus archivos de texto:

1. Clonar el repositorio mediante Git en tu directorio de metadatos:
   ```bash
   git clone --depth 1 https://github.com/libretro/libretro-database.git
   ```
   El flag `--depth 1` descarga únicamente el último estado de la rama principal, evitando el histórico completo de commits.
2. Localizar el archivo `.dat` requerido navegando en la estructura interna del repositorio (verificado por índice de contenidos):
   - **`dat/`** — DATs nativos, construidos y mantenidos por el propio equipo de Libretro para sistemas sin cobertura adecuada en otras fuentes (ej. `ScummVM.dat`, `DOS.dat`, `HBMAME.dat`).
   - **`metadat/`** — importaciones de catálogos de terceros ya convertidos al formato ClrMamePro texto, organizadas en subcarpetas por fuente: `no-intro/`, `redump/`, `tosec/`, `mame/` (y variantes `mame-split/`, `mame-member/`, `mame-nonmerged/`), **`fbneo-split/` y `fbneo-member/`** — esta última contiene `FinalBurn Neo (ClrMame Pro XML, Arcade only).dat`, que resuelve el `[TODO]` dejado pendiente en la sección FBNeo más arriba. También incluye subcarpetas de metadatos puramente descriptivos sin relación con DAT (`genre/`, `developer/`, `publisher/`, `esrb/`...), no confundir con las de verificación.

### Patrón de nombres de ficheros (libretro-database)

Los archivos de este repositorio prescinden de marcas temporales en su nomenclatura y se organizan con nombres limpios orientados a la compatibilidad con los cores de emulación:

- **Estructura en disco:** `[Nombre_Sistema_o_Plataforma].dat`
  *Ejemplos:*
    - `ScummVM.dat`
    - `Magnavox - Odyssey2.dat`
    - `Sinclair - ZX 81.dat`

### Limitaciones técnicas de preservación (libretro-database)

- **Formato de texto plano:** a diferencia del resto de fuentes basadas en XML Logiqx, estos archivos usan el formato clásico de bloques de ClrMamePro (`game ( name "..." rom ( crc ... ) )`); cualquier parser automatizado de la fase de auditoría necesita un lector de bloques de paréntesis, no un lector XML (ver `docs/references.md#clrmamepro-dat-texto`).
- **Filosofía de indexación de RetroArch:** el propósito de estos DAT no es la preservación bit a bit purista, sino permitir el escaneo automático de RetroArch. Por eso usan **claves de emparejamiento alternativas**: CRC32 para cartuchos clásicos, pero para sistemas de disco (ej. PlayStation) usan directamente el **número de serie** grabado en el binario, para evitar calcular checksums sobre ficheros grandes (confirmado en el README del repositorio, sección "Key Field").
- **Reglas de Precedencia:** Si necesitas resolver colisiones o información conflictiva sobre una misma ROM en tu workflow, la arquitectura del repositorio dicta que las definiciones contenidas en la carpeta raíz `/dat/` sobrescriben y tienen prioridad absoluta sobre los metadatos almacenados en `/metadat/`.

## Generación manual desde directorio (DAT From Dir)

**No es una fuente externa** — se genera un DAT propio calculando los hashes reales de los ficheros ROM ya presentes en un directorio, en vez de descargarlo de ningún grupo de preservación. Último recurso cuando no existe DAT oficial para el sistema (No-Intro, Redump, Non-Redump, TOSEC, MAME/FBNeo, libretro) y ya se dispone de una colección organizada localmente cuya integridad se quiere fijar como referencia futura.

**Herramienta confirmada:** SabreTools, función **"DAT From Dir"** (flags `-d`, `--d2d` o `--dfd`). Escanea el directorio indicado y genera un DAT con CRC32, MD5 y SHA-1 de cada fichero encontrado; por defecto incluye la fecha de generación en el nombre del archivo de salida (desactivable con `-b`/`--no-automatic-date`).

```bash
SabreTools --dfd --output-type=xml --name=DatName Path\To\Files
```

El DAT resultante usa la fecha/nombre indicados, en formato Logiqx XML (`--output-type=xml`).

**Alternativa GUI:** Datfile Creator Studio (github.com/Eggmansworld/DatfileCreatorStudio) — misma idea que `SabreTools --dfd` pero con interfaz gráfica nativa, actualización incremental (solo recomputa ficheros nuevos/modificados en vez de rehacer todo el DAT cada vez), modos Mixed/Zipped, y utilidades adicionales (reparador de rutas largas, validador y fusionador de DAT).

### Limitaciones

- **No sustituye a un DAT oficial de verificación** — solo certifica que los hashes coinciden con lo que hay en disco *ahora mismo*; no confirma que esos ficheros sean volcados legítimos y libres de errores, que es justo lo que aportan No-Intro/Redump/TOSEC/MAME.
- **Sin relación Parent-Clone** — al generarse desde ficheros sueltos, no incluye `cloneofid` ni agrupado 1G1R; si se necesita, hay que aplicarlo aparte (fase 5).
- Útil sobre todo para fijar una fotografía de la colección actual antes de reorganizarla, o para colecciones de sistemas verdaderamente huérfanos sin ningún DAT disponible en ninguna otra fuente de esta guía.

## gamelist.xml (DAT de respaldo)

**No es una fuente de DAT** — `gamelist.xml` es un formato de organización/frontend, sin hashes obligatorios (ver `docs/references.md#etiquetas-gamelistxml`). Se documenta aquí solo como **último recurso** cuando ningún grupo de preservación (No-Intro, Redump, Non-Redump, TOSEC, MAME/FBNeo, libretro) cubre el sistema y ya existe una colección personal organizada con `gamelist.xml`.

**Método fiable:** ignorar el contenido del `gamelist.xml` y generar el DAT directamente a partir de los ficheros ROM en disco — ver [Generación manual desde directorio](#generación-manual-desde-directorio-dat-from-dir) más arriba (SabreTools DFD/D2D).

**Método alternativo confirmado:** **Rom Info Tools** (comunidad HyperSpin, `hyperspin-fe.com/files/file/18409-rom-info-tools/`, Windows). Convierte entre formatos de base de datos compatibles (XML/TXT/DAT), incluyendo explícitamente `gamelist.xml`, `nointrodat.dat`, `hyperspin.xml`, `mamelist.xml`, `mameinfo.dat`, `mamehistory.dat`, `retrofe_include.txt`. Entre sus funciones: crear un DAT estilo No-Intro o HyperSpin **a partir de una carpeta de ROMs**, extraer/fusionar información entre formatos, y renombrar ROMs según el fichero de referencia. Cubre este caso — parsear `gamelist.xml` y producir un DAT compatible con gestores tradicionales.

Comprobado que **gamelist-utils no soporta esta conversión** — solo transforma entre formatos de frontend (EmulationStation, RetroArch, SimpleMenu, muOS, Onion, ES-DE), no a DAT/Logiqx; usar Rom Info Tools para este caso en su lugar.

## HyperList XML

**Aclaración de alcance:** HyperList es un formato de organización/frontend de HyperSpin, sin hashes obligatorios (el campo `crc` es opcional y heredado del DAT de origen, ver `docs/references.md#etiquetas-hyperlist`). No es una fuente de DAT de verificación equivalente a No-Intro/Redump/TOSEC/MAME — se documenta aquí porque existe una fuente oficial real de estos XML, útil para poblar el frontend HyperSpin, y porque puede servir de referencia de nombres al construir un DAT propio (ver "Generación de DAT" más abajo).

### Fuente

**hyperspin-fe.com** — el foro sigue operativo (verificado: responde con bloqueo anti-bot, no está caído). Recurso oficial confirmado: **"HyperSpin Official Databases 1.0"**, hyperspin-fe.com/files/file/25951-hyperspin-official-databases/ — publicado por la cuenta oficial `HyperSpin`, contiene 127 ficheros con las bases de datos oficiales de todos los sistemas en un único zip (2.04 MB, HyperBase 2.1, actualizado 2024-05-27), **excepto MAME** (para MAME, el propio autor recomienda usar la base de datos comunitaria v0.236 incluida en el paquete por ser más completa que la oficial). Requiere cuenta gratuita del foro para descargar. El propio autor advierte que este pack no cubre todos los sistemas del sitio — hay bases de datos no oficiales adicionales navegando el foro por sistema.

**Archive.org** — como respaldo si el foro no es accesible: existen ítems individuales dispersos por sistema (ej. `sega-ringedge` → "Sega Ringedge Hyperspin Database"), no un pack unificado equivalente al oficial.

### Generación de DAT (a partir de una colección ya auditada)

Si lo que se necesita es un DAT de verificación real (no solo el XML de organización de HyperSpin), la vía fiable es generarlo desde los ficheros ROM ya auditados contra No-Intro/Redump/TOSEC — ver [Generación manual desde directorio](#generación-manual-desde-directorio-dat-from-dir) más arriba — no parsear el HyperList XML, que no garantiza hashes completos.

Ni RomVault ni ClrMamePro exportan de forma nativa a formato HyperList XML. Se ha citado **DATUtil** (herramienta de Logiqx, el propio creador del formato Logiqx XML) como posible pasarela, pero verificado que su función real es convertir XML a formato **RomCenter**, no a HyperList — la referencia parece incorrecta, no la doy por válida para este caso.

**Herramientas confirmadas** que sí cubren este caso — toman el XML maestro de HyperList (ver "Fuente" más arriba) y lo cruzan contra una carpeta de ROMs ya auditada para generar un HyperList a medida con solo los juegos que se poseen:

- **Rom Info Tools** (ver sección `gamelist.xml` más arriba) — entre sus formatos soportados incluye `hyperspin.xml` como destino.
- **HyperSpin Database Creator** — github.com/swhook52/HyperSpinDatabaseCreator (código abierto, no requiere cuenta de foro). Toma la ruta al XML completo de HyperSpin y la carpeta de ROMs, compara ambos y genera un fichero `*_custom.xml` con solo los juegos presentes en la carpeta; el XML original queda intacto. Requiere renombrar manualmente el resultado al nombre que espera HyperSpin (ver "Patrón de nombres de ficheros" más abajo).
- **Don's HyperSpin List Generator** (`hyperspin-fe.com/files/file/5602-dons-hyperspin-tools/`) — recorta el XML maestro para mostrar solo las ROMs presentes en las carpetas locales; incluye auditor integrado de wheels/artwork/temas faltantes y detector de nombres mal escritos entre el directorio y la lista.

### Patrón de nombres de ficheros (HyperList)

HyperList requiere una correspondencia exacta de nombres de archivo para que el frontend no falle. El XML maestro de cada sistema debe llamarse igual que el nombre interno que HyperSpin tiene registrado para ese sistema:

- **Estructura fija en disco:** `[Nombre_Exacto_Del_Sistema].xml`
  *Ejemplos:*
  - `Nintendo Entertainment System.xml`
  - `Sega Mega Drive.xml`
  - `Sony PlayStation.xml`

**Nota de ubicación:** el XML no va en la carpeta de ROMs; se coloca en `HyperSpin/Databases/[Nombre_Exacto_Del_Sistema]/[Nombre_Exacto_Del_Sistema].xml`, dentro de la instalación del frontend.

### Limitaciones técnicas de preservación (HyperList)

- **Catálogo no siempre al día:** al ser un pack estático (última actualización confirmada: 2024-05-27), puede no incluir prototipos, volcados corregidos o revisiones que No-Intro/Redump añaden después de esa fecha.
- **Sin cobertura de hacks/homebrew:** los listados oficiales cubren solo el catálogo comercial de la época; traducciones fan o juegos independientes modernos requieren añadir manualmente las entradas `<game name="...">` correspondientes.

## Notas

Una vez descargado o generado, el DAT se guarda en `metadata/dat/<Fuente>/` (archivo crudo, tal cual se descarga). Para que `tools/scripts/build-dat-index-*.ps1` lo indexe tiene que estar en la copia de trabajo `sources/dats/<fuente>/`: para No-Intro esa sincronización la hace `tools/scripts/update-sources.ps1`, a partir del manifiesto de sistemas usados en `tools/scripts/config/nointro-systems.json`; el resto de fuentes, de momento, se siguen leyendo directamente de `metadata/dat/<Fuente>/` hasta migrarlas al mismo patrón — ver [custom-pipeline.md](../romsets/custom-pipeline.md).

Conservar el DAT anterior hasta confirmar que el nuevo audita correctamente contra el romset existente (fase 3): un DAT corrupto o de una versión inconsistente puede marcar como inválido un set que en realidad está bien.

**Formatos deliberadamente fuera de esta guía:** Playlist RetroArch (`.lpl`) y RetroArch RDB (`.rdb`) — ver `docs/references.md#formatos` — no se cubren como fuente principal porque son artefactos derivados, no un DAT que se obtenga por separado: el `.rdb` lo compila el propio equipo de RetroArch/libretro a partir de los DAT de No-Intro/Redump, y el `.lpl` lo genera RetroArch localmente al escanear una carpeta contra su `.rdb`.

Si en algún momento hiciera falta reconstruir un DAT a partir de uno de estos dos ficheros (ej. recuperar información desde un dispositivo sin acceso al DAT original):

- **RDBEd** (github.com/schellingb/RDBEd) — confirmado: editor open-source de `.rdb`, lee y escribe tanto `.rdb` como `.dat` (formato ClrMamePro); función **"File → Export DAT"** para exportar el contenido cargado a DAT, y **"Tools → Dump RDB File"** para volcar el `.rdb` a texto legible. Cubre la reconstrucción desde `.rdb`.
- **`.lpl` → DAT:** sin herramienta confirmada. Se ha citado la utilidad `dir2dat` del ecosistema libretro, pero verificado que funciona en la dirección contraria (genera un DAT **desde un directorio de ROMs**, que después se usa para compilar el `.rdb` — igual que SabreTools DFD/D2D, no una conversión inversa desde `.lpl`).

[TODO: sin herramienta confirmada para reconstruir un DAT directamente desde `.lpl`; mientras tanto, la vía más fiable sigue siendo [Generación manual desde directorio](#generación-manual-desde-directorio-dat-from-dir) sobre los ficheros ROM reales]
