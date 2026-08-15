<#
Genera un JSON por sistema con los nombres base esperados de cada familia
de juego (1G1R) a partir de DAT XML Logiqx SIN atributos id/cloneofid
(Redump). Es la variante de build-dat-index-nointro.ps1 para fuentes donde no se
puede resolver relacion parent/clone automaticamente (ver
docs/romsets.md#formato-de-dat).

Agrupacion de familia, en orden de prioridad:
1. Clonelist (metadata/dat/retool/clonelists/<Nombre> (Redump).json, formato
   retool/unexpectedpanda): si el nombre base de la entrada coincide con un
   "searchTerm" de un "variant", la familia usa el "group" de ese variant
   como nombre canonico. Esto agrupa tanto variantes regionales del mismo
   titulo como titulos distintos por region (equivalente a Rockman/Mega
   Man pero en catalogo optico), sin depender de cloneofid.
2. Nombre base exacto (fallback): si no hay clonelist para el sistema, o
   el nombre base no aparece en ningun searchTerm, la familia es el propio
   nombre base (comportamiento anterior).

El fichero metadata/dat-index/aliases/<id>.json sigue existiendo como capa
manual adicional, para corregir/completar casos que el clonelist no cubra.

Mismos criterios de descarte, deteccion de region y categoria que
build-dat-index-nointro.ps1 (duplicados aqui para no acoplar ambos scripts).

Salida: metadata/dat-index/<id>.json, metadata/dat-index/aliases/<id>.json,
metadata/dat-index/debug/<id>.json (mismo esquema que build-dat-index-nointro.ps1,
compatible con inspect-dat-index.ps1 y los scripts de filtrado).

Uso:
    pwsh tools/scripts/build-dat-index-redump.ps1
    pwsh tools/scripts/build-dat-index-redump.ps1 -SystemId psx
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
$ClonelistRoot = Join-Path $DatRoot "retool\clonelists"

# Exclusiones GLOBALES: patrones de revista/cheats/demo que se repiten
# entre varios sistemas Redump (van pegados al titulo, no como tag entre
# parentesis, por lo que el descarte por tag no los detecta). Se combinan
# con las exclusiones especificas de cada sistema via Join-TitleExclusions.
$GlobalTitleExclusions = @(
    '\bDemo\b', 'Not for Sale', 'Non-Sell', 'Action Replay', 'GameShark',
    'CodeBreaker', 'Xploder', 'Famitsu', '\bPreview\b', '\bPromotion\b',
    '\bKiosk\b', '\bTrial\b', '\bSample\b', '\bBeta\b'
)

function Join-TitleExclusions {
    param([string[]]$Specific)
    return (@($GlobalTitleExclusions) + @($Specific)) -join '|'
}

# Exclusiones especificas de PSX: series retail que requieren periferico
# especifico para jugarse (ej. Kids Station), y marcas de revista/cheats
# propias de PSX (ver $GlobalTitleExclusions para las comunes).
$PSXSpecificExclusions = Join-TitleExclusions @(
    'Interactive CD Sampler', 'PlayStation Underground', 'Jampack',
    'Official.*PlayStation Magazine', 'PSi\d?', 'OPSM', 'GSi', 'M6 PlayStation',
    'Planet PSX', 'Pocket PowerStation', 'PlayStation Zone', 'PlayMag', 'Joypad Demo',
    'Screen Attack', 'Gratis! Demo Disc', 'Taikenban', '体験版', '店頭体験版',
    'Plus Yuu', 'Import Player', 'PS-X-Change',
    'Equalizer Game Wizard', 'Power Play for PlayStation', 'Gamebuster',
    'HMV CodeBuster', 'GT Circuit Breaker', 'Best Cheats in the World',
    'Hackerz', 'EQ One', 'Dance-UK', 'Official UK PlayStation Best Games Ever',
    'Kids Station', 'Tech PlayStation', 'Dengeki PlayStation',
    'Memory Card Data Base', 'Interactive Drive', 'Lawson Special'
)

# Exclusiones especificas de Amiga CD32: marcas de revista/coverdisc
# propias de este sistema.
$AmigaCD32SpecificExclusions = Join-TitleExclusions @(
    'CD32 Gamer', 'Amiga CD32 Gamer', 'CD Exchange', 'Amiga CD32 Magazine'
)

# Exclusiones especificas de Xbox: marcas de revista/coverdisc propias.
$XboxSpecificExclusions = Join-TitleExclusions @(
    'Official Xbox Magazine', 'Official Xbox Best Ever Games',
    'Official Xbox Starter Pack', 'Official Xbox 50 Best Games',
    'Official Xbox Live Disc', 'Best Xbox.*Game Disc',
    'Xbox Playable Starter Pack', 'Dance-UK'
)

# Resto de sistemas Redump: solo exclusiones globales (sin marcas
# especificas identificadas todavia). Ampliar si se detectan casos.
$DefaultTitleExclusions = Join-TitleExclusions @()

# id -> @{ Source = "Redump"; Dat = "<nombre de fichero>.dat"; Clonelist = "<nombre en metadata/dat/retool/clonelists/>.json" (opcional); TitleExclusions = "<regex>" (opcional) }
$datMap = [ordered]@{
    "gamecube"   = @{ Source = "Redump"; Dat = "Nintendo - GameCube - Datfile (2019) (2026-06-13 18-14-01).dat"; Clonelist = "Nintendo - GameCube (Redump).json"; TitleExclusions = $DefaultTitleExclusions }
    "wii"        = @{ Source = "Redump"; Dat = "Nintendo - Wii - Datfile (3780) (2026-06-15 03-13-28).dat"; Clonelist = "Nintendo - Wii (Redump).json"; TitleExclusions = $DefaultTitleExclusions }
    "segacd"     = @{ Source = "Redump"; Dat = "Sega - Mega CD & Sega CD - Datfile (549) (2026-05-28 18-06-58).dat"; Clonelist = "Sega - Mega CD & Sega CD (Redump).json"; TitleExclusions = $DefaultTitleExclusions }
    "saturn"     = @{ Source = "Redump"; Dat = "Sega - Saturn - Datfile (2457) (2026-06-14 12-36-08).dat"; Clonelist = "Sega - Saturn (Redump).json"; TitleExclusions = $DefaultTitleExclusions }
    "dreamcast"  = @{ Source = "Redump"; Dat = "Sega - Dreamcast - Datfile (1516) (2026-06-14 18-25-41).dat"; Clonelist = "Sega - Dreamcast (Redump).json"; TitleExclusions = $DefaultTitleExclusions }
    "psx"        = @{ Source = "Redump"; Dat = "Sony - PlayStation - Datfile (10914) (2026-06-15 11-55-46).dat"; Clonelist = "Sony - PlayStation (Redump).json"; TitleExclusions = $PSXSpecificExclusions }
    "ps2"        = @{ Source = "Redump"; Dat = "Sony - PlayStation 2 - Datfile (11774) (2026-06-15 03-41-38).dat"; Clonelist = "Sony - PlayStation 2 (Redump).json"; TitleExclusions = $DefaultTitleExclusions }
    "jaguarcd"   = @{ Source = "Redump"; Dat = "Atari - Jaguar CD Interactive Multimedia System - Datfile (38) (2026-04-03 15-50-49).dat"; TitleExclusions = $DefaultTitleExclusions }
    "pcenginecd" = @{ Source = "Redump"; Dat = "NEC - PC Engine CD & TurboGrafx CD - Datfile (551) (2026-06-14 14-24-19).dat"; Clonelist = "NEC - PC Engine CD & TurboGrafx CD (Redump).json"; TitleExclusions = $DefaultTitleExclusions }
    "3do"        = @{ Source = "Redump"; Dat = "Panasonic - 3DO Interactive Multiplayer - Datfile (672) (2026-06-09 14-48-47).dat"; Clonelist = "Panasonic - 3DO Interactive Multiplayer (Redump).json"; TitleExclusions = $DefaultTitleExclusions }
    "amigacdtv"  = @{ Source = "Redump"; Dat = "Commodore - Amiga CDTV - Datfile (61) (2026-05-16 20-58-08).dat"; Clonelist = "Commodore - Amiga CD (Redump).json"; TitleExclusions = $DefaultTitleExclusions }
    "amigacd32"  = @{ Source = "Redump"; Dat = "Commodore - Amiga CD32 - Datfile (207) (2026-05-08 20-54-04).dat"; Clonelist = "Commodore - Amiga CD32 (Redump).json"; TitleExclusions = $AmigaCD32SpecificExclusions }
    "xbox"       = @{ Source = "Redump"; Dat = "Microsoft - Xbox - Datfile (2683) (2026-06-14 23-43-27).dat"; Clonelist = "Microsoft - Xbox (Redump).json"; TitleExclusions = $XboxSpecificExclusions }
    "neogeocd"   = @{ Source = "Redump"; Dat = "SNK - Neo Geo CD - Datfile (111) (2026-05-06 12-21-03).dat"; TitleExclusions = $DefaultTitleExclusions }
}

# Tokens de region reconocidos por la convencion No-Intro/Redump (lista cerrada).
$knownRegions = @(
    "Argentina", "Asia", "Australia", "Austria", "Bangladesh", "Belgium",
    "Brazil", "Bulgaria", "Canada", "Chile", "China", "Colombia", "Croatia",
    "Czechia", "Denmark", "Egypt", "Europe", "Finland", "France", "Germany",
    "Greece", "Hong Kong", "Hungary", "India", "Indonesia", "Iran", "Iraq",
    "Ireland", "Israel", "Italy", "Japan", "Korea", "Latin America",
    "Mexico", "Netherlands", "New Zealand", "Norway", "Peru", "Poland",
    "Portugal", "Romania", "Russia", "Saudi Arabia", "Scandinavia",
    "Slovakia", "South Africa", "Spain", "Sweden", "Switzerland", "Taiwan",
    "Turkey", "UAE", "United Kingdom", "USA", "Vietnam", "World", "Unknown"
)

function Get-ParenGroups {
    param([string]$Name)
    $matches = [regex]::Matches($Name, '\(([^()]*)\)')
    return @($matches | ForEach-Object { $_.Groups[1].Value })
}

function Get-Regions {
    param([string]$Name)
    foreach ($group in (Get-ParenGroups -Name $Name)) {
        $tokens = $group -split '[,+]' | ForEach-Object { $_.Trim() }
        $matched = @($tokens | Where-Object { $knownRegions -ccontains $_ })
        if ($matched.Count -gt 0) { return $matched }
    }
    return @()
}

function Get-BaseName {
    param([string]$Name)
    $stripped = [regex]::Replace($Name, '\s*[\(\[][^\)\]]*[\)\]]', '')
    return $stripped.Trim()
}

$discardTags = @(
    "Proto", "Demo", "Special Demo", "Trial", "Beta", "Sample", "Kiosk",
    "Test Program", "Program", "BIOS", "DLC", "Update", "System Application",
    "System Module", "E3 Video", "Nintendo 3DS Conference", "Shared Data Archive"
)
$flagTags = @("Aftermarket", "Compilation", "Unl", "Pirate")

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
    param([string]$Name, $Rom, [string]$TitleExclusionRegex)
    $groups = Get-AllGroups -Name $Name
    $matched = @($groups | Where-Object { Test-TagMatch -Group $_ -TagList $discardTags })
    if ($matched.Count -gt 0) {
        return ($matched[0] -replace '\s+\d+$', '').Trim()
    }
    if ($TitleExclusionRegex -and [regex]::IsMatch($Name, $TitleExclusionRegex)) {
        return "revista/cheats"
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

function Get-ClonelistMap {
    # searchTerm (nombre base tal como aparece en el DAT) -> group (nombre canonico curado)
    param([string]$Path)
    $map = @{}
    if (-not $Path -or -not (Test-Path $Path)) { return $map }
    $json = Get-Content -Raw -Path $Path | ConvertFrom-Json
    foreach ($variant in $json.variants) {
        $group = $variant.group
        foreach ($title in $variant.titles) {
            if ($title.searchTerm) { $map[$title.searchTerm] = $group }
        }
    }
    return $map
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

    $clonelistPath = if ($Entry.Clonelist) { Join-Path $ClonelistRoot $Entry.Clonelist } else { $null }
    $clonelistMap = Get-ClonelistMap -Path $clonelistPath
    $clonelistHits = 0

    # Agrupacion: clonelist (nombre base -> group curado) con fallback a
    # nombre base exacto cuando no hay clonelist o no cubre la entrada.
    $families = [ordered]@{}  # canonicalKey -> { CanonicalName, AliasNames(set), Regions(set), Categories(set) }
    $discardedLog = New-Object System.Collections.Generic.List[object]
    $acceptedLog = New-Object System.Collections.Generic.List[string]

    foreach ($game in $games) {
        $fullName = $game.name
        if (-not $fullName) { continue }

        $reason = Get-DiscardReason -Name $fullName -Rom $game.rom -TitleExclusionRegex $Entry.TitleExclusions
        if ($reason) {
            $discardedLog.Add([ordered]@{ name = $fullName; reason = $reason })
            continue
        }
        $acceptedLog.Add($fullName)

        $baseName = Get-BaseName -Name $fullName
        if (-not $baseName) { continue }

        $regions = Get-Regions -Name $fullName
        $category = Get-Category -Name $fullName

        $canonicalKey = $baseName
        if ($clonelistMap.ContainsKey($baseName)) {
            $canonicalKey = $clonelistMap[$baseName]
            $clonelistHits++
        }

        if (-not $families.Contains($canonicalKey)) {
            $families[$canonicalKey] = @{
                CanonicalName = $canonicalKey
                AliasNames    = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
                Regions       = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
                Categories    = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
            }
        }
        $family = $families[$canonicalKey]
        if ($baseName -ne $family.CanonicalName) { [void]$family.AliasNames.Add($baseName) }
        foreach ($r in $regions) { [void]$family.Regions.Add($r) }
        [void]$family.Categories.Add($category)
    }

    # Fichero de alias manual: fusion igual que build-dat-index-nointro.ps1, para
    # anadir a mano equivalencias de titulo que el DAT no puede vincular.
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

    $clonelistNote = if ($clonelistPath) {
        $coverage = if ($acceptedLog.Count -gt 0) { [Math]::Round(100 * $clonelistHits / $acceptedLog.Count, 1) } else { 0 }
        "clonelist: $clonelistHits/$($acceptedLog.Count) aceptados ($coverage%)"
    } else {
        "sin clonelist"
    }
    Write-Host "Generado: $Id.json ($($gamesOut.Count) familias, $($discardedLog.Count) descartados) + aliases/$Id.json ($($aliasesOut.Count) con alias) [$clonelistNote]"
}

$ids = if ($SystemId) { @($SystemId) } else { $datMap.Keys }

foreach ($id in $ids) {
    if (-not $datMap.Contains($id)) {
        Write-Warning "Sistema no mapeado: $id"
        continue
    }
    Build-SystemIndex -Id $id -Entry $datMap[$id]
}
