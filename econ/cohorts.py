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

# WHY the ratio is what it is rather than two. These counterfactuals pin the
# drivers one at a time, after the draws, and re-run. The lifts they imply are
# now computed below rather than read off by eye: the write-up concluded from
# these three numbers that in-term churn was the larger lever, which is the
# opposite of what differencing them says.
def retained_ratio(**pins):
    drv = dict(DRV)
    for k, v in pins.items():
        drv[k] = np.full(P, v)
    outs = []
    for mix_e, mix_a in ((1.0, 0.0), (0.0, 0.0)):
        d2 = dict(drv)
        d2["seg_mix_exam"] = np.full(P, mix_e)
        d2["seg_mix_alevel"] = np.full(P, mix_a)
        o, sm = NS["run"](d2, NS["base_config"]())
        acq = o["acquisitions"].sum(axis=1)
        outs.append(np.where(acq > 0, o["active_hh"].sum(axis=1) / np.maximum(acq, 1e-9), 0.0).mean())
    return float(outs[1] / outs[0]), float(outs[0]), float(outs[1])

_r_nosummer, _e1, _p1 = retained_ratio(summer_lapse_pre=0.0, progress_continue=1.0)
_r_lowchurn, _e2, _p2 = retained_ratio(churn_base=float(NS["DRIVERS"][
    [d[0] for d in NS["DRIVERS"]].index("churn_base")][2][0]))
_r_both, _e3, _p3 = retained_ratio(
    summer_lapse_pre=0.0, progress_continue=1.0,
    churn_base=float(NS["DRIVERS"][[d[0] for d in NS["DRIVERS"]].index("churn_base")][2][0]))
add("year10_ratio_with_no_summer_at_all", _r_nosummer, "ratio",
    "the pre-to-examination retained-month ratio with the summer lapse pinned to zero and progression pinned to one: the summer removed entirely", "15")
add("year10_ratio_with_churn_at_its_floor", _r_lowchurn, "ratio",
    "the same ratio with in-term churn pinned to the bottom of its prior range and the summer left as sampled", "15")
# WHICH of the two levers is larger. The write-up asserted in-term churn and
# never differenced the two counterfactuals against the base. It is the summer,
# by a wide margin. See CHANGELOG 4.14.
add("year10_ratio_lift_from_removing_summer", _r_nosummer - ratio, "ratio points",
    "the Year 10 ratio with the summer removed entirely, less the ratio as sampled", "15 and 19")
add("year10_ratio_lift_from_flooring_churn", _r_lowchurn - ratio, "ratio points",
    "the Year 10 ratio with in-term churn at its floor, less the ratio as sampled", "15 and 19")
add("year10_summer_lever_over_churn_lever",
    (_r_nosummer - ratio) / max(_r_lowchurn - ratio, 1e-9), "ratio",
    "the summer lever divided by the in-term churn lever: which of docs/10's two questions is the larger one", "15 and 19")
add("year10_ratio_with_no_summer_and_floor_churn", _r_both, "ratio",
    "the same ratio with both pinned. An earlier version of this string called it the only combination that recovers the figure docs/10 reasons toward. It does not recover it: nothing in the prior ranges does, and saying otherwise was the same error the write-up made", "15")
add("retained_months_exam_at_floor_churn", _e2, "months per acquisition",
    "examination-year retained months with in-term churn at the bottom of its prior range", "15")
add("retained_months_pre_at_floor_churn", _p2, "months per acquisition",
    "pre-examination retained months with in-term churn at the bottom of its prior range", "15")

# ---------------------------------------------------------------------------
# Demand shock persistence. Independent monthly shocks would mean no sustained
# bad run, which is the failure mode that ends companies.
# ---------------------------------------------------------------------------
# Read from the published per-path column rather than reconstructed from the
# innovations. The innovations are not written to any file, so a figure claiming
# to be reconstructed from them was not checkable by a reader.
longest = OUTC["longest_demand_shock_bad_run"]
add("shock_longest_bad_run_mean", float(longest.mean()), "months",
    "mean of longest_demand_shock_bad_run, a published column of por_paths.csv: the longest run of consecutive months with the demand multiplier below SHOCK_BAD_THRESHOLD", "18")
