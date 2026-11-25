#!/usr/bin/env python3
"""Build the next transcript chunk for ledger-harvest.sh.

usage: harvest-slice.py <transcript.jsonl> <raw-file> <slice-out> <budget-chars> [until-line]

until-line (optional, > 0): never read past this transcript line (the end point of a capture).

Nothing is truncated. The chunk holds whole transcript entries up to the budget. An entry larger than
the budget is split at paragraph/space boundaries into parts; each part is a chunk of its own.

The cursor is read from the raw file: the last header "<!-- harvest tl A-B [part i/k] ... -->".
A header with part i/k and i<k means the entry at line B is only partly done.

stdout: {"done": true}  or  {"first": A, "last": B, "part": [i, k] | null, "count": n, "chars": c}
"""
import json
import os
import re
import sys

tp, raw, out, budget = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
until = int(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] else 0

HDR = re.compile(r"<!-- harvest tl (\d+)-(\d+)(?: part (\d+)/(\d+))? ")
last = None
try:
    with open(raw, encoding="utf-8") as f:
        for line in f:
            m = HDR.match(line)
            if m:
                last = m
except FileNotFoundError:
    pass

cursor, resume_line, resume_part = 0, 0, 0
if last:
    end = int(last.group(2))
    if last.group(3) and int(last.group(3)) < int(last.group(4)):
        cursor, resume_line, resume_part = end - 1, end, int(last.group(3))
    else:
        cursor = end

SECRETS = [
    (re.compile(r"sk-[A-Za-z0-9_-]{10,}"), "[redacted]"),
    (re.compile(r"((?:token|api[_-]?key|password|secret)[A-Za-z_]*[\"=: ]+)[^ \",]{6,}", re.I), r"\1[redacted]"),
]


# Tool traffic is context, not content (user decision 2026-11-24): a tool call is shown as its name and a short
# target; a tool result as its first HEAD characters. Kept in full: tools that carry the assistant's words to the
# user or the user's words back (questions, messages, plans), errors, and rejections (they hold the user's comments).
HEAD = int(os.environ.get("HARVEST_RESULT_HEAD", "400"))
SHORT = 160
FULL_TOOLS = {"AskUserQuestion", "SendMessage", "ExitPlanMode", "mcp__agentbus__agentbus_ask_user",
              "mcp__agentbus__agentbus_publish"}
TARGET_KEYS = ("command", "file_path", "path", "pattern", "url", "query", "skill", "topic", "name")
USE_NAMES = {}


def short_use(b):
    name, inp = b.get("name"), b.get("input") or {}
    if name in FULL_TOOLS:
        return "(tool %s: %s)" % (name, json.dumps(inp, ensure_ascii=False))
    if name in ("Agent", "Task"):
        d = str(inp.get("description", ""))[:300]
        return "(tool %s: %s %s)" % (name, inp.get("subagent_type", ""), d)
    parts = ["%s=%s" % (k, str(inp[k])[:SHORT]) for k in TARGET_KEYS if k in inp][:2]
    return "(tool %s: %s)" % (name, "; ".join(parts))


def short_result(b, c):
    full = (USE_NAMES.get(b.get("tool_use_id")) in FULL_TOOLS or b.get("is_error")
            or str(c).startswith("The user doesn't want") or "user said" in str(c).lower()[:200])
    if full or len(c) <= HEAD:
        return "(result: %s)" % c
    return "(result: %s … [+%d chars])" % (c[:HEAD], len(c) - HEAD)


def queued_text(prompt):
    if isinstance(prompt, list):
        return " ".join(b.get("text", "") for b in prompt if isinstance(b, dict))
    return str(prompt or "")


def text_of(content):
    if isinstance(content, str):
        return content
    parts = []
    for b in content or []:
        if not isinstance(b, dict):
            continue
        t = b.get("type")
        if t == "text":
            parts.append(b.get("text", ""))
        elif t == "tool_use":
            parts.append(short_use(b))
        elif t == "tool_result":
            c = b.get("content")
            if isinstance(c, list):
                c = " ".join(x.get("text", "") for x in c if isinstance(x, dict))
            parts.append(short_result(b, str(c)))
    return " ".join(parts)


def clean(t):
    for rx, rep in SECRETS:
        t = rx.sub(rep, t)
    return t.replace("\r", "").replace("\n", " ⏎ ")


def split(t, limit):
    parts = []
    while len(t) > limit:
        cut = max(t.rfind(" ⏎ ", 0, limit), t.rfind(" ", 0, limit))
        if cut < limit // 2:
            cut = limit
        parts.append(t[:cut])
        t = t[cut:].lstrip()
    parts.append(t)
    return parts


# Map tool_use id -> tool name over the whole transcript, so a result in a later chunk finds its tool.
with open(tp, encoding="utf-8") as f:
    for line in f:
        if '"tool_use"' not in line:
            continue
        try:
            e = json.loads(line)
        except ValueError:
            continue
        for b in ((e.get("message") or {}).get("content") or []):
            if isinstance(b, dict) and b.get("type") == "tool_use":
                USE_NAMES[b.get("id")] = b.get("name")

chunk, size, first, lastn = [], 0, None, None
part = None
with open(tp, encoding="utf-8") as f:
    for n, line in enumerate(f, 1):
        if n <= cursor:
            continue
        if until and n > until:
            break
        try:
            e = json.loads(line)
        except ValueError:
            continue
        kind = e.get("type")
        if kind == "attachment":
            # A message the user typed while the assistant was working (delivered with a tool result) is recorded
            # as a queued_command attachment, not as a user entry. Without this the harvester never sees it.
            att = e.get("attachment") or {}
            if att.get("type") != "queued_command":
                continue
            queued = queued_text(att.get("prompt"))
            if queued.lstrip().startswith("<task-notification"):
                t = clean("(notification: %s)" % queued[:HEAD])      # a background task finished: not the user's words
                kind = "user"
            else:
                t = clean(queued)
                kind = "user"
        elif kind not in ("user", "assistant") or e.get("isMeta"):
            continue
        else:
            t = clean(text_of((e.get("message") or {}).get("content")))
        if not t.strip():
            continue
        prefix = "[tl %d] %s: " % (n, kind)
        if len(prefix) + len(t) > budget:
            if chunk:
                break                      # emit what we have; this entry is handled by the next call
            pieces = split(t, budget - 60)
            k = len(pieces)
            i = resume_part if n == resume_line else 0
            chunk = ["[tl %d part %d/%d] %s: %s" % (n, i + 1, k, kind, pieces[i])]
            first = lastn = n
            part = [i + 1, k]
            size = len(chunk[0])
            break
        if chunk and size + len(prefix) + len(t) + 1 > budget:
            break
        chunk.append(prefix + t)
        size += len(prefix) + len(t) + 1
        first = n if first is None else first
        lastn = n

if not chunk:
    print(json.dumps({"done": True}))
    sys.exit(0)

with open(out, "w", encoding="utf-8") as f:
    f.write("\n".join(chunk) + "\n")
print(json.dumps({"first": first, "last": lastn, "part": part, "count": len(chunk), "chars": size}))
