# AI.tutor: the economics, as an instrument rather than a forecast

**Seed 20260916. Run date 2026-09-16. 20000 paths, 60 monthly steps, United States dollars.**

Every number in this document was produced by a simulation whose every input is a
prior. Not one input is a measurement. Nothing here is a forecast, and the levels
are not evidence. What a simulation on priors is good for is the **ordering of
the levers**, and that ordering is what this document is for.

**There is a tension in that sentence and it is better named than hidden.** The
orderings here are largely orderings of dollar spreads — the price anchor is
ranked above scope on terminal cash because its spread is larger. A ranking by
dollar spread is a use of levels, so "read the ordering, not the levels" cannot
be taken literally. What it means, and all it can mean, is: the **gaps** between
levers are informative where they are large relative to both the sampling error
and the priors' own width, and the **absolute** figures are not informative at
all. Where two levers rank within a few per cent of each other the instrument is
not ranking them, it is saying they are the same size, and this document says so
where that happens.

**And a ranking is only meaningful within one statistic.** Section 12's first
paragraph names the top two by putting a capital requirement beside a terminal
cash spread. Those two happen to be close in magnitude, which makes the
comparison look like one and it is not: a capital figure is bad when it is large
and a cash spread is good when it is large, and nothing converts one into the
other. Within each statistic separately the gap is wide — on capital scope leads
the price anchor by about five to one, on terminal cash the anchor leads scope by
about three to one — and those are the two orderings this instrument can support.
The cross-statistic comparison is not a third ordering; it is the absence of one.

A figure re-derived from a different seed is a different number, and until round
four this document never said by how much. On the headline, terminal cash at the
mean, the sampling error is
**533,244 at one standard error and
1,066,488 at two**, at this path count. Every
level in this document is rendered to the dollar because that is the precision
the file holds, not because it is known to the dollar; read roughly a million
either side of any terminal-cash figure before you read anything else about it.
The scenario deltas are far tighter than that because the scenarios share their
random numbers path by path, which is the point of the paired construction — but
one of them, the sampled foreign exchange rate, is **indistinguishable from zero
at this sample size**, and section 9 says so where it is tabulated.

The seed and the date are quoted wherever a number appears for the same reason.

**Two conventions are load-bearing, and the second is an absence.** Nothing in
this instrument is discounted: terminal cash, the peak funding requirement, every
break-even and the residual are undiscounted nominal sums over sixty months.

**Discounting cuts both ways here, and the obvious direction is the wrong one.**
The headline loss gets *smaller*: at twelve per cent a year the same net cash
line is worth -8,616,257 against the undiscounted
-10,049,080, and at twenty-five per cent
-7,484,668, because the largest negative months are the
late ones. The economics get *worse*: revenue arrives later than cost, so
discounted cost over discounted revenue rises from
1.36 undiscounted to
1.54 at twenty-five per cent. And
content's share of cost **rises** — from 36.5 per
cent to 40.4 — while acquisition's
falls to 23.4, because content is built
early and acquisition spend follows revenue. So discounting sharpens the ordering
this document reports rather than disturbing it, and it shrinks the residual
scenario, which sits entirely at month 60 and is the largest single item in the
scenario table. Nothing here is restated on a discounted basis; these figures are
published so that the omission has a size and a direction rather than only a
mention.

---

## 1. The three things worth knowing

**One. The plan of record is not a seed-stage plan.** Sized at the eightieth
percentile of the peak drawdown and with no buffer, it requires
28.24 million dollars across
the horizon, against 17.52
million for a United Kingdom consumer business alone and
6.73 million for the
go-to-market minimum: five GCSE subjects, one board, one market, no institution
channel. The first eighteen months of the plan of record alone need
10.21 million.

**None of the three numbers in that paragraph is a forecast, and this is the
paragraph most likely to be quoted as one.** Each carries the
1,066,488 sampling interval from the preamble
before anything else; each is undiscounted; and each is the output of priors, not
of measurement. A fourth-round review observed that the caveats in this document
live in sections 11 and 13 while section 1 is the part that gets pasted into a
deck, and it was right. The caveat is here now.

**And that headline is the smaller of the two funding numbers in this document,
which section 11 explains.** It assumes every round closes exactly as the last one runs
out. Staged with six months of buffer on each round, which is what raising
against a plan actually looks like, the same plan of record comes to
37.14 million. Quote whichever you like, but
quote which one.

**Two. About 65.3 per cent of the cost base does not respond to demand at all.** Content is 36.5 per cent of total modelled cost, people
16.9 per cent in Bengaluru plus 8.6 in the United Kingdom, and step
costs 3.3 per cent. Acquisition, which does depend on demand, is
26.5 per cent. Inference, the cost docs/06 builds up so carefully, is
2.5 per cent.

**"Committed" used to be the word in that sentence and it was the wrong one.**
This block is not spent early. 64.9 per
cent of it is spent after month 24, and
44.1 per cent after month 36, against a
go-to-market at month 6. Nothing about it is locked in
before the first customer arrives. What makes it demand-independent is that
`model.py` contains no rule that stops building when the plan is failing — the
content schedule, the headcount ramp and the step costs run to month 60 on every
path, including the ones with no book. That is a property of the instrument, not
of the business, and LIMITS.md states it under "the company never adapts". A real
company facing month 30 of these medians would cut the schedule; this one cannot,
and that is the single largest reason no break-even against a cash target
brackets.

"About" is doing work in that sentence too, and it is meant to. Part of the United
Kingdom people line is not demand-independent: the safeguarding rota steps at
3,000 and again at 25,000 active households, and those steps fire on
most paths. The overwhelming majority of the 65.3 per cent is fixed; a
slice of it is not, and LIMITS.md item 5 says which. This is why **no single driver gets the median path whole**: every break-even
solved in section 10 against a cash target is unbracketed, because the money is
spent whether or not anyone buys — not because it was committed early, but
because nothing in the model ever decides to stop. Four solves against the profitability target do
bracket, and section 10 gives them.

**Three. Two different questions have two different answers, and conflating them
is the easiest mistake available here.** Whether the venture ever makes money is
decided by acquisition cost and the price anchor. How much capital it consumes
getting there is decided by the content build. The sensitivity ordering in
section 8 is different for the two targets and the difference is not noise.

**And the second of those answers is a property of the plan of record rather
than of the business.** On the go-to-market minimum the capital ordering
rearranges: content drivers fall from
5 of the top seven
to 1, and a
Bengaluru salary driver comes second. "Content is the thing to get right" is
true of the plan of record and follows from the scope decision rather than
informing it. Section 8 gives both orderings side by side.

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

**One thing was changed from the stated plan, it should be argued with, and the
change went further than intended: the India pilot is not modelled at all.**

The reason for moving it off the direct-to-parent path is real. DPDP Rules 2025
section 9(3) prohibits tracking, behavioural monitoring and targeted advertising
directed at anyone under 18, the prohibition stands independent of consent, a
parent cannot waive it, and children's-data obligations bite around May 2027,
inside this horizon. D1 rejected India partly on this.

The intention was to model India through institutions instead. **That is not what
the instrument does.** The institution channel here is a single United
Kingdom-priced motion with no market index on its seat price, so the published run
has no India revenue, no India content build and no India entity: `active_in_mean`
is zero in all 60 rows of `out/por_monthly.csv`.

So the direct-to-parent variant, which **costs**
3,061,528 dollars of terminal cash on the
mean, is compared against **no India business at all** rather than against an
institutional one. It prices the prohibition, not the choice between the two
routes in. An Indian institution motion is neither modelled nor costed here, and
the plan of record should not be read as containing one.

---

## 3. The instrument

Three files, in this order: `model.py`, `harness.py`, and then everything else,
which in this directory means `sensitivity.py`, `variants.py`, `funding.py`,
`breakeven.py`, `rescue_grid.py`, `cohorts.py`, `omissions.py`, `params.py`,
`figures.py`, `render.py` and `verify.py`.

`model.py` carries the drivers, the mechanisms and the month loop, behind section
markers. `harness.py` splits that file at its own markers, executes the pieces and
**refuses to proceed unless it rebuilds the published output CSVs character for
character**. The comparison is on the written text, not on in-memory floats,
because the CSV writer loses about one unit in the last place and an in-memory
comparison passes when it should fail.

