<#
Genera un JSON por sistema con los nombres base esperados de cada familia
de juego a partir de DAT XML Logiqx en convencion TOSEC (metadata/dat/TOSEC/).
Es la variante de build-dat-index-nointro.ps1 / build-dat-index-redump.ps1 para DAT
TOSEC, pensada sobre todo para microcomputadoras (ver docs/romsets.md).

Diferencias frente a build-dat-index-redump.ps1 (Redump, tambien sin
cloneofid):
- Convencion de nombre TOSEC: "Titulo (Fecha)(Publisher)(Region)[flags]",
  no "Titulo (Region) (Rev) (...)" de No-Intro. El primer grupo suele ser
  un anio o fecha, no la region.
- Region: codigos ISO de 2 letras (ES, FR, US...), no nombres completos
  (Spain, France...). Pueden ir en mayus o minuscula y combinarse con
  guion (ej. "US-EU").

Igual que las otras variantes: agrupacion de familia por NOMBRE BASE
EXACTO (sin cloneofid disponible), con fichero de alias manual fusionable
en metadata/dat-index/aliases/<id>.json.

Salida: mismo esquema que build-dat-index-nointro.ps1 / build-dat-index-redump.ps1
(metadata/dat-index/<id>.json, aliases/<id>.json, debug/<id>.json).

Uso:
    pwsh tools/scripts/build-dat-index-tosec.ps1
    pwsh tools/scripts/build-dat-index-tosec.ps1 -SystemId gx4000
#>

[CmdletBinding()]
param(
    [string]$SystemId,
    [string]$DatRoot,
    [string]$OutputRoot
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)

if (-not $DatRoot) { $DatRoot = Join-Path $repoRoot "metadata\dat" }
if (-not $OutputRoot) { $OutputRoot = Join-Path $repoRoot "metadata\dat-index" }
$AliasRoot = Join-Path $OutputRoot "aliases"
$DebugRoot = Join-Path $OutputRoot "debug"

# id -> @{ Source = "TOSEC"; Dat = "<nombre de fichero>.dat" }
$datMap = [ordered]@{
    "gx4000" = @{ Source = "TOSEC"; Dat = "Amstrad GX4000 - Games (TOSEC-v2025-01-15_CM).dat" }
}

# Codigos de region TOSEC (ISO 3166-1 alpha-2 + codigos propios de TOSEC
# como EU/US/JP habituales). Lista abierta: ampliar si aparecen nuevos
# codigos al procesar otros DAT TOSEC (microcomputadoras).
$knownRegionCodes = @(
    "AE", "AT", "AU", "BA", "BE", "BG", "BR", "CA", "CH", "CL", "CN",
    "CS", "CZ", "DE", "DK", "EE", "EG", "ES", "EU", "FI", "FR", "GB",
    "GR", "HK", "HR", "HU", "ID", "IE", "IL", "IN", "IR", "IS", "IT",
    "JO", "JP", "KR", "LT", "LU", "LV", "MN", "MX", "MY", "NL", "NO",
    "NP", "NZ", "OM", "PE", "PH", "PL", "PT", "QA", "RO", "RU", "SE",
    "SG", "SI", "SK", "TH", "TR", "TW", "US", "UK", "VN", "YU", "ZA",
    "WORLD"
)

function Get-ParenGroups {
    param([string]$Name)
    $matches = [regex]::Matches($Name, '\(([^()]*)\)')
    return @($matches | ForEach-Object { $_.Groups[1].Value })
}

function Get-Regions {
    param([string]$Name)
    foreach ($group in (Get-ParenGroups -Name $Name)) {
        $tokens = $group -split '[,+\-]' | ForEach-Object { $_.Trim().ToUpperInvariant() }
        $matched = @($tokens | Where-Object { $knownRegionCodes -contains $_ })
        if ($matched.Count -gt 0) { return $matched }
    }
    return @()
}

function Get-BaseName {
    param([string]$Name)
    $stripped = [regex]::Replace($Name, '\s*[\(\[][^\)\]]*[\)\]]', '')
    return $stripped.Trim()
}

