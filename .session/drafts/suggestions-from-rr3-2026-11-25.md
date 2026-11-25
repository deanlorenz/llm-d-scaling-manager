# Suggestion-box drafts from rr-3 (2026-11-25)

Source: `/home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration/.session/review-rules-verified-2026-11-25.md` (rr-3 verification of rr-1). Only rows that are CONFIRMED and class RULE-QUALITY-BOTH are drafted here: the same problem exists in the old latest rules. FALSE, STALE, SETTLED and MIGRATION rows are not suggestions.

Paths: N = `/home/dean/code/llm-d/llm-d-scaling-manager/policy-writer` (new rules). O = `/home/dean/code/llm-d/dean-llmd-scaler-sandbox/worktrees/policy-writer` (old rules, tip `d23d9d7e3`). Every file differs between N and O only at the lines listed in the verification file (path rewrites and the harvest helper path), so the old line is the same line number as the new one, except `CONVENTIONS.md` where every N line from 54 on is one line lower in O. "O same" means the same text at the same line.

These are drafts for the mission owner to submit one by one when the user says so (`conventions/mission-owner.md`, "Proposing a rule or process change"). Nothing here was written to `session-tracking`. 32 entries cover the 53 rr-1 rows.

---

## Coder startup step d writes to a directory that does not exist

rr-1 rows: 34, 47

Finding
- N:conventions/worktree-delegation.md:58 and N:claude-skills/conv-coder-orchestration/SKILL.md:71: `echo ".session/" >> "$(git rev-parse --git-common-dir)/worktrees/$WTID/info/exclude"`; step e (worktree-delegation.md:63-64, conv-coder-orchestration:74) "Fail closed" stops the coder when step d fails.
- `ls -la /home/dean/code/llm-d/llm-d-scaling-manager/repo/worktrees/policy-writer` shows `COMMIT_EDITMSG HEAD commondir gitdir index logs`, no `info/`; `ls .../repo/worktrees/*/info` fails. Git resolves the exclude file to the common one: `git rev-parse --git-path info/exclude` in N prints `.../repo/info/exclude`.
- O same lines (worktree-delegation.md:58, conv-coder-orchestration:71); `ls /home/dean/code/llm-d/dean-llmd-scaler-sandbox/.git/worktrees/*/info` fails the same way.
- The text also says the exclude is "worktree-local" (worktree-delegation.md:60), which is not what git reads.

Need
- A coder startup step that cannot fail on a normal worktree, and text that states what the exclude actually covers.

Proposed solution
- Replace step d by `echo ".session/" >> "$(git rev-parse --git-path info/exclude)"` (resolves to the repo-wide file, as `conv-feature-worktree-setup` L78-83 already does), with a `grep -qxF` guard to avoid duplicate lines, and drop "worktree-local". Or delete step d: `.session/` is committed on mission branches, and an exclude has no effect on tracked files.

Where it might land
- `conventions/worktree-delegation.md` step d; `conv-coder-orchestration` step d.

---

## `git -C` is both forbidden and used by the rules

rr-1 rows: 6, 42, 69, 75

Finding
- N:CONVENTIONS.md:16 "In a pinned session, `git -C` is blocked — use `git show` instead." and N:claude-skills/conv-working-outside-worktree/SKILL.md:15 "Never `cd` into another worktree or use `git -C <other-path>` for reads".
- Used by N:claude-skills/resume-mission/SKILL.md:131 ("explicit paths or `git -C`"), N:claude-skills/conv-feature-worktree-setup/SKILL.md:48-49, 60, 71, 81 (`git -C MISSION_WT ...`), N:conventions/worktree-delegation.md:109-110, 116 (`git -C ../<name> ...`).
- O same lines.

Need
- One rule that says which roles may use `git -C` and for which commands, so a worker following one file does not break another.

Proposed solution
- State the rule once in CONVENTIONS ("`git -C <path>` is allowed only for read commands on a worktree you were told to read, never for writes outside your worktree"), or forbid it and rewrite the skills to use full paths and `git show`. The user decides which; then align the four files.

