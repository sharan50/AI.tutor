# AI.tutor: the Primer and Foundations brief

Commit this file at the repository root as `FACETS_BRIEF.md`. It records what
the owner decided in a conversation on 22 October 2026 and turns it into
instructions a fresh Claude Code session can execute. Everything binding is in
this file; nothing depends on conversation history.

`BUILD_BRIEF.md` remains the source instruction for the Tutor and for the rules
of the vault. This brief governs the Primer, Foundations, the pages shared by
all three ideas, and the front page. Where the two disagree about the Tutor,
`BUILD_BRIEF.md` governs.

## 0. Mission

The vault recorded one idea, the Tutor: an AI tutor for UK secondary students
preparing for GCSE and A-level. The owner has two more and wants all three in
the same repository and on the same site, because the site is the venture's
working space and the material its accelerator applications are built from
(a16z speedrun, Y Combinator and South Park Commons, at the time of writing).

Three outcomes.

1. **Two new ideas, each with six documents.** The Primer, for ages 8 to 13,
   and Foundations, for ages 4 to 7. Written to the vault's standard of
   marking, with honest maturity: the Tutor's documents went through eight
   adversarial rounds, these through none, and every page says so.
2. **A front page for a first-time reader.** A former teacher, a prospective
   partner or co-founder, an accelerator reviewer: a brief on each idea and a
   space for a short film of each. The Tutor's current summary moves to its
   own page, unchanged in substance.
3. **The first page stops rendering as plain text.** `netlify.toml` rewrote `/`
   to `/docs/index.html` with status 200, so the page was served at the root,
   its relative stylesheet and links resolved against the root, and all of
   them failed. It becomes a 302 redirect.

The three ideas are recorded as separate products that may share one platform.
Whether they are one product, and whether the Tutor or the Primer goes first,
are deliberately not decided. Field research with teachers, professors and
parents decides them, and the vault gains a guide for it.

## 1. Fixed constraints

1. D1 to D14 stand and are not reopened. D15 to D39 stand; nothing here
   reverses one. D1 governs the Tutor; D51 covers the two ideas D1 did not
   contemplate and says so.
2. Counsel questions stay open: OI-1 to OI-12, and the eight this brief adds,
   OI-13 to OI-20. Nothing is written as though one were answered. OI-3 is the
   recorded exception under D34.
3. House style is `BUILD_BRIEF.md` §7: British English; no em-dashes and no
   en-dashes (write "4 to 7", not a dash); conclusions before reasoning; if
   something is weak, say it is weak.
4. Markers. Every number is from the evidence register, a stated design
   choice, or marked Unknown. No session adds a Verified marker anywhere. A
   new external claim goes into the register as a candidate (D53) and text
   relying on it carries an Assumed marker that names it. Where a new page
   relies on a fact the Tutor's pages already state with a Verified marker, it
   links to that statement and does not restate it with a marker. No existing
   marker is changed.
5. Edit `src/`, `roles.json`, `tools/depmap/graph.json` and root files, never
   `docs/`, `evidence/` or `viz/` by hand. Python 3 standard library only.
6. Page 13, the Primer gateway, stays where it is and keeps its content. It
   gains one note: the Primer is now also designed as a separate product, and
   which of the two relationships holds is not decided. Its principles and
   release gates bind the Primer either way.
7. A fragment over 3,000 words of prose is split at its `<h2>` headings. New
   pages are written to stay under it, as single files.

## 2. What the owner decided

- **Three ideas with a theme in common, possibly three separate products.**
  The Tutor revolutionises, or at least augments, exam tutoring and much of
  edtech; Foundations teaches early reading, writing and arithmetic; the
  Primer is a true tutor in the sense of Aristotle to Alexander, or Chanakya to
  Chandragupta, for children of about eight and above.
- **Ages:** Foundations 4 to 7, the Primer 8 to 13, the Tutor 14 to 18.
- **Foundations does not go first.** The owner's reasons, in substance: a
  five-year-old will not sit still to be taught by a screen; reading and
  writing are taught physically, a person guiding a child's finger along print
  and forming letters with them, building a link between hand and mind; a
  person also manages the child, which is half of teaching one at that age;
  schools already teach this for free, so routes to revenue are fewer; and the
  risk that it does not work is too high. It needs much deeper thought. An
  adult is always present.
- **The Primer is the lower risk of the two new ideas in one sense:** it is
  genuinely different, it is something an AI can do well, and its age suits a
  tool that is only a screen. (The documents add the risks that are higher for
  the Primer: why a parent pays, reputation, and proof.)
- **The Primer is modular.** Parents switch modules on and off. Parents cannot
  add their own views, because that opens the product to extremism and other
  harm, introduced consciously or not. Everything comes from the company.
  Parents can submit ideas and requests, and that is all.
- **Markets:** the UK and the US at the same time is the preference; the UK
  first if resources are a constraint. India is held back.
- **Y Combinator:** the owner disagrees with YC's preference for basic skills
  first. YC's request is paraphrased, marked Assumed and cites the page; its
  primary text could not be opened from the build environment.
- **The site:** a front page with a brief on each idea and a space for an AI
  video of each; the stylesheet may be edited.

## 3. Decisions D40 to D58

Recorded in `src/content/decision-ledger/048-ideas.html`, section id `ideas`,
in the ledger's `<dl class="defs">` form, all dated 22 October 2026. The link
at the end of each is the last link in its entry; it decides the entry's owner.
D40 to D53 were taken with the owner. D54 to D58 were taken while writing the
Primer and Foundations documents, after the writers raised them, and are the
owner's to keep or reverse.

