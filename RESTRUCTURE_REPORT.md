# Restructure report: Phase A

Pre-brief HEAD `4fc589a`. Every check below was run on the tree the gate commit records.

## What changed

- `src/build.py`. A page's source is `src/content/<slug>.html` or a directory `src/content/<slug>/` of fragments concatenated verbatim in filename order. `--check` writes nothing and prints `file:line message` for any file under `docs/`, `evidence/` or `viz/` that differs from what a build would write. `--section <slug>[#anchor]` prints a page's one-line description from `PAGES` and the fragment that holds the section. The served map is built from `src/viz/dependency-map.html` with `tools/depmap/graph.json` inlined.
- The `Built` stamp. A rebuild on a later day changed every served page's footer, which would have failed §1.3 and made `--check` fail on any day but the build day. The build now keeps a page's existing stamp when nothing else on the page changed, so the stamp records when the page last changed. Pages that changed at the gate carry 17 September 2026; the rest keep 15 September 2026.
- `src/content/`. `04-rights-dossier` and `05-safety-privacy-regulatory` split at `<h2>` by a one-off script, `tools/split_fragment.py`, never by hand. §3.3 requires no fragment over 3,000 words, and `01-product`, `02-style-engine`, `03-curriculum-and-content`, `06-architecture` and `decision-ledger` were also over it, so the same script split them. Each round trip was proved byte for byte before the single file was removed. The fragments carry no `<section>` element, so a section is the run from one top-level `<h2 id>` to the next; nothing follows the last section, so no page has a `999-foot.html`. The script is deleted at the gate.
- `tools/depmap/graph.json`. The `NODES` and `EDGES` arrays moved out of the page unchanged in content (73 nodes, 129 edges; extracted by evaluating the page's own arrays, not by hand). Each node gained `locus`. No node or edge was added. Every locus has an anchor; none needed a page-only locus.
- `tools/depmap.py`: `check`, `impact <node-id>`, `list`. `tools/verify.py`: build freshness, links and anchors, the map. `../AI.fred-idea/tools/depmap/SCHEMA.md` is not readable from this checkout (the sibling repository is absent), so the graph keeps the page's own field names and id grammar.
- `CLAUDE.md` (53 lines), `.claude/commands/impact.md`, `section.md`, `verify.md`.
- Ledger entry D38, in the ledger's form, under its own heading `#repository`. Typed decision counts updated to 38: the ledger standfirst, the contents page, `README.md`. `README.md`'s status table was also stale against the computed status page on tests (12, computed 13), counsel questions (11, computed 12), assumptions (19, computed 21) and assumptions resolvable by reading (7, the register says eight); those now show the computed values and the table says the status page governs.
- `README.md`: editing, layout and status sections. Nothing else.

## Served files at the gate (§3.2)

```
$ git diff --name-only 4fc589a -- docs/ evidence/ viz/
docs/decision-ledger.html
docs/index.html
docs/status.html
viz/dependency-map.html
```

- `docs/decision-ledger.html`: D38 and the standfirst count.
- `docs/index.html`: the decision count, 37 to 38.
- `docs/status.html`: the decision count is computed from the ledger and rose to 38.
- `viz/dependency-map.html`: the data block is now inlined from `graph.json` (JSON rows instead of hand-written object literals, with `locus` on each node). The 347 lines before the block and the 584 lines after it are identical to the previous page.

Byte-identical against `4fc589a`: 17 of 21 served files, being every file not listed above. `git diff --stat` summary: ` 4 files changed, 218 insertions(+), 314 deletions(-)`.

## Word counts, tags stripped

| Page | Before | After | Largest fragment |
|---|---|---|---|
| `00-thesis` | 2,438 | one file, 2,438 | |
| `01-product/` | 3,438 | 10 fragments, 3,438 in all | largest `050-worked.html`, 1,020 |
| `02-style-engine/` | 3,762 | 9 fragments, 3,762 in all | largest `020-set.html`, 737 |
| `03-curriculum-and-content/` | 4,105 | 11 fragments, 4,105 in all | largest `020-cleanroom.html`, 806 |
| `04-rights-dossier/` | 5,377 | 11 fragments, 5,377 in all | largest `030-naming.html`, 942 |
| `05-safety-privacy-regulatory/` | 6,019 | 11 fragments, 6,019 in all | largest `040-basis.html`, 1,845 |
| `06-architecture/` | 3,076 | 11 fragments, 3,076 in all | largest `090-cost.html`, 431 |
| `07-route-a-direct-to-parents` | 1,847 | one file, 1,847 | |
| `08-route-b-through-schools` | 2,100 | one file, 2,100 | |
| `09-route-comparison` | 2,276 | one file, 2,276 | |
| `10-economics` | 2,081 | one file, 2,081 | |
| `11-roadmap` | 2,235 | one file, 2,235 | |
| `12-risk-register` | 2,127 | one file, 2,127 | |
| `13-primer-gateway` | 1,232 | one file, 1,232 | |
| `14-open-items` | 2,342 | one file, 2,342 | |
| `decision-ledger/` | 3,507 | 7 fragments, 3,756 in all | largest `020-taken.html`, 1,569 |
| `index` | 908 | one file, 908 | |
| `sources` | 2,435 | one file, 2,435 | |

Largest fragment file after the split: `src/content/00-thesis.html` at 2,438 words. Fragments over 3,000 words (§3.3 exceptions): none.

## The closure for the kill switch (§3.4)

The kill-switch decisions are D11 (zero-persona operation) and D29 (rehearsed quarterly). The node that carries them is `eng.killswitch`; `gov.licence` carries the SLA, D5, D9 and D29.

```
$ python3 tools/depmap.py impact eng.killswitch
eng.killswitch: Kill-switch read path [engine]  stated at 06-architecture#killswitch
upstream, depends on it, transitively: 9
  1  eng.renderer         Style card renderer              02-style-engine#card
  1  ui.chooser           Educator chooser                 02-style-engine#preset
  2  svc.composer         Composer                         06-architecture#turn
  3  svc.generator        Generator                        06-architecture#turn
  3  ui.session           Session canvas                   01-product#session
  4  svc.verifier         Verifier                         06-architecture#verifier
  5  svc.gate             Gate                             06-architecture#turn
  6  svc.logger           Turn logger                      06-architecture#data
  6  ui.refusal           Refusal notice                   01-product#blocked
downstream, it depends on, transitively: 3
  1  db.presets           Preset registry                  06-architecture#data
  1  ext.cdn              CDN and store metadata           04-rights-dossier#killswitch
  1  gov.licence          Licence and kill-switch SLA      04-rights-dossier#killswitch
edit plan, 9 fragment(s) in document order:
  src/content/01-product/030-session.html
      #session: ui.session (up 3)
  src/content/01-product/060-blocked.html
      #blocked: ui.refusal (up 6)
  src/content/02-style-engine/030-card.html
      #card: eng.renderer (up 1)
  src/content/02-style-engine/040-preset.html
      #preset: ui.chooser (up 1)
  src/content/04-rights-dossier/060-killswitch.html
      #killswitch: ext.cdn (down 1), gov.licence (down 1)
  src/content/06-architecture/020-turn.html
      #turn: svc.composer (up 2), svc.gate (up 5), svc.generator (up 3)
  src/content/06-architecture/030-verifier.html
      #verifier: svc.verifier (up 4)
  src/content/06-architecture/060-data.html
      #data: db.presets (down 1), svc.logger (up 6)
  src/content/06-architecture/070-killswitch.html
      #killswitch: eng.killswitch (this)
```

## The fourth check (§2.3)

Left out. A Verified marker is `<span class="mark verified">Verified</span>` (52 in the fragments) with no `href` and no attribute naming a register entry, and `evidence/sources.html` has no per-entry anchor (each entry is a table row whose id sits in a cell, not in an `id` attribute). "Every Verified marker links a register entry" therefore has nothing mechanical to check. Every `href` into `evidence/sources.html`, with any anchor it carries, is checked by the second check.

## Loci

One line per node: id, stratum, label, locus. Judgement calls: stores are placed where the pages state the record, not all in `06-architecture#data` (the item bank at `03#scope`, validation records at `03#validation`, the child-facing stores at `05#data`, mastery state at `05#basis`, escalation records at `05#gaps`); obligations are placed where the obligation is argued, so `gov.pinned` sits at `03#harness` where D22 is applied and `gov.provenance` at `04#india` where the IT Amendment Rules are stated; `gov.outcome` sits at `04#naming`, the only section that names the advertising and consumer regime.

```
gov.floors           obligation     Accuracy floors                  03-curriculum-and-content#floor
gov.cleanroom        obligation     Clean-room rule                  03-curriculum-and-content#cleanroom
gov.provenance       obligation     Provenance labelling             04-rights-dossier#india
gov.p2               obligation     Promise P2                       01-product#promise
gov.pinned           obligation     Pinned versions                  03-curriculum-and-content#harness
gov.licence          obligation     Licence and kill-switch SLA      04-rights-dossier#killswitch
gov.childrenscode    obligation     Children's code and UK GDPR      05-safety-privacy-regulatory#code
gov.osa              obligation     Online Safety Act scoping        05-safety-privacy-regulatory#osa
gov.zeroretention    obligation     Zero-retention terms             05-safety-privacy-regulatory#data
gov.outcome          obligation     Outcome-claim discipline         04-rights-dossier#naming
ui.session           surface        Session canvas                   01-product#session
ui.refusal           surface        Refusal notice                   01-product#blocked
ui.check             surface        Unaided check                    01-product#session
ui.chooser           surface        Educator chooser                 02-style-engine#preset
ui.adjust            surface        Style controls                   02-style-engine#adjust
ui.paper             surface        Practice paper                   03-curriculum-and-content#papers
ui.grade             surface        Grade range display              05-safety-privacy-regulatory#graderange
ui.parent            surface        Parent report                    01-product#parent
ui.onboard           surface        Adult verification               05-safety-privacy-regulatory#age
ui.school            surface        School console                   08-route-b-through-schools#data
ui.marketing         surface        Marketing site                   05-safety-privacy-regulatory#line
svc.composer         orchestration  Composer                         06-architecture#turn
svc.generator        orchestration  Generator                        06-architecture#turn
svc.verifier         orchestration  Verifier                         06-architecture#verifier
svc.gate             orchestration  Gate                             06-architecture#turn
svc.fallback         orchestration  Validated-item fallback          06-architecture#turn
svc.logger           orchestration  Turn logger                      06-architecture#data
svc.summariser       orchestration  Rolling summariser               06-architecture#cost
svc.adjudication     orchestration  Adjudication queue               03-curriculum-and-content#harness
svc.escalation       orchestration  Escalation routing               05-safety-privacy-regulatory#content
svc.caps             orchestration  Session caps                     06-architecture#planes
svc.billing          orchestration  Billing and entitlement          06-architecture#planes
svc.reporting        orchestration  Progress reporting               01-product#parent
eng.retrieval        engine         Deterministic retrieval          06-architecture#turn
eng.figure           engine         Figure renderer                  06-architecture#figures
eng.cas              engine         Computer algebra check           06-architecture#verifier
eng.citation         engine         Citation presence                06-architecture#verifier
eng.entail           engine         Claim support                    06-architecture#verifier
eng.scope            engine         Scope classifier                 06-architecture#verifier
eng.renderer         engine         Style card renderer              02-style-engine#card
eng.killswitch       engine         Kill-switch read path            06-architecture#killswitch
eng.signature        engine         Signature extraction             02-style-engine#conformance
eng.mastery          engine         Mastery model                    06-architecture#derived
eng.paperasm         engine         Paper assembler                  06-architecture#derived
eng.grademap         engine         Grade range mapper               06-architecture#derived
eng.classifier       engine         Safety classification            06-architecture#planes
db.items             data           Item bank                        03-curriculum-and-content#scope
db.objectives        data           Objective graph                  06-architecture#data
db.validation        data           Validation records               03-curriculum-and-content#validation
db.presets           data           Preset registry                  06-architecture#data
db.styleobj          data           Style objects                    02-style-engine#set
db.licences          data           Licence register                 06-architecture#data
db.snapshot          data           Preset snapshot                  06-architecture#data
db.turns             data           Session and turn log             05-safety-privacy-regulatory#data
db.mastery           data           Mastery state                    05-safety-privacy-regulatory#basis
db.grade             data           Grade range record               06-architecture#derived
db.papers            data           Paper store                      06-architecture#derived
db.learner           data           Learner profile                  05-safety-privacy-regulatory#data
db.accounts          data           Account record                   05-safety-privacy-regulatory#data
db.escalations       data           Escalation records               05-safety-privacy-regulatory#gaps
ext.dfe              supply         DfE subject content              03-curriculum-and-content#cleanroom
ext.board            supply         Board paper structure            04-rights-dossier#line
proc.authoring       supply         Item writers                     03-curriculum-and-content#cleanroom
proc.validators      supply         Examiner validators              03-curriculum-and-content#validation
proc.raters          supply         Style raters                     02-style-engine#preset
proc.creator         supply         Creator review right             04-rights-dossier#creator
ext.genvendor        supply         Generator vendor                 06-architecture#model
ext.verifyvendor     supply         Verifier vendor                  06-architecture#model
ext.ageassurance     supply         Age assurance provider           05-safety-privacy-regulatory#age
ext.safetyvendor     supply         Classifier vendor                06-architecture#planes
ext.billingvendor    supply         Payments                         04-rights-dossier#wargame
ext.cdn              supply         CDN and store metadata           04-rights-dossier#killswitch
ext.schoolidp        supply         School identity provider         08-route-b-through-schools#data
```

## Checks at the gate

```
$ python3 src/build.py --check
build is fresh

$ python3 tools/verify.py
1. build freshness
   build is fresh
2. links and anchors
   1166 links in 20 files, 0 broken
3. dependency map
   depmap: 73 nodes, 129 edges, every locus resolves, served page agrees
4. Verified markers link a register entry: not mechanical, not run (see the docstring)
verify: all checks pass

$ python3 tools/depmap.py check
depmap: 73 nodes, 129 edges, every locus resolves, served page agrees
```

`CLAUDE.md`: 53 lines, headings no deeper than `##`, the nine rules of §2.4 in order. `tools/split_fragment.py`: deleted.

## Fresh-session test question

Question for a fresh session: "What must I do before editing the kill-switch section of architecture?"

The answer it should give: run `python3 tools/depmap.py impact eng.killswitch` first (the dependency rule), and open the fragments it names in the order printed, starting with `src/content/06-architecture/070-killswitch.html`; edit only under `src/content/`, never `docs/`; the section applies D11 and D29, and D11 is a settled decision in `BUILD_BRIEF.md` §2, so neither is reopened; then `python3 src/build.py` and `python3 tools/verify.py`, both passing before the commit.
