# sync-skills.ps1 - pull the live skills back into this repo before committing.
#
# The live copies under %USERPROFILE%\.claude\skills\ are the source of truth;
# this repo is a published snapshot of them. Run this after editing a skill,
# then review `git diff` and commit.
#
#   pwsh ./sync-skills.ps1

$ErrorActionPreference = "Stop"

$live = Join-Path $env:USERPROFILE ".claude\skills"
$dst  = Join-Path $PSScriptRoot "skills"

if (-not (Test-Path $live)) { throw "No live skills directory: $live" }

foreach ($s in Get-ChildItem $dst -Directory) {
    $from = Join-Path $live $s.Name
    if (-not (Test-Path $from)) { Write-Warning "not installed locally, skipped: $($s.Name)"; continue }
    Remove-Item $s.FullName -Recurse -Force
    Copy-Item $from $dst -Recurse -Force
    Write-Host "synced  $($s.Name)" -ForegroundColor Green
}

Write-Host ""
Write-Host "Now review the diff before committing:" -ForegroundColor Yellow
Write-Host "  git diff --stat"
Write-Host "  git grep -niE 'employer|colleague|internal-host names you care about'   # last-look scan"
