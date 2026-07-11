<#
Crea la estructura de carpetas destino para romsets en data/roms,
organizada en arcade/console/micro con una subcarpeta por identificador
canónico de docs/systems.md. Cada carpeta de sistema incluye un stub
vacío de gamelist.xml y la estructura de media/ esperada por
gamelist-utils (https://github.com/JayCanuck/gamelist-utils).

Uso:
    pwsh tools/scripts/create-roms-structure.ps1
    pwsh tools/scripts/create-roms-structure.ps1 -WhatIf

Los identificadores están hardcodeados a partir de docs/systems.md.
Si se añaden o eliminan sistemas en ese fichero, actualizar las listas
de abajo para mantener la coherencia.
#>

[CmdletBinding(SupportsShouldProcess)]
param(
    [string]$RootPath
)

if (-not $RootPath) {
    $scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
    $RootPath = Join-Path (Split-Path -Parent (Split-Path -Parent $scriptDir)) "data\roms"
}

$consolas = @(
    "gameandwatch", "nes", "sg1000", "mastersystem", "fds", "pcengine", "pcenginecd",
    "megadrive", "gb", "lynx", "gamegear", "snes", "neogeo", "gx4000", "amigacdtv",
    "cdi", "segacd", "3do", "jaguar", "amigacd32", "psx", "saturn", "sega32x", "sgb",
    "jaguarcd", "satellaview", "sufami", "n64", "64dd", "ngp", "gbc", "dreamcast",
    "ngpc", "supervision", "ps2", "pokemini", "gba", "gamecube", "nds", "dsiware",
    "psp", "xbox", "xbox360", "wii", "ps3", "3ds", "psvita", "wiiu", "switch",
    "virtualboy", "wswan", "wswanc"
)

$arcade = @(
    "mame", "fbneo", "neogeo", "cps1", "cps2", "cps3", "naomi", "atomiswave",
    "daphne", "naomi2", "chihiro", "triforce"
)

$micro = @(
    "zx81", "dragon32", "c64", "spectrum", "msx", "amstradcpc", "c128", "atarist",
    "amiga", "msx2", "sharpx68000"
)

$groups = @{
    "console" = $consolas
    "arcade"  = $arcade
    "micro"   = $micro
}

$mediaFolders = @("box2d", "box3d", "manual", "mixed", "screenshot", "snap", "title", "wheel")

$gamelistStub = "<?xml version=`"1.0`"?>`n<gameList>`n</gameList>`n"

foreach ($group in $groups.Keys) {
    foreach ($id in $groups[$group]) {
        $path = Join-Path $RootPath "$group\$id"
        if (-not (Test-Path $path)) {
            New-Item -ItemType Directory -Path $path -Force | Out-Null
            Write-Host "Creada: $path"
        }

        $gamelistPath = Join-Path $path "gamelist.xml"
        if (-not (Test-Path $gamelistPath)) {
            Set-Content -Path $gamelistPath -Value $gamelistStub -NoNewline
        }

        foreach ($mediaFolder in $mediaFolders) {
            $mediaPath = Join-Path $path "media\$mediaFolder"
            if (-not (Test-Path $mediaPath)) {
                New-Item -ItemType Directory -Path $mediaPath -Force | Out-Null
            }

            $mediaGitkeepPath = Join-Path $mediaPath ".gitkeep"
            if (-not (Test-Path $mediaGitkeepPath)) {
                New-Item -ItemType File -Path $mediaGitkeepPath -Force | Out-Null
            }
        }
    }
}
