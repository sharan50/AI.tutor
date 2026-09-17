#!/usr/bin/env python3
"""Verify the vault. Standard library only. Exits non-zero on any failure and
prints every failure as file:line message.

  1. build freshness: what a build would write matches docs/, evidence/ and viz/
  2. every internal link and anchor under docs/, evidence/ and viz/ resolves
  3. the dependency map: python3 tools/depmap.py check
  4. not run. A Verified marker is a bare <span class="mark verified"> that
     carries no reference to an entry in evidence/sources.html, and the
     register has no per-entry anchors, so "every Verified marker links a
     register entry" is not mechanical. Recorded in RESTRUCTURE_REPORT.md.
"""
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIRS = ["docs", "evidence", "viz"]


def run(script, *args):
    p = subprocess.run([sys.executable, str(ROOT / script), *args],
                       cwd=ROOT, capture_output=True, text=True)
    return p.returncode, (p.stdout + p.stderr).rstrip()


def check_links():
    """Every href and src under the served directories, resolved on disk."""
    problems, files, links = [], 0, 0
    for d in SITE_DIRS:
        for f in sorted((ROOT / d).rglob("*.html")):
            files += 1
            text = f.read_text(encoding="utf-8")
            rel = f.relative_to(ROOT)
            for m in re.finditer(r'(?:href|src)="([^"]*)"', text):
                target = m.group(1)
                if re.match(r"^(https?:|mailto:|data:|tel:)", target):
                    continue
                links += 1
                line = text[:m.start()].count("\n") + 1
                path, _, anchor = target.partition("#")
                if path == "":
                    dest = f
                else:
                    dest = (f.parent / path).resolve()
                    # The map is published at /map/ from viz/dependency-map.html.
                    if dest in ((ROOT / "map").resolve(), (ROOT / "map" / "index.html").resolve()):
                        dest = ROOT / "viz" / "dependency-map.html"
                    if dest.is_dir():
                        dest = dest / "index.html"
                if not dest.exists():
                    problems.append(f"{rel}:{line} broken link {target}")
                    continue
                if anchor:
                    if dest.suffix != ".html":
                        problems.append(f"{rel}:{line} anchor on a non-HTML target {target}")
                    elif f'id="{anchor}"' not in dest.read_text(encoding="utf-8"):
                        problems.append(f"{rel}:{line} missing anchor #{anchor} in {dest.relative_to(ROOT)}")
    return problems, files, links


def main():
    failed = 0

    print("1. build freshness")
    rc, out = run("src/build.py", "--check")
    print("   " + out.replace("\n", "\n   "))
    failed += rc != 0

    print("2. links and anchors")
    problems, files, links = check_links()
    for p in problems:
        print(p)
    print(f"   {links} links in {files} files, {len(problems)} broken")
    failed += bool(problems)

    print("3. dependency map")
    rc, out = run("tools/depmap.py", "check")
    print("   " + out.replace("\n", "\n   "))
    failed += rc != 0

    print("4. Verified markers link a register entry: not mechanical, not run (see the docstring)")

    print("verify: FAIL" if failed else "verify: all checks pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
