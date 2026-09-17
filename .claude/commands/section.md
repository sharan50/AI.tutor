Open one fragment, and only that fragment.

`$ARGUMENTS` is a page slug, or `<slug>#<anchor>`. Run `python3 src/build.py --section $ARGUMENTS`. It prints the page's one-line description from `PAGES` in `src/build.py`, then the fragment file or files under `src/content/` that hold it.

Read that fragment and nothing else: not the other fragments of the page, and nothing under `docs/`. Report the description, the path, and the fragment's word count with tags stripped.
