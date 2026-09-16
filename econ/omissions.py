"""
omissions.py

Checklist item 8: does any cost have no term at all? Grep for it. Absence is not
conservatism.

Each line below was searched for in model.py and is not there. Each is priced
from a figure the model already carries, so the size of the omission is a number
rather than a shrug. They are NOT added to the model: they are published beside
it, so the reader can see both the gap and what closing it would do.

Output: out/omissions.csv
"""

import csv
import os

import numpy as np

import harness

NS = harness.load()
OUT, SEED, RUN_DATE = NS["OUT"], NS["SEED"], NS["RUN_DATE"]
DRV = NS["_verified"]["drv"]
MOUT = NS["_verified"]["out"]

LINES = ["inference_cost", "support_cost", "payment_cost", "hosting_cost", "verif_cost",
         "cac_spend", "content_cost", "people_beng_cost", "people_uk_cost", "step_cost",
         "school_onboard_cost", "appstore_fee"]
total_cost = float(sum(MOUT[c].sum(axis=1).mean() for c in LINES))
gross = float(MOUT["gross_rev_consumer"].sum(axis=1).mean())
beng_people = float(MOUT["people_beng_cost"].sum(axis=1).mean())
uk_people = float(MOUT["people_uk_cost"].sum(axis=1).mean())
months_live = NS["HORIZON"] - NS["CONSUMER_OPEN"][NS["M_UK"]]
years_live = months_live / 12.0

eng_med = float(np.median(DRV["eng_usd_yr"]))
uk_med = float(np.median(DRV["uk_gbp_yr"])) * NS["FX_GBP_USD"]
oh = float(np.median(DRV["overhead_mult"]))

# Two of the lines below are retention mechanics, not cost lines, so they cannot
# be priced as a cost and were left at zero. A zero in the cost column is
# correct and a zero as the size of the omission is not: the model can be asked
# what a worse book is worth, by scaling the churn drivers and re-running. The
# scale is a prior on how much of the book these two mechanics move, and the
# answer below is the cash consequence of that prior, not a measurement.
CHURN_STRESS = 1.25


def _churn_stress_cost():
    drv = dict(DRV)
    for d in ("churn_base", "churn_m1_extra"):
        drv[d] = DRV[d] * CHURN_STRESS
    out, summary = NS["run"](drv, NS["base_config"]())
    o, _cum = NS["path_outcomes"](out, summary)
    base = float(NS["_verified"]["outcomes"]["terminal_cash"].mean())
    return base - float(o["terminal_cash"].mean())


CHURN_STRESS_COST = _churn_stress_cost()

ROWS = []


def add(line, low, high, basis):
    ROWS.append([SEED, RUN_DATE, line, "%.6f" % low, "%.6f" % high,
                 "%.6f" % (low / total_cost), "%.6f" % (high / total_cost), basis])


# Refunds, chargebacks and failed payments on a consumer subscription. Priced as
# a range on gross consumer revenue, which the model does carry.
add("refunds, chargebacks and failed payments", 0.010 * gross, 0.030 * gross,
    "one to three per cent of modelled gross consumer revenue")

# Professional indemnity, cyber and directors' cover for a child-facing service.
add("insurance: professional indemnity, cyber and directors", 30000.0 * years_live, 80000.0 * years_live,
    "thirty to eighty thousand dollars a year from the UK go-to-market month to the end of the horizon")

# Recruitment. The team goes from a handful to tens of heads inside the horizon.
add("recruitment fees", 0.12 * 35 * eng_med, 0.20 * 35 * eng_med,
    "twelve to twenty per cent of first-year salary on thirty-five hires at the median Bengaluru salary")

# An out-of-hours rota. UK study time is roughly 16:00 to 21:00, which is 21:30
# to 02:30 in Bengaluru, so the product's busiest hours are the build base's night.
add("out-of-hours operations rota", 2.0 * eng_med * oh * 1.30 * years_live,
    4.0 * eng_med * oh * 1.30 * years_live,
    "two to four posts at the median Bengaluru salary and overhead multiplier with a thirty per cent night premium")

# Penetration testing and a bug bounty, which an ICO-facing children's service
# and any institution security review will both ask for.
add("penetration testing and vulnerability disclosure", 25000.0 * years_live, 60000.0 * years_live,
    "twenty-five to sixty thousand dollars a year over the same period")

# Intercompany markup. D13 keeps the Indian operating company for ordinary tax
# reasons, which means a cost-plus arrangement and taxable profit in India.
add("intercompany markup and Indian tax on it", 0.10 * beng_people * 0.25, 0.15 * beng_people * 0.25,
    "a ten to fifteen per cent cost-plus markup on the Bengaluru people cost, taxed at twenty-five per cent")

