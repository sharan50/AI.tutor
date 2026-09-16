# Limits: the checklist, item by item

**Seed @@seed|int@@, run date @@run_date|raw@@.** Every item of the twenty-four-point review
checklist the owner supplied with the instruction for this work, answered
explicitly, including where the answer is clean. That checklist is not in
`BUILD_BRIEF.md`, whose part 4 is a different list, of nine unverified legal and
commercial assumptions; it came with the request and is reproduced by its item
numbers here. Items that are not clean carry
the number they would move and by how much.

Three verdicts are used. **Clean** means the defect is not present. **Clean now**
means it was present, was found, and was fixed; the fix is in `CHANGELOG.md` with
what it moved. **Not clean** means it is still there, and the entry says what it
costs.

---

## Revenue

### 1. Consumption tax: **clean**

There is a tax term on the revenue side in every market. United Kingdom VAT at @@const_VAT_UK_pct|num0@@
per cent and Indian GST at @@const_GST_IN_pct|num0@@ per cent are statutory constants; the United States
effective rate is a sampled driver between @@driver_us_sales_tax_eff_low_pct|num0@@ and @@driver_us_sales_tax_eff_high_pct|num1@@ per cent,
because state treatment of software subscriptions varies; the
rest-of-English-speaking bucket carries a blended @@const_ROW_TAX_pct|num0@@ per cent, which is a stated
prior, not a rate.

**Quoted prices are read as gross, that is, tax-inclusive.** Net revenue is the
gross price divided by one plus the rate. Over the horizon that removes
@@por_total_tax_collected_mean|usd0@@ dollars, or @@por_tax_share_of_gross_pct|num1@@ per cent of gross consumer
revenue. On the United Kingdom alone at @@const_VAT_UK_pct|num0@@ per cent it removes a sixth.

**The other reading, quantified.** If the quoted prices were net and tax were added
on top, revenue over the horizon would be higher by that whole line,
@@por_total_tax_collected_mean|usd0@@ dollars. That is @@por_tax_share_of_gross_pct|num1@@ per cent of GROSS, and because it
would be added to net rather than removed from gross it is @@por_tax_share_of_net_pct|num1@@ per cent MORE
REVENUE, which are two different percentages of two different denominators. It
would reduce the peak funding requirement by approximately the same cash amount.

Institution prices are treated the other way round, as net of VAT, because that is
the convention a business-to-business price is quoted in. The two conventions are
deliberately different and both are in `model.py`.

### 2. Revenue matches the pricing decision: **clean**

Revenue is not users times price. It is an examination-cycle plan billed monthly
plus metered overage: `price + billed_overage × overage_price`, where the overage
price is itself a sampled fraction of the plan price divided by the allowance.
Billed overage is the expectation of the gamma tail above the allowance, less the
tail above the billing cap, computed per path from a sampled mean and coefficient
of variation of sessions per household.

### 3. Allowance and overage: **clean now; the scenario measured the wrong threshold until round 2**

Not "neither". The allowance is **sold but not enforced**: sessions above it are
delivered and cost money. Overage **is billed**, up to @@const_OVERAGE_CAP_MULT|num1@@ times the
allowance. Above that cap, cost runs and revenue does not, so the omission sits on
one side only and its sign is known.

**The scenario that priced enforcement was measuring the wrong threshold until
round 2.** It truncated delivery at the billing cap, @@const_OVERAGE_CAP_MULT|num1@@ times the
allowance, rather than at the allowance itself, so it cut off a level almost no
household reaches and left the overage revenue in place. It now enforces the
allowance and removes the overage line with it, which is what the decision
actually is. See `CHANGELOG.md` 2.3.

@@por_mean_share_over_allowance_pct|num1@@ per cent of active households exceed the allowance being sold to
them. That is a household-month weighted share within each path and then a plain
mean across paths, so a path with a hundred households and a path with one count
equally in it.

**Enforcing the allowance destroys @@delta_por_allowance_enforced_terminal_cash_abs|usd0@@ dollars of terminal cash**,
because the overage revenue lost is larger than the inference cost saved. Before
round 2 this scenario reported a small gain, from truncating delivery at the
billing cap rather than at the allowance.

### 4. Foreign exchange: **not clean, by instruction**

Rates are **fixed**: @@const_FX_GBP_USD|num2@@ dollars to the pound and @@const_FX_INR_USD_inverse|num1@@ rupees to the dollar,
at the owner's explicit instruction. That is a decision, not a draw, and it means
this item cannot be clean.

**What it would move, and the honest answer is "nothing measurable, and that is
partly the scenario's fault".** The `por_fx_sampled` scenario replaces the
sterling rate with a sampled one, drawn outside the published stream so the paths
stay matched. Terminal cash moves by
@@delta_por_fx_sampled_terminal_cash_mean|usd0@@ dollars on the mean. **That is
not "small", it is zero**: the delta is @@delta_por_fx_sampled_t_stat|num2@@
paired standard errors from zero, so at another seed it would carry a different
sign. (A round-four draft reached the same conclusion by comparing against the
*unpaired* standard error of the base mean, which is several times too large for
a paired comparison — the right conclusion from the wrong number, one paragraph
after this document explains the paired-versus-unpaired distinction for the
demand shock.) The peak funding requirement at the eightieth percentile
moves from @@por_peak_funding_p80|usd0@@ to
@@scenario_por_fx_sampled_peak_funding_p80|usd0@@. **The exposure is in the
width, not the centre**, which is exactly what fixing a rate hides: fixed rates do
not remove the risk, they remove the evidence of it.

**Two reasons the scenario understates even so, one of which round four fixed.**
Content is the largest pound-denominated cost in the model — examiner rates in
pounds an hour, authoring in pounds an item — and it used to sit **outside** the
exposure while the much smaller United Kingdom people line sat inside it, so the
scenario priced sterling risk without its largest natural hedge. It is inside now.
What remains: the rupee exposure is not sampled at all, and in fact `FX_INR_USD`
is a **dead constant** — no line in `model.py` reads it, because Bengaluru
salaries and support are drawn directly in dollars from their own priors. So the
rupee exposure does not have a fixed rate; it has no term whatever. The constant
is still published in `out/constants.csv` and still described in this document,
which is why it is named here rather than quietly deleted.

**A second simplification sits inside the same line.** United States prices are
set in dollars and do not move when sterling moves, which is right. India and the
rest-of-English-speaking prices are derived from the sterling base price and so do
move with sterling, which is wrong: those would be set in local currency. The
error exists only in the sampled-rate scenario, because at a fixed rate nothing
moves at all, and it is confined to two markets that are a minority of consumer
revenue.

---

## Cost

### 5. Step costs modelled as slopes: **not clean, one is missing**

Modelled as genuine steps: foreign entity set-up and its annual compliance, per
market; counsel per jurisdiction; the United Kingdom Article 27 representative;
DPIA maintenance and audit readiness; information security certification, first
award and annual renewal; premises above eight heads; the safeguarding rota, which
steps at @@const_ROTA_EXTENDED_AT|num0@@ active households and again at @@const_ROTA_24_7_AT|num0@@ where an
out-of-hours rota is about three and a half further posts; the general and administrative schedule; and
the field sales ramp.

Modelled as a slope where it should be lumpy: **content headcount**, which is
computed continuously as work in the coming year divided by what one head
sustains. Real hiring is lumpy and lags. This understates the cost of a fast ramp.

**Missing entirely: a night rota.** United Kingdom study time is roughly 16:00 to
21:00, which is 21:30 to 02:30 in Bengaluru. The product's busiest hours are the
build base's night, and there is no shift premium anywhere in the cost base.
Priced in `out/omissions.csv` at @@omission_out_of_hours_operations_rota_low|usd0@@ to
@@omission_out_of_hours_operations_rota_high|usd0@@ dollars from the United Kingdom go-to-market month to
the end of the horizon, four and a half years rather than five, which is up to
@@omission_out_of_hours_operations_rota_share_high_pct|num2@@ per cent of the modelled cost base.

### 6. A cost that scales per market, per shift or per institution: **clean, except the shift**

Per institution: `school_onboard_cost`, priced at three quarters of a United
Kingdom person-week per school for the data processing agreement, the security
review and onboarding. Per market: entity annual compliance and counsel, charged
only where a market is actually opened. Per shift: missing, as item 5 says.

### 7. Does a second market cost more per unit: **clean, and it is not almost nothing**

A second United Kingdom board reuses between @@driver_board_reuse_low_pct|num0@@ and @@driver_board_reuse_high_pct|num0@@ per cent of the
items for the same subject and level, sampled; the remainder is built. A foreign
curriculum reuses only @@driver_market_reuse_low_pct|num0@@ to @@driver_market_reuse_high_pct|num0@@ per cent. Neither is near one, so the expansion case is not
being granted for free the thing it is asking to buy.

That this matters is visible in the sweep: pinning `board_reuse` from its fifth to
its ninety-fifth percentile swings terminal cash by @@pinned_board_reuse_swing_abs|usd0@@ dollars,
and `market_reuse` is ranked @@sobol_peak_funding_requirement_rank_of_market_reuse|int@@ on the capital target.

### 8. A cost with no term at all: **not clean, @@omission_line_count|int@@ named and priced**

Grepped for. `out/omissions.csv` names each absent line and prices it from a
figure the model already carries. The list is rendered from the file rather than
typed, because a hand-kept copy of it drifted from the file twice:
@@omission_line_names|raw@@.

@@omission_zero_line_count|int@@ of them are priced at zero and written down
anyway, because a zero recorded is not the same as a line left out:
@@omission_zero_line_names|raw@@.

