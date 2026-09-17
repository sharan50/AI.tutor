#!/usr/bin/env python3
"""Assemble /docs HTML pages from content fragments in /src/content.

No dependencies, no build tooling. Run `python3 src/build.py` from the repo
root after editing any fragment. `python3 src/build.py --check` writes nothing
and exits non-zero, printing `file:line message`, when any served file differs
from what a build would write.

A page's source is either src/content/<slug>.html or a directory
src/content/<slug>/ whose *.html fragments are concatenated verbatim in
filename order (000-head.html, one NNN-<h2 id>.html per section, 999-foot.html).

The "Built" stamp in the footer is kept when a page is otherwise unchanged, so
a rebuild on a later day leaves untouched pages byte-identical and the stamp
records when the page last changed.
"""
from pathlib import Path
import datetime
import shutil
import re
import hashlib
import base64
import json
import os
import sys

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "src" / "content"
DOCS = ROOT / "docs"
EVIDENCE = ROOT / "evidence"
MAP_TEMPLATE = ROOT / "src" / "viz" / "dependency-map.html"
GRAPH = ROOT / "tools" / "depmap" / "graph.json"
MAP_OUT = ROOT / "viz" / "dependency-map.html"

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
    <a href="{map_href}">Map</a>
    <a href="{evidence_href}">Evidence</a>
    <a href="{contents_href}">Contents</a>
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


# ------------------------------------------------------------------ sources

def source_path(slug):
    """A page's source: src/content/<slug>.html, or the directory src/content/<slug>/."""
    single = CONTENT / f"{slug}.html"
    if single.exists():
        return single
    folder = CONTENT / slug
    if folder.is_dir():
        return folder
    return None


def fragment_files(slug):
    """The files a page is assembled from, in the order they are concatenated."""
    src = source_path(slug)
    if src is None:
        return []
    if src.is_dir():
        return sorted(p for p in src.iterdir() if p.suffix == ".html")
    return [src]


def read_source(slug):
    """A page's source text: the fragments concatenated verbatim, in filename order."""
    files = fragment_files(slug)
    if not files:
        return None
    return "".join(p.read_text(encoding="utf-8") for p in files)


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


def switcher_for(current_slug, prefix=""):
    """Every door and every document, so any page is one click from any other.

    prefix is what gets a link from the current page's directory to docs/."""
    def entry(href, number, title, key):
        here = ' class="here"' if key == current_slug else ""
        return f'<a href="{prefix}{href}"{here}><span class="sw-no">{number}</span>{title}</a>'
    out = ['<p class="rail-h">Doors</p>', entry("index.html", "", "Summary", "index")]
    for role in load_roles()["roles"]:
        out.append(entry(f"roles/{role['id']}.html", "", role["title"], f"roles/{role['id']}"))
    out.append(entry("contents.html", "", "Contents", "contents"))
    out.append('<p class="rail-h">Documents</p>')
    for slug, number, title, _desc, _status in PAGES:
        out.append(entry(f"{slug}.html", number or "", title, slug))
    out.append(entry("status.html", "", "Status", "status"))
    out.append(entry("../map/", "", "Impact surface", "map"))
    out.append(entry("../evidence/sources.html", "", "Evidence register", "sources"))
    return "".join(out)


# ------------------------------------------------------------------ render

