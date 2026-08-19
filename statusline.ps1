# Claude Code status line.
# Layout: [Model] <bar> <pct>% (used/total) | $total (+$delta, dtok) | +lines/-lines | duration | project
# PowerShell 5.1 compatible: no `e escape, no ??, no ?., all non-ASCII via [char] codes.

$ErrorActionPreference = 'SilentlyContinue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$raw = [Console]::In.ReadToEnd()
try {
    $d = $raw | ConvertFrom-Json
} catch {
    [Console]::Out.Write('[Claude]')
    exit 0
}

function Get-Prop($obj, $path, $default) {
    $cur = $obj
    foreach ($p in $path.Split('.')) {
        if ($null -eq $cur) { return $default }
        $cur = $cur.$p
    }
    if ($null -eq $cur) { return $default }
    return $cur
}

$model        = Get-Prop $d 'model.display_name' 'Claude'
$pct          = Get-Prop $d 'context_window.used_percentage' $null
$window       = [int](Get-Prop $d 'context_window.context_window_size' 200000)
$inp          = [int](Get-Prop $d 'context_window.current_usage.input_tokens' 0)
$cacheRead    = [int](Get-Prop $d 'context_window.current_usage.cache_read_input_tokens' 0)
$cacheCreate  = [int](Get-Prop $d 'context_window.current_usage.cache_creation_input_tokens' 0)
$tokens       = $inp + $cacheRead + $cacheCreate
$totalCost    = [double](Get-Prop $d 'cost.total_cost_usd' 0)
$linesAdded   = [int](Get-Prop $d 'cost.total_lines_added' 0)
$linesRemoved = [int](Get-Prop $d 'cost.total_lines_removed' 0)
$durationMs   = [long](Get-Prop $d 'cost.total_duration_ms' 0)
$sessionId    = Get-Prop $d 'session_id' 'default'
$cwd          = Get-Prop $d 'workspace.current_dir' (Get-Prop $d 'cwd' '')
$outputStyle  = Get-Prop $d 'output_style.name' 'default'

# Per-turn deltas: persist last seen values per session.
$stateDir = Join-Path $env:TEMP 'claude-statusline'
if (-not (Test-Path $stateDir)) { New-Item -ItemType Directory -Path $stateDir -Force | Out-Null }
$safeId = ($sessionId -replace '[^A-Za-z0-9_-]', '_')
$stateFile = Join-Path $stateDir ($safeId + '.txt')
$prevCost = 0.0
$prevTokens = 0
if (Test-Path $stateFile) {
    foreach ($line in (Get-Content $stateFile)) {
        if ($line -match '^cost=(.+)$')   { $prevCost   = [double]$matches[1] }
        if ($line -match '^tokens=(.+)$') { $prevTokens = [int]$matches[1] }
    }
}
@(('cost=' + $totalCost), ('tokens=' + $tokens)) | Set-Content -Path $stateFile -Encoding ASCII

# Minimal output before the first turn produces usage stats.
if ($null -eq $pct) {
    [Console]::Out.Write('[' + $model + ']')
    exit 0
}

$pctInt = [int][math]::Round([double]$pct)

function Format-Tokens($n) {
    if ($n -ge 1000000) { return ('{0:N1}M' -f ($n / 1000000.0)) }
    if ($n -ge 1000)    { return ('{0:N0}k' -f ($n / 1000.0)) }
    return [string]$n
}

$usedStr  = Format-Tokens $tokens
$totalStr = Format-Tokens $window

# 20-cell context bar.
$filled = [int][math]::Floor($pctInt / 5)
if ($filled -lt 0)  { $filled = 0 }
if ($filled -gt 20) { $filled = 20 }
$empty = 20 - $filled
$block = [string]([char]0x2588)  # full block
$shade = [string]([char]0x2591)  # light shade
$delta = [string]([char]0x0394)  # capital delta
$bar = ($block * $filled) + ($shade * $empty)

# ANSI colors via [char]27.
$ESC   = [char]27
$reset = [string]$ESC + '[0m'
$dim   = [string]$ESC + '[2m'
$cyan  = [string]$ESC + '[36m'
$mag   = [string]$ESC + '[35m'
if     ($pctInt -ge 90) { $color = [string]$ESC + '[31m' }
elseif ($pctInt -ge 70) { $color = [string]$ESC + '[33m' }
else                    { $color = [string]$ESC + '[32m' }

# Cost and per-turn delta.
$costStr  = '{0:F4}' -f $totalCost
$diffCost = $totalCost - $prevCost
if ($diffCost -ge 0) { $deltaCostStr = '+$' + ('{0:F4}' -f $diffCost) }
else                 { $deltaCostStr = '-$' + ('{0:F4}' -f (-$diffCost)) }

# Per-turn token delta (signed).
$diffTok = $tokens - $prevTokens
if ($diffTok -ge 0) { $tdStr = '+' + (Format-Tokens $diffTok) }
else                { $tdStr = '-' + (Format-Tokens (-$diffTok)) }

# Session duration.
$secs = [int][math]::Floor($durationMs / 1000)
if     ($secs -ge 3600) { $dur = '{0}h{1}m' -f [int]([math]::Floor($secs / 3600)), [int](([math]::Floor($secs / 60)) % 60) }
elseif ($secs -ge 60)   { $dur = '{0}m' -f [int]([math]::Floor($secs / 60)) }
else                    { $dur = '{0}s' -f $secs }

if ($cwd) { $proj = Split-Path $cwd -Leaf } else { $proj = '' }

$stylePart = ''
if ($outputStyle -and $outputStyle -ne 'default') {
    $stylePart = ' | ' + $mag + $outputStyle + $reset
}

$parts = @(
    '[' + $model + '] ',
    $color + $bar + $reset + ' ',
    [string]$pctInt + '% ',
    $dim + '(' + $usedStr + '/' + $totalStr + ')' + $reset + ' | ',
    $cyan + '$' + $costStr + $reset,
    ' (' + $deltaCostStr + ', ' + $delta + $tdStr + ') | ',
    '+' + [string]$linesAdded + '/-' + [string]$linesRemoved + ' | ',
    $dur + ' | ',
    $proj,
    $stylePart
)
[Console]::Out.Write(-join $parts)
