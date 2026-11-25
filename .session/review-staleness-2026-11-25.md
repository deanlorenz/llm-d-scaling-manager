# Staleness check of the new rules and of review rr-1 (rr-2, 2026-11-25)

Read-only. Paths: OLD = `/home/dean/code/llm-d/dean-llmd-scaler-sandbox/worktrees/{policy-writer,session-tracking}`; NEW = `/home/dean/code/llm-d/llm-d-scaling-manager/{policy-writer,session-tracking}`. Production paths = `CONVENTIONS.md`, `conventions/`, `claude-skills/`, `bob/`.

## Verdict (three lines)

(i) Yes: the new rules are the latest rules that exist. Old `policy-writer` tip `d23d9d7e3` (2026-11-24 21:05) and old `session-tracking` tip `36d27bcfb` have identical production trees (tree ids equal, A2); nothing newer exists in the old repo. The new rules equal that state plus the two intended rewrites, plus one unexplained omission (`conventions/archived/`, 11 files), which the old policy note itself says to leave behind.
(ii) Stale or wrong in rr-1: the "PR-prep agent rebases against CONVENTIONS L111" claim (that line now says "A rebase is run only as rule 16 says"); the `.claude/skills` "cannot work" blocker is only half right (the rule text does say blocker, but 3 old worktrees cut from upstream branches run with the dir-symlink and a clean `git status`); the `-S`/conventional-commit/`make lint`/merge-queue finding is not a staleness issue, it is genuinely unaddressed and is a new-upstream question, not an old-rules question.
(iii) Not migration-specific, exist identically in the old repo: coder step d exclude command (B2), generic PR rules (B4), no "update an open PR when base moves" rule (B5), `git -C` / `EnterWorktree` / task-file-name contradictions (B6), and the `.claude/skills` real-directory case (B1, B7). Migration-specific: B3 (`missions/`, `suggestion-box/` and `CONVENTIONS.md` not yet present in new `session-tracking`).

## A1. File-level comparison

Commands: `diff -rq -x ledger-harvest -x pr-review <A>/<path> <B>/<path>` for each of the four production paths, then `diff -r` on each differing file (excluding `archived`).

| Pair | Result |
|---|---|
| OLD policy-writer vs OLD session-tracking | No differences (only `claude-skills/pr-review`, untracked upstream copy on session-tracking, and `claude-skills/ledger-harvest`, excluded by the task). |
| NEW policy-writer vs NEW session-tracking | No differences (`CONVENTIONS.md`, `conventions/`, `claude-skills/`, `bob/`). Neither has `pr-review` or `ledger-harvest`. |
| OLD policy-writer vs NEW policy-writer | 17 files differ + 1 directory only in OLD (below). |
| OLD session-tracking vs NEW session-tracking | Same 17 files + same directory (OLD st == OLD pw). |

`bob/custom_modes.yaml`: identical in all four. Every other file under `conventions/` and `claude-skills/` is byte-identical between OLD and NEW.

Differing files (OLD pw vs NEW pw; the OLD session-tracking pair is identical in content):

