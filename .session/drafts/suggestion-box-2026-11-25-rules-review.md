# Suggestion: a review of the shared rules, to triage in the policy-writer mission (35 items)

Written by the incubation-migration mission (2026-11-25). The reader has no context from the session that found these, so this
entry is self-contained. Paths are relative to the workspace root `/home/dean/code/llm-d/llm-d-scaling-manager/`; rule files are
quoted as in `session-tracking` at commit `12308619` (identical to `policy-writer` at `b87fc250`).

## Finding

While moving the workspace to the new repo, the rules (`CONVENTIONS.md`, `conventions/`, `claude-skills/`, `bob/`) were reviewed line by
line. A first reviewer reported 84 findings; a second pass re-checked every one against the actual line (66 confirmed, 7 false, 11
stale). The 53 confirmed rule-quality findings group into the 32 items below, plus 3 items that came up in the same work. Every item was
checked against the previous workspace's latest rules (`d23d9d7e3`): the same lines and problems are there, so they are NOT caused by the
migration. A third pass compared them with the old policy-writer mission's own material (processed suggestions, spec, ledgers): none was
found already decided or adopted; one is queued (#5), eight are partly handled, 23 have no trace.

## Need

Triage the items and fix the ones worth fixing, under this constraint from the user: **the rules already weigh too much on every context.**
So: prefer refining or shortening existing text, or a cheap on-demand rule; add no always-loaded text; drop an item if the fix costs more
than the problem it removes; merge items that share a root cause (for example #7, #19, #24 and #26 are all "text that points at the wrong
place").

## Evidence, in the incubation-migration worktree (read only if an item is unclear)

- `incubation-migration/.session/review-rules-verified-2026-11-25.md`: all 84 findings, one verdict each, with line evidence in both trees.
- `incubation-migration/.session/drafts/suggestions-from-rr3-2026-11-25.md`: the long-form draft of items 1-32 (Finding, Need, Proposed solution).
- `incubation-migration/.session/review-suggestions-mapping-2026-11-25.md`: what the old policy-writer mission already decided, per item.

## Items

Each line: where (file:line) | what is wrong | a direction. "Old" is the status in the old policy-writer mission's material.

**Contradictions between rules**
1. `conventions/worktree-delegation.md:58` and `claude-skills/conv-coder-orchestration/SKILL.md:71` | coder startup step d appends to `<git-common-dir>/worktrees/$WTID/info/exclude`; that `info/` directory does not exist (git uses the shared `info/exclude`), so the "fail closed" step e stops every coder | use the shared exclude, or drop the step. Old: nothing.
2. `CONVENTIONS.md:16` and `claude-skills/conv-working-outside-worktree/SKILL.md:15` forbid `git -C` for reads; `claude-skills/resume-mission/SKILL.md:131`, `claude-skills/conv-feature-worktree-setup/SKILL.md:48-49,60,71,81`, `conventions/worktree-delegation.md:109-116` use it | one rule saying who may use `git -C` and for what. Old: individual statements fixed twice, no single rule.
3. `CONVENTIONS.md:9` "read CONVENTIONS.md, session-start.md, and STATE — nothing else" against `conventions/session-start.md:5-10` (five reads incl. `chat-preferences.md`) and `resume-mission` Steps 1-8 (git and `ls` before the orientation) | state the real list once. Old: the strict gate was deliberate (2026-09-05, 09-17); the mismatch was not examined.
6. `CONVENTIONS.md:14` "avoid `cd`" against `conv-coder-orchestration/SKILL.md:85` and `conv-background-agents/SKILL.md:36` launching with `bash -c "cd <worktree> && ..."` | say the launch string is the exception. Old: nothing.
9. `conventions/coder.md:29-30` "commit after each logical step" (+ heartbeat per commit) against `conv-coder-orchestration/SKILL.md:116` "each task lands as its own commit" | pick one granularity. Old: one-commit-per-task audited and kept; the clash not raised.
10. `conv-coder-orchestration/SKILL.md:121` rule 9 "do not re-run tests, that is the reviewer's job" against `conventions/reviewer.md:25-26` "trust the coder's test execution; do not re-run" (the coder runs them, `coder.md:31`) | say plainly who runs tests. Old: rule 9 left standing, not compared with reviewer.md.
21. `resume-mission/SKILL.md:56` says `EnterWorktree` is only "verified"; L121 calls it; `worktree-delegation.md:82-84` says it cannot retarget a subagent | reword once. Old: behaviors verified, text not reworded.
27. `conventions/resume-and-handoff.md:22` vs the fixed text at `resume-mission/SKILL.md:45-48` (two wordings of the resume question) | point one at the other.
8. `conventions/tasks.md:110`, `tasks.md:12-14`, `worktree-delegation.md:21`, `resume-mission/SKILL.md:54` | a worker's task file has four names (`.session/<slug>.STATE.md`, "STATE file", `.session/task-<id>.md`, `STATE.coder`) | one name. Old: history in a 2026-09-03 ledger, never unified.
29. `conventions/task_file_template.md:11` `Path:` is absolute against `resume-and-handoff.md:93-94` "never absolute" | one sentence: the task-file `Path:` is the only absolute path (it is compared with `git rev-parse --show-toplevel`). Old: deliberate, exception never worded.

**Commands that fail or do nothing**
12. `claude-skills/conv-pr-branch/SKILL.md:12` (re-cut, never rebase), `conv-push/SKILL.md:30-37`, `wind-down/SKILL.md:64` | no procedure to update an open PR after a re-cut (the SHAs change, so it needs a force push, which another rule forbids without approval) | write the approved sequence once. Old: nothing.
14. `conv-pr-branch/SKILL.md:12,28` "branch from `main`" | local `main` is a worktree branch; the PR base is `upstream/main`, and there is no `git fetch` step | name the base and add the fetch. Old: the principle accepted in 2026-09, the word `main` never examined.
15. `conv-pr-branch/SKILL.md:24`, `conv-pr-workflow/SKILL.md:21` "two GitHub MCP servers (`gh-public`, `gh-ibm`)" | they exist only in `~/.bob/settings/mcp.json`; Claude Code has none | say which tool opens PRs per runner (`gh`). Old: nothing.
16. `conv-pr-branch/SKILL.md:16-18` checks only that `.session/` is absent | a branch cut from upstream can carry `.claude/` or `.bob` changes | extend the check. Old: nothing.
17. `conv-pr-branch/SKILL.md:30` "delete the PR branch worktree locally" | no command, and `CONVENTIONS.md:111-112` need listing and approval for removals | give the command form. Old: nothing.
19. `claude-skills/conv-wip-editing/SKILL.md:78,111` and `conventions/policy-writer.md:70` `git add ... && git commit` | the commit steps do not say in which worktree | name it. Old: nothing.
20. `claude-skills/conv-unexplained-files/SKILL.md:55,57` `git log -- session-tracking/` and `git show session-tracking:.session/STATE.md 2>/dev/null || true` | both return nothing (the second error is hidden) | replace with working commands. Old: found 2026-11-24 in `.session/migration-compat-2026-11-24.md:37` of the policy-writer mission, rule not changed.
22. `resume-mission/SKILL.md:76-80` | `git worktree list | grep session-tracking` then "record its path" records a whole line (hash and branch included); `conv-feature-worktree-setup/SKILL.md:71` uses a `--porcelain` + awk form | use one form. Old: not compared.
32. `conv-push/SKILL.md:23` "`git log --oneline origin/<branch>..HEAD`" | fails with "unknown revision" for a branch with no remote ref yet | add the new-branch form. Old: nothing.
13. `conv-push/SKILL.md:26` and `conventions/reviewer.md:25` "lint, DCO ..." | stated for every push; DCO sign-off and verified signatures are needed only for PR branches that may go upstream (not for `policy-writer`, `session-tracking` or `.session/`-only mission branches) | say "PR branches" and point to the project's CONTRIBUTING.md. Old: DCO scoping never discussed.

**Names and wording that point at the wrong place**
4. `CONVENTIONS.md:7,25-33`, `conventions/resume-and-handoff.md` | bare `conventions/...` paths; a mission worktree has no `conventions/`, the files are in `session-tracking/conventions/` | prefix them. Old: nothing.
7. `conventions/session-start.md:65-66`, `conv-feature-worktree-setup/SKILL.md:41`, `resume-mission/SKILL.md:193`, `wind-down/SKILL.md:56` | still name `conventions/state-vs-ledger.md` as the STATE template; it is `conventions/state_template.md` | fix the four names. Old: the move was done, these references were missed.
23. `resume-mission/SKILL.md:205,284` | "see Step 6" and "if Step 6 cleared pending sessions"; that happens in Step 7 | fix the numbers.
25. `conventions/chat-preferences.md:23` "waiting on his confirmation" | a shared rule that names a gender | "the user's".
26. `conventions/policy-writer.md:5-6` | says `.claude/skills/`; the directory is `claude-skills/` (`CONVENTIONS.md:59`) | fix. Already fixed in `b87fc250`.
28. `conventions/session-start.md:47` | slug `YYYY-MM-DD-<mission>-<N>.md` plus the `.md` the sentence appends gives `.md.md` | slug without `.md`.
30. `conventions/tasks.md:81` | the example test name (`TestNilSaturationGuard`) matches no test in this project | a placeholder.
31. `conventions/worktree-delegation.md:203-204` | names "section Code reviewer, last bullet" for the ledger-exempt PR-prep task; the sentence is the second to last (`conv-coder-orchestration/SKILL.md:135`) | quote the sentence.
5. `CONVENTIONS.md:100`, `session-start.md:85`, `mission-owner.md:6`, `coder.md:16`, `conv-coder-orchestration/SKILL.md:117`, plus `resume-mission` and `wind-down` registering the harvester | "maintain the ledger" is said in seven places and nobody is told who writes it (the session or the harvester) | decide once and delete the rest. Old: already queued as item (g) in `STATE.md` of the policy-writer mission, scope never given.
24. `conventions/resume-and-handoff.md:59-89` vs `claude-skills/ledger-capture/SKILL.md:48-51`; `conventions/state-vs-ledger.md:6-49` vs `conv-state-vs-ledger/SKILL.md:12-29`; the STATE template copy inside `conv-state-vs-ledger/SKILL.md:35-75`; the design-validation checkpoint in `conv-tasks` and `conv-coder-orchestration` | rule text copied in five places and drifting | keep one copy, point to it (this also shrinks the context). Old: two of the five parts are open items already.
18. `claude-skills/conv-wip-editing/SKILL.md:66,73,106` and `ledger-capture/SKILL.md:52` say `mv`; `bob/custom_modes.yaml:13-14` says `wip.sh claim` | `~/.local/bin/wip.sh` is a wrapper around `mv` | one word for the claim. Old: the spec records that `wip.sh` wraps `mv`; skills not aligned.

**Do not do as drafted**
11. `conv-coder-orchestration/SKILL.md:135` lists "rebase" for a PR-prep agent while `CONVENTIONS.md:111` says PR branches are re-cut, never rebased | the draft proposed replacing "rebase" with "re-cut". The user decided on 2026-11-16 that a coder (and a PR-prep agent) may be ordered to rebase with an approved command (commit `17cfb58c4`, 2026-11-18). If anything, make the PR-skill text say how the two fit; do not remove the rebase. Old: decided as above.

**Three more items from the same work**
33. `claude-skills/conv-feature-worktree-setup/SKILL.md` Step 4a | Bob is linked per skill (`.bob/skills/ledger-capture` only); Claude is linked per folder | link `.bob/skills` to `session-tracking/claude-skills` like `.claude/skills`. Old: nothing.
34. the same skill | a new mission worktree is not added to the user's `<workspace-root>/*.code-workspace` file (untracked, not versioned) | add the worktree as a folder when it is set up. Old: n/a (new workspace file).
35. `claude-skills/conv-pr-branch/SKILL.md`, the reviewer/tester task rules | the project's `CONTRIBUTING.md` must not be loaded into every context | read it only when a PR branch is started or when reviewer or tester tasks are created. Old: n/a.

## Already done by the migration (do not redo)

- `claude-skills/conv-feature-worktree-setup/SKILL.md` Step 3 no longer treats a tracked upstream skill (`pr-review`) as a blocker; `claude-skills/conv-install-to-session-tracking/SKILL.md` and `CONVENTIONS.md:63` no longer name `pr-review` (`b87fc250`). `resume-mission` no longer says "the main repository" (`4c88ee8a`). Item 26 above was fixed in `b87fc250` too.

## Where it might land

Item by item in the files named above; the shortening items (#5, #24) first, because they lower the context cost.
