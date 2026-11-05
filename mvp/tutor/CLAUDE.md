# Tutor MVP

The Tutor of the AI.tutor vault, built as an MVP for adults who play learners of 14 to
18. `SPEC.md` says what to build; this file says what never changes and how to work.
Before any task, read the sections of `SPEC.md` it names, and `SPEC.md` section 2.

Nothing in this repository is validated by an examiner, and no child may use it.

## Invariants

Each is held by a test in `tests/invariants/`. A change that breaks one is wrong,
whatever else it does.

1. The model never retrieves. The composer chooses every source before the generator
   is called, with no model call, and the generator has no tools.
2. Nothing about a turn reaches the browser, the voice or the face before the gate has
   passed it. A failed turn shows the item verbatim.
3. Style never reaches the content plane: the card goes to the generator and nowhere
   else, never to the composer's choice of sources or to any check.
4. Check items never enter a turn plan.
5. Claude writes, Gemini checks, SymPy checks the mathematics, and nothing overrides
   SymPy.
6. Every expression on screen is rendered from the form SymPy parsed, and every spoken
   script is the spoken form of the gated text.
7. Only its learner sees or hears a self-tutor, behind their passcode. No surface shows
   or plays it to anyone else, and nothing it renders can be downloaded.
8. Nothing can be uploaded. Capture is live, against a challenge the server issued.
9. No learner, user or turn record holds a likeness, audio or video, and only the
   likeness functions hold the store's key.
10. No date of birth, age, school or address is stored anywhere.
11. `Preset.enabled` and `SelfTutor.status` are read at every turn, through a cache of
    at most sixty seconds.
12. No board's material, meaning no specification, past paper, examiners' report or
    mark scheme, from a board or from anywhere that copies one, is read, fetched,
    quoted or stored. `content/sources/dfe/` holds the only source documents.
13. Every item, paper and mark scheme says "Not yet validated by an examiner", and the
    always-on line is on every session screen.
14. No turn's text, learner's message or bank node is written to a log or the console.
15. Safety replies are written in advance, and shown as text from the standard tutor,
    never in a likeness.
16. Only the learner's and the parent's reporting views read `GradeRange`; nothing
    else is decided or gated on it.

## How to work

- Write the test first, and see it fail for the right reason before writing the code.
- Every test in `tests/invariants/` is marked with the phase by which it must pass.
  `PHASE` holds the phase being built; only the owner changes it, and commits the
  change.
  - `make test`: the unit tests, and the invariant tests of finished phases. It must
    pass at every stop and every merge.
  - `make test-phase`: the current phase's own tests, the lead's check that a phase is
    done. They fail until the phase's work is merged.
  - `make test-all`: everything.
- Never skip, weaken or delete a test, or mark one as expected to fail. If you think a
  test is wrong, stop and say why.
- When you stop, a hook runs `make test` and refuses, up to five times in a row, to
  let you finish while it fails; after that it lets you stop, and you must say in your
  report that the tests fail. A git hook refuses any merge that makes it fail.
- The contracts in `tutor/contracts/`, `tutor/config.py` and the tests in
  `tests/invariants/` change only in a lead session, with the reviewer; editing them
  asks the owner first.
- Stay inside the directories your agent definition gives you, and commit your work
  on your branch before you finish.
- Never read, and never ask for, a tester's image, clip, recording or screenshot.
  What a tester found is described in words.
- Before writing the integration for any model, SDK or platform feature, read its
  current documentation.
- Claude: the model id comes from `tutor/config.py`; send no temperature, top_p, top_k
  or prefill; give the generator no tools; use no server-side model fallback; a
  refusal fails the gate.
- Secrets are Modal secrets. Never put one in the repository, a log or the browser.
- Use the network only through uv, git, Modal's command line and documentation pages.
- Interface copy is British English, with no em-dashes or en-dashes.
- When a phase's work is done, report what was built, what the tests show, and
  anything in `SPEC.md` that was unclear. Do not start the next phase.

## Map

- `SPEC.md`: what to build. `PHASE`: the current phase.
- `tutor/contracts/`: the schemas every plane shares.
- `tutor/content/`, `tutor/maths/`, `tutor/figures/`: the bank, the mathematics, the
  figures.
- `tutor/pipeline/`: safety check, composer, generator, verifier, gate, logger; its
  prompts in `tutor/pipeline/prompts/`.
- `tutor/style/`: presets, the card renderer, adjustments, signatures, the kill switch.
- `tutor/likeness/`: consents, capture, liveness, store, voice, face, labels, deletion.
- `tutor/platform/`: accounts, sessions, the scheduler, papers, the grade range,
  reports.
- `tutor/web/`: routes, templates, static files. `tutor/modal_app.py`: the deployment.
- `content/`: objectives, items, presets, paper specifications, the DfE sources.
- `tests/invariants/`, `tests/unit/`, `tests/battery/`, `tests/thresholds.toml`.
- `docs/licences.md`, `docs/retention.md`, `docs/reviewer-policy.md`, `reports/`.
- `.claude/`: the agents, settings and hooks. `.githooks/`: the merge gate.

## Commands

- `uv sync`: install.
- `make test`: the unit tests and the tests of finished phases.
- `make test-phase`: the current phase's tests.
- `make test-all`: every test, including later phases'.
- `make lint`: ruff and mypy.
- `make check-content`: the checks on every item file.
- `make battery`: the slow tests. It calls paid models; run it only when asked.
- `modal serve tutor/modal_app.py`: run it against Modal, for trying.
- `make deploy`: deploy from `main`, refused unless the tests pass and the latest
  battery ran on the current models, prompts, renderer and composer.

## The design

The vault: <https://aitutor-plan.netlify.app/docs/>. Pages 01 (product), 02 (style
engine), 03 (content), 05 (safety) and 06 (architecture) are the design; the MVP build
guide, <https://aitutor-plan.netlify.app/docs/tutor-mvp.html>, gives the reasons for
this build. Read a page when `SPEC.md` names it and you need more than `SPEC.md` says.