Where it might land
- `CONVENTIONS.md` "Work only within your mission worktree"; the three skills and `worktree-delegation.md` get the matching wording.

---

## Reads before the opening orientation: "nothing else" against the actual list

rr-1 rows: 2, 25

Finding
- N:CONVENTIONS.md:9 "Before orientation: read CONVENTIONS.md, session-start.md, and STATE — nothing else."
- N:conventions/session-start.md:5-10 lists five reads before orientation, including `chat-preferences.md` (L9) and role files (L10); N:claude-skills/resume-mission/SKILL.md Steps 1-8 (L63-257) run git and `ls` commands before the orientation block at Step 9 (L270).
- O same lines.

Need
- A statement of exactly what may happen before the orientation block.

Proposed solution
- Change CONVENTIONS L9 to name the allowed reads (the session-start list) and say that `/resume-mission` Steps 1-8 are allowed as the startup procedure.

Where it might land
- `CONVENTIONS.md` line 9; `conventions/session-start.md` L5-12.

---

## Bare `conventions/...` paths in CONVENTIONS.md

rr-1 rows: 3

Finding
- N:CONVENTIONS.md:7, 25-33 write `conventions/session-start.md`, `conventions/mission-owner.md` and so on. A mission worktree has no `conventions/` (`ls -A /home/dean/code/llm-d/llm-d-scaling-manager/incubation-migration` shows only `.git .session`); the files are in `session-tracking/conventions/`. N:conventions/resume-and-handoff.md:93-94 requires workspace-root-relative paths ("never a bare filename").
- O same lines; an O mission worktree such as `worktrees/benchmark-waldorf` has no `conventions/` either.

Need
- Paths in the situational-rules index that a worker can resolve.

Proposed solution
- Write `session-tracking/conventions/...` in CONVENTIONS L7 and L25-33, as L56-59 and L79 already do for other paths.

Where it might land
- `CONVENTIONS.md` L7, L25-33.

---

## Nobody is told who writes the ledger

rr-1 rows: 8

Finding
- N:CONVENTIONS.md:100 "Maintain the session ledger continuously"; same at N:conventions/session-start.md:85, N:conventions/mission-owner.md:6, N:conventions/coder.md:16, N:claude-skills/conv-coder-orchestration/SKILL.md:117; N:claude-skills/resume-mission/SKILL.md:303-307 and N:claude-skills/wind-down/SKILL.md:80-97 register the same ledger with the ledger harvester. No line says whether the session and the harvester both append.
- O same lines. O:.session/STATE.md L172 and L193 already list this as deferred "item (g): remove the 'session appends to the ledger' rules in 7 places" (scope not asked yet).

Need
- One decision on who appends, then the rules in the 7 places aligned.

Proposed solution
- Take up the existing deferred item (g): decide "harvester only" or "session plus harvester", then change the seven lines to match.

Where it might land
- `CONVENTIONS.md` L100 and the other six places named in O STATE L193.

---

## `cd` is forbidden, but launch commands use `cd`

rr-1 rows: 10

Finding
- N:CONVENTIONS.md:14 "Avoid `cd` in shell commands ... `cd` is only permitted when explicitly entering another worktree".
- N:claude-skills/conv-coder-orchestration/SKILL.md:85 and N:claude-skills/conv-background-agents/SKILL.md:36 launch with `nohup bash -c "cd <worktree-path> && ..."`.
- O same lines.

Need
- The launch form should not break the rule it sits under.

Proposed solution
- Add to CONVENTIONS L14: "a `cd` inside the `bash -c` string of a worker launch is allowed". Or pass the directory by a launcher option if one exists.

Where it might land
- `CONVENTIONS.md` L14.

---

## Stale name for the STATE template (four places)

rr-1 rows: 26, 41, 77, 82

Finding
- The template is `conventions/state_template.md`; `N:conventions/state-vs-ledger.md` contains no template (L51-53 "See `conventions/state_template.md`").
- Stale references: N:conventions/session-start.md:65-66, N:claude-skills/conv-feature-worktree-setup/SKILL.md:41, N:claude-skills/resume-mission/SKILL.md:193, N:claude-skills/wind-down/SKILL.md:56.
- O same lines.

