# Gotham Noir for Windows Terminal & PowerShell

## 1. One-Line Install (Windows Terminal + PowerShell Profile)

Run in PowerShell 5.1 or PowerShell 7+ (`pwsh`):

```powershell
irm https://raw.githubusercontent.com/thezaynahmed/gotham-noir/main/ports/windows-terminal/install-windows-terminal.ps1 | iex
```

To select a specific variant (`year-one`, `batcomputer`, `arkham-slate`, `vengeance`):

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/thezaynahmed/gotham-noir/main/ports/windows-terminal/install-windows-terminal.ps1))) -Variant batcomputer
```

This creates a `.bak` backup of your existing `settings.json`, preserves custom schemes, installs all 4 schemes, activates `Gotham Noir` in `profiles.defaults.colorScheme`, and installs the official Windows Terminal JSON Fragment Extension (`%LOCALAPPDATA%\Microsoft\Windows Terminal\Fragments\gotham-noir\themes.json`).

## 2. PowerShell PSReadLine Syntax Highlighting

Add to your `$PROFILE`:

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/thezaynahmed/gotham-noir/main/ports/windows-terminal/gotham-noir-psreadline.ps1))) -Variant year-one
```
