import type { Plugin } from "@opencode-ai/plugin"
import { spawn } from "node:child_process"
import { homedir } from "node:os"
import path from "node:path"

const HOOKS_DIR = path.join(homedir(), ".claude", "hooks")

// Bash hooks: the gate is a cheap pre-filter over the command string; the
// script makes the real decision (exit 2 rejects).
const PYTHON_HOOKS = [
  { script: "check_gh_pr.py", gate: /\bgh\s+pr\s+create\b/ },
  { script: "check_gh_write.py", gate: /\bgh\s+/ },
  { script: "check_git_add.py", gate: /\bgit\s+add\b/ },
  { script: "check_git_commit.py", gate: /\bgit\s+commit\b/ },
  { script: "check_git_push.py", gate: /\bgit\b/ },
]

// Non-Bash hooks: gated on the tool name — Jira write tools directly, plus
// the exec/codemode shapes that could carry one in their arguments.
const TOOL_HOOKS = [
  {
    script: "check_jira_write.py",
    gate: /jira_(?:create_issue|update_issue|add_comment|link_issues|unlink_issues|transition_issue)$|codemode|mcp.exec/i,
  },
]

const PR_CREATE_PREFIX = "gh pr create"

// State-changing steps are the user's actions: hand over the command. The
// regexes skip git global flags (git --no-pager push, git -C /repo push).
const GIT_PUSH = /\bgit(?:\s+-{1,2}[\w-]+(?:[= ]\S+)?)*\s+push\b/
const GIT_COMMIT = /\bgit(?:\s+-{1,2}[\w-]+(?:[= ]\S+)?)*\s+commit\b/

function runHook(script: string, toolName: string, toolInput: unknown, command?: string): Promise<string | undefined> {
  return new Promise((resolve) => {
    const proc = spawn("python3", [path.join(HOOKS_DIR, script)], {
      stdio: ["pipe", "ignore", "pipe"],
    })
    let stderr = ""
    proc.stderr.setEncoding("utf8")
    proc.stderr.on("data", (chunk) => {
      stderr += chunk
    })
    proc.on("error", () => resolve(undefined))
    proc.on("close", (code) => {
      resolve(code === 2 ? stderr.trim() || `${script} rejected this command` : undefined)
    })
    const input =
      command === undefined
        ? { tool_name: toolName, tool_input: toolInput }
        : { tool_name: toolName, tool_input: { command } }
    proc.stdin.write(JSON.stringify(input))
    proc.stdin.end()
  })
}

function matchesPrefix(command: string, prefix: string): boolean {
  for (const segment of command.split(/&&|\|\||;|\|/)) {
    const trimmed = segment.trim()
    if (trimmed === prefix || trimmed.startsWith(prefix + " ")) return true
  }
  return false
}

function writesComment(command: string): boolean {
  const c = command.trim()
  if (/\bgh\s+(pr|issue)\s+comment\b/.test(c)) return true
  if (/\bgh\s+pr\s+review\b/.test(c) && /\s(--comment\b|--body\b|--request-changes\b|--approve\b|-b\b)/.test(c)) return true
  if (!/\bgh\s+api\b/.test(c)) return false
  if (!/\/(pulls|issues)\/[^\s/]+\/comments/.test(c)) return false
  return /(body\s*=)|-X\s+(POST|PATCH|DELETE)|--method\s+[= ]?(POST|PATCH|DELETE)|\s-d\b|\s--data\b|\s--input\b/.test(c)
}

export const ClaudeHooks: Plugin = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      const command = output.args?.command

      if (input.tool === "bash") {
        if (typeof command !== "string" || command.length === 0) return
        const workdir = output.args?.workdir
        const effective =
          typeof workdir === "string" && workdir.length > 0
            ? `cd ${JSON.stringify(workdir)} && ${command}`
            : command

        if (writesComment(command)) {
          throw new Error(
            "Blocked: posting comments to a pull request or issue is disabled by config. Share review feedback with the user in chat instead of commenting on the PR.",
          )
        }

        for (const { script, gate } of PYTHON_HOOKS) {
          if (!gate.test(effective)) continue
          const rejection = await runHook(script, input.tool, output.args, effective)
          if (rejection) throw new Error(rejection)
        }

        if (matchesPrefix(command, PR_CREATE_PREFIX)) {
          throw new Error(
            "Blocked: agents prepare pull requests, they don't open them. Write the PR body to .opencode/pr-body.md, then give the user the gh pr create command to run from the host.",
          )
        }

        if (GIT_PUSH.test(effective)) {
          throw new Error(
            "Blocked: pushing is the user's action. Show the exact git push command and ask the user to run it from the host.",
          )
        }

        if (GIT_COMMIT.test(effective)) {
          throw new Error(
            "Blocked: committing is the user's action. Show the exact git add and git commit commands and ask the user to run them.",
          )
        }

        return
      }

      for (const { script, gate } of TOOL_HOOKS) {
        if (!gate.test(input.tool)) continue
        const rejection = await runHook(script, input.tool, output.args)
        if (rejection) throw new Error(rejection)
      }
    },
  }
}

export default ClaudeHooks
