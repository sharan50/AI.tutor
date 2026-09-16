# AI.tutor: the economics, as an instrument rather than a forecast

**Seed 20260916. Run date 2026-09-16. 20000 paths, 60 monthly steps, United States dollars.**

Every number in this document was produced by a simulation whose every input is a
prior. Not one input is a measurement. Nothing here is a forecast, and the levels
are not evidence. What a simulation on priors is good for is the **ordering of
the levers**, and that ordering is what this document is for.

A figure re-derived from a different seed is a different number. The seed and the
date are quoted wherever a number appears for that reason.

---

## 1. The three things worth knowing

**One. The plan of record is not a seed-stage plan.** Sized at the eightieth
percentile of need, it requires 32.61 million dollars across the
horizon, against 17.69 million for a United Kingdom consumer business alone and
6.92 million for the go-to-market minimum: five GCSE subjects, one board,
one market, no institution channel. The first eighteen months of the plan of
record alone need 12.94 million.

**Two. Roughly two thirds of the cost base is committed before demand can say
anything about it.** Content, people and step costs together are
35.9, 15.2 plus 7.2, and 3.2 per cent of total modelled cost. Acquisition is
30.3 per cent. Inference, the cost docs/06 builds up so carefully, is
2.5 per cent. This is why **no single driver rescues the plan of record**:
every break-even solved in section 10 is unbracketed, because the money is spent
whether or not anyone buys.

**Three. Two different questions have two different answers, and conflating them
is the easiest mistake available here.** Whether the venture ever makes money is
decided by acquisition cost and the price anchor. How much capital it consumes
getting there is decided by the content build. The sensitivity ordering in
section 8 is different for the two targets and the difference is not noise.

---

## 2. What was modelled, and what the owner fixed

Taken from the vault and from the owner's instruction, not invented here.

| | |
|---|---|
| The idea | An AI tutor for United Kingdom secondary students, correctness-warranted against an examiner-validated clean-room item bank, in which the student chooses how they are taught by naming an educator whose style they recognise. It substitutes for part of private human tutoring. |
| The unit of work | A tutoring session covering one objective, with context bounded per D30. The commercial unit is the acquired household, tracked monthly. |
| Where the work is done | Bengaluru. Salaries quoted in rupees, inference in dollars. |
| Where the revenue is | United Kingdom first, then United States and India, then measured expansion across English-speaking curricula. |
| What humans still do | Examiner validation per item, safeguarding review, support, and field sales in the institution channel. |
| Horizon | 60 months from the month the seed closes. |
| Currency | United States dollars at fixed rates, at the owner's instruction. This is why checklist item 4 is not clean; see LIMITS.md. |
| Pricing | An examination-cycle plan billed monthly, with a sold session allowance and metered overage above it, capped. |

**The plan of record**, as the owner stated it: Algebra within GCSE Mathematics is
the minimum viable product and is not what goes to market. Go-to-market within six
months of the seed closing, carrying GCSE Mathematics, English and the sciences.
By month 18, every United Kingdom board across GCSE and A-level in those subjects,
plus pilots in India and the United States. After month 18, measured expansion
across English-speaking curricula, with maturity placed above expansion.

Go-to-market is set at month 6 and the seed is set to close in March 2027, so that
the launch lands in September, at the start of an academic year. That placement is
a decision, and section 12 shows what it is worth.

**One thing was changed from the stated plan and it should be argued with.** The
India pilot is modelled through institutions, not direct to parents. DPDP Rules
2025 section 9(3) prohibits tracking, behavioural monitoring and targeted
advertising directed at anyone under 18, the prohibition stands independent of
consent, and a parent cannot waive it; children's-data obligations bite around
May 2027, inside this horizon. The direct-to-parent version is modelled as a
variant, and it is worth -214,869 dollars of terminal cash over
five years. That is the whole prize for taking on a statutory prohibition.

---

## 3. The instrument

Three files, in this order.

