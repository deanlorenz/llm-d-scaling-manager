---
name: feedback-show-rendered-md-long-in-files
description: "Never show markdown drafts as code blocks in chat; long drafts go in a file, chat gets a short pointer"
metadata:
  node_type: memory
  type: feedback
  originSessionId: 779a7bde-ac7a-4b17-a9c4-5480592ad500
  modified: 2026-10-04T16:05:39.575Z
---

When presenting markdown (e.g. a spec section draft), never wrap it in a code block — show rendered/rich text. Anything long goes into a file (the target doc or a .session/ scratch file) with a short pointer in chat.

**Why:** user corrected this 2026-10-04 while drafting the composite-signal spec; chat-preferences.md already says long content belongs in files, and I still dumped a code-fenced draft.

**How to apply:** draft sections directly into the file, reply with a link + numbered short notes. Related: [[feedback-ask-questions-short-and-scannable]].
