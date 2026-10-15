"""Tests for the pre-tool hooks in this directory.

Each hook reads a Claude-Code-style PreToolUse JSON payload on stdin
({"tool_name": ..., "tool_input": {...}}) and exits 2 with a stderr
message to reject, 0 to allow. Run: python3 -m unittest test_hooks -v
"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

HOOKS_DIR = Path(__file__).parent

JIRA_WRITE_TOOLS = [
    "jira_create_issue",
    "jira_update_issue",
    "jira_add_comment",
    "jira_transition_issue",
    "jira_link_issues",
    "jira_unlink_issues",
]


def run_hook(script, payload, cwd=None):
    return subprocess.run(
        [sys.executable, str(HOOKS_DIR / script)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        cwd=cwd,
    )


def bash_payload(command):
    return {"tool_name": "Bash", "tool_input": {"command": command}}


class CheckJiraWrite(unittest.TestCase):
    """Jira write tools are blocked; read tools pass."""

    def test_blocks_each_write_tool(self):
        for tool in JIRA_WRITE_TOOLS:
            with self.subTest(tool=tool):
                for name in (
                    f"mcp__mcp-gateway__{tool}",
                    f"mcp-gateway_{tool}",
                    tool,
                ):
                    result = run_hook(
                        "check_jira_write.py",
                        {"tool_name": name, "tool_input": {}},
                    )
                    self.assertEqual(result.returncode, 2, result.stderr)
                    self.assertIn("user", result.stderr)

    def test_passes_read_tools(self):
        for tool in (
            "jira_get_issue",
            "jira_search_issues",
            "jira_get_issue_comments",
            "mcp-gateway_jira_get_fields",
        ):
            result = run_hook(
                "check_jira_write.py",
                {"tool_name": tool, "tool_input": {}},
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_passes_non_jira_tools(self):
        for tool in ("Bash", "Read", "mcp-gateway_evg_get_task"):
            result = run_hook(
                "check_jira_write.py",
                {"tool_name": tool, "tool_input": {"command": "ls"}},
            )
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_blocks_indirected_write_via_exec_tool(self):
        result = run_hook(
            "check_jira_write.py",
            {
                "tool_name": "mcp-gateway_mcp-exec",
                "tool_input": {
                    "name": "jira_create_issue",
                    "arguments": {"fields": {"project": "BF"}},
                },
            },
        )
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_blocks_jira_write_named_in_codemode_payload(self):
        result = run_hook(
            "check_jira_write.py",
            {
                "tool_name": "codemode-exec-1",
                "tool_input": {"code": "await jira_transition_issue(...)"},
            },
        )
        self.assertEqual(result.returncode, 2, result.stderr)

    def test_bash_is_not_blocked_for_mentioning_the_tool_name(self):
        """Handing over the call in chat may go through bash echo; allow it."""
        result = run_hook(
            "check_jira_write.py",
            bash_payload('echo "run this: jira_create_issue --fields ..."'),
        )
        self.assertEqual(result.returncode, 0, result.stderr)


class CheckGhWrite(unittest.TestCase):
    """gh write subcommands are blocked; read subcommands pass."""

    def test_blocks_write_subcommands(self):
        blocked = [
            "gh pr merge 5",
            "gh pr close 5",
            "gh pr edit 5 --title x",
            "gh pr ready 5",
            "gh pr reopen 5",
            "gh pr create --draft",
            "gh issue create --title x",
            "gh issue edit 5 --add-label x",
            "gh issue close 5",
            "gh issue comment 5 -m hi",
            "gh gist create file.txt",
            "gh gist edit 5",
            "gh release create v1",
            "gh release upload v1 file",
            "gh repo delete x/y",
            "gh repo create x",
            "gh label create x",
            "gh secret set NAME",
            "gh workflow run ci.yml",
            "gh run cancel 123",
            "gh run rerun 123",
            "gh pr review 5",
            "gh pr review 5 --approve",
            "gh pr review 5 --comment -b hi",
            "gh pr review 5 --request-changes -b fix this",
        ]
        for cmd in blocked:
            with self.subTest(cmd=cmd):
                result = run_hook("check_gh_write.py", bash_payload(cmd))
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("user", result.stderr)

    def test_blocks_write_methods_on_gh_api(self):
        blocked = [
            "gh api repos/x/y/pulls/5 -X PUT -f body=hi",
            "gh api repos/x/y/pulls/5 --method POST -f body=hi",
            "gh api repos/x/y -X DELETE",
            "gh api repos/x/y/pulls/5/comments -d body=hi",
            "gh api repos/x/y/pulls/5/comments --input body.json",
            "gh api repos/x/y/issues/5/labels --field name=bug",
            "gh api repos/x/y/issues/5/labels --raw-field name=bug",
            "gh api graphql -f query='mutation { }'",
            "gh api graphql --input mutation.json",
            "sh -c 'gh api repos/x/y -X PUT'",
            "cd /somewhere && gh pr merge 5",
        ]
        for cmd in blocked:
            with self.subTest(cmd=cmd):
                result = run_hook("check_gh_write.py", bash_payload(cmd))
                self.assertEqual(result.returncode, 2, result.stderr)

    def test_passes_read_subcommands(self):
        allowed = [
            "gh pr view 5 --json number",
            "gh pr list",
            "gh pr checks 5",
            "gh pr diff 5",
            "gh pr status",
            "gh issue view 5",
            "gh issue list -l bug",
            "gh repo view x/y --json defaultBranchRef",
            "gh run view 123 --log",
            "gh release view v1",
            "gh release download v1",
            "gh api repos/x/y/pulls/5/comments",
            "gh api /repos/x/y/pulls/5",
            "gh api graphql -f query='query { repository { } }'",
            "gh api repos/x/y/actions/jobs/1/logs",
        ]
        for cmd in allowed:
            with self.subTest(cmd=cmd):
                result = run_hook("check_gh_write.py", bash_payload(cmd))
                self.assertEqual(result.returncode, 0, result.stderr)


class CheckGitPush(unittest.TestCase):
    """git push is blocked; reads and local-only git commands pass."""

    def test_blocks_push_variants(self):
        blocked = [
            "git push",
            "git push origin main",
            "git push -u origin feature/x",
            "git push --force-with-lease",
            "git add x && git commit -m y && git push",
            "cd /repo && git push",
            "git -C /repo push",
            "git --git-dir=/repo/.git push",
            "git push --dry-run",
            "git --no-pager push",
            "git --paginate push origin main",
            "git -c x=y --no-pager push",
            "git -C /repo --work-tree=/x push",
            "git --git-dir=/r/.git --no-pager push origin main",
            "env git push origin main",
        ]
        for cmd in blocked:
            with self.subTest(cmd=cmd):
                result = run_hook("check_git_push.py", bash_payload(cmd))
                self.assertEqual(result.returncode, 2, result.stderr)
                self.assertIn("user", result.stderr)

    def test_passes_local_git(self):
        allowed = [
            "git status",
            "git log --oneline -5",
            "git push --help",
            "git remote set-url --push origin no_push",
            "git --no-pager log",
            "git --paginate log",
            "command -v git",
        ]
        for cmd in allowed:
            with self.subTest(cmd=cmd):
                result = run_hook("check_git_push.py", bash_payload(cmd))
                self.assertEqual(result.returncode, 0, result.stderr)


class ExistingHooks(unittest.TestCase):
    """The pre-existing hooks keep behaving."""

    def test_gh_pr_create_blocked(self):
        result = run_hook("check_gh_pr.py", bash_payload("gh pr create --draft"))
        self.assertEqual(result.returncode, 2)
        result = run_hook("check_gh_pr.py", bash_payload("gh pr view 5"))
        self.assertEqual(result.returncode, 0)

    def test_git_add_ignores(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["git", "init", "-q"], cwd=tmp)
            Path(tmp, ".gitignore").write_text("secret.txt\n")
            result = run_hook(
                "check_git_add.py", bash_payload("git add -f secret.txt"), cwd=tmp
            )
            self.assertEqual(result.returncode, 2, result.stderr)
            result = run_hook(
                "check_git_add.py", bash_payload("git add .gitignore"), cwd=tmp
            )
            self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()
