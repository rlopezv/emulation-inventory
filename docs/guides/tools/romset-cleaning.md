# Limpieza de romset

Eliminación de clones, contenido no deseado (mahjong, casino, contenido maduro) y duplicados cross-sistema, sobre el romset físico ya auditado (fase 3). No es un filtrado 1G1R completo (eso es la fase 5) — aquí se trata de recortar categorías enteras no deseadas, no de quedarse con una sola región por juego.

Corresponde a la fase 4 de [docs/guides/romsets/workflow.md](../romsets/workflow.md).

**Relación con el pipeline propio:** `filter-by-title-type.ps1` y `filter-cross-system-duplicates.ps1` (documentados en [docs/guides/romsets/custom-pipeline.md](../romsets/custom-pipeline.md)) hacen una limpieza equivalente pero sobre `dat-index/<id>.json` (metadatos), antes de tocar ficheros físicos. Esta guía cubre la limpieza posterior sobre el romset físico con herramientas de terceros.

## ROMSorter

**Fuente:** github.com/drakewill-CRL/ROMSorter. Aplicación de escritorio (no CLI), requiere .NET 6, Windows x64 principalmente (el componente "Librarian" sí es multiplataforma).

**Funciones confirmadas** (interfaz de botones, no scriptable):

- **Zip/Unzip all files** — comprime cada carpeta de ROMs a un ZIP individual (recomprime lo existente, extrae RAR/7z/TAR antes de comprimir) o descomprime todo.
- **Catalog Files / Verify Catalog** — genera un catálogo de nombres+hashes sin necesidad de leer los ficheros completos cada vez, y lo usa después para verificar integridad rápidamente.
- **Rename Single-File games** — renombra ROMs identificadas usando ficheros `.DAT`, compatible con TOSEC.
- **1G1R Sort** — selección 1 Game 1 ROM según prioridad de región (relevante también para la fase 5, pero disponible aquí como atajo si no se necesita el control fino de retool).
- **Everdrive Sort** — organiza en subcarpetas por letra inicial, pensado para flashcarts con límite de ficheros por carpeta.
- Conversión BIN/CUE e ISO → CHD (requiere `chdman` en el sistema).

[TODO: no se ha identificado en la documentación disponible una función específica de "limpieza" por categoría (mahjong/casino/adulto) — parece más orientado a organización/1G1R que a exclusión de categorías; para eso ver Simple Arcade Multifilter más abajo]

## Simple Arcade Multifilter (SAM)

**Fuente:** github.com/markwkidd/ahk-retroarch-playlist-helpers (script AutoHotKey). Pensado específicamente para sets arcade (MAME, FB Alpha).

**Entradas requeridas** (deben coincidir exactamente con la versión del romset a filtrar):

- **`catver.ini`** — fichero de categorización por género/tipo.
- **DAT XML** — metadatos del set. Ambos se obtienen de los repositorios correspondientes a la versión de MAME en uso (2000, 2003, 2010, 2014, 2016) o de FB Alpha.

**Flujo de uso confirmado (2 pasos):**

1. **Configuración** — indicar carpeta de ROMs de origen, DAT, `catver.ini` y carpeta de destino.
2. **Filtrado** — seleccionar categorías a incluir (`OR`) o excluir (`NOT`) mediante checkboxes; tres filtros adicionales disponibles: incluir BIOS, excluir clones, excluir juegos marcados como "Mature" (contenido maduro).

**Salida:** una carpeta nueva con el romset ya filtrado y organizado, incluyendo los BIOS asociados copiados según los criterios elegidos — lista para usar directamente en RetroArch/MAME.

## RA ROM Processor (discos ópticos — CHD/RVZ)

