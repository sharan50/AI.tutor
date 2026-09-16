# Open items

**Seed 20260916, run date 2026-09-16.**

Every question this model does not answer, with one owner and one trigger each.

**This file is the one most likely to be forwarded on its own, so it carries the
same warning the write-up opens with.** Every dollar figure below comes from a
simulation whose every input is a prior. Not one input is a measurement. Nothing
here is a forecast, the levels are not evidence, and the headline terminal-cash
figures carry a sampling interval of about
1,215,678 before any of the priors are argued
with. What the numbers are for is ranking these questions against each other.

**A trigger that cannot produce the quantity is worse than no trigger, because it
looks like a control.** Each row below names an instrument that can actually
produce the number. Where the vault already schedules an instrument that cannot,
the row says so.

**Grouped** by which of section 8's two targets they move: the E items move
whether the venture ever makes money, the C items move how much capital it
consumes getting there. Within a group the rows are *not* strictly ordered by
first-order index, and two earlier drafts claimed orderings that the files do
not support. **E2, the acquisition anchor, leads its group on every measure in
the directory**: first-order index on terminal cash
(0.0569 against
0.0298), on the profitability target
(0.2112 against
0.1693), and on the pinned sweep
(60,938,805 against
29,766,439). E1 is first in this table because it is by
far the cheapest of the two to resolve — a landing page against thirty measured
acquisitions — not because it moves more. **The rows are ordered by cost of
information, and that is the only ordering claimed for them.** Section 8 of the
write-up gives the indices themselves and section 12 gives the caution that the
ordering moves with the statistic you rank on.

---

## The ones that decide whether there is a business

| # | Question | Owner | Trigger that can actually produce it | What it moves |
|---|---|---|---|---|
| E1 | Do parents anchor an AI tutoring subscription against the tutoring rate or against software prices? | Owner | A landing page running a tutoring-anchored price point against a software-anchored one, compared on revenue per visitor. Days, small spend, no product. This is condition C1 in docs/09 and milestone M1 in docs/11, and it is adequate to the quantity. | 29,766,439 dollars of terminal cash between the two states, and 4,342,151 of peak funding at the eightieth percentile. That spread is the largest single dollar figure in this table; it is a spread between two regimes rather than a driver's first-order index, and on the index E2 leads. |
| E2 | What does it cost to acquire a household, at the spend actually planned rather than at low volume? | Owner | Thirty measured acquisitions through one named channel at a stated monthly spend, reported as spend divided by acquisitions, split creator-led and not, then repeated at three times the spend to measure the saturation exponent rather than assume it. One channel test at two spend levels. **It does not settle the exponent, it narrows it.** At thirty acquisitions a cell the sampling error on each cost per acquisition is about a fifth, which puts a standard error of roughly 0.23 on the exponent against a prior range of width 0.68 — a third off the range, not a measurement. Say so when the result arrives, or it will be treated as one. | First-ranked driver on whether a path ever reaches profitability, first-order index 0.211. |
| E3 | How many sessions does a household actually use in a month? | Owner | Thirty households instrumented for one month. docs/11's M4 touches it, through sessions per learner per fourteen days as a secondary metric, and M4 already needs a signed creator and a built product; M5 is where it is measured properly and M5 needs a first cohort. **Nothing in the roadmap produces it cheaply or early.** It appears on both sides of the unit economics and the session allowance cannot be set without it. This is the instrument gap in checklist item 22. | Sets whether 23.6 per cent of households exceed the allowance, or almost none do. |
| E4 | What does age assurance cost per verified adult, and how many checks does one paying household take? | Owner | Three quotes from certified providers gives the **price**, in three phone calls, and is condition C2 in docs/09. It does **not** give the second half, which is the number of checks per acquired household: the model bills exactly one, and `out/omissions.csv` prices the correction at two to five times the modelled line, making it the largest priced omission with no route to being measured. That needs the funnel instrumented once the age-assurance step exists — checks started over households acquired — which is a counter, not a study, but it cannot happen before the product does. A round-four review found this half had no owner and no trigger anywhere. | Age assurance is 1.0 per cent of the modelled cost base. It also subtracts from the acquisition budget, but not pound for pound, which is what an earlier draft said: a dollar of verification cost takes a dollar off the lifetime-value estimate, the budget cap is 0.75 of that estimate, and the cap is then inverted through the saturation exponent, so the effect on spend is neither linear nor one for one — and it is nil on any month where the percentage-of-revenue rule binds before the cap does. |
| E5 | How many reachable households are there in the United Kingdom? | Owner | **The trigger this row used to name cannot produce this quantity, and a round-four review was right about that.** Two weeks of paid search reporting qualified visits per pound and trial starts measures cost per acquisition at low volume, which is E2's quantity, not an asymptote. `pool_uk` is the ceiling on the standing book and the denominator of the saturation term; no two-week test at one spend level can see either. What can: a paid-search run at **three separated spend levels** held long enough for the cost per acquisition to bend, which identifies the saturation curve and its asymptote together, plus a census-based frame on the objective granularity the item bank already uses. Weeks and real money, not days and a small spend. Until then this stays a prior. | Sampled across a thirtyfold range. Its effect is muted in this model because the acquisition budget cap moves with it, and that muting is a model property rather than a fact. |

