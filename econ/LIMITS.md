# Limits: the checklist, item by item

**Seed 20260916, run date 2026-09-16.** Every item from part 4 of the brief, answered
explicitly, including where the answer is clean. Items that are not clean carry
the number they would move and by how much.

Three verdicts are used. **Clean** means the defect is not present. **Clean now**
means it was present, was found, and was fixed; the fix is in `CHANGELOG.md` with
what it moved. **Not clean** means it is still there, and the entry says what it
costs.

---

## Revenue

### 1. Consumption tax: **clean**

There is a tax term on the revenue side in every market. United Kingdom VAT at 20
per cent and Indian GST at 18 per cent are statutory constants; the United States
effective rate is a sampled driver between 0 and 8.5 per cent,
because state treatment of software subscriptions varies; the
rest-of-English-speaking bucket carries a blended 13 per cent, which is a stated
prior, not a rate.

**Quoted prices are read as gross, that is, tax-inclusive.** Net revenue is the
gross price divided by one plus the rate. Over the horizon that removes
4,338,652 dollars, or 11.2 per cent of gross consumer
revenue. On the United Kingdom alone at 20 per cent it removes a sixth.

**The other reading, quantified.** If the quoted prices were net and tax were added
on top, revenue over the horizon would be higher by that whole line,
4,338,652 dollars, which is 11.2 per cent more revenue and would
reduce the mean peak funding requirement by approximately the same amount.

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

### 3. Allowance and overage: **clean, and measured**

Not "neither". The allowance is **sold but not enforced**: sessions above it are
delivered and cost money. Overage **is billed**, up to 2.5 times the
allowance. Above that cap, cost runs and revenue does not, so the omission sits on
one side only and its sign is known.

23.6 per cent of active households exceed the allowance being sold to
them, household-month weighted. Enforcing it instead is worth
98,661 dollars of terminal cash.

### 4. Foreign exchange: **not clean, by instruction**

Rates are **fixed**: 1.27 dollars to the pound and 86.5 rupees to the dollar,
at the owner's explicit instruction. That is a decision, not a draw, and it means
this item cannot be clean.

**What it would move.** The `por_fx_sampled` scenario replaces the sterling rate
with a sampled one, drawn outside the published stream so the paths stay matched.
Terminal cash moves by 93,070 dollars on the mean, which is small,
and the peak funding requirement at the eightieth percentile moves from
32,611,126 to 32,624,546. **The exposure is in the width, not the
centre**, which is exactly what fixing a rate hides: fixed rates do not remove the
risk, they remove the evidence of it. The rupee exposure is not sampled at all in
that scenario, so even this understates.

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
steps at 3,000 active households and again at 25,000 where an
out-of-hours rota is about three and a half further posts; the general and administrative schedule; and
the field sales ramp.

Modelled as a slope where it should be lumpy: **content headcount**, which is
computed continuously as work in the coming year divided by what one head
sustains. Real hiring is lumpy and lags. This understates the cost of a fast ramp.

**Missing entirely: a night rota.** United Kingdom study time is roughly 16:00 to
21:00, which is 21:30 to 02:30 in Bengaluru. The product's busiest hours are the
build base's night, and there is no shift premium anywhere in the cost base.
Priced in `out/omissions.csv` at 449,379 to
898,759 dollars over the horizon, which is up to
1.96 per cent of the modelled cost base.

### 6. A cost that scales per market, per shift or per institution: **clean, except the shift**

Per institution: `school_onboard_cost`, priced at three quarters of a United
Kingdom person-week per school for the data processing agreement, the security
review and onboarding. Per market: entity annual compliance and counsel, charged
only where a market is actually opened. Per shift: missing, as item 5 says.

### 7. Does a second market cost more per unit: **clean, and it is not almost nothing**

A second United Kingdom board reuses between 50 and 92 per cent of the
items for the same subject and level, sampled; the remainder is built. A foreign
curriculum reuses only 10 to 60 per cent. Neither is near one, so the expansion case is not
being granted for free the thing it is asking to buy.

