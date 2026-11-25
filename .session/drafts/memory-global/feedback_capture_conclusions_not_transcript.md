---
name: feedback-capture-conclusions-not-transcript
description: "How to persist decisions from a discussion: self-contained conclusions in the durable doc, not ledger transcript, and not just stated in chat"
metadata: 
  node_type: memory
  type: feedback
  originSessionId: 1af7b12e-fa70-4889-8fc6-abc13f5853a7
  modified: 2026-10-12T16:46:51.589Z
---

When a decision comes out of a long back-and-forth (a live code review, a design discussion),
persisting it means writing the **bottom-line conclusion as a self-contained statement** in the
durable doc (a spec's decision table, not the ledger) — checkable against the code by someone
with zero context on the conversation that produced it. It does not mean copying fragments of
what was said (an item number, a "TBD" note, a reference back to the chat) and assuming the
reader can reconstruct the rule from there.

**Why:** During a `composite-analyzer` mission review (2026-09-22/23), a decision (rename a
loop variable from a bare float to a `VariantCapacity`) was referenced from a table row's `Ref`
column but never actually stated as its own rule anywhere — it silently dropped out because the
capture leaned on "the reader was there for the discussion" instead of writing the rule itself.
Caught only when the user asked directly whether persistence was complete. Root cause named by
the user: "you blindly copy text from the session instead of the bottom-line conclusions... some
text only makes sense in context and in relation to the conversation. The capture should not
rely on having that discussion."

A related, sharper failure in the same session: saying "two corrected rules, going forward" in
a chat reply and treating that sentence as if it were the fix — it wasn't written to memory, a
doc, or anywhere else. Stating an intention in chat is not capturing it. If it isn't written to
a durable file in the same turn, it doesn't exist after the conversation ends.

**How to apply:**
- The ledger is a real-time safety net only — write to it as things happen, but once a decision
  is reflected in its true durable home (spec doc, memory, STATE), the ledger entry has no
  further job. Don't treat the ledger as something a future session needs to read to understand
  a decision.
- When writing a decision row/entry: before moving on, reread it and ask "would this make sense
  and be actionable to someone who was not in this conversation?" If it references "TBD",
  "see item N", or a bare pointer without restating the rule, it has failed this test.
- When I say "going forward I will do X" in a chat reply, that sentence is not the fix. The fix
  is writing X to the actual file (memory, CLAUDE.md, spec doc) in that same turn, before
  claiming it's handled.

**Sharpened 2026-10-12 (benchmark-waldorf mission):** the ledger itself is **append-only,
one-line-per-event** — a simple log of decisions/actions as they happen. Never edit prior
ledger entries in place, and never use the ledger as a session-progress or memory file
(narrative findings, corrections folded into old entries, decision-store content all
belong elsewhere). Routing: progress + mission parameters → STATE; settled
decisions/plans → the mission spec; the ledger only records that they happened. User:
"the ledger is not meant to be your session progress or memory file."
