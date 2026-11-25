---
name: feedback-ask-questions-short-and-scannable
description: "AskUserQuestion question text must be short and scannable, not a context dump"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: a62f398b-c9ed-4c81-be26-75f1bdff01f4
  modified: 2026-09-09T11:50:22.015Z
---

Keep `AskUserQuestion` question text short and scannable — a sentence or two framing the decision,
not a paragraph recapping the full investigation. Put background in prior chat messages/files, not
crammed into the question string itself.

**Why:** User feedback, verbatim: "I do not want to read such long messages as decision questions.
This is unreadable and impossible to find later." A long question is hard to read in the moment
and, since it's not organized like a doc, hard to search back for later.

**How to apply:** Before calling `AskUserQuestion`, if the `question` field is more than ~2-3
sentences, move the detail elsewhere first (a short chat message, or a file) and reduce the
question itself to the actual decision point plus just enough context to disambiguate the options.
Applies to any tool that surfaces a question/decision to the user, not just this one.

Also related: when a coder/spec gives too much unilateral discretion and a divergence happens,
the user wants the underlying spec/task-file gap discussed and fixed cleanly rather than resolved
ad hoc per incident — see [[feedback_never_deviate_from_approved_plan]] and
[[feedback_resolve_ambiguity_before_coder_dispatch]].
