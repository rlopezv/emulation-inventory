<#
Genera metadata/dat-index/<id>.json a partir de los DAT ya curados 1G1R en
data/dats/console/1g1r/, generados externamente con retool.

A diferencia de build-dat-index-nointro.ps1 / -redump.ps1 / -tosec.ps1, estos
DAT NO tienen atributo cloneofid: retool ya resolvio la seleccion 1G1R, asi
que cada <game> del DAT es ya una familia final, no hace falta agrupar por
parent/clone ni por clonelist. El script solo extrae nombre, region y
categoria por entrada.

Se aplica igualmente el filtro de descarte (Proto/Demo/Beta/etc.) como red de
seguridad, aunque el set 1G1R de retool ya deberia venir limpio de esos casos.

No toca los sistemas que aun no tienen fichero en data/dats/console/1g1r/
(su metadata/dat-index/<id>.json existente, generado por otro script, se
deja intacto).

Salida: metadata/dat-index/<id>.json (mismo esquema que el resto de scripts
build-dat-index-*.ps1, para que generate-romset-docs.ps1 siga funcionando
sin cambios). No genera metadata/dat-index/aliases/<id>.json (no hay nada
que fusionar, cada entrada ya es su propia familia).

Uso:
    pwsh tools/scripts/build-dat-index-1g1r.ps1
    pwsh tools/scripts/build-dat-index-1g1r.ps1 -SystemId gb
#>

[CmdletBinding()]
param(
    [string]$SystemId,
    [string]$DatRoot,
    [string]$OutputRoot
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)

if (-not $DatRoot) { $DatRoot = Join-Path $repoRoot "data\dats\console\1g1r" }
if (-not $OutputRoot) { $OutputRoot = Join-Path $repoRoot "metadata\dat-index" }
$DebugRoot = Join-Path $OutputRoot "debug"

# id -> nombre de fichero dentro de data/dats/console/1g1r/
$datMap = [ordered]@{
    "nes"           = "Nintendo - Nintendo Entertainment System (Headered) (20260504-103615).dat"
    "fds"           = "Nintendo - Family Computer Disk System (FDS) (20260317-004812).dat"
    "satellaview"   = "Nintendo - Satellaview (20260322-134432).dat"
    "sufami"        = "Nintendo - Sufami Turbo (20240622-035607).dat"
    "snes"          = "Nintendo - Super Nintendo Entertainment System (20260505-202641).dat"
    "gb"            = "Nintendo - Game Boy (20260501-055403).dat"
    "gbc"           = "Nintendo - Game Boy Color (20260505-192202).dat"
    "gba"           = "Nintendo - Game Boy Advance (20260503-202332).dat"
    "virtualboy"    = "Nintendo - Virtual Boy (20260428-015207).dat"
    "n64"           = "Nintendo - Nintendo 64 (BigEndian) (20260505-135821).dat"
    "pokemini"      = "Nintendo - Pokemon Mini (20250407-153358).dat"
    "nds"           = "Nintendo - Nintendo DS (Decrypted) (20260504-004312).dat"
    "dsiware"       = "Nintendo - Nintendo DSi (Digital) (CDN) (Decrypted) (20260228-234052).dat"
    "3ds"           = "Nintendo - Nintendo 3DS (Decrypted) (20260505-085920).dat"
    "3dseshop"      = "Nintendo - Nintendo 3DS (Digital) (CDN) (20260306-063611).dat"
    "newn3ds"       = "Nintendo - New Nintendo 3DS (Decrypted) (20251121-060655).dat"
    "sg1000"        = "Sega - SG-1000 - SC-3000 (20231205-110448).dat"
    "mastersystem"  = "Sega - Master System - Mark III (20260428-025956).dat"
    "megadrive"     = "Sega - Mega Drive - Genesis (20260504-203329).dat"
    "sega32x"       = "Sega - 32X (20260317-140429).dat"
    "gamegear"      = "Sega - Game Gear (20260422-014958).dat"
    "lynx"          = "Atari - Atari Lynx (LYX) (20251222-090626).dat"
    "jaguar"        = "Atari - Atari Jaguar (J64) (20250208-164242).dat"
    "pcengine"      = "NEC - PC Engine - TurboGrafx-16 (20260124-120557).dat"
    "ngp"           = "SNK - NeoGeo Pocket (20250904-215533).dat"
    "ngpc"          = "SNK - NeoGeo Pocket Color (20240506-123728).dat"
    "wswan"         = "Bandai - WonderSwan (20260124-123054).dat"
    "wswanc"        = "Bandai - WonderSwan Color (20260415-165647).dat"
    "supervision"   = "Watara - Supervision (20250625-093232).dat"
    "gamecube"      = "Nintendo - GameCube (2026-06-13 18-14-01).dat"
    "wii"           = "Nintendo - Wii (2026-06-15 03-13-28).dat"
    "segacd"        = "Sega - Mega CD & Sega CD (2026-05-28 18-06-58).dat"
    "saturn"        = "Sega - Saturn (2026-06-14 12-36-08).dat"
    "dreamcast"     = "Sega - Dreamcast (2026-06-14 18-25-41).dat"
    "psx"           = "Sony - PlayStation (2026-06-15 11-55-46).dat"
    "ps2"           = "Sony - PlayStation 2 (2026-06-15 03-41-38).dat"
    "jaguarcd"      = "Atari - Jaguar CD Interactive Multimedia System (2026-04-03 15-50-49).dat"
    "pcenginecd"    = "NEC - PC Engine CD & TurboGrafx CD (2026-06-14 14-24-19).dat"
    "3do"           = "Panasonic - 3DO Interactive Multiplayer (2026-06-09 14-48-47).dat"
    "neogeocd"      = "SNK - Neo Geo CD (2026-05-06 12-21-03).dat"
    "cdi"           = "Philips - CD-i (2026-07-09 10-16-53).dat"
    "pspminis"      = "Sony - PlayStation Portable (PSN) (Minis) (Decrypted) (20251222-175857).dat"
    "psn"           = "Sony - PlayStation Portable (PSN) (Decrypted) (20260415-170329).dat"
    "gameandwatch"  = "Handheld Electronic Game (Libretro).dat"
    "psp"           = "Sony - PlayStation Portable (2026-06-13 08-01-46).dat"
    "amigacdtv"     = "Commodore - Amiga CDTV (2026-05-16 20-58-08).dat"
    "amigacd32"     = "Commodore - Amiga CD32 (2026-05-08 20-54-04).dat"
    "xbox"          = "Microsoft - Xbox (2026-06-14 23-43-27).dat"
    "atari2600"     = "Atari - Atari 2600 (20260428-103934).dat"
    "atari5200"     = "Atari - Atari 5200 (20260412-121350).dat"
    "atari7800"     = "Atari - Atari 7800 (BIN) (20260504-112425).dat"
    "astrocade"     = "Bally - Astrocade (20220411-220423).dat"
    "vectrex"       = "GCE - Vectrex (20251117-141044).dat"
    "odyssey2"      = "Magnavox - Odyssey 2 (20250723-151315).dat"
    "intellivision" = "Mattel - Intellivision (20260304-102057).dat"
}

