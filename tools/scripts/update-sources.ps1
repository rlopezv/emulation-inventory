<#
Sincroniza sources/dats/no-intro/{pc,full,aftermarket}/ (copia de trabajo,
lo que leen los scripts de indexado) a partir de las descargas crudas en
metadata/dat/No-Intro/{pc,full,aftermarket}/ (archivo completo tal cual se
baja), usando el manifiesto de sistemas realmente usados en
tools/scripts/config/nointro-systems.json.

Para cada sistema del manifiesto y cada pack disponible, busca en
metadata/dat/No-Intro/<pack>/ el fichero cuyo nombre coincide con el
patron "<BaseName> [(Tag)] (<timestamp>).dat" (Tag solo aplica a
pc="Parent-Clone" y aftermarket="Aftermarket"; full no lleva tag). Si hay
varias coincidencias (packs regenerados), usa la de timestamp mas
reciente. El pack no es obligatorio: si un sistema no tiene variante
aftermarket, simplemente no se copia nada para ese pack.

Al finalizar, informa:
- sistemas del manifiesto sin ningun pack encontrado en metadata/ (posible
  descarga pendiente)
- ficheros en sources/dats/no-intro/ que ya no corresponden a ningun
  sistema del manifiesto (candidatos a limpiar a mano; no se borran solos)

Uso:
    pwsh tools/scripts/update-sources.ps1
    pwsh tools/scripts/update-sources.ps1 -SystemId nes
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

$rawRoot = Join-Path $repoRoot "metadata\dat\No-Intro"
$destRoot = Join-Path $repoRoot "sources\dats\no-intro"

# pack -> tag insertado en el nombre de fichero (o $null si no lleva tag)
$packs = [ordered]@{
    pc          = "Parent-Clone"
    full        = $null
    aftermarket = "Aftermarket"
}

function Get-DatPattern {
    param([string]$BaseName, [string]$Tag)
    $escapedBase = [regex]::Escape($BaseName)
    if ($Tag) {
        return "^$escapedBase \($([regex]::Escape($Tag))\) \(\d{8}-\d{6}\)\.dat$"
    }
    return "^$escapedBase \(\d{8}-\d{6}\)\.dat$"
}

function Find-LatestMatch {
    param([string]$Folder, [string]$Pattern)
    if (-not (Test-Path $Folder)) { return $null }
    $candidates = Get-ChildItem -Path $Folder -File | Where-Object { $_.Name -match $Pattern }
    if ($candidates.Count -eq 0) { return $null }
    return ($candidates | Sort-Object Name -Descending | Select-Object -First 1)
}

$ids = if ($SystemId) { @($SystemId) } else { $manifest.Keys }

$missing = New-Object System.Collections.Generic.List[string]
$copiedCount = 0

foreach ($id in $ids) {
    if (-not $manifest.Contains($id)) {
        Write-Warning "Sistema no encontrado en el manifiesto: $id"
        continue
    }
    $baseName = $manifest[$id]
    $foundAny = $false

    foreach ($packName in $packs.Keys) {
        $tag = $packs[$packName]
        $pattern = Get-DatPattern -BaseName $baseName -Tag $tag
        $srcFolder = Join-Path $rawRoot $packName
        $match = Find-LatestMatch -Folder $srcFolder -Pattern $pattern
        if (-not $match) { continue }

        $foundAny = $true
        $destFolder = Join-Path $destRoot $packName
        if (-not (Test-Path $destFolder)) { New-Item -ItemType Directory -Path $destFolder -Force | Out-Null }
        $destPath = Join-Path $destFolder $match.Name

        # Elimina versiones anteriores del mismo sistema/pack antes de copiar la nueva
        Get-ChildItem -Path $destFolder -File -ErrorAction SilentlyContinue |
            Where-Object { $_.Name -match $pattern -and $_.Name -ne $match.Name } |
            Remove-Item -Force

        if (-not (Test-Path $destPath)) {
            Copy-Item -Path $match.FullName -Destination $destPath
            $copiedCount++
            Write-Host "Copiado [$packName]: $($match.Name)"
        }
    }

    if (-not $foundAny) { $missing.Add($id) }
}

if ($missing.Count -gt 0) {
    Write-Warning "Sistemas del manifiesto sin ningun DAT encontrado en metadata/dat/No-Intro/: $($missing -join ', ')"
}

# Ficheros huerfanos en sources/: ya no corresponden a ningun sistema del manifiesto
$expectedBaseNames = @($manifest.Values)
foreach ($packName in $packs.Keys) {
    $destFolder = Join-Path $destRoot $packName
    if (-not (Test-Path $destFolder)) { continue }
    $tag = $packs[$packName]
    Get-ChildItem -Path $destFolder -File | ForEach-Object {
        $suffixPattern = if ($tag) { " \($([regex]::Escape($tag))\) \(\d{8}-\d{6}\)\.dat$" } else { " \(\d{8}-\d{6}\)\.dat$" }
        $strippedBase = $_.Name -replace $suffixPattern, ""
        if ($expectedBaseNames -notcontains $strippedBase) {
            Write-Warning "Huerfano en sources/ [$packName]: $($_.Name) (ya no esta en el manifiesto)"
        }
    }
}

Write-Host "Sincronizacion completa. $copiedCount fichero(s) nuevo(s) copiado(s)."