| File | Explained? | Differing lines |
|---|---|---|
| `CONVENTIONS.md` | yes (path rewrite) | adds new line 54 `<workspace-root>/ ← container, not a git repo; repo/ is the bare clone, every worktree is a direct child`; lines 67-74, 85: `worktrees/<mission-name>/...` and `worktrees/session-tracking/claude-skills` become `<mission-name>/...`, `session-tracking/claude-skills`. |
| `conventions/coder.md` L19 | yes (harvest move) | `HP="$(git worktree list ...)/claude-skills/ledger-harvest/harvest-registry.py"` becomes `HP="$HOME/.claude/bin/ledger-harvest/harvest-registry.py"`. |
| `conventions/mission-owner.md` L54 | yes (path) | `worktrees/session-tracking/suggestion-box/...` becomes `session-tracking/suggestion-box/...`. |
| `conventions/policy-writer.md` L10, 13, 29, 65, 83, 93-94 | yes (path) | `worktrees/policy-writer` -> `policy-writer`, `worktrees/session-tracking` -> `session-tracking`; "repo-root-relative" -> "workspace-root-relative". |
| `conventions/resume-and-handoff.md` L63 | yes (path) | `worktrees/session-tracking/CONVENTIONS.md` -> `session-tracking/CONVENTIONS.md`. |
| `conventions/session-start.md` L14, 17 | yes (path) | same pattern. |
| `conventions/state_template.md` L8 | yes (path) | same pattern. |
| `conventions/task_file_template.md` L40, 42, 55 | yes (path) | same pattern, `git log ... -- worktrees/session-tracking/` -> `session-tracking/`. |
| `conventions/worktree-delegation.md` L105-110, 147 | yes (coder worktrees at `../<name>`) | `git worktree add worktrees/<name> ...` -> `git worktree add ../<name> ...   # sibling of the mission worktree`; `cp`/`git -C worktrees/<name>` -> `../<name>`. |
| `claude-skills/conv-background-agents/SKILL.md` L26 | yes (agentbus note) | `/home/dean/code/llm-d/dean-llmd-scaler-sandbox` -> "the workspace root registered in `~/.agentbus/repos.json` ... currently `/home/dean/code/llm-d/llm-d-scaling-manager`, bus `llmd-sm`". |
| `claude-skills/conv-feature-worktree-setup/SKILL.md` L58, 95 | yes (path) | `worktrees/session-tracking/claude-skills` -> `session-tracking/claude-skills`. |
| `claude-skills/conv-install-to-session-tracking/SKILL.md` L8, 47-48 | yes (path) | `worktrees/policy-writer`/`worktrees/session-tracking` -> bare names. |
| `claude-skills/conv-state-vs-ledger/SKILL.md` L40, 42, 55 | yes (path) | same. |
| `claude-skills/conv-unexplained-files/SKILL.md` L39-42 | yes (path) | same. |
| `claude-skills/ledger-capture/SKILL.md` L96 | yes (path) | `$(dirname "$TRACKING")/$MISSION_NAME` form for the mission worktree path text. |
| `claude-skills/resume-mission/SKILL.md` L96, L305 | yes (path + harvest move) | L96 `worktrees/$MISSION_NAME` -> `$(dirname "$TRACKING")/$MISSION_NAME`; L305 `$TRACKING/claude-skills/ledger-harvest/harvest-registry.py` -> `$HOME/.claude/bin/ledger-harvest/harvest-registry.py`. |
| `claude-skills/wind-down/SKILL.md` L87 | yes (harvest move) | `HP=...` becomes `HP="$HOME/.claude/bin/ledger-harvest/harvest-registry.py"`. |
| **`conventions/archived/` (11 files: agentbus-user-interaction, agentbus, coder-orchestration, feature-worktree-setup, install-to-session-tracking, pr-branch, pr-workflow, push, unexplained-files, wip-editing, working-outside-worktree)** | **no, not on the task's intended list** | Tracked in OLD policy-writer (`git ls-files conventions/archived` -> 11) and OLD session-tracking (11); NEW policy-writer -> 0. Mitigating evidence: `/home/dean/code/llm-d/dean-llmd-scaler-sandbox/worktrees/policy-writer/.session/incubation-migration-policy-note.md` point 2: "Leave `backup_rules/` and `conventions/archived/` behind, as planned." The archived files are retired rules whose content lives in the conv-* skills. The only live references are two prose mentions (`CONVENTIONS.md` L110, `conv-install-to-session-tracking` L177/180), which only say "outside `conventions/archived/`" and do not dereference the folder. |

Finding from A1: exactly one difference is outside the two intended categories, `conventions/archived/` absent in NEW; it matches a stated migration decision (old policy note point 2). Nothing else: no content drift, no missing or extra rule text. `grep -rn "worktrees/"` over NEW production paths leaves only the git-internal `<common-dir>/worktrees/$WTID/info/exclude` (`conv-coder-orchestration` L71, `worktree-delegation.md` L58) and `.claude/worktrees/` (L138): correct as git internals, not stale layout.

## A2. Is anything newer than d23d9d7e3?

Commands (OLD repo, run from `worktrees/policy-writer`):

