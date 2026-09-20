# ai-tools

Configuration and tooling for AI coding agents: Claude Code, OpenCode, and the
`podbox` container sandbox.

## Layout

| Path | Contents |
|---|---|
| `agents/` | Shared `AGENTS.md`, skills, and hooks that Claude and OpenCode both read. |
| `claude/` | Claude Code settings. |
| `opencode/` | OpenCode config, agents, plugins, and TUI settings. |
| `sandbox/` | `podbox`, `opencode-sandbox`, and the sandbox base `Containerfile`. |

## Install

```
./install.sh
```

Installs the Claude and OpenCode configuration, then links the sandbox CLI into
`~/.local/bin`. `opencode-sandbox` is linked only when `podman` is installed and
`docker` is not.

## Update

```
./update.sh
```

Copies the installed Claude and OpenCode configuration back into the repo. The
sandbox CLI is authored here, so `update.sh` leaves `sandbox/` alone.

## Requirements

- `install.sh`: `jq`, `git`, `npm`
- `update.sh`: `jq`, `git`, `rsync`
- The sandbox: `podman`, with the base image built by `podbox build`

## Sandbox

`opencode-sandbox` opens an OpenCode session in a per-project podman sandbox.
`podbox` is the underlying CLI (`up`, `create`, `shell`, `code`, `exec`, `build`,
`rm`, `status`). Run `podbox help` for options.

## Model settings

OpenCode model settings are per machine and not tracked here. Set `model` and
`agent.reviewer.model` in `~/.config/opencode/opencode.jsonc`. `install.sh`
warns when they are missing.
