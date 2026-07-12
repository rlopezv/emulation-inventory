# Referencias técnicas

Glosario de conceptos, fuentes de datos y herramientas de gestión para romsets, DATs y colecciones.

---

## Romsets arcade

Colección completa de archivos ZIP o 7z que contienen los volcados de memoria (dumps) de los chips integrados en las placas originales de las recreativas.

### Tipos

- **Split** — El juego base (parent) contiene los archivos comunes. Las versiones alternativas o regionales (clones) solo contienen sus archivos modificados y dependen del parent para funcionar.
- **Non-Merged** — Cada archivo ZIP contiene absolutamente todo lo necesario para arrancar el juego (tanto los archivos del parent como los del clon), siendo archivos totalmente independientes pero más pesados.
- **Merged** — El parent y todos sus clones asociados se empaquetan juntos dentro de un único archivo ZIP común.

### Parent / Clone

El Parent es la versión principal o más completa de un juego de arcade (normalmente la versión internacional o la más reciente). El Clone es cualquier variante directa de este (versiones regionales, bootlegs, hacks o revisiones anteriores).

### BIOS

Archivos que contienen el sistema operativo básico o el firmware de la placa madre del arcade (por ejemplo, `neogeo.zip`). Son indispensables para arrancar cualquier juego de ese sistema.

### Samples

Archivos de audio digitalizado externo (en formato WAV o FLAC) que no se pudieron volcar de los chips originales de la placa y que el emulador necesita para reproducir efectos de sonido o voces analógicas.

---

## Romsets de sistemas domésticos

Colección de imágenes de software (ROMs, imágenes de disco o casetes) de sistemas domésticos. A diferencia del arcade, no emulan una placa física de recreativa, sino el medio de almacenamiento extraíble diseñado para el consumidor.

### Formatos comunes

- **ROM individuales / Planas** — Archivos `.nes`, `.smc`, `.gb` que contienen el volcado directo del chip del cartucho.
- **Imágenes ópticas** — Formatos `.bin/.cue`, `.iso`, `.img` que preservan pistas de datos y audio analógico de sistemas basados en CD/DVD.

### Grupos de preservación

Organizaciones de la scene encargadas de estandarizar las firmas digitales (hashes) para garantizar copias perfectas:

- **No-Intro** — Centrado en sistemas basados en cartuchos y descargas digitales. Su meta es el volcado puro sin modificaciones, grietas (cracks), cabeceras de emulador obsoletas ni traducciones.
- **Redump** — Especializado en sistemas basados en soporte óptico (CD, DVD, GD-ROM, Blu-ray). Garantizan copias 1:1 exactas byte a byte de los discos comerciales de fábrica.
- **TOSEC** — (The Old School Emulation Center). Dedicado principalmente a la preservación de ordenadores antiguos (Amiga, Commodore, Spectrum, Amstrad, MSX), incluyendo software comercial, de dominio público, demos, aplicaciones y variantes modificadas históricas.

---

## Convenciones de nombrado

Estructura de campos y flags usados por cada fuente de romset para nombrar sus entradas. Necesario para saber qué parser/heurística de región aplica a cada DAT (ver `docs/romsets.md#formato-de-dat`).

### No-Intro

Formato estructural estándar:

```text
Nombre del Juego (Región) (Idiomas) (Información Adicional) (Revisión)
```

- **Nombre del Juego** — título comercial exacto, solo ASCII estándar (sin acentos ni diéresis, se simplifican).
- **Región** — región geográfica del lanzamiento oficial, palabra completa o combinación habitual (`(USA)`, `(Europe)`, `(Japan)`, `(World)`, `(Germany)`).
- **Idiomas** — siglas de idioma separadas por coma dentro de un único paréntesis (`(En,Fr,De,Es,It)`).
- **Información Adicional** — solo si el cartucho original tuvo una condición física especial en tienda (`(Beta)`, `(Proto)`, `(Unl)` para juegos sin licencia oficial).
- **Revisión** — versiones corregidas lanzadas posteriormente en tienda, al final de todo (`(Rev 1)`, `(Rev A)`).

Flags principales:

| Flag | Significado | Descripción |
| --- | --- | --- |
| `(Proto)` | Prototype | Versiones tempranas o prototipos de desarrollo oficiales |
| `(Beta)` | Beta | Versiones de prueba que no llegaron a estado final de distribución |
| `(Unl)` | Unlicensed | Juegos comerciales físicos vendidos sin pagar la licencia oficial (ej. Camerica, Color Dreams) |
| `(Sample)` | Kiosk / Demo | Versiones colocadas en muebles expositores de tiendas para prueba limitada |
| `(Virtual Console)` | Re-release digital | Versión extraída de la tienda digital de Nintendo Wii/Wii U/3DS |
| `(NP)` | Nintendo Power | Juegos grabados en cartuchos flash especiales en quioscos oficiales de Japón |

