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
underneath, and the seasonal overage integral is now computed once per
(phase, segment) per month rather than once per (market, segment), which is what
the code comment says and what the code does. Verified bit-identical: both
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

**Left, and labelled.** The scenarios are kept and the content-cost delta that
produces the non-monotonicity is published beside them. At the time of this entry
the write-up still said "later is worse" was real; round 2 showed that even that
does not survive the median and capital columns, and that the contamination runs
both ways. See 2.5.

### 0.11 The gate had never been shown to refuse

**Found.** The harness's character-for-character check had only ever been seen to
pass. A gate that has never refused is not evidence of anything.

**Fixed.** `python3 harness.py --selftest` perturbs one field of the published
file by one unit in its last decimal place, requires the harness to refuse,
restores the file and requires it to verify again. The result, including the
sha256 of the restored file, is written to `out/harness_selftest.txt`.

---

## Round 1a: found by pulling every figure the write-up quotes, before the reviewers reported

**Figures in this round are from the model as it stood at the time, before the
round 1b model fixes changed them.** They are recorded because a change log that
restates itself after every later change is not a record of anything. The current
values are in `out/figures.csv`.

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

**1b.8 The break-even section implied the narrow scope produced answers.** At the
time of this entry both scopes were unbracketed on every row, and the section was
corrected to say so. Round 2 then found that a third target had been added and
four rows now bracket, which made the correction itself wrong; see 2.1. The
rescue grid, which was built and then never written up at all, is section 10's
second half.

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

---

## Round 2: the same two reviewers, fresh context again, on the corrected artefacts

The brief that commissioned this work predicted that the third round would find
the worst defect, because the first two clear the surface and the third reaches
the structure. That is what happened. Every code claim below was verified against
the model before being accepted; all of them held.

### 2.1 Section 10's central claim was false, and the truth is a better finding

**Found, by both reviewers independently and by pulling the figures myself.**
The write-up said ten questions were solved and "every one is unbracketed". There
are twelve per scope, and **four bracket**, all on the profitability target and
all on the two drivers section 8 says decide whether the venture exists.

The four thresholds were sitting in `out/breakeven.csv` unmentioned, and they are
the most actionable numbers the instrument produces. The narrow scope reaches
half-of-paths profitability at a price that is roughly one hour of GCSE tutoring a
month, which is inside docs/07's own substitution table rather than outside it.

**Why it survived.** The count was hand-typed, and `verify.py` cannot read a
word. `figures.py` now counts bracketed rows, questions, targets and distinct
drivers from the file, and section 10 is rewritten around the four solves.

**Also fixed in the same place.** `bisect()` returned the converged bracket in
the endpoint columns on a bracketed row and the support endpoints on an
unbracketed one, so a reader opening the CSV saw two different quantities under
one pair of headers and would have concluded the metric was flat across the whole
prior range. Both columns are now always the support endpoints.

### 2.2 The only price-to-retention mechanism had its sign backwards on half the sample

**Found.** `feedback_params()` referenced the price to the median over ALL paths.
The two price regimes are far apart, so that reference landed in the gap between
them: every tutoring-anchored path got a churn penalty and every software-anchored
path got a churn **bonus**. Measured on the published draws, the multiplier
averaged 1.617 on tutoring paths and 0.621 on software paths, and exactly half the
sample was being rewarded for its price.

So "the feedback loops cost X" was substantially a transfer between price regimes,
and it damaged precisely the regime the document's second-ranked decision depends
on. The comment above the line said it was referenced to the tutoring band so that
software paths were not penalised; the code did something else.

**Fixed.** Each regime is now referenced to its own modal price, so the elasticity
is within-regime and correctly signed everywhere. The multiplier now averages a
penalty in both regimes, only paths priced below their own regime's mode get
relief, and the correlation with price inside the tutoring regime is 0.85.

### 2.3 The allowance-enforcement scenario enforced the billing cap instead

**Found.** `enforce_allowance` truncated delivery at `OVERAGE_CAP_MULT *
SESSION_ALLOWANCE`, which is forty sessions, not at the sixteen-session allowance,
and left the overage revenue in place. It priced cutting a learner off at a level
almost nobody reaches. The figure was quoted in four places, including as owner
decision 4, and the framing around it was about the posture toward a struggling
learner.

