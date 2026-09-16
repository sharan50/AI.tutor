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
| E1 | Do parents anchor an AI tutoring subscription against the tutoring rate or against software prices? | Owner | A landing page running a tutoring-anchored price point against a software-anchored one, compared on revenue per visitor. Days, small spend, no product. This is condition C1 in docs/09 and milestone M1 in docs/11, and it is adequate to the quantity. | 29,107,825 dollars of terminal cash between the two states, and 4,135,474 of peak funding at the eightieth percentile. The largest single number here. |
| E2 | What does it cost to acquire a household, at the spend actually planned rather than at low volume? | Owner | Thirty measured acquisitions through one named channel at a stated monthly spend, reported as spend divided by acquisitions, split creator-led and not, then repeated at three times the spend to measure the saturation exponent rather than assume it. One channel test at two spend levels. | First-ranked driver on whether a path ever reaches profitability, first-order index 0.220. |
| E3 | How many sessions does a household actually use in a month? | Owner | Thirty households instrumented for one month. docs/11's M4 touches it, through sessions per learner per fourteen days as a secondary metric, and M4 already needs a signed creator and a built product; M5 is where it is measured properly and M5 needs a first cohort. **Nothing in the roadmap produces it cheaply or early.** It appears on both sides of the unit economics and the session allowance cannot be set without it. This is the instrument gap in checklist item 22. | Sets whether 23.6 per cent of households exceed the allowance, or almost none do. |
| E4 | What does age assurance cost per verified adult? | Owner | Three quotes from certified providers. Three phone calls, this quarter, nothing built. Condition C2 in docs/09, and adequate to the quantity. | Age assurance is 1.2 per cent of the modelled cost base, and it subtracts from the acquisition budget pound for pound. |
| E5 | How many reachable households are there in the United Kingdom? | Owner | Two weeks of paid search at the objective granularity the item bank is already organised around, reporting qualified visits per pound and trial starts. Not a market-size report. | Sampled across a thirtyfold range. Its effect is muted in this model because the acquisition budget cap moves with it, and that muting is a model property rather than a fact. |

---

## The ones that decide how much capital it takes

| # | Question | Owner | Trigger that can actually produce it | What it moves |
|---|---|---|---|---|
| C1 | How many items does a full subject bank need at one level for one board? | Content lead | Decompose one DfE subject content document into objectives and count what the ten-items-per-objective rule implies. An afternoon. docs/03 already flags that its own 60-objective figure is a planning number, not a count. | First-ranked driver on the capital requirement, first-order index 0.162. Pinned across its range it swings terminal cash by 13,525,563. |
| C2 | How many minutes does examiner validation take per item, and what is the contract rate? | Content lead | docs/03's timed pilot, **stratified**: not twenty items of one kind in one strand, but a sample across subject, item kind and difficulty, because the cost base extrapolates across up to eleven subjects, two levels and four boards. See checklist item 23. A few hundred pounds either way. | Pinned across its range, 9,787,530 of terminal cash. |
| C3 | What does it cost to author an item, as against validating it? | Content lead | The same pilot, with authoring timed separately. It is a distinct driver and ranks immediately below validation minutes on the capital target, at rank 4 against rank 5. | Pinned across its range, 9,296,821. |
| C4 | How much of a subject bank carries across to a second United Kingdom board? | Content lead | Build one strand to two board specifications and count what changed. One strand, not one subject. | Pinned across its range, 8,824,276. It is the term the whole expansion case rests on and the model deliberately does not let it be near one. |
| C5 | How much carries across to a foreign curriculum? | Content lead | The same exercise against one United States or Indian specification. | Rank 10 driver on the capital target. Decides whether the month-18 international ambition is an extension or a rebuild. |

---

## The ones the model cannot answer at all