No existe una etiqueta de "buen volcado" (como el `[!]` de TOSEC): al ser una base de datos de preservación limpia, que un juego esté en el catálogo ya garantiza implícitamente que es un clon exacto y perfecto de la memoria del chip original.

### Redump

Sigue la misma estructura limpia que No-Intro (ambos grupos colaboran y comparten guía de convención), con parámetros adicionales para discos múltiples, números de serie y ediciones especiales, propios de soporte óptico.

Formato estructural estándar:

```text
Nombre del Juego (Región) (Idiomas) (Discos/Versiones) (Edición)
```

- **Nombre del Juego** — título oficial limpio; Redump conserva de forma estricta mayúsculas, puntuación y subtítulos tal como aparecían en la carátula física.
- **Región** — región geográfica oficial del lanzamiento del disco.
- **Idiomas** — códigos de idioma de dos letras, ordenados alfabéticamente y separados por coma.
- **Información de Discos** — obligatoria si el juego requiere varios soportes físicos (`(Disc 1)`, `(Disc 2)`).
- **Edición o Versión** — tipo de relanzamiento comercial si no es la primera edición (`(Franchise Edition)`, `(Demo)`, `(Beta)`).

Flags principales:

| Flag | Significado | Descripción |
| --- | --- | --- |
| `(Disc 1)` | Multi-disco | Número del disco correspondiente en la caja del juego |
| `(v1.01)` | Versión de software | Actualización de fábrica grabada en las pistas de datos del disco |
| `(Promo)` | Edición promocional | Discos impresos para distribución a prensa o eventos previos al lanzamiento |
| `(Covermount)` | Regalo con revista | Juegos completos oficiales en CD regalados al comprar revistas del sector |
| `(Made in...)` | Lugar de prensado | Solo si el país de fabricación produce variaciones binarias respecto al resto del mundo |

Al igual que No-Intro, Redump no usa etiquetas de "buen volcado" tipo `[!]`: solo admite imágenes binarias perfectas verificadas comparando volcados de múltiples usuarios; estar en su lista ya garantiza copia exacta del original físico de fábrica.

### Non-Redump

Cubre contenido que Redump no acepta en su base principal (prototipos, betas, contenido digital, versiones en tránsito de validación). Formato estructural estándar:

```text
Nombre del Juego (Región) (Idiomas) (Información Digital/Tienda) [Etiquetas de Control]
```

Etiquetas clave:

| Etiqueta | Significado | Descripción |
| --- | --- | --- |
| `!pc-platform-[os]` | Plataforma de PC | Sistema operativo del juego digital (ej. `!pc-platform-windows`, `!pc-platform-linux`) |
| `(Digital)` | Lanzamiento digital | El juego nunca existió en formato físico, obtenido de tienda en línea |
| `[On redump]` | Ya en Redump | Etiqueta de control temporal: el archivo se deslistará porque Redump ya lo aceptó en su base principal |
| `[Archive UUID: x]` | Identificador único | Código alfanumérico largo para rastrear el archivo binario exacto en los servidores |
| `(DLC)` / `(Update)` | Contenido extra | Expansiones o parches de juego digital |

### TOSEC

Formato estructural estándar (orden estricto):

```text
Nombre del Juego vX.XX (Año)(Editor)[Idiomas/Región][Flags de Estado]
```

- **Nombre del Juego** — título oficial sin abreviar.
- **Versión** — pegada al título, separada solo por un espacio (`v1.0`, `Rev 1`, `v2026`); no lleva paréntesis.
- **Año** — año de publicación entre paréntesis; si se desconoce, `(19xx)` o `(20xx)`.
- **Editor** — compañía distribuidora entre paréntesis; si es desconocido, un guion (`-`).
- **Idiomas / Región** — entre corchetes cuadrados: `[a]` alemán, `[es]` español, `[f]` francés, o códigos combinados como `[M3]`/`[M5]` (Multilenguaje 3/5).
- **Flags de Estado** — calidad/tipo del volcado; el más buscado es `[!]` (volcado verificado perfecto).

Flags de calidad de dump más comunes:

