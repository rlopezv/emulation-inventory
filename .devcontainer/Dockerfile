# Ver docs/session-context.md — investigación de herramientas de filtrado/
# conversión de DAT (sesión de dat_sources/dat_processing). Capa propia sobre
# la imagen base del devcontainer, para no tener que instalar retool/
# SabreTools a mano en cada sesión.
#
# - retool: requiere Python 3.10+, SIN binario compilado para Linux (confirmado
#   en unexpectedpanda.github.io/retool/download/) — se clona el repo y se
#   instalan sus dependencias con pip, tal como documenta el propio proyecto.
#   Sin releases con tag (el propio repo se declara "no longer maintained"),
#   así que se clona la rama por defecto (HEAD), no una versión fija.
# - SabreTools: SÍ tiene binario Linux self-contained desde v1.2.0 (confirmado
#   contra la API de GitHub, release 1.2.1: SabreTools_net9.0_linux-x64_release.zip).
#   Se fija esa versión con un ARG para poder subirla a mano cuando haga falta.
# - Igir: CLI Node.js (`igir.io`), agnóstico de fuente de DAT (No-Intro/Redump/
#   TOSEC/MAME) y con inferencia propia de relaciones parent/clone cuando el DAT
#   no las trae (`DATParentInferrer`, confirmado leyendo el código fuente —
#   incluye reglas específicas para la convención de nombrado TOSEC), a
#   diferencia de retool (necesita clonelist propio) y de 1g1r-romset-generator
#   (se niega a agrupar sin `cloneof`). Requiere Node.js >=22 (`igir@5.4.0`
#   declara ese engine) — la imagen base no lo trae, se instala vía NodeSource.
FROM mcr.microsoft.com/devcontainers/python:1-3.12-bookworm

ARG SABRETOOLS_VERSION=1.2.1
ARG IGIR_VERSION=5.4.0
ARG NODE_MAJOR=22

# El repo yarn preinstalado en la imagen base trae una firma GPG inválida
# que bloquea apt-get update (ver tools/application/pyproject.toml) — se
# quita antes de instalar nada más.
RUN rm -f /etc/apt/sources.list.d/yarn.list

# Librerías compartidas headless que pide PySide6 (dependencia de retool, aunque
# aquí solo se use la CLI retool.py, no la GUI retoolgui.py) para poder
# importarse sin fallar en un contenedor sin entorno gráfico.
RUN apt-get update && apt-get install -y --no-install-recommends \
        libgl1 \
        libegl1 \
        libxkbcommon0 \
        libdbus-1-3 \
        unzip \
    && rm -rf /var/lib/apt/lists/*

# --- retool (CLI) ---
RUN git clone --depth 1 https://github.com/unexpectedpanda/retool.git /opt/retool \
    && python3 -m pip install --no-cache-dir \
        alive-progress darkdetect lxml psutil pyside6 strictyaml validators \
    && printf '#!/bin/sh\nexec python3 /opt/retool/retool.py "$@"\n' > /usr/local/bin/retool \
    && chmod +x /usr/local/bin/retool

# --- SabreTools (CLI, binario self-contained Linux x64) ---
RUN curl -fsSL -o /tmp/sabretools.zip \
        "https://github.com/SabreTools/SabreTools/releases/download/${SABRETOOLS_VERSION}/SabreTools_net9.0_linux-x64_release.zip" \
    && unzip -q /tmp/sabretools.zip -d /opt/sabretools \
    && rm /tmp/sabretools.zip \
    && chmod +x /opt/sabretools/SabreTools \
    && ln -s /opt/sabretools/SabreTools /usr/local/bin/sabretools

# --- Node.js (para Igir) ---
RUN curl -fsSL "https://deb.nodesource.com/setup_${NODE_MAJOR}.x" | bash - \
    && apt-get install -y --no-install-recommends nodejs \
    && rm -rf /var/lib/apt/lists/*

# --- Igir (CLI) ---
# `npm install -g` en vez de `npx igir@latest`: npx no siempre corre los
# scripts de instalación completos del paquete nativo (`dolphin-tool`,
# addon .node precompilado) — confirmado en pruebas: con npx falla
# "Cannot find module './addon-dolphin-tool/build/Release/dolphin-tool.node'"
# incluso con Node 22. Fijar versión exacta con ARG, sin usar @latest.
RUN npm install -g "igir@${IGIR_VERSION}" --no-audit --no-fund

# Dependencias de tools/application (sin el paquete propio, que se instala en
# modo editable vía postCreateCommand contra el código ya montado) — cachea
# la capa pesada de pip para que el postCreateCommand real sea casi instantáneo.
RUN python3 -m pip install --no-cache-dir \
        "requests>=2.31" "pyyaml>=6.0" "click>=8.1" "pytest>=8.0"
