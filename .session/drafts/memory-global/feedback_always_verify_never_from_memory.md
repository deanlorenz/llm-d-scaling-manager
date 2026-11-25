---
name: feedback-always-verify-never-from-memory
description: Never answer factual questions about code/mission state from memory or from what a doc claims — always check the actual file/code directly first.
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 37758082-e545-45ea-859e-828e353da659
  modified: 2026-09-23T14:21:20.896Z
---

Always verify factual claims about code or mission state directly (grep/Read the
actual source, file, or test) before stating them — never answer from memory, from
training knowledge, or by trusting what a doc/STATE/decision-table says happened.

**Why:** User correction, composite-analyzer mission, 2026-09-23. This mission's own
history is full of prior verification passes reporting things "landed" that weren't
(verification passes had already flagged items NOT LANDED and then presented
them again as fine). A doc's claim that something "is done" is a claim about a past
state, not the present one.

**How to apply:** Applies broadly — not just to decision-table entries (D-numbers) in
this mission, but to any factual assertion about current code, config, or state,
across all projects. When asked "is X true / did X land / does X exist," grep or Read
the real thing before answering, even if a memory, STATE file, or prior message says
it's true. This reinforces existing rules
[[feedback_capture_conclusions_not_transcript]] (durable docs can be stale) and
[[feedback_dont_deprioritize_unexercised_paths]] (don't trust unverified claims).
