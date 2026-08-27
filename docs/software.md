# Frontends

> **Aviso:** los proyectos de CFW/OS listados aquí están en desarrollo activo; listas de dispositivos compatibles, enlaces y versiones pueden quedar desactualizados. Verificar siempre contra la fuente oficial (repo/página del proyecto) antes de instalar.

Este documento cubre software instalado *en un dispositivo* (CFW, OS Retro, Android CFW, Frontend, Launcher). Las herramientas de gestión de romsets/DATs en PC (scraping, validación, conversión, parcheo...) están en `docs/tools.md`.

## Convenciones

### Tipo

* CFW
* OS Retro
* Android CFW
* Frontend
* Launcher
* Histórico

### Estado

* Activo
* Mantenimiento
* Histórico
* Descontinuado
* Experimental

### Requiere gamelist

* Sí
* No
* Opcional

### Media soportada

* No
* Limitado
* Imágenes
* Vídeos
* Imágenes + vídeos

### Columnas

| Columna | Descripción |
| --- | --- |
| Nombre | Nombre del proyecto o distribución |
| Variante | Rama o edición específica dentro del mismo proyecto |
| Tipo | Categoría funcional del software |
| Familia | Proyecto base o linaje técnico del que deriva |
| SD base | Tamaño mínimo funcional de la tarjeta de sistema (TF1 o almacenamiento interno); solo para CFW, OS Retro y Android CFW |
| Frontend | Interfaz de usuario expuesta al usuario final |
| Requiere gamelist | Si necesita `gamelist.xml` para mostrar metadatos |
| Media soportada | Tipos de recursos visuales que puede mostrar |
| Página / repo | URL del proyecto o repositorio oficial |
| Plataforma principal | Arquitectura o entorno de ejecución principal |
| Dispositivos principales | Hardware objetivo o más habitual |
| Estado | Estado de desarrollo y mantenimiento actual |
| Notas | Observaciones relevantes sobre uso o posicionamiento |

---

## CFW / Distribuciones Handheld Linux

