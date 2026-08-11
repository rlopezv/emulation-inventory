# Generación de gamelist.xml

Generación de `gamelist.xml` para el romset ya organizado en `data/roms/`, normalmente en la misma pasada que la obtención de media (ver [media-scraping.md](media-scraping.md) para el detalle completo de Skraper y SkyScraper, incluida la composición manual de imágenes) — esta guía se centra en la parte de metadatos/gamelist y en la conversión entre formatos de frontend.

Corresponde a la fase 9 de [docs/guides/romsets/workflow.md](../romsets/workflow.md).

No confundir con `generate-romset-docs.ps1` (documentado en [docs/guides/romsets/custom-pipeline.md](../romsets/custom-pipeline.md)), que genera documentación en `docs/guides/romsets/systems/<id>.md` a partir de `dat-index/<id>.json`, no `gamelist.xml`.

## Skraper

Mismo flujo GUI ya documentado en [media-scraping.md](media-scraping.md#uso-habitual-gui-scraping-online) — genera el `gamelist.xml` por sistema en la misma pasada que descarga la media. No requiere ningún paso adicional específico para el gamelist.

## SkyScraper

Mismo flujo de dos fases documentado en [media-scraping.md](media-scraping.md#skyscraper) (`-s <módulo>` para recolectar, sin `-s` para generar el gamelist desde la caché). El detalle específico de esta fase es el **flag `-f` (frontend)**, que determina el formato de salida del gamelist:

```bash
Skyscraper -p snes -f emulationstation
```

**Frontends soportados confirmados:** `emulationstation` (por defecto si no se especifica), `esde`, `pegasus`, `retrobat`, `attractmode`, `aso`.

- **EmulationStation** — formato por defecto, no requiere `-f` explícito.
- **Pegasus** — `-f pegasus`; sencillo, opcionalmente configurable para fijar también el comando de lanzamiento del gamelist de Pegasus.
- **Attract-Mode** — requiere combinarlo obligatoriamente con el flag `-e` (emulador) para que el gamelist quede completo.

## ES Scraper

**Aclaración de identidad:** no es una herramienta descargable aparte — es el **scraper integrado dentro de la propia EmulationStation** (y derivados como ES-DE), accesible desde el menú de la interfaz, no desde línea de comandos externa.

**Flujo confirmado** (ej. en RetroPie): **Main Menu → Scraper** → elegir alcance (un sistema concreto, todos los sistemas, o solo los juegos sin metadatos todavía) → lanzar. El emparejamiento se hace por nombre de fichero contra bases de datos online (TheGamesDB, ScreenScraper según configuración); si un fichero no casa, ofrece sugerencias o permite seleccionar el juego manualmente.

**Miximage generator:** función equivalente al "User Provided Mix" de Skraper o al `artwork.xml` de SkyScraper — combina captura + marquesina + caja/cover + media física en una sola imagen compuesta para la vista de lista. Se puede lanzar desde el propio scraper (individual o multi-scraper) o desde un generador offline aparte.

**Investigado — probable identidad confirmada:** la entrada de `docs/tools.md` describe explícitamente "scraper integrado", lo que coincide con este scraper nativo de EmulationStation, no con un proyecto de terceros. Existe además `elpendor/ES-scraper` (Python, 78 commits) como proyecto de terceros con nombre parecido — descarga boxart y escribe `gamelist.xml`/`es_systems.cfg`, pero su documentación no confirma descarga de vídeo (a diferencia de lo que indica la fila actual de `tools.md`, "Imágenes + vídeos"). Con esto, lo más probable es que la fila ya presente en `tools.md` se refiera al integrado; dejarlo así salvo que se confirme lo contrario.

## RetroScraper

**Corrección:** "SimpleScraper" era un error de nombre — la herramienta real es **RetroScraper**, github.com/zayamatias/retroscraper.

**Fuente:** Python 3 (3.7-3.10), interfaz Kivy, requiere Rust instalado; Windows, Linux y Raspberry Pi.

**Funcionamiento:** lee `es_systems.cfg` de EmulationStation para localizar sistemas y carpetas de ROMs. Descarga metadatos, la caja del juego (en vez de la captura, por defecto), vídeos (desactivables) y bezels.

**Uso:**

```bash
python3 retroscraper.py                        # modo GUI, sin argumentos
python3 retroscraper.py --systems nes,snes      # modo CLI, sistemas concretos
```

Flags adicionales confirmados: `--nodb` (sin base de datos local), `--nobackup` (sin copias de seguridad), `--remote USER PASSWORD` (credenciales de scraper remoto).

## RetroBat

**Fuente:** retrobat.org (ya catalogado como software en `docs/software.md`, no se duplica aquí como herramienta de PC-side — es un paquete instalado en el propio Windows que actúa como frontend). Funciona sobre una versión modificada de EmulationStation; incluye de forma nativa la lógica de indexado y scraping.

### Método 1 — generación local sin scraping

Solo crea la estructura de `gamelist.xml` con la lista de juegos, sin descargar nada (para rellenar rutas/metadatos a mano o por script después):

1. Colocar los ficheros de ROM en `retrobat/roms/<sistema>/`.
2. Arrancar RetroBat.
3. Pulsar **START** (Intro en teclado) para abrir el Main Menu — *(no "Select"/espacio, corregido)*.
4. **GAME SETTINGS → UPDATE GAMELIST**.
5. EmulationStation escanea el directorio y escribe `gamelist.xml` en la raíz de la carpeta de ese sistema, con los nombres de fichero exactos — sin tocar internet.

### Método 2 — scraper interno (online)

Genera el `gamelist.xml` ya completo con descripción/año/género/imágenes:

1. Main Menu → **SCRAPER**.
2. Pestaña **ACCOUNTS** — introducir credenciales de ScreenScraper (cuenta gratuita).
3. **SCRAPER SETTINGS** → elegir sistemas a indexar → **SCRAPE NOW**.
4. Descarga la media a la subcarpeta `media/` del sistema y deja el `gamelist.xml` completo.

## gamelist-utils (conversión entre formatos)

**Fuente:** github.com/JayCanuck/gamelist-utils (Node.js/TypeScript). No genera el `gamelist.xml` desde cero (no es un scraper) — convierte uno ya existente entre formatos de frontend.

**Sintaxis confirmada** — comando `gamelist <acción>`, ejecutado dentro del directorio del romset:

| Acción | Formato destino | Descripción |
| --- | --- | --- |
| `simplemenu` | SimpleMenu (OpenDingux) | Convierte el romset al formato esperado |
| `retroarch` | RetroArch | Symlinks de los ficheros de media para las playlists de RetroArch |
| `es-de` | ES-DE | Symlinks del gamelist y media a las rutas que espera EmulationStation-DE |
| `muos` | muOS | Convierte el romset para compatibilidad muOS |
| `onion` | Onion (Miyoo) | Convierte el romset para compatibilidad Miyoo/Onion |

```bash
gamelist muos
gamelist retroarch --multi=nes,snes,gb
```

`--multi=<sistemas>` procesa varios sistemas en una sola pasada. Todas las acciones admiten `--help` para parámetros específicos adicionales.

## Notas

Skraper y SkyScraper cubren scraping + gamelist + media en una sola pasada (ver `media-scraping.md`); ES Scraper (integrado) es la opción por defecto cuando ya se está dentro del propio frontend en el dispositivo, no en el PC. `gamelist-utils` no sustituye a ninguno de los anteriores — se usa después, cuando ya existe un `gamelist.xml` en un formato y hace falta adaptarlo a otro frontend/CFW sin volver a raspar desde cero.
