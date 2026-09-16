# AI.tutor: the economics, as an instrument rather than a forecast

**Seed @@seed|int@@. Run date @@run_date|raw@@. @@n_paths|int@@ paths, @@horizon_months|int@@ monthly steps, United States dollars.**

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
**@@por_terminal_cash_mc_se|usd0@@ at one standard error and
@@por_terminal_cash_mc_se_two_sigma|usd0@@ at two**, at this path count. Every
level in this document is rendered to the dollar because that is the precision
the file holds, not because it is known to the dollar; read roughly a million
either side of any terminal-cash figure before you read anything else about it.
The scenario deltas are far tighter than that because the scenarios share their
random numbers path by path, which is the point of the paired construction, and
each carries its own paired standard error in `out/variants.csv`. **Use that one,
not the figure above, when judging a scenario**: an earlier draft argued that the
sampled foreign exchange rate is indistinguishable from zero by setting its delta
against the unpaired error, which is several times too large for the comparison.
The conclusion survives on the right number — that scenario's delta is
@@delta_por_fx_sampled_t_stat|num2@@ paired standard errors from zero — and
section 9 says so where it is tabulated.

The seed and the date are quoted wherever a number appears for the same reason.

**Two conventions are load-bearing, and the second is an absence.** Nothing in
this instrument is discounted: terminal cash, the peak funding requirement, every
break-even and the residual are undiscounted nominal sums over sixty months.

**Discounting cuts both ways here, and the obvious direction is the wrong one.**
The headline loss gets *smaller*: at twelve per cent a year the same net cash
line is worth @@por_terminal_cash_npv_12|usd0@@ against the undiscounted
@@por_terminal_cash_mean|usd0@@, and at twenty-five per cent
@@por_terminal_cash_npv_25|usd0@@ — not for the reason an earlier draft gave. It
said "because the largest negative months are the late ones", and they are not:
the magnitude-weighted mean month of negative net cash is
@@por_negative_cash_mean_month|num1@@ against
@@por_positive_cash_mean_month|num1@@ for the positive months. The reason is
duller. @@por_negative_cash_month_count|num0@@ of the
@@horizon_months|int@@ months are negative, so discounting shrinks a sum that is
mostly negative — and the negatives being **early** is what limits how much it
shrinks by. The economics get *worse*: revenue arrives later than cost, so
discounted cost over discounted revenue rises from
@@por_discounted_cost_over_revenue_00|num2@@ undiscounted to
@@por_discounted_cost_over_revenue_25|num2@@ at twenty-five per cent. And
content's share of cost **rises** — from @@por_share_content_cost_pct|num1@@ per
cent to @@por_discounted_content_cost_share_25_pct|num1@@ — while acquisition's
falls to @@por_discounted_cac_spend_share_25_pct|num1@@, because content is
built **earlier than acquisition spend is made** — content's mean month is
@@por_content_cost_mean_month|num1@@ against
@@por_cac_spend_mean_month|num1@@ for acquisition and
@@por_revenue_mean_month|num1@@ for revenue. It is not built early in absolute
terms, as section 1 says; it is built early *relative to the money it is being
weighed against*, which is what a discount rate cares about. So discounting sharpens the ordering
this document reports rather than disturbing it, and it shrinks the residual
scenario, which sits entirely at month 60 and is the largest single item in the
scenario table. Nothing here is restated on a discounted basis; these figures are
published so that the omission has a size and a direction rather than only a
mention.

---

## 1. The three things worth knowing

**One. The plan of record is not a seed-stage plan.** Sized at the eightieth
percentile of the peak drawdown and with no buffer, it requires
@@funding_plan_of_record_whole_horizon_round_size|usdm@@ million dollars across
the horizon, against @@funding_base_case_uk_only_whole_horizon_round_size|usdm@@
million for a United Kingdom consumer business alone and
@@funding_gtm_minimum_uk_one_board_whole_horizon_round_size|usdm@@ million for the
go-to-market minimum: five GCSE subjects, one board, one market, no institution
channel. The first eighteen months of the plan of record alone need
@@funding_plan_of_record_seed_round_size|usdm@@ million.

**None of the three numbers in that paragraph is a forecast, and this is the
paragraph most likely to be quoted as one.** Each carries the
@@por_terminal_cash_mc_se_two_sigma|usd0@@ sampling interval from the preamble
before anything else; each is undiscounted; and each is the output of priors, not
of measurement. A fourth-round review observed that the caveats in this document
live in sections 11 and 13 while section 1 is the part that gets pasted into a
deck, and it was right. The caveat is here now.

**And that headline is the smaller of the two funding numbers in this document,
which section 11 explains.** It assumes every round closes exactly as the last one runs
out. Staged with six months of buffer on each round, which is what raising
against a plan actually looks like, the same plan of record comes to
@@funding_plan_of_record_staged_sum|usdm@@ million. Quote whichever you like, but
quote which one.

**Two. About @@por_share_demand_independent_pct|num1@@ per cent of the cost base does not respond to demand at all.** Content is @@por_share_content_cost_pct|num1@@ per cent of total modelled cost, people
@@por_share_people_beng_cost_pct|num1@@ per cent in Bengaluru plus @@por_share_people_uk_cost_pct|num1@@ in the United Kingdom, and step
costs @@por_share_step_cost_pct|num1@@ per cent. Acquisition, which does depend on demand, is
@@por_share_cac_spend_pct|num1@@ per cent. Inference, the cost docs/06 builds up so carefully, is
@@por_share_inference_cost_pct|num1@@ per cent.

**"Committed" used to be the word in that sentence and it was the wrong one.**
This block is not spent early. @@demand_independent_share_months_24_60|pct1@@ per
cent of it is spent after month 24, and
@@demand_independent_share_months_36_60|pct1@@ per cent after month 36, against a
go-to-market at month @@const_GTM_MONTH|int@@. Nothing about it is locked in
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
@@const_ROTA_EXTENDED_AT|num0@@ and again at @@const_ROTA_24_7_AT|num0@@ active
households. The first fires on @@por_share_paths_over_rota_extended|pct1@@ per
cent of paths and the second on @@por_share_paths_over_rota_24_7|pct1@@ — an
earlier draft said "most paths", which is true of the first and not of the
second. The overwhelming majority of the @@por_share_demand_independent_pct|num1@@ per cent is fixed; a
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
@@sobol_peak_funding_requirement_content_drivers_in_top7|int@@ of the top seven
to @@sobol_gtm_peak_funding_requirement_content_drivers_in_top7|int@@, and a
Bengaluru salary driver arrives at rank
@@sobol_gtm_peak_funding_requirement_rank_of_eng_usd_yr|int@@. "Content is the thing to get right" is
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
| Horizon | @@horizon_months|int@@ months from the month the seed closes. |
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
is zero in all @@horizon_months|int@@ rows of `out/por_monthly.csv`.

So the direct-to-parent variant, which **costs**
@@delta_por_india_d2c_terminal_cash_abs|usd0@@ dollars of terminal cash on the
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
staleness — a derived file generated against an older model and never
regenerated — so `harness.load()` records the SHA-256 of `model.py` **and
`harness.py` together** into `out/provenance.csv`, and `verify.py` fails the
whole run if any generating script's recorded hash is not the current one.
Hashing the harness as well matters: it is the file that splits, executes and
gates the model, and a change to the splitter or to the gate itself would
otherwise leave no trace in any output. That is a weaker check
than the gate and is reported as the weaker thing it is.

**Every mechanism that a variant adds must reproduce the base run exactly when it
is switched off, and every parameter a variant needs is drawn outside the
published random stream.** @@offtest_mechanism_count|int@@ mechanisms are tested
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
runs from @@pathwise_spearman_min_excluding_dependence|num4@@ at the loosest, which is @@pathwise_spearman_min_excluding_dependence_scenario|raw@@, to
@@pathwise_spearman_max|num4@@ at the tightest. The two dependence scenarios sit far below that, at
@@pathwise_spearman_min|num4@@ and above, **by construction and not by accident**: Iman-Conover
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
| Gross consumer revenue over the horizon, mean of paths, USD | @@por_total_gross_consumer_revenue_mean|usd0@@ |
| Consumption tax inside it, USD | @@por_total_tax_collected_mean|usd0@@ |
| Tax as a share of gross, per cent | @@por_tax_share_of_gross_pct|num1@@ |
| Net revenue, consumer and institution together, USD | @@por_total_net_revenue_mean|usd0@@ |
| Institution channel share of net revenue, per cent | @@por_schools_share_of_net_revenue_pct|num2@@ |
| Total cost, USD | @@por_total_cost_mean|usd0@@ |

