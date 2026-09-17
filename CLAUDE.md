# AI.tutor

## What this is
The design and planning record for an AI tutor for UK secondary students: sixteen documents, an evidence register and a decision ledger, served as static HTML.
Nothing described here has been built, and no test described here has been run.
`BUILD_BRIEF.md` is the source instruction and governs where the repository disagrees with it; its §7 house style (British English, no em-dashes, conclusions before reasoning) applies to everything you write.

## Map
- `BUILD_BRIEF.md`: the source instruction; §2 settled decisions, §5 counsel questions, §7 house style.
- `REBUILD_BRIEF.md`: the brief for the tooling and the owner views.
- `RESTRUCTURE_REPORT.md`: what the restructure changed, with the checks it passed.
- `README.md`: what the repository is, its status, how to read and edit it.
- `CLAUDE.md`: this file.
- `netlify.toml`: publish config. `_site/` is assembled by the build and never committed.
- `src/build.py`: the page manifest `PAGES`, the build, `--check`, `--section`.
- `src/content/`: the fragments you edit. A page is `<slug>.html`, or a directory `<slug>/` of fragments.
- `src/viz/dependency-map.html`: the map's template; the build inlines the graph into it.
- `docs/`: the served pages, generated. `docs/style.css` is hand-maintained and never edited by a session.
- `evidence/sources.html`: the evidence register, generated from `src/content/sources.html`.
- `viz/dependency-map.html`: the served map, generated; published at `/map/`.
- `tools/depmap/graph.json`: the dependency map, nodes with a locus and edges.
- `tools/depmap.py`: `check`, `impact <node>`, `list`. `tools/verify.py`: the checks.
- `contracts/`: the creator licence term sheet and heads of terms, markdown, hand-maintained.
- `econ/`: the economics model and its outputs; not part of the site build.
- `.claude/commands/`: `/impact`, `/section`, `/verify`.

## Editing
Edit `src/content/`, never `docs/`, `evidence/` or `viz/`.
Then `python3 src/build.py`, then `python3 tools/verify.py`; both must pass before a commit.

## Reading
Read `PAGES` in `src/build.py` and the counts on `docs/status.html` first.
Open only the fragment the task needs: `python3 src/build.py --section <slug>[#anchor]` names it. Do not read a page in full to find a section.

## Dependencies
Run `python3 tools/depmap.py impact <node>` before editing any decision, invariant or mechanism stated on more than one page; `python3 tools/depmap.py list` names the nodes.
Open the fragments it prints, in the order it prints them, and nothing else.

## Markers
No invented figures: every number is from the evidence register, a stated design choice, or marked Unknown. There is no fourth kind.
A claim not in `evidence/sources.html` may not carry a Verified marker. Never add a Verified marker.
Never change an existing marker; a marker is `<span class="mark verified|assumed|open|unknown|decided">` and it belongs to the author of the claim.

## Splitting
A fragment over 3,000 words of prose, counted with tags stripped, is split at its `<h2>` headings into `src/content/<slug>/`: `000-head.html`, one `NNN-<h2 id>.html` per section, `999-foot.html` only if anything follows the last section.
Cut at line boundaries. Concatenating the directory in filename order must reproduce the page byte for byte; prove it before deleting the single file.

## Counsel questions
Never resolve a counsel question (OI-1 to OI-12 in `docs/14-open-items.html`), and never write as if one were resolved.
OI-3 is the recorded exception: D34 proceeds ahead of it under a fixed convention, and says so where it is applied.

## Settled decisions
D1 to D14 live in `BUILD_BRIEF.md` §2 and are not reopened. Open that section only when a task touches one of them.
