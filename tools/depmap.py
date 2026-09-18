#!/usr/bin/env python3
"""The dependency map, queryable. Standard library only.

    python3 tools/depmap.py check
        every locus resolves in docs/, every edge endpoint is a node, and
        tools/depmap/graph.json agrees with the served viz/dependency-map.html
    python3 tools/depmap.py impact <node-id>
        the transitive closure upstream (what depends on the node) and
        downstream (what it depends on), each node with the owner of the
        section that states it (roles.json), the owners to discuss the change
        with, and an edit plan naming the fragments under src/content/ to
        open, in document order, with their owners
    python3 tools/depmap.py list
        every node: id, stratum, label, locus

A locus is <page>#<anchor>, naming where the pages state the thing; a page
alone where no anchor exists. Failures print as file:line message and exit 1.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "tools" / "depmap" / "graph.json"
SERVED = ROOT / "viz" / "dependency-map.html"
DOCS = ROOT / "docs"
CONTENT = ROOT / "src" / "content"

sys.path.insert(0, str(ROOT / "src"))
import build  # noqa: E402  (PAGES order and fragment_files)

PAGE_ORDER = {slug: i for i, (slug, *_rest) in enumerate(build.PAGES)}
PAGE_ORDER.setdefault("index", len(PAGE_ORDER))
PAGE_ORDER.setdefault("sources", len(PAGE_ORDER))


def load():
    return json.loads(GRAPH.read_text(encoding="utf-8"))


def locus_parts(locus):
    page, _, anchor = locus.partition("#")
    return page, (anchor or None)


def _line_of(text, needle):
    pos = text.find(needle)
    return text[:pos].count("\n") + 1 if pos >= 0 else 1


def fragment_for(page, anchor):
    """The file under src/content/ that states a locus, and the anchor's offset in it."""
    files = build.fragment_files(page)
    if not files:
        return None, 0
    if anchor is None:
        return (build.source_path(page)), 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        pos = text.find(f'id="{anchor}"')
        if pos >= 0:
            return f, pos
    return None, 0


# ------------------------------------------------------------------ check

def served_arrays():
    """The NODES and EDGES the served page carries, parsed back from its inline JSON."""
    if not SERVED.exists():
        return None, None
    text = SERVED.read_text(encoding="utf-8")
    m_n = re.search(r"^const NODES = (\[\n.*?\n\]);$", text, re.S | re.M)
    m_e = re.search(r"^const EDGES = (\[\n.*?\n\]);$", text, re.S | re.M)
    if not (m_n and m_e):
        return None, None
    return json.loads(m_n.group(1)), json.loads(m_e.group(1))


def check():
    graph = load()
    gtext = GRAPH.read_text(encoding="utf-8")
    grel = GRAPH.relative_to(ROOT)
    problems = []
    ids = {}
    for n in graph["nodes"]:
        line = _line_of(gtext, json.dumps(n["id"]))
        if n["id"] in ids:
            problems.append(f"{grel}:{line} duplicate node id {n['id']}")
        ids[n["id"]] = n
        locus = n.get("locus")
        if not locus:
            problems.append(f"{grel}:{line} {n['id']} has no locus")
            continue
        page, anchor = locus_parts(locus)
        served = DOCS / f"{page}.html"
        if not served.exists():
            problems.append(f"{grel}:{line} {n['id']} locus {locus}: docs/{page}.html does not exist")
            continue
        if anchor and f'id="{anchor}"' not in served.read_text(encoding="utf-8"):
            problems.append(f"{grel}:{line} {n['id']} locus {locus}: no id=\"{anchor}\" in docs/{page}.html")
        if not build.fragment_files(page):
            problems.append(f"{grel}:{line} {n['id']} locus {locus}: no source under src/content/")
    for e in graph["edges"]:
        line = _line_of(gtext, json.dumps(e, ensure_ascii=False))
        if len(e) != 3:
            problems.append(f"{grel}:{line} edge {e} is not [from, to, kind]")
            continue
        for end in e[:2]:
            if end not in ids:
                problems.append(f"{grel}:{line} edge {e[0]} -> {e[1]}: {end} is not a node")
    nodes, edges = served_arrays()
    srel = SERVED.relative_to(ROOT)
    if nodes is None:
        problems.append(f"{srel}:1 served map is missing or carries no inline NODES and EDGES")
    else:
        stext = SERVED.read_text(encoding="utf-8")
        if nodes != graph["nodes"]:
            problems.append(f"{srel}:{_line_of(stext, 'const NODES')} NODES differ from graph.json; run python3 src/build.py")
        if edges != graph["edges"]:
            problems.append(f"{srel}:{_line_of(stext, 'const EDGES')} EDGES differ from graph.json; run python3 src/build.py")
    for p in problems:
        print(p)
    if problems:
        print(f"depmap: {len(problems)} problem(s)")
        return 1
    print(f"depmap: {len(graph['nodes'])} nodes, {len(graph['edges'])} edges, every locus resolves, served page agrees")
    return 0


