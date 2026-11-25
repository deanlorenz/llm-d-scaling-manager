---
name: feedback_never_answer_about_code_without_reading
description: "Never state what code does/doesn't do, or answer a question about code, without reading the actual code first — no exceptions for seemingly-obvious cases"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4033edd3-ce50-40a3-9c27-83705af7cacf
  modified: 2026-09-27T09:16:29.457Z
---

Never answer a question about what code does, or make a claim about code behavior (including
accepting/rejecting part of a prior comment or claim), without reading the actual code first.
This applies even when the answer feels obvious, even when it's a small follow-up to something
just discussed, and even when asking the user a clarifying question would seem faster than
re-reading.

**Why:** During composite-analyzer code review (2026-09-24), this failure happened twice in one
session on the same function (`decrementRoleSpare`): first, speculated about a comment's
correctness against `aggregation.AggregateByRole` without reading that function, guessed wrong,
and the user had to state the correct answer directly. Then, immediately after, deleted a
different sentence in the same comment ("Never mutates Result") based on the user's general
"the rest is junk" instruction without independently checking that specific claim against the
code — it turned out the function does mutate `e` (the enclosing struct, via a map field), making
the deleted claim's status genuinely unclear rather than obviously fine to remove. Then asked the
user a clarifying question instead of just reading the code to settle it. The user's exact words:
"NEVER answer questions about code without reading the code -- that is irresponsible behavior
that wastes my time."

**How to apply:** Before writing or deleting any comment claim, before answering "does X do Y,"
before accepting a user's characterization of code as true/false, before proposing a diff — read
the specific function/lines in question first, in this turn, even if a related read happened
minutes ago and even if the answer seems inferable from context. If after reading the answer is
still genuinely unclear, say so and ask a real (non-multiple-choice-guess) question — see
[[feedback_stop_guessing_via_askuserquestion]] — but reading always comes first, never as an
alternative to it.