**Prices are read as gross, that is, tax-inclusive**, which is what United Kingdom
consumer law requires a consumer-facing price to be. Net revenue is the gross
price divided by one plus the rate. Blended across markets that removes
@@por_tax_share_of_gross_pct|num1@@ per cent of gross; on the United Kingdom alone at
twenty per cent VAT it removes a sixth. Under the other reading, in which the
quoted price is net and tax is added on top, revenue would be higher by the whole
tax line: @@por_total_tax_collected_mean|usd0@@ dollars over the horizon.

### Contribution per household, two ways round

Contribution per household month is a ratio, and its denominator collapses on
paths whose book has collapsed, so **the mean of the per-path ratio is not a
number** and is not published anywhere. Two defensible figures are given instead:
the pooled ratio, which is total contribution over total household-months across
every path and every month of the final year, and the median path's own ratio,
over the @@share_paths_with_a_real_final_year|pct1@@ per cent of paths that have a final year to speak of.

| | Pooled | Median path |
|---|---|---|
| Gross: net revenue less inference, support, payment, hosting and store fees | @@final_year_contrib_per_hh_month_gross_pooled|num2@@ | @@final_year_contrib_per_hh_month_gross_median|num2@@ |
| All-in: the same, net of engineering, content, overhead and compliance | @@final_year_contrib_per_hh_month_allin_pooled|num2@@ | @@final_year_contrib_per_hh_month_allin_median|num2@@ |

The first row is a **gross margin**. Quoting it as the value of a customer, which
is the conventional thing to do, overstates: pooled, the all-in figure is
@@gross_minus_allin_contrib_per_hh_month_pooled|num2@@ dollars lower.

**The two columns disagree in sign on the all-in row, and that disagreement is
the finding.** Pooled, a household month contributes
@@final_year_contrib_per_hh_month_allin_pooled|num2@@ dollars all-in. On the median path it consumes
@@allin_consumed_per_hh_month_median|num2@@. The pooled figure is dominated by the few paths with
large books, which carry most of the household-months and spread the fixed costs
over them; the median path is small and the same fixed costs sit on top of it.
Neither is wrong. Quoting only the pooled one would describe a business that most
paths are not running.

### Acquisition cost: the anchor is not the cost

| | Value |
|---|---|
| The low-volume anchor, median of the driver, USD | @@por_cac_anchor_median|num2@@ |
| Effective cost in the final year, pooled at the spend actually modelled, USD | @@final_year_effective_cac_pooled|num2@@ |
| Effective cost on the median path, USD | @@final_year_effective_cac_median|num2@@ |
| Pooled effective over anchor, a ratio | @@final_year_cac_pooled_over_anchor_median|num2@@ |

Channels saturate. The effective cost rises as the square-root-ish power of spend
over a sampled reference spend, and again as the reachable pool is penetrated.
Quoting the anchor as the cost at scale would understate by a factor of
@@final_year_cac_pooled_over_anchor_median|num2@@ at the spend actually modelled. The median path is a different
story, at @@final_year_effective_cac_median|num2@@, because the median path never spends enough to
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
lifetime value is @@final_year_ltv_gross_pooled|num2@@ dollars against a pooled effective acquisition
cost of @@final_year_effective_cac_pooled|num2@@, a ratio of @@final_year_ltv_over_cac_pooled|num2@@. On
@@share_paths_final_year_ltv_below_cac|pct1@@ per cent of individual paths that ratio is below one: the business
is buying households for more than they are worth, in the final year, on that
share of paths. The acquisition budget is capped at @@const_CAC_LTV_CAP|num2@@ times lifetime value,
which is what keeps that share as low as it is.

Note the lifetime value in that ratio is the **gross** one. Against the all-in
contribution the ratio is very much worse: on
@@share_paths_final_year_ltv_allin_below_cac|pct1@@ per cent of paths all-in
lifetime value is below the effective cost of acquiring the household, against
@@share_paths_final_year_ltv_below_cac|pct1@@ per cent on the gross basis. **Quote
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
probability sampled between @@driver_summer_lapse_pre_low|num2@@ and @@driver_summer_lapse_pre_high|num2@@ and a progression
rate sampled between @@driver_progress_continue_low|num2@@ and @@driver_progress_continue_high|num2@@. Running the segment mix pinned to all-examination-year and then to
all-pre-examination-year, on the same random numbers:

| | Value |
|---|---|
| Examination year, months per acquisition | @@retained_months_exam_year_mean|num2@@ |
| Pre-examination year, months per acquisition | @@retained_months_pre_exam_mean|num2@@ |
| A-level, months per acquisition | @@retained_months_alevel_mean|num2@@ |
| **Ratio, pre-examination to examination** | **@@year10_to_year11_retained_months_ratio|num2@@** |

The ratio the code produces is @@year10_to_year11_retained_months_ratio|num2@@, not two. It reaches two or
better on @@share_paths_year10_at_least_doubles|pct2@@ per cent of paths.

**Where does it go? Mostly to the summer, and two earlier drafts of this passage
got that backwards in opposite directions.** The first blamed the summer,
following docs/10's own caveat rather than the model. The second reversed it and
said in-term churn was the culprit — reading three counterfactual ratios off a
list without differencing any of them against the base. Differenced, and now
computed in `out/cohorts.csv` rather than read by eye:

| Counterfactual | Ratio | Lift against the sampled ratio |
|---|---|---|
| As sampled | @@year10_to_year11_retained_months_ratio|num2@@ | — |
| Summer removed entirely: lapse pinned to zero, progression to one | @@year10_ratio_with_no_summer_at_all|num2@@ | **@@year10_ratio_lift_from_removing_summer|num3@@** |
| In-term churn at the floor of its prior, summer left alone | @@year10_ratio_with_churn_at_its_floor|num2@@ | @@year10_ratio_lift_from_flooring_churn|num3@@ |
| Both | @@year10_ratio_with_no_summer_and_floor_churn|num2@@ | — |

**The summer is the larger lever by a factor of
@@year10_summer_lever_over_churn_lever|num0@@**, and the correct reading of these
four rows is narrower than either earlier draft:

1. docs/10's **shape** survives — the pre-examination cohort does retain longer —
   but its magnitude does not: the ratio is @@year10_to_year11_retained_months_ratio|num2@@, not two, and it reaches two on
   @@share_paths_year10_at_least_doubles|pct2@@ per cent of paths.
2. **Neither lever alone recovers two, and neither do both together.** Removing
   the summer entirely still leaves @@year10_ratio_with_no_summer_at_all|num2@@;
   both pinned give @@year10_ratio_with_no_summer_and_floor_churn|num2@@. An
   earlier draft called that combination "the only one that recovers" docs/10's
   figure. It does not recover it. Nothing in the prior ranges does, which is the
   actual finding and is more interesting than either lever.
3. So docs/10's caveat about the summer points at the **right** question, and the
   open items are ordered accordingly: the summer is X5, in-term churn X5b.

There is a larger problem sitting underneath those numbers, and it is in
LIMITS.md: an examination-year household is retained @@retained_months_exam_year_mean|num2@@ months in this
model, against a product sold as a cycle plan running to the last paper. The
average customer of a nine-month plan does not finish a cycle.

**That figure is a floor, not an estimate, and an earlier draft blamed the churn
prior for all of it.** Retained months are computed as active household months
over acquisitions across the whole horizon, and acquisitions are still ramping in
the last months of it, so a large share of them have their retention cut off by
the end of the window rather than by churn. A round-four review re-ran the model
with acquisition switched off after month 24, so every acquisition had at least
three years to run out. The level rises from
@@retained_months_per_path_mean|num2@@ to
@@retained_months_uncensored_mean|num2@@ months, a lift of
@@retained_months_censoring_lift_pct|num0@@ per cent, and that counterfactual is
now a switch in `model.py` rather than a number quoted from a working note. **The ratio between
year groups, which is what refutes docs/10, survives the correction intact** —
that was checked deliberately. The level does not, and every figure built on it,
including the lifetime-value ratio above, is a floor for the same reason.

### The allowance is sold but not enforced

@@por_mean_share_over_allowance_pct|num1@@ per cent of active households exceed the session allowance being
sold to them. That is a household-month weighted share WITHIN each path, then a
plain mean across paths, so a path with a hundred households and a path with one
count equally in it.

The allowance is not enforced. Sessions above it are delivered and cost money, and
they are billed only up to @@const_OVERAGE_CAP_MULT|num1@@ times the allowance. So the omission sits on
one side only and its sign is known rather than assumed away: above the billing
cap, cost runs and revenue does not.

