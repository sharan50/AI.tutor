# Limits: the checklist, item by item

**Seed 20260916, run date 2026-09-16.** Every item of the twenty-four-point review
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

There is a tax term on the revenue side in every market. United Kingdom VAT at 20
per cent and Indian GST at 18 per cent are statutory constants; the United States
effective rate is a sampled driver between 0 and 8.5 per cent,
because state treatment of software subscriptions varies; the
rest-of-English-speaking bucket carries a blended 13 per cent, which is a stated
prior, not a rate.

**Quoted prices are read as gross, that is, tax-inclusive.** Net revenue is the
gross price divided by one plus the rate. Over the horizon that removes
3,771,134 dollars, or 10.8 per cent of gross consumer
revenue. On the United Kingdom alone at 20 per cent it removes a sixth.

**The other reading, quantified.** If the quoted prices were net and tax were added
on top, revenue over the horizon would be higher by that whole line,
3,771,134 dollars. That is 10.8 per cent of GROSS, and because it
would be added to net rather than removed from gross it is 12.2 per cent MORE
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
delivered and cost money. Overage **is billed**, up to 2.5 times the
allowance. Above that cap, cost runs and revenue does not, so the omission sits on
one side only and its sign is known.

**The scenario that priced enforcement was measuring the wrong threshold until
round 2.** It truncated delivery at the billing cap, 2.5 times the
allowance, rather than at the allowance itself, so it cut off a level almost no
household reaches and left the overage revenue in place. It now enforces the
allowance and removes the overage line with it, which is what the decision
actually is. See `CHANGELOG.md` 2.3.

23.6 per cent of active households exceed the allowance being sold to
them. That is a household-month weighted share within each path and then a plain
mean across paths, so a path with a hundred households and a path with one count
equally in it.

**Enforcing the allowance destroys 5,054,773 dollars of terminal cash**,
because the overage revenue lost is larger than the inference cost saved. Before
round 2 this scenario reported a small gain, from truncating delivery at the
billing cap rather than at the allowance.

### 4. Foreign exchange: **not clean, by instruction**

Rates are **fixed**: 1.27 dollars to the pound and 86.5 rupees to the dollar,
at the owner's explicit instruction. That is a decision, not a draw, and it means
this item cannot be clean.

**What it would move, and the honest answer is "nothing measurable, and that is
partly the scenario's fault".** The `por_fx_sampled` scenario replaces the
sterling rate with a sampled one, drawn outside the published stream so the paths
stay matched. Terminal cash moves by
34,458 dollars on the mean. **That is
not "small", it is zero**: the delta is 0.33
paired standard errors from zero, so at another seed it would carry a different
sign. (A round-four draft reached the same conclusion by comparing against the
*unpaired* standard error of the base mean, which is several times too large for
a paired comparison — the right conclusion from the wrong number, one paragraph
after this document explains the paired-versus-unpaired distinction for the
demand shock.) The peak funding requirement at the eightieth percentile
moves from 28,073,340 to
28,120,313. **The exposure is in the
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
898,759 dollars from the United Kingdom go-to-market month to
the end of the horizon, four and a half years rather than five, which is up to
2.30 per cent of the modelled cost base.

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
its ninety-fifth percentile swings terminal cash by 8,824,276 dollars,
and `market_reuse` is ranked 10 on the capital target.

### 8. A cost with no term at all: **not clean, 19 named and priced**

Grepped for. `out/omissions.csv` names each absent line and prices it from a
figure the model already carries. The list is rendered from the file rather than
typed, because a hand-kept copy of it drifted from the file twice:
refunds, chargebacks and failed payments; insurance: professional indemnity, cyber and directors; recruitment fees; out-of-hours operations rota; penetration testing and vulnerability disclosure; intercompany markup and Indian tax on it; age assurance on non-converting checks; consumer subscription regime: renewal reminders, cooling off, easy exit; trial-to-paid conversion and involuntary churn; institution channel variable cost other than inference; institution contract revenue lost to annual recognition; agency margin or off-payroll on-cost on examiner time; organic and referred acquisition; accessibility conformance and audit; corporation tax on trading profit; translation and localisation; regulatory enforcement exposure; examiner supply, as a quantity rather than a price; specification change and curriculum reform.

