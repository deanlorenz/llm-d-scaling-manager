---
name: wind-down
description: Wind down work on a mission — safe checkpoint or full retirement. Supports explicit user invocation and agent invocation. Can run entirely in the background. Follows conventions/resume-and-handoff.md.
---

# Wind down

Rules:
- Accept `checkpoint` or `retire` as the mode.
- If no mode is supplied, ask the user when running interactively.
- If an agent invokes the skill without a user, use `checkpoint` unless the task explicitly says
  to retire.
- Safe checkpoint: keep the session `active`; do not release ownership; run Steps 1–5.
- Full retirement: run Steps 1–7; retire the session and release ownership.
- Steps 1 and 3 are mandatory in both modes.
- Agent invocations may run all steps in the background without user interaction.
- Record the outcome in the ledger and STATE; report to the parent agent when one exists.

See `conventions/resume-and-handoff.md` for the ownership contract and the `ledger-capture` skill for the ledger-capture contract.

## Step 1: Reach a safe stopping point

Finish whatever you're actively doing to a point that isn't mid-edit or half-applied — this
doesn't mean finishing the whole task, just not leaving a file half-written or a multi-step
operation partially done. Stop any background agents *this session* launched that are still
running and not needed further (`TaskStop`) — don't leave orphaned work running that nothing
will collect. Check for a running Bob worker by command line: `ps -eo args | grep -v grep | grep -c 'bob run'`. Bob runs as a `node` process, so a check on the process name sees nothing.

This step cannot be skipped — winding down mid-edit defeats the purpose.

## Step 2: Final pass over the session ledger

The active ledger at `<mission-worktree>/.session/<this-session-slug>.md` should have been
maintained throughout the session. This step is a safety-net pass — go back over this
session's work and confirm everything is captured: findings, decisions, corrections, false
starts. Append anything missing now.

If the ledger is missing significant work, that is a protocol violation from earlier in the
session — record it honestly here and continue. Do not skip this step on that account.

## Step 3: Update STATE.md

This step is **not skippable**. Update `<mission-worktree>/.session/STATE.md` now. The
mission owner's own STATE.md is single-writer — edit it directly, no `.wip` rename needed.
(`conv-wip-editing` applies only to files you do not own.)

Required every wind-down, regardless of time pressure:
- **Drift scan first:** before updating progress fields, scan STATE for settled design,
  reasoning, or decisions that accumulated this session. Move any found to the correct spec
  section, then remove from STATE. STATE must be thin and current-tense when you're done.
- Mark completed steps `[x]` in the checklist
- Set **Last completed** to the last finished step
- Set **Next step / resume point** to exactly where the next session should pick up
- Update **Status**
- Take every git fact you record (branch position, last installed SHA, commits ahead of the remote) from a command run now, not from earlier STATE text. Branch position: `git fetch`, then `git rev-list --left-right --count <remote-ref>...<branch>`.
- If you changed the STATE template (`conventions/state-vs-ledger.md`) or any field annotation
  this session: apply the same change to this living STATE.md in this same step — template and
  living file must stay in sync

The only part ledger-capture (Step 5) may still update afterward is findings it surfaces from
the ledger text — that is what "skippable if out of time" applies to, not the continuation
fields above.

## Step 4: Review and commit local work; never force a push

Rules:
- Run `git status --short` and inspect the diff.
- Classify every changed and untracked path.
- Commit real mission work, documentation, STATE, and this ledger.
- Do not track credentials, generated output, scratch files, or excluded local artifacts.
- List every untracked/excluded file in the ledger.
- Do not discard unexplained changes; stop if ownership is unclear.
- Identify mission versus PR/feature branch before committing.
- Do not commit `.session/` on PR branches unless explicitly allowed.
- Review the exact staged file list before committing.
- Do not push automatically.
- Push only after single-use user authorization and invoking `conv-push`.
- Before an authorized push, inspect outgoing commits and the remote destination.

## Step 4a: Close the harvest at an end point (only if this session is registered with the ledger harvester)

A session is registered when `resume-mission` Step 10 or `coder.md` registered its ledger. Run in both modes, before Step 5.

The session's current directory may not be a mission worktree, so never call the helper through a relative `.claude/skills/...` path. Build its absolute path in the same Bash call as the command (shell variables do not carry over between calls):

```bash
HP="$HOME/.claude/bin/ledger-harvest/harvest-registry.py"
python3 -I "$HP" close "${CLAUDE_CODE_SESSION_ID:-}" --wait 300
```

The command records the end point (the current end of the transcript), starts the harvester, and waits for the `harvest-end` header in the ledger. Text written after the end point is not lost: after a checkpoint the harvester carries on in the same ledger (Step 5); after a retirement it is wind-down chatter.

Exit code:
- 0: continue with Step 5. Run `status` (define `HP` as above, same call): if `skipped_chunks` is above 0, the harvester skipped chunks after repeated failures (a `[harvest-skipped]` entry marks each). Name them in the report (Step 8); their transcript lines were not harvested, or their raw entries are in the ledger uncurated.
- 1 (not registered, or no session id): skip this step. Step 5 runs as before.
- 2 (no transcript found; if the message says Python cannot open the file, the helper path is wrong: fix `HP`): report it, then continue with Step 5 on the session's own ledger.
- 3 (the harvester failed or is not running) or 4 (no header within 300 s): run `python3 -I "$HP" status "$CLAUDE_CODE_SESSION_ID"` (define `HP` as above in the same call) and read the file it names under `~/.claude/ledger-harvest/failed/`. Do not continue silently. Each chunk is retried at most 3 times in total (a counter in the registry); after that the harvester skips it with a `[harvest-skipped]` entry, and `close ... --force` ignores the counter. Interactive: tell the user what failed and ask: run `close` again (a transient failure usually clears), or continue with Step 5 without the harvester. Agent-invoked: run `close` once more; if it fails again, continue with Step 5 and say so in the report.

