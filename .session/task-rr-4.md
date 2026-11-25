Name: rr-4
Conventions: /home/dean/code/llm-d/llm-d-scaling-manager/session-tracking/CONVENTIONS.md  (read it first)
What / goal / mission: Check every rule and skill for dangling references and broken or contradictory instructions about upstream skills, with `pr-review` as the example. Read-only; one report file.
Worktree: incubation-migration (new workspace; only for the report file)
Path: /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration
Branch: incubation-migration
Task SHA: n/a
Session ID: n/a
In: incubation-migration.rr-4.in
Out: incubation-migration.rr-4
Startup verification instructions:
  One command at a time. On any failure publish it on Out: and stop.
  1. `git rev-parse --show-toplevel` in the Path above equals Path.
  2. `git branch --show-current` there prints `incubation-migration`.
  3. `.session/task-rr-4.md` exists under Path.
Role / scope: reviewer, read-only. You write exactly one file, the report named below. No edits to anything else, no git writes in any worktree (no add, commit, checkout, reset, stash, fetch, pull, push), no rm/mv. If a hook or guard blocks a command, report it on Out: and read another way; never override a guard.
Ledger / log: none (the report is the output)
Progress events:
  kind="heartbeat" on Out:, body `session=rr-4 step=<i>/5 <what you just did>`: after the startup checks; after each of parts 1, 2, 3; when the report is written. Then one final note: the report path and a 5-line summary.

Plan / spec: none
Context:
  THE POLICY (stated by the user, 2026-11-25; check the rules against it, do not re-open it):
  - A project repo (here /home/dean/code/llm-d/llm-d-scaling-manager/main) tracks upstream skills in its own `.claude/skills/` (for example `pr-review`) and agents in `.claude/agents/`. Most upstream skills are NOT wanted: the user covers them with his own preferences and wants to control, for instance, how reviews are done, differently from upstream's `pr-review`.
  - Default = disabled by not linking: a worktree's `.claude/skills` is replaced by one directory link to `session-tracking/claude-skills`, so upstream skills simply do not exist for sessions in it.
  - Opt-in = link an upstream skill from `main` into `session-tracking` (for example `session-tracking/claude-skills/<name>` pointing at `main/.claude/skills/<name>`); then every worktree gets it. Setting up a repo or a new worktree should allow choosing which upstream skills to keep.
  - Upstream content is never edited; the removal of an upstream skill from a worktree is never committed, staged, ignored or deleted by a session; no session asks the user about it (old settled decision: /home/dean/code/llm-d/dean-llmd-scaler-sandbox/worktrees/policy-writer/.session/STATE.md lines 30-40 and .../spec-policy-writer.md section T6 around lines 165-180).
  - `~/.claude/settings.json` and ~/.claude/profiles/*.json also carry `skillOverrides: {"pr-review": "off"}` (a global switch).
  The rules to check, identical in two places: /home/dean/code/llm-d/llm-d-scaling-manager/policy-writer and /home/dean/code/llm-d/llm-d-scaling-manager/session-tracking (CONVENTIONS.md, conventions/*.md, claude-skills/*/SKILL.md, bob/custom_modes.yaml). Old copy for comparison: /home/dean/code/llm-d/dean-llmd-scaler-sandbox/worktrees/policy-writer.
  Known so far (verify, do not just repeat): claude-skills/conv-feature-worktree-setup/SKILL.md lines 58-62 say that a tracked `pr-review` means "do not replace the .claude/skills directory ... report this as a blocker", which contradicts the policy; CONVENTIONS.md lists `pr-review/SKILL.md` in its layout block; conv-install-to-session-tracking says to "ignore claude-skills/pr-review ... left untracked on session-tracking".
Refs:
  /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/review-rules-verified-2026-11-25.md (rows that mention pr-review, to be re-judged against the policy above)
Expected output: /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/review-pr-review-2026-11-25.md
Work in these parts; report each as its own section:
  1. Every mention. `grep -rniE 'pr-review|upstream skill|\.claude/skills|\.claude/agents|skillOverrides' ` over the rules (both trees) and over `~/.claude/README.md`, `~/.claude/settings.json`, `~/.claude/profiles/*.json`. Table: file:line | quote | what it instructs | verdict: CONSISTENT with the policy / CONTRADICTS the policy / DANGLING (names something that does not exist; check with ls) / UNCLEAR.
  2. Does any rule describe the opt-in (linking a chosen upstream skill from `main` into `session-tracking`, or choosing which upstream skills to keep when setting up a repo or worktree)? Answer yes/no with file:line. If no, say so plainly; do not invent one.
  3. Mechanics, read-only: in the OLD workspace several mission worktrees were cut from upstream (for example worktrees/single-analyzer, worktrees/composite-analyzer, worktrees/benchmark-waldorf under /home/dean/code/llm-d/dean-llmd-scaler-sandbox). For two of them report: is `.claude/skills` a symlink; what does `git status --short` show for `.claude/skills/pr-review`; what does `git ls-files .claude/skills` show. State what a session in a NEW worktree cut from /home/dean/code/llm-d/llm-d-scaling-manager/main will see after the setup skill links the folder (do not create anything; reason from the old evidence and say that it is inference).
  Final section "Fixes needed": one line per CONTRADICTS or DANGLING item: file:line and the exact change in words (not a patch), plus a line saying whether an opt-in procedure is missing. Do not change any file.
Done / completion criteria:
  Report exists with parts 1, 2, 3 and the fixes section; every claim cites file:line or the command you ran.
Limits: read-only except the one report file. Do not change any rule, setting, link or worktree. Do not push or publish anything.
Extra rules / rule refs:
  none

Steps / subtasks:
  [ ] startup verification  [ ] part 1  [ ] part 2  [ ] part 3  [ ] report
Next step / resume point: (blank — worker fills as it works)
Status: NOT STARTED
Known issues: none
