"""Pre-tool hook: reject git push; pushing is the user's action.

Agents prepare the push command and hand it over, they never push —
not even after in-chat confirmation. git push --help (a man-page read)
and git remote set-url --push (local config) pass.
"""
import json
import re
import sys

# Skip any git global flags between "git" and the subcommand:
# git --no-pager push, git -C /repo --work-tree=/x push, env git push.
_GIT_GLOBAL_FLAG = (
    r"(?:"
    r"-[cC](?:\s|\S*=)\S+"
    r"|--(?:git-dir|work-tree|namespace)(?:=|\s+)\S+"
    r"|--no-pager|--paginate|--bare|--exec-path(?:=\S+)?"
    r")"
)
PUSH = re.compile(rf"\bgit\s+(?:{_GIT_GLOBAL_FLAG}\s+)*push\b")

REJECTION = (
    "ERROR: pushing is the user's action. Prepare the exact git push "
    "command and hand it to the user to run; do not push."
)

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")

if PUSH.search(cmd) and not re.search(r"\bgit\s+push\s+(?:-h\b|--help\b)", cmd):
    print(REJECTION, file=sys.stderr)
    sys.exit(2)

sys.exit(0)
