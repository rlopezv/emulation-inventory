<#
Inserta una seccion "Fuentes de referencia" con el enlace de Wikipedia
justo despues del titulo de cada fichero docs/guides/romsets/systems/<id>.md.
Script de un solo uso, no forma parte del pipeline habitual.
#>

$DocsRoot = Join-Path $PSScriptRoot "..\..\docs\guides\romsets\systems"
$DocsRoot = (Resolve-Path $DocsRoot).Path
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)

$wikiMap = @{
    "3do"          = "https://en.wikipedia.org/wiki/3DO_Interactive_Multiplayer"
    "3ds"          = "https://en.wikipedia.org/wiki/Nintendo_3DS"
    "3dseshop"     = "https://en.wikipedia.org/wiki/Nintendo_eShop"
    "64dd"         = "https://en.wikipedia.org/wiki/Nintendo_64DD"
    "amigacd32"    = "https://en.wikipedia.org/wiki/Amiga_CD32"
    "amigacdtv"    = "https://en.wikipedia.org/wiki/Commodore_CDTV"
    "cdi"          = "https://en.wikipedia.org/wiki/CD-i"
    "dreamcast"    = "https://en.wikipedia.org/wiki/Dreamcast"
    "dsiware"      = "https://en.wikipedia.org/wiki/DSiWare"
    "fds"          = "https://en.wikipedia.org/wiki/Family_Computer_Disk_System"
    "gamecube"     = "https://en.wikipedia.org/wiki/GameCube"
    "gamegear"     = "https://en.wikipedia.org/wiki/Game_Gear"
    "gb"           = "https://en.wikipedia.org/wiki/Game_Boy"
    "gba"          = "https://en.wikipedia.org/wiki/Game_Boy_Advance"
    "gbc"          = "https://en.wikipedia.org/wiki/Game_Boy_Color"
    "gx4000"       = "https://en.wikipedia.org/wiki/Amstrad_GX4000"
    "jaguar"       = "https://en.wikipedia.org/wiki/Atari_Jaguar"
    "jaguarcd"     = "https://en.wikipedia.org/wiki/Atari_Jaguar_CD"
    "lynx"         = "https://en.wikipedia.org/wiki/Atari_Lynx"
    "mastersystem" = "https://en.wikipedia.org/wiki/Master_System"
    "megadrive"    = "https://en.wikipedia.org/wiki/Sega_Genesis"
    "n64"          = "https://en.wikipedia.org/wiki/Nintendo_64"
    "nds"          = "https://en.wikipedia.org/wiki/Nintendo_DS"
    "neogeocd"     = "https://en.wikipedia.org/wiki/Neo_Geo_CD"
    "nes"          = "https://en.wikipedia.org/wiki/Nintendo_Entertainment_System"
    "ngp"          = "https://en.wikipedia.org/wiki/Neo_Geo_Pocket"
    "ngpc"         = "https://en.wikipedia.org/wiki/Neo_Geo_Pocket_Color"
    "pcengine"     = "https://en.wikipedia.org/wiki/TurboGrafx-16"
    "pcenginecd"   = "https://en.wikipedia.org/wiki/TurboGrafx-CD"
    "pokemini"     = "https://en.wikipedia.org/wiki/Pok%C3%A9mon_Mini"
    "ps2"          = "https://en.wikipedia.org/wiki/PlayStation_2"
    "ps3"          = "https://en.wikipedia.org/wiki/PlayStation_3"
    "psp"          = "https://en.wikipedia.org/wiki/PlayStation_Portable"
    "psx"          = "https://en.wikipedia.org/wiki/PlayStation_(console)"
    "satellaview"  = "https://en.wikipedia.org/wiki/Satellaview"
    "saturn"       = "https://en.wikipedia.org/wiki/Sega_Saturn"
    "sega32x"      = "https://en.wikipedia.org/wiki/32X"
    "segacd"       = "https://en.wikipedia.org/wiki/Sega_CD"
    "sg1000"       = "https://en.wikipedia.org/wiki/SG-1000"
    "snes"         = "https://en.wikipedia.org/wiki/Super_Nintendo_Entertainment_System"
    "sufami"       = "https://en.wikipedia.org/wiki/Sufami_Turbo"
    "supervision"  = "https://en.wikipedia.org/wiki/Watara_Supervision"
    "virtualboy"   = "https://en.wikipedia.org/wiki/Virtual_Boy"
    "wii"          = "https://en.wikipedia.org/wiki/Wii"
    "wiiu"         = "https://en.wikipedia.org/wiki/Wii_U"
    "wswan"        = "https://en.wikipedia.org/wiki/WonderSwan"
    "wswanc"       = "https://en.wikipedia.org/wiki/WonderSwan_Color"
    "xbox"         = "https://en.wikipedia.org/wiki/Xbox_(console)"
    "xbox360"      = "https://en.wikipedia.org/wiki/Xbox_360"
}

foreach ($id in $wikiMap.Keys) {
    $path = Join-Path $DocsRoot "$id.md"
    if (-not (Test-Path $path)) {
        Write-Host "Falta fichero: $path"
        continue
    }

    $text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)

    if ($text.Contains("## Fuentes de referencia")) {
        Write-Host "Ya tiene seccion, se omite: $id"
        continue
    }

    $newlineIdx = $text.IndexOf("`n")
    if ($newlineIdx -lt 0) {
        Write-Host "Formato inesperado, se omite: $id"
        continue
    }

    $titleLine = $text.Substring(0, $newlineIdx)
    $rest = $text.Substring($newlineIdx + 1).TrimStart("`n")

    $url = $wikiMap[$id]
    $section = "`n## Fuentes de referencia`n`n- Wikipedia: $url`n`n"

    $newText = $titleLine + $section + $rest

    [System.IO.File]::WriteAllText($path, $newText, $Utf8NoBom)
    Write-Host "Actualizado: $id"
}