They are zero for four different reasons. The breakdown named two of them for
several rounds, then three, and the three-way version still accounted for only
seven of the eight: "organic and referred acquisition" appeared in the list of
zero lines above and in none of the groups below it, which is the same
hand-kept-list failure this item is about. **Four are genuine zeros**: no
scenario here returns a taxable
trading profit, the expansion is across English-speaking curricula by decision,
nothing here puts a probability on enforcement, and examiner supply is a quantity
question rather than a cost. **One is not a cost at all** — institution revenue
lost to annual recognition is a timing artefact that makes the channel look worse
than the plan describes, and it is in the list because a zero recorded is better
than a line left out. **One is a revenue mechanic rather than a cost**: there is
no unpaid channel anywhere in the model, so every household in it is bought, and
organic and referred acquisition is carried at zero not because it is small but
because the model has no term for it at all. That is the one of the eight most
likely to be materially wrong in the company's favour. **The remaining two** are zero only as *cost* lines,
because they are retention mechanics rather than costs, and their size is
published separately in `out/sized_omissions.csv`:
scaling both churn drivers by @@retention_stress_churn_pct|num0@@ per cent costs
@@retention_stress_terminal_cash_cost|usd0@@ dollars of terminal cash, which is
@@retention_stress_share_of_cost_pct|num1@@ per cent of the modelled cost base.
That scale is a prior on how much of the book a reminder-and-easy-exit regime
and involuntary churn move between them, not a measurement of either.

**In total the absent lines are @@omission_total_of_every_absent_line_low|usd0@@ to
@@omission_total_of_every_absent_line_high|usd0@@ dollars, or @@omission_total_of_every_absent_line_share_high_pct|num2@@ per cent of the modelled
cost base at the top of the range**, up from about an eighth before round 3 added
specification change, which is the largest single line in the file. They deepen the hole. They do
not reverse the ordering in section 8 of the write-up, and the largest of them
pushes the same way: specification change acts on the content line, so closing it
would make content a larger share of cost rather than a smaller one. **But a
fifth of the cost base sitting outside the model is not a footnote**, and a
reader who takes the absolute levels from this document rather than the ordering
is being misled by more than they were two rounds ago.

**One more, and it is the important one: the creator licence.** D4 makes named
educators the wedge and D14 requires named presets from day one, and the published
run charges nothing for them, because D5 describes a one-page name-and-likeness
agreement and the vault has never established what a creator charges to sign it.
Rather than invent the figure, the `por_creator_fees` scenario prices both limbs,
a fixed annual minimum per creator and a share of the revenue their audience
brought: @@delta_por_creator_fees_terminal_cash_mean|usd0@@ dollars of terminal cash. **The published run
assumes creators sign for nothing.** That assumption is now visible.

---

## The base case

### 9. The base case silently containing a rejected scenario: **clean now**

It did. `headcount()` hired field sales representatives and `step_costs_usd()`
paid for United States and India entities, foreign counsel and a security
certification in every scenario, including the United Kingdom-only comparator that
opens none of them. Both now gate on the configuration. See `CHANGELOG.md` 0.2 for
what it moved.

The plan of record is charged for every market and channel it opens, and the
schedules that drive content cost are gated the same way.

### 10. Like-for-like comparators: **clean in the file; it was the prose that was not, and it cost a headline conclusion**

Every scenario in `out/variants.csv` shares one drawn driver dictionary and
differs only in named switches. A scenario that carries a market or a channel is
charged its entities, its counsel, its content build and its people.

**It took three rounds to get here, and the third was the expensive one.** Round
1 found the United Kingdom-only comparator hiring sales representatives and
paying for entities it never opens. Round 2 found the institution channel charged
an India content bank that nothing in the model ever bills, which was most of
what "the cost of Route B" appeared to be. Both were defects in the model.

**Round 3 found the same defect one level up, in the prose rather than the
code.** Owner decision 1 quoted a capital figure measured against the
go-to-market minimum beside a terminal-cash figure measured against the United
Kingdom-only scenario and read the pair as one finding about scope. Both scenarios
are internally like for like; the *comparison between the two comparisons* was
not. The conclusion that scope is dominant on capital and minor on return was an
artefact of it, and it was set in bold and repeated. Section 12 now has the
three-rung ladder, every rung measured on the same four statistics, and a
conclusion that is neither the old one nor its mirror: scope is much the largest
decision on capital and the third largest on terminal cash, and it is two
decisions rather than one, because content schedule and market count behave
differently on the two statistics. All three rounds are in `CHANGELOG.md`.

**One comparator is still not like for like and is labelled where it is used.**
The United Kingdom-only scenario drops two consumer markets — the United States
and the rest of the English-speaking world, India being an institution market
here rather than a consumer one — AND the institution channel, so it cannot be
read as a measure of market scope alone. It also keeps the whole United Kingdom
content escalation, which is the larger of the two things "scope" means in this
document; section 12 of the write-up now puts all three rungs of the scope ladder
side by side rather than reading this scenario as the scope reduction.

One comparison in the write-up is **not** like for like and is labelled as such:
the institution channel is charged its costs and credited its revenue, but not
credited the outcome evidence that docs/09 says is the only durable moat. The
instrument cannot value evidence. That is a limit of the instrument.

### 11. The same random numbers: **clean and tested; the passage reporting it was not**

No draw happens inside the month loop, so scenario branches cannot make the
streams diverge. Every variant reuses the base driver dictionary, and every new
parameter is drawn from a separate auxiliary seed.

Tested rather than asserted: `test_off_reproduces_base()` runs each mechanism
switched off and requires the rebuilt monthly CSV text to equal the base
character for character, then runs each switched on and requires that it does
not. All @@offtest_mechanism_count|int@@ pass both ways on every run of
`variants.py`. The list is rendered from `out/offtest.csv` rather than typed,
because a hand-kept copy of it named six against a count of seven:
@@offtest_mechanism_names|raw@@.

Matching is also measured, not just argued. `out/variants.csv` carries for every
scenario the rank correlation of per-path terminal cash against the base and the
mean absolute per-path change beside the change in the mean. Unmatched paths
would collapse the first and inflate the second.

**This is where an earlier draft was wrong, in the passage whose whole point was
that matching is measured.** It named two scenarios as the loosest and the
tightest and neither bound was the bound in the file. Across the scenarios that
only flip a switch the correlation runs from @@pathwise_spearman_min_excluding_dependence|num4@@ to @@pathwise_spearman_max|num4@@.
The two dependence scenarios sit at @@pathwise_spearman_min|num4@@ and above, and that is correct
behaviour rather than a defect: Iman-Conover reordering changes which path holds
which driver value, so it preserves the marginals exactly and path identity not
at all. They are comparable to the base in distribution, not path by path, and
the write-up says so where it uses them.

---

## Acquisition and growth

### 12. Anchor or effective cost: **clean**

Both published. The anchor is a driver with median @@por_cac_anchor_median|num2@@ dollars. The
effective cost at the spend actually modelled is @@final_year_effective_cac_pooled|num2@@ in the final
year, pooled across paths, which is @@final_year_cac_pooled_over_anchor_median|num2@@ times the anchor. On the median
path it is @@final_year_effective_cac_median|num2@@, because the median path never spends enough to
saturate anything. It is published month by month as `cac_effective_blended_mean`
in `out/por_monthly.csv`, with the non-creator channel beside it.

### 13. Break-even struck on the anchor rather than the effective cost: **clean**

The break-even solves pin the anchor, because that is the input, but the target is
evaluated through the saturation and pool-pressure mechanism, so the answer is the
anchor value that produces the outcome at the effective cost. `pinned_sweeps.csv`
carries `final_year_effective_cac_mean` at every pin, so the effective cost at each
pinned anchor is on disk.

### 14. An acquisition budget with no cap: **clean now, and the cap is looser than it sounds**

Capped at @@const_CAC_LTV_CAP|num2@@ times the company's own lifetime value estimate, by inverting the
saturation curve for the spend at which effective cost reaches the cap.

It was not clean in another way: the launch acquisition subsidy ran unconditionally
for all sixty months. It now holds for @@const_ACQ_RAMP_HOLD_MONTHS|int@@ months after go-to-market and tapers
to nothing over the next @@const_ACQ_RAMP_TAPER_MONTHS|int@@. See `CHANGELOG.md` 0.4.

**The cap is struck on the GROSS lifetime value**, which subtracts nothing but
verification. The all-in contribution is negative on the median path, so the rule
permits spending @@const_CAC_LTV_CAP|num2@@ times a number that excludes engineering, content,
overhead and compliance. It is the only restraint on acquisition spend anywhere in
the model, and it is a loose one.

**Does lifetime value exceed cost per acquisition in the final year?** On the mean,
pooled, yes: @@final_year_ltv_gross_pooled|num2@@ against @@final_year_effective_cac_pooled|num2@@, a ratio of
@@final_year_ltv_over_cac_pooled|num2@@. **On @@share_paths_final_year_ltv_below_cac|pct1@@ per cent of individual paths, no.** And the
lifetime value in that ratio is the **gross** one; against the all-in contribution
the ratio is far worse, and on the median path it is negative, which is item 16.

### 15. A ratio between markets asserted as measured: **clean, and the code disagrees with the prose**

docs/10 states that a Year 10 household can afford roughly twice the acquisition
cost of a Year 11 household. The model asserts no such ratio; it produces one from
a sampled summer lapse probability and a sampled progression rate.

