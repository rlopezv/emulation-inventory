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
    pwsh tools/scripts/build-dat-index-nointro.ps1 -SystemId nes -SourceMode Pc
    pwsh tools/scripts/build-dat-index-nointro.ps1 -SystemId nes -SourceMode Merged

Los sistemas No-Intro se leen de tools/scripts/config/nointro-systems.json
(nombre base sin tag de pack ni fecha) y se resuelven en
sources/dats/no-intro/, copia de trabajo sincronizada desde metadata/dat/No-Intro/
por tools/scripts/update-sources.ps1 (no tocar metadata/dat/ directamente
para este flujo). Los tres packs sincronizados se parsean siempre (para que
el contraste informativo funcione en cualquier modo), pero solo uno decide
el arbol de familias del <id>.json final, seleccionable con -SourceMode:

- **FullAftermarket** (por defecto) - full/ (Standard, sin aftermarket -
  confirmado por grep sobre los 30 sistemas del manifiesto: 0 coincidencias
  de "aftermarket") + aftermarket/ (pack separado, mismo esquema id/
  cloneofid nativo que full/) combinados. Los id NO son globales entre
  packs - cada fichero numera desde 0001 por su cuenta (colision confirmada
  en Atari 2600) - se namespacean por origen ("full:0001"/"aftermarket:0001")
  antes de fusionar los lookups y reconstruir el arbol combinado.
- **Pc** - arbol reconstruido enteramente desde pc/ (Parent-Clone), usando
  cloneof="<nombre del padre>" por nombre en vez de id/cloneofid (pc/ no
  trae atributo id). El propio nombre completo del <game> sirve de clave
  (unico dentro del DAT por construccion de No-Intro), asi Get-RootId
  funciona sin cambios sobre este lookup igual que sobre el de full+aftermarket.
- **Merged** - arbol de FullAftermarket como base, completado con las
  familias que solo existen en pc/ (deteccion via el mismo contraste que en
  modo informativo) usando los datos de pc/ para esas entradas.

En cualquier modo se genera el mismo informe de contraste bidireccional
(titulos en pc/ ausentes de full+aftermarket, y viceversa) en
metadata/dat-index/debug/<id>-pc-contrast.json, calculado siempre sobre
full+aftermarket vs pc/ sin importar cual sea la fuente activa; no bloquea
la build. El campo de cruce entre pc/ y full+aftermarket es el nombre
completo del <game> (identico byte a byte entre packs).

Capa de validacion adicional: metadata/dat/retool/clonelists/<BaseName> (No-Intro).json
(repo retool-clonelists-metadata, agrupa por coincidencia de texto
searchTerm/priority, mantenido por la comunidad) se usa como refuerzo/
validacion cruzada del arbol cloneofid - NO como fuente primaria (a
diferencia de build-dat-index-redump.ps1, donde si lo es porque Redump no
exporta cloneofid). Las divergencias entre el grupo cloneofid y el grupo
del clonelist se listan en metadata/dat-index/debug/<id>-clonelist-diff.json.

Los sistemas Non-Redump siguen hardcodeados abajo en $nonRedumpMap con
nombre de fichero exacto (paquete/convencion distinta, sin migrar a
sources/ todavia) resuelto directamente en metadata/dat/Non-Redump/. Si
cambia el fichero DAT de alguno en docs/romsets.md, actualizar esa tabla.
No participan del combinado full+aftermarket ni del contraste con pc/.

gameandwatch usa metadata/dat/libretro/Handheld Electronic Game.dat, en
formato ClrMamePro (texto), fuera del alcance de este script (ver
docs/romsets.md#formato-de-dat). Pendiente de un parser específico.
#>

[CmdletBinding()]
param(
    [string]$SystemId,
    [string]$DatRoot,
    [string]$SourcesRoot,
    [string]$OutputRoot,
    [ValidateSet("FullAftermarket", "Pc", "Merged")]
    [string]$SourceMode = "FullAftermarket"
)

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$repoRoot = Split-Path -Parent (Split-Path -Parent $scriptDir)

if (-not $DatRoot) { $DatRoot = Join-Path $repoRoot "metadata\dat" }
if (-not $SourcesRoot) { $SourcesRoot = Join-Path $repoRoot "sources\dats\no-intro" }
if (-not $OutputRoot) { $OutputRoot = Join-Path $repoRoot "metadata\dat-index" }
$AliasRoot = Join-Path $OutputRoot "aliases"
$DebugRoot = Join-Path $OutputRoot "debug"
$ClonelistRoot = Join-Path $DatRoot "retool\clonelists"
$MetadataRoot = Join-Path $DatRoot "retool\metadata"

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
    # Busca <BaseName>[ <Tag>] (<timestamp>).dat en el pack indicado
    # (full/aftermarket/pc, los tres con esquema Logiqx). Devuelve la ruta
    # completa del fichero mas reciente que coincida, o $null si el pack no
    # tiene fichero para ese sistema (aftermarket/pc no cubren todos).
    param([string]$BaseName, [string]$Pack, [string]$Tag)

    $suffix = if ($Tag) { " $Tag" } else { "" }
    $escapedBase = [regex]::Escape("$BaseName$suffix")
    $pattern = "^$escapedBase \(\d{8}-\d{6}\)\.dat$"
    $folder = Join-Path $SourcesRoot $Pack
    if (-not (Test-Path $folder)) { return $null }
    $match = Get-ChildItem -Path $folder -File |
        Where-Object { $_.Name -match $pattern } |
        Sort-Object Name -Descending | Select-Object -First 1
    if ($match) { return $match.FullName }
    return $null
}

