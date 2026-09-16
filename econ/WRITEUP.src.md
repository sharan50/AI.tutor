# AI.tutor: the economics, as an instrument rather than a forecast

**Seed @@seed|int@@. Run date @@run_date|raw@@. @@n_paths|int@@ paths, @@horizon_months|int@@ monthly steps, United States dollars.**

Every number in this document was produced by a simulation whose every input is a
prior. Not one input is a measurement. Nothing here is a forecast, and the levels
are not evidence. What a simulation on priors is good for is the **ordering of
the levers**, and that ordering is what this document is for.

A figure re-derived from a different seed is a different number. The seed and the
date are quoted wherever a number appears for that reason.

---

## 1. The three things worth knowing

**One. The plan of record is not a seed-stage plan.** Sized at the eightieth
percentile of need, it requires @@funding_plan_of_record_whole_horizon_round_size|usdm@@ million dollars across the
horizon, against @@funding_base_case_uk_only_whole_horizon_round_size|usdm@@ million for a United Kingdom consumer business alone and
@@funding_gtm_minimum_uk_one_board_whole_horizon_round_size|usdm@@ million for the go-to-market minimum: five GCSE subjects, one board,
one market, no institution channel. The first eighteen months of the plan of
record alone need @@funding_plan_of_record_seed_round_size|usdm@@ million.

**Two. About @@por_share_demand_independent_pct|num1@@ per cent of the cost base is committed before demand can say
much about it.** Content is @@por_share_content_cost_pct|num1@@ per cent of total modelled cost, people
@@por_share_people_beng_cost_pct|num1@@ per cent in Bengaluru plus @@por_share_people_uk_cost_pct|num1@@ in the United Kingdom, and step
costs @@por_share_step_cost_pct|num1@@ per cent. Acquisition, which does depend on demand, is
@@por_share_cac_spend_pct|num1@@ per cent. Inference, the cost docs/06 builds up so carefully, is
@@por_share_inference_cost_pct|num1@@ per cent.

"About" is doing work in that sentence and it is meant to. Part of the United
Kingdom people line is not demand-independent: the safeguarding rota steps at
@@const_ROTA_EXTENDED_AT|usd0@@ and again at @@const_ROTA_24_7_AT|usd0@@ active households, and those steps fire on
most paths. The overwhelming majority of the @@por_share_demand_independent_pct|num1@@ per cent is fixed; a
slice of it is not, and LIMITS.md item 5 says which. This is why **no single driver gets the median path whole**: every break-even
solved in section 10 against a cash target is unbracketed, because the money is
spent whether or not anyone buys. Four solves against the profitability target do
bracket, and section 10 gives them.

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

So the direct-to-parent variant, worth @@delta_por_india_d2c_terminal_cash_abs|usd0@@ dollars of terminal cash on
the mean, is compared against **no India business at all** rather than against an
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
verifies again. The result is written to `out/harness_selftest.txt`.

Every script that RUNS THE MODEL goes through `harness.load()`: the sensitivity,
the scenarios, the funding sizing, the break-even solves, the rescue grid, the
cohort counterfactuals, the omissions pricing and the parameter dump. That is what
makes them run the published code rather than a restatement of it.

Three scripts deliberately do not, and must not. `figures.py`, `render.py` and
`verify.py` read the CSVs and never import the model, so that a figure quoted in
the prose is checked against what was written to disk rather than against what the
code would produce if asked again.

**Every mechanism that a variant adds must reproduce the base run exactly when it
is switched off, and every parameter a variant needs is drawn outside the
published random stream.** @@offtest_mechanism_count|int@@ mechanisms are tested this way on every run: the feedback loops, the
app-store fee, sampled foreign exchange, the creator licence, the onshoring
switch and the terminal-value residual. Every one reproduces the base character
for character when off.

Because no draw happens inside the month loop, the streams cannot diverge between
scenarios. That is shown rather than asserted: `out/variants.csv` carries, for
every scenario, the rank correlation of per-path terminal cash against the base
and the mean absolute per-path change beside the change in the mean. Unmatched
paths would collapse the first and inflate the second.

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
saturate anything; that is why the pooled figure is the one to plan against. The
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
contribution the ratio is very much worse, and on the median path it is
negative.

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
better on @@share_paths_year10_at_least_doubles|pct1@@ per cent of paths.

