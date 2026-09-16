"""
figures.py

Derives every figure the write-up is allowed to quote, from the CSVs in out/ and
from nothing else. It does not import model.py and it does not re-run anything:
if a figure cannot be built from a file on disk, it does not exist.

Output: out/figures.csv with name, value, unit, source file and derivation.
"""

import csv
import math
import os
import re

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

FIGS = []


def add(name, value, unit, source, derivation):
    FIGS.append(dict(name=name, value=value, unit=unit, source=source, derivation=derivation))


def read_csv(name):
    with open(os.path.join(OUT, name), newline="") as fh:
        return list(csv.DictReader(fh))


def col(rows, key, cast=float):
    return np.array([cast(r[key]) for r in rows])


# --------------------------------------------------------------------------
# Run metadata
# --------------------------------------------------------------------------
monthly = read_csv("por_monthly.csv")
add("seed", int(monthly[0]["seed"]), "integer", "por_monthly.csv", "the seed column, constant down the file")
add("run_date", monthly[0]["run_date"], "date", "por_monthly.csv", "the run_date column, constant down the file")
add("horizon_months", len(monthly), "months", "por_monthly.csv", "row count")

paths = read_csv("por_paths.csv")
add("n_paths", len(paths), "paths", "por_paths.csv", "row count")

terminal_cash = col(paths, "terminal_cash")
peak_fund = col(paths, "peak_funding_requirement")
trough = col(paths, "trough")
trough_month = col(paths, "trough_month")
rev_passes = col(paths, "month_rev_passes_cost")
fy_cac = col(paths, "final_year_effective_cac")
fy_contrib = col(paths, "final_year_contrib_per_hh_month")
share_over = col(paths, "mean_share_over_allowance")
eff_cac_all = col(paths, "effective_cac_all_in")
cac_anchor = col(paths, "cac_anchor_usd")

# --------------------------------------------------------------------------
# Headline outcomes, plan of record
# --------------------------------------------------------------------------
add("por_terminal_cash_mean", float(terminal_cash.mean()), "USD", "por_paths.csv", "mean of terminal_cash")
add("por_terminal_cash_p50", float(np.percentile(terminal_cash, 50)), "USD", "por_paths.csv", "50th percentile of terminal_cash")
add("por_terminal_cash_p10", float(np.percentile(terminal_cash, 10)), "USD", "por_paths.csv", "10th percentile of terminal_cash")
add("por_terminal_cash_p90", float(np.percentile(terminal_cash, 90)), "USD", "por_paths.csv", "90th percentile of terminal_cash")
add("por_share_reaching_profitability", float((rev_passes >= 0).mean()), "share", "por_paths.csv",
    "share of rows with month_rev_passes_cost >= 0, which marks the first of three consecutive cash-positive months")
add("por_share_reaching_profitability_pct", 100.0 * float((rev_passes >= 0).mean()), "per cent", "por_paths.csv",
    "the same share expressed as a percentage")
reach = rev_passes[rev_passes >= 0]
add("por_median_month_rev_passes_cost", float(np.median(reach)), "month index", "por_paths.csv",
    "median of month_rev_passes_cost over the rows that reach it")
add("por_peak_funding_mean", float(peak_fund.mean()), "USD", "por_paths.csv", "mean of peak_funding_requirement")
add("por_peak_funding_p50", float(np.percentile(peak_fund, 50)), "USD", "por_paths.csv", "50th percentile of peak_funding_requirement")
add("por_peak_funding_p80", float(np.percentile(peak_fund, 80)), "USD", "por_paths.csv", "80th percentile of peak_funding_requirement")
add("por_peak_funding_p95", float(np.percentile(peak_fund, 95)), "USD", "por_paths.csv", "95th percentile of peak_funding_requirement")

# --------------------------------------------------------------------------
# The trough, honestly
# --------------------------------------------------------------------------
cum_mean = col(monthly, "cum_cash_mean")
min_of_mean = float(cum_mean.min())
mean_of_min = float(trough.mean())
add("por_min_of_mean_cash_line", min_of_mean, "USD", "por_monthly.csv", "minimum over months of cum_cash_mean")
add("por_min_of_mean_cash_month", int(cum_mean.argmin()), "month index", "por_monthly.csv", "argmin over months of cum_cash_mean")
add("por_mean_of_per_path_min", mean_of_min, "USD", "por_paths.csv", "mean of the trough column, which is each path's own minimum")
add("por_trough_understatement_ratio", min_of_mean / mean_of_min, "ratio", "por_monthly.csv and por_paths.csv",
    "min of cum_cash_mean divided by mean of the per-path trough")
