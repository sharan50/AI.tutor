"""
cohorts.py

The measurements the monthly file does not carry, each one answering a specific
item on the review checklist. Runs on the harness.

  - retained months per acquisition, by segment, run as two counterfactuals with
    the segment mix pinned, so the Year 10 against Year 11 ratio the code
    actually produces is published rather than the round one in the prose
  - the persistence of the demand shock, so that "no sustained bad run" can be
    answered with a number
  - every averaged conclusion re-stated as the share of individual paths for
    which it is false
  - lifetime value against cost per acquisition in the final year
  - gross contribution per household month beside the all-in figure
  - the night rota that is missing from the cost base, priced

Output: out/cohorts.csv
"""

import csv
import os

import numpy as np

import harness

NS = harness.load()
OUT, SEED, RUN_DATE = NS["OUT"], NS["SEED"], NS["RUN_DATE"]
DRV = NS["_verified"]["drv"]
OUTC = NS["_verified"]["outcomes"]
MOUT = NS["_verified"]["out"]
P = DRV["anchor_u"].shape[0]
T = NS["HORIZON"]

ROWS = []


def add(name, value, unit, derivation, checklist_item):
    ROWS.append([SEED, RUN_DATE, name, ("%.6f" % value) if isinstance(value, float) else value,
                 unit, derivation, checklist_item])


# ---------------------------------------------------------------------------
# Retained months per acquisition, by segment. Two counterfactual runs with the
# segment mix pinned after the draws, so both share the base random numbers.
# ---------------------------------------------------------------------------
def retained_months(mix_exam, mix_alevel):
    drv = dict(DRV)
    drv["seg_mix_exam"] = np.full(P, mix_exam)
    drv["seg_mix_alevel"] = np.full(P, mix_alevel)
    out, _ = NS["run"](drv, NS["base_config"]())
    acq = out["acquisitions"].sum(axis=1)
    months = out["active_hh"].sum(axis=1)
    return np.where(acq > 0, months / np.maximum(acq, 1e-9), 0.0), out


exam_months, exam_out = retained_months(1.0, 0.0)
pre_months, pre_out = retained_months(0.0, 0.0)
al_months, al_out = retained_months(0.0, 1.0)

add("retained_months_exam_year_mean", float(exam_months.mean()), "months per acquisition",
    "every acquisition pinned into the examination-year segment; active households summed over months divided by acquisitions summed over months", "15")
add("retained_months_pre_exam_mean", float(pre_months.mean()), "months per acquisition",
    "every acquisition pinned into the pre-examination-year segment, same arithmetic", "15")
add("retained_months_alevel_mean", float(al_months.mean()), "months per acquisition",
    "every acquisition pinned into the A-level segment, same arithmetic", "15")
ratio = float(pre_months.mean() / exam_months.mean())
add("year10_to_year11_retained_months_ratio", ratio, "ratio",
    "pre-examination-year retained months divided by examination-year retained months, as the code produces it", "15")
add("year10_to_year11_ratio_p10", float(np.percentile(pre_months, 10) / np.percentile(exam_months, 10)), "ratio",
    "the same ratio at the tenth percentile of each", "15")
add("year10_to_year11_ratio_p90", float(np.percentile(pre_months, 90) / np.percentile(exam_months, 90)), "ratio",
    "the same ratio at the ninetieth percentile of each", "15")
share_double = float((pre_months >= 2.0 * exam_months).mean())
add("share_paths_year10_at_least_doubles", share_double, "share",
    "share of paths on which the pre-examination cohort retains at least twice as many months as the examination cohort", "15 and 19")

# ---------------------------------------------------------------------------
# Demand shock persistence. Independent monthly shocks would mean no sustained
# bad run, which is the failure mode that ends companies.
# ---------------------------------------------------------------------------
state = np.zeros(P)
mult = np.zeros((P, T))
var = DRV["shock_sd"] ** 2 / np.maximum(1.0 - DRV["shock_rho"] ** 2, 1e-3)
for t in range(T):
    state = DRV["shock_rho"] * state + DRV["shock_sd"] * DRV["_shock_eps"][:, t]
    mult[:, t] = np.exp(state - 0.5 * var)

bad = mult < 0.80
longest = np.zeros(P, dtype=int)
current = np.zeros(P, dtype=int)
for t in range(T):
    current = np.where(bad[:, t], current + 1, 0)
    longest = np.maximum(longest, current)
