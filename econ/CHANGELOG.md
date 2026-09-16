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

**Superseded twice, and the second half of that sentence is wrong.** Round 2.5
softened "inverts" to "re-ranks"; round 3.4 found even that was never computed
and is false. On `out/sobol.csv`'s `onshore_all` run, item count stays at rank 1
on the capital requirement and the United Kingdom salary driver never enters the
top three on any target. The cash consequence stands; the ordering claim does
not. Left in place as the record of what this round believed, marked here so a
reader arriving at it is not told the opposite of the current finding.

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
content schedule is worth several times what dropping markets is on terminal
cash, while on capital the two are worth about the same. (This entry gave a
multiplier of five, from the round 3 run. It did not move when the scenarios
did, and nor did the one in section 12. Both are rendered tokens now; see 5.7.) `GTM_MINIMUM_SCHEDULES` moved
into `model.py` so `variants.py`, `funding.py`, `rescue_grid.py` and
`breakeven.py` cannot drift apart.

### 3.2 The sensitivity ordering was computed on one scope and quoted as the ordering

**Found.** Every Sobol index in section 8 is computed on the plan of record. The
document's central instruction — work on acquisition to make the business exist,
on content cost to make it fundable — was stated as a property of the business.

**Verified.** On the go-to-market minimum the capital ordering rearranges:
content drivers fall from five of the top seven to one, and `eng_usd_yr` moves
from rank eight to rank two. (That was the round 3 run. The ranks moved with the
model in rounds 4 and 5; section 1 of the write-up renders the current one from
`out/sobol.csv` rather than repeating this.)

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

### 4.3 The acquisition budget cap believed in a household about two and a half times longer-lived than the model delivers

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

### 4.12 And one the author got wrong while fixing 4.11

Writing the caveat about ranking by dollar spread, I put into the preamble that
scope and the price anchor "rank within a few per cent of each other" on terminal
cash. They do not: the anchor leads by about three to one there, and scope leads
by about five to one on capital. What is close in magnitude is the
CROSS-statistic pair section 12 puts side by side — a capital requirement against
a cash spread — and that closeness is meaningless, which was the reviewer's
actual point. Corrected in the preamble and in section 12. Recorded because a
correction introduced while acting on a review is exactly the kind that goes
unreviewed.

### 4.13 What the coherence pass found, and one of them reverses a conclusion

The coherence half of round four ran against a moving target — every output was
rewritten while it worked — and it re-verified each finding against the final
state. It confirmed that rendering the three sources against `out/figures.csv`
reproduces the three documents character for character, so no figure token had
drifted. Every error it found is in hand-typed prose, in a comment, or in a name
the file behind it does not support.

**The Year 10 conclusion was the reverse of the two numbers printed above it.**
Section 4 said in bold: "It is in-term churn, not the summer, that is eating the
Year 10 advantage", and open item X5 ranked in-term churn ahead of the summer on
the strength of it. Differencing the two counterfactuals against the base — which
no draft had done — removing the summer entirely lifts the ratio by about
fourteen times what flooring in-term churn does. LIMITS said the summer and was
right; the write-up and the open items said in-term churn and were wrong, and
sent the owner at the smaller question first, which is the exact failure mode
`OPEN_ITEMS.md` opens by warning about. The lifts are now computed in
`out/cohorts.csv`, the passage gives all four rows with their differences, X5 and
X5b are swapped, and the three documents agree. **The larger finding, which no
draft stated, is that neither lever recovers the two docs/10 reasons toward, and
nor do both together** — `cohorts.py` carried a derivation string calling the
combination "the only one that recovers" it, which it does not.

**Two errors this round introduced while fixing others.** LIMITS and this log
both claimed `out/cohorts.csv` published the assumed and realised retention
months behind 4.3; it published neither, and `cohorts.py` computed neither. They
are computed and published now. And section 13's identity count, corrected in
round four from "four down the whole monthly file" to "two", over-corrected:
three of the five run elementwise down every row. Three is right, the count has
now been wrong in both directions, and nothing in the repository can check it,
because the sentence describes what each identity *is*.

**Counts that the file moved and the prose did not.** LIMITS item 19 said two of
its rows are propositions the document refutes; four are. Item 8's zero-priced
breakdown accounted for six of seven and its "up from a twelfth" is an eighth on
the file's own arithmetic. Item 11 named six mechanisms under a count of seven.
The gate-coverage heading said twenty-two files against twenty-three. A
colon-introduced list of ten commitments named seven. All are now either rendered
from the file or written as "including".

