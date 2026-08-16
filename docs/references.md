# Referencias técnicas

Glosario de conceptos, fuentes de datos y herramientas de gestión para romsets, DATs y colecciones.

---

## Conceptos

### Romsets arcade

Colección completa de archivos ZIP o 7z que contienen los volcados de memoria (dumps) de los chips integrados en las placas originales de las recreativas.

#### Tipos

- **Split** — El juego base (parent) contiene los archivos comunes. Las versiones alternativas o regionales (clones) solo contienen sus archivos modificados y dependen del parent para funcionar.
- **Non-Merged** — Cada archivo ZIP contiene absolutamente todo lo necesario para arrancar el juego (tanto los archivos del parent como los del clon), siendo archivos totalmente independientes pero más pesados.
- **Merged** — El parent y todos sus clones asociados se empaquetan juntos dentro de un único archivo ZIP común.

#### Parent / Clone

El Parent es la versión principal o más completa de un juego de arcade (normalmente la versión internacional o la más reciente). El Clone es cualquier variante directa de este (versiones regionales, bootlegs, hacks o revisiones anteriores).

#### BIOS

Archivos que contienen el sistema operativo básico o el firmware de la placa madre del arcade (por ejemplo, `neogeo.zip`). Son indispensables para arrancar cualquier juego de ese sistema.

#### Samples

Archivos de audio digitalizado externo (en formato WAV o FLAC) que no se pudieron volcar de los chips originales de la placa y que el emulador necesita para reproducir efectos de sonido o voces analógicas.

### Romsets de sistemas domésticos

Colección de imágenes de software (ROMs, imágenes de disco o casetes) de sistemas domésticos. A diferencia del arcade, no emulan una placa física de recreativa, sino el medio de almacenamiento extraíble diseñado para el consumidor.

#### Formatos comunes

- **ROM individuales / Planas** — Archivos `.nes`, `.smc`, `.gb` que contienen el volcado directo del chip del cartucho.
- **Imágenes ópticas** — Formatos `.bin/.cue`, `.iso`, `.img` que preservan pistas de datos y audio analógico de sistemas basados en CD/DVD.

#### Grupos de preservación

Organizaciones de la scene encargadas de estandarizar las firmas digitales (hashes) para garantizar copias perfectas:

- **No-Intro** — Centrado en sistemas basados en cartuchos y descargas digitales. Su meta es el volcado puro sin modificaciones, grietas (cracks), cabeceras de emulador obsoletas ni traducciones.
- **Redump** — Especializado en sistemas basados en soporte óptico (CD, DVD, GD-ROM, Blu-ray). Garantizan copias 1:1 exactas byte a byte de los discos comerciales de fábrica.
- **TOSEC** — (The Old School Emulation Center). Dedicado principalmente a la preservación de ordenadores antiguos (Amiga, Commodore, Spectrum, Amstrad, MSX), incluyendo software comercial, de dominio público, demos, aplicaciones y variantes modificadas históricas.

### CHDs

Compressed Hunks of Data. Formato oficial de compresión sin pérdida creado por el equipo de MAME para almacenar imágenes de discos duros, CDs, DVDs y LaserDiscs.

#### Uso en arcade

Se utiliza para almacenar los datos masivos de juegos de recreativa modernos que dependían de un disco duro interno o una unidad de CD-ROM (como Killer Instinct, Beatmania o la placa Capcom CHD).

#### Uso en sistemas CD

Es el formato de referencia moderno para comprimir juegos de consolas basadas en disco óptico (PS1, PS2, Sega CD, Saturn, Dreamcast, PC Engine CD) reduciendo el tamaño drásticamente sin perder pistas de audio o datos.

#### Relación con romsets ZIP

El archivo ZIP contiene la ROM con el código base del hardware de inicio del juego, mientras que el archivo `.chd` externo (ubicado en una carpeta con el mismo nombre que el ZIP) contiene la imagen del disco de datos pesada. Ambos son necesarios para arrancar el título.

### 1G1R

1 Game 1 ROM (Un Juego, Una ROM). Técnica de filtrado de catálogos que busca eliminar la redundancia dejando una única copia perfecta de cada título en el listado final, priorizando la región óptima del usuario.

#### Reglas regionales

Criterio de prioridades geográficas configurado en el gestor de DATs (ej. `EUR > USA > JPN`). El programa conservará la versión europea; si no existe, buscará la americana, y en su defecto, la japonesa.

#### Exclusiones

Filtros aplicados para purgar el set de archivos innecesarios de cara a la experiencia de juego final:

- **Demos** — Muestras comerciales o jugables incompletas.
- **Betas** — Versiones de desarrollo con bugs.
- **Prototypes** — Ediciones preliminares no comerciales.
- **Rev menores** — Revisiones o parches de software antiguos del mismo juego que no aportan cambios significativos.

#### Cuarentena de exclusivos regionales

