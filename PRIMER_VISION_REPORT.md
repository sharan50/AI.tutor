# PRIMER_VISION_REPORT

What `PRIMER_VISION_BRIEF.md` changed, the checks it passed, and what the independent
review found. Written 31 October 2026.

## 1. Outcome

The Primer's documents now describe the Primer the owner's films show. It is a tablet of
its own, one per child, with nothing else on it. A child asks a why-question aloud or by
typing, and the Primer answers aloud while a drawn explainer builds on the screen in time
with its voice. Every answer has one shape:

1. a checked fact with its source;
2. "the harder bit";
3. three simplest positions from named traditions, each at its strongest;
4. which is closest to what the child thinks, and the other two asking back;
5. the child's real question, probed with evidence;
6. the child's own position, read back.

It may reason with a child about a choice in their own future, neither encouraging nor
discouraging: it sets out the reality and what the schools of thought say. It never says
"I", never uses the child's name and never praises. It remembers past questions and
views as summaries, never word for word, and records no video. No child speaks to it until
its spoken safety battery has passed, and that waits on counsel (section 6).

What was rewritten:

- **The Primer's six documents, P1 to P6.** P5 now holds the technical architecture and
  P6 the go-to-market, as a hardware business.
- **The registers:** the decision ledger, counsel questions, assumptions, tests, risks,
  candidate claims and the dependency map.
- **The shared pages:** which idea goes first and the field research guide.
- **The front page.** The Primer's card now plays the owner's rough cut, labelled as a
  draft.

The MVP demonstration did not change by a byte. P2 lists where it differs from the films.

Nothing has been built and no test has been run.

## 2. The decisions

**The owner's, D101 to D107**, in the owner's words, in `decision-ledger/058-films.html`
(`#films`):

- the films are the Primer (D101);
- children speak or type from launch, ahead of OI-17 (D102);
- the close, "Leave it there, or keep going?", within the time cap (D103);
- past questions and views remembered as summaries, nothing kept word for word, no video
  (D104);
- a dedicated tablet, one per child (D105);
- a child's own future, as filmed, on by default at every age, neither encouraging nor
  discouraging (D106);
- the safeguarding review, run constantly or at the end of each conversation (D107).

**From the films, confirmed by the owner, D108 to D114**, and **taken while writing,
confirmed by the owner, D115 to D117**, in `059-films-confirmed.html`
(`#films-confirmed`). The ledger was split into two sections so that neither file passes
3,000 words:

- the Primer's manner (D108);
- the screen (D109);
- the answer's shape (D110);
- drawn explainers made in advance from a reviewed specification (D111);
- pace (D112);
- evidence, named living people and "roughly" (D113);
- the time argument (D114);
- safety replies shown, never spoken (D115);
- no camera, and the talk key (D116);
- the read-back as the kept summary, with settings not counted as memory (D117).

**How D107 was applied.** The owner said the review runs constantly or at the end of each
conversation, and a flagged exchange is kept briefly, reviewed and deleted. The design
reads this as follows:

- a safety check runs on every turn;
- a fuller review runs at the close;
- the words of a flagged exchange are held for a trained reviewer, as D26 requires, and
  deleted when the review closes.

The owner did not remove the trained reviewer, so the design keeps one.

**Notes on earlier entries:** D30, D44, D46, D47, D48, D49, D50 and D57 each open with a
note saying how the films' decisions bear on them (brief section 7). Three consistency
edits change no decision:

- Foundation's ledger lede and D90 now say D50's image half still governs the Primer;
- the reversals section counts OI-17 among the questions the vault goes ahead of;
- the rights dossier's lede counts three places the vault goes ahead of counsel, and its
  line on voice says the self-tutor's is the one cloned voice on the launch path, since the
  Primer speaks in a stock voice cloned from no one.

## 3. What changed