**A gate that has never been shown to refuse is not a gate.** `python3 harness.py
--selftest` perturbs one field of the published file by one unit in its last
decimal place, confirms the harness refuses, restores the file and confirms it
verifies again. It then does the same for the harness's second gate, the one
that forbids a random draw inside the month loop, by inserting a draw into a
copy of `model.py` and confirming the check rejects it. Both results are written
to `out/harness_selftest.txt`.

Every script that RUNS THE MODEL goes through `harness.load()`: the sensitivity,
the scenarios, the funding sizing, the break-even solves, the rescue grid, the
cohort counterfactuals, the omissions pricing and the parameter dump. That is what
makes them run the published code rather than a restatement of it.

Three scripts deliberately do not, and must not. `figures.py`, `render.py` and
`verify.py` read the CSVs and never import the model, so that a figure quoted in
the prose is checked against what was written to disk rather than against what the
code would produce if asked again.

**The gate covers two files out of the twenty-odd under `out/`, and that gap has
a name now.** `por_monthly.csv` and `por_paths.csv` are rebuilt and compared
character for character on every load. Nothing rebuilds `sobol.csv` or
`funding.csv` or the rest, and rebuilding them would mean re-running the whole
pipeline to check the whole pipeline. What can actually go wrong there is
staleness — a derived file generated against an older `model.py` and never
regenerated — so `harness.load()` records the SHA-256 of the `model.py` it ran
against into `out/provenance.csv`, and `verify.py` fails the whole run if any
generating script's recorded hash is not the current one. That is a weaker check
than the gate and is reported as the weaker thing it is.

**Every mechanism that a variant adds must reproduce the base run exactly when it
is switched off, and every parameter a variant needs is drawn outside the
published random stream.** 7 mechanisms are tested
this way on every run: the feedback loops, the app-store fee, sampled foreign
exchange, the creator licence, the onshoring switch, the terminal-value residual
and the pool reacquisition multiple. Every one reproduces the base character for
character when off, and every one changes the run when on, so none is wired up
and inert.

**Be precise about what that test proves, because an earlier draft of this
section let it read as more than it is.** It is a test of the random streams, not
of the mechanisms. Switching a mechanism off and getting the base run back
character for character shows that its parameters were drawn outside the
published stream and that the two runs are therefore comparable path by path. It
says nothing whatever about whether the mechanism is *right*. All four of the
mechanism defects round 2 found — a churn reference in the wrong place, an
allowance that truncated at the wrong number and kept the revenue anyway,
saturation measured on the wrong quantity, an onshoring switch that moved the
wrong people — passed this test on every run while they were wrong. The
switched-on half catches the narrower failure of a mechanism that does nothing at
all. Neither half is a substitute for reading the code, which is how all four
were actually found.

Because no draw happens inside the month loop, the streams cannot diverge between
scenarios. **That is now checked at the source rather than inferred from its
consequences.** The harness refuses to proceed if any draw call appears inside
the `LOOP` section of `model.py`, and `python3 harness.py --selftest` proves that
second gate refuses by inserting a draw into a copy of the file and confirming
it is rejected. `out/harness_selftest.txt` records both gates. An earlier draft
of this paragraph offered a rank correlation as the evidence, which is a
consequence of the fact rather than the fact.

The consequence is published too, and it is worth having: `out/variants.csv`
carries, for every scenario, the rank correlation of per-path terminal cash
against the base and the mean absolute per-path change beside the change in the
mean. Unmatched paths would collapse the first and inflate the second.

**The range has to be quoted in two parts, and an earlier draft of this section
quoted it wrong.** Across the scenarios that only flip a switch, the correlation
runs from 0.7589 at the loosest, which is gtm_minimum, to
1.0000 at the tightest. The two dependence scenarios sit far below that, at
0.2987 and above, **by construction and not by accident**: Iman-Conover
reordering changes which path holds which driver value, so path identity is
deliberately not preserved there. Those two are matched in their marginals, which
is what the reordering guarantees, and not in their paths. Every other comparison
in section 9 is matched path by path.

**Every driver is a prior, and the registry in `model.py` carries a note on each
one saying what, if anything, anchors its range.** Most notes end in the word
"prior" where nothing does. A handful describe the mechanism instead of the
anchor and should be read as "prior" too: an earlier draft claimed there was no
third kind of note, and `out/drivers.csv` shows there is.

**Two scope responses were added because the comparators were not like for like.**
Platform engineering was a fixed ramp to twenty-two heads regardless of scope,
which charged a one-market, one-subject scenario for a team sized to run the
three consumer markets the plan of record opens plus an institution channel. It is now a floor plus heads per additional
live market and for running the institution channel at all. Running the other
way, the reachable pool was the same whether the product covered one subject or
eleven; it now scales sublinearly with subject breadth from the five-subject
reference the driver is defined at. Both are in `CHANGELOG.md` with what they
moved. Both are decisions with stated constants, not measurements.

---

## 4. Unit economics

| | Value |
|---|---|
| Gross consumer revenue over the horizon, mean of paths, USD | 31,463,185 |
| Consumption tax inside it, USD | 3,441,120 |
| Tax as a share of gross, per cent | 10.9 |
| Net revenue, consumer and institution together, USD | 28,193,230 |
| Institution channel share of net revenue, per cent | 0.61 |
| Total cost, USD | 38,242,310 |

**Prices are read as gross, that is, tax-inclusive**, which is what United Kingdom
consumer law requires a consumer-facing price to be. Net revenue is the gross
price divided by one plus the rate. Blended across markets that removes
10.9 per cent of gross; on the United Kingdom alone at
twenty per cent VAT it removes a sixth. Under the other reading, in which the
quoted price is net and tax is added on top, revenue would be higher by the whole
tax line: 3,441,120 dollars over the horizon.

### Contribution per household, two ways round

Contribution per household month is a ratio, and its denominator collapses on
paths whose book has collapsed, so **the mean of the per-path ratio is not a
number** and is not published anywhere. Two defensible figures are given instead:
the pooled ratio, which is total contribution over total household-months across
every path and every month of the final year, and the median path's own ratio,
over the 99.6 per cent of paths that have a final year to speak of.

| | Pooled | Median path |
|---|---|---|
| Gross: net revenue less inference, support, payment, hosting and store fees | 31.55 | 27.87 |
| All-in: the same, net of engineering, content, overhead and compliance | 13.73 | -105.50 |

The first row is a **gross margin**. Quoting it as the value of a customer, which
is the conventional thing to do, overstates: pooled, the all-in figure is
17.82 dollars lower.

**The two columns disagree in sign on the all-in row, and that disagreement is
the finding.** Pooled, a household month contributes
13.73 dollars all-in. On the median path it consumes
105.50. The pooled figure is dominated by the few paths with
large books, which carry most of the household-months and spread the fixed costs
over them; the median path is small and the same fixed costs sit on top of it.
Neither is wrong. Quoting only the pooled one would describe a business that most
paths are not running.

### Acquisition cost: the anchor is not the cost

| | Value |
|---|---|
| The low-volume anchor, median of the driver, USD | 32.26 |
| Effective cost in the final year, pooled at the spend actually modelled, USD | 54.38 |
| Effective cost on the median path, USD | 31.47 |
| Pooled effective over anchor, a ratio | 1.69 |

Channels saturate. The effective cost rises as the square-root-ish power of spend
over a sampled reference spend, and again as the reachable pool is penetrated.
Quoting the anchor as the cost at scale would understate by a factor of
1.69 at the spend actually modelled. The median path is a different
story, at 31.47, because the median path never spends enough to
saturate anything; that is why the pooled figure is the one to plan against.

A related but different series is published by month in `out/por_monthly.csv` as
`cac_effective_blended_mean`, with the non-creator channel beside it. It is not
the same number: it excludes verification and the shock wastage, and it is a
mean of a within-month weighted cost. Do not read the two as one series.

One more caution on the pooled figure. Pooling weights by acquisitions, so it is
pulled by the largest paths, and LIMITS.md says plainly that the top of that
distribution is not believable. The pooled figure is the right basis for "what
does a household cost at the spend actually modelled" and it is still a
tail-influenced statistic; the median path's figure is beside it for that reason.

**Lifetime value against cost per acquisition in the final year.** Pooled gross
lifetime value is 117.41 dollars against a pooled effective acquisition
cost of 54.38, a ratio of 2.16. On
1.4 per cent of individual paths that ratio is below one: the business
is buying households for more than they are worth, in the final year, on that
share of paths. The acquisition budget is capped at 0.75 times lifetime value,
which is what keeps that share as low as it is.