**`out/drivers.csv` had a low/high header over a mean and a standard deviation.**
`price_drift_yr` is the registry's only normal driver and `params.py` wrote its
two parameters under `low` and `high`, so the file said drift is sampled between
1.5 and 3.0 per cent when it is N(0.015, 0.030), unbounded, with roughly a third
of paths drawing a negative drift. `figures.py` emitted `_low` and `_high` tokens
from those columns, so the wrong reading was one token away from the prose.
Nothing quoted it. The file now has `normal_mean` and `normal_sd` columns and
`figures.py` emits no bounds for a driver that has none.

**Three comments and two names that described something other than the code.**
`units_cost_weight()`'s docstring documented a four-value return beginning with a
quantity it does not compute. A comment in `variants.py` about the
contribution-per-household ratio sat orphaned above the allowance share and
promised a median over a mean. `verify.py`'s tolerance comment claimed six
decimal places over a one-dollar threshold. `commitments_decided_after_their_
round_closed` counted rows whose answer to that question is "no".
`funding.py`'s `closes_at` held a stage's opening month, which its own CSV header
calls `that_stage_opens_month`. A figure derivation omitted the app-store fee
that `path_outcomes()` subtracts, which agrees with the published run only
because that line is zero in it.

**And the write-up's file table sent readers to sixteen files while the argument
rests on twenty.** `rescue_grid.csv`, `sobol_grouped.csv`, `drivers.csv` and
`constants.csv` are all cited by name in the prose and were not in it.

Change log entry 1b.11 still asserted the onshoring conclusion that 2.5 and 3.4
retract. It is left in place as the record of what that round believed and is now
marked superseded where it stands.

### 4.14 What held up

Recorded because a round that only reports failures is not a review.

**Round sizing adds two percentiles and it is safe.** A staged round is the
eightieth percentile of the window's need plus six times the eightieth
percentile of its burn — the construction section 6 refuses for band lines. I
expected this to be a finding and it is not: need and burn correlate at 0.97 to
1.00 across the three windows, so the sum of the percentiles differs from the
percentile of the sum by about seven hundred dollars on a staged total of
thirty-seven million. LIMITS item 20 now states the check and the condition
under which it would stop holding.
 The harness
gate and both its self-tests; the suffix discipline check; that no draw occurs
inside the month loop; that the funding section's staged-versus-headline gap is
buffer rather than quantile arithmetic; that the shared market budget pot does
not penalise the plan of record; that the pre-to-exam retained-month ratio
survives horizon censoring; that the Sobol ANOVA estimator is correctly
specified; and that the launch-delay deltas are not Monte Carlo noise.

---

### 4.15 Following the drivers.csv header fix to its consequence

The header defect in 4.13 was reported as a presentation problem. Following it
into the model makes it a finding about the priors. `price_drift_yr` is the
registry's only normal driver, and it is unbounded: real prices **fall** on
about thirty per cent of paths, and the cumulative real price multiplier at
month 60 runs from about 0.84 at the fifth percentile to about 1.36 at the
ninety-fifth. Every revenue figure in the document compounds that, and no
section quoted the range, because the range does not exist — there are only a
mean and a standard deviation, and the file had been printing them as bounds.
Now in `out/cohorts.csv` and in LIMITS.

### 4.16 The trough section hid its own defect behind a mean

Found by re-reading section 7 while round five ran, not by a reviewer.

The section exists to make one point: the minimum of an average is shallower
than the average of minimums. It made that point about DEPTH correctly and then
made a timing claim out of a mean. It said the averaged line troughs at month 54
while individual paths trough on average at 53.6, and called the averaged line
"later" — four tenths of a month, which is nothing.

The mean was hiding the distribution. The median path troughs at month **59 of
60**, the tenth percentile at 30, and **79.1 per cent of paths have their trough
in the last month of the horizon**: cash is still falling when the window
closes. The trough has not happened yet on four paths in five.

**The consequence is on the number that sizes the rounds.** The peak funding
requirement is the negative of the trough, so every capital figure in section 11
is a floor on that same share of paths. Section 7 now gives the distribution,
section 11 says the table is censored, and LIMITS carries it as its own item.

It is the checklist item 19 defect — a conclusion true only of an averaged line —
committed inside the section whose entire subject is that defect.

### 4.17 The band-placement warning pointed at the wrong axis

Also found by re-reading rather than by a reviewer, and in the same shape as
4.16: a strong claim resting on a comparison nobody had measured.

Section 6 measured the central band line's percentile placement, found it moves,
and warned that **cross-scenario** comparison of band lines is invalid. The
evidence offered was two scenarios ending at 49.9 and 50.1 per cent. Measured
across all 23 scenarios in `out/variants_bands.csv`, the terminal placement
spans 0.38 percentile points. Within the single published run, across the months
from go-to-market, it wanders 7.6 points.

