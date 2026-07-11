<#
Limpia metadata/dat-index/<TargetSystemId>.json dejando solo las familias
que tienen al menos una entrada en el DAT original cuyo <game_id> empiece
por uno de los prefijos permitidos (esquema de Title ID de Nintendo
3DS/DSi: 00040000 = juego base, 00048004 = DSiWare, 0004008c = DLC,
0004000e = Update, 00040002 = Demo, resto = aplicaciones/modulos de
sistema).

No modifica build-dat-index-nointro.ps1 ni su salida general; es un paso de
limpieza adicional a re-ejecutar cada vez que se regenere el
TargetSystemId con build-dat-index-nointro.ps1. Complementa (no sustituye) a
filter-cross-system-duplicates.ps1.

Uso:
    pwsh tools/scripts/filter-by-title-type.ps1 -TargetSystemId 3dseshop -Source No-Intro -Dat "Nintendo - Nintendo 3DS (Digital) (CDN) (20260306-063611).dat"
    pwsh tools/scripts/filter-by-title-type.ps1 -TargetSystemId 3dseshop -Source No-Intro -Dat "..." -AllowedPrefixes 00040000
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TargetSystemId,
    [Parameter(Mandatory = $true)]
    [string]$Source,
    [Parameter(Mandatory = $true)]
    [string]$Dat,
    [string[]]$AllowedPrefixes = @("00040000", "00048004"),
    [string]$DatRoot,
    [string]$IndexRoot
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)
if (-not $DatRoot) { $DatRoot = Join-Path $repoRoot "metadata\dat" }
if (-not $IndexRoot) { $IndexRoot = Join-Path $repoRoot "metadata\dat-index" }
$DebugRoot = Join-Path $IndexRoot "debug"

$datPath = Join-Path $DatRoot "$Source\$Dat"
$targetPath = Join-Path $IndexRoot "$TargetSystemId.json"

if (-not (Test-Path $datPath)) { Write-Warning "DAT no encontrado: $datPath"; return }
if (-not (Test-Path $targetPath)) { Write-Warning "No existe $targetPath"; return }

function Get-BaseName {
    param([string]$Name)
    $stripped = [regex]::Replace($Name, '\s*[\(\[][^\)\]]*[\)\]]', '')
    return $stripped.Trim()
}

[xml]$xml = Get-Content -Raw -Path $datPath
$games = $xml.datafile.game

# Nombres base que tienen al menos una entrada con game_id de tipo permitido.
$allowedBaseNames = New-Object System.Collections.Generic.HashSet[string]
foreach ($g in $games) {
    if (-not $g.name -or -not $g.game_id) { continue }
    $prefix = $g.game_id.Substring(0, 8)
    if ($AllowedPrefixes -ccontains $prefix) {
        [void]$allowedBaseNames.Add((Get-BaseName -Name $g.name))
    }
}

$targetJson = Get-Content -Raw -Path $targetPath | ConvertFrom-Json

$kept = New-Object System.Collections.Generic.List[object]
$removed = New-Object System.Collections.Generic.List[object]

foreach ($entry in $targetJson.games) {
    $allNames = @($entry.name) + @($entry.aliases)
    $isAllowed = @($allNames | Where-Object { $allowedBaseNames.Contains($_) }).Count -gt 0
    if ($isAllowed) {
        $kept.Add($entry)
    } else {
        $removed.Add([ordered]@{ name = $entry.name })
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
    system           = $TargetSystemId
    allowedPrefixes  = @($AllowedPrefixes)
    removed          = @($removed.ToArray() | Sort-Object name)
}
Write-JsonFileNoBom -Path (Join-Path $DebugRoot "$TargetSystemId-filtered-by-title-type.json") -Data $debugOutput

Write-Host "Filtrado $TargetSystemId.json por game_id ($($AllowedPrefixes -join ',')): $($kept.Count) conservados, $($removed.Count) eliminados"
