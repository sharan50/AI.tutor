# Tutor MVP: the build specification

Save this file as `SPEC.md` at the root of the MVP's own repository, beside the
`CLAUDE.md` from the same pack. It is published with the Tutor's MVP build guide,
<https://aitutor-plan.netlify.app/docs/tutor-mvp.html>, which gives the reasons; this
file says what to build. The design it builds is the vault's, pages 01, 02, 03, 05
and 06, at <https://aitutor-plan.netlify.app/docs/>.

Where this file and the guide disagree, the guide governs. Where this file and the
vault's design disagree, the design governs, except at the departures in section 2.
Either disagreement is a bug to report to the owner, not one to settle yourself.

Written 26 October 2026. Nothing here has been built yet. Every number in this file
is a decision of the vault, named where it is used; a design choice of this pack,
listed in section 3.4; or Unknown.

## 1. What you are building

The Tutor, as the vault describes it, for adults who play learners of 14 to 18. A
tester accepts an invitation, sets up a learner, and:

1. picks up where they left off, picks one objective, and is taught it in a chosen
   style;
2. sits an unaided check of three held-out items and is told honestly what it
   showed;
3. sees each tutor turn only after the verifier has passed it, and the item verbatim
   when it has not;
4. sees figures rendered from data, sits practice papers and sees a provisional grade
   range;
5. chooses a style preset, moves its axes, and sees the label change;
6. may turn on the self-tutor: two consents, a live capture with a liveness check, a
   passcode, then the tutor's turns spoken and animated in their own likeness after
   the gate;
7. as the adult on the account, sees the parent report, which shows no transcript by
   default and never shows the likeness.

Around it: a safety check on every message, with the three moves of 05 and a
reviewer's queue; a validator console; a frozen battery; and an owner's console with
the kill switch.

Three things are not real, and every screen that touches them says so: no examiner
has validated any item; no child uses it; no creator has signed, so one fictional
licensed preset shows the machinery.

The owner's priorities are speed of building and fidelity to the design first, and
running cost and latency last. When you must choose, choose the design.

## 2. Where the MVP departs from the product

Everything not in this table is built as the vault describes it. Nothing here
changes the Tutor's design.

| The product | The MVP | Decision |
|---|---|---|
| Learners of 14 to 18 | Adults who play them; no child, and no child's data | D81 |
| Every live item validated by a named examiner (P1, 03) | Items drafted by agents, checked by SymPy, served at status `draft` and labelled "Not yet validated by an examiner" | D82 |
| The algebra of GCSE Higher, aligned to Pearson Edexcel (D19) | The algebra of GCSE Mathematics, both tiers, Level 2 Further Mathematics and A-level Mathematics, aligned to no board; papers of the MVP's own structure | D82, D85 |
| Speech and animation bought from a vendor under D24 (06) | Open models run by the MVP on GPUs rented from Modal; no speech or animation vendor receives a likeness | D83 |
| Check (a) a deterministic parse (06) | The parse, and a model pass over the sentences the generator did not mark as assertions, because the generator labels its own sentences | D86 |
| Check (b) on a pinned, cheaper model (06) | Gemini 4 Argon, because cost comes last and D27 needs another family | D86 |
| Model vendors under zero retention (D24) | Claude Opus 5.5 and Gemini 4 Argon on their standard terms | D86 |
| Transcripts kept twelve months (05) | Kept for the test period, then deleted with everything else about testers | D87 |
| Age assurance from a certified provider (05) | A simulated check, which says it is simulated | D88 |
| Named educators under licence (D5) | One fictional licensed preset; the rating protocol is not built | D88 |
| The kill switch rehearsed quarterly (D29) | Rehearsed once, in phase 4, and again before testers if the preset changes | D88 |
| Payment, Route B's school features, the US course | Not built | D88 |
| A rolling summary of bounded size as the window (D30) | The current session's turns, verbatim: a whole session fits, and D30 exists to bound cost | D88 |
| A trained reviewer, against a written policy (D26) | The owner works the reviewer queue, against `docs/reviewer-policy.md` | D81 |
| Validation by named examiners (03) | The validation workflow runs on a fixture bank only; no MVP item changes status | D82 |
| The synthetic label's form, which waits on OI-26 (01) | The MVP's own label, which answers nothing about OI-26 | D83 |

Where a vault test asks for a live item, the MVP accepts a draft one that SymPy has
checked, because none is validated.

## 3. Stack, accounts and settings

### 3.1 Stack

- **Language:** Python 3.12, in one package, `tutor`, managed with uv.
- **Web:** FastAPI, with pages rendered on the server by Jinja2, and plain JavaScript
  modules for waiting, capture and playback. No front-end framework and no build step.
- **Database:** Postgres on Neon, through SQLAlchemy 2, with Alembic migrations.
- **Hosting:** Modal, for the web app, the workers, the GPU renderers, the likeness
  volume and the scheduled jobs. The MVP does not use Netlify or the vault's site.
- **Text models:** the Anthropic Python SDK, `anthropic`, for Claude Opus 5.5; the
  Google Gen AI Python SDK, `google-genai`, for Gemini 4 Argon.
- **Mathematics:** SymPy. **Papers:** OR-Tools' CP-SAT solver.
- **Likeness:** Chatterbox for the voice, MuseTalk for the face, and MediaPipe's Face
  Landmarker (in the browser and in Python), Silent-Face-Anti-Spoofing and Whisper for
  liveness, all run by the MVP. Each is admitted only by the licence audit (12.6).
- **Tests:** pytest, and Playwright for the browser. **Lint and format:** ruff.
  **Types:** mypy on `tutor/contracts/` and `tutor/pipeline/`.

Before writing the integration for any model, SDK or platform feature, read its
current documentation. They change at short notice, and nothing in this file
overrides the documentation on how to call them.

### 3.2 The owner's accounts

| Account | For | Set before phase 2 |
|---|---|---|
| Anthropic | Claude Opus 5.5 | a monthly spend limit of $500 |
| Google AI Studio | Gemini 4 Argon | a monthly spend limit of $300 |
| Modal | everything that runs | nothing; scale-down is set in code |
| Neon | Postgres | nothing; the cost is Unknown |
| GitHub | the private repository | CI on every push and pull request, with a secret scan |

### 3.3 Secrets and configuration

Secrets are Modal secrets, each attached only to the functions named. None is in the
repository, in an environment file that is committed, or in the browser. The
`capture`, `voice`, `face` and `purge` functions are internal Modal functions, never
web endpoints: the web app authenticates every request and calls them.

| Variable | Modal secret | Attached to | For |
|---|---|---|---|
| `ANTHROPIC_API_KEY` | `anthropic` | `web`, `battery` | Claude |
| `GEMINI_API_KEY` | `gemini` | `web`, `battery` | Gemini |
| `DATABASE_URL` | `neon` | `web`, `jobs`, `battery` | Postgres |
| `SESSION_SECRET` | `app` | `web` | signing cookies and one-time URLs |
| `LIKENESS_KEY` | `likeness` | `capture`, `voice`, `face`, `purge` | encrypting the likeness store |

