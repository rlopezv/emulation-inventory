# Arcade

[TODO: las asociaciones concretas core/romset-versión de las tablas de abajo (~40 filas entre "Cores RetroArch", "Standalone", "Catálogo de Romsets Tradicionales" y "Catálogo de Sistemas Basados en Medios Ópticos y Vídeo") no se han verificado exhaustivamente contra documentación oficial — solo se ha confirmado el procedimiento del Anexo (generación de DAT vía menú de MAME/FBNeo) y corregido lo que resultó incorrecto ahí. Tratar los números de versión concretos con cautela hasta auditarlos.]

## Cores RetroArch (Libretro)

| Core RetroArch       | Romset / versión asociada      | Uso recomendado                                                                                                          | Hardware óptimo                                               |
| :------------------- | :----------------------------- | :----------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------ |
| `fbneo`              | FBNeo actual / matching DAT    | El mejor núcleo actual para arcade 2D, lucha y Neo-Geo. Soporta juego online (Fightcade).                                | PC moderno, Android gama media/alta, SBCs actuales            |
| `fbalpha`                   | FinalBurn Alpha `0.2.97.44`    | Muy ligero en RAM.                                                        | Consolas portátiles de recursos bajos                         |
| `fbalpha2016` | FinalBurn Alpha `0.2.97.39` | Equilibrio perfecto entre catálogo amplio (CPS3, Neo-Geo) y bajo consumo de recursos. Descatalogado del menú oficial, requiere instalación manual. | Raspberry Pi 1/2/Zero, Android antiguo, TV Boxes low-cost |
| `fbalpha2012`        | FinalBurn Alpha `0.2.97.29`    | Alternativa arcade rápida para sistemas que no toleran el motor FBNeo moderno.                                           | Raspberry Pi 2/3, Consolas portátiles baratas                 |
| `fbalpha2012_cps1`   | FinalBurn Alpha `0.2.97.29`    | Ejecución optimizada y exclusiva de la placa Capcom Play System 1.                                                       | Consolas portátiles de recursos bajos                         |
| `fbalpha2012_cps2`   | FinalBurn Alpha `0.2.97.29`    | Ejecución optimizada y exclusiva de la placa Capcom Play System 2.                                                       | Consolas portátiles de recursos bajos                         |
| `fbalpha2012_cps3`   | FinalBurn Alpha `0.2.97.29`    | Ejecución optimizada y exclusiva de la placa Capcom Play System 3 (como *Street Fighter III*).                           | Consolas portátiles de recursos bajos                         |
| `fbalpha2012_neogeo` | FinalBurn Alpha `0.2.97.29`    | Núcleo exclusivo para juegos de Neo-Geo (SNK). Muy ligero en RAM.                                                        | Consolas portátiles de recursos bajos                         |
| `mame2000`           | MAME `0.37b5`                  | Adaptación del código de MAME4All. El núcleo arcade más rápido y que menos batería gasta.                                | Consolas portátiles muy limitadas, móviles de gama de entrada |
| `mame2003`           | MAME `0.78`                    | Legacy puro. Mantenido por compatibilidad histórica estricta con el set 0.78 clásico.                                    | Sistemas Linux integrados antiguos                            |
| `mame2003-plus`      | MAME `0.78` + backports        | Versión mejorada con parches de audio corregidos y soporte extendido de mandos y hacks.                                  | El estándar para Raspberry Pi 3, Miyoo Mini, Powkiddy         |
| `mame2003-xtreme`    | MAME `0.78`                    | Modificación agresiva con trucos de velocidad (*speedhacks*) y overclock inverso para exprimir CPUs modestas.            | PlayStation Classic Mini, NES/SNES Classic Mini               |
| `mame2010`           | MAME `0.139u1`                 | MAME equilibrado para revivir juegos de finales de los 90. Código pesado pero compatible.                                | PC antiguo, Android gama media, Raspberry Pi 3/4              |
| `mame2015`           | MAME `0.160`                   | Ideal para el "punto dulce" de juegos arcade poligonales en 3D primitivo de finales de los 90.                           | Consolas chinas tipo RK3566 o Raspberry Pi 4                  |
| `flycast`            | Sega NAOMI / Atomiswave DAT    | Obligatorio para las recreativas en 3D de SEGA y juegos de lucha en 2D de alta resolución (*MvC2*).                      | Consolas portátiles potentes (Anbernic RG405M, Retroid, Odin) |
| `swanstation`        | Arquitectura Sony Zn-1 / Zn-2  | Emulación a 60FPS de arcades basados en hardware PS1 (*Tekken*, *Rival Schools*) usando su núcleo dedicado.              | Consolas portátiles de gama media y smartphones               |
| `mame`               | MAME actual / matching version | Preservación total, emulación 3D avanzada y microordenadores. Cambia de romset con cada actualización mensual de la app. | PC gaming (x86), Mac, dispositivos de gama entusiasta         |
| `daphne` | Daphne Framefiles / LaserDisc | Adaptación del emulador clásico para jugar a *Dragon's Lair* y similares integrando los menús, filtros de pantalla y configuraciones unificadas de RetroArch. | Consolas portátiles de gama media (RG3566/RK3326), Android, PC |
| `hypseus_singe` | Daphne / Singe 1 & 2 Video Data | Una bifurcación (fork) moderna de Daphne que añade soporte para juegos LaserDisc de segunda generación y títulos basados en el motor *Singe* (*Mad Dog McCree*, *Crime Patrol*). | PC, Raspberry Pi 4/5, Consolas portátiles de gama alta |

