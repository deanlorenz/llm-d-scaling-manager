#!/usr/bin/env python3
"""Registry and anchor helper for ledger-harvest (end point of a capture).

usage:
  harvest-registry.py resolve <transcript> <line> <uuid>
      Check that the entry on <line> has <uuid>. If not, search the transcript for it.
      stdout: the line number to use. exit 0 = found (stderr says "moved" if it shifted), exit 1 = nowhere.
  harvest-registry.py anchor <transcript> [line]
      stdout: {"line": L, "uuid": U}: the last entry at or before [line] (default: end of file) that has an
      anchor. Anchor = the entry's "uuid"; if the format has no uuid, "h:" + sha256 of its message text.
  harvest-registry.py set-end <registry.json> <transcript>
      Record the end point of a capture: until_line / until_uuid = the anchor of the current end of file.
  harvest-registry.py register <session_id> <ledger>
      Register a new ledger for a session: writes $HARVEST_HOME/<session_id>.json = {"ledger": <abs path>}
      (HARVEST_HOME defaults to ~/.claude/ledger-harvest, as in ledger-harvest.sh). Creates nothing else.
      No entry: creates it. Same ledger already registered: no change. A different ledger already registered:
      refuses (exit 1) and overwrites nothing; moving a live session to a next ledger is `start-next`.
      An empty <session_id> (a Bob session has no CLAUDE_CODE_SESSION_ID) exits 0 and says "not registered".
  harvest-registry.py status <session_id>
      Read-only report on one session's harvest (HARVEST_HOME as for register): key: value lines.
      Keys: registered, ledger, raw_cursor_tl (last "harvest tl A-B" B in the raw file), raw_entries, curated_cursor
      (last "curated raw-line A-B" B), pending_raw_entries (raw entries after the curated cursor), until_line,
      until_uuid, harvest_end (yes/no/n-a: the harvest-end header for until_line is in the ledger), lock_held,
      again_pending (a request waits for the lock holder), failed_files (count of failed/<session_id>-* files),
      newest_failure, stalled.
      stalled = yes when the newest failed/ file is newer than the last progress (the ledger or the raw file,
      whichever changed last), or when until_line is set, harvest_end is no, no run holds the lock and
      again_pending is no. Exit code: 0 = not stalled, 3 = stalled, 1 = not registered.
  harvest-registry.py close <session_id> [--wait <seconds>] [--force]
      --force: ignore the per-chunk try counter for this run (HARVEST_FORCE=1). Without it, a chunk whose Bob call
      failed HARVEST_MAX_TRIES (default 3) times is skipped with a [harvest-skipped] entry. `status` shows the
      counters (`tries`) and the number of skipped chunks.
      Close a session's harvest at an end point (wind-down). Finds the session's transcript under
      $HARVEST_PROJECTS (default ~/.claude/projects), records the end point (until_line / until_uuid = the
      anchor of the current end of the transcript), starts the harvester with a SessionEnd event (detached, through
      harvest-hook.sh) and, with --wait, waits for the `harvest-end` header in the ledger.
      Exit codes: 0 = end point recorded (with --wait: the header is in the ledger), 1 = not registered,
      2 = no transcript or no anchor, 3 = failed (a new failed/ file, or the harvester is not running and the
      header is missing after 15 s), 4 = timed out.
  harvest-registry.py reopen <session_id>
      After a checkpoint (the session continues): clear the end point so the harvester carries on in the same
      ledger. Refuses (exit 1) unless an end point is set and its `harvest-end` header is in the ledger.
  harvest-registry.py start-next <registry.json> <new-ledger>
      Checkpoint: point the registry at the next ledger, which continues after the end point:
      from_line = until_line + 1, after_uuid = until_uuid; until_line / until_uuid are cleared.

Registry fields: ledger, from_line, after_uuid, until_line, until_uuid (all but ledger optional).
"""
import fcntl
import glob
import hashlib
import json
import os
import re
import subprocess
import sys
import time

CARRIES = ("user", "assistant", "system", "attachment")


def key_of(e):
    if e.get("uuid"):
        return e["uuid"]
    if e.get("type") in ("user", "assistant"):
        text = json.dumps(e.get("message"), sort_keys=True, ensure_ascii=False)
        return "h:" + hashlib.sha256(text.encode("utf-8")).hexdigest()
    return None