Everything else is in `tutor/config.py`, in one place: `CLAUDE_MODEL =
"claude-opus-5-5"`, `GEMINI_MODEL = "gemini-4-argon"` and the settings in 3.4. A change
to a model, a prompt, the card renderer or the composer's rules for choosing sources
must pass T-REG-01 before it is deployed (D22).

### 3.4 Settings chosen for the MVP

These are this pack's design choices, each the owner's to change. None is a fact
about learners.

| Setting | Value |
|---|---|
| Tutor turns a tester a day | 50 |
| Session length | teaching ends by 20 minutes; the session ends at 30, within 01's fifteen to thirty |
| The unaided check | three check items (01 says two or three); a pass needs all three right on first commit |
| Return after the close | 7 days after a pass, 2 days after a fail |
| The window | every turn of the current session |
| Permitted nodes | the objective's own, and at most 3 explanation nodes of its prerequisites |
| GPU scale-down | after 300 seconds idle |
| GPU containers | at most 2 for each renderer |
| Capture challenge | valid for 120 seconds: 3 head movements and 6 sentences, chosen afresh |
| Self-tutor passcode | at least 6 digits; 5 wrong tries lock it for 15 minutes |
| Face wait | if a sentence's face clip is not ready 2 seconds after its audio, the still likeness speaks it |
| Adjustment positions | five, mapped to 10, 30, 50, 70 and 90 |
| Card bands | five: 0 to 19, 20 to 39, 40 to 59, 60 to 79 and 80 to 100 |
| Clamps | `worked_completeness` at least 40; `digression_tolerance` at most 50; `visual_density` at most 80; must-warn misconceptions always named |
| Papers | no item the learner has seen in the last 14 days |
| Learners | year groups 10 to 13 |
| Screens | every layout works at 390 px wide and at desktop width; touch targets at least 44 px; text at least 18 px on a phone |
| Spend limits | $500 a month at Anthropic and $300 at Google, set at the providers |
| The battery | 12 objectives, 4 for each qualification, under every shipped preset |
| The reviewer queue | read by the owner at least once a day during the test period |
| The kill switch's cache | 60 seconds, from 06 |
| Deletion | purged at once and swept daily; the promise is seven days (D63) |
| The test period | set by the owner before phase 5; Unknown today |

## 4. The repository

```
CLAUDE.md               the invariants and how to work, from the pack
SPEC.md                 this file
PHASE                   the phase being built, a single digit; only the owner changes it
Makefile                test, test-phase, test-all, lint, check-content, battery, deploy
.gitignore              .env*, .claude/worktrees/, .venv/, caches, and audio and video files
.claude/agents/         the team, from the pack
.claude/settings.json   hooks and permissions, from the pack
.claude/hooks/          the scripts the hooks run, from the pack
.githooks/              the merge gate, from the pack
.github/workflows/      the fast tests and a secret scan, on every push and pull request
spikes/                 phase 1's spike, kept apart from the product
content/
  sources/dfe/          the DfE subject content, as the owner downloaded it
  objectives/           one file per qualification
  items/                one file per objective
  presets/              the three style objects
  papers/               the papers' structural specifications
tutor/
  config.py             models and settings, in one place
  contracts/            the typed schemas every plane shares
  content/              the bank, its loader and the checks on items
  maths/                the syntax, the step checks, MathML and the spoken form
  pipeline/             safety check, composer, generator, verifier, gate, logger
  figures/              figure specifications and the SVG renderer
  style/                presets, card renderer, adjustments, signatures, kill switch
  likeness/             consents, capture, liveness, store, voice, face, labels, deletion
  platform/             accounts, roles, sessions, scheduler, papers, grade range, reports
  web/                  routes, templates and static files; static/capture/ holds the capture code
  modal_app.py          the deployment
migrations/             Alembic's migrations
tests/
  invariants/           one file per vault test and per invariant
  unit/                 each plane's own tests
  battery/              the frozen battery and its simulated learner
  thresholds.toml       every threshold, written before the run it judges
  fixtures/
docs/
  licences.md           the licence audit
  retention.md          where each kind of data lives, and how it is deleted
  reviewer-policy.md    what the reviewer does with an escalation
reports/                one report per battery run
```

Who changes what:

| Path | Changed by |
|---|---|
| `PHASE`, `tests/thresholds.toml`, `.claude/`, `.githooks/` | the owner |
| `tutor/contracts/`, `tutor/config.py`, `tests/invariants/`, `docs/reviewer-policy.md` | a lead session, with the reviewer and the owner's approval |
| `content/` except presets and sources | the content author |
| `tutor/pipeline/`, `tutor/maths/`, `tutor/figures/`, `tutor/content/`, `tests/battery/` | the pipeline engineer |
| `tutor/style/`, `content/presets/` | the style engineer |
| `tutor/likeness/`, `tutor/web/static/capture/`, `spikes/`, `docs/licences.md` | the likeness engineer |
| `tutor/web/` except the capture code | the app engineer |
| `tutor/platform/`, `tutor/modal_app.py`, `migrations/`, `.github/workflows/`, `docs/retention.md` | the platform engineer |

Each builder also owns its own folder under `tests/unit/`. The likeness functions are
defined in `tutor/likeness/` and registered in `tutor/modal_app.py`.

### 4.1 The contracts

`tutor/contracts/` holds Pydantic models and nothing else. Every plane imports them,
and no plane defines its own version of one. They change only in a lead session, with
the reviewer, and with every affected test changed in the same commit.

| Contract | Holds | Made by | Read by |
|---|---|---|---|
| `Objective` | the fields of 06, plus `qualification`, `title` and `order` | content | composer, scheduler, scope check |
| `Item`, `Provenance` | the fields of 03 and 06, plus `answer`, `machine_question` and `known_wrong_answers` | content | composer, fallback, papers, check |
| `FigureSpec` | `type`, `version`, `data`, `alt`, `item_id` | content | figure renderer |
| `StyleObject` | `cine.style/1`, exactly as 02 | style | card renderer |
| `StyleCard` | `preset_id`, `renderer_version`, `text`, `adjusted` | card renderer | generator only |
| `TurnPlan` | `session_id`, `objective_id`, `permitted_nodes`, `card`, `window`, `must_warn` | composer | generator, verifier |
| `GeneratedTurn` | `sentences`, `steps`, `figure_ref`, `ready_for_check` | generator | verifier |
| `Verdict` | `a`, `b`, `c` and `d`, each a pass or a fail with its reasons | verifier | gate, logger |
| `GatedTurn` | `turn_id`, the text, its mathematics, its figures, `fallback`, the labels | gate | web, voice |
| `SafetyVerdict` | `category` and `reason` | safety check | session |
| `ClipRequest` | `turn_id`, `sentence_index`, `script`, `script_hash` | web | voice, face |
| `LivenessResult` | `passed`, each check's result and score | liveness | capture |

## 5. Data model

The vault's schema, from 06, unchanged:

