<#
Limpia metadata/dat-index/<TargetSystemId>.json eliminando las familias
que ya estan cubiertas por otro sistema (metadata/dat-index/<BaseSystemId>.json),
comparando por nombre canonico o cualquiera de sus alias.

Caso de uso: 3dseshop parte de un DAT (Digital) (CDN) que incluye tanto
exclusivos de eShop como juegos que tambien tuvieron cartucho fisico
(ya cubiertos por 3ds.json). Este script deja 3dseshop.json solo con
los titulos realmente exclusivos.

No modifica build-dat-index-nointro.ps1 (que sigue generando el indice general
sin filtrar); este es un paso de limpieza posterior, a re-ejecutar cada
vez que se regenere el TargetSystemId con build-dat-index-nointro.ps1.

Uso:
    pwsh tools/scripts/filter-cross-system-duplicates.ps1 -BaseSystemId 3ds -TargetSystemId 3dseshop
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$BaseSystemId,
    [Parameter(Mandatory = $true)]
    [string]$TargetSystemId,
    [string]$IndexRoot
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)
if (-not $IndexRoot) { $IndexRoot = Join-Path $repoRoot "metadata\dat-index" }
$DebugRoot = Join-Path $IndexRoot "debug"

$basePath = Join-Path $IndexRoot "$BaseSystemId.json"
$targetPath = Join-Path $IndexRoot "$TargetSystemId.json"

if (-not (Test-Path $basePath)) { Write-Warning "No existe $basePath"; return }
if (-not (Test-Path $targetPath)) { Write-Warning "No existe $targetPath"; return }

$baseJson = Get-Content -Raw -Path $basePath | ConvertFrom-Json
$targetJson = Get-Content -Raw -Path $targetPath | ConvertFrom-Json

# Set de todos los nombres (canonico + alias) del sistema base.
$baseNames = New-Object System.Collections.Generic.HashSet[string]
foreach ($g in $baseJson.games) {
    [void]$baseNames.Add($g.name)
    foreach ($a in $g.aliases) { [void]$baseNames.Add($a) }
}

$kept = New-Object System.Collections.Generic.List[object]
$removed = New-Object System.Collections.Generic.List[object]

foreach ($g in $targetJson.games) {
    $allNames = @($g.name) + @($g.aliases)
    $match = @($allNames | Where-Object { $baseNames.Contains($_) })
    if ($match.Count -gt 0) {
        $removed.Add([ordered]@{ name = $g.name; matchedAs = $match[0] })
    } else {
        $kept.Add($g)
    }
}

$targetOutput = [ordered]@{
    system    = $targetJson.system
    source    = $targetJson.source
    dat       = $targetJson.dat
    generated = $targetJson.generated
    games     = $kept.ToArray()
}

function Write-JsonFileNoBom {
    param([string]$Path, $Data)
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $json = $Data | ConvertTo-Json -Depth 8
    $json = $json -replace '\\u0027', "'" -replace '\\u0026', '&' -replace '\\u003c', '<' -replace '\\u003e', '>'
    [System.IO.File]::WriteAllText($Path, $json, [System.Text.UTF8Encoding]::new($false))
}

Write-JsonFileNoBom -Path $targetPath -Data $targetOutput

$debugOutput = [ordered]@{
    system  = $TargetSystemId
    filteredAgainst = $BaseSystemId
    removed = @($removed | Sort-Object name)
}
Write-JsonFileNoBom -Path (Join-Path $DebugRoot "$TargetSystemId-filtered-by-$BaseSystemId.json") -Data $debugOutput

Write-Host "Filtrado $TargetSystemId.json contra $BaseSystemId.json: $($kept.Count) conservados, $($removed.Count) eliminados (ya cubiertos por $BaseSystemId)"