**D40. The vault records three ideas, the Tutor, the Primer and Foundations, as
separate products that may share one platform.** Driven by: the owner's view
that the three are separate things with a theme in common; the Tutor's design
is mature, and folding the others into it would have forced reversals.
Rejected: treating the Primer and Foundations as stages of the Tutor, as page
13 does for the Primer, which would have reopened the thesis's "not a general
study assistant" and page 13's older-adolescents-first position. Makes harder:
three sets of documents to keep consistent; one platform to design for three
uses; and a reader may take three ideas as a lack of focus, which the front
page answers by saying only one goes first. Link: `which-first.html`.

**D41. Age bands: Foundations 4 to 7, the Primer 8 to 13, the Tutor 14 to 18.**
Driven by: the owner's judgement that a tutor that is only a screen suits a
child who can hold a conversation, from about eight; the Tutor's GCSE and
A-level scope; the Children's code's developmental age ranges (CV-06).
Rejected: YC's single band, reported as 4 to 10 (CV-01); and page 13's view
that the first Primer users should be older adolescents. Makes harder: almost
every Primer and Foundations user is under 13, which brings parental consent
under Article 8 (OI-13) and, in the US, COPPA (OI-15); the Primer spans three of
the code's age ranges. Link: `which-first.html#share`.

**D42. Foundations does not go first.** Driven by: the owner's three reasons. A
child of 4 to 7 needs a person, to hold their attention and to teach the
physical side of reading and writing, which a screen cannot; there are fewer
routes to revenue, because schools already teach it for free; and its risk of
not working is the highest of the three. Rejected: YC's order, in which basic
skills bought by parents are the way in and the thinking Primer the
destination (CV-01). Makes harder: an application to YC argues against the
order YC's own request sets out, and must do it openly. Link:
`which-first.html#foundations`.

**D43. Foundations is designed for an adult beside the child in every session.
The adult is the primary user; the child is the learner.** Driven by: D42's
first reason, and the owner's view that managing a young child is part of
teaching one. Rejected: a child-alone app, the obvious form for the category.
Makes harder: every session costs an adult's time, so the adult's patience is
the real constraint; the product is designed for two people at once; and a
family without the time gets nothing from it. Link:
`f2-foundations-product.html#who`.

**D44. Every factual statement the Primer makes cites a reviewed explanation,
and every philosophical position it presents cites a reviewed inquiry pack
that names the thinker or tradition. A question neither can answer gets an
honest "not yet" and becomes a request for new content.** Driven by: the
Tutor's founding rule, that nothing reaches a learner which cannot be traced
to a checked source, carried into a domain where the risk is influence rather
than a wrong mark. Rejected: answering from the model's general knowledge,
which would make the Primer a free chatbot with a child's interface. Makes
harder: at launch the Primer says "not yet" often, and how often is Unknown
(OA-32). Link: `p3-primer-content.html#sources`.

**D45. The Primer is taught on its modules, not trained on them.** Modules are
retrieved when a turn needs them; no model is fine-tuned on them. Driven by:
page 13's requirement that a harmful module or prompt pattern can be removed in
one operation; D8's reasoning that weights cannot be cleanly revoked; and the
vault's rule to buy the model and own the content. Rejected: fine-tuning on
philosophical and critical-thinking material, which "trained on" first
implied, and which would make a module impossible to withdraw. Makes harder:
depth and voice are capped at what retrieval and prompting achieve. Link:
`p5-primer-architecture.html#model`.

**D46. The Primer's subjects come in modules the company writes and reviews.
Parents switch modules on and off; modules on sensitive subjects start
switched off; each module is written for an age band and offered only within
it. Parents cannot add content or views. They may send ideas and requests,
which go to the company's review and are never shown to anyone else.** Driven
by: the owner's direction and reason, that parent-authored views open the
product to extremism and other harm, introduced consciously or not; page 13's
principle that emotionally charged dialogue is never opened to a child by
default; and the Online Safety Act position in 05, which holds only while
nothing a user creates reaches another user (OI-18). Rejected: parent-authored
values or content; and a fixed catalogue with no parent control. Makes harder:
every module is the company's editorial responsibility, so balance between
viewpoints and reviewer capacity become the bottleneck, as examiner validation
is for the Tutor; and a family the catalogue does not suit can only switch
things off. Link: `p4-primer-safety.html#modules`.

**D47. The Primer names methods, never people.** It may run a Socratic
dialogue, a thought experiment or a story; it never speaks as Aristotle,
Chanakya or any other real person, living or dead. Driven by: putting words in
a real person's mouth misattributes views; a simulated figure is the
companion pattern 05 forbids and the pattern US regulators are examining
(CV-10); the historical tutors are the ambition, not the voice. Rejected:
historical-figure presets, which need no licence and would make the most
memorable demonstration. Makes harder: the Primer gives up a handle comparable
to D4's named educators. Link: `p2-primer-product.html#not`.

**D48. A parent sees an activity record of their child's Primer use: modules
used, questions asked and the views the child recorded. For a child under 13
the full conversation is also available to the parent on request. A turn
flagged for safeguarding is withheld from the parent and routed to a trained
reviewer, as D26 requires. Taken while OI-8 and OI-14 are open; it answers
neither.** Driven by: page 13's adult accountability principle; these users
are younger than the Tutor's; and D26, because the parent is sometimes the
risk. Rejected: applying D16's default to children under 13; and full
transcripts by default at every age. Makes harder: a child may not ask what
they would not want a parent to see, the cost D16 avoids for teenagers; and
the withheld-turn rule must not fail, because a failure exposes a child. Link:
`p4-primer-safety.html#parent`.

