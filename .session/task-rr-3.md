Name: rr-3
Conventions: /home/dean/code/llm-d/llm-d-scaling-manager/session-tracking/CONVENTIONS.md  (read it first)
What / goal / mission: Refresh the rules review. The review rr-1 (84 findings) was found unreliable: its input (the rules) was current, but some of its claims are false or stale (rr-2 checked 7 and found several wrong). Verify EVERY finding of rr-1 against the actual current lines, sort the true ones into "migration-specific" and "rule-quality (exists in the old repo too)", and turn the true rule-quality ones into suggestion-box drafts. Read-only on all rules.
Worktree: incubation-migration (new workspace; only for your two output files)
Path: /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration
Branch: incubation-migration
Task SHA: n/a
Session ID: n/a
In: incubation-migration.rr-3.in
Out: incubation-migration.rr-3
Startup verification instructions:
  One command at a time. On any failure publish it on Out: and stop.
  1. `git rev-parse --show-toplevel` in the Path above equals Path.
  2. `git branch --show-current` there prints `incubation-migration`.
  3. `.session/task-rr-3.md` exists under Path.
Role / scope: reviewer, read-only. You write exactly two files, named under "Expected output". No edits to anything else, no git writes in any worktree (no add, commit, checkout, reset, stash, fetch, pull, push), no rm/mv. If a hook or guard blocks a command, report it on Out: and read another way; never override a guard.
Ledger / log: none (the reports are the output)
Progress events:
  kind="heartbeat" on Out:, body `session=rr-3 step=<i>/<n> <what you just did>`: after the startup checks; after every 15 findings verified (`findings <done>/84`); when each of the two files is written. Then one final note: the two paths and a 6-line summary.

Plan / spec: none
Context:
  Two workspaces. NEW root /home/dean/code/llm-d/llm-d-scaling-manager (flat: every worktree is a direct child of the root: policy-writer, session-tracking, main, incubation-migration; no `worktrees/` folder). OLD root /home/dean/code/llm-d/dean-llmd-scaler-sandbox (worktrees under worktrees/<name>). The new rules (policy-writer = where rules are edited, session-tracking = production copy, now identical to it) are the old latest rules (old policy-writer tip d23d9d7e3, 2026-11-24) plus two intended changes: (1) path rewrite from worktrees/<name> to <name>; (2) the ledger-harvest scripts moved out of claude-skills into ~/.claude/bin/ledger-harvest (a machine tool; see ~/.claude/README.md). The two repos are different git repositories: compare files on disk.
  The review to verify: /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/review-rules-2026-11-25.md (rr-1). Its tables list findings as `file | line | severity | finding | suggested change`; count them yourself (the report says 84: 5 blocker, 53 fix, 26 nit). Also read the previous check /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/review-staleness-2026-11-25.md (rr-2), which already judged about seven of them.
  Decisions that are SETTLED (do not re-raise them as findings; if a finding contradicts one, mark it "settled: <which>"):
  - `pr-review` is an upstream skill that the user does not need. The whole `.claude/skills` folder of a worktree is linked to `session-tracking/claude-skills`; `pr-review` is not linked or handled per worktree and its removal is never committed. Look for the decision text in the OLD policy-writer mission files (/home/dean/code/llm-d/dean-llmd-scaler-sandbox/worktrees/policy-writer/.session/ : STATE.md, spec, ledgers) and in the processed suggestions under /home/dean/code/llm-d/dean-llmd-scaler-sandbox/worktrees/session-tracking/suggestion-box/ ; cite what you find.
  - DCO sign-off and verified signatures (`-s`, `-S`) are required only for PR branches that may be pushed upstream (project rules: /home/dean/code/llm-d/llm-d-scaling-manager/main/CONTRIBUTING.md). `policy-writer`, `session-tracking` and `.session/`-only mission branches never go upstream and need neither.
  - The `missions/` index, the `suggestion-box/` and the pending-commits flow belong in `session-tracking`.
  - The migration mission does not fix rules. Rule problems are written up as suggestions; a policy-writer session fixes them.
  - Harvester, `apiKeyHelper`, profiles and global memory are global Claude config, not rules.
Refs:
  /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/postmortem-2026-11-25.md
Expected output:
  1. /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/review-rules-verified-2026-11-25.md
  2. /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/drafts/suggestions-from-rr3-2026-11-25.md
  File 1: a summary (counts of each verdict and each class), then ONE table with a row for EVERY rr-1 finding, in rr-1's order, columns: # | file:line | rr-1 severity | verdict | class | evidence. Verdict is exactly one of: CONFIRMED (the quoted line exists as described and the problem is real), FALSE (the line does not say that, or the claimed problem does not exist; say why), STALE (the line changed or the question is settled; say how), UNCLEAR. Class (for CONFIRMED only) is exactly one of: MIGRATION (caused by the new layout or the new workspace state; the old repo does not have it), RULE-QUALITY-BOTH (the same problem exists in the old latest rules), SETTLED (see list above). Evidence: for CONFIRMED the quoted line from the NEW file and, for the class, the same line or its absence in the OLD file (give both paths and line numbers); for FALSE/STALE the line or search (the grep you ran) that shows it.
  File 2: suggestion-box drafts for the CONFIRMED RULE-QUALITY-BOTH findings only. Group findings that share one root cause into ONE entry; one atomic finding per entry. Each entry has the headings `## <short title>`, `Finding` (with file:line evidence from both trees), `Need`, `Proposed solution`, `Where it might land`. Put the entry's rr-1 row numbers at its top. Do not write suggestions for MIGRATION, FALSE, STALE or SETTLED rows. At the end list the MIGRATION rows (they are for the mission owner, not suggestions).
Done / completion criteria:
  All findings of rr-1 appear in file 1 with one verdict each (state the count); every verdict has evidence; both files exist and are non-empty.
Limits: read-only except the two output files. Do not change any rule, STATE or plan. Do not push or publish anything. Do not paste whole files; quote only the relevant line.
Extra rules / rule refs:
  none

Steps / subtasks:
  [ ] startup verification  [ ] read rr-1, rr-2, settled-decision sources  [ ] verify findings in batches  [ ] write file 1  [ ] write file 2
Next step / resume point: (blank — worker fills as it works)
Status: NOT STARTED
Known issues: none