| Flag | Significado | Descripción |
| --- | --- | --- |
| `[!]` | Verified Good Dump | Archivo 100% auténtico, completo y libre de errores |
| `[b]` | Bad Dump | El volcado falló o está corrupto (datos faltantes o no carga) |
| `[f]` | Fixed | Juego modificado para arreglar un error que impedía emularlo |
| `[h]` | Hacked | ROM modificada por usuarios (traducciones de fans, trucos integrados, etc.) |
| `[o]` | Overdump | El archivo contiene más datos de los necesarios al final de la ROM |
| `[cr]` | Cracked | Software al que se le ha removido la protección contra copia física |
| `[t]` | Trained | Incluye un menú inicial (trainer) para activar vidas infinitas o trucos |

### libretro

RetroArch/libretro no tiene un formato de nombrado propio: adopta el de No-Intro, Redump o TOSEC según el tipo de sistema. El escáner de RetroArch no depende tanto del nombre de fichero como del **hash interno (CRC32/MD5)**: al escanear una carpeta, busca coincidencia en su base de datos (`.rdb`) y asigna un nombre limpio uniforme en la playlist.

| Categoría de sistema | Convención adoptada | Formato esperado |
| --- | --- | --- |
| Consolas de cartucho (NES, SNES, Mega Drive, GBA...) | No-Intro | `Nombre del Juego (Región) (Idiomas)` |
| Consolas de disco (PS1, Saturn, Sega CD, Dreamcast...) | Redump (secundario: TOSEC) | `Nombre del Juego (Región) (Idiomas) (Disc X)` |
| Computadoras clásicas y arcade (Amstrad CPC/GX4000, ZX Spectrum, Commodore, MAME/FBNeo) | TOSEC / FBNeo | `Nombre del Juego vX.XX (Año)(Editor)[!]` |

Si las ROMs no siguen el nombre exacto de la convención esperada, el juego sigue funcionando pero **no se descargan carátulas ni thumbnails automáticamente**, ya que el servidor de imágenes de RetroArch indexa por ese nombre exacto.

---

## gamelist.xml

Formato estándar de metadatos de EmulationStation (y derivados como ES-DE) para describir los juegos de un sistema. Se ubica en la raíz de la carpeta del sistema, junto a las ROMs y la carpeta `media/`.

### Formato estándar

```xml
<gameList>
    <game>
        <path>./supermario.smc</path>
        <name>Super Mario World</name>
        <desc>Mario must rescue the Dinosaur Land and the Mushroom Princess from Bowser.</desc>
        <image>./media/images/supermario.png</image>
        <thumbnail>./media/thumbnails/supermario.png</thumbnail>
        <video>./media/videos/supermario.mp4</video>
        <marquee>./media/marquee/supermario.png</marquee>
        <releasedate>19901121T000000</releasedate>
        <developer>Nintendo</developer>
        <publisher>Nintendo</publisher>
        <genre>Platformer</genre>
        <players>2</players>
        <rating>0.85</rating>
        <hash>abc123456</hash>
        <favorite>true</favorite>
        <hidden>false</hidden>
    </game>
</gameList>
```

### Etiquetas

| Etiqueta | Descripción |
| --- | --- |
| `path` | Ruta relativa al archivo ROM del juego, desde la carpeta del sistema |
| `name` | Nombre del juego mostrado en el frontend |
| `desc` | Descripción o sinopsis del juego |
| `image` | Ruta relativa a la imagen principal (carátula o captura destacada) |
| `thumbnail` | Ruta relativa a la miniatura usada en listados |
| `video` | Ruta relativa al vídeo de vista previa (gameplay) |
| `marquee` | Ruta relativa al logo/marquesina del juego |
| `releasedate` | Fecha de lanzamiento en formato `YYYYMMDDTHHMMSS` |
| `developer` | Estudio o persona desarrolladora del juego |
| `publisher` | Editora responsable de la publicación |
| `genre` | Género del juego |
| `players` | Número de jugadores soportados |
| `rating` | Puntuación normalizada entre 0 y 1 |
| `hash` | Hash de verificación del archivo ROM asociado |
| `favorite` | Marca el juego como favorito (`true`/`false`) |
| `hidden` | Oculta el juego del listado sin eliminarlo (`true`/`false`) |

---

## Software Lists

Estándar moderno de MAME utilizado para catalogar y estructurar colecciones de juegos que pertenecen a sistemas domésticos (consolas, ordenadores o sistemas de discos) en lugar de placas puramente de recreativa.

### Diferencias respecto a DATs arcade

Mientras que el DAT arcade define el hardware físico soldado a una placa única, las Software Lists definen los medios de almacenamiento externos (cartuchos, disquetes, casetes o CDs) que se insertan en un sistema específico.

