# GammaOS Core

GammaOS Core es una Custom ROM de código abierto basada en LineageOS 20 (Android 13 TV), diseñada específicamente como una versión mínima de alto rendimiento y bajo consumo para consolas portátiles retro de gama baja, orientada sobre todo (aunque no en exclusiva) a procesadores Rockchip RK3566. Al estar adaptada sobre la base "TV" de Android, sus menús principales no requieren capacidades táctiles nativas. Destaca en la escena por eliminar por completo los servicios pesados de Google de fondo, liberar memoria RAM crítica, corregir los controladores analógicos para ofrecer una respuesta lineal sin zonas muertas y aplicar parches a nivel de kernel que optimizan la GPU (Mali) bajo la API Vulkan. Incluye el frontend Daijishō pre-configurado y permite exprimir al máximo sistemas complejos como Nintendo 64, Dreamcast, PSP y emulación de consolas de sobremesa de sexta generación.

## Dispositivos aplicables

Lista verificada contra el README oficial del proyecto (`https://github.com/TheGammaSqueeze/GammaOSCore#supported-devices`):

- Anbernic RG ARC-D / RG ARC-S
- Anbernic RG353V / RG353VS
- Anbernic RG353P / RG353PS
- Anbernic RG353M
- Anbernic RG503
- PowKiddy RGB30
- PowKiddy RGB20SX
- PowKiddy RGB10MAX3
- PowKiddy RGB20 PRO
- PowKiddy X55 / X35H / X35S
- GameMT E5 Plus / E6 Plus
- GKD Bubble
- MagicX Zero28
- CB408
- TrimUI Smart Pro
- Miyoo Flip

Nota: el README oficial indica que el proyecto está "orientado a" dispositivos de gama baja con chipsets como el Rockchip RK3566, pero no lo declara exclusivo — de hecho incluye TrimUI Smart Pro (Allwinner A133P), por lo que no debe asumirse RK3566 como requisito estricto.

## Tipo de instalación

Imagen flasheada a SD, mediante PhoenixCard u otra herramienta de flasheo de tarjetas equivalente. **No es destructiva**: el sistema se ejecuta al 100% desde la MicroSD externa (ranura TF1) sin sobrescribir la memoria eMMC interna ni el sistema de fábrica (Stock OS). Si se retira la tarjeta, la consola vuelve a arrancar en su sistema original.

## Requisitos previos

- Tarjeta MicroSD para el sistema (SD1): 16GB o 32GB de buena calidad.
- Tarjeta MicroSD opcional para ROMs (SD2): 64GB a 512GB de alta velocidad.
- Software de flasheo: PhoenixCard u otra herramienta de flasheo de tarjetas recomendada en el repositorio oficial de GammaOS.
- Lector de tarjetas MicroSD.

## Descarga

- Repositorio oficial: <https://github.com/TheGammaSqueeze/GammaOSCore>
- Archivos requeridos: descargar el paquete comprimido específico para el modelo de hardware, que incluye la imagen para SD (`.img`).

## Preparación de almacenamiento

- **SD1 (Sistema)**: se prepara con PhoenixCard (o la herramienta equivalente), que escribe la imagen completa; no requiere formateo manual previo por el usuario.
- **SD2 (ROMs, opcional)**: debe formatearse obligatoriamente en exFAT de forma nativa para mantener compatibilidad plug-and-play con entornos Windows/WSL y admitir archivos pesados (superiores a 4GB).
- Al no tocar la eMMC, el Stock OS original permanece intacto y sigue siendo accesible retirando la SD1.
- Estructura de carpetas: Android y el frontend Daijishō leen cualquier ruta física. Para un pipeline propio, inyectar una estructura limpia y estándar como `/ROMS/NES/`, `/ROMS/SNES/`, `/ROMS/Arcade/` o `/ROMS/PSX/` es la solución de organización idónea.

## Instalación

1. Descarga PhoenixCard (o la herramienta recomendada en el repositorio de GammaOS) e inserta la SD1 en el lector del PC.
2. Abre la herramienta, carga la imagen de GammaOS Core y selecciona la SD1 como destino.
3. Ejecuta el volcado. Al finalizar, expulsa la tarjeta de forma segura.

## Primer arranque

1. Inserta la SD1 en la ranura TF1 de la consola.
2. Enciende la consola. [TODO: verificar si el modelo requiere una combinación de botones específica para forzar el arranque prioritario desde SD la primera vez, o si lo detecta automáticamente].
3. El sistema arranca LineageOS 20 (Android 13 TV) y carga el asistente de configuración inicial. Al finalizar, GammaOS Core establece automáticamente Daijishō como el lanzador de escritorio por defecto.

## Configuración post-instalación

- **Sincronización del frontend**: abre la interfaz de Daijishō. Ve a la pestaña de Platforms, selecciona el sistema a configurar y haz clic en `Paths -> Add More`. Apunta a la subcarpeta correspondiente dentro de la tarjeta MicroSD portátil (ej. `/storage/XXXX-XXXX/ROMS/SNES/`).
- **Tratamiento de metadatos en Android**: a diferencia de los CFW de Linux, los frontends avanzados de Android no leen archivos centralizados planos `gamelist.xml` locales. Daijishō realiza un raspado digital (scraping) interno en línea e indexa los títulos en una base de datos SQLite interna protegida. No es necesario inyectar carátulas sueltas en carpetas secundarias de la SD; el propio frontend descarga y organiza las portadas en la memoria interna de la consola.

## Notas

- **Tratamiento de ROMsets Arcade modernos**: gracias a la arquitectura de 64 bits de GammaOS Core y el rendimiento liberado en el kernel, la consola puede ejecutar núcleos modernos de RetroArch. El estándar recomendado por la comunidad para sistemas de placas recreativas (Capcom CPS y Neo-Geo) es FinalBurn Neo (romset en formato Non-Merged). Para juegos de arcade generales, implementa el núcleo estable y equilibrado MAME 2003-Plus (romset `0.78-plus`). Es necesario incluir el archivo de BIOS `neogeo.zip` correspondiente a esa era en la raíz de la carpeta arcade para garantizar la compatibilidad.
- **Optimización total para consolas en disco**: al contar con emuladores independientes modernos y núcleos actualizados de 64 bits de RetroArch (como DuckStation o Flycast), GammaOS Core ofrece soporte nativo perfecto para el formato comprimido CHD (v5) en sistemas basados en discos ópticos (PS1, Sega CD, Saturn y Dreamcast). Se recomienda automatizar la conversión masiva a CHD para reducir el peso de las ISOs a la mitad, estabilizar los fotogramas y eliminar los tirones de audio. Para PSP y PlayStation 2 (en sistemas compatibles), usar el formato CSO o CHD optimizado para AetherSX2.
- **Gestión de RAM y filtro 1G1R obligatorio**: los dispositivos aplicables a la gama Core suelen contar con limitaciones físicas de memoria RAM (habitualmente entre 1GB y 2GB). Los frontends con interfaces ricas como Daijishō devoran una cantidad masiva de RAM al indexar y mantener en memoria listas de juegos kilométricas. Si se intenta cargar un full-set completo con miles de variantes por sistema, el frontend sufre cierres inesperados por falta de memoria (Out of Memory Crashes) o ralentiza la navegación por las pestañas de forma crítica. Es técnicamente obligatorio aplicar un filtro 1G1R estricto (con herramientas como retool) para limitar los subsets a no más de 300 títulos selectos e idiomas preferidos por plataforma, garantizando que el sistema mantenga una tasa de refresco fluida y estable.
