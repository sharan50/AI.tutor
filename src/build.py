#!/usr/bin/env python3
"""Assemble /docs HTML pages from content fragments in /src/content.

No dependencies, no build tooling. Run `python3 src/build.py` from the repo
root after editing any fragment.
"""
from pathlib import Path
import datetime

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "src" / "content"
DOCS = ROOT / "docs"

REVISED = "September 2026"

# (slug, number, title, one-line contents description, status)
PAGES = [
    ("00-thesis", "00", "Thesis",
     "What changed since the 2025 submission, and what the venture is for now.", "done"),
    ("01-product", "01", "Product",
     "The learner, the session, what is promised and what is not.", "done"),
    ("02-style-engine", "02", "Style engine",
     "How teaching style is represented, chosen, adjusted and verified.", "done"),
    ("03-curriculum-and-content", "03", "Curriculum and content",
     "Clean-room item bank, examiner validation, the accuracy floor.", "done"),
    ("04-rights-dossier", "04", "Rights dossier",
     "Exam boards, creators, the licence, and the enforcement war-game.", "done"),
    ("05-safety-privacy-regulatory", "05", "Safety, privacy, regulatory",
     "Age assurance, the child data model, Children's code, OSA scoping.", "done"),
    ("06-architecture", "06", "Architecture",
     "Models, retrieval, data model, kill switch, evaluation harness.", "partial"),
    ("07-route-a-direct-to-parents", "07", "Route A: direct to parents",
     "Pricing, consent model, distribution, compliance posture.", "partial"),
    ("08-route-b-through-schools", "08", "Route B: through schools",
     "Pricing, consent model, distribution, compliance posture.", "partial"),
    ("09-route-comparison", "09", "Route comparison",
     "The document used to choose, with the case for the route not recommended.", "done"),
    ("10-economics", "10", "Economics",
     "Cost per session, price points, the dominant sensitivity.", "todo"),
    ("11-roadmap", "11", "Roadmap",
     "Milestones defined by evidence obtained, not features shipped.", "todo"),
    ("12-risk-register", "12", "Risk register",
     "Ordered by the owner's ranking, with the one place it is not followed.", "partial"),
    ("13-open-items", "13", "Open items",
     "Unverified assumptions and questions for counsel, with what each unblocks.", "done"),
    ("decision-ledger", "", "Decision ledger",
     "Every decision: what was chosen, what was rejected, what it forecloses.", "done"),
]

SHELL = """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}, AI.tutor design vault</title>
<meta name="description" content="{desc}">
<link rel="stylesheet" href="style.css">
</head>
<body>
<main class="sheet">
<header class="masthead">
  <span class="doc-no">{number}</span>
  <span class="repo">AI.tutor design vault, revised {revised}</span>
  <a href="index.html">Contents</a>
</header>
{body}
<footer class="pagefoot">
  <a href="{prev_href}">{prev_label}</a>
  <span class="stamp">Built {built}</span>
  <a href="{next_href}">{next_label}</a>
</footer>
</main>
</body>
</html>
"""


def build():
    built = datetime.date.today().strftime("%d %B %Y")
    DOCS.mkdir(exist_ok=True)
    for i, (slug, number, title, desc, _status) in enumerate(PAGES):
        frag = CONTENT / f"{slug}.html"
        if not frag.exists():
            print(f"  missing fragment: {slug}")
            continue
        prev_i, next_i = i - 1, i + 1
        prev_href = "index.html" if prev_i < 0 else PAGES[prev_i][0] + ".html"
        prev_label = "Contents" if prev_i < 0 else PAGES[prev_i][2]
        next_href = "index.html" if next_i >= len(PAGES) else PAGES[next_i][0] + ".html"
        next_label = "Contents" if next_i >= len(PAGES) else PAGES[next_i][2]
        html = SHELL.format(
            title=title, desc=desc, number=number, revised=REVISED,
            body=frag.read_text(encoding="utf-8").strip(), built=built,
            prev_href=prev_href, prev_label=prev_label,
            next_href=next_href, next_label=next_label,
        )
        (DOCS / f"{slug}.html").write_text(html, encoding="utf-8")
        print(f"  built {slug}.html")

    index_frag = CONTENT / "index.html"
    rows = []
    for slug, number, title, desc, status in PAGES:
        label = {"done": "drafted", "partial": "outline", "todo": "not written"}[status]
        rows.append(
            f'  <li><span class="n">{number}</span>'
            f'<span class="t"><a href="{slug}.html">{title}</a><span>{desc}</span></span>'
            f'<span class="s {status}">{label}</span></li>'
        )
    index_html = SHELL.format(
        title="Contents", desc="AI.tutor venture design vault", number="\u2014",
        revised=REVISED,
        body=index_frag.read_text(encoding="utf-8").replace("<!--CONTENTS-->", "\n".join(rows)).strip(),
        built=built,
        prev_href="00-thesis.html", prev_label="Thesis",
        next_href="00-thesis.html", next_label="Thesis",
    )
    (DOCS / "index.html").write_text(index_html, encoding="utf-8")
    print("  built index.html")


if __name__ == "__main__":
    build()

