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


def _fmt(v):
    return ("%.6f" % v) if isinstance(v, float) else str(v)


def add(name, value, unit, source, derivation):
    """
    Record a figure. A name may be added more than once only if it carries the
    same value each time; a name collision with two different values would let a
    later row silently overwrite an earlier one, and every figure in this file is
    quoted somewhere by name.
    """
    for f in FIGS:
        if f["name"] == name:
            if _fmt(f["value"]) != _fmt(value):
                raise AssertionError(
                    "figure name collision: %r already recorded as %s from %s, now %s from %s"
                    % (name, _fmt(f["value"]), f["source"], _fmt(value), source))
            return
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
# The driver registry and the decided constants, so that a range or a constant
# quoted in prose traces to a file on disk like every other number.
# --------------------------------------------------------------------------
if os.path.exists(os.path.join(OUT, "drivers.csv")):
    drows = read_csv("drivers.csv")
    add("n_drivers", len(drows), "count", "drivers.csv", "row count")
    for r in drows:
        add("driver_%s_low" % r["driver"], float(r["low"]), "driver units", "drivers.csv",
            "the low column for %s" % r["driver"])
        add("driver_%s_high" % r["driver"], float(r["high"]), "driver units", "drivers.csv",
            "the high column for %s" % r["driver"])
        if r["mode"]:
            add("driver_%s_mode" % r["driver"], float(r["mode"]), "driver units", "drivers.csv",
                "the mode column for %s" % r["driver"])
        if r["driver"] == "uk_gbp_yr":
            add("driver_uk_gbp_yr_low_usd", float(r["low"]) * 1.27, "USD", "drivers.csv",
                "the low column for uk_gbp_yr converted at the fixed rate in constants.csv")
            add("driver_uk_gbp_yr_high_usd", float(r["high"]) * 1.27, "USD", "drivers.csv",
                "the high column for uk_gbp_yr converted at the fixed rate in constants.csv")
        add("driver_%s_low_pct" % r["driver"], 100.0 * float(r["low"]), "per cent", "drivers.csv",
            "the low column for %s, as a percentage" % r["driver"])
        add("driver_%s_high_pct" % r["driver"], 100.0 * float(r["high"]), "per cent", "drivers.csv",
            "the high column for %s, as a percentage" % r["driver"])

if os.path.exists(os.path.join(OUT, "constants.csv")):
    for r in read_csv("constants.csv"):
        add("const_%s" % r["constant"], float(r["value"]), "model units", "constants.csv", r["what_it_is"])
        add("const_%s_pct" % r["constant"], 100.0 * float(r["value"]), "per cent", "constants.csv",
            "%s, as a percentage" % r["what_it_is"])

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
# The mean of this per-path ratio is not a usable number: its denominator goes
# to zero on paths whose book has collapsed, so a handful of paths carry the
# mean to millions. The median is published here and cohorts.csv carries the
# pooled figure, which is the one to quote.
add("por_final_year_contrib_per_hh_month_median", float(np.median(fy_contrib)), "USD per household month",
    "por_paths.csv",
    "median of final_year_contrib_per_hh_month, which is net revenue less inference, support, payment and hosting only")
add("por_final_year_contrib_per_hh_month_p05", float(np.percentile(fy_contrib, 5)), "USD per household month",
    "por_paths.csv", "5th percentile of final_year_contrib_per_hh_month")
add("por_final_year_contrib_per_hh_month_p95", float(np.percentile(fy_contrib, 95)), "USD per household month",
    "por_paths.csv", "95th percentile of final_year_contrib_per_hh_month")
add("por_final_year_effective_cac_mean", float(fy_cac.mean()), "USD per acquisition", "por_paths.csv",
    "mean of final_year_effective_cac: final twelve months of acquisition and verification spend divided by final twelve months of acquisitions")
add("por_final_year_effective_cac_median", float(np.median(fy_cac)), "USD per acquisition", "por_paths.csv",
    "median of final_year_effective_cac")
add("por_cac_anchor_median", float(np.median(cac_anchor)), "USD per acquisition", "por_paths.csv",
    "median of the cac_anchor_usd driver column, which is the low-volume anchor and not a cost at scale")
add("por_cac_effective_over_anchor", float(np.median(fy_cac) / np.median(cac_anchor)), "ratio", "por_paths.csv",
    "median final-year effective CAC divided by the median anchor, both medians so the ratio is on one basis")
