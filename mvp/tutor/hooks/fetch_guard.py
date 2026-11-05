#!/usr/bin/env python3
"""PreToolUse hook for WebFetch: refuse an exam board's site, at any subdomain, and
any address that looks like a past paper, a mark scheme or a specification."""
from __future__ import annotations

import json
import re
import sys
from urllib.parse import unquote, urlparse

BOARDS = ["aqa.org.uk", "pearson.com", "edexcel.com", "ocr.org.uk", "wjec.co.uk",
          "eduqas.co.uk", "ccea.org.uk", "sqa.org.uk", "cambridgeinternational.org",
          "cambridgeassessment.org.uk"]
MIRRORS = ["physicsandmathstutor.com", "savemyexams.com", "mathsgenie.co.uk",
           "mathsmadeeasy.co.uk", "onmaths.com"]
NAME = r"(?<![a-z0-9])(?:aqa|edexcel|wjec|eduqas|8300|8365|9ma0)(?![a-z0-9])"
WORDS = r"past[-_ ]?papers?|mark[-_ ]?schemes?|question[-_ ]?papers?" \
        r"|examiners?[-_ ]?reports?|specimen[-_ ]?papers?|" + NAME


def main() -> int:
    data = json.load(sys.stdin)
    url = str(data.get("tool_input", {}).get("url", ""))
    host = (urlparse(url).hostname or "").lower().rstrip(".")
    for domain in BOARDS + MIRRORS:
        if host == domain or host.endswith("." + domain):
            return refuse(f"{host} is an exam board's site or a copy of its papers.")
    if re.search(WORDS, unquote(url), re.I):
        return refuse("This address looks like a board's past paper, mark scheme or "
                      "specification.")
    return 0


def refuse(reason: str) -> int:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": reason + " No board material may reach any agent "
        "(CLAUDE.md, invariant 12)."}}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
