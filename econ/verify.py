"""
verify.py

Re-derives every stated figure from the raw outputs, knowing nothing of the
prose, and then checks the prose against what it derived.

Four passes, and the first two are cheap guards rather than re-derivations:

  0a. CURRENCY TAGS. A usd* format on a figure whose unit is not USD. The two
      render identically, so this is invisible in the output.

  0.  STALENESS. Every generating script records the SHA-256 of the model.py and
      harness.py it ran against; a set whose hashes disagree is refused.

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

    # Cross-check: net cash must equal revenue less every cost line PLUS any
    # terminal value, down the file. The terminal_value term was missing from
    # this identity and it passed only because the published run credits no
    # residual, so a scenario that did would have broken an identity this
    # verifier would not have noticed.
    rev = mcol("net_rev_consumer_mean") + mcol("net_rev_schools_mean")
    cost = sum(mcol(c + "_mean") for c in lines)
    resid = mcol("terminal_value_mean")
    d["_xcheck_net_cash_identity"] = float(np.max(np.abs(rev - cost + resid - mcol("net_cash_mean"))))

    # Cross-check: the scope ladder must decompose. Owner decision 1 rests on
    # reading the content column of a four-row table as two separable
    # decisions, so the separability is checked rather than eyeballed. Foreign
    # content, computed as (plan of record less United Kingdom only), must equal
    # the same quantity computed as (content frozen less the go-to-market
    # minimum). If the two disagree the table cannot be read the way section 12
    # reads it.
    if os.path.exists(os.path.join(OUT, "variants.csv")):
        v = {r["scenario"]: r for r in read_csv("variants.csv")}
        need = ("por", "por_content_frozen", "ukonly", "gtm_minimum")
        if all(n in v for n in need):
            cc = lambda n: float(v[n]["total_content_cost_mean"])
            d["_xcheck_scope_ladder_separable"] = float(
                (cc("por") - cc("ukonly")) - (cc("por_content_frozen") - cc("gtm_minimum")))
            d["scope_ladder_foreign_content_mean"] = cc("por") - cc("ukonly")
            d["scope_ladder_frozen_uk_content_mean"] = cc("gtm_minimum")

    d["por_final_year_effective_cac_mean"] = float(np.mean(pcol("final_year_effective_cac")))
    d["por_mean_share_over_allowance"] = float(np.mean(pcol("mean_share_over_allowance")))
    d["por_band_central_placement_terminal"] = float(mcol("cum_cash_bandcentral_placement")[-1])
    return d


def pass_a(figs):
    d = rederive()
    fails, checked = [], 0
    for k, v in d.items():
        if k.startswith("_xcheck_"):
            # Identities. The threshold below is one dollar on lines that run
            # to tens of millions, not the six decimal places the CSV is
            # written at: the monthly file rounds each column independently, so
            # a sum of twelve rounded columns can differ from a rounded sum by
            # more than the last place. A dollar is loose enough to survive that
            # and tight enough that no real error hides under it. An earlier
            # comment here claimed the six decimal places and did not match the
            # code below.
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
# The trailing guard used to be (?![\d,]), which rejected a perfectly good
# decimal whenever prose put a comma after it: in "-73.54, both read off" the
# match failed on the comma, backtracked, and reported "-73". That is worse than
# a false alarm. It means the scraper was checking a TRUNCATED PREFIX of the
# printed number, so "-73.54" would have been accepted against a figure of -73
# and a wrong decimal could pass. The guard now blocks a following digit, and a
# following comma only when a digit follows it, which is what distinguishes a
# grouped number from a sentence. See CHANGELOG 6.18.
NUM_RE = re.compile(
    r"(?<![\w.])(-?\d{1,3}(?:,\d{3})+(?:\.\d+)?|-?\d+(?:\.\d+)?)(?!\d)(?!,\d)\s*(m\b|bn\b|%|)", re.I)


def printed_tolerance(text):
    """
    Half of the place value of the last digit printed, plus a hair.

    The hair is there because a value landing exactly on the half — 11.45
    rendered to one decimal, 2.585 to two — sits precisely on the boundary, and
    binary floating point puts it a hair either side unpredictably. Without it
    the scrape reports a figure as underivable for having rounded the way the
    renderer rounded it. The hair is a millionth of the place value, far too
    small to let a genuinely different number through.
    """
    if "." in text:
        place = 10 ** (-len(text.split(".")[1]))
    else:
        place = 1.0
    return 0.5 * place * (1.0 + 1e-6)


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


# ---------------------------------------------------------------------------
# Pass 0: staleness. The harness gate proves model.py reproduces its own two
# published CSVs; it says nothing about the other files under out/, which are
# written by scripts that run on the harness but whose output nothing
# re-derives. What can go wrong there is staleness, so every script records the
# model.py it ran against and this refuses a set whose hashes disagree. It is a
# weaker check than the gate and is reported as such.
# ---------------------------------------------------------------------------
def pass_format_units():
    """
    A currency format tag on a quantity that is not money.

    `usd0` and `num0` render identically, so the difference is invisible in the
    output and shows up only when someone reads the source and takes a household
    count for a dollar figure. Twelve tokens were tagged that way until round
    four. This keeps them apart.
    """
    figs = {r["name"]: r for r in read_csv("figures.csv")}
    tok = re.compile(r"@@([A-Za-z0-9_]+)\|([a-z0-9]+)@@")
    fails = []
    for doc in DOCS:
        src = doc.replace(".md", ".src.md")
        if not os.path.exists(src):
            continue
        for m in tok.finditer(open(src).read()):
            name, spec = m.group(1), m.group(2)
            r = figs.get(name)
            if not r:
                continue
            if spec.startswith("usd") and "USD" not in r["unit"]:
                fails.append("%s: %s is tagged %s but its unit is %r"
                             % (os.path.basename(src), name, spec, r["unit"]))
    return fails


def _sha(path):
    import hashlib
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def pass_render_freshness():
    """
    Every published .md must be the render of its own .src.md, against the
    figures.csv on disk.

    render.py refuses to write when a token is missing, which is right, and
    until round 6 nothing downstream could see that it had refused. A chained
    shell command swallowed its exit code; this verifier reported no failures;
    and WRITEUP.md and LIMITS.md sat on disk holding the PREVIOUS render, with
    hand-typed numbers in them that an exemption in verify_allow.csv was
    covering. Every pass here was green over a document that had not been
    rebuilt from its source.

    This reads the manifest render.py writes and refuses a set in which any
    source or rendered file has changed since, any .src.md on disk has no row,
    or the figures file the render was made against is not the current one.
    See CHANGELOG 6.17.
    """
    path = os.path.join(OUT, "render_manifest.csv")
    if not os.path.exists(path):
        return ["render_manifest.csv is missing: run render.py"]
    rows = read_csv(path)
    fails = []
    have = {r["source"] for r in rows}
    for f in sorted(os.listdir(HERE)):
        if f.endswith(".src.md") and f not in have:
            fails.append("%s has no row in the manifest: render.py did not write it, "
                         "which it refuses to do when a token is missing" % f)
    cur_figs = _sha(os.path.join(OUT, "figures.csv"))
    for r in rows:
        src = os.path.join(HERE, r["source"])
        dst = os.path.join(HERE, r["rendered"])
        if not os.path.exists(src):
            fails.append("%s is in the manifest but not on disk" % r["source"])
            continue
        if not os.path.exists(dst):
            fails.append("%s is in the manifest but not on disk" % r["rendered"])
            continue
        if _sha(src) != r["source_sha256"]:
            fails.append("%s has changed since it was last rendered" % r["source"])
        if _sha(dst) != r["rendered_sha256"]:
            fails.append("%s has been edited since it was rendered: the published "
                         "document is not the render of its source" % r["rendered"])
        if r["figures_sha256"] != cur_figs:
            fails.append("%s was rendered against a different figures.csv" % r["rendered"])
    return fails


def pass_staleness():
    import hashlib
    h = hashlib.sha256()
    for f in ("model.py", "harness.py"):
        h.update(open(os.path.join(HERE, f), "rb").read())
    sha = h.hexdigest()
    path = os.path.join(OUT, "provenance.csv")
    if not os.path.exists(path):
        return 0, ["provenance.csv is missing: no script has recorded which model.py it ran against"]
    rows = read_csv("provenance.csv")
    fails = [
        "%s last ran against model.py+harness.py %s, not the current %s: its outputs are stale"
        % (r["script"], r["model_and_harness_sha256"][:12], sha[:12])
        for r in rows if r["model_and_harness_sha256"] != sha
    ]
    return len(rows), fails


def main():
    figs = load_figures()
    allowed = load_allow()
    print("figures on disk: %d" % len(figs))

    unit_fails = pass_format_units()
    print("\nPASS 0a, currency tags on non-currency figures: %d" % len(unit_fails))
    for f in unit_fails:
        print("  FAIL " + f)

    inv_fails = []
    if os.path.exists(os.path.join(OUT, "invariants.csv")):
        inv_fails = ["%s on %s: %s" % (r["invariant"], r["run"], r["detail"])
                     for r in read_csv("invariants.csv") if r["result"] != "pass"]
        print("\nPASS 0b, structural invariants: %d checks"
              % len(read_csv("invariants.csv")))
        for f in inv_fails:
            print("  FAIL " + f)
    else:
        inv_fails = ["invariants.csv is missing: run invariants.py"]
        print("\nPASS 0b, structural invariants: not run")

    render_fails = pass_render_freshness()
    print("\nPASS 0c, published documents match their sources: %s"
          % ("clean" if not render_fails else "%d problems" % len(render_fails)))
    for f in render_fails:
        print("  FAIL " + f)

    n_prov, stale = pass_staleness()
    print("\nPASS 0, generator staleness: %d scripts recorded" % n_prov)
    for f in stale:
        print("  FAIL " + f)
    print("  %d stale" % len(stale))

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

    total = (len(fails) + len(unmatched) + len(stale) + len(unit_fails)
             + len(inv_fails) + len(render_fails))
    print("\nTOTAL FAILURES: %d" % total)
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