Need
- References that lead to the template.

Proposed solution
- Replace the name by `conventions/state_template.md` in the four places.

Where it might land
- Those four files.

---

## A worker's task file has four names

rr-1 rows: 32

Finding
- N:conventions/tasks.md:110 `.session/<slug>.STATE.md`; N:conventions/tasks.md:12-14 "STATE file"; N:conventions/worktree-delegation.md:21 and the skills `.session/task-<id>.md`; N:claude-skills/resume-mission/SKILL.md:54 `.session/task-<id>.md` or `STATE.coder`.
- O same lines.

Need
- One name and one path, so a coder looks in the right place.

Proposed solution
- Use `.session/task-<id>.md` everywhere (the template and the launch recipes use it) and reword `tasks.md` L12-14 and L109-110 and `resume-mission` L54.

Where it might land
- `conventions/tasks.md`, `claude-skills/resume-mission/SKILL.md`.

---

## "Commit after each logical step" against "each task is one commit"

rr-1 rows: 12, 48

Finding
- N:conventions/coder.md:29 "Commit after each logical step or resolved location." and L30 (heartbeat after every commit) against N:claude-skills/conv-coder-orchestration/SKILL.md:116 "Each task lands as its own commit — not batched, not squashed."
- O same lines.

Need
- One commit rule for coders.

Proposed solution
- Decide: one commit per task, or several per task cherry-picked as a set (rule 10, L122, cherry-picks "approved work"). Align coder.md L29-30 and rule 4.

Where it might land
- `conventions/coder.md` L29-30; `conv-coder-orchestration` rule 4.

---

## Who runs the tests: reviewer or nobody

rr-1 rows: 23, 49

Finding
- N:claude-skills/conv-coder-orchestration/SKILL.md:121 (rule 9) "Do not re-run tests — that is the reviewer's job." against N:conventions/reviewer.md:25-26 "Trust the coder's test execution; do not re-run full test suites unless requested." (the coder runs tests: N:conventions/coder.md:31).
- O same lines.

Need
- A statement of who re-runs tests, if anyone, between coder and merge.

Proposed solution
- Reword rule 9 to "do not re-run tests yourself; the coder's run counts, the reviewer re-runs only on request", matching reviewer.md.

Where it might land
- `conv-coder-orchestration` rule 9; `conventions/reviewer.md` L25-26.

---

## PR-prep agent lists "rebase", but PR branches are never rebased

rr-1 rows: 50

Finding
- N:claude-skills/conv-coder-orchestration/SKILL.md:135 "A narrowly scoped PR-prep agent (rebase, lint, DCO, test) ... A rebase is run only as rule 16 says."; N:CONVENTIONS.md:111 "a PR branch is re-cut with `conv-pr-branch`, never rebased"; N:claude-skills/conv-pr-branch/SKILL.md:12 "never by rebasing it". Rule 16 (L128) allows an ordered rebase.
- O same lines (O CONVENTIONS.md:110).

Need
- A PR-prep task list that does not contradict the PR-branch rule.

Proposed solution
- Replace "rebase" in L135 by "re-cut (`conv-pr-branch`)".

Where it might land
- `conv-coder-orchestration` L135.

---

## No procedure to update an open PR when the base moves

rr-1 rows: 54, 61

Finding
- N:claude-skills/conv-pr-branch/SKILL.md:12 re-cut instead of rebase; a re-cut changes the SHAs, so updating an open PR needs a force push. N:claude-skills/conv-push/SKILL.md:30-37 ("Active PR branches") asks for approval but gives no mechanism; N:claude-skills/wind-down/SKILL.md:64 "never force a push"; N:claude-skills/conv-guard-hook/SKILL.md:10 lists force-push as blocked. `grep -rniE "force|lease"` over N finds no procedure.
- O same lines.

Need
- A decided way to update an open PR whose base moved (merge the base into the PR branch, or an approved force push after a re-cut).

