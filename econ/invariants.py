"""
invariants.py

Every mechanism defect found in model.py so far -- MECHANISM_DEFECTS below is
the list, and out/mechanism_defects.csv is written from it -- passed every
automated check in this directory, on every run, while it was wrong: the harness
gate because the defect was in the published run, the off/on test because most
were in the base loop, the accounting identities because they moved households
rather than cash, and verify.py's prose scrape because a wrong number computed
consistently is still on disk.

Every one was found by a reader going through the month loop line by line. That
does not scale and it is not guaranteed to have finished.

This file is a partial answer to that. Each invariant below is a structural
statement about what the month loop must produce which at least one historical
defect violated. They are not accounting identities: an identity asks whether
cash adds up, and every one of these defects left cash adding up perfectly. They
ask whether a household is in the right place at the right time.

**Some invariants are proved to bite** and some are not, and selftest() prints
which is which rather than implying they all are. Proving one means the defect it
was written for is reintroduced into a copy of the model in memory, the invariant
is required to fail, and the copy is discarded. model.py itself is never written
to. There are more reintroduction cases than invariants proved, because four
cases exercise the same check; three invariants have never been run against any
defect and the self-test names them.

This docstring said "seven defects across rounds 2, 4 and 5" and "each invariant
is proved to bite" for two rounds after both had stopped being true, in the file
whose own comments name a stale hand-typed count as the defect. See CHANGELOG
8.2.

Output: out/invariants.csv, out/invariant_selftest.txt
"""

import csv
import os

import numpy as np

import harness

NS = harness.load()
OUT, SEED, RUN_DATE = NS["OUT"], NS["SEED"], NS["RUN_DATE"]
DRV = NS["_verified"]["drv"]
MOUT = NS["_verified"]["out"]
BASE_OUTCOMES = NS["_verified"]["outcomes"]
HORIZON = NS["HORIZON"]


# ---------------------------------------------------------------------------
# The invariants. Each takes (out, drv, cfg) and returns (ok, detail).
# ---------------------------------------------------------------------------
def inv_acquisitions_are_billed(out, drv, cfg, ns):
    """
    Every acquisition must still be standing at the end of the month it arrived
    in, in the segment it arrived into.

    This catches CHANGELOG 4.2, 5.1 and 6.1: an examination-calendar exit
    applied to a cohort in the month it arrived deletes households that have
    been charged their acquisition cost and their age-assurance check and
    billed for nothing.

    Round 6 is the reason the wording above is narrow and mechanical rather than
    broad. The name of this invariant has always been "every acquisition can be
    billed", and the docstring used to assert exactly that. What it actually
    read was a diagnostic written against ONE of the four calendar exits, and
    that diagnostic was algebraically zero whatever the other three did -- it
    could only ever fire if someone edited the single line it was written
    against. The summer lapse and the progression deleted arrivals for five
    rounds underneath it, worth 523,800 dollars of terminal cash, while this
    check read zero in all sixty months of every run and the suite reported it
    as one of the four proved to bite. An invariant named for a general property
    and fitted to one line is worse than no invariant, because the name is what
    a reader trusts. The model's diagnostic is now written against the arrivals
    array rather than against any one exit, and this reads that.
    """
    worst = float(out["arrivals_removed_same_month"].max())
    return worst <= 1e-6, "most arrivals removed in the month they arrived is %.6f" % worst


def inv_penetration_never_falls(out, drv, cfg, ns):
    """
    Cumulative reach must be non-decreasing.

    CHANGELOG 2.4: saturation was measured on the standing book, so a path that
    churned and reacquired saw its penetration FALL and could sell to the same
    market repeatedly at low-volume prices. Cumulative acquisitions are the
    quantity the saturation term now uses, and a cumulative series cannot fall.
    """
    cum = np.cumsum(out["acquisitions"], axis=1)
    worst = float(np.min(np.diff(cum, axis=1)))
    return worst >= -1e-9, "smallest month-on-month change in cumulative acquisitions is %.6f" % worst


