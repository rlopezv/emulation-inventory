<#
Genera un JSON por sistema con los nombres base esperados de cada familia
de juego (1G1R) a partir de los DAT No-Intro / Non-Redump mapeados en
docs/romsets.md (solo sección Consolas).

Las variantes regionales/revisión se agrupan siguiendo la relación
parent/clone (atributo cloneofid) del propio DAT hasta la raíz de cada
familia. El nombre base del parent es el nombre canónico de la familia;
los nombres base de los clones que difieren del parent (releases con
título distinto por región, ej. Rockman/Mega Man) se listan como alias.

Para cada familia se extrae:
- name: nombre base del parent
- aliases: nombres base alternativos de la familia (títulos regionales
  distintos), fusionados con metadata/dat-index/aliases/<id>.json
- regions: regiones agregadas de todos los miembros de la familia
- properties.category: "Oficial", o "Aftermarket"/"Compilation"/"Unl"/
  "Pirate"/"NP" si algún miembro tiene ese tag; se agregan entre miembros

Se descartan por completo (no participan ni como parent ni como alias)
las entradas cuyo nombre contenga un tag Proto/Demo/Beta/Sample/Kiosk/
"Test Program"/Program/BIOS (con o sin sufijo numérico), o cuyo <rom> tenga
status="baddump".

El fichero metadata/dat-index/aliases/<id>.json es una capa manual: se
autogenera a partir de cloneofid la primera vez, pero está pensado para
editarlo a mano (añadir equivalencias que el DAT no vincula, corregir
vínculos erróneos). En cada ejecución se funde con lo detectado
automáticamente sin perder las entradas manuales, y el resultado
fusionado se usa también para agrupar el JSON principal del sistema.

Salida: metadata/dat-index/<id>.json y metadata/dat-index/aliases/<id>.json

Uso:
    pwsh tools/scripts/build-dat-index-nointro.ps1
    pwsh tools/scripts/build-dat-index-nointro.ps1 -SystemId nes

Los sistemas No-Intro se leen de tools/scripts/config/nointro-systems.json
(nombre base sin tag de pack ni fecha) y se resuelven buscando ese patron
en sources/dats/no-intro/full/ (Standard: cada <game> lleva id/cloneofid
numericos, que es lo que este script necesita para reconstruir el arbol
parent/clone). El pack Parent-Clone (sources/dats/no-intro/pc/) NO se usa
todavia como fuente de indexado: agrupa clones por cloneof="<nombre del
padre>" en vez de id/cloneofid, un esquema distinto que este script no
sabe interpretar aun; se sincroniza igualmente como copia de referencia
por tools/scripts/update-sources.ps1, pendiente de una adaptacion futura
del algoritmo si se decide consumirlo. Esa carpeta sources/ es la copia
de trabajo sincronizada desde el archivo crudo en metadata/dat/No-Intro/
por tools/scripts/update-sources.ps1; no tocar metadata/dat/ directamente
para este flujo.

Los sistemas Non-Redump siguen hardcodeados abajo en $nonRedumpMap con
nombre de fichero exacto (paquete/convencion distinta, sin migrar a
sources/ todavia) resuelto directamente en metadata/dat/Non-Redump/. Si
cambia el fichero DAT de alguno en docs/romsets.md, actualizar esa tabla.