add("por_effective_cac_all_in_mean", float(eff_cac_all.mean()), "USD per acquisition", "por_paths.csv",
    "mean of effective_cac_all_in over the whole horizon")
# The size of the largest paths, so a reader can judge their plausibility rather
# than being asked to take the mean on trust.
tot_acq = col(paths, "total_acquisitions")
pool_uk_col = col(paths, "pool_uk")
add("por_total_acquisitions_median", float(np.median(tot_acq)), "households", "por_paths.csv",
    "median over paths of total_acquisitions across the horizon")
add("por_total_acquisitions_p99", float(np.percentile(tot_acq, 99)), "households", "por_paths.csv",
    "99th percentile of total_acquisitions")
add("por_total_acquisitions_max", float(tot_acq.max()), "households", "por_paths.csv",
    "the largest total_acquisitions on any path")
add("por_max_acquisitions_over_own_uk_pool", float((tot_acq / np.maximum(pool_uk_col, 1.0)).max()),
    "ratio", "por_paths.csv",
    "the largest ratio of total acquisitions to that path's own sampled United Kingdom pool; the cap is POOL_REACQUISITION_MULTIPLE per market and the plan of record opens three consumer markets")
add("por_share_paths_terminal_cash_above_100m", float((terminal_cash > 1e8).mean()), "share",
    "por_paths.csv", "share of paths ending the horizon with cumulative cash above one hundred million dollars")

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
# Medians, because the acquisition line is throttled by the budget rule and the
# content line is not, so the mean and the median path spend very differently.
med_content = float(np.median(col(paths, "total_content_cost")))
med_cac = float(np.median(col(paths, "total_cac_spend")))
add("por_median_path_total_content_cost", med_content, "USD", "por_paths.csv",
    "median over paths of total_content_cost")
add("por_median_path_total_cac_spend", med_cac, "USD", "por_paths.csv",
    "median over paths of total_cac_spend, which includes verification")
add("por_median_path_content_over_cac", med_content / med_cac if med_cac else 0.0, "ratio",
    "por_paths.csv", "the median path's content cost divided by its acquisition and verification spend")
for c, v in totals.items():
    add("por_total_%s_mean" % c, v, "USD", "por_monthly.csv", "sum over months of %s_mean" % c)
    add("por_share_%s" % c, v / grand if grand else 0.0, "share", "por_monthly.csv",
        "%s_mean summed over months, divided by the sum of every cost line" % c)
    add("por_share_%s_pct" % c, 100.0 * (v / grand if grand else 0.0), "per cent", "por_monthly.csv",
        "the same share as a percentage")

# Demand-independent cost: content, people and step costs. None of them depends
# on whether a single household buys, which is the reason no single demand driver
# rescues the plan.
DEMAND_INDEPENDENT = ["content_cost", "people_beng_cost", "people_uk_cost", "step_cost"]
_di = sum(totals[c] for c in DEMAND_INDEPENDENT)
add("por_demand_independent_cost_mean", _di, "USD", "por_monthly.csv",
    "content, Bengaluru people, United Kingdom people and step costs, summed over months")
add("por_share_demand_independent", _di / grand if grand else 0.0, "share", "por_monthly.csv",
    "that sum divided by the sum of every cost line")
add("por_share_demand_independent_pct", 100.0 * (_di / grand if grand else 0.0), "per cent",
    "por_monthly.csv", "the same share as a percentage")

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
# A different denominator, and the one a sentence about "more revenue" needs.
add("por_tax_share_of_net_pct", 100.0 * (tax_c / (gross_c - tax_c)) if gross_c > tax_c else 0.0,
    "per cent", "por_monthly.csv",
    "tax collected divided by NET consumer revenue: how much more revenue there would be if the quoted price were net and tax were added on top")
add("por_schools_share_of_net_revenue_pct", 100.0 * rev_s / (rev_c + rev_s) if (rev_c + rev_s) else 0.0, "per cent",
    "por_monthly.csv", "net_rev_schools_mean summed, over total net revenue summed")