def inv_allowance_enforced_means_no_overage(out, drv, cfg, ns):
    """
    If the allowance is enforced, no overage may be billed.

    CHANGELOG 2.3: enforce_allowance truncated delivery at the wrong number and
    kept the overage revenue, so "enforcing" the allowance sold overage on an
    allowance nobody could exceed. Checked only when the switch is on.
    """
    if not cfg.get("enforce_allowance"):
        return True, "not applicable: the allowance is not enforced in this run"
    # NOT share_over_allowance: that is the share of households whose DEMAND
    # exceeds the allowance, and under enforcement they still want more and are
    # cut off — which is the retention risk the scenario exists to price. What
    # enforcement guarantees is about what is DELIVERED. The first version of
    # this invariant checked the wrong column and failed on a correct model.
    live = out["active_hh"] > 1e-6
    if not np.any(live):
        return True, "no active households"
    consumer_sessions = out["sessions_delivered"] - out["school_sessions_delivered"]
    per_hh = np.zeros_like(consumer_sessions)
    per_hh[live] = consumer_sessions[live] / out["active_hh"][live]
    worst = float(per_hh.max())
    return (worst <= NS["SESSION_ALLOWANCE"] + 1e-6,
            "most sessions delivered to one household in a month is %.4f against an allowance of %.0f"
            % (worst, NS["SESSION_ALLOWANCE"]))


def inv_no_revenue_before_the_first_market_opens(out, drv, cfg, ns):
    """
    No revenue, no acquisition and no variable cost before any market is open.

    A boundary check on the first months of the horizon. Nothing has violated it
    yet; it is here because the start of the loop is where an off-by-one lands
    and because several of the historical defects were off-by-one in the calendar.
    """
    first = min(NS["_open_month"](cfg, m) for m in range(NS["NM"]))
    if first >= HORIZON:
        return True, "no market opens inside the horizon"
    pre = slice(0, first)
    bad = float(max(out["gross_rev_consumer"][:, pre].max(),
                    out["acquisitions"][:, pre].max(),
                    out["inference_cost"][:, pre].max()))
    return bad <= 1e-9, "largest pre-launch revenue, acquisition or inference is %.9f" % bad


def inv_school_inference_within_total(out, drv, cfg, ns):
    """
    The institution channel's inference is a part of the inference line, not a
    line beside it.

    CHANGELOG 5.2: school seats' inference sits inside inference_cost, and a
    ratio built against consumer revenue put that cost in a numerator whose
    denominator excluded the institution's revenue. The decomposition has to
    stay a decomposition.
    """
    diff = out["inference_cost"] - out["school_inference_cost"]
    worst = float(diff.min())
    return worst >= -1e-6, "smallest consumer-only inference is %.6f" % worst


def inv_content_heads_within_bengaluru_people(out, drv, cfg, ns):
    """
    The content heads are a part of the Bengaluru people line, not a line beside
    it. Same class as the one above, for the round 4.8 decomposition.
    """
    diff = out["people_beng_cost"] - out["people_beng_content_cost"]
    worst = float(diff.min())
    return worst >= -1e-6, "smallest non-content Bengaluru people cost is %.6f" % worst


def inv_ltv_estimate_below_a_year_and_a_half(out, drv, cfg, ns):
    """
    The acquisition budget cap may not believe in a household that lives longer
    than the calendar allows.

    CHANGELOG 4.3 and 5.4: the estimate assumed retention far above what the
    loop delivers, twice, by using caps and calendar arithmetic the loop does
    not have. The cap it sets scales as roughly the square of the estimate, so
    this is the only restraint on acquisition spend and it was loose by a large
    factor. The bound below is the loop's own: a pre-examination household runs
    to the progression month and then to its own sitting, which cannot exceed
    two academic years.
    """
    # NOT an invariant. A REGRESSION TRIPWIRE, and it is labelled as one below
    # because pretending otherwise would be the same kind of dressing-up this
    # whole directory exists to avoid.
    #
    # Two things are right about it. It calls the model's own ltv_estimate
    # rather than restating the arithmetic — an earlier version reimplemented
    # the formula and so was checking itself, and passed cheerfully against a
    # reintroduced defect. And it extracts the assumed household-months without
    # knowing anything about the function's internals, by differencing two runs
    # at different contributions, which cancels everything except the months.
    #
    # What is wrong with it: the threshold. A principled ceiling would come from
    # the loop's calendar, but the value returned is months scaled by a
    # first-month survival term this check cannot see, so the calendar ceiling
    # is far too loose to discriminate. THRESHOLD is set between the correct
    # code's maximum and the known defect's. That will catch this defect coming
    # back and will not catch a new one, which is what a regression test is.
    contrib = np.ones_like(drv["churn_base"])
    worst = 0.0
    for m in range(ns["NM"]):
        for t in range(ns["HORIZON"]):
            a = ns["ltv_estimate"](drv, contrib, m, t)
            b = ns["ltv_estimate"](drv, 2.0 * contrib, m, t)
            worst = max(worst, float((b - a).max()))
    return (worst <= LTV_MONTHS_TRIPWIRE,
            "longest life the budget cap assumes is %.2f billed household months" % worst)


