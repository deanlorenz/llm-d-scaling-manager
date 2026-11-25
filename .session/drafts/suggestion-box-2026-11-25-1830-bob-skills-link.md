# Suggestion: link the whole skills folder for Bob, as for Claude

## Finding

`conv-feature-worktree-setup` Step 3 links the whole skills folder for Claude
(`<worktree>/.claude/skills -> session-tracking/claude-skills`), but Step 4a links Bob per file: it creates
`<worktree>/.bob/skills/` as a real directory holding one link, `ledger-capture`. So Bob sees one skill and every other
conv-* skill is missing for it, and a new skill needs a new link in every worktree. Evidence: Step 4a of
`session-tracking/claude-skills/conv-feature-worktree-setup/SKILL.md` (the loop over the pairs
`custom_modes.yaml:bob/custom_modes.yaml` and `skills/ledger-capture:claude-skills/ledger-capture`); user ruling
2026-11-25: the Bob links should be like the Claude links.

## Need

Bob gets the same skills as Claude, with one link per worktree.

## Proposed solution

In Step 4a replace the per-skill link by one directory link, `<worktree>/.bob/skills -> ../../session-tracking/claude-skills`
(relative, computed with `realpath --relative-to`), keep the `custom_modes.yaml` link, keep `.bob` in the shared exclude.
If `<worktree>/.bob/skills` already exists as a real directory holding only links, remove each link by exact path and
`rmdir` it before linking. Update the "ledger-capture" wording in the Bob parts of `conv-background-agents` if it names the
per-skill link.

## Where it might land

`claude-skills/conv-feature-worktree-setup/SKILL.md` (Step 4a), the line about `.bob` in `CONVENTIONS.md`'s layout block.
