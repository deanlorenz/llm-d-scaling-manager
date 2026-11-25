# rr-4: upstream skills (pr-review) in the rules, checked against the policy (2026-11-25)

Read-only. Trees checked: `/home/dean/code/llm-d/llm-d-scaling-manager/policy-writer` (PW) and `.../session-tracking` (ST). `diff -rq PW/claude-skills ST/claude-skills` printed nothing and `diff -q PW/CONVENTIONS.md ST/CONVENTIONS.md` printed nothing, so both trees are identical for these files; every line number below holds for both. Rows are written once, with ST paths.

Facts checked first (commands run):
- `ls PW/claude-skills` and `ls ST/claude-skills`: 20 entries, none named `pr-review` (conv-*, ledger-capture, resume-mission, wind-down).
- `ls -la main/.claude/skills`: only `pr-review/`. `git -C main ls-files -v .claude/skills` shows `H .claude/skills/pr-review/SKILL.md` (tracked). `main/.claude/agents/` holds go-reuse-checker, go-reviewer, security-auditor, test-analyzer (tracked).
- `~/.claude/README.md` has no match for the grep pattern (the grep hits on `skill|agent` are lines 12 and 68, unrelated to upstream skills).

## Part 1. Every mention

Root = `/home/dean/code/llm-d/llm-d-scaling-manager/session-tracking`. Verdicts: C = CONSISTENT, X = CONTRADICTS, D = DANGLING, U = UNCLEAR.

