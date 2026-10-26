# TUTOR_MVP_REPORT

What `TUTOR_MVP_BRIEF.md` changed, the checks it passed, and what the independent
review found. Written 26 October 2026.

## 1. Outcome

The Tutor has a build guide for an MVP that runs the whole design for adults who play
learners of 14 to 18. That covers one-objective sessions, the verified turn pipeline,
the style engine, the self-tutor in the tester's own face and voice, papers, the grade
range and the parent report. It teaches the algebra of GCSE Mathematics, Level 2
Further Mathematics (the owner's "GCSE Further Maths") and A-level Mathematics. Agents
draft it, a computer algebra system checks it, and no examiner validates it. The
guide is a Tutor page, `tutor-mvp.html`. The specification pack that Claude Code
builds from is published beside it at `/mvp/tutor/`.

The pack is the instruction manual the owner asked for, and the harness comes first:
- a `CLAUDE.md` of sixteen invariants for the MVP's repository, each held by a test;
- the contracts between the planes;
- every vault test written as a failing test before its code, marked with the phase
  by which it must pass;
- a frozen battery;
- hooks that lint each edit, refuse to let the lead or a builder finish while the
  tests of finished phases fail, refuse secrets, and refuse any fetch from an exam
  board's site;
- a git hook that refuses a merge which breaks those tests;
- seven agents: six builders, each in its own worktree branched from the lead's
  current work, and a reviewer.

`PROMPTS.md` then gives one prompt for each of six phases. Each phase ends with
something the owner can try and the phase's own tests passing.

Three things did not happen:
- **No counsel question was answered.** The MVP holds adult testers' faces and
  voices, and the guide and the ledger say it does not settle their standing in law.
  The export a tester can request holds no likeness. Whether the product's subject
  access route must reach one stays OI-23.
- **No Verified marker was added, and no existing marker was changed.**
- **No claim of learning, validation or vendor.** Nothing says the MVP shows how
  learners engage or learn, or that its items are validated. No model vendor is
  named for the Tutor itself.

The Tutor's design does not change. For itself only, the MVP departs from:
- D24, for its text models;
- P1's validation;
- D19's board alignment;
- 06's bought speech and animation;
- D29's quarterly rehearsal;
- D30's rolling summary.

It says so in the guide, the ledger and the pack.

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
  it can, built for speed, with cost and latency last. A harness is built first, then
  a team of Claude Code agents builds the MVP. It is not M2's release.
- **D81.** Only adults use it, playing learners of 14 to 18.
- **D82.** Its content is the algebra of three qualifications: GCSE Mathematics,
  Level 2 Further Mathematics and A-level Mathematics. A-level Further Mathematics and
  Additional Mathematics are left out, as the owner confirmed when asked.
- **D83.** The self-tutor's voice and face run on open models the MVP hosts itself.

**Taken while writing, for the owner to keep or reverse:**

| | Decision |
|---|---|
| D84 | The harness before any build prompt; nothing merges while the tests of finished phases fail |
| D85 | Both GCSE tiers. GCSE and A-level objectives come from the DfE content. Each Further Mathematics objective comes from the DfE content it extends, and the owner approves the list. Papers follow the MVP's own structure |
| D86 | The tools: Claude Opus 5.5 for turns and the safety check; Gemini 4 Argon for the entailment and scope checks; SymPy; Chatterbox, MuseTalk, MediaPipe, Silent-Face-Anti-Spoofing and Whisper; Modal and Neon. The text models run on standard terms, for the MVP alone |
| D87 | Accounts by invitation. Transcripts and progress are kept for the test period, then deleted with everything else about testers except counts and timings |
| D88 | Left out: payment, real age assurance, real creators, Route B's school features, the US course, D29's quarterly rehearsal and D30's rolling summary |

## 3. What was added

- **The guide,** `src/content/tutor-mvp.html`, 2,730 words. It covers:
  - what is built;
  - the five paths and the one chosen;
  - the harness and the agent team;
  - the content;
  - the self-tutor on open models;
  - the tools;
  - testers, safety and data;
  - costs and caps;
  - the phases;
  - what the MVP cannot show.
- **The pack,** `mvp/tutor/`:
  - `README.md`: what each file is, where it goes, and how the harness works.
  - `CLAUDE.md`: the MVP repository's invariants, how to work, and how tests are gated
    by phase.
  - `SPEC.md`, covering:
    - the departures from the product;
    - stack, accounts, secrets and settings;
    - the repository, with who changes what;
    - the contracts and the data model;
    - content and the clean room;
    - one syntax for mathematics, with its checks, MathML and spoken form;
    - the session;
    - the turn pipeline, with the four checks and the gate;
    - figures;
    - the style engine, with a golden test against 02's Groundwork card;
    - the self-tutor;
    - papers and the grade range, with 05's safeguards;
    - safety, accounts, roles and surfaces;
    - deployment;
    - the tests, with which ones gate a phase;
    - failures.
  - `agents/`: the content author (no fetch tool, and a shell that runs only its
    checks and git), the pipeline, style, likeness, app and platform engineers, and
    the reviewer (no edits).
  - `settings.json`, `hooks/` and `githooks/`: the permissions, the Claude Code hooks
    and the merge gate.
  - `PROMPTS.md`: what to do before phase 0, a prompt for each phase from 0 to 5,
    and the checklist before testers.
- **Registers.**
  - Decisions D80 to D88 in a new ledger section, `055-tutor-mvp.html`, between the
    Primer's demonstration and the decisions not taken. The ledger's standfirst
    counts them.
  - Assumptions OA-45 to OA-47 in a new group, "The Tutor's MVP". The lede and the
    pattern line count them, and the nineteen resolvable by reading stay nineteen.
  - Candidates CV-24 to CV-30, plus the guide's uses of CV-20, CV-21 and CV-22.
- **Shared pages.**
  - The contents page's investor route names the guide.
  - The front page's Tutor card links it.
  - 11's M2 says the MVP counts towards none of M2's exit conditions.
- **Ownership.** The CTO owns the page, the COO its content section, the CFO its
  costs and counsel its safety section. The four frames each gain a clause, and the
  CTO's is rewritten to stay within its cap.
- **The build.** `PAGES` and `GROUPS` gain the page. Nothing else in the build
  changes: `mvp/` was already published and served as text.
- **Root files.** README (counts and layout) and CLAUDE.md (map and page ranges).

## 4. What the research changed

- **Face models.** Some open talking-head pipelines depend on InsightFace's
  pretrained models, which are for non-commercial research only, and Ditto's ships
  one (CV-25). That rules them out. It is why the guide names MuseTalk, whose code is
  MIT and whose model may be used commercially, and makes a licence audit of every
  dependency the first task of phase 1 (OA-45).
- **Voice models.** Several open voice-cloning models are permissively licensed and
  clone from a short sample at inference (CV-24), so D65's render-time conditioning
  costs nothing. Chatterbox also watermarks every file it makes.
- **The verifier's model.** D27 needs a model family other than the generator's.
  Gemini 4 Argon became generally available on 13 October 2026 (CV-28), and it runs
  the entailment and scope checks.
- **Further Mathematics.** No DfE content for it was found. The qualification found
  is AQA's certificate, from the board whose policy EV-21 records (CV-29). Each
  objective is tied to the DfE content it extends, and the owner approves the list
  (D85). This stays weak, and D85 says so.
- **Claude Code.** Its documentation on memory, subagents, hooks, permissions,
  worktrees, sandboxing and agent teams was read; the facts the guide relies on are
  CV-30. Four of them shaped the harness:
  - A subagent's worktree branches from the remote's default branch unless
    `worktree.baseRef` is `head`, so the pack sets `head`.
  - A `domain:` fetch rule matches only the host it names, so the pack denies each
    board's subdomains too and adds a hook that refuses any board host or past-paper
    address.
  - The SubagentStop hook can be limited to named agents, so the stop gate covers the
    builders and not the reviewer.
  - A subagent's own definition can carry hooks, so the content author's shell is
    limited to its checks and git.

  Only stable features are used. Agent teams are experimental and are left out.
- **Hosting.** The MVP needs GPUs, so it runs on Modal with Postgres on Neon (CV-27).
  It does not run on the Netlify team that hosts this site, because spent credits
  pause every project in that team (CV-22).
- **What could not be opened.** Hugging Face, Modal, RunPod and gov.uk could not be
  reached from the build environment. Licence files and READMEs on GitHub, Google
  Cloud's pricing page and Claude Code's permissions and worktrees pages were read
  directly. The rest was read through search summaries, and each candidate row says
  which.

## 5. Checks run, and what each returned

| Check | Result |
|---|---|
| `python3 src/build.py` | Exit 0 |
| `python3 tools/verify.py` | All checks pass: build fresh, 4,426 links in 44 files with none broken, map loci resolve (100 nodes, 191 edges), no view or ownership problems |
| Existing markers | Every marker in every edited source matches `main`; the work only adds markers |
| Verified markers added | None |
| Dashes and American spellings in anything new | None |
| Page size | The guide is 2,730 words by the build's own counter, under the 3,000-word limit; the front page and the Tutor summary stay within their caps |
| Rendering | Every touched page fits at 390 px and 1280 px with no failed request |
| Hook scripts | Run under Python 3.9 and 3.13 against a scratch repository and in a worktree. The stop hook refuses five times while `make test` fails, then lets the session stop, and skips the reviewer. The edit hook reports lint failures. The guard refuses keys in files and commands, allows a local database address, and refuses any change to how the git hooks run. The fetch guard refuses board hosts at any subdomain and past-paper addresses, and allows documentation. The content author's shell runs its checks and git and nothing else |
| Merge gate | In a scratch repository, a merge that keeps `make test` passing is committed; one that breaks it is refused, and so is a conflicted merge finished with `git commit` |
| `settings.json` | Valid JSON: 94 permission rules, 5 hook events |

## 6. The independent review

A fresh agent was given the rules and the change but none of the conversation. It
read every source the work touched, ran the hooks in scratch repositories, and
checked Claude Code's behaviour against its documentation. It found 10 blocking
problems and 18 that were not blocking. It also confirmed:
- the build and checks pass;
- every existing marker is unchanged and in order;
- the new text has no dashes and no American spellings;
- the guide is under 3,000 words.

Every finding was checked against the files, and the Claude Code findings against its
documentation. All were fixed.

| # | Finding | What was done |
|---|---|---|
| 1 | Blocking. The stop hook and the phase gating worked against each other: builders' worktrees would fail each other's phase tests, the lead was refused mid-phase, and phase 0 ran no tests | `make test` now runs the unit tests and the tests of finished phases, and passes when nothing is collected; `make test-phase` is the lead's exit check. The stop hook covers the six builders by name and skips the reviewer. Phase 0's own tests are defined, every invariant test has a phase, and the five-refusal limit is stated wherever the gate is described |
| 2 | Blocking. Subagent worktrees branch from the remote's default branch, so builders would miss local merges | `settings.json` sets `worktree.baseRef` to `head`; the owner commits each change to `PHASE`; CV-30 records the behaviour |
| 3 | Blocking. The board deny rules matched only the bare domains, and the content author's shell could reach the network | Each board domain and five past-paper sites are denied with their subdomains; a fetch hook refuses any board host or past-paper address; the content author's own hook limits its shell to its checks and git; phase 0 proposes Claude Code's sandbox where the machine supports it |
| 4 | Blocking. Nothing enforced "nothing merges while a test fails" | A git hook runs `make test` on every merge, including a conflicted one finished with `git commit`; fast-forward merges are off; the guard refuses `--no-verify` and changes to the hook settings; CI runs on every push; the branch-protection claim is gone |
| 5 | Blocking. Phase 2 depended on later or parallel work | The mathematics, the content checks and the figure renderer move to phase 1, before any item is drafted; the T-VAL-01 census goes to the platform engineer in phase 1; the spike measures liveness on live and replayed attempts; section 17 says which tests gate a phase and which report |
| 6 | Blocking. Testers would be told their likeness stayed on "the MVP's own machines" | The welcome page, the consent screens and the guide now name Modal and Neon and what each holds; "by construction" is limited to speech and animation vendors |
| 7 | Blocking. Further Mathematics objectives would come from an agent's memory of AQA's specification, and a recalled exam question could reach a tester | Each objective is written from the DfE content it extends, named in its reference; the recall rule covers a specification's structure and wording; D85 and the guide call this weak; questions come only from permitted nodes, and any sentence holding mathematics must cite one |
| 8 | Blocking. T-GATE-01 was dropped | It is a phase 4 test and invariant 16, and the guide lists it |
| 9 | Blocking. EV-21 was paraphrased in a way that took a side on OI-1 | Now quoted in its two limbs: training AI tools, and any work produced with AI |
| 10 | Blocking. "The most capable model" was an unregistered claim | Removed; the reason given is that it is the model the Primer's demonstration uses (D78) |
| 11 | Two hooks crashed on Python 3.9 | Every hook runs under 3.9 and 3.13, tested |
| 12 | The likeness functions' secrets could not do what section 12 asked | They are internal functions; the web app checks challenges, writes `LikenessRef` and proxies the recording and the clips |
| 13 | Gaps in the team's workflow | Builders commit on their branch; a returned branch goes back to the same agent, resumed; SPEC.md says who changes what; reading lists are complete |
| 14 | The window disagreed | Every turn of the session, everywhere |
| 15 | The three moves disagreed | The guide now gives them to messages about the tester's own life, feelings or safety, as the specification does |
| 16 | Several departures were undeclared | Declared in the ledger, the brief and SPEC.md's table: D19, 06's bought renderers, check (a)'s model pass, check (b)'s model, D29, D26's written policy and the label's form under OI-26 |
| 17 | The grade range left out 05's safeguards | All of them are in SPEC.md 13 |
| 18 | Names disagreed | "Level 2 Further Mathematics" throughout, noting that the owner called it GCSE Further Maths; the brief's D84 names six builders |
| 19 | A parent tester could capture their own teenager | The tester confirms the face and voice are their own and that they are 18 or over; testers play their learners themselves; the checklist says so |
| 20 | A tester's likeness could reach Anthropic through an agent | Agents never read a tester's image, clip or recording; audio and video files are denied to the read tool |
| 21 | Secrets | The guard scans commands, allows a local database address, and a `.gitignore` and CI's secret scan are added |
| 22 | Test databases | Each run makes and drops its own database on a local Postgres; Neon is for the deployed MVP only |
| 23 | Retention | Neon's history and branches and Modal's logs are recorded and deleted at the end of the test period |
| 24 | Validation contradicted the labels | The workflow runs on a fixture bank; no MVP item changes status |
| 25 | Four invariants had no test, and the battery before a deploy was unenforced | Tests are added for invariants 5, 6, 12 and 15; `make deploy` checks the latest battery's configuration |
| 26 | T-STY-02 could show testers each other's sessions | Graders see battery transcripts only |
| 27 | Numbers missing from the specification's settings | Band edges, screen sizes, year groups and spend limits are listed; the unsourced claim about Claude's parameters is removed |
| 28 | Wording | 11's M2 says "counts towards none"; the guide names 05 and the composer's place, calls the prices candidates, adds CPU and memory to the GPU price, drops the allowance claim, says "some" pipelines and "anyone under 18"; the pick-up answer is a fixed choice; counsel's look at the tester notice is on the checklist |

## 7. What is left for the owner

- Keep or reverse D84 to D88, and the settings `SPEC.md` 3.4 lists as design
  choices.
- D86 uses Claude Opus 5.5, as the Primer's demonstration does. Anthropic also offers
  a more capable and dearer tier, Claude Fable 5.1. With cost last, you may prefer it.
  Switching is one setting and a battery run.
- Check candidates CV-24 to CV-30. The first phase checks the licences again, in
  `docs/licences.md`, before any model is used.
- Approve, when asked:
  - the Further Mathematics objectives;
  - the fictional preset;
  - the look;
  - the sandbox block, if phase 0 proposes one;
  - the paper specifications;
  - the grade range's mapping;
  - the reviewer policy.
- Write down each threshold the pack leaves to you, before the phase that needs it:
  - the liveness and false-accept thresholds, before phase 3;
  - the style scales and T-STY-01's band, before the first battery;
  - T-STY-02's sample size, before phase 5.
- Read the reviewer queue at least once a day while testers use the MVP, and never
  let anyone under 18 use it.
