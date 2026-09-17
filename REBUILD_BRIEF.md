# AI.tutor: Restructure and Views Brief

Commit this file at the repository root as `REBUILD_BRIEF.md`, open Claude Code
in the root, and paste:

```
Read REBUILD_BRIEF.md in full, then execute it. Phase A must pass its gate in §3 and be committed before Phase B begins. The acceptance bar in §5, the loop in §6 including the turn cap and the early exits, and the forbidden moves in §7 are binding.
```

Everything binding is in this file; nothing depends on conversation history.

## 0. Mission

Two outcomes, in two phases, one run.

Phase A makes this repository cheap for a fresh Claude Code session to work
in, without changing a byte of what the reader receives. This repository
already assembles `docs/` from `src/content/` with `src/build.py`, so the
gaps are narrow: there is no `CLAUDE.md`; `viz/dependency-map.html` holds the
map as `NODES` and `EDGES` arrays inside the page, so "what else changes if
this changes" has no command behind it; `04-rights-dossier` (5,400 words) and
`05-safety-privacy-regulatory` (6,000 words) are the two fragments a session
cannot hold beside anything else; and nothing checks that `docs/` is fresh.

Phase B gives the vault a front door and five owner views, so that a person
joining reads what they own and nothing else, without a word of the design
being written twice. Today a newcomer lands on a contents page listing sixteen
documents, a ledger of thirty-odd decisions and 51,000 words. After this they
land on a 1,200-word summary, then a page naming their documents, decisions
and open items, then a reading path. The principle: views, not copies. Every
new page is generated from `roles.json`, `PAGES` in `build.py`, the decision
ledger, the open-items page, `tools/depmap/graph.json` and blocks marked in
the fragments; the only hand-written prose is one capped frame per generated
page. Where a view needs a fact it transcludes the marked block; it never
restates it.

The four reader routes on the current contents page (a media lawyer, a
creator, an investor, an examiner) stay. They are audiences who evaluate one
document; the roles are owners who execute a domain. Both belong on the
contents page.

You are the tooling engineer and, in Phase B, the ownership cartographer. No
prose changes, no design changes, no settled decision reopened, no counsel
question resolved, no page moved.

## 1. Fixed constraints (do not reopen)

1. `BUILD_BRIEF.md` §2 settled decisions stand. §5 counsel questions stay open.
   §7 house style applies to everything you write. The marker rules in
   `README.md` bind: no invented figures; no Verified marker anywhere you
   write; no figure in a frame.
2. Edit `src/`, never `docs/`, `evidence/` or `viz/`. Python 3 standard
   library only, like `build.py`. No dependencies.
3. Phase A changes no prose and no markup: served files are byte-identical at
   the gate except for the additions §2 names. Phase B changes no prose: for
   every page at the gate commit, the text of `<main class="sheet" id="doc">`
   with tags stripped and whitespace collapsed is identical at the end. Markup
   may gain attributes; text may not change. The one exception is
   `index.html`, whose main text at the gate must reappear identically as the
   main text of `contents.html`.
4. No page moves and no anchor changes, other than Phase B adding an `id` to
   an `<h2>` that has none. `docs/style.css` and `netlify.toml` are not
   touched; generated pages use existing classes only and fetch nothing over
   the network.
5. British English; no em-dashes; conclusions before the reasoning.

## 2. Phase A deliverables (exact)

### 2.1 Fragment directories in `build.py`

- A page's source may be either `src/content/<slug>.html` or a directory
  `src/content/<slug>/` of fragments concatenated in filename order:
  `000-head.html` (everything before the first top-level `<section>` carrying
  an `<h2>`), one `NNN-<h2 id>.html` per such section, `999-foot.html`
  (everything after the last). Cut at line boundaries. Concatenation is
  verbatim.
- Split `04-rights-dossier` and `05-safety-privacy-regulatory` this way with a
  one-off script, never by hand. Delete the script once §3 passes. The rule
  going forward, stated in `CLAUDE.md`: a fragment over 3,000 words of prose
  is split at `<h2>`.
- `python3 src/build.py --check` exits non-zero, printing `file:line message`,
  when any file under `docs/`, `evidence/` or `viz/` differs from what a build
  would write.

### 2.2 The dependency map, made queryable

- `tools/depmap/graph.json` becomes the single source: the `NODES` and `EDGES`
  now inside `viz/dependency-map.html`, moved out with their content unchanged.
  Each node gains a `locus`, `<page>#<anchor>`, naming where the pages state
  the thing; where no anchor exists, the page alone. Do not add a node or an
  edge the pages do not state.
