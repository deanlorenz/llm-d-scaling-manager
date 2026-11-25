---
name: conv-install-to-session-tracking
description: Use when installing conventions, skills, or CONVENTIONS.md from policy-writer onto the session-tracking branch.
---

# conv-install-to-session-tracking

`session-tracking` is the production branch of rules and skills. `policy-writer` is the working branch. An install moves reviewed, committed policy-writer commits into production. Nothing else goes.

**This skill runs as a subagent.** Installation is mechanical and self-contained — spawn a subagent to run the procedure. The subagent needs explicit authorization confirmation from you first.

## What is installed

- Production paths: `CONVENTIONS.md`, `conventions/`, `claude-skills/`, `bob/`. Nothing else is installed.
- Never installed: `backup_rules/`, `.session/`, `.claude/`, `*.bak`, or any other path.
- Ignore `claude-skills/pr-review` in every check below. It is an upstream skill, left untracked on `session-tracking`. Do not stage, move, or delete it.

## Caller instructions

1. Confirm you have explicit user authorization to install to `session-tracking`. For a new `session-tracking` that has no install commit yet, the authorization must say "first install" and you pass that to the subagent (see "First install").
2. Record the current `policy-writer` HEAD SHA (run in the policy-writer worktree):
   ```bash
   git rev-parse HEAD
   ```
3. Launch a subagent (`general-purpose`, `haiku`: the install is mechanical):
   ```
   Agent(
     description: "Install policy-writer commits",
     prompt: "<the Subagent instructions block below, with HEAD_SHA filled in, plus the In:/Out: channels and the subscription command>",
     subagent_type: "general-purpose",
     model: "haiku"
   )
   ```
   Assign `In:` `policy-writer.install-<n>.in` and `Out:` `policy-writer.install-<n>` (see `conv-agentbus`), and subscribe to `Out:` yourself.
4. Do not modify `policy-writer` files while the subagent is running.
5. After the subagent reports success, record the install in STATE and ledger.

---

## Subagent instructions

You are installing reviewed `policy-writer` commits onto the production branch `session-tracking`. Follow every step. Stop and report any failure immediately — do not improvise, resolve, or work around.

Set these once (full paths; `HEAD_SHA` is the SHA the caller recorded):

```bash
PW=<full path to policy-writer>
ST=<full path to session-tracking>
PATHS="CONVENTIONS.md conventions claude-skills bob"
```

Entering `$ST` with `cd` is permitted for this authorized operation. Use `$HEAD_SHA`, not the branch name, for the whole procedure.

Subscribe to your `In:` channel and stay subscribed. After each of Steps 1-6, publish `kind="heartbeat"` on `Out:`, body `session=<slug> step=<i>/7 <what you just did>`; send the Step 7 report on `Out:` too. Answer any request from `In:` on `Out:`.

### Step 1: Verify nothing uncommitted would be overwritten

In `$PW`: the production paths must have no uncommitted changes.

```bash
git status --short -- $PATHS
```

In `$ST`: the production paths must have no uncommitted or untracked changes, apart from `claude-skills/pr-review`.

```bash
git status --short -- $PATHS ':!claude-skills/pr-review'
```

Stop if either prints anything. Untracked files elsewhere in `$ST` (mission links, suggestion-box files) do not block the install and must not be touched.

### Step 2: Find the last install and check for divergence

```bash
git log --oneline --grep='^install:' -1
```

The install commit message contains `from policy-writer@<sha>`. Call that `LAST_SHA`. If there is none, stop, unless the caller's authorization says "first install" for a new `session-tracking`: then follow "First install" below instead of Steps 2-4.

`session-tracking` must still match what was last installed. From `$ST`:

```bash
git diff $LAST_SHA HEAD --stat -- $PATHS ':!claude-skills/pr-review'
```

(`$LAST_SHA` is a `policy-writer` commit; the diff compares its tree to the current `session-tracking` HEAD.)

**If the diff is non-empty:** `session-tracking` has content that was not installed from `policy-writer`. STOP. Report every differing file. Do not proceed until the caller resolves it on `policy-writer`.

### Step 3: Classify the commits to install

```bash
git log --reverse --no-merges --format=%h $LAST_SHA..$HEAD_SHA
```

For each commit, list its files:

```bash
git show --name-only --format= <sha>
```

Classify every commit:

- **All files are in the production paths:** install it.
- **No file is in the production paths** (for example, only `.session/` or `backup_rules/`): do not install it. List it as skipped.
- **Mixed:** STOP and report the commit and the files on each side. Do not split, edit, or drop files from it. The caller decides.

