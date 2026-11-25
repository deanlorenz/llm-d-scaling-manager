# llm-d-scaling-manager workspace

This folder is a container, not a git repo. `repo/` is the bare clone of the project; every worktree is a direct child of
this folder:

- `main`: the project code (branch `main`, fast-forwarded from `upstream`).
- `policy-writer`: where the shared rules and skills are edited.
- `session-tracking`: the production copy of the rules and skills. It is changed only by installing reviewed commits from
  `policy-writer`, never by hand.
- one folder per mission (for example `incubation-migration`); its `.session/` holds the mission's STATE, plan and ledger.

Remotes: `origin` is the personal fork (push allowed); `upstream` is `llm-d-incubation/llm-d-scaling-manager`
(push disabled).

Start every session inside the worktree you work in, not in this folder. Read `session-tracking/CONVENTIONS.md` first, then
your mission's `.session/STATE.md`. The rules live in files and skills under `session-tracking/`; this file only points to them.

Code style, commits and pull requests follow the project's own `AGENTS.md` and `CONTRIBUTING.md` (in `main` and in any
worktree cut from it). Nothing here overrides them.
