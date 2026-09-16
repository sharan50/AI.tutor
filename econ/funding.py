"""
funding.py

Sizes the rounds, on the plan of record and on the base case, and checks whether
the staging matches the decisions.

The peak funding requirement is computed without any injection, as the deepest
point of cumulative operating cash flow. That keeps it independent of the round
schedule and stops the round sizing from being circular.

Outputs: out/funding.csv, out/funding_commitments.csv
"""

import csv
import os

import numpy as np

import harness

NS = harness.load()
OUT, SEED, RUN_DATE = NS["OUT"], NS["SEED"], NS["RUN_DATE"]
DRV = NS["_verified"]["drv"]

# Round boundaries, set to the evidence milestones rather than to the calendar.
# Month 18 is where the owner's plan of record says every UK board and both
# levels are live and the two foreign pilots are running; month 36 is where the
# measured expansion is under way.
STAGES = [("seed", 0, 18), ("series_a", 18, 36), ("series_b", 36, 60)]
SIZING_PERCENTILE = 80          # the round is sized at this percentile of need
BUFFER_MONTHS = 6               # months of the stage's own burn carried as buffer

# Two narrower scopes, to answer what a round of seed size could actually buy.
# Both are the plan of record with the expansion removed, not different models.
GTM_MINIMUM = {NS["M_UK"]: [(6, 5, 1, 1)], NS["M_US"]: [], NS["M_IN"]: [], NS["M_ROW"]: []}
ONE_SUBJECT = {NS["M_UK"]: [(6, 1, 1, 1)], NS["M_US"]: [], NS["M_IN"]: [], NS["M_ROW"]: []}

SCENARIOS = {
    "plan_of_record": NS["base_config"](),
    "base_case_uk_only": dict(NS["base_config"](), scope="ukonly", schools=False),
    "gtm_minimum_uk_one_board": dict(NS["base_config"](), scope="ukonly", schools=False,
                                     unit_schedules=GTM_MINIMUM),
    "one_subject_uk_one_board": dict(NS["base_config"](), scope="ukonly", schools=False,
                                     unit_schedules=ONE_SUBJECT),
}


def stage_need(cum, net_cash, a, b):
    """
    Cash the stage has to fund: the deepest drawdown inside the window measured
    from the window's opening balance, so a stage is not credited with cash a
    later stage has not yet raised.
    """
    opening = cum[:, a - 1] if a > 0 else np.zeros(cum.shape[0])
    inside = cum[:, a:b] - opening[:, None]
    return np.maximum(-inside.min(axis=1), 0.0), net_cash[:, a:b]


def main():
    rows = []
    for label, cfg in SCENARIOS.items():
        out, _ = NS["run"](DRV, cfg)
        o, cum = NS["path_outcomes"](out)
        net = out["net_cash"]
        for name, a, b in STAGES:
            need, window = stage_need(cum, net, a, b)
            burn = np.maximum(-window, 0.0).mean(axis=1)
            size = np.percentile(need, SIZING_PERCENTILE) + BUFFER_MONTHS * np.percentile(burn, SIZING_PERCENTILE)
            rows.append([SEED, RUN_DATE, label, name, a, b,
                         "%.6f" % float(np.percentile(need, 50)),
                         "%.6f" % float(np.percentile(need, SIZING_PERCENTILE)),
                         "%.6f" % float(np.percentile(need, 95)),
                         "%.6f" % float(np.percentile(burn, SIZING_PERCENTILE)),
                         "%.6f" % float(size)])
        peak = o["peak_funding_requirement"]
        rows.append([SEED, RUN_DATE, label, "whole_horizon", 0, NS["HORIZON"],
                     "%.6f" % float(np.percentile(peak, 50)),
                     "%.6f" % float(np.percentile(peak, SIZING_PERCENTILE)),
                     "%.6f" % float(np.percentile(peak, 95)),
                     "%.6f" % float(np.maximum(-net, 0.0).mean(axis=1).mean()),
                     "%.6f" % float(np.percentile(peak, SIZING_PERCENTILE))])
        print("%-20s peak funding p50 %14s  p80 %14s  p95 %14s"
              % (label, format(np.percentile(peak, 50), ",.0f"),
                 format(np.percentile(peak, SIZING_PERCENTILE), ",.0f"),
                 format(np.percentile(peak, 95), ",.0f")))

    with open(os.path.join(OUT, "funding.csv"), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "scenario", "stage", "from_month", "to_month",
                    "need_p50", "need_p80", "need_p95", "monthly_burn_p80", "round_size"])
        w.writerows(rows)

    # Does the staging match the decisions? A round that closes after a spend is
    # already committed is not buying that decision; the decision was taken on
    # the previous round's money.
    out, _ = NS["run"](DRV, NS["base_config"]())
    # (milestone, month it lands, month its spend starts). The spend start is
    # what matters: content is built over the six months before delivery and an
    # entity is stood up two months before a market opens, so the decision is
    # taken, and paid for, before the milestone appears.
    W = NS["CONTENT_BUILD_WINDOW"]
    commitments = [
        ("content build for the go-to-market scope begins", 0, 0),
        ("first content delivered, UK go-to-market", 6, 0),
        ("second UK board content live", 10, 10 - W),
        ("A-level content live", 13, 13 - W),
        ("information security certification for the institution channel", 10, 10),
        ("institution channel opens, first sales rep", 12, 12),
        ("US and India entity set-up and market counsel", 13, 13),
        ("US consumer market opens", 15, 15 - W),
        ("India institution pilot opens", 15, 15 - W),
        ("third UK board content live", 16, 16 - W),
        ("all four UK boards live", 18, 18 - W),
        ("rest-of-English-speaking market opens", 24, 24 - W),
        ("second sales rep cohort", 24, 24),
        ("seven UK subjects live", 30, 30 - W),
    ]
    crows = []
    for note, month, starts in commitments:
        stage = next((n for n, a, b in STAGES if a <= month < b), "beyond_horizon")
        closes_at = next((a for n, a, b in STAGES if n == stage), 0)
        prior = next((n for n, a, b in STAGES if a <= starts < b), "before_the_first_round")
        crows.append([SEED, RUN_DATE, note, month, max(starts, 0), stage, closes_at, prior,
                      "no" if starts < closes_at else "yes",
                      "%.6f" % float(out["content_cost"][:, month].mean()),
                      "%.6f" % float(out["step_cost"][:, month].mean())])
    with open(os.path.join(OUT, "funding_commitments.csv"), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "commitment", "month_it_lands", "month_spend_starts",
                    "stage_it_lands_in", "that_stage_opens_month", "stage_that_actually_pays",
                    "decision_taken_after_its_round_closed",
                    "content_cost_that_month_mean", "step_cost_that_month_mean"])
        w.writerows(crows)
    print("wrote funding.csv and funding_commitments.csv")


if __name__ == "__main__":
    main()
