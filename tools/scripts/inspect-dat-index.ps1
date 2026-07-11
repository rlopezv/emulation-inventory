<#
Muestra un resumen de validacion de un JSON generado por
build-dat-index-nointro.ps1: total de familias, entradas sin region detectada,
distribucion de categorias y una muestra de familias con alias.

Uso:
    pwsh tools/scripts/inspect-dat-index.ps1 -SystemId nes
    pwsh tools/scripts/inspect-dat-index.ps1 -SystemId nes -AliasSampleSize 20
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SystemId,
    [string]$IndexRoot,
    [int]$AliasSampleSize = 15
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)
if (-not $IndexRoot) { $IndexRoot = Join-Path $repoRoot "metadata\dat-index" }

$path = Join-Path $IndexRoot "$SystemId.json"
if (-not (Test-Path $path)) {
    Write-Warning "No existe $path. Ejecuta antes build-dat-index-nointro.ps1 -SystemId $SystemId"
    return
}

$json = Get-Content -Raw -Path $path | ConvertFrom-Json
$games = @($json.games)

Write-Host "=== $($json.system) ($($json.source) / $($json.dat)) - generado $($json.generated) ===" -ForegroundColor Cyan
Write-Host ("Total familias: {0}" -f $games.Count)

$emptyRegions = @($games | Where-Object { $_.regions.Count -eq 0 })
Write-Host ("Sin region detectada: {0}" -f $emptyRegions.Count) -ForegroundColor $(if ($emptyRegions.Count -gt 0) { "Yellow" } else { "Green" })
foreach ($g in $emptyRegions) { Write-Host "  - $($g.name)" }

Write-Host "--- Distribucion de categorias ---"
$games | Group-Object { $_.properties.category } | Sort-Object Count -Descending | ForEach-Object {
    Write-Host ("  {0,-12} {1}" -f $_.Name, $_.Count)
}

$withAliases = @($games | Where-Object { $_.aliases.Count -gt 0 })
Write-Host ("--- Familias con alias: {0} (muestra de {1}) ---" -f $withAliases.Count, [Math]::Min($AliasSampleSize, $withAliases.Count))
$withAliases | Select-Object -First $AliasSampleSize | ForEach-Object {
    Write-Host ("  {0} (alias: {1})" -f $_.name, ($_.aliases -join " | "))
}
