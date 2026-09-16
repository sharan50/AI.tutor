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