**Fixed.** It enforces the allowance and removes the billed overage with it, which
is what the commercial decision actually is.

### 2.4 Saturation was measured on the standing book, not on cumulative reach

**Found.** The penetration term feeding both the effective-cost curve and the
budget cap was the instantaneous book over the pool. On a high-churn path the
company could sell to its whole market several times over while the mechanism
meant to make acquisition harder never rose above a fifth. `POOL_REACQUISITION_MULTIPLE`,
added in round 1b, bounded the arithmetic and left the economics untouched: it
fixed the symptom.

**Fixed.** Pressure now rises with cumulative reach, so the effective-cost curve
the write-up presents as the reason the anchor understates at scale is driven by
the quantity it claims.

**Moved.** This entry recorded no figures, which was an omission: it is the
round-2 fix with the largest effect on the acquisition mechanism. Plan-of-record
terminal cash at the mean moved from -8,682,961 at the end of round 1b to
-11,711,069 across the round 2 fixes taken together, of which this was one. The
entry cannot separate its own contribution, because four mechanism fixes were
regenerated in one pass; that is the honest record of it rather than a number
invented after the fact, and the two endpoints are read off the committed
`out/variants.csv` at each round rather than from a working note.

**Left, then fixed in round 3.** `POOL_REACQUISITION_MULTIPLE` came out of this
doing two jobs — bounding cumulative acquisitions and setting the saturation
denominator — as a literal in `model.py` that nothing could vary and no
sensitivity instrument could see. Round 3 made it a configuration key with two
scenarios. See 3.9.

### 2.5 The onshoring scenario moved the wrong people, and X8 was over-claimed

**Found.** `onshore_share` scaled the whole Bengaluru head count, which is
platform engineering plus content authoring plus general and administrative. At
month 12, 63 per cent of what it relocated was content authors and administration,
who work from published DfE subject content and see no learner. It also left
Bengaluru support, the people who actually read learner conversations, where they
were. A transfer restriction would do close to the opposite.

**Fixed.** It now moves platform engineering and support, and neither content
authoring nor administration.

**And the claim about it was too strong.** The write-up said the restricted-transfer
question "inverts the sensitivity ordering". A reviewer ran the decomposition
under full onshoring: it re-ranks, putting a United Kingdom salary driver into the
top three on capital, and content drivers still hold most of the top seven. The
write-up now says re-ranks. It is still the largest thing a letter to counsel
could resolve.

### 2.6 A second omission that changes the ordering, not the levels

**Found, and not admitted anywhere.** The horizon writes the item bank and the
standing book to zero at month 60. A large share of the content spend falls in the
last two years and is charged in full against a truncated revenue window, while
the asset it buys has a life well beyond it.

Every statement of the form "content is the largest line" and "content sets the
slope" is partly a function of where the window was cut, and the document already
had the proof and misread it: the launch-delay scenarios move because one content
step falls past month 60, and the write-up called that a defect in the comparator
without drawing the general conclusion.

**Added.** A `residual` switch credits part of the item bank and the standing book
at the horizon, off in the published run, priced as a scenario. Both its
parameters are priors and neither is a valuation; the point is the size.

### 2.7 Smaller, and there were many

The staging table still listed an India entity and an India pilot the run never
buys, and omitted the rest-of-English-speaking entity it does. The
whole-horizon row of `out/funding.csv` wrote a mean into a column headed p80. The
write-up claimed everything downstream runs through the harness, which is false
for the three scripts that deliberately read only the CSVs. "Four mechanisms are
tested" was five, now six and counted from a file. "Nine named and priced" was
eleven. "M4 is not before M5" is wrong about the roadmap. Two currencies were
presented as one in X8. An app-store cost was written with an inverted sign. The
all-in contribution was defined two ways in two documents. Four table headers
carried units their own rows contradicted. The demand shock's run lengths were
published and its cost never was; it is now measured, and it is a fraction of a
per cent of terminal cash on the mean. The exact figures are in
`out/cohorts.csv` under `shock_cost_*`, and 2.8 below gives the reading.

### 2.8 What the round 2 fixes moved