add("shock_longest_bad_run_mean", float(longest.mean()), "months",
    "longest run of consecutive months with the demand multiplier below 0.80, reconstructed from shock_rho, shock_sd and the published innovations", "18")
add("shock_longest_bad_run_p90", float(np.percentile(longest, 90)), "months", "the ninetieth percentile of that run length", "18")
add("shock_share_paths_bad_run_6plus", float((longest >= 6).mean()), "share",
    "share of paths with at least six consecutive months of demand at or below 0.80", "18")
add("shock_share_paths_bad_run_12plus", float((longest >= 12).mean()), "share",
    "share of paths with at least twelve consecutive such months", "18")
add("shock_rho_median", float(np.median(DRV["shock_rho"])), "AR(1) coefficient", "median of the shock_rho driver column", "18")

# ---------------------------------------------------------------------------
# Averaged conclusions, re-stated per path.
# ---------------------------------------------------------------------------
content = OUTC["total_content_cost"]
cac = OUTC["total_cac_spend"]
people = OUTC["total_people_cost"]
add("share_paths_content_exceeds_acquisition", float((content > cac).mean()), "share",
    "share of paths on which total content cost exceeds total acquisition and verification spend", "19")
add("share_paths_content_is_largest_line", float(((content > cac) & (content > people)).mean()), "share",
    "share of paths on which content is larger than both acquisition and people", "19")
add("share_paths_peak_funding_over_10m", float((OUTC["peak_funding_requirement"] > 1e7).mean()), "share",
    "share of paths whose peak funding requirement exceeds ten million dollars", "19 and 20")
add("share_paths_terminal_cash_positive", float((OUTC["terminal_cash"] > 0).mean()), "share",
    "share of paths ending the horizon with cumulative cash above zero", "19")

# ---------------------------------------------------------------------------
# Lifetime value against cost per acquisition, in the final year.
# ---------------------------------------------------------------------------
# Contribution per household month is a RATIO whose denominator goes to zero on
# paths whose book has collapsed, so the mean of the per-path ratio is not a
# number: a handful of paths with almost no final-year household-months carry it
# to millions. It is therefore reported two defensible ways instead, and the
# mean is not published at all.
#
#   pooled  total contribution over total household-months, summed across every
#           path and every month of the final year. The right figure for "what
#           does a household month contribute".
#   median  the middle path's own ratio, over paths that actually have a final
#           year to speak of.
FY = slice(NS["HORIZON"] - 12, NS["HORIZON"])
hh_months = float(MOUT["active_hh"][:, FY].sum())
contrib_pooled_total = float((MOUT["net_rev_consumer"][:, FY] + MOUT["net_rev_schools"][:, FY]
                              - MOUT["inference_cost"][:, FY] - MOUT["support_cost"][:, FY]
                              - MOUT["payment_cost"][:, FY] - MOUT["hosting_cost"][:, FY]
                              - MOUT["appstore_fee"][:, FY]).sum())
allin_pooled_total = float((MOUT["net_cash"][:, FY] + MOUT["cac_spend"][:, FY]
                            + MOUT["verif_cost"][:, FY]).sum())
gross_pooled = contrib_pooled_total / hh_months
allin_pooled = allin_pooled_total / hh_months

fy_hh_months_path = MOUT["active_hh"][:, FY].sum(axis=1)
REAL = fy_hh_months_path >= 12.0        # at least one household for the final year
fy_contrib = OUTC["final_year_contrib_per_hh_month"]
fy_allin = OUTC["final_year_allin_contrib_per_hh_month"]
fy_cac = OUTC["final_year_effective_cac"]

add("final_year_hh_months_total", hh_months, "household months",
    "active households summed over paths and over the final twelve months", "16")
add("share_paths_with_a_real_final_year", float(REAL.mean()), "share",
    "share of paths with at least twelve final-year household months, which is the set the per-path medians below are taken over", "16 and 17")
add("final_year_contrib_per_hh_month_gross_pooled", gross_pooled, "USD per household month",
    "total net revenue less inference, support, payment, hosting and app store fees over the final year, divided by total final-year household months: a gross margin, not a net one", "16")
add("final_year_contrib_per_hh_month_gross_median", float(np.median(fy_contrib[REAL])), "USD per household month",
    "median over paths with a real final year of the per-path gross contribution ratio", "16")
add("final_year_contrib_per_hh_month_allin_pooled", allin_pooled, "USD per household month",
    "total net cash with acquisition and verification added back over the final year, divided by total final-year household months: net of engineering, content, overhead and compliance", "16")
