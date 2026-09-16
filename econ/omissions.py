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
add("regulatory enforcement exposure", 0.0, 0.0,
    "zero, and deliberately so: no probability of enforcement is modelled, while the smallest United Kingdom penalty in the vault's own verified set exceeds every cost line here except content")

# Examiner supply has a price in this model and no quantity. The month-18 scope
# is five subjects, two levels and four boards, and at the median item count and
# validation minutes that is tens of thousands of hours of qualified United
# Kingdom examiner time. examiner_rate_gbp_hr is perfectly elastic.
_units_m18 = 5 * 2 * 4
_hours = _units_m18 * float(np.median(DRV["items_per_unit"])) * float(np.median(DRV["minutes_per_item"])) / 60.0
add("examiner supply, as a quantity rather than a price", 0.0, 0.0,
    "zero: the model prices examiner time and never asks whether it exists. The month-18 scope needs about %s hours of qualified examiner time and the rate is perfectly elastic"
    % format(_hours, ",.0f"))

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
    print("wrote", path)
    print("absent cost lines total %s to %s, which is %.2f%% to %.2f%% of the modelled cost base of %s"
          % (format(lo, ",.0f"), format(hi, ",.0f"), 100 * lo / total_cost, 100 * hi / total_cost,
             format(total_cost, ",.0f")))