| Where | What |
|---|---|
| P1, thesis (8 fragments, 5,001 words) | The time argument first, as the owner's view (OA-53). Then the tablet, the voice, the explainers and the answer's shape, and why eight. The differences from free AI tools gain the tablet. The weak points gain the tablet's cost, a child's voice ahead of counsel, named living people, own-future reasoning on by default and summaries that may misstate a child. The brief block on the front page carries the time argument. |
| P2, product (12 fragments, 8,783 words) | The child and their tablet. Fourteen promises, each with its test. The shape of a question. A new section on what an answer looks like, and a new section on the screen. The worked example follows the front-page film. The fence around a child's own future. What the parent sees. What the Primer does not do. A new section listing where the demonstration differs. |
| P3, content (11 fragments, 6,039 words) | The "roughly" rule and evidence by market. A new #figures section and a new #explainers section. Packs of three positions at their strongest, with range across a module. The "choices ahead" module, on by default. Reviewers for explainers and for stories of living people. |
| P4, safety (14 fragments, 10,445 words) | New #device, #future and #people sections. Speech from launch ahead of OI-17, with no audio kept. Summaries, not records, and an inventory of everything held. The four-part safeguarding review. The US position with the new candidates. |
| P5, architecture (13 fragments, 11,167 words) | One turn from the talk key to the read-back. New sections on speech, drawn explainers, summaries and the tablet. Seven verifier checks, including the manner check and the no-direction check. Triage on every turn. Tests T-PRM-02, -03, -05, -06, -08 and -09 to -14. Cost, all Unknown. |
| P6, plan (8 fragments, 5,070 words) | Parents buying a tablet and the service. Routes, with the device rules as candidates. Economics with every figure Unknown. A new #hardware section: a stand-in tablet for PM4, the dedicated tablet made only after PM4's evidence. PM1 to PM6, RP1 to RP9 and the decision rule. |
| Ledger | D101 to D117 in two sections. Notes on eight earlier entries. The head's breakdown. Rows in the decisions not taken: who makes the tablet, what the parent's screen runs on, and prices. |
| Counsel | OI-30 (named living people), OI-31 (the device), OI-32 (a child's own future). OI-17 says the Primer goes ahead of it under D102. `CLAUDE.md` records this as the third exception and now says OI-1 to OI-32. |
| Assumptions | OA-53 to OA-60, in a new group "The Primer, as the films show it". OA-60, parents letting the Primer hear their child, was added while integrating because nothing stood behind D102's take-up. OA-23 now covers a spoken conversation. The pattern line reads twenty-two of the fifty-six, and the build reads that hyphenated number. The open items page gained a second section so that no file passes 3,000 words. |
| Tests and risks | T-PRM-06 redefined in two parts, T-PRM-09 to T-PRM-14 added. RP7 to RP9 added. RP3 and RP4 restated. |
| Evidence register | CV-31 to CV-40, in their own section: the films' football figures (Calvin, Sky Sports News, the PFA); the FTC on children's voice recordings; the UK rules for connectable products and their exception that leaves out tablets designed for children under 14; the ICO's standard 14 on connected devices; US children's product certification; FCC and UK radio rules. |
| Map | The tablet, speech, drawn explainers, summaries, the manner check, explainer specifications, device duties and making the tablet. After the review, also the no-direction check, the fence, personal questions as the child meets them, the speech rules, the screen, the answer's shape, figures and named people, pulling from the Primer, the safeguarding review, a Primer turn, the named gaps, the Primer's manner, measuring the Primer, the safeguarding count, the escalation records, and a node for each section that restates a rule (the promises, the worked example, where the words come from, how the Primer differs, the milestones, the risks, the cost, the read-back check, placed sentences, not a companion and what the Primer holds), so that `impact` reaches every page that states them. 135 nodes and 310 edges, up from 101 and 194. Glosses for every new id. |
| Front page | The hero's sentence on the Primer carries the time argument. The card shows the film, and its links to the demonstration say it shows an earlier design. |
| Shared pages | Which idea goes first: the Primer's column, the not-shared table and the decision rule. The field research guide: the Primer's questions rewritten, with a plain description for interviewees. Page 13: its gated mode is the Tutor's, and the Primer for 8 to 13 is a tablet. Contents. |
| Foundation's and the Tutor's pages | One sentence each in F1, F2, F4 and F6, and two in the rights dossier. Each only keeps those pages true now that the Primer has a tablet and a voice. |
| Root files | README (counts, the briefs, the layout), `CLAUDE.md`, and `src/build.py` (page descriptions, the status lines and the count pattern). |

**Counts, before and after:**

- decisions, 100 and 117;
- counsel questions, 29 and 32;
- assumptions, 48 and 56, of which 18 and 22 are resolvable by reading or asking;
- tests, 33 and 39;
- candidates, 30 and 40;
- documents, 32 and 32.

The status page computes them and agrees.

## 4. The film

The owner's "Version B with the Primer", a rough cut, is published unchanged as
`docs/media/primer.mp4`: 3 minutes 40 seconds at 720p, 26 MB, already set up to stream. Its
cover frame is the tablet's wake screen. The owner asked that it be labelled as a draft,
so the caption reads: "A rough cut, still in progress: an illustrative film, made with AI.
Nothing shown here has been built."

As with Foundation's film:

- it has no captions track;
- the README asks that an AI-generated film say so in the film itself, and only the
  caption says so.

P2's worked example follows the film. Where a line in the rough cut runs against a rule the
owner confirmed, the page follows the rule and marks the departure (D101):

- two lines that read as praise (D108);
- a probe that judges the boy's chances from what he says of himself (the fence);
- a single hedge given as advice, which becomes one of three schools of thought on the
  choice (D106);
- ask-backs voiced as the thinkers, which become positions (D47).

No named player is described.

## 5. Checks run

| Check | Result |
|---|---|
| `python3 src/build.py` and `python3 tools/verify.py` | Build exits 0; every check passes. 4,957 links in 44 files, none broken. The map has 135 nodes and 310 edges, and every locus resolves. |
| The frozen demonstration | `primer-mvp.html`, `mvp/`, `mockup/` and `050-mvp.html` are byte for byte unchanged. Every anchor they link to still exists. |
| Splitting | P1 to P6 were each split at their h2 headings. Each set of fragments was proved byte for byte against its page before the single file was deleted. No fragment passes 3,000 words by `build.word_count`. |
| Markers | Against the last commit, across every page: Verified markers number 52 before and after, so none was added. Assumed went from 127 to 172, Open from 31 to 76 and Unknown from 114 to 170, and no page has fewer of any kind. One Unknown went with the transcript-retention claim that D104 deletes. Where a claim was reworded, it kept its marker. |
| House style | No em-dashes or en-dashes in any changed file. The one new "toward" became "towards". |
| Counts | README, the status page, the ledger head, the open items ledes and the pattern line agree. |
| Candidates | Each "Used in" column was compared with the pages that cite it, and CV-06 gained P3. |
| Rendering | Every changed page, the map and the evidence register at 390 and 1280 pixels, before and after the review's fixes: no horizontal overflow and no failed request. The Primer's card was screenshotted with its film and caption. |

## 6. Design calls for the owner

These were taken while writing or reviewing, and each is the owner's to keep or reverse:

- **Speech starts off.** Speech is off until the verified adult consents and switches it
  on, under 05's rule for optional processing (P4). Version C shows a household where it
  is on.
- **The parent's screen** is on the parent's own phone or computer, never on the child's
  tablet. It is listed among the decisions not taken.
- **Things the writers chose:**
  - the module is called "choices ahead";
  - there are no starter questions;
  - a question with only two serious answers waits as "not yet";
  - a child whose country has no local evidence gets "not yet";
  - the fixed reply to "Are you alive?";
  - how long the writing queue is kept;
  - the standing review group also reviews "choices ahead";
  - no reply names gambling, a bookmaker or a stake of money;
  - "Leave it there" and "Keep going" carry equal weight;
  - within a conversation the child's words stay whole until the close (the note on D30).
- **"Go all in".** P2 attributes the "go all in" position to an unnamed general's saying.
  A reviewer should check that attribution.
- **D45's wording.** D45's "Makes harder" still says "depth and voice". It means the
  writing voice, and was left as it was.

These were taken while fixing the independent review (section 7), and are equally yours:

- **The stand-in tablet's camera.** PM4 uses a stand-in without a camera. If none suits,
  you choose between one whose camera is switched off and covered, which T-PRM-13 would not
  pass, and pilot units of the dedicated design (P4).
- **A "show, don't speak" control.** The answer to a typed question is still spoken, so a
  room hears its subject. P4 puts to you a control that lets a child see an answer without
  hearing it; no page decides it.
- **A flagged exchange outlasts a deletion request** until its review closes. Whether that
  is lawful goes to counsel with OI-13 and OI-14; the pages do not decide it.
- **Every answer takes the whole shape.** A question the bank cannot take through every
  stage, a plain fact with no harder bit among them, waits as "not yet" until a writer
  gives it one. The alternative was answers that stop at the fact, which D110 rules out.
- **After a stop or a safety reply**, the child's own words leave the screen at once. The
  reply stays until the child taps "Leave it there", turns the screen off, or a short idle
  period passes, and the screen does not sleep on its own before then. Then the screen
  clears. The idle period's length is Unknown, set with the specialist who writes the
  replies, because the child must have time to read the services named.
- **Stops spread over several conversations.** The review at the close reads a
  safeguarding count: the dates of the child's earlier stops and flags, with no words and
  no subject. When stops repeat, it flags the current exchange for the trained reviewer.
  The threshold is Unknown. The count is kept apart from the parent's record and never
  shown to the parent, because a parent who is the risk could otherwise delete it with
  the record. Neither a deletion request nor an account closure reaches it until the
  safeguarding policy's period ends. Whether that is lawful goes to counsel with OI-13 and
  OI-14. This applies D107's constantly running process. The other choice was to leave
  stops to be seen together only in the parent's record.
- **The count does not follow a child to a new setup.** A parent cannot delete the count,
  but wiping the tablet and setting it up again with a new profile, or closing the account
  and opening another, starts a new count, because nothing links a child across profiles
  or accounts. Whether the count should follow the tablet or the verified adult across a
  new setup is yours to decide, with counsel on OI-13 and OI-14. Making it follow them
  would mean tracking a family across accounts. No page decides it.
- **Test recordings of children's speech.** The spoken batteries need children's voices,
  since adult or synthetic speech would not test how children are misheard. So, once
  counsel has answered on their lawful basis (OI-13, OI-17), recordings are licensed or
  made for testing. Sessions that make them are held to the conditions for any child in a
  Primer session, under their own consent and DPIA. A child reads a script that voices
  nothing of their own life. The recordings are kept apart from every account for a
  period that is Unknown. They are the one exception to your "drop the recording of the
  child", and they are kept only as test material. The alternative is spoken batteries
  without children's speech, which would leave recognition of children untested before
  PM4. Until counsel answers, the spoken batteries cannot run. No child speaks to the
  Primer until T-PRM-06's spoken battery has passed, so speech at PM4, and the speech from
  launch that D102 decides, come no sooner than counsel's answer on the recordings.
  Anything a child says of their own in a recording session is cut from the recording.
  Where it takes 05's path it is held for the trained reviewer until the review closes;
  otherwise it is deleted at once. If you want speech sooner, there are two routes, and
  both are yours to choose. One is to go ahead of counsel for the test recordings as
  well, which would be a new exception. The other is to run the spoken batteries live:
  children read the scripts to the Primer in supervised sessions and the audio is thrown
  away, as D102 does for every child. That keeps no recordings, but the batteries must
  then be run again with children at every update to the recogniser.
- **A review that cannot run.** If the review at the close fails, the whole conversation is
  held for the trained reviewer as a flagged exchange, so a safeguarding signal is never
  lost. The cost is that a trained person may read a conversation in which nothing was
  flagged. How often this happens is Unknown.
- **Explained stages are said in reviewed sentences.** The fact, the positions, and the
  figures and stories used in probing are always the entries' reviewed sentences, so every
  one is drawn. The Primer's own sentences are the questions, the links and the read-back.
  This keeps D111's rule that an answer is served with its drawing.
- **The escalation record keeps none of the child's words**: the category, the dates, the
  reviewer's decision and whom they informed. That follows your "review and delete". The
  cost is that nothing of what the child said survives the review, so P4 says a review
  closes only after any referral has what it needs, and leaves to the safeguarding
  specialist and counsel whether a record of a concern may hold none of the child's words.
- **The read-back may repeat a short phrase** of the child's where it states their
  position, never more. A deterministic check blocks a read-back that repeats any run of
  the child's words longer than a short phrase, so a child's two-word answer can still be
  read back. How long a short phrase may be is Unknown, set before PM4. Forbidding any repeated phrase would make the read-back hard to
  recognise and the rule hard to test.
- **The Primer's voice is a stock synthetic voice**, chosen from vendors at PM4. A voice
  designed for the Primer would be a new decision.

## 7. The independent review

Fresh agents, given the brief, the owner's gap list and the vault's rules but not this
conversation, reviewed the change. Each round had a separate reviewer for each lens. The
lenses were fidelity to the films, the vault's rules, children's safety and privacy, and
the architecture and go-to-market. Every finding was fixed under a written resolution, so
that every page took the same position. The resolutions now hold with the brief (its rule
8).

**Round 1: 49 findings, 26 of them blocking.** Resolutions R1 to R19. The main ones:

- the memory between sessions is called your departure from the films (D104);
- the stand-in's camera is left to you;
- one speaking rate at every age;
- the manner check is stated once, with what it matches exactly and what a classifier
  judges;
- the film's figures are said "roughly";
- a question is kept as the catalogue question, never the child's words;
- P4 lists everything held, the per-turn log and the adjudication queue included;
- an answer is served with its drawing or not at all;
- the display name never reaches the generator;
- a stopped question shows the parent one category only (and, since T9, its date);
- neither the session store nor the flagged hold is ever backed up;
- no detail of family, body or feelings goes into a kept summary;
- a pattern across turns flags every exchange it runs through;
- tests claim no more than their method shows;
- without a connection the tablet shows one fixed screen and keeps nothing.

**Round 2: 34 findings, 8 of them blocking.** Some were found under more than one lens.
Resolutions S1 to S28. The blocking ones:

- P4 called the Primer's voice designed for it, while P2 and P5 called it a stock voice
  (S1);
- P2 made the fact and the harder bit optional, which D110 does not allow (S2);
- after a stop or a safety reply, the reply stayed on the screen for anyone who picked up
  the tablet (S12);
- stops spread over several conversations were never seen together except in the parent's
  record (S13);
- P3 and P5 described different ways of keeping a drawing in time with the voice (S19);
- P5 had PM3 measure how often a child is misheard, which only PM4 can do (S20).

Among the others:

- which film the front page plays;
- the film calling the boy's plan "a clear plan", now marked as a departure;
- T-PRM-07's audio left to PM4's research protocol rather than to D102;
- what the escalation record and the per-turn log keep;
- when a flag writes the words to the hold;
- where the spoken battery's recordings come from;
- holding the stand-in's own system updates;
- a fallback for a blocked read-back;
- the map's notes, and nine new nodes.

**Round 3: 19 findings, 2 of them blocking.** This round was narrower. One reviewer
checked that each of round 2's findings was resolved wherever the same thing is stated.
The other looked for anything the fixes had opened. Resolutions T1 to T15. The blocking
ones:

- the count of repeated stops came from the parent's record, which a parent can have
  deleted and which never holds a flagged exchange, so the child it exists for could be
  missed. It now comes from a safeguarding count the parent never sees and cannot delete
  (T9). A new setup still starts a new count, which round 4 named (U2);
- T-PRM-08 said a flagged exchange reaches nowhere a parent can see, while the reply stays
  on the child's tablet until the conversation closes. The test now covers the parent's
  record, screen and account; the child's tablet is T-PRM-12's; and the child's own words
  leave the screen at once (T10).

Among the others:

- restatements of tests on other pages brought into line;
- the worked example's read-back now repeats only a short phrase, and a check blocks
  a whole turn;
- a flag never appears in the per-turn log;
- the test recordings get a place in the plan before PM4;
- the cost of a review that cannot run is named;
- explained stages are said only in reviewed sentences, so every answer is drawn;
- the map gains six nodes, and its notes and test labels match the pages;
- the appendix lists every resolution.

**Round 4: 23 findings, 3 of them blocking.** Scoped as round 3 was. Resolutions U1 to
U13. The blocking ones:

- P5's withholding rule and risk RP4 still said a flagged exchange reaches nowhere a
  parent can read it (U1);
- the sessions that make test recordings had none of the protections the plan gives a
  child, and did not wait on counsel (U3);
- the safeguarding count can still be reset by setting the tablet up again or opening a
  new account. The pages now say so, and the choice is put to you (U2).

Among the others:

- the stores that keep a flag are named exactly;
- one rule now governs explained stages;
- the read-back may repeat a short phrase, never more;
- T-PRM-08 and T-PRM-10 are each credited with what they test;
- restatements of the tests carry the latest wording;
- the map gains eleven nodes so that `impact` reaches every page that restates a rule;
- the brief and this report are brought into line.

**Round 5: blocking defects only.** Two reviewers read the whole Primer set. One followed
a child through every path. The other checked that every mechanism stated on more than
one page can be true at once. The consistency reviewer found nothing blocking. The safety
reviewer found three holes, fixed under V1 to V3:

- a child could speak to the Primer at PM4 before T-PRM-06's spoken battery had ever run
  (V1);
- a disclosure made during a test-recording session would have stayed in the recording
  (V2);
- a blocked turn could carry a paraphrased personal detail to the adjudicators, and a
  flagged exchange's blocked turns stayed in the adjudication queue (V3).

Two further reviewers checked V1 to V3 and found three more holes, fixed under W1 to W3:

- a backup could keep a test recording, and with it whatever had been cut from it (W1);
- the adjudication queue could be backed up, and a conversation held because its review
  could not run kept its blocked turns there (W2);
- if the spoken battery passed only after PM4, speech could reach children at home
  without a supervised pilot (W3).

A last reviewer checked W1 to W3 against every page that states a backup, the
adjudication queue, the test recordings or when speech is switched on, and found nothing
blocking.

**Where the review stopped.** Round 5 and its checks looked for blocking defects only. A
further round looking for non-blocking defects, such as wording, routing in the map or a
restatement that is true but incomplete, would very likely find some: each earlier round
did. None of the five rounds was run against the films themselves.

## 8. What is left for the owner

- **Your bar.** Watch each film beside the site. The checks here ran against your gap
  list and your decisions. None of them watched the films, so only you can hold the pages
  against the films themselves.
- **The design calls in section 6.** Each is yours to keep or reverse, and the ones the
  review produced are listed there too.
- **The film.** The card's caption is its only label. The film carries no AI label in the
  picture and has no captions track, both of which the README's rules for films ask for.
- **The candidates.** CV-31 to CV-40 were found through search results, because several
  government sites could not be reached from this session. Each is marked Assumed until
  you check it and promote it.
- **Counsel.** OI-30 to OI-32 are new. For the Primer, the vault now goes ahead of OI-17
  (D102), its third such exception after D34 and D59. Several of the review's fixes go to
  counsel with OI-13 and OI-14: the flagged hold and the safeguarding count both outlast a
  deletion request.
- **Speech waits on the spoken battery.** No child speaks to the Primer until T-PRM-06's
  spoken battery has passed, and its recordings wait on counsel. Section 6 sets out the
  two routes to speech sooner, both yours to choose.
- **Nothing is built, and no test has been run.**
- **Merging** waits on you. The pull request now carries four pieces of work.

## Appendix. Every resolution

Each review round's findings were fixed under these resolutions. The pages carry their
canonical wording; this list gives each one's position in a line. Where a later
resolution replaces an earlier one, it says so.

**Round 1**

- **R1.** Remembering a child's past questions and views between sessions is your
  departure from the films (D104), and P2 and P4 say so.
- **R2.** T-PRM-13 stays as defined, and gains a software check of every path that can
  open the microphone. PM4 uses a stand-in without a camera. If none suits, you choose
  between a covered camera, which T-PRM-13 would not pass, and pilot units of the dedicated
  design.
- **R3.** One brisk speaking rate at every age (D112). Whether the youngest need a slower
  one is for PM3 to show and for you to decide.
- **R4.** The manner check is stated once, in P5: a deterministic match for "I", "me",
  "my", "let's" and the display name, and a classifier for praise and for a "we" that
  joins the Primer to the child.
- **R5.** All three of the film's figures are said "roughly".
- **R6.** A question is kept as the catalogue question its entries answer, and the child's
  position as the read-back they accepted or corrected.
- **R7.** P4 lists everything held, the per-turn log and the adjudication queue included.
  The parent's screen reads only summaries, topics, switches and categories.
- **R8.** An answer is served with its drawing or not at all, so pulling a drawing takes
  its answer out of service.
- **R9.** The display name labels the parent's screen and never reaches the generator.
- **R10.** A stopped question appears in the parent's record as "a personal question,
  stopped", and nothing more. T9 adds its date.
- **R11.** Neither the session store nor the flagged hold is backed up. No deletion
  request reaches a flagged exchange before its review closes, and whether that is lawful
  goes to counsel with OI-13 and OI-14.
- **R12.** No detail of family, friends, body or feelings goes into a kept summary, and
  T-PRM-10 audits the summaries for it.
- **R13.** A pattern the review at the close finds flags every exchange it runs through.
- **R14.** The answer to a typed question is still spoken. A "show, don't speak" control
  is put to you.
- **R15.** Within a conversation the child's words stay whole until the close, bounded by
  the time cap. D30's bounded summary covers the Primer's own turns.
- **R16.** T-PRM-10 and T-PRM-11 claim no more than their methods. T-PRM-10 is an audit
  with each vendor's confirmation. T-PRM-11 is a deterministic comparison of the text, with
  the voice's output sampled.
- **R17.** Without a connection the tablet shows one fixed screen, never spoken, that
  keeps nothing typed or heard.
- **R18.** PM2 has the first explainers drawn by hand from their specifications, and the
  code that draws them is built for PM4.
- **R19.** Small items: the fourth story's wording, OA-60 in PM1, CV-38 as the register
  has it, and app stores. OI-26 and OA-8 are restored to their wording.

**Round 2**

- **S1.** The Primer's voice is a stock synthetic voice, chosen from vendors at PM4 and
  cloned from no real person.
- **S2.** Every answer takes the whole shape. A question the bank cannot take through it
  gets "not yet" and joins the writing queue.
- **S3.** The front page plays your rough cut of "Version B with the Primer". "The
  football film" means Version C.
- **S4.** Where the film calls the boy's plan a clear one, P2 marks the line as a
  departure (D108).
- **S5.** The map's gloss for D73 describes it as D111 applies it.
- **S6.** P4 #people tells no fact about the players and repeats none of the figures.
- **S7.** The ledger's lede names D30 among the entries the films narrow.
- **S8.** Page 13's note under Stage 4 names the first-run screen at setup.
- **S9.** How T-PRM-07 handles audio is set in PM4's research protocol and its DPIA, with
  OI-17 open. D102 does not cover it.
- **S10.** T-PRM-10 looks for any turn of the child's, whole or in part, kept outside the
  read-back they accepted. The read-back may repeat a short phrase, never a whole turn.
  U13 replaces this: a short phrase, never more.
- **S11.** Only a safety reply, a stop and the screen without a connection are shown
  without being spoken.
- **S12.** After a stop or a safety reply the screen clears at the close. T10 replaces its
  wording.
- **S13.** Repeated stops across conversations flag the current exchange, at a threshold
  that is Unknown. T9 replaces where the count comes from.
- **S14.** The escalation record holds none of the child's words, and P4 names the cost.
- **S15.** The per-turn log never records which of family, the body, feelings or safety a
  turn was about. T11 replaces its wording.
- **S16.** A flag writes the words to the hold at once. The hold is replicated, never
  backed up, and a review that cannot run holds the conversation.
- **S17.** Whether the device rules' exception reaches the Primer's tablet is part of
  OI-31.
- **S18.** The writing queue holds the question rewritten in general terms, never the
  child's words.
- **S19.** Each drawing step is keyed to a reviewed sentence spoken word for word, and
  claim support compares the two.
- **S20.** PM4 measures how often a child is misheard. PM3 tests only whether children
  speak readily.
- **S21.** The map's notes are corrected, and nine nodes are added so that `impact`
  reaches the pages that state each rule.
- **S22.** P6 keeps no second decision rule, and OA-60 stays in PM1.
- **S23.** The spoken batteries use recordings made for testing with consent, or
  licensed, kept apart from any account.
- **S24.** A stand-in's own system updates wait until T-PRM-13's software check has passed
  on them.
- **S25.** A blocked read-back gets a fixed line asking once more. If that is blocked too,
  the close comes without a read-back.
- **S26.** The storage line of the cost formula names the log, the queues and the hold.
- **S27.** Wherever T-PRM-11 is cited, it is described by its method.
- **S28.** PM1 surveys competing products, children's tablets included, and the
  comparator row names a children's tablet.

**Round 3**

- **T1.** The map's labels for the tests carry their final definitions.
- **T2.** P3, D104 and D107 state S10's rule on the read-back.
- **T3.** The worked example's read-back repeats only a short phrase. A deterministic check
  blocks a whole turn or a longer run of the child's words. U13 narrows the check to any
  run longer than a short phrase.
- **T4.** T-PRM-06 (a) includes repeated stops wherever it is restated.
- **T5.** T-PRM-13 includes the stand-in's system updates wherever it is restated.
- **T6.** P1 and P4 say a parent sees each question as the catalogue question.
- **T7.** The map gains the turn, the named gaps, the manner, measuring, the safeguarding
  count and the escalation records.
- **T8.** This appendix.
- **T9.** A safeguarding count is kept apart from the parent's record, so the parent
  cannot delete it. U2 names what still resets it.
- **T10.** After a stop or a safety reply, the child's words leave the screen at once, and
  the screen does not sleep before the idle period has passed. T-PRM-08 covers the
  parent's record, the parent's screen and the account.
- **T11.** A flag never appears in the per-turn log, which records a flagged turn as a
  stop.
- **T12.** The test recordings are made or licensed before PM4, under a DPIA of their own.
- **T13.** A trained reviewer may read a conversation whose review could not run, and P2
  and P4 say so.
- **T14.** The new nodes' notes match their sections, and P4 #escalation states what the
  escalation record holds.
- **T15.** The fact, the positions, and the figures and stories in probing are said in
  placed reviewed sentences. Claim support blocks the generator's own factual sentence in
  any of them.

**Round 4**

- **U1.** P5's withholding rule and RP4 say the flag keeps an exchange out of the parent's
  record, screen and account. The reply stays on the child's tablet until the close.
- **U2.** A parent cannot delete the safeguarding count, but a new setup starts a new one.
  Whether it should follow the tablet or the adult is yours to decide, with counsel. The
  escalation record is kept for the policy's period, beyond a deletion request.
- **U3.** Test recordings are licensed, or made once counsel has answered on their lawful
  basis, in sessions held to the conditions for any child. Their scripts voice nothing of
  the child's own life. Until counsel answers, the spoken batteries cannot run.
- **U4.** The map gains eleven nodes, so that `impact` reaches every page that restates a
  rule.
- **U5.** The brief's account of what is kept names the date and the safeguarding count.
- **U6.** The flag is kept only with the safeguarding review: in the hold, the escalation
  record and the safeguarding count.
- **U7.** Restatements of T-PRM-11 and T-PRM-12 carry their latest additions.
- **U8.** This report's counts and quotations match the pages.
- **U9.** The worked example's read-back keeps the boy's "probably".
- **U10.** An explained stage holds only placed reviewed sentences, and claim support
  blocks any other sentence in one. This replaces T15's wording.
- **U11.** T-PRM-08 checks the withholding and T-PRM-10 the deletion, and each page credits
  them that way.
- **U12.** P4 names the flagged exchange and the conversation whose review could not run as
  the only exceptions to keeping none of the child's words.
- **U13.** The read-back may repeat a short phrase, never more, and the check blocks any
  longer run of the child's words. This replaces S10's "never a whole turn" and T3's
  check.

**Round 5**

- **V1.** No child speaks to the Primer until T-PRM-06's spoken battery has passed on the
  test recordings, and until then the talk key stays off. Speech therefore comes no sooner
  than counsel's answer on the recordings.
- **V2.** Anything a child says of their own in a recording session is cut from the
  recording. It is held for the trained reviewer where it takes 05's path, and otherwise
  deleted at once.
- **V3.** A blocked turn reaches adjudication with any personal detail removed. A flagged
  exchange's blocked turns move to the hold and are deleted when the review closes.
- **W1.** Test recordings are never backed up, before or after anything is cut from them.
  A part cut from one is held in the hold or deleted at once, and T-PRM-10's audit covers
  them.
- **W2.** The adjudication queue is never backed up. A conversation held because its review
  could not run moves its blocked turns to the hold.
- **W3.** Speech is first switched on for children only in a supervised pilot, PM4's or one
  held to its conditions.