8 of them are priced at zero and written down
anyway, because a zero recorded is not the same as a line left out:
consumer subscription regime: renewal reminders, cooling off, easy exit; trial-to-paid conversion and involuntary churn; institution contract revenue lost to annual recognition; organic and referred acquisition; corporation tax on trading profit; translation and localisation; regulatory enforcement exposure; examiner supply, as a quantity rather than a price.

They are zero for three different reasons and the breakdown used to name only
two of them. **Four are genuine zeros**: no scenario here returns a taxable
trading profit, the expansion is across English-speaking curricula by decision,
nothing here puts a probability on enforcement, and examiner supply is a quantity
question rather than a cost. **One is not a cost at all** — institution revenue
lost to annual recognition is a timing artefact that makes the channel look worse
than the plan describes, and it is in the list because a zero recorded is better
than a line left out. **The remaining two** are zero only as *cost* lines,
because they are retention mechanics rather than costs, and their size is
published separately in `out/sized_omissions.csv`:
scaling both churn drivers by 25 per cent costs
4,788,955 dollars of terminal cash, which is
12.3 per cent of the modelled cost base.
That scale is a prior on how much of the book a reminder-and-easy-exit regime
and involuntary churn move between them, not a measurement of either.

**In total the absent lines are 3,914,123 to
9,458,539 dollars, or 24.22 per cent of the modelled
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
brought: -2,096,227 dollars of terminal cash. **The published run
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
not. All 8 pass both ways on every run of
`variants.py`. The list is rendered from `out/offtest.csv` rather than typed,
because a hand-kept copy of it named six against a count of seven:
feedback; appstore_zero; fx_fixed; creator_zero; onshore_zero; residual_zero; pool_reacq_published; stop_acquisition_never.

Matching is also measured, not just argued. `out/variants.csv` carries for every
scenario the rank correlation of per-path terminal cash against the base and the
mean absolute per-path change beside the change in the mean. Unmatched paths
would collapse the first and inflate the second.

**This is where an earlier draft was wrong, in the passage whose whole point was
that matching is measured.** It named two scenarios as the loosest and the
tightest and neither bound was the bound in the file. Across the scenarios that
only flip a switch the correlation runs from 0.7689 to 1.0000.
The two dependence scenarios sit at 0.2987 and above, and that is correct
behaviour rather than a defect: Iman-Conover reordering changes which path holds
which driver value, so it preserves the marginals exactly and path identity not
at all. They are comparable to the base in distribution, not path by path, and
the write-up says so where it uses them.

---

## Acquisition and growth

### 12. Anchor or effective cost: **clean**

Both published. The anchor is a driver with median 32.26 dollars. The
effective cost at the spend actually modelled is 55.35 in the final
year, pooled across paths, which is 1.72 times the anchor. On the median
path it is 31.84, because the median path never spends enough to
saturate anything. It is published month by month as `cac_effective_blended_mean`
in `out/por_monthly.csv`, with the non-creator channel beside it.

### 13. Break-even struck on the anchor rather than the effective cost: **clean**

The break-even solves pin the anchor, because that is the input, but the target is
evaluated through the saturation and pool-pressure mechanism, so the answer is the
anchor value that produces the outcome at the effective cost. `pinned_sweeps.csv`
carries `final_year_effective_cac_mean` at every pin, so the effective cost at each
pinned anchor is on disk.

### 14. An acquisition budget with no cap: **clean now, and the cap is looser than it sounds**

Capped at 0.75 times the company's own lifetime value estimate, by inverting the
saturation curve for the spend at which effective cost reaches the cap.

It was not clean in another way: the launch acquisition subsidy ran unconditionally
for all sixty months. It now holds for 12 months after go-to-market and tapers
to nothing over the next 12. See `CHANGELOG.md` 0.4.