def render():
    """Every served file the build owns, as {path: text}. Writes nothing."""
    built = datetime.date.today().strftime("%d %B %Y")
    outputs = {}
    counts = compute_counts()
    for i, (slug, number, title, desc, _status) in enumerate(PAGES):
        body = read_source(slug)
        if body is None:
            print(f"  missing fragment: {slug}")
            continue
        body = apply_counts(body.strip(), counts)
        prev_i, next_i = i - 1, i + 1
        prev_href = "contents.html" if prev_i < 0 else PAGES[prev_i][0] + ".html"
        prev_label = "Contents" if prev_i < 0 else PAGES[prev_i][2]
        next_href = "contents.html" if next_i >= len(PAGES) else PAGES[next_i][0] + ".html"
        next_label = "Contents" if next_i >= len(PAGES) else PAGES[next_i][2]
        html = SHELL.format(
            title=title, desc=desc, number=number or "&middot;", numlabel=(f'<span class="sw-no">{number}</span> ' if number else ""), revised=REVISED,
            css="style.css", home="index.html", status_href="status.html", map_href="../map/",
            contents_href="contents.html", evidence_href="../evidence/sources.html",
            switcher=switcher_for(slug), outline=outline_for(body),
            body=body, built=built,
            prev_href=prev_href, prev_label=prev_label,
            next_href=next_href, next_label=next_label,
        )
        outputs[DOCS / f"{slug}.html"] = html

    rows = []
    for slug, number, title, desc, status in PAGES:
        label = {"done": "drafted", "partial": "outline", "todo": "not written"}[status]
        rows.append(
            f'  <li><span class="n">{number}</span>'
            f'<span class="t"><a href="{slug}.html">{title}</a><span>{desc}</span></span>'
            f'<span class="s {status}">{label}</span></li>'
        )
    contents_body = apply_counts(read_source("contents").replace("<!--CONTENTS-->", "\n".join(rows)).strip(), counts)
    outputs[DOCS / "contents.html"] = SHELL.format(
        title="Contents", desc="AI.tutor venture design vault", number="&middot;", numlabel="",
        revised=REVISED, css="style.css", home="index.html", status_href="status.html", map_href="../map/",
        contents_href="contents.html", evidence_href="../evidence/sources.html",
        switcher=switcher_for("contents"), outline=outline_for(contents_body),
        body=contents_body, built=built,
        prev_href="index.html", prev_label="Summary",
        next_href="00-thesis.html", next_label="Thesis",
    )

    outputs[DOCS / "status.html"] = build_status(built, counts)
    outputs.update(render_views(built, counts))

    # The evidence register lives in /evidence, a sibling of /docs, so it needs
    # the same shell with relative paths rewritten one level across.
    body = read_source("sources")
    if body is not None:
        body = body.strip()
        html = SHELL.format(
            title="Evidence register", number="&middot;", numlabel="",
            desc="Every external claim, with its source and the date it was checked.",
            revised=REVISED, css="../docs/style.css", home="../docs/index.html",
            status_href="../docs/status.html", map_href="../map/",
            contents_href="../docs/contents.html", evidence_href="sources.html",
            switcher=switcher_for("sources", "../docs/").replace('href="../docs/../', 'href="../'),
            outline=outline_for(body), body=body, built=built,
            prev_href="../docs/decision-ledger.html", prev_label="Decision ledger",
            next_href="../docs/contents.html", next_label="Contents",
        )
        outputs[EVIDENCE / "sources.html"] = html

    page = render_map()
    if page is not None:
        outputs[MAP_OUT] = page
    return outputs


# ------------------------------------------------------------------ the map
# tools/depmap/graph.json is the single source for the dependency map. The
# served page inlines it at build time, so it still fetches nothing.

def _json_rows(items):
    return "[\n" + ",\n".join(json.dumps(i, ensure_ascii=False) for i in items) + "\n]"


def render_map():
    if not MAP_TEMPLATE.exists() or not GRAPH.exists():
        return None
    graph = json.loads(GRAPH.read_text(encoding="utf-8"))
    template = MAP_TEMPLATE.read_text(encoding="utf-8")
    for marker in ("/*@@NODES@@*/", "/*@@EDGES@@*/"):
        if template.count(marker) != 1:
            raise SystemExit(f"{MAP_TEMPLATE.relative_to(ROOT)}: expected exactly one {marker}")
    return (template.replace("/*@@NODES@@*/", _json_rows(graph["nodes"]))
                    .replace("/*@@EDGES@@*/", _json_rows(graph["edges"])))


# ------------------------------------------------------------------ write / check

STAMP = re.compile(r"Built \d{1,2} [A-Z][a-z]+ \d{4}")


def _unstamped(text):
    return STAMP.sub("Built (stamp)", text)


def write_outputs(outputs):
    for path, text in outputs.items():
        rel = path.relative_to(ROOT)
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.exists():
            old = path.read_text(encoding="utf-8")
            if old == text or _unstamped(old) == _unstamped(text):
                print(f"  unchanged {rel}")
                continue
        path.write_text(text, encoding="utf-8")
        print(f"  built {rel}")


def check_outputs(outputs):
    """Every served file that differs from what a build would write, as file:line."""
    stale = 0
    for path, text in outputs.items():
        rel = path.relative_to(ROOT)
        if not path.exists():
            print(f"{rel}:1 missing; run python3 src/build.py")
            stale += 1
            continue
        old = _unstamped(path.read_text(encoding="utf-8")).split("\n")
        new = _unstamped(text).split("\n")
        if old == new:
            continue
        line = next((n for n, (a, b) in enumerate(zip(old, new), 1) if a != b),
                    min(len(old), len(new)) + 1)
        print(f"{rel}:{line} stale; differs from a fresh build (run python3 src/build.py)")
        stale += 1
    return stale


