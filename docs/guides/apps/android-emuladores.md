# Emuladores Android

A diferencia de los frontends gráficos que solo indexan y decoran menús, los emuladores standalone (independientes) son las aplicaciones nativas encargadas de la ejecución directa, la traducción de instrucciones de CPU y el renderizado por hardware de cada sistema. En el ecosistema Android, el uso de emuladores independientes se prefiere sobre los núcleos unificados en sistemas de quinta generación en adelante. Su arquitectura aprovecha directamente las APIs gráficas de bajo nivel de los procesadores ARM de 64 bits (Vulkan y OpenGL ES) y permite aplicar configuraciones individuales de resolución, parches de rendimiento de pantalla ancha y configuraciones de hilos de CPU optimizadas para cada arquitectura.

## Contexto de uso

Standalone instalable (APK Android). Cada emulador se instala y configura de forma independiente; el frontend (ES-DE, Daijishō, Pegasus) solo apunta a sus rutas de ROMs y los lanza.

## Emuladores cubiertos

La preferencia de este documento es usar siempre el APK oficial (sitio web, buildbot o repositorio del proyecto) como fuente principal, en vez de Google Play. Para DuckStation y Flycast, sus proyectos documentan Google Play como canal principal en su README, pero sí existen builds Android alternativas (GitHub Releases, mirrors) que permiten seguir la preferencia por APK — ver detalle por emulador.

| Sistema / Consola | Emulador recomendado | Formato de datos óptimo | Fuente de descarga principal |
| --- | --- | --- | --- |
| Multiconsola (8/16 bits) | RetroArch (64-bit) | `.zip`, `.chd` | APK oficial directo — buildbot.libretro.com/stable |
| PlayStation 1 | DuckStation | `.chd` (v5) | GitHub Releases oficial, o mirror comunitario (duckstation-mirror.rmacias.workers.dev) para tracking vía Obtainium |
| PlayStation 2 | NetherSX2 | `.chd` (v5) | APK oficial vía GitHub Releases (`Trixarian/NetherSX2-classic`) |
| Nintendo GameCube / Wii | Dolphin | `.rvz` | dolphin-emu.org/download/ (no se pudo confirmar directamente el APK Android por bloqueos del sitio a scrapers, ver nota) |
| PlayStation Portable | PPSSPP | `.cso`, `.iso` | APK oficial (ppsspp.org/download) — Google Play (gratis/Gold) y F-Droid como alternativas |
| Nintendo 3DS | Azahar (sucesor fusionado de Lime3DS y el fork de PabloMK7 de Citra) | `.3ds`, `.cia` | APK oficial (GitHub Releases) — Google Play recomendado por el propio proyecto para la mayoría de usuarios |
| SEGA Dreamcast | Flycast (standalone) | `.chd` (v5) | GitHub Releases — nota: el proyecto dice literalmente "Install Flycast from Google Play" como método oficial |
| SEGA Saturn | Yaba Sanshiro 2 | `.chd` (v5) | Google Play (`org.devmiyax.yabasanshioro2` gratis / `.pro` de pago) — es la única vía oficial actual, ver nota |
| Nintendo DS | DraStic | `.zip` | Software propietario (Exophase); sin canal de descarga verificado, ver nota |

## Descarga

- **Fuente preferente — APK oficial**: sitios web o repositorios de GitHub del proyecto.
- **Google Play Store**: donde el propio proyecto la designa como canal oficial (RetroArch, DuckStation, Flycast, Yaba Sanshiro 2, Azahar), se usa como alternativa o incluso única vía soportada — ver detalle por emulador.

### Detalle por emulador

**RetroArch** — <https://www.retroarch.com/> (sitio) / <https://buildbot.libretro.com/stable> (APK Android directo)
Multiconsola (8/16 bits y núcleos adicionales). La web oficial solo promociona Google Play para Android, pero el buildbot oficial de Libretro publica el APK AArch64 directamente, sin pasar por la tienda. El propio proyecto advierte que la funcionalidad de la versión de Play Store puede diferir de la disponible en las builds del sitio por restricciones de la tienda.

**DuckStation** — <https://github.com/stenzek/duckstation>
PlayStation 1. Requiere una imagen BIOS de PS1 (dumpeada de hardware propio) para poder arrancar; no se distribuye. Soporta renderizado por hardware (D3D11/12, OpenGL, Vulkan, Metal), recompilador/JIT de CPU, save states y mandos con simulación de light gun. El README oficial solo enlaza Google Play para Android (`com.github.stenzek.duckstation`) y aclara que **no dan soporte a la app de Android**. Para tracking vía APK/Obtainium existe un mirror comunitario (`duckstation-mirror.rmacias.workers.dev`) que replica las releases; al ser un mirror de terceros, conviene verificarlo con cautela frente al repo oficial.

