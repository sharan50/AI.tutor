"""
params.py

Dumps the driver registry and the model's decided constants to CSV, so that a
range or a constant quoted in prose traces to a file on disk like every other
number rather than being typed from memory.

Runs on the harness, so it dumps the published model rather than a restatement.

Outputs: out/drivers.csv, out/constants.csv
"""

import csv
import os

import harness

NS = harness.load()
OUT, SEED, RUN_DATE = NS["OUT"], NS["SEED"], NS["RUN_DATE"]

# Constants that are decisions taken in model.py, each with what it is.
CONSTANTS = [
    ("FX_GBP_USD", "United States dollars per pound, fixed at the owner's instruction"),
    ("FX_INR_USD", "United States dollars per rupee, fixed at the owner's instruction"),
    ("VAT_UK", "United Kingdom VAT on business-to-consumer digital services, statutory"),
    ("GST_IN", "Indian GST on OIDAR services, statutory"),
    ("ROW_TAX", "blended rest-of-English-speaking consumption tax, a stated prior"),
    ("SESSION_ALLOWANCE", "sessions included per active household per month, a commercial decision"),
    ("OVERAGE_CAP_MULT", "billed overage capped at this multiple of the allowance, a commercial decision"),
    ("CAC_LTV_CAP", "acquisition spend capped so effective cost stays below this times lifetime value"),
    ("ACQ_RAMP_HOLD_MONTHS", "months the launch acquisition subsidy holds after go-to-market"),
    ("ACQ_RAMP_TAPER_MONTHS", "months over which it then tapers to nothing"),
    ("ROTA_EXTENDED_AT", "active households at which safeguarding cover steps up"),
    ("ROTA_24_7_AT", "active households at which an out-of-hours rota is added"),
    ("PLATFORM_PER_EXTRA_MARKET", "platform engineering heads per additional live consumer market"),
    ("PLATFORM_FOR_INSTITUTIONS", "platform engineering heads for running the institution channel"),
    ("POOL_BREADTH_REFERENCE_SUBJECTS", "subject count the reachable pool driver is defined at"),
    ("POOL_BREADTH_EXPONENT", "exponent by which reachable pool scales with subject breadth"),
    ("CONTENT_BUILD_WINDOW", "months a content step is built over before it is delivered"),
    ("SCHOOL_USAGE_REL", "a school seat's usage relative to a paying household's"),
    ("SCHOOL_ONBOARD_WEEKS", "United Kingdom person-weeks per institution: agreement, security review, onboarding"),
    ("GTM_MONTH", "the month the United Kingdom consumer market opens"),
    ("HORIZON", "months in the horizon"),
    ("N_PATHS", "paths simulated"),
    ("P_TUTORING_ANCHOR", "probability a path lands in the tutoring-anchored price regime"),
    ("SHOCK_BAD_THRESHOLD", "demand multiplier below which a month counts toward a bad run"),
    ("APPSTORE_FEE", "app store commission used by the app-store scenario, the small business rate"),
    ("POOL_REACQUISITION_MULTIPLE", "how many times over the reachable pool may be worked across the horizon; it is also the denominator of the saturation term, so it sets how fast acquisition gets dearer as a market is worked"),
    ("START_YEAR", "calendar year of month zero"),
    ("START_MONTH_IDX", "calendar month index of month zero, zero being January"),
]

if __name__ == "__main__":
    # The "low" and "high" columns mean different things for different
    # distributions, and the header used to hide that. For a normal driver the
    # two registry parameters are a MEAN and a STANDARD DEVIATION, not bounds:
    # writing them under low/high told a reader that price_drift_yr is sampled
    # between 1.5 and 3.0 per cent when it is N(0.015, 0.030), unbounded, with
    # roughly a third of paths drawing a negative drift. The columns now say
    # what they hold, and a normal driver's bounds are left empty because it has
    # none.
    rows = []
    for name, kind, params, note in NS["DRIVERS"]:
        lo = mode = hi = mu = sd = ""
        if kind == "tri":
            lo, mode, hi = params[0], params[1], params[2]
        elif kind == "n":
            mu, sd = params[0], params[1]
        else:
            lo, hi = params[0], params[1]
        fmt = lambda v: ("%.6f" % v) if v != "" else ""
        rows.append([SEED, RUN_DATE, name, kind, fmt(lo), fmt(mode), fmt(hi),
                     fmt(mu), fmt(sd), note])
    path = os.path.join(OUT, "drivers.csv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "driver", "distribution", "low", "mode", "high",
                    "normal_mean", "normal_sd", "what_anchors_the_range"])
        w.writerows(rows)
    print("wrote", path, len(rows), "drivers")

    crows = []
    for name, what in CONSTANTS:
        v = NS[name]
        crows.append([SEED, RUN_DATE, name, "%.6f" % float(v), what])
    # The rupee rate is stored as dollars per rupee; prose quotes rupees per
    # dollar, so its inverse is written down rather than computed in the text.
    crows.append([SEED, RUN_DATE, "FX_INR_USD_inverse", "%.6f" % (1.0 / NS["FX_INR_USD"]),
                  "rupees per United States dollar, the inverse of FX_INR_USD"])
    path = os.path.join(OUT, "constants.csv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "constant", "value", "what_it_is"])
        w.writerows(crows)
    print("wrote", path, len(crows), "constants")
