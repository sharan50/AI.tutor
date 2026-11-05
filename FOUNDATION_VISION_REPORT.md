# FOUNDATION_VISION_REPORT

What `FOUNDATION_VISION_BRIEF.md` changed, the checks it passed, and what the independent
review found. Written 5 November 2026.

## 1. Outcome

Foundation vision is recorded as the owner decided it on 5 November 2026. It is
Foundation's expanded scope: once the first version, for Reception to Year 2, has passed
its pilot, the same instrument would judge other skills practised at a fixed station,
such as cooking at a counter and playing the piano or keyboard, for pupils of 4 to 18 in
schools and, in parallel, in a home version for families.

- **In schools,** Foundation runs on the school's own servers, and the teacher sees the
  class view, as now. The pupil is shown nothing at any age.
- **At home,** a home unit connects to Foundation's cloud service, and the feedback comes
  through an app. The app shows its feedback to adults, and to a learner of 13 or over
  who holds it; a child under 13 is shown nothing.
- **The camera is the only sensor:** no microphone, and no data from the instrument.
  Whether a camera above a keyboard can see which keys are pressed is untested.
- **Which skills the home version covers is the owner's to scope;** the piano and
  keyboard are the owner's main examples.
- **Nothing of Foundation vision is built** before FM4 decides to build Foundation
  further, and each new skill, age range and the home version then passes its own bench
  test and observed pilot.

The first version does not change, except that it now runs on the school's own servers:
the owner settled the choice F5 had left open. It sits in a new page, F7, in Foundation's
group, linked from the front page's Foundation card. Nothing has been built and no test
has been run.

## 2. The decisions

Recorded in a new ledger fragment, `src/content/decision-ledger/065-foundation-vision.html`.

**The owner's, D130 to D135.** D130, D131 and D133 quote the owner's words; D132, D134 and
D135 record the option the owner chose.

- **D130.** The expansion, after a pilot and proof of concept, to skills with "a certain
  amount of fixed positioning", named Foundation vision.
- **D131.** Two versions: school classes, sold to schools and hosted on-prem, and a home
  version sold to families, connected to the cloud, with feedback through an app.
- **D132.** Camera only: no microphone and no data from the instrument.
- **D133.** First to market for Reception to Year 2; then phases to 4 to 18; a home
  version in parallel, scoped by the owner, with the piano and keyboard as the main
  examples.
- **D134.** The home app's feedback goes to adults and to learners of 13 or over; a child
  under 13 sees nothing.
- **D135.** Everything Foundation does in schools runs on the school's own servers.

**Taken while applying them, the owner's to keep or reverse, D136 to D138.**

- **D136.** The gate: nothing built before FM4; each skill, age range and the home
  version has its own bench test and observed pilot; cheap questions asked at FM1.
- **D137.** The home version keeps the desk unit's guarantees: a dedicated camera with no
  microphone, screen, speaker or light, aimed at the work by an adult; frames read in the
  cloud and discarded; the app a verified adult's, who may add the child's own teacher;
  the record kept as text in the family's account and deletable by the adult.
- **D138.** Foundation never supervises: an adult in the room is responsible wherever a
  skill can hurt.

**Superseded in part, each with a note:** D41's band, for the later phases; D89's "not to
parents and not for home use", for the home version; D90's "or in the cloud", for every
school; D93's "never shows the child anything", for a learner of 13 or over in the home
version.

## 3. What changed

