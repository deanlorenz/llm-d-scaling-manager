#!/usr/bin/env bash
# ledger-harvest.sh — keep a session's ledger up to date from its Claude Code transcript.
#
# Run as an async Stop / PreCompact / SessionEnd hook (JSON on stdin), or by hand with the same JSON:
#   echo '{"session_id":"...","transcript_path":"..."}' | ledger-harvest.sh
#
# Registry entry (written by whoever creates the ledger), one per session id:
#   $HARVEST_HOME/<session_id>.json   {"ledger": "/abs/path/to/ledger.md"}
# No entry -> exit 0 silently (most sessions are not harvested). Never breaks the session.
# Every call leaves a request line in $HARVEST_HOME/<session_id>.again (the hook event name) before it tries
# the lock. The one run that holds the lock reads the requests, flushes if one is SessionEnd or PreCompact, and
# runs again until none is left; a call that finds the lock held just exits. One harvester per session.
#
# Two passes, serial, under one per-session lock:
#   pass 1  transcript -> RAW file  ($HARVEST_HOME/<session_id>.raw.md, complete, not tracked)
#           cursor = last "<!-- harvest tl A-B [part i/k] ... -->" header in the raw file
#   pass 2  raw entries -> LEDGER   (curated: drops activity, merges, final state; never drops user points)
#           cursor = last "<!-- curated raw-line A-B ... -->" header in the ledger
# Nothing is truncated: pass 1 chunks by size and splits an oversize entry into parts.
# Each append happens once, after Bob succeeded; a failure leaves the cursors where they were.
set -u

HARVEST_HOME="${HARVEST_HOME:-$HOME/.claude/ledger-harvest}"
BUDGET="${HARVEST_BUDGET:-40000}"            # characters per Bob run
HOLD="${HARVEST_HOLDBACK:-10}"               # raw entries pass 2 leaves for the next run (flush: 0)
MAX_RUNS="${HARVEST_MAX_RUNS:-60}"           # Bob runs per invocation
BOB_TIMEOUT="${HARVEST_BOB_TIMEOUT:-900}"
MAX_TRIES="${HARVEST_MAX_TRIES:-3}"          # failed Bob calls per chunk before the chunk is skipped
FORCE="${HARVEST_FORCE:-0}"                  # 1 = ignore the try counter (the parent retries a chunk on purpose)
here="$(dirname "$(readlink -f "$0")")"
mkdir -p "$HARVEST_HOME/work"
log="$HARVEST_HOME/harvest.log"
say() { printf '%s %s\n' "$(date -u +%FT%TZ)" "$*" >> "$log"; }

input="$(cat)"
sid="$(printf '%s' "$input" | jq -r '.session_id // empty')"
tp="$(printf '%s' "$input" | jq -r '.transcript_path // empty')"
agent="$(printf '%s' "$input" | jq -r '.agent_id // empty')"
event="$(printf '%s' "$input" | jq -r '.hook_event_name // empty')"
[ -n "$agent" ] && exit 0                      # subagent turn: not a session of its own
[ -n "$sid" ] && [ -f "$tp" ] || { say "bad input: sid='$sid' tp='$tp'"; exit 0; }
case "$event" in SessionEnd|PreCompact) HARVEST_FLUSH=1;; esac
[ "${HARVEST_FLUSH:-0}" = 1 ] && HOLD=0

reg="$HARVEST_HOME/$sid.json"
[ -f "$reg" ] || exit 0                         # not a harvested session: nothing to do, nothing to log
ledger="$(jq -r '.ledger // empty' "$reg")"
[ -n "$ledger" ] && [ -f "$ledger" ] || { say "session $sid: ledger missing: '$ledger'"; exit 0; }
raw="$HARVEST_HOME/$sid.raw.md"
[ -f "$raw" ] || printf '# raw harvest %s (not tracked)\n' "$sid" > "$raw"

# Leave the request first, then try the lock: the holder (this call or another) sees the request.
again="$HARVEST_HOME/$sid.again"
printf '%s\n' "${event:-none}" >> "$again"