### Casos de uso

- **Sistemas CD** — Gestión estructural de imágenes binarias complejas.
- **Consolas** — Validación de catálogos exactos por región.
- **Ordenadores** — Configuración automatizada de expansiones de RAM o periféricos necesarios para arrancar un disquete.
- **CHDs** — Vinculación inequívoca entre el archivo de datos hash y el volcado del disco óptico.

---

## CHDs

Compressed Hunks of Data. Formato oficial de compresión sin pérdida creado por el equipo de MAME para almacenar imágenes de discos duros, CDs, DVDs y LaserDiscs.

### Uso en arcade

Se utiliza para almacenar los datos masivos de juegos de recreativa modernos que dependían de un disco duro interno o una unidad de CD-ROM (como Killer Instinct, Beatmania o la placa Capcom CHD).

### Uso en sistemas CD

Es el formato de referencia moderno para comprimir juegos de consolas basadas en disco óptico (PS1, PS2, Sega CD, Saturn, Dreamcast, PC Engine CD) reduciendo el tamaño drásticamente sin perder pistas de audio o datos.

### Relación con romsets ZIP

El archivo ZIP contiene la ROM con el código base del hardware de inicio del juego, mientras que el archivo `.chd` externo (ubicado en una carpeta con el mismo nombre que el ZIP) contiene la imagen del disco de datos pesada. Ambos son necesarios para arrancar el título.

---

## 1G1R

1 Game 1 ROM (Un Juego, Una ROM). Técnica de filtrado de catálogos que busca eliminar la redundancia dejando una única copia perfecta de cada título en el listado final, priorizando la región óptima del usuario.

### Reglas regionales

Criterio de prioridades geográficas configurado en el gestor de DATs (ej. `EUR > USA > JPN`). El programa conservará la versión europea; si no existe, buscará la americana, y en su defecto, la japonesa.

### Exclusiones

Filtros aplicados para purgar el set de archivos innecesarios de cara a la experiencia de juego final:

- **Demos** — Muestras comerciales o jugables incompletas.
- **Betas** — Versiones de desarrollo con bugs.
- **Prototypes** — Ediciones preliminares no comerciales.
- **Rev menores** — Revisiones o parches de software antiguos del mismo juego que no aportan cambios significativos.

### Cuarentena de exclusivos regionales

Cuando el 1G1R prioriza una región (ej. `EUR > USA > JPN`) y descarta un título porque solo existe en japonés, ese descarte no se elimina sin más: se mueve a una subcarpeta `japan/` dentro del set 1G1R correspondiente (ver `data/dats/console/1g1r/japan/`), a la espera de una revisión específica (traducción disponible, relevancia del título, etc.) antes de decidir si se incorpora al set final o se descarta definitivamente.

---

## DATs

### FBNeo DAT

FinalBurn Neo (ClrMame Pro XML, Arcade only).

**Fuente** — Repositorio oficial de FBNeo en GitHub o generado localmente mediante el propio ejecutable del emulador con el comando integrado de volcado XML.

**Uso recomendado** — Ideal para dispositivos de baja potencia o arquitectura ARM (Raspberry Pi, consolas portátiles retro, sistemas Android) debido a su altísima optimización de rendimiento en sistemas clásicos de 8, 16 y 32 bits. Sistemas cubiertos: NeoGeo, CPS1, CPS2, CPS3, Cave.

### MAME DAT

El estándar definitivo de preservación absoluta en PC de gama media/alta. Debe usarse siempre que se busque la máxima fidelidad de emulación y cuando el hardware receptor soporte la carga de cómputo del MAME moderno.

**Generación** — `mame -listxml > mame.xml`

**Sistemas cubiertos** — Arcade general, Naomi, Naomi2, Atomiswave.

### No-Intro DATs

**Uso recomendado** — Obligatorio para auditar, purgar, renombrar y aplicar la estrategia 1G1R en consolas basadas en cartuchos y medios digitales (NES, SNES, Megadrive, N64, GBA, etc.).

**Fuente oficial** — Portal web Datomatic de No-Intro.

**Variantes** — Permite descargar DATs estándar o estructurados en esquemas P/C (Parent-Clone) para facilitar el cribado regional automatizado.

### Redump DATs

**Uso recomendado** — Indispensable para auditar colecciones de discos antes de convertirlas a formato CHD (PS1, Saturn, Dreamcast, PS2, GameCube).

**Fuente oficial** — Redump.org.