add("por_trough_understatement_pct", 100.0 * (1.0 - min_of_mean / mean_of_min), "per cent", "por_monthly.csv and por_paths.csv",
    "one minus that ratio, as a percentage: how much shallower the headline trough is")
add("por_trough_p10", float(np.percentile(trough, 10)), "USD", "por_paths.csv", "10th percentile of the per-path trough")
add("por_trough_p90", float(np.percentile(trough, 90)), "USD", "por_paths.csv", "90th percentile of the per-path trough")
add("por_mean_trough_month", float(trough_month.mean()), "month index", "por_paths.csv", "mean of trough_month")

# --------------------------------------------------------------------------
# Unit economics
# --------------------------------------------------------------------------
add("por_final_year_contrib_per_hh_month_mean", float(fy_contrib.mean()), "USD per household month", "por_paths.csv",
    "mean of final_year_contrib_per_hh_month, which is net revenue less inference, support, payment and hosting only")
add("por_final_year_effective_cac_mean", float(fy_cac.mean()), "USD per acquisition", "por_paths.csv",
    "mean of final_year_effective_cac: final twelve months of acquisition and verification spend divided by final twelve months of acquisitions")
add("por_cac_anchor_median", float(np.median(cac_anchor)), "USD per acquisition", "por_paths.csv",
    "median of the cac_anchor_usd driver column, which is the low-volume anchor and not a cost at scale")
add("por_cac_effective_over_anchor", float(fy_cac.mean() / np.median(cac_anchor)), "ratio", "por_paths.csv",
    "mean final-year effective CAC divided by the median anchor")
add("por_effective_cac_all_in_mean", float(eff_cac_all.mean()), "USD per acquisition", "por_paths.csv",
    "mean of effective_cac_all_in over the whole horizon")
add("por_mean_share_over_allowance", float(share_over.mean()), "share", "por_paths.csv",
    "mean of mean_share_over_allowance: the household-weighted share of active households exceeding the sold session allowance")
add("por_mean_share_over_allowance_pct", 100.0 * float(share_over.mean()), "per cent", "por_paths.csv", "the same share as a percentage")

# --------------------------------------------------------------------------
# Cost split over the horizon, from the monthly means
# --------------------------------------------------------------------------
COST_LINES = ["inference_cost", "support_cost", "payment_cost", "hosting_cost", "verif_cost",
              "cac_spend", "content_cost", "people_beng_cost", "people_uk_cost", "step_cost",
              "school_onboard_cost", "appstore_fee"]
totals = {c: float(col(monthly, c + "_mean").sum()) for c in COST_LINES}
grand = sum(totals.values())
add("por_total_cost_mean", grand, "USD", "por_monthly.csv", "sum over months of the mean of every cost line")
for c, v in totals.items():
    add("por_total_%s_mean" % c, v, "USD", "por_monthly.csv", "sum over months of %s_mean" % c)
    add("por_share_%s" % c, v / grand if grand else 0.0, "share", "por_monthly.csv",
        "%s_mean summed over months, divided by the sum of every cost line" % c)
    add("por_share_%s_pct" % c, 100.0 * (v / grand if grand else 0.0), "per cent", "por_monthly.csv",
        "the same share as a percentage")

rev_c = float(col(monthly, "net_rev_consumer_mean").sum())
rev_s = float(col(monthly, "net_rev_schools_mean").sum())
gross_c = float(col(monthly, "gross_rev_consumer_mean").sum())
tax_c = float(col(monthly, "tax_collected_mean").sum())
add("por_total_net_revenue_mean", rev_c + rev_s, "USD", "por_monthly.csv",
    "sum over months of net_rev_consumer_mean plus net_rev_schools_mean")
add("por_total_gross_consumer_revenue_mean", gross_c, "USD", "por_monthly.csv", "sum over months of gross_rev_consumer_mean")
add("por_total_tax_collected_mean", tax_c, "USD", "por_monthly.csv", "sum over months of tax_collected_mean")
add("por_tax_share_of_gross", tax_c / gross_c if gross_c else 0.0, "share", "por_monthly.csv",
    "tax collected divided by gross consumer revenue: the part of a gross-quoted price that is not revenue")
add("por_tax_share_of_gross_pct", 100.0 * (tax_c / gross_c if gross_c else 0.0), "per cent", "por_monthly.csv", "the same as a percentage")
add("por_schools_share_of_net_revenue_pct", 100.0 * rev_s / (rev_c + rev_s) if (rev_c + rev_s) else 0.0, "per cent",
    "por_monthly.csv", "net_rev_schools_mean summed, over total net revenue summed")