# One run per session at a time. The kernel drops the lock when the process dies (crash, update, reboot).
exec 9>"$HARVEST_HOME/$sid.lock"
flock -n 9 || { say "session $sid: another harvest is running; $event request left for it"; exit 0; }

# End point and start of this ledger (registry fields, all optional). A recorded line is checked against its
# uuid anchor; if the entry moved, the line is looked up again; if the anchor is gone, stop and say so.
reg_py="$here/harvest-registry.py"
from_line="$(jq -r '.from_line // 0' "$reg")"; after_uuid="$(jq -r '.after_uuid // empty' "$reg")"
until_line="$(jq -r '.until_line // 0' "$reg")"; until_uuid="$(jq -r '.until_uuid // empty' "$reg")"
if [ "$until_line" -gt 0 ]; then
  [ -n "$until_uuid" ] || { say "session $sid: until_line set without until_uuid; stopped"; exit 1; }
  until_line="$("$reg_py" resolve "$tp" "$until_line" "$until_uuid" 2>>"$log")" \
    || { say "session $sid: end-point anchor $until_uuid not resolved (not in the transcript, or the helper failed: see the lines above); stopped, owner must look"; exit 1; }
  HOLD=0                                       # a capture end point flushes: no holdback
fi
if [ "$from_line" -gt 0 ]; then
  [ -n "$after_uuid" ] || { say "session $sid: from_line set without after_uuid; stopped"; exit 1; }
  from_line="$("$reg_py" resolve "$tp" $((from_line - 1)) "$after_uuid" 2>>"$log")" \
    || { say "session $sid: start anchor $after_uuid not resolved (not in the transcript, or the helper failed: see the lines above); stopped, owner must look"; exit 1; }
  from_line=$((from_line + 1))
fi

wd="$HARVEST_HOME/work/$sid"
mkdir -p "$wd/.bob"
ln -sfn "$here/harvest-modes.yaml" "$wd/.bob/custom_modes.yaml"
runs=0

bob_call() {   # bob_call <mode> <prompt>  -> BOB_TEXT
  local out status
  runs=$((runs + 1))
  out="$(cd "$wd" && timeout "$BOB_TIMEOUT" bob run -w "$wd" --mode "$1" --max-turns 4 \
        --disable-mcp --disable-subagents -f json "$2" < /dev/null 2>>"$log")"
  status="$(printf '%s' "$out" | jq -r '.status // empty' 2>/dev/null)"
  [ "$status" = "success" ] || { say "session $sid: bob ($1) failed, status='$status'"; return 1; }
  BOB_TEXT="$(printf '%s' "$out" | jq -r '.last_message // ""')"
}

# Failed Bob calls per chunk are counted in the registry ("tries"), keyed by the chunk's first line. A success clears
# the count. At MAX_TRIES the chunk is skipped with a visible [harvest-skipped] entry so one bad chunk cannot block the
# session's harvest for ever; HARVEST_FORCE=1 ignores the count.
tries_get() { jq -r --arg k "$1" '.tries[$k] // 0' "$reg"; }
tries_inc() { local t="$reg.tmp.$$"; jq --arg k "$1" '.tries[$k] = ((.tries[$k] // 0) + 1)' "$reg" > "$t" && mv -f "$t" "$reg"; }
tries_clear() {
  [ "$(tries_get "$1")" != 0 ] || return 0
  local t="$reg.tmp.$$"; jq --arg k "$1" 'del(.tries[$k])' "$reg" > "$t" && mv -f "$t" "$reg"
}