That this matters is visible in the sweep: pinning `board_reuse` from its fifth to
its ninety-fifth percentile swings terminal cash by 9,692,829 dollars,
and `market_reuse` is the ninth-ranked driver on the capital target.

### 8. A cost with no term at all: **not clean, nine named and priced**

Grepped for. `out/omissions.csv` names each absent line and prices it from a
figure the model already carries: refunds, chargebacks and failed payments;
insurance; recruitment fees; the night rota; penetration testing and vulnerability
disclosure; intercompany markup and Indian tax on it; accessibility conformance;
corporation tax; and translation.

The last two are priced at zero and written down anyway, because a zero recorded
is not the same as a line left out: corporation tax because no scenario here
returns a taxable trading profit, translation because the expansion is across
English-speaking curricula by decision.

**In total the absent lines are 1,417,558 to
3,252,942 dollars, or 7.09 per cent of the modelled
cost base at the top of the range.** They deepen the hole; they do not change the
ordering in section 8 of the write-up.

**One more, and it is the important one: the creator licence.** D4 makes named
educators the wedge and D14 requires named presets from day one, and the published
run charges nothing for them, because D5 describes a one-page name-and-likeness
agreement and the vault has never established what a creator charges to sign it.
Rather than invent the figure, the `por_creator_fees` scenario prices both limbs,
a fixed annual minimum per creator and a share of the revenue their audience
brought: -2,204,366 dollars of terminal cash. **The published run
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

### 10. Like-for-like comparators: **clean**

Every scenario in `out/variants.csv` shares one drawn driver dictionary and
differs only in named switches. A scenario that carries a market or a channel is
charged its entities, its counsel, its content build and its people.

One comparison in the write-up is **not** like for like and is labelled as such:
the institution channel is charged its costs and credited its revenue, but not
credited the outcome evidence that docs/09 says is the only durable moat. The
instrument cannot value evidence. That is a limit of the instrument.

### 11. The same random numbers: **clean, and tested**

No draw happens inside the month loop, so scenario branches cannot make the
streams diverge. Every variant reuses the base driver dictionary, and every new
parameter is drawn from a separate auxiliary seed.

Tested rather than asserted: `test_off_reproduces_base()` runs the feedback
machinery, the app-store fee, the exchange-rate override and the creator licence
each switched off, and requires the rebuilt monthly CSV text to equal the base
character for character. All four pass on every run of `variants.py`.

Matching is also measured, not just argued. `out/variants.csv` carries for every
scenario the rank correlation of per-path terminal cash against the base and the
mean absolute per-path change beside the change in the mean. Unmatched paths
would collapse the first and inflate the second. Across every scenario the
correlation runs from 0.7948 at the loosest to
0.9999 at the tightest.

---

## Acquisition and growth

### 12. Anchor or effective cost: **clean**

Both published. The anchor is a driver with median 32.26 dollars. The
effective cost at the spend actually modelled is 54.02 in the final
year, pooled across paths, which is 1.67 times the anchor. On the median
path it is 31.93, because the median path never spends enough to
saturate anything. It is published month by month as `cac_effective_blended_mean`
in `out/por_monthly.csv`, with the non-creator channel beside it.

### 13. Break-even struck on the anchor rather than the effective cost: **clean**

The break-even solves pin the anchor, because that is the input, but the target is
evaluated through the saturation and pool-pressure mechanism, so the answer is the
anchor value that produces the outcome at the effective cost. `pinned_sweeps.csv`
carries `final_year_effective_cac_mean` at every pin, so the effective cost at each
pinned anchor is on disk.

### 14. An acquisition budget with no cap: **clean now**

Capped at 0.75 times the company's own lifetime value estimate, by inverting the
saturation curve for the spend at which effective cost reaches the cap.