`model.py` carries the drivers, the mechanisms and the month loop, behind section
markers. `harness.py` splits that file at its own markers, executes the pieces and
**refuses to proceed unless it rebuilds the published output CSVs character for
character**. The comparison is on the written text, not on in-memory floats,
because the CSV writer loses about one unit in the last place and an in-memory
comparison passes when it should fail.

**A gate that has never been shown to refuse is not a gate.** `python3 harness.py
--selftest` perturbs one field of the published file by one unit in its last
decimal place, confirms the harness refuses, restores the file and confirms it
verifies again. The result is written to `out/harness_selftest.txt`.

Everything downstream, without exception, runs through `harness.load()`. That is
what makes the sensitivity, the scenarios, the funding sizing and the break-even
solves run the published code rather than a restatement of it.

**Every mechanism that a variant adds must reproduce the base run exactly when it
is switched off, and every parameter a variant needs is drawn outside the
published random stream.** Four mechanisms are tested this way on every run: the
feedback loops, the app-store fee, sampled foreign exchange, and the creator
licence. All four reproduce the base character for character when off.

Because no draw happens inside the month loop, the streams cannot diverge between
scenarios. That is shown rather than asserted: `out/variants.csv` carries, for
every scenario, the rank correlation of per-path terminal cash against the base
and the mean absolute per-path change beside the change in the mean. Unmatched
paths would collapse the first and inflate the second. The tightest-coupled
scenario, the allowance enforced, holds a rank correlation of
0.9999 against the base, and the loosest, the software
anchor, 0.7948.

**Every driver is a prior, and the registry in `model.py` says so for each one.**
Where a range is anchored on something, the note says what. Where nothing anchors
it, the note says "prior". There is no third kind.

**Two scope responses were added because the comparators were not like for like.**
Platform engineering was a fixed ramp to twenty-two heads regardless of scope,
which charged a one-market, one-subject scenario for a team sized to run four
markets and an institution channel. It is now a floor plus heads per additional
live market and for running the institution channel at all. Running the other
way, the reachable pool was the same whether the product covered one subject or
eleven; it now scales sublinearly with subject breadth from the five-subject
reference the driver is defined at. Both are in `CHANGELOG.md` with what they
moved. Both are decisions with stated constants, not measurements.

---

## 4. Unit economics

| | USD |
|---|---|
| Gross consumer revenue over the horizon, mean of paths | 38,875,525 |
| Consumption tax inside it | 4,338,652 |
| Tax as a share of gross | 11.2 per cent |
| Net revenue, consumer and institution together | 34,708,038 |
| Institution channel share of net revenue | 0.49 per cent |
| Total cost | 45,865,389 |

**Prices are read as gross, that is, tax-inclusive**, which is what United Kingdom
consumer law requires a consumer-facing price to be. Net revenue is the gross
price divided by one plus the rate. Blended across markets that removes
11.2 per cent of gross; on the United Kingdom alone at
twenty per cent VAT it removes a sixth. Under the other reading, in which the
quoted price is net and tax is added on top, revenue would be higher by the whole
tax line: 4,338,652 dollars over the horizon.

### Contribution per household, two ways round

| | USD per active household month |
|---|---|
| Gross contribution: net revenue less inference, support, payment and hosting | 2,314,540.72 |
| All-in: the same thing net of engineering, content, overhead and compliance | -96,521,075.29 |
| The difference | -98,835,616.01 |

The first figure is a **gross margin**. Quoting it as the value of a customer,
which is the conventional thing to do, overstates by
-98,835,616.01 dollars a household-month. Both are published here so that neither
can be passed off as the other.

### Acquisition cost: the anchor is not the cost

| | USD per acquisition |
|---|---|
| The low-volume anchor, median of the driver | 32.26 |
| Effective cost in the final year, at the spend actually modelled | 39.33 |
| Effective over anchor | 1.22 times |

Channels saturate. The effective cost rises as the square-root-ish power of spend
over a sampled reference spend, and again as the reachable pool is penetrated.
Quoting the anchor as the cost at scale would understate by a factor of
1.22. The effective cost is published by month in `out/por_monthly.csv`
as `cac_effective_blended_mean`, and split from the non-creator channel beside it.