def build():
    DOCS.mkdir(exist_ok=True)
    write_outputs(render())
    assemble_publish_dir()


def check():
    stale = check_outputs(render())
    if stale:
        print(f"{stale} served file(s) differ from a fresh build")
        return 1
    print("build is fresh")
    return 0


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
MAP_SRC = MAP_OUT

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
    return window[:cut].rstrip(" ,;:") + "…"


def build_status(built, counts):
    openitems = read_source("14-open-items")
    curric = read_source("03-curriculum-and-content")
    routes = read_source("09-route-comparison")
    risks_f = read_source("12-risk-register")
    everything = "\n".join(read_source(p[0]) for p in PAGES if read_source(p[0]) is not None)

    oi = _rows(openitems, "OI")
    oa = _rows(openitems, "OA")
    acc = _rows(curric, "ACC")
    risks = _rows(risks_f, "R")
    conds = _rows(routes, "C")
    decisions = range(counts["decisions"])
    tests = counts["test_ids"]
    cheap_n = counts["cheap"]

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

    return SHELL.format(
        title="Status", desc="Everything open, unproven or waiting, on one page.",
        number="&middot;", numlabel="", revised=REVISED, css="style.css", home="index.html",
        status_href="status.html", evidence_href="../evidence/sources.html",
        map_href="../map/", contents_href="contents.html",
        switcher=switcher_for("status"), outline=outline_for(body), body=body, built=built,
        prev_href="contents.html", prev_label="Contents",
        next_href="00-thesis.html", next_label="Thesis",
    )


def _test_blurb(everything, test_id):
    """First sentence near a test's definition, for the status table."""
    m = re.search(re.escape(test_id) + r"[:<][^<]{0,40}</td><td>(.*?)</td>", everything, re.S)
    if m:
        return m.group(1)
    m = re.search(r"<b>" + re.escape(test_id) + r":</b>(.*?)[.<]", everything, re.S)
    return m.group(1) if m else ""


def section(arg):
    """For /section: a page's one-line description and the fragment(s) holding <slug>[#anchor]."""
    slug, _, anchor = arg.partition("#")
    files = fragment_files(slug)
    if not files:
        print(f"src/content/{slug}: no such page")
        return 1
    print(next((p[3] for p in PAGES if p[0] == slug), "(not in PAGES)"))
    for f in files:
        if not anchor or f'id="{anchor}"' in f.read_text(encoding="utf-8"):
            print(f.relative_to(ROOT))
    return 0


# ------------------------------------------------------------------ views
# The front door, the counts on the contents page and one page per owner are
# generated from roles.json, PAGES, the ledger, the open-items register,
# tools/depmap/graph.json and the key blocks marked in the fragments. Nothing
# on them is written twice: a fact is transcluded from the block that states
# it, a count is computed here, and the only hand-written prose is one frame
# per generated page.

ROLES_FILE = ROOT / "roles.json"
TEMPLATES = ROOT / "src" / "templates"
CODEOWNERS = ROOT / ".github" / "CODEOWNERS"
ROLES_DIR = DOCS / "roles"
FRONT_DOOR_WORDS = 1200
ROLE_BLOCK_WORDS = 150   # a longer key block is linked from a role page, not transcluded

_roles = None


def load_roles():
    global _roles
    if _roles is None:
        _roles = json.loads(ROLES_FILE.read_text(encoding="utf-8"))
    return _roles


def written_slugs():
    """Every page with a source fragment: the documents, the contents page, the register."""
    return [p[0] for p in PAGES] + ["contents", "sources"]


def page_dir(slug):
    return EVIDENCE if slug == "sources" else DOCS


def page_title(slug):
    for s, number, title, _d, _s in PAGES:
        if s == slug:
            return (number + " " if number else "") + title
    return {"contents": "Contents", "sources": "Evidence register", "status": "Status"}.get(slug, slug)


def page_sections(slug):
    """[(hid, heading text, html)]: the head first with hid None, then each h2 section."""
    src = read_source(slug)
    out = []
    for part in re.split(r'(?m)^(?=<h2 id=")', src):
        m = re.match(r'<h2 id="([^"]+)"[^>]*>(.*?)</h2>', part, re.S)
        out.append((m.group(1) if m else None, _plain(m.group(2)) if m else "", part))
    return out


