# FOUNDATION_CLASSROOM_REPORT

What `FOUNDATION_CLASSROOM_BRIEF.md` changed, the checks it passed, and what the
independent review found. Written 29 October 2026.

## 1. Outcome

Foundation is now designed as the owner described it: a classroom instrument for the
teacher of children of 4 to 7. A camera on a thin arm over every desk sees the page
and the hand, never the face. Foundation reads what is written, whether it is right,
where the working went wrong and how the pencil is held. The teacher's Windows PC
shows a quiet class view whose tiles turn amber, with plain words and a first triage.
Each child has a term summary for parents' evening. The child is shown nothing and
told nothing. It is sold to schools first, and it does not go first of the three
ideas, by the owner's order and with no judgement that it is the lesser idea.

The old design, a screen coaching a parent or teaching assistant through a session
at home, is replaced entirely, as the owner chose. The ledger keeps it: the six
decisions written for it carry a note saying what supersedes them for Foundation.

The owner's film is on the front page in Foundation's card, with a poster frame of
the desk unit and the caption "An illustrative film, made with AI. Nothing shown here
has been built." The idea is renamed Foundation everywhere current text names it;
page addresses keep the old spelling so that no link breaks.

Nothing has been built and no test has been run.

## 2. The decisions

Recorded in a new ledger section, `src/content/decision-ledger/057-foundation.html`.

**The owner's, D89 to D95:** the classroom tool for teachers, sold to schools, in
the background of a lesson, covering maths, verbal and non-verbal reasoning and
motor skills (D89); the desk unit (D90); what it reads (D91); the teacher's PC
(D92); what it never does (D93); the order, not first and not lesser (D94); and the
name (D95).

**Taken while writing, the owner's to keep or reverse, D96 to D100:**

- **D96, recognition, not generation.** The models recognise characters and joints;
  no model writes a word the teacher reads. Every verdict is computed, and every
  diagnosis is a wrong procedure that reproduces the child's answer. Keeps D54's
  reason.
- **D97, nothing seen is kept.** Frames are discarded as they are read; a frame with
  a face is discarded unread; no microphone.
- **D98, what is held.** The lesson readings and the term summary, as the school's
  record, for the school year; no inferred condition; no ranking a parent sees.
  Keeps D56's second half.
- **D99, a child who is not watched.** A parent's objection turns that desk off,
  and so does a child's own request through the teacher. Taken pending OI-28; if
  counsel requires consent, every camera starts off instead.
- **D100, the teacher's one step.** The teacher says what the class is working on
  before the lesson, and does nothing during it.

**Superseded for Foundation alone:** D43 and D55 by D89; D50's camera half by D90,
with D97 keeping its microphone half (D50 still governs the Primer); D54's letter by
D96; D56 by D91 and D98. D42's order is kept by D94 and its three reasons are
withdrawn, because they described the home design.

## 3. What changed

| Where | What |
|---|---|
| F1 to F6 | Rewritten for the classroom. F1 thesis, the teacher as the only user, what it sees, YC, the order, the weak points. F2 the desk unit, a lesson end to end with Miss Smith and Molly, the class view, the term summary. F3 the four domains, the error catalogue and who checks it, the clean room, the evidence, the tests. F4 the camera, the data held, escalation, the school's part, the US. F5 where it runs, the reader, computed checks and wrong procedures, the alert rules, cost. F6 schools as the customer, routes, economics, FM1 to FM4, RF1 to RF5, the decision rule. Each stays under 3,000 words. |
| Section ids | Kept where other pages link: `#claim`, `#who`, `#session`, `#worked`, `#record`, `#sequence`, `#number`, `#review`, `#cleanroom`, `#evidence`, `#measure`, `#data`, `#escalation`, `#schools`, `#gaps`, `#reuse`, `#arithmetic`, `#guide`, `#cost`, `#routes`, `#economics`, `#milestones`, `#build`. F4's `#voice` became `#camera`, and F5 gained `#deploy` and `#reader`; every link to them was updated. |
| Ledger | D89 to D100 in a new section; superseded notes on D42, D43, D50, D54, D55 and D56; the standfirst. |
| Counsel | OI-28 (the camera in England: lawful basis, biometric data, the schools rules, objection or consent, transparency to young children, a DPIA) and OI-29 (the camera in the US). OI-13 notes that Foundation now has no parent account. `CLAUDE.md` now says OI-1 to OI-29. |
| Assumptions | OA-48 to OA-52 in a new group, "Foundation in the classroom". OA-29, OA-30, OA-33 and OA-34 tested the home design and are withdrawn, listed by number and no longer counted. OA-28 stays as the owner's view, now supporting D93. The pattern line is recounted: eighteen of the forty-eight are resolvable by reading or asking. |
| Tests | T-FND-01 to T-FND-05 redefined and T-FND-06 added: never a face; nothing kept; answers computed; reading accuracy against a teacher; the alerts judged in an observed pilot; nothing reaches the child. |
| Shared pages | Which idea goes first: the answer and the Foundation section restated under D94, the tests table's Foundation column, the not-shared table. Field research: Foundation's questions rewritten for teachers, heads, coordinators, data protection officers and parents of a class that would have the units. Contents, the unresolved table, P1, P4 and P6 brought into line. |
| Map | The five Foundation nodes became the desk unit, the class view, the error catalogue, the page and hand reader and the class record; `gov.novoice` is relabelled and now covers a camera that never sees a face. 101 nodes and 194 edges, from 100 and 191. |
| Name | "Foundation" in every title, heading and line of current text, the build's descriptions, `roles.json`, README and `CLAUDE.md`. The historical briefs and reports at the root keep the old name. |
| Views | `roles.json`: the film, the link "See a lesson", the owners' frames (each at or under 200 words, no figures). README and `CLAUDE.md`: the description, the counts, the new brief and report. The status page's sentence on maturity. |

