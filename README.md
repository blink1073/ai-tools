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
`rm`, `status`, `sessions`, `ls`). Run `podbox help` for options.

Keep-alive: on exit the sandbox stays up while another session is still
attached (an opencode TUI or an interactive shell); the last session out tears
it down, along with its secrets and generated config.

`opencode-sandbox ls` (global, not per-directory) lists running sandboxes with
how long ago each was last used and the slots used against the
`PODBOX_MAX_SANDBOXES` concurrency cap, which launches refuse to exceed.
`opencode-sandbox down [name]` stops and removes a sandbox (default: this
directory's).

Host dotfile sync: `~/.gitignore` and `~/.bashrc` are copied into the sandbox
home on every launch — not just at creation — so host edits reach existing
sandboxes on their next launch. The sandbox git config's `core.excludesFile`
points at the copied `.gitignore`, so git ignores the same paths as the host.

SSH commit signing: a host SSH signing key pair is synced into the sandbox
`~/.ssh` and git there is configured to sign every commit and tag with it
(`gpg.format ssh`, `commit.gpgsign`, `tag.gpgsign`), so sandbox commits meet
the same all-commits-must-be-signed policy as the host. The pair is chosen by,
in order: `PODBOX_SIGNING_KEY` (a `.pub` path), a dedicated
`~/.ssh/id_ed25519_sign_sbx` pair, else the pair named by the host git config's
`user.signingkey`. It must be passphrase-free (signing runs non-interactively);
a key that is not a file, or a `.pub` without its private half, skips the sync
with a warning. Register its public half on GitHub as a **Signing Key**.

GitHub credential: the sandbox token is a fine-grained read-only PAT
(`github_pat_...`) taken from `~/github_token.sh` (`export GITHUB_TOKEN=...`),
re-read on every create so a refreshed token needs no sandbox-side state.
`GH_TOKEN_SANDBOX` overrides the file. A launch that would create the sandbox
fails up front when the file is missing or holds a classic token, rather than
mid-launch.

Resource caps: each sandbox is capped at `PODBOX_CPUS` (default 2) and
`PODBOX_MEMORY` (default 3g).

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
