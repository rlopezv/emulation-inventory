# Preparación de romsets — Cartucho / plano

Flujo de preparación para consolas de cartucho y handhelds verificados con DAT No-Intro — el caso más simple de los cuatro tipos de fuente (frente a microcomputers en [microcomputers.md](microcomputers.md), discos ópticos en [optical-chd.md](optical-chd.md) y arcade en [arcade.md](arcade.md)), ya que no requiere gestión de CHD/BIOS/samples, conversión de contenedor ni diversidad de tipo de medio. Sigue el mismo orden de fases que [docs/guides/romsets/workflow.md](workflow.md); aquí solo se resume qué aplica específicamente a este tipo de fuente, con el detalle completo de cada herramienta en [docs/guides/tools/](../tools/README.md).

## Fuente

No-Intro es la fuente principal (fase 1) — ver [dat-generation.md](../tools/dat-generation.md#no-intro-dat-o-matic) para el flujo completo de DAT-o-MATIC (esquema Parent-Clone obligatorio si se va a aplicar 1G1R después). Para los microcomputers con fuente alternativa (TOSEC, libretro-database, Non-Redump), ver las secciones correspondientes del mismo fichero.

## Verificación contra DAT

Fase 3 — ver [romset-audit.md](../tools/romset-audit.md). JRomManager como herramienta principal; sin CHD ni RVZ implicados en este tipo de fuente, no aplica la sección de validación por hash de discos ópticos.

## Filtrado 1G1R

Fase 5 — ver [1g1r-filtering.md](../tools/1g1r-filtering.md). retool como herramienta principal (requiere el esquema Parent-Clone obtenido en la fase 1); Igir como alternativa moderna para entornos de automatización.

**Parcheo (fase 6, si aplica):** traducciones/hacks sobre cartucho son el caso más común de esta fase — ver [patching.md](../tools/patching.md) (Lunar IPS/Flips para IPS/BPS, formatos habituales en sistemas de 8/16 bits).

## Organización en data/roms

Fase 8 — sin conversión de formato previa (fase 7 no aplica a ROM planas de cartucho, a diferencia de discos ópticos o GameCube/Wii). Ver el pipeline propio (`build-complete-romset.ps1`/`promote-complete-romset.ps1`) en [custom-pipeline.md](custom-pipeline.md).

## Generación de gamelist.xml y media

Fases 9-10 — ver [gamelist-generation.md](../tools/gamelist-generation.md) y [media-scraping.md](../tools/media-scraping.md). Sin particularidades específicas de cartucho frente a otros tipos de fuente en este paso.

## Notas

Al no requerir CHD/RVZ ni BIOS/samples compartidos, este es el flujo con menos pasos intermedios de los tres tipos de fuente — la mayor parte de la complejidad recae en elegir bien la variante del DAT en la fase 1 (headered/headerless, byte order, etc. — ver `docs/references.md#no-intro` y las secciones de casos especiales de N64/NES/SNES/Atari 7800/Atari Lynx/FDS ahí documentadas, y las notas ya anotadas por sistema en `docs/romsets.md`).
