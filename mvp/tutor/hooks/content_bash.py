#!/usr/bin/env python3
"""PreToolUse hook for Bash, set in the content author's own definition: it may run
the content checks and git, and nothing else, so that it has no way to the network."""
from __future__ import annotations

import json
import re
import sys

ALLOWED = ["uv run python -m tutor.content.check", "make check-content", "git status",
           "git diff", "git log", "git add", "git commit", "git show", "ls", "wc"]


def main() -> int:
    data = json.load(sys.stdin)
    command = str(data.get("tool_input", {}).get("command", "")).strip()
    plain = not re.search(r"[;&|`<>]|\$\(", command)
    if plain and any(command == a or command.startswith(a + " ") for a in ALLOWED):
        return 0
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "The content author may run only the content "
        "checks, git and ls or wc, one command at a time."}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