- `git rev-parse policy-writer session-tracking d23d9d7e3` -> `policy-writer == d23d9d7e3`, `session-tracking == 36d27bcfb`. `git rev-parse <ref>:conventions <ref>:claude-skills <ref>:bob <ref>:CONVENTIONS.md` is identical for `d23d9d7e3` and `36d27bcfb` (conventions `30b163cd`, claude-skills `e4c25ed0`, bob `271472ec`, CONVENTIONS.md `f43e9052`). `git diff --stat fc4644de5 d23d9d7e3 -- <production paths>` prints nothing: the five commits after `fc4644de5` (the install source) touch only `.session/`.
- `git log --all --since='2026-11-24 19:00' -- CONVENTIONS.md conventions claude-skills bob`: six commits, all on `policy-writer` or `session-tracking` and all ancestors or install copies of the same content (`169ecd25a`/`9a43a7063` first-install path; `97f5b961c`/`0253eb1ab` setup-skill fix; `90fd0d46c`/`c43b8aa1f` queued-message fix). The wider `git log --all --not d23d9d7e3 -- <paths>` list is long but consists of session-tracking-side copies and other branches' history from before 2026-11-24 (the last non-ancestor rule commits are the install copies at 20:08-20:57 on 11-24).
- Branch rule trees: `git for-each-ref refs/heads refs/remotes` then `git rev-parse <b>:conventions`: only `policy-writer` and `session-tracking` carry the current tree. `origin/policy-writer` (3bbd23c6a, 2026-09-23) and `origin/session-tracking` (5668ca962, 2026-11-18) and `scratch-cb-trial` carry older trees; local `incubation-migration` (old repo) carries the same tree as `origin/policy-writer` (September). None is newer.
- `git stash list` -> empty. `git status --porcelain -- CONVENTIONS.md conventions claude-skills bob` over every directory in `worktrees/`: only `session-tracking` reports `?? claude-skills/pr-review` (the known untracked upstream skill, STATE "Limits": never commit its removal). Full `git status` of old policy-writer: clean; old session-tracking: only `pr-review` and `?? suggestion-box/processed-2026-11-11-1919-policy-writer.md`.
- Suggestion box: `ls worktrees/session-tracking/suggestion-box | grep -v '^processed-'` -> nothing (only `.gitkeep`). STATE says "Every suggestion entry is now processed."
- Old policy-writer `.session/STATE.md` (298 lines, last write 2026-11-24 21:02). "Last completed": "Installs: latest `36d27bcfb` (from `policy-writer@fc4644de5`); no production commit is pending." Status: session 26 parked, checkpoint. "Next step" lists only not-started options: (1) item (g) remove "session appends to the ledger" rules in 7 places (scope not asked yet); (2) hook locator script (global, needs approval); (3) push; (4) other missions; (5) Bob hooks. None is a rule change in progress or half-installed.
- Newest ledger `.session/2026-11-23-policy-writer-26.md` (43 KB, 21:05): last entries: "Seventh install 2026-11-24 ... 36d27bcfb ... No production commit is pending now" and "Checkpoint 2026-11-24 ... lc-26 Verified ... nothing flagged."
- `.session/incubation-migration-policy-note.md` (18 lines, 2026-11-24 20:57): the note the new workspace was built from. Point 2 "Port from the current production state, not the Nov 10 copy ... Latest install: `9432bb8d5`" (since then one more install, `36d27bcfb`, noted in point 7 "first-install path ... installed"). Point 4 predicts the path rewrite (35 references, `resume-mission` L96, `worktree-delegation.md`, `conv-background-agents` L26): exactly what A1 shows. Note: the old STATE and policy note list pending global files (hook locator script, settings) that are outside the rule tree.

State plainly: the newest rule state is old `policy-writer` @ `d23d9d7e3` == old `session-tracking` @ `36d27bcfb` (production paths). Nothing newer exists: no uncommitted rule edits, no stash, no unprocessed suggestion, no other branch, no pending install. The new rules equal that state plus the A1 rewrites.

## A3. Lineage and dates

| Repo | Ref | Commit | Date (+02:00) | Subject |
|---|---|---|---|---|
| OLD | policy-writer tip | `d23d9d7e3` | 2026-11-24 21:05:36 | ledger: checkpoint 2026-11-24 done |
| OLD | policy-writer, install source | `fc4644de5` | 2026-11-24 20:54:45 | ledger: first-install path applied |
| OLD | session-tracking tip | `36d27bcfb` | 2026-11-24 20:57:39 | install: ... from policy-writer@fc4644de5 |
| OLD | session-tracking, previous | `169ecd25a` | 2026-11-24 20:57:20 | conv-install-to-session-tracking: first-install path |
| NEW | policy-writer | `069380bd` | 2026-11-25 11:13:02 | chore: import production rules and skills from old policy-writer@d23d9d7e3 |
| NEW | policy-writer | `d7ca66e8` | 2026-11-25 11:21:12 | docs: rewrite worktrees/<name> paths for the flat workspace layout |
| NEW | policy-writer (tip) | `f00935a7` | 2026-11-25 14:20:32 | refactor: ledger-harvest becomes a machine tool in ~/.claude/bin/ledger-harvest |
| NEW | session-tracking (tip, only commit) | `194b528e` | 2026-11-25 18:02:08 | install: ... from policy-writer@f00935a7 (first install: snapshot of the tree) |

