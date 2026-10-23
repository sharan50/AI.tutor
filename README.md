# AI.tutor

**Design and planning record for three ideas for teaching children with AI.**
Owner: Dhruv Sharan. Build base: Bengaluru. Markets: the UK and the US together
where resources allow, the UK first where they do not (D1 for the Tutor, as
amended by the owner on 22 October 2026; D51 for the other two).

- **The Tutor** (ages 14 to 18). A student chooses **how** they are taught by
  naming an educator whose style they already recognise, and nothing reaches that
  student which cannot be traced to an examiner-validated item. A student can
  also choose a self-tutor, taught in their own face and voice, which only they
  can see. The most developed of the three.
- **The Primer** (ages 8 to 13). A child's why-questions taken seriously: a
  checked explanation first, then the question underneath, explored by asking
  rather than telling, until the child states a view of their own. Its subjects
  come in modules the company writes; parents switch them on and off.
- **Foundations** (ages 4 to 7). Early reading, writing and arithmetic, with an
  adult beside the child in every session and the screen as the adult's guide.
  The least certain of the three, and deliberately not the first.

Which idea goes first between the Tutor and the Primer is open, and is decided by
field research with teachers, professors and parents.

---

## What this repository is

A design, a plan, the evidence behind both, and an honest account of what is
still unknown. It is **not** application code and it is not a product.

**Nothing described here has been built. No test described here has been run.**

The source instruction is [`BUILD_BRIEF.md`](BUILD_BRIEF.md) at the root, for the
Tutor and for the vault's rules. Where this repository and the brief disagree, the
brief governs. [`FACETS_BRIEF.md`](FACETS_BRIEF.md) governs the Primer,
Foundations, the shared pages and the front page.

## Status

| | |
|---|---|
| Documents | 30 across the three ideas, the registers included, plus an evidence register |
| Built | Nothing |
| Tests specified | **32**, none run. There is nothing to run them against |
| Counsel questions | **27** open, none answered. We proceed ahead of OI-3 under D34 and of OI-23 to OI-27 under D59, and each says so where it is applied |
| Assumptions unverified | **40**, of which 17 are resolvable by reading or by asking rather than by building |
| Decisions recorded | **69**, including three, taken on the owner's instruction, that reverse two earlier positions, and D1 and D9, since amended by the owner |
| External claims registered | **42**, each with source and date checked, plus **15** candidates awaiting the owner's check |

[`docs/status.html`](docs/status.html) computes these counts from the registers at
build time and governs where this table disagrees with it.

## How to read it

Start at [`docs/index.html`](docs/index.html), the front page: a brief on each of
the three ideas with a space for a short film of each, which idea goes first, what
the three share, and where everything stands. It is written for a first-time
reader: a former teacher, a prospective partner or co-founder, an accelerator.

[`docs/tutor.html`](docs/tutor.html) is the Tutor's summary: the route, the
settled decisions, the computed counts, the numbers that matter, what is not
known, and a door for each owner. Each door, under [`docs/roles/`](docs/roles/),
names what that owner holds: documents and sections, decisions, open items and
components on the map, what binds them from elsewhere, and a reading path with
cumulative word counts. Every line on those pages is transcluded from the page
that states it or computed at build time; the only hand-written text is one
short frame per page, kept in [`roles.json`](roles.json).

[`docs/contents.html`](docs/contents.html) carries every document grouped by idea,
and five routes through the material: for a lawyer, a creator, an investor, a
curriculum specialist, and a teacher, partner or prospective co-founder.
[`docs/which-first.html`](docs/which-first.html) sets out which idea goes first
and why, and [`docs/field-research.html`](docs/field-research.html) is the guide
for the conversations that decide it.

If you only read three things about the Tutor:

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
3. **Counsel questions stay open.** There are two exceptions. OI-3, board naming,
   where waiting would mean a product that cannot describe itself, is argued in
   [`docs/04-rights-dossier.html`](docs/04-rights-dossier.html) and recorded as
   decision D34. The self-tutor proceeds ahead of OI-23 to OI-27 and is withdrawn
   only if counsel's answer is a categoric no, recorded as decision D59. Neither
   is slipped in.

A claim found by research but not yet checked by the owner is registered as a
**candidate** (CV-01 onwards) in its own section of the evidence register, with its
source and the date found, and text relying on it carries an Assumed marker. Only
the owner promotes a candidate to Verified (decision D53).

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

