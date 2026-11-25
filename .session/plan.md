# incubation-migration — plan (approved in chat 2026-11-10; nothing executed yet)

Target repo: https://github.com/llm-d-incubation/llm-d-scaling-manager

## Decisions

- **Container root:** `/home/dean/code/llm-d/llm-d-scaling-manager/`, NOT a git repo.
- **Layout:** `repo/` = bare clone; every worktree is a direct child of the root
  (`main` lowercase, `session-tracking`, `policy-writer`, `incubation-migration`, ...);
  `llm-d-scaling-manager.code-workspace` at the root, `session-tracking` as its first folder
  (default home of sessions started at the root; they `cd` to the right worktree).
- **Root `CLAUDE.md`:** common anchor only. It points to the rule files in session-tracking.
  Rules stay in micro-rule files and skills (deliberate design); do not inline them.
- **Skills:** per-worktree `.claude/skills` dir-symlink, as today for new missions.
- **Remotes (bare repo):** `upstream` = llm-d-incubation repo (fetch ok, push URL
  `DISABLED-no-push`; verified: a push dry-run fails); `origin` = Dean's new fork (default
  fetch, pushable). Fetch refspec `+refs/heads/*:refs/remotes/origin/*`. Whether to add an
  `ofer`-style remote: open.
- **Carry-over:**
  - Old repo stays as reference; refs to it may remain.
  - Old code/mission worktrees are NOT copied. New clean worktrees off the new upstream.
    Work is re-derived by hand (manual rebase of ideas/plans); old plans are rewritten.
  - session-tracking and policy-writer are orphan branches and stay out of upstream.
    No history import; copy relevant files and update them. Older history via old repo origin.
  - Order: new policy-writer FIRST (it owns rules and skills). session-tracking is mostly an
    install by policy-writer; the install skill/conventions need updating too.
  - Older missions in session-tracking: link to the old worktree.
  - All path references (`worktrees/<name>/...`) are rewritten for the flat layout.
- **Memory:** copy the notes, but first find out whether memory can be shared across
  worktrees (root-started session, or a different folder structure) so we need not copy per
  worktree. If not shareable, move some notes to global memory.

## Open items

Resolved 2026-11-25 (tests, details in the old workspace ledger):
- Memory: auto memory is per git repo, shared by all its worktrees (main and policy-writer share
  `~/.claude/projects/-home-dean-code-llm-d-llm-d-scaling-manager-repo/memory/`); a session started in the
  non-git container root gets its own. User decision: repo-agnostic notes go to ONE global directory via
  `autoMemoryDirectory` (honored; tested). See STATE step 8.
- A root `CLAUDE.md` in the non-git container loads in every worktree and at the root (tested).
- Upstream `main` tracks `CLAUDE.md` ("see @AGENTS.md") and `AGENTS.md` (a Go style guide); they load together
  with the root file, which must not conflict.
- Fork exists: `deanlorenz/llm-d-scaling-manager`.
Still open:
- Does lowercase `main` cause trouble for Claude or VS Code? (no problem seen so far)
- `ofer`-style extra remote? (not added)
- Multi-root VS Code cwd choice, `/cd` and `/add-dir` in the extension: untested.

## Step-4 decisions (approved 2026-11-10)

- Port: CONVENTIONS.md, active conventions/ (13), claude-skills (16), `.bob/` (see open).
- Leave in old repo: backup_rules/, conventions/archived/, PLAN-conventions-split.md.
- Fresh `.session/`; old ledgers/spec stay in old repo (ledgers linked, not copied).
- Two commits: plain copy, then path rewrite (`worktrees/<name>` -> flat `<name>`; ~137 refs
  in ~24 files; reviewed diff). Install and worktree-setup skills reworked in a later step.
- Branch `policy-writer`, orphan, created via `git worktree add --orphan` from `repo/`;
  pushed to origin only with separate per-push approval.
- Open: where is `wip.sh`? Port `.bob/` as-is vs generic global Bob mode (idea only).
- Bob facts: project modes in `.bob/custom_modes.yaml`; global modes in
  `~/.bob/settings/custom_modes.yaml` (currently `customModes: []`; old
  `~/.bob/custom_modes.yaml.bak` has an outdated coder mode). IDE and Shell docs disagree on
  slug-collision precedence, so use unique slugs. Old `.bob/` = one mode `ledger-capture`
  (edit restricted to `*.wip` via fileRegex, references `wip.sh`) plus the skills symlink;
  both untracked in the old policy-writer.

## Steps (in order; each needs go-ahead before execution)

- [x] 1. Create the fork (origin).
- [x] 2. Create the container root; bare clone into `repo/`; configure remotes and refspec.
- [x] 3. Add worktree `main`.
- [x] 4. Create new `policy-writer` (orphan); port rules/skills, update paths. (copy + path rewrite done; the
  rules still need the fixes from `review-rules-2026-11-25.md`, tracked as 4a in STATE)
- [ ] 5. Create `session-tracking` via the updated install; port needed files. (worktree exists, empty on purpose)
- [x] 6. Create `incubation-migration` worktree; port `.session/`.
- [ ] 7. Root `CLAUDE.md`; `.code-workspace`; skills links (after the install).
- [ ] 8. Memory approach decided and applied. (decided: global; not yet applied)
- [ ] 9. Link older missions to the old worktree.
Current status lives in STATE.md; this list is the plan as approved.
