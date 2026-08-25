# backup-setup.ps1 - snapshot your Claude Code setup into a PRIVATE git repo.
#
# Why: if your machine dies, ~/.claude dies with it - your skills, hooks, agents,
# settings, and per-project memory. Keeping a mirrored snapshot in a private repo
# means a new machine is a clone + copy-back away from the exact same setup.
#
# How to use:
#   1. Create a PRIVATE repo (it will hold personal material - never make it public).
#   2. Drop this script in its root and run:  pwsh ./backup-setup.ps1
#   3. Review `git status` for anything secret-looking, then commit and push.
#
# What it deliberately EXCLUDES - never add these back:
#   - config.json           (holds your Anthropic API key; it regenerates on sign-in)
#   - .credentials.json, anything matching *token* / *credentials*, MCP auth caches
#   - runtime caches, session logs, IDE state
# Belt and suspenders: put the same exclusions in the repo's .gitignore, e.g.
#   config.json
#   .credentials.json
#   *token*
#   *credentials*
# and STILL eyeball `git status` before every push. The script is idempotent: it
# wipes the mirror tree each run so deletions in the live setup propagate.

$ErrorActionPreference = "Stop"

$src = "$env:USERPROFILE\.claude"
$dst = "$PSScriptRoot\claude"

if (-not (Test-Path $src)) { throw "Source not found: $src" }

Write-Host "Staging mirror tree..." -ForegroundColor Cyan
if (Test-Path $dst) { Remove-Item $dst -Recurse -Force }
New-Item -ItemType Directory -Path $dst | Out-Null

# --- Root files. NOTE: config.json is intentionally NOT in this list. ---
Write-Host "Copying core config files..." -ForegroundColor Cyan
foreach ($f in @("settings.json", "CLAUDE.md", "statusline.ps1", "keybindings.json")) {
    $p = Join-Path $src $f
    if (Test-Path $p) { Copy-Item $p $dst }
}

# --- Directories: hooks, agents, saved plans. ---
Write-Host "Copying hooks, agents, plans..." -ForegroundColor Cyan
foreach ($sub in @("hooks", "agents", "plans")) {
    $p = Join-Path $src $sub
    if (Test-Path $p) { Copy-Item $p $dst -Recurse -Force }
}

# --- Skills, minus eval-scratch trees. Skill-development workspaces are named
#     "<skill>-workspace" and contain no SKILL.md - throwaway runs, not setup. ---
Write-Host "Copying skills (excluding *-workspace eval scratch)..." -ForegroundColor Cyan
$skillsSrc = Join-Path $src "skills"
if (Test-Path $skillsSrc) {
    $skillsDst = Join-Path $dst "skills"
    New-Item -ItemType Directory -Path $skillsDst -Force | Out-Null
    Get-ChildItem $skillsSrc -Force | Where-Object {
        -not ($_.PSIsContainer -and $_.Name -like "*-workspace" -and `
              -not (Test-Path (Join-Path $_.FullName "SKILL.md")))
    } | ForEach-Object { Copy-Item $_.FullName $skillsDst -Recurse -Force }
}

# --- Plugin manifests only (NOT the plugin cache or downloaded marketplaces). ---
$pluginsSrc = Join-Path $src "plugins"
if (Test-Path $pluginsSrc) {
    $pluginsDst = Join-Path $dst "plugins"
    New-Item -ItemType Directory -Path $pluginsDst -Force | Out-Null
    foreach ($mf in @("installed_plugins.json", "known_marketplaces.json")) {
        $p = Join-Path $pluginsSrc $mf
        if (Test-Path $p) { Copy-Item $p $pluginsDst }
    }
}

# --- Per-project auto-memory only - skip the large per-session logs. ---
Write-Host "Copying per-project memory folders..." -ForegroundColor Cyan
$projectsDir = Join-Path $src "projects"
if (Test-Path $projectsDir) {
    Get-ChildItem $projectsDir -Directory -ErrorAction SilentlyContinue | ForEach-Object {
        $memSrc = Join-Path $_.FullName "memory"
        if (Test-Path $memSrc) {
            $memDst = Join-Path $dst ("projects\" + $_.Name + "\memory")
            New-Item -ItemType Directory -Path $memDst -Force | Out-Null
            Copy-Item "$memSrc\*" $memDst -Recurse -Force -ErrorAction SilentlyContinue
        }
    }
}

Set-Content -Path "$PSScriptRoot\LAST_SNAPSHOT.txt" `
    -Value "Snapshot taken: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"

Write-Host ""
Write-Host "Backup staged at $PSScriptRoot" -ForegroundColor Green
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. git status            # sanity-check that no secrets are staged"
Write-Host "  2. git add -A"
Write-Host "  3. git commit -m 'Snapshot'"
Write-Host "  4. git push              # to your PRIVATE repo"
