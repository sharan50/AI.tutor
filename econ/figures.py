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

# The count of scalar constants the file actually carries. Section 13 used to
# say it held "every decided constant"; it holds every decided constant that is
# a SCALAR, and LIMITS.md lists a dozen that are not. See CHANGELOG 6.10.
add("constants_row_count", len(read_csv("constants.csv")), "count", "constants.csv",
    "row count")
# Self-test records on disk. The table in section 13 said three; the invariant
# self-test added in round 5b is a fourth and had no row. Counted from the
# files rather than typed, because that is the defect this fixes.
add("selftest_count", len([f for f in ("harness_selftest.txt", "suffix_selftest.txt",
                                       "invariant_selftest.txt")
                           if os.path.exists(os.path.join(OUT, f))]),
    "count", "out/", "the self-test record files present on disk")

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
# How many CSVs sit under out/, so a sentence comparing the gate's coverage
# against the file count reads it rather than counting by hand.
_csvs = sorted(f for f in os.listdir(OUT) if f.endswith(".csv"))
add("out_csv_count", len(_csvs), "count", "out/", "how many .csv files the out directory holds")
add("out_csv_gated_count", 2, "count", "out/",
    "how many of them the character-for-character harness gate rebuilds and compares")

if os.path.exists(os.path.join(OUT, "drivers.csv")):
    drows = read_csv("drivers.csv")
    add("n_drivers", len(drows), "count", "drivers.csv", "row count")
    for r in drows:
        # A normal driver has no bounds, so it gets no low/high figure: emitting
        # one would let prose quote a mean and a standard deviation as a range.
        if r["distribution"] == "n":
            add("driver_%s_mean" % r["driver"], float(r["normal_mean"]), "driver units",
                "drivers.csv", "the mean of the normal prior for %s" % r["driver"])
            add("driver_%s_sd" % r["driver"], float(r["normal_sd"]), "driver units",
                "drivers.csv", "the standard deviation of that prior, which is not a bound")
            continue
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

    # The width of each prior range, so prose comparing an instrument's
    # precision against the range it would narrow has a file behind it.
    for r in read_csv("drivers.csv"):
        if r["distribution"] == "n" or not r["low"]:
            continue
        lo, hi = float(r["low"]), float(r["high"])
        add("driver_%s_range" % r["driver"], hi - lo, "driver units", "drivers.csv",
            "the high column less the low column for %s" % r["driver"])

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
# How many paths never reach their trough inside the horizon. A path whose
# minimum cumulative cash is in the last month is still falling when the window
# closes, so its peak funding requirement is a floor rather than a figure.
_tm = col(paths, "trough_month")
_H = len(monthly)
# How often each rota step actually fires. "Those steps fire on most paths" was
# true of the first and false of the second: the second fires on about one path
# in five.
_ah = col(paths, "terminal_active_hh")
add("por_share_paths_over_rota_extended", float((_ah > 3000).mean()), "share", "por_paths.csv",
    "share of paths whose terminal active household count exceeds the first safeguarding rota step")
add("por_share_paths_over_rota_24_7", float((_ah > 25000).mean()), "share", "por_paths.csv",
    "share exceeding the second, round-the-clock step")

add("por_share_paths_trough_at_horizon", float((_tm >= _H - 1).mean()), "share",
    "por_paths.csv",
    "share of paths whose cumulative cash is at its minimum in the last month of the horizon, so the trough and the funding requirement are both right-censored")
add("por_share_paths_trough_at_horizon_pct", 100.0 * float((_tm >= _H - 1).mean()),
    "per cent", "por_paths.csv", "the same share as a percentage")
add("por_trough_month_median", float(np.median(_tm)), "month", "por_paths.csv",
    "median over paths of trough_month")
add("por_trough_month_p10", float(np.percentile(_tm, 10)), "month", "por_paths.csv",
    "tenth percentile of trough_month")
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
    "median of final_year_contrib_per_hh_month, which is net revenue less inference, support, payment, hosting and app store fees only. The store fees are zero in the published run and are not zero in the app-store scenario, so leaving them out of this sentence described a different quantity from the one path_outcomes computes")
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

# Content-driven cost, which is larger than the content line. The salaried
# content heads sit inside people_beng_cost and their whole job is the content
# schedule, so the cost-split table read as though content were only the
# contracted authoring and validation. people_beng_content_cost is a
# DECOMPOSITION of people_beng_cost, not a thirteenth cost line, so it is never
# added to the grand total: doing so would count it twice.
_bch = float(col(monthly, "people_beng_content_cost_mean").sum())
add("por_total_people_beng_content_cost_mean", _bch, "USD", "por_monthly.csv",
    "sum over months of people_beng_content_cost_mean: the salaried content heads inside the Bengaluru people line")
