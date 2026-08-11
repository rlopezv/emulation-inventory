# Obtención de media

Descarga de imágenes (carátulas, capturas, marquesinas) y vídeos asociados al romset, normalmente en el mismo paso que la generación de `gamelist.xml` (ver [gamelist-generation.md](gamelist-generation.md)) — Skraper y SkyScraper hacen ambas cosas en la misma pasada. Se documenta aquí como tarea propia para cubrir también el caso en que el scraper online no encuentra una imagen y hace falta aportarla o componerla manualmente.

Corresponde a la fase 10 de [docs/guides/romsets/workflow.md](../romsets/workflow.md).

## Skraper

**Fuente:** skraper.net (Windows/Linux/macOS). Ejecutable real confirmado: **`SkraperUI.exe`** (no `Skraper.exe`).

**Aclaración importante:** no tiene modo CLI confirmado — probado en la práctica que `SkraperUI.exe -help` simplemente lanza la interfaz gráfica sin mostrar ayuda ni aceptar el flag, y no hay un binario de consola aparte en la instalación. No confundir con **Skyscraper** (`muldjord/skyscraper`, ver más abajo), que sí es CLI y a menudo se referencia con nombre parecido — varias fuentes de terceros mezclan ambas herramientas.

### Uso habitual (GUI, scraping online)

Flujo confirmado por varias guías de terceros (Retro Camel, Retro Game Corps):

1. **Cuenta de ScreenScraper** — Skraper se apoya en la base de datos comunitaria de ScreenScraper.fr; hace falta cuenta propia (gratuita) para scraping en condiciones — el volumen de descarga sin cuenta o con cuenta gratuita está limitado por la propia API de ScreenScraper.
2. **Apuntar a la carpeta de ROMs** — indicar la ruta raíz (ej. `C:\ROMs`), organizada en subcarpetas por sistema.
3. **Elegir sistemas** — seleccionar qué plataformas se van a raspar en esta pasada (NES, PSP, Arcade...).
4. **Elegir tipos de media/metadatos** — carátula, captura, vídeo, marquesina, etc.; cada tipo cuenta como una petición independiente contra la cuota de la API (ej. captura + caja + título = 3 peticiones por juego).
5. **Ruta de salida** — típicamente `ROMs/<sistema>/downloaded_images` o la estructura `media/` esperada por el frontend objetivo (ver `docs/system-paths.md`).
6. **Lanzar el escaneo** — genera un `gamelist.xml` por sistema con los datos raspados, más las imágenes/vídeos en la carpeta de salida configurada.

**Nota práctica:** limpiar el nombre de archivo de las ROMs (quitar tags redundantes tipo `(USA) v1.0` si es posible) mejora la precisión del emparejamiento contra la base de ScreenScraper.

### Composición manual cuando el scraper online no encuentra una imagen

**Precisión importante tras verificarlo en la instalación real (`SkraperUI.exe` 1.4.1):** no existe una fuente de metadatos "Medios Locales" para hacer scraping 100% offline (eso sigue sin estar disponible — para ese caso usar **SkyScraper** y su módulo `import`, ver más abajo). Lo que sí existe, confirmado en la propia interfaz, es el **tipo de media "User Provided Mix"** en la pestaña Media: compone una imagen final (fondo + caja 3D + cartucho + logo) a partir de una plantilla XML propia o de la comunidad, cruzando recursos locales.

**Flujo:** pestaña **Media** → tipo **User Provided Mix** → seleccionar el fichero XML de plantilla → carpeta de salida (típicamente `%ROMROOTFOLDER%\Imgs`).

**Plantillas de comunidad verificadas** (repositorios reales en GitHub, todos confirmados para usar exactamente este flujo de Skraper):