**The number the code actually uses is @@year10_to_year11_retained_months_ratio|num2@@, not two**
(@@retained_months_pre_exam_mean|num2@@ months against @@retained_months_exam_year_mean|num2@@, measured by pinning the
segment mix and re-running on the same random numbers). It reaches two or better
on @@share_paths_year10_at_least_doubles|pct2@@ per cent of paths. docs/10's shape survives; its magnitude
does not, and docs/10's own caveat about the summer is most of why: removing the
summer entirely lifts the ratio by @@year10_ratio_lift_from_removing_summer|num3@@
against @@year10_ratio_lift_from_flooring_churn|num3@@ for flooring in-term churn,
a factor of @@year10_summer_lever_over_churn_lever|num0@@. **Neither recovers two,
and nor do both together** — that is the finding, and it is larger than either
lever. This document said the summer, the write-up then said in-term churn, and
the two disagreed across three files until round four differenced the
counterfactuals instead of reading them off a list.

Market ratios are all sampled, none asserted: price, acquisition cost and
reachable pool relative to the United Kingdom each have a stated range in the
driver registry.

---

## Lifetime value

### 16. A gross margin presented as a net one: **clean, both published**

The mean of this ratio is not a usable number and is published nowhere: its
denominator collapses on paths whose book has collapsed, so a handful of paths
carry it to millions. Two defensible figures are published instead, the pooled
ratio and the median path's.

@@final_year_contrib_per_hh_month_gross_pooled|num2@@ dollars per household month pooled, and
@@final_year_contrib_per_hh_month_gross_median|num2@@ on the median path, is a **gross**
contribution: net revenue less inference, support, payment, hosting and store fees.

The all-in figure, net of engineering, content, overhead and compliance (payment
fees are already out of the gross row above, and are not deducted twice), is @@final_year_contrib_per_hh_month_allin_pooled|num2@@ dollars per household month pooled and
@@final_year_contrib_per_hh_month_allin_median|num2@@ on the median path. Pooled, the all-in figure is
@@gross_minus_allin_contrib_per_hh_month_pooled|num2@@ dollars a household month lower than the gross one.

**The pooled and median all-in figures disagree in sign**, because the pooled one
is dominated by the few paths with large books that spread the fixed costs, and
the median path is small with the same fixed costs on top of it. Both are in
`out/cohorts.csv` and both are in the write-up, so neither can stand in for the
other and neither can stand in for the gross figure.

**The same trap has a second door, and a round-three review found the document
walking through it.** The lifetime-value-against-acquisition-cost comparison was
published on the gross basis only: lifetime value is below acquisition cost on
@@share_paths_final_year_ltv_below_cac|pct1@@ per cent of paths, which reads as
reassurance. On the all-in basis the same comparison fails on
@@share_paths_final_year_ltv_allin_below_cac|pct1@@ per cent. Both are now in
`out/cohorts.csv` and item 19 publishes them side by side. Publishing only the
first is precisely this checklist item, committed by a document whose own answer
to this checklist item was "clean".

---

## Statistics

### 17. Series on the same basis: **clean now, and the enforcement was vacuous until round 2**

Column suffixes are disjoint by construction: `_mean` is a mean over all paths,
`_p10`, `_p50`, `_p90` are percentiles of the per-path distribution at that month,
and `_bandlow`, `_bandcentral`, `_bandhigh` are within-band averages of whole
paths.

**The check that enforces this could not fire until round 2.** It tested whether
a name ended in both a mean suffix and a band suffix, which no string can do, and
it ran on one of the two writers. It now checks that every column in the monthly
file carries exactly one basis and no stray basis marker, that no column in the
per-path file carries an aggregate basis at all, and it runs on both writers.
`suffix_discipline_selftest()` shows it refusing four headers it must refuse, and
the output is in `out/suffix_selftest.txt`. The first real thing it caught was a
driver called `sessions_mean` sitting in a file that has no means in it; it is
now `sessions_per_hh_month`.

No figure in the write-up divides a `_mean` by a `_band`.

### 18. Sustained bad runs: **clean now, and worth less than it looks**

The demand shock is AR(1), not independent. Persistence is sampled between
@@driver_shock_rho_low|num2@@ and @@driver_shock_rho_high|num2@@, median @@shock_rho_median|num2@@. The longest run of consecutive months with the
demand multiplier below @@const_SHOCK_BAD_THRESHOLD|num2@@ averages @@shock_longest_bad_run_mean|num1@@ months and is
@@shock_longest_bad_run_p90|num1@@ at the ninetieth percentile; @@shock_share_paths_bad_run_6plus|pct1@@ per cent of paths contain a run
of six or more and @@shock_share_paths_bad_run_12plus|pct1@@ per cent a run of twelve or more.

**It did nothing at all until round 2.** Realised acquisition spend was recomputed
from realised acquisitions, so a shock that halved customers halved the money
spent and cost nothing. Spend is now committed in advance. See `CHANGELOG.md` 1b.2.

**And the run lengths above are a property of the demand series, not of the
answer.** What the whole persistent-shock apparatus is worth, measured by pinning
the innovation standard deviation to zero and re-running on the same random
numbers: @@shock_cost_terminal_cash_mean|usd0@@ dollars of terminal cash on the mean,
@@shock_cost_terminal_cash_median|usd0@@ on the median path, and @@shock_cost_peak_funding_p80|usd0@@ on the eightieth-percentile
capital requirement. On the @@shock_share_paths_bad_run_12plus|pct1@@ per cent of paths that do take a run of twelve
or more bad months it bites harder, @@shock_cost_on_worst_affected_mean|usd0@@ on the mean of that group, but
even there the median damage is @@shock_cost_on_worst_affected_median|usd0@@. **A sustained demand drought is in
this model and it is not what ends the company.**

**What is still missing.** The shock acts on acquisition only. There is no
correlated shock to retention, to vendor prices, or to the examiner labour market,
and no regime in which several go wrong together for the same reason. A recession
would do all of those at once and this model cannot represent it, and that, not
the acquisition shock, is the thing worth worrying about.

### 19. Conclusions true only of an averaged line: **not clean, and round four found two the table had missed**

Every averaged claim in the write-up is given its per-path share. The last
column says whether the write-up asserts each proposition or denies it, because
**four of these eight rows are propositions the document exists to refute** and
reading their shares as support would invert them. That count was "two" until
round four counted the table; it was wrong before round four added the
variable-cost row and wronger after.

| Proposition | Share of paths on which it holds | The write-up |
|---|---|---|
| Content exceeds acquisition spend | @@share_paths_content_exceeds_acquisition|pct1@@ per cent | asserts it |
| Content exceeds both acquisition and people | @@share_paths_content_is_largest_line|pct1@@ per cent | asserts it |
| The Year 10 cohort retains at least twice the months | @@share_paths_year10_at_least_doubles|pct2@@ per cent | **denies it**, against docs/10 |
| Gross lifetime value is below acquisition cost in the final year | @@share_paths_final_year_ltv_below_cac|pct1@@ per cent | **denies it** on the gross basis |
| Variable cost exceeds half of gross consumer revenue, which is where docs/10's row reverses | @@share_paths_variable_cost_over_half_of_revenue|pct1@@ per cent | **denies it** for the plan, concedes it for these paths |
| All-in lifetime value is below acquisition cost in the final year | @@share_paths_final_year_ltv_allin_below_cac|pct1@@ per cent | asserts it on the all-in basis |
| Peak funding exceeds ten million dollars | @@share_paths_peak_funding_over_10m|pct1@@ per cent | asserts it |
| Terminal cumulative cash is positive | @@share_paths_terminal_cash_positive|pct1@@ per cent | **denies it** |

**Two failures of this item were found in round four and both are fixed above.**
The first: the lifetime-value share was computed by multiplying each path's own
contribution by the SAMPLE MEAN retained months, a scalar. Retention varies
strongly across paths and correlates with churn, so the published share was a
hybrid presented as a per-path statistic, in the answer to the item about exactly
that. Using each path's own realised retention gives
@@share_paths_final_year_ltv_below_cac|pct1@@ per cent against the old
@@share_paths_final_year_ltv_below_cac_scalar_months|pct1@@; both are in
`out/cohorts.csv` so the size of the error is on the record. The second: the
docs/10 variable-cost row was answered with a mean and is now given per path in
section 5 of the write-up, where variable cost exceeds half of revenue on
@@share_paths_variable_cost_over_half_of_revenue|pct1@@ per cent of live paths.

**The two lifetime-value rows are the pair to read together, and an earlier
draft published only the first.** On the gross basis, which charges a household
inference, support, payments and age assurance and nothing else, lifetime value
clears acquisition cost on almost every path. On the all-in basis, which also
carries the content build and the people who make it, it fails on
@@share_paths_final_year_ltv_allin_below_cac|pct1@@ per cent. Quoting the gross
number alone is checklist item 16 — a gross margin presented as a net one — and
it was being done here.

---

## Funding

### 20. Sized on the base case or the plan of record: **clean**

Sized on the **plan of record**, at @@funding_plan_of_record_whole_horizon_round_size|usd0@@ dollars across the
horizon at the eightieth percentile. The base case is stated beside it at
@@funding_base_case_uk_only_whole_horizon_round_size|usd0@@, along with two narrower scopes. They differ enough
that sizing on the base case would underfund the plan actually described.

**One method note, because it looks like a defect this document warns about
elsewhere.** A staged round is sized as the eightieth percentile of the window's
need **plus** six times the eightieth percentile of its monthly burn — two
percentiles of different distributions added together, which is the construction
section 6 refuses for band lines. Here it is safe, and that was measured rather
than assumed: need and burn correlate at 0.97 to 1.00 across the three windows,
so the sum of the two percentiles differs from the eightieth percentile of the
sum by about seven hundred dollars across a staged total of thirty-seven
million. Adding percentiles of near-perfectly correlated quantities is the one
case where it is not blending; if the correlation ever fell, this would need
re-deriving as a joint percentile.