# --------------------------------------------------------------------------
# Band construction and where the band line actually sits
# --------------------------------------------------------------------------
place = col(monthly, "cum_cash_bandcentral_placement")
add("por_band_central_placement_terminal", float(place[-1]), "percentile as a share", "por_monthly.csv",
    "cum_cash_bandcentral_placement in the final row: the percentile of the real per-path distribution the central band line sits at")
add("por_band_central_placement_min", float(place[6:].min()), "percentile as a share", "por_monthly.csv",
    "minimum of cum_cash_bandcentral_placement from month 6 onward")
add("por_band_central_placement_max", float(place[6:].max()), "percentile as a share", "por_monthly.csv",
    "maximum of cum_cash_bandcentral_placement from month 6 onward")

if os.path.exists(os.path.join(OUT, "variants_bands.csv")):
    vb = read_csv("variants_bands.csv")
    for r in vb:
        add("band_placement_%s_%s_terminal" % (r["scenario"], r["band"]), float(r["placement_terminal"]),
            "percentile as a share", "variants_bands.csv",
            "placement_terminal for scenario %s band %s" % (r["scenario"], r["band"]))

# --------------------------------------------------------------------------
# Scenarios
# --------------------------------------------------------------------------
if os.path.exists(os.path.join(OUT, "variants.csv")):
    vr = {r["scenario"]: r for r in read_csv("variants.csv")}
    for name, r in vr.items():
        for k in ("terminal_cash_mean", "terminal_cash_p50", "peak_funding_mean", "peak_funding_p80",
                  "peak_funding_p90", "share_reaching_profitability", "final_year_effective_cac_mean",
                  "final_year_contrib_per_hh_month_mean", "mean_share_over_allowance",
                  "understatement_ratio", "band_central_placement_terminal",
                  "total_content_cost_mean", "total_cost_mean", "total_net_revenue_mean"):
            if k in r:
                add("scenario_%s_%s" % (name, k), float(r[k]), "USD or share", "variants.csv",
                    "column %s for scenario %s" % (k, name))
    base = float(vr["por"]["terminal_cash_mean"])
    for name, r in vr.items():
        if name == "por":
            continue
        add("delta_%s_terminal_cash_mean" % name, float(r["terminal_cash_mean"]) - base, "USD", "variants.csv",
            "terminal_cash_mean for %s less terminal_cash_mean for por" % name)
        if "total_content_cost_mean" in r:
            add("delta_%s_total_content_cost_mean" % name,
                float(r["total_content_cost_mean"]) - float(vr["por"]["total_content_cost_mean"]),
                "USD", "variants.csv",
                "total_content_cost_mean for %s less the same for por" % name)

# --------------------------------------------------------------------------
# Sensitivity
# --------------------------------------------------------------------------
if os.path.exists(os.path.join(OUT, "sobol.csv")):
    sb = read_csv("sobol.csv")
    for target in sorted({r["target"] for r in sb}):
        rows = sorted([r for r in sb if r["target"] == target], key=lambda r: -float(r["sobol_first_order"]))
        add("sobol_%s_sum_first_order" % target, sum(float(r["sobol_first_order"]) for r in rows), "share of variance",
            "sobol.csv", "sum of sobol_first_order over every driver for target %s" % target)
        for i, r in enumerate(rows[:8], start=1):
            add("sobol_%s_rank%d_driver" % (target, i), r["driver"], "driver name", "sobol.csv",
                "driver at rank %d by sobol_first_order for target %s" % (i, target))
            add("sobol_%s_rank%d_value" % (target, i), float(r["sobol_first_order"]), "share of variance", "sobol.csv",
                "sobol_first_order at rank %d for target %s" % (i, target))

if os.path.exists(os.path.join(OUT, "pinned_sweeps.csv")):
    ps = read_csv("pinned_sweeps.csv")
    for d in sorted({r["driver"] for r in ps}):
        rows = sorted([r for r in ps if r["driver"] == d], key=lambda r: int(r["pin_quantile"]))
        lo, hi = float(rows[0]["terminal_cash_mean"]), float(rows[-1]["terminal_cash_mean"])
        add("pinned_%s_terminal_cash_q5" % d, lo, "USD", "pinned_sweeps.csv", "terminal_cash_mean at pin_quantile 5 for %s" % d)
        add("pinned_%s_terminal_cash_q95" % d, hi, "USD", "pinned_sweeps.csv", "terminal_cash_mean at pin_quantile 95 for %s" % d)
        add("pinned_%s_swing" % d, hi - lo, "USD", "pinned_sweeps.csv",
            "terminal_cash_mean at q95 less terminal_cash_mean at q5 for %s" % d)
        add("pinned_%s_swing_abs" % d, abs(hi - lo), "USD", "pinned_sweeps.csv", "absolute value of that swing")