**Enforcing the allowance instead destroys @@delta_por_allowance_enforced_terminal_cash_abs|usd0@@ dollars of terminal
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
| Content: examiner validation and authoring | @@por_total_content_cost_mean|usd0@@ | @@por_share_content_cost_pct|num1@@% |
| Acquisition spend | @@por_total_cac_spend_mean|usd0@@ | @@por_share_cac_spend_pct|num1@@% |
| People, Bengaluru | @@por_total_people_beng_cost_mean|usd0@@ | @@por_share_people_beng_cost_pct|num1@@% |
| People, United Kingdom | @@por_total_people_uk_cost_mean|usd0@@ | @@por_share_people_uk_cost_pct|num1@@% |
| Step costs: entities, counsel, certification, premises, representative | @@por_total_step_cost_mean|usd0@@ | @@por_share_step_cost_pct|num1@@% |
| Payment processing | @@por_total_payment_cost_mean|usd0@@ | @@por_share_payment_cost_pct|num1@@% |
| Inference | @@por_total_inference_cost_mean|usd0@@ | @@por_share_inference_cost_pct|num1@@% |
| Age assurance | @@por_total_verif_cost_mean|usd0@@ | @@por_share_verif_cost_pct|num1@@% |
| Support | @@por_total_support_cost_mean|usd0@@ | @@por_share_support_cost_pct|num1@@% |
| Retrieval, storage, telemetry | @@por_total_hosting_cost_mean|usd0@@ | @@por_share_hosting_cost_pct|num1@@% |
| Institution onboarding, per school | @@por_total_school_onboard_cost_mean|usd0@@ | @@por_share_school_onboard_cost_pct|num1@@% |
| App store fees | @@por_total_appstore_fee_mean|usd0@@ | @@por_share_appstore_fee_pct|num1@@% |

Four readings. The first three each contradict something in the vault or in the
usual telling; the fourth is about what the table leaves out.

**Content is the largest line, not acquisition — and the table above understates
it, because some of the content cost is filed under people.**
@@por_content_head_share_of_beng_people_pct|num1@@ per cent of the Bengaluru
people row is salaried content heads, whose whole job is the content schedule:
@@por_total_people_beng_content_cost_mean|usd0@@ over the horizon, or
@@por_share_people_beng_content_cost_pct|num1@@ per cent of the whole modelled
base. Content-driven cost is therefore
@@por_content_driven_cost_mean|usd0@@, **@@por_share_content_driven_pct|num1@@
per cent of the base rather than the @@por_share_content_cost_pct|num1@@ per cent
the content row shows.** A round-four review found this; the split is now emitted
by `model.py` as its own monthly series rather than reconstructed, and it is a
decomposition of the people line, never added to any total.

docs/10 is right that content does not enter the payback ratio, because it does
not scale with learners. It is nonetheless the largest single call on cash in a
plan that builds this much of it. On
@@share_paths_content_exceeds_acquisition|pct1@@ per cent of individual paths the
contracted content line alone exceeds acquisition, and on
@@share_paths_content_is_largest_line|pct1@@ per cent it exceeds both acquisition
and people, so this is not an artefact of averaging. Those two shares are
computed on the contracted line, so they are lower bounds once the heads are
counted.

**And there is an unresolved question inside that number, which is the honest
finding rather than the figure.** `units_per_content_head`'s own note says a
content head "builds and maintains" content units; `writer_gbp_item` charges an
authoring cost for the same items. Either the salaried head manages a contracted
writer, in which case both are real, or the two are the same work charged twice,
in which case @@por_total_people_beng_content_cost_mean|usd0@@ is a double count
worth @@por_share_people_beng_content_cost_pct|num1@@ per cent of the base.
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
| Inference over gross consumer revenue | @@por_inference_over_gross_revenue_median|pct1@@% | — |
| All variable cost over gross consumer revenue | @@por_variable_over_gross_revenue_median|pct1@@% | @@por_variable_over_gross_revenue_p90|pct1@@% |

Pooled, inference is @@por_inference_over_gross_revenue_pooled|pct2@@ per cent of
gross consumer revenue. But **variable cost exceeds half of revenue on
@@share_paths_variable_cost_over_half_of_revenue|pct1@@ per cent of live paths and
exceeds revenue outright on @@share_paths_variable_cost_over_revenue|pct1@@ per
cent**, which is where docs/10 says its row reverses. So the row does not reverse
on the plan as a whole and it does reverse on a minority of paths, and the honest
statement is the second one as well as the first. The mean of the per-path ratio
is unusable — its denominator collapses on paths whose book collapsed — which is
the same trap this document names correctly for contribution per household and
missed here until round four.

**Age assurance, the condition the route decision turns on, is
@@por_share_verif_cost_pct|num1@@ per cent of cost.** That is not an argument that condition C2 does not
matter. C2 is a threshold test against the first month of contribution, not a
share of the cost base, and section 10 gives its break-even. But the idea that
verification could dominate the cost structure is not supported: what it does is
subtract from the acquisition budget, roughly as docs/10 says — not pound for
pound, and the mechanism is set out in E4 of OPEN_ITEMS.md.

**And a fourth reading, which is about the table rather than in it.** Every share
above is a share of the cost the model *carries*.
`out/omissions.csv` names @@omission_line_count|int@@ cost lines the model does
not carry and prices them at
@@omission_total_of_every_absent_line_low|usd0@@ to
@@omission_total_of_every_absent_line_high|usd0@@ dollars, which at the top of
the range is @@omission_total_of_every_absent_line_share_high_pct|num1@@ per cent
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
published. The central band line sits at the @@por_band_central_placement_terminal|pct1@@ percentile of the real
per-path distribution of cumulative cash at the end of the horizon, and between
the @@por_band_central_placement_min|pct1@@ and @@por_band_central_placement_max|pct1@@ percentiles across the months from go-to-market
onward — a wander of
@@por_band_central_placement_month_spread|pct1@@ percentile points **within this
one run**.

**The warning that used to sit here pointed at the wrong axis.** It said the
placement "moves between scenarios as well" and offered two scenarios ending at
@@band_placement_por_anchor_software_central_terminal|pct1@@ and
@@band_placement_por_anchor_tutoring_central_terminal|pct1@@ as the evidence,
then concluded that cross-scenario comparison of band lines is invalid. Measured
across all @@band_central_placement_scenario_count|int@@ scenarios in
`out/variants_bands.csv`, the terminal placement runs from
@@band_central_placement_scenario_min|pct1@@ to
@@band_central_placement_scenario_max|pct1@@ — a spread of
@@band_central_placement_scenario_spread|pct2@@ percentile points, which is
twenty times smaller than the within-run wander and is not a reason for anything.

**So: comparing terminal band lines between scenarios is fine, and comparing a
band line at one month against a band line at another is not.** The placement is
stable across scenarios and unstable across the horizon, which is the opposite of
what this section used to say.

**What holds regardless: a band line is not a percentile line and must never be
read as one.** Every band line in `out/por_monthly.csv` carries
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
| Minimum of the mean cumulative cash line, USD | @@por_min_of_mean_cash_line|usd0@@ |
| The month it reaches it | @@por_min_of_mean_cash_month|int@@ |
| Mean of each path's own minimum, USD | @@por_mean_of_per_path_min|usd0@@ |
| Ratio of the two | @@por_trough_understatement_ratio|num4@@ |
| **The headline is shallower by** | **@@por_trough_understatement_pct|num1@@ per cent** |

The per-path distribution beside it: tenth percentile @@por_trough_p10|usd0@@,
ninetieth @@por_trough_p90|usd0@@. Planning to the averaged line plans to a
trough @@por_trough_understatement_pct|num1@@ per cent shallower than the one a
given path actually meets.

**The timing is worse than the depth, and an earlier draft of this paragraph
missed it entirely by quoting a mean.** It said the averaged line troughs at
month @@por_min_of_mean_cash_month|int@@ while individual paths trough on average
at @@por_mean_trough_month|num1@@, and called the difference "later" — four tenths
of a month, which is nothing. The mean was hiding the distribution. The **median**
path troughs at month @@por_trough_month_median|int@@, the tenth percentile at
month @@por_trough_month_p10|int@@, and
**@@por_share_paths_trough_at_horizon_pct|num1@@ per cent of paths have their
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
@@driver_shock_rho_low|num2@@ and @@driver_shock_rho_high|num2@@, median @@shock_rho_median|num2@@. The longest run of consecutive months with the
demand multiplier below @@const_SHOCK_BAD_THRESHOLD|num2@@ averages @@shock_longest_bad_run_mean|num1@@ months and reaches
@@shock_longest_bad_run_p90|num1@@ at the ninetieth percentile. @@shock_share_paths_bad_run_6plus|pct1@@ per cent of paths contain a run of
six or more such months and @@shock_share_paths_bad_run_12plus|pct1@@ per cent a run of twelve or more. The run
length is a published column of `out/por_paths.csv`, not a reconstruction.

---

## 8. The sensitivity ordering