### 21. Staging against decisions: **not clean**

@@commitments_spend_starts_in_seed|int@@ of the file's
@@commitments_total|int@@ commitments have their spend starting inside the seed
window, including the United States entity and its market counsel, the security
certification, A-level content and the second and third United Kingdom boards.
The rest-of-English-speaking entity is the other of the two the file names, and
it lands and is paid for in the Series A; an earlier draft called both of them
seed-window.

**The list itself was the defect for four rounds.** It is hand-typed, and until
round 5 every entry landed at month 30 or earlier in a sixty-month horizon, so
six of the model's own content steps were missing and the count was 10 of 14.
One of the six is a second violation of the section's own test. An instrument
that measures whether staging matches decisions, built as a hand-kept list of
half the decisions, is the failure class this document spends most of its change
log converting away from. @@commitments_paid_by_an_earlier_round_than_they_land_in|int@@ commitments land
in a later stage than the one their spend starts in, and until round 6 this
paragraph announced the second one and then named only the first. They are: all
four United Kingdom boards live at month 18, built from month 12, inside the
seed window; and the United States seven-subject step live at month 40, built
from month 34, inside the Series A. The rest-of-English-speaking market at month 24
begins its build at month 18, exactly as the Series A opens, so the file's test
puts it on the right side of the line.

The column that carries this test used to be called
`decision_taken_after_its_round_closed` and answered "no" on both violations and
"yes" on the eighteen clean rows, so a reader filtering the file for the problem
got its complement. It is now `spend_starts_before_its_stage_opens` and answers
yes when the test fails.

**The Series A does not buy those decisions. It refinances them.** `out/funding_commitments.csv`
holds the landing month and the spend-start month for each.

**What it would move.** Nothing in the cash flow; the spend happens either way.
What it moves is the round sizing: the seed for the plan of record is
@@funding_plan_of_record_seed_round_size|usd0@@ dollars, and a round of that size described as a seed will
be raised on seed terms against a Series A-sized commitment.

---

## The measuring instrument

### 22. Does the instrument produce the quantities claimed: **not clean, and it is the worst of the ones that cannot be fixed by writing code**

Decompose revenue per household: it is the plan price, plus the overage, and the
overage is a function of **sessions per household per month**. Decompose the cost
side: variable cost is sessions per household times cost per session.

Sessions per household therefore appears on both sides of the unit economics and
in the pricing decision, since the allowance cannot be set without it.

**No instrument in docs/11 produces it before M5.** M1 is counsel, board policies,
three age-assurance quotes, a landing page and thirty school conversations. M2
produces cost per session from a frozen battery, which gives cost per session but
not sessions per household. M4 instruments return rate and sessions per learner per
fourteen days, and that secondary metric is the first instrument in the roadmap
that touches the quantity at all. M4 comes before M5 in docs/11, and it already requires a signed creator and a
built product, so the quantity is not available cheaply or early on either
milestone. An earlier draft of this item said M4 was not before M5, which is
simply wrong about the roadmap.

**Volume per customer is the factor nothing measures**, exactly as the brief
predicts. `sessions_per_hh_month` is sampled between @@driver_sessions_per_hh_month_low|num1@@ and @@driver_sessions_per_hh_month_high|num0@@ a month, a fivefold
range. docs/03's own arithmetic, three sessions a week for a Year 11 revising one
strand, is about thirteen a month, which sits inside the range rather than at its
top; the range is wider in both directions because nothing measures it.

**What it would move.** `out/breakeven.csv` records the solve. What can be said now
is that the allowance of sixteen sessions, which is a commercial decision already
taken in `model.py`, sits inside that range, so whether @@por_mean_share_over_allowance_pct|num1@@ per cent
of households exceed it or almost none do is not determined by anything measured.

### 23. Do the instrument's strata match the mix the cost base assumes: **not clean**

docs/03's validation pilot is two examiners validating the same twenty items. The
cost base applies `minutes_per_item` across 5 to 11 subjects, two levels and up to
four boards, and `minutes_per_item` is ranked @@sobol_peak_funding_requirement_rank_of_minutes_per_item|int@@ on the capital
target.

Twenty items of one kind, in one strand, of one subject, at one tier, is not a
sample of that population. The same defect as ten of each of five tiers not being
a 45/50/5 population. A pilot that measured a stratified sample across subject,
item kind and difficulty would cost very little more and would actually support
the extrapolation the cost base makes.

Second instance: the segment mix. The cost base assumes an examination-year share
sampled between @@driver_seg_mix_exam_low|num2@@ and @@driver_seg_mix_exam_high|num2@@, and nothing in docs/11 measures the mix
of who actually arrives.

### 24. Will the instrument run under production constraints: **not clean**

The landing-page price test for condition C1 runs without age assurance, without a
product, and without the refusal behaviour. docs/07 identifies the refusal
behaviour as a live retention risk: a tutor that declines questions a free chatbot
answers is a worse experience in the moment. The price test cannot see it, so it
measures willingness to pay for a described product rather than for the one that
will exist.

An operator testing on their own account is not measuring the real workflow
either. The production workflow is an age-verified adult account holder with a
child as the data subject, per docs/07's own statement of the mismatch that is
open item OI-10. Nothing in M1 exercises that path.

---

## Limits of the instrument itself, beyond the checklist

**It cannot value evidence.** docs/09's strongest argument for the institution
channel is that outcome evidence is the only durable moat; docs/08 supplies the
supporting fact, that the comparators carrying weight in education are all
school-based, ASSISTments at 0.18 to 0.29 standard deviations with an ESSA Tier 1
rating and Carnegie Learning MATHia at 0.21 to 0.38. This model charges Route B
its costs, credits it its revenue, and gives it nothing for evidence.

**It is a lower bound in one direction and was an overstatement in the other.**
An earlier run tied the India content build to the institution switch, so the
figure carried an India item bank the channel never bills. That is fixed and the
number here is the corrected one. What remains is that the instrument still
gives Route B no credit for evidence, so the figure is an upper bound on what
dropping the channel is worth, not a settled estimate of it.

**It has no competitive response.** Free general tools sit in front of the same
parent and Google has committed capital at national scale. Nothing here represents
a competitor changing price, changing scope, or entering the United Kingdom
curriculum specifically.

**The company never adapts.** There is no rule that cuts spend when the plan is
failing, beyond the lifetime-value cap on acquisition. The peak funding
requirement is therefore the requirement of the plan as stated, not of a company
that notices and reacts. A real team would cut, and the honest reading of
@@funding_plan_of_record_whole_horizon_round_size|usd0@@ dollars is "this is what it costs to execute the plan of
record without flinching", which is not the same as what it would actually cost.

**The institution channel is one blended channel.** Route B is modelled as a single
sterling-priced motion with a decided representative ramp, not per market. Its
cost is charged where it falls, but the geography of it is not represented.

**Retention has no tenure structure beyond the first month.** After month one, the
hazard is constant until the examination calendar acts. Real subscription hazards
fall with tenure, which makes this pessimistic on the long tail and optimistic on
nothing in particular.

**A-level is one pooled segment**, not two years, with an exit rate sampled between
@@driver_alevel_exit_rate_low|num2@@ and @@driver_alevel_exit_rate_high|num2@@ standing in for the cohort structure.

---

## Limits an adversarial reading found that the sections above did not admit

These were added after a reviewer with no knowledge of how the instrument was
built went looking for them. Each is stated at the strength the evidence supports,
which in several cases is stronger than comfortable.

### The base model has no price elasticity at all, so a higher price buys more customers

Price enters revenue, then lifetime value, then the acquisition budget cap, then
spend, then acquisitions. It appears nowhere in `effective_cac()` and nowhere in
the churn calculation. **In the published run, raising the price raises the number
of households acquired.** That is not a subtle artefact; it is the direction of
the mechanism.

The feedback scenario adds a price-to-churn penalty, but only inside a bundle
with the quality and automation loops, so the price penalty is never priced on its
own. The whole of the price-anchor conclusion, which is the second-ranked decision
in the write-up, rests on a mechanism with no demand-side cost of price anywhere
in it.

**What it would move.** The anchor spread of @@anchor_tutoring_minus_software_terminal_cash_mean|usd0@@ dollars is an
upper bound. docs/12 names the competing anchor explicitly, that the free tools are already on
the parent's phone, and docs/07 states the substitution arithmetic against the
verified 25 to 45 pound hourly tutoring rate. The two price regimes here differ
by roughly the ratio of their modal prices, @@driver_price_uk_tut_gbp_mode|num2@@ against @@driver_price_uk_sw_gbp_mode|num2@@ pounds,
and a difference of that size against a free substitute cannot plausibly leave
conversion untouched. Splitting the feedback bundle so the
price loop can be run alone is a half-day of work and has not been done.

### The largest paths are not plausible and nothing in the instrument says so

Total acquisitions across the horizon run to a median of @@por_total_acquisitions_median|num0@@, a
ninety-ninth percentile of @@por_total_acquisitions_p99|num0@@ and a maximum of @@por_total_acquisitions_max|num0@@.
@@por_share_paths_terminal_cash_above_100m|pct2@@ per cent of paths end the horizon above a hundred million dollars.