| Where | What |
|---|---|
| F7, new | `f7-foundation-vision/`, eleven fragments, 3,140 words in all, split at its headings once the review's fixes took it past 3,000, and proved byte for byte against the single file: the claim, the order and the gate, a proposed rule for what counts as a fixed station, the school version, the home version, what one camera can and cannot judge, what each skill's catalogue needs, safety and privacy, who pays, and what is not decided. |
| F1 to F6 | F1 gains a section on Foundation vision, a note after the D93 box and a sentence saying which of its statements describe the first version alone. F2's "does not go home" is limited to the first version. F3 gains T-FND-07. F4 and F5 say Foundation runs on the school's own servers (D135), and where they speak of the first version alone. F6 adds who pays at home, the ladder after FM4 with the conditions before any test with a child, and RF6 to RF9. The status tables read "of F7", and the Written lines of all but F4 record the revision. |
| Ledger | D130 to D138 in a new fragment; notes on D41, D89, D90 and D93; the head's breakdown; the decisions not taken lose "where Foundation runs", which D135 settles, and gain "what the home version covers". |
| Registers | OI-33 for the home version, in a new "continued" section of the counsel register, since the first is at its word limit; a sentence each in OI-28 and OI-29 for older pupils, other rooms and the home; OI-13 limited to schools; OA-64 to OA-67; T-FND-07; RF6 to RF9; CV-41 to CV-45. |
| Map | 145 nodes and 343 edges, up from 141 and 332: Foundation vision's scope and gate, the home unit, the home app, and "never supervises". Glosses added and updated. |
| Shared pages and root files | The field research guide's Foundation questions; which idea goes first, where the share box the front page shows, the YC box, the tests row and the document counts are qualified for the first version and F7 (Z1, a departure from the brief); the contents page and the front page's Foundation card; `roles.json` (owners of F7's sections and of the new counsel section, the link, Counsel's frame); `src/build.py` (the page, the group, its blurb and the status page's text); `CLAUDE.md` and the README. |

**Counts, before and after:** documents 32 and 33; decisions 129 and 138; tests 40 and
41; counsel questions 32 and 33, one answered for the Primer; assumptions 58 and 62, of
which 22 and 25 are resolvable by reading or asking; candidates 40 and 45.

## 4. The research, and what the network refused

The research could open no page. The build environment's network refused
www.gov.uk, assets.publishing.service.gov.uk, arxiv.org, papers.neurips.cc,
openaccess.thecvf.com, ico.org.uk, www.federalregister.gov, piano-help.hellosimply.com,
support.yousician.com, help.flowkey.com, help.skoove.com, roli.com and support.roli.com.
Five candidates, CV-41 to CV-45, were therefore recorded from search summaries only, and
each row says so: four practice apps described as listening; a camera product described
as tracking the hands over a keyboard; the Children's code's standard on connected toys
and devices; and two papers that point in opposite directions on reading pressed keys
from video alone. No decision rests on any of them, and no figure from a search summary
is used. Nothing was found that could be cited on what England's curriculum asks for in
cooking or music, so no page says anything about it.

The owner can allow these hosts under Network access in the environment's settings, and
each row can then be checked against its page.

## 5. Checks run, and what each returned

- `python3 src/build.py` exits 0, and `python3 tools/verify.py` passes every check: 5,397
  links in 45 files, none broken; the map has 145 nodes and 343 edges, and every locus
  resolves; the views, owners, frames and the front door pass.
- **Markers.** No Verified marker was added: there are 52, as before. No existing marker
  was changed or removed. Markers were only added, each with the claim it marks:
  Assumed from 188 to 210, Open from 67 to 70, Unknown from 202 to 214.
- **Words.** No fragment passes 3,000 words. F7 was split into eleven fragments when it
  reached 3,099, and the directory, read in filename order, reproduced the single file
  byte for byte (sha256 `35eee893...e7b8`, 22,613 bytes) before the single file went; it
  is now 3,140 words, the longest fragment 510.
  The tightest are the field research guide (3,000), the ledger's `048-ideas.html`
  (2,999), which-first (2,995) and F4 (2,994); the counsel register's first section went
  from 2,999 to 2,884 once OI-33 moved to its own section.
- **Frozen files.** The demonstration's files are unchanged byte for byte.
- **House style.** No em-dashes or en-dashes, and no American spellings, in the new text.
- **Layout.** Every page, the map and the evidence register fit at 390 and 1280 pixels,
  with nothing failing to load.

## 6. Calls made while applying the decisions, the owner's to keep or reverse

- **D136 to D138:** the gate before each phase, the home unit's guarantees, and
  "Foundation never supervises".
- **What counts as a fixed station:** a proposed rule in F7, for the owner to adopt or
  amend. Applying it rules out instruments played at the mouth or under the chin, which
  bring the face into view.
- **The home version:** a dedicated home unit rather than the family's phone; the adult
  may add the child's own teacher; a learner of 13 or over holds the app only with the
  adult's leave, and sees only their own feedback; the home record is kept until the
  adult deletes it or closes the account, and how long it should be kept is listed as not
  decided.
- **On the owner's option text:** the "Camera only" option said a camera gives "no notes
  and no timing". That overstated it. Whether a camera above a keyboard can see which keys
  are pressed is untested, and every page says so.
- **Which idea goes first:** the brief had frozen it, but its share box, which the front
  page shows, said the ideas' ages and buyers all differ, and its YC box said parents do
  not buy Foundation. Both are now qualified for the first version and Foundation vision,
  and its document counts include F7.
- **Reading order:** F6 now leads to F7, and F7 to which idea goes first, rather than F7
  back to F1 as the brief had it.
- **The decisions not taken:** "where Foundation runs" is gone, since D135 settles it, and
  "what the home version covers" is added.
- **Counsel's register:** its first section's lede was tightened to make room, and OI-33
  sits in a "continued" section; OI-13 now says Foundation in schools has no parent
  account.
- **Counsel's view frame** now reads "Foundation's cameras watch pupils from four, and
  children at home", within its 200 words.
- **F6's routes:** the existing exclusion of India for ideas sold direct to families is
  applied to the home version.
- **A pre-existing error fixed:** the map's panel said "the thirteen tests named across
  these documents"; it now names no count, since there are 41.

## 7. The independent review

Fresh agents reviewed the change without the conversation, on four lenses: fidelity to
the owner's words, the vault's rules, children's safety and privacy, and coherence across
pages. A second agent tried to refute every finding.

**Round 1** found 44 items. The second reviewers confirmed 39, nine of them blocking, and
all 39 are fixed under resolutions Z1 to Z28 (the appendix). The blocking ones, in short:

- which idea goes first, and the front page through it, still said parents never buy
  Foundation and that the ideas' buyers and ages all differ;
- F4 and OI-13 still said every Foundation child is under 13 and that Foundation has no
  parent account;
- a sentence on F7 rested on two candidates without its Assumed marker;
- no page said when the home unit runs, or how anyone in the house can tell it is on;
- F7 said the home version keeps the desk unit's guarantees, but the home mount can be
  moved and its frames reach the cloud before the face check;
- the conditions before any test with a child, vetting, consent, assent and a DPIA, were
  written for classrooms, not for homes or older learners.

Among the others: the owner's "lessons and home practice" and "musical instruments" quoted
in full; T-FND-07 now checks that a learner sees only their own feedback and that the app
never opens the phone's microphone or camera; the ledger's heading names the calls taken
while applying; and F7 lists what is not decided about the home unit, its record, its
security and the child's teacher.

**Round 2** looked for blocking defects only. One reviewer followed a child through every
path the design describes: a pupil of 5 in the first version's classroom, a pupil of 15
at a school keyboard, a pupil of 12 in a food room, two pupils sharing a station, a child
of 9 and a learner of 14 at home with a younger sibling, a parent who adds the child's
teacher, and the end of an account. Another checked every page against every other: the
canonical texts, the owner's words in the ledger, the candidates' markers and the counts.
The second found nothing. The first raised three points, and its skeptic judged none
blocking: one was not a defect, and two were real but lesser. All three are applied
anyway, as Z29: T-FND-07 now says a learner of 13 or over sees what is read as their own
work, since the home unit cannot tell a sibling from the learner; F7 says that readings
at a shared station cannot be told apart, and lists whose record they go into as not
decided; and F7's table says a knife hold is read as technique, never as a safety check.
No third round was run.

## 8. What is left for the owner

- **Scope the home version.** Which skills it covers is yours; musical instruments, such
  as the piano and keyboard, are your main examples, and F7 designs only what every skill
  shares.
- **Adopt or amend the fixed-station rule** in F7, and keep or reverse D136 to D138 and
  the calls in section 6.
- **Allow the refused hosts** under Network access in the environment's settings, so that
  CV-41 to CV-45 can be checked against their pages; until then they stay candidates.
- **OI-33** goes to counsel before the home version's pilot, as OI-28 does before the
  classroom's.
- Nothing has been built and no test has been run. The review's last round looked for
  blocking defects only, so lesser ones very likely remain.

## Appendix. Every resolution

- **Z1.** which-first: the share box, the YC box, the tests row and the document counts
  qualified for the first version and F7.
- **Z2.** F4: the first version's children, its service and its accounts said to be the
  first version's.
- **Z3.** The owner's "lessons and home practice" quoted in full in F7, OA-66 and its gloss.
- **Z4.** "Musical instruments, such as the piano and keyboard" as the owner's examples,
  in F7, the ledger's D133 and the decisions not taken.
- **Z5.** The adult's leave for a learner of 13 or over attributed to D137.
- **Z6.** The ledger's heading names the decisions and how they were applied.
- **Z7.** T-FND-07: a learner's own work only, and a check that the app never opens the
  phone's microphone or camera.
- **Z8.** F1: the first version's age band.
- **Z9.** F7: the Assumed marker on the research sentence (CV-44, CV-45).
- **Z10.** The ledger's D134: an Assumed marker for CV-06.
- **Z11.** Reading order kept as F6, F7, which-first, and recorded here.
- **Z12.** The map's home app note gives D137's record in full.
- **Z13.** How the app knows a learner's age: the limit recorded in D134, and listed as not
  decided in F7.
- **Z14.** OI-33 in a new counsel section, asking also about transparency with no light,
  the cloud service's location and the household; OI-28 and OI-29 reach the home unit;
  OI-13 limited to schools; Counsel owns the new section.
- **Z15.** F6's conditions before a test with a child apply to every bench test and pilot of
  Foundation vision, at school and at home; F4's gap 5 adds the home.
- **Z16 to Z19.** F7: the home mount and the cloud, the sibling at the unit, a shared
  station, and four items not decided (when the unit runs, the child's teacher, the home
  record, where the cloud runs and how the unit is kept secure).
- **Z20, Z22 and Z23.** F7's table: instruments at the mouth or chin, and drawing; and what
  would end Foundation vision, or a part of it.
- **Z21.** The field research question for OA-67 names the cloud.
- **Z24.** The assumptions' lede counts Foundation vision's four.
- **Z25.** F5's sign-in row limited to schools.
- **Z26.** The status page's text names F7.
- **Z27.** F1, F2, F3, F5 and F6 record the revision; F4 had no room.
- **Z28.** F7 split into fragments, proved byte for byte.
- **Z29.** Round 2's three points: T-FND-07 speaks of what is read as a learner's own work;
  a shared station's readings cannot be told apart, and whose record they go into is not
  decided; a knife hold is read as technique, never as a safety check.