| Nombre | Variante | Tipo | Familia | SD base | Frontend | Requiere gamelist | Media soportada | Página / repo | Plataforma principal | Dispositivos principales | Estado | Notas |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Onion OS        | —        | CFW  | Onion           | 16 GB | Onion UI          | Opcional          | Imágenes          | https://onionui.github.io/                               | Linux Handheld       | Miyoo Mini / Mini+                                             | Activo        | Referencia principal para Miyoo Mini y Mini Plus                     |
| GarlicOS        | 1.x      | CFW  | GarlicOS        | 16 GB | Garlic UI         | Opcional          | Imágenes          | https://www.patreon.com/posts/garlicos-for-76561333      | Linux Handheld       | RG35XX original                                                | Mantenimiento | Rama clásica para RG35XX original                                    |
| GarlicOS        | 2.0      | CFW  | GarlicOS        | 16 GB | Garlic UI         | Opcional          | Imágenes          | https://www.patreon.com/posts/garlicos-2-0-92690050      | Linux Handheld       | RG35XX Plus/H/SP y otros soportes experimentales               | Experimental  | Rama multiplataforma                                                 |
| muOS            | —        | CFW  | muOS            | 8 GB | muOS UI           | Opcional          | Imágenes + vídeos | https://muos.dev/                                        | Linux Handheld       | Familia Anbernic RGXX / H700                                     | Activo        | Recomendable en familia H700 por rapidez y personalización           |
| KNULLI          | —        | CFW  | Batocera        | 32 GB | EmulationStation  | Opcional          | Imágenes + vídeos | https://github.com/knulli-cfw/distribution/releases      | Linux Handheld       | Anbernic XX, TrimUI y otros compatibles                        | Activo        | Fork/derivado tipo Batocera orientado a handhelds                    |
| ROCKNIX         | —        | CFW  | JELOS           | 16 GB | EmulationStation  | Opcional          | Imágenes + vídeos | https://github.com/ROCKNIX/distribution/releases         | Linux Handheld       | RK3326/RK3566/RK3568, RG353, RGARC, RGDS y compatibles       | Activo        | Principal sucesor práctico de JELOS                                  |
| ArkOS           | —        | CFW  | ArkOS           | 16 GB | EmulationStation  | Opcional          | Imágenes + vídeos | https://github.com/christianhaitian/arkos/releases       | Linux Handheld       | RK3326/RK3566                                                  | Activo        | Referencia histórica muy fuerte para RK3326                          |
| AmberELEC       | —        | CFW  | 351ELEC         | 16 GB | EmulationStation  | Opcional          | Imágenes + vídeos | https://github.com/AmberELEC/AmberELEC/releases          | Linux Handheld       | RG351 / RG552                                                  | Activo        | Evolución directa de 351ELEC                                         |
| Adam Image      | —        | CFW  | OpenDingux      | 8 GB | SimpleMenu        | Sí                | Imágenes          | https://github.com/eduardofilo/RG350_adam_image/releases | OpenDingux           | RG350, RG280, RG300X, PocketGo2                                | Activo        | Referencia moderna para JZ4770/OpenDingux                            |
| Rogue CFW       | —        | CFW  | OpenDingux      | 4 GB | GMenu2X           | No                | Limitado          | https://github.com/Ninoh-FOX/RG350-ROGUE-CFW/releases    | OpenDingux           | RG350 / compatibles                                            | Mantenimiento | Alternativa clásica a Adam Image                                     |
| RetroFW         | —        | CFW  | RetroFW         | 4 GB | GMenu2X           | No                | Limitado          | https://github.com/retrofw/retrofw.github.io             | OpenDingux Legacy    | RS97, LDK, RG300 antiguos                                      | Mantenimiento | Base habitual para JZ4760/JZ4760B antiguos                           |
| OpenDingux      | —        | CFW  | OpenDingux      | 4 GB | GMenu2x           | No                | Limitado          | https://github.com/OpenDingux/opendingux                 | OpenDingux           | RG350, RG280M, RG280V, RG300X, PocketGo2 y compatibles JZ4770 | Mantenimiento | Plataforma base Linux para JZ4760B/JZ4770; base de Adam Image y Rogue CFW |
| MiyooCFW        | —        | CFW  | MiyooCFW        | 8 GB | SimpleMenu        | Sí                | Imágenes          | https://github.com/TriForceX/MiyooCFW/releases           | F1C100S              | BittBoy, PocketGo, PowKiddy V90/Q90/Q20 Mini                   | Histórico     | Base histórica para handhelds F1C100S/F1C500S                        |
| BOB (Best of the Best) | Bittboy/PowKiddy | CFW | BOB            | 8 GB | SimpleMenu        | Sí                | Imágenes          | [TODO]                                                   | F1C100S              | BittBoy v2/v2.5/v3.5, PocketGo, PowKiddy Q90/V90               | Histórico     | Imagen curada lista para usar; colección seleccionada, filosofía plug-and-play |
| BOB (Best of the Best) | ArkOS            | CFW | BOB            | 128 GB | EmulationStation  | Opcional          | Imágenes + vídeos | [TODO]                                                   | Linux Handheld       | RG351P/M, RG351V, RG351MP, RGB10 Max                           | Histórico     | Imágenes curadas sobre ArkOS por dispositivo; canales Telegram por modelo |
| Koriki          | —        | CFW  | Batocera        | 16 GB | SimpleMenu        | Opcional          | Imágenes + vídeos | https://github.com/Rparadise-Team/Koriki/releases        | Linux Handheld       | Miyoo Mini, Miyoo Mini+, RG35XX original y compatibles         | Activo        | Adaptación ligera tipo Batocera; mantener como alternativa relevante |
| Koriki          | ED       | CFW  | Batocera        | 16 GB | SimpleMenu        | Opcional          | Imágenes + vídeos | https://github.com/Rparadise-Team/Koriki/releases        | Linux Handheld       | RG35XX Plus, RG35XXH, RG28XX, RG34XX y otros H700          | Activo        | Variante de Koriki adaptada a la familia H700                        |
| Koriki          | BOM      | CFW  | Batocera        | 16 GB | SimpleMenu        | Opcional          | Imágenes + vídeos | https://github.com/Rparadise-Team/Koriki/releases        | Linux Handheld       | Miyoo Mini, Miyoo Mini+, Miyoo Mini Flip, Miyoo Flip, RG35XX original | Activo | Combinación de Koriki con la colección/compilación de juegos BOM (Brothers of Metal) |
| MinUI           | —        | CFW  | MinUI           | 4 GB | MinUI             | No                | No                | https://github.com/shauninman/MinUI/releases             | Linux Handheld       | Miyoo, TrimUI, RG35XX, MagicX Mini Zero 28 y varios handhelds  | Activo        | Enfoque minimalista; no centrado en scraping ni metadatos visuales. En MagicX Mini Zero 28 requiere [Moss-zero28](https://github.com/shauninman/Moss-zero28) (base Tina Linux) en la TF1/INT y MinUI en la TF2/EXT; soporte comunitario (Shaun Inman) desde enero 2025, no oficial de MagicX |
| CrossMix-OS     | —        | CFW  | CrossMix        | 16 GB | EmulationStation  | Opcional          | Imágenes + vídeos | https://github.com/cizia64/CrossMix-OS                   | Linux Handheld       | TrimUI Smart Pro                                               | Activo        | Referencia principal para TrimUI Smart Pro                           |
| spruceOS        | —        | CFW  | spruceOS        | 16 GB | spruceOS UI       | Opcional          | Imágenes          | https://github.com/spruceUI/spruceOS/releases            | Linux Handheld       | Miyoo A30, Miyoo Flip, Miyoo Mini Flip, TrimUI Brick/Smart Pro | Activo        | Proyecto en evolución rápida                                         |
| Tomato OS       | —        | CFW  | Tomato          | 4 GB | SimpleMenu        | Sí                | Imágenes          | https://github.com/jutleys/Trimui-Smart-Tomato           | Linux Handheld       | TrimUI Smart                                                   | Activo        | Firmware ligero específico para TrimUI Smart                         |
| twigUI          | —        | CFW  | twigUI          | [TODO] | twigUI            | Opcional          | Imágenes          | https://github.com/spruceUI/twigUI                        | Linux Handheld       | GKD Pixel 2 (RK3326 compatibles)                                | Activo        | Port directo de spruceOS a la GKD Pixel 2; reemplaza EmulationStation por una interfaz de texto ligera; pantalla apagable durante la carga, atajos por botón físico Menú y apagado automático por inactividad |
| RetroOZ         | —        | CFW  | RetroOZ         | 16 GB | EmulationStation  | Opcional          | Imágenes + vídeos | https://github.com/southoz/RetroOZ                       | Linux Handheld       | RGB10 Max / RGB10 Max 2                                        | Mantenimiento | Alternativa histórica para RGB10 Max                                 |
| The Retro Arena | —        | CFW  | The Retro Arena | 16 GB | EmulationStation  | Opcional          | Imágenes + vídeos | https://github.com/Retro-Arena                           | Linux Handheld       | OGA, RGB10, RS-07, RS-12, RK3326                               | Activo        | Distribución veterana con soporte amplio                             |
| FunKey OS       | —        | CFW  | FunKey          | 4 GB | FunKey UI         | No                | Limitado          | https://github.com/FunKey-Project/FunKey-OS              | Linux Handheld       | FunKey S, RGNano derivados                                    | Activo        | Base para dispositivos ultracompactos                                |
| DrUm78 RGNano  | —        | CFW  | FunKey          | 4 GB | RetroFE           | No                | Imágenes          | https://rgnano.com/custom-firmware/                      | Linux Handheld       | RGNano                                                        | Activo        | CFW específico para RGNano; RetroFE es el lanzador de juegos por defecto, GMenu2X está disponible como interfaz secundaria para utilidades del sistema y reproductor de MP3/vídeo |
| Surwish OS      | —        | CFW  | Surwish         | 16 GB | Surwish UI        | Opcional          | Imágenes          | https://github.com/Surwish/Surwish-Miyoo-Flip            | Linux Handheld       | Miyoo Flip                                                     | Experimental  | Proyecto específico para Miyoo Flip                                  |
| Simple30        | —        | CFW  | Simple30        | 8 GB | SimpleMenu        | Sí                | Imágenes          | https://github.com/retrogamecorps/Simple30               | Linux Handheld       | PocketGo S30                                                   | Activo        | Optimización específica para PocketGo S30                            |
| SimplerS30      | —        | CFW  | SimplerS30      | 4 GB | RetroArch directo | No                | No                | https://github.com/ducalex/SimplerS30                    | Linux Handheld       | PocketGo S30                                                   | Activo        | Alternativa minimalista para PocketGo S30                            |
| MustardOS | — | CFW | MustardOS | 16 GB | Mustard Launcher | Opcional | Imágenes + vídeos | https://mustardos.org/ | Linux Handheld | Familia Anbernic RGXX / H700 | Activo | Distribución con identidad propia; enfocada a simplicidad y experiencia lista para usar; alternativa directa a muOS |
| Allium OS | — | CFW | Allium | 8 GB | Allium UI | Opcional | Imágenes | https://github.com/goweiwen/Allium | Linux Handheld | Miyoo Mini / Mini Plus | Mantenimiento | Alternativa comunitaria para Miyoo Mini |
| plumOS | XU Mini M | CFW | plumOS | 16 GB | EmulationStation | Opcional | Imágenes + vídeos | https://github.com/game-de-it/plumOS | Linux Handheld | MagicX XU Mini M | Activo | Variante plumOS para MagicX XU Mini M |
| dArkOS | — | CFW | dArkOS | 16 GB | EmulationStation | Opcional | Imágenes + vídeos | https://github.com/christianhaitian/dArkOS | Linux Handheld | OGA, RGB10, RGB20, RG351MP, RG353M, RG353V, RG353VS, RG503 | Activo | Sucesor de ArkOS; soporta RK3326 y RK3566 |
| ArkOS4Clone | — | [TODO] | ArkOS | [TODO] | [TODO] (hereda de dArkOS) | [TODO] | [TODO] | https://github.com/lcdyk0517/arkos4clone | Linux Handheld | [TODO] (clones RK3326 no soportados oficialmente, sin lista de modelos confirmada) | Activo | Porting del kernel (d)ArkOS 4.4 a clones RK3326 no soportados vía DTB/U-Boot; incluye herramienta de identificación de clon y de personalización de DTB (mando, batería, refresco). Repo satélite `ArkOS4Clone_Ports_Fixed` para fixes de ports. MIT. No es un CFW independiente — se aplica sobre dArkOS |
| EmuELEC | — | CFW | EmuELEC | [TODO] | EmulationStation | Opcional | Imágenes + vídeos | https://github.com/EmuELEC/EmuELEC | Linux TV Box | TV Box Amlogic S905/S912 (Super Console X / Game Stick) | Activo | CFW basado en LibreELEC/Batocera para TV Boxes Amlogic |