Commands: `git log -N --format='%h %ci %s'` in each. `git diff --stat 069380bd d7ca66e8` -> 15 files, 39 insertions, 38 deletions (the path rewrite only). The import commit `069380bd` adds `CONVENTIONS.md`, `bob/`, `claude-skills/`, `conventions/` (it was a "production rules" import, which explains why `archived/` was never copied). New repo ordering is strictly after the old tips (about 14 hours later). The two repos have different object stores; the lineage is by the commit subjects and content, not by id.

## B. Re-check of rr-1's main claims

Searches were run on the NEW rules and on the OLD policy-writer tree (`d23d9d7e3`). Where a file is byte-identical in OLD and NEW, the OLD answer is the same.

### B1. Blocker: `.claude/skills` dir-symlink in a worktree cut from upstream `main` (tracked `pr-review`)

Verdict: half addressed. The rule detects and names the situation but resolves it by stopping; real-world practice in the old workspace shows the symlink does work.

- `claude-skills/conv-feature-worktree-setup/SKILL.md:60` (identical in OLD): "**If `pr-review` is a tracked git file in this worktree** (run `git -C MISSION_WT ls-files .claude/skills/pr-review` to check), do not replace the `.claude/skills` directory — skip to step 4 and report this as a blocker." And L167: "`.claude/skills` dir-symlink: created / already existed / blocked (pr-review tracked)". Command: `grep -nE "pr-review|real (dir|director)|tracked" claude-skills/conv-feature-worktree-setup/SKILL.md`. So rr-1's "stops with blocker" is accurate to the text. `resume-mission` Step 5b (L146-150) then fails "BROKEN" for a real directory.
- But: the rule does not say what to do instead, and the old workspace did something else. `ls -ld` of old worktrees cut from upstream-derived branches: `benchmark-waldorf/.claude/skills`, `single-analyzer/.claude/skills`, `composite-analyzer/.claude/skills` are dir-symlinks to `session-tracking/claude-skills` although `git ls-files .claude/skills` there shows tracked `.claude/skills/pr-review/SKILL.md`; `git status --porcelain --untracked-files=no` in `benchmark-waldorf` prints nothing. Old `session-tracking` keeps an untracked copy `claude-skills/pr-review/SKILL.md` identical to the tracked file in `benchmark-waldorf` (`diff -q` same); that is the mechanism (CONVENTIONS.md L63 lists `pr-review/SKILL.md` in the layout). The old STATE ("Limits": "`claude-skills/pr-review` on `session-tracking`: upstream skill; never commit its removal, never stage/ignore/delete it, do not ask about it again") and spec T6 ("`pr-review` suppression via `skillOverrides: {"pr-review": "off"}` in `~/.claude/settings.json`") confirm the earlier handling.
- New workspace: `/home/dean/code/llm-d/llm-d-scaling-manager/session-tracking/claude-skills/` has no `pr-review` (A1), and `main/.claude/skills/pr-review/SKILL.md` differs from the old copy (`diff -q` differs: it is a newer upstream version). So in the NEW workspace the old mechanism is missing; whether a symlink over a tracked `pr-review` stays clean in a worktree cut from the new upstream main was not tested here (read-only). rr-1's blocker stands as "rule gives no path forward", but "cannot work" is not proven and old practice contradicts it.
- Not migration-specific: the rule text is identical in OLD. The migration-specific part is only that new session-tracking lacks the `pr-review` copy.

### B2. Blocker: coder startup step d appends to `<common-dir>/worktrees/$WTID/info/exclude`

Verdict: genuinely not addressed; exists identically in OLD.

