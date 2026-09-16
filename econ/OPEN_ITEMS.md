# Open items

**Seed 20260916, run date 2026-09-16.**

Every question this model does not answer, with one owner and one trigger each.

**A trigger that cannot produce the quantity is worse than no trigger, because it
looks like a control.** Each row below names an instrument that can actually
produce the number. Where the vault already schedules an instrument that cannot,
the row says so.

Ordered by how much the answer moves the result, which is the ordering from
section 8 of the write-up rather than from convenience.

---

## The ones that decide whether there is a business

| # | Question | Owner | Trigger that can actually produce it | What it moves |
|---|---|---|---|---|
| E1 | Do parents anchor an AI tutoring subscription against the tutoring rate or against software prices? | Owner | A landing page running a tutoring-anchored price point against a software-anchored one, compared on revenue per visitor. Days, small spend, no product. This is condition C1 in docs/09 and milestone M1 in docs/11, and it is adequate to the quantity. | 30,769,800 dollars of terminal cash between the two states, and 4,441,824 of peak funding at the eightieth percentile. The largest single number here. |
| E2 | What does it cost to acquire a household, at the spend actually planned rather than at low volume? | Owner | Thirty measured acquisitions through one named channel at a stated monthly spend, reported as spend divided by acquisitions, split creator-led and not, then repeated at three times the spend to measure the saturation exponent rather than assume it. One channel test at two spend levels. | First-ranked driver on whether a path ever reaches profitability, first-order index 0.218. |
| E3 | How many sessions does a household actually use in a month? | Owner | Thirty households instrumented for one month. **Nothing in docs/11 produces this before M5**, and M5 needs a built product and a first cohort. It appears on both sides of the unit economics and the session allowance cannot be set without it. This is the instrument gap in checklist item 22. | Sets whether 23.6 per cent of households exceed the allowance, or almost none do. |
| E4 | What does age assurance cost per verified adult? | Owner | Three quotes from certified providers. Three phone calls, this quarter, nothing built. Condition C2 in docs/09, and adequate to the quantity. | Age assurance is 1.1 per cent of the modelled cost base, and it subtracts from the acquisition budget pound for pound. |
| E5 | How many reachable households are there in the United Kingdom? | Owner | Two weeks of paid search at the objective granularity the item bank is already organised around, reporting qualified visits per pound and trial starts. Not a market-size report. | Sampled across a thirtyfold range. Its effect is muted in this model because the acquisition budget cap moves with it, and that muting is a model property rather than a fact. |

---

## The ones that decide how much capital it takes

| # | Question | Owner | Trigger that can actually produce it | What it moves |
|---|---|---|---|---|
| C1 | How many items does a full subject bank need at one level for one board? | Content lead | Decompose one DfE subject content document into objectives and count what the ten-items-per-objective rule implies. An afternoon. docs/03 already flags that its own 60-objective figure is a planning number, not a count. | First-ranked driver on the capital requirement, first-order index 0.165. Pinned across its range it swings terminal cash by 15,940,982. |
| C2 | How many minutes does examiner validation take per item, and what is the contract rate? | Content lead | docs/03's timed pilot, **stratified**: not twenty items of one kind in one strand, but a sample across subject, item kind and difficulty, because the cost base extrapolates across up to eleven subjects, two levels and four boards. See checklist item 23. A few hundred pounds either way. | Pinned across its range, 11,572,921 of terminal cash. |
| C3 | What does it cost to author an item, as against validating it? | Content lead | The same pilot, with authoring timed separately. It is a distinct driver and ranks above validation minutes on the capital target. | Pinned across its range, 10,920,946. |
| C4 | How much of a subject bank carries across to a second United Kingdom board? | Content lead | Build one strand to two board specifications and count what changed. One strand, not one subject. | Pinned across its range, 9,692,829. It is the term the whole expansion case rests on and the model deliberately does not let it be near one. |
| C5 | How much carries across to a foreign curriculum? | Content lead | The same exercise against one United States or Indian specification. | Ninth-ranked driver on the capital target. Decides whether the month-18 international ambition is an extension or a rebuild. |

---

## The ones the model cannot answer at all

| # | Question | Owner | Trigger that can actually produce it | Why the model is silent |
|---|---|---|---|---|
| X1 | What is outcome evidence worth? | Owner | A school pilot with a comparison group and a common assessment, which is a year and a sales motion. docs/09 argues it is the only durable moat. | The instrument charges the institution channel 5,435,967 dollars and credits it nothing for evidence. That figure is a lower bound on Route B's worth, not an estimate of it. |
| X2 | What does a creator charge to license name and likeness? | Owner | Ask three. A conversation each, before any contract. D5 asserts a one-page agreement; nothing establishes its price. | The published run charges zero. Priced at -2,204,366 dollars in the `por_creator_fees` scenario. |
| X3 | Will a competitor move on the United Kingdom curriculum specifically? | Owner | Not resolvable by an instrument. Watch what Google, OpenAI and Oak National Academy ship. | No competitive response of any kind is modelled. |
| X4 | Does the refusal behaviour cost retention? | Product | Correlate gate-fire rate against second-session return from the first live week. docs/06 already instruments the gate-fire rate, so this is a join, not a new instrument. | Gate-fire rate enters cost only. Its retention effect is in the feedback scenario as part of a bundle, not separately. |
| X5 | Does the Year 10 household pay through the summer? | Owner | The first cohort, reported by year group and never blended, across one July and August. This is OA-21 in docs/10. | The model samples it between 0.20 and 0.85 and the ratio it produces is 1.24 rather than the two docs/10 reasons toward. |
| X6 | Would an Indian direct-to-parent service be lawful at all? | Counsel | DPDP Rules 2025 section 9(3) and the Fourth Schedule educational-institution exemption, put to Indian counsel as a specific question about a digital-first platform. | The model prices the revenue at -214,869 dollars over five years. It cannot price a prohibition. |
| X7 | What happens under a correlated downturn? | Owner | Not resolvable in advance. | The shock acts on acquisition only. There is no regime in which demand, retention, vendor prices and the examiner labour market move together. |

---

## Items carried from the vault that this model touches

These are already open in docs/14. They are repeated here only where this
instrument changes what they are worth.

| Vault item | What this instrument adds |
|---|---|
| OI-5, age assurance cost | Now has a cost share, 1.1 per cent of the modelled base, and a break-even solve in `out/breakeven.csv`. The idea that it could dominate the cost structure is not supported; what it does is subtract from the acquisition budget, as docs/10 says. |
| OA-10, the price anchor | Now has a number on it: 30,769,800 dollars of terminal cash between the two states. |
| OA-21, payment across the summer | Now has a ratio: 1.24 rather than two, and it reaches two on 0.0 per cent of paths. |
| The docs/10 assumption that variable cost is small relative to price | Holds. Inference is 2.5 per cent of the modelled cost base, so the sensitivity row docs/10 flags as reversible does not reverse under these priors. |
| OI-7, which entity contracts with the parent | Determines the VAT treatment this model assumes. The model reads consumer prices as gross; a different contracting entity could change the rate but not the reading. |