---

## The ones that decide how much capital it takes

| # | Question | Owner | Trigger that can actually produce it | What it moves |
|---|---|---|---|---|
| C1 | How many items does a full subject bank need at one level for one board? | Content lead | Decompose one DfE subject content document into objectives and count what the ten-items-per-objective rule implies. An afternoon. docs/03 already flags that its own 60-objective figure is a planning number, not a count. **The same stratification objection checklist item 23 raises against C2's pilot applies here and was not stated until round four**: this is one subject, one level, one board, and the cost base applies the answer across up to eleven subjects, two levels and four boards. Do two subjects at different levels, not one, or the answer is a count times an assumption presented as a count. | First-ranked driver on the capital requirement, first-order index 0.157. Pinned across its range it swings terminal cash by 13,525,563. |
| C2 | How many minutes does examiner validation take per item, and what is the contract rate? | Content lead | docs/03's timed pilot, **stratified**: not twenty items of one kind in one strand, but a sample across subject, item kind and difficulty, because the cost base extrapolates across up to eleven subjects, two levels and four boards. See checklist item 23. A few hundred pounds either way. | Pinned across its range, 9,787,530 of terminal cash. |
| C3 | What does it cost to author an item, as against validating it? | Content lead | The same pilot, with authoring timed separately. It is a distinct driver and ranks 4 on the capital target, against rank 5 for validation minutes. | Pinned across its range, 9,296,821. |
| C4 | How much of a subject bank carries across to a second United Kingdom board? | Content lead | Build one strand to two board specifications and count what changed. One strand, not one subject. | Pinned across its range, 8,824,276. It is the term the whole expansion case rests on and the model deliberately does not let it be near one. |
| C5 | How much carries across to a foreign curriculum? | Content lead | The same exercise against one United States or Indian specification. | Rank 10 driver on the capital target. Decides whether the month-18 international ambition is an extension or a rebuild. |

---

## The ones the model cannot answer at all