- `conventions/worktree-delegation.md:58` and `claude-skills/conv-coder-orchestration/SKILL.md:71`: `echo ".session/" >> "$(git rev-parse --git-common-dir)/worktrees/$WTID/info/exclude"`. Same lines in OLD (`grep -rn "info/exclude"` on old tree). Step e (L61-62 / L74) "Fail closed" then aborts.
- Evidence of the defect, both repos: NEW `ls -la /home/dean/code/llm-d/llm-d-scaling-manager/repo/worktrees/policy-writer` shows `COMMIT_EDITMSG HEAD commondir gitdir index logs`, no `info/`; OLD `ls /home/dean/code/llm-d/dean-llmd-scaler-sandbox/.git/worktrees/policy-writer` shows the same, and `ls .git/worktrees/*/info` -> "No such file or directory". `git rev-parse --git-path info/exclude` in NEW policy-writer prints `/home/dean/code/llm-d/llm-d-scaling-manager/repo/info/exclude` (the common file). The sibling rule `conv-feature-worktree-setup/SKILL.md:81` already uses `$(git -C MISSION_WT rev-parse --git-common-dir)/info/exclude` and the old archived rule says "`.git/info/exclude` is not per-worktree" (`conventions/archived/feature-worktree-setup.md:51`). Nothing in the old STATE, spec or audit (`grep WTID`) records this as known or fixed.
- Whether the old coder launches succeeded despite this was not checked (a failed append in a missing directory would abort step d); the rule text is in any case wrong in both repos.

### B3. Blocker: rules assume session-tracking holds `missions/` index, suggestion-box and CONVENTIONS.md

Verdict: genuinely not addressed for the new workspace; the rules assume it in OLD too (that is the old design), so the question is migration-specific.

- `CONVENTIONS.md:58, 66, 79, 88` (identical modulo path in OLD): suggestion-box, `missions/` symlinks, "Access other missions' tracking files via `session-tracking/missions/<mission-name>/`". `grep -rnE "missions/|suggestion-box|pending-commits"` over the rule tree: 34 hits in both OLD and NEW.
- `grep -rniE "intentionally empty|bootstrap|first install|until .*install"` finds only the install skill's first-install path (`conv-install-to-session-tracking/SKILL.md:20, 122-164`), which makes new `session-tracking` hold `CONVENTIONS.md`; nothing about `missions/`, suggestion-box, or reading from `policy-writer/` before the install. Old policy note point 2 says the production state has `ledger-harvest`, 13 conventions, 19 skills, and the migration analysis `.session/migration-compat-2026-11-24.md:17` says `missions/<m>/` links "work in the flat layout". Neither decides whether the new `session-tracking` keeps the index. The new `session-tracking` now has `CONVENTIONS.md` (commit `194b528e`), so rr-1's "every read of `session-tracking/CONVENTIONS.md` fails until the first install" is stale after 18:02 today; `missions/` and `suggestion-box/` are still absent (`ls -A` of NEW session-tracking: `.git CONVENTIONS.md bob claude-skills conventions`).

### B4. PR skills name no `-S`, conventional commits, `make lint/test`, merge queue

Verdict: genuinely not addressed in OLD or NEW; rules are generic by design.

- `grep -rniE "gpg|signed|signature|conventional commit|make lint|make test|merge queue|DCO|sign-off"` over production paths: only `conv-pr-branch/SKILL.md:26` ("Lint, DCO sign-off, and any project-required checks ... If the project has a `Makefile` target or CI pre-check script, use it."), `conv-pr-workflow/SKILL.md:12` ("Lint, DCO, and any project-required checks ... Use the project's `Makefile` target or pre-PR script"), `conv-push/SKILL.md:26`, `reviewer.md:25`, `conv-coder-orchestration/SKILL.md:135`. No `-S`, no conventional commits, no merge queue. OLD count is the same (the 4 skills are byte-identical).
- Old STATE/spec/compat docs: no mention (`grep -iE "make lint|merge queue|conventional commit|DCO|gpg"` on STATE and spec -> nothing relevant). The skills defer to `CONTRIBUTING.md` (`conv-pr-branch` rules 1, 7; `conv-pr-workflow` item 2). These are PR-branch facts for the new upstream repo, not a rule inconsistency; a decision for the user.

### B5. rr-1 D4: updating an open PR when upstream/main moves

Verdict: partly addressed; the "how" for an open PR is not. Exists identically in OLD.

