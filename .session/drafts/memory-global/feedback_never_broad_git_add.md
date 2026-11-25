---
name: feedback-never-broad-git-add
description: "NEVER use a broad git add (git add ., -A, -u, dir/) — always name exact file paths"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 40a92f7f-2a92-40ff-bcd7-1762bd6fd1c1
  modified: 2026-10-14T15:01:07.494Z
---

NEVER use a broad `git add` — no `git add .`, `-A`, `-u`, `--all`, or a directory path. Always stage exact, named file paths.

**Why:** user rule (2026-10-14, benchmark-waldorf). Workspaces such as `results/` hold generated files, including llmdbenchmark's `context.ctx`, a raw kubeconfig credential. A broad add can commit secrets or unreviewed output. Ignore rules are a backstop, not the guard.

**How to apply:** before every commit, `git add <exact paths>` only, then check `git status --short`. This applies to the mission worktrees and any repo.
