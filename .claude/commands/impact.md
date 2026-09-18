Print the edit plan for a dependency-map node before anything is edited.

Run `python3 tools/depmap.py impact $ARGUMENTS` and show its output in full. If the id is not a node, run `python3 tools/depmap.py list`, pick the nearest node by label, and say which you picked.

Then state, in one line each: the fragments under `src/content/` to open, in the order printed; and which decisions, tests and open items the closure touches, from the `d`, `t` and `o` fields of those nodes in `tools/depmap/graph.json`. Open nothing and edit nothing until the plan has been stated.