Cuando el 1G1R prioriza una región (ej. `EUR > USA > JPN`) y descarta un título porque solo existe en japonés, ese descarte no se elimina sin más: se mueve a una subcarpeta `japan/` dentro del set 1G1R correspondiente (ver `data/dats/console/1g1r/japan/`), a la espera de una revisión específica (traducción disponible, relevancia del título, etc.) antes de decidir si se incorpora al set final o se descarta definitivamente.

---

## Formatos

### Formatos de preservación y organización

Tres categorías de formato con propósitos distintos: verificar la integridad de una ROM, organizarla visualmente en un frontend, o acelerar su lectura en un dispositivo con recursos limitados.

#### Formatos de preservación y auditoría

Verifican mediante hashes (CRC32, MD5, SHA1) que las ROMs son copias perfectas, legítimas y libres de errores de lectura.

- **Logiqx XML (`.dat`/`.xml`)** — el estándar universal para consolas y ordenadores clásicos. Organiza la base de datos mediante las etiquetas `<datafile>`/`<game>`. Es el formato nativo de No-Intro, Redump y TOSEC (ver `Convenciones de nombrado` más abajo y `docs/romsets.md#formato-de-dat`).
- **MAME XML (`.dat`/`.xml`)** — el estándar para sistemas arcade. Mucho más complejo por las dependencias de hardware; usa las etiquetas `<mame>`/`<machine>` e incluye información de chips, pantallas y placas.
- **SW List Dat** — variante de MAME estructurada con la etiqueta `<softwarelist>`, especializada en cartuchos o disquetes de consolas emuladas bajo el entorno de MAME. Ver la sección `Software Lists` más abajo para el detalle completo.

#### Formatos de organización y frontends

No contienen hashes de verificación. Su única función es almacenar metadatos estéticos (año, género, desarrollador) y enlazar las ROMs con imágenes, vídeos o manuales en la interfaz gráfica.

- **HyperList (`.xml`)** — el formato clásico y pionero del frontend HyperSpin. Vincula los nombres exactos de archivo con los elementos multimedia de la ruleta de juegos. DATs en `metadata/dat/hyperspin/`.
- **Gamelist (`.xml`)** — el formato estándar en sistemas basados en Linux/Raspberry Pi (Batocera, Recalbox, RetroPie, EmulationStation). Guarda rutas de ROMs junto a sinopsis, carátulas y vídeos locales. Ver la sección `gamelist.xml` más abajo para el esquema completo.
- **Playlist de RetroArch (`.lpl`)** — listas de reproducción en texto plano (JSON), generadas por los menús internos de RetroArch; asocian cada ROM con su core correspondiente.

#### Formatos de bases de datos binarias

- **RetroArch RDB (`.rdb`)** — ROM Database. Conversión binaria compacta (basada en MessagePack) de los DAT de No-Intro y Redump, optimizada para que los dispositivos lean miles de hashes a máxima velocidad durante el escaneo de directorios sin saturar la RAM.

### Convenciones de nombrado

Estructura de campos y flags usados por cada fuente de romset para nombrar sus entradas. Necesario para saber qué parser/heurística de región aplica a cada DAT (ver `docs/romsets.md#formato-de-dat`).

#### No-Intro

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

##### Caso especial — Nintendo 64: orden de bytes (byte order)

Un mismo cartucho de N64 se puede volcar en tres variantes de orden de bytes, todas con idéntico contenido pero distinto hash:

| Extensión | Orden de bytes | Notas |
| --- | --- | --- |
| `.z64` | Big Endian | Formato nativo del cartucho real; el que usa No-Intro como estándar de auditoría |
| `.v64` | Byte Swapped | Formato histórico de dispositivos como el Doctor V64 |
| `.n64` | Little Endian | Variante menos común |

Los primeros 4 bytes del ROM son un "magic number" (`80 37 12 40` en big-endian correcto) que sirve para detectar y corregir el orden de bytes si no coincide. No-Intro cambió su romset de Byte Swapped a Big Endian; el DAT actual solo referencia hashes en `.z64` — un volcado en `.v64`/`.n64` no auditará correctamente contra el DAT sin convertirlo antes al orden de bytes esperado.

##### Caso especial — Headered vs. Headerless (NES, SNES, Atari 7800, Atari Lynx, FDS)

Bloque extra de bytes **prepuesto** al volcado real del cartucho por los copiadores/adaptadores de la época (o por convenciones de emulador posteriores), para guardar metadatos de emulación (mapper, mirroring, tamaño de RAM...) que el propio cartucho original no contiene. No forma parte del contenido original — es un añadido externo, a diferencia del caso de N64 de arriba, donde el "problema" es solo el orden de los bytes del contenido real.