The allowance decision **changed sign**. With the allowance actually enforced
rather than the billing cap, enforcing destroys value: the overage revenue lost
is larger than the inference cost saved. Owner decision 4 in the write-up now
says the opposite of what it said, and it now agrees with the commercial posture
instead of sitting against it.

The terminal-value residual is worth more than any other scenario in the file,
which is the measure of how much the horizon choice was doing.

The demand shock's measured cost is well under one per cent of terminal cash on
the mean — `shock_cost_terminal_cash_mean` in `out/cohorts.csv`, against the mean
of terminal cash itself — while the run lengths read as though it were the thing
that ends the company. An earlier version of this log said "about one per cent"
in 2.7 and "about half a per cent" here, for the same quantity; both are now
stated the same way and point at the file. Both numbers are published together,
because the run lengths without the cost are the misleading half.

The onshoring scenario got smaller once it moved the right people, and stayed
large.

---

## Round 3: two fresh-context reviews, and the structure gave way

The brief predicted this round would find the worst defect, because the first two
clear the surface and the third reaches the structure. It did. Five of the
findings below are about the *shape* of the argument rather than about a figure
in it, and three of those change a conclusion the document was built around.

Both reviewers were given the artefacts and none of the reasoning. Every finding
was checked against the code before being accepted; two were rejected on the
magnitude and one was accepted in the opposite direction from the one reported.

### 3.1 The scope comparator was mismatched, and the headline conclusion was an artefact

**Found.** Owner decision 1 compared the plan of record against the go-to-market
minimum on the capital requirement and against the United Kingdom-only scenario
on terminal cash, then set the two side by side and concluded, in bold and twice,
that scope is dominant on the statistic that sizes rounds and minor on the one
that measures return. The two comparisons are against different scope reductions.
`ukonly` drops the second market and the institution channel and keeps the entire
United Kingdom content escalation to eleven subjects; its content line is most of
the plan of record's. The conclusion was a property of the mismatch.

**Verified.** Run directly against the model: against the plan of record,
`ukonly` is worth +1,609,577 on the mean and +7,550,724 on the median, while the
go-to-market minimum is worth +9,743,120 and +14,923,687. Six times the size on
the mean, twice on the median.

**Fixed.** Two scenarios added, `por_content_frozen` and `gtm_minimum`, so the
scope ladder has three rungs and the market decision separates from the content
decision. Decision 1 now carries a four-row table, and the corrected reading is
not simply the opposite of the old one. Scope is much the largest decision on the
capital requirement and the third largest on terminal cash, behind the residual
and the price-anchor spread — material on both, where the old text had it at
close to nothing on one. And "scope" turns out to be two decisions: freezing the
content schedule is worth five times what dropping markets is on terminal cash,
while on capital the two are worth about the same. `GTM_MINIMUM_SCHEDULES` moved
into `model.py` so `variants.py`, `funding.py`, `rescue_grid.py` and
`breakeven.py` cannot drift apart.

### 3.2 The sensitivity ordering was computed on one scope and quoted as the ordering

**Found.** Every Sobol index in section 8 is computed on the plan of record. The
document's central instruction — work on acquisition to make the business exist,
on content cost to make it fundable — was stated as a property of the business.

**Verified.** On the go-to-market minimum the capital ordering rearranges:
content drivers fall from five of the top seven to one, and `eng_usd_yr` moves
from rank eight to rank two.

**Fixed.** `sensitivity.py` now runs the decomposition on three configurations
and writes them all to `out/sobol.csv` under the `run` column. `figures.py` keeps
the plan of record's names unprefixed and gives the others their own prefix, so
the two orderings can never be pooled into a third that is true of neither.
Section 8 has a new subsection putting them side by side, and section 1 says the
content ordering follows from the scope decision rather than informing it. This is
the **third** item in the document whose answer changes with a choice rather than
with evidence.

### 3.3 The largest scenario in the file appeared in no document

**Found.** `por_residual` is the largest single scenario in `out/variants.csv`
and `WRITEUP.md` did not mention it.

**Fixed.** It is in the scenario table and has its own reading in section 9,
which states that every number in it is a prior, gives the two prior ranges, and
says why it is not in the plan of record.

### 3.4 Open item X8 still carried both claims round 2 retracted