First-order Sobol indices, estimated by sorting on driver rank, cutting into forty
equal-count bins and applying the one-way analysis-of-variance correction for
within-bin noise. Without the correction every driver scores about the bin count
over the path count and a driver that does nothing looks like it does something.

**Read the sum before reading the ordering.** First-order indices sum to
@@sobol_terminal_cash_sum_first_order|num3@@ on terminal cash, @@sobol_terminal_cash_rank_sum_first_order|num3@@ on its rank transform,
@@sobol_peak_funding_requirement_sum_first_order|num3@@ on peak funding and @@sobol_reaches_profitability_sum_first_order|num3@@ on whether a path
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
| 1 | @@sobol_reaches_profitability_rank1_driver|raw@@ | @@sobol_reaches_profitability_rank1_value|num3@@ |
| 2 | @@sobol_reaches_profitability_rank2_driver|raw@@ | @@sobol_reaches_profitability_rank2_value|num3@@ |
| 3 | @@sobol_reaches_profitability_rank3_driver|raw@@ | @@sobol_reaches_profitability_rank3_value|num3@@ |
| 4 | @@sobol_reaches_profitability_rank4_driver|raw@@ | @@sobol_reaches_profitability_rank4_value|num3@@ |
| 5 | @@sobol_reaches_profitability_rank5_driver|raw@@ | @@sobol_reaches_profitability_rank5_value|num3@@ |

### How much capital it takes

Target: the peak funding requirement.

| Rank | Driver | First-order index |
|---|---|---|
| 1 | @@sobol_peak_funding_requirement_rank1_driver|raw@@ | @@sobol_peak_funding_requirement_rank1_value|num3@@ |
| 2 | @@sobol_peak_funding_requirement_rank2_driver|raw@@ | @@sobol_peak_funding_requirement_rank2_value|num3@@ |
| 3 | @@sobol_peak_funding_requirement_rank3_driver|raw@@ | @@sobol_peak_funding_requirement_rank3_value|num3@@ |
| 4 | @@sobol_peak_funding_requirement_rank4_driver|raw@@ | @@sobol_peak_funding_requirement_rank4_value|num3@@ |
| 5 | @@sobol_peak_funding_requirement_rank5_driver|raw@@ | @@sobol_peak_funding_requirement_rank5_value|num3@@ |
| 6 | @@sobol_peak_funding_requirement_rank6_driver|raw@@ | @@sobol_peak_funding_requirement_rank6_value|num3@@ |
| 7 | @@sobol_peak_funding_requirement_rank7_driver|raw@@ | @@sobol_peak_funding_requirement_rank7_value|num3@@ |

**The two orderings are different and the difference is the finding.** Acquisition
cost and the price-anchor regime decide whether. Item count per subject bank,
authoring cost per item, validation minutes per item, reuse across boards and the
examiner rate decide how much. Content-cost drivers take
@@sobol_peak_funding_requirement_content_drivers_in_top7|int@@ of the top seven places on capital and
@@sobol_reaches_profitability_content_drivers_in_top3|int@@ of the top three on whether the venture ever makes money.
Acquisition drivers take @@sobol_reaches_profitability_acq_drivers_in_top3|int@@ of that top three. All three counts are
computed in `figures.py` from `out/sobol.csv` rather than counted by eye.

**Do not lean on those counts, and an earlier draft did.** A count of how many
content drivers appear in a top seven is a fact about how finely the registry
splits each cost, not about the business. Content cost per item is
@@registry_cost_per_item_driver_count|int@@ priors here — validation minutes, the
examiner rate, the authoring rate — because that is how it decomposes; but one
timed pilot measures all of them at once, so as an object of decision it is
**one** quantity. The acquisition set is split across
@@registry_acq_driver_count|int@@.
Rank the registry entries and content wins on count; group them the way the
instruments that would measure them group them and the ranking changes.
`out/sobol_grouped.csv` does that, on genuine scalars rather than by summing
individual indices, which is not a group index:

| Quantity | First-order index on the capital requirement |
|---|---|
| `items_per_unit` alone, rank 1 in the table above | @@sobol_peak_funding_requirement_value_of_items_per_unit|num4@@ |
| Cost per item, as one timed pilot would measure it | @@sobol_grouped_peak_funding_requirement_cost_per_item_usd|num4@@ |
| The cost of one full item bank, items times cost per item | @@sobol_grouped_peak_funding_requirement_cost_of_one_bank_usd|num4@@ |
| The blended acquisition anchor alone | @@sobol_grouped_peak_funding_requirement_cac_anchor_blended_usd|num4@@ |
| Effective acquisition cost at a common spend, which is what E2's channel test measures | @@sobol_grouped_peak_funding_requirement_cac_effective_at_reference_spend_usd|num4@@ |

Read that table rather than the count. **The finding survives and is stronger
stated this way**: the cost of one item bank owns more of the variance in the
capital requirement than any single registry entry does, and more than
acquisition however acquisition is grouped.

The last row exists because a round-five review pointed out that the first
grouping was not symmetric — the content scalar collects four of the eight
content entries, everything one timed pilot and one objective count would
settle, while the anchor collects three of twelve and leaves saturation out.
Grouping acquisition the way its own open item proposes to measure it raises its
index, and the margin narrows. It does not close. The count of five was never the
evidence, and no instrument in this directory can see registry granularity — it
is a defect of the measurement, named in LIMITS.md.

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
| 1 | @@sobol_peak_funding_requirement_rank1_driver|raw@@ | @@sobol_gtm_peak_funding_requirement_rank1_driver|raw@@ |
| 2 | @@sobol_peak_funding_requirement_rank2_driver|raw@@ | @@sobol_gtm_peak_funding_requirement_rank2_driver|raw@@ |
| 3 | @@sobol_peak_funding_requirement_rank3_driver|raw@@ | @@sobol_gtm_peak_funding_requirement_rank3_driver|raw@@ |
| 4 | @@sobol_peak_funding_requirement_rank4_driver|raw@@ | @@sobol_gtm_peak_funding_requirement_rank4_driver|raw@@ |
| 5 | @@sobol_peak_funding_requirement_rank5_driver|raw@@ | @@sobol_gtm_peak_funding_requirement_rank5_driver|raw@@ |
| 6 | @@sobol_peak_funding_requirement_rank6_driver|raw@@ | @@sobol_gtm_peak_funding_requirement_rank6_driver|raw@@ |
| 7 | @@sobol_peak_funding_requirement_rank7_driver|raw@@ | @@sobol_gtm_peak_funding_requirement_rank7_driver|raw@@ |

Content drivers hold
@@sobol_peak_funding_requirement_content_drivers_in_top7|int@@ of the top seven
on the plan of record and
@@sobol_gtm_peak_funding_requirement_content_drivers_in_top7|int@@ on the
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
| @@twoway_driver1|raw@@ | @@pinned_items_per_unit_terminal_cash_q5|usd0@@ | @@pinned_items_per_unit_terminal_cash_q95|usd0@@ | @@pinned_items_per_unit_swing_abs|usd0@@ |
| cac_anchor_usd | @@pinned_cac_anchor_usd_terminal_cash_q5|usd0@@ | @@pinned_cac_anchor_usd_terminal_cash_q95|usd0@@ | @@pinned_cac_anchor_usd_swing_abs|usd0@@ |
| anchor_u | @@pinned_anchor_u_terminal_cash_q5|usd0@@ | @@pinned_anchor_u_terminal_cash_q95|usd0@@ | @@pinned_anchor_u_swing_abs|usd0@@ |
| writer_gbp_item | @@pinned_writer_gbp_item_terminal_cash_q5|usd0@@ | @@pinned_writer_gbp_item_terminal_cash_q95|usd0@@ | @@pinned_writer_gbp_item_swing_abs|usd0@@ |
| minutes_per_item | @@pinned_minutes_per_item_terminal_cash_q5|usd0@@ | @@pinned_minutes_per_item_terminal_cash_q95|usd0@@ | @@pinned_minutes_per_item_swing_abs|usd0@@ |
| board_reuse | @@pinned_board_reuse_terminal_cash_q5|usd0@@ | @@pinned_board_reuse_terminal_cash_q95|usd0@@ | @@pinned_board_reuse_swing_abs|usd0@@ |

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