if os.path.exists(os.path.join(OUT, "twoway_grid.csv")):
    tg = read_csv("twoway_grid.csv")
    vals = np.array([float(r["terminal_cash_mean"]) for r in tg])
    add("twoway_driver1", tg[0]["driver1"], "driver name", "twoway_grid.csv", "the driver1 column")
    add("twoway_driver2", tg[0]["driver2"], "driver name", "twoway_grid.csv", "the driver2 column")
    add("twoway_best_terminal_cash_mean", float(vals.max()), "USD", "twoway_grid.csv", "maximum of terminal_cash_mean over the grid")
    add("twoway_worst_terminal_cash_mean", float(vals.min()), "USD", "twoway_grid.csv", "minimum of terminal_cash_mean over the grid")
    add("twoway_range", float(vals.max() - vals.min()), "USD", "twoway_grid.csv", "that maximum less that minimum")

# --------------------------------------------------------------------------
# Break-evens and funding
# --------------------------------------------------------------------------
if os.path.exists(os.path.join(OUT, "breakeven.csv")):
    for r in read_csv("breakeven.csv"):
        key = "breakeven_%s_%s_%s" % (r["scope"], r["driver"], r["metric"])
        if r["status"] == "bracketed" and r["breakeven_value"]:
            add(key, float(r["breakeven_value"]), "driver units", "breakeven.csv",
                "bisection on a pinned %s against %s = %s" % (r["driver"], r["metric"], r["target"]))
        else:
            add(key + "_status", r["status"], "text", "breakeven.csv", "the status column")
        add(key + "_prior_median", float(r["prior_median"]), "driver units", "breakeven.csv", "the prior_median column")

if os.path.exists(os.path.join(OUT, "funding.csv")):
    for r in read_csv("funding.csv"):
        add("funding_%s_%s_round_size" % (r["scenario"], r["stage"]), float(r["round_size"]), "USD", "funding.csv",
            "round_size for scenario %s stage %s" % (r["scenario"], r["stage"]))
        add("funding_%s_%s_need_p80" % (r["scenario"], r["stage"]), float(r["need_p80"]), "USD", "funding.csv",
            "need_p80 for scenario %s stage %s" % (r["scenario"], r["stage"]))

if os.path.exists(os.path.join(OUT, "cohorts.csv")):
    for r in read_csv("cohorts.csv"):
        try:
            add(r["name"], float(r["value"]), r["unit"], "cohorts.csv", r["derivation"])
        except ValueError:
            add(r["name"], r["value"], r["unit"], "cohorts.csv", r["derivation"])

if os.path.exists(os.path.join(OUT, "omissions.csv")):
    for r in read_csv("omissions.csv"):
        slug = re.sub(r"[^a-z0-9]+", "_", r["absent_cost_line"].split(":")[0].lower()).strip("_")
        add("omission_%s_low" % slug, float(r["low_usd"]), "USD", "omissions.csv", r["basis"])
        add("omission_%s_high" % slug, float(r["high_usd"]), "USD", "omissions.csv", r["basis"])
        add("omission_%s_share_high_pct" % slug, 100.0 * float(r["high_share_of_total_cost"]), "per cent",
            "omissions.csv", "high_share_of_total_cost as a percentage")

if os.path.exists(os.path.join(OUT, "imanconover_check.csv")):
    rows = read_csv("imanconover_check.csv")
    add("imanconover_pairs", len(rows), "count", "imanconover_check.csv", "row count")
    worst = max(abs(float(r["target_rank_corr"]) - float(r["achieved_rank_corr"])) for r in rows)
    add("imanconover_worst_corr_error", worst, "rank correlation", "imanconover_check.csv",
        "largest absolute difference between target_rank_corr and achieved_rank_corr")
    add("imanconover_all_marginals_preserved",
        all(r["marginal_preserved_a"] == "True" and r["marginal_preserved_b"] == "True" for r in rows),
        "boolean", "imanconover_check.csv", "every marginal_preserved column is True")

# --------------------------------------------------------------------------
if __name__ == "__main__":
    path = os.path.join(OUT, "figures.csv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["name", "value", "unit", "source", "derivation"])
        for f in FIGS:
            v = f["value"]
            w.writerow([f["name"], ("%.6f" % v) if isinstance(v, float) else v, f["unit"], f["source"], f["derivation"]])
    print("wrote", path, len(FIGS), "figures")