def entries(tp):
    with open(tp, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            try:
                e = json.loads(line)
            except ValueError:
                continue
            if isinstance(e, dict) and e.get("type") in CARRIES:
                k = key_of(e)
                if k:
                    yield n, k


def anchor(tp, line=None):
    best = None
    for n, k in entries(tp):
        if line is not None and n > line:
            break
        best = (n, k)
    return best


def resolve(tp, line, uuid):
    found = None
    for n, k in entries(tp):
        if k == uuid:
            if n == line:
                return n, False
            found = n if found is None else found
    return (found, True) if found is not None else (None, False)


def write_json(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f)
        f.write("\n")
    os.replace(tmp, path)


def last_end(path, rx):
    """The last number captured by rx (group 1) over the lines of path; 0 if none or no file."""
    last = 0
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                m = re.match(rx, line)
                if m:
                    last = int(m.group(1))
    except OSError:
        pass
    return last


def lock_held(path):
    try:
        fd = os.open(path, os.O_RDWR)
    except OSError:
        return False
    try:
        fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fcntl.flock(fd, fcntl.LOCK_UN)
        return False
    except OSError:
        return True
    finally:
        os.close(fd)


def mtime(path):
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


def status(sid):
    home = os.environ.get("HARVEST_HOME") or os.path.expanduser("~/.claude/ledger-harvest")
    reg = os.path.join(home, sid + ".json")
    if not os.path.exists(reg):
        print("registered: no")
        return 1
    r = json.load(open(reg, encoding="utf-8"))
    ledger = r.get("ledger", "")
    raw = os.path.join(home, sid + ".raw.md")
    until = int(r.get("until_line") or 0)
    raw_cursor = last_end(raw, r"<!-- harvest tl \d+-(\d+)")
    cur = last_end(ledger, r"<!-- curated raw-line \d+-(\d+)")
    entries = 0
    pending = 0
    try:
        with open(raw, encoding="utf-8") as f:
            for n, line in enumerate(f, 1):
                if line.startswith("- ["):
                    entries += 1
                    if n > cur:
                        pending += 1
    except OSError:
        pass
    end = "n-a"
    if until:
        end = "no"
        try:
            if re.search(r"^<!-- harvest-end line %d " % until, open(ledger, encoding="utf-8").read(), re.M):
                end = "yes"
        except OSError:
            pass
    held = lock_held(os.path.join(home, sid + ".lock"))
    again = os.path.exists(os.path.join(home, sid + ".again"))
    fails = glob.glob(os.path.join(home, "failed", sid + "-*"))
    newest = max((mtime(p) for p in fails), default=0.0)
    progress = max(mtime(ledger), mtime(raw))
    stalled = (newest > progress) or (until and end == "no" and not held and not again)
    tries = r.get("tries") or {}
    marks = set()                      # a pass-1 marker is in the raw file and, once curated, in the ledger
    for p in (raw, ledger):
        try:
            marks.update(ln.split("] ", 1)[-1].strip() for ln in open(p, encoding="utf-8") if "[harvest-skipped]" in ln)
        except OSError:
            pass
    skipped = len(marks)
    fmt = lambda t: time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(t)) if t else "-"
    for k, v in (("registered", "yes"), ("ledger", ledger), ("raw_cursor_tl", raw_cursor), ("raw_entries", entries),
                 ("curated_cursor", cur), ("pending_raw_entries", pending), ("until_line", until or "-"),
                 ("until_uuid", r.get("until_uuid", "-")), ("harvest_end", end),
                 ("lock_held", "yes" if held else "no"), ("again_pending", "yes" if again else "no"),
                 ("failed_files", len(fails)), ("newest_failure", fmt(newest)),
                 ("tries", ", ".join("%s=%s" % kv for kv in sorted(tries.items())) or "-"),
                 ("skipped_chunks", skipped),
                 ("stalled", "yes" if stalled else "no")):
        print("%s: %s" % (k, v))
    return 3 if stalled else 0


def harvest_home():
    return os.environ.get("HARVEST_HOME") or os.path.expanduser("~/.claude/ledger-harvest")


def find_transcript(sid):
    root = os.environ.get("HARVEST_PROJECTS") or os.path.expanduser("~/.claude/projects")
    found = sorted(glob.glob(os.path.join(root, "*", sid + ".jsonl")))
    return found[0] if found else None


def has_end_header(ledger, until):
    try:
        with open(ledger, encoding="utf-8") as f:
            return re.search(r"^<!-- harvest-end line %d " % until, f.read(), re.M) is not None
    except OSError:
        return False


