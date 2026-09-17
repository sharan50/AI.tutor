Build, verify, print the failures. Fix nothing unless asked.

Run `python3 src/build.py`, then `python3 tools/verify.py`. Print every `file:line message` line the checks produce and the exit status of each. If everything passes, say so in one line.

Do not edit any file, and do not attempt a fix, unless the user asks for one after seeing the failures.
