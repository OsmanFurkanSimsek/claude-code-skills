# sync-skills.ps1 - pull the live skills back into this repo before committing, and gate what goes public.
#
# The live copies under %USERPROFILE%\.claude\skills\ are the source of truth;
# this repo is a published snapshot of them. Run this after editing a skill,
# then review `git diff` and commit.
#
#   pwsh ./sync-skills.ps1                          # live skills -> ./skills, gate over the whole repo
#   pwsh ./sync-skills.ps1 -Dest <empty temp dir>   # dry run: writes only there, gate over that folder
#   pwsh ./sync-skills.ps1 -LiveDir <dir>           # read the skills from another folder (tests)
#   pwsh ./sync-skills.ps1 -GateOnly                # no sync: only the leak gate, over this repo
#   pwsh ./sync-skills.ps1 -GateOnly -Path <dir>,<dir> -MessageFile <file>
#                                                   # gate other folders (for example each commit a
#                                                   # pre-push hook is about to send) and commit messages
#   add -RequireOwnerList to any of these           # a missing or too short owner list fails the run
#
# WHICH SKILLS: the folder names under THIS repo's own skills/ folder, whatever -Dest is.
# A brand-new skill is published by creating its folder under skills/ first. A name with no
# live folder is skipped and its copy in -Dest is left as it is (hand-made public versions of
# private skills live that way).
#
# This script does five things, in order:
#   1. STAGES each skill in a temp folder: refuses a skill holding a link (symlink, junction:
#      a copy would follow it), copies it from the live directory and deletes private and
#      cache files there (*.private* files and folders, __pycache__, .pytest_cache, .coverage*)
#   2. on the staged copy, CUTS every private block (below) and SCRUBS machine-specific
#      absolute paths (a live skill may hardcode C:\Users\<you>\ ; the published copy
#      must use %USERPROFILE%). It refuses what it cannot cut safely: UTF-16 or UTF-32 text,
#      a text file holding NUL bytes, and any archive, PDF or compressed file (.zip, .skill,
#      .docx, .pdf, gzip, 7z, ...) that $archiveAllow below does not name
#   3. runs the LEAK GATE over the staged copy, and only then replaces the skill folders in
#      -Dest; any problem in steps 1-3 stops the script and leaves -Dest exactly as it was
#   4. REBUILDS every *.skill bundle in this repo's root (a zip for the Claude desktop app)
#      from the stripped skills/<name> folder: entries <name>/..., evals/ folders left out.
#      In a dry run the bundles are written to -Dest instead of the repo root
#   5. runs the LEAK GATE again over the tree it wrote (default -Dest: the whole repo; any
#      other -Dest: that folder) and refuses to finish if anything sensitive is present
#
# PRIVATE BLOCKS: in a markdown file (.md, .markdown) a line that holds only
#   <!-- private:start -->
# up to the next line that holds only
#   <!-- private:end -->
# is cut out, both marker lines included, as whole lines. The marker text must be exactly
# that (spaces or tabs around it are fine). Every other byte stays as it was: CRLF stays CRLF,
# LF stays LF, a UTF-8 file without BOM stays without one. The script stops, naming file and
# line, on: an unclosed block, an end without a start, a start inside an open block, anything
# else that looks like a marker (another spelling, other case, other spacing, marker text inside
# a line), and any marker in a non-markdown file (private code goes in a *.private.* file next
# to it instead).
#
# LEAK GATE: the generic built-in patterns below (this machine's user and computer name,
# credentials, email addresses, GUIDs, private markers and any HTML comment holding "privat",
# sponsor links), *.private* names, links (symlinks, junctions), every archive opened entry by
# entry, PNG text chunks inflated, PDFs refused, UTF-16 text decoded, NUL-holding text files
# flagged; plus the OWNER LIST, -OwnerList (default %USERPROFILE%\.claude\public-gate.txt): one
# regex per line, case-insensitive, '#' starts a comment. Every term that names you, your people,
# your employer, its products and internal hosts, or your private skills goes there, so that this
# public script never names them. A space in any pattern matches any run of whitespace, line
# breaks included, so a two-word term wrapped onto two lines is still found. Everything is
# checked in every file, this script included; the only check this script's own text skips is
# the private-marker one (it documents the markers). No owner list (or fewer than 3 terms): a
# loud warning, or a failure with -RequireOwnerList (the pre-push hook sets it).
#
# The gate is the point. Do not remove it, and do not commit if it fails.

