# GammaOS Next

GammaOS Next es una distribución de Custom ROM altamente optimizada basada en Android 13 (LineageOS 20) y Android 14 (LineageOS 21), según el hardware del dispositivo, diseñada específicamente para consolas portátiles de emulación. Destaca en la escena por ofrecer un entorno completamente limpio de software basura (debloated), inyección nativa de shaders por hardware (GammaShader), un demonio de mapeo de controles de ultra-baja latencia (GammaPad), ecualización de audio a nivel de sistema (GammaEQ) y perfiles de rendimiento energético avanzados.

En algunos dispositivos (confirmado en Anbernic RGDS) incorpora el modo/interfaz **GammaOS Nano**: un frontend de arranque instantáneo con renderizado directo DRM, el sistema de suspensión profunda *Quick Resume* y un menú de superposición (overlay) global in-game accesible manteniendo pulsado el botón de Power — ver detalle en Configuración post-instalación y Notas.

## Dispositivos aplicables

Lista verificada contra el README oficial del proyecto (`https://github.com/TheGammaSqueeze/GammaOSNext`), con versión mínima soportada entre paréntesis:

- Anbernic: RG Vita Pro (v1.3.0), RG Vita (v1.3.1), RG477M / RG477V (v1.2.1), RG557 (v1.2.1), RG556 (v1.2), RG Cube (v1.2), RG406H / RG406V (v1.2), RG476H (v1.2), RG Slide (v1.2), RG405M / RG405V / RG505 (v1.1), RG Rotate (v1.4.0), RG DS (v1.4.0)
- TrimUI: Brick (v1.4.0)
- MagicX: Mini Zero 28 (v1.4.0), XURetro X20 V32 (v1.4.0)
- AYANEO: Pocket Air Mini (v1.3.1), Pocket Micro (v1.0); soporte planificado para Pocket-S/DMG y Pocket AIR
- Retroid Pocket: 4 PRO (v1.0), Classic (v1.0); soporte planificado para Mini v1/v2, Flip 2 y Pocket 5
- PowKiddy: X28 (planned)
- Otros: KT Pocket KT-R1 (v1.0), ZPG Unicorn A1 (v1.0), GameMT E6 MAX (v1.1.0), Mangmi Air X (v1.2)

Nota técnica: el ecosistema GammaOS Next está en constante expansión y la escena añade soporte dinámicamente — revisar siempre el listado de dispositivos compatibles en la página oficial del proyecto antes de descargar cualquier archivo.

## Tipo de instalación

Altamente dependiente del dispositivo: no existe un método universal. Según la arquitectura del procesador (Unisoc, Rockchip o MediaTek), la instalación se realiza mediante flasheo interno por cable con software de PC (SP Flash Tool, UpgradeDownload/UnisocTools), o mediante tarjetas MicroSD auto-flasheables (SD Card Install) que reescriben el almacenamiento interno de forma automatizada al encender la consola.

## Requisitos previos

- Revisión de la documentación del modelo: es estrictamente obligatorio consultar las instrucciones específicas del dispositivo en la wiki oficial del proyecto antes de realizar cualquier acción.
- PC con Windows: generalmente requerido para ejecutar las utilidades oficiales de flasheo de drivers y firmwares (SP Flash Tool, UnisocTools) o programas de descompresión multihilo como 7-Zip.
- Cable de datos USB-C premium: conectado directamente a la placa base del PC (evitar hubs) para evitar pérdidas de energía en mitad del volcado.
- Tarjeta MicroSD de marca reputada: destinada al almacenamiento de juegos o al método de instalación por tarjeta según exija la consola.

## Descarga

- Repositorio oficial: <https://github.com/TheGammaSqueeze/GammaOSNext>
- Sabores disponibles: la gran mayoría de dispositivos permite elegir entre la versión **Lite** (sin servicios de Google, recomendada para máxima RAM libre y batería) y la versión **Full** (con Google Play Store y sincronización).

## Preparación de almacenamiento

El sistema operativo auto-gestiona las particiones internas del almacenamiento al realizar el formateo de fábrica de la consola.

- Tarjeta MicroSD de juegos: debe formatearse externamente en el ordenador utilizando exFAT de forma nativa, para poder alojar archivos de más de 4GB (ISOs pesadas de PS2 o ROMs de Switch).
- Nota de Android: al introducir la MicroSD por primera vez en GammaOS Next, seleccionar siempre la casilla "Almacenamiento portátil". Esto evita que Android cifre la tarjeta y permite extraerla para conectarla a un entorno WSL/PC rápidamente.
- Estructura de carpetas: para un pipeline propio, volcar los juegos en rutas estándar en la raíz de la SD como `/ROMS/PS2/`, `/ROMS/PSP/`, `/ROMS/VITA/` o `/ROMS/SWITCH/`.

## Instalación

⚠️ Crítico: el método de instalación cambia radicalmente entre dispositivos — es obligatorio leer y seguir de forma estricta las instrucciones de la wiki de instalación oficial de GammaOS Next para el hardware específico.