**Particularidad** — Solo aceptan y validan volcados que coincidan de forma exacta con los bytes físicos de los discos comerciales inalterados.

### MAME Software Lists

Colección de archivos XML descriptivos empaquetados junto al núcleo de MAME que detallan las firmas hash (CRC, SHA1) exactas de los juegos domésticos de consola y ordenador conocidos.

| MAME Software Lists | MAME -listxml |
| --- | --- |
| Sistemas CD/consolas | Arcade |
| Software | Hardware arcade |
| CHDs ópticos | ROM arcade |
| XML por sistema | XML global |

---

## Herramientas de gestión

### ClrMamePro

Software clásico de PC para auditar, reconstruir, recortar y renombrar romsets masivos. Es la herramienta nativa más robusta para procesar tanto sets de MAME/FBNeo como colecciones No-Intro utilizando sus correspondientes archivos DAT XML.

### RomCenter

Alternativa visual y moderna a ClrMamePro estructurada como una interfaz de base de datos plana. Es altamente eficiente para reparar de forma rápida nombres incorrectos de archivos ZIP y verificar extensiones de consolas clásicas en lotes.

### JRomManager

Gestor de romsets multiplataforma de código abierto escrito en Java. Destaca por su entorno intuitivo para automatizar filtros 1G1R usando ficheros DAT de No-Intro que incluyan relaciones jerárquicas de padres e hijos.

### retool

Herramienta de línea de comandos (unexpectedpanda/retool) para generar y aplicar reglas de agrupación 1G1R sobre DATs No-Intro/Redump, incluyendo el mapeo de variantes regionales usado en `metadata/dat/clonelist/*.json`. También se usa para producir los DAT curados de `data/dats/console/` (variantes `fullset` y `1g1r` por sistema).

---

## Referencias externas

| Nombre | Enlace | Descripción |
| --- | --- | --- |
| SBC Gaming Handhelds Database | Ver Google Sheet | Base de datos comunitaria en Google Sheets para comparar especificaciones y límites de emulación de consolas portátiles. |
| Retro Game Corps | retrogamecorps.com | Portal de referencia global para guías de configuración, tutoriales y análisis de hardware. |
| Retro Handhelds | retrohandhelds.gg | Noticias de la scene, análisis de hardware, guías de compra y comunidad activa. |
| Joey's Retro Handhelds | joeysretrohandhelds.com | Guías de optimización rápida, configuraciones de emuladores y análisis de sistemas operativos. |
| RetroCatalog | retrocatalog.com | Catálogo visual de consolas portátiles clásicas y modernas orientado al coleccionismo. |
| RGHandhelds Specs | rghandhelds.com | Base de datos de componentes técnicos de portátiles chinas populares. |
| RetroAchievements | retroachievements.org | Plataforma comunitaria de logros y trofeos para emulación retro. |
| OnionOS Wiki | onionui.github.io | Documentación oficial de Onion OS para Miyoo Mini. |
| PortMaster | portmaster.games | Ports nativos de PC para consolas Linux de bajo coste. |
| r/sbcgaming (Reddit) | reddit.com/r/sbcgaming | Foro global sobre SBCs, alertas de ofertas y soporte técnico. |
| Handhelds Wiki | handhelds.wiki | Wiki comunitaria con fichas técnicas, comparativas y datos de emulación de handhelds retro modernos. |
| OpenDingux (retrogamehandheld) | github.com/retrogamehandheld/OpenDingux | Repositorio comunitario con builds de OpenDingux para dispositivos portátiles retro, incluyendo el GKD350H. |
| LineageOS Retroid Pocket 2 | drive.google.com/drive/folders/1pSDVxLSOLqMirmPENWf2sdxrDKfOLd6z | Builds comunitarias de LineageOS (Android 8.1 v2) para Retroid Pocket 2. |
| LineageOS RP2 — Retro Game Corps | retrogamecorps.com/2021/03/21/lineageos-android-8-1-on-retroid-pocket-2 | Guía de instalación de LineageOS Android 8.1 en Retroid Pocket 2. |

---

## Notas operativas

### Pendientes

- Configurar el filtro de regiones para el script de borrado automatizado 1G1R en JRomManager.
- Validar la integridad del set completo de CHD para PS1 usando herramientas de Redump.

### Problemas conocidos

- Los juegos de Naomi 2 sufren caídas de frames intermitentes bajo arquitecturas ARM de bajo coste si no se activa el salto de fotogramas (frame skip).

### Compatibilidades

- La versión de MAME recomendada debe sincronizarse siempre con la revisión exacta del DAT descargado para evitar problemas de firmas perdidas.