add("shock_longest_bad_run_p90", float(np.percentile(longest, 90)), "months", "the ninetieth percentile of longest_demand_shock_bad_run in por_paths.csv", "18")
add("shock_share_paths_bad_run_6plus", float((longest >= 6).mean()), "share",
    "share of por_paths.csv rows whose longest_demand_shock_bad_run is six or more", "18")
add("shock_share_paths_bad_run_12plus", float((longest >= 12).mean()), "share",
    "share of por_paths.csv rows whose longest_demand_shock_bad_run is twelve or more", "18")
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

fy_hh_months_path = OUTC["final_year_hh_months"]   # a published column of por_paths.csv
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
# The same quantity signed so that prose can say "lower by" without a double
# negative, and the median path's all-in figure as an amount consumed.
add("gross_minus_allin_contrib_per_hh_month_pooled", gross_pooled - allin_pooled, "USD per household month",
    "the pooled gross figure less the pooled all-in one: how much lower the all-in figure is", "16")
add("allin_consumed_per_hh_month_median", -float(np.median(fy_allin[REAL])), "USD per household month",
    "the median path's all-in contribution with the sign reversed: what a household month consumes on the median path", "16")

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

# Per-path retention, not the sample mean. blended_months above is a SCALAR
# averaged over every path, and multiplying a per-path contribution by it
# produced a hybrid that was then published as the per-path restatement
# checklist item 19 demands. Retention varies strongly across paths and
# correlates with churn_base, so the hybrid was not close: it roughly doubled
# the share. See CHANGELOG 4.7.
months_path = MOUT["active_hh"].sum(axis=1) / np.maximum(MOUT["acquisitions"].sum(axis=1), 1e-9)
add("retained_months_per_path_mean", float(months_path.mean()), "months",
    "per-path realised retained months: active household months over acquisitions, path by path", "19")
add("retained_months_per_path_p10", float(np.percentile(months_path, 10)), "months",
    "tenth percentile of that per-path figure", "19")
add("retained_months_per_path_p90", float(np.percentile(months_path, 90)), "months",
    "ninetieth percentile of that per-path figure", "19")

ltv_path = fy_contrib * months_path
add("share_paths_final_year_ltv_below_cac", float((ltv_path[REAL] < fy_cac[REAL]).mean()), "share",
    "share of paths with a real final year on which gross lifetime value, computed on THAT PATH's realised retained months, is below the final-year effective cost per acquisition", "14 and 19")
add("share_paths_final_year_ltv_below_cac_scalar_months",
    float(((fy_contrib * blended_months)[REAL] < fy_cac[REAL]).mean()), "share",
    "the same share computed the way it used to be, with the sample-mean retained months applied to every path, published so the size of that error is on the record rather than only in the change log", "19")

# The same share on the all-in basis. Checklist item 16 is about a gross margin
# presented as a net one, and publishing only the gross share commits the very
# error the item names: the gross share is small and reads as reassurance, and
# the all-in share is the one that decides whether a household pays for the
# business that serves it. Both are published, on the same paths, and the
# write-up quotes the second whenever it quotes the first.
ltv_path_allin = fy_allin * months_path
add("share_paths_final_year_ltv_allin_below_cac",
    float((ltv_path_allin[REAL] < fy_cac[REAL]).mean()), "share",
    "share of paths with a real final year on which ALL-IN lifetime value, which carries the demand-independent cost base, is below the final-year effective cost per acquisition", "14, 16 and 19")
add("share_paths_final_year_ltv_allin_below_cac_pct",
    100.0 * float((ltv_path_allin[REAL] < fy_cac[REAL]).mean()), "per cent",
    "the same share as a percentage", "14, 16 and 19")