It was not clean in another way: the launch acquisition subsidy ran unconditionally
for all sixty months. It now holds for 12 months after go-to-market and tapers
to nothing over the next 12. See `CHANGELOG.md` 0.4.

**Does lifetime value exceed cost per acquisition in the final year?** On the mean,
pooled, yes: 108.11 against 54.02, a ratio of
2.00. **On 4.5 per cent of individual paths, no.** And the
lifetime value in that ratio is the **gross** one; against the all-in contribution
the ratio is far worse, and on the median path it is negative, which is item 16.

### 15. A ratio between markets asserted as measured: **clean, and the code disagrees with the prose**

docs/10 states that a Year 10 household can afford roughly twice the acquisition
cost of a Year 11 household. The model asserts no such ratio; it produces one from
a sampled summer lapse probability and a sampled progression rate.

**The number the code actually uses is 1.24, not two**
(3.66 months against 2.96, measured by pinning the
segment mix and re-running on the same random numbers). It reaches two or better
on 0.0 per cent of paths. docs/10's shape survives; its magnitude
does not, and docs/10's own caveat about the summer is why.

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

32.89 dollars per household month pooled, and
27.33 on the median path, is a **gross**
contribution: net revenue less inference, support, payment, hosting and store fees.

The all-in figure, net of engineering, content, overhead, compliance and payment
fees, is 19.85 dollars per household month pooled and
-109.95 on the median path. Pooled, the two differ by
-13.04.

**The pooled and median all-in figures disagree in sign**, because the pooled one
is dominated by the few paths with large books that spread the fixed costs, and
the median path is small with the same fixed costs on top of it. Both are in
`out/cohorts.csv` and both are in the write-up, so neither can stand in for the
other and neither can stand in for the gross figure.

---

## Statistics

### 17. Series on the same basis: **clean, and enforced in code**

Column suffixes are disjoint by construction: `_mean` is a mean over all paths,
`_p10`, `_p50`, `_p90` are percentiles of the per-path distribution at that month,
and `_bandlow`, `_bandcentral`, `_bandhigh` are within-band averages of whole
paths. `check_suffix_discipline()` in `model.py` raises on a header in which a
mean suffix and a band suffix could collide, and it runs on every write.

No figure in the write-up divides a `_mean` by a `_band`.

### 18. Sustained bad runs: **clean**

The demand shock is AR(1), not independent. Persistence is sampled between
0.45 and 0.95, median 0.70. The longest run of consecutive months with demand at
or below 0.80 averages 5.8 months and is 13.0 at the
ninetieth percentile; 36.9 per cent of paths contain a run of six or
more and 12.1 per cent a run of twelve or more.

**What is still missing.** The shock acts on acquisition only. There is no
correlated shock to retention, to vendor prices, or to the examiner labour market,
and no regime in which several go wrong together for the same reason. A recession
would do all of those at once and this model cannot represent it.

### 19. Conclusions true only of an averaged line: **clean, each restated per path**

Every averaged claim in the write-up is given its per-path share:

| Averaged claim | Share of paths on which it holds |
|---|---|
| Content exceeds acquisition spend | 85.4 per cent |
| Content is the single largest line | 65.6 per cent |
| The Year 10 cohort retains at least twice the months | 0.0 per cent |
| Lifetime value is below acquisition cost in the final year | 4.5 per cent |
| Peak funding exceeds ten million dollars | 87.7 per cent |
| Terminal cumulative cash is positive | 9.7 per cent |

---

## Funding

### 20. Sized on the base case or the plan of record: **clean**

Sized on the **plan of record**, at 32,611,126 dollars across the
horizon at the eightieth percentile. The base case is stated beside it at
17,691,569, along with two narrower scopes. They differ enough
that sizing on the base case would underfund the plan actually described.

### 21. Staging against decisions: **not clean**