| # | Question | Owner | Trigger that can actually produce it | Why the model is silent |
|---|---|---|---|---|
| X1 | What is outcome evidence worth? | Owner | A school pilot with a comparison group and a common assessment, which is a year and a sales motion. docs/09 argues it is the only durable moat. | The instrument charges the institution channel 2,248,602 dollars and credits it nothing for evidence. That figure is a lower bound on Route B's worth, not an estimate of it. |
| X2 | What does a creator charge to license name and likeness? | Owner | Ask three. A conversation each, before any contract. D5 asserts a one-page agreement; nothing establishes its price. | The published run charges zero. Priced at -2,088,444 dollars in the `por_creator_fees` scenario. |
| X3 | Will a competitor move on the United Kingdom curriculum specifically? | Owner | Not resolvable by an instrument. Watch what Google, OpenAI and Oak National Academy ship. | No competitive response of any kind is modelled. |
| X4 | Does the refusal behaviour cost retention? | Product | Correlate gate-fire rate against second-session return from the first live week. docs/06 already instruments the gate-fire rate, so this is a join, not a new instrument. | Gate-fire rate enters cost only. Its retention effect is in the feedback scenario as part of a bundle, not separately. |
| X5 | **Does the Year 10 household pay through the summer?** | Owner | One cohort observed across one July and August. This is OA-21 in docs/10 and it is the **first** of the two retention questions, not the second. An earlier version of this table ranked it second, on a reading of the counterfactuals that had not differenced them against the base. | The larger of the two levers by a factor of 14: removing the summer entirely lifts the pre-to-examination retained-month ratio by 0.407, against 0.029 for flooring in-term churn. It still does not reach the two docs/10 reasons toward — it reaches 1.45 — which is the finding rather than the lever. |
| X5b | What is in-term churn, by year group? | Owner | The first cohort measured monthly across one examination cycle, split by year group and never blended. The same instrument answers both questions if it runs across a summer, so this is an ordering of what to look at in the result rather than of what to build. | The smaller lever on the Year 10 ratio, at 0.029 against the summer's 0.407, but it sets the retained-month **level** on which the whole lifetime-value calculation rests, and that level is a floor for the separate reason in LIMITS.md: retention is right-censored by the horizon. |
| X6 | Would an Indian direct-to-parent service be lawful at all? | Counsel | DPDP Rules 2025 section 9(3) and the Fourth Schedule educational-institution exemption, put to Indian counsel as a specific question about a digital-first platform. | The model prices the revenue at -3,044,881 dollars over five years. It cannot price a prohibition. |
| X7 | What happens under a correlated downturn? | Owner | Not resolvable in advance. | The shock acts on acquisition only. There is no regime in which demand, retention, vendor prices and the examiner labour market move together. |
| X8 | **May United Kingdom children's learner data be processed in Bengaluru at all?** | Counsel | docs/05 names it and marks it unconfirmed: an Indian controller processing United Kingdom children's data is a restricted transfer needing an international data transfer agreement or the United Kingdom addendum to standard clauses, plus a transfer risk assessment. Put it to counsel as a specific question about learner content and learner telemetry, separately. It is a question, not a build. | **This is the largest single unmodelled item by cash, and it does not reorder the answer.** Both halves of that sentence were wrong in earlier drafts and are now read off files. Bengaluru engineering is sampled at 14,000 to 45,000 United States dollars a head, against United Kingdom roles at 45,000 to 98,000 pounds, which at the fixed rate is 57,150 to 124,460 dollars. Forcing the learner path onshore is worth -8,243,774 dollars of terminal cash and moves people past content as the largest cost line. It is **not** the only unmodelled item that matters — the residual scenario is larger in the other direction, at 22,223,831 dollars — and it does **not** invert the sensitivity ordering: on `out/sobol.csv`'s `onshore_all` run, item count stays at rank 1 on the capital requirement and the United Kingdom salary driver reaches rank 7, outside the top three. |
| X9 | What is the probability and size of a regulatory penalty? | Owner and counsel | Not resolvable by an instrument. The vault's own verified set is the reference class: the ICO fined Reddit 14.47m pounds in February 2026 for inadequate age assurance and unlawful children's profiling, TikTok 12.7m, Snap 1.95m; Online Safety Act penalties reach the higher of 18m pounds or a tenth of qualifying worldwide revenue, with business-disruption orders reaching app stores and payment processors. | Priced at zero in `out/omissions.csv`, and named there rather than left out. The comparison is now computed in that file rather than asserted: at the fixed rate the **largest** penalty in the reference class, 14.47m pounds, is 18,376,900 dollars, which exceeds every modelled cost line including content at 13,965,826 and exceeds the seed round at 10,173,752. The **smallest**, 1.95m pounds or 2,476,500 dollars, exceeds neither: it is below content, below acquisition at 10,574,170 and below Bengaluru people at 6,448,536. Two earlier drafts stated the smallest as though it were the largest. |
| X10 | Does enough qualified examiner time exist to buy? | Content lead | Ask three examiner-supply agencies what monthly hours they can commit at a stated rate, before committing to the month-18 scope. A week of phone calls. | The model prices examiner time and never asks whether it exists. The month-18 United Kingdom scope is 18.7 full item-bank equivalents after board reuse, which at the median item count and validation minutes is about 22,779 hours of qualified United Kingdom examiner time, and `examiner_rate_gbp_hr` is perfectly elastic. An earlier draft counted the catalogue of forty units rather than the equivalents the model actually builds, and doubled the figure. If supply rather than price is binding, the content schedule is infeasible at any price and item C2 above is a feasibility question, not a cost one. |
| X11 | **When do the specifications this content is written to change?** | Content lead | Ask each awarding body for its published reform and reissue timetable, and count how much of the planned bank sits in subjects already scheduled for reform. A morning per board, and it is answerable today because the timetables are public. | The model builds an item bank once and never rebuilds it: `content_full_equivalents` only ever rises with time and nothing expires. On a five-year horizon that is wrong by construction. `out/omissions.csv` prices it at 837,950 to 2,513,849 dollars, being six to eighteen per cent of the modelled content spend, and that range is a prior on the rate of turnover rather than a measurement of it. It acts on the largest cost line in the model and on the driver the capital requirement is most sensitive to, which is why it is here rather than only in the omissions file. |
| X12 | **Is a salaried content head the same person as a contracted item writer?** | Content lead | Not a measurement: a decision about how the content function is staffed, taken once and written down. An afternoon with the content lead and the draft org chart. It is here rather than among the cost questions because the model cannot settle it and it changes a headline. | `units_per_content_head` charges a salaried head to "build and maintain" content units; `writer_gbp_item` charges an authoring cost per item for the same items. If a head manages contracted writers, both are real and content-driven cost is 43.0 per cent of the base rather than the 35.9 per cent the cost table's content row shows. If the head *is* the writer, 2,768,711 is charged twice — 7.1 per cent of the modelled base, larger than the whole step-cost line. The model publishes the decomposition and takes no view. |

