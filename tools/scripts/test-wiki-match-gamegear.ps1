<#
Prueba de emparejamiento (v2): titulos de la tabla de Wikipedia (List of Game Gear
games), incluyendo variantes regionales embebidas en la celda de titulo
(formato "Titulo (REGION: TituloAlt)" o "Titulo1 (REGION1); Titulo2 (REGION2)"),
contra las familias de metadata/dat-index/gamegear.json (nombre exacto o alias
exacto, tras normalizar). Script de un solo uso para medir el porcentaje de
acierto antes de generalizar el enfoque.
#>

$repoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$jsonPath = Join-Path $repoRoot "metadata\dat-index\gamegear.json"
$wikiPath = "C:\Users\ramon\AppData\Local\Temp\claude\c--Users-ramon-development-emulation\f12c4301-1089-460e-9009-be8c90aa15c3\scratchpad\gamegear-wiki-v2.txt"

function Normalize([string]$s) {
    $curlyApos = [char]0x2019
    $enDash = [char]0x2013
    $emDash = [char]0x2014
    $s = $s.Replace($curlyApos, "'").Replace($enDash, "-").Replace($emDash, "-")
    $s = $s.ToLowerInvariant()
    $s = $s -replace "'", ""
    $s = $s -replace "^the ", ""
    $s = $s -replace ", the$", ""
    $s = $s -replace "[,!.:-]", " "
    $s = $s -replace "\s+", " "
    return $s.Trim()
}

function Get-TitleVariants([string]$field) {
    $variants = New-Object System.Collections.Generic.List[string]
    $segments = $field -split ';'
    foreach ($seg in $segments) {
        $seg = $seg.Trim()
        if (-not $seg) { continue }
        if ($seg -match '^(.*?)\s*\(([A-Z]{2,3}):\s*(.*)\)$') {
            [void]$variants.Add($Matches[1].Trim())
            [void]$variants.Add($Matches[3].Trim())
        } elseif ($seg -match '^(.*?)\s*\([A-Z]{2,3}\)$') {
            [void]$variants.Add($Matches[1].Trim())
        } else {
            [void]$variants.Add($seg)
        }
    }
    return $variants
}

$json = Get-Content -Raw -Path $jsonPath | ConvertFrom-Json

$lookup = @{}
foreach ($g in $json.games) {
    $key = Normalize $g.name
    if (-not $lookup.ContainsKey($key)) { $lookup[$key] = $g.name }
    foreach ($a in $g.aliases) {
        $akey = Normalize $a
        if (-not $lookup.ContainsKey($akey)) { $lookup[$akey] = $g.name }
    }
}

$wikiLines = Get-Content -Path $wikiPath -Encoding UTF8
$total = 0
$matched = 0
$unmatched = New-Object System.Collections.Generic.List[string]

foreach ($line in $wikiLines) {
    if (-not $line.Trim()) { continue }
    $parts = $line -split '\|\|'
    $titleField = $parts[0].Trim()
    if (-not $titleField) { continue }
    $total++

    $variants = Get-TitleVariants $titleField
    $rowMatched = $false
    foreach ($v in $variants) {
        $key = Normalize $v
        if ($lookup.ContainsKey($key)) {
            $rowMatched = $true
            break
        }
    }

    if ($rowMatched) {
        $matched++
    } else {
        [void]$unmatched.Add($titleField)
    }
}

Write-Host "Total wiki: $total"
Write-Host "Matched: $matched"
Write-Host ("Rate: {0:P1}" -f ($matched / $total))
Write-Host ""
Write-Host "Sin match:"
$unmatched | ForEach-Object { Write-Host "  - $_" }