## Standalone

| Emulador Standalone             | Romset / versión asociada      | Uso recomendado                                                                                            | Hardware                                        |
| :------------------------------ | :----------------------------- | :--------------------------------------------------------------------------------------------------------- | :---------------------------------------------- |
| `AdvanceMame`                   | MAME `0.106`                   | Monitores CRT antiguos y recreativas comerciales a frecuencias nativas (15kHz).                            | PC (Windows/Linux), Raspberry Pi                |
| `MAME4All`                      | MAME `0.37b5`                  | Velocidad extrema en hardware antiguo. El core equivalente en RetroArch es `mame2000`.                     | Consolas portátiles clásicas, GP2X, Dingoo A320 |
| `MAME4droid 0.37b5`             | MAME `0.37b5`                  | Móviles Android extremadamente viejos o de gama de entrada. Consume poquísima batería.                     | Android (Gama baja / Antiguos)                  |
| `MAME4droid 0.139u1`            | MAME `0.139u1`                 | Estándar equilibrado para móviles de gama media. Gran compatibilidad de juegos de los 90.                  | Android (Gama media)                            |
| `MAME4droid 0.287`              | MAME `0.287`                   | Versión moderna de 64 bits para ejecutar casi todo el catálogo arcade (incluye ordenadores clásicos).      | Android (Gama alta / TV Boxes modernos)         |
| `XMAME v0.52`                   | MAME `0.37b16`                    | Juegos arcade clásicos de los 80 y placas muy sencillas a máxima velocidad.                                | OpenDingux (RG350, PocketGo, etc.)              |
| `XMAME v0.69`                   | MAME `0.69`                    | Equilibrio intermedio en OpenDingux para juegos que no cargan en la 0.52.                                  | OpenDingux (RG350, PocketGo, etc.)              |
| `XMAME v0.84`                   | MAME `0.84`                    | El motor más avanzado de XMAME. Soporta juegos de principios de los 2000, pero exige más CPU.              | OpenDingux (RG350, PocketGo, etc.)              |
| `FinalBurnAlpha_2020-01-22-.35` | FinalBurn Alpha `0.2.97.35`    | Juegos de lucha 2D (Capcom, Neo-Geo) optimizados para firmwares OpenDingux antiguos.                       | OpenDingux antiguos (Dingoo, GCW Zero)          |
| `FinalBurnAlpha_2020-01-22-.44` | FinalBurn Alpha `0.2.97.44`    | El estándar recomendado para CPS y Neo-Geo con soporte de nombres reales en pantalla (`_alias`).           | OpenDingux modernos (RG350/M, RG280V)           |
| `GnGeo_2020-02-16`              | MAME `0.128` / FBA `0.2.97.39` | Rendimiento impecable en Neo-Geo. Requiere BIOS específica y sufre con juegos de más de 40MB.              | OpenDingux (RG350, PocketGo)                    |
| `FBA320`                        | FinalBurn Alpha `0.2.96.86`    | Precursor histórico. Diseñado para mover CPS1, CPS2 y Neo-Geo en pantallas de 320x240 sin esfuerzo.        | Dingoo A320, Consolas chinas clones de 2010     |
| `Miyoo Arcade`                  | Modificado de FBA / MAME       | Ejecución directa y fluida de arcades en sistemas económicos de pantalla pequeña sin configurar RetroArch. | Miyoo Mini, Powkiddy V90 (NxHope)               |
| `Daphne` (Standalone) | Daphne Framefiles / LaserDisc M2V | El emulador original definitivo para recreativas de LaserDisc. Exige un archivo de lógica de juego y archivos de vídeo de alta definición (*m2v/ogg*). | PC (Windows/Linux), Raspberry Pi, Odroid |