Note the lifetime value in that ratio is the **gross** one. Against the all-in
contribution the ratio is very much worse: on
86.7 per cent of paths all-in
lifetime value is below the effective cost of acquiring the household, against
1.4 per cent on the gross basis. **Quote
both or neither.** The gross share is the one that reads as reassurance and it is
the one an earlier draft published alone, which is checklist item 16 committed
against a checklist item the document had marked clean. The all-in share is the
one that answers whether a household pays for the business that serves it, and
inside this horizon, on these priors, mostly it does not — which is the same
finding as the cost split in section 5, arrived at from the other end.

### Retained months, and the Year 10 result from docs/10

docs/10 argues that a Year 10 household can afford roughly twice the acquisition
cost of a Year 11 household, because the calendar gives it twice the retained
months, and marks the assumption that it pays through the summer as OA-21.

The code does not assert the ratio. It produces one, from a summer lapse
probability sampled between 0.20 and 0.85 and a progression
rate sampled between 0.65 and 0.98. Running the segment mix pinned to all-examination-year and then to
all-pre-examination-year, on the same random numbers:

| | Value |
|---|---|
| Examination year, months per acquisition | 3.63 |
| Pre-examination year, months per acquisition | 3.71 |
| A-level, months per acquisition | 4.09 |
| **Ratio, pre-examination to examination** | **1.02** |

The ratio the code produces is 1.02, not two. It reaches two or
better on 0.01 per cent of paths.

**Where does it go? Mostly to the summer, and two earlier drafts of this passage
got that backwards in opposite directions.** The first blamed the summer,
following docs/10's own caveat rather than the model. The second reversed it and
said in-term churn was the culprit — reading three counterfactual ratios off a
list without differencing any of them against the base. Differenced, and now
computed in `out/cohorts.csv` rather than read by eye:

| Counterfactual | Ratio | Lift against the sampled ratio |
|---|---|---|
| As sampled | 1.02 | — |
| Summer removed entirely: lapse pinned to zero, progression to one | 1.45 | **0.431** |
| In-term churn at the floor of its prior, summer left alone | 1.05 | 0.031 |
| Both | 1.62 | — |

**The summer is the larger lever by a factor of
14**, and the correct reading of these
four rows is narrower than either earlier draft:

1. docs/10's **shape** survives — the pre-examination cohort does retain longer —
   but its magnitude does not: the ratio is 1.02, not two, and it reaches two on
   0.01 per cent of paths.
2. **Neither lever alone recovers two, and neither do both together.** Removing
   the summer entirely still leaves 1.45;
   both pinned give 1.62. An
   earlier draft called that combination "the only one that recovers" docs/10's
   figure. It does not recover it. Nothing in the prior ranges does, which is the
   actual finding and is more interesting than either lever.
3. So docs/10's caveat about the summer points at the **right** question, and the
   open items are ordered accordingly: the summer is X5, in-term churn X5b.

There is a larger problem sitting underneath those numbers, and it is in
LIMITS.md: an examination-year household is retained 3.63 months in this
model, against a product sold as a cycle plan running to the last paper. The
average customer of a nine-month plan does not finish a cycle.

**That figure is a floor, not an estimate, and an earlier draft blamed the churn
prior for all of it.** Retained months are computed as active household months
over acquisitions across the whole horizon, and acquisitions are still ramping in
the last months of it, so a large share of them have their retention cut off by
the end of the window rather than by churn. A round-four review re-ran the model
with acquisition switched off after month 24, so every acquisition had at least
three years to run out, and the level rose by about a sixth. **The ratio between
year groups, which is what refutes docs/10, survives the correction intact** —
that was checked deliberately. The level does not, and every figure built on it,
including the lifetime-value ratio above, is a floor for the same reason.

### The allowance is sold but not enforced

23.6 per cent of active households exceed the session allowance being
sold to them. That is a household-month weighted share WITHIN each path, then a
plain mean across paths, so a path with a hundred households and a path with one
count equally in it.

The allowance is not enforced. Sessions above it are delivered and cost money, and
they are billed only up to 2.5 times the allowance. So the omission sits on
one side only and its sign is known rather than assumed away: above the billing
cap, cost runs and revenue does not.

**Enforcing the allowance instead destroys 4,468,821 dollars of terminal
cash on the mean.** The overage revenue lost is larger than the inference cost
saved, which is what you would expect once the numbers are on the same side of
the question, and is the opposite of what an earlier version of this scenario
said. That version truncated delivery at the billing cap rather than at the
allowance, so it cut off a level almost nobody reaches and kept the overage
revenue; see `CHANGELOG.md` 2.3.

Nothing here was measured: it is a difference between two simulations on invented
priors. What it is, is a question the instrument can now answer rather than argue
about, and it answers it the other way round.

---

## 5. The cost split

Mean over paths of each line summed over the horizon, as a share of total
modelled cost.

| Line | USD | Share |
|---|---|---|
| Content: examiner validation and authoring | 13,965,826 | 36.5% |
| Acquisition spend | 10,125,518 | 26.5% |
| People, Bengaluru | 6,448,536 | 16.9% |
| People, United Kingdom | 3,270,764 | 8.6% |
| Step costs: entities, counsel, certification, premises, representative | 1,271,517 | 3.3% |
| Payment processing | 1,152,288 | 3.0% |
| Inference | 967,319 | 2.5% |
| Age assurance | 394,063 | 1.0% |
| Support | 290,516 | 0.8% |
| Retrieval, storage, telemetry | 270,917 | 0.7% |
| Institution onboarding, per school | 85,044 | 0.2% |
| App store fees | 0 | 0.0% |

Four readings. The first three each contradict something in the vault or in the
usual telling; the fourth is about what the table leaves out.

**Content is the largest line, not acquisition — and the table above understates
it, because some of the content cost is filed under people.**
42.9 per cent of the Bengaluru
people row is salaried content heads, whose whole job is the content schedule:
2,768,711 over the horizon, or
7.2 per cent of the whole modelled
base. Content-driven cost is therefore
16,734,537, **43.8
per cent of the base rather than the 36.5 per cent
the content row shows.** A round-four review found this; the split is now emitted
by `model.py` as its own monthly series rather than reconstructed, and it is a
decomposition of the people line, never added to any total.

docs/10 is right that content does not enter the payback ratio, because it does
not scale with learners. It is nonetheless the largest single call on cash in a
plan that builds this much of it. On
84.9 per cent of individual paths the
contracted content line alone exceeds acquisition, and on
60.2 per cent it exceeds both acquisition
and people, so this is not an artefact of averaging. Those two shares are
computed on the contracted line, so they are lower bounds once the heads are
counted.

**And there is an unresolved question inside that number, which is the honest
finding rather than the figure.** `units_per_content_head`'s own note says a
content head "builds and maintains" content units; `writer_gbp_item` charges an
authoring cost for the same items. Either the salaried head manages a contracted
writer, in which case both are real, or the two are the same work charged twice,
in which case 2,768,711 is a double count
worth 7.2 per cent of the base.
Nothing in `model.py`, in the vault or in this document distinguishes them.
**Nothing here decides it, because it is not the model's to decide** — it is a
question about how the content function is actually staffed, and it is open item
X12.

**The load-bearing assumption in docs/10 holds on the median path and fails on
about one path in sixteen, and an earlier draft answered it with the wrong
denominator.** That document assumes variable cost per month is small **relative
to price**, and says plainly that if it is not, the sensitivity ordering reverses
and cost engineering becomes the priority. This section used to answer it with
inference over **total cost** — a denominator dominated by the content build,
which has nothing to do with the row being tested. Against the denominator the
claim actually needs:

| | median path | p90 of paths |
|---|---|---|
| Inference over gross consumer revenue | 4.3% | — |
| All variable cost over gross consumer revenue | 12.6% | 39.8% |

Pooled, inference is 3.07 per cent of
gross consumer revenue. But **variable cost exceeds half of revenue on
7.3 per cent of live paths and
exceeds revenue outright on 3.7 per
cent**, which is where docs/10 says its row reverses. So the row does not reverse
on the plan as a whole and it does reverse on a minority of paths, and the honest
statement is the second one as well as the first. The mean of the per-path ratio
is unusable — its denominator collapses on paths whose book collapsed — which is
the same trap this document names correctly for contribution per household and
missed here until round four.

