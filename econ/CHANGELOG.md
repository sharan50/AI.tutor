# Change log

One entry per round. What was found, what was fixed, what was deliberately left,
and what the numbers moved from and to.

Seed 20260916 throughout. Run date 2026-09-16. A figure re-derived from a
different seed is a different number, so nothing here is comparable to a run
under another seed.

Intermediate values quoted in this log come from superseded runs. They are not
derivable from the current outputs, which is the point of a change log, and they
are declared in `verify_allow.csv` so the verifier reports rather than hides them.

---

## Round 0: defects found while building, before any review

These were found by running the thing, not by reviewing it. They are recorded
because several of them are exactly the defects the brief's checklist predicts,
and a model that claims to have none of them should be disbelieved.

### 0.1 The acquisition budget deadlocked at zero

**Found.** The budget cap that stops acquisition spend exceeding a fraction of
lifetime value was computed from *realised* contribution per active household.
Before the first customer exists there is no realised contribution, so the cap
was zero, so the spend was zero, so no customer was ever acquired. The model ran
cleanly and reported that no path in twenty thousand ever reached profitability.

**Fixed.** `expected_contrib_pm()` in `model.py` forecasts contribution from the
drivers instead, which is what a company setting a budget would actually do.

**Moved.** Share of paths reaching profitability from 0.0000 to 0.1935. Mean peak
funding requirement from 27,778,913 to 24,156,582.

### 0.2 The UK-only comparator was charged for scope it does not open

**Found.** `headcount()` hired Route B field sales representatives, and
`step_costs_usd()` paid for United States and India entities, foreign counsel and
an information security certification, in every scenario, including the UK-only
comparator that opens none of them. This is checklist item 9 in reverse: not a
base case containing a scenario it rejects, but a comparator carrying costs it
never incurs, which makes every scenario comparison invalid.

**Fixed.** Both functions now take `cfg` and gate on `_open_month()` and
`_school_open_month()`.

**Moved.** UK-only monthly UK people cost at month 40 from 87,326 to 24,961.
UK-only total content cost from 16,461,584 to 8,596,098. The plan of record was
unchanged, which is why the defect could have survived indefinitely.

### 0.3 The India switch could not open India

**Found.** `CONSUMER_OPEN[M_IN]` was hard-coded to infinity to keep India out of
the published run, so `variant_india_d2c` produced output identical to the base
and would have been reported as "India direct to parents changes nothing".

**Fixed.** The month is real and the `india_d2c` switch is what closes it.

**Moved.** The India direct-to-parent variant from exactly equal to the base, to
a terminal cash mean 87,101 above it. The conclusion survived, but only by
accident, and the mechanism that produced it was not running.

### 0.4 The launch acquisition subsidy never switched off

**Found.** `acq_preseed_ramp` added a fixed monthly acquisition budget, sampled
between 6,000 and 120,000 dollars, on top of the revenue-linked rule, for all
sixty months. A standing subsidy that does not depend on revenue and never stops
is not a budget rule. It was the reason the narrowest scope still consumed
millions.

**Fixed.** Renamed `acq_launch_ramp` and tapered: held for twelve months after
go-to-market, then to nothing over the following twelve, after which acquisition
is funded only from trailing revenue.

**Moved.** Plan-of-record mean peak funding from 24,156,582 to 23,817,937. The
one-subject scope's median peak funding from 5,637,538 to 5,214,404.

### 0.5 A currency unit error in the UK salary line

**Found.** The driver `uk_usd_yr` was documented as GBP-quoted and named USD, and
`school_onboard_cost` used it without converting.

**Fixed.** Renamed `uk_gbp_yr`; the conversion applied at both sites.

### 0.6 The creator licence had no cost term at all

**Found.** D4 makes named-educator personas the wedge and D14 requires named
presets shipped from day one, and the model charged nothing for them. Checklist
item 8: absence is not conservatism.

**Left, deliberately, and priced beside the model.** The published run still
carries zero, because D5 describes a one-page name-and-likeness agreement and the
vault has never established what a creator charges for one. Putting a number in
the base would invent the very figure that is missing. Instead `cfg["creator"]`
adds both limbs of a real licence, drawn from the auxiliary stream, and the
`por_creator_fees` scenario publishes what it costs. The assumption that creators
sign for nothing is now visible rather than implicit.

### 0.7 Four fifths of the run time was scipy overhead

**Found.** `scipy.stats.gamma.sf` cost 22.4 seconds of a 27.6 second run.

**Fixed.** Swapped for `scipy.special.gammaincc`, which is what it calls
underneath, and the seasonal overage integral is now computed once per phase per
month rather than once per market per segment. Verified bit-identical: both
published CSVs kept their sha256 across the change.

**Moved.** Nothing. That is the point.

---

### 0.8 Every narrow comparator was charged a platform team sized for the widest one

**Found.** Platform engineering was a decided ramp from four heads to twenty-two,
scaled by a sampled multiplier and by nothing else. A scenario opening one market
with one subject and no institution channel was charged the same engineering team
as the plan of record, which opens three consumer markets and an institution
channel. Since the central recommendation this instrument produces is about scope,
a cost base that does not respond to scope on its second-largest people line makes
that recommendation untestable. This is checklist item 10: the comparators were
not like for like.