**Counts, before and after:** documents 32 and 32; tests 32 and 33; counsel questions
27 and 29; assumptions 47 and 48, with 19 and 18 resolvable cheaply; decisions 88 and
100. The status page computes them and agrees.

**Markers.** No Verified marker was added and no marker on a surviving claim was
changed. Markers went only with claims the owner's replacement deleted:

- in F1, six: the Assumed markers on CV-04 (the novel), on CV-01 twice (D42's order
  and the condition for revisiting it), and on CV-09 twice (the phonics sequence), and
  one Unknown on what families spend on early reading;
- in "which idea goes first", three Assumed markers on D42's withdrawn reasons;
- one Unknown each in F3 (the old reading sequence) and in F4 (adults who read English
  with difficulty, a gap of the home design).

One claim survived and lost its marker in the first commit: F1's description of YC's
request. The review caught it, and its Assumed CV-01 marker is back. Claim tags were
rewritten where their claims were. P1's claim box on the order keeps its tag, D42,
because D94 keeps D42's order; the paragraph after it now cites D94.

## 4. The film

The owner's narrated cut, 76 seconds at 720p and 15.9 MB, is published unchanged as
`docs/media/foundation.mp4`; its index already sits at the front of the file, so it
streams. The poster, `docs/media/foundation.jpg`, is a frame of the desk unit at ten
seconds. The site's policy already allows media from its own origin, and the card
renders at phone and desktop widths with no overflow.

Three things the README's film rules ask that the build could not do:

- **An AI label in the film itself.** The README asks that an AI-generated film say
  so in the film. The card's caption says so; the film shows only a small sparkle
  mark in one corner, which a viewer may not read as a label.
- **Captions.** No captions track was added. Transcribing the narration needed a
  speech model this environment could not reach. A `.vtt` file named in
  `roles.json` under `captions` would add one.
- **Children.** The film shows AI-generated children, some with their faces. None is
  a real child, so the consent rule does not apply, but a viewer cannot tell that
  without the label.

The film's canon is fixed in the brief, section 6, for every future clip. One detail
is an interpretation: the column sum 16 + 8 + 19 is shown with a carried 1. The
documents read it as the child's mistake, since the units make 23 and the carry
should be 2, and as the mistake in the working that Foundation points to.

## 5. Checks run, and what each returned

| Check | Result |
|---|---|
| `python3 src/build.py` | Passes; 71 files assembled for publishing, the film included. |
| `python3 tools/verify.py` | All checks pass: build fresh; links and anchors, 0 broken; the map, every locus resolves; the views, 0 problems. |
| Markers against `origin/main` | No Verified added; removals only with deleted claims, listed above. |
| House style | No em-dashes or en-dashes, no American spellings in the new text. |
| Word counts | F1 2,151; F2 2,428; F3 2,238; F4 2,990; F5 2,229; F6 2,249, after the review's fixes. |
| Rendering | The front page, F1 to F6, which idea goes first, the field research guide, the ledger, the open items, status and contents at 390 and 1280 pixels: no horizontal overflow and no failed request. The film card screenshotted at both widths. The film's type, size and policy checked as served; the test browser has no H.264 decoder, so playback itself was not tested here. |

## 6. The independent review

A fresh agent reviewed the whole change without the conversation, reading CLAUDE.md,
the brief, every Foundation fragment and the diffs of every other file touched. It
found no dashes, American spellings, invented figures or Verified markers, no counsel
question written as answered, no broken anchors, and the arithmetic right throughout.
It found 7 blocking problems and 30 others. All are fixed in the second commit unless
stated.

**Blocking, all fixed:**