**Age assurance, the condition the route decision turns on, is
1.0 per cent of cost.** That is not an argument that condition C2 does not
matter. C2 is a threshold test against the first month of contribution, not a
share of the cost base, and section 10 gives its break-even. But the idea that
verification could dominate the cost structure is not supported: what it does is
subtract from the acquisition budget, roughly as docs/10 says — not pound for
pound, and the mechanism is set out in E4 of OPEN_ITEMS.md.

**And a fourth reading, which is about the table rather than in it.** Every share
above is a share of the cost the model *carries*.
`out/omissions.csv` names 17 cost lines the model does
not carry and prices them at
2,962,891 to
7,514,405 dollars, which at the top of
the range is 19.6 per cent
of the base in that table. The largest of them, specification change, acts on the
content line, so closing them would make content a larger share rather than a
smaller one: the ordering above survives. **The levels do not.** Read this table
as the ordering it is, which is what this whole document is for.

---

## 6. The trajectory, and what the bands actually are

Bands are built by **ranking whole paths on terminal cumulative cash and averaging
within a band of ranks**, not by blending unrelated percentiles. The central band
is ranks 40 to 60 per cent, the low band 10 to 30, the high band 70 to 90.

That construction has a property a reader will not assume, so it is measured and
published. The central band line sits at the 49.9 percentile of the real
per-path distribution of cumulative cash at the end of the horizon, and between
the 49.8 and 57.4 percentiles across the months from go-to-market
onward. It moves between scenarios as well: on the software-anchored scenario it
ends at 49.9, and on the tutoring-anchored one at
50.1.

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

| | Value |
|---|---|
| Minimum of the mean cumulative cash line, USD | -10,683,349 |
| The month it reaches it | 54 |
| Mean of each path's own minimum, USD | -20,342,916 |
| Ratio of the two | 0.5252 |
| **The headline is shallower by** | **47.5 per cent** |

The per-path distribution beside it: tenth percentile -33,233,772,
ninetieth -5,857,945. Planning to the averaged line plans to a
trough 47.5 per cent shallower than the one a
given path actually meets.

**The timing is worse than the depth, and an earlier draft of this paragraph
missed it entirely by quoting a mean.** It said the averaged line troughs at
month 54 while individual paths trough on average
at 53.6, and called the difference "later" — four tenths
of a month, which is nothing. The mean was hiding the distribution. The **median**
path troughs at month 59, the tenth percentile at
month 30, and
**79.1 per cent of paths have their
trough in the last month of the horizon** — that is, cash is still falling when
the window closes and the trough has not happened yet.

**For four paths in five the funding requirement in section 11 is therefore a
floor, not a figure.** The peak drawdown is the negative of the trough, so
right-censoring the trough right-censors the capital requirement with it. This is
the same horizon effect that makes retained months a floor in section 4, acting
on the number that sizes the rounds. Nothing in this instrument tells you how
much more capital month 61 asks for, because there is no month 61.

### The sustained bad run

Independent monthly shocks would remove exactly the failure mode that ends
companies. The demand shock here is AR(1) with persistence sampled between
0.45 and 0.95, median 0.70. The longest run of consecutive months with the
demand multiplier below 0.80 averages 5.8 months and reaches
13.0 at the ninetieth percentile. 36.9 per cent of paths contain a run of
six or more such months and 12.1 per cent a run of twelve or more. The run
length is a published column of `out/por_paths.csv`, not a reconstruction.

---

## 8. The sensitivity ordering

First-order Sobol indices, estimated by sorting on driver rank, cutting into forty
equal-count bins and applying the one-way analysis-of-variance correction for
within-bin noise. Without the correction every driver scores about the bin count
over the path count and a driver that does nothing looks like it does something.

**Read the sum before reading the ordering.** First-order indices sum to
0.176 on terminal cash, 0.772 on its rank transform,
0.796 on peak funding and 0.510 on whether a path
reaches profitability.

**Only the raw terminal-cash decomposition is interaction-dominated**, and that is
a property of its tail rather than of the model: terminal cash is heavy enough
that its variance is largely a handful of paths. On the rank transform and on the
capital requirement, first-order effects explain most of the variance, so the
ordering on those targets can be read as an ordering. It is still worth having
the two-way grid in section 9, because the interaction that remains is
concentrated in exactly the two drivers that matter most.

### Whether the venture ever makes money

Target: does a path run three consecutive cash-positive months inside the horizon.

| Rank | Driver | First-order index |
|---|---|---|
| 1 | cac_anchor_usd | 0.208 |
| 2 | anchor_u | 0.164 |
| 3 | cac_ref_spend_usd | 0.046 |
| 4 | sat_kappa | 0.016 |
| 5 | churn_base | 0.016 |

### How much capital it takes

Target: the peak funding requirement.

| Rank | Driver | First-order index |
|---|---|---|
| 1 | items_per_unit | 0.162 |
| 2 | cac_anchor_usd | 0.109 |
| 3 | anchor_u | 0.103 |
| 4 | writer_gbp_item | 0.081 |
| 5 | minutes_per_item | 0.078 |
| 6 | board_reuse | 0.066 |
| 7 | examiner_rate_gbp_hr | 0.043 |

**The two orderings are different and the difference is the finding.** Acquisition
cost and the price-anchor regime decide whether. Item count per subject bank,
authoring cost per item, validation minutes per item, reuse across boards and the
examiner rate decide how much. Content-cost drivers take
5 of the top seven places on capital and
0 of the top three on whether the venture ever makes money.
Acquisition drivers take 2 of that top three. All three counts are
computed in `figures.py` from `out/sobol.csv` rather than counted by eye.

**Do not lean on those counts, and an earlier draft did.** A count of how many
content drivers appear in a top seven is a fact about how finely the registry
splits each cost, not about the business. Content cost per item is
3 priors here — validation minutes, the
examiner rate, the authoring rate — because that is how it decomposes; but one
timed pilot measures all of them at once, so as an object of decision it is
**one** quantity. The acquisition set is split across
12.
Rank the registry entries and content wins on count; group them the way the
instruments that would measure them group them and the ranking changes.
`out/sobol_grouped.csv` does that, on genuine scalars rather than by summing
individual indices, which is not a group index:

| Quantity | First-order index on the capital requirement |
|---|---|
| `items_per_unit` alone, rank 1 in the table above | 0.1619 |
| Cost per item, as one timed pilot would measure it | 0.2070 |
| The cost of one full item bank, items times cost per item | 0.3868 |
| The blended acquisition anchor | 0.1137 |

Read that table rather than the count. **The finding survives and is stronger
stated this way**: the cost of one item bank owns more of the variance in the
capital requirement than any single registry entry does, and more than the
acquisition anchor. The count of five was never the evidence, and no instrument
in this directory can see registry granularity — it is a defect of the
measurement, named in LIMITS.md.

The practical reading: **work on acquisition and the price anchor to make the
business exist; work on content cost to make it fundable.** They are different
programmes of work and this instrument says they are not substitutes.

### The ordering is a property of the scope, and it rearranges

Every index above is computed on the plan of record. That is not a neutral
choice, and quoting the result as "the sensitivity ordering" — which two earlier
drafts of this document did throughout — asserts something the file does not
support. `out/sobol.csv` now carries the same decomposition on the go-to-market
minimum, and the capital ordering rearranges:

| Rank | Plan of record | Go-to-market minimum |
|---|---|---|
| 1 | items_per_unit | anchor_u |
| 2 | cac_anchor_usd | cac_anchor_usd |
| 3 | anchor_u | eng_usd_yr |
| 4 | writer_gbp_item | eng_ramp_mult |
| 5 | minutes_per_item | cac_ref_spend_usd |
| 6 | board_reuse | items_per_unit |
| 7 | examiner_rate_gbp_hr | overhead_mult |

Content drivers hold
5 of the top seven
on the plan of record and
1 on the
go-to-market minimum. Both counts are computed from the file.

