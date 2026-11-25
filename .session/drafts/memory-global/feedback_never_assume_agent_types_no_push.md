---
name: feedback-never-assume-agent-types-no-push
description: "Ground rules — every session/agent has a role+mission, never overstep it or assign the wrong one; never push/publish without per-operation approval; one-task-at-a-time coder orchestration with per-task spec+commit+review; subagents confined to the target worktree, must report via files not chat"
metadata:
  node_type: memory
  type: feedback
  originSessionId: bde4bb4e-744c-4942-93b8-93c2acf6f90f
  modified: 2026-08-26T14:09:10.739Z
---

Standing rules, stated directly by the user (2026-08-26, single-analyzer worktree session)
after I launched `subagent_type: "go-reviewer"` for an implementation task — it's a
review-only agent (per its own description/mission) and correctly refused to write code.

1. **Every session and every subagent has a role and a mission — never overstep it, and
   never assign the wrong one to a subagent.** The user was explicit that this is not
   narrowly "pick the right `subagent_type` label" — it's the general principle that a
   session's or agent's mission defines what it's for, and handing it work outside that
   mission (or assuming it can flex into a different one) is the actual mistake. Choosing
   `go-reviewer` (a PR-diff-review mission) for coding-implementation work was one instance
   of this, not the rule itself. When delegating, first ask "what is this agent's actual
   mission," and only hand it work that fits that mission — if unsure, ask the user rather
   than guessing.

2. **Never push to git. Never publish to GitHub (PRs, etc.).** The user approves each such
   operation individually — not a standing permission, not inferred from an earlier approval
   in this session. Local commits are fine; `git push`, `gh pr create`, and similar
   publish/share operations always need an explicit ask first, every time.

3. **Don't ignore instructions — ask if unclear.** If a user instruction seems ambiguous or
   in tension with something else, surface the question rather than silently picking an
   interpretation and proceeding.

4. **Coding-task orchestration pattern, when the user asks me to run/orchestrate a coder:**
   - One task at a time — do not batch multiple tasks into one agent invocation expecting it
     to self-sequence through all of them unsupervised.
   - Each task gets a clear spec before the coder starts (Intent / Expected outcome / Todo /
     Refs — the template is `conventions/task_file_template.md`).
   - Each task lands as its own commit — not batched, not squashed across tasks.
   - I (the orchestrating session) review each task's diff when the coder reports it done,
     *before* launching the next task — this is my job to do myself, not to delegate to the
     coder or skip.
   - **A separate background agent may be used for the code-review step** (reviewing the
     coder's commits, producing a report) — this is fine and distinct from the coder itself
     reviewing its own work.

5. **The coder must be structurally confined to its target worktree — cannot run outside
   it, not just instructed not to.** Launching with `isolation: "worktree"` creates the
   agent's own *separate* fresh worktree, which is the wrong tool when the task is "work in
   this specific existing worktree" — it produced exactly this failure once already (agent
   correctly refused, reported it had no write access to the intended path). Do not rely on
   prompt instructions alone ("work in path X, don't go elsewhere") when a structural/tool
   constraint can enforce it instead — omitting `isolation` so the agent inherits the
   orchestrating session's actual cwd was the fix.

6. **All subagents must output to files, never dump long content into the main chat.** This
   applies broadly — coder reports, code-review reports, research findings — anything long
   goes into a file under `docs/plans/...` (or wherever fits the repo's doc conventions), and
   the subagent's chat-visible return should be a short pointer to that file plus a brief
   status, not the content itself. Matches the same file-not-chat discipline already
   recorded for the ledger/spec-writing workflow in this same refactor effort.

**Why this matters:** in this session, launching a review-only agent for implementation work
wasted a full round-trip; a second launch then failed structurally (worktree isolation) before
a third correctly identified the real fix. Both failures trace to moving fast on agent
selection/scoping instead of pausing to check the agent's actual mission and the structural
constraints needed to enforce scope, rather than just stating them in the prompt.

**How to apply:** before every `Agent`/`Workflow` call, state the target agent's actual
mission and confirm the task fits it — don't guess from a name that sounds close. Before any
`git push`/`gh` write command, stop and ask, regardless of what was approved earlier in the
session. When orchestrating multi-step coding work: one task per coder invocation, written
spec first, coder confined to the correct worktree by omitting worktree-isolation (not by
instruction alone), coder and reviewer both write findings to files and return only a short
pointer + status to chat, and I review each task's diff before starting the next.
