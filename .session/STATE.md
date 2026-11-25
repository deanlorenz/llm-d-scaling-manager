# incubation-migration

## Orientation

- **Conventions:** `policy-writer/CONVENTIONS.md` (workspace root `/home/dean/code/llm-d/llm-d-scaling-manager`; the
  production copy `session-tracking` is intentionally EMPTY until the first install, so read the rules from
  `policy-writer/` for now; skills are not linked into this worktree yet: read `policy-writer/claude-skills/<name>/SKILL.md`)
  *(read this first, before any other file)*
- **What / goal / mission:** Move our work to the new repo
  `https://github.com/llm-d-incubation/llm-d-scaling-manager`: flat workspace (container root, bare `repo/`, every
  worktree a direct child), rules and skills in the new `policy-writer`, global Claude config tracked in
  `~/.claude`. This worktree finishes what is left of the migration (steps below).
- **Worktree:** `incubation-migration` (branch `incubation-migration`, orphan, `.session/` only; no code)
- **Role / scope:** Mission owner. Each step needs its go-ahead; no pushes without per-operation approval.
  Writes only here, plus the new workspace (user-granted 2026-11-25: the new root and its worktrees) except
  `session-tracking`, which stays empty until told.
- **Ledger / log:** active `.session/<slug>.md`; captured retired `.session/ledger/<slug>.md`.
  ⚠ The previous sessions' ledgers are in the OLD workspace
  (`/home/dean/code/llm-d/dean-llmd-scaler-sandbox/worktrees/incubation-migration/.session/`): do not read them
  upfront; create your own ledger and open it with `Continues: <that path>`.

## Task

- **Plan / spec:** `.session/plan.md` (decisions approved 2026-11-10; pull on demand)
- **Context:** `.session/review-rules-2026-11-25.md` (read-only review of the new policy-writer rules; 84 findings),
  `~/.claude/README.md` (global config, profiles, tokens, gotchas)
- **Refs:** old workspace `/home/dean/code/llm-d/dean-llmd-scaler-sandbox` (reference only)
- **Limits:** nothing pushed without per-operation approval; nothing written to `session-tracking`; no change to
  `~/.claude/settings.json`, `~/.profile` or VS Code settings without showing the diff first (compare the live file
  with its profile before any copy; check VS Code's own Claude settings before changing auth or env)

## Execution

### Steps / subtasks

- [x] 1. Fork (origin) `deanlorenz/llm-d-scaling-manager`
- [x] 2. Container root, bare clone in `repo/`, remotes (origin = fork, upstream = incubation repo, push disabled)
- [x] 3. Worktree `main` (fast-forwarded to upstream 54e9f94b on 2026-11-25)
- [x] 3a. Agentbus bus `llmd-sm` registered for the new root and tested (2026-11-25)
- [x] 4. New orphan `policy-writer`: 069380bd plain copy of old policy-writer@d23d9d7e3, d7ca66e8 path rewrite,
  f00935a7 ledger-harvest moved to `~/.claude/bin/ledger-harvest` (a machine tool). Rules NOT yet reviewed/fixed: see 4a.
- [ ] 4a. Fix the new policy-writer rules from the review (`.session/review-rules-2026-11-25.md`): 5 blockers, 53 fixes.
  Open decisions D1-D5 are at the end of the report; D3 (bootstrap before first install) goes to a suggestion-box entry.
- [ ] 5. `session-tracking` via the first-install path of `conv-install-to-session-tracking`: worktree exists and is
  EMPTY on purpose; "first install" authorization was given once and is unused. Only after 4a.
- [x] 6. This worktree (created 2026-11-25); `.session/` ported
- [ ] 7. Root `CLAUDE.md` (an anchor; tested: a root CLAUDE.md in the non-git container loads in every
  worktree, and upstream main's own CLAUDE.md = "see @AGENTS.md" loads as well), `llm-d-scaling-manager.code-workspace`
  (session-tracking first), `repo/info/exclude` entries (`.claude/skills`, `.bob`, `*.wip`). Skills links only AFTER
  the first install (user, 2026-11-25).
- [ ] 8. Memory: global memory design approved in principle (user wants repo-agnostic notes global). Draft:
  `.session/drafts/memory-global/` (15 generic notes + statusline note + new MEMORY.md). Tested:
  `autoMemoryDirectory` is honored. To apply (diff first): copy into `~/.claude/memory/`, set
  `autoMemoryDirectory` in profiles/main.json, alt.json and settings.json; delete the stale `~/.claude/memory/index.md`.
- [ ] 9. Link older missions (in the old workspace) from the new `session-tracking`; blocked by 5.

**Last completed:** step 6 (this worktree). Earlier today: global config tracked on `claude-global` (pushed, private
repo), profiles/apiKeyHelper, autoMode rewritten, harvest hook fixed, rules review rr-1.

**Next step / resume point:** ask the user which to take first: (a) the review decisions D1, D2, D4, D5 then fixes in
`policy-writer` (4a), (b) apply the global memory plan (8), (c) steps 7 and 9 pieces that do not depend on the install.
Do not start any of them unasked.

### Status

Workspace is usable: `main`, `policy-writer`, `session-tracking` (empty), `incubation-migration`. Agentbus: this
workspace uses bus `llmd-sm`; publish ownership on `mission.incubation-migration` when you start.

### Known issues

- The docker litellm proxy for the `proxy` profile is not running (`~/.litellm` compose is outdated); untested.
- A session started under an old `settings.json` holds the old `ANTHROPIC_AUTH_TOKEN` in its environment and it
  outranks `apiKeyHelper`: use fresh sessions.
- The VS Code extension "Token Usage" rewrites `~/.claude/settings.json` (adds/removes its `Stop` hook group).
- `~/.claude` branch `claude-global` has one unpushed commit (README); push needs approval.
- The bare clone created local branches for every upstream branch (`fix/*`, `docs/*`, ...): prune later if needed.
- Old workspace sessions' memory dir is the old per-repo one; see step 8.

## Session log
(append-only; the first session started in this worktree adds its own line on start)