add("final_year_contrib_per_hh_month_allin_median", float(np.median(fy_allin[REAL])), "USD per household month",
    "median over paths with a real final year of the per-path all-in contribution ratio", "16")
add("allin_minus_gross_contrib_per_hh_month_pooled", allin_pooled - gross_pooled, "USD per household month",
    "the pooled all-in figure less the pooled gross one: what the gross margin leaves out", "16")

blended_months = float((DRV["seg_mix_exam"] * exam_months + DRV["seg_mix_alevel"] * al_months
                        + np.maximum(1 - DRV["seg_mix_exam"] - DRV["seg_mix_alevel"], 0) * pre_months).mean())
add("blended_retained_months_mean", blended_months, "months",
    "retained months weighted by the sampled segment mix", "14")

cac_pooled = float((MOUT["cac_spend"][:, FY].sum() + MOUT["verif_cost"][:, FY].sum())
                   / max(MOUT["acquisitions"][:, FY].sum(), 1e-9))
ltv_pooled = gross_pooled * blended_months
add("final_year_ltv_gross_pooled", ltv_pooled, "USD per household",
    "pooled gross contribution per household month times blended retained months", "14")
add("final_year_effective_cac_pooled", cac_pooled, "USD per acquisition",
    "total final-year acquisition and verification spend over total final-year acquisitions, pooled across paths", "14")
add("final_year_effective_cac_median", float(np.median(fy_cac[REAL])), "USD per acquisition",
    "median over paths with a real final year of the per-path effective acquisition cost", "14")
add("final_year_ltv_over_cac_pooled", ltv_pooled / cac_pooled, "ratio",
    "pooled gross lifetime value divided by pooled final-year effective cost per acquisition", "14")
add("final_year_cac_pooled_over_anchor_median", cac_pooled / float(np.median(DRV["cac_anchor_usd"])), "ratio",
    "pooled final-year effective acquisition cost divided by the median low-volume anchor: what the anchor understates by at the spend actually modelled", "12 and 13")
add("cac_anchor_median", float(np.median(DRV["cac_anchor_usd"])), "USD per acquisition",
    "median of the cac_anchor_usd driver column, which is the low-volume anchor and not a cost at scale", "12")
ltv_path = fy_contrib * blended_months
add("share_paths_final_year_ltv_below_cac", float((ltv_path[REAL] < fy_cac[REAL]).mean()), "share",
    "share of paths with a real final year on which gross lifetime value is below the final-year effective cost per acquisition", "14 and 19")

# ---------------------------------------------------------------------------
# The night rota that is not in the cost base. Priced rather than waved at.
# UK study time is roughly 16:00 to 21:00, which is 21:30 to 02:30 in Bengaluru.
# ---------------------------------------------------------------------------
NIGHT_FTE = 3.0
NIGHT_PREMIUM = 1.30
HOURS_PER_FTE_YEAR = 2000.0
rota_yr = NIGHT_FTE * float(np.median(DRV["eng_usd_yr"])) * float(np.median(DRV["overhead_mult"])) * NIGHT_PREMIUM
months_live = NS["HORIZON"] - NS["CONSUMER_OPEN"][NS["M_UK"]]
rota_total = rota_yr * months_live / 12.0
total_cost = float(sum(MOUT[c].sum(axis=1).mean() for c in
                       ["inference_cost", "support_cost", "payment_cost", "hosting_cost", "verif_cost",
                        "cac_spend", "content_cost", "people_beng_cost", "people_uk_cost", "step_cost",
                        "school_onboard_cost", "appstore_fee"]))
add("missing_night_rota_cost_per_year", rota_yr, "USD per year",
    "three full-time posts at the median Bengaluru salary and overhead multiplier, with a thirty per cent night premium", "5 and 8")
add("missing_night_rota_cost_total", rota_total, "USD",
    "that annual cost from the UK go-to-market month to the end of the horizon", "5 and 8")
add("missing_night_rota_share_of_total_cost", rota_total / total_cost, "share",
    "the missing rota divided by the total modelled cost", "5 and 8")
add("por_total_cost_recomputed", total_cost, "USD",
    "sum over paths and months of every modelled cost line, averaged over paths", "5")

if __name__ == "__main__":
    path = os.path.join(OUT, "cohorts.csv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "name", "value", "unit", "derivation", "checklist_item"])
        w.writerows(ROWS)
    print("wrote", path, len(ROWS), "rows")
    for r in ROWS:
        print("  %-48s %s" % (r[2], r[3]))
