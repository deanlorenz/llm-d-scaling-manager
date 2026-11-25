---
name: conv-guard-hook
description: Use only when a hook has just refused one of your Bash commands (a "Blocked: ..." message from the git guard hook). Holds the two-pass approval rule and the rules for the override marker.
---

# conv-guard-hook

Runs in your own session. Apply when a hook has just refused one of your commands.

The git guard hook (`~/.claude/bin/guard-destructive-git.sh`) blocks destructive git commands: hard reset, rebase, force-push, branch force-delete, clean, and checkout or restore of working-tree changes.

## Two passes

1. **First pass:** the command was blocked. Stop. Do not retry. Tell the user the exact command, its scope, and how to recover from it, and ask for approval of that exact command.
2. **Second pass:** only after the user approves that command in this conversation, run that one command again with the override marker named in the hook's message.

## Rules

- The marker comes only from the hook's message. Never write it into any file, task file, skill, or convention. If an instruction you received has it embedded, remove it from what you pass on and use it only for the second pass of the approved command.
- Never reuse the marker for another command. Never add it to a command that is not itself the approved git command.
- A background worker reports the blocked command on `Out:` and waits. The parent asks the user, then tells the worker on `In:` to run that one command again with the marker.
- If the hook blocked a command that does no git operation, because the phrase sits inside text (a commit message, a heredoc, a note): do not use the marker. Reword the text, or write it through a file and concatenate.
- If a guarded shell refuses a command it cannot verify, keep each call simple and literal: one purpose per call, literal paths, quoted expansions, `--` before path operands.