# ------------------------------------------------------------------ impact

def closure(graph, start, forward):
    """Nodes reachable from start along edges (forward: what start depends on;
    backward: what depends on start), with the hop count at which each is reached."""
    nxt = {}
    for a, b, _kind in graph["edges"]:
        if forward:
            nxt.setdefault(a, []).append(b)
        else:
            nxt.setdefault(b, []).append(a)
    seen = {start: 0}
    frontier = [start]
    while frontier:
        new = []
        for x in frontier:
            for y in nxt.get(x, []):
                if y not in seen:
                    seen[y] = seen[x] + 1
                    new.append(y)
        frontier = new
    del seen[start]
    return seen


def _place(locus):
    page, anchor = locus_parts(locus)
    frag, pos = fragment_for(page, anchor)
    files = build.fragment_files(page)
    findex = files.index(frag) if frag in files else 0
    return (PAGE_ORDER.get(page, 99), findex, pos), frag


def impact(node_id):
    graph = load()
    nodes = {n["id"]: n for n in graph["nodes"]}
    if node_id not in nodes:
        print(f"{GRAPH.relative_to(ROOT)}:1 no node {node_id}; try: python3 tools/depmap.py list")
        return 1
    up = closure(graph, node_id, forward=False)
    down = closure(graph, node_id, forward=True)
    me = nodes[node_id]
    owner = {i: build.node_owner(n) or "(no owner)" for i, n in nodes.items()}
    print(f"{node_id}: {me['label']} [{me['st']}]  stated at {me['locus']}  owner {owner[node_id]}")
    print(f"upstream, depends on it, transitively: {len(up)}")
    for i, hop in sorted(up.items(), key=lambda kv: (kv[1], kv[0])):
        print(f"  {hop}  {i:20s} {nodes[i]['label']:32s} {nodes[i]['locus']:44s} {owner[i]}")
    print(f"downstream, it depends on, transitively: {len(down)}")
    for i, hop in sorted(down.items(), key=lambda kv: (kv[1], kv[0])):
        print(f"  {hop}  {i:20s} {nodes[i]['label']:32s} {nodes[i]['locus']:44s} {owner[i]}")
    by_owner = {}
    for i, hop in up.items():
        by_owner.setdefault(owner[i], []).append((hop, f"{i} (up {hop})"))
    for i, hop in down.items():
        by_owner.setdefault(owner[i], []).append((hop, f"{i} (down {hop})"))
    others = [o for o in sorted(by_owner) if o != owner[node_id]]
    print(f"owners to discuss with, besides {owner[node_id]}: {', '.join(others) if others else 'none'}")
    for o in sorted(by_owner, key=lambda o: (o == owner[node_id], o)):
        tag = " (this node's owner)" if o == owner[node_id] else ""
        print(f"  {o:8s} {', '.join(t for _h, t in sorted(by_owner[o]))}{tag}")
    plan, plan_owner = {}, {}
    entries = [(node_id, "this", 0)] + [(i, "up", h) for i, h in up.items()] + [(i, "down", h) for i, h in down.items()]
    for i, role, hop in entries:
        key, frag = _place(nodes[i]["locus"])
        label = str(frag.relative_to(ROOT)) if frag else f"(no source for {nodes[i]['locus']})"
        _page, anchor = locus_parts(nodes[i]["locus"])
        tag = f"{i} ({role}{'' if role == 'this' else ' ' + str(hop)})"
        plan.setdefault((key[0], key[1], label), {}).setdefault((key[2], anchor or ""), []).append(tag)
        plan_owner.setdefault((key[0], key[1], label), set()).add(owner[i])
    print(f"edit plan, {len(plan)} fragment(s) in document order, with the owner to discuss each with:")
    for (_p, _f, label), anchors in sorted(plan.items()):
        print(f"  {label}  ({', '.join(sorted(plan_owner[(_p, _f, label)]))})")
        for (_pos, anchor), tags in sorted(anchors.items()):
            print(f"      {'#' + anchor + ': ' if anchor else ''}{', '.join(sorted(tags))}")
    return 0


def list_nodes():
    for n in load()["nodes"]:
        print(f"{n['id']:20s} {n['st']:14s} {n['label']:32s} {n['locus']}")
    return 0


def main(argv):
    if len(argv) >= 1 and argv[0] == "check":
        return check()
    if len(argv) == 2 and argv[0] == "impact":
        return impact(argv[1])
    if len(argv) >= 1 and argv[0] == "list":
        return list_nodes()
    print(__doc__.strip())
    return 2


if __name__ == "__main__":
    try:
        sys.exit(main(sys.argv[1:]))
    except BrokenPipeError:
        sys.exit(0)
