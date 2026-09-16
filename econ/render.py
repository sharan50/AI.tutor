"""
render.py

Renders *.src.md to *.md, replacing every @@name|format@@ token with the value
of that figure from out/figures.csv.

This is not a find-and-replace across prose. Each token is unique, explicit, and
resolved from the figures file at render time, so a quoted figure cannot drift
from the file it claims to come from and an unknown name fails loudly rather
than rendering as itself.

Formats:
  usd0   -1234567.8  ->  -1,234,568
  usdm   -12361321   ->  -12.36        (millions, two decimals)
  usdm1  -12361321   ->  -12.4         (millions, one decimal)
  usdk    536980     ->  537           (thousands, whole)
  pct0    0.1840     ->  18
  pct1    0.1840     ->  18.4
  pct2    0.1840     ->  18.40
  pctv1   18.4       ->  18.4          (value already a percentage)
  num0 num1 num2 num3 num4            (plain, that many decimals)
  int     60.0       ->  60
  raw                                  (verbatim)
"""

import csv
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
TOKEN = re.compile(r"@@([A-Za-z0-9_]+)\|([a-z0-9]+)@@")


def load():
    figs = {}
    with open(os.path.join(OUT, "figures.csv"), newline="") as fh:
        for r in csv.DictReader(fh):
            figs[r["name"]] = r["value"]
    return figs


def fmt(value, spec, name):
    if spec == "raw":
        return str(value)
    try:
        v = float(value)
    except ValueError:
        raise SystemExit("render: figure %r is not numeric but format %r was asked for" % (name, spec))
    if spec == "usd0":
        return format(v, ",.0f")
    if spec == "usdm":
        return format(v / 1e6, ",.2f")
    if spec == "usdm1":
        return format(v / 1e6, ",.1f")
    if spec == "usdk":
        return format(v / 1e3, ",.0f")
    if spec == "pct0":
        return format(v * 100, ",.0f")
    if spec == "pct1":
        return format(v * 100, ",.1f")
    if spec == "pct2":
        return format(v * 100, ",.2f")
    if spec == "pctv1":
        return format(v, ",.1f")
    if spec == "int":
        return format(int(round(v)), "d")
    m = re.fullmatch(r"num(\d)", spec)
    if m:
        return format(v, ",.%df" % int(m.group(1)))
    raise SystemExit("render: unknown format %r for figure %r" % (spec, name))


def render(path, figs):
    src = open(path).read()
    missing = []

    def sub(m):
        name, spec = m.group(1), m.group(2)
        if name not in figs:
            missing.append(name)
            return m.group(0)
        return fmt(figs[name], spec, name)

    out = TOKEN.sub(sub, src)
    if missing:
        print("render: %s references %d figures that are not in figures.csv:" % (path, len(set(missing))))
        for n in sorted(set(missing)):
            print("   ", n)
        return None, len(set(missing))
    dest = path.replace(".src.md", ".md")
    with open(dest, "w") as fh:
        fh.write(out)
    n = len(TOKEN.findall(src))
    print("rendered %-26s -> %-22s %d figures resolved" % (os.path.basename(path), os.path.basename(dest), n))
    return dest, 0


if __name__ == "__main__":
    figs = load()
    print("figures available: %d" % len(figs))
    bad = 0
    for f in sorted(os.listdir(HERE)):
        if f.endswith(".src.md"):
            _dest, n = render(os.path.join(HERE, f), figs)
            bad += n
    sys.exit(1 if bad else 0)
