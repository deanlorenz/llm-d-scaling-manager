---
name: feedback-resolve-ambiguity-before-coder-dispatch
description: "Never pass an \"A and/or B\" or similarly optional spec instruction into a coder's task prompt verbatim — resolve it to one precise, checkable instruction before dispatch"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 2f961960-731c-4005-96ca-17c110db1d04
  modified: 2026-09-06T22:51:44.094Z
---

Never write a coder/subagent task instruction that leaves the coder a choice between options
("add a log line and/or a metric", "use X or Y", etc.). Resolve every such ambiguity to one
precise, concrete instruction *before* dispatch — even when the ambiguity originated in a spec
document written earlier, not in the task prompt itself.

**Why:** On 2026-09-06/07 in the single-analyzer mission, `spec.md`'s CT6 fix design
said "add a log line (and/or metric)" for the post-normalization composite signal. The task
prompt to the coder carried that phrasing forward unchanged. The coder built only the log line
and moved on — no decision point was ever visible, so the unbuilt metric half went completely
untracked until the user noticed it missing during a later review. User: "NEVER give the coder
a choice. Only precise instructions — that is exactly how things get forgotten."

**How to apply:**
- Before writing any task prompt/STATE file for a coder, scan the instructions (including any
  spec text being copied in) for optional/either-or phrasing: "and/or", "or", "your call",
  "if applicable", "as needed". Each one is a decision the mission owner must make now, not
  defer to the executor.
- If both options should eventually happen but only one fits the current task's scope, say so
  explicitly and create an explicit tracked line (STATE.md Known Issues / TODO) for the deferred
  half — so "not done yet" is visible, not silent.
- A spec document being pre-existing and already reviewed does not exempt its ambiguous phrasing
  from this — resolve it at dispatch time regardless of where the ambiguity originated.
- After a coder finishes, check its output against the *resolved* instruction, not the original
  ambiguous one — "the coder did something reasonable" is not the same as "the coder did the
  thing I actually needed."
