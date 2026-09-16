"""
breakeven.py

Where a number does not exist, do not invent one. Take it as an input and answer
the question that can be answered without it: how good or bad may this figure be
before the plan stops working.

Each driver below is pinned across the whole sample, after the draws, so every
run in a solve shares its random numbers with the base. The solve is a bisection
on the pinned value against a stated target.

Outputs: out/breakeven.csv
"""

import csv
import math
import os

import numpy as np

import harness

NS = harness.load()
OUT, SEED, RUN_DATE = NS["OUT"], NS["SEED"], NS["RUN_DATE"]
DRV = NS["_verified"]["drv"]
BASE_CFG = NS["base_config"]()

STEPS = 8
CAPITAL_CEILING_USD = 10_000_000.0     # a stated constraint, not a finding


def metric_share(o):
    return float((o["month_rev_passes_cost"] >= 0).mean())


def metric_terminal_median(o):
    return float(np.median(o["terminal_cash"]))


def metric_peak_funding_p80(o):
    return float(np.percentile(o["peak_funding_requirement"], 80))


METRICS = {
    # name: (function, target, what the target means)
    "share_reaching_profitability": (metric_share, 0.50,
        "half the paths run three consecutive cash-positive months inside the horizon"),
    "terminal_cash_median": (metric_terminal_median, 0.0,
        "the median path ends the horizon having returned the cash it consumed"),
    "peak_funding_p80": (metric_peak_funding_p80, CAPITAL_CEILING_USD,
        "the plan needs no more than ten million dollars at the eightieth percentile"),
}


# A break-even is only a useful question on a scope that can be rescued. On the
# plan of record it cannot: no value of any single driver, anywhere in its prior
# range, reaches any of the targets, because roughly two thirds of the cost base
# is committed before demand can speak to it. Both scopes are therefore solved,
# and the plan of record's answer is reported as the finding it is.
GTM_MINIMUM = {NS["M_UK"]: [(6, 5, 1, 1)], NS["M_US"]: [], NS["M_IN"]: [], NS["M_ROW"]: []}
SCOPES = {
    "plan_of_record": BASE_CFG,
    "gtm_minimum_uk_one_board": dict(NS["base_config"](), scope="ukonly", schools=False,
                                     unit_schedules=GTM_MINIMUM),
}


def evaluate(driver, value, metric_fn, anchor_tutoring=False, scope="plan_of_record"):
    drv = dict(DRV)
    drv[driver] = np.full_like(DRV[driver], value)
    if anchor_tutoring:
        drv["anchor_u"] = np.zeros_like(DRV["anchor_u"])
    out, summary = NS["run"](drv, SCOPES[scope])
    o, _cum = NS["path_outcomes"](out, summary)
    return metric_fn(o)


def bisect(driver, lo, hi, metric_fn, target, log_scale, anchor_tutoring, scope, steps=STEPS):
    """
    Returns (value, (f_lo, f_hi), bracketed). If the target is not bracketed by
    the driver's own prior range, that is the answer and it is reported as such
    rather than extrapolated: no value of that driver alone reaches the target.
    """
    f_lo = evaluate(driver, lo, metric_fn, anchor_tutoring, scope)
    f_hi = evaluate(driver, hi, metric_fn, anchor_tutoring, scope)
    if (f_lo - target) * (f_hi - target) > 0:
        return None, (f_lo, f_hi), False
    for _ in range(steps):
        mid = math.exp((math.log(lo) + math.log(hi)) / 2) if log_scale else (lo + hi) / 2
        f_mid = evaluate(driver, mid, metric_fn, anchor_tutoring, scope)
        if (f_lo - target) * (f_mid - target) <= 0:
            hi, f_hi = mid, f_mid
        else:
            lo, f_lo = mid, f_mid
    mid = math.exp((math.log(lo) + math.log(hi)) / 2) if log_scale else (lo + hi) / 2
    return mid, (f_lo, f_hi), True


# The support of each driver is its own prior range, taken from the registry so
# the two cannot drift apart.
SUPPORT = {name: (kind, params) for name, kind, params, _ in NS["DRIVERS"]}