```
Objective        id, strand, dfe_content_ref, tier, prerequisites[], must_warn[]
Item             id, objective_id, kind, body, worked_solution, figure_spec?,
                 provenance{...}, status
ValidationRecord item_id, validator_id, date, result, notes, revalidate_after

Preset           id, kind(archetype|licensed), display_name, fallback_archetype_id,
                 enabled                            // the kill switch
StyleObject      preset_id, dimensions{12}, register_note, exemplars(null),
                 renderer_version, provenance{...}
CreatorLicence   id, preset_id, term_start, term_end, schedules[], status

Learner          id, account_id, year_group, preset_id, adjustments{}
MasteryState     learner_id, objective_id, attempts, unaided_pass, last_seen, due
GradeRange       learner_id, band_low, band_high, computed_at, n_items,
                 spec_coverage, sufficient(bool), calibrated(bool=false)
Paper            id, spec_id, item_ids[], mark_total, assembled_at, checks{}
Session          id, learner_id, objective_id, preset_snapshot, started, ended
Turn             id, session_id, role, text, citations[], verdicts{a,b,c,d},
                 gate_result, style_signatures{12}
Escalation       session_id, category, raised_at, reviewed_by, reviewed_at, action

Account          id, verification{bool, method, provider_ref, timestamp}, billing

SelfTutor        learner_id, status(off|active|deleting), passcode_hash, created_at,
                 last_session_at, delete_requested_at
Consent          id, account_id, learner_id, party(adult|learner),
                 notice_version, given_at, withdrawn_at
LikenessRef      learner_id, kind(face|voice|conditioning), store_ref
```

The MVP adds these, and adds `nickname`, `qualification` and `tier` to `Learner`,
`learner_view(can|cannot|null)` to `MasteryState`, and `cohort` to `Account`:

```
User             id, account_id, email, password_hash, roles[], created_at
Invitation       id, token_hash, roles[], created_by, expires_at, used_at
CaptureChallenge id, learner_id, head_moves[], sentences[], issued_at, used_at
AccessLog        id, user_id, target, reason(escalation|adjudication|support), at
Adjudication     id, turn_id, test, drawn_as(failure|sample), result,
                 adjudicator_id, at
BatteryRun       id, started_at, config_hash, results{}, report_path
Counter          day, kind, value        // turns, GPU seconds; never content
```

- No field anywhere holds a date of birth, an age, a school, an address or a
  photograph. A test fails if one appears.
- No learner, user or turn record holds a likeness, audio or video. `LikenessRef` is
  the only pointer, and only the likeness functions can follow it.
- `Account.billing` stays empty: there is no payment (D88).
- Every account's `verification` is `{true, "simulated", null, <time>}`.
- Provenance is written once. The loader refuses to change the provenance of an item
  already in the bank; a changed item gets a new id, and the old one is withdrawn.
- `Account.cohort` holds D33's flags, so the experiment's machinery exists: whether
  named presets are offered, and, separately, whether the self-tutor is (D68). The
  owner sets them; by default both are on.

## 6. Content

### 6.1 The clean room

No board's material reaches any agent: no specification, past paper, examiners'
report or mark scheme, whether from a board or from a site that copies one (D12,
EV-21). The only source documents are the DfE subject content for GCSE Mathematics
and for A-level Mathematics, which the owner downloads from gov.uk into
`content/sources/dfe/` before phase 1. The content author has no web access, and
writes everything else from its own knowledge of mathematics. An agent that notices
it is recalling a board's question, or a board's specification, its topic list, its
order or its wording, stops and writes something of its own. No tester's material
reaches an agent either: what a tester found is described in words.

### 6.2 Objectives

Three qualifications (D82, D85):

- `gcse-maths`: the algebra of the DfE subject content for GCSE Mathematics, both
  tiers. Each objective records its tier.
- `a-level-maths`: the algebra and functions of the DfE subject content for A-level
  Mathematics.
- `l2-further-maths`: the algebra of Level 2 Further Mathematics, the qualification
  the owner called GCSE Further Maths, written from no board's material. No DfE
  subject content for it was found, and the qualification found, AQA's certificate,
  comes from the board whose policy EV-21 records. Each objective is written from the
  DfE GCSE or A-level content it extends, which its `dfe_content_ref` names, so that
  the list rests on statutory content and not on the one course found. The owner
  approves the list, checking that each objective names its reference, before any
  item is drafted. This is weak: an agent's sense of what such a course covers may
  still echo that course.

An objective is one item-bank node, taught in one session (01). It has an id of the
form `OBJ-GCSE-QUAD-03`, a title in plain words, its qualification and tier,
`dfe_content_ref`, its prerequisites, its must-warn misconception nodes, and its
place in the qualification's order. How many
objectives there are is Unknown until the decomposition.

### 6.3 Items

Ten for each objective, as 03 plans: one explanation node, three misconception nodes,
three practice items and three check items. Each item has:

- a body that stands alone, because the fallback serves it verbatim;
- a worked solution, as steps in the syntax of section 7;
- for a misconception node: the wrong answer, why it tempts, and what shows it wrong;
- for practice and check items: marks, a command word (Solve, Simplify, Factorise,
  Expand, Find, Show that, Sketch, Write down, Work out), a difficulty, the answer, and
  known wrong answers, each linked to a misconception node;
- where it can, a `machine_question`, such as `{"task": "solve", "input": "2x + 3 =
  11"}`, from which SymPy can re-derive the answer;
- a figure specification, where a figure carries the idea better than words (section
  10);
- its provenance record.

Every check item's answer is one the CAS can mark: a number, an expression, an
equation, an inequality, a set of values or a point. "Show that" and proof items are
practice or explanation items only. **Check items never enter a turn plan.**

### 6.4 Provenance in the MVP

The record of 03, with these values: `written_by` is `agent:content-author` and the
session's id; `derived_from` is the objective's DfE content reference;
`structure_basis` is `authored`; `board_alignment` is `none`; `tier` is the
objective's; `attestation` is `no awarding-body material consulted`;
`similarity_check` is all null, because no screening service is procured;
`validated_by`, `validation_date` and `validation_result` are null; and `status` is
`draft`.

### 6.5 Checking items

`uv run python -m tutor.content.check` runs on every item file. The pipeline engineer
builds it in phase 1, before any item is drafted; the after-edit hook runs it on each
item file, and `make test` runs it on the whole bank, so the merge gate refuses a bank
that fails it:

- the file validates against the contracts;
- every worked step passes the step check of section 7;
- every answer agrees with SymPy's own result from `machine_question`, where there is
  one;
- every known wrong answer differs from the answer;
- no two items share a body;
- every linked misconception and every must-warn id exists;
- every figure specification renders.

An item the checks reject is rewritten or dropped. Then a fresh session of the content
author, given only the items and not the conversation that drafted them, reads each
objective's ten for level, clarity and whether the misconceptions are real ones, and
lists problems for a rewrite. Record the share of steps the CAS could not decide; it
is a measurement, never a reason to skip a check. If a mathematics teacher can read a
random sample before phase 5, record what they find in `reports/`, against OA-46.

### 6.6 Labels