**Lifetime value against cost per acquisition in the final year.** Gross lifetime
value averages 7,606,691.42 dollars against an effective acquisition cost of
39.33, a ratio of 193,413.55. On 4.5 per cent of
individual paths that ratio is below one: the business is buying households for
more than they are worth, in the final year, on that share of paths. The
acquisition budget is capped at 0.75 times lifetime value, which is what keeps
that share as low as it is.

### Retained months, and the Year 10 result from docs/10

docs/10 argues that a Year 10 household can afford roughly twice the acquisition
cost of a Year 11 household, because the calendar gives it twice the retained
months, and marks the assumption that it pays through the summer as OA-21.

The code does not assert the ratio. It produces one, from a summer lapse
probability sampled between 0.20 and 0.85 and a progression
rate sampled between 0.65 and 0.98. Running the segment mix pinned to all-examination-year and then to
all-pre-examination-year, on the same random numbers:

| | Months per acquisition |
|---|---|
| Examination year | 2.96 |
| Pre-examination year | 3.66 |
| A-level | 4.06 |
| **Ratio, pre-examination to examination** | **1.24** |

The ratio the code produces is 1.24, not two. And it reaches two or
better on only 0.0 per cent of paths. The shape of the docs/10 result
survives, the magnitude does not, and the document's own caveat is the reason:
the summer is where it goes.

### The allowance is sold but not enforced

23.6 per cent of active households exceed the session allowance being
sold to them, weighted by household-months.

The allowance is not enforced. Sessions above it are delivered and cost money, and
they are billed only up to two and a half times the allowance. So the omission
sits on one side only and its sign is known rather than assumed away: above the
billing cap, cost runs and revenue does not. Enforcing the allowance instead is
worth
98,661 dollars of terminal cash: real, small, and now measured
rather than argued about.

---

## 5. The cost split

Mean over paths of each line summed over the horizon, as a share of total
modelled cost.

| Line | USD | Share |
|---|---|---|
| Content: examiner validation and authoring | 16,461,584 | 35.9% |
| Acquisition spend | 13,893,077 | 30.3% |
| People, Bengaluru | 6,969,273 | 15.2% |
| People, United Kingdom | 3,286,454 | 7.2% |
| Payment processing | 1,413,464 | 3.1% |
| Step costs: entities, counsel, certification, premises, representative | 1,452,033 | 3.2% |
| Inference | 1,128,418 | 2.5% |
| Age assurance | 522,936 | 1.1% |
| Support | 348,556 | 0.8% |
| Retrieval, storage, telemetry | 324,171 | 0.7% |
| Institution onboarding, per school | 65,424 | 0.1% |
| App store fees | 0 | 0.0% |

Three readings, each of which contradicts something in the vault or in the usual
telling.

**Content is the largest line, not acquisition.** docs/10 is right that content
does not enter the payback ratio, because it does not scale with learners. It is
nonetheless the largest single call on cash in a plan that builds this much of it.
On 85.4 per cent of individual paths content exceeds acquisition, and on
65.6 per cent it exceeds both acquisition and people, so this is not an
artefact of averaging.

**The load-bearing assumption in docs/10 holds.** That document assumes variable
cost per month is small relative to price, and says plainly that if it is not, the
sensitivity ordering reverses and cost engineering becomes the priority. Inference
is 2.5 per cent of total cost under these priors. The row does not reverse.

**Age assurance, the condition the route decision turns on, is
1.1 per cent of cost.** That is not an argument that condition C2 does not
matter. C2 is a threshold test against the first month of contribution, not a
share of the cost base, and section 10 gives its break-even. But the idea that
verification could dominate the cost structure is not supported: what it does is
subtract from the acquisition budget, exactly as docs/10 says.

---

## 6. The trajectory, and what the bands actually are

Bands are built by **ranking whole paths on terminal cumulative cash and averaging
within a band of ranks**, not by blending unrelated percentiles. The central band
is ranks 40 to 60 per cent, the low band 10 to 30, the high band 70 to 90.

