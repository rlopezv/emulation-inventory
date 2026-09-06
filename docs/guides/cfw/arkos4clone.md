# ArkOS4Clone

ArkOS4Clone es una adaptación comunitaria de ArkOS/dArkOS pensada para extender su compatibilidad a clones de hardware RK3326 no soportados oficialmente (más allá del RG351MP original) — variantes tipo R36S y hardware de marca XiFan/AISLPC, entre otros. Retomado por la comunidad (liderada por `lcdyk0517`) tras el archivado de ArkOS oficial, sigue actualizando componentes como PPSSPP y RetroArch.

## Dispositivos aplicables

- AISLPC R36T Max (RK3326, panel cuadrado 720×720) — confirmado, configuración dedicada en `consoles/r36tmax/` a 720p
- Familia de clones R36S y hardware XiFan compatible con el sistema de detección de DTB del proyecto (lista completa no exhaustiva — verificar el dispositivo concreto con la herramienta de identificación antes de asumir soporte)
- Release `20260815` añadió soporte adicional para RGB10, RGBV10, RGB10X (confirmar vigencia en la release más reciente antes de instalar)

## Tipo de instalación

Imagen flasheada a SD (kernel/rootfs de (d)ArkOS 4.4 portado), con selección de **DTB (Device Tree Binary)** específico del modelo de clon durante la configuración — este es el paso que diferencia la instalación de la del ArkOS oficial, ya que el hardware clon no se autodetecta de forma fiable sin él.

## Requisitos previos

- Tarjeta MicroSD (sistema, y opcionalmente una segunda para ROMs, mismo esquema TF1/TF2 que ArkOS).
- Software de flasheo de imagen (Rufus/BalenaEtcher/`dd`).
- **Antes de encender por primera vez**: conectar el cargador; en dispositivos con batería original, confirmar que el voltaje esté por encima de 3.3V (requisito explícito del proyecto — un voltaje insuficiente puede corromper el primer arranque).

## Descarga

- Repositorio oficial: <https://github.com/lcdyk0517/arkos4clone>
- Wiki del proyecto (lectura recomendada antes de instalar): <https://github.com/lcdyk0517/arkos4clone/wiki>
- Herramienta de identificación de DTB (necesaria para clones no autodetectados): <https://r36s.dpdns.org/dtbTools.html>

## Preparación de almacenamiento

Mismo esquema que ArkOS (ver `arkos.md`): SD1 sistema, SD2 opcional para ROMs. `[TODO]` confirmar si ArkOS4Clone requiere algún paso de preparación distinto al ArkOS oficial (no verificado en detalle contra la wiki).

## Instalación

1. Identifica el tipo exacto de tu clon con la herramienta de DTB (`r36s.dpdns.org/dtbTools.html`) antes de flashear — **no renombrar el DTB arbitrariamente**: el propio proyecto advierte que un nombre incorrecto puede hacer que el sistema detecte el dispositivo como un R36S genérico en vez del modelo real.
2. Flashea la imagen correspondiente a la SD1 con la herramienta de flasheo habitual.
3. Para el R36T Max en concreto, la configuración vive en `consoles/r36tmax/` (resolución 720p) — confirmar que la release descargada incluye esta configuración antes de dar el flasheo por bueno.
4. Durante la configuración se elige entre dos kernels disponibles — `[TODO]` confirmar el criterio de elección (no detallado en el extracto de wiki revisado).

## Primer arranque

1. Conecta el cargador y verifica el voltaje de batería (>3.3V) antes de encender, según el requisito de arriba.
2. La detección del dispositivo la realiza el propio programa `console-detect`, leyendo `/boot/boot.ini` — si el dispositivo arranca identificado como el modelo incorrecto, revisar el nombre del DTB usado en el paso de instalación.
3. `[TODO]` resto del flujo de primer arranque (selección de tarjeta ROMs, expansión de partición, etc.) no confirmado en detalle — previsiblemente análogo al de ArkOS oficial (ver `arkos.md`) por herencia directa del proyecto, pero sin verificar paso a paso.

## Configuración post-instalación

`[TODO]` no confirmado en detalle contra la wiki — previsiblemente igual que ArkOS oficial (mismo `es_systems.cfg`/estructura de `/roms/`) por herencia directa, pendiente de verificar.

## Notas

- **No confundir con ArkOS oficial** (`arkos.md`) ni con dArkOS (`darkos.md`) — ArkOS4Clone es un fork específico para hardware clon no soportado por ninguno de los dos, con su propio mecanismo de selección de DTB.
- El proyecto tiene actividad reciente (release `20260815` confirmada) y buena adopción comunitaria (cientos de estrellas/forks en GitHub a fecha de esta revisión) — no tratarlo como legado pese a partir de un ArkOS oficial ya archivado.
- Revisar siempre la wiki del proyecto antes de instalar, especialmente la sección de identificación de DTB — es el paso que más frecuentemente causa problemas en clones no oficiales.