add("share_paths_final_year_ltv_below_cac_pct",
    100.0 * float((ltv_path[REAL] < fy_cac[REAL]).mean()), "per cent",
    "the gross share as a percentage, published beside the all-in one so the two are never quoted apart", "14, 16 and 19")

# ---------------------------------------------------------------------------
# What the demand shock is actually worth. Checklist item 18 published the run
# lengths, which are a property of the demand series, and never the cost, which
# is a property of the answer. One paired run settles it.
# ---------------------------------------------------------------------------
def _pin_run(**pins):
    drv = dict(DRV)
    for k, v in pins.items():
        drv[k] = np.full(P, v)
    o, sm = NS["run"](drv, NS["base_config"]())
    oc, cum = NS["path_outcomes"](o, sm)
    return oc


_noshock = _pin_run(shock_sd=0.0)
add("shock_cost_terminal_cash_mean",
    float(OUTC["terminal_cash"].mean() - _noshock["terminal_cash"].mean()), "USD",
    "terminal cash mean with the demand shock as sampled, less the same with shock_sd pinned to zero: what the whole persistent-shock apparatus is worth", "18")
add("shock_cost_terminal_cash_median",
    float(np.median(OUTC["terminal_cash"]) - np.median(_noshock["terminal_cash"])), "USD",
    "the same on the median path", "18")
add("shock_cost_peak_funding_p80",
    float(np.percentile(OUTC["peak_funding_requirement"], 80)
          - np.percentile(_noshock["peak_funding_requirement"], 80)), "USD",
    "the same on the eightieth-percentile peak funding requirement", "18")
_worst = longest >= 12
if _worst.any():
    add("shock_cost_on_worst_affected_mean",
        float(OUTC["terminal_cash"][_worst].mean() - _noshock["terminal_cash"][_worst].mean()), "USD",
        "the same terminal-cash difference, over only the paths with a run of twelve or more bad months", "18")
    add("shock_cost_on_worst_affected_median",
        float(np.median(OUTC["terminal_cash"][_worst]) - np.median(_noshock["terminal_cash"][_worst])), "USD",
        "the median of that difference over the same worst-affected paths", "18")

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

# ---------------------------------------------------------------------------
# Five quantities a round-four adversarial review showed the document was
# asserting without a number behind it. Each is cheap to compute from the
# published outputs and each corrects or qualifies a claim in the write-up.
# ---------------------------------------------------------------------------

# 0. What the acquisition budget cap believes about retention, against what the
#    model delivers. Two documents claimed this file published both numbers
#    before it did; round 4's coherence pass caught that. It does now.
_ch = np.clip(DRV["churn_base"], 1e-3, 0.95)
_keep_first = (1.0 - DRV["churn_m1_extra"]) * (1.0 - _ch)
_num = np.zeros(P); _den = np.zeros(P)
for _t in range(NS["HORIZON"]):
    _to_sit = float((NS["EXAM_CAL_MONTH"][NS["M_UK"]] - NS["cal_month"](_t)) % 12)
    _m_exam = np.minimum(1.0 / _ch, _to_sit)
    _m_pre = (np.minimum(1.0 / _ch, _to_sit + 10.0)
              + (1.0 - DRV["summer_lapse_pre"]) * DRV["progress_continue"] * _m_exam)
    _m_al = np.minimum(1.0 / _ch, _to_sit + 12.0)
    _mix_e, _mix_a = DRV["seg_mix_exam"], DRV["seg_mix_alevel"]
    _mix_p = np.maximum(1.0 - _mix_e - _mix_a, 0.0)
    _w = MOUT["acquisitions"][:, _t]
    _num += _w * _keep_first * (_mix_e * _m_exam + _mix_p * _m_pre + _mix_a * _m_al)
    _den += _w
_assumed = float((_num / np.maximum(_den, 1e-9)).mean())
_realised = float((MOUT["active_hh"].sum(axis=1)
                   / np.maximum(MOUT["acquisitions"].sum(axis=1), 1e-9)).mean())
