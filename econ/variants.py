"""
variants.py

Structural probes and scenario variants. Runs on the harness, so it runs the
published model.

Two rules hold for everything in this file, and are tested rather than asserted:

  1. A variant that changes the mechanism must reproduce the base run EXACTLY
     when the new mechanism is switched off. test_off_reproduces_base() checks
     this on the written CSV text, not on in-memory floats.
  2. Every new parameter is drawn OUTSIDE the published random stream, from the
     auxiliary seeds in model.py, so the two runs stay comparable path by path
     rather than only in aggregate.

Outputs: out/variants.csv, out/variants_bands.csv, out/imanconover_check.csv
"""

import csv
import os

import numpy as np
from scipy import stats

import harness

NS = harness.load()
OUT, SEED, RUN_DATE = NS["OUT"], NS["SEED"], NS["RUN_DATE"]
DRV = NS["_verified"]["drv"]
P = DRV["anchor_u"].shape[0]
T = NS["HORIZON"]


# ---------------------------------------------------------------------------
# Iman-Conover: impose a target rank correlation by reordering, which preserves
# every marginal exactly. Nothing about the distributions changes; only which
# path gets which value.
# ---------------------------------------------------------------------------
def iman_conover(cols, target_corr, rng):
    n, k = cols.shape
    scores = stats.norm.ppf(np.arange(1, n + 1) / (n + 1.0))
    R = np.column_stack([rng.permutation(scores) for _ in range(k)])
    Tm = np.corrcoef(R, rowvar=False)
    Pm = np.linalg.cholesky(target_corr)
    Qm = np.linalg.cholesky(Tm)
    S = Pm @ np.linalg.inv(Qm)
    Rstar = R @ S.T
    out = np.empty_like(cols)
    for j in range(k):
        sorted_col = np.sort(cols[:, j])
        order = np.argsort(np.argsort(Rstar[:, j], kind="stable"), kind="stable")
        out[:, j] = sorted_col[order]
    return out


# Dependence imposed between drivers. Every one of these is a prior about how
# the world hangs together, not a measurement, and each is stated so it can be
# argued with.
DEPENDENCE = [
    ("price_uk_tut_gbp", "churn_base", 0.35,
     "a higher price is harder to hold on to"),
    ("cac_anchor_usd", "pool_uk", -0.40,
     "a larger reachable pool is a cheaper one to find people in"),
    ("minutes_per_item", "examiner_rate_gbp_hr", -0.30,
     "the slower examiners are the cheaper ones per hour"),
    ("price_in_mtok_usd", "price_out_mtok_usd", 0.80,
     "vendor input and output prices move together"),
    ("turns_per_session", "sessions_mean", -0.25,
     "longer sessions substitute for more of them"),
    ("churn_base", "summer_lapse_pre", 0.40,
     "a book that churns in term churns harder over the summer"),
    ("cac_anchor_usd", "creator_share", -0.30,
     "where paid acquisition is dear, creator channels carry more of the load"),
    ("eng_usd_yr", "uk_gbp_yr", 0.50,
     "one labour market, two currencies"),
    ("items_per_unit", "minutes_per_item", 0.25,
     "a bigger bank is a bank of harder items"),
    ("sat_kappa", "cac_ref_spend_usd", -0.35,
     "a channel that saturates fast saturates at a smaller spend"),
]


def dependence_matrix(names):
    idx = {n: i for i, n in enumerate(names)}
    C = np.eye(len(names))
    for a, b, r, _why in DEPENDENCE:
        C[idx[a], idx[b]] = C[idx[b], idx[a]] = r
    # Nearest positive definite by eigenvalue clipping, if the stated set is not
    # internally consistent. Reported if it fires.
    w, v = np.linalg.eigh(C)
    if w.min() < 1e-8:
        w = np.clip(w, 1e-8, None)
        C = v @ np.diag(w) @ v.T
        d = np.sqrt(np.diag(C))
        C = C / np.outer(d, d)
        print("dependence matrix was not positive definite; repaired by eigenvalue clipping")
    return C


