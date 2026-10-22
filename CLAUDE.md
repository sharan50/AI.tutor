# AI.tutor

## What this is
The design and planning record for three ideas for teaching children with AI, served as static HTML: the Tutor, for UK secondary students of 14 to 18 preparing for GCSE and A-level; the Primer, for children of 8 to 13; and Foundations, for children of 4 to 7 with an adult beside them. Each has its own documents; they share an evidence register, an open-items register and a decision ledger.
Nothing described here has been built, and no test described here has been run.
`BUILD_BRIEF.md` is the source instruction for the Tutor and for the vault's rules, and governs where the repository disagrees with it; its §7 house style (British English, no em-dashes or en-dashes, conclusions before reasoning) applies to everything you write. `FACETS_BRIEF.md` governs the Primer, Foundations, the shared pages and the front page.

## Map
- `BUILD_BRIEF.md`: the source instruction; §2 settled decisions, §5 counsel questions, §7 house style.
- `REBUILD_BRIEF.md`: the brief for the tooling and the owner views.
- `RESTRUCTURE_REPORT.md` and `VIEWS_REPORT.md`: what each phase of that brief changed, with the checks it passed.
- `FACETS_BRIEF.md`: the brief for the Primer, Foundations and the front page; decisions D40 onwards, OI-13 onwards, OA-22 onwards, the candidate claims.
- `FACETS_REPORT.md`: what that brief changed, the checks it passed and the independent review.
- `roles.json`: the five owners, what each owns and reads, the ledger overrides, the Tutor summary's picks (`summary`), and the front page's ideas, briefs and films (`front`).
- `README.md`: what the repository is, its status, how to read and edit it.
- `CLAUDE.md`: this file.
- `netlify.toml`: publish config. `_site/` is assembled by the build and never committed.
- `src/build.py`: the page manifest `PAGES`, the grouping by idea `GROUPS`, the build, `--check`, `--section`.
- `src/content/`: the fragments you edit. A page is `<slug>.html`, or a directory `<slug>/` of fragments.
- `src/viz/dependency-map.html`: the map's template; the build inlines the graph into it.
- `src/templates/`: `front.html` (the front page and its frame), `summary.html` (the Tutor summary and its frame) and `role.html`.
- `docs/`: the served pages, generated. `index.html` is the front page, `tutor.html` the Tutor summary, `contents.html` the contents page, `roles/<id>.html` one page per owner. The Tutor's pages are `00` to `14`, the Primer's `p1` to `p6`, Foundations' `f1` to `f6`. `docs/style.css` is hand-maintained; a session edits it only when the owner asks for a design change (D52).
- `evidence/sources.html`: the evidence register, generated from `src/content/sources.html`.
- `viz/dependency-map.html`: the served map, generated; published at `/map/`.
- `tools/depmap/graph.json`: the dependency map, nodes with a locus and edges.
- `tools/depmap.py`: `check`, `impact <node>`, `list`. `tools/verify.py`: the checks.
- `.github/CODEOWNERS`: generated from `roles.json`.
- `contracts/`: the creator licence term sheet and heads of terms, markdown, hand-maintained.
- `econ/`: the economics model and its outputs; not part of the site build.
- `.claude/commands/`: `/impact`, `/section`, `/verify`, `/role`.

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
A claim you find but cannot have the owner check goes into the register's candidates section as a CV row with its source and the date found, and text relying on it carries an Assumed marker naming it (D53). Only the owner promotes a candidate.
Never change an existing marker; a marker is `<span class="mark verified|assumed|open|unknown|decided">` and it belongs to the author of the claim.

## Ownership
`roles.json` is the source of ownership: every section has exactly one owner and every ledger entry resolves to one; `python3 src/build.py --role <id>` names what a role owns.
A section's owner is who a change to it is discussed with before it is made.
Views are generated: edit `roles.json` or the fragments, never `docs/roles/`, `docs/index.html` or `docs/tutor.html`; a fact reaches a view through a `data-key` block transcluded from the fragment, never restated. Each idea's brief on the front page is the `<slug>.brief.1` block at the head of its thesis.

## Splitting
A fragment over 3,000 words of prose, counted with tags stripped, is split at its `<h2>` headings into `src/content/<slug>/`: `000-head.html`, one `NNN-<h2 id>.html` per section, `999-foot.html` only if anything follows the last section.
Cut at line boundaries. Concatenating the directory in filename order must reproduce the page byte for byte; prove it before deleting the single file.

## Counsel questions
Never resolve a counsel question (OI-1 to OI-20 in `docs/14-open-items.html`), and never write as if one were resolved.
OI-3 is the recorded exception: D34 proceeds ahead of it under a fixed convention, and says so where it is applied.

## Settled decisions
D1 to D14 live in `BUILD_BRIEF.md` §2 and are not reopened. Open that section only when a task touches one of them.
D1 governs the Tutor; D51 sets the markets for the Primer and Foundations.
