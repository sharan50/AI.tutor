# AI.tutor: the Tutor MVP brief

Commit this file at the repository root as `TUTOR_MVP_BRIEF.md`. It records what the
owner decided on 26 October 2026 about a first build of the Tutor, and turns it into
instructions a fresh Claude Code session can execute. Everything binding is in this
file; nothing depends on conversation history.

`BUILD_BRIEF.md` remains the source instruction for the Tutor and for the vault's
rules. This brief governs the Tutor's MVP build guide (`src/content/tutor-mvp.html`),
the specification pack it publishes for Claude Code (`mvp/tutor/`), and the register
entries it adds: decisions D80 to D88, assumptions OA-45 to OA-47 and candidate claims
CV-24 to CV-30.

## 1. What the MVP is

A working build of the Tutor that matches the product described in 01, 02 and 06 as
closely as an MVP can, used only by adults who play learners of 14 to 18. It runs the
whole design: sessions with one objective, an unaided check and an honest close; the
turn pipeline, with a deterministic composer, a generator, a four-part verifier and a
gate that falls back to the item verbatim; figures rendered from data; practice papers
and the provisional grade range; the style engine, with archetypes, a licensed preset,
student adjustments and the kill switch; the self-tutor, with two consents, live
capture, a liveness check, a passcode, voice and face rendered after the gate, labels
and deletion; the parent report; safety routing to a reviewer; and a validator
console.

What it does not have is the examiner: every item is drafted by agents and checked by
a computer algebra system, and every screen says that no examiner has validated it.
No child uses it. It is not M2's release, it is not evidence about learners, and it
decides nothing about the route or which idea goes first.

The owner's priorities: speed of building and fidelity to the product description
first; running cost and latency last.

## 2. The owner's decisions, 26 October 2026

Five ways to build were discussed: one agent, plane by plane; a harness first, then a
team of agents; an agent-native tutor; buying the visible layer and building only the
content and verification planes; and an AI app builder for the app with services for
the core. The second was recommended, as the only one fast without dropping a promise.
The owner then took the three decisions it needed and chose no other path:

- **Who uses it:** adult testers (D81).
- **Content:** the full algebra strand for ages 14 to 18 in three qualifications, GCSE
  Mathematics, GCSE Further Mathematics and A-level Mathematics; A-level Further
  Mathematics and Additional Mathematics are left out (D82). The owner confirmed the
  three when asked.
- **The self-tutor's voice and face:** open models, run by the MVP itself (D83).

D80 records the path.

## 3. Defaults taken while writing

The owner did not specify these. Each is a decision the owner may keep or reverse: the
harness (D84), the content's sources and tiers (D85), the models and hosting (D86),
what testers' data is kept (D87) and what the MVP leaves out (D88).

## 4. Decisions D80 to D88

Recorded in a new ledger section, `src/content/decision-ledger/055-tutor-mvp.html`,
`<h2 id="tutor-mvp">D80 to D88: the Tutor's MVP</h2>`, placed after the Primer's
demonstration and before the decisions not taken, each as `<dt>` and `<dd>` with
Driven by, Rejected and Makes harder. The last link in each entry names its owner.

- **D80.** The Tutor is shown first by an MVP that matches the product's capabilities
  as closely as it can, built for speed, with running cost and latency deprioritised.
  It is built by a harness first and then a team of Claude Code agents. It is not M2's
  release and decides nothing about the route or which idea goes first. Owner: the
  CEO, through 11's M2.
- **D81.** Only adults use it, playing learners of 14 to 18. No child uses it, and it
  holds no child's data. Owner: counsel.
- **D82.** Its content is the algebra strand of GCSE Mathematics, Level 2 Further
  Mathematics and A-level Mathematics, drafted in full by agents under the clean-room
  rule (D12), checked by the computer algebra system, and labelled as not validated by
  an examiner. Owner: the COO.
- **D83.** The self-tutor's voice and face run on open models the MVP hosts on rented
  GPUs, so no speech or animation vendor receives a likeness; for the likeness, D24
  and D65 hold by construction. Owner: the CTO.
- **D84.** The harness is built before any build prompt: a CLAUDE.md of the design's
  invariants, the contracts between the planes, the vault's tests as failing tests, a
  frozen battery, hooks that run the tests, one subagent per plane and a reviewer
  agent; nothing merges with a failing test. Owner: the CTO.
- **D85.** Both GCSE tiers. GCSE and A-level objectives are written from the DfE
  subject content. No DfE content for Level 2 Further Mathematics was found, and
  AQA's certificate, the one found, comes from the board whose AI policy EV-21
  records, so its objectives are written from no board's material and approved by
  the owner.
  Practice papers follow the MVP's own structure, not a board's. Owner: the COO.
- **D86.** The tools: Claude Opus 5.5 generates turns and classifies safety; Gemini 4
  Argon checks entailment and scope, a different family as D27 requires; SymPy checks
  the mathematics; Chatterbox speaks and MuseTalk animates, with MediaPipe, a passive
  anti-spoofing model and Whisper checking liveness; the app, its workers, the
  renderers and the likeness store run on Modal, with Postgres on Neon. The text
  models are used on their standard terms, a departure from D24 for the MVP alone. The
  choice binds the MVP only. Owner: the CTO.
- **D87.** Testers' data: accounts by invitation; transcripts and progress kept for
  the test period and deleted at its end, with everything else about testers except
  counts and timings; likenesses under D63's rules; nothing about a tester's life
  beyond what they type. Owner: counsel.
- **D88.** Left out: payment, real age assurance (a simulated check stands in), real
  creators (one fictional licensed preset shows the machinery), Route B's school
  features, the US course, and D30's rolling summary, because a whole session fits
  in the window. Owner: the CTO.

## 5. Register entries