# Age assurance is charged once per ACQUIRED household. Every check on someone
# who does not convert is free. A reusable identity check is billed per attempt.
_verif_total = float(MOUT["verif_cost"].sum(axis=1).mean())
add("age assurance on non-converting checks", 2.0 * _verif_total, 5.0 * _verif_total,
    "the model bills one check per acquisition; at two to five checks per acquired household, which is a conservative funnel for a consumer trial, the line is two to five times what is modelled")

# The United Kingdom consumer subscription regime. The Digital Markets,
# Competition and Consumers Act 2024 brings mandatory renewal reminders, a
# cooling-off right on renewal and an easy-exit duty; the Consumer Contracts
# Regulations bring a fourteen-day cancellation right. All of them are retention
# and revenue mechanics and none has a term here.
add("consumer subscription regime: renewal reminders, cooling off, easy exit", 0.0, 0.0,
    "zero as a cost line, because these are retention mechanics rather than costs. The size is not zero: scaling both churn drivers by %.0f per cent, which is this file's prior on what a reminder-and-easy-exit regime does to a consumer book, costs %s of terminal cash, shared with the row below"
    % (100 * (CHURN_STRESS - 1.0), format(CHURN_STRESS_COST, ",.0f")))

# Trial-to-paid conversion and involuntary churn. Acquisitions here are paying
# households from the month after acquisition; failed cards appear only as a
# cost line and never as retention.
add("trial-to-paid conversion and involuntary churn", 0.0, 0.0,
    "zero as a cost line: an acquisition is a paying household immediately, and failed payments reduce cash without reducing the book, so involuntary churn is absent from retention entirely. The size is the same %s churn stress as the row above, not a second independent amount"
    % format(CHURN_STRESS_COST, ",.0f"))

# Accessibility conformance, which a school procurement process asks for directly.
add("accessibility conformance and audit", 15000.0 * years_live * 0.5, 40000.0 * years_live * 0.5,
    "fifteen to forty thousand dollars a year, from roughly halfway through the horizon")

# Corporation tax. Named and priced at zero, because the plan loses money
# throughout and a zero written down is not the same as a line left out.
add("corporation tax on trading profit", 0.0, 0.0,
    "zero: no scenario in this instrument returns a taxable trading profit inside the horizon")

# Translation and localisation. Near zero by construction, and that is a
# consequence of the English-speaking expansion decision rather than an oversight.
add("translation and localisation", 0.0, 0.0,
    "zero: the plan of record expands only across English-speaking curricula")

# Regulatory enforcement exposure. Written down because a zero recorded is not
# the same as a line left out, and because the vault's own verified facts put a
# single penalty above every cost line here except content. docs/05: the ICO
# fined Reddit 14.47m pounds in February 2026 for inadequate age assurance and
# unlawful profiling of children, TikTok 12.7m and Snap 1.95m; Online Safety Act
# penalties are the higher of 18m pounds or a tenth of qualifying worldwide
# revenue, with business-disruption orders reaching app stores and payment
# processors. Priced at zero because this instrument has no probability to put
# on it, and the zero is the point.
# The comparison is computed rather than asserted. Two earlier drafts asserted
# it and both were wrong: the SMALLEST penalty in the reference class does not
# exceed every cost line except content, and does not exceed the seed round.
_PENALTIES_GBP = {"Snap": 1.95e6, "TikTok": 12.7e6, "Reddit": 14.47e6}
_pen_lo = min(_PENALTIES_GBP.values()) * NS["FX_GBP_USD"]
_pen_hi = max(_PENALTIES_GBP.values()) * NS["FX_GBP_USD"]
_line_totals = {c: float(MOUT[c].sum(axis=1).mean()) for c in LINES}
_lo_exceeds = sorted(c for c, v in _line_totals.items() if v > 0 and _pen_lo > v)
_hi_exceeds = sorted(c for c, v in _line_totals.items() if v > 0 and _pen_hi > v)
add("regulatory enforcement exposure", 0.0, 0.0,
    "zero, and deliberately so: no probability of enforcement is modelled. Against the modelled cost lines, the smallest penalty in the vault's verified United Kingdom set is %s dollars and exceeds %d of the %d non-zero cost lines; the largest is %s dollars and exceeds %d of them. Only the largest exceeds the whole modelled content line, and only the largest exceeds the seed round"
    % (format(_pen_lo, ",.0f"), len(_lo_exceeds), len([v for v in _line_totals.values() if v > 0]),
       format(_pen_hi, ",.0f"), len(_hi_exceeds)))

