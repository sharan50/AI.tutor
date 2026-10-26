#!/usr/bin/env python3
"""Stop and SubagentStop hook: refuse to finish while `make test` fails.

Runs in the checkout the stopping session works in, which for a subagent is its own
worktree. After five refusals in one session it lets the session stop, so that a
stuck agent does not run on; the reviewer and CI still refuse the merge.
"""
import json
import os
import subprocess
import sys
from pathlib import Path

MAX_REFUSALS = 5


def repo_root(start: Path) -> Path | None:
    p = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=start,
                       capture_output=True, text=True)
    return Path(p.stdout.strip()) if p.returncode == 0 else None


def main() -> int:
    data = json.load(sys.stdin)
    start = Path(data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR", "."))
    root = repo_root(start)
    if root is None or not (root / "Makefile").exists():
        return 0  # the harness is not built yet

    git_dir = subprocess.run(["git", "rev-parse", "--git-dir"], cwd=root,
                             capture_output=True, text=True).stdout.strip()
    state = (root / git_dir / "claude-stop-refusals").resolve()  # per worktree
    session = data.get("session_id", "unknown")
    counts = json.loads(state.read_text()) if state.exists() else {}

    run = subprocess.run(["make", "test"], cwd=root, capture_output=True, text=True)
    if run.returncode == 0:
        counts.pop(session, None)
        state.write_text(json.dumps(counts))
        return 0

    counts[session] = counts.get(session, 0) + 1
    if counts[session] > MAX_REFUSALS:
        counts.pop(session)  # let this stop through; the next one is guarded again
        state.write_text(json.dumps(counts))
        return 0
    state.write_text(json.dumps(counts))
    tail = "\n".join((run.stdout + run.stderr).splitlines()[-30:])
    print(f"make test fails in {root}. Fix it before you finish; never skip or "
          f"weaken a test. If you cannot, say so in your report.\n{tail}",
          file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