**Assumptions**, in a new group, "The Tutor's MVP", after "The Primer" in
`14-open-items/020-assumptions.html`, each marked new:

- **OA-45.** That open voice and face models make a recognisable likeness from a
  short live capture, and that every model and dependency used is licensed for
  commercial use. Resolved in the first phase by a spike and a licence audit.
- **OA-46.** That the computer algebra system catches most errors in agent-drafted
  items, so that a mathematics teacher reading a sample finds few it missed. Resolved
  in testing.
- **OA-47.** That the owner, directing an agent team on this harness, can build the
  MVP without a hired engineer. The owner's premise; tested by the first phase.

The lede gains "three by the Tutor's MVP"; the pattern line's total becomes
forty-seven, and its count of nineteen readings is unchanged.

**Candidates**, in `sources/080-candidates.html`, found 26 October 2026:

- **CV-24.** Open voice-cloning models and their licences: Chatterbox (MIT, zero-shot,
  a watermark in every output), OmniVoice and CosyVoice (Apache 2.0); XTTS-v2 and
  F5-TTS's weights carry non-commercial terms.
- **CV-25.** Open face-animation models and their licences: MuseTalk (MIT code, its
  trained model usable commercially, real time on a V100, dependencies under their
  own terms); EchoMimic (Apache 2.0); InsightFace's pretrained models are for
  non-commercial research only, and Ditto's pipeline ships one.
- **CV-26.** Liveness and speech checks: MediaPipe (Apache 2.0) has a face landmarker
  for the web; Silent-Face-Anti-Spoofing is Apache 2.0; Whisper is MIT.
- **CV-27.** Modal bills GPUs by the second, at rates third parties list.
- **CV-28.** Gemini 4 Argon: generally available on the Gemini API as
  `gemini-4-argon`, and priced on Google Cloud's page.
- **CV-29.** The DfE subject content for GCSE and A-level Mathematics, and AQA's Level
  2 Certificate in Further Mathematics.
- **CV-30.** Claude Code's harness features the guide relies on.

No counsel question is added, and no test identifier: the MVP runs the vault's tests;
it does not define new ones.

## 6. What the research found

- Many open face-animation pipelines depend on InsightFace's pretrained models, which
  are for non-commercial research only. That excludes them for a venture's MVP, and it
  is why the guide names MuseTalk and requires a licence audit of every dependency on
  the first day.
- Open voice models that clone from a short sample at inference are common, and
  several are permissively licensed, so D65's render-time conditioning costs nothing.
- Google's newest model, Gemini 4 Argon, became generally available on the Gemini API
  on 13 October 2026; the verifier uses it.
- Hugging Face, Modal, RunPod and gov.uk could not be opened from the build
  environment. Licence files and READMEs on GitHub, and Google Cloud's pricing page,
  were opened directly; the rest was read through search summaries, and each
  candidate row says which.

## 7. Where each part goes

- **The page,** `src/content/tutor-mvp.html`, unnumbered, in the Tutor group, under
  3,000 words: `#what`, `#paths`, `#harness`, `#team`, `#content`, `#selftutor`,
  `#stack`, `#safety`, `#costs`, `#phases`, `#limits`. Owned by the CTO, except
  `#content` (the COO), `#safety` (counsel) and `#costs` (the CFO).
- **The specification pack,** `mvp/tutor/`, hand-maintained and published as text at
  `/mvp/tutor/`: a README, the MVP repository's `CLAUDE.md`, `SPEC.md`, the subagent
  definitions in `agents/`, a `settings.json` with hooks and permissions, the scripts
  those hooks run in `hooks/`, and `PROMPTS.md` with the phase prompts and the
  checklist before testers.
- **The build:** `PAGES` and `GROUPS` gain the page.
- **Registers:** the ledger section and its head; the open items; the candidates and
  their note.
- **Shared pages:** the contents page's investor route names the guide; the front
  page's Tutor card links it; 11's M2 says the MVP is not its release.
- **Ownership:** `roles.json` gives the page to the CTO with the three sections above.
- **Root files:** README, CLAUDE.md, and `TUTOR_MVP_REPORT.md` when the work is done.

## 8. Rules for this work

1. D1 to D79 stand. The MVP departs from D24 for its text models, from P1's
   validation and from D30's rolling summary for itself only, and says so wherever it
   does; the Tutor's design does not change.
2. Counsel questions OI-1 to OI-27 stay open and none is written as answered.
3. House style is `BUILD_BRIEF.md` section 7: British English, no em-dashes or
   en-dashes, conclusions before reasoning, and weak things called weak.
4. Every number on the page is from the evidence register, a stated design choice, or
   marked Unknown. A provider's price, a model's licence or a tool's feature is a
   candidate (D53) and carries an Assumed marker naming it. No Verified marker is
   added; no existing marker is changed.
5. Edit `src/`, `roles.json`, root files and `mvp/`; never `docs/`, `evidence/` or
   `viz/` by hand. Python 3 standard library only.
6. Nothing may suggest the MVP shows how learners engage or learn, or that its items
   are validated. No real learner is shown, and no child is invited to use it.
7. Nothing may name a model vendor for the Tutor itself; the MVP's choices bind the
   MVP only.
8. No board material reaches any agent: no specification, past paper or mark scheme.

## 9. Acceptance bar

1. `python3 src/build.py` and `python3 tools/verify.py` pass.
2. Every existing marker in every edited file is unchanged, in order.
3. No dashes and no American spellings in anything new, apart from code and URLs.
4. The page is under 3,000 words; the front page and the Tutor summary stay within
   their caps.
5. Every touched page fits at 390 px and 1280 px.
6. An independent review, given the rules and the change but not the conversation,
   finds nothing blocking, or every finding is fixed and recorded in the report.