## Step 5: Run ledger-capture on this session's own ledger

Run ledger-capture against this session's active ledger file at
`<mission-worktree>/.session/<slug>.md`. After capture appends the verification summary and the
session is retired, move the ledger to `<mission-worktree>/.session/ledger/<slug>.md` and update
its STATE log path.

Default launch (Bob, tested 2026-11-16):
1. Write the task file `.session/task-lc-<n>.md` from `conventions/task_file_template.md` and commit it by exact path. Fill: `Name: lc-<n>`; `Worktree`, `Path`, `Branch` of the mission worktree; `In: <mission>.lc-<n>.in`; `Out: <mission>.lc-<n>`; `Startup verification instructions` (one command at a time; on any failure publish it on `Out:` and stop): `git rev-parse --show-toplevel` equals `Path`, `git branch --show-current` equals `Branch`, `.session/task-lc-<n>.md` exists; `Role / scope`: ledger-capture, follows the `ledger-capture` skill and decides nothing it leaves to the owner; `Progress events`: as listed in the `ledger-capture` skill; `Limits`: writes only STATE.md, the spec and the end of the ledger.
2. Subscribe to `Out:` yourself. Make sure the mission worktree has the `.bob` links (`conv-feature-worktree-setup`, step 4a).
3. Launch:
   ```bash
   export P="Task file: .session/task-lc-<n>.md. Mission: <mission>. Ledger: <ledger path>. In: <mission>.lc-<n>.in. Out: <mission>.lc-<n>. Subscribe with agentbus_subscribe(topic=\"<mission>.lc-<n>.in\", session_id=\"lc-<n>\"). Run the startup verification in the task file first, then load the ledger-capture skill and follow it exactly. Publish status, findings, questions and completion to Out:."
   nohup timeout 600 bob run -w <mission-worktree> --mode ledger-capture --max-turns 80 "$P" < /dev/null > /tmp/lc-<n>.log 2>&1 &
   ```
4. Wait for its completion note on `Out:`. Heartbeats show progress: 5 minutes without one means possibly stuck, so check the process. If this launch does not work, see `conv-background-agents`.

Rules:
- Send progress, clarification, or interim-result requests to its `In:` channel.
- Wait for completion when running interactively.
- An agent-invoked wind-down may continue entirely in the background; record whether capture
  finished.
- Ledger-capture confirms every point in the ledger is reflected somewhere durable and appends
  `## Verified <date>` when done.
- Only after it completes may STATE.md be updated with its findings or references to them.
- Checkpoint mode, after `## Verified` is appended and Step 4a closed the harvest: run `python3 -I "$HP" reopen "$CLAUDE_CODE_SESSION_ID"` (define `HP` as in Step 4a, in the same call) so the harvester carries on in the same ledger. The next ledger-capture handles only what follows the last `## Verified`. Retirement: do not reopen.
- If ledger-capture flags a finding for every mission, propose it yourself (`conventions/mission-owner.md`, "Proposing a rule or process change"). Ledger-capture writes nothing.

This step runs in both modes (checkpoint and retirement).

If the session closes or there is not enough time before ledger-capture finishes, this step
is effectively skipped — do not wait for it and do not block wind-down on it. The next
`/resume-mission` pending-session scan will pick up the unverified ledger and run
ledger-capture at that point.

## Steps 6–7: Full retirement only

*Skip these steps for a safe checkpoint. Session-log entry stays `active`.*

## Step 6: Mark this session's Session-log entry retired

Once ledger-capture (Step 5) has finished and appended its `## Verified` marker: move the active
ledger to `.session/ledger/<slug>.md`, then update its entry in `STATE.md`'s Session log from
`status=active` to `status=retired` with the new ledger path. Edit STATE.md directly — you
own it. This can be combined with Step 3's `STATE.md` update — no need for two round-trips.

## Step 7: Release ownership on agentbus

```
agentbus_publish(topic="mission.<mission-name>", from_session="<this-session-slug>", kind="handoff",
  body="session=<this-session-slug> releasing ownership of <mission-name>")
```

Do this after the Session-log entry is marked `retired` — the release confirms the session
genuinely ended, not just paused.

## Step 8: Report

Tell the user or parent agent plainly what happened — which steps completed, which were skipped and
why, and whether it is safe to close. Distinguish clearly between committed and pushed:
- **Safe checkpoint:** "Checkpoint saved — state committed; session remains active."
- **Full retirement, local only:** "Retirement saved locally — ledger captured and verified,
  state and work committed, ownership released; no push was authorized."
- **Full retirement, pushed:** "Safe to close — ledger captured and verified, state committed,
  push authorized and completed, ownership released."
- **Full retirement, some steps skipped:** say exactly what was skipped and that the next
  `/resume-mission` will pick up the rest.
- **Harvest:** say whether Step 4a closed the harvest, was skipped (not registered), or failed and was bypassed.
- **Ledger-capture didn't finish:** say so explicitly — entry is still `active`, not `retired`;
  don't claim safe to close when it isn't verified yet.