# Misma lista cerrada de regiones que build-dat-index-nointro.ps1
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
    "System Module", "E3 Video", "Nintendo 3DS Conference", "Shared Data Archive",
    "Not For Sale"
)

$flagTags = @("Aftermarket", "Compilation", "Unl", "Pirate", "NP")

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
    param([string]$Id, [string]$DatFile)

    $datPath = Join-Path $DatRoot $DatFile
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

    $gamesOut = New-Object System.Collections.Generic.List[object]
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

        $gamesOut.Add([ordered]@{
            name       = Get-BaseName -Name $fullName
            aliases    = @()
            regions    = @(Get-Regions -Name $fullName | Sort-Object)
            properties = [ordered]@{ category = Get-Category -Name $fullName }
        })
    }

    $gamesOut = @($gamesOut | Sort-Object { $_.name })

    $output = [ordered]@{
        system    = $Id
        source    = "1G1R (retool)"
        dat       = $DatFile
        generated = (Get-Date -Format "yyyy-MM-dd")
        games     = $gamesOut
    }
    Write-JsonFile -Path (Join-Path $OutputRoot "$Id.json") -Data $output

    $debugOutput = [ordered]@{
        system    = $Id
        discarded = @($discardedLog | Sort-Object name)
        accepted  = @($acceptedLog | Sort-Object)
    }
    Write-JsonFile -Path (Join-Path $DebugRoot "$Id.json") -Data $debugOutput

    Write-Host "Generado: $Id.json ($($gamesOut.Count) familias, $($discardedLog.Count) descartados)"
}

$ids = if ($SystemId) { @($SystemId) } else { $datMap.Keys }

foreach ($id in $ids) {
    if (-not $datMap.Contains($id)) {
        Write-Warning "Sistema no mapeado: $id"
        continue
    }
    Build-SystemIndex -Id $id -DatFile $datMap[$id]
}