add("ltv_cap_assumed_months", _assumed, "months",
    "the retained months ltv_estimate assumes, weighted by the acquisitions actually made in each month and using the United Kingdom examination calendar: what the only restraint on acquisition spend believes", "14")
add("ltv_cap_realised_months", _realised, "months",
    "the retained months the model delivers over the same run, right-censored by the horizon", "14")
add("ltv_cap_months_overstatement", _assumed / max(_realised, 1e-9), "ratio",
    "the first divided by the second. The budget cap inverts the saturation curve, so permitted spend scales as roughly the square of this", "14")

# 0b. The one unbounded prior in the registry. price_drift_yr is normal, not
#     uniform, so it has no low or high and out/drivers.csv used to print its
#     mean and standard deviation under a low/high header. These are the
#     quantities a reader actually wants from it.
_pd = DRV["price_drift_yr"]
add("price_drift_share_paths_negative", float((_pd < 0).mean()), "share",
    "share of paths on which real price drift is negative: the prior is normal and unbounded, so prices fall on this share of paths", "the instrument")
add("price_drift_multiplier_at_horizon_p05", float(np.percentile((1.0 + _pd) ** 5.0, 5)), "multiple",
    "the cumulative real price multiplier at month 60 at the fifth percentile of paths", "the instrument")
add("price_drift_multiplier_at_horizon_p95", float(np.percentile((1.0 + _pd) ** 5.0, 95)), "multiple",
    "the same at the ninety-fifth percentile", "the instrument")

# 1. Monte Carlo error. "A figure re-derived from a different seed is a
#    different number" was stated and never sized. It is one line from the
#    paths file, and it turns out one tabulated scenario is indistinguishable
#    from zero at this sample size.
tc = OUTC["terminal_cash"]
mc_se = float(tc.std(ddof=1) / np.sqrt(tc.shape[0]))
add("por_terminal_cash_mc_se", mc_se, "USD",
    "standard error of the mean of terminal_cash across paths: the sampling error on the headline level at this seed and this path count", "the instrument")
add("por_terminal_cash_mc_se_two_sigma", 2.0 * mc_se, "USD",
    "twice that, which is the interval a figure quoted to the dollar actually carries", "the instrument")

# 2. Discounting. There is none anywhere in the model: terminal cash, peak
#    funding, every break-even and the residual are all undiscounted nominal
#    sums over sixty months. Content spend is front- and mid-loaded against
#    revenue that arrives late, so this is not neutral. Computed post hoc from
#    the monthly net cash line, which is exact.
net_month = MOUT["net_cash"]
months = np.arange(net_month.shape[1])
for rate in (0.0, 0.12, 0.25):
    disc = (1.0 + rate) ** (-(months / 12.0))
    npv = float((net_month * disc[None, :]).sum(axis=1).mean())
    tag = "%02d" % int(round(rate * 100))
    add("por_terminal_cash_npv_%s" % tag, npv, "USD",
        "mean over paths of net cash discounted monthly at %d per cent a year: the model discounts nothing, and this is what that is worth" % int(round(rate * 100)),
        "the instrument")
    add("por_npv_%s_less_undiscounted" % tag, npv - float(tc.mean()), "USD",
        "that present value less the undiscounted terminal cash mean", "the instrument")
    # Which way discounting cuts is not obvious and the write-up asserted it
    # before it was computed. It cuts BOTH ways: the nominal loss shrinks,
    # because the largest negative months are the late ones, while the economics
    # look worse, because revenue is later than cost. Both are published.
    _cl = ["inference_cost", "support_cost", "payment_cost", "hosting_cost", "verif_cost",
           "cac_spend", "content_cost", "people_beng_cost", "people_uk_cost", "step_cost",
           "school_onboard_cost", "appstore_fee"]
    d_tot = float(sum((MOUT[c].mean(axis=0) * disc).sum() for c in _cl))
    d_rev = float(((MOUT["net_rev_consumer"] + MOUT["net_rev_schools"]).mean(axis=0) * disc).sum())
    for line in ("content_cost", "cac_spend"):
        add("por_discounted_%s_share_%s_pct" % (line, tag),
            100.0 * float((MOUT[line].mean(axis=0) * disc).sum()) / d_tot, "per cent",
            "%s as a share of discounted total cost at %d per cent a year" % (line, int(round(rate * 100))),
            "the instrument")
    add("por_discounted_cost_over_revenue_%s" % tag, d_tot / max(d_rev, 1e-9), "ratio",
        "discounted total cost over discounted net revenue at %d per cent a year" % int(round(rate * 100)),
        "the instrument")