def section_of(slug, anchor):
    """The h2 section holding id="anchor"; None if it sits in the head or is absent."""
    for hid, _t, html in page_sections(slug):
        if f'id="{anchor}"' in html:
            return hid
    return None


def word_count(html_str):
    return len(_plain(html_str).split())


def owner_of(slug, hid):
    """The one role owning a section: a role listing the section, else the role
    listing the page. None when there is no owner or more than one."""
    roles = load_roles()["roles"]
    sec = [r["id"] for r in roles if hid and f"{slug}#{hid}" in r["owns"]]
    page = [r["id"] for r in roles if slug in r["owns"]]
    owners = sec or page
    return owners[0] if len(owners) == 1 else None


def readers_of(slug, hid):
    return [r["id"] for r in load_roles()["roles"]
            if f"{slug}#{hid}" in r["reads"] or slug in r["reads"]]


def ledger_entries():
    """Every decision: id, its dt text (or the table's decision cell), the rest of
    the entry, the ledger section it sits in, and the document the entry names
    (the last link to a page in PAGES; None where there is none)."""
    pages = {p[0] for p in PAGES}
    out = []
    for hid, _t, html in page_sections("decision-ledger"):
        for m in re.finditer(r'<tr><td class="id">(D\d+)</td><td>(.*?)</td>(.*?)</tr>', html, re.S):
            out.append(dict(id=m.group(1), text=m.group(2), rest=m.group(3), section=hid))
        for m in re.finditer(r'<dt>(D\d+)\.\s*(.*?)</dt>\s*<dd>(.*?)</dd>', html, re.S):
            out.append(dict(id=m.group(1), text=m.group(2), rest=m.group(3), section=hid))
    for e in out:
        docs = [(p, a) for p, a in re.findall(r'href="([0-9a-z-]+)\.html(?:#([^"]+))?"', e["rest"]) if p in pages]
        e["document"] = docs[-1] if docs else None
    return sorted(out, key=lambda e: int(e["id"][1:]))


def decision_owner(entry):
    """roles.json overrides first; else the owner of the section the entry's
    document names; else the owner of the ledger section it sits in."""
    overrides = load_roles().get("decisions", {}).get("overrides", {})
    if entry["id"] in overrides:
        return overrides[entry["id"]]
    if entry["document"]:
        page, anchor = entry["document"]
        owner = owner_of(page, section_of(page, anchor) if anchor else None)
        if owner:
            return owner
    return owner_of("decision-ledger", entry["section"])


def open_items():
    out = []
    for hid, _t, html in page_sections("14-open-items"):
        for m in re.finditer(r'<tr>\s*<td class="id">(O[IA]-\d+)</td>\s*<td>(.*?)</td>', html, re.S):
            out.append(dict(id=m.group(1), text=m.group(2), section=hid,
                            marker="open" if m.group(1).startswith("OI") else "assumed"))
    return out


def compute_counts():
    """One set of counts, from the sources, used everywhere a count is shown."""
    entries = ledger_entries()
    items = open_items()
    everything = "\n".join(read_source(p[0]) for p in PAGES if read_source(p[0]) is not None)
    tests = sorted(set(re.findall(r"\bT-[A-Z]+-\d+\b", everything)))
    openitems = read_source("14-open-items")
    cheap = re.search(r"<b>(\w+) of the [\w-]+ assumptions are resolvable", openitems)
    return dict(
        documents=len(PAGES),
        decisions=len(entries),
        settled=sum(1 for e in entries if e["section"] == "settled"),
        taken=sum(1 for e in entries if e["section"] != "settled"),
        counsel=sum(1 for i in items if i["marker"] == "open"),
        assumptions=sum(1 for i in items if i["marker"] == "assumed"),
        claims=len(re.findall(r'<td class="id">EV-\d+</td>', read_source("sources") or "")),
        tests=len(tests), test_ids=tests,
        risks=len(_rows(read_source("12-risk-register"), "R")),
        cheap=cheap.group(1) if cheap else "several",
    )


_ONES = ("zero one two three four five six seven eight nine ten eleven twelve "
         "thirteen fourteen fifteen sixteen seventeen eighteen nineteen").split()
_TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()


