<#
Copia la raiz y las subcarpetas validas de un sistema de romsets en
F:\roms\console\<sistema> hacia una carpeta nueva F:\roms\console-complete\<sistema>,
aplanando todo a un solo nivel, para tener un romset "completo" (raiz + jpn/unl/pack/
usa/aftermarket/soniccd/cia/etc.) excluyendo las carpetas _SD, duplicates,
_duplicates y raw (redundantes o restos de pruebas). Tambien suma el contenido de
F:\roms\console\_extra\<sistema> (salvo que se indique -SkipExtra).

Uso:
    pwsh tools/scripts/build-complete-romset.ps1 -SystemId gb -WhatIf
    pwsh tools/scripts/build-complete-romset.ps1 -SystemId gb
    pwsh tools/scripts/build-complete-romset.ps1 -SystemId gb -SkipExtra
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SystemId,

    [string]$SourceRoot = "F:\roms\console",

    [string]$DestRoot = "F:\roms\console-complete",

    [string]$ExtraSystemId,

    [switch]$SkipExtra,

    [switch]$WhatIf
)

$ExcludedDirs = @('_SD', 'duplicates', '_duplicates', 'raw')

$sourceSystemDir = Join-Path $SourceRoot $SystemId
if (-not (Test-Path $sourceSystemDir)) {
    throw "No existe la carpeta de origen: $sourceSystemDir"
}

$destSystemDir = Join-Path $DestRoot $SystemId

# Recopilar origenes: raiz primero, luego subcarpetas validas en orden alfabetico
$sources = New-Object System.Collections.Generic.List[object]

$rootFiles = @(Get-ChildItem -Path $sourceSystemDir -File -Force)
foreach ($f in $rootFiles) {
    $sources.Add([PSCustomObject]@{ Origin = "(root)"; File = $f })
}

$subDirs = @(Get-ChildItem -Path $sourceSystemDir -Directory -Force |
    Where-Object { $ExcludedDirs -notcontains $_.Name } |
    Sort-Object Name)

foreach ($dir in $subDirs) {
    $files = @(Get-ChildItem -Path $dir.FullName -File -Recurse -Force)
    foreach ($f in $files) {
        $sources.Add([PSCustomObject]@{ Origin = $dir.Name; File = $f })
    }
}

if (-not $SkipExtra) {
    $extraId = if ($ExtraSystemId) { $ExtraSystemId } else { $SystemId }
    $extraDir = Join-Path (Join-Path $SourceRoot "_extra") $extraId
    if (Test-Path $extraDir) {
        $extraFiles = @(Get-ChildItem -Path $extraDir -File -Recurse -Force)
        foreach ($f in $extraFiles) {
            $sources.Add([PSCustomObject]@{ Origin = "_extra"; File = $f })
        }
    } else {
        Write-Host "Aviso: no existe _extra para '$extraId' ($extraDir). Si el nombre de carpeta en _extra difiere, usa -ExtraSystemId."
    }
}

# Detectar colisiones por nombre de fichero, manteniendo la primera ocurrencia
$seen = @{}
$toCopy = New-Object System.Collections.Generic.List[object]
$collisions = New-Object System.Collections.Generic.List[string]

foreach ($entry in $sources) {
    $name = $entry.File.Name
    if ($seen.ContainsKey($name)) {
        $collisions.Add("$name -- omitido de '$($entry.Origin)', ya copiado desde '$($seen[$name])'")
        continue
    }
    $seen[$name] = $entry.Origin
    $toCopy.Add($entry)
}

# Resumen por origen
$byOrigin = $toCopy | Group-Object Origin | Sort-Object Name

Write-Host "Sistema: $SystemId"
Write-Host "Origen: $sourceSystemDir"
Write-Host "Destino: $destSystemDir"
Write-Host ""
Write-Host "Desglose por carpeta de origen:"
foreach ($g in $byOrigin) {
    Write-Host ("  {0}: {1}" -f $g.Name, $g.Count)
}
Write-Host ""
Write-Host "Total a copiar: $($toCopy.Count)"

Write-Host ""
Write-Host "Colisiones de nombre detectadas ($($collisions.Count)):"
if ($collisions.Count -gt 0) {
    foreach ($c in $collisions) { Write-Host "  - $c" }
} else {
    Write-Host "  (ninguna)"
}

if ($WhatIf) {
    Write-Host ""
    Write-Host "-WhatIf activo: no se ha copiado nada."
    return
}

if (-not (Test-Path $destSystemDir)) {
    New-Item -ItemType Directory -Path $destSystemDir -Force | Out-Null
}

foreach ($entry in $toCopy) {
    $destPath = Join-Path $destSystemDir $entry.File.Name
    Copy-Item -LiteralPath $entry.File.FullName -Destination $destPath -Force
}

Write-Host ""
Write-Host "Copia completada: $($toCopy.Count) ficheros en $destSystemDir"