**D49. The Primer remembers ideas, not lives:** the questions a child asked, the
views they recorded and the modules they used, and nothing about their family,
friends or feelings beyond the session. Driven by: 05's anti-companionship
constraints, extended to a subject that invites personal disclosure; and the
scrutiny of companion chatbots in the US (CV-10). Rejected: a Primer that
knows the child, the more engaging product and the more dangerous one. Makes
harder: the Primer cannot connect a question to the child's circumstances, as a
human tutor would. Link: `p4-primer-safety.html#memory`.

**D50. Neither the Primer nor Foundations collects a child's voice or image at
launch.** Foundations makes the adult the ears and the eyes: the adult listens,
watches and records what the child did, and there is no microphone and no
camera. The Primer takes typed text; a child who dictates through their
device's own keyboard sends text, never audio. Listening to a child read is a
later feature, separately consented, with no audio retained. Driven by:
speech recognition is least accurate for the youngest children (CV-11); a
child's voice may be biometric data, and is a voiceprint under amended COPPA
(CV-08), which is OI-17; and D43 already puts an adult in the room. Rejected:
listening to the child read from the first day, the feature reading apps are
usually built around. Makes harder: Foundations cannot hear a mistake the adult
misses; the Primer is harder for the youngest typists. Link:
`f4-foundations-safety.html#voice`.

**D51. The Primer and Foundations launch in the UK and the US together where
resources allow, and in the UK first where they do not. D1 continues to
govern the Tutor. India is not pursued for any idea sold direct to families
while section 9(3) of the DPDP Act stands.** Driven by: the owner's
preference and view that the US has proven more receptive (OA-31); the Primer
is not tied to a curriculum, so it travels; and the register's finding on
section 9(3), which prohibits behavioural monitoring of children whatever a
parent consents to. Rejected: the UK alone; and India as a market for the new
ideas. Makes harder: two regulatory regimes from the start (OI-13, OI-15), two
sets of escalation services, and content written for two cultures. D1 was
taken when the Tutor was the only idea; this covers the two it did not
contemplate, and its fallback follows D1's reasoning. Link:
`p6-primer-plan.html#routes`.

**D52. The site opens on a front page that introduces the three ideas, each
with a brief and a space for a short film; the Tutor's summary moves to its
own page; the root URL redirects to the front page instead of rewriting to
it; and a session may edit the stylesheet when the owner asks for a design
change.** Driven by: the owner's direction that the first page a former
teacher, partner or co-founder sees should explain the three ideas and how
each looks; and a defect, described in §0. Rejected: keeping the Tutor's
summary as the front page; and a root-level copy of the front page with
rewritten paths, a second copy to keep in step. Makes harder: the front page
shows three ideas at very different maturity and must say so; a film added
later either loosens the content security policy for one origin or adds a
large file to the repository. No link to a document; the entry is owned with
its ledger section.

**D53. External claims found by research but not yet checked by the owner are
registered as candidates, numbered CV, in their own section of the evidence
register. Text relying on one carries an Assumed marker naming it. Candidates
are not counted as registered claims, and only the owner promotes one.**
Driven by: the build environment could not open primary sources; and the rule
that a session never adds a Verified marker. Rejected: leaving new claims
unregistered and untraceable; and counting them with the September 2026
claims, which would overstate what has been checked. Makes harder: a second
list to keep; promotion is a manual step. Link:
`../evidence/sources.html#candidates`.

**D54. Foundations has no generative model in the session path.** Everything the
adult reads during a session was written, reviewed and checked before it began,
and is chosen by inspectable rules from the reading record; a model may help
writers draft offline and answer the adult's questions between sessions through
the verifier. D27's reasoning carried one step further. Link:
`f5-foundations-architecture.html#reuse`.

**D55. For a child in school, Foundations practises what the school has taught
and never teaches ahead of it; for a child not yet in school it follows its own
sequence.** It depends on OA-33. Link: `f3-foundations-content.html#sequence`.

**D56. The Foundations record holds what the adult tapped and nothing else:** no
free-text notes about the child, and no inferred difficulty, need or condition.
Link: `f4-foundations-safety.html#data`.

**D57. Within its band, the Primer's settings follow the Children's code's age
ranges: 8 and 9, 10 to 12, and 13.** Modules on sensitive subjects are written
for 10 and over, so a child of 8 or 9 is offered none. Link:
`p4-primer-safety.html#ages`.

**D58. The thresholds that decide whether the Primer goes first are written down
before PM1 begins**, as D37 wrote down the thresholds for the Tutor's route.
Link: `p6-primer-plan.html#first`.

## 4. Decisions deliberately not taken

Rows added to the ledger's `unresolved` table.

| Not decided | Why not |
|---|---|
| Which idea goes first, the Tutor or the Primer. | Foundations is ruled out (D42). Between the other two, the field research decides, against the tests on `which-first`. |
| Whether the three are one product with three versions, or three products. | It turns on whether a child would move from one to the next, which nothing in the vault can yet say. |
| Prices for the Primer and Foundations. | No anchor exists. OA-22 and OA-29. |
| Whether Foundations is built at all. | OA-28 and OA-29 are answerable by asking; FM3 is the observed test. |

## 5. Counsel questions OI-13 to OI-20

Appended to the counsel table in `14-open-items`, marked **New.**, with the
decision each unblocks and the cost of getting it wrong. No answer, likely
answer or range.

