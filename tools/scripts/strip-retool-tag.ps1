<#
Renombra ficheros quitando desde " (Retool" hasta el final del nombre (justo
antes de la extension), eliminando todo lo que retool y sus flags anadieron
tras el nombre base del DAT.

Uso:
    pwsh tools/scripts/strip-retool-tag.ps1 -Path data/dats -WhatIf
    pwsh tools/scripts/strip-retool-tag.ps1 -Path data/dats
#>

[CmdletBinding()]
param(
    [string]$Path = "data/dats",

    [switch]$WhatIf
)

$pattern = ' \(Retool.*$'

$files = @(Get-ChildItem -Path $Path -File -Recurse -Force | Where-Object { $_.Name -match $pattern })

if ($files.Count -eq 0) {
    Write-Host "No se encontraron ficheros con el tag Retool en $Path."
    return
}

foreach ($f in $files) {
    $newName = $f.Name -replace ' \(Retool.*(\.[^.]+)$', '$1'
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
