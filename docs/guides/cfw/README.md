# Guías de instalación de CFW

Guías paso a paso para instalar los CFW/OS marcados como `Recomendado` o `Verificado` en `docs/distributions.md`. Cada guía es un scaffold pendiente de contenido.

## Tipos de instalación

Cada guía declara en su sección "Tipo de instalación" cuál de estos tres métodos aplica, ya que difieren sustancialmente en herramientas y pasos:

- **Imagen flasheada a SD** — se escribe una imagen de disco completa (Etcher/Rufus/dd) en la SD, típico de OS Retro para SBC (Batocera, Recalbox).
- **Extracción a SD existente** — se descomprime un zip directamente sobre una SD ya formateada (FAT32/ext4), a menudo con esquema de doble tarjeta TF1 (sistema) + TF2 (ROMs), típico de CFW/OS Handheld para consolas portátiles.
- **Flasheo por fastboot o herramienta de fabricante** — se usa fastboot, SP Flash Tool u otra herramienta específica del SoC para escribir directamente en el almacenamiento interno, típico de Android CFW.

| CFW | Dispositivos aplicables (principal) | Guía |
| --- | --- | --- |
| Batocera | Raspberry Pi 3B+ | [batocera.md](batocera.md) |
| Recalbox | Raspberry Pi 5 (4GB) | [recalbox.md](recalbox.md) |
| BOB (Best of the Best) | PocketGo Bitboy, Pocket Go, PowKiddy Q90/V90/Q20 Mini | [bob.md](bob.md) |
| BOB A13 (Batocera v35b) | PowKiddy A13 | [bob-a13.md](bob-a13.md) |
| BOB (Best of the Best) — variante ArkOS | Anbernic RG351P/M/V/MP, PowKiddy RGB10 Max | [bob-arkos.md](bob-arkos.md) |
| RetroFW | PowKiddy LDK Landscape/Vertical, Retrogame RS97, Anbernic RG99, PowKiddy RS-07 | [retrofw.md](retrofw.md) |
| Adam Image | Anbernic RG350/RG280M/RG350M/RG280V/RG350P/RG300X, PocketGo2 V1 | [adam-image.md](adam-image.md) |
| ArkOS | Hardkernel Odroid-Go-Advance, RK2020 | [arkos.md](arkos.md) |
| ROCKNIX | PowKiddy RGB10, Anbernic RG353P/RG353V, RGARC-S | [rocknix.md](rocknix.md) |
| dArkOS | PowKiddy RGB20, RGB10 Max 2 | [darkos.md](darkos.md) |
| Simple30 | PocketGo S30 | [simple30.md](simple30.md) |
| AmberELEC | Anbernic RG351M/RG351V/RG351MP | [amberelec.md](amberelec.md) |
| Koriki BOM | Miyoo Mini, Miyoo Mini Plus, Miyoo Mini Flip, Miyoo Flip, RG35XX Original | [koriki.md](koriki.md) |
| KNULLI | Anbernic RG35XX Plus/RG35XXH/RG35XXSP/RG34XX/RG34XXSP/RG40XXV/RG40XXH/RG CubeXX, PowKiddy V10/V90S | [knulli.md](knulli.md) |
| FunKey OS | Base para RGNano y derivados | [funkey-os.md](funkey-os.md) |
| DrUm78 RGNano | Anbernic RGNano | [drum78-rgnano.md](drum78-rgnano.md) |
| CrossMix-OS | TrimUI TRIMUI Smart Pro, TRIMUI Brick | [crossmix-os.md](crossmix-os.md) |
| MinUI | TrimUI Model S | [minui.md](minui.md) |
| spruceOS | Miyoo A30 | [spruceos.md](spruceos.md) |
| muOS | Anbernic RG28XX | [muos.md](muos.md) |
| GammaOS Core | Anbernic RG353/RG503/RGARC, PowKiddy RGB/X series, GKD Bubble, TrimUI Smart Pro, Miyoo Flip (lista completa verificada en la guía) | [gammaos-core.md](gammaos-core.md) |
| GammaOS Next | Anbernic RG Vita/Cube/406H/406V/505/405/DS/Rotate, TrimUI Brick, MagicX Mini Zero 28/X20 V32, AYANEO Pocket, Retroid Pocket 4, KT-R1, ZPG, GameMT (lista completa verificada en la guía) | [gammaos-next.md](gammaos-next.md) |
| LineageOS (RP2) | Retroid Pocket 2 | [lineageos-rp2.md](lineageos-rp2.md) |
| OnionOS | Miyoo Mini, Miyoo Mini Plus | [onionos.md](onionos.md) |
| GarlicOS | Anbernic RG35XX (Original) | [garlicos.md](garlicos.md) |
| EmuELEC | TV Boxes (Amlogic S905/S912), Super Console X, Game Sticks | [emuelec.md](emuelec.md) |
| RogueOS | GKD Pixel 2 | [rogueos.md](rogueos.md) |
| twigUI | GKD Pixel 2 | [twigui.md](twigui.md) |
| plumOS (build GKD Pixel 2) | GKD Pixel 2 | [plumos-pixel2.md](plumos-pixel2.md) |
