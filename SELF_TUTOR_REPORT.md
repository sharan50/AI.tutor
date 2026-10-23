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
| D60 | The self-tutor is the learner's alone: it plays behind the learner's own passcode, no surface of the product shows it to anyone else, and nothing it renders can be shared, exported or downloaded |
| D61 | Live capture only, head and shoulders and a prompted voice sample, with a liveness check; no uploads and no full-body image |
| D62 | Separate, explicit consent from the verified adult and the learner; off by default |
| D63 | Delete at any moment; rendering stops at the next turn; primary stores within seven days; clips never stored; also deleted when the account closes or after twelve months unused |
| D64 | Speaks only gated text, rendered after the verifier from the on-screen text; every clip labelled as synthetic; no claim to be the learner, no comment on their face or voice, no filter; safeguarding replies only as text from the standard tutor |
| D65 | No weights trained on a learner; render-time conditioning only |
| D66 | Every archetype; a named educator's preset only where that creator opts in through a new licence term (Schedule 4) |
| D67 | Families buying directly only (Route A) at launch; through schools it stays off until counsel answers OI-23 for a school as controller |
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
- **Dependency map.** Ten nodes and 28 edges. Five "governs" edges from the facets
  work were turned round to match the other 43.
- **Tooling and structure:**
  - `14-open-items` was over the 3,000-word limit. It is now a directory whose
    fragments reproduce the old page byte for byte; the built page was unchanged by
    the split. The evidence register was over the limit too, and is split the
    same way.
  - `build.py` no longer crashes when a key block above a page's first section is
    too long to transclude on a role page; it links to the page instead. The Tutor's
    longer brief was the first block to reach that case.

## 4. Checks run, and what each returned

| Check | Result |
|---|---|
| `python3 src/build.py` | Exit 0 |
| `python3 tools/verify.py` | All checks pass: build fresh, every link and anchor resolves, map loci resolve (100 nodes, 191 edges), no view or ownership problems |
| Existing markers | Every marker span in every edited source matches `main`, in order; the split register's Verified markers are 3 before and after |
| Verified markers added | None |
| Dashes and American spellings in anything new | None, apart from a source URL |
| Line endings | Unchanged in every edited file |
| Rendering | Every touched page fits at 390 px and 1280 px with no failed request; the new sections checked by eye on desktop |
| Page sizes | Every single-file page stays under 3,000 words; the front page and the Tutor summary stay under their caps |

## 5. The independent review

A fresh agent was given the rules and the change but none of the conversation, and
read everything the work touched. It found 1 blocking problem, 9 that should be fixed
and 5 nits. It also confirmed:
- no Verified marker was added and no existing marker changed;
- the 14 split reproduces the old page;
- the build change is correct;
- every new edge follows the direction used for its kind, and every id is defined.

Every finding was checked in context, and all were fixed.

| # | Finding | What was done |
|---|---|---|
| B1 | Pages promised that no one, the parent included, would ever see or hear the self-tutor, while a parent's subject access right is unconditional and its reach is OI-23. That wrote as if OI-23 were answered | Every page now promises only what the product shows. The parent-facing line keeps its clause on that basis and names what is kept. OI-23 asks how subject access meets D60, including where the parent is the risk (D26) |
| S1 | Clips were "not stored" in one place, cached in another, and purged within seven days in a third | One rule: never stored. Clips are out of every seven-day list, and T-SLF-04 checks that none exists |
| S2 | "At the next turn" sat beside a sixty-second cache | The deleting write clears the cached flag; the ceiling bounds a failed clearing; T-SLF-04 checks both |
| S3 | Five places still said D34 was the only decision taken ahead of counsel; 05 said there was no user-created persona; 20 said no facial image is ever stored; two places said the other thirteen settled decisions stand | Dated sentences were added, leaving the decided claims as written. The age-check sentence is scoped to the age check. The self-tutor now needs the Online Safety Act duties assessment that the trigger list requires |
| S4 | 04 said there is no endorsement to imply and no licence to take, against Schedule 4 and OI-27 | Confined to archetypes and marked as the vault's reading. OI-27 now asks the question |
| S5 | D68 randomised learners, not cohorts; "stays clean" overclaimed; T-SLF-01's outcomes differed between pages | Cohort wording, as D33 requires. The interaction is pre-registered. Outcomes are aligned and include the return rate |
| S6 | Safeguarding replies would be spoken in the child's own voice; learners have no sign-in, so D60 had no boundary against the account holder; subject access could reach a parent who is the risk | Safety turns are text from the standard tutor. A learner's passcode guards the self-tutor (D60), and T-SLF-05 tests the account holder's surfaces. D26 is in OI-23 |
| S7 | `impact gov.provenance` and `impact gov.osa` reached no self-tutor node | Three "governs" edges added |
| S8 | The Tutor brief was 170 words, which took it off the CEO page; the evidence register was over 3,000 words | The brief is trimmed to 149 words without losing the self-tutor. The register is split, and its built page is unchanged |
| S9 | The parent-facing line omitted the derived conditioning and the consent records | Both are named |

The nits were fixed:
- D69's reason;
- the creator opt-in timing in 02, now fifteen minutes for new sessions and the next turn for one in progress;
- marketing demonstrations made outside the product;
- CV-13's reading;
- this report's wording on schools.

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