`out/twoway_grid.csv` holds @@twoway_driver1|raw@@ against @@twoway_driver2|raw@@. Terminal cash
across the grid runs from @@twoway_worst_terminal_cash_mean|usd0@@ to @@twoway_best_terminal_cash_mean|usd0@@, a range of
@@twoway_range|usd0@@.

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
| Condition C1 passes: tutoring anchor on every path | @@delta_por_anchor_tutoring_terminal_cash_mean|usd0@@ | @@delta_por_anchor_tutoring_terminal_cash_p50|usd0@@ | @@delta_por_anchor_tutoring_peak_funding_p80|usd0@@ | @@delta_por_anchor_tutoring_sign_agrees_mean_and_median|int@@ |
| Condition C1 fails: software anchor on every path | @@delta_por_anchor_software_terminal_cash_mean|usd0@@ | @@delta_por_anchor_software_terminal_cash_p50|usd0@@ | @@delta_por_anchor_software_peak_funding_p80|usd0@@ | @@delta_por_anchor_software_sign_agrees_mean_and_median|int@@ |
| Without the institution channel | @@delta_por_no_schools_terminal_cash_mean|usd0@@ | @@delta_por_no_schools_terminal_cash_p50|usd0@@ | @@delta_por_no_schools_peak_funding_p80|usd0@@ | @@delta_por_no_schools_sign_agrees_mean_and_median|int@@ |
| United Kingdom consumer only, no institution channel | @@delta_ukonly_terminal_cash_mean|usd0@@ | @@delta_ukonly_terminal_cash_p50|usd0@@ | @@delta_ukonly_peak_funding_p80|usd0@@ | @@delta_ukonly_sign_agrees_mean_and_median|int@@ |
| Half the engineering forced onshore | @@delta_por_onshore_half_terminal_cash_mean|usd0@@ | @@delta_por_onshore_half_terminal_cash_p50|usd0@@ | @@delta_por_onshore_half_peak_funding_p80|usd0@@ | @@delta_por_onshore_half_sign_agrees_mean_and_median|int@@ |
| All learner-facing engineering onshore | @@delta_por_onshore_all_terminal_cash_mean|usd0@@ | @@delta_por_onshore_all_terminal_cash_p50|usd0@@ | @@delta_por_onshore_all_peak_funding_p80|usd0@@ | @@delta_por_onshore_all_sign_agrees_mean_and_median|int@@ |
| With driver dependence imposed | @@delta_por_dependence_terminal_cash_mean|usd0@@ | @@delta_por_dependence_terminal_cash_p50|usd0@@ | @@delta_por_dependence_peak_funding_p80|usd0@@ | @@delta_por_dependence_sign_agrees_mean_and_median|int@@ |
| With the feedback loops switched on | @@delta_por_feedback_on_terminal_cash_mean|usd0@@ | @@delta_por_feedback_on_terminal_cash_p50|usd0@@ | @@delta_por_feedback_on_peak_funding_p80|usd0@@ | @@delta_por_feedback_on_sign_agrees_mean_and_median|int@@ |
| Dependence and feedback together | @@delta_por_dependence_feedback_terminal_cash_mean|usd0@@ | @@delta_por_dependence_feedback_terminal_cash_p50|usd0@@ | @@delta_por_dependence_feedback_peak_funding_p80|usd0@@ | @@delta_por_dependence_feedback_sign_agrees_mean_and_median|int@@ |
| Creators want money | @@delta_por_creator_fees_terminal_cash_mean|usd0@@ | @@delta_por_creator_fees_terminal_cash_p50|usd0@@ | @@delta_por_creator_fees_peak_funding_p80|usd0@@ | @@delta_por_creator_fees_sign_agrees_mean_and_median|int@@ |
| A share of billing through an app store | @@delta_por_appstore_terminal_cash_mean|usd0@@ | @@delta_por_appstore_terminal_cash_p50|usd0@@ | @@delta_por_appstore_peak_funding_p80|usd0@@ | @@delta_por_appstore_sign_agrees_mean_and_median|int@@ |
| Go-to-market three months later | @@delta_por_launch_plus3_terminal_cash_mean|usd0@@ | @@delta_por_launch_plus3_terminal_cash_p50|usd0@@ | @@delta_por_launch_plus3_peak_funding_p80|usd0@@ | @@delta_por_launch_plus3_sign_agrees_mean_and_median|int@@ |
| Go-to-market six months later | @@delta_por_launch_plus6_terminal_cash_mean|usd0@@ | @@delta_por_launch_plus6_terminal_cash_p50|usd0@@ | @@delta_por_launch_plus6_peak_funding_p80|usd0@@ | @@delta_por_launch_plus6_sign_agrees_mean_and_median|int@@ |
| Foreign exchange sampled rather than fixed — **not distinguishable from zero**, see below | @@delta_por_fx_sampled_terminal_cash_mean|usd0@@ | @@delta_por_fx_sampled_terminal_cash_p50|usd0@@ | @@delta_por_fx_sampled_peak_funding_p80|usd0@@ | @@delta_por_fx_sampled_sign_agrees_mean_and_median|int@@ |
| India opened direct to parents | @@delta_por_india_d2c_terminal_cash_mean|usd0@@ | @@delta_por_india_d2c_terminal_cash_p50|usd0@@ | @@delta_por_india_d2c_peak_funding_p80|usd0@@ | @@delta_por_india_d2c_sign_agrees_mean_and_median|int@@ |
| The allowance enforced | @@delta_por_allowance_enforced_terminal_cash_mean|usd0@@ | @@delta_por_allowance_enforced_terminal_cash_p50|usd0@@ | @@delta_por_allowance_enforced_peak_funding_p80|usd0@@ | @@delta_por_allowance_enforced_sign_agrees_mean_and_median|int@@ |
| United Kingdom content frozen at the go-to-market five subjects | @@delta_por_content_frozen_terminal_cash_mean|usd0@@ | @@delta_por_content_frozen_terminal_cash_p50|usd0@@ | @@delta_por_content_frozen_peak_funding_p80|usd0@@ | @@delta_por_content_frozen_sign_agrees_mean_and_median|int@@ |
| The go-to-market minimum: one market, one board, no institution channel | @@delta_gtm_minimum_terminal_cash_mean|usd0@@ | @@delta_gtm_minimum_terminal_cash_p50|usd0@@ | @@delta_gtm_minimum_peak_funding_p80|usd0@@ | @@delta_gtm_minimum_sign_agrees_mean_and_median|int@@ |
| The horizon credits a residual rather than writing everything to zero | @@delta_por_residual_terminal_cash_mean|usd0@@ | @@delta_por_residual_terminal_cash_p50|usd0@@ | @@delta_por_residual_peak_funding_p80|usd0@@ | @@delta_por_residual_sign_agrees_mean_and_median|int@@ |

The plan of record itself is @@scenario_por_terminal_cash_mean|usd0@@ on the mean and
@@scenario_por_terminal_cash_p50|usd0@@ on the median path. The gap between those two numbers is
the reason the second column exists.

Six readings.

**The largest single scenario in that table is the residual, at
@@delta_por_residual_terminal_cash_mean|usd0@@ dollars, and it is an artefact of
where the horizon was cut rather than a finding about the business.** The
published run writes everything to zero at month 60: the item bank, which is an
asset with a life well beyond the horizon, and the standing book of subscribers,
which is what a buyer would actually be buying. The `por_residual` scenario
credits both — a sampled share of accumulated content cost retained as an asset,
and the standing book at a sampled multiple of its monthly contribution — and the
answer flips from a loss to a gain on the mean. Every number in that scenario is
a prior: the retained share is drawn uniform on
@@residual_content_retained_low|num2@@ to @@residual_content_retained_high|num2@@
and the book multiple uniform on @@residual_book_months_low|num1@@ to
@@residual_book_months_high|num1@@ months, and nothing in the vault anchors
either. It is in this document because a scenario that large cannot sit in a CSV
unmentioned, and it is **not** in the plan of record, because writing a residual
you have invented into your base case is how a base case stops being one. Read it
as the size of the question "what is this worth at month 60 if you do not
liquidate it", not as an answer to it.

Five more readings.

**The price anchor is worth @@anchor_tutoring_minus_software_terminal_cash_mean|usd0@@ dollars between its two states**, and
it is a landing page and a few days of spend to test. It is condition C1 in
docs/09, and nothing else in this instrument comes close to it on cost of
information.

Read that figure from the middle column, not the right-hand one. The right-hand
column gives each regime against the published run, and the published run draws
each path into one regime or the other with probability @@const_P_TUTORING_ANCHOR|num2@@, so it is a
mixture of both. The quantity a landing-page test resolves is the spread between
the regimes, which is the larger number.

**Dropping the institution channel is worth @@delta_por_no_schools_terminal_cash_mean|usd0@@ dollars on the mean and
@@delta_por_no_schools_terminal_cash_p50|usd0@@ on the median path.** Field sales
salaries, per-school onboarding, a security certification and its annual renewal,
against contracts worth @@por_schools_share_of_net_revenue_pct|num2@@ per cent of net revenue. On these priors Route B
as scoped here does not pay for itself inside the horizon. docs/09's argument for
Route B was never that it pays sooner; it was that it produces the outcome
evidence that is the only durable moat, and this instrument does not value
evidence. That is a limit of the instrument, not a refutation of the argument.

