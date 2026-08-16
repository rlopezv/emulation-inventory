# Preparación de romsets — Cartucho / plano

Flujo de preparación para consolas de cartucho y handhelds verificados con DAT No-Intro — el caso más simple de los cuatro tipos de fuente (frente a microcomputers en [microcomputers.md](microcomputers.md), discos ópticos en [optical-chd.md](optical-chd.md) y arcade en [arcade.md](arcade.md)), ya que no requiere gestión de CHD/BIOS/samples, conversión de contenedor ni diversidad de tipo de medio. Sigue el mismo orden de fases que [docs/guides/romsets/workflow.md](workflow.md); aquí solo se resume qué aplica específicamente a este tipo de fuente, con el detalle completo de cada herramienta en [docs/guides/tools/](../tools/README.md).

## Fuente

No-Intro es la fuente principal (fase 1) — ver [dat-generation.md](../tools/dat-generation.md#no-intro-dat-o-matic) para el flujo completo de DAT-o-MATIC (esquema Parent-Clone obligatorio si se va a aplicar 1G1R después). Para los microcomputers con fuente alternativa (TOSEC, libretro-database, Non-Redump), ver las secciones correspondientes del mismo fichero.

## Formato de ROM recomendado por sistema

Sistemas clasificados como Cartucho/plano en [docs/guides/romsets/README.md](README.md#clasificación-de-sistemas-por-flujo). Salvo los casos señalados, No-Intro solo publica un formato para el sistema — no hay elección real que documentar, se listan igual por completitud. Detalle técnico completo de los casos especiales (headered/headerless, byte order) en `docs/references.md`.

| Identificador canónico | Formato recomendado | Notas |
| --- | --- | --- |
| `atari2600` | — | Formato único |
| `astrocade` | — | Formato único |
| `odyssey2` | — | Formato único |
| `intellivision` | — | Formato único |
| `gameandwatch` | — | Fuente libretro, no No-Intro |
| `atari5200` | — | Formato único |
| `vectrex` | — | Formato único |
| `atari7800` | BIN (headerless) | También A78 (headered, 128 bytes) — ver `docs/references.md#caso-especial--headered-vs-headerless-nes-snes-atari-7800-atari-lynx-fds` |
| `nes` | Headered (iNES, 16 bytes) | También Headerless — mismo caso especial de `docs/references.md` |
| `sg1000` | — | Incluye SC-3000 |
| `mastersystem` | — | Formato único |
| `fds` | FDS (raw) | También QD (QuickDisk) |
| `pcengine` | — | Formato único |
| `megadrive` | — | Formato único |
| `gb` | — | Formato único |
| `lynx` | LYX (headerless) | También LNX (headered, catálogo reducido) y BLL — mismo caso especial de `docs/references.md` |
| `gamegear` | — | Formato único |
| `snes` | Headerless (`.sfc`) | No-Intro no publica variante Headered por separado |
| `sega32x` | — | Formato único |
| `jaguar` | J64 | Ver nota en `docs/romsets.md` (ABS/COF vacíos, JAG solo 1 entrada) |
| `satellaview` | — | Formato único |
| `sufami` | — | Formato único |
| `n64` | BigEndian (`.z64`) | También ByteSwapped (`.v64`) — ver `docs/references.md#caso-especial--nintendo-64-orden-de-bytes-byte-order` |
| `64dd` | — | Formato único |
| `ngp` | — | Formato único |
| `gbc` | — | Subconjunto dual-mode/DMG-compatible (cartucho gris) ejecutable también en `gb`; no requiere DAT ni formato distinto |
| `ngpc` | — | Formato único |
| `supervision` | — | Formato único |
| `pokemini` | — | Formato único |
| `gba` | — | Formato único |
| `nds` | Decrypted | También Encrypted |
| `dsiware` | Decrypted | Variante No-Intro estándar; también disponibles Encrypted y CDN |
| `pspminis` | Decrypted | Contenido digital PSN |
| `psn` | Decrypted | Contenido digital PSN |
| `3ds` | `.3DS` (Desencriptado) o `.CCI` (comprimido, CSO para 3DS) | DAT No-Intro `Nintendo - Nintendo 3DS (Decrypted)`; también Encrypted |
| `3dseshop` | Digital (CDN) | DAT No-Intro `Nintendo - Nintendo 3DS (Digital) (CDN)`; también existen `(Digital) (Updates)` y `(Digital) (DLC)`, sin mapear todavía como fila propia en `docs/romsets.md` |
| `newn3ds` | Decrypted | También Encrypted |
| `virtualboy` | — | Formato único |
| `wswan` | — | Formato único |
| `wswanc` | — | Formato único |
| `psvita` | `.ZIP` (NoNpDrm comprimido) o `.PKG` (con clave de licencia) | Formatos soportados por Vita3K; solo catálogo digital cubierto (No-Intro `PSN Content`/`Updates`) |

**Casos especiales fuera de esta tabla** (ver [docs/guides/romsets/README.md](README.md#clasificación-de-sistemas-por-flujo)): `sgb` (sin DAT propio, requiere extraer del No-Intro de `gb`/`gbc` los títulos con soporte Super Game Boy) y `gx4000` (fuente TOSEC homebrew mal mantenida, requiere curación manual) no encajan limpio en este flujo simple.

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
