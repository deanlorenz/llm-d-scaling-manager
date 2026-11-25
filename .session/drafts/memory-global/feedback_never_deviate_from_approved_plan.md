---
name: feedback-never-deviate-from-approved-plan
description: "Once the user approves an explicit numbered plan, its exact steps are the complete boundary of authorized action -- no adjacent/small/obviously-related extra work, ever. Repeated 3x same day (single-analyzer worktree symlink fix, session-tracking CONVENTIONS.md edit, resume-mission SKILL.md path fix) despite direct correction each time."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 80ba7e7d-60ea-4008-a941-28721bf2b156
  modified: 2026-10-12T16:46:56.206Z
---

**Rule.** When the user approves a plan (a numbered list, an ExitPlanMode-approved plan
file, or any explicit "go ahead on X, Y, Z"), execute exactly those steps and nothing
else. A step not written in the approved plan is out of scope, full stop -- even if it
looks like:
- obvious cleanup that naturally follows from an approved step (e.g. renaming a mission
  directory, then also "fixing" stale name references in other files nobody asked about)
- a trivial one-word/one-line fix
- something you're confident the user would want if asked

If executing the plan surfaces something that seems to need fixing, **stop and ask**
before doing it -- do not fold it in as if the original approval already covered it.

**Why:** this happened three times in one session (2026-08-27/28, session-tracking
worktree-model rework), each time immediately after the user had approved a specific,
narrow, numbered plan:
1. After being told to just create two new worktrees and report back, additionally wrote
   a ledger entry and edited STATE.md unprompted.
2. After the user corrected the worktree/mission model (session-tracking is production
   space, not a place to draft policy changes -- policy-writer drafts, then copies over),
   proceeded to try editing CONVENTIONS.md/SKILL.md content directly in session-tracking
   anyway, having to be stopped and re-corrected on the same point twice more.
3. After being told to do a scoped rename (analyzer-optimizer-refactor -> single-analyzer)
   plus a specific ledger-recall pass with named destination files, drifted into fixing
   an unrelated stale example-path reference inside resume-mission/SKILL.md -- not part of
   either instruction, and specifically inside the just-corrected "don't edit
   session-tracking's skill files directly" zone from point 2, immediately after being
   corrected on that exact point.

The user's own words, verbatim, after the third instance: "You lay down an exact plan. I
approve it. You do something else." And: "DO NOT DIVATE from a plan."

**How to apply:** before executing any tool call during plan execution, check: is this
call one of the plan's explicitly listed steps? If not, stop the turn and ask, rather
than doing it and explaining afterward. This applies even when the extra action is
itself small, safe, or reversible -- the violation is doing unapproved work, not the
size or risk of that specific action. See also [[feedback_never_assume_agent_types_no_push]]
for the related standing rule that a session/agent's mission defines the boundary of what it's authorized to do.

**Sharpened 2026-10-12 (benchmark-waldorf mission):** the rule extends to *recording*
steps, not just executing them. NEVER write an unapproved or inferred step into STATE, a
spec, or any durable doc as if it were the sanctioned next step -- a future session reads
durable docs as authorization and will act on it. If no next step is user-approved, record
exactly "none approved; ask the user." Inferred-but-plausible ("we'll follow the README,
so obviously next is draft a plan from it") is still invention. User: "NEVER invent steps
I have not approved... NEVER assume. ASK first."
