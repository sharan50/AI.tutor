"""
rescue_grid.py

Every single-driver break-even in out/breakeven.csv is unbracketed: no value of
any one driver, anywhere in its prior range, gets the median path whole. That is
the finding, but it is not a useful instruction on its own.

This asks the next question. Taking the two drivers that the break-even
endpoints get closest on, the acquisition anchor and the tutoring-anchored
price, it grids them together on two scopes and reports where the boundary
actually sits. The price-anchor regime is pinned to tutoring throughout, because
price does nothing on a path that anchors on software, and pinning it is stated
rather than hidden.

All pins are applied after the draws, so every cell shares the base random
numbers with every other cell and with the published run.

Output: out/rescue_grid.csv
"""

import csv
import os

import numpy as np

import harness

NS = harness.load()
OUT, SEED, RUN_DATE = NS["OUT"], NS["SEED"], NS["RUN_DATE"]
DRV = NS["_verified"]["drv"]

GTM_MINIMUM = {NS["M_UK"]: [(6, 5, 1, 1)], NS["M_US"]: [], NS["M_IN"]: [], NS["M_ROW"]: []}
SCOPES = {
    "plan_of_record": NS["base_config"](),
    "gtm_minimum_uk_one_board": dict(NS["base_config"](), scope="ukonly", schools=False,
                                     unit_schedules=GTM_MINIMUM),
}

D1, D2 = "cac_anchor_usd", "price_uk_tut_gbp"
QUANTILES = [5, 20, 40, 60, 80, 95]


def run_cell(scope, v1, v2):
    drv = dict(DRV)
    drv[D1] = np.full_like(DRV[D1], v1)
    drv[D2] = np.full_like(DRV[D2], v2)
    drv["anchor_u"] = np.zeros_like(DRV["anchor_u"])      # condition C1 passing
    out, summary = NS["run"](drv, SCOPES[scope])
    o, cum = NS["path_outcomes"](out, summary)
    return o


def main():
    rows = []
    for scope in SCOPES:
        for q1 in QUANTILES:
            v1 = float(np.percentile(DRV[D1], q1))
            for q2 in QUANTILES:
                v2 = float(np.percentile(DRV[D2], q2))
                o = run_cell(scope, v1, v2)
                rows.append([SEED, RUN_DATE, scope, D1, q1, "%.6f" % v1, D2, q2, "%.6f" % v2,
                             "%.6f" % float(np.median(o["terminal_cash"])),
                             "%.6f" % float(o["terminal_cash"].mean()),
                             "%.6f" % float(np.percentile(o["peak_funding_requirement"], 80)),
                             "%.6f" % float((o["month_rev_passes_cost"] >= 0).mean()),
                             "%.6f" % float(o["final_year_effective_cac"].mean())])
            print("  %-26s %s q%d row done" % (scope, D1, q1))
    path = os.path.join(OUT, "rescue_grid.csv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "scope", "driver1", "q1", "value1", "driver2", "q2", "value2",
                    "terminal_cash_median", "terminal_cash_mean", "peak_funding_p80",
                    "share_reaching_profitability", "final_year_effective_cac_mean"])
        w.writerows(rows)
    print("wrote", path, len(rows), "cells")

    for scope in SCOPES:
        cells = [r for r in rows if r[2] == scope and float(r[9]) > 0]
        if cells:
            best = min(cells, key=lambda r: (-int(r[4]), int(r[7])))
            print("%s: median path whole in %d of %d cells; the hardest cell that clears is "
                  "%s at q%s (%.2f) with %s at q%s (%.2f)"
                  % (scope, len(cells), len([r for r in rows if r[2] == scope]),
                     D1, best[4], float(best[5]), D2, best[7], float(best[8])))
        else:
            print("%s: the median path is never whole anywhere on this grid" % scope)


if __name__ == "__main__":
    main()