pass1() {      # 0 = appended a chunk, 1 = caught up, 2 = failure
  local res first last part ptxt entries key n
  res="$("$here/harvest-slice.py" "$tp" "$raw" "$wd/slice.md" "$BUDGET" "$until_line" 2>>"$log")" || { say "slice failed"; return 2; }
  [ "$(printf '%s' "$res" | jq -r '.done // false')" = "true" ] && return 1
  first="$(printf '%s' "$res" | jq -r '.first')"; last="$(printf '%s' "$res" | jq -r '.last')"
  part="$(printf '%s' "$res" | jq -r 'if .part then "\(.part[0])/\(.part[1])" else "" end')"
  ptxt=""; [ -n "$part" ] && ptxt=" part $part"
  key="p1:$first$ptxt"; n="$(tries_get "$key")"
  if [ "$FORCE" != 1 ] && [ "$n" -ge "$MAX_TRIES" ]; then
    printf '\n<!-- harvest tl %s-%s%s %s -->\n- [tl %s] open-question: [harvest-skipped] transcript lines %s-%s were not harvested: the Bob call failed %s times (answers in failed/). Read them in the transcript if they matter.\n' \
      "$first" "$last" "$ptxt" "$(date -u +%FT%TZ)" "$first" "$first" "$last" "$n" >> "$raw"
    say "session $sid: pass 1 tl $first-$last$ptxt SKIPPED after $n failed tries"
    tries_clear "$key"; rm -f "$wd/slice.md"; return 0
  fi
  grep -E '^- \[tl' "$raw" | tail -20 > "$wd/context.md"
  [ -s "$wd/context.md" ] || echo "(none yet)" > "$wd/context.md"
  bob_call ledger-harvest "Record the transcript slice in @slice.md. Entries already recorded (do not repeat them) are in @context.md." \
    || { tries_inc "$key"; rm -f "$wd/slice.md" "$wd/context.md"; return 2; }
  entries="$(printf '%s\n' "$BOB_TEXT" | grep -E '^- \[tl [0-9]+' || true)"
  if [ -z "$entries" ]; then
    # Only an explicit NONE means "nothing to record". Anything else is a failure: keep the answer, do not advance.
    if [ "$(printf '%s' "$BOB_TEXT" | tr -d '[:space:]')" = "NONE" ]; then
      entries="(nothing to record)"
    else
      mkdir -p "$HARVEST_HOME/failed"; printf '%s\n' "$BOB_TEXT" > "$HARVEST_HOME/failed/$sid-p1-$first-$last.txt"
      say "session $sid: pass 1 tl $first-$last: no parseable entries and not NONE; answer saved in failed/; cursor not advanced"
      tries_inc "$key"; rm -f "$wd/slice.md" "$wd/context.md"; return 2
    fi
  fi
  printf '\n<!-- harvest tl %s-%s%s %s -->\n%s\n' "$first" "$last" "$ptxt" "$(date -u +%FT%TZ)" "$entries" >> "$raw"
  tries_clear "$key"
  say "session $sid: raw tl $first-$last$ptxt"
  rm -f "$wd/slice.md" "$wd/context.md"
  return 0
}