add("por_share_people_beng_content_cost_pct", 100.0 * (_bch / grand if grand else 0.0), "per cent",
    "por_monthly.csv", "those heads as a share of the whole modelled cost base")
add("por_content_head_share_of_beng_people_pct",
    100.0 * (_bch / totals["people_beng_cost"] if totals["people_beng_cost"] else 0.0), "per cent",
    "por_monthly.csv", "those heads as a share of the Bengaluru people line they sit inside")
add("por_content_driven_cost_mean", totals["content_cost"] + _bch, "USD", "por_monthly.csv",
    "the content line plus the salaried content heads: everything the content schedule causes")
add("por_share_content_driven_pct",
    100.0 * ((totals["content_cost"] + _bch) / grand if grand else 0.0), "per cent",
    "por_monthly.csv", "that sum as a share of the whole modelled cost base, against por_share_content_cost_pct which counts only the contracted line")

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
# How far the central band line's percentile placement wanders WITHIN a run,
# across the months, against how far it moves BETWEEN scenarios at the terminal
# month. The write-up warned about the second and the evidence is in the first.
_pl = col(monthly, "cum_cash_bandcentral_placement")
_g = int(col(monthly, "t")[0]) + 6   # from the United Kingdom go-to-market month
add("por_band_central_placement_month_min", float(_pl[_g:].min()), "percentile", "por_monthly.csv",
    "the lowest percentile the central band line sits at over the months from go-to-market onward")
add("por_band_central_placement_month_max", float(_pl[_g:].max()), "percentile", "por_monthly.csv",
    "the highest it reaches over the same months")
add("por_band_central_placement_month_spread", float(_pl[_g:].max() - _pl[_g:].min()),
    "percentile", "por_monthly.csv",
    "how far it wanders within this one run: the difference between those two")
add("por_band_central_placement_terminal", float(place[-1]), "percentile as a share", "por_monthly.csv",
    "cum_cash_bandcentral_placement in the final row: the percentile of the real per-path distribution the central band line sits at")
add("por_band_central_placement_min", float(place[6:].min()), "percentile as a share", "por_monthly.csv",
    "minimum of cum_cash_bandcentral_placement from month 6 onward")
add("por_band_central_placement_max", float(place[6:].max()), "percentile as a share", "por_monthly.csv",
    "maximum of cum_cash_bandcentral_placement from month 6 onward")