Proposed solution
- The user decides; then add the steps to `conv-pr-branch` and point `conv-push` "Active PR branches" at them (including the guard-hook two-pass approval if a force push is chosen).

Where it might land
- `conv-pr-branch`, `conv-push`.

---

## `conv-push` and `reviewer.md` do not scope DCO and checks to PR branches

rr-1 rows: 60

Finding
- N:claude-skills/conv-push/SKILL.md:26 "Run applicable tests, lint, DCO, and project pre-push checks." is a step for every push; only L28 is PR-only. N:conventions/reviewer.md:25 "Verify linting and DCO compliance." likewise.
- Settled: DCO and signatures apply only to PR branches that may be pushed upstream (`/home/dean/code/llm-d/llm-d-scaling-manager/main/CONTRIBUTING.md` L48-56); `policy-writer`, `session-tracking` and `.session/`-only mission branches never need them.
- O same lines.

Need
- A worker on a rules branch must not demand sign-off or signatures.

Proposed solution
- In conv-push L26 and reviewer.md L25 add "for a PR branch" and say other branches need none of these.

Where it might land
- `conv-push` L26; `conventions/reviewer.md` L25.

---

## `conv-pr-branch` names `main` as the base; the PR base is `upstream/main`

rr-1 rows: 51

Finding
- N:claude-skills/conv-pr-branch/SKILL.md:12 "Always branch from `main`"; L28 repeats "Confirm the target base branch". Local `main` is a worktree branch (`git -C /home/dean/code/llm-d/llm-d-scaling-manager/main branch --show-current` prints `main`); `git remote -v` there shows `upstream https://github.com/llm-d-incubation/llm-d-scaling-manager.git` (push `DISABLED-no-push`). `N:conventions/worktree-delegation.md:158` already says `upstream/main`. No `git fetch upstream` step.
- O same lines; the O repo has the same remote setup (`upstream` push `DISABLED-no-push`, local `main`).

Need
- A base that is current, and rules L12 and L28 that do not say the same thing twice.

Proposed solution
- "Run `git fetch <remote>` and branch from `<remote>/<base>` (CONTRIBUTING names the base)"; merge L28 into L12.

Where it might land
- `conv-pr-branch` L12, L28.

---

## Two GitHub MCP servers that Claude Code does not have

rr-1 rows: 52, 59

Finding
- N:claude-skills/conv-pr-branch/SKILL.md:24 and N:claude-skills/conv-pr-workflow/SKILL.md:21 "This repo has two GitHub MCP servers (`gh-public`, `gh-ibm`)". They exist only in `~/.bob/settings/mcp.json` (keys: agentbus, gh-public, gh-ibm); a Claude Code session has no GitHub MCP server.
- O same lines.

Need
- The rule should say which tool opens PRs for each runner.

Proposed solution
- State per runner which tool is used (Bob: the MCP server matching the remote; Claude Code: `gh`, if that is the decision), or drop the sentence.

Where it might land
- `conv-pr-branch` L24; `conv-pr-workflow` L21.

---

## `conv-pr-branch` checks only `.session/`

rr-1 rows: 55

Finding
- N:claude-skills/conv-pr-branch/SKILL.md:16-18 verifies `.session` absent only; a branch cut from upstream could carry `.claude/` or `.bob` changes.
- O same lines.

Need
- A check that the PR branch contains only the intended files.

Proposed solution
- Add `git diff --name-only <base>...HEAD` and review it before pushing.

Where it might land
- `conv-pr-branch` rule 3.

---

## `conv-pr-branch` says "delete the PR branch worktree" without a command

rr-1 rows: 56

Finding
- N:claude-skills/conv-pr-branch/SKILL.md:30 "delete the PR branch worktree locally": no command, no location for creating it; N:CONVENTIONS.md:111-112 require listing and per-step approval for removals.
- O same line.

Need
- An exact, approved form.

Proposed solution
- Name `git worktree add <workspace-root>/<name> -b <branch> <base>` for creation and `git worktree remove <path>` for removal, with the approval reminder.

Where it might land
- `conv-pr-branch` rule 8.

---

