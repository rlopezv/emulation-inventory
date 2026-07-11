Este es el prompt que yo usaría. Mantiene prácticamente toda la capacidad de control de la versión endurecida, pero elimina redundancias y concentra la validación en un único punto.

---

# Bartop Curated Collection v2

Voy a adjuntar un catálogo de juegos para el sistema `<SISTEMA>`.

Tu tarea es transformarlo en una colección **Bartop Curated**.

## Objetivo

Generar una colección optimizada para:

* Bartop horizontal.
* EmulationStation.
* ES-DE.
* Batocera.
* RetroArch.

No es una colección de preservación histórica.

No es un fullset.

No es una colección No-Intro.

La prioridad es la experiencia de juego.

La pregunta principal NO es:

> "¿Es un juego importante?"

La pregunta principal es:

> "¿Merece ocupar espacio en una bartop?"

---

# Flujo interactivo obligatorio

Antes de comenzar el análisis:

1. Solicita el sistema objetivo.
2. Solicita el catálogo inicial de juegos.
3. Confirma si deben incluirse o excluirse variantes CD cuando existan.
4. Una vez recibidos los datos, aplica automáticamente las reglas específicas del sistema seleccionado.

---

# Proceso obligatorio de curación

Antes de generar cualquier salida final debes completar internamente las siguientes fases:

### Fase 0: Inventario

* Contar todos los juegos originales.
* Detectar duplicados exactos.
* Detectar variantes regionales redundantes.
* Detectar revisiones redundantes.
* Detectar variantes CD.
* Detectar homebrew, hacks, traducciones, prototipos y betas.

Ningún juego puede quedar sin estado final.

Cada juego debe terminar exactamente en uno de estos estados:

* Conservado.
* Eliminado.
* Sustituido por 1G1R.

---

### Fase 1: Evaluación

Asignar a todos los juegos:

* Tier.
* Arcade Rating.

Ningún juego puede quedar sin evaluar.

---

### Fase 2: Aplicación de filtros

Eliminar automáticamente:

* Tier C.
* Tier D.
* Arcade Rating B.
* Arcade Rating C.

Aplicar también todas las reglas de exclusión.

---

### Fase 3: Aplicación de 1G1R

Mantener una única versión por juego.

Permitir excepciones únicamente cuando exista:

* Diferencia significativa de contenido.
* Mejor rendimiento.
* Versión más cercana al arcade.
* Exclusiva regional.
* Mejor experiencia demostrable.

Toda excepción debe documentarse en la columna "Notas".

---

### Fase 4: Detección de ausencias

Revisar el catálogo histórico reconocido del sistema.

Identificar automáticamente juegos ausentes que sean:

* Tier S, A o B.
* Arcade Rating S o A.

Añadirlos automáticamente.

Justificar cada incorporación.

No existe límite de añadidos.

---

### Fase 5: Reconciliación

Verificar coherencia entre:

* Catálogo final.
* Juegos eliminados.
* Juegos añadidos.
* Estadísticas.

---

# Condiciones específicas por sistema

### NES

Prioriza conversions arcade, acción inmediata, run & gun, shoot'em up y beat'em up.

Favorece juegos compatibles con controles de 2 botones.

### Master System

Prioriza conversions arcade de Sega, shoot'em up, acción directa y plataformas arcade.

Favorece partidas cortas y alta rejugabilidad.

### SNES

Prioriza cooperativos, arcade conversions, beat'em up, shoot'em up, run & gun y acción inmediata.

Penaliza RPG y aventuras largas.

### Mega Drive

Prioriza run & gun, shoot'em up, beat'em up y acción arcade.

Favorece títulos Sega con alta rejugabilidad.

### PC Engine

Prioriza shoot'em up, arcade ports y acción inmediata.

Favorece HuCard/TurboGrafx-16 compatibles con controles simples.

Excluir PC Engine CD/TurboGrafx-CD salvo indicación explícita.

### PSX

Prioriza lucha, shoot'em up, lightgun, racers arcade y beat'em up.

Penaliza juegos excesivamente dependientes del analógico.

### Saturn

Prioriza arcade japoneses, lucha, shoot'em up y conversions arcade de Sega.

