# Post-mortem: what the migration changed on 2026-11-25, and whether each change belongs to the migration

Sources: the old-workspace ledger `2026-11-24-incubation-migration-2.md` (old `.session/`), `git log` of the new
worktrees, `~/.claude` git log. M = required by the migration (plan steps 1-9). D = migration-driven design change the
user approved. R = related request that grew out of the migration (user-requested). N = not migration; user-initiated.

## A. New workspace (/home/dean/code/llm-d/llm-d-scaling-manager)

| # | Change | Where | Class | Note |
|---|---|---|---|---|
| A1 | Fork, container root, bare `repo/`, remotes, `main` worktree | steps 1-3 (2026-11-10/11) | M | |
| A2 | `main` fast-forwarded cea2f9e -> upstream 54e9f94b | `main` | M | user: "refresh the main repo from upstream"; nothing pushed, `origin/main` still old |
| A3 | Agentbus bus `llmd-sm` registered, tested | `~/.agentbus/repos.json` | M | outside the workspace; user approved the exact command |
| A4 | New orphan `policy-writer`: 069380bd plain copy of old tip d23d9d7e3 | policy-writer | M | |
| A5 | d7ca66e8 path rewrite (15 files, +39/-38) | policy-writer | M | every hunk is a path change; 6 hand edits need behavior (resume-mission `$TRACKING` sibling path, coder worktrees at `../<name>`, agentbus line) |
| A6 | f00935a7 ledger-harvest scripts moved out of the rules repo to `~/.claude/bin/ledger-harvest` (5 files removed, 3 doc refs changed) | policy-writer | D | grew out of "the hook must work in several workspaces"; user chose option A; content verified identical before removal |
| A7 | `session-tracking`: empty orphan worktree, then first install 194b528e (34 files) | session-tracking | M | installed BEFORE the rules were reviewed, against the user's earlier ordering; user then chose to keep it |
| A8 | `incubation-migration` worktree, `.session/` ported, STATE/plan rewritten | incubation-migration | M | plan step 6 |

Not done, still open (plan): root `CLAUDE.md`, `.code-workspace`, `repo/info/exclude`, skills links (the whole `.claude/skills`
folder is linked to `session-tracking/claude-skills`; `pr-review` is an upstream skill that is not linked or handled per worktree,
settled earlier by the policy-writer mission), `missions/` + `suggestion-box/` in the new `session-tracking`, and, after the new
workspace works: deciding which older missions to migrate or copy to it (migration scope).

## B. Global Claude config and machine (outside the workspace)

| # | Change | Class | Note |
|---|---|---|---|
| B1 | `~/.claude/bin/ledger-harvest/` (5 files) + the three harvest hooks in `settings.json` point there | D | needed so hooks work from any workspace |
| B2 | `settings.json`: `ANTHROPIC_AUTH_TOKEN` removed from `env`, `apiKeyHelper` per profile; `profiles/{main,alt,cb-*,proxy}.json`; default = copy of main | D | user ruling (2026-11-25): related to the migration; the tools and where they are used must be flexible; the plaintext token also had to leave the file before it could be tracked |
| B3 | `~/.profile`: `LOCAL_PROXY_KEY` appended; `~/.bash_aliases`: `cbx-*`, `claude-main/alt/proxy` appended | D | part of B2; user approved |
| B4 | Allow rules for the new `policy-writer` path; dead `Write(...)` rule dropped | R / N | the new path rules are M; dropping the dead rule is cleanup, not migration |
| B5 | `autoMode` text rewritten for the new workspace (old one kept as a one-line reference) | M | the new workspace becomes the main one |
| B6 | `~/.claude` became a worktree of `dean-ai-overlay` (branch `claude-global`), allowlist `.gitignore`, `README.md`; repo made private; two pushes | N | user-initiated ("the global settings are getting bigger ... should be tracked") |
| B7 | Global memory: `autoMemoryDirectory` -> `~/.claude/memory`, 15 notes + statusline note, `index.md` removed; 7 old-repo notes archived | M (plan step 8) | the shape (one global pool) is the user's decision |
| B8 | Root `CLAUDE.md` loading test, memory-directory tests, overlay-merge test, header-dump test | - | scratch only; every scratch file removed |

## C. Old workspace

Changed: only the files of the old MIGRATION mission's own worktree (`worktrees/incubation-migration/.session/`: ledger
entries, drafts, task files, `STATE.md` with a "MOVED" pointer; commits on its branch `incubation-migration`). No other old
worktree (`policy-writer`, `session-tracking`, mission worktrees) was written to: they were only read. No rule, skill,
convention or production file of the old repo was touched; the old per-repo memory directory is unchanged.
Verified on actual files, not only git (2026-11-25): in the old `policy-writer` and `session-tracking` worktrees no production-path
file is newer than the tip commit, there are no `.wip` lock files, no ignored or untracked files under the production paths
(except the untracked upstream `pr-review` in `session-tracking`), and the old `policy-writer` working files are byte-identical
to the copy that was imported (069380bd).

## D. Rules: scan for references to the old workspace (new `policy-writer` and new `session-tracking`, same result)

Searched HEAD of both for `worktrees/`, `dean-llmd`, `llm-scaler`, `llmd-scaler`, `ev-shindin`, `biranofer`, `ofer`, `WVA`,
`workload-variant`, `feat/wva`, `/home/dean`, `repo-restructure`, `bobi`, `claude-skills/ledger-harvest`, `sandbox`.
Remaining hits, all intended or generic: the workspace-root sentence in `conv-background-agents` L26 (names the new root and
bus `llmd-sm`); the word "worktrees" meaning git worktrees; `<git-common-dir>/worktrees/$WTID/info/exclude` (a git-internal
path); "sandbox" as a generic word (sandboxed coder, no filesystem sandbox). No old repo name, old branch, old path or
old project name remains. A grep does not prove the prose still fits: that is the job of the refreshed review.
