#!/usr/bin/env python3
"""Assemble /docs HTML pages from content fragments in /src/content.

No dependencies, no build tooling. Run `python3 src/build.py` from the repo
root after editing any fragment.
"""
from pathlib import Path
import datetime
import shutil
import re
import hashlib
import base64

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
<link rel="stylesheet" href="{css}">
</head>
<body>
<a class="skip" href="#doc">Skip to the document</a>

<header class="topbar">
  <a class="brand" href="{home}"><b>AI.tutor</b> <span>design vault</span></a>
  <details class="switcher">
    <summary>{numlabel}{title}</summary>
    <div class="sw-panel">{switcher}</div>
  </details>
  <nav class="toplinks">
    <a href="{status_href}">Status</a>
    <a href="../map/">Map</a>
    <a href="{evidence_href}">Evidence</a>
    <a href="{home}">Contents</a>
  </nav>
</header>

<div class="layout">
  <aside class="rail">{outline}</aside>
  <main class="sheet" id="doc">
{body}
  </main>
</div>

<nav class="pager">
  <a class="prev" href="{prev_href}"><span>Previous</span>{prev_label}</a>
  <a class="next" href="{next_href}"><span>Next</span>{next_label}</a>
</nav>

<footer class="pagefoot">
  <div class="legend-row">
    <span class="li"><span class="mark verified">Verified</span>checked against a named source</span>
    <span class="li"><span class="mark assumed">Assumed</span>reasoned, not checked</span>
    <span class="li"><span class="mark open">Open</span>a question for a lawyer</span>
    <span class="li"><span class="mark unknown">Unknown</span>a number we do not have</span>
    <span class="li"><span class="mark decided">Decision</span>a choice taken here</span>
  </div>
  <div class="meta-row">
    <span>AI.tutor design vault, revised {revised}. Nothing here has been built.</span>
    <span class="stamp">Built {built}</span>
  </div>
