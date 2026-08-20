<#
Driver de lote: aplica convert-cloneofid-to-parent-clone.ps1 sobre full/ +
aftermarket/ de cada sistema del manifiesto tools/scripts/config/nointro-
systems.json, generando el DAT Parent-Clone de todos en
sources/dats/no-intro/fullset/ (entrada real de Retool) en una sola pasada.

Paso siguiente a update-sources.ps1 en el flujo real, no un sustituto: primero
update-sources.ps1 sincroniza sources/dats/no-intro/{pc,full,aftermarket}/
desde metadata/dat/No-Intro/, despues este script convierte full+aftermarket
al esquema Parent-Clone que Retool necesita. No toca pc/ (informativo, ver
convert-cloneofid-to-parent-clone.ps1) ni sources/dats/redump/ (sin
mecanismo de sincronizacion propio todavia).

Para cada sistema del manifiesto: localiza el full/ (obligatorio) y
aftermarket/ (opcional, se omite si no existe) mas recientes por timestamp,
y llama al conversor con ambos como entrada. El timestamp del nombre de
salida es el de full/ (no el de hoy), para que el fichero generado quede
trazable al DAT de origen real.

Uso:
    pwsh tools/scripts/generate-parent-clone-fullset.ps1
    pwsh tools/scripts/generate-parent-clone-fullset.ps1 -SystemId megadrive
#>

[CmdletBinding()]
param(
    [string]$SystemId
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)

$manifestPath = Join-Path $scriptDir "config\nointro-systems.json"
$manifestRaw = (Get-Content -Raw -Path $manifestPath | ConvertFrom-Json).systems
$manifest = [ordered]@{}
foreach ($prop in $manifestRaw.PSObject.Properties) { $manifest[$prop.Name] = $prop.Value }

$fullRoot = Join-Path $repoRoot "sources\dats\no-intro\full"
$aftermarketRoot = Join-Path $repoRoot "sources\dats\no-intro\aftermarket"
$outRoot = Join-Path $repoRoot "sources\dats\no-intro\fullset"
if (-not (Test-Path $outRoot)) { New-Item -ItemType Directory -Path $outRoot -Force | Out-Null }

$converter = Join-Path $scriptDir "convert-cloneofid-to-parent-clone.ps1"

$ids = if ($SystemId) { @($SystemId) } else { $manifest.Keys }

$results = New-Object System.Collections.Generic.List[pscustomobject]

foreach ($id in $ids) {
    if (-not $manifest.Contains($id)) {
        Write-Warning "Sistema no encontrado en el manifiesto: $id"
        continue
    }
    $baseName = $manifest[$id]
    $escaped = [regex]::Escape($baseName)

    $fullMatch = Get-ChildItem -Path $fullRoot -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match "^$escaped \(\d{8}-\d{6}\)\.dat$" } |
        Sort-Object Name -Descending | Select-Object -First 1
    $afterMatch = Get-ChildItem -Path $aftermarketRoot -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name -match "^$escaped \(Aftermarket\) \(\d{8}-\d{6}\)\.dat$" } |
        Sort-Object Name -Descending | Select-Object -First 1

    if (-not $fullMatch) {
        Write-Warning "$id : sin full/, saltado"
        $results.Add([pscustomobject]@{ Id = $id; Status = "sin full/" })
        continue
    }

    $inputs = @($fullMatch.FullName)
    if ($afterMatch) { $inputs += $afterMatch.FullName }

    if ($fullMatch.Name -match '\((\d{8}-\d{6})\)\.dat$') { $ts = $matches[1] } else { $ts = (Get-Date -Format "yyyyMMdd-HHmmss") }

    $outName = "$baseName (Parent-Clone) ($ts).dat"
    $outPath = Join-Path $outRoot $outName

    try {
        & $converter -InputDat $inputs -OutputDat $outPath -Name $baseName -Url "https://www.no-intro.org" | Out-Null
        $gameCount = (Select-String -Path $outPath -Pattern '<game ').Count
        Write-Host "OK  $id -> $outName ($gameCount games)"
        $results.Add([pscustomobject]@{ Id = $id; Status = "OK"; Games = $gameCount; Inputs = $inputs.Count })
    } catch {
        Write-Warning "$id : ERROR - $($_.Exception.Message)"
        $results.Add([pscustomobject]@{ Id = $id; Status = "ERROR: $($_.Exception.Message)" })
    }
}

Write-Host "`n=== RESUMEN ==="
$results | Format-Table -AutoSize | Out-String | Write-Host