# --------------------------------------------------------------------------
# What the horizon writes to zero, and when the content spend falls. These are
# the numbers behind the terminal-value limit in LIMITS.md.
# --------------------------------------------------------------------------
content_by_month = col(monthly, "content_cost_mean")
_tot_content = float(content_by_month.sum())
add("por_content_share_last_24m_pct",
    100.0 * float(content_by_month[36:].sum()) / _tot_content if _tot_content else 0.0,
    "per cent", "por_monthly.csv", "content_cost_mean summed over months 36 onward, over the same summed over all months")
add("por_content_share_last_12m_pct",
    100.0 * float(content_by_month[48:].sum()) / _tot_content if _tot_content else 0.0,
    "per cent", "por_monthly.csv", "content_cost_mean summed over the final twelve months, over the same summed over all months")
add("por_terminal_active_hh_mean", float(col(monthly, "active_hh_mean")[-1]), "households",
    "por_monthly.csv", "active_hh_mean in the final row")
add("por_terminal_month_net_cash_mean", float(col(monthly, "net_cash_mean")[-1]), "USD",
    "por_monthly.csv", "net_cash_mean in the final row")
_tnr = float(col(monthly, "net_rev_consumer_mean")[-1] + col(monthly, "net_rev_schools_mean")[-1])
add("por_terminal_month_net_rev_mean", _tnr, "USD", "por_monthly.csv",
    "net_rev_consumer_mean plus net_rev_schools_mean in the final row")