def apply_dependence(drv):
    rng = np.random.default_rng(NS["SEED_AUX_DEPENDENCE"])
    names = sorted({n for a, b, _r, _w in DEPENDENCE for n in (a, b)})
    cols = np.column_stack([drv[n] for n in names])
    C = dependence_matrix(names)
    new = iman_conover(cols, C, rng)
    out = dict(drv)
    for j, n in enumerate(names):
        out[n] = new[:, j]
    return out, names, C


# ---------------------------------------------------------------------------
# Feedback loops the base model does not have. Each lever is then reported net
# of its own penalty rather than gross.
# ---------------------------------------------------------------------------
def feedback_params(drv, cfg, on=True):
    if not on:
        return None
    rng = np.random.default_rng(NS["SEED_AUX_FEEDBACK"])
    price_elast = rng.uniform(0.20, 1.40, P)
    quality_gamma = rng.uniform(0.0, 0.80, P)
    autom_beta = rng.uniform(0.0, 8.0, P)

    # Does a higher price cost retention? Referenced to the midpoint of the
    # tutoring-anchored band, so a software-anchored path is not penalised.
    price_now = NS["gross_price_usd"](drv, NS["M_UK"], 0)
    ref = np.median(price_now)
    churn_price_mult = (np.maximum(price_now, 1e-6) / ref) ** price_elast

    # Does expanding faster cost quality, and does that cost retention? Build
    # intensity is content built this month per content head, normalised.
    plan, live = NS["content_build_plan"](drv, cfg)
    build = np.column_stack(plan)                       # (P, T)
    intensity = build / np.maximum(drv["units_per_content_head"], 1e-6)[:, None]
    scale = np.percentile(intensity[intensity > 0], 90) if np.any(intensity > 0) else 1.0
    lag = np.zeros_like(intensity)
    lag[:, 3:] = intensity[:, :-3]                      # quality damage shows up later
    churn_quality_mult = 1.0 + quality_gamma[:, None] * np.clip(lag / max(scale, 1e-9), 0.0, 3.0)

    # Does a higher automation ceiling cost engineering? Fewer support minutes
    # per household is more automation, and it is bought with heads.
    lo, hi = 0.4, 6.0
    autom = np.clip((hi - drv["support_min_hh_month"]) / (hi - lo), 0.0, 1.0)
    eng_heads_extra = autom_beta * autom

    return dict(churn_price_mult=churn_price_mult,
                churn_quality_mult=churn_quality_mult,
                eng_heads_extra=eng_heads_extra,
                support_mult=np.ones(P))


def feedback_off():
    """The identity feedback. Must reproduce the base run exactly."""
    return dict(churn_price_mult=np.ones(P),
                churn_quality_mult=np.ones((P, T)),
                eng_heads_extra=np.zeros(P),
                support_mult=np.ones(P))


# ---------------------------------------------------------------------------
# Scenarios
# ---------------------------------------------------------------------------
def sampled_fx():
    rng = np.random.default_rng(NS["SEED_AUX_FX"])
    # A random walk on GBP/USD with a sampled terminal dispersion. Fixed FX is
    # the owner's instruction; this exists to price what that instruction costs.
    sd = rng.uniform(0.04, 0.16, P)
    z = rng.standard_normal(P)
    return dict(gbp=NS["FX_GBP_USD"] * np.exp(sd * z - 0.5 * sd ** 2))


def appstore_params():
    rng = np.random.default_rng(NS["SEED_AUX_APPSTORE"])
    return dict(share=rng.uniform(0.15, 0.70, P), fee=np.full(P, 0.15))


SCENARIOS = {}


def scenario(name, note):
    def deco(fn):
        SCENARIOS[name] = (fn, note)
        return fn
    return deco


@scenario("por", "the plan of record, as published")
def s_por():
    return DRV, NS["base_config"]()


@scenario("por_feedback_off", "the feedback machinery present but switched off; must equal por exactly")
def s_fb_off():
    return DRV, dict(NS["base_config"](), feedback=feedback_off())


@scenario("por_feedback_on", "price costs retention, expansion pace costs quality, automation costs engineering")
def s_fb_on():
    cfg = NS["base_config"]()
    return DRV, dict(cfg, feedback=feedback_params(DRV, cfg, on=True))