| file:line | quote | what it instructs | verdict |
|---|---|---|---|
| CONVENTIONS.md:59 | `claude-skills/ ← canonical skill source; every worktree's .claude/skills symlinks here` | one dir-link per worktree | C (matches "default = disabled by not linking") |
| CONVENTIONS.md:63 | `pr-review/SKILL.md` (inside the claude-skills/ layout block) | says session-tracking's claude-skills contains pr-review | X and D: `ls` shows no `pr-review` in claude-skills; under the policy it is absent by default and present only if the user opts in. Layout shows it as always present. |
| CONVENTIONS.md:74 | `.claude/skills -> <abs-path>/session-tracking/claude-skills ← dir-symlink` | each worktree's `.claude/skills` is the dir-link | C |
| CONVENTIONS.md:85 | `If .claude/skills is missing or broken in your worktree: skills live at session-tracking/claude-skills/ ... Invoke conv-feature-worktree-setup to repair it.` | repair path | C |
| conventions/policy-writer.md:6 | `canonical .claude/skills/ stored on the session-tracking branch` | names the canonical skill location as `.claude/skills/` on the branch; the real location is `claude-skills/` (CONVENTIONS.md:59) | U (wording only; `.claude/skills/` does not exist on session-tracking as a path). Minor DANGLING-style naming slip. |
| conv-install-to-session-tracking/SKILL.md:16 | `Ignore claude-skills/pr-review in every check below. It is an upstream skill, left untracked on session-tracking. Do not stage, move, or delete it.` | tells the installer to ignore a path that does not exist and to treat pr-review as living in session-tracking's claude-skills | X (policy: pr-review is not in session-tracking unless opted in, and then it is a link, and it is never "ignored" by exclusion rules) and D (path absent now). The "do not stage, move, or delete" part is consistent with the policy. |
| conv-install-to-session-tracking/SKILL.md:64 | `no uncommitted or untracked changes, apart from claude-skills/pr-review` | exempts pr-review from the clean check | X / D (same reason as :16) |
| conv-install-to-session-tracking/SKILL.md:67 | `git status --short -- $PATHS ':!claude-skills/pr-review'` | pathspec excludes pr-review | X / D (excludes a path that is not there; an opted-in link would also be silently skipped) |
| conv-install-to-session-tracking/SKILL.md:83 | `git diff $LAST_SHA HEAD --stat -- $PATHS ':!claude-skills/pr-review'` | same exclusion | X / D |
| conv-install-to-session-tracking/SKILL.md:171 | `diff -r -x pr-review $PW/claude-skills claude-skills` | verify step skips pr-review | X / D (the old tree had a pr-review link, the new ones do not) |
| conv-feature-worktree-setup/SKILL.md:54-56 | `### 3. Set up .claude/skills dir-symlink` / "Skill discovery does not walk above the worktree root" | link the whole folder | C |
| conv-feature-worktree-setup/SKILL.md:58 | `if MISSION_WT/.claude/skills already exists and is a directory symlink resolving to session-tracking/claude-skills, step 3 is already done` | idempotent check | C |
| conv-feature-worktree-setup/SKILL.md:60 | `If pr-review is a tracked git file in this worktree (run git -C MISSION_WT ls-files .claude/skills/pr-review ...), do not replace the .claude/skills directory — skip to step 4 and report this as a blocker.` | refuses to link the folder whenever the worktree has the tracked upstream skill, which is exactly the normal case for a worktree cut from `main` | X (core contradiction: policy says the folder is replaced by one link and upstream skills then simply do not exist) |
| conv-feature-worktree-setup/SKILL.md:62-65 | `Otherwise, clear the old .claude/skills ... Every entry must be a symlink ... If it prints anything, stop and report it.` | for a real dir with a tracked `pr-review/` (a real directory, not a symlink) the `find ... ! -type l` check prints it and the skill says stop | X (same effect as :60; it also blocks the normal case. No step says what to do with tracked upstream content.) |
| conv-feature-worktree-setup/SKILL.md:75, 82 | `ln -s "$SKILLS_ABS" MISSION_WT/.claude/skills`; `grep -qxF ".claude/skills" "$EXCLUDE" \|\| echo ".claude/skills" >> "$EXCLUDE"` | creates the link and adds `.claude/skills` to the repo-shared exclude | U: exclude does nothing for paths already tracked in the index (the old worktrees show tracked pr-review, see part 3). Not a contradiction in text. Also relates to the rule that a session never ignores the removal of an upstream skill: an exclude entry for the link path is not the same as ignoring the removal, but the text does not say how the tracked entries are to be handled. |
| conv-feature-worktree-setup/SKILL.md:88 | `for skill in MISSION_WT/.claude/skills/*/; do ... test -r "$skill/SKILL.md"` | verify every entry resolves | C (only passes where the folder is the link) |
| conv-feature-worktree-setup/SKILL.md:112 | `If a link path already exists and is not the expected link, stop and report it. Do not replace it. Exclude .bob ... as for .claude/skills` | .bob links | C (not about upstream skills) |
| conv-feature-worktree-setup/SKILL.md:167 | `.claude/skills dir-symlink: created / already existed / blocked (pr-review tracked)` | report option that names pr-review as a blocker | X (same as :60) |
| resume-mission/SKILL.md:147-148 | `test -r ".claude/skills/$skill/SKILL.md" \|\| { echo "BROKEN: $skill"; exit 1; }` | checks resume-mission and wind-down resolve | C (loop is only over those two skills, not pr-review) |
| wind-down/SKILL.md:84 | `never call the helper through a relative .claude/skills/... path` | use absolute path | C (not about upstream skills) |
| bob/custom_modes.yaml | no match for any pattern | n/a | C (nothing to check) |
| ~/.claude/settings.json:85-88 | `"skillOverrides": { "claude-api": "name-only", "pr-review": "off" }` | global switch turning pr-review off | C (matches policy item on the global switch). Note: a global `off` also covers an opted-in link, so opting in requires removing this entry; no rule says so (see part 2). |
| ~/.claude/profiles/main.json:85-88 and alt.json:85-88 | same `skillOverrides` block with `"pr-review": "off"` | same | C |
| ~/.claude/settings.json:226, profiles/main.json:216, profiles/alt.json:216 | `PR review via the project subagents in .claude/agents (go-reviewer, security-auditor, test-analyzer, go-reuse-checker)` | tells the model to review PRs via the project agents | U: the four agents exist in `main/.claude/agents/` (checked with `ls`), but the policy says the user wants to control how reviews are done differently from upstream's `pr-review`. This text points at upstream agents as the user's review method. It is not wrong against the policy text (the policy only names skills), but it should be confirmed by the user whether those agents are wanted. Also in worktrees, `.claude/agents` is whatever the checkout has; no rule links or disables it. |
| ~/.claude/README.md | no match | n/a | C |