Every commitment through month 18 has its spend starting inside the seed window,
including both foreign entities, foreign counsel, the security certification,
A-level content and the second and third United Kingdom boards. Two commitments
land after the Series A opens with their spend starting before it: all four boards
live at month 18, built from month 12, and the rest-of-English-speaking market at
month 24, built from month 18.

**The Series A does not buy those decisions. It refinances them.** `out/funding_commitments.csv`
holds the landing month and the spend-start month for each.

**What it would move.** Nothing in the cash flow; the spend happens either way.
What it moves is the round sizing: the seed for the plan of record is
12,935,477 dollars, and a round of that size described as a seed will
be raised on seed terms against a Series A-sized commitment.

---

## The measuring instrument

### 22. Does the instrument produce the quantities claimed: **not clean, and this is the worst of them**

Decompose revenue per household: it is the plan price, plus the overage, and the
overage is a function of **sessions per household per month**. Decompose the cost
side: variable cost is sessions per household times cost per session.

Sessions per household therefore appears on both sides of the unit economics and
in the pricing decision, since the allowance cannot be set without it.

**No instrument in docs/11 produces it before M5.** M1 is counsel, board policies,
three age-assurance quotes, a landing page and thirty school conversations. M2
produces cost per session from a frozen battery, which gives cost per session but
not sessions per household. M4 instruments return rate and sessions per learner
per fourteen days, which is the first thing that touches it, and M4 requires a
signed creator and a built product.

**Volume per customer is the factor nothing measures**, exactly as the brief
predicts. `sessions_mean` is sampled between 3.5 and 18 a month, a fivefold range,
and the top of that range is what docs/03's own usage arithmetic implies for a
revising Year 11.

**What it would move.** `out/breakeven.csv` records the solve. What can be said now
is that the allowance of sixteen sessions, which is a commercial decision already
taken in `model.py`, sits inside that range, so whether 23.6 per cent
of households exceed it or almost none do is not determined by anything measured.

### 23. Do the instrument's strata match the mix the cost base assumes: **not clean**

docs/03's validation pilot is two examiners validating the same twenty items. The
cost base applies `minutes_per_item` across 5 to 11 subjects, two levels and up to
four boards, and `minutes_per_item` is the fourth-ranked driver on the capital
target.

Twenty items of one kind, in one strand, of one subject, at one tier, is not a
sample of that population. The same defect as ten of each of five tiers not being
a 45/50/5 population. A pilot that measured a stratified sample across subject,
item kind and difficulty would cost very little more and would actually support
the extrapolation the cost base makes.

Second instance: the segment mix. The cost base assumes an examination-year share
sampled between 0.40 and 0.85, and nothing in docs/11 measures the mix
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
channel is that outcome evidence is the only durable moat and that every comparator
that carries weight in education is school-based. This model charges Route B its
costs, credits it its revenue, and gives it nothing for evidence. The
5,435,967 dollar figure is therefore a lower bound on Route B's
worth, not an estimate of it.

**It has no competitive response.** Free general tools sit in front of the same
parent and Google has committed capital at national scale. Nothing here represents
a competitor changing price, changing scope, or entering the United Kingdom
curriculum specifically.

**The company never adapts.** There is no rule that cuts spend when the plan is
failing, beyond the lifetime-value cap on acquisition. The peak funding
requirement is therefore the requirement of the plan as stated, not of a company
that notices and reacts. A real team would cut, and the honest reading of
32,611,126 dollars is "this is what it costs to execute the plan of
record without flinching", which is not the same as what it would actually cost.

**The institution channel is one blended channel.** Route B is modelled as a single
sterling-priced motion with a decided representative ramp, not per market. Its
cost is charged where it falls, but the geography of it is not represented.

**Retention has no tenure structure beyond the first month.** After month one, the
hazard is constant until the examination calendar acts. Real subscription hazards
fall with tenure, which makes this pessimistic on the long tail and optimistic on
nothing in particular.

**A-level is one pooled segment**, not two years, with an exit rate sampled between
0.35 and 0.72 standing in for the cohort structure.
