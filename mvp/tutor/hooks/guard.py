#!/usr/bin/env python3
"""PreToolUse hook for Edit and Write: refuse to write anything that looks like an
API key, so that no secret reaches the repository."""
import json
import re
import sys

PATTERNS = [
    r"sk-ant-[A-Za-z0-9_\-]{20,}",   # Anthropic
    r"AIza[0-9A-Za-z_\-]{35}",        # Google
    r"\bak-[A-Za-z0-9]{20,}",         # Modal token id
    r"\bas-[A-Za-z0-9]{20,}",         # Modal token secret
    r"postgres(?:ql)?://[^\s:@/]+:[^\s@/]+@",  # a database URL with a password
]


def main() -> int:
    data = json.load(sys.stdin)
    ti = data.get("tool_input", {})
    text = "\n".join(str(ti.get(k, "")) for k in ("content", "new_string"))
    for pattern in PATTERNS:
        if re.search(pattern, text):
            print(json.dumps({"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "This looks like a secret. Secrets live in "
                "Modal secrets, never in the repository."}}))
            return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
