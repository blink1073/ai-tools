"""Pre-tool hook: reject git add if any explicit files are in .gitignore."""

import json
import shlex
import subprocess
import sys

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")

try:
    tokens = shlex.split(cmd)
except ValueError:
    sys.exit(0)

# Split into command segments on shell control operators, tracking the
# working directory implied by any preceding `cd <path>` segments so a
# command like `cd /other/repo && git add foo` is checked against that
# repo instead of this hook's own process cwd, and so a later `git add`
# in a chained command isn't polluted by tokens from a subsequent
# `git commit`/`git push` segment.
SEPARATORS = {"&&", "||", ";"}
segments = [[]]
for tok in tokens:
    if tok in SEPARATORS:
        segments.append([])
    else:
        segments[-1].append(tok)

cwd = None
git_segment = None
for seg in segments:
    if not seg:
        continue
    if seg[0] == "cd" and len(seg) >= 2:
        cwd = seg[1]
        continue
    if seg[0] == "git" and len(seg) >= 2 and seg[1] == "add":
        git_segment = seg
        break

if git_segment is None:
    sys.exit(0)

add_args = git_segment[2:]

# Reject -f/--force which bypasses .gitignore
if "-f" in add_args or "--force" in add_args:
    print("ERROR: git add -f/--force bypasses .gitignore", file=sys.stderr)
    sys.exit(2)

# Extract explicit file arguments (non-flag tokens after any -- separator)
if "--" in add_args:
    files = add_args[add_args.index("--") + 1 :]
else:
    files = [t for t in add_args if not t.startswith("-")]

if not files:
    sys.exit(0)

result = subprocess.run(
    ["git", "check-ignore", "--verbose"] + files,
    capture_output=True,
    text=True,
    cwd=cwd,
)
if result.returncode == 0:
    print(
        "ERROR: The following files are listed in .gitignore and must not be added:\n"
        + result.stdout.strip(),
        file=sys.stderr,
    )
    sys.exit(2)
