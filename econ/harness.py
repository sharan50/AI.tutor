"""
harness.py

Splits model.py at its own section markers and executes the pieces, so that
everything downstream runs the published code rather than a restatement of it.

It refuses to be believed unless it rebuilds the published output CSVs character
for character. The comparison is on the written CSV text, not on in-memory
floats: the CSV writer loses about one unit in the last place, so an in-memory
comparison passes when it should fail.

Usage:
    python3 harness.py            verify, and say so
    from harness import load      returns the verified namespace
"""

import csv
import datetime
import difflib
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MODEL = os.path.join(HERE, "model.py")
OUTDIR = os.path.join(HERE, "out")
MARKER = "# === SECTION: "

EXPECTED_SECTIONS = ["HEADER", "CONSTANTS", "DRAWS", "MECHANISM", "LOOP",
                     "AGGREGATE", "EMIT", "MAIN"]


class HarnessRefusal(Exception):
    """Raised when the harness cannot reproduce the published output."""


def split_sections(path=MODEL):
    """Split model.py on its own markers. Returns [(name, source), ...]."""
    src = open(path).read()
    lines = src.splitlines(keepends=True)
    sections, name, buf = [], None, []
    for line in lines:
        if line.startswith(MARKER):
            if name is not None:
                sections.append((name, "".join(buf)))
            name = line[len(MARKER):].split("=")[0].strip()
            buf = [line]
        else:
            buf.append(line)
    if name is not None:
        sections.append((name, "".join(buf)))
    if not sections:
        raise HarnessRefusal("no section markers found in %s" % path)
    names = [n for n, _ in sections]
    if names != EXPECTED_SECTIONS:
        raise HarnessRefusal("section list changed: %r, expected %r" % (names, EXPECTED_SECTIONS))
    return sections


def exec_sections(sections):
    """Execute each section in order into one namespace."""
    ns = {"__name__": "model_under_harness", "__file__": MODEL}
    for name, src in sections:
        try:
            exec(compile(src, "<model.py:%s>" % name, "exec"), ns)
        except Exception as exc:
            raise HarnessRefusal("section %s failed to execute: %r" % (name, exc))
    return ns


def _diff_report(label, published, rebuilt):
    pl, rl = published.splitlines(), rebuilt.splitlines()
    report = ["%s: rebuilt text does not match the published file" % label,
              "  published %d lines, %d chars, sha256 %s" % (len(pl), len(published),
                                                             hashlib.sha256(published.encode()).hexdigest()[:16]),
              "  rebuilt   %d lines, %d chars, sha256 %s" % (len(rl), len(rebuilt),
                                                             hashlib.sha256(rebuilt.encode()).hexdigest()[:16])]
    shown = 0
    for line in difflib.unified_diff(pl, rl, "published", "rebuilt", lineterm="", n=0):
        report.append("  " + line[:240])
        shown += 1
        if shown > 12:
            report.append("  ... further differences suppressed")
            break
    return "\n".join(report)


def verify(ns=None, quiet=False):
    """
    Rebuild the published CSVs from the executed sections and compare the text
    character for character. Returns the namespace, or raises HarnessRefusal.
    """
    ns = ns or exec_sections(split_sections())
    drv = ns["draw_drivers"]()
    out, summary = ns["run"](drv, ns["base_config"]())
    o, cum = ns["path_outcomes"](out, summary)

    checks = [
        ("por_monthly.csv", ns["monthly_csv_text"](out, cum, "por")),
        ("por_paths.csv", ns["paths_csv_text"](o, drv, "por")),
    ]
    for fname, rebuilt in checks:
        path = os.path.join(OUTDIR, fname)
        if not os.path.exists(path):
            raise HarnessRefusal("published file missing: %s. Run model.py first." % path)
        published = open(path, newline="").read()
        if published != rebuilt:
            raise HarnessRefusal(_diff_report(fname, published, rebuilt))
        if not quiet:
            print("%-18s reproduced character for character (%d chars, sha256 %s)"
                  % (fname, len(published), hashlib.sha256(published.encode()).hexdigest()[:16]))

    ns["_verified"] = dict(drv=drv, out=out, outcomes=o, cum=cum)
    return ns


def model_sha():
    return hashlib.sha256(open(MODEL, "rb").read()).hexdigest()


def _record_provenance():
    """
    The gate proves that model.py reproduces its own two published CSVs. It says
    nothing about the other files under out/, which are written by scripts that
    run ON the harness but whose output nothing re-derives. The failure mode
    that leaves is staleness: a derived CSV generated against an older model.py
    and never regenerated, which no amount of byte-exactness on por_monthly.csv
    would catch.

    So every script that loads the harness records which model.py it ran
    against, and verify.py refuses a set of files whose recorded hashes are not
    all the current one. It is a staleness check, not a reproduction check, and
    it is reported as the weaker thing it is.
    """
    script = os.path.basename(sys.argv[0]) or "interactive"
    path = os.path.join(OUTDIR, "provenance.csv")
    sha = model_sha()
    rows = {}
    if os.path.exists(path):
        with open(path, newline="") as fh:
            rdr = csv.reader(fh)
            header = next(rdr, None)
            for r in rdr:
                if len(r) >= 2:
                    rows[r[0]] = r
    rows[script] = [script, sha, datetime.datetime.now(datetime.timezone.utc)
                    .strftime("%Y-%m-%dT%H:%M:%SZ")]
    with open(path, "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["script", "model_sha256", "ran_at_utc"])
        for k in sorted(rows):
            w.writerow(rows[k])


def load(quiet=True):
    """Downstream entry point. Everything else in this directory calls this."""
    ns = verify(quiet=quiet)
    try:
        _record_provenance()
    except OSError:
        pass
    return ns


def selftest():
    """
    Prove the gate bites. Perturb one field of the published monthly CSV by one
    unit in the last decimal place it is written at, confirm the harness refuses,
    then restore the file and confirm it verifies again.

    A gate that has never been shown to refuse is not a gate.
    """
    path = os.path.join(OUTDIR, "por_monthly.csv")
    original = open(path, newline="").read()
    lines = original.split("\n")
    fields = lines[30].split(",")
    before = fields[7]
    fields[7] = "%.6f" % (float(before) + 0.000001)
    lines[30] = ",".join(fields)
    log = ["harness self-test",
           "perturbed por_monthly.csv row 30 field 7 from %s to %s, one unit in the last place"
           % (before, fields[7])]
    try:
        open(path, "w", newline="").write("\n".join(lines))
        try:
            verify(quiet=True)
            log.append("RESULT: FAILED. The harness accepted a file it should have refused.")
            ok = False
        except HarnessRefusal:
            log.append("RESULT: the harness refused, as it must.")
            ok = True
    finally:
        open(path, "w", newline="").write(original)
    verify(quiet=True)
    log.append("file restored; the harness verifies again.")
    log.append("sha256 of the restored file: %s"
               % hashlib.sha256(original.encode()).hexdigest())
    text = "\n".join(log) + "\n"
    with open(os.path.join(OUTDIR, "harness_selftest.txt"), "w") as fh:
        fh.write(text)
    print(text, end="")
    return ok


if __name__ == "__main__":
    try:
        ns = verify()
    except HarnessRefusal as exc:
        print("HARNESS REFUSES TO PROCEED")
        print(exc)
        sys.exit(1)
    print("harness verified: seed %s, run date %s, %d paths, %d months"
          % (ns["SEED"], ns["RUN_DATE"], ns["N_PATHS"], ns["HORIZON"]))
    if "--selftest" in sys.argv:
        sys.exit(0 if selftest() else 1)
