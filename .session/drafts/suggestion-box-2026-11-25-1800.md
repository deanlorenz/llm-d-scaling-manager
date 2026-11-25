# Suggestion: say where rules are read before the first install (bootstrap), and make the conventions self-consistent

## Finding

The conventions send every session to `session-tracking/` (CONVENTIONS.md L7, L25-30, L56-57, L85-88;
`resume-mission` Steps 2, 3, 5c; `conv-feature-worktree-setup` Steps 3, 4a, 5; `ledger-capture` "Read first";
`policy-writer.md` L17; `mission-owner.md`). In the new workspace `session-tracking` exists but is empty on purpose
until the first install, so a literal reading fails at the first read. The conventions do not say what a session does
before the first install (may it read `policy-writer/` directly, which skills it may use, whether `missions/` links
and the suggestion box exist yet).

Evidence: `.session/review-rules-2026-11-25.md` (incubation-migration worktree, 2026-11-25), blockers 3-5 and
decisions D1, D3, D5. The same review lists contradictions the bootstrap question touches:
`git -C` forbidden (CONVENTIONS L16, `conv-working-outside-worktree` L15) but used in `resume-mission` L131,
`conv-feature-worktree-setup`, `worktree-delegation.md`; `EnterWorktree` "verified" vs "called"; the task-file name.

## Need

One paragraph in CONVENTIONS.md (and the matching lines in `resume-mission` and `conv-feature-worktree-setup`) that
states the bootstrap rule, and one rule each for `git -C`, `EnterWorktree` and the task-file name.

## Proposed solution

- Add a "Before the first install" paragraph: the rules are read from the `policy-writer` worktree; skills are read
  from `policy-writer/claude-skills/<name>/SKILL.md`; no `missions/` links or suggestion box exist; the mission owner
  keeps STATE locally.
- Pick one position on `git -C` (allowed for read-only commands on a named worktree, or forbidden everywhere) and
  fix the four files that disagree; same for `EnterWorktree` and the task-file name.

## Where it might land

CONVENTIONS.md (bootstrap paragraph), `conventions/session-start.md`, `resume-mission`, `conv-feature-worktree-setup`,
`conv-working-outside-worktree`.
