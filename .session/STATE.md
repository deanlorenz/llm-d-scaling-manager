# incubation-migration

## Orientation

- **Conventions:** `policy-writer/CONVENTIONS.md` (workspace root `/home/dean/code/llm-d/llm-d-scaling-manager`; the
  production copy `session-tracking` got its first install on 2026-11-25 (194b528e, from policy-writer@f00935a7) and
  is the place to read rules from; `policy-writer/` is where they are edited; skills are linked into this worktree
  (`.claude/skills` -> `session-tracking/claude-skills`, set up 2026-11-25)
  *(read this first, before any other file)*
- **What / goal / mission:** Move our work to the new repo
  `https://github.com/llm-d-incubation/llm-d-scaling-manager`: flat workspace (container root, bare `repo/`, every
  worktree a direct child), rules and skills in the new `policy-writer`, global Claude config tracked in
  `~/.claude`. This worktree finishes what is left of the migration (steps below).
- **Worktree:** `incubation-migration` (branch `incubation-migration`, orphan, `.session/` only; no code)
- **Role / scope:** Mission owner. Each step needs its go-ahead; no pushes without per-operation approval.
  Writes only here, plus the new workspace (user-granted 2026-11-25: the new root and its worktrees) except
  `session-tracking`, which gets installs of reviewed `policy-writer` commits (conv-install-to-session-tracking) and, as the setup skill's documented exception, untracked convenience links under `missions/` (and the empty `suggestion-box/`); nothing else is written there.
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
  f00935a7 ledger-harvest moved to `~/.claude/bin/ledger-harvest` (a machine tool). Rules review and staleness check: see 4a.
- [ ] 4a. Rules review (NOT a migration step; user, 2026-11-25): rr-1 (`.session/review-rules-2026-11-25.md`, 84 findings)
  may be stale or partly wrong. rr-2 (`.session/task-rr-2.md`, report `.session/review-staleness-2026-11-25.md`) checks (A) whether
  the new rules equal the newest rules that exist in the old workspace and (B) which rr-1 findings are already addressed.
  Migration does NOT fix rules. Rule issues found along the way are written up as suggestion-box entries (drafts in
  `.session/drafts/`, submitted after the migration, the user said wait) and fixed by a new policy-writer session. User ruling on
  rr-1's decisions: D1 yes (the `missions/` index, suggestion box and pending-commits flow live in `session-tracking`);
  D2-D5 are rule-quality questions, not migration decisions; they are VALID open items for the policy-writer mission and
  must not be dropped: each becomes a suggestion-box draft after the refreshed review verifies it (rr-2 found D4/D5/D2 are
  NOT addressed in the old repo either; my earlier note "already handled" was wrong). D3 waits for the end of the migration.
  rr-2 RESULT (2026-11-25, `.session/review-staleness-2026-11-25.md`): the new rules ARE the newest that exist (old policy-writer
  d23d9d7e3 and old session-tracking 36d27bcfb have identical trees; nothing newer anywhere in the old repo). rr-1 was partly
  wrong/stale (e.g. PR-prep rebase claim). Findings B2, B4-B7 exist identically in the old repo: suggestion-box material, not
  migration. Migration-specific: `missions/` and `suggestion-box/` absent in the new session-tracking, (user: the pr-review
  question is settled: the whole `.claude/skills` folder is linked to `session-tracking/claude-skills`, upstream's `pr-review` is not
  linked or handled per worktree; my earlier "missing untracked pr-review copy" item is withdrawn).
  `conventions/archived/` (11 files) was left behind on purpose.
  rr-3 RESULT (2026-11-25; `.session/review-rules-verified-2026-11-25.md`, suggestion drafts `.session/drafts/suggestions-from-rr3-2026-11-25.md`):
  all 84 rr-1 findings re-checked on the actual lines: 66 CONFIRMED, 7 FALSE, 11 STALE. Of the 66: 53 rule-quality items that exist
  identically in the old rules (32 suggestion drafts, NOT submitted: user said wait until the migration ends), 11 SETTLED (pr-review,
  missions index/suggestion-box in session-tracking, harvester, profiles), 2 MIGRATION-caused rule-text leftovers (row 9: CONVENTIONS.md:110
  names `conventions/archived/`, which was left behind on purpose; row 73: `resume-mission` L22/69/154 say "the main repository", which no
  longer exists as a checkout in the flat layout). Those two are also rule edits: they go to the suggestion box, not into the migration.
  Also noted: `conv-feature-worktree-setup` L60 still says to report a tracked pr-review as a blocker, against the settled decision (old
  policy-writer STATE.md L35-36, spec-policy-writer.md T6).
- [x] 5. `session-tracking` first install DONE 2026-11-25: root commit 194b528e from policy-writer@f00935a7 (34 files,
  tree ids verified equal, local, not pushed). It carries the rules BEFORE the review fixes (user, 2026-11-25: keep it,
  option 1): the fixes of 4a go through `policy-writer` and reach `session-tracking` by normal incremental installs
  (cherry-picks, `LAST_SHA` = f00935a7). The "first install" authorization is consumed.
- [x] 6. This worktree (created 2026-11-25); `.session/` ported
- [ ] 7. (partly done 2026-11-25: skills links, `.bob` links, `repo/info/exclude` entries, `missions/incubation-migration/` links and empty
  `suggestion-box/` in `session-tracking` are in place, verified; STILL OPEN: root `CLAUDE.md`, `.code-workspace`; drafts in `.session/drafts/root/`, not applied; `.bob/skills` is now a dir-link to `session-tracking/claude-skills` like `.claude/skills`, user 2026-11-25) Root `CLAUDE.md` (an anchor; tested: a root CLAUDE.md in the non-git container loads in every
  worktree, and upstream main's own CLAUDE.md = "see @AGENTS.md" loads as well), `llm-d-scaling-manager.code-workspace`
  (session-tracking first), `repo/info/exclude` entries (`.claude/skills`, `.bob`, `*.wip`). Skills links only AFTER
  the first install (user, 2026-11-25).
- [x] 8. Memory (applied 2026-11-25): one global auto-memory directory `~/.claude/memory/` (15 generic notes +
  statusline note, rebuilt MEMORY.md, stale index.md removed), `autoMemoryDirectory` set in profiles/main.json,
  alt.json and the live settings.json; verified from `main`, the container root and the old workspace. Committed
  on `claude-global` (9774278, not pushed). The 7 old-repo-only notes stay archived in the old per-repo directory
  `~/.claude/projects/-home-dean-code-llm-d-dean-llmd-scaler-sandbox/memory/` (invisible to sessions). Draft kept in
  `.session/drafts/memory-global/`.
- [ ] 9. Older missions: link them from the new `session-tracking`; and, once the new workspace works, decide which of them to
  migrate or copy into it (migration scope, user 2026-11-25) (needs the review decision D1: does
  the `missions/` index live there; any write into `session-tracking` needs the user's go-ahead).

**Last completed:** step 8 (global memory applied), after step 6 (this worktree). Earlier today: global config tracked
on `claude-global` (private repo; first 3 commits pushed), profiles/apiKeyHelper, autoMode rewritten, harvest hook
fixed, rules review rr-1.

**Next step / resume point:** read the rr-2 staleness report and show the user its verdict; then ask which to take first:
(a) re-sync `policy-writer` with the newest old rules if rr-2 finds it stale (a migration fix); (b) the pieces of step 7 that do not depend on the install (root `CLAUDE.md`,
`.code-workspace`, `repo/info/exclude`); (c) pushing `claude-global` (2 commits ahead: README, memory). Do not start
any of them unasked. The suggestion-box draft (`.session/drafts/suggestion-box-2026-11-25-1800.md`) is not submitted.

### Status

Workspace is usable: `main`, `policy-writer`, `session-tracking` (first install done), `incubation-migration`. Agentbus: this
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
