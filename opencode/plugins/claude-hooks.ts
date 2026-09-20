import type { Plugin } from "@opencode-ai/plugin"
import { spawn } from "node:child_process"
import { homedir } from "node:os"
import path from "node:path"

const HOOKS_DIR = path.join(homedir(), ".claude", "hooks")

const PYTHON_HOOKS = [
  { script: "check_gh_pr.py", gate: /\bgh\s+pr\s+create\b/ },
  { script: "check_git_add.py", gate: /\bgit\s+add\b/ },
  { script: "check_git_commit.py", gate: /\bgit\s+commit\b/ },
]

const PR_CREATE_PREFIX = "gh pr create"

const GUARDED_PREFIXES = ["git push"]

function runHook(script: string, command: string): Promise<string | undefined> {
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
    proc.stdin.write(JSON.stringify({ tool_input: { command } }))
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
  if (/\bgh\s+pr\s+review\b/.test(c) && /\s(--comment\b|--body\b|--request-changes\b|-b\b)/.test(c)) return true
  if (!/\bgh\s+api\b/.test(c)) return false
  if (!/\/(pulls|issues)\/[^\s/]+\/comments/.test(c)) return false
  return /(body\s*=)|-X\s+(POST|PATCH|DELETE)|--method\s+[= ]?(POST|PATCH|DELETE)|\s-d\b|\s--data\b|\s--input\b/.test(c)
}

export const ClaudeHooks: Plugin = async () => {
  let userMessages = 0
  const seenUserMessages = new Set<string>()
  const blockedAt = new Map<string, number>()

  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool !== "bash") return
      const command = output.args?.command
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
        const rejection = await runHook(script, effective)
        if (rejection) throw new Error(rejection)
      }

      if (matchesPrefix(command, PR_CREATE_PREFIX)) {
        throw new Error(
          "Blocked: agents prepare pull requests, they don't open them. Write the PR body to .opencode/pr-body.md, then give the user the gh pr create command to run from the host.",
        )
      }

      const prefix = GUARDED_PREFIXES.find((p) => matchesPrefix(command, p))
      if (!prefix) return
      const blocked = blockedAt.get(prefix)
      if (blocked === undefined || blocked >= userMessages) {
        blockedAt.set(prefix, userMessages)
        throw new Error(
          `${prefix} is blocked pending explicit user confirmation. Do not retry yet: show the exact command to the user and ask them to confirm. After the user replies in chat, retry the command once.`,
        )
      }
      blockedAt.delete(prefix)
    },
    event: async ({ event }) => {
      if (event.type !== "message.updated") return
      const info = (event.properties as { info?: { id?: string; role?: string; summary?: unknown } }).info
      if (!info || info.role !== "user" || info.summary !== undefined || typeof info.id !== "string") return
      if (seenUserMessages.has(info.id)) return
      seenUserMessages.add(info.id)
      userMessages += 1
    },
  }
}

export default ClaudeHooks
