Name: rr-5
Conventions: /home/dean/code/llm-d/llm-d-scaling-manager/session-tracking/CONVENTIONS.md  (read it first)
What / goal / mission: For each of 32 drafted rule suggestions, find out whether the OLD policy-writer mission already discussed or decided it. Read-only; one report file. The user will drop what is already decided and look at the rest one by one.
Worktree: incubation-migration (new workspace; only for the report file)
Path: /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration
Branch: incubation-migration
Task SHA: n/a
Session ID: n/a
In: incubation-migration.rr-5.in
Out: incubation-migration.rr-5
Startup verification instructions:
  One command at a time. On any failure publish it on Out: and stop.
  1. `git rev-parse --show-toplevel` in the Path above equals Path.
  2. `git branch --show-current` there prints `incubation-migration`.
  3. `.session/task-rr-5.md` exists under Path.
Role / scope: reviewer, read-only. You write exactly one file, the report named below. No edits to anything else, no git writes in any worktree (no add, commit, checkout, reset, stash, fetch, pull, push), no rm/mv. If a hook or guard blocks a command, report it on Out: and read another way; never override a guard.
Ledger / log: none (the report is the output)
Progress events:
  kind="heartbeat" on Out:, body `session=rr-5 step=<i>/<n> <what you just did>`: after the startup checks; after every 8 suggestions mapped (`mapped <done>/32`); when the report is written. Then one final note: the report path and a 6-line summary.

Plan / spec: none
Context:
  The 32 drafts: /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/drafts/suggestions-from-rr3-2026-11-25.md (each `## ` heading is one suggestion; its first line lists the review rows). Evidence for each is in /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/review-rules-verified-2026-11-25.md (rows of the same numbers). They were found by a review of the rules on 2026-11-25; the same lines and problems exist in the old latest rules (old policy-writer tip d23d9d7e3). It is NOT known whether the old policy-writer mission already discussed, decided, rejected or queued any of them: that is what you establish.
  Old policy-writer mission material (OLD workspace root /home/dean/code/llm-d/dean-llmd-scaler-sandbox):
  - worktrees/session-tracking/suggestion-box/ : the processed suggestion entries (names `processed-<date>-<time>-<mission>.md`, about 30) and any unprocessed ones.
  - worktrees/policy-writer/.session/ : STATE.md, spec-policy-writer.md, task and ledger files (also under .session/ledger/), drafts, notes (for example incubation-migration-policy-note.md and migration-compat-2026-11-24.md).
  - worktrees/policy-writer/ top level: PLAN-conventions-split.md, backup_rules/, conventions/archived/ (rules that were archived, with their reasons).
  - `git log` of the old branches `policy-writer` and `session-tracking` (commit messages that mention the topic), run from /home/dean/code/llm-d/dean-llmd-scaler-sandbox (read-only commands only: log, show, grep).
Refs:
  none
Expected output: /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/review-suggestions-mapping-2026-11-25.md
  First a summary (counts per verdict). Then ONE table with a row per suggestion, in the draft's order: # | title | rr-1 rows | verdict | evidence | what the old mission decided. Verdict is exactly one of:
  - ALREADY-ADOPTED: an old entry/decision changed the rules to fix this, and the rule text now in the old tip reflects it (so the draft may be wrong or stale: say which, with the line).
  - ALREADY-DECIDED-NO-CHANGE: the old mission looked at this and decided to keep the rule as it is (quote the reasoning and where).
  - ALREADY-QUEUED: an old suggestion or open item for this exists but the rules were not changed yet (give the entry/file).
  - PARTLY: part of the draft was handled (say which part).
  - NEW: no trace in the old material (state the searches you ran: the grep patterns and the places).
  Evidence: file path and line (or commit id) for every verdict other than NEW; for NEW, the searches. Never judge from memory or from what a document claims about itself; read the entry.
Done / completion criteria:
  All 32 suggestions have one verdict with evidence; the report exists and is non-empty.
Limits: read-only except the one report file. Do not change any rule, suggestion draft, STATE or plan. Do not push or publish anything. Quote only the relevant lines; do not paste whole files.
Extra rules / rule refs:
  none

Steps / subtasks:
  [ ] startup verification  [ ] list the old material  [ ] map the 32  [ ] write the report
Next step / resume point: (blank — worker fills as it works)
Status: NOT STARTED
Known issues: none
