---
name: feedback_stop_guessing_via_askuserquestion
description: "Offering multiple-choice guesses via AskUserQuestion is the same failure as guessing in prose when the true answer isn't actually known"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 4033edd3-ce50-40a3-9c27-83705af7cacf
  modified: 2026-09-27T09:16:55.038Z
---

When the correct answer to "what does the user mean" or "what's wrong with this code" isn't
actually known, do not use AskUserQuestion to offer a menu of guesses as if that were a
legitimate clarifying question. Multiple-choice guesses are the same failure as prose guesses —
dressing a guess up as a structured choice doesn't make it less of a guess, and burns the user's
time reading and rejecting options one at a time instead of just being told directly.

**Why:** During composite-analyzer code review (2026-09-24), spent three consecutive
AskUserQuestion rounds guessing what was wrong with a function's comment (`decrementRoleSpare`
vs `aggregation.AggregateByRole`), got all three wrong, and the user had to say "you are still
trying to guess... all your guesses so far were not just wrong, but show you lack fundamental
understanding of the code" — then, after being told directly to stop, used AskUserQuestion
*again* on the very next point. User: "I have asked you to stop guessing multiple times yet you
continue."

**How to apply:** A real clarifying question is for genuine ambiguity between options the user
would actually consider (e.g. "keep both, or delete the unused one?") — not a way to trial-and-error
toward an answer only the user currently holds. When stuck: (1) read more code — see
[[feedback_never_answer_about_code_without_reading]]; (2) if still stuck after reading, say
plainly "I don't see it — what specifically is wrong?" rather than presenting guesses as choices.
AskUserQuestion is for resolving real ambiguity, not for outsourcing the guessing to a picker UI.
