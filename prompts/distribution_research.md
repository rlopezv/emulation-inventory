# Prompt - Investigar recomendación de software para distributions.md

Voy a darte el nombre de un dispositivo ya presente en `docs/devices.md` (marca, modelo y specs de hardware).

Tu tarea es investigar qué CFW/OS/frontend le corresponde y devolver una fila lista para añadir a `docs/distributions.md`, siguiendo exactamente las convenciones de ese documento.

## Columnas a rellenar

| Columna | Qué investigar |
| --- | --- |
| Dispositivo | Nombre exacto tal como aparece en `docs/devices.md` |
| Familia | Familia de SoC/hardware para agrupación (ej. RK3326, H700, JZ4770) |
| Tipo | Categoría del software recomendado (ver valores normalizados abajo) |
| Software recomendado | CFW/OS/frontend principal recomendado |
| Alternativas | Opciones secundarias válidas, separadas por `/` |
| Frontend recomendado | Interfaz de usuario expuesta por el software recomendado |
| Instalación real | Software realmente instalado hoy (o `[TODO]`/`Desconocido` si no lo sabes) |
| Frontend real | Interfaz de la instalación real (o `[TODO]`/`Desconocido`) |
| Estado instalación | Estado verificado de la instalación real (ver valores normalizados abajo) |
| Contenido recomendado | Estrategia de distribución de contenido en tarjetas SD (ej. "TF1: sistema + ROMs, BIOS, saves") |
| Estado recomendación | Solidez de la recomendación (ver valores normalizados abajo) |
| Notas | Observaciones operativas, versiones, advertencias |

## Valores normalizados de Tipo

- CFW — firmware para un dispositivo o familia de hardware concreta
- OS Retro — sistema operativo retro de propósito general para SBC o PC
- OS Handheld — sistema operativo retro de propósito general para múltiples handhelds
- Android CFW — ROM Android personalizada orientada a emulación
- Stock Mod — modificación del firmware de fábrica sin reemplazarlo
- Frontend — aplicación de lanzador/interfaz sobre un OS existente

## Valores normalizados de Estado instalación

- Verificado — instalación confirmada y documentada
- Pendiente — instalación prevista pero no ejecutada
- No instalado — dispositivo sin instalar
- Desconocido — estado no verificado
- No aplica — dispositivo que no requiere instalación de CFW

## Valores normalizados de Estado recomendación

- Recomendado — opción principal clara y bien soportada
- Válido — opción funcional aunque no sea la principal
- Alternativo — alternativa razonable en contextos específicos
- Legado — recomendación histórica, superada por opciones más modernas
- Experimental — soporte no estable o en desarrollo
- No recomendado — opción desaconsejada para este dispositivo
- `[TODO]` — sin investigar/confirmar todavía

## Criterios de recomendación, en este orden de prioridad

1. Compatibilidad técnica con el dispositivo o familia de hardware.
2. Recomendación y adopción de la comunidad, consenso.
3. Madurez, estabilidad y mantenimiento activo.
4. Coherencia con el ecosistema de la documentación (evitar introducir un software sin relación con lo ya recomendado en dispositivos de la misma familia, salvo que esté justificado).
5. Facilidad para mantener una estructura de colección clara, documentable y migrable.
6. Simplicidad operativa.
7. Preferencias explícitas conocidas del usuario (ver más abajo).

## Preferencias conocidas a respetar

- Steam Deck está fuera de alcance, no lo tengas en cuenta como referencia.
- El usuario tiene licencia de LaunchBox BigBox.
- Koriki debe aparecer como alternativa relevante cuando el dispositivo sea Miyoo Mini, Miyoo Mini Plus o RG35XX original.
- RG35XX original NO debe tratarse como parte de la familia H700 moderna (SoC distinto).

## Reglas

1. Antes de proponer un software como recomendado o alternativa, comprueba si ya existe una fila para él en `docs/software.md` (mismo Nombre/Variante). Si no existe, indícalo explícitamente en tus notas de respuesta (fuera de la fila) en vez de inventar el nombre; puede hacer falta darlo de alta antes o junto con esta fila.
2. No inventes datos de instalación real: si no la conoces, usa `Desconocido` en Estado instalación y `[TODO]` en Instalación real/Frontend real.
3. No redefinas hardware, sistemas ni software aquí — esto es solo la recomendación y el estado de instalación.
4. Si hay varios dispositivos de la misma familia de SoC ya documentados en `docs/distributions.md`, prioriza coherencia con lo ya recomendado para esa familia salvo razón técnica concreta para desviarte (explícala en Notas).
5. Devuelve el resultado como una única fila de tabla Markdown, lista para pegar en `docs/distributions.md`, con esta cabecera de referencia:

```markdown
| Dispositivo | Familia | Tipo | Software recomendado | Alternativas | Frontend recomendado | Instalación real | Frontend real | Estado instalación | Contenido recomendado | Estado recomendación | Notas |
```

6. Después de la fila, añade una lista breve de: (a) qué software mencionado no existe todavía en `docs/software.md`, (b) qué campos quedaron en `[TODO]`/`Desconocido` y por qué.