There is now a ceiling, `POOL_REACQUISITION_MULTIPLE`, set at
@@const_POOL_REACQUISITION_MULTIPLE|num1@@, so no path acquires more
than that multiple of its own sampled pool in any market, and the largest ratio of
acquisitions to that path's own United Kingdom pool is @@por_max_acquisitions_over_own_uk_pool|num2@@ across three
open consumer markets. **That bounds the arithmetic; it does not make the top of
the distribution believable.**

**And it is load-bearing, which the document did not say until a round-three
review pointed it out.** The same constant is also the denominator of the
saturation term, so it sets how fast the effective cost of acquisition rises as
a market is worked — one number doing two jobs, neither of them measured. It is
now a configuration key rather than a buried literal, and two scenarios price
it: working the pool twice over rather than three times is worth
@@delta_por_reacq_low_terminal_cash_mean|usd0@@ dollars of terminal cash, and
five times over @@delta_por_reacq_high_terminal_cash_mean|usd0@@. Nothing in the
vault sets this number. It is a prior, it is not in `out/drivers.csv` because it
is a constant rather than a sampled driver, and a constant that moves the answer
by that much while being invisible to the sensitivity analysis is a defect of
this instrument rather than a property of the business. The reachable-pool prior is log-uniform across a
thirtyfold range and the market relatives multiply it further, so the upper tail
describes a business several times the size of the demand the vault has evidence
for. Those paths are what makes the mean of terminal cash, which is why the
scenario table in the write-up now gives the median beside it.

### "Content is the largest line" is partly a property of the budget rule

The median content cost over the horizon is @@por_median_path_total_content_cost|usd0@@ and the median
acquisition and verification spend is @@por_median_path_total_cac_spend|usd0@@. Taking each path's
own ratio and then the median of those, the typical path spends
@@por_median_path_content_over_cac_pathwise|num1@@ times as much on content as on
acquisition.

**The two medians in that first sentence do not belong to the same path, and
until round 7 this passage said they did.** It read "on the median path, content
costs X and acquisition costs Y, a ratio of Z" over a ratio of two separately
taken medians; the path holding the median content cost spends nothing like the
median on acquisition. The conclusion survives — the per-path median ratio is
within a few per cent of the ratio-of-medians — but the attribution to a single
path did not, and it is the same construction round 6 removed from the scenario
table's delta column and left standing here. Content is almost entirely exogenous: a fixed schedule
times a sampled item cost, with no demand feedback at all. Acquisition is
throttled by the lifetime-value cap and the launch-subsidy taper.

So the claim is true, and part of the reason it is true is that on most paths the
company barely markets. A plan that spends that ratio on content against customers
is not a plan anyone would execute, and the instruction the write-up draws from
it, that content cost is what makes the venture fundable, should be read with
that in view.

### The lifetime-value cap is struck on a gross figure

`CAC_LTV_CAP` limits acquisition spend to @@const_CAC_LTV_CAP|num2@@ times lifetime value, and the
lifetime value it uses subtracts nothing but verification. It is the gross margin,
not the all-in one, and the all-in figure is negative on the median path. The cap
is therefore looser than it sounds, and it is the only thing in the model
restraining acquisition spend.

### How finely a cost is split decides how high it ranks, and no instrument sees that

`out/sobol.csv` ranks the @@n_drivers|int@@ registry entries. A count of how many
of them in a top seven belong to one cost is therefore a fact about the registry,
not about the business. Content cost per item is
@@registry_cost_per_item_driver_count|int@@ entries because that is how it
decomposes; one timed pilot measures all of them at once. The content-driver set
this document counts with is @@registry_content_driver_count|int@@ entries and
the acquisition set is @@registry_acq_driver_count|int@@, and both are read off
the same sets `figures.py` uses for the top-seven counts rather than listed by
hand — the acquisition entries act through effectively one anchor. Split a cost finely and its
entries individually rank lower while its block ranks higher; split it coarsely
and the reverse.

`out/sobol_grouped.csv` computes indices on the grouped scalars and section 8 of
the write-up quotes those beside the registry ranking. It does **not** sum
individual indices to make a group index, which would be wrong.

**The first version of it was not symmetric, which a round-five review caught.**
The content scalar collects four of the eight content entries — everything one
timed pilot and one objective count would settle — while the acquisition scalar
collected three of twelve and left the saturation exponent out, although E2's own
trigger is a channel test at two spend levels, which measures effective cost *at*
a spend. A fourth grouped quantity does it that way. The conclusion survives both
groupings and the margin narrows under the symmetric one. **That it survives is
luck rather than method**: there is no instrument here that would have told us if
it had not, and the grouping is still a judgement about which questions one
instrument answers together.

### Decided constants are not in the sensitivity at all