- `CONVENTIONS.md:111`: "A rebase needs the user's approval of the exact command each time; a PR branch is re-cut with `conv-pr-branch`, never rebased."
- `conv-pr-branch/SKILL.md:10` rule 1: "Bring a stale PR branch current by re-cutting it from the base, never by rebasing it."
- `conv-push/SKILL.md:31-37` "Active PR branches": never push to an active PR branch without a warning, a commit list, and explicit approval "for that specific update". `wind-down/SKILL.md:64` "never force a push". `conv-guard-hook/SKILL.md:10`: the hook blocks rebase and force-push.
- `conv-coder-orchestration/SKILL.md:128` rule 16 ("No unprompted rebase ... A coder or PR-prep agent never rebases on its own because a branch looks stale: it reports the moved base to the parent") and L135 ("A narrowly scoped PR-prep agent (rebase, lint, DCO, test) ... A rebase is run only as rule 16 says"). So rr-1's specific claim that L135 contradicts CONVENTIONS L111 is stale: L135 now defers to rule 16, which requires the user's approval of the exact command (a slight remaining tension: rule 16 allows an ordered rebase, `conv-pr-branch` rule 1 says PR branches are never rebased).
- Not addressed: the case "PR already open, base moved, branch re-cut -> push needs force". `grep -rniE "force|force-with-lease|merge .* into"` finds no rule for it; `conv-push` Active PR branches covers approval but not the mechanism. Old spec lines 944-947 (rebase) say the same and stop there. Rule-quality question, not migration-specific.

### B6. rr-1 D5: `git -C`, `EnterWorktree`, task-file-name contradictions

Verdict: genuinely not addressed as a single rule; exist identically in OLD, with a recorded old decision for part of it.

- `git -C`: `CONVENTIONS.md:16` ("In a pinned session, `git -C` is blocked") and `conv-working-outside-worktree/SKILL.md:15` ("Never ... `git -C <other-path>` for reads") versus `resume-mission/SKILL.md:131` ("cross-worktree files except via explicit paths or `git -C`"), `conv-feature-worktree-setup/SKILL.md:48-49, 60, 71, 81, 102, 131` (`git -C MISSION_WT ...` for the mission worktree), `worktree-delegation.md:109-116` (`git -C ../<name> ...`). Command: `grep -rnE "git -C"`. Same in OLD.
- `EnterWorktree`: `resume-mission/SKILL.md:56` ("verify worktree isolation (`EnterWorktree`)") versus L121 `EnterWorktree(path: "<full path to $MISSION_WT>")`; `worktree-delegation.md:83`. Old STATE "Known issues": "Known gaps in `conv-working-outside-worktree` vs the archived rule (user decision 2026-11-16: do not change the rule): (1) the archived rule banned `EnterWorktree`/`ExitWorktree` ... the skill only says never `cd`. ... Revisit only if agents misuse `EnterWorktree`." This is a recorded user decision for one part (EnterWorktree ban not restored); the other part (the contradiction inside the rules) is not recorded.
- Task-file names: `.session/task-<id>.md` (`worktree-delegation.md:21-22, 51, 66, 108-110`; `conv-coder-orchestration` L42, 65, 76, 84), `STATE.coder` (`resume-mission` L54), `.session/<slug>.STATE.md` (`conventions/tasks.md:110`), `task-lc-<n>.md` (`resume-mission` L225-229, `wind-down` L107-111). Same in OLD. No doc in old STATE/spec resolves it.

### B7. rr-1 D2: how conv-* skills reach a worktree whose `.claude/skills` is a real directory

Verdict: addressed only as "report a blocker and stop" (B1), plus the real-directory branch for a directory made solely of symlinks. Exists identically in OLD.

- `conv-feature-worktree-setup/SKILL.md:65`: "If it is a real directory: list it first ... Every entry must be a symlink ... If it prints anything, stop and report it. Otherwise remove each symlink by its exact path with `rm`, then `rmdir`." So a real directory containing a real tracked file (`pr-review`) is exactly the stop case; no per-skill-link variant exists. `CONVENTIONS.md:85-87` offers the fallback "read any `SKILL.md` directly from `session-tracking/claude-skills/`".
- OLD: the same text (identical file apart from path), and the old practice (B1) was dir-symlink over the tracked `pr-review`. No old STATE/spec entry records a per-skill-link decision. User-level skills (`~/.claude/skills`) were not used for conv-* in the old repo; `pr-review` alone was suppressed globally (spec T6). Rule-quality question, not migration-specific.

## Notes on rr-1 accuracy (spot checks made while re-checking)

- rr-1 "33 of 33 files read" is plausible: `git ls-files` in NEW policy-writer counts the same tree (CONVENTIONS.md + 13 conventions + 19 SKILL.md + `bob/custom_modes.yaml`).
- rr-1 reviewed the correct, latest rule content; its findings are not "from a stale version". The only staleness is time-based inside the new workspace (new `session-tracking` got its first install `194b528e` at 18:02, after rr-1's start), which affects B3's "CONVENTIONS.md missing" part only.