**Found.** The write-up's onshoring paragraph was corrected in round 2 from
"inverts the ordering" to "re-ranks it". `OPEN_ITEMS.md` still said "the one
unmodelled item that reorders the answer" and "inverts the sensitivity ordering
the whole write-up is built on".

**And the round 2 correction was itself wrong.** It claimed onshoring moves a
United Kingdom salary driver into the top three and pushes item count down.
Verified against the model: under `onshore_share=1.0`, `items_per_unit` stays at
rank 1 on the capital requirement and `uk_gbp_yr` reaches rank 7. Across all four
targets it never enters the top three. Three drafts of the same paragraph, none
of them computed.

**Fixed.** `onshore_all` added as a third Sobol run, so the paragraph is read off
a file. Both documents now say onshoring is the largest single unmodelled item by
cash and does **not** rearrange the ordering, and X8 no longer claims to be the
only such item — the residual is larger in the other direction.

### 3.5 The break-evens were solved against a target that is not viability

**Found.** The four solved break-evens are all against "half of all paths run
three consecutive cash-positive months", and the write-up called the result the
point at which "half of this becomes viable".

**Verified.** At the plan of record's break-even price the median path still ends
the horizon deeply negative, peak funding at the eightieth percentile is barely
moved, and a third of the paths that *hit* the target still end with negative
cash. (One reviewer put that last share above half. Recomputed on the regenerated
run it is lower than that, and the point stands on either figure: a path can
string three cash-positive months together and still lose money over the
horizon.)

**Fixed.** `breakeven.py` now reports, for every solved row, the two statistics
the solve did not target and the share of target-hitting paths that still end
negative. Section 10 quotes them and retracts the word viable.

### 3.6 The off-test is a stream test and was reading as a mechanism test

**Found.** Section 3 presented the switched-off reproduction test as the thing
that makes the mechanisms trustworthy. All four of round 2's mechanism defects
passed it on every run while they were wrong.

**Fixed.** The test is now two-sided — off must reproduce exactly, on must not —
which catches a mechanism that is wired up and inert. Section 3 says plainly that
neither half is a correctness test, names the four defects that passed it, and
says reading the code is how they were found.

### 3.7 The gate covers two of the output files and the document implied more

**Found.** The character-for-character gate covers `por_monthly.csv` and
`por_paths.csv`. Nothing checks the other derived outputs.

**Fixed.** `harness.load()` records the SHA-256 of the `model.py` each script ran
against into `out/provenance.csv`, and `verify.py` gained a pass that fails the
whole run if any recorded hash is not the current one. It is a staleness check
rather than a reproduction check and is described as the weaker thing it is.

### 3.8 Two omissions priced at zero could be sized, and one was missing entirely

**Found.** The consumer subscription regime and involuntary churn are retention
mechanics, correctly zero as cost lines, and were given no size at all when
`cohorts.py` could produce one. Separately, specification change and curriculum
reform are absent from the model, the limits, the open items and the omissions
file: `content_full_equivalents` only ever rises and no item ever expires, on a
five-year horizon.

**Fixed.** `omissions.py` runs a churn stress and writes the cash consequence to
`out/sized_omissions.csv`, which LIMITS item 8 quotes. Specification change is a
priced omission line and a new open item X11 with an owner and a trigger that can
actually produce the quantity, the awarding bodies' published reform timetables.

### 3.9 A constant doing two jobs, invisible to every instrument

**Found.** `POOL_REACQUISITION_MULTIPLE` bounds cumulative acquisitions and is
the denominator of the saturation term. It is a literal, so no sweep, no Sobol
index and no scenario could see it, and nothing in the vault sets it.

**Fixed.** It is a configuration key with two scenarios, `por_reacq_low` and
`por_reacq_high`, and an off-test entry. LIMITS names it load-bearing and says
that a constant moving the answer while being invisible to the sensitivity
analysis is a defect of the instrument.

### 3.10 The all-in lifetime value comparison was published on the gross basis only

**Found.** "Lifetime value is below acquisition cost" was published at a small
percentage of paths on the gross basis and nowhere on the all-in basis. That is
checklist item 16 — a gross margin presented as a net one — committed by a
document whose answer to item 16 was "clean".

