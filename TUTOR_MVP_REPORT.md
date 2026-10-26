# TUTOR_MVP_REPORT

What `TUTOR_MVP_BRIEF.md` changed, the checks it passed, and what the independent
review found. Written 26 October 2026.

## 1. Outcome

The Tutor has a build guide for an MVP that runs the whole design for adults who play
learners of 14 to 18: one-objective sessions, the verified turn pipeline, the style
engine, the self-tutor in the tester's own face and voice, papers, the grade range
and the parent report. It teaches the algebra of GCSE Mathematics, GCSE Further
Mathematics and A-level Mathematics, drafted by agents, checked by a computer algebra
system, and validated by no examiner. The guide is a Tutor page, `tutor-mvp.html`.
The specification pack Claude Code builds from is published beside it at
`/mvp/tutor/`.

The pack is the instruction manual the owner asked for. It is built on the harness
first: a `CLAUDE.md` of fifteen invariants for the MVP's repository, the contracts
between the planes, every vault test written as a failing test before its code, a
frozen battery, hooks that lint each edit and refuse to let a session or an agent
finish while the fast tests fail, permission rules that ask the owner before a
contract, a test or a threshold changes, and seven agents: six builders, each in its
own worktree, and a reviewer. `PROMPTS.md` then gives one prompt for each of six
phases, each ending in something the owner can try.

Three things did not happen:
- No counsel question was answered. The MVP holds adult testers' faces and voices,
  and the guide and the ledger say it does not settle their standing in law; the
  export a tester can request holds no likeness, and whether the product's subject
  access route must reach one stays OI-23.
- No Verified marker was added, and no existing marker was changed.
- Nothing says the MVP shows how learners engage or learn, or that its items are
  validated, and no model vendor is named for the Tutor itself.

The Tutor's design does not change. The MVP departs from D24 for its text models,
from P1's validation and from D30's rolling summary, for itself only, and says so
in the guide, the ledger and the pack.

Counts after this work, computed by the build:

| | |
|---|---|
| Documents | 32 |
| Decisions | 88: 14 settled (two since amended by the owner), 74 taken |
| Counsel questions | 27, none answered |
| Assumptions | 47, of which 19 are resolvable by reading or asking |
| Tests specified | 32, none run |
| External claims | 42 registered, plus 30 candidates awaiting the owner's check |

## 2. The owner's decisions and the defaults

**The owner's decisions, 26 October 2026,** after five ways to build were set out
and the second recommended:
- **D80.** The Tutor is shown first by an MVP that matches the product as closely as
  it can, built for speed, with cost and latency last; a harness first, then a team
  of Claude Code agents. It is not M2's release.
- **D81.** Only adults use it, playing learners of 14 to 18.
- **D82.** Its content is the algebra of three qualifications, GCSE Mathematics, GCSE
  Further Mathematics and A-level Mathematics; A-level Further Mathematics and
  Additional Mathematics are left out, as the owner confirmed when asked.
- **D83.** The self-tutor's voice and face run on open models the MVP hosts itself.

**Taken while writing, for the owner to keep or reverse:**

| | Decision |
|---|---|
| D84 | The harness before any build prompt; nothing merges while a test fails |
| D85 | Both GCSE tiers; GCSE and A-level objectives from the DfE content; Further Mathematics from no board's material, approved by the owner; papers of the MVP's own structure |
| D86 | The tools: Claude Opus 5.5 for turns and the safety check; Gemini 4 Argon for the entailment and scope checks; SymPy; Chatterbox, MuseTalk, MediaPipe, Silent-Face-Anti-Spoofing and Whisper; Modal and Neon. The text models on standard terms, for the MVP alone |
| D87 | Accounts by invitation; transcripts and progress kept for the test period, then deleted with everything else about testers but counts and timings |
| D88 | Left out: payment, real age assurance, real creators, Route B's school features, the US course and D30's rolling summary |

## 3. What was added

- **The guide,** `src/content/tutor-mvp.html`, 2,533 words: what is built; the five
  paths and the one chosen; the harness; the agent team; the content; the self-tutor
  on open models; the tools; testers, safety and data; costs and caps; the phases;
  and what the MVP cannot show.
- **The pack,** `mvp/tutor/`:
  - `README.md`: what each file is, where it goes, and how the harness works.
  - `CLAUDE.md`: the MVP repository's invariants, each held by a test, and how to
    work, including the phase gating of tests.
  - `SPEC.md`: the departures from the product; the stack, accounts, secrets and
    settings; the repository and the contracts; the data model; content and the
    clean room; one syntax for mathematics, its checks, MathML and its spoken form;
    the session; the turn pipeline with the four checks and the gate; figures; the
    style engine, with a golden test against 02's Groundwork card; the self-tutor;
    papers and the grade range; safety; accounts, roles and surfaces; deployment;
    the tests; and failures.
  - `agents/`: the content author (no web access), the pipeline, style, likeness, app
    and platform engineers, and the reviewer (no edits).
  - `settings.json` and `hooks/`: the permissions and the hooks, with the scripts
    they run.
  - `PROMPTS.md`: what to do before phase 0, a prompt for each phase from 0 to 5,
    and the checklist before testers.
