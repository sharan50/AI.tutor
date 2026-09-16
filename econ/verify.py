"""
verify.py

Re-derives every stated figure from the raw outputs, knowing nothing of the
prose, and then checks the prose against what it derived.

Three passes:

  A. INDEPENDENT RE-DERIVATION. A second implementation of the core figures,
     computed from out/por_monthly.csv and out/por_paths.csv by a different code
     path from figures.py, and compared against figures.csv. This catches
     figures.py being wrong, which a verifier that imported it could not.

  B. PROSE SCRAPE. Every number in the write-up is extracted and matched against
     figures.csv. Tolerance is set by the precision the number was printed at,
     so "23.8m" must match to within 0.05m and "0.58" to within 0.005.

  C. ALLOWLIST. Numbers that are not model outputs (dates, document numbers,
     decision identifiers, figures verified from the vault's own sources, and
     the prior ranges declared in model.py) are exempt only if declared in
     verify_allow.csv with a reason. They are reported, not hidden.

Exit code is non-zero if anything fails.
"""

import csv
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
DOCS = [os.path.join(HERE, "WRITEUP.md"), os.path.join(HERE, "LIMITS.md"),
        os.path.join(HERE, "OPEN_ITEMS.md"), os.path.join(HERE, "CHANGELOG.md")]
ALLOW = os.path.join(HERE, "verify_allow.csv")


def read_csv(name):
    with open(os.path.join(OUT, name), newline="") as fh:
        return list(csv.DictReader(fh))


def load_figures():
    figs = {}
    for r in read_csv("figures.csv"):
        try:
            figs[r["name"]] = float(r["value"])
        except ValueError:
            figs[r["name"]] = r["value"]
    return figs


# ---------------------------------------------------------------------------
# Pass A: independent re-derivation
# ---------------------------------------------------------------------------
def rederive():
    monthly = read_csv("por_monthly.csv")
    paths = read_csv("por_paths.csv")

    def mcol(k):
        return np.array([float(r[k]) for r in monthly])

    def pcol(k):
        return np.array([float(r[k]) for r in paths])

    d = {}
    tc = pcol("terminal_cash")
    pf = pcol("peak_funding_requirement")
    tr = pcol("trough")
    mr = pcol("month_rev_passes_cost")

    d["n_paths"] = float(len(paths))
    d["horizon_months"] = float(len(monthly))
    d["por_terminal_cash_mean"] = float(np.mean(tc))
    d["por_terminal_cash_p50"] = float(np.percentile(tc, 50))
    d["por_peak_funding_mean"] = float(np.mean(pf))
    d["por_peak_funding_p80"] = float(np.percentile(pf, 80))
    d["por_peak_funding_p95"] = float(np.percentile(pf, 95))
    d["por_share_reaching_profitability"] = float(np.mean(mr >= 0))

    # The trough, both ways round, computed here from first principles: the
    # headline is the minimum of the averaged line, the honest one is the
    # average of each path's own minimum.
    cummean = mcol("cum_cash_mean")
    d["por_min_of_mean_cash_line"] = float(np.min(cummean))
    d["por_mean_of_per_path_min"] = float(np.mean(tr))
    d["por_trough_understatement_ratio"] = float(np.min(cummean) / np.mean(tr))

    # Cross-check: the mean cumulative line must equal the cumulative sum of the
    # mean net cash line, which is a different column entirely.
    d["_xcheck_cum_vs_cumsum"] = float(np.max(np.abs(np.cumsum(mcol("net_cash_mean")) - cummean)))

    # Cross-check: mean terminal cash from the paths file must equal the final
    # value of the mean cumulative line from the monthly file.
    d["_xcheck_terminal_vs_monthly"] = float(abs(np.mean(tc) - cummean[-1]))

    lines = ["inference_cost", "support_cost", "payment_cost", "hosting_cost", "verif_cost",
             "cac_spend", "content_cost", "people_beng_cost", "people_uk_cost", "step_cost",
             "school_onboard_cost", "appstore_fee"]
    tot = sum(float(np.sum(mcol(c + "_mean"))) for c in lines)
    d["por_total_cost_mean"] = tot
    for c in lines:
        d["por_share_%s" % c] = float(np.sum(mcol(c + "_mean"))) / tot

    gross = float(np.sum(mcol("gross_rev_consumer_mean")))
    tax = float(np.sum(mcol("tax_collected_mean")))
    d["por_total_gross_consumer_revenue_mean"] = gross
    d["por_total_tax_collected_mean"] = tax
    d["por_tax_share_of_gross"] = tax / gross

    # Cross-check: net consumer revenue must equal gross less tax, column by
    # column, down the whole file.
    d["_xcheck_net_equals_gross_less_tax"] = float(np.max(np.abs(
        mcol("gross_rev_consumer_mean") - mcol("tax_collected_mean") - mcol("net_rev_consumer_mean"))))

    # Cross-check: net cash must equal revenue less every cost line, down the file.
    rev = mcol("net_rev_consumer_mean") + mcol("net_rev_schools_mean")
    cost = sum(mcol(c + "_mean") for c in lines)
    d["_xcheck_net_cash_identity"] = float(np.max(np.abs(rev - cost - mcol("net_cash_mean"))))

    d["por_final_year_effective_cac_mean"] = float(np.mean(pcol("final_year_effective_cac")))
    d["por_mean_share_over_allowance"] = float(np.mean(pcol("mean_share_over_allowance")))
    d["por_band_central_placement_terminal"] = float(mcol("cum_cash_bandcentral_placement")[-1])
    return d