gameandwatch usa metadata/dat/libretro/Handheld Electronic Game.dat, en
formato ClrMamePro (texto), fuera del alcance de este script (ver
docs/romsets.md#formato-de-dat). Pendiente de un parser específico.
#>

[CmdletBinding()]
param(
    [string]$SystemId,
    [string]$DatRoot,
    [string]$SourcesRoot,
    [string]$OutputRoot
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)

if (-not $DatRoot) { $DatRoot = Join-Path $repoRoot "metadata\dat" }
if (-not $SourcesRoot) { $SourcesRoot = Join-Path $repoRoot "sources\dats\no-intro" }
if (-not $OutputRoot) { $OutputRoot = Join-Path $repoRoot "metadata\dat-index" }
$AliasRoot = Join-Path $OutputRoot "aliases"
$DebugRoot = Join-Path $OutputRoot "debug"

$noIntroManifestPath = Join-Path $scriptDir "config\nointro-systems.json"
$noIntroManifestRaw = (Get-Content -Raw -Path $noIntroManifestPath | ConvertFrom-Json).systems
$noIntroManifest = [ordered]@{}
foreach ($prop in $noIntroManifestRaw.PSObject.Properties) { $noIntroManifest[$prop.Name] = $prop.Value }

# Non-Redump: fuera del manifiesto de No-Intro (formato/paquete distinto),
# se mantienen con nombre de fichero exacto en metadata/dat/Non-Redump/.
$nonRedumpMap = [ordered]@{
    "wiiu"    = "Non-Redump - Nintendo - Wii U (20260312-235110).dat"
    "ps3"     = "Non-Redump - Sony - PlayStation 3 (20250908-072347).dat"
    "psp"     = "Non-Redump - Sony - PlayStation Portable (20260421-200314).dat"
    "cdi"     = "Non-Redump - Philips - CD-i (20260429-044928).dat"
    "xbox360" = "Non-Redump - Microsoft - Xbox 360 (20251219-035655).dat"
}

$datMap = [ordered]@{}
foreach ($key in $noIntroManifest.Keys) {
    $datMap[$key] = @{ Source = "No-Intro"; BaseName = $noIntroManifest[$key] }
}
foreach ($key in $nonRedumpMap.Keys) {
    $datMap[$key] = @{ Source = "Non-Redump"; Dat = $nonRedumpMap[$key] }
}

function Resolve-NoIntroDat {
    # Busca <BaseName> (<timestamp>).dat en full/ (Standard: unico esquema
    # con id/cloneofid que este script sabe interpretar). Devuelve la ruta
    # completa del fichero mas reciente que coincida, o $null.
    param([string]$BaseName)

    $escapedBase = [regex]::Escape($BaseName)
    $pattern = "^$escapedBase \(\d{8}-\d{6}\)\.dat$"
    $folder = Join-Path $SourcesRoot "full"
    if (-not (Test-Path $folder)) { return $null }
    $match = Get-ChildItem -Path $folder -File |
        Where-Object { $_.Name -match $pattern } |
        Sort-Object Name -Descending | Select-Object -First 1
    if ($match) { return $match.FullName }
    return $null
}

# Tokens de región reconocidos por la convención No-Intro (lista cerrada).
# Auditada contra todos los DAT de No-Intro/Non-Redump (ver historial de
# build-dat-index-nointro): "United Kingdom" es el token real, no "UK".
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
    # Recorre los grupos entre paréntesis en orden y usa el primero que
    # contenga al menos un token de región reconocido (no asume que sea
    # necesariamente el primer grupo del nombre; ej. "Zanac (AI) (Japan)").
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

# Tags que descartan la entrada por completo (proto/demo/no final).
$discardTags = @(
    "Proto", "Demo", "Special Demo", "Trial", "Beta", "Sample", "Kiosk",
    "Test Program", "Program", "BIOS", "DLC", "Update", "System Application",
    "System Module", "E3 Video", "Nintendo 3DS Conference", "Shared Data Archive",
    "Not For Sale"
)

# Tags que se conservan pero marcan la entrada como no oficial.
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
    # Devuelve el tag/motivo de descarte, o $null si la entrada se conserva.
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

function Get-RootId {
    param([string]$Id, [hashtable]$Lookup, [hashtable]$Memo)

    if ($Memo.ContainsKey($Id)) { return $Memo[$Id] }

    $visited = [System.Collections.Generic.HashSet[string]]::new()
    $current = $Id
    while ($true) {
        if (-not $visited.Add($current)) { break }  # ciclo: cortamos aquí
        $node = $Lookup[$current]
        if (-not $node -or -not $node.CloneOfId -or -not $Lookup.ContainsKey($node.CloneOfId)) {
            break
        }
        $current = $node.CloneOfId
    }
    $Memo[$Id] = $current
    return $current
}

function Write-JsonFile {
    param([string]$Path, $Data)
    $dir = Split-Path -Parent $Path
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
    $json = $Data | ConvertTo-Json -Depth 8
    # ConvertTo-Json escapa innecesariamente ' & < > como \uXXXX; son
    # caracteres válidos y sin ambigüedad en JSON, se desescapan para
    # que el fichero sea legible (ej. "David Crane's Amazing Tennis").
    $json = $json -replace '\\u0027', "'" -replace '\\u0026', '&' -replace '\\u003c', '<' -replace '\\u003e', '>'
    [System.IO.File]::WriteAllText($Path, $json, [System.Text.UTF8Encoding]::new($false))
}

function Build-SystemIndex {
    param([string]$Id, [hashtable]$Entry)

    if ($Entry.Source -eq "No-Intro") {
        $datPath = Resolve-NoIntroDat -BaseName $Entry.BaseName
        if (-not $datPath) {
            Write-Warning "DAT no encontrado para '$Id' (No-Intro, base '$($Entry.BaseName)') en sources/dats/no-intro/full/. ¿Falta ejecutar update-sources.ps1?"
            return
        }
    } else {
        $datPath = Join-Path $DatRoot "$($Entry.Source)\$($Entry.Dat)"
        if (-not (Test-Path $datPath)) {
            Write-Warning "DAT no encontrado para '$Id': $datPath"
            return
        }
    }

    [xml]$xml = Get-Content -Raw -Path $datPath
    $games = $xml.datafile.game
    if (-not $games) {
        Write-Warning "Sin elementos <game> en '$Id': $datPath"
        return
    }

    # 1) Filtrar descartes y construir lookup id -> nodo
    $lookup = @{}
    $discardedLog = New-Object System.Collections.Generic.List[object]
    $acceptedLog = New-Object System.Collections.Generic.List[string]
    foreach ($game in $games) {
        $fullName = $game.name
        if (-not $fullName -or -not $game.id) { continue }

        $reason = Get-DiscardReason -Name $fullName -Rom $game.rom
        if ($reason) {
            $discardedLog.Add([ordered]@{ name = $fullName; reason = $reason })
            continue
        }
        $acceptedLog.Add($fullName)

        $lookup[$game.id] = @{
            Id         = $game.id
            CloneOfId  = $game.cloneofid
            FullName   = $fullName
            BaseName   = Get-BaseName -Name $fullName
            Regions    = Get-Regions -Name $fullName
            Category   = Get-Category -Name $fullName
        }
    }

    # 2) Resolver raíz de familia (parent/clone) por id
    $memo = @{}
    $families = [ordered]@{}  # rootId -> { CanonicalName, AliasNames(set), Regions(set), Categories(set) }

    foreach ($node in $lookup.Values) {
        if (-not $node.BaseName) { continue }

        $rootId = Get-RootId -Id $node.Id -Lookup $lookup -Memo $memo
        $rootNode = $lookup[$rootId]
        $canonicalName = $rootNode.BaseName

        if (-not $families.Contains($rootId)) {
            $families[$rootId] = @{
                CanonicalName = $canonicalName
                AliasNames    = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
                Regions       = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
                Categories    = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
            }
        }
        $family = $families[$rootId]
        if ($node.BaseName -ne $canonicalName) {
            [void]$family.AliasNames.Add($node.BaseName)
        }
        foreach ($r in $node.Regions) { [void]$family.Regions.Add($r) }
        [void]$family.Categories.Add($node.Category)
    }

    # 3) Cargar fichero de alias manual (si existe) y fusionar
    $aliasPath = Join-Path $AliasRoot "$Id.json"
    $manualAliases = @()
    if (Test-Path $aliasPath) {
        $existing = Get-Content -Raw -Path $aliasPath | ConvertFrom-Json
        if ($existing.aliases) { $manualAliases = @($existing.aliases) }
    }

    # Índice canonical -> family, para fusionar por nombre
    $familyByCanonical = @{}
    foreach ($key in $families.Keys) { $familyByCanonical[$families[$key].CanonicalName] = $families[$key] }

    foreach ($manualEntry in $manualAliases) {
        $canonical = $manualEntry.canonical
        $aliasesToAdd = @($manualEntry.aliases)
        if (-not $familyByCanonical.ContainsKey($canonical)) {
            Write-Warning "Alias manual en '$Id' referencia un nombre canónico no encontrado en el DAT: '$canonical' (se ignora)"
            continue
        }
        $targetFamily = $familyByCanonical[$canonical]
        foreach ($aliasName in $aliasesToAdd) {
            if ($aliasName -eq $canonical) { continue }
            [void]$targetFamily.AliasNames.Add($aliasName)

            # Si ese alias era el canónico de OTRA familia auto-detectada, fusionamos esa familia también.
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

    # 4) Salida del índice principal, ordenada por nombre canónico
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
        dat       = (Split-Path -Leaf $datPath)
        generated = (Get-Date -Format "yyyy-MM-dd")
        games     = @($gamesOut)
    }
    Write-JsonFile -Path (Join-Path $OutputRoot "$Id.json") -Data $output

    # 5) Persistir el fichero de alias fusionado (auto + manual)
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

    # 6) Fichero de depuración: descartados (con motivo) y aceptados (nombre
    # completo del DAT). Solo para revisar patrones y afinar los filtros de
    # descarte; se borra metadata/dat-index/debug/ entera al terminar.
    $debugOutput = [ordered]@{
        system    = $Id
        discarded = @($discardedLog | Sort-Object name)
        accepted  = @($acceptedLog | Sort-Object)
    }
    Write-JsonFile -Path (Join-Path $DebugRoot "$Id.json") -Data $debugOutput

    Write-Host "Generado: $Id.json ($($gamesOut.Count) familias, $($discardedLog.Count) descartados) + aliases/$Id.json ($($aliasesOut.Count) con alias)"
}

$ids = if ($SystemId) { @($SystemId) } else { $datMap.Keys }

foreach ($id in $ids) {
    if (-not $datMap.Contains($id)) {
        Write-Warning "Sistema no mapeado: $id"
        continue
    }
    Build-SystemIndex -Id $id -Entry $datMap[$id]
}