def inv_segment_mix_sums_to_one(out, drv, cfg, ns):
    """
    A cohort is made of exactly one cohort's worth of households.

    seg_mix_exam and seg_mix_alevel are drawn independently, U(0.40, 0.85) and
    U(0.03, 0.25), so their sum exceeds one on about a twentieth of paths. The
    old arithmetic floored the pre-examination share at zero and rescaled
    nothing, so on those paths the loop put more households into stock than
    acquisitions bought: billed, consuming inference, with no acquisition cost
    and no age-assurance check paid for any of them. The clamp did not prevent
    it, it concealed it. See CHANGELOG 6.2.

    This is checked on the shares the model computes, across every path, rather
    than on an aggregate the defect barely moves.
    """
    mp, me, ma = ns["normalise_segment_mix"](drv["seg_mix_exam"], drv["seg_mix_alevel"])
    total = mp + me + ma
    worst = float(np.max(np.abs(total - 1.0)))
    return (worst <= 1e-12,
            "worst departure from one across %d paths: %.3e" % (total.shape[0], worst))


# Set between the correct code's maximum (about 13.7) and the maximum the
# CHANGELOG 5.4 defect produces (about 18.2). See the note in the function.
LTV_MONTHS_TRIPWIRE = 16.0

INVARIANTS = [
    ("every acquisition can be billed", inv_acquisitions_are_billed, "4.2 and 5.1"),
    ("cumulative reach never falls", inv_penetration_never_falls, "2.4"),
    ("an enforced allowance bills no overage", inv_allowance_enforced_means_no_overage, "2.3"),
    ("nothing happens before the first market opens", inv_no_revenue_before_the_first_market_opens, "boundary"),
    ("school inference stays inside the inference line", inv_school_inference_within_total, "5.2"),
    ("content heads stay inside the people line", inv_content_heads_within_bengaluru_people, "4.8"),
    ("a cohort is one cohort's worth of households", inv_segment_mix_sums_to_one, "6.2"),
    ("TRIPWIRE: the budget cap's assumed life", inv_ltv_estimate_below_a_year_and_a_half, "4.3 and 5.4"),
]


def run_all(out, drv, cfg, label, ns=NS):
    rows = []
    for name, fn, entry in INVARIANTS:
        ok, detail = fn(out, drv, cfg, ns)
        rows.append([SEED, RUN_DATE, label, name, "pass" if ok else "FAIL", detail, entry])
    return rows


# ---------------------------------------------------------------------------
# Proof that each invariant bites.
#
# The defect each one was written for is reintroduced by patching the SOURCE of
# model.py in memory, executing the patched copy through the harness splitter,
# and requiring the invariant to fail on it. model.py on disk is never written
# to. An invariant that has never been shown to fail is not an invariant, which
# is the same argument the harness gate's self-test rests on.
#
# The defects below are the real ones, taken from the change log entries they
# come from, not inventions chosen to be easy to catch.
# ---------------------------------------------------------------------------
# The mechanism defects found in model.py by reading the month loop, one row
# each. This list exists because the COUNT of them has been stated by hand in
# three documents and has been wrong twice: the write-up said seven for a round
# after round 6 had found three more, and LIMITS said "all seven" forty lines
# under its own enumeration of ten. A count that is quoted in three places and
# maintained in none is a defect waiting to happen, so the enumeration is the
# artefact and the count is derived from it. See CHANGELOG 7.4.
MECHANISM_DEFECTS = [
    ("2.1", "a churn reference in the wrong place"),
    ("2.3", "an allowance that truncated at the wrong number and kept the revenue anyway"),
    ("2.4", "saturation measured on the standing book rather than cumulative reach"),
    ("2.6", "an onshoring switch that moved the wrong people"),
    ("4.2", "the A-level sitting exit applied to households that had just progressed"),
    ("5.1", "both sitting exits applied to households acquired that same month"),
    ("5.4", "a lifetime-value estimate using a calendar the loop does not have"),
    ("6.1", "the summer lapse and the progression applied to that month's arrivals"),
    ("6.2", "a segment mix that did not sum to one, so households were billed that were never bought"),
    ("6.3", "the budget cap valuing an examination household acquired in its sitting month at zero months"),
    ("7.9", "the reachable pool's catalogue read on the undelayed calendar while content is built on the delayed one"),
]


