Name: rr-2
Conventions: /home/dean/code/llm-d/llm-d-scaling-manager/session-tracking/CONVENTIONS.md  (read it first)
What / goal / mission: Staleness check. A previous review (rr-1) of the NEW workspace's rules reported 84 findings and five "decisions". The user doubts that review: the OLD workspace's policy-writer mission has already revised and fixed rules, and the user suspects the new copy (or the review) is based on a stale version. Find out, with evidence, (A) whether the new rules are the latest rules that exist anywhere, and (B) which of rr-1's main findings are already addressed by rules that exist. Read-only.
Worktree: incubation-migration (new workspace; only for the report file)
Path: /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration
Branch: incubation-migration
Task SHA: n/a
Session ID: n/a
In: incubation-migration.rr-2.in
Out: incubation-migration.rr-2
Startup verification instructions:
  One command at a time. On any failure publish it on Out: and stop.
  1. `git rev-parse --show-toplevel` in the Path above equals Path.
  2. `git branch --show-current` there prints `incubation-migration`.
  3. `.session/task-rr-2.md` exists under Path.
Role / scope: reviewer, read-only. You write exactly one file, the report named below. No edits to anything else, no git writes in any worktree (no add, commit, checkout, reset, stash, fetch, pull, push), no rm/mv. If a hook or guard blocks a command, report it on Out: and read another way; never override a guard.
Ledger / log: none (the report is the output)
Progress events:
  kind="heartbeat" on Out:, body `session=rr-2 step=<i>/6 <what you just did>`: after the startup checks, after each of Parts A1, A2, A3, B, and when the report is written. Then one final note: report path plus a 5-line summary.

Plan / spec: none
Context:
  Two workspaces on this machine.
  OLD workspace root: /home/dean/code/llm-d/dean-llmd-scaler-sandbox. Worktrees in it: worktrees/policy-writer (branch `policy-writer`, where rules are edited) and worktrees/session-tracking (branch `session-tracking`, the production copy). Rules live at the top of those trees: CONVENTIONS.md, conventions/, claude-skills/, bob/. Old layout: worktrees are under <root>/worktrees/<name>.
  NEW workspace root: /home/dean/code/llm-d/llm-d-scaling-manager. FLAT layout: every worktree is a direct child of the root (policy-writer, session-tracking, main, incubation-migration); there is no `worktrees/` folder. The new `policy-writer` was created on 2026-11-25 by copying the old policy-writer branch tip d23d9d7e3 (commit 069380bd), then rewriting `worktrees/<name>` paths (d7ca66e8) and moving the ledger-harvest scripts out of claude-skills to ~/.claude/bin/ledger-harvest (f00935a7). The new `session-tracking` got a snapshot of the new policy-writer at f00935a7 as commit 194b528e. The old and the new repos are different git repositories (different object stores): compare files on disk, not by commit id across the two.
  Intended differences between old and new: (1) the path rewrite (worktrees/<name> -> <name>, the resume-mission `$TRACKING` sibling path, coder worktrees at ../<name>, the agentbus note in conv-background-agents), (2) the ledger-harvest directory is gone from claude-skills and three doc references now name $HOME/.claude/bin/ledger-harvest/harvest-registry.py. Anything else is unexplained.
  rr-1 report (the review being doubted): /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/review-rules-2026-11-25.md. Read its "Summary" and "Open decisions for the user" sections.
Refs:
  none
Expected output: /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/review-staleness-2026-11-25.md
Work in these parts; report each as its own section:
  A1. File-level comparison. Compare the production paths (CONVENTIONS.md, conventions/, claude-skills/, bob/) of OLD policy-writer vs OLD session-tracking vs NEW policy-writer vs NEW session-tracking (use `diff -r`, ignoring claude-skills/ledger-harvest which moved, and claude-skills/pr-review). Table: file | where it differs | explained by the intended differences above? (yes/no) | the differing lines. Every difference that is NOT explained is a finding.
  A2. Is there anything newer than the old policy-writer tip d23d9d7e3 (committed 2026-11-24 21:05) that holds rule changes? Check, read-only: `git log --all` and `git reflog` in the OLD repo for any commit touching CONVENTIONS.md, conventions/, claude-skills/ or bob/ that is not an ancestor of d23d9d7e3; `git stash list`; uncommitted changes in every old worktree under worktrees/ for those paths; branches other than policy-writer/session-tracking that carry rule files; unprocessed files in worktrees/session-tracking/suggestion-box/ (names not starting with `processed-`); the old policy-writer mission files worktrees/policy-writer/.session/STATE.md and its newest ledger under .session/ (read their "next step", "known issues" and anything that says a rule change is planned, pending, or being installed); the file worktrees/policy-writer/.session/incubation-migration-policy-note.md (a note the policy-writer session wrote for the migration). State plainly: "the newest rule state is X (commit/path)" or list what is newer.
  A3. Dates: for the new policy-writer's three commits and the old branch tips, give commit ids and dates, so the user can see the lineage.
  B. Re-check rr-1's main claims against the rules that actually exist. For each item below, search the OLD latest rules and the NEW rules for text that already addresses it, and report: "already addressed at <file>:<line> (quote)" or "genuinely not addressed" with the evidence of your search (the grep you ran): (1) blocker: `.claude/skills` dir-symlink cannot work in a worktree cut from upstream main, which has a real `.claude/skills` with tracked `pr-review` (check conv-feature-worktree-setup and CONVENTIONS for how a tracked pr-review is handled; also the old STATE/ledger notes about pr-review); (2) blocker: coder startup step d appends to `<common-dir>/worktrees/$WTID/info/exclude`; (3) blocker: rules assume session-tracking holds missions/ index, suggestion-box and CONVENTIONS.md; (4) PR skills do not name `-S` signatures, conventional commits, make lint/test, the merge queue (note: these matter for PR branches only); (5) rr-1 decision D4: how an open PR is updated when upstream/main moves (look at CONVENTIONS.md "Ownership and data safety", conv-pr-branch, conv-pr-workflow, conv-push, conv-coder-orchestration rule 16); (6) rr-1 decision D5: `git -C`, `EnterWorktree`, and the task-file name contradictions; (7) rr-1 decision D2: how conv-* skills reach a worktree whose `.claude/skills` is a real directory. For (5)-(7) also say whether the question exists in the OLD repo as well (i.e. is it a rule-quality question unrelated to the migration).
  Final verdict section: three lines: (i) are the new rules the latest rules that exist (yes/no, evidence); (ii) which rr-1 findings are stale or wrong; (iii) which findings are about the rules themselves and exist identically in the old repo (not migration-specific).
Done / completion criteria:
  Report file exists, all parts A1-A3 and B and the verdict are present, every claim cites a file path and line or the command you ran.
Limits: read-only except the one report file. Do not change any rule. Do not push or publish anything.
Extra rules / rule refs:
  none

Steps / subtasks:
  [ ] startup verification  [ ] A1  [ ] A2  [ ] A3  [ ] B  [ ] verdict and report
Next step / resume point: (blank — worker fills as it works)
Status: NOT STARTED
Known issues: none