| Sistema | Formato de cabecera | Tamaño | Extensión con cabecera | Extensión sin cabecera |
| --- | --- | --- | --- | --- |
| NES | iNES / NES 2.0 | 16 bytes | `.nes` | `.nes` (mismo, sin bloque inicial) |
| SNES | SMC (copier header) | 512 bytes | `.smc` | `.sfc` |
| Famicom Disk System | fwNES/FDS | 16 bytes | `.fds` | `.fds` (mismo, sin bloque inicial) |
| Atari 7800 | A78 | 128 bytes | `.a78` | `.a78` (mismo, sin bloque inicial) |
| Atari Lynx | LNX | 64 bytes | `.lnx` | `.lyx` |

No-Intro publica DAT **Headered** y **Headerless** por separado para los sistemas donde aplica (NES es el caso más citado); el SNES headerless (`.sfc`, sin cabecera SMC) es el predominante en el set actual de No-Intro. Auditar con el DAT equivocado (headered contra un romset sin cabecera, o viceversa) produce un hash distinto y el gestor de ROMs marcará el fichero como inválido aunque el contenido del juego sea correcto — comprobar cuál de los dos usa `docs/romsets.md`/el gestor de ROMs antes de dar un set por corrupto.

#### Redump

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

#### Non-Redump

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

#### TOSEC

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

#### libretro

RetroArch/libretro no tiene un formato de nombrado propio: adopta el de No-Intro, Redump o TOSEC según el tipo de sistema. El escáner de RetroArch no depende tanto del nombre de fichero como del **hash interno (CRC32/MD5)**: al escanear una carpeta, busca coincidencia en su base de datos (`.rdb`) y asigna un nombre limpio uniforme en la playlist.

| Categoría de sistema | Convención adoptada | Formato esperado |
| --- | --- | --- |
| Consolas de cartucho (NES, SNES, Mega Drive, GBA...) | No-Intro | `Nombre del Juego (Región) (Idiomas)` |
| Consolas de disco (PS1, Saturn, Sega CD, Dreamcast...) | Redump (secundario: TOSEC) | `Nombre del Juego (Región) (Idiomas) (Disc X)` |
| Computadoras clásicas y arcade (Amstrad CPC/GX4000, ZX Spectrum, Commodore, MAME/FBNeo) | TOSEC / FBNeo | `Nombre del Juego vX.XX (Año)(Editor)[!]` |

Si las ROMs no siguen el nombre exacto de la convención esperada, el juego sigue funcionando pero **no se descargan carátulas ni thumbnails automáticamente**, ya que el servidor de imágenes de RetroArch indexa por ese nombre exacto.

### Logiqx XML (DAT)

> Formato de preservación/auditoría — ver también `Formatos de preservación y organización` más arriba.

Formato nativo de No-Intro, Redump y TOSEC. Cada `<game>` es una familia de un mismo lanzamiento (con sus posibles clones regionales) y cada `<rom>` dentro de él uno de sus ficheros verificables por hash.

#### Formato estándar (Logiqx XML)

```xml
<?xml version="1.0"?>
<!DOCTYPE datafile PUBLIC "-//Logiqx//DTD ROM Management Datafile//EN" "http://www.logiqx.com/Dats/datafile.dtd">
<datafile>
    <header>
        <name>Nintendo - Super Nintendo Entertainment System</name>
        <description>Nintendo - Super Nintendo Entertainment System (Parent-Clone)</description>
        <version>20260101</version>
        <author>No-Intro</author>
    </header>
    <game name="Super Mario World (USA)">
        <description>Super Mario World (USA)</description>
        <rom name="Super Mario World (USA).sfc" size="524288" crc="b19cd7db" md5="6b47bb75d16514b6a476aa0c73a683a" sha1="0e7a591520c56106367c8e9c9d4d5d7b8b0b7c9"/>
    </game>
    <game name="Super Mario World (Europe)" cloneof="Super Mario World (USA)">
        <description>Super Mario World (Europe)</description>
        <rom name="Super Mario World (Europe).sfc" size="524288" crc="a1b2c3d4" md5="..." sha1="..."/>
    </game>
</datafile>
```

#### Etiquetas (Logiqx XML)

| Etiqueta | Descripción |
| --- | --- |
| `header/name` | Identificador corto del sistema cubierto por el DAT |
| `header/description` | Descripción completa, suele indicar si es set Parent-Clone |
| `header/version` | Fecha o número de versión del DAT (control de actualizaciones) |
| `header/author` | Grupo que mantiene el DAT (No-Intro, Redump, TOSEC) |
| `game@name` | Nombre completo del lanzamiento, con región/idiomas/flags según la convención de la fuente |
| `game@cloneof` | Referencia al `name` del juego padre; presente en No-Intro/Non-Redump, ausente en Redump (el agrupado 1G1R se resuelve por nombre base o clonelist) |
| `rom@name` | Nombre de archivo esperado |
| `rom@size` | Tamaño en bytes |
| `rom@crc` / `rom@md5` / `rom@sha1` | Hashes de verificación de integridad |