**The cap is struck on the GROSS lifetime value**, which subtracts nothing but
verification. The all-in contribution is negative on the median path, so the rule
permits spending 0.75 times a number that excludes engineering, content,
overhead and compliance. It is the only restraint on acquisition spend anywhere in
the model, and it is a loose one.

**Does lifetime value exceed cost per acquisition in the final year?** On the mean,
pooled, yes: 120.41 against 55.35, a ratio of
2.18. **On 10.4 per cent of individual paths, no.** And the
lifetime value in that ratio is the **gross** one; against the all-in contribution
the ratio is far worse, and on the median path it is negative, which is item 16.

### 15. A ratio between markets asserted as measured: **clean, and the code disagrees with the prose**

docs/10 states that a Year 10 household can afford roughly twice the acquisition
cost of a Year 11 household. The model asserts no such ratio; it produces one from
a sampled summer lapse probability and a sampled progression rate.

**The number the code actually uses is 1.04, not two**
(3.79 months against 3.63, measured by pinning the
segment mix and re-running on the same random numbers). It reaches two or better
on 0.01 per cent of paths. docs/10's shape survives; its magnitude
does not, and docs/10's own caveat about the summer is most of why: removing the
summer entirely lifts the ratio by 0.407
against 0.029 for flooring in-term churn,
a factor of 14. **Neither recovers two,
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

31.92 dollars per household month pooled, and
17.25 on the median path, is a **gross**
contribution: net revenue less inference, support, payment, hosting and store fees.

The all-in figure, net of engineering, content, overhead and compliance (payment
fees are already out of the gross row above, and are not deducted twice), is 15.56 dollars per household month pooled and
-96.59 on the median path. Pooled, the all-in figure is
16.36 dollars a household month lower than the gross one.

**The pooled and median all-in figures disagree in sign**, because the pooled one
is dominated by the few paths with large books that spread the fixed costs, and
the median path is small with the same fixed costs on top of it. Both are in
`out/cohorts.csv` and both are in the write-up, so neither can stand in for the
other and neither can stand in for the gross figure.

**The same trap has a second door, and a round-three review found the document
walking through it.** The lifetime-value-against-acquisition-cost comparison was
published on the gross basis only: lifetime value is below acquisition cost on
10.4 per cent of paths, which reads as
reassurance. On the all-in basis the same comparison fails on
85.2 per cent. Both are now in
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
0.45 and 0.95, median 0.70. The longest run of consecutive months with the
demand multiplier below 0.80 averages 5.8 months and is
13.0 at the ninetieth percentile; 36.9 per cent of paths contain a run
of six or more and 12.1 per cent a run of twelve or more.

**It did nothing at all until round 2.** Realised acquisition spend was recomputed
from realised acquisitions, so a shock that halved customers halved the money
spent and cost nothing. Spend is now committed in advance. See `CHANGELOG.md` 1b.2.

**And the run lengths above are a property of the demand series, not of the
answer.** What the whole persistent-shock apparatus is worth, measured by pinning
the innovation standard deviation to zero and re-running on the same random
numbers: 33,890 dollars of terminal cash on the mean,
-13,735 on the median path, and 29,101 on the eightieth-percentile
capital requirement. On the 12.1 per cent of paths that do take a run of twelve
or more bad months it bites harder, -3,593,795 on the mean of that group, but
even there the median damage is -563,979. **A sustained demand drought is in
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
| Content exceeds acquisition spend | 84.5 per cent | asserts it |
| Content exceeds both acquisition and people | 59.9 per cent | asserts it |
| The Year 10 cohort retains at least twice the months | 0.01 per cent | **denies it**, against docs/10 |
| Gross lifetime value is below acquisition cost in the final year | 10.4 per cent | **denies it** on the gross basis |
| Variable cost exceeds half of gross consumer revenue, which is where docs/10's row reverses | 1.4 per cent | **denies it** for the plan, concedes it for these paths |
| All-in lifetime value is below acquisition cost in the final year | 85.2 per cent | asserts it on the all-in basis |
| Peak funding exceeds ten million dollars | 83.3 per cent | asserts it |
| Terminal cumulative cash is positive | 11.5 per cent | **denies it** |