## Sistemas Operativos Retro (SBC / PC)

| Nombre | Variante | Tipo | Familia | SD base | Frontend | Requiere gamelist | Media soportada | Página / repo | Plataforma principal | Dispositivos principales | Estado | Notas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Batocera | Oficial | OS Retro | Batocera | 32 GB | EmulationStation | Opcional | Imágenes + vídeos | https://batocera.org/ | SBC / PC | Raspberry Pi, PC x86, mini PC, Odroid, Orange Pi y SBC compatibles | Activo | Referencia principal para sistemas dedicados de emulación |
| Batocera | BOB A13 | OS Retro | Batocera | 64 GB | EmulationStation | Opcional | Imágenes + vídeos | [TODO] | RK3128 | PowKiddy A13, PS5000, PS7000 | Histórico | Build comunitaria asociada a Batocera v35/v35b para RK3128 |
| Recalbox | Oficial | OS Retro | Recalbox | 16 GB | EmulationStation | Opcional | Imágenes + vídeos | https://www.recalbox.com/ | SBC / PC | Raspberry Pi, PC, Odroid | Activo | Alternativa sencilla y muy integrada para Raspberry Pi y PC |
| RetroPie | Oficial | OS Retro | RetroPie | 8 GB | EmulationStation | Opcional | Imágenes + vídeos | https://retropie.org.uk/ | SBC / PC | Raspberry Pi, PC Linux, Odroid | Activo | Ecosistema clásico basado en scripts y paquetes |
| Lakka | Oficial | OS Retro | LibreELEC | 8 GB | RetroArch | No | Limitado | https://www.lakka.tv/ | SBC / PC | Raspberry Pi, PC, Odroid, Orange Pi y otros SBC | Activo | Experiencia centrada en RetroArch; menos orientado a gamelists visuales |
| RGB-Pi OS | Oficial | OS Retro | RGB-Pi | 16 GB | EmulationStation | Opcional | Imágenes + vídeos | https://www.rgb-pi.com/ | Raspberry Pi | Raspberry Pi con salida RGB/CRT | Activo | Especializado en uso con CRT y cableado RGB-Pi |
| Pi Entertainment System | PES | OS Retro | PES | 8 GB | EmulationStation | Opcional | Imágenes + vídeos | https://pes.mundayweb.com/ | Raspberry Pi | Raspberry Pi | Histórico | Proyecto veterano para Raspberry Pi |
| RetroDECK | Oficial | OS Retro | RetroDECK | 8 GB | ES-DE | Opcional | Imágenes + vídeos | https://retrodeck.net/ | Linux / PC | Linux desktop, Steam Deck, handheld PC x86 | Activo | Solución empaquetada tipo Flatpak; útil como referencia aunque no uses Steam Deck |
| Bazzite | ES-DE | OS Retro | Bazzite | 64 GB | ES-DE | Opcional | Imágenes + vídeos | https://bazzite.gg/ | Linux / PC | Mini PC x86, handheld PC, Steam Deck, HTPC | Activo | Sistema moderno tipo consola basado en Fedora/uBlue |
| ChimeraOS | Oficial | OS Retro | ChimeraOS | 64 GB | Steam Big Picture / ES-DE | Opcional | Imágenes + vídeos | https://chimeraos.org/ | Linux / PC | Mini PC x86, HTPC, handheld PC | Activo | Sistema orientado a experiencia consola sobre hardware PC |
| RetroBat | — | OS Retro | RetroBat | — | EmulationStation | Opcional | Imágenes + vídeos | https://www.retrobat.org/ | Windows | PC Windows, handheld PC x86 | Activo | Paquete todo-en-uno (RetroArch + emuladores + ES-DE) preconfigurado para Windows |