Summary of part 1: the same pr-review handling appears in three rule files. Nothing else mentions upstream skills or `.claude/agents` in the rules.

## Part 2. Is the opt-in described anywhere?

No. Searched `CONVENTIONS.md`, `conventions/`, `claude-skills/`, `bob/` in ST with `grep -rniE 'opt-in|opt in|which (upstream )?skills|choose which|link .*upstream|upstream'`. The only hits are `upstream/main` as a git base ref (resume-mission/SKILL.md:245, state_template.md:18, conv-state-vs-ledger/SKILL.md:43, worktree-delegation.md:158, tasks.md:55, conv-push/SKILL.md:28, conv-pr-branch/SKILL.md:22, conv-pr-workflow/SKILL.md:14) and the install-skill line `conv-install-to-session-tracking/SKILL.md:16` (which talks about an untracked copy, not a link). No rule says to link `session-tracking/claude-skills/<name>` to `main/.claude/skills/<name>`, and `conv-feature-worktree-setup` has no step where the user picks which upstream skills to keep. Nothing is invented here: the procedure is missing. Related gap: the global `skillOverrides {"pr-review": "off"}` would also hide an opted-in link; no rule mentions it.

Precedent in the old workspace (not in any rule): `ls -la /home/dean/code/llm-d/dean-llmd-scaler-sandbox/worktrees/session-tracking/claude-skills/pr-review` shows a symlink to `/home/dean/code/llm-d/dean-llmd-scaler-sandbox/worktrees/Main/.claude/skills/pr-review`. So the old session-tracking opted in by link, and that is what the install-skill line 16 text calls "left untracked". The new session-tracking has no such link.

## Part 3. Mechanics in the old workspace

Base: `/home/dean/code/llm-d/dean-llmd-scaler-sandbox/worktrees`. Commands: `ls -ld <wt>/.claude/skills`, then inside each worktree `git status --short .claude/skills/pr-review`, `git ls-files .claude/skills`, `git ls-files -v .claude/skills`.

| worktree | `.claude/skills` | `git status --short .claude/skills/pr-review` | `git ls-files .claude/skills` | `ls-files -v` flag |
|---|---|---|---|---|
| single-analyzer | symlink -> `.../worktrees/session-tracking/claude-skills` | empty | `.claude/skills/pr-review/SKILL.md` | `h` (assume-unchanged) |
| composite-analyzer | symlink -> same target | empty | `.claude/skills/pr-review/SKILL.md` | not read (`ls-files` only) |
| benchmark-waldorf | symlink -> same target | empty | `.claude/skills/pr-review/SKILL.md` | `S` (skip-worktree) |

Also: `git check-ignore -v .claude/skills/pr-review/SKILL.md` fails with "beyond a symbolic link" in both, and `git status --short` in single-analyzer lists only unrelated untracked `.session` files. So in these worktrees the index still records `pr-review/SKILL.md` as tracked, the folder was replaced by a link, and git is kept quiet by a per-entry flag (`h` or `S`), not by any exclude. No rule in the new tree mentions `skip-worktree`, `assume-unchanged` or how those flags get set (`grep` over ST found only unrelated `update-index` in conventions/worktree-delegation.md:187-191). The setup skill's text (:60) would have refused all three worktrees as "blocked", so the flags and link were evidently set by hand or by a different, older version of the skill.

