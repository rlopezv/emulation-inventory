# Guías de frontends y apps

Guías de configuración de frontends y de instalación de emuladores standalone que corren *sobre* un CFW/OS ya instalado, a diferencia de `docs/guides/cfw/`, que cubre el firmware en sí. Cada guía es un scaffold pendiente de contenido.

## Contexto de uso

Cada guía declara en "Contexto de uso" si el frontend/app viene embebido en el CFW (sin instalación propia) o es standalone (requiere descarga e instalación aparte, típico en Android/PC):

- **Embebido en CFW** — viene incluido de fábrica en el firmware (EmulationStation, SimpleMenu); no tiene sección de Descarga/Instalación propia.
- **Standalone instalable** — app independiente (APK Android, ejecutable Windows/Linux) que se instala sobre un sistema ya existente (ES-DE, Daijishō, Pegasus, emuladores Android).

| Frontend / App | Contexto | Guía |
| --- | --- | --- |
| EmulationStation | Embebido en CFW | [emulationstation.md](emulationstation.md) |
| SimpleMenu | Embebido en CFW | [simplemenu.md](simplemenu.md) |
| GMenu2X | Embebido en CFW | [gmenu2x.md](gmenu2x.md) |
| RetroFE | Embebido en CFW | [retrofe.md](retrofe.md) |
| ES-DE | Standalone (Android/PC) | [es-de.md](es-de.md) |
| Daijishō | Standalone (Android) | [daijisho.md](daijisho.md) |
| Pegasus | Standalone (Android/PC) | [pegasus.md](pegasus.md) |
| pyMenu | Embebido en CFW / Standalone ligero | [pymenu.md](pymenu.md) |
| Emuladores Android | Standalone (Android) | [android-emuladores.md](android-emuladores.md) |
| RetroArch | Embebido en CFW / Standalone (Android/PC) | [retroarch.md](retroarch.md) |