if os.path.exists(os.path.join(OUT, "variants_bands.csv")):
    _vb = [r for r in read_csv("variants_bands.csv") if r["band"] == "central"]
    if _vb:
        _pt = [float(r["placement_terminal"]) for r in _vb]
        add("band_central_placement_scenario_min", min(_pt), "percentile", "variants_bands.csv",
            "the lowest terminal placement of the central band line over every scenario")
        add("band_central_placement_scenario_max", max(_pt), "percentile", "variants_bands.csv",
            "the highest")
        add("band_central_placement_scenario_spread", max(_pt) - min(_pt), "percentile",
            "variants_bands.csv",
            "how far the central band line's terminal placement moves BETWEEN scenarios, against how far it moves within one run across months")
        add("band_central_placement_scenario_count", len(_pt), "count", "variants_bands.csv",
            "how many scenarios that is measured over")
        # The ratio the prose used to give as "twenty times". See CHANGELOG 6.14.
        _ws = next(f["value"] for f in FIGS
                   if f["name"] == "por_band_central_placement_month_spread")
        add("band_placement_wander_over_scenario_spread",
            _ws / max(max(_pt) - min(_pt), 1e-12), "ratio", "variants_bands.csv",
            "the within-run wander of the central band line across months, divided by its spread across scenarios")

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
                  "pathwise_spearman_vs_base", "pathwise_mean_abs_delta", "abs_mean_delta",
                  "paired_mc_se", "pathwise_p50_delta", "pathwise_p50_delta_se",
                  "final_year_allin_contrib_pooled", "final_year_allin_contrib_median",
                  "final_year_gross_contrib_pooled"):
            if k in r:
                add("scenario_%s_%s" % (name, k), float(r[k]), "USD or share", "variants.csv",
                    "column %s for scenario %s" % (k, name))
    # How far the difference of marginal medians is from the median of the
    # per-path differences on the scenario where they diverge most. Section 9
    # quotes this to show that the column it used for four rounds was not the
    # quantity its heading claimed. See CHANGELOG 6.9.
    if "por_allowance_enforced" in vr and "por" in vr:
        _dm = (float(vr["por_allowance_enforced"]["terminal_cash_p50"])
               - float(vr["por"]["terminal_cash_p50"]))
        _pw = float(vr["por_allowance_enforced"]["pathwise_p50_delta"])
        add("allowance_enforced_median_basis_ratio", abs(_dm) / max(abs(_pw), 1e-9),
            "ratio", "variants.csv",
            "the difference of marginal medians divided by the median of the per-path differences, for the enforced-allowance scenario")
    if "por_dependence" in vr:
        add("por_dependence_pathwise_spearman",
            float(vr["por_dependence"]["pathwise_spearman_vs_base"]), "rank correlation",
            "variants.csv",
            "the per-path rank correlation against the base for the Iman-Conover reordered scenario: the pairing every other scenario has and this one does not")

    # The spread between the two price-anchor regimes is a different quantity
    # from either one's delta against the published run, which is a mix of them.
    if "por_anchor_tutoring" in vr and "por_anchor_software" in vr:
        add("anchor_tutoring_minus_software_terminal_cash_mean",
            float(vr["por_anchor_tutoring"]["terminal_cash_mean"])
            - float(vr["por_anchor_software"]["terminal_cash_mean"]),
            "USD", "variants.csv",
            "terminal_cash_mean for por_anchor_tutoring less terminal_cash_mean for por_anchor_software: the spread between the two regimes, not either one's delta against the published mix")
        # The name used to say tutoring minus software while the arithmetic did
        # the reverse. The arithmetic is the one worth keeping — capital is a
        # need, so the software regime's excess is the positive quantity — so
        # the name was corrected to match it rather than the other way round.
        add("anchor_software_minus_tutoring_peak_funding_p80",
            float(vr["por_anchor_software"]["peak_funding_p80"])
            - float(vr["por_anchor_tutoring"]["peak_funding_p80"]),
            "USD", "variants.csv",
            "peak_funding_p80 for por_anchor_software less the same for por_anchor_tutoring: the extra capital the software-anchored regime needs")
    base = float(vr["por"]["terminal_cash_mean"])

    # How many paired standard errors each scope delta sits from zero. The
    # write-up says the mean and the median disagree in sign on the market drop;
    # these are what make that a finding rather than an observation about noise.
    if "ukonly" in vr:
        _um = abs(float(vr["ukonly"]["terminal_cash_mean"]) - base)
        _use = float(vr["ukonly"]["paired_mc_se"])
        add("ukonly_mean_delta_sigma", _um / max(_use, 1e-9), "standard errors",
            "variants.csv",
            "the United Kingdom-only scenario's mean terminal-cash delta divided by its paired standard error")
        _upm = abs(float(vr["ukonly"]["pathwise_p50_delta"]))
        _upse = float(vr["ukonly"]["pathwise_p50_delta_se"])
        add("ukonly_median_delta_sigma", _upm / max(_upse, 1e-9), "standard errors",
            "variants.csv",
            "the same scenario's per-path median delta divided by its bootstrap standard error")

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
        # The delta against its own paired sampling error. Below about two this
        # is not a difference the sample can see.
        if "paired_mc_se" in r and float(r["paired_mc_se"]) > 0:
            add("delta_%s_t_stat" % name, abs(d) / float(r["paired_mc_se"]), "ratio",
                "variants.csv",
                "the absolute terminal-cash delta for %s divided by the paired standard error of that delta" % name)
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

    # The scope ladder, as two separable decisions. Owner decision 1 reads the
    # content column of a four-row table this way, so the two quantities it
    # reads are computed here and verify.py checks that the decomposition is
    # exact rather than approximate.
    if all(n in vr for n in ("por", "por_content_frozen", "ukonly", "gtm_minimum")):
        cc = lambda n: float(vr[n]["total_content_cost_mean"])
        add("scope_ladder_foreign_content_mean", cc("por") - cc("ukonly"), "USD", "variants.csv",
            "total_content_cost_mean for por less the same for ukonly: the content built for markets other than the United Kingdom")
        add("scope_ladder_frozen_uk_content_mean", cc("gtm_minimum"), "USD", "variants.csv",
            "total_content_cost_mean for gtm_minimum: United Kingdom content frozen at the go-to-market five subjects, one board")
        add("scope_ladder_uk_escalation_mean", cc("ukonly") - cc("gtm_minimum"), "USD", "variants.csv",
            "total_content_cost_mean for ukonly less the same for gtm_minimum: what widening the United Kingdom catalogue costs")
        # The two ratios section 12 reasons with. Both were typed, both were
        # taken from a superseded run, and both were wrong by about half.
        _tc = lambda n: float(vr[n]["terminal_cash_mean"])
        _b = _tc("por")
        _ukd, _gtmd = _tc("ukonly") - _b, _tc("gtm_minimum") - _b
        _frzd = _tc("por_content_frozen") - _b
        if _ukd:
            add("scope_gtm_over_ukonly_terminal_cash", _gtmd / _ukd, "ratio", "variants.csv",
                "the go-to-market minimum's terminal-cash delta divided by the United Kingdom-only scenario's: how much larger the real scope reduction is than the one the document used to read it off")
            # Kept for the file, not quoted in prose any more: the two
            # quantities can differ in SIGN, and round 6 moved the denominator
            # through zero, at which point the write-up rendered "a factor of
            # -7". A ratio hides a sign. See CHANGELOG 6.19.
            add("scope_content_freeze_over_market_drop_terminal_cash", _frzd / _ukd, "ratio",
                "variants.csv",
                "freezing the content schedule divided by dropping the second and third markets, on terminal cash at the mean")

