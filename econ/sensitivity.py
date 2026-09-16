"""
sensitivity.py

Runs on the harness, which means it runs the published model.py rather than a
restatement of it.

Four instruments, in increasing cost and decreasing generality:
  1. first-order Sobol indices, estimated by binning on driver rank
  2. a decile tornado
  3. pinned sweeps, where a driver is fixed across the whole sample and the model
     re-run, with the pin applied AFTER the draws so every run in a sweep shares
     its random numbers and the difference is that driver's alone
  4. a two-way grid over the two drivers that own the most variance

Outputs, all under out/:
  sobol.csv  tornado.csv  pinned_sweeps.csv  twoway_grid.csv
"""

import csv
import os
import sys

import numpy as np

import harness

NS = harness.load()
OUT = NS["OUT"]
SEED = NS["SEED"]
RUN_DATE = NS["RUN_DATE"]
DRIVER_NAMES = NS["DRIVER_NAMES"]

BASE = NS["_verified"]
DRV = BASE["drv"]
OUTCOMES = BASE["outcomes"]

# The three things the brief asks the instrument to report on.
def targets(o):
    y = o["terminal_cash"]
    # Terminal cash is heavy-tailed, so a variance decomposition on it is partly
    # a decomposition of its outliers. The rank transform is reported beside it
    # and the two orderings are compared rather than one being quoted alone.
    rank = np.empty_like(y)
    rank[np.argsort(y, kind="stable")] = np.arange(y.shape[0], dtype=float)
    rank = rank / (y.shape[0] - 1.0)
    return {
        "terminal_cash": y,
        "terminal_cash_rank": rank,
        "peak_funding_requirement": o["peak_funding_requirement"],
        "reaches_profitability": (o["month_rev_passes_cost"] >= 0).astype(float),
    }


TARGETS = targets(OUTCOMES)
N_BINS = 40

# The ordering is a property of the scope it was computed on, not of the
# business. On the plan of record the content escalation is the largest single
# commitment and content drivers dominate; on the go-to-market minimum there is
# almost no content escalation to be wrong about, and the ordering rearranges.
# Reporting one ordering as "the" ordering is the error this second run exists
# to make impossible, so both are written to sobol.csv under the run column and
# the write-up quotes them side by side.
# The third run is here because the write-up makes an ordering claim about full
# onshoring, and an ordering claim with no file behind it is exactly what the
# reviews kept catching. An earlier draft asserted that onshoring put a United
# Kingdom salary driver into the top three and pushed item count down; both were
# typed rather than read, and both were wrong.
ALT_RUNS = [
    ("gtm_minimum", dict(scope="ukonly", schools=False, unit_schedules=None)),
    ("onshore_all", dict(onshore_share=1.0)),
]


def scope_runs():
    runs = [("por", TARGETS)]
    for name, over in ALT_RUNS:
        cfg = dict(NS["base_config"]())
        cfg.update(over)
        if name == "gtm_minimum":
            cfg["unit_schedules"] = NS["GTM_MINIMUM_SCHEDULES"]
        out, summary = NS["run"](dict(DRV), cfg)
        o, _cum = NS["path_outcomes"](out, summary)
        runs.append((name, targets(o)))
    return runs


def sobol_first_order(x, y, k=N_BINS):
    """
    Var(E[Y|X]) / Var(Y), estimated by sorting on the rank of X, cutting into k
    equal-count bins and applying the one-way ANOVA correction for bin noise.
    Without the correction every index is biased upward by the within-bin
    variance, and a driver that does nothing scores about k/N.
    """
    n = x.shape[0]
    order = np.argsort(x, kind="stable")
    ys = y[order]
    per = n // k
    ys = ys[:per * k].reshape(k, per)
    grand = ys.mean()
    ssb = per * ((ys.mean(axis=1) - grand) ** 2).sum()
    ssw = ((ys - ys.mean(axis=1, keepdims=True)) ** 2).sum()
    msb = ssb / (k - 1)
    msw = ssw / max(per * k - k, 1)
    var_cond = (msb - msw) / per
    tot = y.var()
    if tot <= 0:
        return 0.0
    return float(max(var_cond / tot, 0.0))


def decile_spread(x, y):
    n = x.shape[0]
    order = np.argsort(x, kind="stable")
    ys = y[order]
    per = n // 10
    lo = ys[:per].mean()
    hi = ys[n - per:].mean()
    return float(lo), float(hi), float(hi - lo)


def write_csv(name, header, rows):
    path = os.path.join(OUT, name)
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    print("wrote", path, len(rows), "rows")
    return path