add("por_terminal_annual_run_rate", 12.0 * _tnr, "USD", "por_monthly.csv",
    "that final-month net revenue multiplied by twelve")

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
                  "mean_share_over_allowance",
                  "understatement_ratio", "band_central_placement_terminal",
                  "total_content_cost_mean", "total_cost_mean", "total_net_revenue_mean",
                  "pathwise_spearman_vs_base", "pathwise_mean_abs_delta", "abs_mean_delta"):
            if k in r:
                add("scenario_%s_%s" % (name, k), float(r[k]), "USD or share", "variants.csv",
                    "column %s for scenario %s" % (k, name))
    # The spread between the two price-anchor regimes is a different quantity
    # from either one's delta against the published run, which is a mix of them.
    if "por_anchor_tutoring" in vr and "por_anchor_software" in vr:
        add("anchor_tutoring_minus_software_terminal_cash_mean",
            float(vr["por_anchor_tutoring"]["terminal_cash_mean"])
            - float(vr["por_anchor_software"]["terminal_cash_mean"]),
            "USD", "variants.csv",
            "terminal_cash_mean for por_anchor_tutoring less terminal_cash_mean for por_anchor_software: the spread between the two regimes, not either one's delta against the published mix")
        add("anchor_tutoring_minus_software_peak_funding_p80",
            float(vr["por_anchor_software"]["peak_funding_p80"])
            - float(vr["por_anchor_tutoring"]["peak_funding_p80"]),
            "USD", "variants.csv",
            "peak_funding_p80 for por_anchor_software less the same for por_anchor_tutoring")
    base = float(vr["por"]["terminal_cash_mean"])
    base_p50 = float(vr["por"]["terminal_cash_p50"])
    base_pf80 = float(vr["por"]["peak_funding_p80"])
    # The real range of the path-matching diagnostic, computed rather than
    # hand-picked: quoting two scenarios as "the loosest and the tightest" was
    # wrong by a factor of nearly three.
    sp = {n: float(r["pathwise_spearman_vs_base"]) for n, r in vr.items()}
    lo_name = min(sp, key=sp.get)
    dep = {n: v for n, v in sp.items() if "dependence" in n}
    nodep = {n: v for n, v in sp.items() if "dependence" not in n}
    add("pathwise_spearman_min", sp[lo_name], "rank correlation", "variants.csv",
        "the lowest pathwise_spearman_vs_base over every scenario")
    add("pathwise_spearman_min_scenario", lo_name, "scenario name", "variants.csv",
        "the scenario carrying that lowest value")
    add("pathwise_spearman_min_excluding_dependence", min(nodep.values()), "rank correlation",
        "variants.csv",
        "the lowest pathwise_spearman_vs_base over scenarios that do not reorder driver values across paths")
    add("pathwise_spearman_min_excluding_dependence_scenario",
        min(nodep, key=nodep.get), "scenario name", "variants.csv", "the scenario carrying that value")
    add("pathwise_spearman_max_dependence", max(dep.values()), "rank correlation", "variants.csv",
        "the highest pathwise_spearman_vs_base among the scenarios that do reorder driver values across paths")
    add("pathwise_spearman_max", max(sp.values()), "rank correlation", "variants.csv",
        "the highest pathwise_spearman_vs_base over every scenario")
    for name, r in vr.items():
        if name == "por":
            continue
        d = float(r["terminal_cash_mean"]) - base
        add("delta_%s_terminal_cash_mean" % name, d, "USD", "variants.csv",
            "terminal_cash_mean for %s less terminal_cash_mean for por" % name)
        # Terminal cash is heavy-tailed, so a delta in the mean can differ from
        # the delta on the median path, and for several scenarios it differs in
        # SIGN. Both are published and the write-up quotes both.
        dm = float(r["terminal_cash_p50"]) - base_p50
        add("delta_%s_terminal_cash_p50" % name, dm, "USD", "variants.csv",
            "terminal_cash_p50 for %s less terminal_cash_p50 for por" % name)
        add("delta_%s_terminal_cash_p50_abs" % name, abs(dm), "USD", "variants.csv",
            "the absolute value of that median difference")
        add("delta_%s_peak_funding_p80" % name,
            float(r["peak_funding_p80"]) - base_pf80, "USD", "variants.csv",
            "peak_funding_p80 for %s less peak_funding_p80 for por" % name)
        add("delta_%s_peak_funding_p80_abs" % name,
            abs(float(r["peak_funding_p80"]) - base_pf80), "USD", "variants.csv",
            "the absolute value of that difference")
        add("delta_%s_sign_agrees_mean_and_median" % name,
            1.0 if (d == 0 and dm == 0) or (d * dm > 0) else 0.0, "boolean", "variants.csv",
            "1 when the mean delta and the median delta for %s have the same sign, 0 when they disagree" % name)
        # The magnitude, so prose can say "costs" or "is worth" without writing a
        # minus sign into a sentence that already carries the direction in words.
        add("delta_%s_terminal_cash_abs" % name, abs(d), "USD", "variants.csv",
            "the absolute value of that difference; the direction is in the sign of delta_%s_terminal_cash_mean" % name)
        if "total_content_cost_mean" in r:
            dc = float(r["total_content_cost_mean"]) - float(vr["por"]["total_content_cost_mean"])
            add("delta_%s_total_content_cost_mean" % name, dc, "USD", "variants.csv",
                "total_content_cost_mean for %s less the same for por" % name)
            add("delta_%s_total_content_cost_abs" % name, abs(dc), "USD", "variants.csv",
                "the absolute value of that difference")

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

    # Counts stated in words in the prose must be counted here, not typed.
    CONTENT_DRIVERS = {"items_per_unit", "writer_gbp_item", "minutes_per_item",
                       "board_reuse", "examiner_rate_gbp_hr", "market_reuse",
                       "reval_frac_yr", "units_per_content_head"}
    ACQ_DRIVERS = {"cac_anchor_usd", "cac_ref_spend_usd", "sat_kappa", "pool_pressure_psi",
                   "creator_share", "creator_cac_rel", "pool_uk", "acq_pct_of_rev",
                   "acq_launch_ramp", "cac_rel_us", "cac_rel_in", "cac_rel_row"}
    for target in sorted({r["target"] for r in sb}):
        rows = sorted([r for r in sb if r["target"] == target], key=lambda r: -float(r["sobol_first_order"]))
        top7 = [r["driver"] for r in rows[:7]]
        top3 = [r["driver"] for r in rows[:3]]
        add("sobol_%s_content_drivers_in_top7" % target, len([d for d in top7 if d in CONTENT_DRIVERS]),
            "count", "sobol.csv", "how many of the top seven drivers by first-order index for %s are content-cost drivers" % target)
        add("sobol_%s_acq_drivers_in_top3" % target, len([d for d in top3 if d in ACQ_DRIVERS]),
            "count", "sobol.csv", "how many of the top three drivers for %s are acquisition drivers" % target)
        add("sobol_%s_content_drivers_in_top3" % target, len([d for d in top3 if d in CONTENT_DRIVERS]),
            "count", "sobol.csv", "how many of the top three drivers for %s are content-cost drivers" % target)
        # Ranks by name, so an ordinal quoted in prose is read off the file for
        # the target it claims rather than typed from a different one.
        for pos, r in enumerate(rows, start=1):
            add("sobol_%s_rank_of_%s" % (target, r["driver"]), pos, "rank", "sobol.csv",
                "the rank of %s by first-order index for target %s" % (r["driver"], target))

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
    berows = read_csv("breakeven.csv")
    # Counts stated in prose must be computed. "Every one is unbracketed" was
    # hand-typed and was false, and the verifier cannot see a word.
    add("breakeven_rows_total", len(berows), "count", "breakeven.csv", "row count")
    add("breakeven_rows_bracketed", len([r for r in berows if r["status"] == "bracketed"]),
        "count", "breakeven.csv", "rows whose status is bracketed")
    add("breakeven_rows_unbracketed", len([r for r in berows if r["status"] != "bracketed"]),
        "count", "breakeven.csv", "rows whose status is not bracketed")
    for scope in sorted({r["scope"] for r in berows}):
        sc = [r for r in berows if r["scope"] == scope]
        add("breakeven_%s_questions" % scope, len(sc), "count", "breakeven.csv",
            "questions solved for scope %s" % scope)
        add("breakeven_%s_bracketed" % scope, len([r for r in sc if r["status"] == "bracketed"]),
            "count", "breakeven.csv", "bracketed rows for scope %s" % scope)
    add("breakeven_distinct_drivers", len({r["driver"] for r in berows}), "count", "breakeven.csv",
        "distinct drivers appearing in the breakeven table")
    add("breakeven_distinct_metrics", len({r["metric"] for r in berows}), "count", "breakeven.csv",
        "distinct targets the questions were solved against")
    for r in berows:
        if r["status"] == "bracketed" and r["breakeven_value"]:
            v = float(r["breakeven_value"])
            add("breakeven_at_%s_%s_%s" % (r["scope"], r["driver"], r["metric"]), v,
                "driver units", "breakeven.csv",
                "the bracketed break-even value for %s on %s against %s" % (r["driver"], r["scope"], r["metric"]))
            if r["driver"] == "price_uk_tut_gbp":
                add("breakeven_%s_price_hours_at_25" % r["scope"], v / 25.0, "hours",
                    "breakeven.csv",
                    "that monthly price as hours of GCSE tutoring at the bottom of the verified 25 to 45 pound hourly band")
                add("breakeven_%s_price_hours_at_45" % r["scope"], v / 45.0, "hours",
                    "breakeven.csv", "the same at the top of that band")
    for r in berows:
        key = "breakeven_%s_%s_%s" % (r["scope"], r["driver"], r["metric"])
        if r["status"] == "bracketed" and r["breakeven_value"]:
            add(key, float(r["breakeven_value"]), "driver units", "breakeven.csv",
                "bisection on a pinned %s against %s = %s" % (r["driver"], r["metric"], r["target"]))
        else:
            add(key + "_status", r["status"], "text", "breakeven.csv", "the status column")
        add(key + "_prior_median", float(r["prior_median"]), "driver units", "breakeven.csv", "the prior_median column")