- `viz/dependency-map.html` becomes a built page: `build.py` inlines
  `graph.json` into a template at `src/viz/dependency-map.html`, so the served
  page still fetches nothing.
- `tools/depmap.py` with three commands: `check` (every locus resolves in
  `docs/`; every edge endpoint is a node; `graph.json` and the served page
  agree), `impact <node-id>` (the transitive closure upstream and downstream,
  printed as an edit plan naming the fragments under `src/content/` to open,
  in order), `list`.
- If `../AI.fred-idea/tools/depmap/SCHEMA.md` is readable, mirror its id
  grammar, facet names and command names where they fit. Do not copy
  `depmap.mjs`; it is bound to that repository's harness.

### 2.3 `tools/verify.py`

Standard library only. Non-zero exit; `file:line message`. Four checks: build
freshness; every internal link and anchor under `docs/` and `evidence/`
resolves; `depmap.py check`; and, if the markup makes it mechanical, that
every Verified marker links an entry in `evidence/sources.html`. If the fourth
is not mechanical, say why in the report and leave it out.

### 2.4 `CLAUDE.md`

Under 100 lines, no heading deeper than `##`, in this order:

1. What the repository is, in three lines, including that nothing has been
   built.
2. The map: one line per top-level path.
3. The editing rule: edit `src/content/`, never `docs/`; then
   `python3 src/build.py`; then `python3 tools/verify.py`.
4. The reading rule: read `PAGES` in `build.py` and the counts on
   `docs/status.html` first; open only the fragment the task needs.
5. The dependency rule: `python3 tools/depmap.py impact <node>` before editing
   any decision, invariant or mechanism stated on more than one page.
6. The marker rules, in three lines.
7. The split rule.
8. The counsel-questions rule: never resolve one; OI-3 is the recorded
   exception.
9. Where the settled decisions live: `BUILD_BRIEF.md` §2, opened only when a
   task touches one.

### 2.5 `.claude/commands/`

`impact.md`, `section.md`, `verify.md`: closure to edit plan; one fragment plus
its one-line description from `PAGES`; build, verify, print failures, fix
nothing unless asked.

### 2.6 The ledger

One entry, numbered with the next free number after the last entry in
`src/content/decision-ledger.html` (the ledger already runs past the count
`README.md` states; the ledger governs), in the ledger's form. Record:
fragment directories and the split rule; the map as `graph.json` with `check`
and `impact`; the freshness check. Rejected: a separate data file the viz
fetches at runtime (the no-network convention forbids it); leaving the map
inside the page. Made harder: two files to keep in step, closed by `check`.
Update every typed statement of the decision count to the true count; Phase B
replaces typed counts with computed ones.

### 2.7 `README.md`

Editing, layout and status sections updated. Nothing else.

## 3. Phase A gate

Phase B does not begin until all of this holds and is committed as one commit
whose message begins `gate:`. That commit is "the gate commit" everywhere below.

1. `python3 src/build.py --check` and `python3 tools/verify.py` pass.
2. `git diff --name-only <pre-brief HEAD> -- docs/ evidence/ viz/` lists only
   `docs/decision-ledger.html`, any page carrying the decision count, and
   `viz/dependency-map.html`. Every other served file is byte-identical. The
   output goes in `RESTRUCTURE_REPORT.md`.
3. No fragment under `src/content/` exceeds 3,000 words of prose, counted with
   tags stripped. A single `<section>` that exceeds it is allowed and listed.
4. `python3 tools/depmap.py impact <the node for the kill-switch decision, or
   the nearest node>` prints a closure that names real fragments; it goes in
   the report for the founder to judge.
