param(
    [ValidateSet("chromium", "firefox", "webkit")]
    [string]$Browser = "chromium",
    [string]$Markers = "smoke",
    [switch]$Headed
)

$env:BROWSER = $Browser
if ($Headed) { $env:HEADLESS = "false" }
python -m pytest -m $Markers --browser $Browser --alluredir allure-results