A commit that touches the production paths but sits at or before `LAST_SHA` is never in the range, so the range skips it (for example a commit held back earlier, or one whose path was added to the production paths later). The caller lists such commits as explicit picks in the prompt; cherry-pick them first, in order, under the same rules.

Report the install list and the skip list to the caller before continuing.

### Step 4: Cherry-pick, one commit at a time

Apply `conv-cherry-pick`. Only the commits classified "install", in order, from `$ST`:

```bash
git cherry-pick <sha>
```

If any pick conflicts or fails: run `git cherry-pick --abort`, stop, and report the commit and the conflicting files. Do not resolve conflicts. Do not `git checkout <branch> -- <path>`, hand-copy files, or delete files to make a pick apply.

### First install (a new `session-tracking` with no earlier install commit)

Only when the caller's authorization says "first install". It replaces Steps 2-4. Steps 1, 5, 6 and 7 apply, with the changes marked below. The result is one snapshot of the production paths at `$HEAD_SHA`; the individual `policy-writer` commits are not imported, so there is no classification and no cherry-pick.

Preconditions. Check all of them from `$ST`, and stop if any fails:

```bash
git log --oneline --grep='^install:' -1
git ls-files -- $PATHS
ls -d $PATHS 2>/dev/null
git ls-tree --name-only $HEAD_SHA -- $PATHS
```

The first three must print nothing (a branch with no commit yet gives an error for the first one: that is fine). The fourth must list at least `CONVENTIONS.md`, `conventions` and `claude-skills`. Anything else on `$ST` under the production paths is content with no known origin: stop and report it.

Copy the snapshot, from `$ST`:

```bash
git archive $HEAD_SHA -- $PATHS | tar -x -f -
git add -- $PATHS
git diff --cached --name-only
```

`git archive` writes only the files of that commit under those paths, and `tar` keeps their modes. Every name from the last command must be inside the production paths. Then compare the staged tree with the commit, one pair of plain commands per path (a tree id covers every file's content and mode); skip a pair if that path is not in the commit:

```bash
git rev-parse :CONVENTIONS.md
git rev-parse $HEAD_SHA:CONVENTIONS.md
git write-tree --prefix=conventions/
git rev-parse $HEAD_SHA:conventions
git write-tree --prefix=claude-skills/
git rev-parse $HEAD_SHA:claude-skills
git write-tree --prefix=bob/
git rev-parse $HEAD_SHA:bob
```

The two ids of each pair must be identical. In Step 5, skip the line `git diff --name-only <ST HEAD before step 4> HEAD` (there is no earlier HEAD); the rest of Step 5 applies. In Step 6, use this message instead (the commit is the root commit when the branch had none):

```bash
git commit -m "install: CONVENTIONS.md + conventions/ + claude-skills/ + bob/ from policy-writer@$HEAD_SHA (first install: snapshot of the tree)"
```

Later installs use Steps 1-7 as written: `LAST_SHA` is the `$HEAD_SHA` of this first install.

### Step 5: Verify

From `$ST`:

```bash
diff -r -x pr-review $PW/claude-skills claude-skills
diff -r $PW/conventions conventions
diff $PW/CONVENTIONS.md CONVENTIONS.md
diff -r $PW/bob bob
git diff --name-only <ST HEAD before step 4> HEAD
git ls-files | grep -E '(^backup_rules/|^\.session/|^\.claude/|\.bak$)' || echo none
grep -rohE 'conventions/[A-Za-z0-9_-]+\.md' CONVENTIONS.md conventions claude-skills --exclude-dir=archived | sort -u | while read f; do test -f "$f" || echo "MISSING $f"; done
```

The four `diff` commands must print nothing. Every name from `git diff --name-only` must be inside the production paths. The `git ls-files` command must print `none`. The last command (dangling references) must print nothing: every `conventions/<name>.md` cited in production must exist outside `conventions/archived/`. If anything else appears, stop and report.

### Step 6: Install commit

```bash
git commit --allow-empty -m "install: CONVENTIONS.md + conventions/ + claude-skills/ + bob/ from policy-writer@$HEAD_SHA"
```

Always record the exact `policy-writer` SHA used.

### Step 7: Report back

Return:
- Commits installed and commits skipped (with the reason)
- Any mixed commit, conflict, or divergence stopped on
- Diff result (clean / any unexpected differences)
- Install commit SHA on `session-tracking`
- Push: this skill does NOT push — the caller handles push authorization separately.
