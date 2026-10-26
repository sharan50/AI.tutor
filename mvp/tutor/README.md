# The Tutor MVP's specification pack

This pack is what you give Claude Code to build the Tutor's MVP: a working build of
the whole design, for adults who play learners of 14 to 18, taught from the algebra
of GCSE Mathematics, Level 2 Further Mathematics and A-level Mathematics, with the
self-tutor on open models. The reasons for every choice are in the build guide,
<https://aitutor-plan.netlify.app/docs/tutor-mvp.html>; where the pack and the guide
disagree, the guide governs.

Written 26 October 2026. Nothing in it has been built or run.

## What is in it

| File | Goes to, in the MVP's repository | What it is |
|---|---|---|
| `CLAUDE.md` | `CLAUDE.md` | the invariants and how to work, read by every session |
| `SPEC.md` | `SPEC.md` | what to build, section by section |
| `agents/*.md` | `.claude/agents/` | the team: six builders, each in its own worktree, and a reviewer |
| `settings.json` | `.claude/settings.json` | the permissions and the hooks |
| `hooks/*` | `.claude/hooks/` | the scripts the hooks run |
| `githooks/*` | `.githooks/` | the git hooks that refuse a merge which breaks the tests |
| `PROMPTS.md` | nowhere: keep it yourself | the prompt for each phase, and the checklist before testers |

## How the harness works

- **The invariants** are in `CLAUDE.md`, which Claude Code reads at the start of every
  session, and each is held by a test.
- **The tests come first.** Phase 0 writes every test as a failing test, marked with
  the phase by which it must pass. `PHASE` says which phase the build is in, and only
  you change it. `make test` runs the unit tests and the tests of finished phases;
  `make test-phase` runs the current phase's, and is how the lead knows a phase is
  done.
- **The hooks.** After every edit, the changed file is linted, and an item file is
  checked by the algebra system. When the lead or a builder tries to finish, `make
  test` runs, and the hook refuses up to five times in a row while it fails; then it
  lets the agent stop, and the agent must say the tests fail. Anything that looks like
  an API key is refused before it is written or run.
- **The merge gate.** A git hook runs `make test` on every merge and refuses one that
  fails, so nothing reaches `main` that breaks a finished phase. CI runs the same
  tests, and a secret scan, on every push.
- **The permissions.** Changes to the contracts, the configuration, the invariant
  tests, the thresholds, `PHASE`, `CLAUDE.md`, `SPEC.md`, `.claude/` and `.githooks/`
  ask you first. The DfE sources cannot be edited. A hook refuses any fetch from an
  exam board's site, at any subdomain, or from an address that looks like a past
  paper or a mark scheme. The content author has no fetch tool, and its shell runs
  only the content checks and git.
- **The team.** A lead session, the one you paste a prompt into, sends the builders to
  work in parallel, each in its own worktree branched from the lead's current work;
  the reviewer reads every change; the tests and the reviewer decide what merges.

Phase 0 checks that each hook and rule behaves as described, in the main checkout and
in a worktree, and reports any that does not. Claude Code's sandbox, where the
machine supports it, adds a network allowlist for every command; phase 0 proposes one
for you to approve. Agent teams, an experimental feature, are not used.

## How to use it

1. Read the build guide, then `PROMPTS.md` from the top. "Before phase 0" lists the
   accounts, the files to copy, the DfE documents to download and the secrets to make.
2. Paste the phase 0 prompt into a Claude Code session at the root of the new
   repository. When it reports, check what it says, try the result, and change and
   commit `PHASE` yourself.
3. Do the same for each phase. Each prompt says what done looks like, and each phase
   ends with something for you to try.
4. Before the first tester, go through the checklist at the end of `PROMPTS.md`.

## What it does not do

It does not make the content validated: every item is a draft, checked by a computer
algebra system and by no examiner, and every screen says so. It does not make the MVP
evidence about learners. And it is not for children: never let anyone under 18 use
it.
