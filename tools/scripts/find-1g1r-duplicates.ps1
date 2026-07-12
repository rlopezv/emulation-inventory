<#
Busca posibles duplicados dentro de cada metadata/dat-index/<id>.json generado
por build-dat-index-1g1r.ps1: mismo nombre base (name) apareciendo mas de una
vez en games[]. En un set 1G1R correcto cada nombre deberia aparecer una sola
vez; si aparece repetido, normalmente es porque el DAT original traia dos
entradas distintas (ej. distinta region o distinta Rev) que retool no fusiono
en una sola familia.

Solo lee metadata/dat-index/<id>.json, no vuelve a tocar los DAT en crudo.

Uso:
    pwsh tools/scripts/find-1g1r-duplicates.ps1
    pwsh tools/scripts/find-1g1r-duplicates.ps1 -SystemId nes
#>

[CmdletBinding()]
param(
    [string]$SystemId,
    [string]$IndexRoot
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)

if (-not $IndexRoot) { $IndexRoot = Join-Path $repoRoot "metadata\dat-index" }

# Solo los sistemas generados por build-dat-index-1g1r.ps1 (source = "1G1R (retool)").
$files = if ($SystemId) {
    @(Get-Item (Join-Path $IndexRoot "$SystemId.json") -ErrorAction SilentlyContinue)
} else {
    @(Get-ChildItem -Path $IndexRoot -Filter "*.json" -File)
}

$totalDuplicates = 0

foreach ($file in $files) {
    if (-not $file) { continue }
    $json = Get-Content -Raw -Path $file.FullName | ConvertFrom-Json
    if ($json.source -ne "1G1R (retool)") { continue }

    $groups = $json.games | Group-Object -Property name | Where-Object { $_.Count -gt 1 }
    if ($groups.Count -eq 0) { continue }

    Write-Host "=== $($json.system) ($($groups.Count) nombres duplicados) ==="
    foreach ($g in $groups) {
        Write-Host "  $($g.Name):"
        foreach ($entry in $g.Group) {
            $regions = ($entry.regions -join ', ')
            Write-Host "    - regiones: [$regions] categoria: $($entry.properties.category)"
        }
    }
    $totalDuplicates += $groups.Count
    Write-Host ""
}

Write-Host "Total nombres duplicados encontrados: $totalDuplicates"