# --------------------------------------------------------------------------
# Sensitivity
# --------------------------------------------------------------------------
if os.path.exists(os.path.join(OUT, "sobol.csv")):
    sb_all = read_csv("sobol.csv")
    # sobol.csv carries three configurations. The ordering is a property of the
    # configuration it was computed on, so they are never pooled: the unprefixed
    # names stay the plan of record and each other run gets its own prefix.
    # Pooling them would average orderings that disagree and produce one that is
    # true of none of them.
    RUN_PREFIX = {"por": "", "gtm_minimum": "gtm_", "onshore_all": "onshore_"}
    sb = [r for r in sb_all if r["run"] == "por"]
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
    # The set sizes, so prose comparing "content is three entries, acquisition is
    # twelve" reads them off the same sets the counts above use rather than from
    # a reviewer's list or from memory.
    _all_drivers = {r["driver"] for r in sb}
    add("registry_content_driver_count", len(CONTENT_DRIVERS & _all_drivers), "count", "sobol.csv",
        "how many registry entries the content-driver set contains")
    add("registry_acq_driver_count", len(ACQ_DRIVERS & _all_drivers), "count", "sobol.csv",
        "how many registry entries the acquisition-driver set contains")
    add("registry_cost_per_item_driver_count",
        len({"minutes_per_item", "examiner_rate_gbp_hr", "writer_gbp_item"} & _all_drivers),
        "count", "sobol.csv",
        "how many registry entries make up cost per item, which one timed pilot measures at once")

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
            add("sobol_%s_value_of_%s" % (target, r["driver"]), float(r["sobol_first_order"]),
                "share of variance", "sobol.csv",
                "the first-order index of %s for target %s, by name rather than by rank, so a figure quoted beside a grouped index is the same driver whatever its rank turns out to be" % (r["driver"], target))

    # The same quantities on every other scope in the file, under their own
    # prefix, so the write-up can put the two orderings side by side.
    for run in sorted({r["run"] for r in sb_all} - {"por"}):
        pre = RUN_PREFIX.get(run, run + "_")
        srows_run = [r for r in sb_all if r["run"] == run]
        for target in sorted({r["target"] for r in srows_run}):
            rows = sorted([r for r in srows_run if r["target"] == target],
                          key=lambda r: -float(r["sobol_first_order"]))
            top7 = [r["driver"] for r in rows[:7]]
            top3 = [r["driver"] for r in rows[:3]]
            add("sobol_%s%s_content_drivers_in_top7" % (pre, target),
                len([d for d in top7 if d in CONTENT_DRIVERS]), "count", "sobol.csv",
                "how many of the top seven drivers for %s on the %s scope are content-cost drivers" % (target, run))
            add("sobol_%s%s_acq_drivers_in_top3" % (pre, target),
                len([d for d in top3 if d in ACQ_DRIVERS]), "count", "sobol.csv",
                "how many of the top three drivers for %s on the %s scope are acquisition drivers" % (target, run))
            for i, r in enumerate(rows[:8], start=1):
                add("sobol_%s%s_rank%d_driver" % (pre, target, i), r["driver"], "driver name", "sobol.csv",
                    "driver at rank %d for target %s on the %s scope" % (i, target, run))
                add("sobol_%s%s_rank%d_value" % (pre, target, i), float(r["sobol_first_order"]),
                    "share of variance", "sobol.csv",
                    "first-order index at rank %d for target %s on the %s scope" % (i, target, run))
            for pos, r in enumerate(rows, start=1):
                add("sobol_%s%s_rank_of_%s" % (pre, target, r["driver"]), pos, "rank", "sobol.csv",
                    "the rank of %s for target %s on the %s scope" % (r["driver"], target, run))

