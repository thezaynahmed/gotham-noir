# Gotham Noir Installer for Windows Terminal (Store, Preview, Unpackaged) + PowerShell
[CmdletBinding()]
param(
    [string]$Variant = "Year One",
    [string]$SettingsPath = "",
    [string]$FragmentDir = "",
    [switch]$SkipFragment,
    [switch]$SkipSettings
)

$ErrorActionPreference = "Stop"

function Remove-JsonComments {
    param([Parameter(Mandatory)][string]$JsonText)
    $sb = [System.Text.StringBuilder]::new($JsonText.Length)
    $inString = $false
    $escaped = $false
    $inLine = $false
    $inBlock = $false
    $len = $JsonText.Length
    for ($i = 0; $i -lt $len; $i++) {
        $ch = $JsonText[$i]
        $next = if ($i + 1 -lt $len) { $JsonText[$i + 1] } else { [char]0 }
        if ($inLine) {
            if ($ch -eq [char]10) {
                $inLine = $false
                [void]$sb.Append($ch)
            } elseif ($ch -eq [char]13 -and $next -eq [char]10) {
                $inLine = $false
                [void]$sb.Append($ch)
            }
            continue
        }
        if ($inBlock) {
            if ($ch -eq [char]42 -and $next -eq [char]47) {
                $inBlock = $false
                $i++
            }
            continue
        }
        if ($inString) {
            [void]$sb.Append($ch)
            if ($escaped) {
                $escaped = $false
            } elseif ($ch -eq [char]92) {
                $escaped = $true
            } elseif ($ch -eq [char]34) {
                $inString = $false
            }
            continue
        }
        if ($ch -eq [char]34) {
            $inString = $true
            [void]$sb.Append($ch)
        } elseif ($ch -eq [char]47 -and $next -eq [char]47) {
            $inLine = $true
            $i++
        } elseif ($ch -eq [char]47 -and $next -eq [char]42) {
            $inBlock = $true
            $i++
        } else {
            [void]$sb.Append($ch)
        }
    }
    return $sb.ToString()
}

$VariantMap = @{
    "year-one"                  = "Gotham Noir - Year One"
    "year one"                  = "Gotham Noir - Year One"
    "gotham noir - year one"    = "Gotham Noir - Year One"
    "batcomputer"               = "Gotham Noir - Batcomputer"
    "gotham noir - batcomputer" = "Gotham Noir - Batcomputer"
    "arkham-slate"              = "Gotham Noir - Arkham Slate"
    "arkham slate"              = "Gotham Noir - Arkham Slate"
    "arkham"                    = "Gotham Noir - Arkham Slate"
    "gotham noir - arkham slate"= "Gotham Noir - Arkham Slate"
    "vengeance"                 = "Gotham Noir - Vengeance"
    "gotham noir - vengeance"   = "Gotham Noir - Vengeance"
}
$lookupKey = $Variant.Trim().ToLowerInvariant()
if ($VariantMap.ContainsKey($lookupKey)) {
    $TargetScheme = $VariantMap[$lookupKey]
} else {
    $TargetScheme = "Gotham Noir - Year One"
}

$GothamPayload = @'
{
  "schemes": [
    {
      "name": "Gotham Noir - Year One",
      "background": "#15171a",
      "foreground": "#d8d6cf",
      "cursorColor": "#f0c946",
      "selectionBackground": "#323a46",
      "black": "#15171a",
      "red": "#e86a74",
      "green": "#63c794",
      "yellow": "#f0c946",
      "blue": "#74aeeb",
      "purple": "#b695e8",
      "cyan": "#68c5ce",
      "white": "#d8d6cf",
      "brightBlack": "#878d96",
      "brightRed": "#f28b94",
      "brightGreen": "#7ed8a9",
      "brightYellow": "#f7d96d",
      "brightBlue": "#93c2f2",
      "brightPurple": "#c8aef0",
      "brightCyan": "#84d6de",
      "brightWhite": "#eceae4"
    },
    {
      "name": "Gotham Noir - Batcomputer",
      "background": "#101215",
      "foreground": "#dce0e5",
      "cursorColor": "#f5d042",
      "selectionBackground": "#2b3440",
      "black": "#101215",
      "red": "#ee6b78",
      "green": "#56cca0",
      "yellow": "#f5d042",
      "blue": "#72b4f5",
      "purple": "#bc9bf0",
      "cyan": "#5ecad6",
      "white": "#dce0e5",
      "brightBlack": "#828a96",
      "brightRed": "#f68e99",
      "brightGreen": "#73dcb5",
      "brightYellow": "#fae06c",
      "brightBlue": "#94c8fa",
      "brightPurple": "#ceb4f5",
      "brightCyan": "#7fdae3",
      "brightWhite": "#eff2f6"
    },
    {
      "name": "Gotham Noir - Arkham Slate",
      "background": "#1d1f21",
      "foreground": "#dad5c7",
      "cursorColor": "#e6c15a",
      "selectionBackground": "#373e47",
      "black": "#1d1f21",
      "red": "#e37370",
      "green": "#88c082",
      "yellow": "#e6c15a",
      "blue": "#80b0dc",
      "purple": "#bc9cd9",
      "cyan": "#74bfbd",
      "white": "#dad5c7",
      "brightBlack": "#929690",
      "brightRed": "#ec918f",
      "brightGreen": "#a0cfa0",
      "brightYellow": "#eed27e",
      "brightBlue": "#9dc3e6",
      "brightPurple": "#ceb4e5",
      "brightCyan": "#92d1cf",
      "brightWhite": "#ece7da"
    },
    {
      "name": "Gotham Noir - Vengeance",
      "background": "#151417",
      "foreground": "#ddd8d5",
      "cursorColor": "#e5535c",
      "selectionBackground": "#3a2c33",
      "black": "#151417",
      "red": "#ef6c74",
      "green": "#6ec798",
      "yellow": "#e8be54",
      "blue": "#7baee6",
      "purple": "#be9ae6",
      "cyan": "#6fc2ca",
      "white": "#ddd8d5",
      "brightBlack": "#918994",
      "brightRed": "#f68e94",
      "brightGreen": "#87d7ad",
      "brightYellow": "#f2ce74",
      "brightBlue": "#9ac2ee",
      "brightPurple": "#cfb2ee",
      "brightCyan": "#8ad2d9",
      "brightWhite": "#f0ecea"
    }
  ]
}
'@
$ParsedPayload = $GothamPayload | ConvertFrom-Json
$GothamNames = @($ParsedPayload.schemes | ForEach-Object { $_.name })