Favorece experiencias cercanas a recreativa.

### Dreamcast

Prioriza títulos derivados de NAOMI y Atomiswave.

Favorece lucha, shoot'em up, racers arcade y multijugador local.

---

# Exclusiones

Eliminar:

* Homebrew.
* Hacks.
* Traducciones.
* Prototipos.
* Betas.
* Demos.
* Unlicensed.
* Variantes redundantes.
* Revisiones redundantes.
* Duplicados.
* Juegos educativos.
* Juegos infantiles de baja calidad.
* Shovelware.
* Juegos dependientes de teclado.
* Juegos dependientes de ratón.
* Juegos dependientes de analógico.
* Juegos dependientes de periféricos especiales.

---

# Política regional y 1G1R

Prioridad regional:

1. España (ES)
2. Europa (EUR) con español
3. USA (EN)
4. Japón (JAP)

Reglas:

* Mantener español cuando el idioma sea relevante para la experiencia.
* Si el idioma no es relevante, priorizar la versión técnicamente superior.
* En shoot'em up, fighting, racers, beat'em up, puzzle y arcade-like el idioma no es determinante.
* Mantener JAP cuando sea claramente superior o más cercana al arcade.
* Mantener USA cuando sea técnicamente superior a EUR.
* Excluir revisiones regionales redundantes.

---

# Tier

### Tier S

Imprescindible.

### Tier A

Muy recomendable.

### Tier B

Recomendable.

### Tier C

Excluir.

### Tier D

Excluir.

Mantener únicamente Tier S, A y B.

---

# Arcade Rating

### Arcade S

Perfecto para bartop.

* Shoot'em up.
* Beat'em up.
* Fighting.
* Run & Gun.
* Puzzle arcade.
* Sports arcade.
* Maze.
* Platform arcade.

### Arcade A

Muy adecuado.

* Acción inmediata.
* Plataformas rápidos.
* Carreras arcade.
* Party games.

### Arcade B

Excluir.

### Arcade C

Excluir.

Mantener únicamente Arcade Rating S y A.

---

# Clasificación

| Campo   | Valores               |
| ------- | --------------------- |
| Tier    | S, A, B               |
| Arcade  | S, A                  |
| Rot     | H, V, HV              |
| Ctrl    | 2B, 3B, 6B, LG, WHEEL |
| Players | 1P, 2P, 3P, 4P        |

---

# Auditoría final obligatoria

Antes de responder verifica:

* Todos los juegos originales han sido procesados.
* Todos los juegos tienen Tier.
* Todos los juegos tienen Arcade Rating.
* Se han aplicado exclusiones.
* Se ha aplicado 1G1R.
* No existen duplicados.
* Todo añadido aparece en el catálogo final.
* Ningún eliminado aparece en el catálogo final.
* Las estadísticas cuadran.

La siguiente igualdad debe cumplirse exactamente:

```text
Total final =
Juegos originales
- Eliminados
+ Añadidos
```

Si cualquier comprobación falla:

**No generes la respuesta. Corrige primero.**

---

# Formato de salida obligatorio

## Leyenda

| Campo  | Valores               |
| ------ | --------------------- |
| Tier   | S, A, B               |
| Arcade | S, A                  |
| Rot    | H, V, HV              |
| Ctrl   | 2B, 3B, 6B, LG, WHEEL |

---

## Catálogo `<SISTEMA>` curado

| Juego | Género | Tier | Arcade |  Rot  | Ctrl  | Players | Notas |
| ----- | ------ | ---: | -----: | :---: | :---: | :-----: | ----- |

Incluir TODOS los juegos resultantes.

No truncar la tabla.

---

## Juegos eliminados

| Juego | Motivo |
| ----- | ------ |

---

## Juegos añadidos

| Juego | Motivo |
| ----- | ------ |

---

## Estadísticas

| Métrica           | Valor |
| ----------------- | ----- |
| Juegos originales | X     |
| Eliminados        | X     |
| Añadidos          | X     |
| Total final       | X     |

No resumir.

No mostrar únicamente diferencias.

Mostrar siempre el catálogo final completo.