**Two failures of this item were found in round four and both are fixed above.**
The first: the lifetime-value share was computed by multiplying each path's own
contribution by the SAMPLE MEAN retained months, a scalar. Retention varies
strongly across paths and correlates with churn, so the published share was a
hybrid presented as a per-path statistic, in the answer to the item about exactly
that. Using each path's own realised retention gives
10.4 per cent against the old
9.9; both are in
`out/cohorts.csv` so the size of the error is on the record. The second: the
docs/10 variable-cost row was answered with a mean and is now given per path in
section 5 of the write-up, where variable cost exceeds half of revenue on
1.4 per cent of live paths.

**The two lifetime-value rows are the pair to read together, and an earlier
draft published only the first.** On the gross basis, which charges a household
inference, support, payments and age assurance and nothing else, lifetime value
clears acquisition cost on almost every path. On the all-in basis, which also
carries the content build and the people who make it, it fails on
85.2 per cent. Quoting the gross
number alone is checklist item 16 — a gross margin presented as a net one — and
it was being done here.

---

## Funding

### 20. Sized on the base case or the plan of record: **clean**

Sized on the **plan of record**, at 28,073,340 dollars across the
horizon at the eightieth percentile. The base case is stated beside it at
17,397,857, along with two narrower scopes. They differ enough
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

10 of the file's
20 commitments have their spend starting inside the seed
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
log converting away from. One commitment lands
after the Series A opens with its spend starting before it: all four boards live
at month 18, built from month 12. The rest-of-English-speaking market at month 24
begins its build at month 18, exactly as the Series A opens, so the file's test
puts it on the right side of the line.

**The Series A does not buy those decisions. It refinances them.** `out/funding_commitments.csv`
holds the landing month and the spend-start month for each.

**What it would move.** Nothing in the cash flow; the spend happens either way.
What it moves is the round sizing: the seed for the plan of record is
10,173,013 dollars, and a round of that size described as a seed will
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
predicts. `sessions_per_hh_month` is sampled between 3.5 and 18 a month, a fivefold
range. docs/03's own arithmetic, three sessions a week for a Year 11 revising one
strand, is about thirteen a month, which sits inside the range rather than at its
top; the range is wider in both directions because nothing measures it.

**What it would move.** `out/breakeven.csv` records the solve. What can be said now
is that the allowance of sixteen sessions, which is a commercial decision already
taken in `model.py`, sits inside that range, so whether 23.6 per cent
of households exceed it or almost none do is not determined by anything measured.

### 23. Do the instrument's strata match the mix the cost base assumes: **not clean**

docs/03's validation pilot is two examiners validating the same twenty items. The
cost base applies `minutes_per_item` across 5 to 11 subjects, two levels and up to
four boards, and `minutes_per_item` is ranked 5 on the capital
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
28,073,340 dollars is "this is what it costs to execute the plan of
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

**What it would move.** The anchor spread of 30,067,131 dollars is an
upper bound. docs/12 names the competing anchor explicitly, that the free tools are already on
the parent's phone, and docs/07 states the substitution arithmetic against the
verified 25 to 45 pound hourly tutoring rate. The two price regimes here differ
by roughly the ratio of their modal prices, 22.00 against 7.00 pounds,
and a difference of that size against a free substitute cannot plausibly leave
conversion untouched. Splitting the feedback bundle so the
price loop can be run alone is a half-day of work and has not been done.

### The largest paths are not plausible and nothing in the instrument says so

Total acquisitions across the horizon run to a median of 42,854, a
ninety-ninth percentile of 3,487,742 and a maximum of 25,676,916.
2.63 per cent of paths end the horizon above a hundred million dollars.

There is now a ceiling, `POOL_REACQUISITION_MULTIPLE`, set at
3.0, so no path acquires more
than that multiple of its own sampled pool in any market, and the largest ratio of
acquisitions to that path's own United Kingdom pool is 37.44 across three
open consumer markets. **That bounds the arithmetic; it does not make the top of
the distribution believable.**

