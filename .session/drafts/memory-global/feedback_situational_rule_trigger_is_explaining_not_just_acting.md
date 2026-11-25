---
name: feedback-situational-rule-trigger-is-explaining-not-just-acting
description: "Not every explanation of a guarded mechanism is the situational-rule trigger — a \"do you know how\" question is fine to answer from judgment; the real trigger is being asked to simulate/plan the actual steps"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: f0b5d26d-8d1e-4d1f-8bc6-293e564eb247
  modified: 2026-09-08T20:08:03.324Z
---

A situational rules file's trigger (e.g. `coder-orchestration.md`, gated on "before dispatching or
orchestrating a coder agent") does **not** fire on every question that touches the guarded area.

**Why:** In the `composite-analyzer` mission (2026-09-08), asked "do you know how to launch a
coder and reviewer in the bg?", I answered from general `Agent`-tool knowledge plus a prior-session
memory note instead of reading `conventions/coder-orchestration.md` first, and the answer missed
some specifics (`worktree-delegation.md`, the three named isolation setups, a numbered rule I'd
guessed at instead of citing). I initially treated this as a process failure and wrote a memory
saying the trigger fires on "any authoritative statement about the guarded area." **The user
corrected that directly: the judgment call was reasonable for a plain question.** Not every
explanation is a trigger. If unsure whether an answer needs the source file, ask the user whether
they want the actual steps simulated — *that* request is the real trigger, not the question itself.

**How to apply:** answer "do you know how to X" from existing knowledge/memory when it's a
genuine question, not a proxy for starting the work. Ask the user "want me to walk through the
actual steps I'd take?" when the judgment call about triggering is close — offering to simulate
is itself fine and costs nothing; simulating without asking, or treating every mention of a
guarded topic as the trigger, is the overcorrection to avoid. Read the file for real once dispatch
(or a requested simulation of it) is actually imminent.
