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
`~/.local/bin`. `opencode-sandbox` is linked when `podman` is installed.

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

`opencode/opencode.json` is a template with `__DEFAULT_MODEL__` and
`__HEAVY_MODEL__` placeholders. `install.sh` picks a profile from
`opencode/models.json` based on whether `docker` is installed, then fills the
placeholders in `~/.config/opencode/opencode.json`: the top-level `model` gets
the default, and the `plan` and `reviewer` agents get the heavy model.

| Profile | Default | Heavy |
|---|---|---|
| `docker` | `glm-5p3-flash` | `kimi-k3` |
| `no-docker` | `deepseek-v4p1-flash` | `glm-5p3-flash` |

A concrete value already in the local config is left alone, so hand-set models
survive reinstalling. `update.sh` compares the local config against the mapping
for this machine's profile and writes any hand-set values back into
`opencode/models.json`, then restores the placeholders in the repo template.