function Resolve-RetoolDataPath {
    # El BaseName del manifiesto incluye a veces un tag de formato que los
    # ficheros de retool-clonelists-metadata no llevan (ej. "Atari - Atari
    # Lynx (LYX)" -> "Atari - Atari Lynx (No-Intro).json", sin "(LYX)"; idem
    # "(BigEndian)", "(Decrypted)", "(J64)"...). Se prueba primero el nombre
    # exacto y, si no existe, se reintenta quitando el ultimo grupo entre
    # parentesis. Reutilizable para clonelists/ y metadata/ (mismo patron de
    # nombre "<Sistema> (No-Intro).json" en ambas carpetas).
    param([string]$BaseName, [string]$Root)
    $candidates = @($BaseName)
    $stripped = [regex]::Replace($BaseName, '\s*\([^()]*\)$', '')
    if ($stripped -ne $BaseName) { $candidates += $stripped }
    foreach ($candidate in $candidates) {
        $path = Join-Path $Root "$candidate (No-Intro).json"
        if (Test-Path $path) { return $path }
    }
    return $null
}

function Resolve-ClonelistPath {
    param([string]$BaseName)
    return Resolve-RetoolDataPath -BaseName $BaseName -Root $ClonelistRoot
}

function Resolve-MetadataPath {
    param([string]$BaseName)
    return Resolve-RetoolDataPath -BaseName $BaseName -Root $MetadataRoot
}