## `conv-wip-editing` says `mv`; the Bob mode says `wip.sh`

rr-1 rows: 67, 71, 84

Finding
- N:claude-skills/conv-wip-editing/SKILL.md:66, 73, 106 `mv FILE_PATH FILE_PATH.wip`; N:claude-skills/ledger-capture/SKILL.md:52 "claim with `mv`"; N:bob/custom_modes.yaml:13-14 "claiming them with the wip.sh script (wip.sh claim <file>)". `~/.local/bin/wip.sh` exists.
- O same lines.

Need
- One claim procedure, or a statement that the two are equivalent.

Proposed solution
- Name `wip.sh claim|release` as the procedure where it is available and keep `mv` as the equivalent, in both skills.

Where it might land
- `conv-wip-editing`, `ledger-capture` L52.

---

## Commit steps that name no worktree

rr-1 rows: 18, 68

Finding
- N:claude-skills/conv-wip-editing/SKILL.md:78 and L111 `git add FILE_PATH && git commit -m ...`; N:conventions/policy-writer.md:70 `git add missions/<name>/ && git commit -m "chore: ..."`. Neither names the worktree. The files are in another worktree than the session's (N:claude-skills/conv-wip-editing/SKILL.md:18, "files in another worktree" are not owned), and N:claude-skills/conv-working-outside-worktree/SKILL.md:44 forbids committing another branch from outside its worktree; `cd` and `git -C` are restricted (rows on `git -C`).
- O same lines.

Need
- A way to commit that follows the rules around it.