# Tags que descartan la entrada por completo. Formato TOSEC: flags de
# calidad de dump entre corchetes ([a]lternate, [cr]acked, [f]ixed,
# [h]acked, [o]verdump, [p]irate, [t]rained, [!] verificado no aplica
# aqui) ademas de los habituales entre parentesis.
$discardTags = @(
    "Proto", "Demo", "Beta", "Sample", "Preview", "a", "cr", "f", "h",
    "o", "p", "t", "pirate", "trainer", "hack", "fixed", "cracked",
    "alternate", "overdump"
)
$flagTags = @("Aftermarket", "Compilation", "Unl", "Unlicensed", "Pirate", "Hack")

function Get-AllGroups {
    param([string]$Name)
    $matches = [regex]::Matches($Name, '[\(\[]([^\)\]]*)[\)\]]')
    return @($matches | ForEach-Object { $_.Groups[1].Value })
}

function Test-TagMatch {
    param([string]$Group, [string[]]$TagList)
    $normalized = ($Group -replace '\s+\d+$', '').Trim()
    return @($TagList | Where-Object { $_ -ieq $normalized }).Count -gt 0
}

function Get-DiscardReason {
    param([string]$Name, $Rom)
    $groups = Get-AllGroups -Name $Name
    $matched = @($groups | Where-Object { Test-TagMatch -Group $_ -TagList $discardTags })
    if ($matched.Count -gt 0) {
        return ($matched[0] -replace '\s+\d+$', '').Trim()
    }
    $roms = @($Rom)
    if (@($roms | Where-Object { $_.status -eq "baddump" }).Count -gt 0) {
        return "baddump"
    }
    return $null
}

function Get-Category {
    param([string]$Name)
    $groups = Get-AllGroups -Name $Name
    $matched = @($groups | Where-Object { Test-TagMatch -Group $_ -TagList $flagTags })
    if ($matched.Count -eq 0) { return "Oficial" }
    return ($matched[0] -replace '\s+\d+$', '').Trim()
}

function Write-JsonFile {
    param([string]$Path, $Data)
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $json = $Data | ConvertTo-Json -Depth 8
    $json = $json -replace '\\u0027', "'" -replace '\\u0026', '&' -replace '\\u003c', '<' -replace '\\u003e', '>'
    [System.IO.File]::WriteAllText($Path, $json, [System.Text.UTF8Encoding]::new($false))
}