**PPSSPP** — <https://www.ppsspp.org/download>
PlayStation Portable. Es el caso más limpio para "APK preferente": tiene APK directo oficial en la propia web (`ppsspp.org/files/.../ppsspp.apk`), además de Google Play (versión gratuita `org.ppsspp.ppsspp` y Gold de pago `org.ppsspp.ppssppgold`) y F-Droid. Quien ya tenga PPSSPP Gold en PC/Mac puede reclamar la versión Android sin coste adicional.

**Dolphin** — <https://dolphin-emu.org/download/>
Nintendo GameCube / Wii. La página de descargas oficial (confirmada por el pack de configs de Obtainium para emuladores) es `dolphin-emu.org/download/`; no se ha podido verificar el detalle exacto del APK Android por bloqueos del sitio a herramientas de scraping automatizado (error 403). Existe también un subdominio `buildbot.mobile.dolphin-emu.org` mencionado en búsquedas, pero su certificado SSL no coincide con el dominio (apunta a infraestructura CDN genérica) — **no se recomienda como fuente** hasta verificarlo desde un navegador real. Usa el formato de compresión propio RVZ (sin pérdida, tamaño de bloque recomendado 128 KB) que conserva parches de texturas HD y trucos.

**Azahar** — <https://github.com/azahar-emu/azahar>
Nintendo 3DS. Sucesor fusionado de Lime3DS y el fork de PabloMK7 de Citra, ambos surgidos tras el cierre de Citra — **estos dos nombres ya no son proyectos activos independientes**, cualquier referencia a "Lime3DS" o "Citra (PabloMK7)" en fuentes antiguas debe entenderse como Azahar hoy. Requisitos mínimos en Android: Android 10.0+, SoC equivalente a Snapdragon 835, 2GB RAM. El propio proyecto recomienda Google Play "para la mayoría de usuarios", pero también ofrece APK directo desde Releases (sin actualizaciones automáticas) y variante "Vanilla" más rápida vía Obtainium.

**Flycast** — <https://github.com/flyinghead/flycast>
SEGA Dreamcast, también compatible con Naomi/Atomiswave (arcade Sega). El README oficial designa explícitamente Google Play como "el método de distribución oficial", aunque también publica builds Android en GitHub Releases (master y nightly).

**NetherSX2** — <https://github.com/Trixarian/NetherSX2-classic> (también existe `Trixarian/NetherSX2-patch`, mismo mantenedor)
PlayStation 2. Es una copia modificada de AetherSX2 (build 3668) con el parche anti-tampering de NetherSX2 aplicado, mantenida por Trixarian sobre el NetherSX2 original de Anon y EZOnTheEyes. APK directo en GitHub Releases (versión estable `NetherSX2-v2.1-3668.apk` y de desarrollo `NetherSX2-v2.2n-3668.apk`). Incluye soporte de RetroAchievements, juego online, bases de datos de juegos y mandos actualizadas, parches de pantalla ancha y sin interlace, sin publicidad. No incluye BIOS ni ROMs: exige colocar la BIOS de PS2 obtenida legalmente en `/bios/` y las ISOs en `/games/` o la carpeta preferida. **Nota de seguridad**: no usar el dominio espejo `nethersx2.com.tr` — no es un canal oficial verificado; usar únicamente los repos de GitHub citados.

**Yaba Sanshiro 2** — <https://www.yabasanshiro.com/>
SEGA Saturn, basado en el proyecto de código abierto Yabause (GPL), desarrollado por devmiyax. La app original "Yaba Sanshiro" fue retirada de Google Play en octubre de 2020 por infracción de la política de abuso de dispositivos/red; el propio desarrollador la relanzó como **Yaba Sanshiro 2** (sin función de cheats), disponible en versión gratuita (`org.devmiyax.yabasanshioro2`) y Pro de pago (`org.devmiyax.yabasanshioro2.pro`). Google Play es actualmente la única vía oficial verificada.

**DraStic** — Nintendo DS, desarrollado por Exophase. **Sigue siendo software propietario**: en 2020 se anunciaron planes de liberar el código, pero nunca se llegó a publicar el binario como código abierto. Los repositorios de GitHub relacionados (`drastic32_r36s`, `DrasticDS_nx`) son solo wrappers/ports comunitarios que explícitamente no incluyen el emulador, la BIOS ni la base de datos — el core sigue siendo cerrado y de pago. `[TODO: no se ha podido verificar la ficha o canal de descarga Android actual]`.

## Instalación

1. **Habilitar sideloading**: en los ajustes de seguridad del dispositivo Android, activa el permiso para "Instalar aplicaciones de fuentes desconocidas" en el navegador o explorador de archivos.
2. **Instalación manual**: ejecuta los archivos `.apk` descargados e instálalos de forma individual en el escritorio de la consola.
3. **Configuración de permisos de almacenamiento**: al abrir cada emulador por primera vez, concede el permiso de acceso total a los archivos (All Files Access). Esto es vital para que las aplicaciones puedan escanear la tarjeta MicroSD externa portátil exFAT.