### MAME XML (DAT)

> Formato de preservación/auditoría — ver también `Formatos de preservación y organización` más arriba.

Estándar para arcade, generado localmente con `mame -listxml` (no se descarga como fichero suelto). Cada `<machine>` describe una placa completa: no solo los ROMs, también los chips, pantallas y dependencias de hardware necesarias para que el driver funcione.

#### Formato estándar (MAME XML)

```xml
<?xml version="1.0"?>
<!DOCTYPE mame>
<mame build="0.263">
    <machine name="sf2" sourcefile="cps1.cpp">
        <description>Street Fighter II: The World Warrior (World 910522)</description>
        <year>1991</year>
        <manufacturer>Capcom</manufacturer>
        <rom name="sf2e.03" size="131072" crc="a303af92" sha1="..." region="maincpu" offset="0"/>
        <device_ref name="z80"/>
        <display type="raster" rotate="0" width="384" height="224" refresh="59.633739"/>
        <driver status="good"/>
    </machine>
    <machine name="sf2ce" cloneof="sf2" romof="sf2">
        <description>Street Fighter II': Champion Edition (World 920513)</description>
        <year>1992</year>
        <manufacturer>Capcom</manufacturer>
    </machine>
</mame>
```

#### Etiquetas (MAME XML)

| Etiqueta | Descripción |
| --- | --- |
| `machine@name` | Nombre corto del set (nombre del ZIP sin extensión) |
| `machine@cloneof` | Set padre lógico (para agrupado Parent-Clone) |
| `machine@romof` | Set del que hereda ROMs físicamente (relevante para sets `Split`/`Merged`, ver `Romsets arcade` más arriba) |
| `description` | Título completo, con región/revisión entre paréntesis |
| `year` / `manufacturer` | Año de lanzamiento y fabricante de la placa |
| `rom@region` | Chip o subsistema al que pertenece el dump (`maincpu`, `gfx1`, `soundcpu`...) |
| `display@rotate` | Orientación de pantalla (`0`/`90`/`180`/`270`), relevante para bartop |
| `driver@status` | Estado de emulación del set (`good`, `imperfect`, `preliminary`) |

### ClrMamePro (DAT texto)

> Formato de preservación/auditoría — ver también `Formatos de preservación y organización` más arriba.

Formato de texto plano anterior a Logiqx XML, todavía en uso por **libretro-database** para sistemas sin cobertura adecuada en No-Intro/Redump/TOSEC (`spectrum`, `zx81`, `scummvm`, `dos`). Requiere un parser distinto al XML.

#### Formato estándar (ClrMamePro texto)

```text
clrmamepro (
    name "libretro-database | ZX Spectrum"
    description "libretro | ZX Spectrum"
    version 20260101
    author "libretro"
)

game (
    name "Chuckie Egg"
    description "Chuckie Egg"
    rom ( name "Chuckie Egg.tzx" size 47616 crc a1b2c3d4 md5 6b47bb75d16514b6a476aa0c73a683a sha1 0e7a591520c56106367c8e9c9d4d5d7b8b0b7c9 )
)
```

#### Campos

| Campo | Descripción |
| --- | --- |
| `clrmamepro/name` | Identificador corto del sistema cubierto por el DAT |
| `clrmamepro/description` | Descripción completa del DAT |
| `clrmamepro/version` | Fecha o número de versión |
| `game/name` | Nombre del lanzamiento (define el nombre de carpeta/archivo si el set es multi-ROM) |
| `rom/name` | Nombre de archivo esperado |
| `rom/size` | Tamaño en bytes |
| `rom/crc` / `rom/md5` / `rom/sha1` | Hashes de verificación de integridad |

### Software Lists

> Formato de preservación/auditoría (SW List Dat) — ver también `Formatos de preservación y organización` más arriba.

Estándar moderno de MAME utilizado para catalogar y estructurar colecciones de juegos que pertenecen a sistemas domésticos (consolas, ordenadores o sistemas de discos) en lugar de placas puramente de recreativa.

#### Formato estándar (SW List Dat)

```xml
<?xml version="1.0"?>
<!DOCTYPE softwarelist SYSTEM "softwarelist.dtd">
<softwarelist name="snes" description="Nintendo Super Famicom/Super NES cartridge software">
    <software name="smw">
        <description>Super Mario World (USA)</description>
        <year>1990</year>
        <publisher>Nintendo</publisher>
        <part name="cart" interface="snes_cart">
            <dataarea name="rom" size="524288">
                <rom name="smw.sfc" size="524288" crc="b19cd7db" sha1="0e7a591520c56106367c8e9c9d4d5d7b8b0b7c9"/>
            </dataarea>
        </part>
    </software>
</softwarelist>
```

