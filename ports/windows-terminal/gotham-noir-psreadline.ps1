# Gotham Noir PowerShell PSReadLine Syntax Theme
[CmdletBinding()]
param(
    [ValidateSet("year-one", "batcomputer", "arkham-slate", "vengeance")]
    [string]$Variant = "year-one",
    [switch]$PassThru
)

$VariantColors = @{
    "year-one" = @{
        Command          = "#74aeeb"
        Parameter        = "#e29754"
        String           = "#63c794"
        Operator         = "#68c5ce"
        Number           = "#e29754"
        Comment          = "#878d96"
        Keyword          = "#b695e8"
        Variable         = "#d8d6cf"
        Type             = "#f0c946"
        Member           = "#68c5ce"
        Error            = "#e86a74"
        InlinePrediction = "#878d96"
        Selection        = "#323a46"
        Default          = "#d8d6cf"
    }
    "batcomputer" = @{
        Command          = "#72b4f5"
        Parameter        = "#e89b54"
        String           = "#56cca0"
        Operator         = "#5ecad6"
        Number           = "#e89b54"
        Comment          = "#828a96"
        Keyword          = "#bc9bf0"
        Variable         = "#dce0e5"
        Type             = "#f5d042"
        Member           = "#5ecad6"
        Error            = "#ee6b78"
        InlinePrediction = "#828a96"
        Selection        = "#2b3440"
        Default          = "#dce0e5"
    }
    "arkham-slate" = @{
        Command          = "#80b0dc"
        Parameter        = "#df9a5f"
        String           = "#88c082"
        Operator         = "#74bfbd"
        Number           = "#df9a5f"
        Comment          = "#929690"
        Keyword          = "#bc9cd9"
        Variable         = "#dad5c7"
        Type             = "#e6c15a"
        Member           = "#74bfbd"
        Error            = "#e37370"
        InlinePrediction = "#929690"
        Selection        = "#373e47"
        Default          = "#dad5c7"
    }
    "vengeance" = @{
        Command          = "#7baee6"
        Parameter        = "#e5985a"
        String           = "#6ec798"
        Operator         = "#6fc2ca"
        Number           = "#e5985a"
        Comment          = "#918994"
        Keyword          = "#be9ae6"
        Variable         = "#ddd8d5"
        Type             = "#e8be54"
        Member           = "#6fc2ca"
        Error            = "#ef6c74"
        InlinePrediction = "#918994"
        Selection        = "#3a2c33"
        Default          = "#ddd8d5"
    }
}

$selected = $VariantColors[$Variant]
if (Get-Command Set-PSReadLineOption -ErrorAction SilentlyContinue) {
    Set-PSReadLineOption -Colors $selected
}
if ($PassThru) {
    return $selected
}
