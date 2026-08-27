# Guías de uso de herramientas

Guías de detalle de uso (comandos, parámetros, ejemplos) de las herramientas de PC catalogadas en `docs/tools.md`, organizadas por tarea. Todas las guías tienen ya contenido sustancial, pero no se ha auditado sistemáticamente cada afirmación contra la documentación oficial de cada herramienta — al completar o revisar una guía, contrastar contra la fuente primaria (repo, sitio de documentación oficial) en vez de asumir que lo ya escrito es correcto.

Complementan a [docs/guides/romsets/workflow.md](../romsets/workflow.md), que define el flujo end-to-end por fases y enlaza aquí para el detalle de cada una. No duplican el catálogo de `docs/tools.md` (nombre, categoría, estado, enlace) ni el pipeline de scripts propios documentado en [docs/guides/romsets/custom-pipeline.md](../romsets/custom-pipeline.md); donde una tarea coincide con ese pipeline, la guía enlaza a él en vez de repetir contenido.

| Tarea | Fase de workflow.md | Guía |
| --- | --- | --- |
| Generación/obtención de DAT | 1 | [dat-generation.md](dat-generation.md) |
| Procesado de DAT (conversión de formato) | 2 | [dat-conversion.md](dat-conversion.md) |
| Auditoría de romset contra DAT | 3 | [romset-audit.md](romset-audit.md) |
| Limpieza de romset | 4 | [romset-cleaning.md](romset-cleaning.md) |
| Filtrado 1G1R | 5 | [1g1r-filtering.md](1g1r-filtering.md) |
| Parcheo | 6 | [patching.md](patching.md) |
| Compresión / conversión de formato | 7 | [conversion-compression.md](conversion-compression.md) |
| Generación de gamelist.xml | 9 | [gamelist-generation.md](gamelist-generation.md) |
| Obtención de media | 10 | [media-scraping.md](media-scraping.md) |

La fase 8 (organización en `data/roms`) no tiene guía propia aquí: está cubierta por `build-complete-romset.ps1` / `promote-complete-romset.ps1`, documentados en [docs/guides/romsets/custom-pipeline.md](../romsets/custom-pipeline.md).