**The reason is not subtle and it does not weaken the finding; it sharpens it.**
On the plan of record the content escalation to eleven subjects, two levels and
four boards is the largest single commitment, so being wrong about item count or
authoring cost is the most expensive kind of wrong available. On the go-to-market
minimum there is almost no escalation to be wrong about — the bank is built once
and never widened — so what is left to be wrong about is the price regime, the
acquisition anchor and how many engineers it takes to keep a product running.
The instrument is telling you that **the content ordering is a consequence of the
scope decision in section 12, not an input to it.** Decide the scope first; the
sensitivity ordering follows from it, and "content is the thing to get right" is
true of the plan of record and not of the alternative.

That is a third item in this document whose answer changes with a choice rather
than with evidence, alongside which statistic sizes the rounds and which
statistic ranks the levers. None of the three is settled by more simulation.

### Pinned sweeps

Each driver pinned across the whole sample at its own fifth and ninety-fifth
percentile, with the pin applied after the draws so both runs share every random
number and the difference is that driver's alone.

| Driver pinned | Terminal cash at q5 | at q95 | Swing |
|---|---|---|---|
| items_per_unit | -3,270,667 | -16,796,230 | 13,525,563 |
| cac_anchor_usd | 29,948,633 | -24,110,702 | 54,059,335 |
| anchor_u | 3,007,876 | -23,216,271 | 26,224,147 |
| writer_gbp_item | -5,380,841 | -14,677,662 | 9,296,821 |
| minutes_per_item | -5,156,551 | -14,944,080 | 9,787,530 |
| board_reuse | -14,475,750 | -5,651,474 | 8,824,276 |

Two notes on that table. The `anchor_u` row is degenerate and is reported as such:
that driver is a uniform compared against a threshold, so pinning it is not a
sweep but a switch between two regimes. Its two values are the whole of its
effect, and section 9 restates it as the scenario pair it actually is. And the
three columns are each rounded from their own float, so subtracting the printed
endpoints will occasionally differ from the printed swing by one dollar;
`out/pinned_sweeps.csv` carries the unrounded values.

---

## 9. The two-way grid, and the scenarios

### The grid

The two drivers owning the most variance, crossed five by five, each cell a full
re-run on the same random numbers. `sensitivity.py` selects them on the
rank-transformed terminal-cash target; they are also ranks one and two on the
capital target, so the pair is the same either way.

`out/twoway_grid.csv` holds items_per_unit against cac_anchor_usd. Terminal cash
across the grid runs from -30,008,332 to 26,418,733, a range of
56,427,066.

The shape matters more than the range. Moving one step down the content axis costs
roughly the same amount wherever you are on the acquisition axis: content is close
to additive. Moving one step along the acquisition axis, from its tenth to its
thirtieth percentile, changes terminal cash by tens of millions and changes the
share of paths reaching profitability far more than the whole content axis does.
**Acquisition sets the level; content sets the slope.**

### The scenarios

All share the same drivers and the same random stream, and differ only in the
switches named. Every scenario that opens a market or a channel is charged for it.

**Three columns, and the third is the one to argue with.** Terminal cash is
heavy-tailed, so a difference in its mean is partly a difference in a handful of
paths. The delta on the median path is given beside it, and where the two
disagree in sign the scenario is marked. A third column gives the effect on the
peak funding requirement at the eightieth percentile, which is the statistic
section 11 sizes the rounds on.

| Scenario | Delta, mean | Delta, median path | Delta, peak funding p80 | Mean and median agree in sign: 1 yes, 0 no |
|---|---|---|---|---|
| Condition C1 passes: tutoring anchor on every path | 13,056,956 | 3,003,207 | -2,275,227 | 1 |
| Condition C1 fails: software anchor on every path | -13,167,191 | -2,330,385 | 1,887,310 | 1 |
| Without the institution channel | 2,250,258 | 2,267,498 | -2,285,788 | 1 |
| United Kingdom consumer only, no institution channel | 714,598 | 7,531,207 | -10,720,377 | 1 |
| Half the engineering forced onshore | -4,047,410 | -3,394,938 | 3,539,881 | 1 |
| All learner-facing engineering onshore | -8,094,819 | -6,800,038 | 7,290,369 | 1 |
| With driver dependence imposed | 3,252,573 | 6,939 | 162,051 | 1 |
| With the feedback loops switched on | -5,035,412 | -1,048,518 | 1,005,977 | 1 |
| Dependence and feedback together | -2,894,522 | -1,027,775 | 1,183,933 | 1 |
| Creators want money | -2,011,477 | -1,342,430 | 1,388,058 | 1 |
| A share of billing through an app store | -2,063,411 | -343,099 | 272,409 | 1 |
| Go-to-market three months later | -738,257 | 289,750 | -453,252 | 0 |
| Go-to-market six months later | 448,044 | 1,968,414 | -2,956,895 | 1 |
| Foreign exchange sampled rather than fixed — **not distinguishable from zero**, see below | 41,692 | 64,314 | 69,051 | 1 |
| India opened direct to parents | -3,061,528 | -2,938,530 | 4,394,553 | 1 |
| The allowance enforced | -4,468,821 | -527,176 | 435,173 | 1 |
| United Kingdom content frozen at the go-to-market five subjects | 8,231,678 | 7,387,443 | -11,214,138 | 1 |
| The go-to-market minimum: one market, one board, no institution channel | 8,767,565 | 14,846,335 | -21,511,799 | 1 |
| The horizon credits a residual rather than writing everything to zero | 20,943,045 | 5,976,334 | -259,478 | 1 |

The plan of record itself is -10,049,080 on the mean and
-19,974,828 on the median path. The gap between those two numbers is
the reason the second column exists.

Six readings.

**The largest single scenario in that table is the residual, at
20,943,045 dollars, and it is an artefact of
where the horizon was cut rather than a finding about the business.** The
published run writes everything to zero at month 60: the item bank, which is an
asset with a life well beyond the horizon, and the standing book of subscribers,
which is what a buyer would actually be buying. The `por_residual` scenario
credits both — a sampled share of accumulated content cost retained as an asset,
and the standing book at a sampled multiple of its monthly contribution — and the
answer flips from a loss to a gain on the mean. Every number in that scenario is
a prior: the retained share is drawn uniform on
0.15 to 0.65
and the book multiple uniform on 6.0 to
30.0 months, and nothing in the vault anchors
either. It is in this document because a scenario that large cannot sit in a CSV
unmentioned, and it is **not** in the plan of record, because writing a residual
you have invented into your base case is how a base case stops being one. Read it
as the size of the question "what is this worth at month 60 if you do not
liquidate it", not as an answer to it.

Five more readings.

**The price anchor is worth 26,224,147 dollars between its two states**, and
it is a landing page and a few days of spend to test. It is condition C1 in
docs/09, and nothing else in this instrument comes close to it on cost of
information.

Read that figure from the middle column, not the right-hand one. The right-hand
column gives each regime against the published run, and the published run draws
each path into one regime or the other with probability 0.50, so it is a
mixture of both. The quantity a landing-page test resolves is the spread between
the regimes, which is the larger number.

**Dropping the institution channel is worth 2,250,258 dollars on the mean and
2,267,498 on the median path.** Field sales
salaries, per-school onboarding, a security certification and its annual renewal,
against contracts worth 0.61 per cent of net revenue. On these priors Route B
as scoped here does not pay for itself inside the horizon. docs/09's argument for
Route B was never that it pays sooner; it was that it produces the outcome
evidence that is the only durable moat, and this instrument does not value
evidence. That is a limit of the instrument, not a refutation of the argument.

**The feedback loops cost 5,035,412 dollars.** A higher price costs
retention, expanding faster costs quality and quality costs retention, and a higher
automation ceiling costs engineering heads. The base model has none of these and
is therefore optimistic by that amount. Every lever in section 8 should be read
net of its own penalty. Section 12's ranking is NOT stated on feedback-on
figures: `out/variants.csv` carries no feedback-on version of the individual
levers, so every figure there is feedback-off and each is optimistic by a share
of this amount.

**Imposed dependence is worth 3,252,573 dollars, in the favourable
direction.** Ten rank correlations were imposed by Iman-Conover reordering, which
preserves every marginal exactly: 10 pairs, worst achieved-against-target
error 0.016, and every marginal verified unchanged in
`out/imanconover_check.csv`. The direction is not a comfort: it means the base run
is conservative on dependence and optimistic on feedback, and the two do not
cancel. Together they are -2,894,522.

**The launch-delay scenarios do not support any conclusion at all, and the honest
thing is to say so rather than to quote the one column that agrees with
intuition.** On the mean, both delays cost money. On the median path and on the
capital requirement, both delays HELP:

| | Delta, mean | Delta, median path | Delta, peak funding p80 |
|---|---|---|---|
| Three months late | -738,257 | 289,750 | -453,252 |
| Six months late | 448,044 | 1,968,414 | -2,956,895 |

Two things are wrong with these scenarios and both run the same way.

`launch_shift` moves the content schedule along with the market openings, so a
six-month shift pushes the month-54 content step past the end of the horizon and
the run never pays for it: content cost falls by
1,720,691 dollars against the plan of record at six months,
against 189,913 at three. And `launch_shift` does NOT move the
platform headcount floor, the general and administrative schedule, the data
protection officer hires, the initial counsel spend or the Article 27
representative, so a delayed launch pays the same sixty months of fixed overhead
against a shorter trading window.

The first effect flatters delay and the second penalises it, and nothing here
separates them. **Draw no calendar conclusion from these two rows.** What the
model does say about the calendar is in the retained-month figures in section 4,
which are about when in the year a household is acquired rather than when the
product launches.

---

## 10. What the break-evens say

**On the cash targets, there are none. On the profitability target, there are
four, and they are the most actionable numbers in this document.**

3 targets were solved by bisection on a pinned driver, each across that
driver's entire prior range: the median path ending the horizon whole, the plan
needing no more than ten million dollars at the eightieth percentile, and half of
all paths running three consecutive cash-positive months.
12 questions per scope, 24 rows in all.
20 are unbracketed and 4 bracket.

**Nothing rescues the cash targets.** No value of the reachable pool, the
acquisition anchor, age assurance cost, validation minutes, item count, sessions
per household, churn or price, anywhere in its prior range, gets the median path
whole on either scope. Two of those eight — the reachable pool and the
acquisition anchor — were also solved against the ten-million-dollar capital
ceiling and fail that too; the other six were solved against the median-path
target only, and this paragraph used to read as though all eight had failed
both. That is not a modelling failure; it is the answer, and the reason is in
the cost split. Content is 36.5 per cent of cost, people 16.9 per cent in
Bengaluru plus 8.6 in the United Kingdom, and step costs 3.3 per cent.
A driver that acts only on demand cannot move a cost base that demand does not
touch. (The one qualification: the United Kingdom safeguarding rota steps on
active households, so part of that people line does respond to demand. See
LIMITS.md item 5.)

### The four that do solve

All four are on the same target, half of all paths running three consecutive
cash-positive months, and all four are on the two drivers section 8 says decide
whether the venture exists at all. **That is a tautology, not corroboration, and
an earlier draft called it "the instrument agreeing with itself" as though it
were evidence.** A bisection can only bracket a target on a driver that moves
that target a lot, and the Sobol index ranks drivers by exactly how much they
move it. Both are computed on the same metric. There is no information in the
agreement; it would have been alarming only if it had failed.

| Scope | Driver | Break-even | Prior median | Prior mode |
|---|---|---|---|---|
| Plan of record | acquisition anchor | 9.57 USD | 32.26 | — |
| Plan of record | tutoring-anchored price | 38.55 GBP a month | 25.21 | 22.00 |
| Go-to-market minimum | acquisition anchor | 15.29 USD | 32.26 | — |
| Go-to-market minimum | tutoring-anchored price | 25.54 GBP a month | 25.21 | 22.00 |

The price rows carried the *mode* of the triangular prior under a column headed
"Prior median" in an earlier draft. For a triangular distribution those are
different numbers, and both are now shown. The acquisition anchor is log-uniform
and has no separate mode to show.

The price rows are the ones to look at, because docs/07 already has the
comparator. Against the verified £25 to £45 an hour GCSE tutoring rate, the
narrow scope's break-even price of
25.54 a month is
1.02 hours of human tutoring at the bottom of that band and
0.57 hours at the top. **That is inside docs/07's own substitution
table, not outside it.** The plan of record needs
38.55 a month, which is
1.54 hours at the bottom of the band, near the top of that table.

Both price figures are conditional on condition C1 passing, because they are
solved with the anchor regime pinned to tutoring. If C1 fails there is no price
in the range that reaches the target on either scope.

**"Viable" is the wrong word, and it was the word an earlier draft used.** The
target these four solve against is that half of all paths run three consecutive
cash-positive months. That is a low bar, and `out/breakeven.csv` now carries what
the plan looks like at each solved value on the statistics the solve did not
target. At the plan of record's break-even price, the median path still ends the
horizon at
-12,568,477
dollars, peak funding at the eightieth percentile is still
23,167,649,
and of the paths that *do* hit the target,
33.8
per cent still end the horizon with negative cash. Three cash-positive months in
a row is a thing a business can do on its way to failing.

**What changes is the instruction, not the level.** The question is not "what
rescues the plan", to which the answer is still nothing: none of these four
values gets the median path whole, and the same file says so in the rows above.
It is "at what acquisition cost, or at what price, does half of this stop being
structurally cash-negative every single month", and the instrument answers that
on both scopes. It is a threshold worth knowing and it is not a rescue.

### What it takes, taken two at a time

"No single driver rescues it" is true and it is not an instruction. The next
question is which *pair* does. `rescue_grid.py` crosses the two drivers whose
break-even endpoints come closest, the acquisition anchor and the
tutoring-anchored price, six by six on both scopes. **The price-anchor regime is
pinned to tutoring throughout**, because price does nothing on a path that
anchors on software, and pinning it is stated rather than buried: every figure
below is conditional on condition C1 passing. Every cell is a full re-run on the
same random numbers.

| | Plan of record | Go-to-market minimum |
|---|---|---|
| Cells of 36 where the median path ends the horizon whole | 7 | 11 |
| Highest acquisition anchor that clears anywhere on the grid | 14.00 | 24.40 |
| Price needed at that anchor, GBP a month | 31.35 | 36.59 |
| Best cell | 48,006,660 | 18,155,843 |
| Worst cell | -22,891,318 | -5,953,224 |

**The boundary is set almost entirely by acquisition cost.** Read the grid across
a row and the price axis moves the number; read it down a column and the
acquisition axis decides whether there is a number to move.

**These are grid quantiles, not solved boundaries, and should not be read as
thresholds.** The highest anchor that clears anywhere on the plan-of-record grid
is 14.00 dollars and on the narrow-scope grid
24.40; the true boundaries lie somewhere between those
tested points and the next ones up, so the ratio between them is bounded loosely
rather than measured. The grid's top price is the ninety-fifth percentile of the
prior, not its maximum, so "no price in the range" means no price the grid tested.
The solved thresholds are in the break-even table above; the grid is here for the
shape, which is that the acquisition axis decides and the price axis adjusts.

**The instruction this yields is about scope and about acquisition, not about any
other parameter.** How much is attempted before the first evidence arrives is the
owner's decision; what a household costs to acquire is the first thing worth
measuring. Neither is a model output.

---

## 11. The funding requirement

Rounds sized at the eightieth percentile of the need inside each window, plus six
months of that window's own burn as buffer. The peak funding requirement is
computed without any injection, as the deepest point of cumulative operating cash
flow, so the sizing is not circular.

| Scope | Seed, to month 18 | Series A, 18 to 36 | Series B, 36 to 60 | Whole horizon, p80 |
|---|---|---|---|---|
| Plan of record | 10,208,123 | 11,919,922 | 15,013,480 | 28,237,786 |
| United Kingdom consumer only | 8,408,296 | 5,445,512 | 9,170,111 | 17,517,410 |
| Go-to-market minimum: five subjects, one board | 3,282,405 | 2,281,449 | 3,413,837 | 6,725,987 |
| One subject, one board | 1,977,898 | 2,195,901 | 3,348,427 | 5,722,828 |

**The round is sized on the plan of record, and the base case is stated beside
it.** They differ by enough that sizing on the base case would underfund the plan
the owner has actually described: 28.24 million against
17.52 million across the horizon.

**The last column and the first three are computed by different rules, and the
difference is not small.** Each staged round carries six months of that stage's
own burn as buffer; the whole-horizon figure is the bare eightieth percentile of
the peak drawdown with no buffer at all. Added up, the plan of record's three
staged rounds come to 37,141,525, which is
8,903,739 more than the whole-horizon figure, a ratio of
1.315. **Raise against the staged number rather than the headline** if you want a
number that survives rounds closing late: the headline is what the plan consumes
if every round closes exactly as the previous one runs out, which is not how
rounds close. As in section 8, each figure in that table is rounded from its own
float, so adding the printed rows will differ from the printed sum by a dollar;
`out/funding.csv` carries the unrounded values.

