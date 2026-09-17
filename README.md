# AI.tutor

**Design and planning record for an AI tutor for UK secondary students.**
Owner: Dhruv Sharan. Build base: Bengaluru. Market: the UK.

A student chooses **how** they are taught by naming an educator whose style they
already recognise, and nothing reaches that student which cannot be traced to an
examiner-validated item.

---

## What this repository is

A design, a plan, the evidence behind both, and an honest account of what is
still unknown. It is **not** application code and it is not a product.

**Nothing described here has been built. No test described here has been run.**

The source instruction is [`BUILD_BRIEF.md`](BUILD_BRIEF.md) at the root. Where
this repository and the brief disagree, the brief governs.

## Status

| | |
|---|---|
| Documents | 16, plus an evidence register and a decision ledger |
| Built | Nothing |
| Tests specified | **13**, none run. There is nothing to run them against |
| Counsel questions | **12** open, none answered. We proceed ahead of exactly one (OI-3), and it says so where it is applied |
| Assumptions unverified | **21**, of which 8 are resolvable by reading or by asking rather than by building |
| Decisions recorded | **39**, including 3 that reverse earlier positions |
| External claims registered | **42**, each with source and date checked |

[`docs/status.html`](docs/status.html) computes these counts from the registers at
build time and governs where this table disagrees with it.

## How to read it

Start at [`docs/index.html`](docs/index.html), the front door: the route, the
settled decisions, the computed counts, the numbers that matter, what is not
known, and a door for each owner. Each door, under [`docs/roles/`](docs/roles/),
names what that owner holds: documents and sections, decisions, open items and
components on the map, what binds them from elsewhere, and a reading path with
cumulative word counts. Every line on those pages is transcluded from the page
that states it or computed at build time; the only hand-written text is one
short frame per page, kept in [`roles.json`](roles.json).

[`docs/contents.html`](docs/contents.html) carries the reading order and the
four routes through the material for a lawyer, a creator, an investor or a
curriculum specialist.

If you only read three things:

1. [`docs/00-thesis.html`](docs/00-thesis.html): why the 2025 differentiation is
   dead and what replaced it.
2. [`docs/09-route-comparison.html`](docs/09-route-comparison.html): the decision,
   with three falsifiable conditions and the strongest case for the route not
   recommended.
3. [`docs/14-open-items.html`](docs/14-open-items.html): everything this design
   rests on that has not been established.

## How claims are marked

Nothing factual is unmarked. Markers sit in the right margin, or inline where a
single sentence carries one.

| Marker | Meaning |
|---|---|
| **Verified** (green) | Checked September 2026 against a named source, registered in [`evidence/sources.html`](evidence/sources.html) |
| **Assumed** (amber) | Reasoned, not checked. Shapes the plan and could be wrong |
| **Open** (red) | A question for a lawyer, deliberately unanswered |
| **Unknown** (violet) | A number the plan needs and does not have. Never filled with a plausible substitute |
| **Decision** (plain) | A choice taken here, recorded in [`docs/decision-ledger.html`](docs/decision-ledger.html) |

Three rules follow, and they are the ones a contributor most easily breaks:

1. **No invented figures.** Every number is from the evidence register, a stated
   design choice, or marked Unknown. There is no fourth kind.
2. **A claim not in the evidence register may not carry a Verified marker.**
3. **Counsel questions stay open.** The single exception is OI-3, board naming,
   where waiting would mean a product that cannot describe itself. That exception
   is argued in [`docs/04-rights-dossier.html`](docs/04-rights-dossier.html) and
   recorded as decision D34, not slipped in.

## Editing

Pages are assembled from fragments. **Edit `src/content/`, never `docs/`,
`evidence/` or `viz/`**, then:

```
python3 src/build.py
python3 tools/verify.py
```

The build regenerates every page in `docs/`, `evidence/sources.html` and
`viz/dependency-map.html`. `python3 src/build.py --check` reports any served
file that differs from a fresh build; `verify.py` runs that first, then checks
every internal link and anchor, then the dependency map.

A page's source is either `src/content/<slug>.html` or a directory
`src/content/<slug>/` of fragments concatenated verbatim in filename order:
`000-head.html`, one `NNN-<h2 id>.html` per section, and `999-foot.html` if
anything follows the last section. A fragment over 3,000 words of prose,
counted with tags stripped, is split at its `<h2>` headings.

Before editing a decision, invariant or mechanism stated on more than one
page, run `python3 tools/depmap.py impact <node>`; it prints the fragments to
open, in order. The map is `tools/depmap/graph.json`, and
`python3 tools/depmap.py check` proves every node's locus resolves and that the
served map agrees with it.

The page manifest, the navigation order and the per-page legend live in
[`src/build.py`](src/build.py). `docs/style.css` is hand-maintained and is not
generated. [`CLAUDE.md`](CLAUDE.md) carries the working rules for a coding
session.

## Layout

```
BUILD_BRIEF.md                 the source instruction
REBUILD_BRIEF.md               the brief for the tooling and the owner views
RESTRUCTURE_REPORT.md          what the restructure changed, with its checks
VIEWS_REPORT.md                what the views added, with the identity proof and the ownership table
roles.json                     the five owners, what each owns and reads, the front door's picks
CLAUDE.md                      working rules for a coding session
README.md                      this file
netlify.toml                   static publish config
.claude/commands/              /impact, /section, /verify, /role
.github/CODEOWNERS             generated from roles.json
src/
  build.py                     assembles docs/, evidence/ and viz/ from fragments
  content/                     the fragments you actually edit
    <slug>.html                a page in one file
    <slug>/                    a page in fragments, one per h2 section
  viz/dependency-map.html      the map's template; the build inlines graph.json
  templates/                   summary.html, the front door and its frame; role.html
tools/
  depmap.py                    check, impact <node>, list
  depmap/graph.json            the dependency map: nodes with a locus, and edges
  verify.py                    build freshness, links and anchors, the map
docs/
  index.html                   the front door, generated
  contents.html                contents, reading order and the four reader routes
  roles/<id>.html              one generated page per owner
  00-thesis.html .. 14-open-items.html
  decision-ledger.html
  status.html                  generated from the registers
  style.css                    hand-maintained
evidence/
  sources.html                 42 external claims, source and date checked
viz/
  dependency-map.html          the served map, generated; published at /map/
contracts/
  creator-licence-term-sheet.md      creator-facing, one page, plain English
  creator-licence-heads-of-terms.md  counsel-facing, with Schedules 2 and 3
econ/                          the economics model and its outputs; not part of the site
```

## Publishing

Static output. No framework, no JavaScript, no fonts or assets fetched over the
network. Netlify publishes the **repository root**, not `docs/`, because
`evidence/` is a sibling of `docs/` and every sourced claim links to it. `/`
rewrites to `docs/index.html`. See [`netlify.toml`](netlify.toml).

The screen design is dark; the print stylesheet converts to light, because these
documents get printed and sent to lawyers.

## Conventions

- **British English.**
- **No em-dashes.** Commas and semicolons for clause separation.
- Conclusions before the reasoning that supports them.
- If something is weak, say it is weak.
- New decisions go in the decision ledger, not only in the document they affect,
  and carry what was rejected and what the choice makes harder later.
- New external claims go in the evidence register with the date checked.
