# RetroFE

RetroFE es un frontend de código abierto orientado a la presentación visual, con soporte para carátulas, vídeos de vista previa y transiciones animadas, tradicionalmente asociado a cabinas arcade y bartops. En el firmware DrUm78 RGNano se usa como lanzador de juegos por defecto de la Anbernic RGNano, adaptado al hardware ultracompacto (pantalla de 240x240 píxeles).

## Contexto de uso

Embebido en CFW (viene incluido, sin instalación propia).

## CFWs / plataformas donde se usa

- DrUm78 RGNano (Anbernic RGNano) — lanzador de juegos por defecto; el propio firmware ofrece además GMenu2X como interfaz secundaria para utilidades del sistema y reproductor de MP3/vídeo (ver [gmenu2x.md](gmenu2x.md) y `docs/guides/cfw/drum78-rgnano.md`).

## Descarga

No aplica: viene integrado en el CFW.

## Instalación

No aplica: viene integrado en el CFW.

## Estructura de carpetas y ROMs

Las ROMs se organizan en carpetas por sistema con nombres en minúsculas montadas bajo `/mnt/` (ej. `/mnt/gba/`, `/mnt/gbc/`, `/mnt/nes/`, `/mnt/snes/`, `/mnt/gg/`). Los BIOS de sistemas que los requieren se colocan en `/mnt/bios/`.

## Metadatos y scraping

RetroFE en DrUm78 RGNano no usa `gamelist.xml`; empareja carátulas por nombre de archivo:

- **Tratamiento de carátulas (previews)**: exige imágenes `.png` dentro de una subcarpeta `previews` en el directorio de cada sistema (ej. `/mnt/snes/previews/`). El nombre del archivo debe coincidir exactamente con el de la ROM.
- **Resolución objetivo**: al tratarse de una pantalla física cuadrada de 240x240 píxeles, las carátulas deben reescalarse a ese tamaño (filtro Lanczos recomendado) y reducirse a 8 bits de profundidad de color para evitar saturar la memoria de vídeo.

## Notas

- Búsqueda en subcarpetas soportada en versiones recientes de DrUm78, útil para organizar sets grandes de sistemas de 8 bits.
- Ver `docs/guides/cfw/drum78-rgnano.md` para el resto de detalles de instalación y configuración específicos del CFW.