That construction has a property a reader will not assume, so it is measured and
published. The central band line sits at the 49.7 percentile of the real
per-path distribution of cumulative cash at the end of the horizon, and between
the 49.7 and 56.3 percentiles across the months from go-to-market
onward. It moves between scenarios as well: on the software-anchored scenario it
ends at 50.0, and on the tutoring-anchored one at
50.0.

**Cross-scenario comparison of band lines is therefore invalid unless the
placement is quoted with them.** Every band line in `out/por_monthly.csv` carries
a `_bandlow`, `_bandcentral` or `_bandhigh` suffix; every mean over all paths
carries `_mean`; and `check_suffix_discipline()` in `model.py` refuses a header in
which the two could collide. A `_mean` figure and a `_band` figure must never be
divided by one another.

---

## 7. The trough, honestly

**The minimum of an average is shallower than the average of minimums**, and the
headline understates.

| | USD |
|---|---|
| Minimum of the mean cumulative cash line, the headline figure | -13,528,468 at month 43 |
| Mean of each path's own minimum | -23,665,988 |
| Ratio | 0.5716 |
| **The headline is shallower by** | **42.8 per cent** |

The per-path distribution beside it: tenth percentile -38,384,994, ninetieth
-8,066,912, mean month of the trough 54.0. The averaged line reaches its
low at month 43; individual paths reach theirs, on average, at month
54.0. Planning to the averaged line plans to a trough that is
42.8 per cent shallower and later than the one a given path actually meets.

### The sustained bad run

Independent monthly shocks would remove exactly the failure mode that ends
companies. The demand shock here is AR(1) with persistence sampled between
0.45 and 0.95, median 0.70. The longest run of consecutive months with demand at
or below 0.80 averages 5.8 months and reaches 13.0 at the
ninetieth percentile. 36.9 per cent of paths contain a run of six or more
such months and 12.1 per cent a run of twelve or more.

---

## 8. The sensitivity ordering

First-order Sobol indices, estimated by sorting on driver rank, cutting into forty
equal-count bins and applying the one-way analysis-of-variance correction for
within-bin noise. Without the correction every driver scores about the bin count
over the path count and a driver that does nothing looks like it does something.

**Read the sum before reading the ordering.** First-order indices sum to
0.138 on terminal cash, 0.772 on its rank transform,
0.742 on peak funding and 0.507 on whether a path
reaches profitability. **The model is interaction-dominated.** A tornado read on
its own would mislead, and that is why the two-way grid in section 9 is here.

### Whether the venture ever makes money

Target: does a path run three consecutive cash-positive months inside the horizon.

| Rank | Driver | First-order index |
|---|---|---|
| 1 | cac_anchor_usd | 0.218 |
| 2 | anchor_u | 0.158 |
| 3 | cac_ref_spend_usd | 0.046 |
| 4 | sat_kappa | 0.018 |
| 5 | churn_base | 0.012 |

### How much capital it takes

Target: the peak funding requirement.

| Rank | Driver | First-order index |
|---|---|---|
| 1 | items_per_unit | 0.165 |
| 2 | cac_anchor_usd | 0.085 |
| 3 | minutes_per_item | 0.082 |
| 4 | writer_gbp_item | 0.082 |
| 5 | anchor_u | 0.080 |
| 6 | board_reuse | 0.060 |
| 7 | examiner_rate_gbp_hr | 0.043 |

**The two orderings are different and the difference is the finding.** Acquisition
cost and the price-anchor regime decide whether. Item count per subject bank,
authoring cost per item, validation minutes per item, reuse across boards and the
examiner rate decide how much. 5 of the top seven drivers on
capital are content-cost drivers, against 0 in the top three on
whether the venture ever makes money. Both counts are computed in `figures.py`
from `out/sobol.csv` rather than counted by eye.

The practical reading: **work on acquisition and the price anchor to make the
business exist; work on content cost to make it fundable.** They are different
programmes of work and this instrument says they are not substitutes.

### Pinned sweeps