`out/sobol.csv` and `out/tornado.csv` cover the @@n_drivers|int@@ sampled drivers. They cover
none of the constants in `out/constants.csv`, and `out/constants.csv` is itself
incomplete: it omits the two seasonality shapes, the examination-month and
season-shift maps, the United States, India and rest-of-English-speaking opening
months and `SCHOOL_OPEN` (the United Kingdom's is in the file, as `GTM_MONTH`),
all four content schedules, the
market budget weights, the segment usage relatives, the sales and creator ramps,
the platform headcount floor and the general and administrative schedule. Those
are invented numbers that drive every calendar statement in the document, and
nothing sweeps them.

The four that carry the most weight, and are named as decisions rather than
findings: `P_TUTORING_ANCHOR` at @@const_P_TUTORING_ANCHOR|num2@@, which makes every plan-of-record
figure a mixture of two regimes; `POOL_BREADTH_EXPONENT` and
`PLATFORM_PER_EXTRA_MARKET`, which between them set the ratio the write-up calls
the owner's largest decision; and `OVERAGE_CAP_MULT` at @@const_OVERAGE_CAP_MULT|num1@@, which sets the
one-sided asymmetry that checklist item 3 rests on.

**One of them stopped being invisible in round 3, and the exercise shows what the
rest are hiding.** `POOL_REACQUISITION_MULTIPLE`, at
@@const_POOL_REACQUISITION_MULTIPLE|num1@@, does two jobs: it bounds cumulative
acquisitions and it is the denominator of the saturation term, so it also sets
how fast acquisition gets dearer as a market is worked. It is now a configuration
key with two scenarios, and moving it from three to two is worth
@@delta_por_reacq_low_terminal_cash_mean|usd0@@ dollars of terminal cash while
moving it to five is worth @@delta_por_reacq_high_terminal_cash_mean|usd0@@. That
is comparable with several of the sampled drivers that section 8 ranks, from a
number nothing in the vault sets and no instrument in this directory could see
until it was lifted out. **The other constants above have not had this done to
them, and the presumption should be that some of them would behave the same
way.**

### The retained book is far shorter than the product being sold

An examination-year household is retained @@retained_months_exam_year_mean|num2@@ months. The commercial unit
is an examination-cycle plan billed monthly to the last paper, which docs/07 puts
at nine months for a September acquisition and five or six for a January one. **The
average customer in this model never completes a cycle.** Two things produce
that and an earlier version of this passage credited only the first: the in-term
churn prior, which nothing has measured, and the horizon, which right-censors
retention for the reason set out further down this document. The level is a
floor. Either way the pricing decision and the retention prior are describing
different products, which is the point of this item and does not depend on the
split.

### The foreign markets are the United Kingdom calendar copied

The United Kingdom calendar in the model is right: a June exit, a July and August
lapse, September and January acquisition peaks, a March to May usage peak. The
others are that year with a shift applied.

- **The rest-of-English-speaking bucket is given a June sitting and a
  July-to-August summer lapse.** Australia, New Zealand and Singapore run a
  January academic year with terminal examinations in October and November and
  their long holiday across December and January. The model lapses their
  pre-examination cohort during their term and empties their examination cohort
  mid-year. There is one seasonal phase shift for the whole bucket and it is zero.
- **That bucket is also one price, one tax rate, one acquisition cost and one
  pool** for Ireland's Leaving Certificate, eight Australian state certificates,
  thirteen Canadian provincial curricula, New Zealand's NCEA and Cambridge
  qualifications in Singapore. `ROW_TAX` is a single blended @@const_ROW_TAX_pct|num0@@ per cent against
  rates from 5 to 23 per cent.
- **The United States is given levels and boards, and a terminal May sitting.** It
  has neither. The pre-examination to examination to lapse machinery is a
  terminal-high-stakes-sitting structure, and the mass United States tutoring
  drivers are year-round: SAT and ACT across seven sittings, and grade
  maintenance. The May sitting modelled is an Advanced Placement analogue taken by
  a minority.
- **India is given one board rising to two**, against CBSE, ICSE and roughly
  thirty state boards.

None of this changes the ordering of the levers, because the ordering is set by
acquisition cost and content cost and both are market-agnostic in this model. It
does mean **every foreign-market level in this document is weaker than the United
Kingdom ones**, and the expansion case should not be argued from them.

---

## What a second adversarial round found, after the first had cleared the surface

### The horizon writes a five-year asset to zero, and that is what makes content look expensive

`terminal_cash` is the cumulative cash at month @@horizon_months|int@@ and nothing else. At that
month the instrument assigns **zero** value to the item bank it has just spent
@@por_total_content_cost_mean|usd0@@ dollars building, and zero to the standing book of
@@por_terminal_active_hh_mean|num0@@ households still paying.

That is not a neutral default. A large share of the content spend falls in the
last two years and is charged in full against a truncated revenue window:
@@por_content_share_last_24m_pct|num1@@ per cent of content spend falls in months 36 to @@horizon_months|int@@, and
@@por_content_share_last_12m_pct|num1@@ per cent in the final twelve. Terminal-month net cash is
@@por_terminal_month_net_cash_mean|usd0@@ and terminal-month net revenue @@por_terminal_month_net_rev_mean|usd0@@, an annual
run rate of @@por_terminal_annual_run_rate|usd0@@.

**Every statement in this document of the form "content is the largest line",
"content sets the slope" and "@@por_share_demand_independent_pct|num1@@ per cent
of the cost base does not respond to demand" is partly a function of where the
window was cut.** The `por_residual` scenario
credits a residual and is worth @@delta_por_residual_terminal_cash_mean|usd0@@ dollars of terminal cash and
@@delta_por_residual_peak_funding_p80|usd0@@ on the capital requirement. Both of its parameters are priors
and neither is defensible as a valuation; the point is the size, not the number.

Nothing sweeps the horizon itself, no scenario stops building content when the
remaining window is shorter than the payback, and the launch-delay scenarios in
section 9 of the write-up are the same defect showing through in another place.
**Whether this one changes the ordering rather than the levels is not known,
because nothing here computes it.** This paragraph asserted for four rounds that
it does, and named the restricted-transfer question as the other item that does.
Both halves were wrong. The restricted-transfer half was the round-2 position,
retracted in round 4 once the decomposition was actually run under full
onshoring — `out/sobol.csv` carries it as the `onshore_all` run, item count
holds rank 1 exactly as on the plan of record, and the write-up's section 12 says
plainly that it barely moves the ordering at all. The residual half was never
computed in any round: `out/sobol.csv` carries three configurations and a
residual-on decomposition is not among them. What is known is the size of the
cash, which is in the two figures above. The ordering claim is withdrawn rather
than restated, and it is a one-run job to settle if it matters.

### Age assurance is charged once per acquired household, never per check

`verif_total += acq * v`. Every check on somebody who does not convert is free.
A reusable identity check is billed per attempt, so at any realistic ratio of
checks to conversions the line is a multiple of what is modelled, priced in
`out/omissions.csv` at @@omission_age_assurance_on_non_converting_checks_low|usd0@@ to
@@omission_age_assurance_on_non_converting_checks_high|usd0@@ dollars.

The conclusion elsewhere in this file that verification does not dominate the cost
structure rests on a @@por_share_verif_cost_pct|num1@@ per cent share that assumes one check per acquired
household. **Nothing states that ratio and nothing measures it.** Condition C2 in
docs/09 is a threshold against first-month contribution and is unaffected; the
share-of-cost claim is not.

### There is no United Kingdom consumer subscription regime in the model

A monthly consumer subscription sold to United Kingdom households inside this
horizon carries the Digital Markets, Competition and Consumers Act 2024 duties,
mandatory renewal reminders, a cooling-off right on renewal and an easy-exit
obligation, and the fourteen-day cancellation right under the Consumer Contracts
Regulations. All of them are retention and revenue mechanics. None has a term
here, and unlike the other absent lines they cannot be priced from anything the
model carries, so `out/omissions.csv` records them at zero and says why.

Related and in the same class: **there is no trial-to-paid step and no involuntary
churn.** An acquisition is a paying household from the month after it is acquired.
Failed cards appear only as a cost line, never as a reason a household leaves.
Every operator of a consumer subscription would put involuntary churn at a
material fraction of gross churn.

### The app-store fee is the small-business rate on every path

`appstore_params()` sets @@const_APPSTORE_FEE_pct|num0@@ per cent on every path, including paths billing
tens of millions a year, where the small-business rate does not apply and the
headline rate is double. The app-store decision is priced at the lower rate
throughout.

---

## What a third adversarial round found, which is about shape rather than figures

The brief predicted that a third round would reach the structure, because the
first two clear the surface. It did. These five are not arithmetic errors. Each
is a place where the document drew a conclusion its own files do not support, and
in three of them the conclusion was load-bearing.

### The scope conclusion was an artefact of comparing against two different scopes

Owner decision 1 put a capital figure computed against the go-to-market minimum
beside a terminal-cash figure computed against the United Kingdom-only scenario,
and concluded in bold that scope is dominant on one statistic and minor on the
other. The United Kingdom-only scenario keeps the entire content escalation, so
its content line is close to the plan of record's, and the second figure was not
measuring scope. Section 12 now carries the three-rung ladder and the opposite
conclusion.

**The general form of this defect is worth naming, because it will recur.** Two
comparisons against differently-shaped counterfactuals, each correct in
isolation, set side by side and read as a single finding. Nothing in the
verifier can see it: both figures existed on disk, both were rendered from
tokens, both traced to `out/variants.csv` and `out/funding.csv`. **Every number
in the sentence was right and the sentence was wrong.** That is the limit of
Pass B and it is stated in section 13 of the write-up, but this is the first time
the limit actually bit on a headline conclusion.

### The sensitivity ordering is conditional on the scope and was quoted as unconditional

Every first-order index in section 8 is computed on the plan of record.
`out/sobol.csv` now carries the go-to-market minimum and the full-onshoring
configuration beside it, and the capital ordering rearranges between them:
content drivers hold
@@sobol_peak_funding_requirement_content_drivers_in_top7|int@@ of the top seven
on the plan of record and
@@sobol_gtm_peak_funding_requirement_content_drivers_in_top7|int@@ on the
go-to-market minimum. The instruction "work on content cost to make it fundable"
is a consequence of a scope decision that has not been taken.

**What is still not clean.** Only three configurations are decomposed. The
ordering is presumably conditional on other choices too — the institution
channel, the price regime, the launch date — and nothing here establishes which.
The honest statement is that the ordering is known to move with scope, is not
known to be stable under anything else, and was published as though it were a
property of the business.

### A break-even against a weak target read as a rescue

@@breakeven_rows_bracketed_on_profitability|int@@ of the @@breakeven_rows_bracketed|int@@ solved break-evens target half of all paths stringing three
cash-positive months together; the remaining one targets the median path ending
the horizon whole, on the narrowest scope. `out/breakeven.csv` now carries, for each solved
row, the median path's terminal cash and the eightieth-percentile funding
requirement at that same value, and the share of the paths that meet the target
and still end the horizon negative. On the plan of record that last share is
@@breakeven_plan_of_record_price_uk_tut_gbp_share_reaching_profitability_at_be_hitting_paths_ending_negative_pct|num1@@
per cent. The number was always in the file; the word attached to it was wrong.

### Two mechanisms were tested by the wrong test, and the test said so in the right words

The switched-off reproduction test is a test of the random streams. Section 3
presented it under the heading of mechanism validation, and every one of round
2's four mechanism defects passed it while wrong. It is now two-sided, which
catches inert mechanisms, and is described for what it is. **There is still no
mechanism correctness test in this instrument and there cannot easily be one:
what would it compare against?** The four defects were found by reading the
code, which is the only method that has worked, and which does not scale.

### The gate covers two files of @@out_csv_count|int@@

`por_monthly.csv` and `por_paths.csv` are rebuilt character for character on
every load. The other derived outputs are not rebuilt by anything, and the check
that now exists — every generating script recording the SHA-256 of `model.py`
and `harness.py` together, and `verify.py` refusing a set whose hashes disagree
— catches staleness and nothing else. A derived CSV can be generated by a buggy
`sensitivity.py` against the right model and pass.

### And one absence that is not about shape at all

**Specification change.** `content_full_equivalents` is monotone in time. No item
ever expires. Over a sixty-month horizon in a market whose awarding bodies reissue
specifications on published timetables, part of the bank being built in year one
is being written to a specification that will not exist in year five.
`out/omissions.csv` prices it at
@@omission_specification_change_and_curriculum_reform_low|usd0@@ to
@@omission_specification_change_and_curriculum_reform_high|usd0@@ dollars, which
is a prior on the rate of turnover and not a measurement. It acts on the largest
cost line in the model and on the driver the capital requirement is most
sensitive to. It was absent from the model, from this document, from the open
items and from the omissions file until round three. It is open item X11 and the
trigger is a morning's reading of public timetables.

---

## What a fourth adversarial round found, which was two live mechanism defects and a sign

Three rounds had cleared the surface and then the structure. The fourth went
back into the month loop and found two things wrong in it, plus a conclusion
published with its sign inverted. All three are fixed; what follows is what is
still not clean after them.

### There is no discounting anywhere, and the largest scenario in the file is the one it would shrink

Terminal cash, the peak funding requirement, every break-even, the rescue grid
and the residual are undiscounted nominal sums over sixty months. There is no
cost of capital, no present value, and no financing cost on the
@@funding_plan_of_record_whole_horizon_round_size|usd0@@ the plan raises — no
interest, no fees, and nothing for the cash sitting idle between rounds.

`out/cohorts.csv` now prices the first half of that: the same net cash line
discounted at twelve per cent a year is @@por_terminal_cash_npv_12|usd0@@ and at
twenty-five per cent @@por_terminal_cash_npv_25|usd0@@, against
@@por_terminal_cash_mean|usd0@@ undiscounted. **The direction matters more than
the level.** Content spend is front- and mid-loaded and revenue arrives late, so
discounting makes content relatively dearer and sharpens the ordering this
document reports; and the residual scenario, the largest single item in the
scenario table at @@delta_por_residual_terminal_cash_mean|usd0@@, sits entirely
at month 60 and would shrink by more than anything else. Nothing in the write-up
is restated on a discounted basis. A reader who would discount should assume
every level here is optimistic about late money and that the residual in
particular is the most optimistic thing in the file.

### The acquisition budget cap still believes in a longer-lived household than the model delivers

Round four found `ltv_estimate` — the company's own running estimate, and the
only restraint on acquisition spend anywhere in the model — assuming roughly two
and a half times the retention the same model delivered, because it ignored
first-month attrition and the examination calendar. Round five found a third
cause: the pre-examination branch capped its life at the sitting plus ten months
while the loop moves that household on at the sitting plus **two**, so the
function round four rewrote to take the calendar from the loop was using
arithmetic the loop does not.

All three are fixed. The gap is smaller and is **not** closed: `out/cohorts.csv`
publishes `ltv_cap_assumed_months` at @@ltv_cap_assumed_months|num2@@ against
`ltv_cap_realised_months` at @@ltv_cap_realised_months|num2@@, a ratio of
@@ltv_cap_months_overstatement|num2@@. What remains is a geometric life ignoring
the other exits, and realised retention being itself right-censored by the
horizon — the second of which means the true ratio is smaller than the published
one.

**Why it matters more than the dollars.** `budget_cap_from_ltv` inverts the
saturation curve, so permitted spend scales as roughly the square of the
estimate. An estimate that is half right permits four times the spend wherever
the cap binds, and this cap is the only brake the model has other than the pool
multiple that nothing sets.

### Retained months are right-censored and the write-up blamed churn for all of it

`cohorts.py` computes retained months as active household months over
acquisitions across the whole horizon. Acquisitions are still ramping at month
58, so a large share of them have their retention cut off by the end of the
window rather than by churn. The examination-year figure is therefore a floor.
The **ratio** between year groups, which is what refutes docs/10's assumption,
is not affected — a fourth-round reviewer checked that specifically and it
survives — but "that follows entirely from the in-term churn prior" was too
strong about the level, and the lifetime-value ratio built on it is a floor too.

### The demand shock's cost is smaller than the Monte Carlo error on the mean

`shock_cost_terminal_cash_mean` in `out/cohorts.csv` is a small number, and the
sampling error on the headline mean is @@por_terminal_cash_mc_se|usd0@@. The
shock's cost is measured on a PAIRED run, which is far tighter than that, so the
comparison is not quite apples to apples — but it is the right thing to hold in
mind when reading any unpaired difference in this document. The sampled
foreign-exchange scenario is the case where it bites: its delta is not small, it
is **zero** at this sample size.

### The funding requirement is right-censored for four paths in five

`out/por_paths.csv` records each path's trough month.
@@por_share_paths_trough_at_horizon_pct|num1@@ per cent of paths have it in the
**last month of the horizon**: cash is still falling when the window closes and
the trough has not happened yet. The median path troughs at month
@@por_trough_month_median|int@@ of @@horizon_months|int@@.

The peak funding requirement is the negative of the trough, so every capital
figure in section 11 — the @@funding_plan_of_record_whole_horizon_round_size|usd0@@
headline, the staged sum, all four scopes — is a **floor** on the same four paths
in five. The instrument has nothing to say about how much more month 61 asks for,
because there is no month 61.

This was hidden by a mean. The write-up quoted the mean trough month,
@@por_mean_trough_month|num1@@ against the averaged line's
@@por_min_of_mean_cash_month|int@@, and concluded the averaged line troughs
"later" by four tenths of a month, which was right when it was written and is
not now: the averaged line troughs @@por_averaged_line_trough_gap_months|num1@@
months earlier than the average path. The mean sits between a fifth of paths that
trough early and four fifths that never trough at all, and describes neither.
**It is the same defect as checklist item 19 and it was inside the section whose
entire subject is that a mean of minimums is not the minimum of a mean.**

### The reachable pool responds to subjects and not to levels or boards

`model.py` scales the reachable pool with subject breadth and discards the level
and board counts from the same call. So the go-to-market minimum — five subjects,
one level, one board — and the plan of record's United Kingdom at month 18 — five
subjects, two levels, four boards, and @@uk_content_fe_ratio_por_over_gtm_month18|num1@@ times the content by the
model's own full-equivalent measure (@@uk_content_fe_por_month18|num1@@ against
@@uk_content_fe_gtm_month18|num1@@, and eight times by raw subject-level-board count) — are
credited the **same** reachable pool, through a window that spans the whole seed
and Series A. A United Kingdom household sits one awarding body's specification;
a one-board product cannot serve three quarters of them. Round 0 fixed the
subject half of exactly this asymmetry and left the board and level half.

