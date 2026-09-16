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
    out, _summary = ns["run"](drv, ns["base_config"]())
    o, cum = ns["path_outcomes"](out)

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


def load(quiet=True):
    """Downstream entry point. Everything else in this directory calls this."""
    return verify(quiet=quiet)


if __name__ == "__main__":
    try:
        ns = verify()
    except HarnessRefusal as exc:
        print("HARNESS REFUSES TO PROCEED")
        print(exc)
        sys.exit(1)
    print("harness verified: seed %s, run date %s, %d paths, %d months"
          % (ns["SEED"], ns["RUN_DATE"], ns["N_PATHS"], ns["HORIZON"]))
