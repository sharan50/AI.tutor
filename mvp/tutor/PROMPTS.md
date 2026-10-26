# Tutor MVP: the phase prompts

Keep this file yourself, outside the MVP's repository, so that no agent works ahead of
the phase it was given. Paste one prompt at a time into a new Claude Code session at
the repository's root: that session is the lead, and the agents in `.claude/agents/`
are its team. Start each phase only when you have tried the last one, its tests pass,
and you have changed `PHASE` to the new number yourself.

Written 26 October 2026, with the build guide,
<https://aitutor-plan.netlify.app/docs/tutor-mvp.html>, and `SPEC.md`.

## Before phase 0

1. Make the accounts in `SPEC.md` 3.2, and set the spend limits at Anthropic and
   Google.
2. Make a private GitHub repository and clone it.
3. Copy in from the pack: `CLAUDE.md` and `SPEC.md` to the root; `agents/*.md` to
   `.claude/agents/`; `settings.json` to `.claude/settings.json`; `hooks/*` to
   `.claude/hooks/`. Write `0` in a file called `PHASE`.
4. Download the DfE subject content for GCSE Mathematics and for A-level Mathematics
   from gov.uk into `content/sources/dfe/`. Nothing else goes in that folder, and no
   board's document goes anywhere in the repository.
5. Make the Modal secrets in `SPEC.md` 3.3. For `LIKENESS_KEY` and `SESSION_SECRET`,
   use long random strings that you keep nowhere else.
6. Make sure the machine has Python 3.12, uv, git, make and a local Postgres for the
   fast tests. In a Claude Code cloud environment, install Postgres in the setup
   script and allow network access to the providers' and Modal's hosts.
7. Commit, and push.

## Phase 0: the harness

```
Read CLAUDE.md and SPEC.md in full. This is phase 0: build the harness and no
product code.

1. Create the layout in SPEC.md section 4, a pyproject.toml with the stack in 3.1,
   and a Makefile with test, test-all, lint, check-content and battery targets.
   Make pytest read PHASE and run, under `make test`, only the tests marked with
   that phase or an earlier one.
2. Write every contract in SPEC.md 4.1 as Pydantic models in tutor/contracts/, the
   data model of section 5 as SQLAlchemy models, and a first Alembic migration.
3. Write every test in SPEC.md section 17 as a failing test in tests/invariants/,
   one file each, marked with its phase. Each must fail because what it tests does
   not exist yet, not because the test is broken: give the code it calls stub
   interfaces that raise NotImplementedError.
4. Write the fakes for Claude, Gemini and the renderers, behind the interfaces the
   tests call.
5. Check that every hook and permission rule in .claude/settings.json does what it
   says, in the main checkout and in a worktree: edit a contract, write a fake key,
   break a test and try to stop. Report any that does not work, and do not change
   .claude/ without asking me.
6. Write tutor/modal_app.py with the web function serving one page, "Tutor MVP:
   nothing here yet", migrate the Neon database, and deploy.
7. Add GitHub Actions that run `make test` on every pull request.

Done when `make test` passes, `make test-all` fails only with NotImplementedError,
and the page is live. Report the address, the number of tests for each phase, how
each hook and rule behaved, and anything in SPEC.md that was unclear. Do not start
phase 1.
```

Then set branch protection on `main`, requiring the check from GitHub Actions.

## Phase 1: spikes and foundations

```
Read CLAUDE.md, and SPEC.md sections 2 and 18. This is phase 1. Dispatch these
agents in parallel, each in its own worktree, with the SPEC.md sections its
definition names:

- likeness-engineer: first the licence audit (SPEC.md 12.6) for every model and
  dependency in 3.1 and section 12. Then a spike outside the product: a test page
  that captures my face and voice live, and a script that makes the likeness say
  one fixed sentence with Chatterbox and MuseTalk, timed on two GPU types.
- content-author: the objective lists for the three qualifications (SPEC.md 6.2).
  Present the Further Mathematics list for my approval, and write no items.
- style-engineer: the three presets and the card renderer with its golden test
  (SPEC.md 11.1 and 11.2). Propose the fictional preset's values for my approval.
- platform-engineer: the database, accounts, invitations, roles, sign-in, the
  simulated age check and learners (SPEC.md 5 and 15).
- app-engineer: the app's shell, phone first: welcome, sign-in, account, learner
  home and an empty session screen with the always-on line. Propose a look.

When each finishes, have the reviewer read its change. Merge, one at a time, the
changes the reviewer passes, running `make test` after each merge. Send back to
its agent any change the reviewer does not pass.

Done when a likeness has spoken a fixed sentence, I have approved the Further
Mathematics list, the fictional preset and the look, and phase 1's tests pass.
Report the licence table, the render times, the number of objectives in each
qualification, and the Spine and fictional cards. Do not start phase 2.
```

Before phase 2: try the shell on a phone, read the cards, and approve or change the
lists. Delete your spike capture. Change `PHASE` to 2.

## Phase 2: the turn pipeline

