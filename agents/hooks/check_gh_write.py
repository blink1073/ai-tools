"""Pre-tool hook: reject gh write subcommands; GitHub is read-only for agents.

Matches the raw command string so nested invocations (sh -c, chained
commands, wrappers like podbox) are caught too. Read subcommands and
plain GET api calls pass; explicit write methods, data-carrying api
calls, and graphql mutations are rejected.
"""
import json
import re
import sys

WRITE_SUBCOMMANDS = re.compile(
    r"\bgh\s+(?:"
    r"pr\s+(?:create|merge|close|edit|reopen|ready|comment|review|lock|unlock|pin|unpin)"
    r"|issue\s+(?:create|edit|close|reopen|comment|delete|pin|unpin|lock|unlock|transfer)"
    r"|gist\s+(?:create|edit|delete)"
    r"|release\s+(?:create|delete|edit|upload|archive|unarchive)"
    r"|repo\s+(?:create|delete|edit|fork|rename|archive|unarchive)"
    r"|label\s+(?:create|edit|delete|remove|clone)"
    r"|secret\s+(?:set|delete|remove)"
    r"|variable\s+(?:set|delete|remove)"
    r"|workflow\s+run"
    r"|run\s+(?:rerun|cancel|delete)"
    r"|ssh-key\s+add"
    r")\b"
)

API_WRITE_METHOD = re.compile(
    r"\bgh\s+api\b(?=[^|;&]*(?:-X|--method)\s*=?\s*[\"']?"
    r"(?:POST|PUT|PATCH|DELETE)\b)"
)

# A graphql read is a POST too, so data flags alone don't condemn it —
# only the mutation keyword or an unreadable --input file does.
GRAPHQL_WRITE = re.compile(
    r"\bgh\s+api\s+graphql\b(?=[^|;&]*(?:\bmutation\b|--input\b))"
)

API_DATA_CARRYING = re.compile(
    r"\bgh\s+api\b(?![^|;&]*graphql)"
    r"(?=[^|;&]*\s(?:-f|-F|--field|--raw-field|--input|-d|--data)\b)"
)

REJECTION = (
    "ERROR: GitHub is read-only for agents. The user creates, comments "
    "on, edits, reviews, merges, and closes. Hand the user the exact "
    "command to run instead."
)

data = json.load(sys.stdin)
cmd = data.get("tool_input", {}).get("command", "")

if (
    WRITE_SUBCOMMANDS.search(cmd)
    or API_WRITE_METHOD.search(cmd)
    or GRAPHQL_WRITE.search(cmd)
    or API_DATA_CARRYING.search(cmd)
):
    print(REJECTION, file=sys.stderr)
    sys.exit(2)

sys.exit(0)