So the placement is **stable** across scenarios and **unstable** across the
horizon, and the warning had it exactly backwards. Comparing terminal band lines
between scenarios is fine; comparing a band line at one month against one at
another is not. Both spreads are now figures, the section says which comparison
is unsafe, and the rule that survives either way — a band line is not a
percentile line — is stated on its own.

Worth noting what this does NOT change: the construction, the suffix discipline
that keeps `_mean` and `_band` columns from colliding, and the measurement of the
placement itself were all correct. It was only the sentence drawing a conclusion
from them.

### 4.18 A currency tag on twelve quantities that are not money

Found by sweeping every figure token against its unit in `out/figures.csv`.

`usd0` and `num0` render identically — both are a comma-separated integer — so
twelve tokens tagging household counts, rota thresholds and pound-denominated
driver bounds as `usd0` produced exactly the right output. The prose around each
was correct. The defect is only visible to someone reading the source, where a
household count is labelled as dollars.

Retagged to `num0`, which leaves all three rendered documents byte-identical, and
`verify.py` gained a pass that fails the run on any currency tag over a
non-currency unit. `render.py`'s format table says which is which and why they
are kept apart.

**And the provenance file was recording things that generate nothing.** An
ad-hoc `python3 -` that loads the harness to check a number wrote a row into
`out/provenance.csv` under the script name `-`. It writes no output, so the row
stands for nothing. `harness.load()` now records only callers whose name ends in
`.py`.

## Round 5: two more mechanism defects, and a positive result the document reported as a failure

The protocol says repeat until a round returns nothing new. Round 5 returned a
great deal, including two live defects in the month loop — one of them the same
ordering error round 4 found, on the other of the two paths into the segment.

Every finding was checked against the code before being accepted.

### 5.1 The sitting-month exits deleted households acquired that same month

**Found.** Round 4 fixed the A-level sitting exit against the PROGRESSION path.
The same error was live on the ACQUISITION path, on both segments. Acquisitions
are added to `stock` before the calendar block runs, so a household acquired in
a sitting month was charged its effective acquisition cost and its age-assurance
check, billed for **nothing** — billing starts the month after — and deleted at
the end of the month it arrived in.

**Verified.** Tracking arrivals separately and exempting them from both
same-month exits, paired: terminal cash at the mean -7,867,103 against the
published -10,049,080.

**Moved.** About +2.2m on the mean, roughly twice what round 4's fix was worth
and larger than the creator-fee and app-store scenarios that have their own rows
in the scenario table. It passed the harness gate, the off/on test and every
accounting identity — the same three gates round 4's version passed while wrong.

**Left.** `seg_mix_exam` does not vary with the calendar, so the model still buys
examination-year households in the sitting month, merely at a price that now
buys something. What share of arrivals is examination-year in which month is
unmeasured, so it stays a prior rather than becoming a second invented schedule.

### 5.2 An institution cost in a consumer ratio, twice

**Found.** `inference_cost` carries the institution channel's seat consumption as
well as the consumer book's. `cohorts.py` divided it by `gross_rev_consumer`,
which excludes institution revenue entirely. The published claim — that variable
cost exceeds half of revenue on a minority of paths and exceeds revenue outright
on a few per cent — was an artefact of that. On the paths carrying the headline,
about four fifths of the "variable cost" was institution inference, against
institution revenue more than twice its size that the denominator did not see.

**Fixed.** `model.py` emits `school_inference_cost` as its own monthly series, a
decomposition of `inference_cost` and never a thirteenth cost line. The ratio is
consumer-only, and so is `final_year_contrib_per_hh_month`, which had both the
institution channel's revenue and its inference in a numerator whose denominator
is consumer household months.

**The corrected finding is stronger than the published one.** Constructed
consistently, docs/10's load-bearing row does not reverse on a minority of paths;
it does not reverse at all. Checklist item 19's table drops the row it had
conceded.

### 5.3 "Not bracketed" was read as failure regardless of which side it sits on

**Found.** Section 10 said the ten-million-dollar capital ceiling is failed on
both scopes by both drivers solved against it. On the go-to-market minimum the
ceiling is **met across the entire prior range of both**: at the top of the
acquisition anchor's log-uniform prior, four times its median, the narrow scope
still needs about 7.2m. Section 11's own table said the same thing from the
other end, and section 10 contradicted it for two rounds.

`bisect()` returns "not bracketed" when the metric does not cross the target
inside the prior range. That says nothing about which side of it the metric sits
on, and four of the twenty-four rows are unbracketed on the satisfying side.

**Fixed.** `breakeven.py` classifies every unbracketed row as met or missed
across the range, with the direction of "good" taken per metric. `figures.py`
counts both. Section 10 now reports the result it had been inverting: **the
narrow scope stays inside a ten-million-dollar ceiling wherever the acquisition
anchor and the reachable pool land inside their priors.** It is the most
actionable positive result in the file.