# 3. Variable cost against PRICE, which is the quantity docs/10's load-bearing
#    row is about. The write-up answered it with inference over TOTAL COST, a
#    denominator dominated by the content build, which is a different question.
gross_rev = MOUT["gross_rev_consumer"].sum(axis=1)
var_lines = ["inference_cost", "support_cost", "payment_cost", "hosting_cost"]
inf_tot = MOUT["inference_cost"].sum(axis=1)
var_tot = sum(MOUT[c].sum(axis=1) for c in var_lines)
LIVE = gross_rev > 0
add("por_inference_over_gross_revenue_pooled", float(inf_tot.sum() / gross_rev.sum()), "share",
    "total inference cost over total gross consumer revenue, pooled across paths: docs/10's row is variable cost against PRICE, not against total cost", "19")
add("por_inference_over_gross_revenue_median", float(np.median((inf_tot[LIVE] / gross_rev[LIVE]))), "share",
    "the same ratio on the median path", "19")
add("por_variable_over_gross_revenue_median", float(np.median((var_tot[LIVE] / gross_rev[LIVE]))), "share",
    "all four variable cost lines over gross consumer revenue, on the median path", "19")
add("por_variable_over_gross_revenue_p90", float(np.percentile((var_tot[LIVE] / gross_rev[LIVE]), 90)), "share",
    "the same at the ninetieth percentile of paths", "19")
add("share_paths_variable_cost_over_half_of_revenue",
    float((var_tot[LIVE] / gross_rev[LIVE] > 0.50).mean()), "share",
    "share of live paths on which variable cost exceeds half of gross consumer revenue, which is where docs/10 says its sensitivity row reverses", "19")
add("share_paths_variable_cost_over_revenue",
    float((var_tot[LIVE] / gross_rev[LIVE] > 1.00).mean()), "share",
    "share of live paths on which variable cost exceeds gross consumer revenue outright", "19")

# 4. When the demand-independent block is actually spent. "Committed before
#    demand can say much about it" was read as a statement about timing and it
#    is not one: it is a statement about the model having no rule that stops
#    building.
BLOCK = ["content_cost", "people_beng_cost", "people_uk_cost", "step_cost"]
blk = sum(MOUT[c] for c in BLOCK)
blk_total = float(blk.sum(axis=1).mean())
gtm = NS["CONSUMER_OPEN"][NS["M_UK"]]
for lo, hi, label in ((0, 18, "0_18"), (18, 36, "18_36"), (36, 60, "36_60"), (24, 60, "24_60")):
    v = float(blk[:, lo:hi].sum(axis=1).mean())
    add("demand_independent_spent_months_%s" % label, v, "USD",
        "the demand-independent block spent in months %d to %d" % (lo, hi), "the instrument")
    add("demand_independent_share_months_%s" % label, v / blk_total, "share",
        "that as a share of the whole block", "the instrument")
add("demand_independent_share_after_gtm",
    float(blk[:, gtm:].sum(axis=1).mean()) / blk_total, "share",
    "the share of the demand-independent block spent AFTER the United Kingdom go-to-market month", "the instrument")

if __name__ == "__main__":
    path = os.path.join(OUT, "cohorts.csv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "name", "value", "unit", "derivation", "checklist_item"])
        w.writerows(ROWS)
    print("wrote", path, len(ROWS), "rows")
    for r in ROWS:
        print("  %-48s %s" % (r[2], r[3]))
