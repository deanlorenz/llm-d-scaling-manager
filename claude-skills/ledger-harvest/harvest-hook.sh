#!/usr/bin/env bash
# harvest-hook.sh — hook entry for ledger-harvest. Used for Stop, PreCompact and SessionEnd.
# Copies the hook JSON from stdin, starts ledger-harvest.sh detached (it outlives this hook and the session),
# and returns at once with exit 0. Exit 0 matters: for PreCompact an exit 2 would block compaction, and
# SessionEnd has a 1.5 s budget by default.
here="$(dirname "$(readlink -f "$0")")"
tmp="$(mktemp "${TMPDIR:-/tmp}/harvest-hook.XXXXXX")" || exit 0
cat > "$tmp"
setsid nohup bash -c '"$0" < "$1"; rm -f "$1"' "$here/ledger-harvest.sh" "$tmp" > /dev/null 2>&1 < /dev/null &
exit 0