5. `CLAUDE.md` is under 100 lines and carries every rule in §2.4.
6. The splitter is deleted. `RESTRUCTURE_REPORT.md` is written: what changed,
   the output of §3.2, word counts before and after, exceptions under §3.3,
   the closure from §3.4, the fourth-check decision from §2.3, and one
   fresh-session test question for the founder ("What must I do before editing
   the kill-switch section of architecture?") with the answer it should give.

## 4. Phase B deliverables (exact)

### 4.1 `roles.json`

At the root. Five roles: `ceo`, `cto`, `coo`, `cfo`, `counsel`. Fields per
role: `id`, `title`, `github` (a handle, or null meaning the repository
owner), `frame` (at most 200 words, hand-written, no figures), `owns` (page
slugs and `slug#anchor` section loci), `reads` (loci). Owning a page owns all
its sections except those another role lists. Every `<h2>` section of every
page except the ones this brief generates has exactly one owner.

Starting assignment; adjust only where a section plainly belongs elsewhere,
and list every adjustment in the report:

| Role | Owns |
|------|------|
| ceo | `00-thesis`, `01-product`, `07-route-a-direct-to-parents`, `08-route-b-through-schools`, `09-route-comparison`, `11-roadmap`, `12-risk-register`, `13-primer-gateway`, `14-open-items` (the register), `decision-ledger`, `sources` (the evidence register), `status` |
| cto | `06-architecture`, `02-style-engine` |
| coo | `03-curriculum-and-content`; the creator-licence section of `04-rights-dossier` as reader, not owner |
| cfo | `10-economics`; the "Pricing and unit economics" sections of `07` and `08` |
| counsel | `04-rights-dossier`, `05-safety-privacy-regulatory`, `contracts/`, the counsel-questions section of `14`; the "Compliance posture" and "Data and consent model" sections of `07` and `08` as reader |

Two further maps:

- `decisions`: each ledger entry's owner is the owner of the document its
  `Document` field names, unless listed here as an override. Start with no
  overrides; add one only where the `Document` field names a page whose owner
  plainly should not hold the decision, and list every override in the report.
  Every entry from D1 to the last must resolve; the two entries this brief
  adds resolve to `ceo`.
- `summary`: `decisions` (the settled group, D1 to D14, one line each; if the
  build finds the group larger, take the first twelve and say so), `route`
  (the recommendation in 09, transcluded from its key block), `keys` (the key
  blocks the front door transcludes), `unknowns` (up to eight items from 14:
  counsel questions first, then assumptions).

### 4.2 Key blocks

In the fragments, mark one or two existing elements per section with
`data-key="<slug>.<section-id>.<n>"`: the sentence or list that states the
section's decision, mechanism or number. Add the attribute; change nothing
else. Where a section's `<h2>` has no `id`, give it one derived from its text
and record the addition. The report lists every key block with its text.

### 4.3 `src/build.py`, extended

`src/content/index.html` becomes `src/content/contents.html`, verbatim. After
assembling the pages, the build:

1. Computes one set of counts, from the sources, used everywhere a count is
   shown: documents, decisions (settled and taken), counsel questions open,
   assumptions unverified, external claims registered, tests specified. If
   `status.html` carries typed numbers, it now shows the computed ones; where
   a computed number disagrees with a typed one, do not change any source, and
   list the disagreement in the report.
2. Generates `docs/index.html`, the front door, from
   `src/templates/summary.html` and `roles.json`, at most 1,200 words all in:
   the frame (at most 150 words, which must carry the line that nothing has
   been built); "The route", transcluded; "What is settled", the settled
   decisions as one line each, the ledger's own `<dt>` text, linked; "Where it
   stands", the computed counts; "The numbers that matter", the transcluded
   key blocks; "What is not known", the picked items with their markers,
   linked; five role doors, each with the title, the first sentence of the
   frame and the reading path's word count; and a compact full contents list,
   one line per page.
3. Generates `docs/contents.html` from its source, so the four reader routes
   and "How to read this" live there.
4. Generates `docs/roles/<id>.html` per role from `src/templates/role.html`:
   the frame; "What you own", being documents and sections (title, words,
   link), decisions (id, `<dt>` text, link), open items (label, marker, link
   to the item), and depmap nodes whose locus falls in an owned section (id,
   label, locus link); "What binds you", the decisions owned by others that
   reach an owned section within one hop in `graph.json`; "Reading path",
   owned pages and sections in document order then read sections, with
   cumulative word counts; the role's key blocks.
5. Adds a "Doors" group to the switcher, above the document list: Summary,
   the five roles, Contents. Points the topbar's Contents link and the brand
   link where they now belong. Role pages get `numlabel` empty and sit outside
   the pager sequence.
6. Writes `.github/CODEOWNERS` from `roles.json`: one line per owned path
   under `src/content/`, the handle or the repository owner's.

`--check` covers every generated file.

### 4.4 `tools/verify.py`, extended

New checks in the existing form: a section has zero or two owners; a ledger
entry has no owner; a referenced key block is missing or not transcluded
verbatim; a digit-bearing sentence on the front door sits outside a key block
or a computed count; the front door exceeds 1,200 words or a frame exceeds
200; a Verified marker appears on a generated page; `CODEOWNERS` is stale;
the four reader routes are absent from `contents.html`.

### 4.5 The ledger

One entry, the next free number, in the ledger's form. Decision: the vault has
a generated front door and one generated page per owner; ownership is set at
section level in `roles.json`; facts reach a view by transcluding a marked
block. Rejected: hand-written role pages (they drift); page-level ownership
(07 and 08 split between three owners); including whole fragments in role
pages. Made harder: a prose edit on a generated page is lost on the next
build; ownership changes only through `roles.json`.

### 4.6 `CLAUDE.md`, `.claude/commands/role.md`, `README.md`

`CLAUDE.md` gains the ownership rule in three lines: `roles.json` is the source
of ownership; a section's owner is who a change is discussed with; views are
generated, edit `roles.json` or the fragments, never `docs/roles/`. It stays
under 100 lines. `role.md`: given a role id, prints its owned fragments under
`src/content/`, its decisions and open items, and scopes the session to them.
`README.md`: the "How to read it" section and the layout tree updated.
Nothing else.

## 5. Acceptance bar (the stop condition)

1. §3 passed and the gate commit exists.
2. `python3 src/build.py --check`, `python3 tools/verify.py` and
   `python3 tools/depmap.py check` pass.
3. The text-identity rule of §1.3 holds for every page at the gate commit; the
   script that proves it, and its output, go in the report.
4. Every section has exactly one owner and every ledger entry resolves; the
   ownership table goes in the report.
5. The front door is under 1,200 words; every frame is under 200; each role's
   reading path word count is in the report.
6. Every key block is listed in the report with its text, and every computed
   count that disagrees with a typed one is listed with both values.

## 6. The loop

Phase A:

1. Read `README.md`, `BUILD_BRIEF.md` §6 and §7, `src/build.py`, and the
   `NODES` and `EDGES` arrays in `viz/dependency-map.html` (not its rendering
   code). Read one entry of the decision ledger for its form. Do not read any
   other content fragment in full; grep 04 and 05 for `<section>` and `<h2>`.
2. Fragment directories in `build.py`; `--check`; the splitter; build.
   `git diff --stat -- docs/` must be empty. If a page does not reassemble
   byte-identically, stop and report; do not edit the page to make it fit.
3. `graph.json`, the loci, the built viz, `depmap.py`. Run `check`.
4. `verify.py`. Run it.
5. `CLAUDE.md`, the commands, the ledger entry, `README.md`.
6. Delete the splitter. Full verify. Write `RESTRUCTURE_REPORT.md`. The gate
   commit.

Phase B:

7. Read the ledger's `Document` fields, the structure of `14-open-items`, and
   `graph.json`. Do not read fragments in full until step 9, and then only to
   choose key blocks.
8. `roles.json` with the assignment of §4.1. Run a completeness script.
9. Mark key blocks. Rebuild; run the text-identity script; it must pass.
10. Extend the build: contents source, counts, templates, generated pages, the
    switcher, `CODEOWNERS`. Build; `--check`.
11. Extend `verify.py`. Run it.
12. The ledger entry. Build; verify; depmap check.
13. `CLAUDE.md`, `role.md`, `README.md`. Full verify. Write `VIEWS_REPORT.md`:
    what changed; §5.3's output; the ownership table; every adjustment and
    override; the key-block list; the front door's word count and each role's
    reading path; count disagreements.

Commit at the end of each step, with a message in the repository's style.

Cap: 55 turns, of which Phase A takes no more than 25. Early exits: a step 2
failure; a locus you cannot place without inventing an anchor (record the node
without one, list it, continue; not an exit); any need to edit prose; in
Phase B, text identity failing for a cause that is not your own markup, or a
computed count that cannot be derived mechanically from the sources (leave
that count typed, say so, continue; not an exit). A section you cannot assign
without a judgement the founder should make is assigned to `ceo`, listed, and
not an exit. On an early exit, commit what passes, write whichever report the
phase owes, stop. An exit in Phase B leaves the gate commit intact.

## 7. Forbidden moves

- Editing prose, anchors, markers, `style.css` or `netlify.toml`; in Phase B,
  changing the text of any existing element, including to make a key block
  read better in transclusion.
- Resolving a counsel question, or adding a Verified marker.
- Adding a node or an edge the pages do not state.
- Adding a dependency, or a class to `style.css`.
- Reopening a §2 decision.
- Hand-writing a list the build can generate.
- Two owners for a section, or a section with none.
- Moving a page or changing an anchor, other than adding an `id` to an
  `<h2>` that has none.
- A frame over 200 words, or a front door over 1,200.
- Em-dashes anywhere.
- Narrating in a report. State results.