- **Registers.**
  - Decisions D80 to D88 in a new ledger section, `055-tutor-mvp.html`, between the
    Primer's demonstration and the decisions not taken; the ledger's standfirst
    counts them.
  - Assumptions OA-45 to OA-47 in a new group, "The Tutor's MVP"; the lede and the
    pattern line count them, and the nineteen resolvable by reading stay nineteen.
  - Candidates CV-24 to CV-30, and the guide's uses of CV-20, CV-21 and CV-22.
- **Shared pages.** The contents page's investor route names the guide; the front
  page's Tutor card links it; 11's M2 says the MVP is not its release.
- **Ownership.** The CTO owns the page, the COO its content section, the CFO its
  costs and counsel its safety section; the four frames each gain a clause, the
  CTO's rewritten to stay within its cap.
- **The build.** `PAGES` and `GROUPS` gain the page. Nothing else in the build
  changes: `mvp/` was already published and served as text.
- **Root files.** README (counts and layout) and CLAUDE.md (map and page ranges).

## 4. What the research changed

- **Face models.** Many open talking-head pipelines depend on InsightFace's
  pretrained models, which are for non-commercial research only (CV-25). That
  excluded them, and is why the guide names MuseTalk, whose code is MIT and whose
  model may be used commercially, and makes a licence audit of every dependency the
  first task of phase 1 (OA-45).
- **Voice models.** Several open voice-cloning models are permissively licensed and
  clone at inference from a short sample (CV-24), so D65's render-time conditioning
  costs nothing. Chatterbox also watermarks every file it makes.
- **The verifier's model.** D27 needs a family other than the generator's. Gemini 4
  Argon became generally available on 13 October 2026 (CV-28) and is used for the
  entailment and scope checks.
- **Further Mathematics.** No DfE content for it was found, and the qualification
  found is AQA's certificate, from the board whose policy EV-21 records (CV-29). Its
  objectives are written from no board's material and approved by the owner (D85).
- **Claude Code.** A research agent read Claude Code's documentation on memory,
  subagents, hooks, permissions, worktrees and agent teams (CV-30). The harness uses
  only stable features: subagents with worktree isolation, command hooks on edits
  and on stopping, and permission rules. Agent teams, which are experimental, are not
  used.
- **Hosting.** The MVP needs GPUs, so it runs on Modal with Postgres on Neon (CV-27),
  and not on the Netlify team that hosts this site, whose credits, once spent, pause
  every project in the team (CV-22).
- **What could not be opened.** Hugging Face, Modal, RunPod and gov.uk could not be
  reached from the build environment. Licence files and READMEs on GitHub and Google
  Cloud's pricing page were opened directly; the rest was read through search
  summaries, and each candidate row says which.

## 5. Checks run, and what each returned

| Check | Result |
|---|---|
| `python3 src/build.py` | Exit 0 |
| `python3 tools/verify.py` | All checks pass: build fresh, 4,425 links in 44 files with none broken, map loci resolve (100 nodes, 191 edges), no view or ownership problems |
| Existing markers | Every marker in every edited source matches `main`; the work only adds markers |
| Verified markers added | None |
| Dashes and American spellings in anything new | None |
| Page size | The guide is 2,533 words by the build's own counter, under the 3,000-word limit; the front page and the Tutor summary stay within their caps |
| Rendering | Every touched page fits at 390 px and 1280 px with no failed request |
| Hook scripts | Run against a scratch repository: the stop hook refuses while `make test` fails, five times in a row and then lets the session stop, in the main checkout and in a worktree; the edit hook reports lint failures and passes a clean file; the guard refuses a file holding an API key; each does nothing before the harness exists |
| `settings.json` | Valid JSON, with 61 permission rules and 5 hook events |

## 6. The independent review

To follow when the review returns.

## 7. What is left for the owner

- Keep or reverse D84 to D88, and the settings `SPEC.md` 3.4 lists as design
  choices.
- Check candidates CV-24 to CV-30. The first phase checks the licences again, in
  `docs/licences.md`, before any model is used.
- Write down, before the phases that need them, the thresholds the pack leaves to
  the owner: the liveness and false-accept thresholds before phase 3, the style
  scales and T-STY-01's band before the first battery, and T-STY-02's sample size
  before phase 5.
- Approve, when asked, the Further Mathematics objectives, the fictional preset, the
  look, the paper specifications and the grade range's mapping.
- Read the reviewer queue at least once a day while testers use the MVP, and never
  let a learner under 18 use it.
