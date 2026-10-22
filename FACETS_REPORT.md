# FACETS_REPORT

What `FACETS_BRIEF.md` changed, the checks it passed, and what the independent
review found and what was done about each finding. Written 22 October 2026.

## 1. Outcome

The vault records three ideas instead of one: the Tutor (14 to 18), the Primer
(8 to 13) and Foundations (4 to 7). The site opens on a front page that
introduces all three, and the first page no longer renders as plain text.

- Nothing in D1 to D14 was reopened and nothing in D15 to D39 was reversed.
- No counsel question was answered or written as answered.
- No Verified marker was added and no existing marker was changed.

Counts after this work, computed by the build:

| | |
|---|---|
| Documents | 30, the registers included |
| Decisions | 58: 14 settled, 44 taken |
| Counsel questions | 20, none answered |
| Assumptions | 34, of which 15 are resolvable by reading or asking |
| Tests specified | 26, none run |
| External claims | 42 registered, plus 12 candidates awaiting the owner's check |

## 2. The plain-text first page

**Cause.** `netlify.toml` rewrote `/` to `/docs/index.html` with status 200.
A rewrite serves the page at the address requested, so the front page was
served at `/`. Its relative `style.css` resolved to `/style.css`, which does not
exist, and every relative link on it resolved against the root as well.

**Fix.** A 302 redirect, so the browser lands on `/docs/index.html` (D52).

**How it was checked.** A local server reproducing both behaviours:
- With the rewrite, the stylesheet request returned 404 and the page rendered
  unstyled.
- With the redirect, the browser ended on `/docs/index.html` with no failed
  request.

Netlify's deploy preview for the pull request processed the redirect and
header rules without errors.

## 3. What was added

- **Twelve documents:** P1 to P6 for the Primer and F1 to F6 for Foundations.
  Each is a first draft, revised once after the independent review, and its
  head says so.
- **Two shared pages:**
  - Which idea goes first. Foundations does not (D42). The Tutor or the Primer
    is decided by one rule written down in advance, on `which-first#open`.
  - A field research guide for teachers, professors and parents.
- **Registers:**
  - Decisions D40 to D58. D40 to D53 were taken with the owner; D54 to D58 were
    taken while writing and are the owner's to keep or reverse.
  - Counsel questions OI-13 to OI-20.
  - Assumptions OA-22 to OA-34.
  - Candidates CV-01 to CV-12, in their own section of the evidence register
    (D53).
- **The front page.** A brief on each idea, transcluded from its thesis, and a
  labelled space for a short film of each. Below the cards: which idea goes
  first, what the three share, what happens next, the computed counts, and
  links to the documents and owner views. The Tutor's summary moved to
  `docs/tutor.html`.
- **Navigation.** The switcher, the contents page and the status page group
  pages by idea.
- **Stylesheet**, edited at the owner's request (D52): accents for each idea,
  the front page, brief boxes and film spaces, in light, dark and print.
- **Tooling:**
  - `GROUPS` lists each idea's pages by slug, and `verify.py` checks that the
    groups partition the pages.
  - The front page and the Tutor summary get the same checks: the digit rule,
    the word cap and the frame.
  - There is a fifth reader route.
  - Film settings are escaped and validated, and embedded films add only their
    own origin to the content security policy.
  - The status page finds each test's description from its defining row; the
    Tutor's descriptions were blank before.
  - The dependency map gains 17 nodes for the new components.

## 4. Checks run, and what each returned

| Check | Result |
|---|---|
| `python3 src/build.py` | Exit 0, no warnings |
| `python3 tools/verify.py` | All checks pass: build fresh, every link and anchor resolves, map loci resolve, no view or ownership problems, groups partition the pages |
| Page linter (house style, ids, anchors, ranges, Verified markers) on all fourteen new pages | 0 problems |
| Verified markers in new files | None |
| Existing markers | Every marker span in every edited source matches `main` |
| Em-dashes and en-dashes in anything new | None |
| Front page | Under 1,200 words; no figure outside a computed count or key block; frame under 150 words |
| Rendering | Front page checked in light and dark at desktop width and at 390 px; no failed requests |

## 5. The independent review

A fresh agent, given the rules and the diff but none of the conversation, read
everything the branch changed. It found 5 blocking problems, 24 that should be
fixed, and a list of nits. It also confirmed that the mechanical rules held: no
Verified marker added, no existing marker changed, no dashes, and no American
spellings. Every finding was checked in context before it was acted on.