Proposed solution
- State for each: which worktree the command runs in (the session's own), and for another worktree "the owning session commits" as `conv-working-outside-worktree` L36 already says for copies.

Where it might land
- `conv-wip-editing` steps 6 and 5; `conventions/policy-writer.md` L68-71.

---

## `conv-unexplained-files` Step 3 commands return nothing

rr-1 rows: 66

Finding
- N:claude-skills/conv-unexplained-files/SKILL.md:55 `git log --oneline -10 -- session-tracking/` and L57 `git show session-tracking:.session/STATE.md 2>/dev/null || true`. In N the log prints 0 lines and the show fails with "fatal: path '.session/STATE.md' does not exist in 'session-tracking'", hidden by `|| true`.
- O:claude-skills/conv-unexplained-files/SKILL.md:55 `-- worktrees/session-tracking/`, L57 same; both return nothing in O too (0 lines; "exists on disk, but not in 'session-tracking'").

Need
- A check that can find an owning session.

Proposed solution
- List worktrees with `git worktree list` and read each candidate's `.session/STATE.md` by full path (a read, allowed by `conv-working-outside-worktree`).

Where it might land
- `conv-unexplained-files` Step 3.

---

## `resume-mission` says `EnterWorktree` is only "verified" and also called

rr-1 rows: 74

Finding
- N:claude-skills/resume-mission/SKILL.md:56 "verify worktree isolation (`EnterWorktree`)" against L121 `EnterWorktree(path: "<full path to $MISSION_WT>")` and L127-128 "Coders must be isolated ... Entering any other worktree is a violation"; N:conventions/worktree-delegation.md:82-84 "`EnterWorktree` cannot retarget a subagent".
- O same lines. (O:.session/STATE.md "Known issues" records a 2026-11-16 decision about a different gap, the ban on `EnterWorktree`; it does not resolve this one.)

Need
- Whether a session already inside its worktree calls `EnterWorktree`, and that coders do not.

Proposed solution
- Reword L56 to "a delegated worker does not call `EnterWorktree`; it verifies its worktree with `git rev-parse --show-toplevel`", and say in Step 4 that a session already inside `$MISSION_WT` skips the call.

Where it might land
- `resume-mission` L56 and Step 4.

---

## `resume-mission` Step 2 records a whole `git worktree list` line as a path

rr-1 rows: 79

Finding
- N:claude-skills/resume-mission/SKILL.md:76 `git worktree list | grep session-tracking`, L80 "Record its path as `$TRACKING`" (the line also holds the hash and branch). N:claude-skills/conv-feature-worktree-setup/SKILL.md:71 uses a `--porcelain` plus awk filter.
- O same lines.

Need
- One lookup that returns only the path.

Proposed solution
- Use the same awk filter as `conv-feature-worktree-setup`.

Where it might land
- `resume-mission` Step 2.

---

## `resume-mission` refers to the wrong step number

rr-1 rows: 80

Finding
- N:claude-skills/resume-mission/SKILL.md:205 "the Session log (see Step 6)" (inside Step 6) and L284 "if Step 6 cleared any pending sessions"; pending sessions are cleared at Step 7 (L215).
- O same lines.

Need
- Correct cross-references.

Proposed solution
- Step 6 to Step 7 in L284; L205 refers to the Session-log reading in Step 7.

Where it might land
- `resume-mission` L205, L284.

---

## Rule text copied instead of pointed to (five places)

rr-1 rows: 20, 28, 63, 65, 83

Finding
- N:conventions/resume-and-handoff.md:59-89 repeats the `ledger-capture` contract and differs from N:claude-skills/ledger-capture/SKILL.md:48-51 (no "create no files", no "append only", destinations omit the end of the ledger).
- N:conventions/state-vs-ledger.md:6-49 restates N:claude-skills/conv-state-vs-ledger/SKILL.md:12-29; N:claude-skills/conv-state-vs-ledger/SKILL.md:35-75 holds a copy of the STATE template that differs from N:conventions/state_template.md and L10 points to the template file.
- The design-validation checkpoint is in N:claude-skills/conv-tasks/SKILL.md:40 and N:claude-skills/conv-coder-orchestration/SKILL.md:119 (rr-1 says L120), not in `conventions/tasks.md`.
- N:claude-skills/wind-down/SKILL.md:107-112 repeats N:claude-skills/resume-mission/SKILL.md:225-230 (task file recipe and the `bob run` launch).
- O same lines.

Need
- One home per rule so copies cannot drift.

Proposed solution
- Keep the skill as the source for each item and replace the copy by a pointer: handoff.md to `ledger-capture`; `state-vs-ledger.md` and the skill's template copy to the other file and `state_template.md`; checkpoint kept in one of the two skills; wind-down Step 5 to resume-mission Step 7.

Where it might land
- The five files listed.

---

## "his confirmation" in a shared rule

rr-1 rows: 11

Finding
- N:conventions/chat-preferences.md:23 "🟡 a statement waiting on his confirmation before Claude proceeds". O same file and line.

Need
- Neutral wording in a shared rule.

Proposed solution
- "the user's confirmation".

Where it might land
- `conventions/chat-preferences.md` L23.

---

## Text slips in `policy-writer.md`

rr-1 rows: 15, 17, 19

Finding
- N:conventions/policy-writer.md:5-6 "canonical `.claude/skills/` stored on the `session-tracking` branch": the directory is `claude-skills/` (N:CONVENTIONS.md:59).
- N:conventions/policy-writer.md:79 "(and/or `session-tracking.pending-commits`)" against L40 and N:claude-skills/conv-agentbus/SKILL.md:28 (both channels).
- N:conventions/policy-writer.md:80-84 numbered list "2." followed by "1." to "4." at the same indent.
- O same lines.

Need
- Correct names and one reading of the subscription rule.

Proposed solution
- `claude-skills/`; "and"; nest the four sub-items as a. to d.

Where it might land
- `conventions/policy-writer.md` L5-6, L79, L80-84.

---

## Resume question wording differs between two files

rr-1 rows: 22

Finding
- N:conventions/resume-and-handoff.md:22 "Ask user: "Continuing `<slug>`?"" against the fixed text in N:claude-skills/resume-mission/SKILL.md:45-48. O same lines.

Need
- One wording.

Proposed solution
- Point handoff.md step 1 to the quoted text in `resume-mission` Case 2.

Where it might land
- `conventions/resume-and-handoff.md` L22.

---

## Ledger slug shown with `.md` and then `.md` is appended

rr-1 rows: 27

Finding
- N:conventions/session-start.md:47 "Create a new ledger at `.session/<slug>.md` (slug: `YYYY-MM-DD-<mission>-<N>.md`" gives `.session/YYYY-MM-DD-<mission>-<N>.md.md`. O same line.

Need
- A slug without the extension.

Proposed solution
- slug: `YYYY-MM-DD-<mission>-<N>`.

Where it might land
- `conventions/session-start.md` L47.

---

## Task file `Path:` is absolute while docs must use relative paths

rr-1 rows: 31

Finding
- N:conventions/task_file_template.md:11 "Path: <absolute-path ...>" against N:conventions/resume-and-handoff.md:93-94 "never absolute". The startup check compares `Path` with `git rev-parse --show-toplevel`, so it must be absolute.
- O same lines.

Need
- The exception stated.

Proposed solution
- Add to the Doc-Reference Path Rule: "task-file `Path:` is the only absolute path, it is compared with `git rev-parse --show-toplevel`".

Where it might land
- `conventions/resume-and-handoff.md` L91-96.

---

## Example test name in `tasks.md` matches no test in this project

rr-1 rows: 33

Finding
- N:conventions/tasks.md:81 "Ran 1 of 150 Specs — `TestNilSaturationGuard` — SUCCESS". `grep -rl NilSaturationGuard` over `/home/dean/code/llm-d/llm-d-scaling-manager/main` and the O worktrees (*.go) finds nothing. O same line.

Need
- A neutral example.

Proposed solution
- "Ran 1 of 150 specs — `<TestName>` — SUCCESS".

Where it might land
- `conventions/tasks.md` L81.

---

## Wrong bullet named for the ledger-exempt task

rr-1 rows: 37

Finding
- N:conventions/worktree-delegation.md:203-204 "section "Code reviewer", last bullet"; the last bullet there is N:claude-skills/conv-coder-orchestration/SKILL.md:136 (default launch); the exemption "needs no reviewer, no state file, no ledger" is L135. O same lines.

Need
- A reference that leads to the exemption.

Proposed solution
- Quote the sentence instead of counting bullets.

Where it might land
- `conventions/worktree-delegation.md` L203-204.

---

## `conv-push` log check fails for a new branch

rr-1 rows: 62

Finding
- N:claude-skills/conv-push/SKILL.md:23 "Run `git log --oneline origin/<branch>..HEAD`" fails with "unknown revision" when the branch has no remote ref yet. O same line.

Need
- A check that works for the first push.

Proposed solution
- Add the new-branch form, for example `git log --oneline <base>..HEAD` with the PR base.

Where it might land
- `conv-push` L23.

---

# MIGRATION rows (for the mission owner, not suggestions)

These exist only in the new workspace.

- Row 9 (`CONVENTIONS.md:110`): N:CONVENTIONS.md:110 names `conventions/archived/`, which does not exist in N (`ls N/conventions/archived` fails); O has it with 11 tracked files. The old policy note (`O/.session/incubation-migration-policy-note.md` point 2) said to leave it behind, so this is an intended omission; the sentence now refers to a folder that is not there.
- Row 73 (`resume-mission` L22, L69, L154): "the main repository's copy" and "links into the main repository". In O this was the root checkout; in N there is no main checkout (`repo/` is bare, `main/` is a worktree of upstream code with no `CONVENTIONS.md`), so the phrase is undefined.

Observations from the checks (not rr-1 rows), state at 19:08-19:09 on 2026-11-25:

- `session-tracking` has `missions/incubation-migration/` (two symlinks, `STATE.md` and `ledgers`, created 19:08) and an empty `suggestion-box/` (created 19:08). `git -C /home/dean/code/llm-d/llm-d-scaling-manager/session-tracking status --short` shows `?? missions/`. No other mission is indexed: `policy-writer` and `main` have no `missions/<name>/` entry, so `resume-mission` Step 3 (`ls "$TRACKING/missions/"`) lists only one mission. O has 14 entries.
- The new `incubation-migration` worktree has no `.claude/` and no `.bob/` (`ls -A` shows only `.git .session`): the skill links of `conv-feature-worktree-setup` Steps 3 and 4a were not created there.