def number_words(n):
    if n < 20:
        return _ONES[n]
    if n < 100:
        return _TENS[n // 10] + ("-" + _ONES[n % 10] if n % 10 else "")
    return str(n)


def apply_counts(html_str, counts):
    """The text of every element carrying data-count becomes the computed count.
    data-format="words" writes it as a word, keeping the typed capitalisation."""
    def fix(m):
        n = counts[m.group(3)]
        if m.group(4) == "words":
            text = number_words(n)
            if m.group(5)[:1].isupper():
                text = text[0].upper() + text[1:]
        else:
            text = str(n)
        return m.group(1) + text + m.group(6)
    return re.sub(r'(<(\w+)[^>]*\sdata-count="([^"]+)"(?:\s+data-format="(\w+)")?[^>]*>)(.*?)(</\2>)',
                  fix, html_str, flags=re.S)


def extract_element(text, start):
    """The whole element whose opening tag begins at text[start]."""
    tag = re.match(r"<([a-z0-9]+)", text[start:]).group(1)
    depth = 0
    for m in re.compile(rf"<(/?){tag}\b[^>]*>").finditer(text, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return text[start:m.end()]
    raise ValueError(f"unclosed <{tag}> at offset {start}")


def key_blocks():
    """Every block marked data-key in the fragments: key -> dict(slug, section, html)."""
    out = {}
    for slug in written_slugs():
        for hid, _t, html in page_sections(slug):
            for m in re.finditer(r'<[a-z0-9]+[^>]*\sdata-key="([^"]+)"', html):
                out[m.group(1)] = dict(slug=slug, section=hid, html=extract_element(html, m.start()))
    return out


def rebase_links(html_str, slug, to_dir):
    """Rewrite the relative hrefs of a block written on page `slug` so that they
    resolve from the directory `to_dir`. Absolute links are left alone."""
    src_dir = page_dir(slug)

    def fix(m):
        href = m.group(1)
        if re.match(r"^(https?:|mailto:|data:|tel:)", href):
            return m.group(0)
        path, _, anchor = href.partition("#")
        target = src_dir / f"{slug}.html" if path == "" else src_dir / path
        rel = os.path.relpath(os.path.normpath(str(target)), str(to_dir))
        if path.endswith("/"):
            rel += "/"
        return f'href="{rel}' + (f"#{anchor}" if anchor else "") + '"'
    return re.sub(r'href="([^"]*)"', fix, html_str)


def transclude(key, to_dir, blocks):
    if key not in blocks:
        return f'<p data-key-missing="{key}"></p>'
    return rebase_links(blocks[key]["html"], blocks[key]["slug"], to_dir)


def locus_href(locus, to_dir):
    page, _, anchor = locus.partition("#")
    rel = os.path.relpath(str(page_dir(page) / f"{page}.html"), str(to_dir))
    return rel + (f"#{anchor}" if anchor else "")


def node_owner(node):
    page, _, anchor = node["locus"].partition("#")
    return owner_of(page, section_of(page, anchor) if anchor else None)


def _section_title(slug, hid):
    return next((t for h, t, _x in page_sections(slug) if h == hid), hid)


def first_sentence(text):
    m = re.match(r"(.*?[.!?])(\s|$)", text, re.S)
    return m.group(1) if m else text


def _ul(items, cls="tight"):
    return f'<ul class="{cls}">' + "".join(f"<li{attrs}>{body}</li>" for attrs, body in items) + "</ul>"


def role_scope(role_id):
    """[(slug, hid, title, words)] for the sections a role owns, and for the ones it reads."""
    owned, read = [], []
    for slug in written_slugs():
        for hid, title, html in page_sections(slug):
            if hid is None:
                continue
            entry = (slug, hid, title, word_count(html))
            if owner_of(slug, hid) == role_id:
                owned.append(entry)
            elif role_id in readers_of(slug, hid):
                read.append(entry)
    return owned, read


def path_lines(sections, to_dir):
    """Owned or read sections grouped by page: a whole page is one line with the
    page's words (its head included); a partly held page is one line per section."""
    lines = []
    for slug in written_slugs():
        mine = [x for x in sections if x[0] == slug]
        if not mine:
            continue
        secs = page_sections(slug)
        href = os.path.relpath(str(page_dir(slug) / f"{slug}.html"), str(to_dir))
        if len(mine) == sum(1 for hid, _t, _h in secs if hid):
            lines.append((f'<a href="{href}">{page_title(slug)}</a>', sum(word_count(h) for _i, _t, h in secs)))
        else:
            for _s, hid, title, words in mine:
                lines.append((f'<a href="{href}#{hid}">{page_title(slug)}: {title}</a>', words))
    return lines


def render_summary(built, counts, cfg, blocks, entries, owners, path_words):
    s = cfg["summary"]
    to = DOCS
    tpl = (TEMPLATES / "summary.html").read_text(encoding="utf-8")
    by_id = {e["id"]: e for e in entries}
    settled_group = [e["id"] for e in entries if e["section"] == "settled"]
    wanted = list(s["decisions"])
    if len(settled_group) > len(wanted):
        print(f"  note: the settled group has {len(settled_group)} entries; the front door takes the first twelve")
        wanted = settled_group[:12]
    settled = _ul((' data-from="decision-ledger"',
                   f'<a href="decision-ledger.html#{by_id[d]["section"]}">{d}</a> ' + _plain(by_id[d]["text"]))
                  for d in wanted if d in by_id)

    def card(name, label, note):
        return (f'<div class="stat"><span class="stat-n" data-count="{name}">{counts[name]}</span>'
                f'<span class="stat-l">{label}</span><span class="stat-note">{note}</span></div>')
    standing = '<div class="stats">' + "".join([
        card("documents", "documents", "drafted, none built"),
        card("decisions", "decisions",
             f'<span data-count="settled">{counts["settled"]}</span> settled, '
             f'<span data-count="taken">{counts["taken"]}</span> taken'),
        card("counsel", "counsel questions", "open, none answered"),
        card("assumptions", "assumptions", "unverified"),
        card("claims", "external claims", "registered, source and date checked"),
        card("tests", "tests specified", "<b>none run</b>"),
    ]) + "</div>"
    numbers = "\n".join(transclude(k, to, blocks) for k in s["keys"])
    items = {i["id"]: i for i in open_items()}
    unknowns = _ul((' data-from="14-open-items"',
                    f'<span class="mark {items[i]["marker"]}">{"Open" if items[i]["marker"] == "open" else "Assumed"}</span> '
                    f'<a href="14-open-items.html#{items[i]["section"]}">{i}</a> ' + _plain(items[i]["text"]))
                   for i in s["unknowns"] if i in items)
    doors = '<div class="split">' + "".join(
        f'<div><h4><a href="roles/{r["id"]}.html">{r["title"]}</a></h4><p>{first_sentence(r["frame"])}</p>'
        f'<p data-count="path:{r["id"]}">Reading path: {path_words[r["id"]]:,} words</p></div>'
        for r in cfg["roles"]) + "</div>"
    rows = [(number, f'<a href="{slug}.html">{title}</a>') for slug, number, title, _d, _s in PAGES]
    rows += [("", '<a href="status.html">Status</a>'), ("", '<a href="../evidence/sources.html">Evidence register</a>'),
             ("", '<a href="../map/">Impact surface</a>'), ("", '<a href="contents.html">Contents and reader routes</a>')]
    contents = '<ul class="contents">' + "".join(
        f'<li data-from="PAGES"><span class="n">{n}</span><span class="t">{t}</span></li>' for n, t in rows) + "</ul>"
    body = (tpl.replace("<!--ROUTE-->", transclude(s["route"], to, blocks))
               .replace("<!--SETTLED-->", settled).replace("<!--STANDING-->", standing)
               .replace("<!--NUMBERS-->", numbers).replace("<!--UNKNOWNS-->", unknowns)
               .replace("<!--DOORS-->", doors).replace("<!--CONTENTS-->", contents)).strip()
    n = word_count(body)
    if n > FRONT_DOOR_WORDS:
        print(f"  warning: the front door is {n} words, over {FRONT_DOOR_WORDS}")
    return SHELL.format(
        title="Summary", desc="AI.tutor design vault: the route, what is settled, where it stands, and who owns what.",
        number="&middot;", numlabel="", revised=REVISED, css="style.css", home="index.html",
        status_href="status.html", map_href="../map/", contents_href="contents.html",
        evidence_href="../evidence/sources.html",
        switcher=switcher_for("index"), outline=outline_for(body), body=body, built=built,
        prev_href="status.html", prev_label="Status",
        next_href="contents.html", next_label="Contents",
    )


def render_role(role, built, cfg, blocks, entries, owners, graph):
    rid, to = role["id"], ROLES_DIR
    tpl = (TEMPLATES / "role.html").read_text(encoding="utf-8")
    owned, read = role_scope(rid)
    own_lines = path_lines(owned, to)
    own_docs = _ul(("", f"{link} <span>{words:,} words</span>") for link, words in own_lines)
    mine = [e for e in entries if owners[e["id"]] == rid]
    own_dec = _ul(("", f'<a href="../decision-ledger.html#{e["section"]}">{e["id"]}</a> ' + _plain(e["text"]))
                  for e in mine)
    nodes = [n for n in graph["nodes"] if node_owner(n) == rid]
    item_ids = set()
    for n in nodes:
        item_ids.update(n.get("o", []))
    for it in open_items():
        if owner_of("14-open-items", it["section"]) == rid:
            item_ids.add(it["id"])
    items = [it for it in open_items() if it["id"] in item_ids]
    own_items = _ul(("", f'<span class="mark {it["marker"]}">{"Open" if it["marker"] == "open" else "Assumed"}</span> '
                     f'<a href="../14-open-items.html#{it["section"]}">{it["id"]}</a> ' + _plain(it["text"]))
                    for it in items)
    own_nodes = _ul(("", f'<b>{n["id"]}</b> {n["label"]}, <a href="{locus_href(n["locus"], to)}">{n["locus"]}</a>')
                    for n in nodes)
    by_node = {n["id"]: n for n in graph["nodes"]}
    mine_ids = {n["id"] for n in nodes}
    binds = {}
    for a, b, _k in graph["edges"]:
        for x, y in ((a, b), (b, a)):
            if x in mine_ids and y not in mine_ids:
                for d in by_node[y].get("d", []):
                    if owners.get(d) not in (None, rid):
                        binds.setdefault(d, set()).add(y)
    by_id = {e["id"]: e for e in entries}
    bind_lines = _ul(("", f'<a href="../decision-ledger.html#{by_id[d]["section"]}">{d}</a> ({owners[d]}) '
                      + _plain(by_id[d]["text"]) + " <span>via " + ", ".join(sorted(via)) + "</span>")
                     for d, via in sorted(binds.items(), key=lambda kv: int(kv[0][1:])) if d in by_id)
    path, cum = [], 0
    for link, words in own_lines + path_lines(read, to):
        cum += words
        path.append(("", f"{link} <span>{words:,} words, {cum:,} cumulative</span>"))
    path_html = f'<ol class="tight">' + "".join(f"<li>{b}</li>" for _a, b in path) + "</ol>"
    order = {slug: i for i, slug in enumerate(written_slugs())}
    keys = sorted((k for k, b in blocks.items() if owner_of(b["slug"], b["section"]) == rid),
                  key=lambda k: (order[blocks[k]["slug"]],
                                 [hid for hid, _t, _h in page_sections(blocks[k]["slug"])].index(blocks[k]["section"]),
                                 k))
    # A block is transcluded when it is short and carries no Verified marker; a
    # generated page may carry none. Anything else is linked and read in place.
    def in_place(k):
        n = word_count(blocks[k]["html"])
        if 'class="mark verified"' in blocks[k]["html"]:
            return f"carries a Verified marker, {n:,} words"
        return f"{n:,}-word block" if n > ROLE_BLOCK_WORDS else None
    shown = [transclude(k, to, blocks) for k in keys if in_place(k) is None]
    longer = [k for k in keys if in_place(k) is not None]
    keys_html = "\n".join(shown)
    if longer:
        keys_html += "\n" + _ul(("", f'<a href="{locus_href(blocks[k]["slug"] + "#" + blocks[k]["section"], to)}">'
                                  f'{page_title(blocks[k]["slug"])}: {_section_title(blocks[k]["slug"], blocks[k]["section"])}</a> '
                                  f'<span>{in_place(k)}, read in place</span>') for k in longer)
    body = (tpl.replace("<!--TITLE-->", role["title"])
               .replace("<!--FRAME-->", f'<p class="standfirst">{role["frame"]}</p>')
               .replace("<!--OWN-DOCS-->", own_docs).replace("<!--OWN-DECISIONS-->", own_dec)
               .replace("<!--OWN-ITEMS-->", own_items).replace("<!--OWN-NODES-->", own_nodes)
               .replace("<!--BINDS-->", bind_lines).replace("<!--PATH-->", path_html)
               .replace("<!--KEYS-->", keys_html)).strip()
    html = SHELL.format(
        title=role["title"], desc=f"What the {role['title'].lower()} owns, what binds them, and their reading path.",
        number="&middot;", numlabel="", revised=REVISED, css="../style.css", home="../index.html",
        status_href="../status.html", map_href="../../map/", contents_href="../contents.html",
        evidence_href="../../evidence/sources.html",
        switcher=switcher_for(f"roles/{rid}", "../"), outline=outline_for(body), body=body, built=built,
        prev_href="../index.html", prev_label="Summary",
        next_href="../contents.html", next_label="Contents",
    )
    return html, cum


def render_codeowners(cfg):
    owner = "@" + cfg["repository"].split("/")[0]

    def handle(r):
        return ("@" + r["github"]) if r.get("github") else owner
    page_lines, section_lines = {}, []
    for r in cfg["roles"]:
        for item in r["owns"]:
            slug, _, hid = item.partition("#")
            if slug == "contracts":
                page_lines.setdefault("contracts/", []).append(handle(r))
                continue
            src = source_path(slug)
            if src is None:
                continue
            rel = str(src.relative_to(ROOT)) + ("/" if src.is_dir() else "")
            if not hid:
                page_lines.setdefault(rel, []).append(handle(r))
            elif src.is_dir():
                frag = next((f for f in fragment_files(slug) if f'id="{hid}"' in f.read_text(encoding="utf-8")), None)
                if frag is not None:
                    section_lines.append((str(frag.relative_to(ROOT)), handle(r)))
            else:
                page_lines.setdefault(rel, []).append(handle(r))
    lines = ["# Generated by src/build.py from roles.json. Edit roles.json, never this file.",
             "# A section owned by another role inside a single-file page lists both handles.", ""]
    lines += [f"{p} {' '.join(dict.fromkeys(h))}" for p, h in sorted(page_lines.items())]
    lines += [f"{p} {h}" for p, h in sorted(section_lines)]
    return "\n".join(lines) + "\n"


def render_views(built, counts):
    cfg = load_roles()
    graph = json.loads(GRAPH.read_text(encoding="utf-8")) if GRAPH.exists() else {"nodes": [], "edges": []}
    blocks = key_blocks()
    entries = ledger_entries()
    owners = {e["id"]: decision_owner(e) for e in entries}
    outputs, path_words = {}, {}
    for role in cfg["roles"]:
        html, words = render_role(role, built, cfg, blocks, entries, owners, graph)
        outputs[ROLES_DIR / f"{role['id']}.html"] = html
        path_words[role["id"]] = words
        counts[f"path:{role['id']}"] = words
    outputs[DOCS / "index.html"] = render_summary(built, counts, cfg, blocks, entries, owners, path_words)
    outputs[CODEOWNERS] = render_codeowners(cfg)
    return outputs


def role_scope_report(role_id):
    """For /role: the fragments a role owns under src/content/, its decisions and its open items."""
    cfg = load_roles()
    role = next((r for r in cfg["roles"] if r["id"] == role_id), None)
    if role is None:
        print(f"roles.json: no role {role_id}; roles are " + ", ".join(r["id"] for r in cfg["roles"]))
        return 1
    print(f"{role['title']} ({role_id})")
    print("fragments owned:")
    for slug in written_slugs():
        secs = [hid for hid, _t, _h in page_sections(slug) if hid]
        mine = [hid for hid in secs if owner_of(slug, hid) == role_id]
        if not mine:
            continue
        files = fragment_files(slug)
        if len(mine) == len(secs):
            print(f"  {source_path(slug).relative_to(ROOT)}{'/' if source_path(slug).is_dir() else ''}")
        else:
            for hid in mine:
                frag = next((f for f in files if f'id="{hid}"' in f.read_text(encoding="utf-8")), files[0])
                print(f"  {frag.relative_to(ROOT)}  #{hid}")
    entries = ledger_entries()
    print("decisions:")
    for e in entries:
        if decision_owner(e) == role_id:
            print(f"  {e['id']}  {_plain(e['text'], 110)}")
    graph = json.loads(GRAPH.read_text(encoding="utf-8")) if GRAPH.exists() else {"nodes": []}
    ids = set()
    for n in graph["nodes"]:
        if node_owner(n) == role_id:
            ids.update(n.get("o", []))
    for it in open_items():
        if owner_of("14-open-items", it["section"]) == role_id:
            ids.add(it["id"])
    print("open items:")
    for it in open_items():
        if it["id"] in ids:
            print(f"  {it['id']}  {_plain(it['text'], 110)}")
    return 0


if __name__ == "__main__":
    args = sys.argv[1:]
    if "--check" in args:
        sys.exit(check())
    if len(args) == 2 and args[0] == "--section":
        sys.exit(section(args[1]))
    if len(args) == 2 and args[0] == "--role":
        sys.exit(role_scope_report(args[1]))
    build()