**Fixed.** Both shares are computed in `cohorts.py` and published beside each
other in LIMITS items 16 and 19, and item 19's table now says for each row
whether the write-up asserts the proposition or denies it.

### 3.11 Smaller, and again there were many

Section 11 named an India entity in the staging that `out/funding_commitments.csv`
does not contain, and LIMITS called both foreign entities seed-window when one
lands in the Series A; both are now counted from the file. The United
Kingdom-only scenario drops two consumer markets, not three. Section 1 quoted the
whole-horizon funding figure without saying it is the smaller of the two numbers
in the document. Section 12 said items 3 onward were ordered by terminal cash;
they are grouped, not ordered. `OPEN_ITEMS.md` claimed an ordering its own first
two rows break. The break-even table headed a column "Prior median" and put a
mode in it. The examiner-hours figure counted the catalogue rather than the full
item-bank equivalents the model builds, and was too large by about a factor of
two. X9 said the *smallest* penalty in the reference class exceeds every cost
line except content and exceeds the seed round; the largest does, the smallest
does neither, and the comparison is now computed in `omissions.py`. E4 said age
assurance subtracts from the acquisition budget pound for pound; it does not, and
the mechanism is now described. `SHOCK_BAD_THRESHOLD`'s comment said "at or
below" against a strict inequality. A figures name said tutoring minus software
over an arithmetic that did the reverse. A share rendering as "0.0 per cent" now
renders at two decimals. Three `verify_allow.csv` reasons described superseded
values as current. `econ/README.md` still carried the harness claim round 2
corrected in the write-up. Section 3's "four accounting identities down the whole
monthly file" is three down the file and one point check, and a fifth was added
that checks the section 12 scope ladder decomposes exactly, because owner
decision 1 now rests on reading it as two separable decisions. The auxiliary priors
drawn outside the published stream were literals in `variants.py` quoted in prose
with no file behind them; they are now declared once and written to
`out/aux_params.csv`.

### 3.12 Rejected, and why

The reviewers were wrong twice and imprecise once, and the brief says to check.
One report treated the Iman-Conover scenarios' low path correlation as a defect;
it is the documented and intended behaviour of rank reordering and section 3
already says so. One treated the residual scenario's size as evidence that the
horizon is too short; the horizon is the owner's instruction and the residual
prices what that instruction costs, which is the point of running it.

### 3.13 Two more, found by the author rather than by a reviewer

**`units_target()` was dead code that would have been wrong if used.** It read
`UNIT_SCHEDULES` directly rather than the configuration's schedules, so any
future caller would have silently ignored every narrow-scope scenario. Nothing
called it. Removed rather than fixed, with a comment saying why, because dead
code that would be wrong if used is worse than no code.

**The claim that no draw happens inside the month loop was asserted, and what
the document offered as evidence was a consequence rather than the fact.** Every
paired comparison in the write-up depends on it. The harness now refuses any
`model.py` with a draw call inside its `LOOP` section, and `--selftest` proves
that second gate refuses by inserting one into a copy of the file. Both gates
are recorded in `out/harness_selftest.txt`.

**And the staleness check from 3.7 bit for real during this round**, on a
comment-only edit to `model.py` that left both published CSVs byte-identical. It
invalidated every derived output and forced a full regeneration. That is the
intended behaviour and it is not free; `econ/README.md` says so, and says why a
check that tried to hash only the code would be the wrong trade in a repository
where a misleading comment is a defect these reviews keep finding.

---

## Round 4: back into the month loop, and it found two live defects and a sign

Round 3 reached the structure of the argument. Round 4 went back into the code
and found two mechanisms wrong in the published run, plus an owner decision
published with its sign inverted. Every finding was checked against the model
before being accepted; the two mechanism defects reproduced to the dollar.

### 4.1 An owner decision was published with its sign inverted

**Found.** Section 12's decision 6 read "Direct to parents is **worth**
3,239,977 over five years against DPDP section 9(3)", and section 2 said the same.
`out/variants.csv` says `por_india_d2c` terminal cash is -14,951,046 against the
plan of record's -11,711,069. Opening India direct to parents **destroys** that
much cash and **raises** the capital requirement by 4,450,728.

