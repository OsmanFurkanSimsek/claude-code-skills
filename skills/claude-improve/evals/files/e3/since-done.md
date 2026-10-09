# Re-runs of scan.py --since "<Done time>" for the two done items

Both runs read the same transcripts as scan.md; only the start differs. Header line and the metrics that matter.

## CI-3 (Done: 2026-10-02 08:20 UTC)

`python scan.py --since "2026-10-02 08:20" --out since-ci3.md --json since-ci3.json`

Window: 2026-10-02 08:20 to 2026-10-09 08:00 UTC (7.0 days). Sessions: 12 (+1 with no assistant turn skipped); subagent runs: 9.
- Sessions by start source: startup 7, clear 5
- Bash/PowerShell: 401 calls, 1 errors. Classes: no_such_file 1
- `"bash.err.heredoc_eof.per_week": 0.0` (baseline 5.0, target below 2)

## CI-4 (Done: 2026-10-02 08:30 UTC)

`python scan.py --since "2026-10-02 08:30" --out since-ci4.md --json since-ci4.json`

Window: 2026-10-02 08:30 to 2026-10-09 08:00 UTC (7.0 days). Sessions: 11 (+1 with no assistant turn skipped); subagent runs: 9.
- Sessions by start source: startup 6, clear 5
- Tool results over 25K chars: 1 (31K Read, report-builder: reports/2026-10-06_quarterly.md); web page fetches over 25K: 0
- `"big_outputs_25k.per_week": 1.0` (baseline 9.0, target below 3)
