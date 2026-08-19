# install.ps1 - install these skills into your Claude Code setup.
#
# Copies every skill in .\skills\ into %USERPROFILE%\.claude\skills\.
# Existing folders with the same name are overwritten, so back them up first
# if you have edited them.
#
#   pwsh ./install.ps1            # install all skills
#   pwsh ./install.ps1 e2e elon   # install only the named ones

param([string[]]$Only)

$ErrorActionPreference = "Stop"

$src = Join-Path $PSScriptRoot "skills"
$dst = Join-Path $env:USERPROFILE ".claude\skills"

if (-not (Test-Path $src)) { throw "No skills folder next to this script: $src" }
New-Item -ItemType Directory -Path $dst -Force | Out-Null

$skills = Get-ChildItem $src -Directory
if ($Only) { $skills = $skills | Where-Object { $Only -contains $_.Name } }
if (-not $skills) { throw "Nothing to install. Available: $((Get-ChildItem $src -Directory).Name -join ', ')" }

foreach ($s in $skills) {
    $target = Join-Path $dst $s.Name
    if (Test-Path $target) { Remove-Item $target -Recurse -Force }
    Copy-Item $s.FullName $dst -Recurse -Force
    Write-Host "installed  $($s.Name)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Done. Restart Claude Code, then try /e2e or /elon." -ForegroundColor Yellow