**How it survived four documents and a verifier.** The sentence renders
`delta_por_india_d2c_terminal_cash_abs`, whose own derivation note in
`out/figures.csv` says the direction lives in the sign of the other token. Every
other negative scenario in the document is written as "costs"; India was the only
one written as "worth". `verify.py` Pass B passed it on every run, because the
absolute value did exist on disk to the precision printed. This is the limit
section 13 describes, biting on a decision rather than a detail.

**Fixed.** Both sites now say "costs", give the median and the capital figures
beside the mean, and state the conclusion that follows: on these priors DPDP
section 9(3) is not a prohibition the owner is paying for.

### 4.2 The A-level exit fired on the cohort in the month it arrived

**Found.** In the examination-calendar block, arrivals from GCSE were added to
the A-level stock and the A-level *sitting* exit rate — sampled 0.35 to 0.72 —
was then applied to the whole stock including them, two years before their own
sitting. The two lines were in the wrong order.

**Verified.** Swapping them and re-running: terminal cash at the mean
-10,661,517 against the published -11,711,069.

**Moved.** +1,049,552 on the mean, larger than the entire persistent-demand-shock
apparatus and comparable to the creator-fee and app-store scenarios that have
their own rows in the scenario table. It passed the harness gate (it was in the
published run, so byte-exactness confirmed it), the off/on test (it is not a
switchable mechanism) and every accounting identity (it moves stock, not cash).

### 4.3 The acquisition budget cap believed in a household 2.6 times longer-lived than the model delivers

**Found.** `ltv_estimate` is the company's own running estimate of what a
household is worth and the only restraint on acquisition spend anywhere in the
model. It computed a geometric life from `churn_base` with constant caps, and
ignored two things the loop does: an acquisition is hit by `churn_m1_extra` and
then by `churn_base` in the month it arrives, before it is ever billed; and an
examination-year household is wiped at the sitting whatever its churn rate.

**Verified.** Assumed months: mean 8.351. Realised months in the same run: 3.309.
`budget_cap_from_ltv` inverts the saturation curve, so permitted spend scales as
roughly the square of the estimate.

**Fixed.** Both are now taken from the loop's own quantities: a first-month
survival factor, and a cap at the months remaining to that market's next sitting
rather than at a constant. **Not closed.** The estimate still runs ahead of
realised retention, partly because a geometric life ignores the other exits and
partly because realised retention is itself right-censored by the horizon (4.9).
`out/cohorts.csv` publishes both numbers and LIMITS.md says the cap remains loose.

### 4.4 The largest pound-denominated cost in the model sat outside the foreign-exchange exposure

**Found.** `fx_scale` reached consumer prices, the school seat price, school
onboarding, United Kingdom people and onshore support. It did not reach content,
which is wholly pound-quoted — examiner contract rates in pounds an hour,
authoring in pounds an item — and which is four times the size of the United
Kingdom people line. The sampled-rate scenario priced sterling risk without its
largest natural hedge.

**Also.** The comment above the rates claimed the scenario sampled both. It
samples one. `FX_INR_USD` is read by no line in `model.py` at all: Bengaluru
salaries and support are drawn directly in dollars, so the rupee exposure has no
term rather than a fixed one, while `out/constants.csv` publishes the constant
and the write-up described it as a rate the model uses.

**Fixed.** Content carries `fx_scale`. The comment says what is true, and
`FX_INR_USD` is labelled dead where it is defined rather than deleted, because
two documents describe it.

### 4.5 Smaller, in the model

`school_onboard_cost` omitted `overhead_mult`, which every other people cost
carries, making an onboarding person-week cheaper than the same person-week
anywhere else. Fixed.

### 4.6 Dead machinery, one piece of which would have been wrong if read

`acq_cum`, `cac_cum`, `contrib_cum` and `months_cum` were populated every month,
returned in the summary and read by nothing. `contrib_cum` accumulated the
whole-book blended contribution against each cohort, so any future cohort payback
computed from it would have credited an Indian pre-examination cohort the United
Kingdom examination-year average; and `months_cum` counted the acquisition month
while `active_hh` does not, so two household-month counts differing by about a
quarter sat in the same dict. Removed, as `units_target()` was in round 3, for
the same reason.