1. **The map's glosses described the home design.** The dependency map's tests, risks
   and D43 to D56 glosses still had the old text, and D89 to D100, OI-28, OI-29,
   OA-48 to OA-52, T-FND-06 and the new RF rows had none. All are rewritten or added
   in `src/viz/dependency-map.html`, and the withdrawn OA-30 and OA-33 glosses are
   removed.
2. **The front page's opening sentence** still said one idea "helps an adult teach a
   young child". It now says one tells the teacher of a young class which child needs
   help, and with what, and the shared rule no longer calls every idea a tutor.
3. **The brief promised an outcome.** "No one gets left behind" is the film's closing
   line, so it stays, framed as the aim; "Foundation can" is now "Foundation is
   designed to".
4. **F1's description of YC's request had lost its CV-01 marker**, and attributed to
   the request a point it does not make. The marker is restored and the sentence
   reworded.
5. **The arm was called fixed**, though D90 and the film make it flexible. The pages
   now say it is set at installation and then locked, and D97 records that as a design
   choice.
6. **Faces were said never to be processed**, though the face check reads every frame
   to discard those with a face. The pages now say a face is discarded by the check
   before anything else reads it, and OI-28 asks whether that check is itself
   biometric processing.
7. **The pattern line** still said "those nineteen" and "M1 and PM1". It says eighteen,
   names OA-51, and adds FM1.

**Other findings, fixed:**

- P1's paragraph on the order separates the owner's view (OA-28) from the order
  (D94).
- F1 says six superseded decisions, not five; and it no longer says the owner intends
  to build Foundation regardless of F6's rule.
- F4's standfirst names the three counsel answers the pilot waits on, matching FM3;
  its DPIA gap now covers FM2's collection as well as the pilot.
- The term summary says 4 &times; 6 was "once answered 16, which adding can give", not
  that the child added.
- The film's sentence: all three pages now list the comma before "Spike" with the
  capitals and the full stop, as the film's verdict panel does.
- F3's domains lede now matches the owner's four domains and explains the table's
  rows.
- F5 says every diagnosis of a wrong answer is computed, by recomputing the working
  or reproducing the answer, not that every diagnosis is a reproduced procedure.
- T-FND-04's threshold is written before FM2 on every page.
- The field research guide: a question tests OA-28 again; the closing question no
  longer tests D42; the log example cites OA-51.
- Which idea goes first: the case for one product no longer assumes families buy
  Foundation; "included for completeness" and "designed as fully as the Primer" are
  replaced.
- OI-17 limits Foundation to a microphone ever being added. OA-28's cost of being
  wrong no longer describes an adult's time. Counsel's frame describes Foundation's
  camera rather than its users' ages.
- F4: the class view is never shown on a screen the class can see, and parents'
  evening opens one child's summary at a time; readings belong to a desk, so a child
  who moves is misattributed until the teacher changes the seating; "the contract
  must say so"; age assurance "largely falls away", as 05 says of Route B; the
  escalation section rests on D89 and no longer counts its bullets; the leftover
  "one set of settings" is gone.
- The candidates register's "used in" columns for CV-01, CV-04, CV-09 and CV-11 no
  longer name pages that stopped citing them.
- D90 and D92 in the ledger now use the owner's words.
- The open items' head says FM1 puts Foundation's questions to counsel, not that it
  answers them. The unresolved table says Foundation "does not go first" rather than
  "is ruled out", and lists where Foundation runs as a decision not taken.
- F6 says D51's exclusion of India covers ideas sold to families, and that offering
  Foundation to schools in India is not considered.
- F3 no longer claims what Year 2 covers.
- The pages' maturity line said "reviewed once" before the review reported; it now
  says "revised once after an independent review".
- This report's marker list undercounted the removals; it is corrected above.

**Kept, with the reason:**

- **P1's claim tag, D42.** Changing a claim's tag on a surviving claim is close to
  changing its marker, and D94 keeps D42's order, so the tag still holds. The
  paragraph after it cites D94.

## 7. What is left for the owner

- **Keep or reverse D96 to D100.** D99 goes slightly beyond your words: it lets a
  child's own request turn their desk off, as well as a parent's objection. D97 now
  also locks the arm after installation.
- **Two rules the review prompted,** both design choices in F4 and F2: the class view
  never appears on a screen the class can see, and a desk's readings follow the desk,
  so the teacher updates the seating when a child moves.
- **The film's AI label and captions**, above.
- **Where Foundation runs.** D90 allows the school's servers or the cloud. The
  documents do not choose; FM2 measures what each costs.
- **The decision rule at FM4** in F6 is proposed, for you to adopt or amend before
  FM1 reports.
- **The risks RF1 to RF5** are ordered by the documents' judgement, not yours.