### 5.4 The lifetime-value estimate used a calendar the loop does not have

**Found.** Round 4 rewrote `ltv_estimate` to take the examination calendar from
the loop. Its pre-examination branch capped the household's life at the sitting
plus ten months; the loop moves that household on at the sitting plus **two**.
Those are different quantities and not congruent — for a household acquired in
the sitting month the true figure is two and the code used ten — and the
post-progression term counted the months to this year's sitting rather than to
the household's own.

**Fixed.** Both terms come from the loop's calendar now. `LIMITS.md` no longer
attributes the residual gap to two causes when there were three.

### 5.5 Dead code, again

A nested loop in the month loop whose entire body bound a view of `stock` and
discarded it — the remains of the accumulators round 4 removed. A constant in
`cohorts.py` referenced nowhere. Both removed on the rule rounds 3 and 4 set.

### 5.6 The staging test ran on the first half of the plan

**Found.** `funding.py`'s commitments list is hand-typed and every entry landed
at month 30 or earlier, in a sixty-month horizon. Six of the model's own content
steps were missing, so the count section 11 reasons from was 10 of 14 rather
than 10 of 20 — and one of the missing six, the United States seven-subject step,
violates the section's own test a second time: it lands in the Series B window
and starts its build inside the Series A.

**Fixed.** All six added. The instrument that measures "staging against
decisions" was itself a hand-typed list, which is the failure class round 4 spent
an entry converting away from.

### 5.7 Two multipliers taken from a superseded run

Section 12 said the real scope reduction is worth "six times" the one the
document used to read it off, and that freezing content is worth "five times"
what dropping markets is. Both were round 3 figures. The scenarios moved twice
since and the words did not; both are about half the true values. Both are
rendered tokens now, and so is the rank ordinal in section 1 that said a
Bengaluru salary driver "comes second" when the file and section 8's own table
both say third.

### 5.8 Claims with no artefact behind them

"The level rose by about a sixth" under an acquisition-off counterfactual that
existed only in a working note: `stop_acquisition_after` is a configuration key
now, with an off-test, and the lift is a figure. "Those steps fire on most
paths": true of the first safeguarding rota step, false of the second, which
fires on about one path in five. Both now rendered.

### 5.9 A paired conclusion argued from an unpaired error

The sampled foreign-exchange scenario is indistinguishable from zero — reached
by comparing its delta against the standard error of the base mean, which is
several times too large for a scenario that shares its random numbers path by
path. `out/variants.csv` carries a `paired_mc_se` column now and the preamble
quotes the t-statistic. The conclusion held; the number offered for it did not.

### 5.10 The grouped indices were not grouped on the same principle

The content scalar collects four of eight content entries, everything one timed
pilot and one objective count would settle. The acquisition scalar collected
three of twelve and left out saturation, although E2's own trigger measures
effective cost *at* a spend. A fourth grouped quantity does it symmetrically.
The conclusion survives and the margin narrows.

### 5.11 Two absent lines and one asymmetry, now written down

Agency margin or off-payroll on-cost on examiner time — the largest cost line
carries no overhead term at all, and X10's trigger assumes an agency. No organic
or referred acquisition of any kind: every household in the model is bought, so
there is no mechanism by which the book grows without spending, which is part of
why no single driver rescues the plan. And the reachable pool scales with subject
breadth while discarding levels and boards, so the go-to-market minimum and a
scope with twelve times the content are credited the same pool. The last is not
corrected, because mapping board coverage onto households needs a prior nothing
supplies — and because the pool is nearly inert, which is the more interesting
half of the finding.

### 5.12 Smaller, and again there were many

LIMITS asserted a sentence 250 lines above the passage that retracts it, and
quoted a superseded pair of retention figures while pointing at a file holding a
different pair. Item 19 said two of its rows are propositions the document
refutes; four are. Item 8 accounted for six of seven zero-priced lines. Item 11
named six mechanisms under a count of seven. A "where to look" table omitted the
two self-test records that are the evidence for section 3's central claim. The
staleness check is described as hashing `model.py` in four places and hashes
`model.py` and `harness.py`; the CSV column said `model_sha256` over a hash of
two files. `breakeven.py`'s header comment said no driver reaches any target when
four bracket. Five more comments and docstrings described something other than
the code below them. The change log asserted "2.6 times" over its own 8.351 and
3.309. Section 10's tautology argument was itself wrong: the price driver
brackets while ranking sixth on that target, and the real reason is the pinning,
which the write-up says two paragraphs later.

### 5.13 What held up

Recorded because a round that only reports failures is not a review.