Every item, worked solution, paper and mark scheme says "Not yet validated by an
examiner" wherever a tester sees it.

## 7. Mathematics

### 7.1 One syntax

All mathematics an agent or a model writes is in one machine syntax, parsed by
SymPy's `parse_expr` with implicit multiplication and the caret as a power:
`2x^2 - 3x + 1`, `(x + 2)(x - 3)`, `sqrt(x)`, `x/(x + 1)`, `log(x, 2)`, `e^x`.
Equations use `=`; inequalities use `<`, `<=`, `>` and `>=`; a set of values is
`{1, 2}`; an interval is `x > 3` or `-1 <= x < 4`; a point is `(2, -1)`. In text, an
expression is written inline as `[[2x + 3 = 11]]`. A token that does not parse fails
check (d).

### 7.2 Steps

A worked step is `{from, to, relation, cites, after}`, where `after` is the sentence
it follows, and `relation` is one of:

| Relation | Checked by |
|---|---|
| `equivalent` | `simplify(from - to) == 0`, or SymPy's `equals` |
| `equivalent_equation` | the solution sets over the reals agree |
| `implies` | every solution of `from` satisfies `to` |
| `solves` | `to` is the solution set of `from` |
| `evaluates` | exact agreement for rationals; otherwise agreement to a stated tolerance |

A step the CAS cannot decide within a time limit is marked `unchecked`. It does not
fail check (d); it is logged and sampled for the owner's adjudication under T-MTH-01.
A step the CAS decides against always fails check (d), and nothing overrides it (06).

### 7.3 Rendering and speaking

Every expression on screen is rendered from its parsed form, as MathML from SymPy's
presentation printer, never from free text. Worked steps show as lines of
mathematics. One deterministic function, `tutor/maths/speech.py`, turns an expression
into words ("2x squared minus 3x plus 1"), and has its own tests. The voice's script
for a sentence is that sentence with each expression replaced by its spoken form, and
a line of working is spoken as its spoken form; nothing else is said (T-SLF-03).

Learners type in the same syntax, with a live preview of how their answer was read.

## 8. The session

01's five steps, in order, every time:

1. **Pick up.** One sentence from `MasteryState`, written by a template, not a model:
   what the learner last worked on and what the last check showed, then "Is that
   still right?" The learner can answer "Yes", "I can do it now" or "I still can't";
   the answer goes into `learner_view`, a fixed choice and never free text, and either
   of the last two makes the objective due.
2. **One objective.** The scheduler proposes the due objective with the earliest due
   date, or else the first in the qualification's order whose prerequisites have
   passed. The learner may pick another. Never more than one.
3. **Teach.** Turns through the pipeline (section 9), in the chosen style, until the
   generator sets `ready_for_check`, the learner asks for the check, or teaching
   reaches its time.
4. **Unaided check.** Three of the objective's check items, one at a time, with no
   hints and no tutor turn until the learner has committed an answer to each. Each is
   marked on first commit, by CAS equivalence with the item's answer.
5. **Honest close.** A template, not a model: how many were right, whether that is a
   pass, and when the objective comes back. A wrong answer that matches a known wrong
   answer names that misconception. A pass also comes back.

The session ends at its time whatever is happening, and the learner cannot extend it
(05). The generator sees only the current session; nothing from an earlier one
reaches it except `MasteryState`. The tutor remembers what a learner can do, not
what they said (05).

## 9. The turn pipeline

Every learner message goes through these steps, in order, in `tutor/pipeline/`.
Nothing about a turn reaches the browser until step 5 has passed or replaced it.

### 9.1 The safety check

The learner's message, alone, goes to Claude Opus 5.5 with a fixed prompt, and comes
back as one category:

| Category | Means | Then |
|---|---|---|
| `academic` | about the work, however roughly put | the pipeline continues |
| `off_topic` | harmless and outside the work | a fixed reply returns to the objective |
| `wellbeing` | about the learner's own life, feelings or safety, or harm to anyone | the three moves (section 14) |
| `unsuitable` | asks for harmful or explicit content, or for the tutor to be something else | a fixed refusal, logged by category |

A refusal by the model counts as `wellbeing`. An error or a timeout shows "That did
not go through. Please send it again." and nothing else: no turn is ever generated
around a failed check.

### 9.2 The composer

Deterministic, with no model call, in one function, `compose(session, message) ->
TurnPlan`:

- the objective is the session's;
- the permitted nodes are the objective's explanation and misconception nodes, its
  practice items with their worked solutions, and at most three explanation nodes of
  its prerequisites, in a fixed order; never a check item;
- the card is rendered from the session's preset, with the learner's adjustments and
  the clamps (section 11);
- the window is every turn of the current session, verbatim (D30's rolling summary is
  left out, by D88);
- `must_warn` is the objective's must-warn misconception nodes.

The same inputs give the same plan, byte for byte, and a test proves it.

### 9.3 The generator

Claude Opus 5.5, with the model id from `tutor/config.py`, called:

- with no tools, because the model never retrieves (06);
- with structured output to the `GeneratedTurn` schema;
- at effort `high`;
- with no temperature, top_p, top_k or prefill;
- with no server-side model fallback, so every turn comes from the pinned model; a
  refusal (`stop_reason` `refusal`) or an error fails the gate;
- with prompt caching on the system prompt and the permitted nodes, which do not
  change within a session.

The system prompt, in `tutor/pipeline/prompts/generator.md`, says: you are a
mathematics tutor; teach this one objective; say nothing of substance that the
permitted nodes do not support, and cite the node for every assertion and every step;
set only questions taken from a permitted node, as written or with its numbers
changed, and never write a new exam-style question; write all mathematics in the
syntax; follow the card; claim no feelings, preferences or life outside the session;
do not invite personal disclosure; never mention the learner's face or voice; write
in British English without dashes. The card, the nodes and the window follow it, in
that order.

```json
{
  "sentences": [
    {"text": "Start with [[2x + 3 = 11]].", "role": "instruction",
     "cites": ["IB-GCSE-LIN-001"]}
  ],
  "steps": [
    {"from": "2x + 3 = 11", "to": "2x = 8", "relation": "equivalent_equation",
     "cites": ["IB-GCSE-LIN-001"], "after": 0}
  ],
  "figure_ref": null,
  "ready_for_check": false
}
```

A sentence's `role` is one of `assertion`, `question`, `instruction`, `feedback` and
`check_in`. A figure is chosen, never made: `figure_ref` names a figure specification
on a permitted node, or is null (D28).

### 9.4 The verifier

Four checks, all blocking (06), in `tutor/pipeline/verifier.py`. Checks (b) and (c)
use Gemini 4 Argon, a different family from the generator (D27); check (d) uses no
model.