**Herramienta recomendada — Obtainium** (<https://github.com/ImranR98/Obtainium>, paquete `dev.imranr.obtainium`): app Android de código abierto que instala y mantiene actualizadas apps directamente desde sus fuentes (GitHub Releases, GitLab, F-Droid, etc.), en vez de depender de Play Store. Encaja directamente con la preferencia de este documento por el APK oficial: sigue las páginas de Releases de proyectos como Azahar, NetherSX2 o Flycast y notifica/instala nuevas versiones automáticamente, evitando el proceso manual de descargar e instalar cada `.apk` a mano.

## Estructura de carpetas y ROMs

Los emuladores independientes de Android ofrecen una flexibilidad absoluta, ya que se configuran indicándoles las rutas físicas de forma manual:

- **La raíz estándar**: es plenamente compatible con el esquema de carpetas clásico en minúsculas de un pipeline propio dentro de la MicroSD externa (ejemplo: `/ROMS/ps2/`, `/ROMS/psp/`, `/ROMS/dolphin/`).
- **Mapeo del directorio de juegos**: entra a la interfaz interna de cada emulador instalado (ej. Dolphin), ve a ajustes de directorios, haz clic en Add Folder y selecciona la subcarpeta correspondiente de la tarjeta MicroSD.
- **Ubicación de las BIOS**: a diferencia de RetroArch, donde todo se unifica en `/system/`, los emuladores standalone guardan las BIOS en carpetas internas protegidas dentro del almacenamiento nativo de Android (`/Android/data/[nombre_del_emulador]/files/bios/`), o en una carpeta `/bios/` explícita dentro de su propio almacenamiento (caso NetherSX2). Un pipeline propio debe instruir al usuario o automatizar la inyección de archivos críticos como el `scph1001.bin` de PS1 o el set de archivos `.bin` de PS2 mediante el explorador de la consola.

## Metadatos y scraping

Los emuladores independientes no procesan metadatos visuales avanzados basados en texto ni leen archivos XML planos (`gamelist.xml`) en las carpetas de las ROMs:

- **Interfaces de texto plano internas**: los emuladores leen la carpeta física en tiempo real y muestran los juegos en forma de listas de texto plano estructuradas por los nombres físicos de los archivos.
- **Vistas en cuadrícula locales**: algunos emuladores (como DuckStation o PPSSPP) permiten descargar portadas de forma interna haciendo clic derecho sobre el juego en la interfaz, guardando la carátula en su memoria caché interna privada dentro de la partición eMMC de la consola. Un pipeline propio no requiere inyectar imágenes sueltas en subcarpetas de la tarjeta SD para estas aplicaciones, ya que la decoración multimedia enriquecida se delega por completo al frontend central (Daijishō o ES-DE).

## Notas

- **Optimización del formato de compresión CHD (v5)**: este es el punto de ingeniería más crítico. Los emuladores de alto rendimiento de Android de 64 bits (DuckStation, NetherSX2, Flycast, Yaba Sanshiro 2) leen de forma nativa y perfecta el formato comprimido CHD (v5). Es necesario automatizar la conversión masiva de ISOs y combinaciones `.bin`/`.cue` a CHD, lo que reduce el peso de la biblioteca a la mitad, estabiliza los fotogramas por segundo eliminando el cuello de botella de lectura del bus físico de la MicroSD y unifica los archivos de pistas múltiples en un solo bloque limpio indexable por el frontend.
- **El formato propietario RVZ para Dolphin**: para la emulación de Nintendo GameCube y Wii, Dolphin utiliza un formato de compresión sin pérdida avanzado llamado RVZ. Un pipeline propio debe pasar los volcados `.iso` por el compresor de Dolphin para convertirlos a RVZ utilizando un tamaño de bloque optimizado de 128 KB. El formato RVZ conserva las funciones de parches de texturas HD y trucos, ahorrando gigabytes críticos en la MicroSD.
- **Tratamiento de ROMsets Arcade**: al utilizar la versión de RetroArch de 64 bits o el emulador standalone FinalBurn Neo, las colecciones arcade deben compilarse utilizando estrictamente el archivo DAT oficial actualizado de FinalBurn Neo (romset en formato Non-Merged). Evitar inyectar sets obsoletos como MAME 2003 en dispositivos Android modernos, ya que los controladores gráficos actuales están optimizados para arquitecturas de emulación sincronizadas y actualizadas.
- **Gestión 1G1R y estabilidad**: aunque los emuladores standalone manejan mejor las carpetas pesadas que los frontends (no se cuelgan por falta de RAM al abrir una lista larga), tener miles de clones e idiomas duplicados dificulta la configuración de controles táctiles o el mapeo de configuraciones gráficas personalizadas por juego. Aplicar un filtro 1G1R limpio asegura una biblioteca optimizada y un rendimiento de juego fluido y ordenado.