| # | Question | Unblocks | Cost of getting it wrong |
|---|---|---|---|
| OI-13 | For the Primer and Foundations, whose users are almost all under 13 and whose account holder is a parent: which lawful basis applies to the child's data, and what does the UK GDPR Article 8 threshold require of the consent flow? | The privacy notices, DPIAs and consent flows of both ideas. Related to OI-10. | The second limb of the Reddit finding: profiling children without a lawful basis. |
| OI-14 | Is the Primer's parent activity record (D48), with turns flagged for safeguarding withheld from the parent and routed to a trained reviewer, lawful and consistent with the Children's code, and what must the child be told about it? | The parent surface of the Primer. Related to OI-8. | A record that exposes a child at risk, or withholds from a parent what they are entitled to see. |
| OI-15 | For a US launch of the Primer and Foundations: what does COPPA as amended in 2025 require (consent method, retention, notices), which state laws add to it, including laws on companion chatbots, and does a tutor that declines companionship by design fall outside the latter? | The US half of D51. | Enforcement by the FTC, a rebuilt consent flow, or a product classed as a companion chatbot. |
| OI-16 | Does an AI that discusses philosophical, religious and moral questions with children engage duties beyond the Children's code and the Online Safety Act position in 05: consumer protection law on content for children, for example, and, where a school uses it, the expectations on schools to present political issues in a balanced way? | The sensitive modules (D46), and any route through schools. | A module withdrawn under complaint, or a school that cannot use the product. |
| OI-17 | If either new idea ever listens to a child, Foundations to hear them read or the Primer to take spoken questions, is the recording or anything derived from it biometric or special category data under UK GDPR, or a voiceprint under amended COPPA; and does processing on the device and discarding the audio change the answer? | The listening features D50 defers. | Building the feature in a form the ICO or the FTC treats as biometric processing of young children. |
| OI-18 | Do parent-submitted ideas and requests (D46), never shown to other users, keep the Primer outside the Online Safety Act's user-to-user duties; and does that change if a request leads to a module the company then publishes to all users? | The request channel. Related to OI-4. | OI-4's cost, on a product for younger children. |
| OI-19 | Where a school uses Foundations or the Primer, which party controls the child's record, the school or the company, and what does that make each responsible for? Raised while writing F4. | Any route through schools for the two new ideas, and the data processing terms. | A school that cannot lawfully adopt it, or a company holding records it cannot justify. |
| OI-20 | For a US launch of the Primer and Foundations, what duties to report suspected abuse or risk would fall on the company or its reviewers in each state where they are offered, and how do those duties interact with D26 and D48? Raised while writing P4. | The US escalation paths in P4 and F4. | A reviewer who breaches a reporting duty, or a reporting rule that exposes a child to the parent who is the risk. |

## 6. Assumptions OA-22 to OA-34

Two new groups in the assumptions section of `14-open-items`: `<h3>The
Primer</h3>` (OA-22 to OA-27, OA-32) and `<h3>Foundations and markets</h3>`
(OA-28 to OA-31, OA-33, OA-34). Each marked **New.** The seven flagged cheap are
resolvable by reading or by asking, which brings the register's count to
fifteen of thirty-four; the "pattern" paragraph is updated to name them. OA-33
and OA-34 were raised while writing F3 and F6.

| # | Assumption | Shapes | Cost of being wrong | Cheap |
|---|---|---|---|---|
| OA-22 | That parents of 8 to 13 year olds will pay for the Primer with no exam to prepare for. What purchase, if any, it replaces is unknown. | The Primer's whole commercial case. | A product children use and nobody pays for. | Yes: asking parents, and a landing page. |
| OA-23 | That a child of 8 to 13 can hold a typed conversation on a screen long enough for an inquiry to work, and that this is something current AI does well. The owner's view; the youngest band is least certain. | Session design and the age floor. | A floor that should have been higher, or sessions too short to reach the deeper question. | No: observed at PM3. |
| OA-24 | That a change in how a child reasons can be measured by a blind-rated rubric on unaided work, sensitively enough to show a difference in a pilot. | T-PRM-07 and the evidence claim. | No way to show the Primer works, the first thing an investor or a school asks. | No. |
| OA-25 | That what is known about Philosophy for Children (CV-05) transfers to an AI-led version, in either direction. | How the evidence case is argued. | Borrowing a positive result that does not transfer, or being deterred by a null one that does not either. | No. |
| OA-26 | That parents accept an AI discussing big questions with their child when every module is company-written and can be switched off. | D46, and whether sensitive modules exist at all. | A catalogue switched off wholesale, or a press story that ends the product. | Yes: asking parents. |
| OA-27 | That one company-written catalogue can serve families across the range of beliefs in the UK and the US well enough that switching off is the exception. | D46 and D51 together. | Two catalogues, or a product that suits only some families. | No. |
| OA-28 | That children of 4 to 7 learn early reading and writing poorly from a screen without an adult, because of attention and the physical side of reading and writing. The owner's view, and the basis of D42 and D43. | Foundations' whole design. | An adult's time spent on what a child could do alone; or, if right but unproven, an argument an investor can dismiss. | Yes: asking Reception and Year 1 teachers. |
| OA-29 | That parents of 4 to 7 year olds feel less urgency to pay than parents of exam candidates, because school teaches early reading for free. | D42 and Foundations' commercial case. | Ruling out the idea with the most willing payers. | Yes: asking parents. |
| OA-30 | That an adult will sit with the child for each Foundations session and can follow the guidance without training. | D43 and the whole product. | A product that only works for families with time, the inequality tutoring already has. | No. |
| OA-31 | That the US has proven more receptive than the UK to consumer education products for children. The owner's view, and the basis of D51. | D51's simultaneous launch. | Two regulatory regimes paid for at once with no gain from the second. | Yes: reading published market data. |
| OA-32 | That the explanation bank can answer most of the questions a child in a band actually asks, at launch. | D44's "not yet", and whether children come back. | A Primer that says "not yet" so often that children stop asking. | No: measured at PM3. |
| OA-33 | That an adult can reliably tell Foundations which sounds the child's class has covered, from what the school sends home. | D55. | The rule for children in school cannot work as written. | Yes: asking Reception teachers and parents. |
| OA-34 | That parents' urgency to pay for help with early reading, where it exists, concentrates where a child is falling behind, for example around the Year 1 phonics check (CV-09). | Foundations' price and message. | A product priced and pitched for every family and bought by few. | Yes: asking parents. |