```
Read CLAUDE.md, and SPEC.md sections 2 and 18. This is phase 2. Dispatch these
agents in parallel, each in its own worktree:

- pipeline-engineer: the mathematics (section 7), the safety check, composer,
  generator, verifier, gate, fallback and logger (section 9), the content checks
  (6.5), and the battery with its simulated learner (section 17).
- content-author: the items for the twelve battery objectives first (four for each
  qualification, which you choose and I approve), then onwards in each
  qualification's order. Run the content checks on every file.
- platform-engineer: sessions, the scheduler, the check and the close (section 8),
  the turn cap, the counters, and the adjudication queues with the access log.
- app-engineer: the session screen: the waiting steps, turns with mathematics, the
  answer box and its preview, the check and the close; and the validator console's
  adjudication screens.
- style-engineer: the signatures at logging time (11.6). Propose the scales and
  T-STY-01's band for tests/thresholds.toml, for me to write in.

Review and merge as in phase 1. Then run the battery once, with my approval.

Done when the battery has run and reported the gate-fire rate and each check's
failure rate, I have taken a session to an honest close on my phone, and phase 2's
tests pass. Report the battery's numbers, the share of steps the CAS could not
decide, the time of each step, and the items drafted so far. Do not start phase 3.
```

Before phase 3: take sessions under Groundwork and Spine, and adjudicate the
battery's failures and its sample in the validator console. Write the liveness
thresholds and T-SLF-02's false-accept threshold in `tests/thresholds.toml`. Change
`PHASE` to 3.

## Phase 3: the self-tutor

```
Read CLAUDE.md, and SPEC.md sections 2 and 18. This is phase 3. Dispatch these
agents in parallel, each in its own worktree:

- likeness-engineer: consents, capture, liveness, passcode, sample and choice, the
  store, rendering after the gate, labels and provenance, and deletion (section 12),
  using what the spike learnt.
- app-engineer: the self-tutor's screens, the session's likeness pane, the
  standard-tutor switch and deletion from both the session and the account.
- platform-engineer: the deletion sweeps, account closing, the twelve-month rule,
  and the route listing for T-SLF-05.

Review and merge as before. Then I will run T-SLF-02's attacks with you: photographs,
videos and recordings of me, replayed.

Done when T-SLF-02 to T-SLF-06 pass, and I have made a self-tutor, been taught by it,
switched to the standard tutor and deleted it, with nothing left. Report the
false-accept rate, the render times in sessions, and how often the still likeness
was used. Do not start phase 4.
```

Before phase 4: take a session with the self-tutor on a phone, then delete it.
Change `PHASE` to 4.

## Phase 4: around the session

```
Read CLAUDE.md, and SPEC.md sections 2 and 18. This is phase 4. Dispatch these
agents in parallel, each in its own worktree:

- pipeline-engineer: the figure renderer and its types (section 10).
- style-engineer: adjustments and clamps, the labels, the kill switch and its
  rehearsal script, the creator's controls and the self-tutor opt-in (11.3 to 11.5).
- platform-engineer: papers and T-PAP-01, the grade range, the parent report's data,
  the reviewer's queue, 03's validation workflow, cohort flags, the owner's
  console's data and the end of the test period (sections 13, 14 and 15).
- app-engineer: the screens for all of these, and T-STY-02's blind grading screen.
- content-author: the paper specifications for my approval, then the rest of the
  content.

Review and merge as before. Then run the battery, with my approval, and the kill
switch's rehearsal.

Done when T-PAP-01, T-STY-01 and T-STY-03 pass, T-STY-02's grading screen works,
the rehearsal's times are recorded, and every screen in SPEC.md section 15 works at
390 px and at desktop width. Report the battery's numbers, the rehearsal's times,
the paper specifications, the grade range's mapping, and how much of each
qualification has items. Do not start phase 5.
```

Before phase 5: set the test period's end in the console, write T-STY-02's sample
size and test in `tests/thresholds.toml`, make the invitations, and change `PHASE`
to 5.

## Phase 5: testers

```
Read CLAUDE.md, and SPEC.md sections 2 and 18. This is phase 5: adult testers are
using the MVP. Each time I bring you what a tester found, reproduce it with a test,
fix it through the right agent, have the reviewer read it, and merge. Run the
battery after any change to a model, a prompt, the renderer or the composer. When
I ask, run T-STY-02's analysis on the testers' gradings, and the checklist at the
end of PROMPTS.md, which I will paste.
```

## Before anyone else uses it

Go through this list yourself, with the lead session's help, before the first
invitation and again before each new group of testers.

- `make test-all` passes on `main`, and the deployed commit is that commit.
- The latest battery report has been read: the gate-fire rate, each measured test
  against its floor, the time of each step and the tokens per session.
- The welcome page says everything in `SPEC.md` section 14, before sign-in.
- A message of each safety category gets its reply, and a `wellbeing` message
  reaches the reviewer's queue. You will read the queue at least once a day.
- Every screen with an item, a paper or a mark scheme says "Not yet validated by an
  examiner", and the always-on line is on every session screen.
- The spend limits are set at Anthropic and Google, the turn cap stops a tester at
  its limit, and the GPU containers stop after their idle time.
- A self-tutor made and deleted leaves nothing behind, and no surface but the
  learner's own, behind the passcode, plays one.
- `docs/licences.md` covers every model and dependency, and none is for
  non-commercial use only.
- No secret is in the repository or its history.
- The test period's end is set, and its deletion has been rehearsed on a copy.
- Every tester is an adult, has been told they play a learner of 14 to 18, and has
  been asked never to let a child use it.