[CmdletBinding()]
param(
    # Where the live skills are read from.
    [string]$LiveDir = (Join-Path $env:USERPROFILE '.claude\skills'),
    # Where the synced skills are written. An empty temp folder makes it a dry run.
    [string]$Dest = (Join-Path $PSScriptRoot 'skills'),
    # Only run the leak gate (no sync, nothing written) over -Path and -MessageFile.
    [switch]$GateOnly,
    # -GateOnly: the folders to gate (default: this repo). Each is gated as a repo root.
    [string[]]$Path = @($PSScriptRoot),
    # -GateOnly: a text file of commit messages to gate too (email addresses are allowed there).
    [string]$MessageFile,
    # Your own private terms, one regex per line. Missing: a loud warning (see -RequireOwnerList).
    [string]$OwnerList = (Join-Path $env:USERPROFILE '.claude\public-gate.txt'),
    # Fail, not just warn, when the owner list is missing or holds fewer than 3 terms.
    [switch]$RequireOwnerList
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.IO.Compression

# Archives a skill may ship, as '<skill>/<path inside it>'. Keep it short: list one only after
# checking its content by hand. Zip-based ones are still opened and gated entry by entry.
$archiveAllow = @()

$markerish   = '<!--[\s-]*private|private\s*:\s*(start|end)'   # anything that looks like a marker (any case)
$markerLine  = '^[ \t]*<!-- private:(start|end) -->[ \t]*$'      # the only accepted form (exact case)
$markerGate  = $markerish + '|<!--(?:(?!-->)[\s\S])*?privat'     # the gate: also any HTML comment holding "privat"
$markdownExt = @('.md', '.markdown')
$scrubExt    = @('.md', '.json', '.txt', '.ps1', '.py', '.js')
$textExt     = @('.md', '.markdown', '.txt', '.json', '.jsonl', '.yaml', '.yml', '.toml', '.ini', '.cfg',
                 '.csv', '.tsv', '.ps1', '.psm1', '.psd1', '.py', '.js', '.mjs', '.cjs', '.ts', '.sh',
                 '.bash', '.bat', '.cmd', '.html', '.htm', '.css', '.xml', '.svg', '.sql',
                 '.gitignore', '.gitattributes')
$latin1      = [Text.Encoding]::Latin1   # one char per byte: decode + encode gives back the same bytes
$utf8        = [Text.UTF8Encoding]::new($false)
$bom         = $latin1.GetString([byte[]](0xEF, 0xBB, 0xBF))
$homeText    = $latin1.GetString([Text.Encoding]::UTF8.GetBytes("$env:USERPROFILE\"))   # e.g. C:\Users\alice\
$ic          = [Text.RegularExpressions.RegexOptions]::IgnoreCase

function Get-FullPath([string]$Path) {
    $full = $ExecutionContext.SessionState.Path.GetUnresolvedProviderPathFromPSPath($Path)
    if ($full.Length -gt 3) { $full = $full.TrimEnd('\', '/') }
    return $full
}
function Test-Inside([string]$Child, [string]$Parent) {
    return $Child -ieq $Parent -or $Child.StartsWith($Parent.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)
}

# The real path on disk: junctions, symlinks and 8.3 short names followed, real case. A path
# that does not exist yet is resolved up to its nearest existing parent.
$realPathCs = @'
using System;
using System.Runtime.InteropServices;
using System.Text;
using Microsoft.Win32.SafeHandles;
namespace SyncSkills {
  public static class RealPath {
    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    static extern SafeFileHandle CreateFileW(string name, uint access, uint share, IntPtr sa, uint disposition, uint flags, IntPtr template);
    [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
    static extern uint GetFinalPathNameByHandleW(SafeFileHandle h, StringBuilder buffer, uint size, uint flags);
    public static string Get(string path) {
      using (SafeFileHandle h = CreateFileW(path, 0, 7, IntPtr.Zero, 3, 0x02000000, IntPtr.Zero)) {
        if (h.IsInvalid) return null;
        StringBuilder sb = new StringBuilder(32768);
        uint n = GetFinalPathNameByHandleW(h, sb, (uint)sb.Capacity, 0);
        if (n == 0 || n >= sb.Capacity) return null;
        string s = sb.ToString();
        if (s.StartsWith(@"\\?\UNC\")) return @"\\" + s.Substring(8);
        if (s.StartsWith(@"\\?\")) return s.Substring(4);
        return s;
      }
    }
  }
}
'@
function Get-RealPath([string]$Path) {
    $full = Get-FullPath $Path
    $tail = [Collections.Generic.List[string]]::new()
    $cur  = $full
    while ($cur -and -not (Test-Path -LiteralPath $cur)) { $tail.Insert(0, (Split-Path $cur -Leaf)); $cur = Split-Path $cur -Parent }
    if (-not $cur) { return $full }
    $real = $cur
    if ($IsWindows) {
        if (-not ('SyncSkills.RealPath' -as [type])) { Add-Type -TypeDefinition $realPathCs }
        $r = [SyncSkills.RealPath]::Get($cur)
        if ($r) { $real = $r }
    }
    foreach ($t in $tail) { $real = Join-Path $real $t }
    if ($real.Length -gt 3) { $real = $real.TrimEnd('\', '/') }
    return $real
}

function Test-PrivateOrCache($Item) {
    $n = $Item.Name
    return ($n -like '*.private*') -or ($n -eq '.coverage') -or ($n -like '.coverage.*') -or
           ($Item.PSIsContainer -and ($n -eq '__pycache__' -or $n -eq '.pytest_cache'))
}
function Test-TextName([string]$Name) {
    $e = [IO.Path]::GetExtension($Name).ToLowerInvariant()
    return (-not $e) -or ($textExt -contains $e)
}
function Test-HasNul([byte[]]$B) { return [Array]::IndexOf($B, [byte]0) -ge 0 }

# A space in a pattern (plain or escaped) matches any whitespace: \s+ outside [...], \s inside it.
# So a two-word term that a hard-wrapped line split in two ("Acme<line break>Corp") still matches.
function ConvertTo-SpacedPattern([string]$P) {
    $sb = [Text.StringBuilder]::new()
    $inClass = $false
    $i = 0
    while ($i -lt $P.Length) {
        $c = $P[$i]
        $escSpace = ($c -eq '\') -and ($i + 1 -lt $P.Length) -and ($P[$i + 1] -eq ' ')
        if ($inClass) {
            if ($c -eq ' ') { [void]$sb.Append('\s'); $i++; continue }
            if ($escSpace) { [void]$sb.Append('\s'); $i += 2; continue }
            [void]$sb.Append($c)
            if ($c -eq '\' -and $i + 1 -lt $P.Length) { [void]$sb.Append($P[$i + 1]); $i += 2; continue }
            if ($c -eq ']') { $inClass = $false }
            $i++
        } elseif ($c -eq ' ' -or $escSpace) {
            while ($i -lt $P.Length) {
                if ($P[$i] -eq ' ') { $i++ }
                elseif ($P[$i] -eq '\' -and $i + 1 -lt $P.Length -and $P[$i + 1] -eq ' ') { $i += 2 }
                else { break }
            }
            if ($i -lt $P.Length -and '*+?{'.Contains($P[$i])) { [void]$sb.Append('(?:\s+)') } else { [void]$sb.Append('\s+') }
        } elseif ($c -eq '\' -and $i + 1 -lt $P.Length) {
            [void]$sb.Append($c).Append($P[$i + 1]); $i += 2
        } elseif ($c -eq '[') {
            $inClass = $true; [void]$sb.Append($c); $i++
            if ($i -lt $P.Length -and $P[$i] -eq '^') { [void]$sb.Append('^'); $i++ }
            if ($i -lt $P.Length -and $P[$i] -eq ']') { [void]$sb.Append(']'); $i++ }
        } else {
            [void]$sb.Append($c); $i++
        }
    }
    return $sb.ToString()
}

# 'zip' for anything a zip reader opens; another word for compressed formats no check can read;
# 'archive name' for a file named like an archive that is not a readable zip; $null otherwise.
function Get-ArchiveKind([byte[]]$B, [string]$Name) {
    $n = $B.Length
    if ($n -ge 4 -and $B[0] -eq 0x50 -and $B[1] -eq 0x4B -and
        (($B[2] -eq 3 -and $B[3] -eq 4) -or ($B[2] -eq 5 -and $B[3] -eq 6) -or ($B[2] -eq 7 -and $B[3] -eq 8))) { return 'zip' }
    if ($n -ge 2 -and $B[0] -eq 0x1F -and $B[1] -eq 0x8B) { return 'gzip' }
    if ($n -ge 3 -and $B[0] -eq 0x42 -and $B[1] -eq 0x5A -and $B[2] -eq 0x68) { return 'bzip2' }
    if ($n -ge 6 -and $B[0] -eq 0xFD -and $B[1] -eq 0x37 -and $B[2] -eq 0x7A -and $B[3] -eq 0x58 -and $B[4] -eq 0x5A -and $B[5] -eq 0) { return 'xz' }
    if ($n -ge 6 -and $B[0] -eq 0x37 -and $B[1] -eq 0x7A -and $B[2] -eq 0xBC -and $B[3] -eq 0xAF -and $B[4] -eq 0x27 -and $B[5] -eq 0x1C) { return '7z' }
    if ($n -ge 4 -and $B[0] -eq 0x52 -and $B[1] -eq 0x61 -and $B[2] -eq 0x72 -and $B[3] -eq 0x21) { return 'rar' }
    if ($n -ge 4 -and $B[0] -eq 0x28 -and $B[1] -eq 0xB5 -and $B[2] -eq 0x2F -and $B[3] -eq 0xFD) { return 'zstd' }
    $e = [IO.Path]::GetExtension($Name).ToLowerInvariant()
    # A PDF keeps its text in compressed streams no check here reads. Readers accept up to 1 KB of
    # anything before the %PDF- header, so a file that is not text-named is searched that far.
    if ($e -eq '.pdf') { return 'pdf' }
    if ($n -ge 5) {
        $head = $latin1.GetString($B, 0, [Math]::Min($n, 1024))
        if ($head.StartsWith('%PDF-', [StringComparison]::Ordinal) -or (-not (Test-TextName $Name) -and $head.Contains('%PDF-'))) { return 'pdf' }
    }
    if (@('.zip', '.skill', '.gz', '.tgz', '.bz2', '.xz', '.7z', '.rar', '.zst', '.tar', '.jar',
          '.docx', '.xlsx', '.pptx') -contains $e) { return 'archive name' }
    return $null
}
function Test-PngMagic([byte[]]$B) {
    return $B.Length -ge 8 -and $B[0] -eq 0x89 -and $B[1] -eq 0x50 -and $B[2] -eq 0x4E -and $B[3] -eq 0x47 -and
           $B[4] -eq 0x0D -and $B[5] -eq 0x0A -and $B[6] -eq 0x1A -and $B[7] -eq 0x0A
}
function Expand-Zlib([byte[]]$B, [int]$Offset, [int]$Count) {
    $z = [IO.Compression.ZLibStream]::new([IO.MemoryStream]::new($B, $Offset, $Count), [IO.Compression.CompressionMode]::Decompress)
    $out = [IO.MemoryStream]::new()
    try { $z.CopyTo($out) } finally { $z.Dispose() }
    return , $out.ToArray()
}
# The compressed text chunks of a real PNG (zTXt, iTXt with its compression flag set), inflated, as
# @(type, bytes) pairs. Plain tEXt / iTXt and anything after IEND are read with the raw bytes.
function Get-PngTextChunks([byte[]]$B) {
    $out = [Collections.Generic.List[object]]::new()
    $p = 8
    while ($p + 8 -le $B.Length) {
        $len  = ([int64]$B[$p] -shl 24) + ([int64]$B[$p + 1] -shl 16) + ([int64]$B[$p + 2] -shl 8) + [int64]$B[$p + 3]
        $type = $latin1.GetString($B, $p + 4, 4)
        $s    = $p + 8
        if ($s + $len -gt $B.Length) { break }
        $k = [Array]::IndexOf($B, [byte]0, $s, [int]$len)
        if ($type -ceq 'zTXt' -and $k -ge 0 -and $k + 2 -le $s + $len) {
            $out.Add(@($type, (Expand-Zlib $B ($k + 2) ($s + $len - $k - 2))))
        } elseif ($type -ceq 'iTXt' -and $k -ge 0 -and $k + 3 -le $s + $len -and $B[$k + 1] -eq 1) {
            $l = [Array]::IndexOf($B, [byte]0, $k + 3, $s + $len - $k - 3)
            $t = if ($l -ge 0) { [Array]::IndexOf($B, [byte]0, $l + 1, $s + $len - $l - 1) } else { -1 }
            if ($t -lt 0) { throw 'iTXt chunk without its text field' }
            $out.Add(@($type, (Expand-Zlib $B ($t + 1) ($s + $len - $t - 1))))
        }
        if ($type -ceq 'IEND') { break }
        $p = $s + [int]$len + 4
    }
    return , $out
}
# Why the private-block cut cannot read this file safely, or $null.
function Get-EncodingProblem([byte[]]$B, [string]$Name) {
    $n = $B.Length
    if (($n -ge 2 -and $B[0] -eq 0xFF -and $B[1] -eq 0xFE) -or ($n -ge 2 -and $B[0] -eq 0xFE -and $B[1] -eq 0xFF) -or
        ($n -ge 4 -and $B[0] -eq 0 -and $B[1] -eq 0 -and $B[2] -eq 0xFE -and $B[3] -eq 0xFF)) {
        return 'UTF-16 or UTF-32 text (byte order mark)'
    }
    if ((Test-TextName $Name) -and (Test-HasNul $B)) { return 'NUL bytes in a text file (UTF-16 without a byte order mark?)' }
    return $null
}
# The texts a gate reads out of a file: decoded by its byte order mark; a file holding NUL bytes
# is read as UTF-8 and as UTF-16 (both byte orders). NulText = NUL bytes in a text-named file.
function Get-TextViews([byte[]]$B, [string]$Name) {
    $views = [Collections.Generic.List[string]]::new()
    $n = $B.Length
    $nulText = $false
    if ($n -ge 4 -and $B[0] -eq 0xFF -and $B[1] -eq 0xFE -and $B[2] -eq 0 -and $B[3] -eq 0) {
        $views.Add([Text.Encoding]::UTF32.GetString($B, 4, $n - 4))
    } elseif ($n -ge 4 -and $B[0] -eq 0 -and $B[1] -eq 0 -and $B[2] -eq 0xFE -and $B[3] -eq 0xFF) {
        $views.Add([Text.UTF32Encoding]::new($true, $false).GetString($B, 4, $n - 4))
    } elseif ($n -ge 2 -and $B[0] -eq 0xFF -and $B[1] -eq 0xFE) {
        $views.Add([Text.Encoding]::Unicode.GetString($B, 2, $n - 2))
    } elseif ($n -ge 2 -and $B[0] -eq 0xFE -and $B[1] -eq 0xFF) {
        $views.Add([Text.Encoding]::BigEndianUnicode.GetString($B, 2, $n - 2))
    } else {
        $views.Add($utf8.GetString($B))
        if (Test-HasNul $B) {
            $views.Add([Text.Encoding]::Unicode.GetString($B))
            $views.Add([Text.Encoding]::BigEndianUnicode.GetString($B))
            $nulText = Test-TextName $Name
        }
    }
    return @{ Views = $views; NulText = $nulText }
}

# Cuts every private block out of $Text (whole lines, markers included). Problems go to
# $Problems as "<file> line <n>: <what>"; the caller stops the sync if there are any.
function Remove-PrivateBlocks([string]$Text, [string]$Label, [bool]$IsMarkdown, $Problems) {
    $hasBom = $Text.StartsWith($bom, [StringComparison]::Ordinal)
    if ($hasBom) { $Text = $Text.Substring(3) }
    $lines = [regex]::Split($Text, '(?<=\n)')   # each piece keeps its own line ending
    $kept  = [Text.StringBuilder]::new()
    $open  = 0                                  # line of the open private:start, 0 = outside
    $cut   = 0
    for ($i = 0; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        $n    = $i + 1
        $body = $line.TrimEnd([char[]]"`r`n")
        if ([regex]::IsMatch($body, $markerish, $ic)) {
            $m = [regex]::Match($body, $markerLine)   # exact form only, case-sensitive
            if (-not $IsMarkdown) {
                $Problems.Add("$Label line ${n}: private marker in a non-markdown file (put private code in a *.private.* file)")
            } elseif (-not $m.Success) {
                $Problems.Add("$Label line ${n}: private marker text that is not a whole marker line in the exact form <!-- private:start --> or <!-- private:end -->")
            } elseif ($m.Groups[1].Value -eq 'start') {
                if ($open) { $Problems.Add("$Label line ${n}: private:start inside the block opened at line $open (nested)") }
                else { $open = $n }
            } elseif ($open) {
                $open = 0; $cut++
            } else {
                $Problems.Add("$Label line ${n}: private:end without a private:start")
            }
            continue
        }
        if (-not $open) { [void]$kept.Append($line) }
    }
    if ($open) { $Problems.Add("$Label line ${open}: private:start is never closed") }
    $out = $kept.ToString()
    if ($hasBom) { $out = $bom + $out }
    return @{ Text = $out; Cut = $cut }
}

# ---------- the leak gate ----------
# Each entry: a label and a regex (case-insensitive) that must NOT appear anywhere in the scanned
# tree, in file and folder names, or inside archives. Add to this list, never shorten it. It holds
# generic checks only: every term that names you, your people, your employer, its products or
# internal hosts, or your private skills goes in the owner list instead (see the top). No pattern
# here matches its own text, so this script is checked by all of them except 'private markers'.
# Machine identifiers come from the running machine: its user name and computer name.
$machineIds = @(@($env:USERNAME, $env:COMPUTERNAME, [Environment]::UserName, [Environment]::MachineName) |
                Where-Object { $_ -and $_.Length -ge 3 } | Sort-Object -Unique | ForEach-Object { [regex]::Escape($_) })
$gate = [ordered]@{}
if ($machineIds.Count) { $gate['machine identifiers'] = $machineIds -join '|' }
$gate['credentials'] =
    'sk-ant-[A-Za-z0-9_-]{15,}|ghp_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{20,}|' +
    'xox[baprs]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{35}|BEGIN [A-Z ]*PRIVATE KEY'
$gate['email addresses'] =
    '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
$gate['GUIDs'] =
    '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'
$gate['private markers'] =
    $markerGate
$gate['third-party skill markers (sponsor links)'] =
    'github\.com/sponsors|buymeacoff[e]e|patreon\.com'
$selfSkip = @('private markers')   # the only check this script's own text skips: it documents the markers
$gateRe = [ordered]@{}
foreach ($k in $gate.Keys) { $gateRe[$k] = [regex]::new((ConvertTo-SpacedPattern $gate[$k]), $ic) }
$lblOwner   = 'owner list'
$lblPrivate = 'private files or folders (*.private*)'
$lblLinks   = 'links (symlinks, junctions: pushed as their target path)'
$lblArchive = 'archives or compressed files the gate cannot fully read'
$lblNul     = 'NUL bytes in a text file (UTF-16 without a byte order mark?)'

function Read-OwnerList([string]$File) {
    $res = @{ Found = $false; Regexes = [Collections.Generic.List[regex]]::new(); Problems = [Collections.Generic.List[string]]::new() }
    if (-not $File -or -not (Test-Path -LiteralPath $File -PathType Leaf)) { return $res }
    $res.Found = $true
    $n = 0
    foreach ($line in [IO.File]::ReadAllLines($File)) {
        $n++
        $t = $line.Trim()
        if (-not $t -or $t.StartsWith('#')) { continue }
        try { $res.Regexes.Add([regex]::new((ConvertTo-SpacedPattern $t), $ic)) } catch { $res.Problems.Add("owner list line ${n}: not a valid regex") }
    }
    return $res
}
$owner = Read-OwnerList $OwnerList
# Why the owner list cannot protect this run, or $null.
$ownerGap = if (-not $owner.Found) { "no owner list at $OwnerList" }
            elseif ($owner.Regexes.Count -lt 3) { "the owner list $OwnerList holds $($owner.Regexes.Count) term(s), at least 3 are needed" }
            else { $null }

function Add-Hit([string]$Label, [string]$Where) { $script:G[$Label].Add($Where) }
function Get-LineNo([string]$Text, [int]$Index) { return [regex]::Matches($Text.Substring(0, $Index), "`n").Count + 1 }

# Checks texts against the built-in patterns and the owner list. -Self: this script's own text,
# which skips only the $selfSkip checks. -NoEmails: commit messages (co-author and author lines).
function Test-Text([string]$Where, $Views, [switch]$Self, [switch]$NoEmails, [switch]$NoLine) {
    $checks = [Collections.Generic.List[object]]::new()
    foreach ($k in $gateRe.Keys) {
        if ($Self -and $selfSkip -contains $k) { continue }
        if ($NoEmails -and $k -eq 'email addresses') { continue }
        $checks.Add(@($k, $gateRe[$k]))
    }
    foreach ($re in $owner.Regexes) { $checks.Add(@($lblOwner, $re)) }
    foreach ($c in $checks) {
        foreach ($v in $Views) {
            $m = $c[1].Match($v)
            if ($m.Success) {
                if ($NoLine) { Add-Hit $c[0] $Where } else { Add-Hit $c[0] "${Where}:$(Get-LineNo $v $m.Index)" }
                break
            }
        }
    }
}
function Test-Zip([string]$Where, [byte[]]$Bytes, [int]$Depth) {
    try { $zip = [IO.Compression.ZipArchive]::new([IO.MemoryStream]::new($Bytes), [IO.Compression.ZipArchiveMode]::Read) }
    catch { Add-Hit $lblArchive "$Where (cannot be opened)"; return }
    try {
        foreach ($e in $zip.Entries) {
            $ew = "$Where!/$($e.FullName)"
            Test-Text "$ew (entry name)" @($e.FullName) -NoLine
            if (@($e.FullName -split '[\\/]' | Where-Object { $_ -like '*.private*' }).Count) { Add-Hit $lblPrivate $ew }
            if ($e.FullName -match '[\\/]$') { continue }   # folder entry
            if ($e.IsEncrypted) { Add-Hit $lblArchive "$ew (encrypted)"; continue }
            if ($e.Length -gt 64MB) { Add-Hit $lblArchive "$ew (too large to check)"; continue }
            try {
                $s = $e.Open(); $ms = [IO.MemoryStream]::new(); $s.CopyTo($ms); $s.Dispose()
                $eb = $ms.ToArray()
            } catch { Add-Hit $lblArchive "$ew (cannot be read)"; continue }
            Test-Bytes $ew $eb $e.Name '' $false $Depth
        }
    } catch { Add-Hit $lblArchive "$Where (cannot be read)" }
    finally { $zip.Dispose() }
}
function Test-Bytes([string]$Where, [byte[]]$Bytes, [string]$Name, [string]$AllowKey, [bool]$IsSelf, [int]$Depth) {
    $kind = Get-ArchiveKind $Bytes $Name
    if ($kind -eq 'zip') {
        if ($Depth -ge 4) { Add-Hit $lblArchive "$Where (archives nested too deep)" } else { Test-Zip $Where $Bytes ($Depth + 1) }
        return
    }
    if ($kind) {
        if ($archiveAllow -notcontains $AllowKey) { Add-Hit $lblArchive "$Where ($kind)"; return }
        if ($kind -ne 'pdf') { return }   # an allowlisted PDF is still read as text below
    }
    # Every other file is read as text, images included (a file named .png that is not one is just
    # text); a real PNG also has its compressed text chunks inflated and read.
    if (Test-PngMagic $Bytes) {
        try {
            foreach ($c in (Get-PngTextChunks $Bytes)) { Test-Text "$Where (PNG $($c[0]) chunk)" @($utf8.GetString($c[1])) -NoLine }
        } catch { Add-Hit $lblArchive "$Where (a PNG text chunk cannot be read)" }
    }
    $t = Get-TextViews $Bytes $Name
    if ($t.NulText) { Add-Hit $lblNul $Where }
    Test-Text $Where $t.Views -Self:$IsSelf
}
# Everything under $Dir except .git; never descends into a link.
function Get-TreeItems([string]$Dir) {
    foreach ($i in ([IO.DirectoryInfo]::new($Dir)).EnumerateFileSystemInfos('*', [IO.SearchOption]::TopDirectoryOnly)) {
        if ($i.Name -eq '.git') { continue }
        $i
        if (($i.Attributes -band [IO.FileAttributes]::Directory) -and -not ($i.Attributes -band [IO.FileAttributes]::ReparsePoint)) {
            Get-TreeItems $i.FullName
        }
    }
}
# Every link (reparse point) at or under $Dir, never descending into one; .git included.
function Get-LinkPaths([string]$Dir) {
    $d = [IO.DirectoryInfo]::new($Dir)
    if ($d.Attributes -band [IO.FileAttributes]::ReparsePoint) { return $d.FullName }
    foreach ($i in $d.EnumerateFileSystemInfos('*', [IO.SearchOption]::TopDirectoryOnly)) {
        if ($i.Attributes -band [IO.FileAttributes]::ReparsePoint) { $i.FullName }
        elseif ($i.Attributes -band [IO.FileAttributes]::Directory) { Get-LinkPaths $i.FullName }
    }
}
# Gates one folder (as a repo root: its own sync-skills.ps1 skips only the $selfSkip checks) or one
# file of commit messages. Prints PASS / FAIL per check and returns the number of failed checks.
function Invoke-LeakGate([string]$Root, [string]$Title, [string]$Messages) {
    $script:G = [ordered]@{}
    foreach ($l in @($gate.Keys) + @($lblOwner, $lblPrivate, $lblLinks, $lblArchive, $lblNul)) {
        $script:G[$l] = [Collections.Generic.List[string]]::new()
    }
    foreach ($p in $owner.Problems) { $script:G[$lblOwner].Add($p) }
    if ($ownerGap -and $RequireOwnerList) { $script:G[$lblOwner].Add("$ownerGap (-RequireOwnerList)") }
    if ($Root) {
        $base = Get-FullPath $Root
        foreach ($i in Get-TreeItems $base) {
            $rel = [IO.Path]::GetRelativePath($base, $i.FullName).Replace('\', '/')
            if ($i.Attributes -band [IO.FileAttributes]::ReparsePoint) { Add-Hit $lblLinks $rel; continue }
            Test-Text "$rel (name)" @($rel) -NoLine
            if ($i.Name -like '*.private*') { Add-Hit $lblPrivate $rel }
            if (-not ($i.Attributes -band [IO.FileAttributes]::Directory)) {
                $key = if ($rel.StartsWith('skills/')) { $rel.Substring(7) } else { $rel }
                Test-Bytes $rel ([IO.File]::ReadAllBytes($i.FullName)) $i.Name $key ($rel -ieq 'sync-skills.ps1') 0
            }
        }
    }
    if ($Messages) { Test-Text 'commit messages' @([IO.File]::ReadAllText($Messages)) -NoEmails }

    Write-Host ""
    Write-Host "Leak gate over $Title :" -ForegroundColor Cyan
    if ($ownerGap -and -not $RequireOwnerList) {
        Write-Host "  WARNING  $ownerGap." -ForegroundColor Red
        Write-Host "           Only the generic checks ran: names of people, of your employer, its products and" -ForegroundColor Red
        Write-Host "           internal hosts, and of private skills are NOT checked. Put them in that file (one" -ForegroundColor Red
        Write-Host "           regex per line); -RequireOwnerList turns this warning into a failure." -ForegroundColor Red
    }
    $failed = 0
    foreach ($l in $script:G.Keys) {
        $h = $script:G[$l]
        if ($l -eq $lblOwner -and -not $owner.Found -and -not $h.Count) { continue }
        if ($h.Count) {
            Write-Host "  FAIL  $l" -ForegroundColor Red
            $h | Select-Object -First 5 | ForEach-Object { Write-Host "        $_" -ForegroundColor Red }
            $failed++
        } elseif ($l -eq $lblPrivate) {
            Write-Host "  PASS  no private files or folders (*.private*)" -ForegroundColor Green
        } elseif ($l -eq $lblOwner) {
            Write-Host "  PASS  owner list ($($owner.Regexes.Count) terms)" -ForegroundColor Green
        } else {
            Write-Host "  PASS  $l" -ForegroundColor Green
        }
    }
    return $failed
}

# ---------- gate only ----------
if ($GateOnly) {
    $failed = 0
    foreach ($p in $Path) {
        if (-not (Test-Path -LiteralPath $p -PathType Container)) { throw "-Path is not a folder: $p" }
        $failed += Invoke-LeakGate $p (Get-FullPath $p) $null
    }
    if ($MessageFile) {
        if (-not (Test-Path -LiteralPath $MessageFile -PathType Leaf)) { throw "-MessageFile not found: $MessageFile" }
        $failed += Invoke-LeakGate $null "commit messages ($MessageFile)" $MessageFile
    }
    Write-Host ""
    if ($failed) {
        Write-Host "$failed check(s) FAILED - do NOT push." -ForegroundColor Red
        exit 1
    }
    Write-Host "All checks passed." -ForegroundColor Green
    exit 0
}

# ---------- where to read and write ----------
$repoRoot   = Get-FullPath $PSScriptRoot
$repoSkills = Get-FullPath (Join-Path $PSScriptRoot 'skills')
$LiveDir    = Get-FullPath $LiveDir
$Dest       = Get-FullPath $Dest
if (-not (Test-Path -LiteralPath $LiveDir -PathType Container)) { throw "No live skills directory: $LiveDir" }
if (-not (Test-Path -LiteralPath $repoSkills -PathType Container)) { throw "No skills folder in this repo: $repoSkills" }
# Compared as real paths, so a junction, a short name or another spelling of a folder is seen
# for what it is.
$realLive   = Get-RealPath $LiveDir
$realDest   = Get-RealPath $Dest
$realRoot   = Get-RealPath $repoRoot
$realSkills = Get-RealPath $repoSkills
if ((Test-Inside $realDest $realLive) -or (Test-Inside $realLive $realDest)) {
    throw "-Dest and -LiveDir must not contain each other: -Dest $Dest, -LiveDir $LiveDir"
}
$isRepoDest = $realDest -ieq $realSkills
if (-not $isRepoDest -and ((Test-Inside $realDest $realRoot) -or (Test-Inside $realRoot $realDest))) {
    throw "-Dest must be this repo's skills folder or a folder outside this repo: $Dest"
}
$gateRoot = if ($isRepoDest) { $repoRoot } else { $Dest }

$names = @(Get-ChildItem -LiteralPath $repoSkills -Directory | ForEach-Object Name)
$stage = Join-Path ([IO.Path]::GetTempPath()) ('sync-skills-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $stage | Out-Null
try {
    # ---------- 1. stage: refuse links, copy, then delete private and cache files ----------
    # A link (symlink, junction, any reparse point) inside a live skill would be followed by the
    # copy and publish whatever it points at, so it stops the sync before anything is copied.
    $toStage = [Collections.Generic.List[string]]::new()
    $links   = [Collections.Generic.List[string]]::new()
    foreach ($name in $names) {
        if ($name -like '*.private*') { Write-Warning "private folder name, never synced: $name"; continue }
        $from = Join-Path $LiveDir $name
        if (-not (Test-Path -LiteralPath $from -PathType Container)) { Write-Warning "not installed locally, skipped: $name"; continue }
        foreach ($l in Get-LinkPaths $from) {
            $rel = [IO.Path]::GetRelativePath($from, $l).Replace('\', '/')
            $links.Add($(if ($rel -eq '.') { "$name (the skill folder itself)" } else { "$name/$rel" }))
        }
        $toStage.Add($name)
    }
    if ($links.Count) {
        throw ("Links (symlinks, junctions) inside live skills; a copy would follow them. Nothing was written to ${Dest}:`n  " + ($links -join "`n  "))
    }
    $staged = [Collections.Generic.List[string]]::new()
    foreach ($name in $toStage) {
        Copy-Item -LiteralPath (Join-Path $LiveDir $name) -Destination $stage -Recurse -Force
        $staged.Add($name)
    }
    $doomed = @(Get-ChildItem -LiteralPath $stage -Recurse -Force | Where-Object { Test-PrivateOrCache $_ } |
                Sort-Object { $_.FullName.Length })
    foreach ($d in $doomed) {
        if (-not (Test-Path -LiteralPath $d.FullName)) { continue }   # inside a folder already removed
        Remove-Item -LiteralPath $d.FullName -Recurse -Force
        Write-Host "left out (private or cache): $([IO.Path]::GetRelativePath($stage, $d.FullName).Replace('\', '/'))" -ForegroundColor Yellow
    }

    # ---------- 2. cut private blocks, scrub machine-specific paths ----------
    $problems = [Collections.Generic.List[string]]::new()
    $scrubbed = 0
    foreach ($f in Get-ChildItem -LiteralPath $stage -Recurse -File -Force) {
        $rel   = [IO.Path]::GetRelativePath($stage, $f.FullName).Replace('\', '/')
        $ext   = $f.Extension.ToLowerInvariant()
        $bytes = [IO.File]::ReadAllBytes($f.FullName)
        $kind  = Get-ArchiveKind $bytes $f.Name
        if ($kind) {
            if ($archiveAllow -notcontains $rel) {
                $problems.Add("${rel}: archive or compressed file ($kind) inside a skill; ship its files unpacked (a PDF as text or images), or name it in `$archiveAllow after checking it by hand")
            }
            continue
        }
        $enc = Get-EncodingProblem $bytes $f.Name
        if ($enc) { $problems.Add("${rel}: $enc; save it as UTF-8 (the private-block cut reads UTF-8 only)"); continue }
        if (Test-HasNul $bytes) {   # binary: nothing to cut, but marker text in it cannot be cut either
            $v = Get-TextViews $bytes $f.Name
            if (@($v.Views | Where-Object { [regex]::IsMatch($_, $markerish, $ic) }).Count) {
                $problems.Add("${rel}: private marker text inside a binary file")
            }
            continue
        }
        $text = $latin1.GetString($bytes)
        $new  = $text
        if ([regex]::IsMatch($text, $markerish, $ic)) {
            $r   = Remove-PrivateBlocks $text $rel ($markdownExt -contains $ext) $problems
            $new = $r.Text
            if ($r.Cut) { Write-Host "cut $($r.Cut) private block(s) in $rel" -ForegroundColor Yellow }
        }
        if ($scrubExt -contains $ext) {
            $s = $new.Replace($homeText, '%USERPROFILE%\')
            if (-not [string]::Equals($s, $new, [StringComparison]::Ordinal)) {
                Write-Host "scrubbed absolute path in $rel" -ForegroundColor Yellow
                $scrubbed++
                $new = $s
            }
        }
        if (-not [string]::Equals($new, $text, [StringComparison]::Ordinal)) {
            [IO.File]::WriteAllBytes($f.FullName, $latin1.GetBytes($new))
        }
    }
    if ($problems.Count) {
        throw ("Private-block problems; nothing was written to ${Dest}:`n  " + ($problems -join "`n  "))
    }
    if ($scrubbed) { Write-Host "$scrubbed file(s) rewritten to use %USERPROFILE%" -ForegroundColor Yellow }

    # ---------- 3. check the staged tree, then replace the folders in -Dest ----------
    $left = [Collections.Generic.List[string]]::new()
    foreach ($i in Get-ChildItem -LiteralPath $stage -Recurse -Force) {
        $rel = [IO.Path]::GetRelativePath($stage, $i.FullName).Replace('\', '/')
        if (Test-PrivateOrCache $i) { $left.Add("$rel (private or cache)") }
        elseif (-not $i.PSIsContainer -and [regex]::IsMatch($latin1.GetString([IO.File]::ReadAllBytes($i.FullName)), $markerish, $ic)) { $left.Add("$rel (private marker)") }
    }
    if ($left.Count) { throw ("Staged copy is not clean; nothing was written to ${Dest}:`n  " + ($left -join "`n  ")) }
    if (Invoke-LeakGate $stage 'the staged copy (before anything is written)' $null) {
        throw "Leak gate failed on the staged copy; nothing was written to ${Dest}. Fix the live skill, then re-run."
    }

    if (-not (Test-Path -LiteralPath $Dest)) { New-Item -ItemType Directory -Path $Dest | Out-Null }
    foreach ($name in $staged) {
        $target = Join-Path $Dest $name
        if (Test-Path -LiteralPath $target) { Remove-Item -LiteralPath $target -Recurse -Force }
        Copy-Item -LiteralPath (Join-Path $stage $name) -Destination $Dest -Recurse -Force
        Write-Host "synced  $name" -ForegroundColor Green
    }
} finally {
    Remove-Item -LiteralPath $stage -Recurse -Force -ErrorAction SilentlyContinue
}

# ---------- 4. rebuild the *.skill bundles from the stripped folders ----------
# Same layout as a Claude desktop bundle: entries <name>/<path> with forward slashes, files only,
# folders and files in ordinal order, evals/ folders left out. Fixed entry dates keep an unchanged
# skill's bundle byte-identical.
function Get-BundleFiles([string]$Dir, [string]$Prefix) {
    $d = [IO.DirectoryInfo]::new($Dir)
    $files = [string[]]@($d.GetFiles() | ForEach-Object Name)
    [Array]::Sort($files, [StringComparer]::Ordinal)
    foreach ($n in $files) { [pscustomobject]@{ Full = (Join-Path $Dir $n); Entry = "$Prefix/$n" } }
    $dirs = [string[]]@($d.GetDirectories() | Where-Object { $_.Name -ne 'evals' } | ForEach-Object Name)
    [Array]::Sort($dirs, [StringComparer]::Ordinal)
    foreach ($n in $dirs) { Get-BundleFiles (Join-Path $Dir $n) "$Prefix/$n" }
}
function Build-Bundle([string]$Src, [string]$Name, [string]$Out) {
    $tmp   = "$Out.tmp-" + [guid]::NewGuid().ToString('N')
    $stamp = [DateTimeOffset]::new(2000, 1, 1, 0, 0, 0, [TimeSpan]::Zero)
    $fs    = [IO.File]::Open($tmp, [IO.FileMode]::CreateNew)
    try {
        $zip = [IO.Compression.ZipArchive]::new($fs, [IO.Compression.ZipArchiveMode]::Create)
        try {
            foreach ($f in @(Get-BundleFiles $Src $Name)) {
                $e = $zip.CreateEntry($f.Entry, [IO.Compression.CompressionLevel]::Optimal)
                $e.LastWriteTime = $stamp
                $w = $e.Open()
                try { $b = [IO.File]::ReadAllBytes($f.Full); $w.Write($b, 0, $b.Length) } finally { $w.Dispose() }
            }
        } finally { $zip.Dispose() }
    } finally { $fs.Dispose() }
    Move-Item -LiteralPath $tmp -Destination $Out -Force
}
$bundleDir = if ($isRepoDest) { $repoRoot } else { $Dest }
foreach ($b in @(Get-ChildItem -LiteralPath $repoRoot -File -Force | Where-Object { $_.Extension -ieq '.skill' })) {
    $name = $b.BaseName
    $src  = Join-Path $Dest $name
    if (-not (Test-Path -LiteralPath $src -PathType Container)) { $src = Join-Path $repoSkills $name }
    if (-not (Test-Path -LiteralPath $src -PathType Container)) {
        Write-Warning "no skills/$name folder: $($b.Name) not rebuilt (the gate still opens it)"
        continue
    }
    Build-Bundle $src $name (Join-Path $bundleDir $b.Name)
    Write-Host "rebuilt $($b.Name) from the stripped skills/$name" -ForegroundColor Green
}

# ---------- 5. leak gate over what was written ----------
$failed = Invoke-LeakGate $gateRoot $gateRoot $null

Write-Host ""
if ($failed) {
    Write-Host "$failed check(s) FAILED - do NOT commit. Fix the live skill, then re-run." -ForegroundColor Red
    exit 1
}

if (-not $isRepoDest) {
    Write-Host "All checks passed. Dry run: only $Dest was written; this repo's skills/ is untouched." -ForegroundColor Green
    exit 0
}
Write-Host "All checks passed. Review and commit:" -ForegroundColor Green
Write-Host "  git diff --stat"
Write-Host "  git add -A ; git commit -m '...' ; git push"
Write-Host ""
Write-Host "After pushing, confirm what the world sees:" -ForegroundColor Yellow
Write-Host "  git clone --depth 1 https://github.com/OsmanFurkanSimsek/claude-code-skills /tmp/pubcheck"