**And it is load-bearing, which the document did not say until a round-three
review pointed it out.** The same constant is also the denominator of the
saturation term, so it sets how fast the effective cost of acquisition rises as
a market is worked — one number doing two jobs, neither of them measured. It is
now a configuration key rather than a buried literal, and two scenarios price
it: working the pool twice over rather than three times is worth
-2,910,525 dollars of terminal cash, and
five times over 4,163,784. Nothing in the
vault sets this number. It is a prior, it is not in `out/drivers.csv` because it
is a constant rather than a sampled driver, and a constant that moves the answer
by that much while being invisible to the sensitivity analysis is a defect of
this instrument rather than a property of the business. The reachable-pool prior is log-uniform across a
thirtyfold range and the market relatives multiply it further, so the upper tail
describes a business several times the size of the demand the vault has evidence
for. Those paths are what makes the mean of terminal cash, which is why the
scenario table in the write-up now gives the median beside it.

### "Content is the largest line" is partly a property of the budget rule

On the median path, content costs 12,448,547 over the horizon and
acquisition and verification together cost 1,393,372, a ratio of
8.9 to one. Content is almost entirely exogenous: a fixed schedule
times a sampled item cost, with no demand feedback at all. Acquisition is
throttled by the lifetime-value cap and the launch-subsidy taper.

So the claim is true, and part of the reason it is true is that on most paths the
company barely markets. A plan that spends that ratio on content against customers
is not a plan anyone would execute, and the instruction the write-up draws from
it, that content cost is what makes the venture fundable, should be read with
that in view.

### The lifetime-value cap is struck on a gross figure

`CAC_LTV_CAP` limits acquisition spend to 0.75 times lifetime value, and the
lifetime value it uses subtracts nothing but verification. It is the gross margin,
not the all-in one, and the all-in figure is negative on the median path. The cap
is therefore looser than it sounds, and it is the only thing in the model
restraining acquisition spend.

### How finely a cost is split decides how high it ranks, and no instrument sees that

`out/sobol.csv` ranks the 80 registry entries. A count of how many
of them in a top seven belong to one cost is therefore a fact about the registry,
not about the business. Content cost per item is
3 entries because that is how it
decomposes; one timed pilot measures all of them at once. The content-driver set
this document counts with is 8 entries and
the acquisition set is 12, and both are read off
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

`out/sobol.csv` and `out/tornado.csv` cover the 80 sampled drivers. They cover
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
findings: `P_TUTORING_ANCHOR` at 0.50, which makes every plan-of-record
figure a mixture of two regimes; `POOL_BREADTH_EXPONENT` and
`PLATFORM_PER_EXTRA_MARKET`, which between them set the ratio the write-up calls
the owner's largest decision; and `OVERAGE_CAP_MULT` at 2.5, which sets the
one-sided asymmetry that checklist item 3 rests on.

**One of them stopped being invisible in round 3, and the exercise shows what the
rest are hiding.** `POOL_REACQUISITION_MULTIPLE`, at
3.0, does two jobs: it bounds cumulative
acquisitions and it is the denominator of the saturation term, so it also sets
how fast acquisition gets dearer as a market is worked. It is now a configuration
key with two scenarios, and moving it from three to two is worth
-2,910,525 dollars of terminal cash while
moving it to five is worth 4,163,784. That
is comparable with several of the sampled drivers that section 8 ranks, from a
number nothing in the vault sets and no instrument in this directory could see
until it was lifted out. **The other constants above have not had this done to
them, and the presumption should be that some of them would behave the same
way.**

### The retained book is far shorter than the product being sold

An examination-year household is retained 3.63 months. The commercial unit
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
  qualifications in Singapore. `ROW_TAX` is a single blended 13 per cent against
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

`terminal_cash` is the cumulative cash at month 60 and nothing else. At that
month the instrument assigns **zero** value to the item bank it has just spent
13,965,826 dollars building, and zero to the standing book of
28,667 households still paying.

That is not a neutral default. A large share of the content spend falls in the
last two years and is charged in full against a truncated revenue window:
38.9 per cent of content spend falls in months 36 to 60, and
14.7 per cent in the final twelve. Terminal-month net cash is
307,676 and terminal-month net revenue 1,013,769, an annual
run rate of 12,165,227.