What a session in a NEW worktree cut from `/home/dean/code/llm-d/llm-d-scaling-manager/main` will see (INFERENCE from the above; nothing was created):
- `git -C main ls-files -v .claude/skills` shows `H .claude/skills/pr-review/SKILL.md` (tracked) and `.claude/agents/*.md` are tracked, so a fresh checkout contains a real `.claude/skills/pr-review/` directory.
- Running `conv-feature-worktree-setup` step 3 as written: line 60's `ls-files` check is true, so the skill skips linking and reports "blocked (pr-review tracked)" (:167). Even without that check, :65's `find ... ! -type l` prints `pr-review` and the skill stops. So the skill cannot reach the state the policy wants for any worktree cut from `main`.
- If the folder were replaced by the link anyway (as in the old workspace), the session would see only the 20 `session-tracking/claude-skills` skills; `pr-review` would be absent (not in ST's claude-skills, and the global `skillOverrides` is off anyway). The index would still list `pr-review/SKILL.md` as tracked; unless the entry is flagged (`h`/`S`), `git status` in that worktree would show ` D .claude/skills/pr-review/SKILL.md`, or git would refuse the path as beyond a symbolic link. That is the "removal shown as a change" the policy says must never be committed, staged, ignored or deleted by a session. Whether to flag the entry is not covered by any rule; this is the open mechanics question.
- Counter-check in the current worktree: `incubation-migration/.claude/skills` is a symlink to `.../session-tracking/claude-skills` and `git -C incubation-migration ls-files -v .claude` prints nothing (this branch has no tracked `.claude`), so it does not reproduce the case.

## Fixes needed

One line per CONTRADICTS or DANGLING item (apply identically in PW and ST). Words only; no file was changed.

1. CONVENTIONS.md:63: remove the `pr-review/SKILL.md` line from the claude-skills layout block; optionally add one line saying upstream skills appear there only as opt-in links to `main/.claude/skills/<name>`.
2. conv-feature-worktree-setup/SKILL.md:60: delete the "if `pr-review` is tracked ... report this as a blocker" paragraph; say instead that upstream skills tracked in the worktree are expected, the folder is still replaced by the single link, and the setup never stages, commits, ignores or deletes the tracked upstream entries (and does not ask the user about them).
3. conv-feature-worktree-setup/SKILL.md:62-65: adjust the real-directory branch so a tracked upstream skill directory (a real directory with tracked files, not a link) is handled per the policy (how it is moved aside without `rm -rf` and without a git write is not stated by any rule and needs the user's decision), rather than "stop and report".
4. conv-feature-worktree-setup/SKILL.md:167: drop "blocked (pr-review tracked)" from the report options; report which upstream skills (if any) were opted in.
5. conv-install-to-session-tracking/SKILL.md:16: remove "Ignore claude-skills/pr-review ... left untracked on session-tracking"; keep only a rule that upstream links in `claude-skills/` are not edited or deleted (if links are present, decide whether the install should skip them).
6. conv-install-to-session-tracking/SKILL.md:64, 67, 83, 171: remove the `claude-skills/pr-review` exemptions (`apart from ...`, `':!claude-skills/pr-review'` twice, `-x pr-review`), since the path is absent; if an opted-in link is later added, replace with a general rule for links.
7. conventions/policy-writer.md:6: change "canonical `.claude/skills/` stored on the `session-tracking` branch" to `claude-skills/` (naming slip, minor).
8. Opt-in procedure: MISSING. No rule describes linking `session-tracking/claude-skills/<name>` to `main/.claude/skills/<name>`, choosing upstream skills during repo or worktree setup, or removing the matching `skillOverrides` entry when a skill is opted in. A new rule or setup step is needed.
9. Open (UNCLEAR, for the user): `~/.claude/settings.json:226` and both profiles' line 216 recommend the upstream `.claude/agents` for PR review; confirm that matches the "control reviews myself" policy.
