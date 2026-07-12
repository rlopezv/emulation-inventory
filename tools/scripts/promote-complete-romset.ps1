<#
Promociona F:\roms\console-complete\<sistema> (generado por build-complete-romset.ps1)
a F:\roms\console\<sistema>, sustituyendo por completo el contenido anterior alli y
en F:\roms\console\_extra\<sistema>. Por defecto NO borra ni mueve nada, solo informa
de lo que haria; hace falta pasar -Execute para ejecutar de verdad.

Uso:
    pwsh tools/scripts/promote-complete-romset.ps1 -SystemId sg1000
    pwsh tools/scripts/promote-complete-romset.ps1 -SystemId sg1000 -Execute
    pwsh tools/scripts/promote-complete-romset.ps1 -SystemId wswan -ExtraSystemId wonderswan -Execute
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$SystemId,

    [string]$SourceRoot = "F:\roms\console",

    [string]$CompleteRoot = "F:\roms\console-complete",

    [string]$ExtraSystemId,

    [switch]$Execute
)

$completeSystemDir = Join-Path $CompleteRoot $SystemId
if (-not (Test-Path $completeSystemDir)) {
    throw "No existe $completeSystemDir. Genera primero el romset completo con build-complete-romset.ps1."
}

$completeCount = @(Get-ChildItem -LiteralPath $completeSystemDir -File -Recurse -Force).Count
if ($completeCount -eq 0) {
    throw "$completeSystemDir esta vacio. No hay nada que promover."
}

$sourceSystemDir = Join-Path $SourceRoot $SystemId
$extraId = if ($ExtraSystemId) { $ExtraSystemId } else { $SystemId }
$extraDir = Join-Path (Join-Path $SourceRoot "_extra") $extraId

$sourceCount = if (Test-Path $sourceSystemDir) { @(Get-ChildItem -LiteralPath $sourceSystemDir -File -Recurse -Force).Count } else { 0 }
$extraCount = if (Test-Path $extraDir) { @(Get-ChildItem -LiteralPath $extraDir -File -Recurse -Force).Count } else { 0 }

Write-Host "Sistema: $SystemId"
Write-Host ""
Write-Host "Origen a promover: $completeSystemDir ($completeCount ficheros)"
Write-Host "Se borraria: $sourceSystemDir ($sourceCount ficheros)"
Write-Host "Se borraria: $extraDir ($extraCount ficheros)"
Write-Host "Destino final: $sourceSystemDir <- contenido de $completeSystemDir"

if (-not $Execute) {
    Write-Host ""
    Write-Host "Modo informativo (sin -Execute): no se ha borrado ni movido nada."
    return
}

if (Test-Path $sourceSystemDir) {
    try {
        Remove-Item -LiteralPath $sourceSystemDir -Recurse -Force -ErrorAction Stop
    } catch {
        throw "No se pudo borrar $sourceSystemDir. Nada mas se ha tocado. Error: $($_.Exception.Message)"
    }
}

$moveOk = $false
$lastError = $null
for ($attempt = 1; $attempt -le 3; $attempt++) {
    try {
        Move-Item -LiteralPath $completeSystemDir -Destination $sourceSystemDir -ErrorAction Stop
        $moveOk = $true
        break
    } catch {
        $lastError = $_
        Start-Sleep -Seconds 3
    }
}

if (-not $moveOk) {
    Write-Host ""
    Write-Host "ERROR: fallo el Move-Item de $completeSystemDir a $sourceSystemDir tras 3 intentos."
    Write-Host "Detalle: $($lastError.Exception.Message)"
    Write-Host ""
    Write-Host "IMPORTANTE: $sourceSystemDir puede estar vacio o no existir ahora mismo."
    Write-Host "El contenido original sigue intacto en: $completeSystemDir"
    Write-Host "No se ha tocado $extraDir. Reintenta manualmente o vuelve a ejecutar este script."
    throw "Promocion abortada para $SystemId."
}

$movedCount = @(Get-ChildItem -LiteralPath $sourceSystemDir -File -Recurse -Force).Count
if ($movedCount -ne $completeCount) {
    Write-Host ""
    Write-Host "ERROR: $sourceSystemDir tiene $movedCount ficheros, se esperaban $completeCount."
    Write-Host "No se ha tocado $extraDir. Revisa $sourceSystemDir manualmente antes de continuar."
    throw "Promocion abortada para $SystemId (recuento no coincide tras el movimiento)."
}

if (Test-Path $extraDir) {
    Remove-Item -LiteralPath $extraDir -Recurse -Force
}

Write-Host ""
Write-Host "Promocion completada. $sourceSystemDir tiene ahora $movedCount ficheros."