**Every statement in this document of the form "content is the largest line",
"content sets the slope" and "64.0 per cent
of the cost base does not respond to demand" is partly a function of where the
window was cut.** The `por_residual` scenario
credits a residual and is worth 22,345,533 dollars of terminal cash and
-277,735 on the capital requirement. Both of its parameters are priors
and neither is defensible as a valuation; the point is the size, not the number.

Nothing sweeps the horizon itself, no scenario stops building content when the
remaining window is shorter than the payback, and the launch-delay scenarios in
section 9 of the write-up are the same defect showing through in another place.
**This is the second item, alongside the restricted-transfer question, that
changes the ordering rather than the levels, and it is cheaper to test than that
one.**

### Age assurance is charged once per acquired household, never per check

`verif_total += acq * v`. Every check on somebody who does not convert is free.
A reusable identity check is billed per attempt, so at any realistic ratio of
checks to conversions the line is a multiple of what is modelled, priced in
`out/omissions.csv` at 805,658 to
2,014,145 dollars.

The conclusion elsewhere in this file that verification does not dominate the cost
structure rests on a 1.0 per cent share that assumes one check per acquired
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

`appstore_params()` sets 15 per cent on every path, including paths billing
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
5 of the top seven
on the plan of record and
1 on the
go-to-market minimum. The instruction "work on content cost to make it fundable"
is a consequence of a scope decision that has not been taken.

**What is still not clean.** Only three configurations are decomposed. The
ordering is presumably conditional on other choices too — the institution
channel, the price regime, the launch date — and nothing here establishes which.
The honest statement is that the ordering is known to move with scope, is not
known to be stable under anything else, and was published as though it were a
property of the business.

### A break-even against a weak target read as a rescue

The four solved break-evens target half of all paths stringing three
cash-positive months together. `out/breakeven.csv` now carries, for each solved
row, the median path's terminal cash and the eightieth-percentile funding
requirement at that same value, and the share of the paths that meet the target
and still end the horizon negative. On the plan of record that last share is
33.1
per cent. The number was always in the file; the word attached to it was wrong.

### Two mechanisms were tested by the wrong test, and the test said so in the right words

The switched-off reproduction test is a test of the random streams. Section 3
presented it under the heading of mechanism validation, and every one of round
2's four mechanism defects passed it while wrong. It is now two-sided, which
catches inert mechanisms, and is described for what it is. **There is still no
mechanism correctness test in this instrument and there cannot easily be one:
what would it compare against?** The four defects were found by reading the
code, which is the only method that has worked, and which does not scale.

### The gate covers two files of 23

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
837,950 to
2,513,849 dollars, which
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
28,073,340 the plan raises — no
interest, no fees, and nothing for the cash sitting idle between rounds.

`out/cohorts.csv` now prices the first half of that: the same net cash line
discounted at twelve per cent a year is -7,141,539 and at
twenty-five per cent -6,459,642, against
-7,880,764 undiscounted. **The direction matters more than
the level.** Content spend is front- and mid-loaded and revenue arrives late, so
discounting makes content relatively dearer and sharpens the ordering this
document reports; and the residual scenario, the largest single item in the
scenario table at 22,345,533, sits entirely
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
publishes `ltv_cap_assumed_months` at 5.87 against
`ltv_cap_realised_months` at 3.72, a ratio of
1.58. What remains is a geometric life ignoring
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
sampling error on the headline mean is 613,323. The
shock's cost is measured on a PAIRED run, which is far tighter than that, so the
comparison is not quite apples to apples — but it is the right thing to hold in
mind when reading any unpaired difference in this document. The sampled
foreign-exchange scenario is the case where it bites: its delta is not small, it
is **zero** at this sample size.

### The funding requirement is right-censored for four paths in five

`out/por_paths.csv` records each path's trough month.
78.0 per cent of paths have it in the
**last month of the horizon**: cash is still falling when the window closes and
the trough has not happened yet. The median path troughs at month
59 of 60.