| Check | In the MVP | Fails when |
|---|---|---|
| a. Citation presence | In code, every assertion, every step and every sentence that holds mathematics, whatever its role, cites at least one permitted node. Then Gemini reads each other sentence, with the one before it, and says whether it makes a curricular assertion | any of those has no permitted citation, or Gemini finds an assertion under another role |
| b. Claim support | Gemini, once for each assertion, given only that sentence and the text of the nodes it cites, says whether they entail it | any assertion is not entailed; each failure goes to the adjudication queue |
| c. Scope | Gemini, given the turn and the titles of the qualification's objectives, says whether everything in it lies inside them | anything lies outside |
| d. Mathematics | SymPy on every step and every inline expression (section 7) | a step is wrong, or an expression does not parse |

Each Gemini call uses structured output and a fixed prompt in
`tutor/pipeline/prompts/`, and is given nothing from the card or the conversation:
style never reaches the content plane (06). An error or a timeout in any check fails
that check.

### 9.5 The gate and the fallback

A turn passes when all four checks pass. Otherwise the learner sees 01's blocked
turn, built with no model call:

> I am not going to answer that one, because I could not check it against anything I
> trust. I have flagged it. Here is what I can give you now: the worked solution for
> the closest thing I do have. No examiner has checked it yet.

followed, verbatim, by the permitted node with the most words in common with the
learner's message (ties go to the objective's explanation node), with its id and its
label. The failed turn is logged and never shown.

### 9.6 The logger

One `Turn` row for each tutor turn: the text, the citations, the four verdicts, the
gate's result, the fallback item if one was used, each step's time, the tokens and
model ids, and the style signatures (11.6). Never write a turn's text, a learner's
message or a node to a log or to the console.

### 9.7 While the learner waits

Nothing is shown before the gate, so the wait is shown honestly: "Writing", then
"Checking the sources", then "Checking the maths", then the turn. Do not stream the
generator's tokens to the screen; that would show text the gate has not passed.

## 10. Figures

Rendered, never generated (D28): an SVG built by a template from a `FigureSpec`
stored on an item, in `tutor/figures/`. The algebra needs these types:

| Type | Draws |
|---|---|
| `number_line` | points, open and closed ends, shaded intervals |
| `axes_plot` | axes and grid, functions over a range, marked points, asymptotes |
| `line_graph` | a straight line with its gradient and intercept marked |
| `region` | lines in two variables and a shaded region |
| `area_model` | a rectangle split to show expanding or factorising |
| `function_machine` | a chain of operations, and its inverse |
| `table` | a table of values, or a sequence and its differences |

Each SVG carries its item's id in its `<metadata>`, scales to the screen's width,
has a text alternative from its specification, and never carries meaning by colour
alone. Each type is tested against a fixed SVG. `visual_density` governs how often
the generator chooses one.

## 11. The style engine

### 11.1 Presets

Three style objects, in `content/presets/`:

- `arch.groundwork` and `arch.spine`: the two vectors in 02, copied exactly, register
  notes included.
- `lic.fictional`: one licensed preset for a fictional educator, with `kind`
  `licensed`, the display name "A. Example (fictional)", a `creator_ref` to a fictional
  `CreatorLicence`, and `provenance.source` `fictional`. Its twelve values are the
  owner's choice, distinct from both archetypes, made in phase 1. It is not opted in
  to the self-tutor by default (D66).

The rating protocol of 02 is not built: there is no creator to rate (D88).

### 11.2 The card renderer, `cine.card/1.0.0`

`render(style_object, "cine.card/1.0.0") -> str`: deterministic, versioned, and the
only way a card comes into existence (02). Each dimension falls in one of five bands,
0 to 19, 20 to 39, 40 to 59, 60 to 79 and 80 to 100 (3.4), and each band gives one
instruction. The card opens "Teaching style for this session.", gives the lines in
the order of 02's card, then the `constraints` verbatim, then "Register: " and the
register note.

02's card for `arch.groundwork` is the specification of every band Groundwork
reaches. A golden test renders `arch.groundwork` and requires every line of that
card, in order and word for word; the renderer may add one line, for
`digression_tolerance`, which 02's card leaves out. The style engineer writes the
other bands in the same voice, and the owner reads the Spine and fictional cards
before phase 2. A card holds no creator's name, quotation or phrasing attributable to
anyone (02). The model never sees the style object, only the card.

### 11.3 Adjustments

Six controls in plain words, each with five positions and the preset's own position
marked, kept for each learner and qualification between sessions, with one tap back
to the preset (D10):

| Control | Moves |
|---|---|
| "Tell me the rule first, or let me work it out" | `entry_point`, `formalism_latency` |
| "Correct me, or make me spot it" | `error_response` |
| "One example all the way through, or a new one each time" | `example_policy` |
| "Explain it to me, or ask me questions" | `question_density`, and `talk_ratio` the other way |
| "Words first, or symbols from the start" | `notation_discipline`, `abstraction_pace` |
| "Show me every step, or leave some to me" | `worked_completeness` |

The first two are 02's; the other four are this pack's design choice. The clamps in
3.4 then apply, and the learner cannot cross one. Once any axis has moved, the label
reads "Style preset: [Name], adjusted by you." An adjusted style is visible only to
its learner and cannot be named, published, shared or sent (02, and T2 in 05).

### 11.4 The kill switch

`Preset.enabled` is the whole switch (06): one boolean, read on every turn through
one cache with a sixty-second lifetime, set in one place and asserted by a test. From
the first turn that reads it as false, a session uses `fallback_archetype_id`. The
owner's console sets it in one write. A rehearsal script disables the fictional
preset while a session runs, and records how long a new session and the running one
took to lose it. D29 rehearses the product's switch quarterly; the MVP rehearses once,
in phase 4, and again before testers if the preset changes.

When the fictional licence ends, the preset, its style object, every card and every
`Session.preset_snapshot` that refers to it are purged within seven days, and the
transcripts keep only the neutral identifier (06).

### 11.5 The creator's controls

For the fictional preset, the owner's console offers 02's three ways of acting on an
objection: move a dimension, add a constraint (emitted verbatim into the card), and
withdraw (the kill switch). Each is one change to one record. It also holds the
self-tutor opt-in (D66): while it is off, the preset is not offered in the
self-tutor's chooser, and a self-tutor session using it falls back at its next turn.

### 11.6 Signatures

At logging time, each turn's raw counts for 02's twelve signatures go into
`Turn.style_signatures`, and each session's values are computed when it ends. What
can be counted is counted in code: questions per tutor turn, tutor and learner tokens,
figures per thousand words, symbols per hundred words, steps shown against the steps
in the item's worked solution, and misconception nodes cited before the learner's
first attempt. The rest need each sentence tagged: an instance or a general
statement, on the critical path or not, an invitation to test an answer or a
correction, and which example context. Gemini tags them, from a fixed rubric; the
generator never tags its own turns. The scale from each raw value to 0 to 100, and
T-STY-01's tolerance band, are written in `tests/thresholds.toml` before the first
battery run, and never changed after a run to make it pass.

## 12. The self-tutor

Off until both consents are given. It changes how a turn is presented, never what it
says (01, D64).

### 12.1 Turning it on