## Android CFW / Stock Mods

| Nombre | Variante | Tipo | Familia | SD base | Frontend | Requiere gamelist | Media soportada | Página / repo | Plataforma principal | Dispositivos principales | Estado | Notas |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| GammaOS | Legacy | Android CFW | GammaOS | — | Android Launcher | No | Imágenes + vídeos | https://github.com/TheGammaSqueeze/GammaOS | Android | RG405M, RG405V, RG505, Retroid Pocket 3+, PowKiddy X18S y T618 compatibles | Mantenimiento | Rama clásica; útil en dispositivos Android donde el firmware stock es débil |
| GammaOS | Next | Android CFW | GammaOS | 32 GB | Android Launcher | No | Imágenes + vídeos | https://github.com/TheGammaSqueeze/GammaOSNext | Android | Anbernic RG Vita Pro/RG Vita/RG477M/RG477V/RG557/RG556/RG Cube/RG406H/RG406V/RG476H/RG Slide/RG405M/RG405V/RG505/RG Rotate/RG DS; TrimUI Brick; MagicX Mini Zero 28/XURetro X20 V32; AYANEO Pocket Air Mini/Pocket Micro; Retroid Pocket 4 PRO/Classic; KT Pocket KT-R1; ZPG Unicorn A1; GameMT E6 MAX; Mangmi Air X | Activo | Lista de dispositivos según README oficial del proyecto (2026); proyecto vivo, cambia con frecuencia — verificar siempre contra la fuente oficial |
| GammaOS | Core | Android CFW | GammaOS | 32 GB | Android Launcher | No | Imágenes + vídeos | https://github.com/TheGammaSqueeze/GammaOSCore | Android | Anbernic RG ARC-D, RG ARC-S, RG353V, RG353VS, RG353P, RG353PS, RG353M, RG503; PowKiddy RGB30, RGB20SX, RGB10MAX3, RGB20 PRO, X55, X35H, X35S; GameMT E5 Plus, E6 Plus; GKD Bubble; MagicX Zero28; CB408; TrimUI Smart Pro; Miyoo Flip | Activo | Lista de dispositivos compatibles según README oficial del proyecto (2026); proyecto vivo, cambia con frecuencia — verificar siempre contra la fuente oficial |
| GammaOS | Nano | Android CFW | GammaOS | [TODO] | Android Launcher | No | Imágenes + vídeos | https://github.com/TheGammaSqueeze/GammaOSNext | Android | GKD 350H Ultra, TrimUI Brick, MagicX Zero 40, MagicX XURetro X20 V32, MagicX Mini Zero 28, Anbernic RG Rotate, Anbernic RG DS | Activo | Descrita por el propio proyecto como "micro-OS completo sobre Android", no un launcher tradicional; distribuida dentro del repo GammaOSNext; v1.4.1 (agosto 2026); lista de dispositivos según README oficial — proyecto vivo, verificar siempre contra la fuente |
| 351Droid | — | Android CFW | Android | — | Android Launcher | No | Imágenes + vídeos | https://github.com/351Droid/351Droid | Android | RG351M, RG351P, RG351MP, RG351V | Histórico | Port Android 11 para la familia RG351 |
| Anbernic H700 StockOS Mod | cbepx-me | Stock Mod | Anbernic StockOS | — | Stock UI | No | Limitado | https://github.com/cbepx-me/Anbernic-H700-RG-xx-StockOS-Modification | Linux Handheld | RG35XX Plus/H/SP, RG28XX, RG40XXH/V, RG Cube XX, RG34XX | Activo | Modificación del firmware stock H700; no es Android, pero encaja mejor como modificación de stock |
| Modified Stock OS | Genérico | Stock Mod | Stock Mod | — | Stock UI | No | Limitado | Depende del autor | Linux Handheld / Android | Varias familias | Mantenimiento | Entrada paraguas para modificaciones de firmware stock no modeladas como proyecto independiente |
| RogueOS | — | Stock Mod | RogueOS | 4 GB | EmulationStation | Opcional | Imágenes + vídeos | https://github.com/Ninoh-FOX/PIXEL2-ROGUE-OS/releases | Linux Handheld | GKD Pixel 2 | Activo | Por Ninoh-FOX; hereda drivers de pantalla/energía de fábrica. PortMaster integrado, avisos de batería por vibración al 10%/5% y apagado seguro al 1%, RetroArch actualizado y reproductor de música con pantalla apagada. Arranque de fábrica (~30s) |
| plumOS-GKD | — | Stock Mod | plumOS | 16 GB | EmulationStation | Opcional | Imágenes + vídeos | https://github.com/game-de-it/plumOS-GKD | Linux Handheld | GKD Bubble, GKD Mini Plus, GKD Pixel 2 | Activo | Comunidad game-de-it; hereda base de fábrica. Arranque y sleep mode más rápidos del grupo; ecualizador ajustado a los altavoces; núcleos ligeros (picoarch, pyxel) con RetroArch configurado para reducir input lag. GKD Pixel 2 usa un repositorio de build específico (`game-de-it/plumOS-pixel2`), distinto del repo genérico de esta fila |
| LineageOS | Android 8.1 v2 (RP2) | Android CFW | LineageOS | — | Android Launcher | No | Imágenes + vídeos | https://retrogamecorps.com/2021/03/21/lineageos-android-8-1-on-retroid-pocket-2/ | Android | Retroid Pocket 2 | Mantenimiento | Build comunitaria para RP2; limpia apps stock y mejora rendimiento general. |
| RetroidOS | — | Stock Mod | RetroidOS | — | Android Launcher | No | Imágenes + vídeos | [TODO] | Android | Retroid Pocket (varias generaciones) | Activo | Firmware Android stock del fabricante Retroid; alternativa a LineageOS cuando no se quiere sustituir el sistema base |

