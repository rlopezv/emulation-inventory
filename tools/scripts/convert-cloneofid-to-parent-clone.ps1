<#
Conversor generico e independiente: recibe uno o varios DAT Logiqx que usan
el esquema Standard (id/cloneofid numericos - full/aftermarket de No-Intro,
o cualquier otro DAT con ese mismo esquema) y devuelve un unico DAT Logiqx
fusionado en esquema Parent-Clone (cloneof="<nombre completo del padre>",
sin atributo id), que es el que acepta Retool para resolver relaciones
parent/clone (Retool no interpreta id/cloneofid).

No depende del pipeline de dat-index ni del manifiesto de sistemas
(tools/scripts/config/nointro-systems.json) - es pura transformacion de
esquema DAT a DAT, no aplica ninguna curacion propia (no descarta Proto/
Demo/Beta/etc., eso es trabajo de Retool aguas abajo via sus flags y
clonelist). Preserva todos los <game> de todos los ficheros de entrada.

Fusion de varios ficheros de entrada: los id NO son globales entre DAT (cada
fichero numera desde 0001 por su cuenta - colision confirmada entre full/ y
aftermarket/ del mismo sistema en No-Intro), asi que se namespacean por
origen (nombre base del fichero de entrada) antes de resolver el arbol
combinado. Un <game> sin atributo id se conserva igualmente (namespaceado
por su propio nombre) pero no puede participar como cloneofid de otro ni
seguir una cadena cloneofid (no tiene id que seguir).

Resolucion de raiz: igual que build-dat-index-nointro.ps1 (cadena
cloneofid hasta el nodo raiz, memoizada, a prueba de ciclos), pero SIN
agrupar por nombre base ni colapsar variantes regionales en alias - cada
<game> de entrada se conserva como <game> independiente en la salida, con
cloneof apuntando al NOMBRE COMPLETO (no al nombre base) del juego raiz de
su cadena. Esto es intencional: el pc/ oficial de No-Intro tampoco colapsa
variantes, solo enlaza clones entre si.

Limitacion conocida: el pc/ oficial de No-Intro incluye <release
region="..."/> con codigos de region reales de su base de datos interna,
que este script no tiene. Se aproxima con Get-Regions (mismo detector de
tokens de region por nombre que build-dat-index-nointro.ps1) - un solo
<release> por juego con la primera region detectada, o "Unknown" si no se
detecta ninguna. No es una replica byte a byte del pc/ oficial, es
funcionalmente equivalente para que Retool resuelva cloneof correctamente.

Cabecera <url>: Retool identifica el DAT leyendo <name>/<url> para buscar el
clonelist correspondiente en su carpeta clonelists/ (ver docs/guides/tools/
1g1r-filtering.md#mecanismo-de-las-clonelist). Sin <url>, Retool puede no
localizar el clonelist adecuado y caer a una deteccion mas pobre que no
capta retitulados regionales muy divergentes (ej. visto en NES: "1943 - The
Battle of Midway (USA)"/"1943 - The Battle of Valhalla (Japan)" - el cloneof
del DAT generado SI era correcto, pero sin <url> Retool no aplico el
clonelist que agrupa ambos titulos explicitamente). Por defecto se rellena
con "https://www.no-intro.org" (fuente habitual de los DAT de entrada);
ajustar con -Url si el origen es otro.

Uso:
    pwsh tools/scripts/convert-cloneofid-to-parent-clone.ps1 -InputDat "full.dat","aftermarket.dat" -OutputDat "salida (Parent-Clone).dat"
    pwsh tools/scripts/convert-cloneofid-to-parent-clone.ps1 -InputDat "full.dat" -OutputDat "salida.dat" -Name "Mi Sistema"
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string[]]$InputDat,

    [Parameter(Mandatory = $true)]
    [string]$OutputDat,

    [string]$Name,

    [string]$Url = "https://www.no-intro.org"
)

# Mismo detector de tokens de region que build-dat-index-nointro.ps1
# (lista cerrada, auditada contra los DAT de No-Intro/Non-Redump).
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
    param([string]$Str)
    $matches = [regex]::Matches($Str, '\(([^()]*)\)')
    return @($matches | ForEach-Object { $_.Groups[1].Value })
}

function Get-FirstRegion {
    param([string]$GameName)
    foreach ($group in (Get-ParenGroups -Str $GameName)) {
        $tokens = $group -split '[,+]' | ForEach-Object { $_.Trim() }
        $matched = @($tokens | Where-Object { $knownRegions -ccontains $_ })
        if ($matched.Count -gt 0) { return $matched[0] }
    }
    return "Unknown"
}

function Get-RootKey {
    # Cadena cloneofid hasta la raiz, memoizada, a prueba de ciclos - igual
    # que Get-RootId en build-dat-index-nointro.ps1.
    param([string]$Key, [hashtable]$Lookup, [hashtable]$Memo)

    if ($Memo.ContainsKey($Key)) { return $Memo[$Key] }

    $visited = [System.Collections.Generic.HashSet[string]]::new()
    $current = $Key
    while ($true) {
        if (-not $visited.Add($current)) { break }  # ciclo: cortamos aqui
        $node = $Lookup[$current]
        if (-not $node -or -not $node.CloneOfKey -or -not $Lookup.ContainsKey($node.CloneOfKey)) {
            break
        }
        $current = $node.CloneOfKey
    }
    $Memo[$Key] = $current
    return $current
}