1. **Two consents.** The adult's, then the learner's, on separate screens, each after
   01's plain statement: what is kept (a face scan, a voice sample and what is derived
   from them), where it is kept (encrypted, on Modal, which hosts the MVP; no speech
   or animation company receives it), that the product shows it to no one else, the
   adult included, and how to delete it. The learner's words are written for a
   fifteen-year-old, not adapted from the adult's. Each makes a `Consent` row with its
   notice version (D62). In the MVP one tester gives both, and the screens say so.
2. **Live capture.** The tester first confirms that the face and the voice will be
   their own and that they are 18 or over; a self-tutor of anyone else, a child above
   all, is never made. The browser asks for the camera and the microphone, and the
   web app issues a `CaptureChallenge`. The browser records a head-and-shoulders clip
   while the learner follows the head movements, then the learner reads the sentences
   aloud, and sends the recording to the web app with the challenge's id. The web app
   accepts it only within the challenge's lifetime and only once, marks the challenge
   used, and passes the recording, held in memory and written nowhere, to the capture
   function. There is no file input anywhere in the app (D61).
3. **Liveness.** MediaPipe's face landmarker guides the movements and blinks in the
   browser and checks them again on the server; Silent-Face-Anti-Spoofing scores the
   frames on the server; Whisper transcribes the audio, which must match the
   sentences. All three must pass, against thresholds the owner writes in
   `tests/thresholds.toml` before phase 3. A failure says so and offers another try;
   nothing from it is kept.
4. **A passcode.** The learner sets one, kept as a hash in `SelfTutor.passcode_hash`.
   Without it the self-tutor does not play, so the account holder cannot open it
   (D60).
5. **A sample, then a choice.** The self-tutor says one fixed sentence. The learner
   keeps it or discards it, and discarding deletes it.

### 12.2 The likeness store

A Modal volume, `likeness`, holding the face clip, the voice sample and anything
derived from them, each file encrypted with `LIKENESS_KEY`. Only the `capture`,
`voice`, `face` and `purge` functions have the key or the volume; the web app has
neither. The capture function returns opaque references, which the web app writes
into `LikenessRef`; the rows hold nothing else. Every read or write of the
store is logged with the function, the learner's id and the reason. Nothing is
trained on a likeness: conditioning happens at render time and is dropped when the
render ends (D65).

### 12.3 Rendering

After the gate, never before (D64). For each sentence of a passed turn:

1. the web app builds the script from the stored turn (7.3), never from anything the
   browser sent, and sends the `voice` function a `ClipRequest` with the script's
   hash;
2. Chatterbox speaks the script in the learner's voice, at one neutral delivery: no
   preset, dimension or register note reaches the voice (D69);
3. MuseTalk animates the captured clip to that audio;
4. the label "AI-generated in your likeness" is drawn into the frames, and provenance
   metadata, saying the clip is synthetic and giving the turn's id, the time, and the
   models and their versions, is written into the file (T-SLF-06);
5. the web app streams the clip to the browser, behind the learner's session and
   passcode, and stores it nowhere: responses carry `Cache-Control: no-store`, and the
   player offers no download, share or export.

The first sentence plays while the rest render. If a sentence's face clip is late,
by the face wait in 3.4, the still likeness speaks it; if the voice fails, the turn
stays as text. The text is on screen first and never waits for a clip.

### 12.4 In a session

- The always-on line reads "AI tutor, shown in your likeness. Style preset:
  Groundwork." With the fictional preset, where it is opted in: "AI tutor, shown in
  your likeness. Style preset licensed from A. Example (fictional). A. Example does
  not appear, and does not write or check these answers." (01)
- A fallback turn is spoken exactly as written.
- A safety reply, and the tutor's answer to any message the safety check did not
  class `academic`, is shown as text from the standard tutor and never rendered in
  the likeness (D64).
- It never claims to be the learner, never comments on their face or voice, and
  offers no filter or alteration (D64).
- "Standard tutor for this session" is one tap away and deletes nothing.
- Figures render beside the likeness.

### 12.5 Deletion

The learner, in a session, or the adult, from the account, can delete it at any
moment, with no reason asked. The write sets `SelfTutor.status` to `deleting` and
clears the cached flag, so the next turn has the standard tutor; the cache's
sixty-second ceiling bounds it if the clearing fails. The `purge` function removes
the files at once, the `jobs` function then removes the `LikenessRef` rows, and a
daily run retries anything left, so that nothing remains after seven days (D63). The
same runs when an account closes, after twelve months without a self-tutor session,
and when the test period ends. Record in `docs/retention.md` whether Modal backs up
volumes, and for how long; how long Neon's history and any branch made from `main`
keep testers' rows; and what Modal's logs keep, which must never include a learner's
words. At the end of the test period, delete those copies too, or record why one
cannot be.

### 12.6 The licence audit, first

Before any model or library in this section is used, phase 1 records in
`docs/licences.md`, for each model, its weights and every dependency they bring:
the licence, where it was read, and whether it permits commercial use. Anything that
does not, or is unclear, is replaced or left out. Some open face pipelines depend on
InsightFace's pretrained models, which are for non-commercial research only; none of
those is used (OA-45).

## 13. Papers and the grade range

Both are computed, never generated, and neither calls a model (06).

**Papers.** `content/papers/` holds the MVP's own structural specification for each
qualification and tier: the mark total, the time allowed, the coverage across
objectives, the command-word mix and the difficulty distribution, each with a
tolerance. They are design choices, written in phase 4 and approved by the owner; no
board's paper shape is used (D85). The assembler solves for a paper with CP-SAT, one
worker and a fixed seed, so that the same inputs give the same paper, from practice
items only, excluding items the learner has seen recently (3.4). T-PAP-01 runs at
assembly, and a paper that fails is not assembled. Every paper has its mark scheme,
called "CINE mark scheme" wherever a tester sees it (D36), with the label. The CAS
marks final answers; the tester marks the rest against the mark scheme.

**The grade range.** For the algebra strand alone, and saying so: an arithmetic
mapping from the learner's unaided-check results to a band, recomputed every session
and built as 05 sets out:

- always a range, never a point, and worded as a current performance band on the
  MVP's own items, never a forecast; the word "prediction" appears nowhere;
- shown with the evidence it rests on (how many items, over what period, covering
  what share of the strand) and with the objectives that would move it;
- never comparative: no learner is shown against another;
- not shown below the sufficiency gate, a least number of check items and a least
  share of the qualification's objectives;
- hideable by the learner from their own view, with a plain note that the parent's
  report still shows it;
- open to challenge, answered by showing the item results behind it;
- marked "Provisional, and not calibrated against any examination" (`calibrated` is
  false).

The mapping and the gate are design choices written in `tutor/platform/grade.py`,
approved by the owner in phase 4 and explained on the screen that shows the range.
Only the learner's and the parent's reporting views read `GradeRange`, and nothing
is decided or gated on it (D35, T-GATE-01).

## 14. Safety

05 runs as written, with the owner as the reviewer.

**The three moves,** for every `wellbeing` message, a message about the learner's own
life, feelings or safety, as text from the standard tutor, written in advance in
`tutor/pipeline/replies.py`:

> Thank you for telling me. If you want to talk to someone now, you can call Childline
> free on 0800 1111, or Samaritans on 116 123, at any time. I am passing this on so
> that a person can look at it.

The session then offers "Carry on" and "Stop here". The tutor asks nothing about what
was said. An `Escalation` row goes to the reviewer's queue with its category; the
reviewer sees that session's transcript, and the access is logged with its reason.
The reviewer works to `docs/reviewer-policy.md`, which a lead session drafts in phase
4 and the owner approves: how soon the queue is read, what the reviewer does when a
tester may really be at risk, and that nothing from an escalation goes to anyone
else. If testers outside the UK are invited, add their country's services to the
reply before they start.

**Fixed replies,** for `off_topic`: "That is outside what I can help with here.
Shall we carry on with [objective]?"; and for `unsuitable`: "I cannot help with that.
Shall we carry on with [objective]?"

**Anti-companionship** (05): the tutor claims no feelings, preferences or life
outside the session; the MVP never starts contact, so it sends no notifications and
no email; it remembers nothing about a learner but `MasteryState`; and the session
cap holds. There is no engagement objective anywhere: no streaks, badges, loss
aversion or reminders to come back (D25).

**The welcome page says,** before anyone signs in: this is for adults, who play a
learner of 14 to 18, and never for a child; nothing in it is validated by an
examiner; Anthropic and Google receive what testers type and what the tutor writes,
on their standard terms; Modal runs the MVP and the open models, and Neon holds
accounts, transcripts and progress until the test ends; a tester's face and voice, if
they make a self-tutor, are stored encrypted on Modal, go to no speech or animation
company, and are shown to no one else; and this is a tutoring test, not a place to
seek help, with the services to call.

**Staff access** (05): nobody browses transcripts. The reviewer sees an escalated
session; the validator sees turns drawn for adjudication; the admin sees a session a
tester has asked about. Each access writes an `AccessLog` row with its reason.

## 15. Accounts, roles and surfaces

**Accounts.** By invitation only. The owner makes an invitation in the console and
sends the link themselves; the tester sets a password, kept with argon2id, on first
use. The MVP sends no email. Sessions use a signed, HttpOnly, Secure, SameSite=Lax
cookie, and every form carries a CSRF token. The simulated age check is one screen,
"A real product would check your age with a certified provider here. This test only
records that you are an adult.", and a box to confirm it (D88). The tester then makes
one or more learners, each with a nickname, a year group from 10 to 13, a
qualification and a tier, and plays each of them themselves.

**Roles:** `tester` (the adult on an account, and the learners they play),
`reviewer`, `validator` and `admin`. The owner holds all four. Nobody else holds more
than `tester` unless the owner grants it.

**Surfaces,** phone first. Each works at 390 px wide and at desktop width; every
control is a real button, link or input with a label; touch targets are at least
44 px.

| Surface | For | Holds |
|---|---|---|
| Welcome | anyone | the statements in section 14, and sign-in |
| Account | the adult | the learners, the parent report, the adult's self-tutor consent, deleting a self-tutor, requesting the full record, deleting everything |
| Learner home | the learner | the pick-up line, the objectives with the scheduler's proposal, style and adjustments, papers, the grade range, the self-tutor |
| Session | the learner | the always-on line, turns with their mathematics and figures, the waiting steps, the answer box and its preview, the check, the close, the self-tutor and the standard-tutor switch |
| Paper | the learner | a timed paper, the answers, the results, the CINE mark scheme |
| Reviewer | `reviewer` | the escalation queue, each session's access logged |
| Validator console | `validator` | the adjudication queues for T-GND-01 and T-MTH-01, T-SCP-01's sample, and 03's validation workflow on the fixture bank |
| Owner's console | `admin` | invitations, testers and cohorts, presets and the kill switch, the fictional creator's controls, counters and caps, battery runs and reports, the test period, deletions |

**The parent report** (01) shows objectives attempted, objectives passed on the
unaided check, time on task, the schedule of returns and the grade range. It never
shows a transcript by default (D16), and never an image, a voice or a clip of a
self-tutor (D60). "Request the full record" makes a request the owner fulfils by
export. The export holds no likeness, which the web app cannot reach; whether the
product's subject access route must reach it is OI-23, which the MVP does not answer.

**Validation.** 03's workflow is built and shown working on a fixture bank kept apart
from the MVP's own. No MVP item changes status: every one stays draft, and keeps its
label (D82).

**The always-on line** (01), at the top of every session screen and never behind a
menu: "AI tutor. Style preset: Groundwork.", or "AI tutor. Style preset licensed from
A. Example (fictional). A. Example does not write or check these answers.", or the
adjusted and self-tutor forms above; and under it, "Nothing here has been validated by
an examiner."

**The look.** Plain and calm: one accent colour, text of at least 18 px on a phone,
mathematics at the size of the text, figures at full width. The app engineer proposes
the look in phase 1, and the owner approves it by trying the shell. Interface copy is
British English, with no dashes. No copy says or implies that the tutor does not make
things up (D21), and none names an exam board.

## 16. Deployment

One Modal app, `tutor-mvp`, defined in `tutor/modal_app.py`:

| Function | Runs | Secrets |
|---|---|---|
| `web` | the FastAPI app, on CPU | `anthropic`, `gemini`, `neon`, `app` |
| `capture` | storing a capture, and the liveness checks, on a GPU | `likeness` |
| `voice` | Chatterbox, on a GPU | `likeness` |
| `face` | MuseTalk, on a GPU | `likeness` |
| `purge` | deleting likenesses | `likeness` |
| `jobs` | daily: deletion sweeps, the twelve-month rule, the end of the test period, T-VAL-01's census | `neon` |
| `battery` | T-REG-01 and the measured tests | `anthropic`, `gemini`, `neon` |

The GPU functions scale down after their idle time and run at most their number of
containers (3.4); the phase 1 spike chooses the GPU type by measured render time. The
likeness functions are called by the web app and are never web endpoints. Neon has
one project, whose `main` branch holds the MVP's data; no branch is made from it while
testers' data is there. `make deploy` runs `modal deploy tutor/modal_app.py` from a
commit on `main`, and refuses unless `make test` passes and the latest `BatteryRun`
ran on the current models, prompts, card renderer and composer, by its
`config_hash`.

GitHub Actions runs `make test` and a secret scan on every push and every pull
request, against a Postgres service. The battery runs on demand, from the console or
with `make battery`, never in CI, because it calls paid models.

## 17. Tests

Written before the code they test. Each plane's own tests are in `tests/unit/`; the
vault's tests and the invariants' are in `tests/invariants/`, one file each, each
marked with the phase by which it must pass. `PHASE` holds the phase being built:

- `make test`: the unit tests, the content checks on the whole bank, and the
  invariant tests of finished phases, those marked lower than `PHASE`. It must pass
  at every stop and every merge; when nothing is collected, as in phase 0, it passes.
- `make test-phase`: the invariant tests marked with the current phase. They fail
  until the phase's work is merged, and the lead runs them to know a phase is done.
- `make test-all`: every test, the later phases' included.