Para sistemas ópticos, `part`/`dataarea` se sustituyen por `part`/`diskarea` con un elemento `disk` (hash SHA1 del CHD en vez de CRC/SHA1 del ROM):

```xml
<part name="cdrom1" interface="cdrom">
    <diskarea name="cdrom">
        <disk name="ff7 (usa) (disc 1)" sha1="..."/>
    </diskarea>
</part>
```

#### Etiquetas (SW List Dat)

| Etiqueta | Descripción |
| --- | --- |
| `softwarelist@name` | Identificador corto del sistema cubierto (coincide con el driver MAME del sistema doméstico) |
| `softwarelist@description` | Descripción completa del sistema |
| `software@name` | Nombre corto de la entrada (nombre del set) |
| `description` | Título completo del lanzamiento |
| `year` / `publisher` | Año de lanzamiento y editora |
| `part@interface` | Tipo de medio/conector emulado (`snes_cart`, `cdrom`, `floppy_5_25`...) |
| `dataarea/rom` | Dump de cartucho/disquete, con hash CRC32/SHA1 |
| `diskarea/disk` | Dump de disco óptico (CHD), identificado por SHA1 en vez de CRC |

#### Diferencias respecto a DATs arcade

Mientras que el DAT arcade define el hardware físico soldado a una placa única, las Software Lists definen los medios de almacenamiento externos (cartuchos, disquetes, casetes o CDs) que se insertan en un sistema específico.

#### Casos de uso

- **Sistemas CD** — Gestión estructural de imágenes binarias complejas.
- **Consolas** — Validación de catálogos exactos por región.
- **Ordenadores** — Configuración automatizada de expansiones de RAM o periféricos necesarios para arrancar un disquete.
- **CHDs** — Vinculación inequívoca entre el archivo de datos hash y el volcado del disco óptico.

### HyperList

> Formato de organización/frontend — ver también `Formatos de preservación y organización` más arriba.

Formato del frontend HyperSpin, orientado a bartop/cabinet. No contiene hashes de verificación: el atributo `game@name` debe coincidir exactamente con el nombre de archivo de la ROM (sin extensión) para que el frontend vincule cada entrada con su ROM y con los elementos multimedia (wheel art, marquee, vídeo) alojados en carpetas separadas, no referenciados dentro del propio XML. DATs en `metadata/dat/hyperspin/`.

#### Formato estándar (HyperList)

```xml
<?xml version="1.0" encoding="UTF-8"?>
<menu>
    <game name="Super Mario World">
        <description>Super Mario World</description>
        <cloneof></cloneof>
        <crc></crc>
        <manufacturer>Nintendo</manufacturer>
        <year>1990</year>
        <genre>Platform</genre>
        <rating>5</rating>
        <enabled>Yes</enabled>
    </game>
</menu>
```

#### Etiquetas (HyperList)

| Etiqueta | Descripción |
| --- | --- |
| `game@name` | Debe coincidir exactamente con el nombre de archivo de la ROM (sin extensión); es la clave de enlace con los ficheros de media |
| `description` | Nombre mostrado en la ruleta de HyperSpin |
| `cloneof` | Set padre, heredado del DAT arcade de origen cuando aplica (vacío en sistemas sin relación Parent-Clone) |
| `crc` | Hash CRC32, opcional, heredado del DAT de origen |
| `manufacturer` | Desarrollador o distribuidor del juego |
| `year` | Año de lanzamiento |
| `genre` | Género del juego |
| `rating` | Puntuación, escala `0`-`5` |
| `enabled` | Muestra u oculta la entrada en la ruleta (`Yes`/`No`) sin eliminarla del XML |

### gamelist.xml

> Formato de organización/frontend — ver también `Formatos de preservación y organización` más arriba.

Formato estándar de metadatos de EmulationStation (y derivados como ES-DE) para describir los juegos de un sistema. Se ubica en la raíz de la carpeta del sistema, junto a las ROMs y la carpeta `media/`.

#### Formato estándar (gamelist.xml)

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

#### Etiquetas (gamelist.xml)

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

### Playlist de RetroArch (.lpl)

> Formato de organización/frontend — ver también `Formatos de preservación y organización` más arriba.

Lista de reproducción generada por el menú interno de RetroArch al escanear una carpeta de ROMs contra su base `.rdb`. Texto plano en JSON; cada entrada asocia una ROM con el core que debe cargarla, evitando tener que seleccionar el core manualmente cada vez.

#### Formato estándar (.lpl)

```json
{
    "version": "1.5",
    "default_core_path": "",
    "default_core_name": "",
    "label_display_mode": 0,
    "right_thumbnail_mode": 0,
    "left_thumbnail_mode": 0,
    "sort_mode": 0,
    "items": [
        {
            "path": "/roms/snes/Super Mario World (USA).sfc",
            "label": "Super Mario World (USA)",
            "core_path": "/cores/snes9x_libretro.so",
            "core_name": "Nintendo - SNES / SFC (Snes9x)",
            "crc32": "b19cd7db|crc",
            "db_name": "Nintendo - Super Nintendo Entertainment System.lpl"
        }
    ]
}
```