## Frontends

| Nombre | Variante | Tipo | Familia | Frontend | Requiere gamelist | Media soportada | Página / repo | Plataforma principal | Dispositivos principales | Estado | Notas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| EmulationStation Desktop Edition | ES-DE | Frontend | EmulationStation | ES-DE | Opcional | Imágenes + vídeos | https://es-de.org/ | Android, Windows, Linux, macOS | Multiplataforma | Activo | Referencia principal para reutilización de gamelist.xml y media |
| Pegasus Frontend | — | Frontend | Pegasus | Pegasus | Opcional | Imágenes + vídeos | https://pegasus-frontend.org/ | Android, Windows, Linux, macOS | Multiplataforma | Activo | Altamente configurable; requiere mayor trabajo inicial |
| LaunchBox | Desktop | Frontend | LaunchBox | LaunchBox | No | Imágenes + vídeos | https://www.launchbox-app.com/ | Windows | PC Windows | Activo | Interfaz de escritorio orientada a gestión de colecciones |
| LaunchBox | BigBox | Frontend | LaunchBox | BigBox | No | Imágenes + vídeos | https://www.launchbox-app.com/ | Windows | PC Windows, bartops, recreativas, HTPC | Activo | Interfaz premium orientada a uso con mando y recreativas |
| RetroArch | Android | Frontend | RetroArch | RetroArch | No | Limitado | https://www.retroarch.com/ | Android | Tablets, móviles, Android TV, handhelds Android | Activo | Más gestor de emulación que frontend de colección |