The page manifest, the grouping by idea, the navigation order and the per-page
legend live in [`src/build.py`](src/build.py). `docs/style.css` is
hand-maintained and is not generated. [`CLAUDE.md`](CLAUDE.md) carries the
working rules for a coding session.

### Adding a film to the front page

Each idea's card on the front page has a space for a short film. In
[`roles.json`](roles.json), under `front`, each idea has `"video": null`, which
shows the placeholder. To fill it, either:

- put the file under `docs/media/` (for example `docs/media/primer.mp4`, with an
  optional poster image and captions file) and set
  `"video": {"src": "media/primer.mp4", "poster": "media/primer.jpg", "captions": "media/primer.vtt"}`.
  Keep the file small: GitHub refuses files over 100 MB; or
- upload it to a video host and set
  `"video": {"embed": "https://www.youtube-nocookie.com/embed/VIDEO_ID"}`. The
  build adds that host, and only that host, to the site's content security
  policy.

Then run the build and the checks as above.

Three rules for the films, because they show products that are not built and
are seen by parents and teachers:

- **Label them.** Each card captions its film as illustrative, saying that
  nothing shown has been built; set your own wording with `"caption"` if
  needed, but keep the point. If a film is AI-generated, say so in the film
  itself.
- **No real child without written consent.** Do not show a real child unless a
  parent has consented in writing to this use, and never show a child's name,
  school or face where it can be avoided.
- **Show the design, not a promise.** A film may show how an idea would work;
  it may not show an outcome the documents do not claim, such as a child
  reading faster.

## Layout

```
BUILD_BRIEF.md                 the source instruction, for the Tutor and the vault's rules
REBUILD_BRIEF.md               the brief for the tooling and the owner views
FACETS_BRIEF.md                the brief for the Primer, Foundations and the front page
RESTRUCTURE_REPORT.md          what the restructure changed, with its checks
VIEWS_REPORT.md                what the views added, with the identity proof and the ownership table
FACETS_REPORT.md               what the facets brief changed, its checks and its independent review
roles.json                     the five owners, what each owns and reads, the Tutor summary's and the front page's picks
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
  templates/                   front.html, the front page; summary.html, the Tutor summary; role.html
tools/
  depmap.py                    check, impact <node>, list
  depmap/graph.json            the dependency map: nodes with a locus, and edges
  verify.py                    build freshness, links and anchors, the map
docs/
  index.html                   the front page, generated: the three ideas
  tutor.html                   the Tutor summary, generated
  contents.html                contents grouped by idea, and the five reader routes
  roles/<id>.html              one generated page per owner
  00-thesis.html .. 14-open-items.html     the Tutor, and the shared open-items register
  p1-primer-thesis.html .. p6-primer-plan.html
  f1-foundations-thesis.html .. f6-foundations-plan.html
  which-first.html             which idea goes first
  field-research.html          the guide for teachers, professors and parents
  decision-ledger.html
  status.html                  generated from the registers
  style.css                    hand-maintained
evidence/
  sources.html                 42 external claims, source and date checked, and 15 candidates
viz/
  dependency-map.html          the served map, generated; published at /map/
contracts/
  creator-licence-term-sheet.md      creator-facing, one page, plain English
  creator-licence-heads-of-terms.md  counsel-facing, with Schedules 2 and 3
econ/                          the economics model and its outputs; not part of the site
```

## Publishing

Static output. No framework, no JavaScript on the documents, no fonts or assets
fetched over the network. Netlify publishes `_site/`, which the build assembles
from `docs/`, `evidence/` and `contracts/`, because `evidence/` is a sibling of
`docs/` and every sourced claim links to it. `/` redirects to
`docs/index.html`; it must not rewrite, because a rewrite serves the page at the
root, where its relative stylesheet and links fail (D52). See
[`netlify.toml`](netlify.toml).

The screen design is dark; the print stylesheet converts to light, because these
documents get printed and sent to lawyers.

## Conventions

- **British English.**
- **No em-dashes or en-dashes.** Commas and semicolons for clause separation;
  "4 to 7" for a range.
- Conclusions before the reasoning that supports them.
- If something is weak, say it is weak.
- New decisions go in the decision ledger, not only in the document they affect,
  and carry what was rejected and what the choice makes harder later.
- New external claims go in the evidence register with the date checked.