| # | Finding | What was done |
|---|---|---|
| B1 | Two different "written in advance" rules decided whether the Primer goes first | Fixed. There is one rule, on `which-first#open`, with the Tutor's half defined (M1 leaves C1 and C2 of 09 standing) and one tie-break. P6 points to it, and so does D58 |
| B2 | Candidate claims used without an Assumed marker | Fixed on every page that relies on one, and in D41 and D42 |
| B3 | Claims about YC's request beyond CV-01, and "more honest" | Fixed. YC's request is described only in CV-01's terms. F1 now says "more modest about what a screen can do" |
| B4 | "a parent buying a thinking companion" | Fixed: "a tutor for their child's questions" |
| B5 | The showcase transcript invited the child back and praised one view | Fixed in P2: a plain close, a neutral acknowledgement, and an annotation saying the same reply follows either view |
| S1 | The parent's record could expose a child's question | D48 amended: a declined or switched-off question appears by category, not its words; the child is told beforehand what a parent can see; the residual risk is named in P4 and routed to OI-14 and RP4 |
| S2 | The map let the parent view read escalation records, and no test enforced withholding | Fixed. The edge is removed. New blocking test T-PRM-08 covers the whole flagged exchange, including the Primer's own reply |
| S3 | Foundations' question box for the adult had no safety path | D54 narrowed: no free-text box anywhere; the adult opens reviewed explanations instead |
| S4 | "Suggests a health professional", triggered by the record, contradicted D56 | Fixed. Static advice is always available and never triggered by tap data |
| S5 | Pilots with children lacked basic safeguards | Fixed in P6, P4, F6 and F4: vetting, a second adult or a parent, the child's assent and a way to stop, a DPIA first, and retention |
| S6 | The bereavement reply assumed a family structure and claimed feelings | Fixed in P2, and marked for a specialist's review |
| S7 | P4 had no inventory of the data held | Fixed: a data table on F4's pattern |
| S8 | The Primer's age bands bypassed 05's age design | D57 amended: age in years from the verified adult, a recorded departure from 05, and the limit stated. P4, P3 and P5 aligned |
| S9 | P2 promised in the form D21 forbids | Fixed. Promises follow 01's pattern; D21 carries over to T-PRM-01 |
| S10 | The owner's assumptions were stated as fact, including on the front page | Fixed. The reasons are marked as the owner's, with OA-28 and OA-29 |
| S11 | The front page promised an outcome P2 does not | Fixed on the front page, the contents page and the P1 brief |
| S12 | A human-run pilot cannot test whether AI does this well | OA-23 split: the child's half is tested at PM3, the AI's at PM4 |
| S13 | A default-on module contained sensitive questions | Fixed in P3 and P2 |
| S14 | The clean room clashed with D55's reasoning | Fixed. F3 states the tension, and the adult uses the school's words where known |
| S15 | F3 overclaimed that the guidance is correct | Fixed. It now claims checks only where a rule can make them |
| S16 | P1's competitor table was unmarked | Fixed: marked Assumed and softened, with an added weakness that the category is unsurveyed |
| S17 | D50 called a voice recording a voiceprint | Fixed: "a voiceprint derived from it is personal information" |
| S18 | Stale counts on the contents page and page 14 | Fixed. Five routes; "none answered" |
| S19 | The map panel showed blank text for new decisions | Fixed. Entries are in the right tables, the new questions and assumptions are added, and sorting is natural |
| S20 | New pages did not state their maturity | Fixed. Every new page has a Maturity line, and the status page's wording is updated |
| S21 | The field research guide broke its own rules | Fixed. The closing questions moved to the end, hypotheticals were rewritten as past behaviour, and the OA-21 line was corrected |
| S22 | The film placeholders implied built products | Fixed. "Film to come", an illustrative caption on every film, grammar fixed, the play button replaced, and README rules on labelling and consent |
| S23 | F4 and P4 miscounted their counsel questions and omitted OI-20 | Fixed |
| S24 | `GROUPS` was assigned by slug prefix | Fixed. Listed by slug, with a partition check in `verify.py` |

The nits were fixed:
- the brief-state line on the Primer card;
- the footer date;
- this report, which did not exist;
- escaping, type and https checks for films;
- the status page's risk card and its standfirst;
- the reversals wording in the README;
- the candidates' "Used in" column;
- D45's "mode";
- six which-first points;
- the Foundations worked example;
- the "For the team" heading, now "Owner views", with the owner named on the front page;
- the remaining wording points on the Primer and Foundations pages.

One point was left as it was, with the reason. F4's line on how the Children's code
was read states the vault's own reading, not CV-06's content, so it needs no
candidate marker. The working-position line earlier on F4 does carry one.

## 6. The brief's acceptance bar

1. The build and the checks pass, with no warnings about the front page. **Met.**
2. Every id the brief names appears where the brief puts it. **Met.** The
   brief was updated for what writing and review added: D54 to D58, OI-19,
   OI-20, OA-33, OA-34 and T-PRM-08.
3. No Verified marker added, no existing marker changed, no counsel question
   answered, no dashes. **Met.**
4. The root URL lands on a styled front page with no failed requests. **Met**
   locally; Netlify's preview processed the redirect without errors.
5. An independent review, with every finding fixed or answered here. **Met.**

## 7. What is left for the owner

- **Check the twelve candidates** in the evidence register and promote those
  that hold. Allowing `www.ycombinator.com`, `ico.org.uk`, `www.gov.uk`,
  `www.legislation.gov.uk` and `educationendowmentfoundation.org.uk` in the
  environment's network settings would let a session read the primary sources.
- **Keep or reverse D54 to D58**, taken while writing.
- **Adopt or amend the two proposed rules:** the go-first rule on
  `which-first#open`, and Foundations' FM4 rule in F6.
- **Write the go-first thresholds before PM1** (D58).
- **Add the films** when they exist, under the rules in the README.
- **Run the field research**, and record each answer against its id.