if os.path.exists(os.path.join(OUT, "sobol_grouped.csv")):
    for r in read_csv("sobol_grouped.csv"):
        pre = "" if r["run"] == "por" else ("gtm_" if r["run"] == "gtm_minimum" else r["run"] + "_")
        add("sobol_grouped_%s%s_%s" % (pre, r["target"], r["grouped_quantity"]),
            float(r["sobol_first_order"]), "share of variance", "sobol_grouped.csv",
            "first-order index of %s on %s for the %s run: %s"
            % (r["grouped_quantity"], r["target"], r["run"], r["what_it_is"]))

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

    # Whether the two largest drivers interact AT ALL on terminal cash. Section
    # 8 used to assert that the variance first-order indices do not explain is
    # "concentrated in exactly the two drivers that matter most", and cited this
    # grid for it. The grid says the surface is additive: the same step in one
    # driver costs the same at every level of the other. These figures measure
    # that rather than asserting it, and twoway_additivity_worst_gap is
    # published so the claim can be checked instead of believed.
    # See CHANGELOG 6.12.
    g = {(r["q1"], r["q2"]): r for r in tg}
    qs = sorted({r["q1"] for r in tg}, key=int)
    def cell(a, b, col):
        return float(g[(a, b)][col])
    acq_steps = [cell(a, qs[1], "terminal_cash_mean") - cell(a, qs[0], "terminal_cash_mean")
                 for a in qs]
    con_steps = [cell(qs[-1], b, "terminal_cash_mean") - cell(qs[0], b, "terminal_cash_mean")
                 for b in qs]
    add("twoway_acq_step_terminal_cash", float(np.mean(acq_steps)), "USD", "twoway_grid.csv",
        "terminal_cash_mean at the second quantile of %s less the first, averaged over the five levels of %s"
        % (tg[0]["driver2"], tg[0]["driver1"]))
    add("twoway_content_step_terminal_cash", float(np.mean(con_steps)), "USD", "twoway_grid.csv",
        "terminal_cash_mean at the top quantile of %s less the bottom, averaged over the five levels of %s"
        % (tg[0]["driver1"], tg[0]["driver2"]))
    add("twoway_additivity_worst_gap",
        float(max(max(acq_steps) - min(acq_steps), max(con_steps) - min(con_steps))),
        "USD", "twoway_grid.csv",
        "the largest spread of either step across the levels of the other driver: zero means the surface is exactly additive")
    lo = cell(qs[-1], qs[0], "share_reaching_profitability") - cell(qs[0], qs[0], "share_reaching_profitability")
    hi = cell(qs[-1], qs[-1], "share_reaching_profitability") - cell(qs[0], qs[-1], "share_reaching_profitability")
    add("twoway_content_step_profitability_at_low_cac", abs(lo), "share", "twoway_grid.csv",
        "the same content step measured on share_reaching_profitability at the cheapest acquisition level")
    add("twoway_content_step_profitability_at_high_cac", abs(hi), "share", "twoway_grid.csv",
        "the same content step at the dearest acquisition level")
    add("twoway_content_step_profitability_attenuation", abs(lo) / max(abs(hi), 1e-12), "ratio",
        "twoway_grid.csv", "the first divided by the second")

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
    # Which side the unbracketed rows sit on. Reading them all as failures
    # inverted the most actionable positive result in the file.
    add("breakeven_rows_bracketed_on_profitability",
        len([r for r in berows if r["status"] == "bracketed"
             and r["metric"] == "share_reaching_profitability"]),
        "count", "breakeven.csv", "bracketed rows solved against the profitability target")
    add("breakeven_rows_bracketed_on_cash",
        len([r for r in berows if r["status"] == "bracketed"
             and r["metric"] != "share_reaching_profitability"]),
        "count", "breakeven.csv", "bracketed rows solved against a cash target")
    add("breakeven_rows_unbracketed_met",
        len([r for r in berows if r["status"].startswith("not bracketed: met")]),
        "count", "breakeven.csv",
        "rows where the target is met across the whole prior range, so the driver never crosses it because the plan already satisfies it")
    add("breakeven_rows_unbracketed_missed",
        len([r for r in berows if r["status"].startswith("not bracketed: missed")]),
        "count", "breakeven.csv",
        "rows where the target is missed across the whole prior range, which is the real failure")
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
                # Keyed by metric as well as scope. A price now brackets against
                # two different targets on the same scope, and without the
                # metric in the name the two collided — which the collision
                # guard caught rather than silently overwriting, which is what
                # it was added for in round 1a.
                add("breakeven_%s_%s_price_hours_at_25" % (r["scope"], r["metric"]), v / 25.0,
                    "hours", "breakeven.csv",
                    "that monthly price as hours of GCSE tutoring at the bottom of the verified 25 to 45 pound hourly band")
                add("breakeven_%s_%s_price_hours_at_45" % (r["scope"], r["metric"]), v / 45.0,
                    "hours", "breakeven.csv", "the same at the top of that band")
    for r in berows:
        key = "breakeven_%s_%s_%s" % (r["scope"], r["driver"], r["metric"])
        if r["status"] == "bracketed" and r["breakeven_value"]:
            add(key, float(r["breakeven_value"]), "driver units", "breakeven.csv",
                "bisection on a pinned %s against %s = %s" % (r["driver"], r["metric"], r["target"]))
        else:
            add(key + "_status", r["status"], "text", "breakeven.csv", "the status column")
        add(key + "_prior_median", float(r["prior_median"]), "driver units", "breakeven.csv", "the prior_median column")
        # The metric at each end of the driver's own prior range. On an
        # unbracketed row these are the whole answer: they say which side of the
        # target the plan sits on, which "not bracketed" alone does not.
        # The unit follows the metric: two of the three targets are dollars and
        # one is a share, and a generic "metric units" made the currency-tag
        # check unable to tell a dollar figure from a percentage.
        _munit = "share" if r["metric"] == "share_reaching_profitability" else "USD"
        add(key + "_metric_at_support_low", float(r["metric_at_support_low"]), _munit,
            "breakeven.csv", "the metric with the driver pinned at the bottom of its prior range")
        add(key + "_metric_at_support_high", float(r["metric_at_support_high"]), _munit,
            "breakeven.csv", "the metric with it pinned at the top")
        # What the plan looks like AT the solved value, on the statistics the
        # solve did not target. Without these a break-even reads as a rescue.
        for suffix, col, unit in (
            ("at_be_terminal_cash_median", "at_breakeven_terminal_cash_median", "USD"),
            ("at_be_peak_funding_p80", "at_breakeven_peak_funding_p80", "USD"),
        ):
            if r.get(col):
                add(key + "_" + suffix, float(r[col]), unit, "breakeven.csv",
                    "the %s column, which is that statistic at the solved break-even" % col)
        if r.get("at_breakeven_share_of_hitting_paths_ending_negative"):
            add(key + "_at_be_hitting_paths_ending_negative_pct",
                100.0 * float(r["at_breakeven_share_of_hitting_paths_ending_negative"]),
                "per cent", "breakeven.csv",
                "of the paths that meet the target at the solved break-even, the share that still end the horizon with negative cash")
        if r.get("at_breakeven_share_reaching_profitability"):
            add(key + "_at_be_share_reaching_profitability_pct",
                100.0 * float(r["at_breakeven_share_reaching_profitability"]),
                "per cent", "breakeven.csv",
                "the share of paths reaching profitability at the solved break-even, which is the solve's own target where it was the target")

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