function Build-SystemIndex {
    param([string]$Id, [hashtable]$Entry)

    $datPath = Join-Path $DatRoot "$($Entry.Source)\$($Entry.Dat)"
    if (-not (Test-Path $datPath)) {
        Write-Warning "DAT no encontrado para '$Id': $datPath"
        return
    }

    [xml]$xml = Get-Content -Raw -Path $datPath
    $games = $xml.datafile.game
    if (-not $games) {
        Write-Warning "Sin elementos <game> en '$Id': $datPath"
        return
    }

    $families = [ordered]@{}
    $discardedLog = New-Object System.Collections.Generic.List[object]
    $acceptedLog = New-Object System.Collections.Generic.List[string]

    foreach ($game in $games) {
        $fullName = $game.name
        if (-not $fullName) { continue }

        $reason = Get-DiscardReason -Name $fullName -Rom $game.rom
        if ($reason) {
            $discardedLog.Add([ordered]@{ name = $fullName; reason = $reason })
            continue
        }
        $acceptedLog.Add($fullName)

        $baseName = Get-BaseName -Name $fullName
        if (-not $baseName) { continue }

        $regions = Get-Regions -Name $fullName
        $category = Get-Category -Name $fullName

        if (-not $families.Contains($baseName)) {
            $families[$baseName] = @{
                CanonicalName = $baseName
                AliasNames    = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
                Regions       = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
                Categories    = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
            }
        }
        $family = $families[$baseName]
        foreach ($r in $regions) { [void]$family.Regions.Add($r) }
        [void]$family.Categories.Add($category)
    }

    $aliasPath = Join-Path $AliasRoot "$Id.json"
    $manualAliases = @()
    if (Test-Path $aliasPath) {
        $existing = Get-Content -Raw -Path $aliasPath | ConvertFrom-Json
        if ($existing.aliases) { $manualAliases = @($existing.aliases) }
    }

    $familyByCanonical = @{}
    foreach ($key in $families.Keys) { $familyByCanonical[$families[$key].CanonicalName] = $families[$key] }

    foreach ($manualEntry in $manualAliases) {
        $canonical = $manualEntry.canonical
        $aliasesToAdd = @($manualEntry.aliases)
        if (-not $familyByCanonical.ContainsKey($canonical)) {
            Write-Warning "Alias manual en '$Id' referencia un nombre canonico no encontrado en el DAT: '$canonical' (se ignora)"
            continue
        }
        $targetFamily = $familyByCanonical[$canonical]
        foreach ($aliasName in $aliasesToAdd) {
            if ($aliasName -eq $canonical) { continue }
            [void]$targetFamily.AliasNames.Add($aliasName)

            if ($familyByCanonical.ContainsKey($aliasName) -and $familyByCanonical[$aliasName] -ne $targetFamily) {
                $otherFamily = $familyByCanonical[$aliasName]
                foreach ($a in $otherFamily.AliasNames) { [void]$targetFamily.AliasNames.Add($a) }
                foreach ($r in $otherFamily.Regions) { [void]$targetFamily.Regions.Add($r) }
                foreach ($c in $otherFamily.Categories) { [void]$targetFamily.Categories.Add($c) }
                [void]$targetFamily.AliasNames.Add($aliasName)
                $familyByCanonical[$aliasName] = $targetFamily
                foreach ($key in @($families.Keys)) {
                    if ($families[$key] -eq $otherFamily) { $families.Remove($key) }
                }
            }
        }
    }

    $gamesOut = @($families.Values | Sort-Object { $_.CanonicalName } | ForEach-Object {
        $categories = @($_.Categories)
        $finalCategory = if ($categories -contains "Oficial") { "Oficial" } else { ($categories | Sort-Object) -join ", " }
        [ordered]@{
            name       = $_.CanonicalName
            aliases    = @($_.AliasNames | Sort-Object)
            regions    = @($_.Regions | Sort-Object)
            properties = [ordered]@{ category = $finalCategory }
        }
    })

    $output = [ordered]@{
        system    = $Id
        source    = $Entry.Source
        dat       = $Entry.Dat
        generated = (Get-Date -Format "yyyy-MM-dd")
        games     = @($gamesOut)
    }
    Write-JsonFile -Path (Join-Path $OutputRoot "$Id.json") -Data $output

    $aliasesOut = @($families.Values | Where-Object { $_.AliasNames.Count -gt 0 } | Sort-Object { $_.CanonicalName } | ForEach-Object {
        [ordered]@{
            canonical = $_.CanonicalName
            aliases   = @($_.AliasNames | Sort-Object)
        }
    })
    $aliasOutput = [ordered]@{
        system  = $Id
        aliases = @($aliasesOut)
    }
    Write-JsonFile -Path $aliasPath -Data $aliasOutput

    $debugOutput = [ordered]@{
        system    = $Id
        discarded = @($discardedLog | Sort-Object name)
        accepted  = @($acceptedLog | Sort-Object)
    }
    Write-JsonFile -Path (Join-Path $DebugRoot "$Id.json") -Data $debugOutput

    Write-Host "Generado: $Id.json ($($gamesOut.Count) familias, $($discardedLog.Count) descartados) + aliases/$Id.json ($($aliasesOut.Count) con alias) [TOSEC, agrupado por nombre base]"
}

$ids = if ($SystemId) { @($SystemId) } else { $datMap.Keys }

foreach ($id in $ids) {
    if (-not $datMap.Contains($id)) {
        Write-Warning "Sistema no mapeado: $id"
        continue
    }
    Build-SystemIndex -Id $id -Entry $datMap[$id]
}