if os.path.exists(os.path.join(OUT, "funding.csv")):
    frows = read_csv("funding.csv")
    _fw = {(r["scenario"], r["stage"]): r for r in frows}
    if ("plan_of_record", "whole_horizon") in _fw and ("gtm_minimum_uk_one_board", "whole_horizon") in _fw:
        add("funding_por_less_gtm_minimum_whole_horizon",
            float(_fw[("plan_of_record", "whole_horizon")]["round_size"])
            - float(_fw[("gtm_minimum_uk_one_board", "whole_horizon")]["round_size"]),
            "USD", "funding.csv",
            "whole-horizon round_size for the plan of record less the same for the go-to-market minimum")
    # The staged rounds carry a buffer and the whole-horizon figure does not, so
    # they are computed by different rules and their sum is not the headline.
    for scen in sorted({r["scenario"] for r in frows}):
        staged = sum(float(r["round_size"]) for r in frows
                     if r["scenario"] == scen and r["stage"] != "whole_horizon")
        whole = [float(r["round_size"]) for r in frows
                 if r["scenario"] == scen and r["stage"] == "whole_horizon"]
        add("funding_%s_staged_sum" % scen, staged, "USD", "funding.csv",
            "the three staged round_size values for %s, added" % scen)
        if whole:
            add("funding_%s_staged_over_whole" % scen, staged / whole[0], "ratio", "funding.csv",
                "that staged sum divided by the whole-horizon round_size for %s" % scen)
            add("funding_%s_staged_less_whole" % scen, staged - whole[0], "USD", "funding.csv",
                "that staged sum less the whole-horizon round_size for %s" % scen)
    for r in frows:
        add("funding_%s_%s_round_size" % (r["scenario"], r["stage"]), float(r["round_size"]), "USD", "funding.csv",
            "round_size for scenario %s stage %s" % (r["scenario"], r["stage"]))
        add("funding_%s_%s_need_p80" % (r["scenario"], r["stage"]), float(r["need_p80"]), "USD", "funding.csv",
            "need_p80 for scenario %s stage %s" % (r["scenario"], r["stage"]))

