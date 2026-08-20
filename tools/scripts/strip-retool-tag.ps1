<#
Renombra ficheros de salida de retool quitando el ruido que retool y sus
flags de linea de comandos anaden tras el nombre base del DAT (todo desde
" (Retool" en adelante: fecha/hora de la pasada, flags tipo
"[-aABbcdDekmMoPrv]", el marcador "(-d)" de deduplicado, y la palabra suelta
"report" en los .txt), conservando lo que si aporta informacion:

- El recuento de titulos entre parentesis, ej. "(510)"/"(1,297)" - se queda
  tal cual, pegado al final del nombre.
- El marcador "(Removed titles)" cuando aplica (informe de titulos
  descartados que retool genera junto al DAT principal) - se queda antes
  del recuento. Sin esto, el .dat principal y el de "Removed titles" del
  mismo sistema colapsarian al mismo nombre tras quitar el resto (mismo
  nombre base, misma fecha de version) y uno de los dos se perderia el
  renombrado por colision.
- Todo lo que ya iba antes de " (Retool" (nombre del sistema, fecha de
  version del DAT origen) - nunca se toca, no forma parte del tag de retool.

Ejemplos:
    "Bandai - WonderSwan (20260819-205002) (Retool 2026-08-19 21-34-17) (190) [-aABbcdDekmMoPrv].dat"
        -> "Bandai - WonderSwan (20260819-205002) (190).dat"
    "Bandai - WonderSwan (20260819-205002) (Retool 2026-08-19 21-34-17) (Removed titles) (16) [-aABbcdDekmMoPrv].dat"
        -> "Bandai - WonderSwan (20260819-205002) (Removed titles) (16).dat"
    "Bandai - WonderSwan (20260819-205002) (Retool 2026-08-19 21-34-17) [-aABbcdDekmMoPrv] report.txt"
        -> "Bandai - WonderSwan (20260819-205002).txt"

Recursivo: procesa -Path y todas sus subcarpetas (Get-ChildItem -Recurse) -
sistemas en 1g1r/, fullset/, fullset/japan/, fullset/other/, etc. se
renombran en la misma pasada.

Uso:
    pwsh tools/scripts/strip-retool-tag.ps1 -Path data/dats -WhatIf
    pwsh tools/scripts/strip-retool-tag.ps1 -Path data/dats
#>

[CmdletBinding()]
param(
    [string]$Path = "data/dats",

    [switch]$WhatIf
)

$retoolTagPattern = ' \(Retool.*$'

$files = @(Get-ChildItem -Path $Path -File -Recurse -Force | Where-Object { $_.Name -match $retoolTagPattern })

if ($files.Count -eq 0) {
    Write-Host "No se encontraron ficheros con el tag Retool en $Path."
    return
}

foreach ($f in $files) {
    $ext = [System.IO.Path]::GetExtension($f.Name)
    $beforeRetool = ($f.Name -split ' \(Retool', 2)[0]
    $tail = $f.Name.Substring($beforeRetool.Length, $f.Name.Length - $beforeRetool.Length - $ext.Length)

    $removedTitles = if ($tail -match '\(Removed titles\)') { ' (Removed titles)' } else { '' }
    $countMatch = [regex]::Match($tail, '\((?<n>[\d,]+)\)')
    $count = if ($countMatch.Success) { " ($($countMatch.Groups['n'].Value))" } else { '' }

    $newName = "$beforeRetool$removedTitles$count$ext"
    $newPath = Join-Path $f.DirectoryName $newName

    if ($newName -eq $f.Name) { continue }

    if (Test-Path -LiteralPath $newPath) {
        Write-Host "OMITIDO (ya existe destino): $($f.Name)"
        continue
    }

    if ($WhatIf) {
        Write-Host "Renombraria: $($f.Name)"
        Write-Host "        ->   $newName"
    } else {
        Rename-Item -LiteralPath $f.FullName -NewName $newName
        Write-Host "Renombrado: $newName"
    }
}

Write-Host ""
Write-Host "Total procesados: $($files.Count)"
