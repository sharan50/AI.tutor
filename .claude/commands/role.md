Scope the session to one owner.

`$ARGUMENTS` is a role id from `roles.json`: `ceo`, `cto`, `coo`, `cfo` or `counsel`. Run `python3 src/build.py --role $ARGUMENTS`. It prints the fragments under `src/content/` the role owns (a page's file or directory, or one section fragment with its anchor), then the role's decisions, then its open items.

For the rest of the session open only the fragments printed, and edit nothing else. A change to any other fragment is discussed with that section's owner, named in `roles.json`, before it is made. Never edit `docs/roles/` or `docs/index.html`; both are generated.
