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
fy_contrib = OUTC["final_year_contrib_per_hh_month"]
fy_allin = OUTC["final_year_allin_contrib_per_hh_month"]
fy_cac = OUTC["final_year_effective_cac"]
blended_months = float((DRV["seg_mix_exam"] * exam_months + DRV["seg_mix_alevel"] * al_months
                        + np.maximum(1 - DRV["seg_mix_exam"] - DRV["seg_mix_alevel"], 0) * pre_months).mean())
ltv_gross = fy_contrib * blended_months
add("final_year_contrib_per_hh_month_gross_mean", float(fy_contrib.mean()), "USD per household month",
    "net revenue less inference, support, payment and hosting only: a gross margin, not a net one", "16")
add("final_year_contrib_per_hh_month_allin_mean", float(fy_allin.mean()), "USD per household month",
    "net cash per active household month with acquisition and verification added back, so net of engineering, content, overhead, compliance and payment fees", "16")
add("allin_minus_gross_contrib_per_hh_month", float(fy_allin.mean() - fy_contrib.mean()), "USD per household month",
    "the all-in figure less the gross one: what the gross margin leaves out", "16")
add("blended_retained_months_mean", blended_months, "months",
    "retained months weighted by the sampled segment mix", "14")
add("final_year_ltv_gross_mean", float(ltv_gross.mean()), "USD per household",
    "gross contribution per household month times blended retained months", "14")
add("final_year_effective_cac_mean", float(fy_cac.mean()), "USD per acquisition",
    "final twelve months of acquisition and verification spend divided by final twelve months of acquisitions", "14")
add("final_year_ltv_over_cac_mean", float(ltv_gross.mean() / fy_cac.mean()), "ratio",
    "mean gross lifetime value divided by mean final-year effective cost per acquisition", "14")
add("share_paths_final_year_ltv_below_cac", float((ltv_gross < fy_cac).mean()), "share",
    "share of paths on which gross lifetime value is below the final-year effective cost per acquisition", "14 and 19")

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
