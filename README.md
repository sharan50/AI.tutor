# AI.tutor: venture design vault

The design and planning record for an AI tutor for UK GCSE and A-level students,
built in Bengaluru. There is no code, no pilot and no customer. This repository is
the source of truth for the design; a later phase turns it into a product.

Origin: an IIM-A MBA submission from 2025, substantially revised in September 2026
after the market and the law both moved. See `docs/00-thesis.html` for what survived
that revision and what did not.

## Reading order

Start at `docs/index.html`. Read 00, then 09, then whichever of 04 and 05 matches
who you are. A lawyer wants 04 and 13. An investor wants 00 and 09. A creator wants
04. A curriculum specialist wants 02 and 03.

## The provenance convention

Every claim carries a tag in the right margin.

- **Verified**: checked against a named source on a named date. Sources in `evidence/sources.html`.
- **Assumed**: reasoned, not confirmed. Listed in `docs/14-open-items.html`.
- **Open**: unresolved, and something depends on it.
- **Decision**: a choice made deliberately. Recorded in `docs/decision-ledger.html`.

A page with no tags has not been written properly yet.

## Status

Drafted: 00, 01, 02, 03, 04, 05, 09, 13, decision ledger.
Outline only: 06, 07, 08, 12.
Blocked and not written: 10 (economics), 11 (roadmap), each on inputs that do not exist yet.

The one decision everything downstream is waiting on: which board, subject and tier
to launch with. It unblocks the accuracy floor in 03, cost per session in 06, and
documents 10 and 11 entirely.

## Editing and publishing

Content lives in `src/content/` as HTML fragments. The page shell, navigation and
contents list are generated.

```
python3 src/build.py
```

No dependencies and no build tooling. Netlify runs the same command and publishes
`docs/`.

## Also here

- `BUILD_BRIEF.md`, the instruction that produced this repository.
- `contracts/`, creator licence heads of terms.
- `evidence/sources.html`, every external claim with its source and check date.

