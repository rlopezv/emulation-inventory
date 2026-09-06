# GammaOS Nano

GammaOS Nano es una variante ligera de GammaOS Next orientada a dispositivos de formato reducido (handhelds pequeños/giratorios), con una interfaz de lanzador más minimalista que la UI completa de GammaOS Next — pensada para hardware con pantalla pequeña o factor de forma especial (ej. mecanismo giratorio) donde la UI completa no encaja bien o sobra complejidad. **Se distribuye desde el mismo repositorio y el mismo sistema de releases que GammaOS Next** (`TheGammaSqueeze/GammaOSNext`), no como un repositorio propio — las releases de un dispositivo concreto se etiquetan como "GammaOS Nano" cuando ese es el modo de UI por defecto para ese modelo.

**Documentación oficial escasa para "Nano" en concreto**: el README y la wiki del repositorio documentan en detalle GammaOS Next (instalación, hotkeys, changelog), pero no describen Nano como variante aparte — solo aparece nombrada en la tabla de dispositivos soportados de cada release. `[TODO]` los pasos de instalación/primer arranque específicos de Nano no están confirmados contra una guía oficial dedicada; se documentan aquí solo los hechos verificados directamente contra el repo.

## Dispositivos aplicables

Confirmado contra la tabla de dispositivos soportados y las releases de `github.com/TheGammaSqueeze/GammaOSNext`:

- TrimUI Brick (v1.4.1)
- MagicX Zero 40 (v1.4.1)
- MagicX Mini Zero 28 (v1.4.1)
- MagicX XURetro X20 V32 (v1.4.1)
- GKD 350H Ultra (v1.4.1)
- Anbernic RG Rotate (release `v1.4.0-ANBERNICRGROTATE`, confirmada en el listado de releases del repo — no aparece en la tabla de dispositivos del README actual pese a tener release propia, discrepancia no resuelta)

Nota: en el modelo RG Rotate, el modo Next completo (UI rica) está disponible desde la misma instalación mediante un switch — Nano es la UI por defecto, no la única opción (ver `docs/distributions.md`).

## Tipo de instalación

`[TODO]` no confirmado específicamente para Nano contra una guía oficial dedicada. GammaOS Next (mismo repo/mecanismo de distribución) usa imagen flasheada a SD — asumible por continuidad de repo, pero sin verificar que el proceso sea idéntico para Nano.

## Requisitos previos

`[TODO]` no confirmado específicamente para Nano — ver requisitos de GammaOS Next/Core (`gammaos-next.md`/`gammaos-core.md`) como referencia aproximada mientras no se verifique aparte.

## Descarga

- Repositorio oficial: <https://github.com/TheGammaSqueeze/GammaOSNext>
- Releases de Nano etiquetadas por dispositivo, ej. `v1.4.0-ANBERNICRGROTATE`, `v1.4.1` (TrimUI Brick, MagicX Zero 40/Mini Zero 28/XURetro X20 V32, GKD 350H Ultra) — descargar la release específica del modelo, no asumir que una release sirve para otro modelo aunque comparta versión.

## Preparación de almacenamiento

`[TODO]` no confirmado específicamente para Nano.

## Instalación

`[TODO]` no confirmado específicamente para Nano — no copiar sin verificar los pasos de `gammaos-next.md`/`gammaos-core.md`, aunque compartan repositorio.

## Primer arranque

`[TODO]` no confirmado específicamente para Nano.

## Configuración post-instalación

`[TODO]` no confirmado específicamente para Nano.

## Notas

- **Relación con GammaOS Next/Core**: Nano, Next y Core son tres líneas de producto de la misma familia (TheGammaSqueeze) con distinto público objetivo (Nano = formato reducido/UI ligera, Next = Android 14 GSI general, Core = LineageOS 20 orientado a RK3566 de gama baja) — no tratarlas como intercambiables ni asumir que un procedimiento de una aplica a otra sin confirmar.
- Antes de instalar, revisar si existe ya una guía comunitaria específica de Nano para el modelo concreto (ej. foros de la escena PowKiddy/MagicX/Anbernic) — este fichero documenta solo lo verificado contra el repositorio oficial a fecha de esta revisión (2026-09-06).