**The feedback loops cost @@delta_por_feedback_on_terminal_cash_abs|usd0@@ dollars.** A higher price costs
retention, expanding faster costs quality and quality costs retention, and a higher
automation ceiling costs engineering heads. The base model has none of these and
is therefore optimistic by that amount. Every lever in section 8 should be read
net of its own penalty. Section 12's ranking is NOT stated on feedback-on
figures: `out/variants.csv` carries no feedback-on version of the individual
levers, so every figure there is feedback-off and each is optimistic by a share
of this amount.

**Imposed dependence is worth @@delta_por_dependence_terminal_cash_mean|usd0@@ dollars, in the favourable
direction.** Ten rank correlations were imposed by Iman-Conover reordering, which
preserves every marginal exactly: @@imanconover_pairs|int@@ pairs, worst achieved-against-target
error @@imanconover_worst_corr_error|num3@@, and every marginal verified unchanged in
`out/imanconover_check.csv`. The direction is not a comfort: it means the base run
is conservative on dependence and optimistic on feedback, and the two do not
cancel. Together they are @@delta_por_dependence_feedback_terminal_cash_mean|usd0@@.

**The launch-delay scenarios do not support any conclusion at all, and the honest
thing is to say so rather than to quote the one column that agrees with
intuition.** On the mean, both delays cost money. On the median path and on the
capital requirement, both delays HELP:

| | Delta, mean | Delta, median path | Delta, peak funding p80 |
|---|---|---|---|
| Three months late | @@delta_por_launch_plus3_terminal_cash_mean|usd0@@ | @@delta_por_launch_plus3_terminal_cash_p50|usd0@@ | @@delta_por_launch_plus3_peak_funding_p80|usd0@@ |
| Six months late | @@delta_por_launch_plus6_terminal_cash_mean|usd0@@ | @@delta_por_launch_plus6_terminal_cash_p50|usd0@@ | @@delta_por_launch_plus6_peak_funding_p80|usd0@@ |

Two things are wrong with these scenarios and both run the same way.

`launch_shift` moves the content schedule along with the market openings, so a
six-month shift pushes the month-54 content step past the end of the horizon and
the run never pays for it: content cost falls by
@@delta_por_launch_plus6_total_content_cost_abs|usd0@@ dollars against the plan of record at six months,
against @@delta_por_launch_plus3_total_content_cost_abs|usd0@@ at three. And `launch_shift` does NOT move the
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

@@breakeven_distinct_metrics|int@@ targets were solved by bisection on a pinned driver, each across that
driver's entire prior range: the median path ending the horizon whole, the plan
needing no more than ten million dollars at the eightieth percentile, and half of
all paths running three consecutive cash-positive months.
@@breakeven_plan_of_record_questions|int@@ questions per scope, @@breakeven_rows_total|int@@ rows in all.
@@breakeven_rows_unbracketed|int@@ are unbracketed and @@breakeven_rows_bracketed|int@@ bracket.

**Nothing rescues the cash targets.** No value of the reachable pool, the
acquisition anchor, age assurance cost, validation minutes, item count, sessions
per household, churn or price, anywhere in its prior range, gets the median path
whole on either scope. The other six of those eight were solved against the
median-path target only.

**But two of them were also solved against the ten-million-dollar capital
ceiling, and there the answer is the opposite of what this paragraph used to
say.** "Not bracketed" means only that the metric does not *cross* the target
inside the prior range; it says nothing about which side of it the metric sits
on, and two drafts read every unbracketed row as a failure. On the plan of record
the reachable pool and the acquisition anchor do fail the ceiling everywhere. **On
the go-to-market minimum they meet it everywhere** — at the very top of the
acquisition anchor's log-uniform prior, four times its median, the narrow scope
still needs
@@breakeven_gtm_minimum_uk_one_board_cac_anchor_usd_peak_funding_p80_metric_at_support_high|usd0@@
against the ten-million ceiling, and across the reachable pool's thirtyfold range
the figure never leaves the neighbourhood of
@@breakeven_gtm_minimum_uk_one_board_pool_uk_peak_funding_p80_metric_at_support_low|usd0@@.
Section 11's own table says the same thing from the other end, and this section
contradicted it for two rounds. `out/breakeven.csv` now records which side every
unbracketed row sits on:
@@breakeven_rows_unbracketed_met|int@@ of the
@@breakeven_rows_unbracketed|int@@ unbracketed rows are unbracketed because the
target is **met** across the whole prior range.

**That is the most actionable positive result in the file and it was being
reported as a failure.** The narrow scope stays inside a ten-million-dollar
capital ceiling at the eightieth percentile wherever the acquisition anchor and
the reachable pool land inside their priors. That is not a modelling failure; it is the answer, and the reason is in
the cost split. Content is @@por_share_content_cost_pct|num1@@ per cent of cost, people @@por_share_people_beng_cost_pct|num1@@ per cent in
Bengaluru plus @@por_share_people_uk_cost_pct|num1@@ in the United Kingdom, and step costs @@por_share_step_cost_pct|num1@@ per cent.
A driver that acts only on demand cannot move a cost base that demand does not
touch. (The one qualification: the United Kingdom safeguarding rota steps on
active households, so part of that people line does respond to demand. See
LIMITS.md item 5.)

### The four that do solve

All four are on the same target, half of all paths running three consecutive
cash-positive months, and all four are on the two drivers section 8 says decide
whether the venture exists at all — and **two drafts running have got the reason
for that wrong in opposite directions.** The first called it "the instrument
agreeing with itself", as though it were corroboration. The second called it a
tautology, on the argument that a bisection can only bracket on a driver the
index ranks highly. That argument fails on this file: the price driver brackets
while ranking @@sobol_reaches_profitability_rank_of_price_uk_tut_gbp|int@@ on the
same target, at @@sobol_reaches_profitability_value_of_price_uk_tut_gbp|num4@@
against the anchor regime's
@@sobol_reaches_profitability_value_of_anchor_u|num4@@ — and the anchor regime,
which ranks second, has no break-even at all.

**The real reason is the pinning, and the write-up says so two paragraphs
below.** The price solve pins the anchor regime to tutoring; the Sobol run does
not. So the price row brackets *conditionally*, on a scope where the largest
competing uncertainty has been switched off, while `anchor_u` cannot bracket
because it is a regime switch rather than a continuum. The agreement between the
two lists is neither corroboration nor a tautology. It is a consequence of what
each instrument was allowed to hold fixed, which is the sort of thing that has to
be read off the code rather than inferred from the shape of the answer.

| Scope | Driver | Break-even | Prior median | Prior mode |
|---|---|---|---|---|
| Plan of record | acquisition anchor | @@breakeven_at_plan_of_record_cac_anchor_usd_share_reaching_profitability|num2@@ USD | @@por_cac_anchor_median|num2@@ | — |
| Plan of record | tutoring-anchored price | @@breakeven_at_plan_of_record_price_uk_tut_gbp_share_reaching_profitability|num2@@ GBP a month | @@breakeven_plan_of_record_price_uk_tut_gbp_share_reaching_profitability_prior_median|num2@@ | @@driver_price_uk_tut_gbp_mode|num2@@ |
| Go-to-market minimum | acquisition anchor | @@breakeven_at_gtm_minimum_uk_one_board_cac_anchor_usd_share_reaching_profitability|num2@@ USD | @@por_cac_anchor_median|num2@@ | — |
| Go-to-market minimum | tutoring-anchored price | @@breakeven_at_gtm_minimum_uk_one_board_price_uk_tut_gbp_share_reaching_profitability|num2@@ GBP a month | @@breakeven_gtm_minimum_uk_one_board_price_uk_tut_gbp_share_reaching_profitability_prior_median|num2@@ | @@driver_price_uk_tut_gbp_mode|num2@@ |

The price rows carried the *mode* of the triangular prior under a column headed
"Prior median" in an earlier draft. For a triangular distribution those are
different numbers, and both are now shown. The acquisition anchor is log-uniform
and has no separate mode to show.

The price rows are the ones to look at, because docs/07 already has the
comparator. Against the verified £25 to £45 an hour GCSE tutoring rate, the
narrow scope's break-even price of
@@breakeven_at_gtm_minimum_uk_one_board_price_uk_tut_gbp_share_reaching_profitability|num2@@ a month is
@@breakeven_gtm_minimum_uk_one_board_price_hours_at_25|num2@@ hours of human tutoring at the bottom of that band and
@@breakeven_gtm_minimum_uk_one_board_price_hours_at_45|num2@@ hours at the top. **That is inside docs/07's own substitution
table, not outside it.** The plan of record needs
@@breakeven_at_plan_of_record_price_uk_tut_gbp_share_reaching_profitability|num2@@ a month, which is
@@breakeven_plan_of_record_price_hours_at_25|num2@@ hours at the bottom of the band, near the top of that table.