**Fixed.** Platform headcount is now a floor, because the product must exist at
all, plus `PLATFORM_PER_EXTRA_MARKET` heads for each additional live consumer
market and `PLATFORM_FOR_INSTITUTIONS` heads for running the institution channel.
Both constants are decisions, stated in `model.py`, and neither is a measurement.

### 0.9 The reachable pool did not respond to how many subjects the product covered

**Found, running the other way.** `pool_uk` is documented as reachable United
Kingdom households, and it was applied unchanged whether the product covered one
subject or eleven. Having just stopped over-charging narrow scopes on engineering,
this would have left them over-credited on demand.

**Fixed.** The driver is now defined at the five-subject go-to-market scope and
scales sublinearly with subject breadth, `(subjects / 5) ** 0.6`. Again a decision
with stated constants.

### 0.10 The launch-delay scenarios are contaminated by the horizon

**Found, in the draft write-up rather than in the code.** The draft explained a
six-month launch delay costing less than a three-month one by appeal to the
September intake. That explanation is wrong. `launch_shift` moves the content
schedule along with the market openings, so a six-month shift pushes the
month-54 content step past the end of the horizon and the run never pays for it.

**Left, and labelled.** The scenarios are kept because "later is worse" is real,
and the content-cost delta that produces the non-monotonicity is now published
beside them so the artefact is visible. No calendar conclusion is drawn from them.

### 0.11 The gate had never been shown to refuse

**Found.** The harness's character-for-character check had only ever been seen to
pass. A gate that has never refused is not evidence of anything.

**Fixed.** `python3 harness.py --selftest` perturbs one field of the published
file by one unit in its last decimal place, requires the harness to refuse,
restores the file and requires it to verify again. The result, including the
sha256 of the restored file, is written to `out/harness_selftest.txt`.

---

## Round 1a: found by pulling every figure the write-up quotes, before the reviewers reported

### 1a.1 The mean contribution per household month was not a number

**Found.** `final_year_contrib_per_hh_month` is a ratio whose denominator, final-year
household months, goes to zero on paths whose book has collapsed. 84 of 20,000
paths exceeded a thousand dollars a household month and the maximum was 3.2e10, so
the **mean** of that column was 2,314,540 dollars per household month. The all-in
version was worse: 3,245 paths beyond a thousand, and a mean of -96,521,075. The
lifetime value to acquisition cost ratio inherited it and read 193,413.

The medians were sane throughout, which is why this survived a first reading: the
figure looks fine until you ask for the mean.

**Fixed.** The mean is published nowhere. Two figures are published instead: the
pooled ratio, total contribution over total household months across every path and
month of the final year, and the median path's own ratio over the paths that have
a final year at all. Both are computed in `cohorts.py` from the verified monthly
arrays, so the published CSVs did not have to be regenerated.

**Moved.** Gross contribution per household month from a meaningless 2,314,540 to
32.89 pooled and 27.33 on the median path. All-in from -96,521,075 to 19.85 pooled
and -109.95 on the median path. Lifetime value over acquisition cost from 193,413
to 2.00.

**And it exposed something worth having.** The pooled and median all-in figures
disagree in sign. Pooled, a household month contributes 19.85 dollars all-in; on
the median path it consumes 109.95. The pooled figure is dominated by the few
paths with large books, which carry most of the household months and spread the
fixed costs across them. Both are now published, because quoting only the pooled
one describes a business that most paths are not running.

### 1a.2 "The model is interaction-dominated" was true of one target in four

**Found.** The write-up asserted it flatly. The first-order Sobol sums are 0.138 on
terminal cash, 0.772 on its rank transform, 0.742 on the peak funding requirement
and 0.507 on whether a path reaches profitability. The claim holds only for raw
terminal cash, and there it is a property of the tail rather than of the model.

**Fixed.** The write-up now says which target is interaction-dominated and why, and
says plainly that on the robust targets the ordering can be read as an ordering.
The correction makes the document's central claim stronger, not weaker.

### 1a.3 The price-anchor figure was the wrong quantity

**Found.** The write-up said the price anchor is worth
`delta_por_anchor_software_terminal_cash_mean` "between its two states". That figure
is the software-anchored scenario against the published run, and the published run
is a fifty-fifty mix of the two regimes. The spread between the regimes is a
different and larger number.

**Fixed.** `anchor_tutoring_minus_software_terminal_cash_mean` is now computed in
`figures.py` and quoted at all four sites, with the mix explained where the
scenario table shows both columns.

### 1a.4 figures.csv could silently overwrite a figure

**Found.** `figures.py` wrote 1,283 rows which loaded as 1,163 unique names. The
duplicates were identical values from the rescue grid re-adding its axis labels,
so nothing was wrong. But a name collision carrying two different values would
have let a later row overwrite an earlier one, and every figure in that file is
quoted somewhere by name.

