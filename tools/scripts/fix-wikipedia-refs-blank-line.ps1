<#
Corrige la falta de linea en blanco entre el titulo y la seccion
"Fuentes de referencia" insertada por add-wikipedia-refs.ps1.
Script de un solo uso.
#>

$DocsRoot = Join-Path $PSScriptRoot "..\..\docs\guides\romsets\systems"
$DocsRoot = (Resolve-Path $DocsRoot).Path
$Utf8NoBom = [System.Text.UTF8Encoding]::new($false)

$files = Get-ChildItem -Path $DocsRoot -Filter "*.md" | Where-Object { $_.Name -ne "README.md" }

foreach ($f in $files) {
    $text = [System.IO.File]::ReadAllText($f.FullName, [System.Text.Encoding]::UTF8)
    $fixedText = $text -replace "(?m)^(#[^\n]*)\n## Fuentes de referencia", "`$1`n`n## Fuentes de referencia"
    if ($fixedText -ne $text) {
        [System.IO.File]::WriteAllText($f.FullName, $fixedText, $Utf8NoBom)
        Write-Host "Corregido: $($f.Name)"
    }
}