Both price figures are conditional on condition C1 passing, because they are
solved with the anchor regime pinned to tutoring. If C1 fails there is no price
in the range that reaches the target on either scope.

**"Viable" is the wrong word, and it was the word an earlier draft used.** The
target these four solve against is that half of all paths run three consecutive
cash-positive months. That is a low bar, and `out/breakeven.csv` now carries what
the plan looks like at each solved value on the statistics the solve did not
target. At the plan of record's break-even price, the median path still ends the
horizon at
@@breakeven_plan_of_record_price_uk_tut_gbp_share_reaching_profitability_at_be_terminal_cash_median|usd0@@
dollars, peak funding at the eightieth percentile is still
@@breakeven_plan_of_record_price_uk_tut_gbp_share_reaching_profitability_at_be_peak_funding_p80|usd0@@,
and of the paths that *do* hit the target,
@@breakeven_plan_of_record_price_uk_tut_gbp_share_reaching_profitability_at_be_hitting_paths_ending_negative_pct|num1@@
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
| Cells of @@rescue_plan_of_record_cells_total|int@@ where the median path ends the horizon whole | @@rescue_plan_of_record_cells_clearing|int@@ | @@rescue_gtm_minimum_uk_one_board_cells_clearing|int@@ |
| Highest acquisition anchor that clears anywhere on the grid | @@rescue_plan_of_record_highest_cac_that_clears|num2@@ | @@rescue_gtm_minimum_uk_one_board_highest_cac_that_clears|num2@@ |
| Price needed at that anchor, GBP a month | @@rescue_plan_of_record_price_needed_at_that_cac|num2@@ | @@rescue_gtm_minimum_uk_one_board_price_needed_at_that_cac|num2@@ |
| Best cell | @@rescue_plan_of_record_best_median|usd0@@ | @@rescue_gtm_minimum_uk_one_board_best_median|usd0@@ |
| Worst cell | @@rescue_plan_of_record_worst_median|usd0@@ | @@rescue_gtm_minimum_uk_one_board_worst_median|usd0@@ |

**The boundary is set almost entirely by acquisition cost.** Read the grid across
a row and the price axis moves the number; read it down a column and the
acquisition axis decides whether there is a number to move.

**These are grid quantiles, not solved boundaries, and should not be read as
thresholds.** The highest anchor that clears anywhere on the plan-of-record grid
is @@rescue_plan_of_record_highest_cac_that_clears|num2@@ dollars and on the narrow-scope grid
@@rescue_gtm_minimum_uk_one_board_highest_cac_that_clears|num2@@; the true boundaries lie somewhere between those
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
| Plan of record | @@funding_plan_of_record_seed_round_size|usd0@@ | @@funding_plan_of_record_series_a_round_size|usd0@@ | @@funding_plan_of_record_series_b_round_size|usd0@@ | @@funding_plan_of_record_whole_horizon_round_size|usd0@@ |
| United Kingdom consumer only | @@funding_base_case_uk_only_seed_round_size|usd0@@ | @@funding_base_case_uk_only_series_a_round_size|usd0@@ | @@funding_base_case_uk_only_series_b_round_size|usd0@@ | @@funding_base_case_uk_only_whole_horizon_round_size|usd0@@ |
| Go-to-market minimum: five subjects, one board | @@funding_gtm_minimum_uk_one_board_seed_round_size|usd0@@ | @@funding_gtm_minimum_uk_one_board_series_a_round_size|usd0@@ | @@funding_gtm_minimum_uk_one_board_series_b_round_size|usd0@@ | @@funding_gtm_minimum_uk_one_board_whole_horizon_round_size|usd0@@ |
| One subject, one board | @@funding_one_subject_uk_one_board_seed_round_size|usd0@@ | @@funding_one_subject_uk_one_board_series_a_round_size|usd0@@ | @@funding_one_subject_uk_one_board_series_b_round_size|usd0@@ | @@funding_one_subject_uk_one_board_whole_horizon_round_size|usd0@@ |

**The round is sized on the plan of record, and the base case is stated beside
it.** They differ by enough that sizing on the base case would underfund the plan
the owner has actually described: @@funding_plan_of_record_whole_horizon_round_size|usdm@@ million against
@@funding_base_case_uk_only_whole_horizon_round_size|usdm@@ million across the horizon.

**The last column and the first three are computed by different rules, and the
difference is not small.** Each staged round carries six months of that stage's
own burn as buffer; the whole-horizon figure is the bare eightieth percentile of
the peak drawdown with no buffer at all. Added up, the plan of record's three
staged rounds come to @@funding_plan_of_record_staged_sum|usd0@@, which is
@@funding_plan_of_record_staged_less_whole|usd0@@ more than the whole-horizon figure, a ratio of
@@funding_plan_of_record_staged_over_whole|num3@@. **Raise against the staged number rather than the headline** if you want a
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
@@por_share_paths_trough_at_horizon_pct|num1@@ per cent of paths have their
trough in the last month of the horizon — still falling when the window closes.
Every figure in the table above is right-censored on that share of paths.
Section 7 gives the distribution.

@@share_paths_peak_funding_over_10m|pct1@@ per cent of individual paths need more than ten million dollars.

### The staging does not match the decisions

`out/funding_commitments.csv` sets each milestone's landing month beside the month
its spend *starts*, because content is built over the six months before it is
delivered and an entity is stood up before a market opens.

@@commitments_spend_starts_in_seed|int@@ of the file's
@@commitments_total|int@@ commitments have their spend starting inside the seed
window, among them the United States entity and its market counsel, the
information security certification, A-level content, the second and third United
Kingdom boards, the first sales representative and the go-to-market content build
itself. (An earlier draft introduced that list with a colon, as though it were
all of them; it is seven of the @@commitments_spend_starts_in_seed|int@@.) The Series A
does not buy them; it refinances decisions the seed already committed to. The
file names @@commitments_entity_count|int@@ entity set-ups —
@@commitments_entity_names|raw@@ — of which
@@commitments_entities_paid_by_seed|int@@ is paid for out of the seed window; an
earlier draft named an India entity, which this model never stands up because
India is an institution market here, and called both entities seed-window.
@@commitments_paid_by_an_earlier_round_than_they_land_in|int@@ commitment lands in the
Series A window with its spend starting before that round opens: all four United
Kingdom boards live at month 18, built from month 12.
The rest-of-English-speaking market at month 24 starts its build at month 18,
exactly when the Series A opens, so by the file's own test it does not qualify.

**A round of @@funding_plan_of_record_seed_round_size|usd0@@ dollars is not a seed round.** Calling it one and
then discovering at month 18 that the Series A is paying for choices made at month
12 is the failure mode that staging is supposed to prevent.

---

## 12. The decisions that are yours, not the model's

**The ordering of the top two depends on which statistic you rank on, and nothing
here can settle that for you.** On the capital requirement at the eightieth
percentile, scope comes first: @@funding_por_less_gtm_minimum_whole_horizon|usd0@@
against the price anchor's @@anchor_software_minus_tutoring_peak_funding_p80|usd0@@.
On terminal cash at the mean the anchor comes first,
@@anchor_tutoring_minus_software_terminal_cash_mean|usd0@@ against the same scope
reduction's @@delta_gtm_minimum_terminal_cash_abs|usd0@@, and both comparisons are
now against the go-to-market minimum rather than against two different scope
reductions. Both statistics are published so that the disagreement is visible
rather than resolved by whichever one was quoted.

**Do not read those two figures against each other.** One is a capital
requirement and one is a cash spread; the first is bad when large and the second
good when large, and they happen to be close in magnitude, which makes the
comparison look meaningful. It is not. What the two lines above say is that scope
leads on capital and the anchor leads on terminal cash, each by a wide margin
within its own statistic, and that nothing here converts between them. Both
statistics carry the @@por_terminal_cash_mc_se_two_sigma|usd0@@ sampling interval
from the preamble before any of the priors are argued with.

Items 3 onward are grouped rather than ranked. An earlier draft said they were
ordered by terminal cash at the mean; they are not, and they are not ordered by
anything else either. Each carries its own figure, and the same caution about
which statistic you are reading applies to every one of them.

**Every figure below is feedback-off**, because `out/variants.csv` carries no
feedback-on version of the individual levers. The feedback loops cost
@@delta_por_feedback_on_terminal_cash_abs|usd0@@ dollars in total, so each lever here is optimistic by some
share of that. Read the ordering, not the levels, and read the ordering knowing
it moves with the statistic.