| Dispositivo / sistema objetivo | Plantilla | Repositorio | Layout |
| --- | --- | --- | --- |
| Miyoo Mini / Anbernic RG35XX (GarlicOS / OnionOS) | Garlic Onion Skraper Mix | `ebzero/garlic-onion-skraper-mix` | 3 imágenes (caja 3D, captura, logo), escalado a 333×480 |
| Anbernic RG Nano | RG Nano Skraper Mix | `tobio-tenma/rg-nano-skraper-mix` | Pantalla cuadrada 1:1 (240×240), logo agrandado sobre captura recortada; incluye script de conversión PNG→JPG |
| Miyoo Mini / RG35XX (variante legibilidad) | Garlic OS Skraper Shadow | `timault/Garlic-Os-Skraper-` | Pantalla completa con degradado negro (Black Gradient Shadow) para que el texto blanco del menú siga siendo legible sobre capturas brillantes |
| Miyoo Mini / OnionOS (por orientación) | OnionOS Skraper Template | `dashqa/onion-os-skraper-template` | Dos variantes: Big Wheel (cajas verticales — Genesis, SNES, NES, NeoGeo, MAME) y Small Wheel (cajas cuadradas — Game Boy, GBA, PS1, NDS) |
| TrimUI Smart Pro / TrimUI Brick | TSP-MIX | `acatone-git/TSP-MIX` | Panorámico 16:9 para la pantalla de la TrimUI Smart Pro/Brick; fork de `garlic-onion-skraper-mix` adaptado a este hardware |
| EmuELEC / colecciones variadas | Skraper Mixed Images Definitions | `joyrider3774/skraper_mixed_images` | Compendio de composiciones XML variadas para arcade y consolas clásicas |

## SkyScraper

**Fuente:** github.com/muldjord/skyscraper (Linux, también disponible para Windows vía WSL). CLI real, documentación completa en gemba.github.io/skyscraper.

**Dos fases de trabajo confirmadas:**

1. **Recolección** — rellena la caché de recursos de Skyscraper desde el módulo indicado con `-s`:

   ```bash
   Skyscraper -p snes -s screenscraper
   ```

   Módulos disponibles incluyen `screenscraper`, `thegamesdb`, `openretro`, `esgamelist` (importar desde un `gamelist.xml` ya existente de EmulationStation) y `import` (recursos propios, ver abajo).

2. **Generación del gamelist** — se omite `-s` para generar el `gamelist.xml` a partir de todo lo ya cacheado, sin volver a raspar:

   ```bash
   Skyscraper -p snes
   ```

### Importar recursos propios (`-s import`) — caso "el scraper no encontró la imagen"

```bash
Skyscraper -p snes -s import
```

Importa ficheros colocados manualmente en `~/.skyscraper/import/{screenshots,covers,wheels,marquees,videos}/`. El nombre de archivo debe coincidir exactamente con el nombre base de la ROM (ej. `Bubble Bobble.nes` → `Bubble Bobble.jpg`/`.png` en la subcarpeta correspondiente). Es la vía para completar a mano los juegos que ningún módulo online encontró, antes de generar el gamelist final.

### Composición en capas (`artwork.xml`)

Sistema de plantillas para componer la imagen final combinando varios recursos ya cacheados (screenshot, cover, wheel...) en una sola imagen, en vez de usarlos por separado:

- Nodo `<output>` — lienzo de la composición (ej. 640×480).
- Nodo `<layer>` — una capa por recurso, con `resource` (`screenshot`/`cover`/`wheel`...), posición (`x`/`y`), tamaño (`width`/`height`) y alineación (`align`/`valign`).
- Modificadores por capa: `<rounded>` (esquinas redondeadas), `<stroke>` (borde), `<gamebox>` (perspectiva 3D de caja), `<shadow>` (sombra proyectada).

Plantillas de ejemplo incluidas en el propio repositorio (`artwork.xml.example1`, etc.) como punto de partida.

## Notas

Ambas herramientas escriben directamente en la estructura `media/` de `data/roms/<sistema>/` esperada por `gamelist.xml` (ver `docs/references.md#gamelistxml`) — revisar que las rutas generadas coincidan con las que el frontend objetivo espera antes de desplegar (ver `docs/system-paths.md`).

Para el caso de "faltan imágenes tras el scraping online", el flujo recomendado es: 1) completar a mano los recursos que falten en la carpeta de importación de SkyScraper (`-s import`) o en Skraper vía "User Provided Mix", 2) regenerar el gamelist/mix con esos recursos ya incluidos, en vez de perseguir manualmente cada imagen suelta fuera del flujo de la herramienta.