**The summer is not where it goes, and an earlier draft of this passage said it
was, following docs/10's own caveat rather than the model.** Pinning the summer
lapse to zero and progression to one, which removes the summer entirely, lifts
the ratio only to @@year10_ratio_with_no_summer_at_all|num2@@. Pinning in-term churn to the bottom of its
prior range instead, with the summer left alone, gives @@year10_ratio_with_churn_at_its_floor|num2@@. Only
pinning both recovers it, at @@year10_ratio_with_no_summer_and_floor_churn|num2@@. **It is in-term churn, not the
summer, that is eating the Year 10 advantage**, and docs/10's caveat sends the
owner to measure the wrong thing first.

There is a larger problem sitting underneath those numbers, and it is in
LIMITS.md: an examination-year household is retained @@retained_months_exam_year_mean|num2@@ months in this
model, against a product sold as a cycle plan running to the last paper. The
average customer of a nine-month plan does not finish a cycle. That follows from
the churn prior, which nothing has measured.

### The allowance is sold but not enforced

@@por_mean_share_over_allowance_pct|num1@@ per cent of active households exceed the session allowance being
sold to them. That is a household-month weighted share WITHIN each path, then a
plain mean across paths, so a path with a hundred households and a path with one
count equally in it.

The allowance is not enforced. Sessions above it are delivered and cost money, and
they are billed only up to two and a half times the allowance. So the omission
sits on one side only and its sign is known rather than assumed away: above the
billing cap, cost runs and revenue does not. Enforcing the allowance instead is
worth
@@delta_por_allowance_enforced_terminal_cash_mean|usd0@@ dollars of terminal cash on the mean. Nothing here was
measured: that is a difference between two simulations on invented priors. What
it is, is a question the instrument can now answer rather than argue about.

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

Three readings, each of which contradicts something in the vault or in the usual
telling.

**Content is the largest line, not acquisition.** docs/10 is right that content
does not enter the payback ratio, because it does not scale with learners. It is
nonetheless the largest single call on cash in a plan that builds this much of it.
On @@share_paths_content_exceeds_acquisition|pct1@@ per cent of individual paths content exceeds acquisition, and on
@@share_paths_content_is_largest_line|pct1@@ per cent it exceeds both acquisition and people, so this is not an
artefact of averaging.

**The load-bearing assumption in docs/10 holds.** That document assumes variable
cost per month is small relative to price, and says plainly that if it is not, the
sensitivity ordering reverses and cost engineering becomes the priority. Inference
is @@por_share_inference_cost_pct|num1@@ per cent of total cost under these priors. The row does not reverse.

**Age assurance, the condition the route decision turns on, is
@@por_share_verif_cost_pct|num1@@ per cent of cost.** That is not an argument that condition C2 does not
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
published. The central band line sits at the @@por_band_central_placement_terminal|pct1@@ percentile of the real
per-path distribution of cumulative cash at the end of the horizon, and between
the @@por_band_central_placement_min|pct1@@ and @@por_band_central_placement_max|pct1@@ percentiles across the months from go-to-market
onward. It moves between scenarios as well: on the software-anchored scenario it
ends at @@band_placement_por_anchor_software_central_terminal|pct1@@, and on the tutoring-anchored one at
@@band_placement_por_anchor_tutoring_central_terminal|pct1@@.

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
| Minimum of the mean cumulative cash line, USD | @@por_min_of_mean_cash_line|usd0@@ |
| The month it reaches it | @@por_min_of_mean_cash_month|int@@ |
| Mean of each path's own minimum, USD | @@por_mean_of_per_path_min|usd0@@ |
| Ratio of the two | @@por_trough_understatement_ratio|num4@@ |
| **The headline is shallower by** | **@@por_trough_understatement_pct|num1@@ per cent** |

The per-path distribution beside it: tenth percentile @@por_trough_p10|usd0@@, ninetieth
@@por_trough_p90|usd0@@, mean month of the trough @@por_mean_trough_month|num1@@. The averaged line reaches its
low at month @@por_min_of_mean_cash_month|int@@; individual paths reach theirs, on average, at month
@@por_mean_trough_month|num1@@. Planning to the averaged line plans to a trough that is
@@por_trough_understatement_pct|num1@@ per cent shallower and later than the one a given path actually meets.

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

