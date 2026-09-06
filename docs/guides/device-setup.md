# Preparar una distribución para un dispositivo

Secuencia de principio a fin para dejar un dispositivo de `docs/devices.md` funcionando con su distribución recomendada. No introduce contenido nuevo — encadena en orden las guías y catálogos que ya existen por separado.

## 1. Decidir qué instalar

Consultar la fila del dispositivo en `docs/distributions.md`: software recomendado (CFW/OS), frontend recomendado y contenido recomendado. Si el dispositivo no tiene fila, o está en `[TODO]`, resolver eso primero (`prompts/distribution_research.md`) antes de continuar.

## 2. Instalar el CFW/OS

Seguir la guía correspondiente en `docs/guides/cfw/<cfw>.md` (ver índice en [cfw/README.md](cfw/README.md)). El tipo de instalación (imagen flasheada, extracción a SD, fastboot/herramienta de fabricante) está indicado en cada guía.

## 3. Preparar el romset

Independiente del dispositivo concreto: seguir `docs/guides/romsets/workflow.md` (DAT → auditoría → 1G1R → parcheo → compresión → gamelist), usando `docs/romsets.md` para saber qué fuente/DAT corresponde a cada sistema. El detalle de cada fase (comandos, parámetros) está en `docs/guides/tools/README.md`. El formato de ROM final por sistema (cartucho/plano, CHD, RVZ, CSO...) sigue la clasificación de `docs/guides/romsets/README.md#clasificación-de-sistemas-por-flujo`.

## 4. Preparar la BIOS

Ver `docs/bios.md` para qué ficheros exige cada sistema (obligatorios/opcionales) y `docs/guides/bios.md` para cómo obtenerlos (volcado de hardware propio), verificarlos (hash) y organizarlos (nombre exacto, subcarpetas especiales).

## 5. Desplegar en las rutas del CFW instalado

Con el CFW ya instalado (paso 2) y el romset + BIOS ya preparados (pasos 3-4), copiar cada cosa a su ruta según `docs/system-paths.md`: ROMs, BIOS, saves/states (vacíos en una instalación nueva), gamelist.xml y media.

## 6. Configurar el frontend

Seguir la guía correspondiente en `docs/guides/apps/<frontend>.md` (ver índice en [apps/README.md](apps/README.md)) para el frontend recomendado en el paso 1 — solo aplica cuando el frontend requiere configuración propia además de la instalación del CFW (algunos vienen embebidos y preconfigurados).

## 7. Personalizar (opcional)

Temas de frontend y overlays/bezels por sistema: ver la sección de overlays/bezels en `docs/references.md` para el criterio de cuándo aplican, y usar `prompts/theme_bezel_research.md` para buscar y verificar el pack concreto contra la fuente primaria del dispositivo+CFW.

## 8. Verificar perfil de rendimiento (si aplica)

Si el hardware trabaja en o más allá de sus límites (sin stick analógico, SoC justo para ciertos sistemas), consultar `docs/guides/hardware-profiles/README.md` para saber qué juegos/sistemas tienen rendimiento curado documentado para esa combinación hardware+CFW.