@scenario("por_dependence", "Iman-Conover dependence between drivers, every marginal preserved exactly")
def s_dep():
    drv, _names, _C = apply_dependence(DRV)
    return drv, NS["base_config"]()


@scenario("por_dependence_feedback", "dependence and feedback together")
def s_dep_fb():
    drv, _n, _C = apply_dependence(DRV)
    cfg = NS["base_config"]()
    return drv, dict(cfg, feedback=feedback_params(drv, cfg, on=True))


@scenario("por_fx_sampled", "the fixed rate replaced by a sampled one, to price what fixing it hides")
def s_fx():
    return DRV, dict(NS["base_config"](), fx=sampled_fx())


@scenario("por_india_d2c", "India opened direct to parents rather than through institutions")
def s_india():
    return DRV, dict(NS["base_config"](), india_d2c=True)


@scenario("por_appstore", "a share of consumer billing routed through an app store at 15 per cent")
def s_app():
    return DRV, dict(NS["base_config"](), appstore=appstore_params())


@scenario("por_allowance_enforced", "the session allowance enforced rather than sold and overshot")
def s_enf():
    return DRV, dict(NS["base_config"](), enforce_allowance=True)


@scenario("ukonly", "UK consumer only: no second market, no institution channel, and charged accordingly")
def s_uk():
    return DRV, dict(NS["base_config"](), scope="ukonly", schools=False)


@scenario("por_no_schools", "the plan of record without the institution channel, everything else identical")
def s_nosch():
    return DRV, dict(NS["base_config"](), schools=False)


def creator_params():
    rng = np.random.default_rng(NS["SEED_AUX_CREATOR"])
    return dict(fee_per_creator_yr=rng.uniform(2000.0, 40000.0, P),
                rev_share=rng.uniform(0.0, 0.15, P))


@scenario("por_creator_fees", "signed creators want money: a fixed annual minimum each, plus a share of the revenue their audience brought")
def s_creator():
    return DRV, dict(NS["base_config"](), creator=creator_params())


@scenario("por_anchor_tutoring", "condition C1 passes: every path anchors on the tutoring rate")
def s_anchor_tut():
    drv = dict(DRV)
    drv["anchor_u"] = np.zeros(P)
    return drv, NS["base_config"]()


@scenario("por_anchor_software", "condition C1 fails: every path anchors on software prices")
def s_anchor_sw():
    drv = dict(DRV)
    drv["anchor_u"] = np.ones(P)
    return drv, NS["base_config"]()


@scenario("por_launch_plus3", "go-to-market three months later, landing outside the September intake")
def s_l3():
    return DRV, dict(NS["base_config"](), launch_shift=3)


@scenario("por_launch_plus6", "go-to-market six months later")
def s_l6():
    return DRV, dict(NS["base_config"](), launch_shift=6)


OUTCOME_COLS = [
    "terminal_cash_mean", "terminal_cash_p50", "peak_funding_mean", "peak_funding_p50",
    "peak_funding_p90", "share_reaching_profitability", "median_month_rev_passes_cost",
    "terminal_active_hh_mean", "final_year_effective_cac_mean",
    "final_year_contrib_per_hh_month_mean", "mean_share_over_allowance",
    "total_tax_collected_mean", "min_of_mean_trough", "mean_of_min_trough",
    "understatement_ratio", "band_central_placement_terminal",
]


def evaluate(name):
    fn, note = SCENARIOS[name]
    drv, cfg = fn()
    out, _ = NS["run"](drv, cfg)
    o, cum = NS["path_outcomes"](out)
    ts = NS["trough_stats"](cum)
    placement = NS["band_percentile_placement"](cum, cum, "central")
    reach = o["month_rev_passes_cost"] >= 0
    vals = dict(
        terminal_cash_mean=float(o["terminal_cash"].mean()),
        terminal_cash_p50=float(np.median(o["terminal_cash"])),
        peak_funding_mean=float(o["peak_funding_requirement"].mean()),
        peak_funding_p50=float(np.percentile(o["peak_funding_requirement"], 50)),
        peak_funding_p90=float(np.percentile(o["peak_funding_requirement"], 90)),
        share_reaching_profitability=float(reach.mean()),
        median_month_rev_passes_cost=float(np.median(o["month_rev_passes_cost"][reach])) if reach.any() else float("nan"),
        terminal_active_hh_mean=float(o["terminal_active_hh"].mean()),
        final_year_effective_cac_mean=float(o["final_year_effective_cac"].mean()),
        final_year_contrib_per_hh_month_mean=float(o["final_year_contrib_per_hh_month"].mean()),
        mean_share_over_allowance=float(o["mean_share_over_allowance"].mean()),
        total_tax_collected_mean=float(o["total_tax_collected"].mean()),
        min_of_mean_trough=ts["min_of_mean"],
        mean_of_min_trough=ts["mean_of_min"],
        understatement_ratio=ts["understatement_ratio"],
        band_central_placement_terminal=float(placement[-1]),
    )
    return note, vals, out, o, cum, placement


