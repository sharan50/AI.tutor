#!/usr/bin/env python3
"""PostToolUse hook for Edit and Write: lint the file just changed, and run the
content checks on an item file. Reports a failure back to Claude as a block."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], cwd: Path) -> str | None:
    p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)
    return None if p.returncode == 0 else (p.stdout + p.stderr).strip()


def main() -> int:
    data = json.load(sys.stdin)
    path = Path(data.get("tool_input", {}).get("file_path", ""))
    if not path.is_file() or shutil.which("uv") is None:
        return 0
    top = subprocess.run(["git", "rev-parse", "--show-toplevel"], cwd=path.parent,
                         capture_output=True, text=True)
    if top.returncode != 0 or not (Path(top.stdout.strip()) / "pyproject.toml").exists():
        return 0  # the harness is not built yet
    root = Path(top.stdout.strip())

    problems = []
    if path.suffix == ".py":
        for cmd in (["uv", "run", "ruff", "check", str(path)],
                    ["uv", "run", "ruff", "format", "--check", str(path)]):
            out = run(cmd, root)
            if out:
                problems.append(out)
    rel = path.resolve().relative_to(root.resolve())
    if rel.parts[:2] == ("content", "items"):
        out = run(["uv", "run", "python", "-m", "tutor.content.check", str(path)], root)
        if out:
            problems.append(out)

    if problems:
        reason = f"Checks fail on {rel}:\n" + "\n".join(problems)[-3000:]
        print(json.dumps({"decision": "block", "reason": reason}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