def close(sid, wait, force=False):
    home = harvest_home()
    path = os.path.join(home, sid + ".json")
    if not os.path.exists(path):
        print("registered: no")
        return 1
    tp = find_transcript(sid)
    a = anchor(tp) if tp else None
    if not a:
        print("no transcript or no anchored entry for session %s" % sid, file=sys.stderr)
        return 2
    reg = json.load(open(path, encoding="utf-8"))
    reg["until_line"], reg["until_uuid"] = a
    write_json(path, reg)
    started = time.time()
    hook = os.path.join(os.path.dirname(os.path.abspath(__file__)), "harvest-hook.sh")
    payload = json.dumps({"session_id": sid, "transcript_path": tp, "hook_event_name": "SessionEnd", "reason": "other"})
    env = dict(os.environ)
    if force:
        env["HARVEST_FORCE"] = "1"      # ignore the per-chunk try counter for this run
    subprocess.run([hook], input=payload.encode("utf-8"), check=False, env=env)
    print("end point: line %d (%s)" % a)
    if not wait:
        return 0
    ledger = reg.get("ledger", "")
    while True:
        time.sleep(2)
        if has_end_header(ledger, a[0]):
            print("harvest end reached")
            return 0
        if any(mtime(p) > started for p in glob.glob(os.path.join(home, "failed", sid + "-*"))):
            print("failure: a new file in %s" % os.path.join(home, "failed"))
            return 3
        idle = not lock_held(os.path.join(home, sid + ".lock")) and not os.path.exists(os.path.join(home, sid + ".again"))
        if idle and time.time() - started > 15:
            print("the harvester is not running and the harvest-end header is missing")
            return 3
        if time.time() - started > wait:
            print("timed out after %d s" % wait)
            return 4


def reopen(sid):
    path = os.path.join(harvest_home(), sid + ".json")
    if not os.path.exists(path):
        print("registered: no")
        return 1
    reg = json.load(open(path, encoding="utf-8"))
    until = int(reg.get("until_line") or 0)
    if not until or not has_end_header(reg.get("ledger", ""), until):
        print("no end point with a harvest-end header: not reopened", file=sys.stderr)
        return 1
    reg.pop("until_line", None)
    reg.pop("until_uuid", None)
    write_json(path, reg)
    print("reopened: the harvester carries on in %s" % reg.get("ledger"))
    return 0


def main(argv):
    cmd = argv[1]
    if cmd == "close":
        wait = int(argv[argv.index("--wait") + 1]) if "--wait" in argv else 0
        return close(argv[2], wait, "--force" in argv)
    if cmd == "reopen":
        return reopen(argv[2])
    if cmd == "status":
        return status(argv[2])
    if cmd == "resolve":
        n, moved = resolve(argv[2], int(argv[3]), argv[4])
        if n is None:
            print("anchor %s not found in %s" % (argv[4], argv[2]), file=sys.stderr)
            return 1
        if moved:
            print("anchor %s moved: line %s -> %d" % (argv[4], argv[3], n), file=sys.stderr)
        print(n)
        return 0
    if cmd == "anchor":
        a = anchor(argv[2], int(argv[3]) if len(argv) > 3 else None)
        if not a:
            print("no anchored entry", file=sys.stderr)
            return 1
        print(json.dumps({"line": a[0], "uuid": a[1]}))
        return 0
    if cmd == "set-end":
        reg = json.load(open(argv[2], encoding="utf-8"))
        a = anchor(argv[3])
        if not a:
            print("no anchored entry in %s" % argv[3], file=sys.stderr)
            return 1
        reg["until_line"], reg["until_uuid"] = a
        write_json(argv[2], reg)
        print(json.dumps({"until_line": a[0], "until_uuid": a[1]}))
        return 0
    if cmd == "register":
        sid, ledger = argv[2], os.path.abspath(argv[3])
        if not sid:
            print("no session id (not a Claude session?): not registered")
            return 0
        if not os.path.isfile(ledger):
            print("ledger file does not exist: %s" % ledger, file=sys.stderr)
            return 1
        home = os.environ.get("HARVEST_HOME") or os.path.expanduser("~/.claude/ledger-harvest")
        os.makedirs(home, exist_ok=True)
        path = os.path.join(home, sid + ".json")
        if os.path.exists(path):
            cur = json.load(open(path, encoding="utf-8")).get("ledger")
            if cur == ledger:
                print("already registered: %s" % path)
                return 0
            print("session %s is already registered for another ledger (%s); not overwritten" % (sid, cur),
                  file=sys.stderr)
            return 1
        write_json(path, {"ledger": ledger})
        print("registered %s -> %s" % (path, ledger))
        return 0
    if cmd == "start-next":
        reg = json.load(open(argv[2], encoding="utf-8"))
        if not reg.get("until_line") or not reg.get("until_uuid"):
            print("registry has no end point; run set-end first", file=sys.stderr)
            return 1
        reg["ledger"] = argv[3]
        reg["from_line"] = int(reg.pop("until_line")) + 1
        reg["after_uuid"] = reg.pop("until_uuid")
        write_json(argv[2], reg)
        print(json.dumps(reg))
        return 0
    print(__doc__, file=sys.stderr)
    return 2


sys.exit(main(sys.argv))