def test_off_reproduces_base():
    """A mechanism switched off must reproduce the base run character for character."""
    base_out, _ = NS["run"](DRV, NS["base_config"]())
    base_o, base_cum = NS["path_outcomes"](base_out)
    base_text = NS["monthly_csv_text"](base_out, base_cum, "por")
    results = []
    for name, cfg in [
        ("feedback", dict(NS["base_config"](), feedback=feedback_off())),
        ("appstore_zero", dict(NS["base_config"](), appstore=dict(share=np.zeros(P), fee=np.zeros(P)))),
        ("fx_fixed", dict(NS["base_config"](), fx=dict(gbp=np.full(P, NS["FX_GBP_USD"])))),
        ("creator_zero", dict(NS["base_config"](),
                              creator=dict(fee_per_creator_yr=np.zeros(P), rev_share=np.zeros(P)))),
    ]:
        out, _ = NS["run"](DRV, cfg)
        o, cum = NS["path_outcomes"](out)
        text = NS["monthly_csv_text"](out, cum, "por")
        ok = (text == base_text)
        results.append((name, ok))
        print("  switched-off reproduction, %-14s %s" % (name, "EXACT" if ok else "DIFFERS"))
        if not ok:
            raise AssertionError("variant %s does not reproduce the base run when switched off" % name)
    return results


def main():
    print("checking that each mechanism reproduces the base run when switched off")
    test_off_reproduces_base()

    rows, band_rows = [], []
    for name in SCENARIOS:
        note, vals, out, o, cum, placement = evaluate(name)
        rows.append([SEED, RUN_DATE, name, note] + ["%.6f" % vals[c] for c in OUTCOME_COLS])
        for band in ("low", "central", "high"):
            pl = NS["band_percentile_placement"](cum, cum, band)
            line = NS["band_line"](cum, cum, band)
            band_rows.append([SEED, RUN_DATE, name, band,
                              "%.6f" % float(line[-1]), "%.6f" % float(pl[-1]),
                              "%.6f" % float(pl[NS["HORIZON"] // 2]), "%.6f" % float(np.mean(pl[6:]))])
        print("  %-26s terminal_cash_mean %s" % (name, format(vals["terminal_cash_mean"], ",.0f")))

    with open(os.path.join(OUT, "variants.csv"), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "scenario", "note"] + OUTCOME_COLS)
        w.writerows(rows)
    with open(os.path.join(OUT, "variants_bands.csv"), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "scenario", "band", "terminal_band_line",
                    "placement_terminal", "placement_mid", "placement_mean_from_m6"])
        w.writerows(band_rows)

    drv2, names, C = apply_dependence(DRV)
    with open(os.path.join(OUT, "imanconover_check.csv"), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "driver_a", "driver_b", "target_rank_corr",
                    "achieved_rank_corr", "marginal_preserved_a", "marginal_preserved_b", "rationale"])
        for a, b, r, why in DEPENDENCE:
            ach = stats.spearmanr(drv2[a], drv2[b]).statistic
            pa = bool(np.array_equal(np.sort(drv2[a]), np.sort(DRV[a])))
            pb = bool(np.array_equal(np.sort(drv2[b]), np.sort(DRV[b])))
            w.writerow([SEED, RUN_DATE, a, b, "%.4f" % r, "%.4f" % ach, pa, pb, why])
    print("wrote variants.csv, variants_bands.csv, imanconover_check.csv")


if __name__ == "__main__":
    main()
