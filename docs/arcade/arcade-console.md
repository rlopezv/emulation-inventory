# Catálogo consolas

Este documento define una colección **Bartop Curated** para sistemas clásicos emulados en entorno horizontal, orientada a **EmulationStation**, **ES-DE**, **Batocera** y **RetroArch**.

No se trata de un fullset, una colección de preservación histórica ni una selección No-Intro completa. La finalidad principal es construir una lista jugable, limpia y coherente para una bartop: juegos rápidos, claros, rejugables y adecuados para controles arcade.

La pregunta de curación no es únicamente si un juego es importante o conocido, sino:

> ¿Merece ocupar espacio en una bartop?

---

### Capas de decisión

La selección se organiza en varias capas sucesivas. Un juego debe superar todas las capas aplicables para permanecer en el catálogo final.

#### Layer 0 — Inventario

Se parte del catálogo inicial proporcionado para cada sistema. En esta fase se identifican:

* Duplicados exactos.
* Variantes regionales redundantes.
* Revisiones redundantes.
* Versiones alternativas del mismo juego.
* Juegos CD, HuCard, cartucho u otros formatos, según corresponda al sistema.
* Homebrew, hacks, traducciones, prototipos, betas y demos.
* Juegos dependientes de periféricos especiales.

Cada entrada original debe terminar con un estado claro:

* **Conservado**.
* **Eliminado**.
* **Sustituido por 1G1R**.

---

#### Layer 1 — Adecuación bartop

Se evalúa si el juego funciona bien en una bartop horizontal. Se priorizan juegos con:

* Inicio rápido.
* Partidas cortas o rejugables.
* Acción inmediata.
* Controles simples.
* Lectura visual clara.
* Buena respuesta con joystick y botones arcade.
* Valor multijugador local cuando proceda.

Se penalizan juegos que dependan excesivamente de:

* Texto.
* Menús complejos.
* Progresión larga.
* Exploración lenta.
* Guardado frecuente.
* Periféricos especiales.
* Teclado, ratón o controles analógicos.

---

#### Layer 2 — Tier de calidad

Cada juego recibe un **Tier** según su relevancia jugable dentro del sistema y su valor real en una colección bartop.

| Tier | Significado      | Decisión |
| ---- | ---------------- | -------- |
| S    | Imprescindible   | Mantener |
| A    | Muy recomendable | Mantener |
| B    | Recomendable     | Mantener |
| C    | Prescindible     | Eliminar |
| D    | No recomendable  | Eliminar |

El catálogo final solo conserva juegos **Tier S, A o B**.

---

#### Layer 3 — Arcade Rating

El **Arcade Rating** mide la adecuación específica del juego al entorno bartop, no su importancia histórica.

| Arcade | Significado          | Decisión |
| ------ | -------------------- | -------- |
| S      | Perfecto para bartop | Mantener |
| A      | Muy adecuado         | Mantener |
| B      | Poco adecuado        | Eliminar |
| C      | No adecuado          | Eliminar |

El catálogo final solo conserva juegos con **Arcade S o Arcade A**.

---

#### Layer 4 — 1G1R

Se aplica una política **1G1R** para evitar redundancia. En general, se conserva una sola versión por juego.

La versión preferente se elige según:

1. Mejor idioma cuando el texto sea relevante.
2. Mejor rendimiento.
3. Mejor velocidad.
4. Mejor conversión arcade.
5. Mayor compatibilidad con controles simples.
6. Versión más completa o pulida.
7. Mayor adecuación al sistema objetivo.

Pueden mantenerse varias versiones solo si existe una diferencia significativa de contenido, rendimiento, jugabilidad, región o experiencia.

Toda excepción debe justificarse en la columna **Notas**.

---

#### Layer 5 — Exclusiones automáticas

Se eliminan automáticamente:

* Homebrew.
* Hacks.
* Traducciones no oficiales.
* Prototipos.
* Betas.
* Demos.
* Juegos unlicensed.
* Duplicados.
* Revisiones redundantes.
* Variantes regionales redundantes.
* Juegos educativos.
* Juegos infantiles de baja calidad.
* Shovelware.
* Juegos dependientes de teclado.
* Juegos dependientes de ratón.
* Juegos dependientes de analógico.
* Juegos dependientes de periféricos especiales, salvo indicación contraria.

---

#### Layer 6 — Detección de ausencias

Después de limpiar y curar el catálogo inicial, se revisa el catálogo histórico reconocido del sistema para detectar ausencias relevantes.

Se pueden añadir juegos no presentes en la lista inicial cuando cumplan estas condiciones:

* Tier S, A o B.
* Arcade Rating S o A.
* Buena adecuación al sistema y al formato.
* Valor claro en bartop.

No existe un límite fijo de añadidos.

---

## Leyenda de campos

| Campo   | Valores               | Descripción                                                 |
| ------- | --------------------- | ----------------------------------------------------------- |
| Juego   | Texto                 | Nombre del juego conservado en el catálogo final.           |
| Género  | Texto                 | Género principal desde la perspectiva bartop.               |
| Tier    | S, A, B               | Calidad e importancia dentro de la colección.               |
| Arcade  | S, A                  | Adecuación al uso en bartop.                                |
| Rot     | H, V, HV              | Orientación recomendada: horizontal, vertical o mixta.      |
| Ctrl    | 2B, 3B, 6B, LG, WHEEL | Control recomendado.                                        |
| Players | 1P, 2P, 3P, 4P, 5P    | Número máximo razonable de jugadores.                       |
| Notas   | Texto                 | Justificación, 1G1R, región, formato o excepción relevante. |