def run_sobol_and_tornado():
    srows, trows = [], []
    for rname, tset in scope_runs():
        for tname, y in tset.items():
            for d in DRIVER_NAMES:
                x = DRV[d]
                s = sobol_first_order(x, y)
                lo, hi, spread = decile_spread(x, y)
                srows.append([SEED, RUN_DATE, rname, tname, d, "%.6f" % s])
                trows.append([SEED, RUN_DATE, rname, tname, d,
                              "%.6f" % lo, "%.6f" % hi, "%.6f" % spread, "%.6f" % abs(spread)])
    write_csv("sobol.csv", ["seed", "run_date", "run", "target", "driver", "sobol_first_order"], srows)
    write_csv("tornado.csv", ["seed", "run_date", "run", "target", "driver",
                              "decile1_mean", "decile10_mean", "spread", "abs_spread"], trows)
    ranked = {}
    for rname in ["por"] + [n for n, _ in ALT_RUNS]:
        for tname in TARGETS:
            rows = [r for r in srows if r[2] == rname and r[3] == tname]
            rows.sort(key=lambda r: -float(r[5]))
            ranked[(rname, tname)] = [(r[4], float(r[5])) for r in rows]
    return ranked


def pinned_run(pins):
    """Re-run the model with drivers pinned across the whole sample.

    The pin is applied to a copy of the already-drawn dictionary, so every run
    in a sweep uses the same random numbers as the base and the difference
    between runs is the pinned driver's alone.
    """
    drv = dict(DRV)
    for name, value in pins.items():
        drv[name] = np.full_like(DRV[name], value)
    out, summary = NS["run"](drv, NS["base_config"]())
    o, cum = NS["path_outcomes"](out, summary)
    return o, cum


PIN_QUANTILES = [5, 25, 50, 75, 95]


def run_pinned_sweeps(top_drivers):
    rows = []
    for d in top_drivers:
        for q in PIN_QUANTILES:
            v = float(np.percentile(DRV[d], q))
            o, cum = pinned_run({d: v})
            rows.append([SEED, RUN_DATE, d, q, "%.6f" % v,
                         "%.6f" % float(o["terminal_cash"].mean()),
                         "%.6f" % float(np.median(o["terminal_cash"])),
                         "%.6f" % float(o["peak_funding_requirement"].mean()),
                         "%.6f" % float((o["month_rev_passes_cost"] >= 0).mean()),
                         "%.6f" % float(o["final_year_effective_cac"].mean()),
                         "%.6f" % float(o["terminal_active_hh"].mean())])
            print("  pinned %-26s q%-3d -> terminal_cash_mean %s"
                  % (d, q, format(o["terminal_cash"].mean(), ",.0f")))
    return write_csv("pinned_sweeps.csv",
                     ["seed", "run_date", "driver", "pin_quantile", "pin_value",
                      "terminal_cash_mean", "terminal_cash_median",
                      "peak_funding_requirement_mean", "share_reaching_profitability",
                      "final_year_effective_cac_mean", "terminal_active_hh_mean"], rows)


GRID_QUANTILES = [10, 30, 50, 70, 90]


def run_twoway(d1, d2):
    rows = []
    for q1 in GRID_QUANTILES:
        v1 = float(np.percentile(DRV[d1], q1))
        for q2 in GRID_QUANTILES:
            v2 = float(np.percentile(DRV[d2], q2))
            o, cum = pinned_run({d1: v1, d2: v2})
            rows.append([SEED, RUN_DATE, d1, q1, "%.6f" % v1, d2, q2, "%.6f" % v2,
                         "%.6f" % float(o["terminal_cash"].mean()),
                         "%.6f" % float(o["peak_funding_requirement"].mean()),
                         "%.6f" % float((o["month_rev_passes_cost"] >= 0).mean())])
        print("  grid row q%d done" % q1)
    return write_csv("twoway_grid.csv",
                     ["seed", "run_date", "driver1", "q1", "value1", "driver2", "q2", "value2",
                      "terminal_cash_mean", "peak_funding_requirement_mean",
                      "share_reaching_profitability"], rows)


def main():
    ranked = run_sobol_and_tornado()
    # The sweeps and the grid are instruments on the plan of record, so they
    # take the plan of record's ordering. The second ordering is written to the
    # files beside it and is not silently averaged into this one.
    top = [d for d, _ in ranked[("por", "terminal_cash_rank")][:8]]
    print("top first-order Sobol drivers on terminal cash:")
    for d, s in ranked[("por", "terminal_cash")][:12]:
        print("  %-28s %.4f" % (d, s))
    print("the same ordering on the go-to-market minimum, for comparison:")
    for d, s in ranked[("gtm_minimum", "peak_funding_requirement")][:8]:
        print("  %-28s %.4f" % (d, s))
    run_pinned_sweeps(top[:6])
    run_twoway(top[0], top[1])
    with open(os.path.join(OUT, "sensitivity_top.txt"), "w") as fh:
        fh.write("seed %s run_date %s\n" % (SEED, RUN_DATE))
        for (rname, tname), items in ranked.items():
            fh.write("run %s target %s\n" % (rname, tname))
            for d, s in items[:15]:
                fh.write("  %-30s %.6f\n" % (d, s))
    print("done")


if __name__ == "__main__":
    main()