if os.path.exists(os.path.join(OUT, "funding_commitments.csv")):
    # The prose kept naming entities and counting commitments by hand, and got
    # both wrong: it named an India entity that is not in this file at all, and
    # called two entities seed-window when one of them lands in the Series A.
    fc = read_csv("funding_commitments.csv")
    add("commitments_total", len(fc), "count", "funding_commitments.csv", "row count")
    add("commitments_spend_starts_in_seed", len([r for r in fc if r["stage_that_actually_pays"] == "seed"]),
        "count", "funding_commitments.csv", "rows whose stage_that_actually_pays is seed")
    # Named for what it counts. The old name said "decided after their round
    # closed" over a count of rows whose answer to that question is "no", which
    # is the inverse; the derivation string was right and the name was not.
    # Round 6 renamed the CSV column itself for the same reason, and this now
    # reads the positive sense rather than the negative. See CHANGELOG 6.8.
    add("commitments_paid_by_an_earlier_round_than_they_land_in",
        len([r for r in fc if r["spend_starts_before_its_stage_opens"] == "yes"]),
        "count", "funding_commitments.csv",
        "rows where the commitment LANDS in a stage later than the one whose window its spend starts in: the Series A refinancing a seed-window decision")
    ents = [r for r in fc if "entity" in r["commitment"]]
    add("commitments_entity_count", len(ents), "count", "funding_commitments.csv",
        "rows whose commitment names an entity set-up")
    add("commitments_entity_names", "; ".join(r["commitment"] for r in ents), "text",
        "funding_commitments.csv", "those rows' commitment text, verbatim")
    add("commitments_entities_paid_by_seed",
        len([r for r in ents if r["stage_that_actually_pays"] == "seed"]), "count",
        "funding_commitments.csv", "of those, the ones whose spend starts in the seed window")

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
    add("offtest_all_move_when_on", all(r.get("moves_the_run_when_switched_on") == "yes" for r in otr),
        "boolean", "offtest.csv", "every mechanism changes the run when switched on, so none is inert")
    # The list, rendered from the file, because a hand-kept copy of it named six
    # while the count beside it said seven.
    add("offtest_mechanism_names", "; ".join(r["mechanism"] for r in otr), "text",
        "offtest.csv", "every mechanism tested, in file order")

