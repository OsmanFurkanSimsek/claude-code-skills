# sync-skills.ps1 - pull the live skills back into this repo before committing.
#
# The live copies under %USERPROFILE%\.claude\skills\ are the source of truth;
# this repo is a published snapshot of them. Run this after editing a skill,
# then review `git diff` and commit.
#
#   pwsh ./sync-skills.ps1
#
# This script does three things, in order:
#   1. copies each skill folder from the live directory
#   2. SCRUBS machine-specific absolute paths (a live skill may hardcode
#      C:\Users\<you>\ ; the published copy must use %USERPROFILE%)
#   3. runs a LEAK GATE and refuses to finish if anything sensitive is present
#
# The gate is the point. Do not remove it, and do not commit if it fails.

$ErrorActionPreference = "Stop"

$live = Join-Path $env:USERPROFILE ".claude\skills"
$dst  = Join-Path $PSScriptRoot "skills"

if (-not (Test-Path $live)) { throw "No live skills directory: $live" }

# ---------- 1. copy ----------
foreach ($s in Get-ChildItem $dst -Directory) {
    $from = Join-Path $live $s.Name
    if (-not (Test-Path $from)) { Write-Warning "not installed locally, skipped: $($s.Name)"; continue }
    Remove-Item $s.FullName -Recurse -Force
    Copy-Item $from $dst -Recurse -Force
    Write-Host "synced  $($s.Name)" -ForegroundColor Green
}

# ---------- 2. scrub machine-specific paths ----------
$homePath = "$env:USERPROFILE\"          # e.g. C:\Users\alice\
$scrubbed = 0
Get-ChildItem $dst -Recurse -File -Include *.md,*.json,*.txt,*.ps1,*.py,*.js | ForEach-Object {
    $raw = [IO.File]::ReadAllText($_.FullName)
    $new = $raw.Replace($homePath, '%USERPROFILE%\')
    if ($new -ne $raw) {
        [IO.File]::WriteAllText($_.FullName, $new)
        Write-Host "scrubbed absolute path in $($_.FullName.Substring($dst.Length + 1))" -ForegroundColor Yellow
        $scrubbed++
    }
}
if ($scrubbed) { Write-Host "$scrubbed file(s) rewritten to use %USERPROFILE%" -ForegroundColor Yellow }

# ---------- 3. leak gate ----------
# Each entry: a label and a regex that must NOT appear anywhere in this repo.
# Add to this list, never shorten it.
$gate = [ordered]@{
  'employer / product / internal hosts' =
    'GN Store Nord|GN Audio|Jabra|ReSound|SteelSeries|Beltone|Interton|SWART|gnaudio|ONEGN|' +
    'apim-llm-gateway|hotjar-jabra-kv|dkcph|Zendesk_Data|processedcustomercomments|Hotjar|' +
    'AppFigures|Rayfin|PI Planning'
  'people / private matters' =
    'Civilstyrelsen|Bydammen|Tatsiana|Shkoda|Mette Frank|Kasper Kok'
  'machine identifiers' =
    [regex]::Escape($env:USERNAME) + '|' + [regex]::Escape($env:COMPUTERNAME) + '|CascadeProjects|OneDrive'
  'credentials' =
    'sk-ant-[A-Za-z0-9_-]{15,}|ghp_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{20,}|' +
    'xox[baprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|BEGIN [A-Z ]*PRIVATE KEY'
  'email addresses' =
    '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
  'GUIDs' =
    '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
}

# NOTE: this script is excluded from its own scan - it necessarily contains the
# very patterns it searches for. Everything else in the repo is scanned.
$self   = $PSCommandPath
$files  = Get-ChildItem $PSScriptRoot -Recurse -File |
          Where-Object { $_.FullName -notlike '*\.git\*' -and
                         $_.FullName -ne $self -and
                         $_.Extension -ne '.skill' -and $_.Extension -ne '.png' }
$failed = 0

Write-Host ""
Write-Host "Leak gate:" -ForegroundColor Cyan
foreach ($name in $gate.Keys) {
    $hits = $files | Select-String -Pattern $gate[$name] -List -ErrorAction SilentlyContinue
    if ($hits) {
        Write-Host "  FAIL  $name" -ForegroundColor Red
        $hits | Select-Object -First 5 | ForEach-Object {
            Write-Host "        $($_.Path.Substring($PSScriptRoot.Length + 1)):$($_.LineNumber)" -ForegroundColor Red
        }
        $failed++
    } else {
        Write-Host "  PASS  $name" -ForegroundColor Green
    }
}

# third-party skills must never be published
$thirdParty = $files | Select-String -Pattern 'github\.com/sponsors|buymeacoffee|patreon\.com' -List -ErrorAction SilentlyContinue
if ($thirdParty) {
    Write-Host "  FAIL  third-party skill markers (sponsor links)" -ForegroundColor Red
    $thirdParty | ForEach-Object { Write-Host "        $($_.Path.Substring($PSScriptRoot.Length + 1))" -ForegroundColor Red }
    $failed++
} else {
    Write-Host "  PASS  no third-party skill markers" -ForegroundColor Green
}

Write-Host ""
if ($failed) {
    Write-Host "$failed check(s) FAILED - do NOT commit. Fix the live skill, then re-run." -ForegroundColor Red
    exit 1
}

Write-Host "All checks passed. Review and commit:" -ForegroundColor Green
Write-Host "  git diff --stat"
Write-Host "  git add -A ; git commit -m '...' ; git push"
Write-Host ""
Write-Host "After pushing, confirm what the world sees:" -ForegroundColor Yellow
Write-Host "  git clone --depth 1 https://github.com/OsmanFurkanSimsek/claude-code-skills /tmp/pubcheck"