Every figure in the scenario table, the scope ladder and the funding table
reconciles to the CSVs to the dollar. The cost split, the whole Sobol section
including both scope orderings and the onshoring ordering, the rescue grid, the
two-way grid, the Year 10 counterfactuals and their differencing, the trough
table and the new censoring figures, all fifteen discounting figures, the
penalty comparison, the examiner-hours and night-rota derivations. Both harness
gates and the source-level no-draw check. The suffix discipline and its
self-test. The two-sided off-test on every mechanism. The five identities and the
count of them. `enforce_allowance` truncating delivery and removing the overage
with it. The A-level exit firing on the standing stock. `fx_scale` reaching
content. `people_beng_content_cost` never entering a total. And the
percentile-addition in the round sizing, which I expected to be a finding and is
not: need and burn correlate at 0.97 to 1.00, so the sum of the percentiles is
the percentile of the sum to within seven hundred dollars on thirty-seven
million.

---

### 5.14 What the round 5 fixes moved, and one of them changed a headline

Plan-of-record terminal cash at the mean moved from -10,049,080 to
-7,880,764 across 5.1, 5.2 and 5.4 together, most of it the sitting-month
arrivals.

**And section 10's central claim changed.** Until these fixes, no value of any
single driver anywhere in its prior range got the median path whole on either
scope. A price on the go-to-market minimum now does, at about 42 pounds a
month with condition C1 passing, and at that price the run needs about 4.8m of
capital at the eightieth percentile and 71 per cent of paths reach
profitability. It is the only place in the document where one driver inside its
own prior produces a plan that returns the cash it consumes on the median path
and stays inside the capital ceiling at once. It is conditional on the narrow
scope, on the tutoring anchor and on a price near the top of its prior, and the
section says so.

**The name-collision guard added in round 1a earned its keep.** With a price
bracketing against two different targets on the same scope, two figures tried to
take the same name. The guard refused the run instead of silently overwriting,
which is what it was built for and the first time it has fired on anything real.
The hours-of-tutoring figures are keyed by metric now.

**And the currency-tag pass added earlier in round 5 caught two of its own.** The
support-end break-even figures carried a generic "metric units", so a dollar
figure and a share were indistinguishable to the check. The unit follows the
metric now.

## Round 5b: building the thing round 5 said was missing

Round 5's LIMITS entry said seven mechanism defects had passed every automated
check here while wrong, that all seven were found by reading the month loop, and
that what would close it had not been built. Leaving that as a note would have
been the easy option.

### 5.15 invariants.py

Seven structural checks on what the month loop must produce. Not accounting
identities — all seven historical defects left cash adding up perfectly — but
statements about whether a household is in the right place at the right time.

**Four are proved to bite.** The defect each was written for is reintroduced
into a copy of `model.py` in memory, the check is required to fail on it, and the
copy is discarded. `model.py` on disk is never written to. This is the harness
gate's own argument: a check that has never been shown to fail is not a check.
`out/invariant_selftest.txt` records the result.

**Writing it caught four things, three of them mine.**

*The suite found a real contamination.* `sessions_delivered` mixed consumer and
institution sessions, so any sessions-per-household figure built from it over
consumer households would have been exactly the defect 5.2 had just fixed
elsewhere. `school_sessions_delivered` is emitted separately now. Nothing in the
documents divided it that way yet, which is the point of finding it first.

*The suite found a flaw in round 5's own fix.* The arrivals exemption compared a
churned `stock` against un-churned `arrivals` and clamped the difference at zero.
The clamp hid the mismatch and made the exemption slightly too generous on paths
with a small standing book. Arrivals now take the same churn as the stock they
are part of, and the clamp is gone because it is no longer needed.

*Two of the seven checks did not catch their own defect when first written, and
the self-test is the only reason I know.* One used household months per
acquisition with a floor of one: the exits fire in one month a year, so an
aggregate over sixty months barely moves. It now reads a diagnostic the model
publishes for the purpose, written in terms of `arrivals` so that reintroducing
the defect cannot alter the diagnostic too. The other **reimplemented
`ltv_estimate`'s arithmetic inside the check**, so it was comparing the formula
against itself and passed cheerfully against a reintroduced defect. It calls the
model's function now and extracts the assumed months by differencing two runs at
different contributions, which cancels everything except the quantity wanted.

**What it does not do, stated in LIMITS rather than glossed.** Three of the seven
are containment or boundary checks no defect has yet violated, so they are
untested in the only way that counts. One is a regression tripwire rather than an
invariant — its threshold sits between the correct code's value and a known
defect's, because a principled ceiling would need the survival term the check
cannot see — and it is labelled `TRIPWIRE:` in the file and in the CSV. And the
whole suite was written after seven defects were known, so it is fitted to them.
A defect of an unfamiliar shape will pass it.

The second implementation of the month loop by an independent route, which would
catch all seven without being told about any of them, is still not built.

### 5.16 A result that flickered, and what that says about reporting it