The practical reading: **work on acquisition and the price anchor to make the
business exist; work on content cost to make it fundable.** They are different
programmes of work and this instrument says they are not substitutes.

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
| Foreign exchange sampled rather than fixed | @@delta_por_fx_sampled_terminal_cash_mean|usd0@@ | @@delta_por_fx_sampled_terminal_cash_p50|usd0@@ | @@delta_por_fx_sampled_peak_funding_p80|usd0@@ | @@delta_por_fx_sampled_sign_agrees_mean_and_median|int@@ |
| India opened direct to parents | @@delta_por_india_d2c_terminal_cash_mean|usd0@@ | @@delta_por_india_d2c_terminal_cash_p50|usd0@@ | @@delta_por_india_d2c_peak_funding_p80|usd0@@ | @@delta_por_india_d2c_sign_agrees_mean_and_median|int@@ |
| The allowance enforced | @@delta_por_allowance_enforced_terminal_cash_mean|usd0@@ | @@delta_por_allowance_enforced_terminal_cash_p50|usd0@@ | @@delta_por_allowance_enforced_peak_funding_p80|usd0@@ | @@delta_por_allowance_enforced_sign_agrees_mean_and_median|int@@ |

The plan of record itself is @@scenario_por_terminal_cash_mean|usd0@@ on the mean and
@@scenario_por_terminal_cash_p50|usd0@@ on the median path. The gap between those two numbers is
the reason the second column exists.

Five readings.

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
whole or brings the capital requirement under ten million dollars, on either
scope. That is not a modelling failure; it is the answer, and the reason is in
the cost split. Content is @@por_share_content_cost_pct|num1@@ per cent of cost, people @@por_share_people_beng_cost_pct|num1@@ per cent in
Bengaluru plus @@por_share_people_uk_cost_pct|num1@@ in the United Kingdom, and step costs @@por_share_step_cost_pct|num1@@ per cent.
A driver that acts only on demand cannot move a cost base that demand does not
touch. (The one qualification: the United Kingdom safeguarding rota steps on
active households, so part of that people line does respond to demand. See
LIMITS.md item 5.)

### The four that do solve

All four are on the same target, half of all paths running three consecutive
cash-positive months, and all four are on the two drivers section 8 says decide
whether the venture exists at all. **That is not a coincidence; it is the
instrument agreeing with itself.**

| Scope | Driver | Break-even | Prior median |
|---|---|---|---|
| Plan of record | acquisition anchor | @@breakeven_at_plan_of_record_cac_anchor_usd_share_reaching_profitability|num2@@ USD | @@por_cac_anchor_median|num2@@ |
| Plan of record | tutoring-anchored price | @@breakeven_at_plan_of_record_price_uk_tut_gbp_share_reaching_profitability|num2@@ GBP a month | @@driver_price_uk_tut_gbp_mode|num2@@ |
| Go-to-market minimum | acquisition anchor | @@breakeven_at_gtm_minimum_uk_one_board_cac_anchor_usd_share_reaching_profitability|num2@@ USD | @@por_cac_anchor_median|num2@@ |
| Go-to-market minimum | tutoring-anchored price | @@breakeven_at_gtm_minimum_uk_one_board_price_uk_tut_gbp_share_reaching_profitability|num2@@ GBP a month | @@driver_price_uk_tut_gbp_mode|num2@@ |

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

**This changes the instruction section 10 gives, not its level.** The question is
not "what rescues the plan", to which the answer is nothing. It is "at what
acquisition cost, or at what price, does half of this become viable", and the
instrument answers it on both scopes.

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

@@share_paths_peak_funding_over_10m|pct1@@ per cent of individual paths need more than ten million dollars.

### The staging does not match the decisions

`out/funding_commitments.csv` sets each milestone's landing month beside the month
its spend *starts*, because content is built over the six months before it is
delivered and an entity is stood up before a market opens.

Every commitment through month 18, including the United States and India entities,
foreign counsel, the information security certification, A-level content and the
second and third United Kingdom boards, has its spend starting inside the seed
window. The Series A does not buy them; it refinances decisions the seed already
committed to. One commitment lands in the Series A window with its spend starting before that
round opens: all four United Kingdom boards live at month 18, built from month 12.
The rest-of-English-speaking market at month 24 starts its build at month 18,
exactly when the Series A opens, so by the file's own test it does not qualify.