#### Campos (.lpl)

| Campo | Descripción |
| --- | --- |
| `items[].path` | Ruta absoluta al archivo ROM |
| `items[].label` | Nombre mostrado en el menú de RetroArch, tomado de la base `.rdb` si el hash coincide |
| `items[].core_path` | Core libretro asignado para lanzar la entrada |
| `items[].core_name` | Nombre legible del core |
| `items[].crc32` | Hash CRC32 usado para el emparejamiento contra la `.rdb`, no el nombre de archivo |
| `items[].db_name` | Base de datos `.rdb` de origen del emparejamiento (identifica el sistema) |

### RetroArch RDB (.rdb)

> Formato de bases de datos binarias — ver también `Formatos de preservación y organización` más arriba.

Conversión binaria compacta (basada en MessagePack) de los DAT de No-Intro y Redump, una por sistema, distribuida junto a RetroArch. No es legible como texto ni editable a mano; su único propósito es que el escáner interno resuelva miles de hashes contra nombre limpio a máxima velocidad sin cargar un XML completo en RAM en dispositivos de bajos recursos.

#### Estructura (.rdb)

Cada registro serializado equivale a los mismos campos que su DAT Logiqx XML de origen (nombre, CRC32, MD5, SHA1, tamaño), pero empaquetados en binario. Se genera con la herramienta interna `retroarch --database` o se descarga ya compilada desde el repositorio `libretro-database` (carpeta `rdb/`).

#### Notas (.rdb)

- No mantener editado manualmente en el repo: si se necesita modificar la base de un sistema, editar el DAT Logiqx XML de origen y regenerar el `.rdb`, no al revés.
- El emparejamiento en RetroArch se hace por hash (ver `libretro` en `Convenciones de nombrado` más arriba), no por nombre de archivo.

---

## Fuentes de DAT

Fuentes concretas de descarga/generación de DAT, organizadas por grupo de preservación. Para el formato de fichero de cada una (Logiqx XML, MAME XML, ClrMamePro texto...) ver `Formatos de preservación y organización` más arriba; para qué fuente usa cada sistema del inventario, ver `docs/romsets.md`; para el flujo de obtención paso a paso, ver `docs/guides/romsets/workflow.md`.

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

### Non-Redump DATs

**Uso recomendado** — Fuente alternativa cuando no hay DAT Redump disponible: prototipos/betas que Redump no acepta en su base principal, o sistemas sin cobertura Redump todavía (PS3, PSP, Xbox 360).

**Fuente oficial** — Repositorio comunitario en GitHub (ver enlace por sistema en `docs/romsets.md`).

**Particularidad** — No garantiza la misma exactitud byte a byte que Redump; cubre contenido que Redump rechaza explícitamente de su base principal.

### TOSEC DATs

**Uso recomendado** — Microcomputers sin cobertura adecuada en No-Intro (ej. `gx4000`) y preservación de ordenadores clásicos en general.

**Fuente oficial** — tosecdev.org, como set completo de todas las plataformas en un único paquete (hay que extraer solo el/los DAT del sistema necesario).

**Particularidad** — Convención de nombre distinta a No-Intro/Redump (fecha antes que región, códigos de región de 2 letras); ver `Convenciones de nombrado` más arriba.

### libretro DATs

**Uso recomendado** — Sistemas sin cobertura adecuada en las fuentes anteriores (ej. `spectrum`, `zx81`, `scummvm`, `dos`).

**Fuente oficial** — Repositorio `libretro-database` en GitHub.

**Particularidad** — Formato de texto plano ClrMamePro, no XML Logiqx; requiere un parser distinto (ver `docs/romsets.md#formato-de-dat`).

### WHDLoad DAT

**Uso recomendado** — Fuente primaria para `amiga`: catálogo WHDLoad (Commodore Amiga), un juego = un `.lha` con carga instantánea sin pantallas de disquetera, frente al `.ADF` original que requiere emular la disquetera físicamente.

**Fuente oficial** — `github.com/MrV2K/WHDLoad-Database`, generado a partir de los DAT oficiales del proyecto Retroplay (repositorio histórico de la escena WHDLoad). Publica el mismo catálogo en varios formatos (JSON/XML/CSV/XLSX y DAT ClrMamePro); se usa el DAT ClrMamePro (`Commodore - Amiga - WHDLoad.dat`), con checksums CRC32/MD5/SHA1 por rom. Copiado a `metadata/dat/WHDLoad/`.

**Particularidad** — No es un DAT de preservación de volcado original (no certifica bytes físicos de disquete como TOSEC/No-Intro): cataloga paquetes WHDLoad ya modificados para arrancar desde disco duro virtual, con parches de compatibilidad aplicados por la comunidad. Formato de texto plano ClrMamePro, no XML Logiqx.