### 4.7 A per-path statistic that was not one, in the answer to the item about exactly that

**Found.** `cohorts.py` computed lifetime value as each path's own contribution
times the SAMPLE MEAN retained months, a scalar, and published the resulting
share as the per-path restatement checklist item 19 demands. Retention varies
strongly across paths and correlates with churn.

**Fixed.** Each path's own realised retention. Both shares are published, so the
size of the error is on the record rather than only here. Checklist item 19 is no
longer marked clean.

### 4.8 The cost-split table understated content, because some of it is filed under people

**Found.** The salaried content heads sit inside `people_beng_cost` and their
whole job is the content schedule. The cost table's content row counts only the
contracted authoring and validation, and section 12's argument about content
schedule versus market count runs off that table.

**Fixed.** `model.py` emits `people_beng_content_cost` as its own monthly series
— a decomposition of the people line, never added to any total — and section 5
gives content-driven cost beside the content line.

**Left, and opened as X12.** `units_per_content_head` charges a salaried head to
"build and maintain" content units while `writer_gbp_item` charges an authoring
cost for the same items. Either both are real or one is a double count. Nothing
in the model, the vault or this document distinguishes them, and it is not the
model's question to settle.

### 4.9 Three claims that were true of a mean and asserted of the plan

**docs/10's load-bearing row** was answered with inference over *total cost*, a
denominator dominated by the content build. Against the denominator the claim
needs — variable cost against price — the row holds on the median path and
reverses on a minority of them. Both are now published.

**"64.9 per cent of the cost base is committed before demand can say much about
it"** is not about timing: two thirds of that block is spent more than eighteen
months after the first customer. What makes it demand-independent is that the
model has no rule that stops building. The word "committed" is gone and the
timing split is published.

**Retained months are right-censored by the horizon.** Acquisitions are still
ramping at month 58, so a large share have their retention cut off by the window
rather than by churn. The level is a floor; the ratio between year groups, which
is what refutes docs/10, survives the correction and was checked deliberately.

### 4.10 Things the document asserted without a number, now with one

Monte Carlo error was never sized. It is now, in `out/cohorts.csv` as
`por_terminal_cash_mc_se`, and the write-up's preamble quotes it. At that size the
sampled-foreign-exchange scenario — tabulated to the dollar and discussed in three
places as "small" — is **indistinguishable from zero**.

Discounting is absent entirely and was in no limits section and no omissions
file. It is now sized at two rates. The direction sharpens this document's own
conclusion and shrinks the residual scenario, the largest item in the scenario
table.

Registry granularity: a count of "how many content drivers in the top seven" is
a fact about how finely the registry splits each cost. `out/sobol_grouped.csv`
computes indices on grouped scalars instead, and section 8 quotes those. The
conclusion survives the regrouping; nothing in the directory would have told us
if it had not.

### 4.11 Smaller, in the documents

Section 10 called the four break-evens landing on the two drivers section 8 ranks
first "the instrument agreeing with itself"; it is a tautology, since a bisection
can only bracket on a driver that moves the target and the index ranks by exactly
that. Section 13 said three identities run down every row of the monthly file;
two do. The net-cash identity omitted the terminal-value term and passed only
because the published run credits no residual. The scope-ladder separability
check added in round 3 cannot fail, because content sums over markets in an
independent loop — it is a regression test, not evidence, and section 12 now says
so and gives the two-per-cent gap on the columns that do not decompose. Four open
items named triggers that cannot produce their quantity at the precision claimed:
E5, E2, E4's second half and C1. `verify.py` carried a dead `tol` variable.
`provenance.csv` hashed `model.py` and not `harness.py`, leaving the file that
splits, executes and gates the model outside the staleness check.

### 4.12 What held up

Recorded because a round that only reports failures is not a review. The harness
gate and both its self-tests; the suffix discipline check; that no draw occurs
inside the month loop; that the funding section's staged-versus-headline gap is
buffer rather than quantile arithmetic; that the shared market budget pot does
not penalise the plan of record; that the pre-to-exam retained-month ratio
survives horizon censoring; that the Sobol ANOVA estimator is correctly
specified; and that the launch-delay deltas are not Monte Carlo noise.
