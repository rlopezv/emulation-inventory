# Prompt - Investigar dispositivo para devices.md

Voy a darte el nombre (marca + modelo) de un dispositivo de emulación (handheld, SBC, tablet o bartop).

Tu tarea es investigar sus especificaciones técnicas y devolver una fila lista para añadir a `docs/devices.md`, siguiendo exactamente las convenciones de ese documento.

## Columnas a rellenar

| Columna | Qué investigar |
| --- | --- |
| Marca | Fabricante o marca comercial |
| Modelo | Nombre de modelo exacto (sin la marca) |
| Procesador | SoC/CPU principal, con núcleos y frecuencia si están documentados |
| Memoria | RAM disponible |
| Pantalla | Tamaño de pantalla en pulgadas |
| Resolución | Resolución nativa de la pantalla |
| Aspect Ratio | Relación de aspecto de la pantalla |
| Orientación | Posición de uso y factor de forma (ver valores normalizados abajo) |
| Año salida | Año de lanzamiento comercial |
| Fiabilidad | Confianza en los datos que tú mismo documentas, no calidad del hardware (ver criterio abajo) |
| SD | Configuración de ranuras de almacenamiento externo (ver formato abajo) |
| Imagen | Nombre de archivo propuesto para `docs/imgs/` (no lo crees, solo propón el nombre) |

## Valores normalizados de Orientación

Usa uno de estos, o propón uno nuevo coherente si ninguno encaja (indícalo explícitamente si lo haces):

- SBC — placa sin pantalla
- Horizontal — pantalla apaisada, posición de juego estándar
- Vertical — pantalla en portrait
- Clamshell horizontal — formato concha con pantalla horizontal
- Horizontal tablet — tablet con pantalla apaisada
- Dual-screen clamshell — formato consola con dos pantallas
- Arcade tabletop horizontal — formato tabletop/bartop de pantalla fija
- Mini arcade tabletop fija / horizontal — formato bartop miniatura

## Formato de SD

Usa uno de estos patrones, adaptando el tamaño si es interno:

- `TF1` — única ranura microSD
- `TF1 + TF2` — dos ranuras microSD
- `TF Interna` — microSD fija interna sin ranura accesible externamente
- `TF Interna + TF1` — microSD fija interna + ranura microSD externa
- `TF Interna (XX GB) + TF1` — microSD interna fija con tamaño conocido + ranura microSD externa
- `Interna (XX GB)` — almacenamiento eMMC/UFS sin ranura externa
- `Interna (XX GB) + TF1` — almacenamiento eMMC/UFS + ranura microSD

## Criterio de Fiabilidad

Evalúa cuántas fuentes independientes confirman cada dato, no lo mezcles con tu opinión sobre el hardware en sí:

- Muy alta — datos verificados en múltiples fuentes fiables (ficha oficial del fabricante + reviews técnicos coincidentes)
- Alta — datos bien documentados con alta confianza (una fuente fiable clara, sin contradicciones)
- Media-Alta — datos mayoritariamente fiables con alguna incertidumbre menor (algún campo sin confirmar)
- Media — datos parciales o con fuentes contradictorias
- Baja — datos escasos, especulativos o sin verificar

## Reglas

1. No inventes datos. Si un campo no se puede verificar con confianza razonable, usa `[TODO]` en esa celda en vez de una estimación no marcada como tal.
2. No mezcles software, CFW ni recomendaciones de firmware en la respuesta — `docs/devices.md` es solo inventario de hardware.
3. Si el dispositivo tiene varias variantes/revisiones de hardware relevantes (ej. distinto SoC entre v1 y v2), indícalo en el propio campo o pregunta antes de asumir cuál es la que se está documentando.
4. Cita brevemente de qué tipo de fuente sale cada dato dudoso (ficha oficial, review, foro comunitario) como nota aparte de la fila, no dentro de la tabla.
5. Devuelve el resultado como una única fila de tabla Markdown, lista para pegar en `docs/devices.md`, con esta cabecera de referencia:

```markdown
| Marca | Modelo | Procesador | Memoria | Pantalla | Resolución | Aspect Ratio | Orientación | Año salida | Fiabilidad | SD | Imagen |
```

6. Después de la fila, añade una lista breve de qué campos quedaron en `[TODO]` y por qué, si los hay.