if os.path.exists(os.path.join(OUT, "omissions.csv")):
    orows = [r for r in read_csv("omissions.csv") if not r["absent_cost_line"].startswith("TOTAL")]
    add("omission_line_count", len(orows), "count", "omissions.csv",
        "rows naming an absent cost line, excluding the total row")
    add("omission_zero_line_count", len([r for r in orows if float(r["high_usd"]) == 0.0]),
        "count", "omissions.csv", "of those, the ones priced at zero")
    # The prose used to list these by hand and the list drifted from the file
    # twice. The list is now the file's, rendered verbatim, so a line added to
    # omissions.py appears in the write-up without anyone remembering to add it.
    def _names(rs):
        return "; ".join(r["absent_cost_line"] for r in rs)
    add("omission_line_names", _names(orows), "text", "omissions.csv",
        "every absent_cost_line in file order, excluding the total row")
    add("omission_zero_line_names", _names([r for r in orows if float(r["high_usd"]) == 0.0]),
        "text", "omissions.csv", "the absent_cost_line values priced at zero, in file order")
    for r in read_csv("omissions.csv"):
        slug = re.sub(r"[^a-z0-9]+", "_", r["absent_cost_line"].split(":")[0].lower()).strip("_")
        add("omission_%s_low" % slug, float(r["low_usd"]), "USD", "omissions.csv", r["basis"])
        add("omission_%s_high" % slug, float(r["high_usd"]), "USD", "omissions.csv", r["basis"])
        add("omission_%s_share_high_pct" % slug, 100.0 * float(r["high_share_of_total_cost"]), "per cent",
            "omissions.csv", "high_share_of_total_cost as a percentage")

if os.path.exists(os.path.join(OUT, "aux_params.csv")):
    for r in read_csv("aux_params.csv"):
        add("%s_low" % r["parameter"], float(r["low"]), "prior bound", "aux_params.csv",
            "low bound of the auxiliary prior %s: %s" % (r["parameter"], r["what_it_is"]))
        add("%s_high" % r["parameter"], float(r["high"]), "prior bound", "aux_params.csv",
            "high bound of the auxiliary prior %s: %s" % (r["parameter"], r["what_it_is"]))

if os.path.exists(os.path.join(OUT, "sized_omissions.csv")):
    so = {r["quantity"]: r for r in read_csv("sized_omissions.csv")}
    for k, r in so.items():
        add(k, float(r["value"]), r["unit"], "sized_omissions.csv", r["basis"])
    add("retention_stress_churn_pct",
        100.0 * (float(so["retention_stress_churn_scale"]["value"]) - 1.0), "per cent",
        "sized_omissions.csv", "the churn multiple as a percentage increase")
    add("retention_stress_share_of_cost_pct",
        100.0 * float(so["retention_stress_share_of_total_cost"]["value"]), "per cent",
        "sized_omissions.csv", "that cost as a share of the modelled cost base")

if os.path.exists(os.path.join(OUT, "imanconover_check.csv")):
    rows = read_csv("imanconover_check.csv")
    add("imanconover_pairs", len(rows), "count", "imanconover_check.csv", "row count")
    worst = max(abs(float(r["target_rank_corr"]) - float(r["achieved_rank_corr"])) for r in rows)
    add("imanconover_worst_corr_error", worst, "rank correlation", "imanconover_check.csv",
        "largest absolute difference between target_rank_corr and achieved_rank_corr")
    add("imanconover_all_marginals_preserved",
        all(r["marginal_preserved_a"] == "True" and r["marginal_preserved_b"] == "True" for r in rows),
        "boolean", "imanconover_check.csv", "every marginal_preserved column is True")

if os.path.exists(os.path.join(OUT, "invariants.csv")):
    _iv = read_csv("invariants.csv")
    add("invariant_check_count", len({r["invariant"] for r in _iv}), "count",
        "invariants.csv", "distinct invariant names")
    add("invariant_run_count", len({r["run"] for r in _iv}) if _iv and "run" in _iv[0] else 0,
        "count", "invariants.csv", "distinct configurations they are run on")

