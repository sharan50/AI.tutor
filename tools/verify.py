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
  5. the views: every section has one owner; every ledger entry has an
     owner; every referenced key block exists and is transcluded verbatim; no
     digit on the front door sits outside a key block, a computed count or a
     transcluded register line; the front door is under 1,200 words and every
     frame under its cap with no figure; no Verified marker on a generated
     page; CODEOWNERS is what the build would write; the four reader routes
     are on contents.html.
"""
import re
import subprocess
import sys
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE_DIRS = ["docs", "evidence", "viz"]
sys.path.insert(0, str(ROOT / "src"))
import build  # noqa: E402

READER_ROUTES = ("A UK media lawyer", "The first creator you want to sign", "An investor",
                 "A curriculum specialist or examiner")


class DigitOutsideData(HTMLParser):
    """Text inside <main> that carries a digit and sits in no element marked
    data-key, data-count or data-from."""
    def __init__(self):
        super().__init__()
        self.stack, self.shield, self.in_main, self.hits = [], 0, False, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        shielded = any(k in a for k in ("data-key", "data-count", "data-from"))
        if tag == "main":
            self.in_main = True
        self.stack.append((tag, shielded))
        if shielded:
            self.shield += 1

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                self.shield -= sum(1 for _t, sh in self.stack[i:] if sh)
                del self.stack[i:]
                break
        if tag == "main":
            self.in_main = False

    def handle_data(self, data):
        if self.in_main and self.shield == 0 and re.search(r"\d", data):
            self.hits.append((self.getpos()[0], re.sub(r"\s+", " ", data).strip()[:70]))


def main_text(path):
    m = re.search(r'<main class="sheet" id="doc">(.*?)</main>', path.read_text(encoding="utf-8"), re.S)
    return build._plain(m.group(1)) if m else ""


def check_views():
    problems = []
    cfg = build.load_roles()
    roles = cfg["roles"]
    for slug in build.written_slugs():
        for hid, _t, _h in build.page_sections(slug):
            if hid is None:
                continue
            owners = ([r["id"] for r in roles if f"{slug}#{hid}" in r["owns"]]
                      or [r["id"] for r in roles if slug in r["owns"]])
            if len(owners) != 1:
                problems.append(f"roles.json:1 {slug}#{hid} has {len(owners)} owners: {', '.join(owners) or 'none'}")
    for e in build.ledger_entries():
        if build.decision_owner(e) is None:
            problems.append(f"roles.json:1 ledger entry {e['id']} has no owner")
    blocks = build.key_blocks()
    for k in [cfg["summary"]["route"]] + list(cfg["summary"]["keys"]):
        if k not in blocks:
            problems.append(f"roles.json:1 key block {k} is not marked in any fragment")
    generated = [build.DOCS / "index.html"] + sorted((build.DOCS / "roles").glob("*.html"))
    for f in generated:
        if not f.exists():
            problems.append(f"{f.relative_to(ROOT)}:1 missing; run python3 src/build.py")
            continue
        text, rel = f.read_text(encoding="utf-8"), f.relative_to(ROOT)
        for m in re.finditer(r'<[a-z0-9]+[^>]*\sdata-key="([^"]+)"', text):
            key, line = m.group(1), text[:m.start()].count("\n") + 1
            if key not in blocks:
                problems.append(f"{rel}:{line} key block {key} is not in the fragments")
                continue
            want = build.rebase_links(blocks[key]["html"], blocks[key]["slug"], f.parent)
            if build.extract_element(text, m.start()) != want:
                problems.append(f"{rel}:{line} key block {key} is not transcluded verbatim")
        for m in re.finditer(r'data-key-missing="([^"]+)"', text):
            problems.append(f"{rel}:{text[:m.start()].count(chr(10)) + 1} key block {m.group(1)} is missing")
        main = re.search(r'<main class="sheet" id="doc">(.*?)</main>', text, re.S)
        if main and 'class="mark verified"' in main.group(1):
            line = text[:text.find('class="mark verified"', main.start())].count("\n") + 1
            problems.append(f"{rel}:{line} a Verified marker on a generated page")
    front = build.DOCS / "index.html"
    if front.exists():
        p = DigitOutsideData()
        p.feed(front.read_text(encoding="utf-8"))
        for line, snippet in p.hits:
            problems.append(f"docs/index.html:{line} digit outside a key block or computed count: {snippet}")
        n = len(main_text(front).split())
        if n > build.FRONT_DOOR_WORDS:
            problems.append(f"docs/index.html:1 front door is {n} words, over {build.FRONT_DOOR_WORDS}")
        template = build.TEMPLATES / "summary.html"
        frame = build._plain(template.read_text(encoding="utf-8").split("<h2", 1)[0])
        if len(frame.split()) > 150:
            problems.append(f"src/templates/summary.html:1 frame is {len(frame.split())} words, over 150")
        if re.search(r"\d", frame):
            problems.append("src/templates/summary.html:1 frame carries a figure")
        if "has been built" not in frame and "been built" not in frame:
            problems.append("src/templates/summary.html:1 frame does not carry the line that nothing has been built")
    for r in roles:
        words = len(r["frame"].split())
        if words > 200:
            problems.append(f"roles.json:1 frame of {r['id']} is {words} words, over 200")
        if re.search(r"\d", r["frame"]):
            problems.append(f"roles.json:1 frame of {r['id']} carries a figure")
    if build.CODEOWNERS.exists():
        if build.CODEOWNERS.read_text(encoding="utf-8") != build.render_codeowners(cfg):
            problems.append(".github/CODEOWNERS:1 stale; differs from what the build would write")
    else:
        problems.append(".github/CODEOWNERS:1 missing; run python3 src/build.py")
    contents = build.DOCS / "contents.html"
    if contents.exists():
        text = contents.read_text(encoding="utf-8")
        for route in READER_ROUTES:
            if f"<h4>{route}</h4>" not in text:
                problems.append(f"docs/contents.html:1 reader route missing: {route}")
    else:
        problems.append("docs/contents.html:1 missing")
    return problems


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

    print("5. the views: ownership, ledger owners, key blocks, the front door, frames, CODEOWNERS, reader routes")
    problems = check_views()
    for p in problems:
        print(p)
    print(f"   {len(problems)} problem(s)")
    failed += bool(problems)

    print("verify: FAIL" if failed else "verify: all checks pass")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