if os.path.exists(os.path.join(OUT, "rescue_grid.csv")):
    rg = read_csv("rescue_grid.csv")
    for scope in sorted({r["scope"] for r in rg}):
        cells = [r for r in rg if r["scope"] == scope]
        clearing = [r for r in cells if float(r["terminal_cash_median"]) > 0]
        add("rescue_%s_cells_total" % scope, len(cells), "count", "rescue_grid.csv",
            "cells in the grid for scope %s" % scope)
        add("rescue_%s_cells_clearing" % scope, len(clearing), "count", "rescue_grid.csv",
            "cells whose terminal_cash_median is above zero for scope %s" % scope)
        add("rescue_%s_best_median" % scope, max(float(r["terminal_cash_median"]) for r in cells),
            "USD", "rescue_grid.csv", "highest terminal_cash_median in the grid for %s" % scope)
        add("rescue_%s_worst_median" % scope, min(float(r["terminal_cash_median"]) for r in cells),
            "USD", "rescue_grid.csv", "lowest terminal_cash_median in the grid for %s" % scope)
        if clearing:
            worst_cac = max(float(r["value1"]) for r in clearing)
            at = [r for r in clearing if float(r["value1"]) == worst_cac]
            add("rescue_%s_highest_cac_that_clears" % scope, worst_cac, "USD per acquisition",
                "rescue_grid.csv", "largest value1 among cells whose terminal_cash_median is above zero, for %s" % scope)
            add("rescue_%s_price_needed_at_that_cac" % scope, min(float(r["value2"]) for r in at),
                "GBP per month", "rescue_grid.csv",
                "smallest value2 that clears at that acquisition cost, for %s" % scope)
        for r in cells:
            add("rescue_%s_cac_q%s_price_q%s_median" % (scope, r["q1"], r["q2"]),
                float(r["terminal_cash_median"]), "USD", "rescue_grid.csv",
                "terminal_cash_median at cac_anchor_usd q%s and price_uk_tut_gbp q%s for %s"
                % (r["q1"], r["q2"], scope))
            add("rescue_%s_cac_q%s_value" % (scope, r["q1"]), float(r["value1"]),
                "USD per acquisition", "rescue_grid.csv", "the pinned acquisition anchor at q%s" % r["q1"])
            add("rescue_%s_price_q%s_value" % (scope, r["q2"]), float(r["value2"]),
                "GBP per month", "rescue_grid.csv", "the pinned tutoring-anchored price at q%s" % r["q2"])

if os.path.exists(os.path.join(OUT, "cohorts.csv")):
    for r in read_csv("cohorts.csv"):
        try:
            add(r["name"], float(r["value"]), r["unit"], "cohorts.csv", r["derivation"])
        except ValueError:
            add(r["name"], r["value"], r["unit"], "cohorts.csv", r["derivation"])

if os.path.exists(os.path.join(OUT, "offtest.csv")):
    otr = read_csv("offtest.csv")
    add("offtest_mechanism_count", len(otr), "count", "offtest.csv", "row count")
    add("offtest_all_exact", all(r["reproduces_base_exactly"] == "yes" for r in otr),
        "boolean", "offtest.csv", "every mechanism reproduces the base run exactly when switched off")

if os.path.exists(os.path.join(OUT, "omissions.csv")):
    orows = [r for r in read_csv("omissions.csv") if not r["absent_cost_line"].startswith("TOTAL")]
    add("omission_line_count", len(orows), "count", "omissions.csv",
        "rows naming an absent cost line, excluding the total row")
    add("omission_zero_line_count", len([r for r in orows if float(r["high_usd"]) == 0.0]),
        "count", "omissions.csv", "of those, the ones priced at zero")
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
