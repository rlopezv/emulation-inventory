# Credenciales de API — fuentes de metadatos de juego

Varias fuentes de referencia usadas para curación y generación de `gamelist.xml` (ver `docs/guides/romsets/systems/README.md#fuentes-de-referencia--más-allá-de-wikipedia`) requieren registrarse para obtener una credencial de acceso. Esta página centraliza el procedimiento de alta y el límite de uso de cada una — es el único sitio que hay que mirar para saber "cómo consigo acceso a X"; las páginas que citan cada fuente enlazan aquí en vez de repetir el procedimiento.

No cubre fuentes de DAT/romset (`docs/dat-sources.md` ya tiene su propio campo "¿Requiere intervención manual?" para eso) — solo APIs de metadatos de juego (sinopsis, género, desarrollador, plataforma...) para curación y scraping.

**Los valores reales de cada credencial (`client_id`, `client_secret`, API key) van en `private/api-credentials.md` (gitignored) una vez obtenidos — nunca en este fichero ni en ningún otro documento versionado.**

| Fuente | Tipo de credencial | Alta | Límite de uso |
| --- | --- | --- | --- |
| MobyGames | API key | Registro gratuito en MobyPro (`mobygames.com/info/api/`) | 720 peticiones/hora en uso no comercial (1 cada 5s, ráfaga máx. 1/s) |
| IGDB | `client_id` + `client_secret` (credenciales de app de Twitch) | Registrar una app en la consola de desarrolladores de Twitch (IGDB es propiedad de Twitch/Amazon); canjear por token OAuth vía `POST id.twitch.tv/oauth2/token` (`grant_type=client_credentials`) | 4 peticiones/segundo por app |
| GiantBomb | API key | Registro gratuito (`giantbomb.com/api/`, requiere cuenta de sitio) | 200 peticiones/recurso/hora (HTTP 420 al superarlo, "Rate limit exceeded"), máx. 100 resultados por página |
| RetroAchievements | Web API key + usuario (ambos van en cada petición) | Cuenta gratuita en `retroachievements.org`, clave visible en el panel de usuario ("Keys") | Sin cifra publicada, la documentación solo pide cachear resultados por estar "sujeto a rate-limiting" |
| TheGamesDB | API key | Crear cuenta en `thegamesdb.net`, con sesión iniciada solicitar la clave en `api.thegamesdb.net/key.php` | Clave pública (free): 1500 queries/mes (hasta 30000 peticiones básicas o 15000 con artwork si se agrupan bien, según reporte de la propia comunidad en el foro oficial — no está en la documentación formal); clave privada (repositorios grandes, solicitud aparte): límites mayores, hasta ~120000 resultados/mes |

LaunchBox Games Database y OpenVGDB no aparecen aquí porque no requieren credencial: se consultan como fichero local (`Metadata.zip`/`Metadata.db` o `openvgdb.sqlite`) descargado una vez, sin autenticación ni rate limit — ver detalle de cada una en `docs/guides/romsets/systems/README.md`.
