---
name: feedback-dont-deprioritize-unexercised-paths
description: "Never treat \"my test run didn't exercise this code path\" as a signal that it's unimportant, low-priority, or safe to defer."
metadata: 
  node_type: memory
  type: feedback
  originSessionId: ad8383e2-12a5-4b32-a85f-d992bd265264
  modified: 2026-08-19T14:21:20.337Z
---

Do not use "this code path wasn't exercised in my test/run" as a reason to
deprioritize, defer, or downplay building support for it (extraction,
tooling, coverage, etc.). Existing code paths should be assumed to cover a
real, possible scenario someone deliberately wrote — the fact that one
particular smoke test didn't happen to trigger it is not evidence about its
importance.

**Why:** Corrected directly after doing this in the old sandbox repo's
benchmark-tooling port: I found real k1/k2 saturation-analyzer decision log
lines (`k2-decision`, `replica-capacity-decision`, `variant-capacity-source`,
`zero-replica-capacity-estimate`, etc.) that an existing tool
(`dump_k2_decisions.py`) already parses, and I framed *not yet building*
equivalent extraction into my own tooling as "blocked on validation" because
my one real test run never exercised those paths. That framing is wrong: a
tiny single-variant, never-scaled smoke test not hitting a zero-replica/
scale-from-zero/multi-tier-fallback path says nothing about whether that path
matters — it says my test was narrow. The user's correction: "always assume
that existing code is covering a real possible path. Analyzing if a code path
has become redundant is typically a different mission" — i.e. determining
dead/redundant code is its own deliberate investigation, never a side-effect
inference from "I didn't happen to see it fire."

**How to apply:** When auditing or extending observability/extraction/test
coverage and a real code path exists (a log line, a metric, a branch, an
error case) that a specific run/test didn't trigger: build/extract for it
anyway, on schedule with everything else that *did* fire. It is fine to note
factually that you lack *end-to-end validation data* for that specific piece
(a real limitation worth stating) — but that must never be phrased or acted
on as a reason the work itself is lower priority or deferrable. If the user
wants to know whether a code path is actually dead, they will ask for that
specifically as its own investigation.