---

## Items carried from the vault that this model touches

These are already open in docs/14. They are repeated here only where this
instrument changes what they are worth.

| Vault item | What this instrument adds |
|---|---|
| OI-5, age assurance cost | Now has a cost share, 1.0 per cent of the modelled base, and a break-even solve in `out/breakeven.csv`. The idea that it could dominate the cost structure is not supported; what it does is subtract from the acquisition budget, as docs/10 says. |
| OA-10, the price anchor | Now has a number on it: 29,766,439 dollars of terminal cash between the two states. |
| OA-21, payment across the summer | Now has a ratio: 1.04 rather than two, and it reaches two on 0.01 per cent of paths. It also now has a size: the summer is the larger of the two retention levers by a factor of 14, so docs/10's own caveat points at the right question. What it does **not** have is a route to two — removing the summer entirely reaches 1.45, and flooring in-term churn as well reaches 1.61. Nothing in the prior ranges recovers the figure docs/10 reasons toward. |
| The docs/10 assumption that variable cost is small relative to price | Holds. Inference is 2.7 per cent of the modelled cost base, so the sensitivity row docs/10 flags as reversible does not reverse under these priors. |
| OI-7, which entity contracts with the parent | Determines the VAT treatment this model assumes. The model reads consumer prices as gross; a different contracting entity could change the rate but not the reading. |
