# SELF_TUTOR_REPORT

What `SELF_TUTOR_BRIEF.md` changed, the checks it passed, and what the independent
review found. Written 23 October 2026.

## 1. Outcome

The Tutor is designed to launch with a self-tutor. A learner may choose to be taught
by a tutor with their own face and voice, in any style the product offers, with
nothing trained on them. Every Tutor document it touches now says how it works.

Three things did not happen:
- No counsel question was answered.
- No Verified marker was added, and no existing marker was changed.
- No benefit is claimed for the self-tutor anywhere.

The self-tutor proceeds ahead of counsel's answers on OI-23 to OI-27 under D59's
rule. It is withdrawn in a market only if counsel advises in writing that no form of
it may launch there. Every page that applies the rule says so, as D34 does for OI-3.

Two settled decisions have now been amended by the owner:
- **D1**, on 22 October.
- **D9**, today. Cloning a creator's voice, or anyone's but the learner's own, stays
  off the launch path; the learner's own voice in the self-tutor is on it.

The ledger records the D9 amendment as what it is: a re-opening on the owner's
preference and an unverified view (OA-38), overriding the ledger's own rule for D9
alone.

Counts after this work, computed by the build:

| | |
|---|---|
| Decisions | 69: 14 settled (two since amended by the owner), 55 taken |
| Counsel questions | 27, none answered |
| Assumptions | 40, of which 17 are resolvable by reading or asking |
| Tests specified | 32, none run |
| External claims | 42 registered, plus 15 candidates awaiting the owner's check |

## 2. The owner's decisions and the defaults

**The owner's decisions, 23 October 2026:**
- Voice, image and style are all included.
- The Tutor launches with the self-tutor.
- Counsel's questions are logged, and only a categoric no stops it (D59).
- The owner's view of Ofcom is recorded as OA-38, beside the vault's existing
  working position (OI-4).

**Taken while writing, for the owner to keep or reverse:**

| | Decision |
|---|---|
| D60 | The self-tutor is the learner's alone: no parent, school, creator or other user sees or hears it, and nothing it renders can be shared, exported or downloaded |
| D61 | Live capture only, head and shoulders and a prompted voice sample, with a liveness check; no uploads and no full-body image |
| D62 | Separate, explicit consent from the verified adult and the learner; off by default |
| D63 | Delete at any moment; rendering stops at the next turn; primary stores within seven days; also deleted when the account closes or after twelve months unused |
| D64 | Speaks only gated text, rendered after the verifier from the on-screen text; every clip labelled as synthetic; no claim to be the learner, no comment on their face or voice, no filter |
| D65 | No weights trained on a learner; render-time conditioning only |
| D66 | Every archetype; a named educator's preset only where that creator opts in through a new licence term (Schedule 4) |
| D67 | Families buying directly only (Route A) at launch; schools later |
| D68 | A second factor in D14's experiment, not a third arm |
| D69 | No style dimension reaches the voice: one neutral delivery under every preset |

## 3. What was added

- **01 Product.** The self-tutor section: turning it on, the session, the controls,
  and the six tests T-SLF-01 to T-SLF-06. Also the label wording for a named preset
  in a self-tutor, a line on the parent report, and two lines in what the product
  does not do.
- **02 Style engine.** The likeness carries no style; named presets by opt-in; D68
  and D69.
- **04 Rights dossier.** The learner's own likeness, the misuse case, the opt-in
  term, and labelling as a question (OI-26). The creator licence table, the kill
  switch and the India section are updated.
- **05 Safety, privacy and regulatory.** A child's face and voice:
  - what is held, the two consents, the Children's code, Ofcom with the owner's view
    marked, the US, safeguarding and wellbeing;
  - new data rows, with clips not stored;
  - one sentence in the parent-facing line, the standards it engages, and a DPIA
    before launch;
  - trigger T9: nobody but the learner sees or hears a self-tutor.
- **06 Architecture.** Rendering after the gate, the likeness store, the fallback
  chain, deletion on the kill switch's mechanics, the vendor rules, and the render
  cost as an Unknown.
- **07, 08, 10, 11 and 12:**
  - 07 and 08: pricing and marketing rules, and schools off at launch;
  - 10: the render cost per turn as an Unknown input;
  - 11: M1's counsel questions, M2's release gates and D68 in the D14 design;
  - 12: risks R12 to R15.
- **Registers.**
  - Decisions D59 to D69.
  - Counsel questions OI-23 to OI-27.
  - Assumptions OA-37 to OA-40, with OA-40 resolvable by asking parents.
  - Candidates CV-13 to CV-15: the adjacent research, none of which tests the
    question directly.
- **Shared pages.** The thesis and the front-page brief name the self-tutor. Which
  idea goes first and the field research guide gain a line each.
- **Contracts.** Schedule 4 in the heads of terms, and a line in the term sheet.
- **Dependency map.** Ten nodes and 25 edges. Five "governs" edges from the facets
  work were turned round to match the other 43.
- **Tooling and structure:**
  - `14-open-items` was over the 3,000-word limit. It is now a directory whose
    fragments reproduce the old page byte for byte; the built page was unchanged by
    the split.
  - `build.py` no longer crashes when a key block above a page's first section is
    too long to transclude on a role page; it links to the page instead. The Tutor's
    longer brief was the first block to reach that case.

## 4. Checks run, and what each returned

| Check | Result |
|---|---|
| `python3 src/build.py` | Exit 0 |
| `python3 tools/verify.py` | All checks pass: build fresh, every link and anchor resolves, map loci resolve (100 nodes, 188 edges), no view or ownership problems |
| Existing markers | Every marker span in every edited source matches `main`, in order; the split register's Verified markers are 3 before and after |
| Verified markers added | None |
| Dashes and American spellings in anything new | None, apart from a source URL |
| Line endings | Unchanged in every edited file |
| Rendering | Every touched page fits at 390 px and 1280 px with no failed request; the new sections checked by eye on desktop |
| Page sizes | Every single-file page stays under 3,000 words; the front page and the Tutor summary stay under their caps |

## 5. The independent review

To be completed when the review returns.

## 6. What is left for the owner

- **Keep or reverse D60 to D69**, especially:
  - D61: no full-body image;
  - D66: named styles by opt-in only;
  - D67: schools off at launch.
- **Instruct counsel on OI-23 to OI-27 at M1.** A categoric no in a market removes
  the self-tutor there; a conditional answer changes the design.
- **Write T-SLF-02's false-accept threshold before M2 begins.**
- **Choose the speech and animation vendor at M2.** If it would handle a learner's
  face or voice outside India and the UK, the parent-facing line changes before
  launch.
- **Check candidates CV-13 to CV-15** and promote those that hold.
- **Ask parents about consent (OA-40)** during the field research.