The arrivals-churn correction above moved one break-even back across the line it
had just crossed. Within round 5, on the same priors and the same seed, the
go-to-market minimum's median-path cash target went: unreachable, then reachable
at about 42 pounds a month after 5.1 and 5.2, then unreachable again after 5.15.
The write-up asserted the middle state in bold before the third fix landed.

Nothing about the business changed. Three arithmetic corrections did, and the
result sits close enough to zero that each of them was decisive: at the top of
the price prior the median path now ends about 56 thousand dollars short over
five years, against about five million short at the bottom of the same prior.

Section 10 reports the **margin** rather than a verdict, and says the instrument
cannot tell which side of zero it lands on. That is the honest reading and it is
more useful than either of the two verdicts this round produced. It is also a
caution that generalises: a bracketed-or-not answer is a threshold on a
continuous quantity, and near the threshold it carries none of the precision the
word "break-even" implies.

### 5.17 A tolerance that reported correct numbers as wrong

`verify.py`'s prose scrape allowed half the place value of the last digit
printed. A figure landing exactly on the half — 11.45 to one decimal, 2.585 to
two — sits on the boundary, and binary floating point puts it a hair either side
unpredictably, so the scrape reported two figures as underivable for having
rounded the way the renderer rounded them. The tolerance carries a millionth of
the place value now, which is far too small to admit a genuinely different
number. Found by the check failing on correct prose, which is the only way this
class shows up.

### 5.18 What round 5b moved, recorded late

This section exists because round 6's coherence pass found it missing. Section
5.14 recorded the plan-of-record terminal cash mean moving to -7,880,764 across
the round 5 fixes. Sections 5.15 to 5.17 then changed the model again -- arrivals
took the same churn as the stock they are part of, and the clamp that had been
hiding the mismatch went -- and recorded nothing about what that did to the
headline. The published value after round 5b was **-8,049,733**.

A change log whose stated purpose is "what the numbers moved from and to" has to
say so in the round that moves them, not leave the last figure in it stale while
the file on disk says something else. `verify_allow.csv` made it worse by
exempting -7,880,764 with the reason "it is the current value", which had
stopped being true in the same round.

---

## Round 6

Two fresh-context reviews again, a coherence pass and an adversarial pass, each
given the artefacts and none of the reasoning behind them. The protocol says to
repeat until a round returns nothing new. This round returned three live
mechanism defects, one duplicated function carrying arithmetic a previous round
had removed, four wrong magnitudes in the prose, and a diagnostic that was
tautologically zero. It is not a converging round.

### 6.1 The summer lapse and the progression deleted households in the month they arrived

This is the same defect as 4.2 and 5.1, on the two calendar paths neither of
those rounds looked at.

`model.py` states the rule in a comment above the stock array: the
examination-calendar exits must not fire on this month's arrivals, because
billing starts the month after acquisition, so an arrival deleted in its arrival
month has paid its acquisition cost and its age-assurance check and been billed
for nothing. Round 5 made the two SITTING exits obey it. The summer lapse and
the year-group progression, twenty lines below and in the same block, kept
operating on the whole stock.

A pre-examination household acquired in the month after the sitting lost the
lapse before its first invoice. One acquired two months after lost the lapse and
was then either moved into the examination segment or deleted outright: about
44 per cent of it gone in the month it arrived.

**Moved.** Paired against the same random numbers: terminal cash mean
-8,049,733 to -7,525,932, **+523,800**, against a paired standard error of
20,312 — 25.8 sigma. Terminal active households +870.6. Acquisitions +3,139.
Peak funding mean -66,770.

**And the check that was supposed to catch it read zero in all sixty months.**
`arrivals_removed_same_month` compared what the two sitting exits removed
against what they ought to have removed, and those two expressions are
algebraically identical given the line above them. The column could only ever
become non-zero if someone edited that one line. `invariants.py` read it under
the name "every acquisition can be billed" and asserted in its docstring that
"every acquisition must be able to produce billed household months" — a general
property, checked by a quantity fitted to one line, while two of the four exits
violated it. The self-test proved the check bites, against the defect it was
written for, which is the whole of what it proved.

The diagnostic is now written against the arrivals array rather than against any
one exit: after the calendar block, every household acquired this month must
still be standing in the segment it was acquired into. The self-test now
reintroduces the summer-lapse defect and the progression defect separately and
confirms the check refuses both, which the old form could not have done.

### 6.2 The three segment shares did not sum to one

`seg_mix_exam` is U(0.40, 0.85) and `seg_mix_alevel` is U(0.03, 0.25), drawn
independently. Their sum exceeds one on **5.125 per cent of paths** and reaches
1.0967. The code floored the pre-examination share at zero with an `np.maximum`
and rescaled nothing, so on those paths the loop put more households into stock
than acquisitions bought. They were billed, they consumed inference, and no
acquisition cost and no age-assurance check was paid for any of them.

