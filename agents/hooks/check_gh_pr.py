"""Pre-tool hook: reject gh pr create; the user opens PRs from the host."""
import json
import re
import sys

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")

if not re.search(r"\bgh\s+pr\s+create\b", cmd):
    sys.exit(0)

print(
    "ERROR: agents prepare pull requests, they don't open them. Write the PR "
    "body to .opencode/pr-body.md, then give the user the gh pr create command "
    "to run from the host.",
    file=sys.stderr,
)
sys.exit(2)