A test is never skipped, weakened or marked as expected to fail to get a change
through. A test that is wrong is changed in a lead session, with the reviewer, and the
reason goes in the commit message.

**Phase 0's own tests** hold the harness: the contracts load, and the vault's two
style vectors and its provenance example validate against them; `.claude/settings.json`
parses; every hook script runs on Python 3.9 and later; the Makefile has its targets;
the git hooks are installed; and every invariant test is marked with a phase.

**The vault's tests, as the MVP runs them.** A test that gates must pass, or meet its
threshold, before its phase is done. A test that reports runs, and the owner reads it
against its floor; the battery is too small to show that a floor is met with
confidence, which is M2's work, and every report says so.

| Test | The MVP's version | Kind | Phase | Gates |
|---|---|---|---|---|
| T-VAL-01 | The census: no item is live without a complete validation record within its date, and a failure takes items out of live. No MVP item is live, so the test also proves, on the fixture bank, that it would catch one | fast, and nightly | 1 | yes |
| T-MTH-01 | SymPy on every checkable step, against 03's floor of 99.0 per cent; the owner adjudicates a sample of the unchecked steps | the checker fast, the rate slow | 2 | the checker |
| T-GND-01 | Automated entailment of every assertion in the battery, against 03's floor of 99.5 per cent; the owner adjudicates a sample, and every failure; reported for each turn and each session | slow | 2 | no |
| T-SCP-01 | The scope check on the battery, against 03's floor of 99.5 per cent, and the owner's sample | slow | 2 | no |
| T-REG-01 | The frozen battery, under every shipped preset, with the measured tests above, on every change to a model, a prompt, the card renderer or the composer's rules | slow | 2 | it must run |
| T-ZERO-01 | The same battery with the persona registry empty, so that only the archetypes remain (D11, D23) | slow | 2 | it must run |
| T-SLF-02 | Photographs, videos and recordings replayed by the owner are refused; the false-accept rate is judged against a threshold the owner writes before phase 3 | slow, with the owner | 3 | yes |
| T-SLF-03 | Every clip's script equals the spoken form of the gated text | fast, and in every render | 3 | yes |
| T-SLF-04 | After deletion the next turn has no likeness, and none within sixty seconds even if the cache is not cleared; the store and `LikenessRef` hold nothing; no clip exists; no GPU container wrote to disk | fast with fakes, slow end to end | 3 | yes |
| T-SLF-05 | No surface lets anyone but the learner see or hear a self-tutor, or obtain anything it renders: every route is listed and tried with every role, and without the passcode | fast | 3 | yes |
| T-SLF-06 | Every clip carries the visible label and the provenance metadata | fast, and in every render | 3 | yes |
| T-PAP-01 | At assembly: every item a CAS-checked draft; the mark total, the coverage, the command-word mix and the difficulty within tolerance; no item twice in a paper or in the learner's recent history | fast | 4 | yes |
| T-GATE-01 | No component outside the learner's and the parent's reporting views reads `GradeRange`: not the scheduler, the composer or any experiment (D35) | fast | 4 | yes |
| T-STY-01 | The signatures of the battery's transcripts against each preset's vector: at least ten of twelve within the band, and none outside twice it | slow | 4 | yes |
| T-STY-03 | One objective under every shipped preset: the objective's required nodes cited under each, and no difference in correctness | slow | 4 | yes |
| T-STY-02 | Blind discrimination: a grader sees two battery transcripts of one objective under two presets, and the two cards, and says which is which; the sample size and the test are written down first. Graders see battery transcripts only, never a tester's session (T1 in 05) | built in 4, graded by testers in 5 | 5 | no |

T-SLF-01, T-CAL-01 and T-STY-04 do not run: the first two need real learners and real
examinations, and the third applies only under D6.

The battery's simulated learner is Gemini 4 Argon, following a fixed script for each
objective: answer correctly once, make the objective's first known misconception, ask
for the rule, go off the topic once, ask about something beyond the objective, ask for
the check, and answer the check from scripted answers, some of them wrong. Each report
gives every measured rate against its floor, the gate-fire rate, the time of each step
and the tokens used.

**The invariants' own tests,** all fast, each marked with the phase that builds what
it tests:

| Phase | Tests |
|---|---|
| 0 | no field anywhere holds a date of birth, an age, a school or an address; no learner, user or turn table has a column for a likeness, audio or video; no route accepts a file, and no template has a file input; every route needs a signed-in user, except the welcome, sign-in and invitation pages |
| 1 | the Groundwork card's golden test; no content file names an exam board or a past paper, and `content/sources/` holds only the DfE's documents (invariant 12) |
| 2 | the generator is called with no tools; no check item ever appears in a `TurnPlan`; the card is not an input to the composer's choice of sources or to any check; the composer gives the same plan for the same inputs; nothing about a turn reaches the browser before its verdict; the checks use another model family from the generator's, and a SymPy failure always fails the gate (invariant 5); every expression on screen is rendered from its parsed form (invariant 6); every served item carries its label; no turn's text, message or node is written to a log; safety replies come only from `replies.py` (invariant 15) |
| 3 | the web app builds every script from a stored turn, and the likeness functions are not web endpoints; `SelfTutor.status` is read through a cache of sixty seconds, tested with a fake clock; no turn after a message the safety check did not class `academic` is rendered in a likeness (invariant 15) |
| 4 | `Preset.enabled` is read through a cache of sixty seconds, tested with a fake clock; every paper and mark scheme carries its label |

Fast tests use no network, no GPU and no paid call. The models sit behind interfaces
with fakes, and the suite finishes in minutes. Each run makes its own database on a
local Postgres server, which the Makefile names by `TEST_DATABASE_URL`, and drops it
after, so that runs in different worktrees do not meet.

## 18. Build order

Six phases, each ending in something the owner can try and `make test-phase` passing:

0. accounts and the harness;
1. spikes and foundations: the licence audit and the likeness spike, liveness
   included; the database and accounts; the mathematics, the content checks and the
   figure renderer; the objective lists; the presets and the card renderer; the
   T-VAL-01 census; the app's shell;
2. the turn pipeline: the safety check, the composer, generator, verifier, gate and
   fallback; the session's five steps; the battery; the first content;
3. the self-tutor;
4. around the session: papers, the grade range, the parent report, the reviewer's
   queue and its policy, the validator console, the kill switch and the creator's
   controls, and the rest of the content;
5. testers.

The prompts for each, and the checklist before anyone else uses the MVP, are in
`PROMPTS.md`, which the owner keeps outside the repository.

## 19. When something fails

| Failure | The learner sees |
|---|---|
| The generator refuses, errors or times out | the blocked turn and the item verbatim |
| A check errors or times out | the same |
| Gemini is unavailable | the same, for every turn, until it returns |
| The safety check fails | "That did not go through. Please send it again." |
| A GPU is cold or slow | the text at once, and the clip when it is ready |
| The face fails | the still likeness, speaking |
| The voice fails | the text alone |
| The database is unavailable | an error page; nothing is generated |
| A daily cap is reached | a message saying so, and that it resets tomorrow |