Each driver pinned across the whole sample at its own fifth and ninety-fifth
percentile, with the pin applied after the draws so both runs share every random
number and the difference is that driver's alone.

| Driver pinned | Terminal cash at q5 | at q95 | Swing |
|---|---|---|---|
| items_per_unit | -3,166,721 | -19,107,704 | 15,940,982 |
| cac_anchor_usd | 39,866,217 | -27,445,338 | 67,311,555 |
| anchor_u | 4,111,600 | -26,658,200 | 30,769,800 |
| writer_gbp_item | -5,673,253 | -16,594,199 | 10,920,946 |
| minutes_per_item | -5,371,759 | -16,944,680 | 11,572,921 |
| board_reuse | -16,020,599 | -6,327,771 | 9,692,829 |

The `anchor_u` row is degenerate and is reported as such: that driver is a uniform
compared against a threshold, so pinning it is not a sweep but a switch between
two regimes. Its two values are the whole of its effect, and section 9 restates it
as the scenario pair it actually is.

---

## 9. The two-way grid, and the scenarios

### The grid

The two drivers owning the most variance on the capital target, crossed five by
five, each cell a full re-run on the same random numbers.

`out/twoway_grid.csv` holds items_per_unit against cac_anchor_usd. Terminal cash
across the grid runs from -34,437,778 to 33,284,894, a range of
67,722,672.

The shape matters more than the range. Moving one step down the content axis costs
roughly the same amount wherever you are on the acquisition axis: content is close
to additive. Moving one step along the acquisition axis, from its tenth to its
thirtieth percentile, changes terminal cash by tens of millions and changes the
share of paths reaching profitability far more than the whole content axis does.
**Acquisition sets the level; content sets the slope.**

### The scenarios

All share the same drivers and the same random stream, and differ only in the
switches named. Every scenario that opens a market or a channel is charged for it.

| Scenario | Terminal cash, mean | Against the plan of record |
|---|---|---|
| Plan of record | -11,157,351 | |
| Condition C1 passes: tutoring anchor on every path | 4,111,600 | 15,268,951 |
| Condition C1 fails: software anchor on every path | -26,658,200 | -15,500,849 |
| Without the institution channel | -5,721,384 | 5,435,967 |
| United Kingdom consumer only | -7,964,475 | 3,192,876 |
| With driver dependence imposed | -6,678,404 | 4,478,947 |
| With the feedback loops switched on | -19,477,538 | -8,320,187 |
| Dependence and feedback together | -17,301,678 | -6,144,327 |
| Creators want money | -13,361,717 | -2,204,366 |
| A share of billing through an app store | -13,717,066 | -2,559,715 |
| Go-to-market three months later | -12,650,999 | -1,493,648 |
| Go-to-market six months later | -11,951,223 | -793,872 |
| Foreign exchange sampled rather than fixed | -11,064,281 | 93,070 |
| India opened direct to parents | -11,372,220 | -214,869 |
| The allowance enforced | -11,058,690 | 98,661 |

Five readings.

**The price anchor is worth -15,500,849 dollars between its two states**, and it is a
landing page and a few days of spend to test. It is condition C1 in docs/09 and
nothing else in this instrument comes close to it on cost of information.

**The institution channel destroys 5,435,967 dollars.** Field sales
salaries, per-school onboarding, a security certification and its annual renewal,
against contracts worth 0.49 per cent of net revenue. On these priors Route B
as scoped here does not pay for itself inside the horizon. docs/09's argument for
Route B was never that it pays sooner; it was that it produces the outcome
evidence that is the only durable moat, and this instrument does not value
evidence. That is a limit of the instrument, not a refutation of the argument.

**The feedback loops cost -8,320,187 dollars.** A higher price costs
retention, expanding faster costs quality and quality costs retention, and a higher
automation ceiling costs engineering heads. The base model has none of these and
is therefore optimistic by that amount. Every lever in section 8 should be read
net of its own penalty, and the section 11 ranking is stated on the feedback-on
figures for that reason.

