#!/bin/bash
# SessionStart hook: in a cloud session, install the project's dependencies.
[ "$CLAUDE_CODE_REMOTE" = "true" ] || exit 0
cd "$CLAUDE_PROJECT_DIR" || exit 0
[ -f pyproject.toml ] && command -v uv >/dev/null && uv sync --quiet
exit 0