The peak funding requirement is the negative of the trough, so every capital
figure in section 11 — the 28,073,340
headline, the staged sum, all four scopes — is a **floor** on the same four paths
in five. The instrument has nothing to say about how much more month 61 asks for,
because there is no month 61.

This was hidden by a mean. The write-up quoted the mean trough month,
53.1 against the averaged line's
44, and concluded the averaged line troughs
"later" — by four tenths of a month. The mean sits between a fifth of paths that
trough early and four fifths that never trough at all, and describes neither.
**It is the same defect as checklist item 19 and it was inside the section whose
entire subject is that a mean of minimums is not the minimum of a mean.**

### The reachable pool responds to subjects and not to levels or boards

`model.py` scales the reachable pool with subject breadth and discards the level
and board counts from the same call. So the go-to-market minimum — five subjects,
one level, one board — and the plan of record's United Kingdom at month 18 — five
subjects, two levels, four boards, and about twelve times the content — are
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

`price_drift_yr` is the registry's only **normal** driver: N(0.015, 0.030),
unbounded in both directions. Real prices **fall** on
30.3 per cent of paths, and the cumulative
real price multiplier at month 60 runs from
0.84 at the fifth percentile to
1.36 at the ninety-fifth. That is a wide
prior on the quantity every revenue figure in this document compounds, and it is
not one of the ranges the write-up quotes.

`out/drivers.csv` printed that mean and standard deviation under a `low`/`high`
header until round four, which said the driver was sampled between 1.5 and 3.0
per cent. It was not, and `figures.py` was one token away from putting the wrong
reading into the prose. The file now has `normal_mean` and `normal_sd` columns
and emits no bounds for a driver that has none.

### A one-sided prior on the one cost the document says is well understood

`infer_decline_yr` is sampled on a strictly positive range, so there is no path
in 20000 on which the unit price of inference rises. Every other
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
"2,248,621" understates the channel's cost
and its revenue at once. It is small either way — the channel is
0.55 per cent of net revenue — but the
figure is not a clean measure of anything.

---

## What five rounds of review say about the gates in this directory

This is the most important limit in the document and it is an empirical one, so
it goes last rather than among the checklist items.

Seven mechanism defects have been found in `model.py` across rounds 2, 4 and 5:
a churn reference in the wrong place, an allowance that truncated at the wrong
number and kept the revenue anyway, saturation measured on the wrong quantity,
an onshoring switch that moved the wrong people, a sitting-month exit applied to
a cohort in the month it arrived — twice, on two different paths into the
segment — and a lifetime-value estimate using a calendar the loop does not have.

**Every one of them passed every automated check in this directory, on every
run, while it was wrong.** Not by accident: the checks cannot see this class of
defect by construction.

- The **character-for-character harness gate** compares the published CSVs
  against a rebuild from the same source. A defect that is *in* the published
  run reproduces perfectly. The gate proves the file matches the code; it says
  nothing about whether the code is right.
- The **two-sided off-test** applies only to switchable mechanisms. Five of the
  seven defects were in the base loop, which has no switch.
- The **five accounting identities** check that cash adds up. Five of the seven
  moved households, ratios or a spend cap — quantities that do not appear in a
  cash identity.
- **`verify.py` Pass B** checks that a number in the prose exists on disk at the
  precision printed. A wrong number computed consistently is on disk.
- The **staleness check** proves the outputs were generated against the current
  code. Against the current *wrong* code, they were.

All seven were found by a reader going through the month loop line by line.
That is the only method that has worked here, it does not scale, and it is not
guaranteed to have finished. **The honest position after five rounds is not that
the mechanisms are correct; it is that a defect of this class survives until
somebody reads the code, and five readings have found seven.** A sixth reading
should be assumed to find more.

**What would actually close it** is not another gate of the kind above. It is a
second implementation of the month loop by a different route — a cohort-level
accounting that tracks each acquisition's own months and cash and reconciles to
the aggregate series — which would catch every one of the seven, because all
seven put a household in the wrong place or at the wrong time. That is a day of
work and it has not been done. It is the largest single improvement available to
this instrument and it is not in the open items, because it is a question about
this directory rather than about the business.