pass2() {      # 0 = appended a curated block, 1 = caught up, 2 = failure
  local rcur total bound a r first last entries key n tl1
  rcur="$(grep -oE '<!-- curated raw-line [0-9]+-[0-9]+' "$ledger" | tail -1 | sed -E 's/.*-//')"; rcur="${rcur:-0}"
  total="$(wc -l < "$raw")"
  if [ "$HOLD" -gt 0 ]; then
    bound="$(grep -n '^- \[' "$raw" | tail -n "$HOLD" | head -1 | cut -d: -f1)"
    [ "$(grep -c '^- \[' "$raw")" -le "$HOLD" ] && bound=1
    bound=$((bound - 1))
  else
    bound="$total"
  fi
  a=$((rcur + 1))
  # An entry belongs to this ledger when the first transcript line of its range is in [from_line, until_line].
  r="$(awk -v a="$a" -v b="$bound" -v B="$BUDGET" -v out="$wd/raw.md" -v from="$from_line" -v until="$until_line" '
        NR>=a && NR<=b && /^- \[/ { tl=$0; sub(/^- \[tl /, "", tl); tl=tl+0
                                    if (tl < from) next; if (until > 0 && tl > until) next
                                    if (sz>0 && sz+length($0)>B) exit; print $0 > out; sz+=length($0)+1; last=NR; if(!first) first=NR }
        END { print first+0, last+0 }' "$raw")"
  first="${r% *}"; last="${r#* }"
  [ "$first" -gt 0 ] || { rm -f "$wd/raw.md"; return 1; }
  key="p2:$first"; n="$(tries_get "$key")"
  if [ "$FORCE" != 1 ] && [ "$n" -ge "$MAX_TRIES" ]; then
    # Nothing is lost: the raw entries go into the ledger as they are, behind a visible marker.
    tl1="$(head -1 "$wd/raw.md" | grep -oE '^- \[tl [0-9]+' | grep -oE '[0-9]+$')"
    printf '\n<!-- curated raw-line %s-%s %s -->\n- [tl %s] open-question: [harvest-skipped] curation of raw-line %s-%s failed %s times (answers in failed/); the raw entries follow uncurated.\n%s\n' \
      "$first" "$last" "$(date -u +%FT%TZ)" "${tl1:-0}" "$first" "$last" "$n" "$(cat "$wd/raw.md")" >> "$ledger"
    say "session $sid: pass 2 raw-line $first-$last SKIPPED after $n failed tries (raw entries copied)"
    tries_clear "$key"; rm -f "$wd/raw.md"; return 0
  fi
  grep -E '^- \[' "$ledger" | tail -60 > "$wd/curated-context.md"
  [ -s "$wd/curated-context.md" ] || echo "(none yet)" > "$wd/curated-context.md"
  bob_call ledger-curate "Curate the raw entries in @raw.md. Entries already in the ledger (do not repeat them) are in @curated-context.md." \
    || { tries_inc "$key"; rm -f "$wd/raw.md" "$wd/curated-context.md"; return 2; }
  entries="$(printf '%s\n' "$BOB_TEXT" | grep -E '^- \[' || true)"
  if [ -z "$entries" ]; then
    if [ "$(printf '%s' "$BOB_TEXT" | tr -d '[:space:]')" = "NONE" ]; then
      entries="(nothing to record)"
    else
      mkdir -p "$HARVEST_HOME/failed"; printf '%s\n' "$BOB_TEXT" > "$HARVEST_HOME/failed/$sid-p2-$first-$last.txt"
      say "session $sid: pass 2 raw-line $first-$last: no parseable entries and not NONE; answer saved in failed/; cursor not advanced"
      tries_inc "$key"; rm -f "$wd/raw.md" "$wd/curated-context.md"; return 2
    fi
  fi
  printf '\n<!-- curated raw-line %s-%s %s -->\n%s\n' "$first" "$last" "$(date -u +%FT%TZ)" "$entries" >> "$ledger"
  tries_clear "$key"
  say "session $sid: curated raw-line $first-$last"
  rm -f "$wd/raw.md" "$wd/curated-context.md"
  return 0
}

caught_up=0
while :; do
  # Take the requests left so far; a SessionEnd or PreCompact among them means flush (no holdback) from now on.
  if mv -f "$again" "$again.work" 2>/dev/null; then
    grep -qE '^(SessionEnd|PreCompact)$' "$again.work" && { HARVEST_FLUSH=1; HOLD=0; }
    rm -f "$again.work"
  fi
  caught_up=0
  while [ "$runs" -lt "$MAX_RUNS" ]; do
    did=0
    pass1; rc=$?; [ $rc -eq 2 ] && exit 1; [ $rc -eq 0 ] && did=1
    pass2; rc=$?; [ $rc -eq 2 ] && exit 1; [ $rc -eq 0 ] && did=1
    [ $did -eq 0 ] && { caught_up=1; break; }
  done
  [ -f "$again" ] || break                       # a call came in while we worked: go round again
done
# Reached the end point with both passes caught up: mark the ledger (once). The caller waits for this header.
if [ "$caught_up" = 1 ] && [ "$until_line" -gt 0 ] && ! grep -q "^<!-- harvest-end line $until_line " "$ledger"; then
  printf '\n<!-- harvest-end line %s %s -->\n' "$until_line" "$(date -u +%FT%TZ)" >> "$ledger"
  say "session $sid: harvest end line $until_line"
fi
# A call may have left a request after the last check and found the lock still held: release it and look once
# more; if there is one, start again as a new run (it takes the lock itself).
exec 9>&-
[ -f "$again" ] && { printf '%s' "$input" | exec "$0"; }
exit 0
