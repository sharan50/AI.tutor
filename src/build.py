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
     "What the 2025 differentiation lost, and why a parent pays when Gemini is free.", "done"),
    ("01-product", "01", "Product",
     "The learner, the session, the four promises, and one topic taught twice.", "done"),
    ("02-style-engine", "02", "Style engine",
     "Twelve dimensions, the rating protocol, conformance tests, the D6 seam.", "done"),
    ("03-curriculum-and-content", "03", "Curriculum and content",
     "Clean-room item bank, examiner validation, the accuracy floor as a number.", "done"),
    ("04-rights-dossier", "04", "Rights dossier",
     "Exam boards, the creator licence, the kill switch, the enforcement war-game.", "done"),
    ("05-safety-privacy-regulatory", "05", "Safety, privacy and regulatory",
     "Age assurance, the child data model, Children's code, the OSA trigger list.", "done"),
    ("06-architecture", "06", "Architecture",
     "The turn pipeline, the verifier, kill switch mechanics, cost per session.", "done"),
    ("07-route-a-direct-to-parents", "07", "Route A: direct to parents",
     "Pricing, consent, distribution, compliance, and the June cliff.", "done"),
    ("08-route-b-through-schools", "08", "Route B: through schools",
     "The same four, into a market that cut its tutoring offer last year.", "done"),
    ("09-route-comparison", "09", "Route comparison",
     "The document used to choose, with the case for the route not recommended.", "done"),
    ("10-economics", "10", "Economics",
     "Cost from the architecture, and the dominant variable derived not assumed.", "done"),
    ("11-roadmap", "11", "Roadmap",
     "Milestones defined by evidence obtained, plus the D14 and D6 decision rules.", "done"),
    ("12-risk-register", "12", "Risk register",
     "The owner's ranking, and why engineering priority runs close to its reverse.", "done"),
    ("13-primer-gateway", "13", "Primer gateway",
     "A gated path from trusted exam practice to safe, independent inquiry.", "done"),
    ("14-open-items", "14", "Open items",
     "Twelve counsel questions and twenty-one assumptions, with what each unblocks.", "done"),
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
<details class="legend">
<summary>How claims are marked</summary>
<div class="legend-body">
<p>Nothing factual in this vault is unmarked. Markers sit in the right margin, or inline where a single sentence carries one.</p>
<ul>
<li><span class="mark verified">Verified</span> Checked September 2026 against the named source, registered in <a href="../evidence/sources.html">the evidence register</a>.</li>
<li><span class="mark assumed">Assumed</span> Reasoned, not checked. Shapes the plan and could be wrong.</li>
<li><span class="mark open">Open</span> A question for a lawyer, deliberately unanswered here.</li>
<li><span class="mark decided">Decision</span> A choice taken here, recorded in the <a href="decision-ledger.html">decision ledger</a>.</li>
<li><span class="mark unknown">Unknown</span> A number the plan needs and does not have. Never filled with a plausible substitute.</li>
</ul>
</div>
</details>
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
        title="Contents", desc="AI.tutor venture design vault", number="\u00b7",
        revised=REVISED,
        body=index_frag.read_text(encoding="utf-8").replace("<!--CONTENTS-->", "\n".join(rows)).strip(),
        built=built,
        prev_href="00-thesis.html", prev_label="Thesis",
        next_href="00-thesis.html", next_label="Thesis",
    )
    (DOCS / "index.html").write_text(index_html, encoding="utf-8")
    print("  built index.html")

    # The evidence register lives in /evidence, a sibling of /docs, so it needs
    # the same shell with relative paths rewritten one level across.
    src_frag = CONTENT / "sources.html"
    if src_frag.exists():
        html = SHELL.format(
            title="Evidence register", number="\u00b7",
            desc="Every external claim, with its source and the date it was checked.",
            revised=REVISED, body=src_frag.read_text(encoding="utf-8").strip(),
            built=built,
            prev_href="../docs/decision-ledger.html", prev_label="Decision ledger",
            next_href="../docs/index.html", next_label="Contents",
        )
        html = (html
                .replace('href="style.css"', 'href="../docs/style.css"')
                .replace('href="index.html"', 'href="../docs/index.html"')
                .replace('href="../evidence/sources.html"', 'href="sources.html"')
                .replace('href="decision-ledger.html"', 'href="../docs/decision-ledger.html"'))
        out = ROOT / "evidence"
        out.mkdir(exist_ok=True)
        (out / "sources.html").write_text(html, encoding="utf-8")
        print("  built ../evidence/sources.html")


if __name__ == "__main__":
    build()