The clamp did not prevent this. It concealed it, which is the failure mode this
document's own checklist item names.

**Moved.** Renormalising in the loop and in the budget cap together: terminal
cash mean **-64,839** across all paths (paired SE 11,051, 5.9 sigma), and
**-1,265,157** on the 1,025 paths affected. Terminal households -92 overall,
-1,805 on the affected paths.

Not disclosed anywhere before this round. It is now an invariant with its own
reintroduction.

### 6.3 The budget cap believed an examination household acquired in its sitting month was worth nothing

`ltv_estimate` capped an examination-year household's life at
`(EXAM_CAL_MONTH[m] - cal_month(t)) % 12`. In the sitting month itself that is
zero. But the loop exempts that month's arrivals from that month's sitting exit,
so such a household survives to the next sitting and is billed twelve times. The
closed form and the loop disagreed by the whole of an examination household's
life, in one month of every twelve, and `budget_cap_from_ltv` inverts the
saturation curve, so the permitted spend collapsed by roughly the square of the
error.

`to_progress` carried the same modulus and was consistent with the loop only
because of 6.1. Fixing 6.1 without this would have reopened the disagreement on
the pre-examination branch.

**Moved.** +300,708 of terminal cash, paired SE 23,322, 12.9 sigma. Terminal
households +1,846. Acquisitions +10,773.

### 6.4 The demand shock was not stationary at month zero

`shock_state` starts at exactly zero but the half-variance subtracted from it
was the STATIONARY variance, so the supposedly mean-one multiplier had mean
below one during burn-in: 0.969 at month zero, 0.995 at the United Kingdom
go-to-market month, reaching one around month nine. The launch ran into a demand
headwind that was an artefact of the initial condition. The correction is the
time-varying variance, which converges to the stationary one.

### 6.5 cohorts.py re-implemented ltv_estimate, and the copy carried the arithmetic 5.4 removed

The "what the acquisition budget cap believes" figure — the one the write-up and
LIMITS use to say the cap assumes more retention than the model delivers — was
computed by a duplicate of `ltv_estimate` living in `cohorts.py`. The duplicate
capped the pre-examination leg at the sitting plus ten and reused `m_exam` for
the post-progression leg. Both are exactly the forms CHANGELOG 5.4 says were
removed from the real function; `invariants.py` uses one of them as its
REINTRODUCED DEFECT in the self-test.

**Moved.** `ltv_cap_assumed_months` published 5.866317; what `ltv_estimate`
actually assumes is 5.227200. The published figure was 12.2 per cent high, and
so was the overstatement ratio built on it. LIMITS.md narrated the round-5 fix
in detail and then quoted the unfixed number.

The months are now factored out of `ltv_estimate` into `ltv_billed_months` and
`cohorts.py` calls it. There is one implementation.

### 6.6 The pooled contribution included the institution channel; the median beside it did not

CHANGELOG 5.2 stripped institution revenue and school inference out of
`path_outcomes`' per-path contribution. It left the pooled twin in `cohorts.py`
untouched, carrying institution revenue in the numerator and the whole inference
line as its cost, over a denominator of consumer household months only. The
write-up prints the two in a single table row.

**Moved.** Gross contribution per household month, pooled: 31.904323 published
against 31.560924 on the consumer-only basis the median column uses.

### 6.7 Two code comments said four where the file says two

`breakeven.py` said in two places that four rows are unbracketed on the
satisfying side. There are two. The write-up said two and was right; a reader
sent to the code found the wrong count waiting for them.

### 6.8 A column whose "yes" meant "fine" under a name that read like a flag

`out/funding_commitments.csv` carried `decision_taken_after_its_round_closed`,
which answered "no" on the two rows that violate the staging test and "yes" on
the eighteen that do not. A reader filtering the file for the problem got its
complement. It is now `spend_starts_before_its_stage_opens` and answers yes when
the test fails.

### 6.9 A paired error on two scenarios where the pairing is destroyed by construction

`apply_dependence` reorders the driver columns by Iman-Conover, so path i in
`por_dependence` carries different driver values from path i in the base. The
file says so itself: `pathwise_spearman_vs_base` is 0.2998 and 0.2985 for the
two dependence scenarios against 0.77 to 1.00 for every other. A paired standard
error was published for them anyway, and the preamble told the reader to use the
paired error for every scenario. `variants.csv` now carries a `pairing_holds`
column.

The same table's "Delta, median path" column was the difference of two marginal
medians — p50(scenario) less p50(base) — taken over what is in general a
different path in each term, presented as the path-level check on a heavy-tailed
mean. It cannot do that job. The genuine per-path median difference is now
published beside it with a paired bootstrap error, because the column it
replaces carried no error at all while sign conclusions were drawn from it.