Separately, the pool reads the **unshifted** schedule months while the content
build applies `launch_shift`, so under the launch-delay scenarios the pool widens
on the original calendar while the content arrives late. That is a third
contamination of those rows, on top of the two section 9 already names.

**It is not corrected here, and the reason is worth more than the correction
would be.** Mapping board coverage onto reachable households needs a prior
nothing in the vault supplies. And the pool is nearly inert: `out/breakeven.csv`
shows it pinned across its thirtyfold range moving the median path's terminal
cash and the capital requirement by a few per cent, because the acquisition
envelope is revenue-driven rather than pool-driven. So the narrow scope's
advantage in this document is **not** protected by an argument that it reaches as
many households — it is protected by the pool doing almost nothing. Open item E5
says the muting is a model property rather than a fact; what it did not say is
that the muting is what makes this asymmetry invisible.

### The one prior with no bounds, and the file used to print it as if it had them

`price_drift_yr` is the registry's only **normal** driver: N(@@driver_price_drift_yr_mean|num3@@, @@driver_price_drift_yr_sd|num3@@),
unbounded in both directions. Real prices **fall** on
@@price_drift_share_paths_negative|pct1@@ per cent of paths, and the cumulative
real price multiplier at month 60 runs from
@@price_drift_multiplier_at_horizon_p05|num2@@ at the fifth percentile to
@@price_drift_multiplier_at_horizon_p95|num2@@ at the ninety-fifth. That is a wide
prior on the quantity every revenue figure in this document compounds, and it is
not one of the ranges the write-up quotes.

`out/drivers.csv` printed that mean and standard deviation under a `low`/`high`
header until round four, which said the driver was sampled between 1.5 and 3.0
per cent. It was not, and `figures.py` was one token away from putting the wrong
reading into the prose. The file now has `normal_mean` and `normal_sd` columns
and emits no bounds for a driver that has none.

### A one-sided prior on the one cost the document says is well understood

`infer_decline_yr` is sampled on a strictly positive range, so there is no path
in @@n_paths|int@@ on which the unit price of inference rises. Every other
uncertain quantity here is two-sided. This one encodes a view — that model
prices only fall — which has held recently and is not a law. It is not in the
list of priors this document flags, and it should be.

### The institution channel is a lower bound at both ends

School seats consume inference and nothing else: support, hosting, payment
processing and age assurance are all driven by active **consumer** households, so
a seat costs nothing to support, host, bill or verify. And institution revenue is
recognised only in the annual renewal month, so a contract signed in any other
month earns nothing until the following one, and contracts landing in the last
months of the horizon are never recognised at all. Both are in
`out/omissions.csv`. Together they mean
"@@delta_por_no_schools_terminal_cash_mean|usd0@@" understates the channel's cost
and its revenue at once. It is small either way — the channel is
@@por_schools_share_of_net_revenue_pct|num2@@ per cent of net revenue — but the
figure is not a clean measure of anything.

---

## What six rounds of review say about the gates in this directory

This is the most important limit in the document and it is an empirical one, so
it goes last rather than among the checklist items.

Ten mechanism defects have been found in `model.py` across rounds 2, 4, 5 and 6:
a churn reference in the wrong place, an allowance that truncated at the wrong
number and kept the revenue anyway, saturation measured on the wrong quantity,
an onshoring switch that moved the wrong people, a sitting-month exit applied to
a cohort in the month it arrived — twice, on two different paths into the
segment — a lifetime-value estimate using a calendar the loop does not have, the
summer lapse and the year-group progression firing on the month's arrivals in
exactly the way the two sitting exits had been fixed not to, a segment mix that
did not sum to one so that households were billed which had never been bought,
and a lifetime-value cap that valued an examination household acquired in its own
sitting month at zero months of life.

**Every one of them passed every automated check in this directory, on every
run, while it was wrong.** Not by accident: the checks cannot see this class of
defect by construction.

- The **character-for-character harness gate** compares the published CSVs
  against a rebuild from the same source. A defect that is *in* the published
  run reproduces perfectly. The gate proves the file matches the code; it says
  nothing about whether the code is right.
- The **two-sided off-test** applies only to switchable mechanisms. Eight of the
  ten defects were in the base loop, which has no switch.
- The **five cross-checks**, four of which are accounting identities and one of
  which is a scope-ladder decomposition, check that cash adds up. Eight of the ten
  moved households, ratios or a spend cap — quantities that do not appear in a
  cash identity. This is now measured rather than asserted:
  `out/invariant_defect_costs.csv` re-runs the model with each historical defect
  put back and records what terminal cash does, and
  @@invariant_defects_costing_no_cash|int@@ of the reintroduced defects move the
  terminal cash mean by **exactly nothing** — identical to six decimal places —
  because they move a decomposition rather than a total. No cash identity can
  see those, on any run, ever.
- The **structural invariants**, added in round 5b as the answer to all of the
  above, did not catch round 6's three because two of them were outside what any
  invariant then covered and the third was covered by an invariant that was
  arithmetically incapable of firing. That is written up in the round 6 section
  below, and it is the most instructive single item in this document.
- **`verify.py` Pass B** checks that a number in the prose exists on disk at the
  precision printed. A wrong number computed consistently is on disk.
- The **staleness check** proves the outputs were generated against the current
  code. Against the current *wrong* code, they were.