function Get-ClonelistMap {
    # searchTerm (nombre base tal como aparece en el DAT) -> group (nombre
    # canonico curado por retool-clonelists-metadata). Igual que en
    # build-dat-index-redump.ps1 (duplicado aqui para no acoplar ambos scripts).
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

function Get-LanguageMap {
    # nombre completo del <game> -> lista de codigos de idioma ("En","Fr"...)
    # curados por retool-clonelists-metadata (metadata/dat/retool/metadata/).
    # OPCIONAL y usado DESPUES del calculo propio (Resolve-Languages, cadena
    # nombre+region) - no rellena el campo languages, solo sirve para
    # detectar divergencias entre lo calculado y lo curado (ver paso 9 de
    # Build-SystemIndex, debug/<id>-language-diff.json).
    param([string]$Path)
    $map = @{}
    if (-not $Path -or -not (Test-Path $Path)) { return $map }
    $json = Get-Content -Raw -Path $Path | ConvertFrom-Json
    foreach ($prop in $json.PSObject.Properties) {
        $languages = $prop.Value.languages
        if ($languages) { $map[$prop.Name] = @($languages) }
    }
    return $map
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

# Idioma por defecto SOLO para regiones con un idioma dominante razonable
# (fallback de ultimo recurso, cuando la deteccion por nombre no dio idioma
# - ver Get-LanguageForRegions). Region ausente de este mapa = sin default,
# no se inventa dato (ver CLAUDE.md "Do not invent data"): "Asia", "Belgium"
# (Fr/Nl oficiales), "Bangladesh", "Scandinavia", "Switzerland" (De/Fr/It
# oficiales) quedan fuera por ambiguedad real de idioma dominante.
# "Unknown" y "Europe" SI tienen default (En) - decision explicita del
# usuario: mejor asumir ingles que dejar el campo vacio.
$regionLanguageDefaults = @{
    "Argentina"      = "Es"
    "Australia"      = "En"
    "Austria"        = "De"
    "Brazil"         = "Pt"
    "Bulgaria"       = "Bg"
    "Canada"         = "En"
    "Chile"          = "Es"
    "China"          = "Zh"
    "Colombia"       = "Es"
    "Croatia"        = "Hr"
    "Czechia"        = "Cs"
    "Denmark"        = "Da"
    "Egypt"          = "Ar"
    "Europe"         = "En"
    "Finland"        = "Fi"
    "France"         = "Fr"
    "Germany"        = "De"
    "Greece"         = "El"
    "Hong Kong"      = "Zh"
    "Hungary"        = "Hu"
    "India"          = "En"
    "Indonesia"      = "Id"
    "Iran"           = "Fa"
    "Iraq"           = "Ar"
    "Ireland"        = "En"
    "Israel"         = "He"
    "Italy"          = "It"
    "Japan"          = "Ja"
    "Korea"          = "Ko"
    "Latin America"  = "Es"
    "Mexico"         = "Es"
    "Netherlands"    = "Nl"
    "New Zealand"    = "En"
    "Norway"         = "No"
    "Peru"           = "Es"
    "Poland"         = "Pl"
    "Portugal"       = "Pt"
    "Romania"        = "Ro"
    "Russia"         = "Ru"
    "Saudi Arabia"   = "Ar"
    "Slovakia"       = "Sk"
    "South Africa"   = "En"
    "Spain"          = "Es"
    "Sweden"         = "Sv"
    "Taiwan"         = "Zh"
    "Turkey"         = "Tr"
    "UAE"            = "Ar"
    "United Kingdom" = "En"
    "USA"            = "En"
    "Vietnam"        = "Vi"
    "World"          = "En"
    "Unknown"        = "En"
}

function Get-LanguageForRegions {
    # Ultimo recurso: primera region (en el orden ya devuelto por
    # Get-Regions/el mapa curado) que tenga un default razonable.
    param([string[]]$Regions)
    foreach ($region in $Regions) {
        if ($regionLanguageDefaults.ContainsKey($region)) { return @($regionLanguageDefaults[$region]) }
    }
    return @()
}

function Resolve-Languages {
    # Cadena de relleno propia (SIN retool-clonelists-metadata - ver paso 9
    # de Build-SystemIndex para el papel de retool ahora, capa de
    # validacion posterior, no de relleno): 1) deteccion por nombre
    # (Get-Languages), 2) default por region (Get-LanguageForRegions, solo
    # regiones no ambiguas). El resultado incluye Source para que quede
    # trazable que un idioma "region-default" es una inferencia, no un dato
    # verificado.
    param([string]$FullName, [string[]]$Regions)

    $byName = Get-Languages -Name $FullName
    if ($byName.Count -gt 0) {
        return @{ Languages = $byName; Source = "name" }
    }
    $byRegion = Get-LanguageForRegions -Regions $Regions
    if ($byRegion.Count -gt 0) {
        return @{ Languages = $byRegion; Source = "region-default" }
    }
    return @{ Languages = @(); Source = "none" }
}

function Get-ParenGroups {
    param([string]$Name)
    $matches = [regex]::Matches($Name, '\(([^()]*)\)')
    return @($matches | ForEach-Object { $_.Groups[1].Value })
}

function Get-Revision {
    # Tag oficial de No-Intro para revisiones corregidas: "(Rev 1)", "(Rev A)".
    # Devuelve la etiqueta cruda (ej. "1", "A"), o $null si no hay tag.
    param([string]$Name)
    $match = [regex]::Match($Name, '\(Rev ([^)]+)\)', 'IgnoreCase')
    if ($match.Success) { return $match.Groups[1].Value }
    return $null
}

function Get-Version {
    # Convencion de aftermarket/homebrew: "(v1.1)", "(v2.100)". Devuelve el
    # numero crudo (ej. "1.1"), o $null si no hay tag. Distinta de Revision
    # (No-Intro oficial) - no se mezclan, cada familia suele usar solo una.
    param([string]$Name)
    $match = [regex]::Match($Name, '\(v([\d.]+[A-Za-z]?)\)', 'IgnoreCase')
    if ($match.Success) { return $match.Groups[1].Value }
    return $null
}

function Test-IsAlt {
    # Dump alternativo del mismo contenido: "(Alt)", "(Alt 2)". A
    # despriorizar/excluir por defecto en una seleccion 1G1R.
    param([string]$Name)
    return [regex]::IsMatch($Name, '\(Alt(?:\s*\d*)?\)', 'IgnoreCase')
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

function Get-Languages {
    # Convencion No-Intro: "Nombre (Region) (Idiomas) (...) (Revision)" - el
    # grupo de idiomas es una lista separada por comas de codigos de 2 letras
    # ("En","Fr","Es"...) que aparece INMEDIATAMENTE despues del grupo de
    # region reconocido. Se usa la posicion relativa a la region (no solo el
    # patron de 2 letras) para evitar falsos positivos - verificado: existen
    # grupos de 2 letras coincidentes con el patron pero que NO son idioma
    # cuando aparecen fuera de esa posicion (ej. "(Ge)" antes de la region en
    # un titulo de NES, no despues). Fuente primaria de la cadena de relleno
    # (ver Resolve-Languages) - Get-LanguageMap (retool) ya no rellena, es
    # una capa de validacion posterior (ver Get-SystemIndex paso 9).
    #
    # Caso compilacion: en cartuchos "Juego A + Juego B" el grupo de idioma
    # tambien puede venir separado por "+" ademas de coma, uno por titulo
    # incluido (ej. "(En,Ja,Fr,De,Es,It+En)" = "En,Ja,Fr,De,Es,It" del primer
    # juego + "En" del segundo) - se trata "+" igual que "," y se deduplica,
    # si no el ultimo token ("It+En") no matchea el patron de 2 letras y
    # descarta el grupo entero, cayendo al idioma por region (bug real
    # encontrado revisando divergencias contra retool en una compilacion).
    param([string]$Name)
    $groups = Get-ParenGroups -Name $Name
    for ($i = 0; $i -lt $groups.Count; $i++) {
        $tokens = $groups[$i] -split '[,+]' | ForEach-Object { $_.Trim() }
        $isRegionGroup = @($tokens | Where-Object { $knownRegions -ccontains $_ }).Count -gt 0
        if (-not $isRegionGroup -or ($i + 1) -ge $groups.Count) { continue }
        $nextTokens = @($groups[$i + 1] -split '[,+]' | ForEach-Object { $_.Trim() } | Select-Object -Unique)
        $allMatchPattern = @($nextTokens | Where-Object { $_ -notmatch '^[A-Z][a-z]$' }).Count -eq 0
        if ($nextTokens.Count -gt 0 -and $allMatchPattern) { return $nextTokens }
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
    # $Lookup tipado como IDictionary (no Hashtable) para aceptar tambien
    # [ordered]@{} sin que PowerShell lo convierta silenciosamente a un
    # Hashtable normal (que perderia el orden de insercion) al pasarlo a
    # una funcion con parametro [hashtable].
    param([string]$Id, [System.Collections.IDictionary]$Lookup, [hashtable]$Memo)

    if ($Memo.ContainsKey($Id)) { return $Memo[$Id] }

    $visited = [System.Collections.Generic.HashSet[string]]::new()
    $current = $Id
    while ($true) {
        if (-not $visited.Add($current)) { break }  # ciclo: cortamos aquí
        $node = $Lookup[$current]
        if (-not $node -or -not $node.CloneOfId -or -not $Lookup.Contains($node.CloneOfId)) {
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

function Add-GamesToLookup {
    # Parsea un DAT Logiqx (full/aftermarket) y anade sus <game> aceptados a
    # $Lookup, namespaceando id/cloneofid por $Origin ("full"/"aftermarket")
    # porque cada pack numera sus id desde 0001 por su cuenta (colision
    # confirmada entre packs del mismo sistema: no son ids globales).
    param(
        [System.Collections.IDictionary]$Lookup,
        [System.Collections.Generic.List[object]]$DiscardedLog,
        [System.Collections.Generic.List[string]]$AcceptedLog,
        [string]$Path,
        [string]$Origin,
        [string]$SystemId
    )
    if (-not $Path) { return }

    [xml]$xml = Get-Content -Raw -Path $Path
    $games = $xml.datafile.game
    if (-not $games) {
        Write-Warning "Sin elementos <game> en '$SystemId' ($Origin): $Path"
        return
    }
    foreach ($game in $games) {
        $fullName = $game.name
        if (-not $fullName -or -not $game.id) { continue }

        $reason = Get-DiscardReason -Name $fullName -Rom $game.rom
        if ($reason) {
            $DiscardedLog.Add([ordered]@{ name = $fullName; reason = $reason; origin = $Origin })
            continue
        }
        $AcceptedLog.Add($fullName)

        $key = "${Origin}:$($game.id)"
        $cloneOfKey = if ($game.cloneofid) { "${Origin}:$($game.cloneofid)" } else { $null }
        $regions = Get-Regions -Name $fullName
        $langResult = Resolve-Languages -FullName $fullName -Regions $regions
        $Lookup[$key] = @{
            Id             = $key
            CloneOfId      = $cloneOfKey
            FullName       = $fullName
            BaseName       = Get-BaseName -Name $fullName
            Origin         = $Origin
            Regions        = $regions
            Languages      = $langResult.Languages
            LanguageSource = $langResult.Source
            Category       = Get-Category -Name $fullName
            Revision       = Get-Revision -Name $fullName
            Version        = Get-Version -Name $fullName
            IsAlt          = Test-IsAlt -Name $fullName
        }
    }
}

function Add-PcGamesToLookup {
    # Parsea el pack pc/ (Parent-Clone): cloneof="<nombre completo del
    # padre>", sin atributo id. Se usa el propio nombre completo del <game>
    # como clave (unico dentro del DAT por construccion de No-Intro), asi
    # Get-RootId funciona sin cambios sobre este lookup igual que sobre el
    # de full+aftermarket (namespaceado por id). Usado en -SourceMode Pc y
    # Merged.
    param(
        [System.Collections.IDictionary]$Lookup,
        [System.Collections.Generic.List[object]]$DiscardedLog,
        [System.Collections.Generic.List[string]]$AcceptedLog,
        [string]$Path,
        [string]$SystemId
    )
    if (-not $Path) { return }

    [xml]$xml = Get-Content -Raw -Path $Path
    $games = $xml.datafile.game
    if (-not $games) {
        Write-Warning "Sin elementos <game> en '$SystemId' (pc): $Path"
        return
    }
    foreach ($game in $games) {
        $fullName = $game.name
        if (-not $fullName) { continue }

        $reason = Get-DiscardReason -Name $fullName -Rom $game.rom
        if ($reason) {
            $DiscardedLog.Add([ordered]@{ name = $fullName; reason = $reason; origin = "pc" })
            continue
        }
        $AcceptedLog.Add($fullName)

        $regions = Get-Regions -Name $fullName
        $langResult = Resolve-Languages -FullName $fullName -Regions $regions
        $Lookup[$fullName] = @{
            Id             = $fullName
            CloneOfId      = if ($game.cloneof) { $game.cloneof } else { $null }
            FullName       = $fullName
            BaseName       = Get-BaseName -Name $fullName
            Origin         = "pc"
            Regions        = $regions
            Languages      = $langResult.Languages
            LanguageSource = $langResult.Source
            Category       = Get-Category -Name $fullName
            Revision       = Get-Revision -Name $fullName
            Version        = Get-Version -Name $fullName
            IsAlt          = Test-IsAlt -Name $fullName
        }
    }
}

function New-EmptyFamily {
    param([string]$CanonicalName)
    return @{
        CanonicalName = $CanonicalName
        AliasNames    = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
        Regions       = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
        Languages     = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
        Categories    = [System.Collections.Generic.HashSet[string]]::new([System.StringComparer]::OrdinalIgnoreCase)
        # Detalle por-clon (necesario para 1G1R por idioma+region: el
        # agregado de arriba solo dice QUE existe tal region/idioma en la
        # familia, no QUE clon concreto lo tiene).
        Members       = New-Object System.Collections.Generic.List[object]
    }
}

function Add-NodeToFamily {
    param([hashtable]$Family, $Node)
    if ($Node.BaseName -ne $Family.CanonicalName) { [void]$Family.AliasNames.Add($Node.BaseName) }
    foreach ($r in $Node.Regions) { [void]$Family.Regions.Add($r) }
    foreach ($l in $Node.Languages) { [void]$Family.Languages.Add($l) }
    [void]$Family.Categories.Add($Node.Category)
    $Family.Members.Add([ordered]@{
        name           = $Node.FullName
        origin         = $Node.Origin
        regions        = @($Node.Regions | Sort-Object)
        languages      = @($Node.Languages | Sort-Object)
        languageSource = $Node.LanguageSource
        category       = $Node.Category
        revision       = $Node.Revision
        version        = $Node.Version
        isAlt          = $Node.IsAlt
    })
}

function Build-Families {
    # Resuelve la raiz de familia (parent/clone) de cada nodo de $Lookup via
    # Get-RootId (generico: solo necesita .Id/.CloneOfId, sirve igual para
    # el lookup namespaceado full+aftermarket que para el de pc/ por nombre).
    param([System.Collections.IDictionary]$Lookup)

    $memo = @{}
    $families = [ordered]@{}  # rootId -> familia (ver New-EmptyFamily)
    $canonicalByNodeId = @{}

    foreach ($node in $Lookup.Values) {
        if (-not $node.BaseName) { continue }

        $rootId = Get-RootId -Id $node.Id -Lookup $Lookup -Memo $memo
        $rootNode = $Lookup[$rootId]
        $canonicalName = $rootNode.BaseName
        $canonicalByNodeId[$node.Id] = $canonicalName

        if (-not $families.Contains($rootId)) {
            $families[$rootId] = New-EmptyFamily -CanonicalName $canonicalName
        }
        Add-NodeToFamily -Family $families[$rootId] -Node $node
    }

    return [ordered]@{ Families = $families; CanonicalByNodeId = $canonicalByNodeId }
}

function Build-SystemIndex {
    param([string]$Id, [hashtable]$Entry)

    $isNoIntro = $Entry.Source -eq "No-Intro"
    $aftermarketPath = $null
    $pcPath = $null

    if ($isNoIntro) {
        $fullPath = Resolve-NoIntroDat -BaseName $Entry.BaseName -Pack "full"
        if (-not $fullPath) {
            Write-Warning "DAT no encontrado para '$Id' (No-Intro, base '$($Entry.BaseName)') en sources/dats/no-intro/full/. ¿Falta ejecutar update-sources.ps1?"
            return
        }
        $aftermarketPath = Resolve-NoIntroDat -BaseName $Entry.BaseName -Pack "aftermarket" -Tag "(Aftermarket)"
        $pcPath = Resolve-NoIntroDat -BaseName $Entry.BaseName -Pack "pc" -Tag "(Parent-Clone)"
    } else {
        $fullPath = Join-Path $DatRoot "$($Entry.Source)\$($Entry.Dat)"
        if (-not (Test-Path $fullPath)) {
            Write-Warning "DAT no encontrado para '$Id': $fullPath"
            return
        }
    }

    # 0) Mapa de idiomas curado por retool-clonelists-metadata: YA NO es
    # fuente de relleno (ver Resolve-Languages, cadena propia por
    # nombre+region). Se usa mas abajo (paso 9) como capa de validacion
    # posterior - divergencias entre lo calculado y lo que dice retool.
    $languageMap = @{}
    if ($isNoIntro) {
        $languageMapPath = Resolve-MetadataPath -BaseName $Entry.BaseName
        $languageMap = Get-LanguageMap -Path $languageMapPath
    }

    # 1) Filtrar descartes y construir lookup full+aftermarket (id
    # namespaceado por origen) y lookup pc (nombre completo como clave). Se
    # parsean ambos siempre -salvo pc/ si no existe para el sistema- porque
    # el contraste informativo (paso 7) los necesita sin importar el modo.
    # [ordered]@{} (no @{} normal): un Hashtable normal itera en orden de
    # bucket hash, no de insercion, lo que puede hacer que dos familias con
    # el mismo nombre base por coincidencia (raro pero real - ver caso NES
    # "Lion King, The" duplicado entre full y una entrada sin cloneofid)
    # resuelvan de forma no determinista cual "gana" en el merge de alias
    # manual del paso 3 (ultimo-en-sobrescribir, orden indefinido).
    $famLookup = [ordered]@{}
    $famDiscardedLog = New-Object System.Collections.Generic.List[object]
    $famAcceptedLog = New-Object System.Collections.Generic.List[string]
    Add-GamesToLookup -Lookup $famLookup -DiscardedLog $famDiscardedLog -AcceptedLog $famAcceptedLog -Path $fullPath -Origin "full" -SystemId $Id
    Add-GamesToLookup -Lookup $famLookup -DiscardedLog $famDiscardedLog -AcceptedLog $famAcceptedLog -Path $aftermarketPath -Origin "aftermarket" -SystemId $Id

    $pcLookup = [ordered]@{}
    $pcDiscardedLog = New-Object System.Collections.Generic.List[object]
    $pcAcceptedLog = New-Object System.Collections.Generic.List[string]
    if ($pcPath) {
        Add-PcGamesToLookup -Lookup $pcLookup -DiscardedLog $pcDiscardedLog -AcceptedLog $pcAcceptedLog -Path $pcPath -SystemId $Id
    }

    # -SourceMode Pc/Merged requieren pc/; si el sistema no tiene pack pc/
    # se degrada a FullAftermarket avisando (aftermarket/pc no cubren todos
    # los sistemas del manifiesto).
    $effectiveMode = $SourceMode
    if ($effectiveMode -in @("Pc", "Merged") -and -not $pcPath) {
        Write-Warning "Modo '$effectiveMode' pedido para '$Id' pero no hay pack pc/ disponible - se usa FullAftermarket"
        $effectiveMode = "FullAftermarket"
    }

    if ($effectiveMode -eq "Pc") {
        if ($pcLookup.Count -eq 0) {
            Write-Warning "Sin elementos <game> validos en '$Id' (pc): $pcPath"
            return
        }
        $lookup = $pcLookup
        $discardedLog = $pcDiscardedLog
        $acceptedLog = $pcAcceptedLog
    } else {
        if ($famLookup.Count -eq 0) {
            Write-Warning "Sin elementos <game> validos en '$Id': $fullPath"
            return
        }
        $lookup = $famLookup
        $discardedLog = $famDiscardedLog
        $acceptedLog = $famAcceptedLog
    }

    # 2) Resolver raíz de familia (parent/clone) sobre la fuente activa.
    $built = Build-Families -Lookup $lookup
    $families = $built.Families
    $canonicalByNodeId = $built.CanonicalByNodeId

    # 2b) -SourceMode Merged: completar el arbol full+aftermarket con las
    # familias que solo existen en pc/ (mismo criterio que el contraste del
    # paso 7 - onlyInPc), usando los datos de pc/ para esas entradas.
    $mergedCount = 0
    if ($effectiveMode -eq "Merged" -and $pcLookup.Count -gt 0) {
        $famAcceptedSet = [System.Collections.Generic.HashSet[string]]::new([string[]]$famAcceptedLog, [System.StringComparer]::Ordinal)
        $pcBuilt = Build-Families -Lookup $pcLookup
        $familyByCanonical = @{}
        foreach ($key in $families.Keys) { $familyByCanonical[$families[$key].CanonicalName] = $families[$key] }

        foreach ($pcNode in $pcLookup.Values) {
            if ($famAcceptedSet.Contains($pcNode.FullName)) { continue }  # ya cubierto por full+aftermarket

            $pcCanonical = $pcBuilt.CanonicalByNodeId[$pcNode.Id]
            if (-not $familyByCanonical.ContainsKey($pcCanonical)) {
                $newKey = "pc:$pcCanonical"
                $families[$newKey] = New-EmptyFamily -CanonicalName $pcCanonical
                $familyByCanonical[$pcCanonical] = $families[$newKey]
            }
            Add-NodeToFamily -Family $familyByCanonical[$pcCanonical] -Node $pcNode
            $canonicalByNodeId[$pcNode.Id] = $pcCanonical
            $acceptedLog.Add($pcNode.FullName)
            $mergedCount++
        }
    }

    # 3) Cargar fichero de alias manual (si existe) y fusionar
    $aliasPath = Join-Path $AliasRoot "$Id.json"
    $manualAliases = @()
    if (Test-Path $aliasPath) {
        $existing = Get-Content -Raw -Path $aliasPath | ConvertFrom-Json
        if ($existing.aliases) { $manualAliases = @($existing.aliases) }
    }

    # Índice canonical -> family, para fusionar por nombre. Nota: dos raíces
    # cloneofid distintas pueden compartir CanonicalName por coincidencia de
    # título entre juegos NO relacionados (frecuente con títulos genéricos:
    # "Baseball", "Tetris"...) sin que eso sea un problema - son entradas
    # legítimamente distintas en el índice final, que sí admite "name"
    # repetido. Solo importa cuando un alias MANUAL referencia ese nombre de
    # forma ambigua (ver aviso dentro del bucle de fusión más abajo).
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
                foreach ($l in $otherFamily.Languages) { [void]$targetFamily.Languages.Add($l) }
                foreach ($c in $otherFamily.Categories) { [void]$targetFamily.Categories.Add($c) }
                foreach ($m in $otherFamily.Members) { $targetFamily.Members.Add($m) }
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
            languages  = @($_.Languages | Sort-Object)
            properties = [ordered]@{ category = $finalCategory }
            members    = @($_.Members | Sort-Object { $_.name })
        }
    })

    $output = [ordered]@{
        system         = $Id
        source         = $Entry.Source
        sourceMode     = $effectiveMode
        dat            = if ($effectiveMode -eq "Pc") { Split-Path -Leaf $pcPath } else { Split-Path -Leaf $fullPath }
        datAftermarket = if ($effectiveMode -ne "Pc" -and $aftermarketPath) { Split-Path -Leaf $aftermarketPath } else { $null }
        datPc          = if ($effectiveMode -in @("Pc", "Merged") -and $pcPath) { Split-Path -Leaf $pcPath } else { $null }
        generated      = (Get-Date -Format "yyyy-MM-dd")
        games          = @($gamesOut)
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

    # 7) Informe de contraste bidireccional entre full+aftermarket y pc/,
    # calculado siempre sobre los datos "pristinos" (fam*/pc*), sin importar
    # -SourceMode - en Merged, $acceptedLog ya incluye lo fusionado y dejaria
    # el contraste vacio si se calculase sobre el, por eso se usa famAcceptedLog.
    # Puramente informativo, no bloquea la build.
    $pcNote = "sin pc/"
    if ($pcPath) {
        $famAcceptedSet = [System.Collections.Generic.HashSet[string]]::new([string[]]$famAcceptedLog, [System.StringComparer]::Ordinal)
        $pcAcceptedSet = [System.Collections.Generic.HashSet[string]]::new([string[]]$pcAcceptedLog, [System.StringComparer]::Ordinal)
        $onlyInPc = @($pcAcceptedSet | Where-Object { -not $famAcceptedSet.Contains($_) } | Sort-Object)
        $onlyInFullAftermarket = @($famAcceptedSet | Where-Object { -not $pcAcceptedSet.Contains($_) } | Sort-Object)
        if ($onlyInPc.Count -gt 0 -or $onlyInFullAftermarket.Count -gt 0) {
            $contrastOutput = [ordered]@{
                system                = $Id
                pc                    = (Split-Path -Leaf $pcPath)
                onlyInPc              = $onlyInPc
                onlyInFullAftermarket = $onlyInFullAftermarket
            }
            Write-JsonFile -Path (Join-Path $DebugRoot "$Id-pc-contrast.json") -Data $contrastOutput
        }
        $pcNote = "pc contraste: $($onlyInPc.Count) solo-pc / $($onlyInFullAftermarket.Count) solo-full+aftermarket"
        if ($effectiveMode -eq "Merged") { $pcNote += " ($mergedCount fusionados)" }
    }

    # 8) Validación cruzada contra el clonelist de retool-clonelists-metadata
    # (metadata/dat/retool/clonelists/): capa de refuerzo, NO sustituye al
    # arbol cloneofid en No-Intro (a diferencia de Redump, ver
    # build-dat-index-redump.ps1). Solo se registran divergencias.
    $clonelistNote = "sin clonelist"
    if ($isNoIntro) {
        $clonelistPath = Resolve-ClonelistPath -BaseName $Entry.BaseName
        $clonelistMap = Get-ClonelistMap -Path $clonelistPath
        if ($clonelistMap.Count -gt 0) {
            $diffs = New-Object System.Collections.Generic.List[object]
            foreach ($node in $lookup.Values) {
                if (-not $clonelistMap.ContainsKey($node.BaseName)) { continue }
                $clonelistGroup = $clonelistMap[$node.BaseName]
                $cloneofidGroup = $canonicalByNodeId[$node.Id]
                if ($clonelistGroup -ne $cloneofidGroup) {
                    $diffs.Add([ordered]@{
                        baseName        = $node.BaseName
                        cloneofidFamily = $cloneofidGroup
                        clonelistGroup  = $clonelistGroup
                    })
                }
            }
            if ($diffs.Count -gt 0) {
                $diffOutput = [ordered]@{
                    system    = $Id
                    clonelist = (Split-Path -Leaf $clonelistPath)
                    diffs     = @($diffs | Sort-Object baseName)
                }
                Write-JsonFile -Path (Join-Path $DebugRoot "$Id-clonelist-diff.json") -Data $diffOutput
            }
            $clonelistNote = "clonelist: $($diffs.Count) divergencias"
        }
    }

    # 9) Validación de idioma contra retool-clonelists-metadata: capa
    # OPCIONAL y POSTERIOR al calculo propio (Resolve-Languages, paso 1) -
    # retool ya NO rellena el campo languages, solo sirve para detectar
    # divergencias entre lo calculado (nombre + default por region) y lo
    # que dice retool, por cada clon individual (mas granular que el
    # clonelist-diff del paso 8, que compara por baseName de familia).
    $languageNote = "sin metadata idioma"
    if ($languageMap.Count -gt 0) {
        $langDiffs = New-Object System.Collections.Generic.List[object]
        foreach ($node in $lookup.Values) {
            if (-not $languageMap.ContainsKey($node.FullName)) { continue }
            $retoolLanguages = @($languageMap[$node.FullName] | Sort-Object)
            # "nolang" es un marcador especial de retool ("sin contenido de
            # texto", no un codigo de idioma real - 17266 casos en todo
            # retool-clonelists-metadata, no es raro: juegos genuinamente sin
            # texto). Nuestro algoritmo nunca puede "acertarlo" porque no hay
            # ninguna senal textual de "sin idioma" en el nombre - se excluye
            # de la comparacion, no es una divergencia real.
            if ($retoolLanguages -contains "nolang") { continue }
            $computedLanguages = @($node.Languages | Sort-Object)
            if (@(Compare-Object $retoolLanguages $computedLanguages).Count -gt 0) {
                $langDiffs.Add([ordered]@{
                    name               = $node.FullName
                    computedLanguages  = $computedLanguages
                    computedSource     = $node.LanguageSource
                    retoolLanguages    = $retoolLanguages
                })
            }
        }
        if ($langDiffs.Count -gt 0) {
            $langDiffOutput = [ordered]@{
                system   = $Id
                metadata = (Split-Path -Leaf $languageMapPath)
                diffs    = @($langDiffs | Sort-Object name)
            }
            Write-JsonFile -Path (Join-Path $DebugRoot "$Id-language-diff.json") -Data $langDiffOutput
        }
        $languageNote = "idioma: $($langDiffs.Count) divergencias"
    }

    Write-Host "Generado: $Id.json [$effectiveMode] ($($gamesOut.Count) familias, $($discardedLog.Count) descartados) + aliases/$Id.json ($($aliasesOut.Count) con alias) [$pcNote] [$clonelistNote] [$languageNote]"
}

$ids = if ($SystemId) { @($SystemId) } else { $datMap.Keys }

foreach ($id in $ids) {
    if (-not $datMap.Contains($id)) {
        Write-Warning "Sistema no mapeado: $id"
        continue
    }
    Build-SystemIndex -Id $id -Entry $datMap[$id]
}