### 6.10 Section 13 said constants.csv holds every decided constant

It holds every decided constant that is a SCALAR. The seasonality shapes, the
examination-month and season-shift maps, the market opening months, the four
content schedules, the market budget weights, the segment usage relatives, the
sales and creator ramps, the platform headcount floor and the general and
administrative schedule are all decisions and none is in the file. LIMITS.md has
listed them correctly for three rounds while section 13 claimed otherwise.

### 6.11 The provenance file was writable by anyone who ran a script

`_record_provenance()` recorded any caller whose name ended in `.py`. Both
round-6 reviewers wrote throwaway scripts to check the arithmetic, ran them
against the harness, and silently added `t2.py`, `t3.py`, `t5.py`, `t7.py`,
`t11.py` and `t14.py` to the file whose job is to record which generating
scripts produced the published set. A reader should not be able to write to it
by reading. There is an allowlist now.

### 6.12 The two-way grid was cited for a claim it refutes

Section 8 said the variance the first-order indices do not explain is
"concentrated in exactly the two drivers that matter most", and offered the
two-way grid in support. The grid shows the surface is exactly additive on
terminal cash: the acquisition step costs the same at every one of the five
content levels, to the cent, and the content step the same at every one of the
five acquisition levels. The two largest drivers do not interact at all on that
target. Nothing in this directory computes a second-order index, so the missing
variance is not attributed anywhere and never was.

Where the grid does show interaction is on whether a path reaches profitability,
and the section now reports that instead.

### 6.13 Four magnitudes stated by hand, four of them wrong

"About three to one" over 4.04. "Twenty times smaller" over 17.40. "About half a
per cent" over 1.10 per cent. "About twelve times the content" over 3.74 on the
model's own full-equivalent measure, and never above 5.00 anywhere in the
`board_reuse` prior.

Three of the four had survived five rounds of review, because a hand-typed
multiple reads as prose rather than as a figure and the prose scrape is weakest
on small numbers. All four are rendered tokens now, derived from the two figures
each one compares, so the multiple cannot drift from its operands.

### 6.14 Smaller, and again there were many

A section-5 headline saying the docs/10 assumption fails "on about one path in
sixteen" — 6.25 per cent — four lines above its own rendered figure of 1.4 per
cent. A colon-introduced list of eight off-tested mechanisms naming seven, with
the missing one being the acquisition-stop switch section 4 then relies on. A
LIMITS item saying eight omissions are zero "for three different reasons" and
then accounting for seven of them, with the eighth having a fourth reason of its
own. A LIMITS paragraph announcing a second staging violation and naming only
the first. A section-10 sentence asserting that all four break-even solves are
on section 8's top two drivers, refuted three lines below by the paragraph
correcting the previous draft of the same sentence. `invariants.py` and its
three output files missing from every enumeration in the write-up and the README
that claims to be complete. Two `verify_allow.csv` exemption reasons that had
the live and superseded values the wrong way round. Changelog subsections out of
order in two places.


### 6.15 What round 6 moved

Plan-of-record terminal cash at the mean, across 6.1, 6.2, 6.3 and 6.4 together:
**-8,049,733 to -7,278,633**, a move of **+771,100**. Terminal active households
28,471 to 31,102, +9.2 per cent. Every component is a paired measurement against
the same random numbers, and `out/invariant_defect_costs.csv` now records what
each defect is worth on its own by putting it back and re-running:

| Defect | Change log | What fixing it is worth, terminal cash mean |
|---|---|---|
| Sitting-month exits on the month's arrivals | 4.2 and 5.1 | +2,141,420 |
| Summer lapse on the month's arrivals | 6.1 | +362,070 |
| Year-group progression on the month's arrivals | 6.1 | +163,849 |
| Both round 6.1 exits together | 6.1 | +524,796 |
| Segment mix not summing to one | 6.2 | **-66,202** |
| Budget cap's calendar | 4.3 and 5.4 | +248,646 |
| School inference outside the inference line | 5.2 | **0** |
| Content heads outside the people line | 4.8 | **0** |

Two things in that table are worth saying out loud.

The segment-mix fix is **negative**. The defect flattered the model: it billed
households that had never been bought, so correcting it costs money. A reader
who assumes every correction found by review moves the answer in the
conservative direction has the sign wrong on this one.

Two rows are **exactly zero** — identical to six decimal places, not merely
small. Those defects moved a decomposition series rather than a total, so no
accounting identity in `verify.py` could ever have detected them on any run.
That was asserted in LIMITS.md for three rounds. It is now measured.

The two round 6.1 rows do not sum to the combined row, because the progression
acts on whatever the summer lapse left.