---

## Leyenda de orientación

| Valor | Significado                                          |
| ----- | ---------------------------------------------------- |
| H     | Horizontal                                           |
| V     | Vertical                                             |
| HV    | Alterna o funciona razonablemente en ambos contextos |

---

## Leyenda de controles

| Valor | Significado                     |
| ----- | ------------------------------- |
| 2B    | Joystick + 2 botones            |
| 3B    | Joystick + 3 botones            |
| 6B    | Joystick + 6 botones            |
| LG    | Lightgun                        |
| WHEEL | Volante o control de conducción |

Cuando un juego requiere **LG** o **WHEEL**, solo debe mantenerse si la bartop o instalación objetivo soporta ese periférico o si existe un mapeo cómodo y jugable.

---

## Política regional

La prioridad regional general es:

1. España / versión en español.
2. Europa con español.
3. USA / inglés.
4. Japón.

Esta prioridad puede cambiar cuando el idioma no sea relevante para la experiencia.

En géneros como shoot’em up, fighting, carreras arcade, beat’em up, puzzle arcade o juegos de acción inmediata, el idioma suele ser secundario. En esos casos puede priorizarse una versión japonesa o estadounidense si ofrece mejor rendimiento, velocidad, fidelidad arcade o compatibilidad.

---

## Criterio por tipo de juego

Se favorecen especialmente:

* Shoot’em up.
* Beat’em up.
* Run & gun.
* Fighting.
* Puzzle arcade.
* Plataformas arcade.
* Carreras arcade.
* Sports arcade.
* Maze games.
* Pinball.
* Acción de pantalla fija.
* Cooperativos locales.

Se penalizan o excluyen normalmente:

* RPG largos.
* Aventuras conversacionales.
* Visual novels.
* Estrategia pesada.
* Simuladores lentos.
* Juegos de gestión.
* Juegos excesivamente dependientes del idioma.
* Juegos con ritmo incompatible con partidas cortas.
* Títulos técnicamente pobres o frustrantes sin valor arcade claro.

---

## Catálogos arcade por sistema

| Sistema | Fabricante | Año | Bits / arquitectura | Medio | Enfoque de curación | Acceso |
| --- | --- | ---: | --- | --- | --- | --- |
| NES | Nintendo | 1983 | 8-bit | Cartucho | Acción simple, arcade temprano, run & gun, plataformas | [NES](./arcade-nes.md) |
| Master System | Sega | 1985 | 8-bit | Cartucho / Card | Arcade Sega, shmups, plataformas rápidos | [Master System](./arcade-mastersystem.md) |
| Mega Drive | Sega | 1988 | 16-bit | Cartucho | Beat'em up, run & gun, shmups, lucha | [Mega Drive](./arcade-megadrive.md) |
| SNES | Nintendo | 1990 | 16-bit | Cartucho | Cooperativos, beat'em up, shmups, run & gun, acción inmediata | [SNES](./arcade-snes.md) |
| Neo Geo CD | SNK | 1994 | 16-bit arcade | CD-ROM | Exclusivos CD o mejoras evidentes frente a AES/MVS | [Neo Geo CD](./arcade-neogeocd.md) |
| PC Engine | NEC / Hudson Soft | 1987 | 8-bit CPU / 16-bit vídeo | HuCard | Shmups, arcade ports, acción inmediata | [PC Engine](./arcade-pcengine.md) |
| PC Engine CD | NEC / Hudson Soft | 1988 | PC Engine + CD-ROM² | CD-ROM | Shmups CD, arcade ports, fighting, acción | [PC Engine CD](./arcade-pcenginecd.md) |
| PlayStation 1 | Sony | 1994 | 32-bit | CD-ROM | Lucha, carreras arcade, lightgun, shmups, acción 3D | [PlayStation 1](./arcade-psx.md) |
| Saturn | Sega | 1994 | 32-bit | CD-ROM | Arcade japonés, lucha, shmups, beat'em up, lightgun y ports Sega/Capcom/SNK | [Saturn](./arcade-saturn.md) |
| Nintendo 64 | Nintendo | 1996 | 64-bit | Cartucho | 4P local, carreras arcade, wrestling, fighting, shooters, party, puzzle | [Nintendo 64](./arcade-n64.md) |
| Dreamcast | Sega | 1998 | 128-bit | GD-ROM | Oficiales, arcade ports e indie/post-commercial arcade-like; sin Atomiswave ports | [Dreamcast](./arcade-dreamcast.md) |
| Sega 32X | Sega | 1994 | Add-on 32-bit | Cartucho 32X | Arcade ports, acción poligonal, shooters | [Sega 32X](./arcade-sega32x.md) |
| Sega CD | Sega | 1991 | Mega Drive + CD | CD-ROM | Ports CD, FMV selectivo, racers, shooters | [Sega CD](./arcade-segacd.md) |
