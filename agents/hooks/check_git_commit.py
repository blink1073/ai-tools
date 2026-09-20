"""Pre-tool hook: reject git commit messages with AI attribution footers."""

import json
import re
import shlex
import sys

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")

try:
    tokens = shlex.split(cmd)
except ValueError:
    sys.exit(0)

# Find 'git commit' in the token stream
try:
    git_idx = next(i for i, t in enumerate(tokens) if t == "git")
except StopIteration:
    sys.exit(0)

if git_idx + 1 >= len(tokens) or tokens[git_idx + 1] != "commit":
    sys.exit(0)

# Extract the commit message from -m/--message flags
commit_args = tokens[git_idx + 2 :]
message_parts = []
i = 0
while i < len(commit_args):
    t = commit_args[i]
    if t in ("-m", "--message") and i + 1 < len(commit_args):
        message_parts.append(commit_args[i + 1])
        i += 2
    elif t.startswith("--message="):
        message_parts.append(t[len("--message=") :])
        i += 1
    else:
        i += 1

if not message_parts:
    sys.exit(0)