</footer>
</body>
</html>
"""


def outline_for(fragment):
    """Section outline for the left rail, built from the fragment's own h2s."""
    heads = re.findall(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', fragment, re.S)
    if not heads:
        return ""
    items = []
    for hid, label in heads:
        label = re.sub(r"<[^>]+>", "", label).strip()
        items.append(f'<li><a href="#{hid}">{label}</a></li>')
    return ('<div class="rail-inner"><p class="rail-h">On this page</p><ol class="rail-nav">'
            + "".join(items) + "</ol></div>")


def switcher_for(current_slug):
    """Every document, so any page is one click from any other."""
    out = []
    for slug, number, title, _desc, _status in PAGES:
        here = ' class="here"' if slug == current_slug else ""
        no = number or ""
        out.append(f'<a href="{slug}.html"{here}><span class="sw-no">{no}</span>{title}</a>')
    out.append('<a href="status.html"><span class="sw-no"></span>Status</a>')
    out.append('<a href="../map/"><span class="sw-no"></span>Impact surface</a>')
    out.append('<a href="../evidence/sources.html"><span class="sw-no"></span>Evidence register</a>')
    return "".join(out)



def build():
    built = datetime.date.today().strftime("%d %B %Y")
    DOCS.mkdir(exist_ok=True)
    for i, (slug, number, title, desc, _status) in enumerate(PAGES):
        frag = CONTENT / f"{slug}.html"
        if not frag.exists():
            print(f"  missing fragment: {slug}")
            continue
        body = frag.read_text(encoding="utf-8").strip()
        prev_i, next_i = i - 1, i + 1
        prev_href = "index.html" if prev_i < 0 else PAGES[prev_i][0] + ".html"
        prev_label = "Contents" if prev_i < 0 else PAGES[prev_i][2]
        next_href = "index.html" if next_i >= len(PAGES) else PAGES[next_i][0] + ".html"
        next_label = "Contents" if next_i >= len(PAGES) else PAGES[next_i][2]
        html = SHELL.format(
            title=title, desc=desc, number=number or "&middot;", numlabel=(f'<span class="sw-no">{number}</span> ' if number else ""), revised=REVISED,
            css="style.css", home="index.html", status_href="status.html",
            evidence_href="../evidence/sources.html",
            switcher=switcher_for(slug), outline=outline_for(body),
            body=body, built=built,
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
    index_body = index_frag.read_text(encoding="utf-8").replace("<!--CONTENTS-->", "\n".join(rows)).strip()
    index_html = SHELL.format(
        title="Contents", desc="AI.tutor venture design vault", number="&middot;", numlabel="",
        revised=REVISED, css="style.css", home="index.html", status_href="status.html",
        evidence_href="../evidence/sources.html",
        switcher=switcher_for("index"), outline=outline_for(index_body),
        body=index_body, built=built,
        prev_href="status.html", prev_label="Status",
        next_href="00-thesis.html", next_label="Thesis",
    )
    (DOCS / "index.html").write_text(index_html, encoding="utf-8")
    print("  built index.html")

    build_status(built)

    # The evidence register lives in /evidence, a sibling of /docs, so it needs
    # the same shell with relative paths rewritten one level across.
    src_frag = CONTENT / "sources.html"
    if src_frag.exists():
        body = src_frag.read_text(encoding="utf-8").strip()
        html = SHELL.format(
            title="Evidence register", number="&middot;", numlabel="",
            desc="Every external claim, with its source and the date it was checked.",
            revised=REVISED, css="../docs/style.css", home="../docs/index.html",
            status_href="../docs/status.html", evidence_href="sources.html",
            switcher=switcher_for("sources").replace('href="', 'href="../docs/')
                                            .replace('href="../docs/../evidence/', 'href="'),
            outline=outline_for(body), body=body, built=built,
            prev_href="../docs/decision-ledger.html", prev_label="Decision ledger",
            next_href="../docs/index.html", next_label="Contents",
        )
        out = ROOT / "evidence"
        out.mkdir(exist_ok=True)
        (out / "sources.html").write_text(html, encoding="utf-8")
        print("  built ../evidence/sources.html")

    assemble_publish_dir()



# Netlify publishes PUBLISH_DIR, not the repository root. Anything absent from
# PUBLISHED is therefore never uploaded, rather than uploaded and then hidden
# behind a rule. BUILD_BRIEF.md and src/ are repository files, not site pages:
# nothing in docs/ or evidence/ links to them, and they do not belong on a
# public URL. README.md is left out for the same reason; its links point at the
# two things above and would dangle.
PUBLISH_DIR = ROOT / "_site"
PUBLISHED = ["docs", "evidence", "contracts"]


# viz/dependency-map.html is the one page here that runs a script. It goes to
# /map/ rather than into docs/, because header rules are matched by path prefix
# and there is no way to write "everything except this page". Separate prefixes
# mean the strict policy that covers the documents is never loosened to
# accommodate the map.
MAP_SRC = ROOT / "viz" / "dependency-map.html"

STRICT_CSP = ("default-src 'none'; script-src 'none'; style-src 'self'; "
              "img-src 'self' data:; font-src 'self'; base-uri 'none'; "
              "form-action 'none'")


def _csp_hashes(html, tag):
    """SHA-256 of each inline block, so the policy names this page's own code.

    Computed from the file at build time rather than written down, so it cannot
    fall out of step with the page the way a pasted hash would.
    """
    pat = re.compile(r"<" + tag + r"[^>]*>(.*?)</" + tag + r">", re.S)
    out = []
    for body in pat.findall(html):
        digest = hashlib.sha256(body.encode("utf-8")).digest()
        out.append("'sha256-" + base64.b64encode(digest).decode("ascii") + "'")
    return out


def publish_map():
    if not MAP_SRC.exists():
        return None
    html = MAP_SRC.read_text(encoding="utf-8")
    out = PUBLISH_DIR / "map"
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(html, encoding="utf-8")
    scripts, styles = _csp_hashes(html, "script"), _csp_hashes(html, "style")
    print(f"  published /map/: {len(scripts)} scripts and {len(styles)} styles, hashed")
    return scripts, styles


def write_headers(map_hashes):
    """One _headers file, generated, so the map's policy and the documents'
    policy cannot overlap on a path and be intersected by the browser."""
    lines = []

    def block(path, extra):
        lines.append(path)
        lines.append("  X-Content-Type-Options: nosniff")
        lines.append("  X-Frame-Options: DENY")
        lines.append("  Referrer-Policy: strict-origin-when-cross-origin")
        lines.extend(extra)
        lines.append("")

    for path in ("/", "/docs/*", "/evidence/*"):
        block(path, ["  Content-Security-Policy: " + STRICT_CSP])
    # The contracts are markdown by design; serve them as text so a creator
    # opens them in the browser instead of downloading a file.
    block("/contracts/*", ["  Content-Security-Policy: " + STRICT_CSP,
                           "  Content-Type: text/plain; charset=utf-8"])
    if map_hashes:
        scripts, styles = map_hashes
        csp = ("default-src 'none'; script-src " + " ".join(scripts)
               + "; style-src " + " ".join(styles) + " https://fonts.googleapis.com"
               + "; font-src https://fonts.gstatic.com; img-src 'self' data:; "
                 "base-uri 'none'; form-action 'none'; frame-ancestors 'none'")
        block("/map/*", ["  Content-Security-Policy: " + csp])
    (PUBLISH_DIR / "_headers").write_text("\n".join(lines), encoding="utf-8")
    print(f"  wrote _site/_headers: {sum(1 for l in lines if l and not l.startswith(' '))} path rules")


def assemble_publish_dir():
    if PUBLISH_DIR.exists():
        shutil.rmtree(PUBLISH_DIR)
    PUBLISH_DIR.mkdir()
    for name in PUBLISHED:
        src = ROOT / name
        if src.is_dir():
            shutil.copytree(src, PUBLISH_DIR / name)
    write_headers(publish_map())
    n = sum(1 for _ in PUBLISH_DIR.rglob("*") if _.is_file())
    print(f"  assembled _site/ for publishing: {n} files from {', '.join(PUBLISHED)}, plus the map")


# ---------------------------------------------------------------- status view
# Generated from the registers themselves, so it cannot drift from the
# documents the way a hand-maintained summary would.

def _rows(fragment, prefix):
    """Table rows whose first cell is an id like OI-3 or ACC-2."""
    pat = re.compile(
        r'<tr>\s*<td class="id">(' + prefix + r'-?\d+)</td>(.*?)</tr>', re.S)
    out = []
    for ident, rest in pat.findall(fragment):
        cells = re.findall(r"<td[^>]*>(.*?)</td>", rest, re.S)
        out.append((ident, cells))
    return out


def _plain(html_str, limit=None):
    t = re.sub(r"<[^>]+>", "", html_str)
    t = (t.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
          .replace("&middot;", "-").replace("&nbsp;", " "))
    t = re.sub(r"\s+", " ", t).strip()
    if not limit or len(t) <= limit:
        return t
    # cut at the last sentence end inside the budget, else the last word
    window = t[:limit]
    cut = max(window.rfind(". "), window.rfind("? "), window.rfind("; "))
    if cut > limit * 0.45:
        return window[:cut + 1]
    cut = window.rfind(" ")
    return window[:cut].rstrip(" ,;:") + "\u2026"


def build_status(built):
    read = lambda n: (CONTENT / n).read_text(encoding="utf-8")
    openitems = read("14-open-items.html")
    ledger = read("decision-ledger.html")
    curric = read("03-curriculum-and-content.html")
    routes = read("09-route-comparison.html")
    risks_f = read("12-risk-register.html")
    everything = "\n".join((CONTENT / f"{p[0]}.html").read_text(encoding="utf-8")
                           for p in PAGES if (CONTENT / f"{p[0]}.html").exists())

    oi = _rows(openitems, "OI")
    oa = _rows(openitems, "OA")
    acc = _rows(curric, "ACC")
    risks = _rows(risks_f, "R")
    conds = _rows(routes, "C")
    decisions = set(re.findall(r'<td class="id">D(\d+)</td>', ledger)) | \
                set(re.findall(r"<dt>D(\d+)\.", ledger))
    tests = sorted(set(re.findall(r"\bT-[A-Z]+-\d+\b", everything)))
    cheap = re.search(r"<b>(\w+) of the [\w-]+ assumptions are resolvable", openitems)
    cheap_n = cheap.group(1) if cheap else "several"

    def card(n, label, note):
        return (f'<div class="stat"><span class="stat-n">{n}</span>'
                f'<span class="stat-l">{label}</span><span class="stat-note">{note}</span></div>')

    stats = "".join([
        card(len(PAGES), "documents", "drafted, none built"),
        card(len(tests), "tests specified", "<b>none run</b>"),
        card(len(oi), "questions for counsel", "none answered"),
        card(len(oa), "assumptions", f"{cheap_n} answerable by reading or asking"),
        card(len(decisions), "decisions", "each with what it forecloses"),
        card(len(risks), "risks", "ordered by the owner's ranking"),
    ])

    cond_rows = "".join(
        f'<tr><td class="id">{i}</td><td>{_plain(c[0], 210)}</td>'
        f'<td>{_plain(c[1], 190)}</td><td class="pill-cell"><span class="pill wait">untested</span></td></tr>'
        for i, c in conds)

    oi_rows = "".join(
        f'<tr><td class="id">{i}</td><td>{_plain(c[0], 250)}</td><td>{_plain(c[1], 130)}</td></tr>'
        for i, c in oi)

    oa_rows = "".join(
        f'<tr><td class="id">{i}</td><td>{_plain(c[0], 230)}</td><td>{_plain(c[1], 120)}</td></tr>'
        for i, c in oa)

    test_rows = "".join(
        f'<tr><td class="id">{t}</td><td>{_plain(_test_blurb(everything, t), 170)}</td>'
        f'<td class="pill-cell"><span class="pill stop">not run</span></td></tr>' for t in tests)

    acc_rows = "".join(
        f'<tr><td class="id">{i}</td><td>{_plain(c[0], 170)}</td>'
        f'<td class="id">{_plain(c[2]) if len(c) > 2 else ""}</td>'
        f'<td class="pill-cell"><span class="pill stop">not run</span></td></tr>' for i, c in acc)

    risk_rows = "".join(
        f'<tr><td class="id">{i}</td><td>{_plain(c[0], 210)}</td><td>{_plain(c[1], 150)}</td></tr>'
        for i, c in risks)

    body = f"""<h1>Status</h1>
<p class="standfirst">Everything in this vault that is open, unproven or waiting, on one page.
Generated from the registers themselves at build time, so it cannot drift from the documents
the way a hand-maintained summary would.</p>

<div class="stats">{stats}</div>

<div class="claim">
<p>The single most important line on this page is the second figure: <b>{len(tests)} tests
specified and none run.</b> There is no product, no pilot and no customer, so every accuracy
and style claim in this vault is a commitment rather than a measurement. Read everything
else here in that light.</p>
<span class="tag open">Unproven<span class="src">no pilot, no users, no revenue</span></span>
</div>

<h2 id="conditions">The three conditions that decide the route</h2>
<p><a href="09-route-comparison.html">09</a> recommends Route A on three conditions. Two can be
tested this quarter for almost nothing, and either can flip the decision on its own.</p>
<div class="tw"><table>
<thead><tr><th class="id">#</th><th>Condition</th><th>How it is tested</th><th>State</th></tr></thead>
<tbody>{cond_rows}</tbody></table></div>

<h2 id="counsel">Questions for counsel</h2>
<p>Deliberately unanswered. One, OI-3, we are proceeding ahead of under D34, and it says so
where it is applied. Full text in <a href="14-open-items.html">14</a>.</p>
<div class="tw"><table>
<thead><tr><th class="id">#</th><th>Question</th><th>Unblocks</th></tr></thead>
<tbody>{oi_rows}</tbody></table></div>

<h2 id="assumptions">Assumptions the plan rests on</h2>
<p>None verified. {cheap_n.capitalize()} of them resolve by reading a published document or making
a phone call, rather than by building anything, which is why
<a href="11-roadmap.html#m1">milestone M1</a> contains almost no engineering.</p>
<div class="tw"><table>
<thead><tr><th class="id">#</th><th>Assumption</th><th>Shapes</th></tr></thead>
<tbody>{oa_rows}</tbody></table></div>

<h2 id="floors">Accuracy floors</h2>
<div class="tw"><table>
<thead><tr><th class="id">#</th><th>Floor</th><th class="id">Test</th><th>State</th></tr></thead>
<tbody>{acc_rows}</tbody></table></div>

<h2 id="tests">Every test in the vault</h2>
<div class="tw"><table>
<thead><tr><th class="id">Test</th><th>What it establishes</th><th>State</th></tr></thead>
<tbody>{test_rows}</tbody></table></div>

<h2 id="risks">Risks</h2>
<p>In the owner's ranking. <a href="12-risk-register.html#ordering">12</a> explains why the
engineering priority runs close to the reverse of it.</p>
<div class="tw"><table>
<thead><tr><th class="id">#</th><th>Risk</th><th>Leading indicator</th></tr></thead>
<tbody>{risk_rows}</tbody></table></div>
"""

    html = SHELL.format(
        title="Status", desc="Everything open, unproven or waiting, on one page.",
        number="&middot;", numlabel="", revised=REVISED, css="style.css", home="index.html",
        status_href="status.html", evidence_href="../evidence/sources.html",
        switcher=switcher_for("status"), outline=outline_for(body), body=body, built=built,
        prev_href="index.html", prev_label="Contents",
        next_href="00-thesis.html", next_label="Thesis",
    )
    (DOCS / "status.html").write_text(html, encoding="utf-8")
    print("  built status.html")


def _test_blurb(everything, test_id):
    """First sentence near a test's definition, for the status table."""
    m = re.search(re.escape(test_id) + r"[:<][^<]{0,40}</td><td>(.*?)</td>", everything, re.S)
    if m:
        return m.group(1)
    m = re.search(r"<b>" + re.escape(test_id) + r":</b>(.*?)[.<]", everything, re.S)
    return m.group(1) if m else ""


if __name__ == "__main__":
    build()