REINTRODUCTIONS = [
    ("every acquisition can be billed", "4.2 and 5.1",
     "                std_exam = stock[:, ms(m, S_EXAM), :] - arrivals[:, ms(m, S_EXAM), :]",
     "                std_exam = stock[:, ms(m, S_EXAM), :]"),
    ("school inference stays inside the inference line", "5.2",
     '        out["school_inference_cost"][:, t] = school_sessions * cps\n',
     '        out["school_inference_cost"][:, t] = school_sessions * cps * 3.0\n'),
    ("content heads stay inside the people line", "4.8",
     '        out["people_beng_content_cost"][:, t] = (content_heads * drv["eng_usd_yr"]\n'
     '                                                 * drv["overhead_mult"] / 12.0)',
     '        out["people_beng_content_cost"][:, t] = (content_heads * drv["eng_usd_yr"]\n'
     '                                                 * drv["overhead_mult"] / 12.0) * 5.0'),
    ("every acquisition can be billed", "6.1, the summer lapse",
     '                std_pre = stock[:, ms(m, S_PRE), :] - arrivals[:, ms(m, S_PRE), :]\n'
     '                lapsed = std_pre * per_month[:, None]',
     '                std_pre = stock[:, ms(m, S_PRE), :]\n'
     '                lapsed = std_pre * per_month[:, None]'),
    ("every acquisition can be billed", "6.1, the progression",
     '                std_pre = stock[:, ms(m, S_PRE), :] - arrivals[:, ms(m, S_PRE), :]\n'
     '                moving = std_pre * drv["progress_continue"][:, None]',
     '                std_pre = stock[:, ms(m, S_PRE), :]\n'
     '                moving = std_pre * drv["progress_continue"][:, None]'),
    # Both round 6.1 exits at once, because that is the state the model was
    # actually in for five rounds and therefore the cost the documents quote.
    # The two rows above are each defect on its own; their costs do not sum to
    # this one, because the progression acts on what the lapse left.
    ("every acquisition can be billed", "6.1, both exits together",
     '                std_pre = stock[:, ms(m, S_PRE), :] - arrivals[:, ms(m, S_PRE), :]\n'
     '                lapsed = std_pre * per_month[:, None]\n'
     '                stock[:, ms(m, S_PRE), :] -= lapsed\n'
     '            if cm == (em + 2) % 12:\n'
     '                std_pre = stock[:, ms(m, S_PRE), :] - arrivals[:, ms(m, S_PRE), :]\n'
     '                moving = std_pre * drv["progress_continue"][:, None]\n'
     '                stock[:, ms(m, S_PRE), :] -= std_pre',
     '                stock[:, ms(m, S_PRE), :] *= (1.0 - per_month)[:, None]\n'
     '            if cm == (em + 2) % 12:\n'
     '                moving = stock[:, ms(m, S_PRE), :] * drv["progress_continue"][:, None]\n'
     '                stock[:, ms(m, S_PRE), :] = 0.0'),
    ("a cohort is one cohort's worth of households", "6.2",
     "    mix_p = np.maximum(1.0 - mix_e - mix_a, 0.0)\n"
     "    total = mix_p + mix_e + mix_a\n"
     "    return mix_p / total, mix_e / total, mix_a / total",
     "    mix_p = np.maximum(1.0 - mix_e - mix_a, 0.0)\n"
     "    return mix_p, mix_e, mix_a"),
    ("TRIPWIRE: the budget cap's assumed life", "4.3 and 5.4",
     "    m_pre_first = np.minimum(1.0 / ch, to_progress)",
     "    m_pre_first = np.minimum(1.0 / ch, to_sitting + 10.0)"),
]


def _run_patched(old_src, new_src):
    """Execute a patched copy of model.py. Nothing is written to disk."""
    src = open(harness.MODEL).read()
    if src.count(old_src) != 1:
        raise AssertionError("re-introduction anchor no longer matches model.py: %r"
                             % old_src[:60])
    patched = src.replace(old_src, new_src)
    sections, name, buf = [], None, []
    for line in patched.splitlines(keepends=True):
        if line.startswith(harness.MARKER):
            if name is not None:
                sections.append((name, "".join(buf)))
            name = line[len(harness.MARKER):].split("=")[0].strip()
            buf = [line]
        else:
            buf.append(line)
    sections.append((name, "".join(buf)))
    ns = harness.exec_sections(sections)
    cfg = ns["base_config"]()
    drv = ns["draw_drivers"]()
    out, sm = ns["run"](drv, cfg)
    po, cum = ns["path_outcomes"](out, sm)
    return out, drv, cfg, ns, po


