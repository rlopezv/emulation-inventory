# Curacion por sistema

Ficheros de curacion con informacion de referencia especifica por sistema (catalogo oficial vs. prototipos/homebrew, casos especiales de fuente, etc.) que no encaja como fila de tabla en `docs/romsets.md`.

Cada fichero puede combinar contenido curado a mano con una seccion auto-generada (entre `<!-- AUTO-GENERADO INICIO -->` / `<!-- AUTO-GENERADO FIN -->`) con el listado de familias de `metadata/dat-index/<id>.json`, regenerable con `tools/scripts/generate-romset-docs.ps1`.

Esta carpeta complementa, no sustituye:
- `docs/romsets.md` -- asociacion sistema -> DAT (fuente, formato, alternativa).
- `metadata/dat-index/<id>.json` -- indice generado a partir del DAT real.

## Fuentes de referencia — más allá de Wikipedia

Cada `<id>.md` lleva una sección `## Fuentes de referencia` con una tabla `| Tipo | Fuente | Detalle |` (formato fijado 2026-09-06, sustituye al bullet anidado anterior — ver `tools/scripts/build-fuentes-referencia-table.py`):

- **`Especialista`** — una base de datos dedicada a ese sistema concreto (ej. ZXDB para `spectrum`, SNES Central para `snes`). Una fila por fuente confirmada; `` `[TODO]` `` con el motivo cuando se investigó y no se encontró ninguna utilizable, o "Sin investigar todavía" cuando aún no se ha buscado.
- **`Genérica`** — catálogo amplio que cubre muchos sistemas (Wikipedia, y las de la lista de abajo cuando se confirmen aplicables a ese sistema concreto). Wikipedia siempre lleva su propia fila (artículo `List of <Sistema> games`, o `` `[TODO]` `` con el motivo si no existe artículo — ver `docs/session-context.md`, sesión 2026-09-06, `c128` como caso confirmado).

El detalle de cada fuente **genérica** con credencial (procedimiento de alta, límite de uso, orden de preferencia) vive en `docs/guides/tools/api-credentials.md` y `docs/guides/tools/metadata-source-priority.md` — no se repite aquí. Alternativas a considerar cuando Wikipedia no baste, verificadas una a una antes de citarlas en cualquier `<id>.md`:

Procedimiento de alta y límite de uso de cada API con credencial: ver `docs/guides/tools/api-credentials.md` (centralizado ahí, no repetido aquí). Orden de preferencia recomendado entre estas fuentes (y por qué): `docs/guides/tools/metadata-source-priority.md`.

