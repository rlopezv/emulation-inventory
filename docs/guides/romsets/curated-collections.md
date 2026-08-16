# Colecciones curadas (borrador — pendiente de verificación de fuentes)

**Estado: esbozo inicial, no integrado todavía en el resto de la documentación.** Este fichero es autocontenido a propósito — no está enlazado desde `docs/guides/romsets/README.md` ni desde ningún otro documento hasta que las fuentes citadas aquí se verifiquen con el mismo nivel de rigor que el resto del repo (confirmar con datos reales, no solo con lo que dice la fuente de sí misma).

## Qué es esto

Hasta ahora `docs/romsets.md` y `data/dats/` solo contemplan dos tipos de conjunto por sistema: **Fullset** (catálogo completo) y **1G1R** (una ROM por juego, filtrado por región/idioma). Una **colección curada** es un tercer tipo de conjunto, ortogonal a los otros dos: un subconjunto (o cruce de varios sistemas) seleccionado por un criterio editorial — tema, publisher, "mejores juegos", limitación de espacio — en vez de por reglas mecánicas de deduplicación regional.

No sustituye a Fullset/1G1R; se construye a partir de uno de ellos (normalmente el 1G1R) aplicando un filtro de lista curada encima.

## Precedente ya existente en este repo

`metadata/dat/hyperspin/` ya contiene colecciones de este tipo, sin que hasta ahora se hayan documentado como tal: ficheros `<Publisher> Classics.xml` (`Namco Classics.xml`, `Atari Classics.xml`, `Capcom Classics.xml`, `Data East Classics.xml`, `Irem Classics.xml`, `Konami Classics.xml`, `Midway Classics.xml`, `Nintendo Classics.xml`, `SNK Classics.xml`, `Sega Classics.xml`, `Taito Classics.xml`), formato HyperSpin "menu" (`<game name="<shortname MAME>">` con `<description>`, sin CRC/manufacturer/year rellenos en la muestra inspeccionada). Agrupan juegos arcade de un mismo fabricante en una única "rueda" de frontend, cruzando placas/hardware distintos bajo un mismo tema.

## Fuentes candidatas identificadas (sin verificar en profundidad todavía)

| Fuente | Qué es (según investigación preliminar) | Nivel de confianza |
| --- | --- | --- |
| HyperSpin `<Publisher> Classics.xml` | Ya en `metadata/dat/hyperspin/`, formato conocido, contenido real inspeccionado directamente. | Alto — datos ya en el repo |
| Hardware Target Game Database (HTGDB) — `github.com/frederic-mahe/Hardware-Target-Game-Database` | Proyecto de investigación archivística: layouts de fichero/carpeta optimizados para hardware real (flashcarts, MiSTer FPGA); de aquí salen "gamepacks" empaquetados por sistema (existe una colección "HTGDB Gamepacks" en archive.org). **Corrección importante:** no es "Hardcore Gaming 101" (confusión de sigla inicial del usuario) — son proyectos distintos que solo coinciden en las siglas. | Medio — confirmado que existe y qué es por búsqueda web, no inspeccionado el contenido real de un gamepack |
| Tiny Best Set: GO! — alojado en archive.org (`archive.org/details/tiny-best-set-go`) | Colección "best of" curada a mano para dispositivos de almacenamiento limitado (Miyoo Mini/Onion OS, RG35XX/GarlicOS), ~1900 juegos cruzando Arcade/Neo Geo/Atari 2600/TurboGrafx-16/GB/GBC/GBA/NES/SNES/Game Gear/Master System/Genesis; variantes más grandes (~55-95GB) añaden Sega CD/TurboGrafx CD/PSX. | Medio — confirmado que existe y su alcance aproximado por búsqueda web, no inspeccionado el contenido real |

[TODO: verificar cada fuente candidata con el mismo rigor que `MAMERedump` (descargar/inspeccionar contenido real, no solo la descripción) antes de decidir si se usan como referencia de diseño, como fuente de datos, o se descartan.]

## Preguntas de diseño abiertas (sin resolver)

- ¿Dónde viven las colecciones curadas en la estructura del repo? Candidatos: `data/dats/<sistema>/collections/<nombre>/`, o una carpeta nueva paralela a `fullset`/`1g1r` en `data/dats/`.
- ¿Se construyen sobre el DAT Fullset o sobre el 1G1R ya filtrado?
- ¿Cómo se referencia la pertenencia de un juego a una colección? Lista de nombres plana (como los HyperSpin `.xml`), o un campo nuevo en `metadata/dat-index/<id>.json` (similar a como `members[]` ya guarda `category`).
- ¿Colecciones mono-sistema (ej. "Namco Classics" dentro de arcade) frente a colecciones transversales multi-sistema (ej. Tiny Best Set, que cruza consolas)? Puede que necesiten modelarse distinto — la primera encaja en el patrón ya usado por `docs/arcade/arcade-{system}.md` (catálogo curado Bartop), la segunda no tiene precedente en el repo todavía.
- ¿Reutilizamos el criterio de curación de las fuentes externas tal cual, o solo como inspiración para una lista propia?
- **Formato de las ROMs dentro de la colección — sin decidir todavía.** No hay ninguna recomendación fijada de si una colección curada debe distribuirse en el mismo formato que el Fullset/1G1R de origen (CHD para óptico, plano/comprimido para cartucho) o en un formato propio pensado para el caso de uso de la colección (ej. las fuentes candidatas de arriba están orientadas a espacio limitado en flashcart/SD — HTGDB explícitamente optimiza layout para hardware real, Tiny Best Set apunta a Miyoo Mini/RG35XX vía Onion/GarlicOS). Antes de fijar una recomendación habría que revisar qué formato usa cada fuente candidata en la práctica (pendiente, parte de la verificación de fuentes de la sección anterior) y si eso encaja con `docs/system-paths.md` (rutas esperadas por CFW) para los dispositivos de `docs/devices.md` a los que vaya destinada la colección.

## Siguiente paso

Verificar las fuentes candidatas (ver tabla de arriba) antes de tocar `docs/romsets.md`, `CLAUDE.md` (descripción de `data/dats/`) o `docs/guides/romsets/README.md`. Este fichero se integrará en la documentación principal solo cuando ese trabajo esté hecho.
