---
name: feedback-name-doc-with-section-refs
description: "Every reference to a section of an older/other doc must name the doc (e.g. \"spec.md §5.1\"), never a bare \"§5.1\""
metadata:
  node_type: memory
  type: feedback
  originSessionId: 779a7bde-ac7a-4b17-a9c4-5480592ad500
  modified: 2026-10-05T08:46:27.364Z
---

When referring to a section of a previous/other document, always give the document name with the section number — `spec.md §5.1.2`, `composite-signal-redesign.md §2.1` — never a bare `§5.1.2`. Bare `§x` is reserved for the document currently being written.

**Why:** user corrected this 2026-10-05 while rebuilding the composite-signal spec from three older specs whose section numbers overlap (spec.md, composite-signal-redesign.md, spec-v2.md all have §1/§2/...), so a bare section number is ambiguous.

**How to apply:** in chat and in files. Related: [[feedback-show-rendered-md-long-in-files]].