**Imposed dependence is worth 4,478,947 dollars, in the favourable
direction.** Ten rank correlations were imposed by Iman-Conover reordering, which
preserves every marginal exactly: 10 pairs, worst achieved-against-target
error 0.016, and every marginal verified unchanged in
`out/imanconover_check.csv`. The direction is not a comfort: it means the base run
is conservative on dependence and optimistic on feedback, and the two do not
cancel. Together they are -6,144,327.

**Launching later is not monotonic, and the reason is a defect in the comparator
rather than a fact about the calendar.** Three months late costs
-1,493,648; six months late costs -793,872, which is less.

That is not a finding about examination timing. `launch_shift` moves the content
schedule along with the market openings, so a six-month shift pushes the
month-54 content step past the end of the horizon and the run simply never pays
for it. Content cost falls by -1,787,131 dollars against the plan of
record at a six-month shift, against -223,133 at three months.
**The saving is the horizon boundary, not the season.** The two launch scenarios
are therefore usable for "later is worse" and not for comparing one delay against
another, and no calendar conclusion should be drawn from them.

---

## 10. What the break-evens say

**On the plan of record, there are none.** Ten questions were solved by bisection
on a pinned driver, each across that driver's entire prior range, against three
targets: the median path ending the horizon whole, half of paths reaching
profitability, and the plan needing no more than ten million dollars at the
eightieth percentile. **Every one is unbracketed.** No value of the reachable
pool, the acquisition anchor, age assurance cost, validation minutes, item count,
sessions per household, churn or price, anywhere in its prior range, reaches any
of those targets on the plan of record.

That is not a modelling failure; it is the answer. Content, people and step costs
are 35.9, 15.2, 7.2 and 3.2 per cent of cost and none of
them depends on whether a single household buys. A driver that acts only on demand
cannot move a cost base that demand does not touch.

**The break-evens are therefore solved again on a scope that can be rescued**: the
go-to-market minimum, being five GCSE subjects at one board in the United Kingdom
with no institution channel. Those results are in `out/breakeven.csv`, and the
same file records the plan-of-record answer as "not bracketed by the prior range",
which is the finding rather than a gap.

**The instruction this yields is about scope, not about any parameter.** The lever
that moves this plan is how much of it is attempted before the first evidence
arrives, and that lever belongs to the owner rather than to the model.

---

## 11. The funding requirement

Rounds sized at the eightieth percentile of the need inside each window, plus six
months of that window's own burn as buffer. The peak funding requirement is
computed without any injection, as the deepest point of cumulative operating cash
flow, so the sizing is not circular.

| Scope | Seed, to month 18 | Series A, 18 to 36 | Series B, 36 to 60 | Whole horizon, p80 |
|---|---|---|---|---|
| Plan of record | 12,935,477 | 13,148,354 | 16,776,035 | 32,611,126 |
| United Kingdom consumer only | 8,534,321 | 5,570,173 | 9,179,522 | 17,691,569 |
| Go-to-market minimum: five subjects, one board | 3,422,985 | 2,391,692 | 3,430,937 | 6,918,907 |
| One subject, one board | 2,121,725 | 2,298,599 | 3,323,897 | 5,901,874 |

**The round is sized on the plan of record, and the base case is stated beside
it.** They differ by enough that sizing on the base case would underfund the plan
the owner has actually described: 32.61 million against
17.69 million across the horizon.

87.7 per cent of individual paths need more than ten million dollars.

### The staging does not match the decisions

`out/funding_commitments.csv` sets each milestone's landing month beside the month
its spend *starts*, because content is built over the six months before it is
delivered and an entity is stood up before a market opens.

Every commitment through month 18, including the United States and India entities,
foreign counsel, the information security certification, A-level content and the
second and third United Kingdom boards, has its spend starting inside the seed
window. The Series A does not buy them; it refinances decisions the seed already
committed to. Two commitments land in the Series A window with spend starting
before it opens: all four United Kingdom boards live at month 18, whose content
build starts at month 12, and the rest-of-English-speaking market at month 24,
whose build starts at month 18.