## Catálogo de Romsets Tradicionales (ROMs Puras)


| Familia  | Romset base                    | Core RetroArch       | Standalone                    | Estado      | Disponible | Notas / Particularidades                                                                   |
| :------- | :----------------------------- | :------------------- | :---------------------------- | :---------- | :--------: | :----------------------------------------------------------------------------------------- |
| FBNeo    | FBNeo actual / matching DAT    | `fbneo`              | FinalBurn Neo                 | Actual      |    [ ]     | Estándar moderno. Soporta juego online (Fightcade) y retro-logros. Core Vivo.              |
| FBA      | FinalBurn Alpha 0.2.97.44      | `fbalpha`            | —                             | Legacy      |    [x]     | Última versión oficial de la rama FBA antes de la transición a FBNeo.                      |
| FBA      | FinalBurn Alpha 0.2.97.39      | `fbalpha2016`        | —                             | Legacy      |    [x]     | Descatalogado en RetroArch (requiere instalación manual). Equilibrio óptimo en SBCs.       |
| FBA      | FinalBurn Alpha 0.2.97.29      | `fbalpha2012`        | —                             | Legacy      |    [x]     | Muy ligero. Diseñado para hardware antiguo o consolas portátiles de recursos bajos.        |
| FBA      | FinalBurn Alpha 0.2.97.29      | `fbalpha2012_cps1`   | —                             | Legacy      |    [ ]     | Sub-núcleo optimizado para Capcom CPS1. Usar DAT extraído para evitar sobrecarga.          |
| FBA      | FinalBurn Alpha 0.2.97.29      | `fbalpha2012_cps2`   | —                             | Legacy      |    [ ]     | Sub-núcleo optimizado para Capcom CPS2. Usar DAT extraído para evitar sobrecarga.          |
| FBA      | FinalBurn Alpha 0.2.97.29      | `fbalpha2012_cps3`   | —                             | Legacy      |    [ ]     | Sub-núcleo optimizado para Capcom CPS3. Evita problemas de desborde de RAM.                |
| FBA      | FinalBurn Alpha 0.2.97.29      | `fbalpha2012_neogeo` | —                             | Legacy      |    [ ]     | Sub-núcleo optimizado para SNK Neo-Geo. Requiere `neogeo.zip` externo en la raíz.          |
| MAME     | MAME 0.37b5                    | `mame2000`           | MAME4All                      | Histórico   |    [x]     | Rendimiento rápido a costa de precisión. El estándar para sistemas muy obsoletos.          |
| MAME     | MAME 0.78                      | `mame2003`           | —                             | Legacy      |    [x]     | Reemplazado en la práctica por la versión Plus debido a bugs estructurales.                |
| MAME     | MAME 0.78 + backports          | `mame2003-plus`      | —                             | Vigente     |    [x]     | Versión activa. Añade mejoras de sonido (exige *samples* específicos) y hacks. Core Vivo.  |
| MAME     | MAME 0.78                      | `mame2003-xtreme`    | —                             | Alternativo |    [x]     | Fork optimizado para velocidad. Soporta bandas sonoras en CD y roms de Plus.               |
| MAME     | MAME 0.139u1                   | `mame2010`           | MAME4droid 0.139u1            | Legacy      |    [x]     | Core abandonado con problemas de rendimiento. Conservado por retrocompatibilidad.          |
| MAME     | MAME 0.160                     | `mame2015`           | —                             | Legacy      |    [ ]     | Core intermedio obsoleto. Reemplazado por el núcleo `mame` actual.                         |
| MAME     | MAME actual / matching version | `mame`               | MAME Official                 | Actual      |    [ ]     | Emulador oficial actualizado mensualmente. Alta precisión, exige CPUs potentes. Core Vivo. |
| MAME     | MAME 0.106                     | —                    | AdvanceMame                   | Legacy      |    [ ]     | Diseñado originalmente para salida de vídeo nativa en monitores arcade CRT y TVs.          |
| MAME     | MAME 0.37b5                    | —                    | MAME4All                      | Histórico   |    [x]     | Versión independiente clásica para sistemas operativos basados en Linux/Dingux.            |
| MAME     | MAME 0.37b5                    | —                    | MAME4droid 0.37b5             | Histórico   |    [x]     | Versión clásica para teléfonos Android muy antiguos. Excelente rendimiento.                |
| MAME     | MAME 0.139u1 (Modernizado)     | —                    | MAME4droid (2024)             | Vigente     |    [x]     | Versión moderna e independiente para Android actuales. Basada en el romset 0.139u1.        |
| MAME     | MAME 0.37b16                   | —                    | XMAME v0.52                   | Histórico   |    [x]     | Excepción técnica: El binario se llama v0.52 pero exige estrictamente el romset 0.37b16.   |
| MAME     | MAME 0.69                      | —                    | XMAME v0.69                   | Histórico   |    [x]     | Versión intermedia para OpenDingux. Usar si el juego no es compatible con la v0.52.        |
| MAME     | MAME 0.84                      | —                    | XMAME v0.84                   | Histórico   |    [ ]     | El motor más avanzado y compatible de XMAME, pero el que consume más CPU.                  |
| FBA      | FinalBurn Alpha 0.2.97.35      | —                    | FinalBurnAlpha_2020-01-22-.35 | Legacy      |    [ ]     | Versión standalone específica para preservar la compatibilidad en ciertos firmwares.       |
| FBA      | FinalBurn Alpha 0.2.97.44      | —                    | FinalBurnAlpha_2020-01-22-.44 | Legacy      |    [ ]     | Versión standalone pura. Soporta visualización de nombres reales mediante `_alias`.        |
| GnGeo    | MAME 0.128 / FBA 0.2.97.39     | —                    | GnGeo                         | Legacy      |    [ ]     | Emulador exclusivo de Neo-Geo de línea de comandos. Híbrido muy rápido en CPUs MIPS.       |
| FBA      | FinalBurn Alpha 0.2.96.86      | —                    | FBA320                        | Histórico   |    [ ]     | El emulador arcade clásico de la consola Dingoo A320. Origen de la scene portátil.         |
| FBA/MAME | Modificado de FBA / MAME       | —                    | Miyoo Arcade                  | Legacy      |    [ ]     | Emulador optimizado de fábrica para el firmware cerrado de la Miyoo Mini original.         |