| # | Question | Owner | Trigger that can actually produce it | Why the model is silent |
|---|---|---|---|---|
| X1 | What is outcome evidence worth? | Owner | A school pilot with a comparison group and a common assessment, which is a year and a sales motion. docs/09 argues it is the only durable moat. | The instrument charges the institution channel 2,238,366 dollars and credits it nothing for evidence. That figure is a lower bound on Route B's worth, not an estimate of it. |
| X2 | What does a creator charge to license name and likeness? | Owner | Ask three. A conversation each, before any contract. D5 asserts a one-page agreement; nothing establishes its price. | The published run charges zero. Priced at -2,082,643 dollars in the `por_creator_fees` scenario. |
| X3 | Will a competitor move on the United Kingdom curriculum specifically? | Owner | Not resolvable by an instrument. Watch what Google, OpenAI and Oak National Academy ship. | No competitive response of any kind is modelled. |
| X4 | Does the refusal behaviour cost retention? | Product | Correlate gate-fire rate against second-session return from the first live week. docs/06 already instruments the gate-fire rate, so this is a join, not a new instrument. | Gate-fire rate enters cost only. Its retention effect is in the feedback scenario as part of a bundle, not separately. |
| X5 | What is in-term churn, by year group? | Owner | The first cohort measured monthly across one examination cycle, split by year group and never blended. **Not** the summer question: pinning the summer away entirely only lifts the Year 10 ratio to 1.75, while pinning in-term churn to its floor and leaving the summer alone gives 1.31. | The ratio the model produces is 1.24 rather than the two docs/10 reasons toward, and in-term churn is the driver of that gap, not the summer. |
| X5b | Does the Year 10 household pay through the summer? | Owner | The same cohort across one July and August. This is OA-21 in docs/10, and it is the second question rather than the first. | Worth 1.75 against 1.24 on the retained-month ratio, at the extreme of removing the summer altogether. |
| X6 | Would an Indian direct-to-parent service be lawful at all? | Counsel | DPDP Rules 2025 section 9(3) and the Fourth Schedule educational-institution exemption, put to Indian counsel as a specific question about a digital-first platform. | The model prices the revenue at -3,286,962 dollars over five years. It cannot price a prohibition. |
| X7 | What happens under a correlated downturn? | Owner | Not resolvable in advance. | The shock acts on acquisition only. There is no regime in which demand, retention, vendor prices and the examiner labour market move together. |
| X8 | **May United Kingdom children's learner data be processed in Bengaluru at all?** | Counsel | docs/05 names it and marks it unconfirmed: an Indian controller processing United Kingdom children's data is a restricted transfer needing an international data transfer agreement or the United Kingdom addendum to standard clauses, plus a transfer risk assessment. Put it to counsel as a specific question about learner content and learner telemetry, separately. It is a question, not a build. | **This is the one unmodelled item that reorders the answer rather than shifting it.** Bengaluru engineering is sampled at 14,000 to 45,000 a head against United Kingdom roles at 45,000 to 98,000 in pounds. Forcing the learner path onshore is worth -13,390,271 dollars of terminal cash and moves people past content as the largest cost line, which inverts the sensitivity ordering the whole write-up is built on. |
| X9 | What is the probability and size of a regulatory penalty? | Owner and counsel | Not resolvable by an instrument. The vault's own verified set is the reference class: the ICO fined Reddit 14.47m pounds in February 2026 for inadequate age assurance and unlawful children's profiling, TikTok 12.7m, Snap 1.95m; Online Safety Act penalties reach the higher of 18m pounds or a tenth of qualifying worldwide revenue, with business-disruption orders reaching app stores and payment processors. | Priced at zero in `out/omissions.csv`, and named there rather than left out. The smallest penalty in that reference class exceeds every modelled cost line except content, and exceeds the whole seed round. |
| X10 | Does enough qualified examiner time exist to buy? | Content lead | Ask three examiner-supply agencies what monthly hours they can commit at a stated rate, before committing to the month-18 scope. A week of phone calls. | The model prices examiner time and never asks whether it exists. The month-18 scope needs tens of thousands of hours of qualified United Kingdom examiner time and `examiner_rate_gbp_hr` is perfectly elastic. If supply rather than price is binding, the content schedule is infeasible at any price and item C2 above is a feasibility question, not a cost one. |

---

## Items carried from the vault that this model touches

These are already open in docs/14. They are repeated here only where this
instrument changes what they are worth.

| Vault item | What this instrument adds |
|---|---|
| OI-5, age assurance cost | Now has a cost share, 1.2 per cent of the modelled base, and a break-even solve in `out/breakeven.csv`. The idea that it could dominate the cost structure is not supported; what it does is subtract from the acquisition budget, as docs/10 says. |
| OA-10, the price anchor | Now has a number on it: 29,107,825 dollars of terminal cash between the two states. |
| OA-21, payment across the summer | Now has a ratio: 1.24 rather than two, and it reaches two on 0.0 per cent of paths. |
| The docs/10 assumption that variable cost is small relative to price | Holds. Inference is 2.7 per cent of the modelled cost base, so the sensitivity row docs/10 flags as reversible does not reverse under these priors. |
| OI-7, which entity contracts with the parent | Determines the VAT treatment this model assumes. The model reads consumer prices as gross; a different contracting entity could change the rate but not the reading. |