# Examiner supply has a price in this model and no quantity.
# The hours are taken from the model's own content function rather than from
# the headline unit count. Forty units is the catalogue; what has to be written
# and validated is full item-bank equivalents, which is fewer because further
# boards of a subject reuse part of the first board's bank. Counting the
# catalogue overstated this line by roughly a factor of two.
_fe_m18 = float(np.median(NS["content_full_equivalents"](DRV, NS["M_UK"], 18)))
_hours = (_fe_m18 * float(np.median(DRV["items_per_unit"]))
          * float(np.median(DRV["minutes_per_item"])) / 60.0 * 1.10)
add("examiner supply, as a quantity rather than a price", 0.0, 0.0,
    "zero: the model prices examiner time and never asks whether it exists. The month-18 United Kingdom scope is %.1f full item-bank equivalents after board reuse, which at the median item count and validation minutes and the ten per cent second-validation sample is about %s hours of qualified examiner time, and the rate is perfectly elastic"
    % (_fe_m18, format(_hours, ",.0f")))

# Specification change. Awarding bodies reissue specifications, and a reformed
# subject invalidates the part of an item bank that was written to the old one.
# The model builds content once and never rebuilds it: content_full_equivalents
# is monotone in t and nothing ever expires. Priced from the model's own content
# cost at a rate of reissue rather than left at zero.
_content_total = float(MOUT["content_cost"].sum(axis=1).mean())
add("specification change and curriculum reform", 0.06 * _content_total, 0.18 * _content_total,
    "six to eighteen per cent of the modelled content spend: the model never expires an item, and on a five-year horizon a share of the bank is written to a specification that has since been reissued. The range is a prior on how much of the bank turns over, not a measurement")

if __name__ == "__main__":
    path = os.path.join(OUT, "omissions.csv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "absent_cost_line", "low_usd", "high_usd",
                    "low_share_of_total_cost", "high_share_of_total_cost", "basis"])
        w.writerows(ROWS)
    lo = sum(float(r[3]) for r in ROWS)
    hi = sum(float(r[4]) for r in ROWS)
    with open(path, "a", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow([SEED, RUN_DATE, "TOTAL of every absent line", "%.6f" % lo, "%.6f" % hi,
                    "%.6f" % (lo / total_cost), "%.6f" % (hi / total_cost),
                    "sum of the rows above, against the modelled total cost of %.0f" % total_cost])
    # The retention stress is written on its own, because it is not a cost line
    # and must not be summed into the total above. It is here so the two rows
    # that quote it in prose have a file to trace to.
    rpath = os.path.join(OUT, "sized_omissions.csv")
    with open(rpath, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "quantity", "value", "unit", "basis"])
        w.writerow([SEED, RUN_DATE, "retention_stress_churn_scale", "%.6f" % CHURN_STRESS,
                    "multiple", "the multiple applied to both churn drivers"])
        w.writerow([SEED, RUN_DATE, "retention_stress_terminal_cash_cost", "%.6f" % CHURN_STRESS_COST,
                    "USD",
                    "the two retention omissions above are priced at zero as cost lines because they are not costs; this is what the book being that much worse is worth in terminal cash, and it is a prior on the size of the effect, not a measurement of it"])
        w.writerow([SEED, RUN_DATE, "retention_stress_share_of_total_cost",
                    "%.6f" % (CHURN_STRESS_COST / total_cost), "share",
                    "that cost against the modelled cost base"])
        w.writerow([SEED, RUN_DATE, "examiner_full_equivalents_month18", "%.6f" % _fe_m18,
                    "full item-bank equivalents",
                    "median full item-bank equivalents of United Kingdom content at month 18, after board reuse, from the model's own content function"])
        w.writerow([SEED, RUN_DATE, "penalty_smallest_usd", "%.6f" % _pen_lo, "USD",
                    "the smallest penalty in the vault's verified United Kingdom set, 1.95m pounds to Snap, at the fixed rate"])
        w.writerow([SEED, RUN_DATE, "penalty_largest_usd", "%.6f" % _pen_hi, "USD",
                    "the largest, 14.47m pounds to Reddit in February 2026, at the fixed rate"])
        w.writerow([SEED, RUN_DATE, "examiner_hours_month18", "%.6f" % _hours, "hours",
                    "those equivalents at the median item count and median validation minutes, with the ten per cent second-validation sample"])
    print("wrote", rpath)
    print("wrote", path)
    print("absent cost lines total %s to %s, which is %.2f%% to %.2f%% of the modelled cost base of %s"
          % (format(lo, ",.0f"), format(hi, ",.0f"), 100 * lo / total_cost, 100 * hi / total_cost,
             format(total_cost, ",.0f")))