All ten were found by a reader going through the month loop line by line.
That is the only method that has worked here, it does not scale, and it is not
guaranteed to have finished. **The honest position after six rounds is not that
the mechanisms are correct; it is that a defect of this class survives until
somebody reads the code, and six readings have found ten.**

The previous version of this paragraph ended "a sixth reading should be assumed
to find more". A sixth reading found three, one of which had been sitting under a
check written to catch precisely it. The sentence stands unchanged for the
seventh, and the rate of discovery is not falling fast enough to argue that the
process has converged. Anyone relying on a level from this instrument, rather
than on the ordering it is for, should read that as the warning it is.

**Something has been built against it, and it is worth being precise about how
far it goes.** `invariants.py` asserts structural statements about what the month
loop must produce — not that cash adds up, which all ten defects left perfect,
but that a household is in the right place at the right time.
@@invariant_proved_count|int@@ of the @@invariant_check_count|int@@ are
proved to bite the way the harness gate is: the defect each was written for is
reintroduced into a copy of `model.py` in memory, the check is required to fail,
and the copy is discarded, across @@invariant_reintroduction_case_count|int@@
reintroduction cases in total. `out/invariant_selftest.txt` records it, and now
names the ones that are **not** proved instead of implying there are none.

**That sentence read "@@invariant_reintroduction_case_count|int@@ of them" for one round, and the file it cites
agreed with it, and both were wrong.** The figure behind it counted
reintroduction *cases*; four of those cases are the same invariant, so three
checks were being credited with a proof that had never been run. Two of the
three were written for named historical defects and simply have no
reintroduction; the third is a boundary check. The self-test's own summary line
computed "the other zero are boundary checks" by subtracting the case count from
the invariant count, which are counts of different things that happened to be
equal.

It is worth being blunt about what that means, because it is the second time in
two rounds the same thing has happened in this same file. Round 6 found an
invariant whose NAME claimed a property its code did not check. Round 7 found
the COUNT of those invariants claiming coverage the suite did not have. The
artefact built to say what is and is not verified was, twice, the artefact
overstating what is verified.

**And one of them was proved to bite while being incapable of catching what its
own name promised.** The round 6 section below is the account; the short version
is that "every acquisition can be billed" read a diagnostic that was
algebraically zero, was reintroduced against the single line that diagnostic was
written for, refused it, and was reported as proved — while two of the four
exits it was named after were violating the property in every run. Being proved
to bite is necessary and it is not sufficient. It shows the check can fail; it
does not show the check covers what its name says.

**Three things it does not do.** Some of the checks are containment or
boundary statements that no defect found so far has violated, so they are
untested in the only way that matters. One is not an invariant at all but a
regression tripwire, thresholded between the correct code's value and a known
defect's, and it is labelled as one in the file: it will catch that defect
returning and will not catch a new one. And the whole suite was written *after*
seven defects were known, so it is fitted to the defects that have been found. A
defect of a shape nobody has met yet will pass it.

**The stronger thing still has not been built**: a second implementation of the
month loop by a different route, a cohort-level accounting that tracks each
acquisition's own months and cash and reconciles to the aggregate series. That
would catch all @@mechanism_defect_count|int@@ without having been told about any of them. It is a day of
work, it is the largest single improvement available to this instrument, and it
is not in the open items because it is a question about this directory rather
than about the business.

**Two things the suite found on its first run**, which is the only evidence that
it does anything: `sessions_delivered` mixed consumer and institution sessions,
so a sessions-per-household figure built from it would have been the same
contamination as CHANGELOG 5.2; and the round 5 arrivals fix compared a churned
stock against un-churned arrivals and clamped the difference at zero, which hid
the mismatch and made the exemption slightly too generous on paths with a small
standing book. Neither was found by a reviewer.

---

## What a sixth adversarial round found, which was three more live mechanism defects

The protocol this document was built under says to run paired fresh-context
reviews until a round returns nothing new, and to expect three rounds. This is
the sixth, and it returned three live mechanism defects in the month loop, a
duplicated function carrying arithmetic a previous round had removed, and a
diagnostic that was arithmetically incapable of firing. The count of mechanism
defects found by reading the loop is now **ten**, across rounds 2, 4, 5 and 6.
Every one of them passed every automated gate in this directory on every run
while it was wrong.

### The invariant that was named for a property it did not check

This is the one worth reading even if nothing else here is.

Round 5b added `invariants.py` as the answer to exactly the problem the section
above describes: the gates cannot see a defect that is in the published run, so
the loop needs structural checks that are not about reproduction. The first
invariant in the list is called **"every acquisition can be billed"**, and its
docstring asserted that "every acquisition must be able to produce billed
household months". That is a real property and it is the right one to check.

What the check actually read was a single diagnostic column, and that column
compared what the two examination-sitting exits removed against what they ought
to have removed. Given the line immediately above it, those two expressions are
the same expression. The column was zero by construction. It could not become
non-zero unless someone edited the one line it was written against — which is
precisely what the self-test did, and the self-test passed, and the suite
reported the check as one of four "proved to bite".

Underneath it, two of the four examination-calendar exits — the summer lapse and
the year-group progression — were deleting households in the month they arrived,
for five rounds, worth @@limits_round6_arrivals_fix_usd|usd0@@ of terminal cash
against the @@limits_round5_sitting_fix_usd|usd0@@ that the two exits it COULD
see were worth. The check read zero in all sixty months of every run the whole
time. Those two figures are measured by putting each defect back and re-running,
and they are in `out/invariant_defect_costs.csv` with everything else the suite
has been proved against.

An invariant fitted to one line and named for a general property is worse than
no invariant at all, because the name is what a reader trusts and the name was
doing work the code was not. The diagnostic is now written against the arrivals
array rather than against any exit, and the self-test reintroduces each of the
offending exits separately and confirms the check refuses each one.

The general lesson, which applies to every check in this directory and not only
that one: **a check written after a defect, against the defect, tests the fix
and not the property.** The suite still says so about itself, and now it says it
with an instance.

### A clamp that concealed rather than prevented

The three segment shares did not sum to one. Two were drawn independently and
their sum exceeds one on a twentieth of paths; an `np.maximum` floored the third
at zero and rescaled nothing. On those paths the model billed households it had
never bought. It is fixed and it is now an invariant, but the thing to take from
it is that the clamp is what made it invisible: without the `np.maximum` the
pre-examination share would have gone negative and the defect would have
surfaced in the first run. Every remaining clamp in `model.py` is a candidate
for the same reading.

### What is still not clean after this round

**The all-in contribution per household month mixes two channels.** `model.py`
computes it as net cash plus acquisition spend plus verification, over
**consumer** household months. Net cash carries the institution channel's entire
cost base — the United Kingdom sales reps, the institution platform heads, the
security certification, the per-school onboarding and the school inference —
against a channel that is about one per cent of net revenue. Round 5 fixed
exactly this contamination on the GROSS row and left it on the all-in row, which
is the row the write-up calls the one that answers whether a household pays for
the business that serves it. Removing the institution channel entirely moves the
pooled figure from @@scenario_por_final_year_allin_contrib_pooled|num2@@ to
@@scenario_por_no_schools_final_year_allin_contrib_pooled|num2@@ and the median
path from @@scenario_por_final_year_allin_contrib_median|num2@@ to
@@scenario_por_no_schools_final_year_allin_contrib_median|num2@@, both read off
the `por_no_schools` scenario rather than typed in. The
figures quoted in section 4 and in item 19 inherit it. It is left rather than
fixed because there is a real question about which basis is wanted, and the
answer is the owner's: the honest position is that the row as published is
neither a consumer figure nor a whole-business figure.

**The acquisition budget cap is blind to every variant's mechanism.**
`expected_contrib_pm` takes no configuration. It always credits overage revenue,
so under the enforced-allowance scenario the cap believes in revenue that is
never billed; it never subtracts the app-store fee or the creator revenue share;
it always uses the Bengaluru support rate even under onshoring. Every
cost-adding scenario therefore runs an acquisition budget a company that knew its
own economics would not run, and the contamination has a known sign. Measured on
the two largest cases it is about one per cent of the allowance-enforced delta
and about two per cent of the app-store delta — small, but systematic, and it
was not written down before this round.

**"Met" and "missed across the whole prior range" are decided on two points.**
When the bisection finds no bracket, the status is read off the two endpoint
evaluations alone. If a metric were non-monotone with an interior excursion past
the target, the label would be wrong. The two rows the write-up calls the most
actionable positive result in the file were checked on a nine-point grid this
round and are monotone, so those two labels are sound. The other
@@breakeven_rows_unbracketed_missed|int@@ rest
on two evaluations each and are not independently checked.

**The band-placement stability argument is measured where the construction
forces the answer.** Bands are ranked on terminal cumulative cash, so the
central band line's placement at the final month is pinned near the fiftieth
percentile by construction, and measuring it across scenarios measures the
construction rather than the model. `out/variants_bands.csv` carries the low and
high bands too, and nothing in the prose reads them: the high band's
cross-scenario placement at mid-horizon moves several times further than the
central band's does at the terminal month. The conclusion the section draws —
that terminal band lines may be compared across scenarios — is true of the band
and the month it was measured on, and is stated more narrowly than it was.

**The demand-independent share omits the launch subsidy.** For twelve months
after go-to-market the acquisition envelope is a fixed dollar amount independent
of revenue and of the demand shock, tapering over the twelve after that. It sits
in the acquisition line and therefore outside the content-people-step sum the
document calls demand-independent. Including it raises that share by about one
percentage point, which pushes the document's own argument further in its own
direction and is recorded here rather than folded in silently.
