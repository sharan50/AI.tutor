#!/usr/bin/env python3
"""Stop and SubagentStop hook: refuse to finish while `make test` fails.

`make test` runs the unit tests and the tests of finished phases, so it should pass
at every stop. The hook runs in the checkout the stopping session works in, which
for a builder is its own worktree. It refuses five times in a row; the sixth time it
lets the session stop, so that a stuck agent does not run on, and the agent must say
in its report that the tests fail. The git hook still refuses to merge its work.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

MAX_REFUSALS = 5


def git(args: list[str], cwd: Path) -> str | None:
    p = subprocess.run(["git", *args], cwd=cwd, capture_output=True, text=True)
    return p.stdout.strip() if p.returncode == 0 else None


def main() -> int:
    data = json.load(sys.stdin)
    if data.get("agent_type") == "reviewer":
        return 0  # the reviewer changes nothing
    start = Path(data.get("cwd") or os.environ.get("CLAUDE_PROJECT_DIR", "."))
    top = git(["rev-parse", "--show-toplevel"], start)
    if top is None or not (Path(top) / "Makefile").exists():
        return 0  # the harness is not built yet
    root = Path(top)

    state = (root / git(["rev-parse", "--git-dir"], root) / "claude-stop-refusals").resolve()
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
    print(f"make test fails in {root} (refusal {counts[session]} of {MAX_REFUSALS}). "
          "Fix it before you finish; never skip or weaken a test. If you cannot, "
          f"say so plainly in your report.\n{tail}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