**And read every figure in this section as an order of magnitude, not a number.**
They are rendered to the dollar because that is what the file holds, not because
they are known to the dollar. Nothing in this instrument is.

**Read them as floors, too.** The peak funding requirement is the negative of a
path's cash trough, and
79.1 per cent of paths have their
trough in the last month of the horizon — still falling when the window closes.
Every figure in the table above is right-censored on that share of paths.
Section 7 gives the distribution.

84.5 per cent of individual paths need more than ten million dollars.

### The staging does not match the decisions

`out/funding_commitments.csv` sets each milestone's landing month beside the month
its spend *starts*, because content is built over the six months before it is
delivered and an entity is stood up before a market opens.

10 of the file's
14 commitments have their spend starting inside the seed
window, among them the United States entity and its market counsel, the
information security certification, A-level content, the second and third United
Kingdom boards, the first sales representative and the go-to-market content build
itself. (An earlier draft introduced that list with a colon, as though it were
all of them; it is seven of the 10.) The Series A
does not buy them; it refinances decisions the seed already committed to. The
file names 2 entity set-ups —
United States entity set-up and market counsel; rest-of-English-speaking entity set-up and market counsel — of which
1 is paid for out of the seed window; an
earlier draft named an India entity, which this model never stands up because
India is an institution market here, and called both entities seed-window.
1 commitment lands in the
Series A window with its spend starting before that round opens: all four United
Kingdom boards live at month 18, built from month 12.
The rest-of-English-speaking market at month 24 starts its build at month 18,
exactly when the Series A opens, so by the file's own test it does not qualify.

**A round of 10,208,123 dollars is not a seed round.** Calling it one and
then discovering at month 18 that the Series A is paying for choices made at month
12 is the failure mode that staging is supposed to prevent.

---

## 12. The decisions that are yours, not the model's

**The ordering of the top two depends on which statistic you rank on, and nothing
here can settle that for you.** On the capital requirement at the eightieth
percentile, scope comes first: 21,511,799
against the price anchor's 4,162,537.
On terminal cash at the mean the anchor comes first,
26,224,147 against the same scope
reduction's 8,767,565, and both comparisons are
now against the go-to-market minimum rather than against two different scope
reductions. Both statistics are published so that the disagreement is visible
rather than resolved by whichever one was quoted.

**Do not read those two figures against each other.** One is a capital
requirement and one is a cash spread; the first is bad when large and the second
good when large, and they happen to be close in magnitude, which makes the
comparison look meaningful. It is not. What the two lines above say is that scope
leads on capital and the anchor leads on terminal cash, each by a wide margin
within its own statistic, and that nothing here converts between them. Both
statistics carry the 1,066,488 sampling interval
from the preamble before any of the priors are argued with.

Items 3 onward are grouped rather than ranked. An earlier draft said they were
ordered by terminal cash at the mean; they are not, and they are not ordered by
anything else either. Each carries its own figure, and the same caution about
which statistic you are reading applies to every one of them.

**Every figure below is feedback-off**, because `out/variants.csv` carries no
feedback-on version of the individual levers. The feedback loops cost
5,035,412 dollars in total, so each lever here is optimistic by some
share of that. Read the ordering, not the levels, and read the ordering knowing
it moves with the statistic.

**1. How much scope to attempt before the first evidence arrives.** The plan of
record needs 28,237,786 against
6,725,987 for the
go-to-market minimum, a spread of 21,511,799
**on the capital requirement**. On terminal cash the same reduction is worth
8,767,565 at the mean and
14,846,335 on the median path. **Scope is much
the largest decision on the capital requirement and the third largest on terminal
cash**, behind the terminal-value residual and the price-anchor regime spread of
26,224,147. It is material on
both, which is the thing that changed.

Two earlier drafts said the opposite — that scope was dominant on capital and
minor on return — and the reason is worth stating, because it is the kind of
error this document exists to catch. The terminal-cash figure was being read off
the `ukonly` scenario, which drops the second market and the institution channel
but keeps the entire United Kingdom content escalation to eleven subjects. Its
content line is 8,596,098 against the
go-to-market minimum's 1,151,306. On
terminal cash that scenario is worth 714,598,
which is close to nothing and which the document duly called close to nothing.
The real scope reduction is worth six times that. So the capital figure was a
comparison against the real scope reduction, the terminal-cash figure was a
comparison against a different and much smaller one, and the conclusion drawn
from putting them side by side was an artefact of the mismatch rather than a
property of the business. The ladder now has three rungs and they are compared
like for like:

| Scope | Terminal cash, mean | Terminal cash, median | Peak funding p80 | Content cost |
|---|---|---|---|---|
| Plan of record | -10,049,080 | -19,974,828 | 28,237,786 | 13,965,826 |
| Content frozen at go-to-market, markets unchanged | -1,817,401 | -12,587,384 | 17,023,648 | 6,521,034 |
| United Kingdom only, content unchanged | -9,334,482 | -12,443,621 | 17,517,410 | 8,596,098 |
| Go-to-market minimum, both reduced | -1,281,515 | -5,128,493 | 6,725,987 | 1,151,306 |

**The two middle rows are the point, and they say something the write-up had no
way to say before.** Freezing the United Kingdom content schedule while keeping
every market takes 7,444,792 off
the content line; dropping every market but the United Kingdom while keeping the
content schedule takes 5,369,727 off it. Both
are large, and the content escalation is the larger of the two. On the capital
requirement they are worth almost the same — freezing content
11,214,138, dropping markets
10,720,377 — and together with the rest of the
reduction they come to 21,511,799. On
terminal cash they are not close: freezing content is worth
8,231,678 and dropping markets
714,598, a factor of five.

**The two decisions separate exactly on the content column, and that is checked
rather than eyeballed — but read what the check covers.** Foreign content
computed as the plan of record less the United Kingdom-only scenario is
5,369,727; computed as content-frozen less the
go-to-market minimum it is the same figure to the dollar, and `verify.py` fails
the run if the two ever disagree. A round-four review pointed out that this
identity holds **by construction** — `content_build_plan()` sums over markets in
an independent loop, so United Kingdom and foreign content are disjoint additive
terms and the check cannot fail. It is a regression test against someone
introducing an interaction later, not evidence of anything today. On the two
columns this section actually reasons from, terminal cash and the capital
requirement, the decisions do **not** decompose exactly: the two separate effects
sum to about two per cent more than the combined scenario. Two per cent does not
disturb the conclusion, and the conclusion is stated knowing it rather than
claiming an exactness that belongs to a different column. So the content column really
does decompose into 1,151,306 of content you
must build to go to market at all, 7,444,792 of
United Kingdom catalogue widening, and 5,369,727
of foreign curriculum. Those are three separable commitments and they are taken
at different times.

So "how much scope" is two decisions and they are not interchangeable. **How many
subjects, levels and boards to build is the one that moves terminal cash; how
many markets to open moves capital and almost nothing else.** If you are sizing a
round, either lever will do. If you are asking whether the thing returns the cash
it consumes, only the content schedule answers. The earlier drafts framed this as
a single question about ambition and it is not one.

It is entirely yours either way: the model has no view on how much ambition is
correct, only on what each amount costs.

**2. Whether to test the price anchor before building anything.** Worth
26,224,147 between its two states, and it costs a landing page.
It is already condition C1 in docs/09 and already milestone M1 in docs/11. The decision
is whether you will actually stop if it fails.

**3. Whether to run the institution channel at all inside this horizon.** Costs
2,250,258 here, and buys outcome evidence that this instrument cannot
value. docs/09 makes the case for it honestly and this model is not equipped to
answer it. You are.

**4. What the session allowance should be, and whether to enforce it.** The
allowance is set at 16 sessions a month in `model.py` as a decision, and
23.6 per cent of households exceed it. **Enforcing it costs
4,468,821**, because the overage revenue lost exceeds the
inference cost saved.

That is the rare case where the commercial posture and the arithmetic point the
same way: the product exists for the struggling learner, the struggling learner
is the one who exceeds the allowance, and on these priors they are worth more in
overage than they cost in inference. The decision that remains yours is the
allowance level itself, which sets how much of that shows up as overage rather
than as plan price.