def selftest():
    log = ["invariant self-test",
           "each invariant is checked against the defect it was written for,",
           "reintroduced into a copy of model.py in memory. model.py is not modified.",
           ""]
    ok = True
    by_name = {n: fn for n, fn, _ in INVARIANTS}
    # What each defect was worth. The self-test already runs the defective model
    # to prove the check refuses it, so the paired cost is one extra call and it
    # means the sizes quoted in LIMITS and the change log trace to a file like
    # every other number here rather than to a measurement taken by hand.
    # See CHANGELOG 6.1.
    base_terminal = float(np.mean(BASE_OUTCOMES["terminal_cash"]))
    costs = [[SEED, RUN_DATE, "correct model", "-", "%.6f" % base_terminal, "0.000000"]]
    for name, entry, old_src, new_src in REINTRODUCTIONS:
        out, drv, cfg, pns, po = _run_patched(old_src, new_src)
        passed, detail = by_name[name](out, drv, cfg, pns)
        defect_terminal = float(np.mean(po["terminal_cash"]))
        costs.append([SEED, RUN_DATE, name, entry, "%.6f" % defect_terminal,
                      "%.6f" % (base_terminal - defect_terminal)])
        if passed:
            log.append("FAILED: %-46s did not catch its own defect (%s)" % (name, entry))
            ok = False
        else:
            log.append("caught : %-46s (change log %s)" % (name, entry))
            log.append("         %s" % detail)
            log.append("         costs {:+,.0f} of terminal cash at the mean"
                       .format(base_terminal - defect_terminal))
    with open(os.path.join(OUT, "invariant_defect_costs.csv"), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "invariant", "change_log_entry",
                    "terminal_cash_mean_with_the_defect",
                    "what_the_fix_is_worth_at_the_mean"])
        w.writerows(costs)
    log.append("")
    # These two lines said "8 of the 8 invariants have a historical defect to be
    # proved against. The other 0 are boundary or containment checks." Both
    # halves were false, and the zero was produced by subtracting two counts of
    # DIFFERENT THINGS: there are eight reintroduction CASES, but four of them
    # are the same invariant, so five distinct invariants are proved and three
    # have never been run against any defect at all. Two of those three were
    # written for named historical defects and simply have no reintroduction.
    #
    # This is the same defect as the one round 6 rewrote this file to fix: a
    # count that claims more coverage than the code delivers, in the artefact
    # whose entire purpose is to say what is and is not covered.
    # See CHANGELOG 7.3.
    proved = sorted({name for name, _entry, _o, _n in REINTRODUCTIONS})
    unproved = [n for n, _fn, _e in INVARIANTS if n not in proved]
    log.append("%d reintroduction cases, covering %d of the %d invariants."
               % (len(REINTRODUCTIONS), len(proved), len(INVARIANTS)))
    log.append("The other %d have never been run against any defect and are NOT proved"
               % len(unproved))
    log.append("to bite, whatever their names claim:")
    for n in unproved:
        log.append("   unproved: %s" % n)
    text = "\n".join(log) + "\n"
    with open(os.path.join(OUT, "invariant_selftest.txt"), "w") as fh:
        fh.write(text)
    print(text, end="")
    return ok


def main():
    cfg = NS["base_config"]()
    rows = run_all(MOUT, DRV, cfg, "por")
    # The enforced-allowance invariant is vacuous on the published run, so it is
    # also exercised on the scenario it is about.
    enf_out, enf_sm = NS["run"](DRV, dict(cfg, enforce_allowance=True))
    rows += run_all(enf_out, DRV, dict(cfg, enforce_allowance=True), "por_allowance_enforced")

    path = os.path.join(OUT, "invariants.csv")
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "run", "invariant", "result", "detail",
                    "change_log_entry_it_was_written_for"])
        w.writerows(rows)
    failed = [r for r in rows if r[4] != "pass"]
    for r in rows:
        print("  %-24s %-46s %-5s %s" % (r[2], r[3], r[4], r[5]))
    print("wrote", path, len(rows), "checks,", len(failed), "failures")

    mpath = os.path.join(OUT, "mechanism_defects.csv")
    with open(mpath, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["seed", "run_date", "change_log_entry", "what_it_was"])
        for entry, what in MECHANISM_DEFECTS:
            w.writerow([SEED, RUN_DATE, entry, what])
    print("wrote", mpath, len(MECHANISM_DEFECTS), "mechanism defects")
    return 0 if not failed else 1


if __name__ == "__main__":
    import sys
    code = main()
    if "--selftest" in sys.argv:
        code = code or (0 if selftest() else 1)
    sys.exit(code)