## 7. Candidate claims CV-01 to CV-12

A new section of `src/content/sources.html`, `<h2 id="candidates">Candidates
awaiting the owner's check</h2>`, after the registered sections, with a short
explanation of D53 and a table: #, claim, source (with URL), found, used in.
All found on 22 October 2026 through web search; no primary page could be
opened from the build environment, so each records what the source is
reported to say.

- **CV-01** Y Combinator's Fall 2026 Requests for Startups include "The
  Primer". It opens by observing that the best education has always been
  one-to-one tutoring, that Aristotle taught Alexander, and that the privilege
  was reserved for the few; it names as the long-term goal the Primer of Neal
  Stephenson's *The Diamond Age*, which teaches a girl not only to read but to
  think and reason; and it asks for adaptive teaching of reading, writing and
  arithmetic to young children, at close to the quality of a private tutor and
  at consumer scale, supplementing teachers rather than replacing them,
  starting as something parents buy for basic skills. Secondary write-ups give
  the ages as 4 to 10 and the author as Andrew Miklas. Source:
  https://www.ycombinator.com/rfs#the-primer (link supplied by the owner),
  read through search summaries of that page; secondary write-ups at
  modelence.com and explainx.ai.
- **CV-02** Alexander was about thirteen when Aristotle began to teach him, at
  Mieza. Sources: secondary; "Historical Perspective and Medical Maladies of
  Alexander the Great" (PMC9078372); "Aristotle: the first encyclopedist"
  (arXiv physics/0209063). Accounts of the period differ.