- **[MobyGames](https://www.mobygames.com/platform/)** — catálogo genérico por plataforma, cubre prácticamente cualquier sistema de esta carpeta. **La web bloquea el acceso automático (HTTP 403)** — para consultar el listado de juegos por plataforma sin depender de abrir la página a mano, usar la **API REST oficial** (`mobygames.com/info/api/`, parámetro `platform` con el `platform_id` numérico de cada sistema) en vez de intentar adivinar/scrapear la URL de la página. `MobyGamesScraper` (ver `docs/tools.md`) es un cliente ya hecho para esa API que exporta a CSV, aunque con mantenimiento mínimo. Sigue haciendo falta confirmar a mano el `platform_id`/slug de cada sistema antes de citarlo en un `<id>.md` — no asumir un patrón de URL de página sin comprobarlo.
- **[TheGamesDB](https://thegamesdb.net/)** — base de datos comunitaria gratuita, ya usada como fuente por herramientas ya catalogadas en `docs/tools.md` (Skraper/SkyScraper la incluyen como uno de sus orígenes de scraping). **Documentación oficial vigente en `api.thegamesdb.net`** (Swagger; la wiki histórica en `wiki.thegamesdb.net` queda obsoleta como referencia). Endpoints confirmados: `GET /v1/Platforms` (listado completo, para resolver el `id` numérico de cada sistema) y `GET /v1/Games/ByPlatformID?id=<id>` (listado de juegos de esa plataforma; admite varios id separados por coma); alta de credencial en `docs/guides/tools/api-credentials.md`.
- **[LaunchBox Games Database](https://gamesdb.launchbox-app.com/)** — especialmente relevante aquí porque el usuario ya tiene licencia de LaunchBox BigBox. **Sin API oficial** (confirmado, no es una limitación de acceso nuestra) — la vía real es la web navegable sin cuenta (por plataforma/juego), o la **descarga completa de la base de datos** en `https://gamesdb.launchbox-app.com/Metadata.zip` (actualizada a diario), que evita por completo el tema de rate-limiting al traer todo de golpe. Con LaunchBox instalado, esa base ya está disponible localmente como SQLite (`LaunchBox.Metadata.db`) sin necesidad de parsear el XML del ZIP a mano — script ad-hoc: `tools/scripts/launchbox-platform-games.py` (ver `tools/scripts/README.md`). Mismo esquema de campos que el ZIP, pero no necesariamente el mismo contenido: la base local solo se actualiza cuando la app de LaunchBox sincroniza, mientras que `Metadata.zip` se regenera a diario en el servidor — verificado un desfase real de ~1000 juegos y 1 plataforma (comparación 2026-09-06). Irrelevante para listados de referencia puntuales; si se necesita el dato más reciente, sincronizar desde la app o volver a descargar el ZIP en vez de asumir que la base local está al día.
- **[IGDB](https://www.igdb.com/)** (Internet Game Database, propiedad de Twitch/Amazon) — catálogo genérico por plataforma con buena cobertura y calidad de metadatos textuales; **sin artwork útil para retro** (no distingue versión por plataforma en sus recursos gráficos, según nota del propio mantenedor de SkyScraper). API oficial v4 (`api.igdb.com`), autenticación vía credenciales de app de Twitch (alta en `docs/guides/tools/api-credentials.md`); consultas en lenguaje Apicalypse (`fields ...; where platforms=<id>; limit ...;`) contra `POST /v4/games` (filtrando por el `id` numérico de `/v4/platforms`). `SkyScraper` (ver `docs/tools.md`) ya cubre esta fuente vía su módulo `igdb`, pero solo scrapea por emparejamiento contra una romset ya presente en disco — para un listado de referencia independiente de tener ya los ficheros, script propio: `tools/scripts/igdb-platform-games.py` (ver `tools/scripts/README.md`).
- **[OpenVGDB](https://github.com/OpenVGDB/OpenVGDB)** — base de datos SQLite descargable sin API/credencial (`releases/latest`, un único `.zip` con `openvgdb.sqlite`), mismo patrón que LaunchBox: fichero local, sin rate limit. **Fuente parada, no viva**: la última release (v29.0) es de noviembre de **2021**, sin nada posterior — usar solo como snapshot legado, nunca para lanzamientos recientes. Su valor real: **incluye hashes CRC/MD5/SHA1 por ROM** junto con título/desarrollador/editora/género — de todas las fuentes de esta lista, solo RetroAchievements ofrece algo parecido. Cubre 33 sistemas con datos reales verificados (de los 43 listados en su tabla `SYSTEMS`; `3DO`, `Atari Jaguar CD`, `NEC PC-FX` y `Commodore 64` figuran en esa tabla pero tienen **0 filas reales** — placeholders sin datos, confirmado por consulta directa 2026-09-06, no usar pese a aparecer listados). Script ad-hoc: `tools/scripts/openvgdb-platform-games.py`.
- **[RetroAchievements](https://retroachievements.org/)** — cobertura limitada a los sistemas que soporta con logros (no es un catálogo genérico como las demás fuentes de esta lista), pero es la única que **devuelve hashes MD5 junto con el listado de juegos** (`API_GetGameList.php`, parámetro `h=1`) — conecta directamente con `rahashes`/`unofficial-ra-dats` (ver `docs/dat-sources.md`), ya usados en este repo para verificación de CHD. Autenticación con usuario + web API key (alta en `docs/guides/tools/api-credentials.md`). Script ad-hoc: `tools/scripts/retroachievements-platform-games.py`.
- **[Gamia](https://gamia-archive.fandom.com/)** — wiki de nicho (Fandom) con categoría propia `Category:Video_game_lists_by_platform`. **Cobertura pequeña, confirmada completa**: solo 26 artículos de lista en toda la categoría (sin paginación pendiente, verificado vía API), así que no sustituye a Wikipedia — solo aporta cuando cubre justo el sistema que Wikipedia no tiene. API de MediaWiki estándar y accesible sin bloqueo anti-bot (a diferencia de Sega Retro): `gamia-archive.fandom.com/api.php?action=query&list=categorymembers&cmtitle=Category:Video_game_lists_by_platform&cmlimit=500&format=json`. Confirmado útil para `psvita` (`List of PlayStation Vita video games`); ojo con falsos amigos de alcance — `List of Atari XE Game System video games` es específico de la XEGS, no de toda la familia 400/800/XL/XE de `atari800`, así que no vale como sustituto directo ahí.
- **[GiantBomb](https://www.giantbomb.com/)** — más editorial/wiki que catálogo puro de "lista de juegos" (incluye personajes, compañías, conceptos, no solo juegos), pero cubre plataformas como recurso propio. API oficial (`www.giantbomb.com/api/documentation/`), alta de credencial en `docs/guides/tools/api-credentials.md`. Recursos identificados por `guid` (string, ej. `3030-121`) además de un `id` numérico propio; el filtrado de `GET /games/` por plataforma usa ese `id` numérico, no el guid (`filter=platforms:<id>`, admite varios separados por coma con lógica OR) — el `id` de cada plataforma se resuelve antes vía `GET /platforms/?filter=name:<nombre>`. `field_list` (coma-separado) limita los campos devueltos, recomendable para no gastar cuota de golpe.
- **Páginas de comunidad especializadas por sistema** — más profundas que las genéricas de arriba para el sistema concreto que cubren, a costa de no ser genéricas.
  - `spectrum` (ZX Spectrum) — **[ZXDB](https://github.com/zxdb/ZXDB)** es la base de datos real (dump MySQL descargable, `ZXDB_mysql.sql.zip`), que alimenta varios frontends: [Spectrum Computing](https://spectrumcomputing.co.uk/) (HTML navegable, catálogo/mapas de memoria/carátulas/foro) y **[World of Spectrum](https://worldofspectrum.org/using-the-api/software)** (API REST JSON **en vivo**, confirmada funcionando con `X-API-KEY=test` sin registro — 24.368 registros totales, campos `features`/`controls`/`roles`/`publishers` por título; tope de paginación de 10 resultados/página). Script ad-hoc contra la API: `tools/scripts/worldofspectrum-games.py`.
  - `dragon32` (Dragon 32/64) — **[The Dragon Archive](https://www.worldofdragon.org/)** (wiki HTML, sin API/export). Cobertura confirmada: solo Dragon 32/64/200 y Tano Dragon — **no cubre TRS-80 CoCo** (variante de hardware del mismo sistema en `docs/systems.md`), asumido como limitación conocida en vez de buscar una fuente que cubra ambos.
  - `vic20` — **[VIC-20 Listings](http://www.vic20listings.freeolamail.com/proglist.html)** (nota: el sitio **no soporta HTTPS**, usar la URL `http://` tal cual). Confirmado vivo y con contenido real: índice de listados type-in con autor, revista/libro de origen + país, fecha y requisito de RAM (`UN`/`16K`...) por programa. Solo HTML navegable, sin CSV/API.
  - `sharpx68000` — sin fuente especialista confirmada por ahora (GamesX descartado: es un wiki general de hardware retro, no dedicado a X68000) — `[TODO]`.

| Sistema | Fichero |
| --- | --- |
| `3do` | [3do.md](3do.md) |
| `3ds` | [3ds.md](3ds.md) |
| `3dseshop` | [3dseshop.md](3dseshop.md) |
| `64dd` | [64dd.md](64dd.md) |
| `amiga` | [amiga.md](amiga.md) |
| `amigacd32` | [amigacd32.md](amigacd32.md) |
| `amigacdtv` | [amigacdtv.md](amigacdtv.md) |
| `amstradcpc` | [amstradcpc.md](amstradcpc.md) |
| `arcadia2001` | [arcadia2001.md](arcadia2001.md) |
| `astrocade` | [astrocade.md](astrocade.md) |
| `atari2600` | [atari2600.md](atari2600.md) |
| `atari5200` | [atari5200.md](atari5200.md) |
| `atari7800` | [atari7800.md](atari7800.md) |
| `atari800` | [atari800.md](atari800.md) |
| `atarist` | [atarist.md](atarist.md) |
| `c128` | [c128.md](c128.md) |
| `c64` | [c64.md](c64.md) |
| `cdi` | [cdi.md](cdi.md) |
| `channelf` | [channelf.md](channelf.md) |
| `coleco` | [coleco.md](coleco.md) |
| `dragon32` | [dragon32.md](dragon32.md) |
| `dreamcast` | [dreamcast.md](dreamcast.md) |
| `dsiware` | [dsiware.md](dsiware.md) |
| `fds` | [fds.md](fds.md) |
| `gameandwatch` | [gameandwatch.md](gameandwatch.md) |
| `gamecube` | [gamecube.md](gamecube.md) |
| `gamegear` | [gamegear.md](gamegear.md) |
| `gb` | [gb.md](gb.md) |
| `gba` | [gba.md](gba.md) |
| `gbc` | [gbc.md](gbc.md) |
| `gx4000` | [gx4000.md](gx4000.md) |
| `intellivision` | [intellivision.md](intellivision.md) |
| `jaguar` | [jaguar.md](jaguar.md) |
| `jaguarcd` | [jaguarcd.md](jaguarcd.md) |
| `lynx` | [lynx.md](lynx.md) |
| `mastersystem` | [mastersystem.md](mastersystem.md) |
| `megadrive` | [megadrive.md](megadrive.md) |
| `megaduck` | [megaduck.md](megaduck.md) |
| `msx` | [msx.md](msx.md) |
| `msx2` | [msx2.md](msx2.md) |
| `n64` | [n64.md](n64.md) |
| `nds` | [nds.md](nds.md) |
| `ndsi` | [ndsi.md](ndsi.md) |
| `neogeo` | [neogeo.md](neogeo.md) |
| `neogeocd` | [neogeocd.md](neogeocd.md) |
| `nes` | [nes.md](nes.md) |
| `newn3ds` | [newn3ds.md](newn3ds.md) |
| `ngp` | [ngp.md](ngp.md) |
| `ngpc` | [ngpc.md](ngpc.md) |
| `odyssey2` | [odyssey2.md](odyssey2.md) |
| `pcengine` | [pcengine.md](pcengine.md) |
| `pcenginecd` | [pcenginecd.md](pcenginecd.md) |
| `plus4` | [plus4.md](plus4.md) |
| `pokemini` | [pokemini.md](pokemini.md) |
| `ps2` | [ps2.md](ps2.md) |
| `ps3` | [ps3.md](ps3.md) |
| `psn` | [psn.md](psn.md) |
| `psp` | [psp.md](psp.md) |
| `pspminis` | [pspminis.md](pspminis.md) |
| `psvita` | [psvita.md](psvita.md) |
| `psx` | [psx.md](psx.md) |
| `satellaview` | [satellaview.md](satellaview.md) |
| `saturn` | [saturn.md](saturn.md) |
| `sega32x` | [sega32x.md](sega32x.md) |
| `segacd` | [segacd.md](segacd.md) |
| `sg1000` | [sg1000.md](sg1000.md) |
| `sgb` | [sgb.md](sgb.md) |
| `sharpx68000` | [sharpx68000.md](sharpx68000.md) |
| `snes` | [snes.md](snes.md) |
| `spectrum` | [spectrum.md](spectrum.md) |
| `sufami` | [sufami.md](sufami.md) |
| `supervision` | [supervision.md](supervision.md) |
| `switch` | [switch.md](switch.md) |
| `thomson` | [thomson.md](thomson.md) |
| `vectrex` | [vectrex.md](vectrex.md) |
| `vic20` | [vic20.md](vic20.md) |
| `virtualboy` | [virtualboy.md](virtualboy.md) |
| `wii` | [wii.md](wii.md) |
| `wiiu` | [wiiu.md](wiiu.md) |
| `wswan` | [wswan.md](wswan.md) |
| `wswanc` | [wswanc.md](wswanc.md) |
| `xbox` | [xbox.md](xbox.md) |
| `xbox360` | [xbox360.md](xbox360.md) |
| `zx81` | [zx81.md](zx81.md) |