# (driver, metric, anchor_tutoring, question, the instrument that could settle it)
QUESTIONS = [
    ("pool_uk", "terminal_cash_median", False,
     "how small can the reachable UK household pool be before the median path ends the horizon under water",
     "two weeks of paid search at the objective granularity the item bank already uses, reporting qualified visits per pound and cost per trial start"),
    ("pool_uk", "peak_funding_p80", False,
     "how small can the reachable UK household pool be before the plan needs more than ten million dollars at the eightieth percentile",
     "as above"),
    ("cac_anchor_usd", "terminal_cash_median", False,
     "how dear can a household be to acquire at low volume before the median path ends the horizon under water",
     "thirty measured acquisitions through one named channel at a stated monthly spend, reported as spend divided by acquisitions, split creator-led and not"),
    ("cac_anchor_usd", "peak_funding_p80", False,
     "how dear can a household be to acquire before the plan needs more than ten million dollars at the eightieth percentile",
     "as above"),
    ("verif_cost_usd", "terminal_cash_median", False,
     "how large can age assurance per verified adult be before the median path ends the horizon under water",
     "three quotes from certified providers, which is condition C2 in docs/09 and costs three phone calls"),
    ("minutes_per_item", "terminal_cash_median", False,
     "how slow can examiner validation be before the median path ends the horizon under water",
     "the timed pilot in docs/03: two examiners, the same twenty items, a few hundred pounds"),
    ("items_per_unit", "terminal_cash_median", False,
     "how large can a full subject bank be before the median path ends the horizon under water",
     "decompose one DfE subject content document into objectives and count the items the ten-per-objective rule implies"),
    ("sessions_per_hh_month", "terminal_cash_median", False,
     "how little can a household use the product before the median path ends the horizon under water",
     "nothing in docs/11 produces this before M5; it needs thirty households instrumented for one month, and it is the factor the planned instruments do not measure"),
    ("churn_base", "terminal_cash_median", False,
     "how fast can the book churn in term before the median path ends the horizon under water",
     "the first cohort measured over one examination cycle, split by year group and never blended"),
    ("price_uk_tut_gbp", "terminal_cash_median", True,
     "with condition C1 passing on every path, how low can the tutoring-anchored price be before the median path ends the horizon under water",
     "landing-page price testing, condition C1 in docs/09, days and a small spend"),
    ("cac_anchor_usd", "share_reaching_profitability", False,
     "how cheap must a household be to acquire before half of all paths run three consecutive cash-positive months",
     "the same thirty measured acquisitions at two spend levels"),
    ("price_uk_tut_gbp", "share_reaching_profitability", True,
     "with condition C1 passing on every path, how high must the price be before half of all paths run three consecutive cash-positive months",
     "the same landing-page price test"),
]


def main():
    rows = []
    for scope in SCOPES:
        for driver, mname, anchor_tut, question, trigger in QUESTIONS:
            kind, params = SUPPORT[driver]
            lo, hi = (params[0], params[2]) if kind == "tri" else (params[0], params[1])
            log_scale = (kind == "lu")
            fn, target, meaning = METRICS[mname]
            value, ends, bracketed = bisect(driver, lo, hi, fn, target, log_scale, anchor_tut, scope)
            base_val = float(np.median(DRV[driver]))
            rows.append([SEED, RUN_DATE, scope, driver, mname, "%.6f" % target, meaning,
                         "anchor_tutoring" if anchor_tut else "published",
                         "%.6f" % lo, "%.6f" % hi,
                         "%.6f" % ends[0], "%.6f" % ends[1],
                         "bracketed" if bracketed else "not bracketed by the prior range",
                         ("%.6f" % value) if value is not None else "",
                         "%.6f" % base_val, question, trigger])
            print("%-26s %-20s %-30s %s" % (scope, driver, mname,
                  ("break-even at %.4f (prior median %.4f)" % (value, base_val)) if bracketed
                  else "no value in the prior range reaches the target: ends %.4f and %.4f" % ends))

    with open(os.path.join(OUT, "breakeven.csv"), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "scope", "driver", "metric", "target", "target_meaning", "sample",
                    "support_low", "support_high", "metric_at_support_low", "metric_at_support_high",
                    "status", "breakeven_value", "prior_median", "question", "trigger"])
        w.writerows(rows)
    print("wrote breakeven.csv")


if __name__ == "__main__":
    main()