- **CV-03** Chanakya, traditionally identified with Kautilya and credited with
  the Arthashastra, became counsellor and adviser to Chandragupta, founder of
  the Mauryan empire, and helped him overthrow the Nanda dynasty; legend makes
  him a teacher at Taxila. Not every historian accepts the identification, and
  the text's dating is disputed. Sources: Britannica, "Chanakya"
  (https://www.britannica.com/biography/Chanakya); UCLA Center for India and
  South Asia, "Kautilya and Arthashastra".
- **CV-04** In *The Diamond Age*, Nell's Primer is voiced live by a human actor,
  Miranda, who becomes a mother figure to her; the novel leaves open how much
  of Nell's development comes from the machine and how much from Miranda.
  Sources: SuperSummary character list; review at rambles.net.
- **CV-05** The Education Endowment Foundation's evaluations of Philosophy for
  Children: an efficacy trial reported in 2015 (Durham; 48 schools; Years 4 and
  5) found small positive effects on reading and maths, summarised as about
  two months' additional progress, at moderate security; a later and larger
  effectiveness trial (NFER; Year 6; 75 intervention and 123 control schools)
  found no evidence of an effect on reading or maths, at the EEF's highest
  security rating, and the EEF removed the programme from its promising
  projects. Teachers reported gains in respect for others' views that the
  pupil survey did not detect. Sources:
  https://educationendowmentfoundation.org.uk/projects-and-evaluation/projects/philosophy-for-children-effectiveness-trial;
  https://www.nfer.ac.uk/publications/evaluation-of-philosophy-for-children-an-effectiveness-trial/;
  the 2015 EEF project report.
- **CV-06** The ICO's Children's code covers online services likely to be
  accessed by under-18s and sets five age ranges for age-appropriate design:
  0 to 5, 6 to 9, 10 to 12, 13 to 15 and 16 to 17. Sources: law-firm summaries
  (Penningtons; Simmons and Simmons); the code itself not opened.
- **CV-07** Under UK GDPR Article 8, the age at which a child can consent to an
  information society service is 13; below it, consent must be given or
  authorised by a holder of parental responsibility, and the controller must
  make reasonable efforts to verify it; section 9 of the Data Protection Act
  2018 sets the age, and the requirement does not apply to online preventive
  or counselling services. The text has since been amended by the Data (Use
  and Access) Act 2025; the current consolidated text was not checked. Sources:
  ICO, "What are the rules about an ISS and consent?"; legislation.gov.uk.
- **CV-08** The US Federal Trade Commission's amended COPPA Rule was published on
  22 April 2025, took effect on 23 June 2025, and required most operators to
  comply by 22 April 2026. Verifiable parental consent applies to children under
  13; the amendments add consent methods, require separate consent for
  targeted advertising and for disclosures not integral to the service, bring
  biometric identifiers including voiceprints into "personal information",
  and require a written data retention policy. Sources: Hunton; Jones Day;
  BBB National Programs.
- **CV-09** In England, children take a phonics screening check in Year 1; the
  Department for Education keeps a list of validated systematic synthetic
  phonics programmes, which start in Reception and give a structured route to
  the check; schools are not required by law to choose one from the list.
  Sources: DfE, "Choosing a phonics teaching programme" (archived copy);
  Oxford University Press education blog.
- **CV-10** On 11 September 2025 the FTC opened an inquiry under section 6(b)
  into consumer AI chatbots acting as companions, with orders to seven
  companies, asking how they measure and monitor harm to children and teens.
  California's SB 243, signed on 13 October 2025 and operative from 1 January
  2026, imposes safeguards on companion chatbots with obligations aimed at
  minors; other states have followed. Sources: FTC press release,
  https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-launches-inquiry-ai-chatbots-acting-companions;
  DLA Piper; California Lawyers Association.
- **CV-11** Automatic speech recognition makes more errors on children's speech
  than on adults', and more the younger the child; fine-tuning on children's
  speech narrows the gap but has not closed it. Sources: "Kid-Whisper" (AIES
  2024); "Causal analysis of ASR errors for children" (arXiv 2502.08587);
  Interspeech 2005.
- **CV-12** US services a child or adult in crisis can be pointed to: the
  Childhelp National Child Abuse Hotline, 1-800-422-4453, around the clock;
  and the 988 Suicide and Crisis Lifeline, by call or text. Sources: Childhelp
  2024 hotline impact report; Nationwide Children's Hospital.

## 8. Tests, risks and milestones

Each test is defined once, in a table row whose first cell is
`<td class="id">T-...</td>` and whose second cell says what it establishes.
Floors stated here are design choices and are tagged as such.

**Primer** (defined in `p3-primer-content#measure` and
`p5-primer-architecture#checks`):

| Test | Establishes |
|---|---|
| T-PRM-01 | Grounding: every factual statement in a sampled Primer turn cites an explanation-bank node and is entailed by it. Floor 99.5% of sampled turns, the Tutor's P2 floor, as a design choice. Below it, the affected module answers "not yet" until fixed. |
| T-PRM-02 | Attribution: every statement that a named thinker or tradition held a view is supported by an inquiry-pack entry. Any unsupported attribution in the release sample blocks the release. |
| T-PRM-03 | No asserted conclusion: on a question an inquiry pack marks contested, the Primer never states a conclusion as its own, across a red-team battery that includes "just tell me". Any failure blocks the release. |
| T-PRM-04 | Freedom to disagree: a scripted child who disagrees, or holds to a view, is not steered back. Blind raters score transcripts for pressure, leading language and unequal treatment of views. Threshold Unknown until the rater protocol exists. |
| T-PRM-05 | Module switch: a module switched off, or outside the child's band, contributes nothing to any turn. Deterministic, over the whole registry; blocks every release. |
| T-PRM-06 | Triage: a question about the child's own life, safety or distress starts no inquiry and takes 05's path. Scripted battery across bands; blocking. |
| T-PRM-07 | Reasoning outcome: a blind-rated rubric on unaided written answers before and after a block of sessions, against a comparison group. Page 13's learning-value gate; not a release check. |

**Foundations** (defined once, in `f3-foundations-content#measure`; F5
describes the mechanisms):

| Test | Establishes |
|---|---|
| T-FND-01 | Decodability: every word in a practice text uses only correspondences the child has been taught, plus the listed exception words for their stage. A deterministic rule, no model. Floor 100%; blocking. |
| T-FND-02 | Sequence: correspondences and number facts are introduced only in the order of the chosen progression. Deterministic; blocking. |
| T-FND-03 | Arithmetic: every number fact and worked step is checked by computation, not by a model, reusing the Tutor's computer algebra check. Floor 100%; blocking. |
| T-FND-04 | The adult's guide: an untrained parent or teaching assistant runs a session as designed from the on-screen guidance alone. Observed at FM2 and FM3. |
| T-FND-05 | No child audio: no audio is captured, transmitted or stored. Network and storage audit; blocking. |

**Risks**, in a table in each plan page (`p6-primer-plan#risks`,
`f6-foundations-plan#risks`) whose first cell is the id. The owner has not
ranked these; the page says so and orders them by severity as judged.

- RP1 A conversation about a big question is reported as the product
  indoctrinating a child. RP2 Children use it and parents do not pay (OA-22).
  RP3 The Primer is classed as a companion chatbot in the US (CV-10, OI-15).
  RP4 A safeguarding disclosure inside an inquiry is missed, or reaches a
  parent who is the risk (D48). RP5 Reviewers become the bottleneck and "not
  yet" dominates (OA-32). RP6 No measurable effect on reasoning (OA-24,
  OA-25).
- RF1 Adults do not sit for sessions (OA-30). RF2 Nobody pays (OA-29). RF3 A
  practice text with a non-decodable word teaches a child to guess (T-FND-01).
  RF4 A route through schools fails on due diligence, as 05 warns for the
  Tutor (OA-20 applies). RF5 The owner's caution proves right: the idea is
  sound and still not worth building.

**Milestones**, defined by evidence obtained, ordered cheapest first, with no
dates (D32 applies to all three ideas):

- PM1 Asked, not built: the field research (OA-22, OA-26, priors on OA-23),
  OI-13 to OI-18 put to counsel, a landing page. PM2 The first modules,
  written and reviewed by different people; the review protocol tested. PM3 A
  human-run pilot: a trained facilitator runs the Primer's method over a
  screen, from the modules, with consenting families; tests OA-23 and OA-32
  before anything is built. PM4 The built Primer in a supervised pilot with
  independent evaluation: page 13's gates, T-PRM-01 to T-PRM-07. PM5 Revealed
  willingness to pay. PM6 Release as a gated product, or hold.
- FM1 Asked: Reception and Year 1 teachers, teaching assistants, parents
  (OA-28, OA-29). FM2 A paper prototype of the adult's guide, used by adults
  with their own children and observed (T-FND-04). FM3 An observed pilot of
  the built guide with consenting families or one school (T-FND-01 to
  T-FND-05). FM4 Decide whether to build further.

## 9. Pages

Numbering: the Tutor keeps 00 to 14. The Primer's pages are P1 to P6 and
Foundations' F1 to F6. The two shared pages carry no number.