---

## Catálogo de Sistemas Basados en Medios Ópticos y Vídeo

| Familia     | Romset base                     | Core RetroArch   | Standalone         | Estado  | Disponible | Notas / Particularidades                                                                                                                                     |
| :---------- | :------------------------------ | :--------------- | :----------------- | :------ | :--------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Sega Arcade | Sega NAOMI / Atomiswave DAT     | `flycast`        | Flycast Standalone | Actual  |    [ ]     | Requiere archivos `.zip` + `.chd` (ó `.gdi`/`.lst`). Las BIOS (`naomi.zip`/`awbios.zip`) van estrictamente en la carpeta `system` de RetroArch.              |
| Sony ZN     | Hardware Arcade basado en PS1   | `fbneo` / `mame` | —                  | Actual  |    [ ]     | Placas tipo Zn-1/Zn-2. No usa ISOs de PS1; se gestiona con un romset arcade tradicional combinado con sus carpetas contenedoras `.chd`.                      |
| Daphne      | Daphne Framefiles / LaserDisc   | `daphne`         | Daphne             | Vigente |    [ ]     | Especializado en juegos LaserDisc (*Dragon's Lair*). No usa ROMs estándar; requiere archivos de vídeo `.m2v` y un archivo de texto de sincronización `.txt`. |
| Daphne      | Daphne / Singe 1 & 2 Video Data | `hypseus_singe`  | Hypseus Singe      | Actual  |    [ ]     | Fork moderno de Daphne. Añade soporte para juegos basados en el motor *Singe*. Optimiza espacio al sustituir los vídeos planos por formatos `.mp4` y `.ogg`. |

---

### Glosario de Estados y Comportamiento de los Romsets

* **Actual / Vigente / Alternativo (Cores Vivos):** El romset cambia constantemente en su desarrollo madre. En **consolas portátiles chinas**, el set se queda congelado en la fecha exacta en la que el desarrollador compiló el firmware (ej. OnionOS, ArkOS). *Acción: Se recomienda generar el .dat desde el menú interno de RetroArch de la propia consola para clavar las firmas CRC.*
* **Legacy / Histórico (Cores Congelados):** El código del emulador no se ha movido en años. Las firmas CRC de los archivos `.zip` son fijas y universales. *Acción: Puedes usar cualquier romset histórico de internet (ej. MAME 0.37b5 o FBA 0.2.97.29) y encajará a la primera bajo la estructura Non-Merged elegida.*

---

### Anexo: procedimiento para generar archivos .DAT personalizados

Cuando trabajes con núcleos catalogados como **"Vivos"** dentro del sistema operativo de una consola china, utiliza este protocolo para obtener el índice exacto de archivos y evitar pantallas negras:

#### Método RetroArch (confirmado para `mame2003-plus`; corregido)

**Corrección importante:** no existe la opción "Crear archivo DAT de ROMs" en Información del Núcleo tal como se describía antes — comprobado contra la documentación oficial de `mame2003-plus`. El procedimiento real es distinto y ocurre **dentro del propio menú de MAME del core**, no en el menú de RetroArch:

1. Enciende la consola portátil, ejecuta **RetroArch** y carga el core (`mame2003-plus` confirmado; otros cores MAME/FBNeo pueden variar, no verificado para cada uno).
2. Con un juego cargado, entra al **menú de MAME** — o bien activándolo como opción de core, o pulsando la tecla `Tab` si el modo de entrada tiene habilitado el interfaz `mame_keyboard`.
3. Dentro de ese menú, selecciona la opción de core **"Generate XML DAT"**.
4. Si se activó el menú de MAME solo para este paso, desactivarlo de nuevo como opción de core al terminar.

[TODO: no se ha confirmado la ruta exacta donde queda guardado el fichero DAT generado, ni si este procedimiento es idéntico para otros cores además de `mame2003-plus` (ej. `fbneo`, `mame2010`) — verificar caso por caso]

#### Método Standalone (para emuladores FBA / FBNeo de PC — confirmado)

1. Descarga en tu ordenador el ejecutable oficial para Windows de la subversión correspondiente del emulador (ej. *FinalBurn Alpha v0.2.97.44*, o FBNeo actual).
2. Abre la aplicación, despliega la pestaña superior **Misc** y elige entre dos opciones confirmadas contra la wiki oficial de FBNeo:
   * **"Generate dat file"** — genera un único DAT para una categoría concreta (arcade, o un sistema doméstico específico: Megadrive, PC-Engine/TurboGrafx-16, SuprGrafx, Sega SG-1000, ColecoVision, Sega Master System, Game Gear, MSX-1, ZX Spectrum).
   * **"Generate all dats"** — genera todos los DAT disponibles a la vez, en una carpeta de destino elegida.
3. Formato de salida confirmado: **ClrMamePro (XML)**.