### RetroAchievements como fuente de datos

No es una fuente de DAT de preservación (no certifica volcados perfectos como No-Intro/Redump/TOSEC) — es una fuente complementaria de **hashes de identificación** y **parches de traducción**, con tres formas de acceso a los mismos datos, todas confirmadas y trazables al mismo origen:

**1. API web en vivo** — `api-docs.retroachievements.org`. Requiere clave API personal (sección "Keys" del panel de control de la cuenta), pasada como parámetro `y` en cada petición. No exponer la clave públicamente.

- `API_GetGame.php` — metadatos básicos de un juego (título, consola, editora, género, fecha):

  ```bash
  curl "https://retroachievements.org/API/API_GetGame.php?y=TU_API_KEY&i=1"
  ```

- `API_GetGameHashes.php` — hashes de ROM vinculados a un juego, incluyendo `Labels` (ej. `nointro`, `rapatches`) y `PatchUrl` cuando existe un parche de traducción asociado:

  ```bash
  curl "https://retroachievements.org/API/API_GetGameHashes.php?i=14402&y=TU_API_KEY"
  ```

  ```json
  {
    "Results": [
      {
        "MD5": "1b1d9ac862c387367e904036114c4825",
        "Name": "Sonic The Hedgehog (USA, Europe) (Ru) (NewGame).md",
        "Labels": ["nointro", "rapatches"],
        "PatchUrl": "https://github.com/RetroAchievements/RAPatches/raw/main/MD/Translation/Russian/1-Sonic1-Russian.zip"
      }
    ]
  }
  ```

**2. RAHashes** — github.com/RetroAchievements/RAHashes. La base de datos de hashes en sí, la fuente que consulta la API. Organizada por grupo de origen: `No Intro`, `Redump`, `TOSEC`, `Final Burn Neo`, `Legacy`, `OpenGood`, `MAME`, entre otras. En revisión activa por el propio equipo a fecha de esta consulta.

**3. RAPatches** — github.com/RetroAchievements/RAPatches. Repositorio de parches de traducción y similares, referenciado desde `PatchUrl` en la respuesta de la API. Complementa a `docs/guides/tools/patching.md` como fuente adicional de parches, no cubierta ahí.

**Réplica estática semanal (sin API):** `retool-clonelists-metadata/retroachievements/` (ver más abajo, tabla de enlaces) — un JSON por sistema con entradas `name`/`crc`/`md5`/`sha1`, sin necesidad de clave API ni conexión en el momento de usarlo.

**Importante — el hash de RA no siempre es un hash de fichero completo.** Para sistemas de cartucho (No-Intro), suele coincidir con el hash estándar del ROM, así que comparar directamente contra un DAT (Logiqx, o cualquier gestor tipo RomVault/ClrMamePro/RomCenter) funciona. Para **sistemas ópticos (Redump/CHD/RVZ) no funciona igual**: RA usa un método propio por consola — para PS1, por ejemplo, localiza el ejecutable principal vía `SYSTEM.CNF`, concatena su ruta+nombre con su contenido, y hashea ese conjunto; la documentación oficial de RetroAchievements lo indica explícitamente ("the RA hash will never match a full-file hash"). Ningún gestor de ROMs genérico puede reproducir esto calculando un CRC/MD5/SHA1 normal del CHD/RVZ o del volcado reconstruido — hace falta **RAHasher**, que implementa el algoritmo específico de RA por consola (ver `docs/guides/tools/romset-audit.md#identificación-rápida-de-chdrvz-sin-descomprimir-rahasher`).

**Herramientas relacionadas** (catalogadas en `docs/tools.md`): **RAHasher** (hashea CHD/RVZ directamente sin descomprimir, ver `docs/guides/tools/romset-audit.md#identificación-rápida-de-chdrvz-sin-descomprimir-rahasher`) y **RA ROM Processor** (Docker, organiza/verifica/desduplica una biblioteca completa cruzándola contra la base de hashes de RA, con scraping de metadatos vía SkyScraper integrado).

---

## Herramientas

Catálogo completo de herramientas de PC para gestión, validación, conversión, scraping y parcheo de romsets/DATs: ver `docs/tools.md`.

---

## Enlaces externos

### Preservación y gestión de DAT

