# The Tutor MVP's specification pack

This pack is what you give Claude Code to build the Tutor's MVP: a working build of
the whole design, for adults who play learners of 14 to 18, taught from the algebra
of GCSE Mathematics, GCSE Further Mathematics and A-level Mathematics, with the
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
| `PROMPTS.md` | nowhere: keep it yourself | the prompt for each phase, and the checklist before testers |

## How the harness works

- **The invariants** are in `CLAUDE.md`, which Claude Code reads at the start of every
  session, and each is held by a test.
- **The tests come first.** Phase 0 writes every test as a failing test, marked with
  the phase by which it must pass. `PHASE` says which phase the build is in, and only
  you change it.
- **The hooks.** After every edit, the changed file is linted, and an item file is
  checked by the algebra system. When a session or an agent tries to finish, the fast
  tests run, and it may not finish while they fail. Anything that looks like an API
  key is refused before it is written.
- **The permissions.** Changes to the contracts, the invariant tests, the thresholds,
  `PHASE`, `CLAUDE.md`, `SPEC.md` and `.claude/` ask you first. The DfE sources cannot
  be edited. The exam boards' sites cannot be fetched, and the content author has no
  web access at all.
- **The team.** A lead session, the one you paste a prompt into, sends the builders to
  work in parallel, each in its own worktree; the reviewer reads every change; the
  tests and the reviewer decide what merges; and GitHub's branch protection refuses a
  merge with failing tests.

Phase 0 checks that each hook and rule behaves as described, in the main checkout and
in a worktree, and reports any that does not. Agent teams, an experimental feature,
are not used.

## How to use it

1. Read the build guide, then `PROMPTS.md` from the top. "Before phase 0" lists the
   accounts, the files to copy, the DfE documents to download and the secrets to make.
2. Paste the phase 0 prompt into a Claude Code session at the root of the new
   repository. When it reports, check what it says, try the result, and change `PHASE`
   yourself.
3. Do the same for each phase. Each prompt says what done looks like, and each phase
   ends with something for you to try.
4. Before the first tester, go through the checklist at the end of `PROMPTS.md`.

## What it does not do

It does not make the content validated: every item is a draft, checked by a computer
algebra system and by no examiner, and every screen says so. It does not make the MVP
evidence about learners. And it is not for children: never let a learner under 18 use
it.