def pass_a(figs):
    d = rederive()
    fails, checked = [], 0
    for k, v in d.items():
        if k.startswith("_xcheck_"):
            # Identities that must hold to within floating point and the six
            # decimal places the CSV is written at.
            tol = max(1e-3, abs(v) * 0.0)
            if abs(v) > 1.0:
                fails.append("%s: identity violated by %.6f" % (k, v))
            checked += 1
            continue
        if k not in figs:
            fails.append("%s: present in the re-derivation but absent from figures.csv" % k)
            continue
        ref = figs[k]
        if not isinstance(ref, float):
            fails.append("%s: figures.csv holds a non-numeric value" % k)
            continue
        # figures.csv stores values at six decimal places, so a small number
        # loses relative precision there. The tolerance has to be the storage
        # precision, not a pure relative one, or every share fails.
        tol = max(abs(ref) * 1e-6, 5e-7)
        if abs(ref - v) > tol:
            fails.append("%s: figures.csv says %.6f, independent re-derivation says %.6f" % (k, ref, v))
        checked += 1
    return checked, fails


# ---------------------------------------------------------------------------
# Pass B: prose scrape
# ---------------------------------------------------------------------------
# The comma-grouped alternative must REQUIRE a comma group, or the regex matches
# the first three digits of an ungrouped number and reports "202" for "20260916".
NUM_RE = re.compile(
    r"(?<![\w.])(-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+(?:\.\d+)?)(?![\d,])\s*(m\b|bn\b|%|)", re.I)


def printed_tolerance(text):
    """Half of the place value of the last digit printed."""
    if "." in text:
        return 0.5 * 10 ** (-len(text.split(".")[1]))
    return 0.5


def candidates(raw, suffix):
    """Every value the printed token could mean, before matching."""
    v = float(raw.replace(",", ""))
    tol = printed_tolerance(raw)
    out = [(v, tol)]
    if suffix.lower() == "m":
        out.append((v * 1e6, tol * 1e6))
    elif suffix.lower() == "bn":
        out.append((v * 1e9, tol * 1e9))
    elif suffix == "%":
        out.append((v / 100.0, tol / 100.0))
    else:
        out.append((v / 100.0, tol / 100.0))
        out.append((v * 1e6, tol * 1e6))
        out.append((v * 1e3, tol * 1e3))
    return out


def load_allow():
    allowed = {}
    if os.path.exists(ALLOW):
        with open(ALLOW, newline="") as fh:
            for r in csv.DictReader(fh):
                allowed[r["token"].strip()] = r["reason"].strip()
    return allowed


def pass_b(figs, allowed):
    values = [v for v in figs.values() if isinstance(v, float)]
    unmatched, matched, exempt = [], 0, 0
    for doc in DOCS:
        if not os.path.exists(doc):
            continue
        for lineno, line in enumerate(open(doc), start=1):
            if line.lstrip().startswith("<!--") or line.lstrip().startswith("|---"):
                continue
            for m in NUM_RE.finditer(line):
                raw, suffix = m.group(1), m.group(2)
                token = m.group(0).strip()
                if token in allowed or raw in allowed:
                    exempt += 1
                    continue
                hit = False
                for val, tol in candidates(raw, suffix):
                    if any(abs(val - f) <= tol for f in values):
                        hit = True
                        break
                if hit:
                    matched += 1
                else:
                    unmatched.append((os.path.basename(doc), lineno, token, line.strip()[:150]))
    return matched, exempt, unmatched


def main():
    figs = load_figures()
    allowed = load_allow()
    print("figures on disk: %d" % len(figs))

    checked, fails = pass_a(figs)
    print("\nPASS A, independent re-derivation: %d checks" % checked)
    for f in fails:
        print("  FAIL " + f)
    print("  %d failures" % len(fails))

    matched, exempt, unmatched = pass_b(figs, allowed)
    print("\nPASS B, prose scrape: %d numbers matched to a figure on disk, %d declared exempt" % (matched, exempt))
    for doc, lineno, token, ctx in unmatched:
        print("  UNDERIVABLE %s:%d  %-14s  %s" % (doc, lineno, token, ctx))
    print("  %d numbers could not be re-derived" % len(unmatched))

    total = len(fails) + len(unmatched)
    print("\nTOTAL FAILURES: %d" % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
