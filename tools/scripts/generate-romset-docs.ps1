<#
Genera/actualiza una seccion auto-generada en docs/guides/romsets/systems/<id>.md
por cada metadata/dat-index/<id>.json, con la lista de familias y su
categoria (Oficial/Unl/Pirate/etc).

La seccion auto-generada va delimitada por marcadores para poder
convivir con contenido curado a mano en el mismo fichero (ver
gx4000.md, curado aparte). Si el fichero no existe, se crea con esa
seccion. Si ya existe:
- con marcadores: se reemplaza solo el contenido entre marcadores.
- sin marcadores: se anade la seccion al final del fichero.

Tambien regenera la tabla indice de docs/guides/romsets/systems/README.md
a partir de los ficheros .md presentes en esa carpeta.

Uso:
    pwsh tools/scripts/generate-romset-docs.ps1
    pwsh tools/scripts/generate-romset-docs.ps1 -SystemId psx
#>

[CmdletBinding()]
param(
    [string]$SystemId,
    [string]$IndexRoot,
    [string]$DocsRoot
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)

if (-not $IndexRoot) { $IndexRoot = Join-Path $repoRoot "metadata\dat-index" }
if (-not $DocsRoot) { $DocsRoot = Join-Path $repoRoot "docs\guides\romsets\systems" }

$StartMarker = "<!-- AUTO-GENERADO INICIO -->"
$EndMarker = "<!-- AUTO-GENERADO FIN -->"
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)

function Read-TextFile {
    param([string]$Path)
    if (-not (Test-Path $Path)) { return $null }
    return [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
}

function Write-TextFile {
    param([string]$Path, [string]$Content)
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    [System.IO.File]::WriteAllText($Path, $Content, $Utf8NoBom)
}

function Build-AutoSection {
    param($Json)

    # Agrupa por (nombre, regiones) solo para mostrar: cuando el nombre base
    # ya no distingue discos (ej. "Disc 1"/"Disc 2" quitados al generar el
    # dat-index), varias entradas con el mismo nombre y las mismas regiones
    # son casi siempre el mismo juego repartido en varios discos, no juegos
    # distintos. Se muestran como una sola fila con el numero de discos.
    # No modifica metadata/dat-index/<id>.json, solo el render de la tabla.
    $groups = @($Json.games | Group-Object -Property { "$($_.name)|$($_.regions -join ',')" })

    $lines = New-Object System.Collections.Generic.List[string]
    [void]$lines.Add($StartMarker)
    [void]$lines.Add("")
    [void]$lines.Add("### Indice generado")
    [void]$lines.Add("")
    [void]$lines.Add("Fuente: ``$($Json.source)`` -- ``$($Json.dat)``. Generado: ``$($Json.generated)``. Total: $($groups.Count) familias.")
    [void]$lines.Add("")
    [void]$lines.Add("Regenerar con: ``pwsh tools/scripts/generate-romset-docs.ps1 -SystemId $($Json.system)``")
    [void]$lines.Add("")
    [void]$lines.Add("| Nombre | Categoria | Regiones | Discos | Alias |")
    [void]$lines.Add("| --- | --- | --- | --- | --- |")
    foreach ($grp in $groups) {
        $first = $grp.Group[0]
        $name = $first.name -replace '\|', '\|'
        $categories = @($grp.Group | ForEach-Object { $_.properties.category } | Select-Object -Unique)
        $category = if ($categories -contains "Oficial") { "Oficial" } else { ($categories | Sort-Object) -join ", " }
        $regions = ($first.regions -join ', ')
        $aliasSet = @($grp.Group | ForEach-Object { $_.aliases } | Select-Object -Unique)
        $aliases = ($aliasSet -replace '\|', '\|') -join ' / '
        $discs = $grp.Count
        [void]$lines.Add("| $name | $category | $regions | $discs | $aliases |")
    }
    [void]$lines.Add("")
    [void]$lines.Add($EndMarker)
    return ($lines -join "`n")
}

function Update-DocFile {
    param([string]$Id, [string]$AutoSection)

    $path = Join-Path $DocsRoot "$Id.md"
    $existing = Read-TextFile -Path $path

    if (-not $existing) {
        $content = "# $Id -- Curacion`n`n$AutoSection`n"
        Write-TextFile -Path $path -Content $content
        Write-Host "Creado: $path"
        return
    }

    $startIdx = $existing.IndexOf($StartMarker)
    $endIdx = $existing.IndexOf($EndMarker)

    if ($startIdx -ge 0 -and $endIdx -ge 0 -and $endIdx -gt $startIdx) {
        $before = $existing.Substring(0, $startIdx)
        $after = $existing.Substring($endIdx + $EndMarker.Length)
        $content = $before + $AutoSection + $after
    } else {
        $separator = if ($existing.EndsWith("`n")) { "`n" } else { "`n`n" }
        $content = $existing + $separator + $AutoSection + "`n"
    }

    Write-TextFile -Path $path -Content $content
    Write-Host "Actualizado: $path"
}

function Update-Readme {
    $readmePath = Join-Path $DocsRoot "README.md"
    $files = @(Get-ChildItem -Path $DocsRoot -Filter "*.md" | Where-Object { $_.Name -ne "README.md" } | Sort-Object Name)

    $rows = $files | ForEach-Object {
        $id = [System.IO.Path]::GetFileNameWithoutExtension($_.Name)
        "| ``$id`` | [$($_.Name)]($($_.Name)) |"
    }

    $content = @"
# Curacion por sistema

Ficheros de curacion con informacion de referencia especifica por sistema (catalogo oficial vs. prototipos/homebrew, casos especiales de fuente, etc.) que no encaja como fila de tabla en ``docs/romsets.md``.

Cada fichero puede combinar contenido curado a mano con una seccion auto-generada (entre ``$StartMarker`` / ``$EndMarker``) con el listado de familias de ``metadata/dat-index/<id>.json``, regenerable con ``tools/scripts/generate-romset-docs.ps1``.

Esta carpeta complementa, no sustituye:
- ``docs/romsets.md`` -- asociacion sistema -> DAT (fuente, formato, alternativa).
- ``metadata/dat-index/<id>.json`` -- indice generado a partir del DAT real.

| Sistema | Fichero |
| --- | --- |
$($rows -join "`n")
"@

    Write-TextFile -Path $readmePath -Content ($content + "`n")
    Write-Host "Actualizado: $readmePath"
}

$jsonFiles = if ($SystemId) {
    @(Get-Item (Join-Path $IndexRoot "$SystemId.json") -ErrorAction SilentlyContinue)
} else {
    @(Get-ChildItem -Path $IndexRoot -Filter "*.json" -File)
}

foreach ($file in $jsonFiles) {
    if (-not $file) { continue }
    $id = [System.IO.Path]::GetFileNameWithoutExtension($file.Name)
    $json = Get-Content -Raw -Path $file.FullName | ConvertFrom-Json
    $autoSection = Build-AutoSection -Json $json
    Update-DocFile -Id $id -AutoSection $autoSection
}

Update-Readme