if (-not $SkipFragment) {
    if ([string]::IsNullOrWhiteSpace($FragmentDir)) {
        $FragmentDir = Join-Path $env:LOCALAPPDATA "Microsoft\Windows Terminal\Fragments\gotham-noir"
    }
    New-Item -ItemType Directory -Path $FragmentDir -Force | Out-Null
    $FragmentFile = Join-Path $FragmentDir "themes.json"
    [System.IO.File]::WriteAllText($FragmentFile, ($ParsedPayload | ConvertTo-Json -Depth 10) + "`n", [System.Text.UTF8Encoding]::new($false))
    Write-Host "Wrote Windows Terminal fragment extension: $FragmentFile"
}

if (-not $SkipSettings) {
    if ([string]::IsNullOrWhiteSpace($SettingsPath)) {
        $Candidates = @(
            (Join-Path $env:LOCALAPPDATA "Packages\Microsoft.WindowsTerminal_8wekyb3d8bbwe\LocalState\settings.json"),
            (Join-Path $env:LOCALAPPDATA "Packages\Microsoft.WindowsTerminalPreview_8wekyb3d8bbwe\LocalState\settings.json"),
            (Join-Path $env:LOCALAPPDATA "Microsoft\Windows Terminal\settings.json")
        )
        $SettingsPath = $Candidates | Where-Object { Test-Path $_ } | Select-Object -First 1
        if (-not $SettingsPath) { $SettingsPath = $Candidates[0] }
    }

    $SettingsParent = Split-Path -Parent $SettingsPath
    if (-not [string]::IsNullOrWhiteSpace($SettingsParent)) {
        New-Item -ItemType Directory -Path $SettingsParent -Force | Out-Null
    }

    if (Test-Path $SettingsPath) {
        Copy-Item -Path $SettingsPath -Destination "$SettingsPath.bak" -Force
        $RawJson = [System.IO.File]::ReadAllText($SettingsPath, [System.Text.UTF8Encoding]::new($false)).TrimStart([char]0xFEFF)
        $CleanJson = Remove-JsonComments -JsonText $RawJson
        if ([string]::IsNullOrWhiteSpace($CleanJson)) { $CleanJson = "{}" }
        $SettingsObj = $CleanJson | ConvertFrom-Json
    } else {
        $SettingsObj = [PSCustomObject]@{}
    }

    $ExistingSchemes = @()
    if ($SettingsObj.PSObject.Properties["schemes"] -and $SettingsObj.schemes) {
        $ExistingSchemes = @($SettingsObj.schemes | Where-Object { $GothamNames -notcontains $_.name })
    }
    $MergedSchemes = @($ExistingSchemes + $ParsedPayload.schemes)
    $SettingsObj | Add-Member -NotePropertyName "schemes" -NotePropertyValue $MergedSchemes -Force

    if (-not $SettingsObj.PSObject.Properties["profiles"] -or -not $SettingsObj.profiles) {
        $SettingsObj | Add-Member -NotePropertyName "profiles" -NotePropertyValue ([PSCustomObject]@{}) -Force
    }
    if (-not $SettingsObj.profiles.PSObject.Properties["defaults"] -or -not $SettingsObj.profiles.defaults) {
        $SettingsObj.profiles | Add-Member -NotePropertyName "defaults" -NotePropertyValue ([PSCustomObject]@{}) -Force
    }
    $SettingsObj.profiles.defaults | Add-Member -NotePropertyName "colorScheme" -NotePropertyValue $TargetScheme -Force

    [System.IO.File]::WriteAllText($SettingsPath, ($SettingsObj | ConvertTo-Json -Depth 12) + "`n", [System.Text.UTF8Encoding]::new($false))
    Write-Host "Updated Windows Terminal settings ($SettingsPath) -> $TargetScheme"
}