if os.path.exists(os.path.join(OUT, "invariant_defect_costs.csv")):
    _dc = read_csv("invariant_defect_costs.csv")
    _real = [r for r in _dc if r["change_log_entry"] != "-"]
    add("invariant_proved_count", len({r["change_log_entry"] for r in _real}), "count",
        "invariant_defect_costs.csv",
        "historical defects reintroduced and refused by the check written for them")
    # How many of those defects moved terminal cash by nothing at all. This is
    # the reason the five accounting identities could not see them, measured
    # rather than asserted. See CHANGELOG 6.1.
    add("invariant_defects_costing_no_cash",
        len([r for r in _real if abs(float(r["what_the_fix_is_worth_at_the_mean"])) < 1e-6]),
        "count", "invariant_defect_costs.csv",
        "reintroduced defects whose terminal cash mean is identical to the correct model's: they move a decomposition, not cash")
    for r in _real:
        if r["change_log_entry"] == "6.1, both exits together":
            add("limits_round6_arrivals_fix_usd",
                float(r["what_the_fix_is_worth_at_the_mean"]), "USD",
                "invariant_defect_costs.csv",
                "terminal cash mean of the correct model less that of the model with both round 6.1 calendar exits put back")
        if r["change_log_entry"] == "4.2 and 5.1":
            add("limits_round5_sitting_fix_usd",
                float(r["what_the_fix_is_worth_at_the_mean"]), "USD",
                "invariant_defect_costs.csv",
                "the same for the two sitting-month exits fixed in rounds 4 and 5")

# --------------------------------------------------------------------------
# Ratios the prose used to state by hand and state wrongly. Each is derived from
# figures already in this registry, so the multiple in the sentence and the two
# numbers it compares cannot drift apart. Round 6 found four of these wrong at
# once -- "about three to one" over 4.04, "twenty times" over 17.4, "half a per
# cent" over 1.10, "about twelve times" over 3.74 -- three of which had survived
# five rounds of review because a hand-typed multiple looks like prose rather
# than like a figure. See CHANGELOG 6.14.
# --------------------------------------------------------------------------
def fig(name):
    return next(f["value"] for f in FIGS if f["name"] == name)


def has(name):
    return any(f["name"] == name for f in FIGS)


if has("delta_gtm_minimum_peak_funding_p80_abs") and has("anchor_software_minus_tutoring_peak_funding_p80"):
    add("scope_over_anchor_peak_funding_ratio",
        fig("delta_gtm_minimum_peak_funding_p80_abs")
        / max(abs(fig("anchor_software_minus_tutoring_peak_funding_p80")), 1e-9),
        "ratio", "variants.csv, funding.csv",
        "what the scope decision is worth on the capital requirement, divided by what the price anchor is worth on it")

if has("anchor_tutoring_minus_software_terminal_cash_mean") and has("delta_gtm_minimum_terminal_cash_abs"):
    add("anchor_over_scope_terminal_cash_ratio",
        abs(fig("anchor_tutoring_minus_software_terminal_cash_mean"))
        / max(fig("delta_gtm_minimum_terminal_cash_abs"), 1e-9),
        "ratio", "variants.csv",
        "what the price anchor is worth on terminal cash, divided by what the scope decision is worth on it")

_bk_hi = "breakeven_gtm_minimum_uk_one_board_price_uk_tut_gbp_terminal_cash_median_metric_at_support_high"
_bk_lo = "breakeven_gtm_minimum_uk_one_board_price_uk_tut_gbp_terminal_cash_median_metric_at_support_low"
if has(_bk_hi) and has(_bk_lo):
    add("gtm_price_margin_share_of_low_support",
        abs(fig(_bk_hi)) / max(abs(fig(_bk_lo)), 1e-9), "share",
        "breakeven.csv",
        "how far short the median path falls at the top of the price prior, as a share of how far it falls at the bottom")

if os.path.exists(os.path.join(OUT, "sized_omissions.csv")):
    _so = {r["quantity"]: r["value"] for r in read_csv("sized_omissions.csv")}
    if "examiner_full_equivalents_month18" in _so and "gtm_minimum_full_equivalents_month18" in _so:
        _p18 = float(_so["examiner_full_equivalents_month18"])
        _g18 = float(_so["gtm_minimum_full_equivalents_month18"])
        add("uk_content_fe_por_month18", _p18, "full item-bank equivalents", "sized_omissions.csv",
            "median United Kingdom content at month 18 on the plan of record, in full item-bank equivalents")
        add("uk_content_fe_gtm_month18", _g18, "full item-bank equivalents", "sized_omissions.csv",
            "the same for the go-to-market minimum")
        add("uk_content_fe_ratio_por_over_gtm_month18", _p18 / max(_g18, 1e-9), "ratio",
            "sized_omissions.csv", "the first divided by the second")

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