**A round of @@funding_plan_of_record_seed_round_size|usd0@@ dollars is not a seed round.** Calling it one and
then discovering at month 18 that the Series A is paying for choices made at month
12 is the failure mode that staging is supposed to prevent.

---

## 12. The decisions that are yours, not the model's

**The ordering of the top two depends on which statistic you rank on, and nothing
here can settle that for you.** On the capital requirement at the eightieth
percentile, scope comes first: @@funding_por_less_gtm_minimum_whole_horizon|usd0@@ against the price anchor's
@@anchor_tutoring_minus_software_peak_funding_p80|usd0@@. On terminal cash at the mean, the anchor comes first:
@@anchor_tutoring_minus_software_terminal_cash_mean|usd0@@ against a scope difference the same statistic puts at
@@delta_ukonly_terminal_cash_abs|usd0@@. The two statistics disagree by more than an order of
magnitude and they disagree about the order. Both are published so that the
disagreement is visible rather than resolved by whichever one was quoted.

Items 3 onward are ordered by terminal cash at the mean, and the same caution
applies to every one of them.

**Every figure below is feedback-off**, because `out/variants.csv` carries no
feedback-on version of the individual levers. The feedback loops cost
@@delta_por_feedback_on_terminal_cash_abs|usd0@@ dollars in total, so each lever here is optimistic by some
share of that. Read the ordering, not the levels, and read the ordering knowing
it moves with the statistic.

**1. How much scope to attempt before the first evidence arrives.** The plan of
record needs @@funding_plan_of_record_whole_horizon_round_size|usd0@@ against @@funding_gtm_minimum_uk_one_board_whole_horizon_round_size|usd0@@ for the
go-to-market minimum, a spread of @@funding_por_less_gtm_minimum_whole_horizon|usd0@@ **on the capital
requirement**. On terminal cash the nearest published comparison is the United
Kingdom-only scenario, which the same statistic puts at @@delta_ukonly_terminal_cash_mean|usd0@@,
close to nothing. **Scope is the dominant decision on the statistic that sizes
rounds and a minor one on the statistic that measures return**, and you are
entitled to know that before acting on it.

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
@@por_mean_share_over_allowance_pct|num1@@ per cent of households exceed it. Enforcing is worth
@@delta_por_allowance_enforced_terminal_cash_mean|usd0@@. The number is small; the commercial posture it implies,
toward the struggling learner the product exists for, is not.

**5. Whether to bill through an app store.** Costs @@delta_por_appstore_terminal_cash_abs|usd0@@ and buys
distribution the model does not credit. docs/04 identifies app stores and payment
processors as the real chokepoint, which is an argument for a second relationship
rather than for or against the fee.

**6. Whether India is worth a statutory prohibition.** Direct to parents is worth
@@delta_por_india_d2c_terminal_cash_abs|usd0@@ over five years against DPDP section 9(3). The institution
route in India carries no such conflict, and **this instrument does not model it**,
so the figure is the prohibition's price and not a comparison between the two
routes in. See section 2.

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

**It re-ranks the sensitivity; it does not invert it.** Running the decomposition
under full onshoring moves a United Kingdom salary driver into the top three on
capital and pushes item count down, but content drivers still hold most of the
top seven and section 8's instruction survives with a people driver inserted. An
earlier draft of this paragraph said it inverted the ordering. It does not, and
saying so was the kind of overstatement this document is supposed to catch. It
is still the largest thing a letter to counsel could resolve. It is X8 in
OPEN_ITEMS.md.

---

## 13. Where to look

| File | What it holds |
|---|---|
| `model.py` | Drivers, mechanisms, month loop. Every driver's note says what anchors its range, or that nothing does. |
| `harness.py` | The character-for-character gate. Every script that runs the model goes through it. |
| `out/por_monthly.csv` | The monthly output of the published run: @@horizon_months|int@@ rows, every series as a mean, three percentiles and three band lines. |
| `out/por_paths.csv` | @@n_paths|int@@ rows: every per-path outcome and every driver value. |
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
disk.

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
absent cost lines, off-tests and driver ranks rather than leaving them to prose.
Run the verifier anyway, because it catches the other kind of error.
