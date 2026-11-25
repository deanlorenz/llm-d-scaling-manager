---
name: StatusLine PS1 Translator
description: Translate PS1 escapes to a dynamic status line for Claude Code's statusLine
type: project
---

The StatusLine PS1 Translator expands common Bash PS1 escapes (e.g., \u, \h, \w, \t, \A, \d, \s, \D{format}) into a dynamic status line for Claude Code's statusLine.

How to use:
- Script path: /home/dean/.claude/statusline_ps1.sh
- Environment variable: PS1_FORMAT to customize the PS1-like string (default: \u@\h:\w\$)
- Settings.json should reference the script via a statusLine command, e.g.:
  "statusLine": { "type": "command", "command": "bash -lc '/home/dean/.claude/statusline_ps1.sh'" }

Notes:
- The translator strips color wrappers (\[ and \]) so the output is clean in Claude Code's status line.
- The initial version focuses on core tokens; a follow-up can add Git integration (branch, dirty state) and advanced tokens.