- **Dispositivos con instalación por SD** (ej. RG Vita Pro): se extraen las partes del zip unificado con 7-Zip para obtener el archivo `.img`. Se graba en la MicroSD con Rufus/Etcher. Se introduce en la consola apagada y, al encenderla, se inicia un script automático que formatea el almacenamiento interno e inyecta la ROM de forma desatendida. Al finalizar, se retira la tarjeta.
- **Dispositivos con instalación por cable PAC** (ej. RG Vita): se instala el instalador de controladores Unisoc en Windows. Se carga el archivo `.pac` unificado en la herramienta `UpgradeDownload.exe`. Con la consola apagada, se mantiene presionada la combinación física de botones (Back + botón Anbernic) y se conecta el cable USB al PC. La herramienta inyecta el firmware.
- **Dispositivos MediaTek por cable** (ej. AYANEO Pocket Air Mini): se instalan los drivers Auto-Installer y se abre SP Flash Tool. Se carga el mapa de dispersión `_scatter.txt` de la ROM, se cambia al modo `Format All + Download` y se conecta la consola apagada para iniciar el volcado.

## Primer arranque

1. Al finalizar el flasheo según el método específico de hardware, desconecta los cables y realiza el primer encendido en frío.
2. El primer arranque se demora entre 1 y 3 minutos debido a que Android debe inicializar los nuevos entornos de ejecución y optimizar los sistemas de archivos. La pantalla puede parecer congelada temporalmente en el logotipo de la marca; esto es normal.
3. Completa los pasos del asistente de configuración de GammaOS (Setup Wizard).

## Configuración post-instalación

- **Sincronización del frontend**: abre la interfaz del launcher pre-configurado de fábrica (Daijishō) o una alternativa preferida como Beacon o ES-DE. Ve al menú de plataformas, selecciona el sistema a mapear y añade la ruta física del directorio de juegos apuntando directamente a la tarjeta MicroSD externa (ej. `/storage/XXXX-XXXX/ROMS/PS2/`).
- **Tratamiento de metadatos en Android**: a diferencia de los entornos cerrados de Linux, los frontends avanzados de Android no leen archivos planos locales `gamelist.xml`. Daijishō realiza su propio raspado digital (scraping) interno en línea e indexa los títulos en una base de datos SQLite interna protegida del sistema operativo de la consola. No requiere inyectar imágenes sueltas en la MicroSD.
- **Interfaz GammaOS Nano** (confirmado en RGDS): en dispositivos que la incorporan, el sistema incorpora tres entornos visuales completos intercambiables presionando `L1` en el menú principal:
  - *DSi System Menu*: recreación del carrusel de baldosas de Nintendo de doble pantalla con menús táctiles inferiores funcionales.
  - *PS3 XMB*: recreación de la XrossMediaBar de PlayStation con ondas animadas de fondo y refracción lumínica en los iconos transparentes.
  - *Minima*: interfaz minimalista de alto rendimiento basada en texto, inspirada en filosofías como MinUI.
  - Permite fondos de pantalla personalizados e incluso fondos en vídeo en bucle (video wallpapers), difuminados automáticamente para no penalizar la lectura del texto de los menús.

## Notas

- **Modificaciones de rendimiento y overclocks**: según la compilación del dispositivo, GammaOS Next puede incluir modificaciones a nivel de kernel. Por ejemplo, en la AYANEO Pocket Air Mini aplica un overclock de fábrica a la GPU Mali-G76 MC4 de 850 MHz a 950 MHz (+11.8%), beneficiando a emuladores dependientes de GPU como Dolphin o PPSSPP a altas resoluciones. Los emuladores dependientes estrictamente de hilos de CPU (como AetherSX2 para PS2) no ven un incremento masivo por este cambio aislado.
- **Optimización del formato de consolas en disco**: al contar con emuladores modernos e independientes de 64 bits de rendimiento extremo (como DuckStation o Flycast), el formato de compresión CHD (v5) es el estándar para cualquier sistema basado en discos compactos. Reduce el peso de las ISOs a la mitad, alivia el bus de lectura de la MicroSD y estabiliza la tasa de fotogramas por segundo. Para PSP, usar el formato CSO.
- **Gestión de almacenamiento relajada**: GammaOS Next cuenta con una modificación de políticas de seguridad del sistema operativo denominada Relaxed Scoped Storage, que afloja las restricciones de acceso a carpetas de Android moderno, permitiendo que emuladores independientes y frontends accedan a las carpetas de ROMs y archivos de guardado en la MicroSD sin bloqueos constantes de permisos.
- **Gestión de memoria RAM (filtro 1G1R)**: aunque estos dispositivos cuentan con más recursos que las gamas de entrada (generalmente entre 3GB y 4GB de RAM), frontends avanzados como Daijishō devoran una cantidad masiva de RAM al indexar y mantener en caché colecciones con miles de variantes por sistema. Es altamente recomendable aplicar un filtro 1G1R estricto antes de transferir los juegos, dejando subsets limpios de títulos esenciales por plataforma.
- **Interfaz GammaOS Nano (RGDS)** — motor de emulación DraStic-nano: el reproductor nativo de Nintendo DS ha sido reescrito a bajo nivel en Android para lograr un control de fotogramas (frame pacing) perfecto en configuraciones de doble pantalla. Incorpora soporte para RetroAchievements (modo Softcore). La característica estrella es Quick Resume, que guarda de forma transparente el estado del juego al apagar la consola y lo restaura de golpe en frío al encenderla, ocultando la carga tras una previsualización limpia del título.
- **Interfaz GammaOS Nano (RGDS)** — Control Center: al ejecutar emuladores o aplicaciones tradicionales de una sola pantalla en el panel superior, la pantalla táctil inferior muta automáticamente en un centro de control en tiempo real con lecturas de rendimiento (frecuencias de CPU/GPU, temperatura, uso de RAM), diales deslizantes de brillo/volumen independientes y un menú para lanzar aplicaciones directas en la segunda pantalla con transiciones fluidas.