| Nombre | Enlace | Descripción |
| --- | --- | --- |
| No-Intro DAT-o-MATIC | datomatic.no-intro.org | Portal oficial de descarga de DAT No-Intro; detalle de uso en `docs/guides/tools/dat-generation.md#no-intro-dat-o-matic`. |
| Redump | redump.org | Portal oficial de descarga de DAT Redump (sección Datfiles); detalle de uso en `docs/guides/tools/dat-generation.md#redump`. |
| TOSEC | tosecdev.org | Portal oficial del proyecto TOSEC; detalle de uso en `docs/guides/tools/dat-generation.md#tosec-the-old-school-emulation-center`. |
| libretro-database | github.com/libretro/libretro-database | Repositorio de DAT ClrMamePro texto y catálogos importados de terceros (No-Intro, Redump, TOSEC, MAME, FBNeo); detalle de uso en `docs/guides/tools/dat-generation.md#libretro-database-clrmamepro-texto`. |
| Eggmansworld/Datfiles | github.com/Eggmansworld/Datfiles | Colección curada de DAT de nicho, organizados para RomVault: arcade ambience, computadoras clásicas (C64, VIC20, Sharp X68000), pinball, máquinas tragamonedas, visual novels, Touhou, RPG Maker, iPod Clickwheel Games — contenido sin cobertura en No-Intro/Redump/TOSEC/libretro-database. |
| HerbFargus/retropie-dat | github.com/HerbFargus/retropie-dat | DAT de MAME/AdvMAME/FBA organizados por carpeta de core exacto (`lr-mame2003-plus`, `lr-mame2010`, `lr-fbneo`, `lr-fbalpha2012`, `gngeopi`...) — útil para sincronizar el DAT con la versión de core instalada en hardware de baja potencia con cores antiguos. Mantenimiento limitado (20 commits, actividad reciente no confirmada). |
| RAHashes | github.com/RetroAchievements/RAHashes | Base de datos oficial de hashes de RetroAchievements, organizada por grupo de origen (No-Intro, Redump, TOSEC, FBNeo...); detalle en `docs/references.md#retroachievements-como-fuente-de-datos`. |
| RAPatches | github.com/RetroAchievements/RAPatches | Repositorio oficial de parches (traducciones, etc.) de RetroAchievements, referenciado por `PatchUrl` en la API; detalle en `docs/references.md#retroachievements-como-fuente-de-datos`. |
| retool-clonelists-metadata | github.com/unexpectedpanda/retool-clonelists-metadata | Fuente oficial de los ficheros de clonelist que usa retool (y el propio `metadata/dat/retool/clonelists/*.json` de este repo) para sistemas sin `cloneofid` nativo, como Redump; generados automáticamente desde Redump y No-Intro. Incluye además `metadata/` (metadatos adicionales por juego), `mias/` (listas Missing In Action) y una carpeta `retroachievements/` con hashes (CRC/MD5/SHA1) verificados por RetroAchievements por sistema — válido para comparación directa en sistemas de cartucho (No-Intro); **no** en sistemas ópticos (Redump/CHD), donde el hash de RA es un método propio (no de fichero completo) y requiere RAHasher para calcularlo, ver `docs/references.md#retroachievements-como-fuente-de-datos`. |
| RomVault — Supported DATs | wiki.romvault.com/doku.php?id=supported_dats | Wiki de RomVault; documenta fuentes de DAT adicionales no cubiertas por los portales oficiales, incluyendo `Non-Redump-Custom` (PS3/Xbox 360 de fuentes scene/P2P) y `DeDupe-NoIntro` (Non-Redump con duplicados de Redump eliminados). |
| MetalSlug/MAMERedump | github.com/MetalSlug/MAMERedump | Colección de referencia (54 sistemas ópticos: Redump + intersección MAME + TOSEC, recodificados a CHD), copia local en `metadata/dat/MAMERedump/`. **No es una herramienta de matching** — el propio README indica explícitamente que el programa de emparejamiento/fusión no está publicado ("The matching and merging program remains unpublished"); las carpetas `Scripts/`, `GDI Files/` y `Additional Cue Files/` son solo utilidades/plantillas para *construir* CHDs, no metadatos de identificación. **Sí es útil como fuente de hash**: cada DAT en `MAMERedump/full/<Sistema> (N).dat` (esquema MAME `<machine>`/`<disk name="....chd" sha1="...">`, sin `cloneofid`) da el SHA1 real de cada CHD indexado por nombre — el mismo hash que calcula `chdman info` sobre un CHD local, lo que permite un cruce por hash (fiable) en vez de por nombre de fichero (verificado con datos reales: PC Engine CD trae 551 discos frente a los 528 miembros del `Sony/NEC` Redump ya sincronizado en este repo, captura más reciente). Copia local incluye también `MAMERedump/MAME/` (16 DAT, intersección/exclusivas de MAME software list) y `MAMERedump/Tosec/` (exclusivas TOSEC). |
| Fresh1G1R Dats | github.com/UnluckyForSome/Fresh1G1R | DAT 1G1R ya filtrados con retool, actualizados a diario vía GitHub Actions, en tres perfiles de criterio (McLean, PropeR, Hearto). Alternativa de referencia/comparación al filtrado propio de la fase 5 del workflow, no sustituye al proceso documentado en `docs/guides/tools/1g1r-filtering.md`. |

### Hardware y comunidad

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
