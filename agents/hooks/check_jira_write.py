"""Pre-tool hook: reject Jira write tools; Jira is read-only for agents.

Reads a Claude-Code-style PreToolUse payload on stdin. Matches write
tools by name suffix so any server prefix works (mcp__server__jira_...,
server_jira_..., bare jira_...), and catches indirection (exec/codemode
tools carrying a Jira write tool name inside their arguments). Bash is
always allowed: Jira is only reachable through MCP tools, and a Bash
command naming the tool is the agent handing the user the command.
"""
import json
import re
import sys

WRITE_SUFFIX = re.compile(
    r"jira_(?:create_issue|update_issue|add_comment|link_issues"
    r"|unlink_issues|transition_issue)$"
)
WRITE_ANYWHERE = re.compile(
    r"jira_(?:create_issue|update_issue|add_comment|link_issues"
    r"|unlink_issues|transition_issue)"
)

REJECTION = (
    "ERROR: Jira is read-only for agents. The user files, comments on, "
    "edits, links, and transitions issues. Prepare the ticket or field "
    "values and hand them to the user with the exact call to run."
)

data = json.load(sys.stdin)
tool_name = data.get("tool_name", "") or ""

if tool_name == "Bash":
    sys.exit(0)

if WRITE_SUFFIX.search(tool_name) or WRITE_ANYWHERE.search(
    json.dumps(data.get("tool_input", {}))
):
    print(REJECTION, file=sys.stderr)
    sys.exit(2)

sys.exit(0)