**Fixed.** `add()` now refuses a name collision that carries a different value, and
drops an exact repeat. At the time of this entry that took the file from 1,283
rows to 1,163, written and loaded alike; the current count is whatever
`figures.py` last reported and is not this number.

---

## Round 1b: two reviewers in fresh context, given only the artefacts

A coherence pass and an adversarial pass, each run with no knowledge of how the
instrument was built. Between them they found more than thirty items. Every
structural claim below was verified against the code before being accepted; all
of them held.

### Model defects

**1b.1 India age assurance was charged twice and credited at zero.** The
acquisition loop charged India double verification, correctly, because verifiable
parental consent under the DPDP Rules is a heavier process. `ltv_estimate`
credited India nothing. The India acquisition budget cap was therefore struck on
a lifetime value that omitted the largest India-specific unit cost. Both now call
one `verification_cost()` function.

**1b.2 The demand shock cost nothing.** `realised_spend = acq * cac_b` recomputed
spend from realised acquisitions, so a shock that halved customers also halved
the money spent. The model could not represent spending a budget and getting
nobody, which is the only way a demand shock ends a company. Checklist item 18's
"clean" verdict was resting on a shock that did not bite. Spend is now committed
in advance and only running out of market reduces it.

**1b.3 Cumulative acquisition was unbounded.** The reachable pool capped the
standing book and nothing capped the flow, so a path could churn and reacquire
its way to tens of millions of households in a market of a few million. The worst
path bought 51.5 million. `POOL_REACQUISITION_MULTIPLE` now caps cumulative
acquisitions per market at three times that path's own pool.

**1b.4 The institution channel was charged an India content bank it never bills.**
The India content build and the India entity were gated on the institution switch,
but `SCHOOL_OPEN` is only ever read for the United Kingdom, so there is no India
institution motion in this model at all. Dropping the channel therefore dropped an
India item bank, and roughly forty-six per cent of "the cost of Route B" was that
bank. India content is now gated on India trading, and the dead per-market
`SCHOOL_OPEN` entries are gone.

**1b.5 The suffix-discipline gate could never fire.** It tested whether a column
name ended in both a mean suffix and a band suffix, which no string can do. It
also ran on one of the two writers. It is now a real check on both, and
`suffix_discipline_selftest()` shows it refusing four headers it must refuse. The
first thing it caught was a genuine ambiguity: the driver `sessions_mean` ended in
an aggregate suffix inside a per-path file, and is now `sessions_per_hh_month`.

### Reporting defects

**1b.6 The passage claiming matching was measured got the measurement wrong.** It
named two scenarios as the loosest and tightest rank correlation and neither was
the bound in the file. The real loosest is the dependence scenario at 0.28, three
times looser than quoted, and that is correct behaviour rather than a defect:
Iman-Conover deliberately does not preserve path identity. Both figures are now
computed from the column rather than hand-picked, and the dependence scenarios are
separated out with the reason.

**1b.7 Every scenario delta was a mean of a heavy-tailed distribution.** The
median delta flips sign against the mean for several scenarios. The scenario table
now carries the mean, the median path and the effect on peak funding side by side,
with a column saying whether the first two agree in sign.

**1b.8 The break-even section implied the narrow scope produced answers.** Both
scopes are unbracketed on every row. The section now says so, and the rescue grid,
which was built and then never written up at all, is now section 10's second half.

**1b.9 The staged rounds and the headline are computed by different rules.** Each
staged round carries six months of buffer and the whole-horizon figure carries
none, so the three staged rounds sum to about a third more than the number the
document led with. Both are now printed with the difference named.

**1b.10 The summer is not what costs the Year 10 advantage.** The write-up blamed
it, following docs/10's own caveat. Removing the summer entirely lifts the ratio
to 1.75, not 2; only pinning in-term churn to its floor as well recovers 2. The
open item now sends the owner to measure in-term churn first and the summer
second.

### Added because they were absent

**1b.11 The restricted transfer of United Kingdom children's data to Bengaluru.**
docs/05 names it and marks it unconfirmed, and nothing in the model touched it.
If counsel forces the learner path onshore, people overtakes content as the
largest cost line and the sensitivity ordering the whole document is built on
inverts. `onshore_share` prices it, two scenarios run it, and it is open item X8.
It is the single most consequential thing either reviewer found.

**1b.12 Regulatory enforcement exposure and examiner supply**, both priced at zero
in `out/omissions.csv` and named there, because a zero written down is not the
same as a line left out.

### Left deliberately

The base model still has **no price elasticity of demand**: raising the price
raises acquisitions, because price feeds the budget cap and nothing else. Splitting
the feedback bundle so the price loop runs alone is half a day and has not been
done. It is stated plainly in LIMITS.md, and it means the anchor spread is an
upper bound.

The **foreign-market calendars** are the United Kingdom's with a shift. The
southern-hemisphere academic year, the absence of a terminal sitting in the United
States, and the treatment of a dozen curricula as one bucket are all named in
LIMITS.md and none is fixed. They do not change the ordering, because the ordering
is set by two market-agnostic drivers, and they do mean no foreign-market level in
this document should be argued from.