Every new page opens as the Tutor's do: `<h1>`, a `standfirst` stating the
conclusion, a `meta` list (Document, Status "Design. Nothing here has been
built; no test here has been run.", Written "22 October 2026", Read next), a
`toc` listing the sections, then the sections, each `<h2 id="...">` at the start
of a line, with exactly the ids below. Between 1,200 and 2,600 words of prose
each.

| Slug | No. | Title | Owner | Section ids |
|---|---|---|---|---|
| `p1-primer-thesis` | P1 | Primer: thesis | ceo | claim, why, tutors, yc, different, weak, gateway |
| `p2-primer-product` | P2 | Primer: product | ceo | child, promise, session, worked, off, personal, parent, not |
| `p3-primer-content` | P3 | Primer: content and evidence | coo | sources, bank, packs, modules, review, cleanroom, evidence, measure |
| `p4-primer-safety` | P4 | Primer: safety, privacy and regulatory | counsel | posture, ages, modules, parent, memory, voice, escalation, companion, us, gaps |
| `p5-primer-architecture` | P5 | Primer: architecture | cto | reuse, turn, checks, triage, registry, killswitch, model, cost |
| `p6-primer-plan` | P6 | Primer: plan | ceo; `#economics` cfo | who, routes, economics, milestones, risks, first |
| `f1-foundations-thesis` | F1 | Foundations: thesis | ceo | claim, caution, yc, adult, screen, weak |
| `f2-foundations-product` | F2 | Foundations: product | ceo | who, promise, session, worked, screen, record, not |
| `f3-foundations-content` | F3 | Foundations: content and evidence | coo | sequence, decodable, writing, number, review, cleanroom, evidence, measure |
| `f4-foundations-safety` | F4 | Foundations: safety, privacy and regulatory | counsel | posture, ages, voice, data, escalation, schools, us, gaps |
| `f5-foundations-architecture` | F5 | Foundations: architecture | cto | reuse, guide, decodable, arithmetic, listening, cost |
| `f6-foundations-plan` | F6 | Foundations: plan | ceo; `#economics` cfo | who, routes, economics, milestones, risks, build |
| `which-first` | | Which idea goes first | ceo | answer, foundations, open, tests, share, one |
| `field-research` | | Field research guide | ceo | purpose, who, how, common, tutor, primer, foundations, after |

Required key blocks (the front page transcludes them, so each is short, has no
Verified marker, and states its idea's age band):

- `00-thesis.brief.1`, a `<div class="brief">` added to 00's head after the meta
  list; and `p1-primer-thesis.brief.1`, `f1-foundations-thesis.brief.1` in the
  same place on P1 and F1. Each 90 to 140 words: the idea in one line, who it
  is for, what makes it different, its honest state.
- `which-first.answer.1`, `which-first.share.1`, `field-research.purpose.1`.

What each page must contain, beyond its sections' titles:

- **P1** The claim in four sentences. Why conversation is what current AI does
  best and why eight to thirteen suits a screen (OA-23). The historical tutors
  as the ambition (CV-02, CV-03), never the voice (D47). What YC asked for
  (CV-01), where the Primer agrees and where it parts (D42). What makes it
  different from free study modes: the Tutor's warranty carried to ideas
  (D44), modules (D46), no engagement objective (D25 carried over). Where the
  case is weak: why a parent pays (OA-22), reputation (RP1), proof (OA-24,
  OA-25, CV-05). How it relates to the Tutor and page 13, and an answer to
  page 13's argument for older adolescents first.
- **P2** The child: a nine-year-old and a twelve-year-old. Promises with a
  test each. A session: clarify, explain from the bank, find the question
  underneath, the child's starting view, a counterexample, uncertainty, the
  child's revised view, recorded. A worked transcript of one why-question
  explored end to end, annotated with the bank node, pack entry, module and
  check behind each turn. A short transcript of a request to a module that is
  switched off; and one of a question about the child's own life (triage, no
  inquiry). What the parent sees (D48). What it does not do, including D47.
- **P3** Where every statement comes from (D44); the explanation bank; the
  inquiry packs, several traditions including non-Western ones, positions
  attributed and never asserted; modules and which are sensitive; who writes
  and who reviews, never the same person, a standing review group for
  sensitive modules; what may not enter (no copyrighted translations or
  commercial programme materials, positions paraphrased with attribution);
  the evidence (CV-05, honestly); how we would know it works (T-PRM-07,
  OA-24), with the tests table.
- **P4** Posture in one paragraph; age bands against the code's ranges (CV-06),
  consent (CV-07, OI-13); modules and the request channel (D46, OI-18); what a
  parent sees (D48, OI-14); memory (D49); voice (D50); escalation in the UK
  (05's three moves) and the US (CV-12), with the same honest limit 05 states;
  not a companion (05's four constraints, CV-10); the US position (CV-08,
  OI-15, OI-16); named gaps.
- **P5** What it reuses from 06 (composer, generator, verifier, gate, kill
  switch, logger, classifier, caps); a Primer turn; the two new checks,
  attribution and contested-question, with the tests table; triage before
  inquiry; the module registry and the switch (T-PRM-05); pulling a module in
  one operation; models, taught on not trained on (D45); cost per session,
  Unknown with what decides it.
- **P6** Who pays and why that is unknown (OA-22); routes (parents first;
  schools later; the UK and the US, D51); economics, almost all Unknown, with
  what would measure each figure; milestones PM1 to PM6; risks RP1 to RP6; what
  would make the Primer go first.
- **F1** The claim; the owner's caution stated plainly as the owner's (D42's
  reasons), not softened; YC's order and why the owner disagrees; why the
  adult is the point (D43); what the screen adds (the next step in a proven
  sequence, practice built only from what the child knows, what to listen
  for); where the case is weak, including the owner's own reasons (OA-28,
  OA-29).
- **F2** The adult and the child; promises with tests; a session (short,
  stopping at the first sign of fatigue); a worked session showing the screen
  guiding the adult and the adult doing what a screen cannot, the finger on
  the print, the letter formed by hand, real objects for counting; what the
  screen does and does not do (no microphone, no camera, D50); the reading
  record; what it does not do, including rewards for the child (D25).
- **F3** The reading and number sequences, written originally to published
  expectations (CV-09; OI-9 applies to any DfE material used as a source);
  decodable practice (T-FND-01); writing, taught by the adult with guidance on
  letter formation; number, with physical objects; who writes and who checks;
  what may not enter (commercial phonics programmes' materials); the evidence,
  stated as what is known and what is not; how we would know it works.
- **F4** Posture; ages and consent (CV-06, CV-07, OI-13); no microphone at
  launch (D50, CV-11, OI-17); the data held; escalation, mostly through the
  present adult; through schools (OA-20 applies); the US (CV-08, OI-15); named
  gaps.
- **F5** What it reuses (verifier, kill switch, eng.cas, the account); the
  adult's guide; the decodability check; arithmetic checks; if listening is
  ever added (D50, OI-17); cost, Unknown.
- **F6** Who might pay (parents, schools; OA-29); routes; economics, Unknown;
  milestones FM1 to FM4; risks RF1 to RF5; what would justify building it.
- **which-first** The answer so far (D42; Tutor or Primer open); why
  Foundations does not go first; what decides between the Tutor and the
  Primer, as a decision rule; the tests (who pays and how urgently; the
  cheapest make-or-break assumption; regulatory weight; what is already done;
  what an AI does well; fit with the accelerators, without claims about what
  any accelerator wants beyond CV-01); what the three share and what they do
  not; one product or three.
- **field-research** What it is for; who to talk to for each idea; how to ask
  (past behaviour, not opinions of the idea; adults only, no children's data;
  notes mapped to assumption ids); questions for everyone; for the Tutor; for
  the Primer; for Foundations, including questions that could prove the owner
  wrong; what to do with the answers (record against the ids; the owner
  changes markers).

## 10. The front page, the Tutor summary and video

- `docs/index.html` becomes the front page, generated from
  `src/templates/front.html` and the `front` block of `roles.json`. Its frame,
  the text before the first `<h2>`, is under 150 words, carries no figure and
  says nothing has been built. Below it: the three ideas as cards (Tutor,
  Primer, Foundations), each with a video space and its transcluded brief and
  links; which goes first; what the three share; what happens next; where it
  stands, as computed counts; and links for going deeper. Under 1,200 words.
  No digit outside a key block, a computed count or a `data-from` element.
- Each card's video comes from `roles.json`: `null` renders a placeholder; a
  `src` (with optional `poster` and `captions`) under `docs/media/` renders a
  `<video>`; an `embed` URL renders an `<iframe>`, and the build adds that
  origin to `frame-src` in the generated `_headers`. `media-src 'self'` is
  added to the strict policy.
- `docs/tutor.html` is the Tutor summary: the previous front door, generated
  from `src/templates/summary.html` and the `summary` block, its frame renamed
  to the Tutor.
- The switcher, the contents page and the pager group pages by idea: Tutor,
  Primer, Foundations, and "Across all three" (which-first, field-research,
  14, the ledger).

## 11. Tooling

- `src/build.py`: `PAGES` gains the fourteen new pages; a `GROUPS` list maps
  them to ideas; the front page renderer; the Tutor summary moves to
  `tutor.html`; grouped switcher and contents; a `body_class` on the shell for
  the front page only, so every other page's markup is unchanged; idea risks
  on the status page; a count of candidates; test blurbs found from a test's
  defining row; video and the content security policy.
- `tools/verify.py`: the front-page rules apply to `index.html` and
  `tutor.html` and to both templates; the front block's keys must exist; a
  fifth reader route on the contents page, "A teacher, partner or prospective
  co-founder".
- `roles.json`: ownership per §9; frames updated, under 200 words, no figures.
- `tools/depmap/graph.json`: nodes for the new components with loci on the new
  pages, and edges to the shared ones.
- `netlify.toml`: the root redirect (§0).
- `README.md` and `CLAUDE.md`: three ideas, this brief, the stylesheet rule
  (D52), how to add a film.

## 12. Acceptance bar

1. `python3 src/build.py` then `python3 tools/verify.py` pass, with no
   warnings about the front page.
2. Every decision, question, assumption, candidate, test, risk and milestone in
   §3 to §8 appears where this brief puts it, with the id given.
3. No Verified marker added; no existing marker changed; no counsel question
   answered or written as answered; no em-dash or en-dash in anything new.
4. The root URL, served as Netlify serves it, lands on a styled front page with
   no failed requests.
5. An independent reviewer with none of this conversation reads the new pages
   for anything that would embarrass the owner in front of a teacher, a
   parent or an accelerator, and every finding is fixed or answered in
   `FACETS_REPORT.md`.

## 13. Forbidden moves

- Reopening D1 to D14, reversing D15 to D39, or answering a counsel question.
- A Verified marker, a figure with no source, or a plausible substitute for an
  Unknown.
- Editing `docs/`, `evidence/` or `viz/` by hand.
- Moving or renaming an existing page, or changing page 13 beyond its note.
- Claims about what an accelerator wants beyond CV-01.
- Collecting, or designing research that collects, any child's data.
