#!/usr/bin/env python3
"""PreToolUse hook for Edit, Write and Bash: refuse anything that would put a secret
in the repository, and any command that would skip or switch off the git hooks."""
from __future__ import annotations

import json
import re
import sys

SECRETS = [
    r"sk-ant-[A-Za-z0-9_\-]{20,}",   # Anthropic
    r"AIza[0-9A-Za-z_\-]{35}",        # Google
    r"\bak-[A-Za-z0-9]{20,}",         # Modal token id
    r"\bas-[A-Za-z0-9]{20,}",         # Modal token secret
    # a database URL with a password, unless it points at this machine
    r"postgres(?:ql)?://[^\s:@/]+:[^\s@/]+@(?!localhost\b|127\.0\.0\.1\b)",
]
GIT_BYPASS = [r"--no-verify", r"-c\s+core\.hooksPath",
              r"config\s+(?:--\S+\s+)*core\.hooksPath\s+\S", r"--unset\S*\s+core\.hooksPath",
              r"config\s+(?:--\S+\s+)*merge\.ff\s+\S", r"--unset\S*\s+merge\.ff"]


def deny(reason: str) -> int:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason}}))
    return 0


def main() -> int:
    data = json.load(sys.stdin)
    ti = data.get("tool_input", {})
    text = "\n".join(str(ti.get(k, "")) for k in ("content", "new_string", "command"))
    for pattern in SECRETS:
        if re.search(pattern, text):
            return deny("This looks like a secret. Secrets live in Modal secrets, "
                        "never in the repository, a command line or a log.")
    if data.get("tool_name") == "Bash":
        for pattern in GIT_BYPASS:
            if re.search(pattern, str(ti.get("command", ""))):
                return deny("The git hooks guard every merge. Do not skip them or "
                            "change how they run; ask the owner.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