function Write-JsonEscapedXmlText {
    # Escapa el texto para insertarlo como contenido/atributo XML.
    param([string]$Text)
    if ($null -eq $Text) { return "" }
    return [System.Security.SecurityElement]::Escape($Text)
}

# 1) Parsear todos los ficheros de entrada, namespaceando por nombre base
# del fichero para evitar colision de id entre ficheros distintos.
$lookup = [ordered]@{}
$originNames = New-Object System.Collections.Generic.List[string]

foreach ($path in $InputDat) {
    if (-not (Test-Path $path)) {
        throw "No existe el fichero de entrada: $path"
    }
    $origin = [System.IO.Path]::GetFileNameWithoutExtension($path)
    $originNames.Add($origin)

    [xml]$xml = Get-Content -Raw -Path $path
    $games = $xml.datafile.game
    if (-not $games) {
        Write-Warning "Sin elementos <game> en '$path' - se omite"
        continue
    }

    foreach ($game in $games) {
        $fullName = $game.name
        if (-not $fullName) { continue }

        $localKey = if ($game.id) { $game.id } else { "name:$fullName" }
        $key = "${origin}:${localKey}"
        $cloneOfKey = if ($game.id -and $game.cloneofid) { "${origin}:$($game.cloneofid)" } else { $null }

        $roms = @($game.rom | Where-Object { $_ })

        $lookup[$key] = @{
            Key        = $key
            CloneOfKey = $cloneOfKey
            FullName   = $fullName
            Roms       = $roms
            Region     = Get-FirstRegion -GameName $fullName
        }
    }
}

if ($lookup.Count -eq 0) {
    throw "Ningun <game> valido en los ficheros de entrada indicados."
}

# 2) Resolver raiz de cada <game> (por nombre completo del <game> raiz, NO
# por nombre base - pc/ oficial tampoco colapsa variantes regionales).
$memo = @{}
$rootNameByKey = @{}
foreach ($node in $lookup.Values) {
    $rootKey = Get-RootKey -Key $node.Key -Lookup $lookup -Memo $memo
    $rootNameByKey[$node.Key] = $lookup[$rootKey].FullName
}

# 3) Construir el XML de salida en esquema Parent-Clone.
$sb = New-Object System.Text.StringBuilder
[void]$sb.AppendLine('<?xml version="1.0"?>')
[void]$sb.AppendLine('<datafile xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="https://datomatic.no-intro.org/stuff https://datomatic.no-intro.org/stuff/schema_nointro_datfile_v4.xsd">')

$headerName = if ($Name) { $Name } else { ($originNames -join " + ") + " (Parent-Clone, generado)" }
$headerNameEscaped = Write-JsonEscapedXmlText -Text $headerName
$today = Get-Date -Format "yyyyMMdd-HHmmss"

[void]$sb.AppendLine("`t<header>")
[void]$sb.AppendLine("`t`t<name>$headerNameEscaped</name>")
[void]$sb.AppendLine("`t`t<description>$headerNameEscaped</description>")
[void]$sb.AppendLine("`t`t<version>$today</version>")
[void]$sb.AppendLine("`t`t<date>$today</date>")
[void]$sb.AppendLine("`t`t<url>$(Write-JsonEscapedXmlText -Text $Url)</url>")
[void]$sb.AppendLine("`t`t<homepage>Generado por convert-cloneofid-to-parent-clone.ps1 a partir de: $(Write-JsonEscapedXmlText -Text ($originNames -join ', '))</homepage>")
[void]$sb.AppendLine("`t</header>")

foreach ($node in ($lookup.Values | Sort-Object FullName)) {
    $nameEscaped = Write-JsonEscapedXmlText -Text $node.FullName
    $rootName = $rootNameByKey[$node.Key]
    $isRoot = ($rootName -eq $node.FullName)

    if ($isRoot) {
        [void]$sb.AppendLine("`t<game name=`"$nameEscaped`">")
    } else {
        $cloneofEscaped = Write-JsonEscapedXmlText -Text $rootName
        [void]$sb.AppendLine("`t<game name=`"$nameEscaped`" cloneof=`"$cloneofEscaped`">")
    }
    [void]$sb.AppendLine("`t`t<description>$nameEscaped</description>")
    [void]$sb.AppendLine("`t`t<release name=`"$nameEscaped`" region=`"$($node.Region)`"/>")
    foreach ($rom in $node.Roms) {
        $romAttrs = New-Object System.Collections.Generic.List[string]
        foreach ($attrName in @("name", "size", "crc", "md5", "sha1", "status")) {
            $value = $rom.$attrName
            if ($value) {
                $romAttrs.Add("$attrName=`"$(Write-JsonEscapedXmlText -Text $value)`"")
            }
        }
        [void]$sb.AppendLine("`t`t<rom $($romAttrs -join ' ')/>")
    }
    [void]$sb.AppendLine("`t</game>")
}

[void]$sb.AppendLine('</datafile>')

$dir = Split-Path -Parent $OutputDat
if ($dir -and -not (Test-Path $dir)) { New-Item -ItemType Directory -Path $dir -Force | Out-Null }
[System.IO.File]::WriteAllText($OutputDat, $sb.ToString(), [System.Text.UTF8Encoding]::new($false))

$rootCount = @($rootNameByKey.Values | Select-Object -Unique).Count
Write-Host "Generado: $OutputDat ($($lookup.Count) juegos, $rootCount familias) desde $($InputDat.Count) fichero(s): $($originNames -join ', ')"