**5. Whether to bill through an app store.** Costs 2,063,411 and buys
distribution the model does not credit. docs/04 identifies app stores and payment
processors as the real chokepoint, which is an argument for a second relationship
rather than for or against the fee.

**6. Whether India is worth a statutory prohibition — and on these priors it is
not, which is the opposite of what this paragraph used to say.** Opening India
direct to parents **costs** 3,061,528 of
terminal cash over five years, 2,938,530
on the median path, and **raises** the capital requirement at the eightieth
percentile by 4,394,553. It loses money
because it carries an entity, market counsel, a content bank
(2,495,758 of additional content cost),
a platform head and double age assurance, against prices sampled at a fraction of
the United Kingdom's.

Two earlier drafts wrote that figure as "worth". It is rendered from a token
whose name ends in `_abs`, and `out/figures.csv` says in its own derivation note
that the direction lives in the sign of the other token. Every other negative
scenario in this document is written as "costs". India was the only one written
as "worth", and the sentence inverted an owner decision as a result. Section 13's
warning about what the verifier cannot see is this, exactly: the absolute value
did exist on disk to the precision printed, so every automated check passed.

The institution route in India carries no such conflict, and **this instrument
does not model it**, so none of these figures is a comparison between the two
routes in. What they say is narrower and still useful: on these priors DPDP
section 9(3) is not a prohibition the owner is paying for. It is one that saves
money. See section 2.

**7. Where to launch in the calendar. The instrument has nothing usable to say
about this, and it is on the list so that nobody reads its silence as agreement.**
The two delay scenarios disagree with themselves across the three statistics and
are contaminated at both ends; section 9 sets out how. What the calendar mechanics
do say is about when in the year a household is acquired rather than when the
product launches: an examination-year household acquired after Christmas has
months rather than a year, and the retained-month figures in section 4 are the
size of that.

**8. Whether to fix the exchange rate.** You instructed fixed rates. Sampling them
moves the mean by 41,692, which is small; what it changes is the
width of the distribution, not its centre. See LIMITS.md.

---

**And one that is not yours, which is why it is not on the list.** Whether United
Kingdom children's learner data may be processed in Bengaluru at all is a question
for counsel, not a decision for you. docs/05 flags it as a standard position not
confirmed for this fact pattern. If the answer forces the learner path onshore,
the Bengaluru cost base goes with it: 8,094,819 dollars of terminal cash
at the worst reading, 7,290,369 on the capital requirement, and people
overtakes content as the largest cost line.

**It barely moves the sensitivity ordering at all.** The decomposition was run
under full onshoring and written to `out/sobol.csv` under the `onshore_all` run,
so this paragraph can be read off a file instead of asserted. On the capital
requirement, item count stays at rank
1 — the
same rank it holds on the plan of record — and the United Kingdom salary driver
reaches rank 7,
which is inside the top seven and outside the top three. Content drivers hold
4 of the
top seven, against
5 on the plan of
record. Two earlier drafts of this paragraph were wrong in the same direction:
the first said onshoring inverted the ordering, the second said it moved a
United Kingdom salary driver into the top three and pushed item count down.
Neither had been computed. Both are now, and what onshoring does is move a large
amount of cash — see the two figures above — without rearranging what the answer
is most sensitive to. It is still the largest thing a letter to counsel could
resolve, because the cash is real whether or not the ordering moves. It is X8 in
OPEN_ITEMS.md.

---

## 13. Where to look

| File | What it holds |
|---|---|
| `model.py` | Drivers, mechanisms, month loop. Every driver's note says what anchors its range, or that nothing does. |
| `harness.py` | The character-for-character gate. Every script that runs the model goes through it. |
| `out/por_monthly.csv` | The monthly output of the published run: 60 rows, every series as a mean, three percentiles and three band lines. |
| `out/por_paths.csv` | 20000 rows: every per-path outcome and every driver value. |
| `out/sobol.csv`, `out/tornado.csv` | The full sensitivity, every driver against four targets, on three configurations. The `run` column says which; the orderings differ and must not be pooled. |
| `out/pinned_sweeps.csv`, `out/twoway_grid.csv` | The sweeps and the grid. |
| `out/variants.csv`, `out/variants_bands.csv` | Every scenario, and where each one's band lines actually sit. |
| `out/imanconover_check.csv` | Target against achieved rank correlation, and proof each marginal is unchanged. |
| `out/breakeven.csv` | The break-even solves, including the unbracketed ones. |
| `out/funding.csv`, `out/funding_commitments.csv` | Round sizing, and the staging test. |
| `out/cohorts.csv`, `out/omissions.csv` | The checklist measurements and the priced absent cost lines. |
| `out/sized_omissions.csv` | Quantities that are not cost lines but were being reported as zero: the retention stress, the examiner hours, the penalty comparison. |
| `out/rescue_grid.csv` | The two-driver rescue grid behind the second half of section 10, on both scopes. |
| `out/sobol_grouped.csv` | The same decomposition on grouped scalars rather than registry entries, because the registry's granularity is not the business's. |
| `out/drivers.csv`, `out/constants.csv` | Every sampled driver with its range and what anchors it, and every decided constant with what it is. |
| `out/aux_params.csv` | The priors drawn outside the published random stream, which are not in `out/drivers.csv` because they are not in the published run. |
| `out/provenance.csv` | Which `model.py` each generating script last ran against. `verify.py` fails the run if they disagree. |
| `out/offtest.csv` | Each mechanism, off and on: exact when off, and not inert when on. |
| `out/figures.csv` | Every figure quoted anywhere, with its source file and its derivation. |
| `LIMITS.md`, `OPEN_ITEMS.md`, `CHANGELOG.md` | What is not clean, what is unanswered, and what moved. |

`verify.py` first refuses any set of outputs whose generating scripts did not all
run against the current `model.py` — a check that has already bitten, on a
comment-only edit to `model.py` that left every published CSV byte-identical —
then re-derives the core figures from the raw CSVs by a different code path from
`figures.py`, checks five identities — **three** of them down every row of the
monthly file (net revenue equals gross less tax; net cash equals revenue less
every cost line plus any residual; the cumulative line is the running sum of the
monthly one), one a point check that terminal cash at the horizon agrees with
that cumulative line, and one that the scope ladder in section 12 decomposes on
its content column — and then scrapes every number in this document and matches
it against a figure on disk.

**That count has now been wrong twice in opposite directions**, which is a small
thing worth recording because it is the argument of the next two paragraphs. It
said "four accounting identities down the whole monthly file" when one of the
four was a point check; a round-four correction over-corrected to "two", missing
that the running-sum check is computed the same elementwise way as the other two.
Three is right. Nothing in this repository counts the identities for the prose,
because the prose describes what each one *is*, and that is the class of
statement no verifier here can check.

**Be clear about what that second pass does and does not do.** It checks that
every number printed here exists on disk to the precision it is printed at. It
does not check that the sentence around the number is true, and it cannot: a
figure quoted in the wrong place, or described as the wrong quantity, passes.

It is also far weaker on small numbers than on large ones. With on the order of a
thousand figures on disk, a seven-digit dollar amount effectively cannot match by
accident; a one-decimal percentage often can; and a small integer, a month index
or a rank, matches something almost always. **So the pass is strongest exactly
where it is least needed**, because the dollar figures are substituted from
`out/figures.csv` at render time and cannot drift by construction, and weakest on
the hand-typed counts and ordinals, which is where every error the reviewers found
actually was. Numbers written as words escape it entirely.

The remedy has been to convert counts and ordinals into rendered tokens computed
from the files, which is why `figures.py` now counts bracketed break-even rows,
absent cost lines, off-tests, entity set-ups and driver ranks rather than leaving
them to prose, and renders two of the lists verbatim from the file that holds
them. Run the verifier anyway, because it catches the other kind of error.

**The third review round found the failure mode this pass cannot reach, and it is
worth stating because it was the worst defect in the document.** Owner decision 1
set a capital figure measured against one scope reduction beside a terminal-cash
figure measured against a different one, and drew a conclusion from the pair.
Every number in that sentence existed on disk, was rendered from a token, and
traced to a file. The verifier passed it on every run. **What was wrong was the
comparison, and no scraper can see a comparison.** That is what the review
protocol is for, and it is why the protocol says to repeat until a round returns
nothing new rather than until the verifier is quiet.
