#!/usr/bin/env python3
"""One-off: split src/content/<slug>.html into src/content/<slug>/ at its
top-level <h2> headings, cutting at line boundaries, so that concatenating
the fragments in filename order reproduces the original byte for byte.

    python3 tools/split_fragment.py <slug>

000-head.html holds everything before the first <h2>; NNN-<h2 id>.html holds
each section; 999-foot.html would hold anything after the last section and is
written only if there is any. The original file is removed once the
round-trip has been proved.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "src" / "content"
BLOCK = re.compile(r"<(div|section|table|dl|ul|ol|blockquote|figure|details)\b")
UNBLOCK = re.compile(r"</(div|section|table|dl|ul|ol|blockquote|figure|details)>")


def split(slug):
    src = CONTENT / f"{slug}.html"
    original = src.read_text(encoding="utf-8")
    lines = original.splitlines(keepends=True)
    cuts = []
    depth = 0
    for i, line in enumerate(lines):
        m = re.match(r'<h2 id="([^"]+)"', line)
        if m:
            if depth != 0:
                raise SystemExit(f"{src}:{i + 1} <h2> is nested (depth {depth}); not splitting")
            cuts.append((i, m.group(1)))
        depth += len(BLOCK.findall(line)) - len(UNBLOCK.findall(line))
    if not cuts:
        raise SystemExit(f"{src}: no <h2 id> headings; nothing to split")
    pieces = [("000-head.html", lines[:cuts[0][0]])]
    for n, (start, hid) in enumerate(cuts):
        end = cuts[n + 1][0] if n + 1 < len(cuts) else len(lines)
        pieces.append((f"{(n + 1) * 10:03d}-{hid}.html", lines[start:end]))
    folder = CONTENT / slug
    folder.mkdir()
    for name, chunk in pieces:
        if chunk:
            (folder / name).write_text("".join(chunk), encoding="utf-8")
    rebuilt = "".join(p.read_text(encoding="utf-8")
                      for p in sorted(folder.iterdir()) if p.suffix == ".html")
    if rebuilt != original:
        raise SystemExit(f"{slug}: round trip failed; original left in place")
    src.unlink()
    for name, chunk in pieces:
        if chunk:
            print(f"  {folder.relative_to(ROOT)}/{name}: {len(chunk)} lines")


if __name__ == "__main__":
    for s in sys.argv[1:]:
        split(s)