## Launchers

| Nombre               | Variante | Tipo     | Familia          | Frontend         | Requiere gamelist | Media soportada   | Página / repo                                                          | Plataforma principal | Dispositivos principales                             | Estado | Notas                                                  |
| -------------------- | -------- | -------- | ---------------- | ---------------- | ----------------- | ----------------- | ---------------------------------------------------------------------- | -------------------- | ---------------------------------------------------- | ------ | ------------------------------------------------------ |
| Daijishō             | —        | Launcher | Daijishō         | Daijishō         | No                | Imágenes + vídeos | https://daijisho.com/                                                  | Android              | Odin, Retroid, Anbernic Android, tablets, Android TV | Activo | Launcher Android de referencia durante varios años     |
| Dawn Launcher        | —        | Launcher | Dawn             | Dawn             | No                | Imágenes + vídeos | [TODO]                                                                  | Android              | MagicX Zero 40, MagicX Mini Zero 28                  | Activo | Launcher stock preinstalado de fábrica en dispositivos MagicX; estética similar a Daijishō |
| Beacon Game Launcher | —        | Launcher | Beacon           | Beacon           | No                | Imágenes + vídeos | https://play.google.com/store/apps/details?id=com.radikal.gamelauncher | Android              | Android handhelds, tablets, Android TV               | Activo | Launcher moderno con enfoque minimalista               |
| Console Launcher     | —        | Launcher | Console Launcher | Console Launcher | No                | Imágenes + vídeos | https://play.google.com/store/apps/details?id=com.k2.consolelauncher   | Android              | Android handhelds, tablets, Android TV               | Activo | Interfaz inspirada en consolas tradicionales           |
| DIG                  | —        | Launcher | DIG              | DIG              | No                | Imágenes + vídeos | https://diglauncher.com/                                               | Android              | Android handhelds, tablets, Android TV               | Activo | Uno de los launchers Android clásicos de la escena     |
| RESET Collection     | —        | Launcher | RESET Collection | RESET Collection | No                | Imágenes + vídeos | https://resetcollection.app/                                           | Android              | Android handhelds, tablets, Android TV               | Activo | Launcher premium orientado a coleccionismo y metadatos |

## Históricos / Legado

| Nombre | Variante | Tipo | Familia | Frontend | Requiere gamelist | Media soportada | Página / repo | Plataforma principal | Dispositivos principales | Estado | Notas |
|---|---|---|---|---|---|---|---|---|---|---|---|
| JELOS | — | Histórico | JELOS | EmulationStation | Opcional | Imágenes + vídeos | https://github.com/JustEnoughLinuxOS/distribution | Linux Handheld | RK3326, RK3566, RG353, RGB30 y compatibles | Histórico | Proyecto clave del que derivan o se inspiran ROCKNIX y numerosos sistemas modernos |
| 351ELEC | — | Histórico | 351ELEC | EmulationStation | Opcional | Imágenes + vídeos | https://github.com/351ELEC/351ELEC | Linux Handheld | RG351P, RG351M, RG351V, RG351MP | Histórico | Predecesor directo de AmberELEC y referencia histórica para la familia RG351 |