---
name: feedback-never-rm-rf-on-unowned
description: "NEVER rm -rf on anything not owned/created, even with user approval for the deletion — use rm on the exact listed file + rmdir for empty dirs"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 7dfdf62c-6499-411f-a5a1-748c4dad51f2
  modified: 2026-10-12T16:37:27.584Z
---

NEVER use `rm -rf` on anything I do not own or did not create — **even when the user has
explicitly approved deleting that folder**. For approved deletions of not-owned content:
`rm` the exact, previously-listed file(s), then `rmdir` the now-empty directories
(`rmdir` refuses non-empty dirs — built-in safety).

**Why:** the user rejected `rm -rf .claude/skills` (contained a tracked, not-mine
`pr-review/SKILL.md`) even though they had just approved "simply delete the folder".
Approval to delete authorizes the *outcome*, never the *tool*. CONVENTIONS.md already had
the clause ("confirm each entry is … a file you created and own") — I misapplied it by
letting the approval override the tool choice. The user added this should live in both
conventions and memories.

**How to apply:** before any removal, list the exact files; for each, ask "did I create
or own this?" If no → single-path `rm` (content verified captured elsewhere first) +
`rmdir`, never `-rf`. When a guard or rejection fires, ask "is there a safer command?"
before retrying. See [[feedback-git-destructive-confirm]].