**A round of 12,935,477 dollars is not a seed round.** Calling it one and
then discovering at month 18 that the Series A is paying for choices made at month
12 is the failure mode that staging is supposed to prevent.

---

## 12. The decisions that are yours, not the model's

Ranked by how much each moves the answer. Every figure is on the feedback-on
scenario where a comparable one exists, because the levers should be read net of
their own penalties.

**1. How much scope to attempt before the first evidence arrives.** The plan of
record needs 32,611,126 against 6,918,907 for the
go-to-market minimum. This is the largest single number in this document and it is
entirely yours: the model has no view on how much ambition is correct, only on
what each amount costs. Nothing else on this list comes close.

**2. Whether to test the price anchor before building anything.** Worth
-15,500,849 between its two states, and it costs a landing page. It is
already condition C1 in docs/09 and already milestone M1 in docs/11. The decision
is whether you will actually stop if it fails.

**3. Whether to run the institution channel at all inside this horizon.** Costs
5,435,967 here, and buys outcome evidence that this instrument cannot
value. docs/09 makes the case for it honestly and this model is not equipped to
answer it. You are.

**4. What the session allowance should be, and whether to enforce it.** The
allowance is set at 16 sessions a month in `model.py` as a decision, and
23.6 per cent of households exceed it. Enforcing is worth
98,661. The number is small; the commercial posture it implies,
toward the struggling learner the product exists for, is not.

**5. Whether to bill through an app store.** Costs -2,559,715 and buys
distribution the model does not credit. docs/04 identifies app stores and payment
processors as the real chokepoint, which is an argument for a second relationship
rather than for or against the fee.

**6. Whether India is worth a statutory prohibition.** Direct to parents is worth
-214,869 over five years against DPDP section 9(3). The institution
route in India carries no such conflict and is what the plan of record models.

**7. Where to launch in the calendar.** Delay costs money: three months late is
-1,493,648. The instrument cannot tell you which month is best,
because its delay scenarios move the content schedule with the launch and so
collide with the end of the horizon; see section 9. What the calendar mechanics
in the model do say is that an examination-year household acquired after
Christmas has months rather than a year, and the model's own retained-month
figures in section 4 are the size of that.

**8. Whether to fix the exchange rate.** You instructed fixed rates. Sampling them
moves the mean by 93,070, which is small; what it changes is the
width of the distribution, not its centre. See LIMITS.md.

---

## 13. Where to look

| File | What it holds |
|---|---|
| `model.py` | Drivers, mechanisms, month loop. Every driver's note says what anchors its range, or that nothing does. |
| `harness.py` | The character-for-character gate. Everything downstream runs through it. |
| `out/por_monthly.csv` | The monthly output of the published run: 60 rows, every series as a mean, three percentiles and three band lines. |
| `out/por_paths.csv` | 20000 rows: every per-path outcome and every driver value. |
| `out/sobol.csv`, `out/tornado.csv` | The full sensitivity, every driver against four targets. |
| `out/pinned_sweeps.csv`, `out/twoway_grid.csv` | The sweeps and the grid. |
| `out/variants.csv`, `out/variants_bands.csv` | Every scenario, and where each one's band lines actually sit. |
| `out/imanconover_check.csv` | Target against achieved rank correlation, and proof each marginal is unchanged. |
| `out/breakeven.csv` | The break-even solves, including the unbracketed ones. |
| `out/funding.csv`, `out/funding_commitments.csv` | Round sizing, and the staging test. |
| `out/cohorts.csv`, `out/omissions.csv` | The checklist measurements and the priced absent cost lines. |
| `out/figures.csv` | Every figure quoted anywhere, with its source file and its derivation. |
| `LIMITS.md`, `OPEN_ITEMS.md`, `CHANGELOG.md` | What is not clean, what is unanswered, and what moved. |

`verify.py` re-derives the core figures from the raw CSVs by a different code path
from `figures.py`, checks four accounting identities down the whole monthly file,
and then scrapes every number in this document and matches it against a figure on
disk. Run it. It is the only reason to believe any of the above.