**Fuente:** github.com/RandomNinjaAtk/docker-raromprocessor. Contenedor Docker que cubre un hueco real de ROMSorter/SAM: ninguna de las dos herramientas anteriores trabaja con discos ópticos (CHD/RVZ), y esta sí — apoyándose en la capacidad de **RAHasher** de identificar CHD/RVZ sin descomprimir (ver [romset-audit.md](romset-audit.md#identificación-rápida-de-chdrvz-sin-descomprimir-rahasher)).

**Confirmado:** adquiere/organiza/procesa/verifica/desduplica una biblioteca de ROMs completa, cruzándola contra la base de hashes de RetroAchievements (ver `docs/references.md#retroachievements-como-fuente-de-datos`) vía RAHasher, y encadena **SkyScraper** (ver [media-scraping.md](media-scraping.md)) para el scraping de metadatos del resultado ya limpio.

**Flujo:** genera carpetas de entrada por plataforma; con la opción **AutoStart** activada, basta con copiar/mover los ROMs a ese volumen para que el contenedor los procese automáticamente — valida/empareja contra la base de RA, desduplica, y guarda el resultado ya organizado (más media) en el volumen de salida.

[TODO: no se ha verificado el detalle exacto de configuración del contenedor (variables de entorno, plataformas soportadas) — consultar el README del repositorio antes de desplegarlo]

### Alternativa manual sin Docker — script PowerShell con RAHasher

Si no se quiere levantar el contenedor de RA ROM Processor, se puede automatizar directamente con **RAHasher** y un script propio: escanea una carpeta de CHD/RVZ, calcula el hash de RA de cada uno, lo cruza contra el JSON de `retroachievements/` correspondiente, y separa los que tienen logros de los que no.

**Preparación:**

1. **RAHasher.exe** — tres vías confirmadas para conseguirlo sin compilar:
   - **Ya instalado con LaunchBox** (si ya se usa) — `LaunchBox\Third Party\RetroAchievements\rahasher.exe` (ruta exacta confirmada; nota el espacio en "Third Party").
   - **Binarios precompilados oficiales** — github.com/LeXofLeviafan/RAHasher (repositorio original, con Releases).
   - **Compilar desde código fuente** — solo necesario con el fork `nixxou/RAHasher` (el usado como referencia en el resto de esta guía por su documentación de sintaxis más completa), que no publica binarios: MSYS2+Makefile o Visual Studio.
2. El JSON del sistema a limpiar, desde `retroachievements/` de `retool-clonelists-metadata` (ver [dat-generation.md](dat-generation.md#redump)). **Nombre real del fichero sin guion** (corregido): `Sony PlayStation.json`, no `Sony - PlayStation.json`.
3. El "sistema" que espera RAHasher admite tanto claves de texto (`PS1`, `Saturn`, `GC`, `Wii`...) como ID numérico — **más seguro usar la clave de texto** para evitar errores de ID (confirmados dos casos incorrectos en la guía original: Saturn es **39**, no 19; GameCube es **16**, no 24).

**Script** (`limpiar_romset.ps1`), con las correcciones aplicadas:

```powershell
# ================= CONFIGURACIÓN =================
$Sistema_RA   = "PS1"                                     # Clave de texto de RAHasher (más segura que el ID numérico)
$Ruta_Juegos  = "D:\Ruta\A\Tus\Archivos\CHD"               # Carpeta de tus juegos reales
$Archivo_JSON = "C:\LimpiezaRA\Sony PlayStation.json"      # Sin guion en el nombre real del fichero
$RAHasher_Exe = "C:\LimpiezaRA\RAHasher.exe"               # Compilado desde código fuente, no hay binario oficial
# =================================================

# 1. Cargar e indexar los hashes válidos del JSON en memoria
Write-Host "Cargando base de datos JSON de RetroAchievements..." -ForegroundColor Cyan
$DatosJSON = Get-Content -Raw -Path $Archivo_JSON | ConvertFrom-Json
$HashesValidos = @{}
foreach ($item in $DatosJSON.retroachievements) {
    $HashesValidos[$item.sha1.ToLower()] = $item.name
}

# 2. Crear carpeta de destino para los juegos válidos
$Carpeta_Destino = Join-Path $Ruta_Juegos "_Con_Logros"
if (!(Test-Path $Carpeta_Destino)) { New-Item -ItemType Directory -Path $Carpeta_Destino | Out-Null }

# 3. Escanear los juegos de la carpeta
$Formatos = "*.chd", "*.rvz"
$Archivos = Get-ChildItem -Path $Ruta_Juegos -Include $Formatos -Recurse | Where-Object { $_.FullName -notlike "*_Con_Logros*" }

Write-Host "Iniciando escaneo de $($Archivos.Count) juegos con RAHasher..." -ForegroundColor Yellow

foreach ($archivo in $Archivos) {
    # RAHasher.exe [sistema] "ruta" — orden confirmado en la documentación oficial
    $ResultadoRA = & $RAHasher_Exe $Sistema_RA $archivo.FullName 2>$null

    # [TODO: sin verificar — formato exacto de la salida de texto de RAHasher no confirmado.
    # Probar contra un solo fichero conocido antes de lanzar el script contra todo el romset,
    # y ajustar esta expresión regular si no extrae el hash correctamente.]
    $HashCalculado = ($ResultadoRA | Out-String).Trim() -replace '(?s).*?\s([a-f0-9]{32,40})$', '$1'

    if ($HashCalculado -match '^[a-f0-9]{32,40}$') {
        $HashCalculado = $HashCalculado.ToLower()
        if ($HashesValidos.ContainsKey($HashCalculado)) {
            $NombreJuegoRA = $HashesValidos[$HashCalculado]
            Write-Host "[OK] COINCIDENCIA: '$($archivo.Name)' -> $NombreJuegoRA" -ForegroundColor Green
            Move-Item -LiteralPath $archivo.FullName -Destination $Carpeta_Destino -Force
        } else {
            Write-Host "[--] SIN LOGROS: '$($archivo.Name)' (Hash RA: $HashCalculado)" -ForegroundColor Red
        }
    } else {
        Write-Host "[!!] ERROR: RAHasher no pudo parsear '$($archivo.Name)'" -ForegroundColor DarkYellow
    }
}

Write-Host "`nProceso finalizado. Juegos compatibles en _Con_Logros." -ForegroundColor Cyan
```

**Qué hace:** separa en `_Con_Logros` únicamente los ficheros cuyo hash de RA coincide con el JSON — de facto, un filtrado 1G1R basado en "qué versión tiene logros asignados" en vez de en prioridad de región (si USA tiene logros y EUR/JAP no, solo se mueve la versión USA).

**Antes de confiar en el resultado:** verificar manualmente con un solo fichero conocido que el parseo de la salida de RAHasher extrae el hash correcto — es el único paso de todo el script que no se ha podido confirmar contra documentación oficial.

## Notas

El resultado de esta fase alimenta la fase 5 (filtrado 1G1R, [1g1r-filtering.md](1g1r-filtering.md)): conviene limpiar categorías no deseadas (mahjong, casino, adulto, BIOS sueltas) antes de aplicar 1G1R, para no perder tiempo procesando contenido que se va a descartar de todos modos.

A diferencia de la fase 3 (auditoría), estas herramientas sí modifican o reorganizan ficheros directamente — hacer una copia de seguridad del romset auditado antes de ejecutar cualquiera de las dos, especialmente la primera vez.