**1. How much scope to attempt before the first evidence arrives.** The plan of
record needs @@funding_plan_of_record_whole_horizon_round_size|usd0@@ against
@@funding_gtm_minimum_uk_one_board_whole_horizon_round_size|usd0@@ for the
go-to-market minimum, a spread of @@funding_por_less_gtm_minimum_whole_horizon|usd0@@
**on the capital requirement**. On terminal cash the same reduction is worth
@@delta_gtm_minimum_terminal_cash_mean|usd0@@ at the mean and
@@delta_gtm_minimum_terminal_cash_p50|usd0@@ on the median path. **Scope is much
the largest decision on the capital requirement and the third largest on terminal
cash**, behind the terminal-value residual and the price-anchor regime spread of
@@anchor_tutoring_minus_software_terminal_cash_mean|usd0@@. It is material on
both, which is the thing that changed.

Two earlier drafts said the opposite — that scope was dominant on capital and
minor on return — and the reason is worth stating, because it is the kind of
error this document exists to catch. The terminal-cash figure was being read off
the `ukonly` scenario, which drops the second market and the institution channel
but keeps the entire United Kingdom content escalation to eleven subjects. Its
content line is @@scenario_ukonly_total_content_cost_mean|usd0@@ against the
go-to-market minimum's @@scenario_gtm_minimum_total_content_cost_mean|usd0@@. On
terminal cash that scenario is worth @@delta_ukonly_terminal_cash_mean|usd0@@,
which is close to nothing and which the document duly called close to nothing.
The real scope reduction is worth
@@scope_gtm_over_ukonly_terminal_cash|num0@@ times that. So the capital figure was a
comparison against the real scope reduction, the terminal-cash figure was a
comparison against a different and much smaller one, and the conclusion drawn
from putting them side by side was an artefact of the mismatch rather than a
property of the business. The ladder now has three rungs and they are compared
like for like:

| Scope | Terminal cash, mean | Terminal cash, median | Peak funding p80 | Content cost |
|---|---|---|---|---|
| Plan of record | @@scenario_por_terminal_cash_mean|usd0@@ | @@scenario_por_terminal_cash_p50|usd0@@ | @@scenario_por_peak_funding_p80|usd0@@ | @@scenario_por_total_content_cost_mean|usd0@@ |
| Content frozen at go-to-market, markets unchanged | @@scenario_por_content_frozen_terminal_cash_mean|usd0@@ | @@scenario_por_content_frozen_terminal_cash_p50|usd0@@ | @@scenario_por_content_frozen_peak_funding_p80|usd0@@ | @@scenario_por_content_frozen_total_content_cost_mean|usd0@@ |
| United Kingdom only, content unchanged | @@scenario_ukonly_terminal_cash_mean|usd0@@ | @@scenario_ukonly_terminal_cash_p50|usd0@@ | @@scenario_ukonly_peak_funding_p80|usd0@@ | @@scenario_ukonly_total_content_cost_mean|usd0@@ |
| Go-to-market minimum, both reduced | @@scenario_gtm_minimum_terminal_cash_mean|usd0@@ | @@scenario_gtm_minimum_terminal_cash_p50|usd0@@ | @@scenario_gtm_minimum_peak_funding_p80|usd0@@ | @@scenario_gtm_minimum_total_content_cost_mean|usd0@@ |

**The two middle rows are the point, and they say something the write-up had no
way to say before.** Freezing the United Kingdom content schedule while keeping
every market takes @@delta_por_content_frozen_total_content_cost_abs|usd0@@ off
the content line; dropping every market but the United Kingdom while keeping the
content schedule takes @@delta_ukonly_total_content_cost_abs|usd0@@ off it. Both
are large, and the content escalation is the larger of the two. On the capital
requirement they are worth almost the same — freezing content
@@delta_por_content_frozen_peak_funding_p80_abs|usd0@@, dropping markets
@@delta_ukonly_peak_funding_p80_abs|usd0@@ — and together with the rest of the
reduction they come to @@delta_gtm_minimum_peak_funding_p80_abs|usd0@@. On
terminal cash they are not close: freezing content is worth
@@delta_por_content_frozen_terminal_cash_mean|usd0@@ and dropping markets
@@delta_ukonly_terminal_cash_mean|usd0@@, a factor of
@@scope_content_freeze_over_market_drop_terminal_cash|num0@@.

**The two decisions separate exactly on the content column, and that is checked
rather than eyeballed — but read what the check covers.** Foreign content
computed as the plan of record less the United Kingdom-only scenario is
@@scope_ladder_foreign_content_mean|usd0@@; computed as content-frozen less the
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
does decompose into @@scope_ladder_frozen_uk_content_mean|usd0@@ of content you
must build to go to market at all, @@scope_ladder_uk_escalation_mean|usd0@@ of
United Kingdom catalogue widening, and @@scope_ladder_foreign_content_mean|usd0@@
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
@@anchor_tutoring_minus_software_terminal_cash_mean|usd0@@ between its two states, and it costs a landing page.
It is already condition C1 in docs/09 and already milestone M1 in docs/11. The decision
is whether you will actually stop if it fails.

**3. Whether to run the institution channel at all inside this horizon.** Costs
@@delta_por_no_schools_terminal_cash_mean|usd0@@ here, and buys outcome evidence that this instrument cannot
value. docs/09 makes the case for it honestly and this model is not equipped to
answer it. You are.

**4. What the session allowance should be, and whether to enforce it.** The
allowance is set at @@const_SESSION_ALLOWANCE|int@@ sessions a month in `model.py` as a decision, and
@@por_mean_share_over_allowance_pct|num1@@ per cent of households exceed it. **Enforcing it costs
@@delta_por_allowance_enforced_terminal_cash_abs|usd0@@**, because the overage revenue lost exceeds the
inference cost saved.

That is the rare case where the commercial posture and the arithmetic point the
same way: the product exists for the struggling learner, the struggling learner
is the one who exceeds the allowance, and on these priors they are worth more in
overage than they cost in inference. The decision that remains yours is the
allowance level itself, which sets how much of that shows up as overage rather
than as plan price.

**5. Whether to bill through an app store.** Costs @@delta_por_appstore_terminal_cash_abs|usd0@@ and buys
distribution the model does not credit. docs/04 identifies app stores and payment
processors as the real chokepoint, which is an argument for a second relationship
rather than for or against the fee.

**6. Whether India is worth a statutory prohibition — and on these priors it is
not, which is the opposite of what this paragraph used to say.** Opening India
direct to parents **costs** @@delta_por_india_d2c_terminal_cash_abs|usd0@@ of
terminal cash over five years, @@delta_por_india_d2c_terminal_cash_p50_abs|usd0@@
on the median path, and **raises** the capital requirement at the eightieth
percentile by @@delta_por_india_d2c_peak_funding_p80|usd0@@. It loses money
because it carries an entity, market counsel, a content bank
(@@delta_por_india_d2c_total_content_cost_abs|usd0@@ of additional content cost),
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
moves the mean by @@delta_por_fx_sampled_terminal_cash_mean|usd0@@, which is small; what it changes is the
width of the distribution, not its centre. See LIMITS.md.

---

**And one that is not yours, which is why it is not on the list.** Whether United
Kingdom children's learner data may be processed in Bengaluru at all is a question
for counsel, not a decision for you. docs/05 flags it as a standard position not
confirmed for this fact pattern. If the answer forces the learner path onshore,
the Bengaluru cost base goes with it: @@delta_por_onshore_all_terminal_cash_abs|usd0@@ dollars of terminal cash
at the worst reading, @@delta_por_onshore_all_peak_funding_p80|usd0@@ on the capital requirement, and people
overtakes content as the largest cost line.

**It barely moves the sensitivity ordering at all.** The decomposition was run
under full onshoring and written to `out/sobol.csv` under the `onshore_all` run,
so this paragraph can be read off a file instead of asserted. On the capital
requirement, item count stays at rank
@@sobol_onshore_peak_funding_requirement_rank_of_items_per_unit|num0@@ — the
same rank it holds on the plan of record — and the United Kingdom salary driver
reaches rank @@sobol_onshore_peak_funding_requirement_rank_of_uk_gbp_yr|num0@@,
which is inside the top seven and outside the top three. Content drivers hold
@@sobol_onshore_peak_funding_requirement_content_drivers_in_top7|num0@@ of the
top seven, against
@@sobol_peak_funding_requirement_content_drivers_in_top7|num0@@ on the plan of
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
| `out/por_monthly.csv` | The monthly output of the published run: @@horizon_months|int@@ rows, every series as a mean, three percentiles and three band lines. |
| `out/por_paths.csv` | @@n_paths|int@@ rows: every per-path outcome and every driver value. |
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
| `out/provenance.csv` | Which `model.py` **and `harness.py`** each generating script last ran against, hashed together. `verify.py` fails the run if they disagree. |
| `out/harness_selftest.txt`, `out/suffix_selftest.txt` | The records of the three self-tests: both harness gates, and the column-naming discipline. |
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
