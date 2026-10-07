# AGENTS.md

Dotfiles-style config repo for AI coding agents: Claude Code, OpenCode, and the
`podbox` container sandbox. No build or test suite. CI runs `./install.sh`
then `./update.sh` on macOS as a smoke test; run both locally to verify
changes.

## Sync direction (get this right or lose work)

- `install.sh`: copies the repo into the home directory (`~/.claude`,
  `~/.config/opencode`) and symlinks `sandbox/podbox` +
  `sandbox/opencode-sandbox` into `~/.local/bin`.
- `update.sh`: copies installed config back into the repo. Run it after
  hand-editing installed config, before committing.
- `sandbox/` is the exception: it is authored here and symlinked (not copied),
  so edits to `~/.local/bin/podbox` are the repo file. `update.sh` never syncs
  `sandbox/` back.

## Files with special handling

- `opencode/opencode.json` is a template. Keep the `__DEFAULT_MODEL__` /
  `__HEAVY_MODEL__` placeholders; concrete model ids live only in
  `opencode/models.json`. `install.sh` fills placeholders (profile is `docker`
  when `docker` is on PATH, else `no-docker`) and leaves hand-set models alone;
  `update.sh` restores the placeholders and adopts hand-set values into
  `models.json`.
- `claude/settings.json` tracks only the Bash allow/deny lists. `update.sh`
  deliberately never syncs the whole `~/.claude/settings.json`, because the
  live file can carry env vars, API keys, and model routing that must not be
  committed.
- Bash permission rules are mirrored in two places and must stay aligned:
  `claude/settings.json` (`Bash(...)` entries) and `opencode/opencode.json`
  (`permission.bash`). Add new rules to both.

## Layout notes

- `agents/` is the shared layer: `agents/AGENTS.md` installs as
  `~/.claude/CLAUDE.md` and `~/.config/opencode/AGENTS.md`; `agents/hooks/*.py`
  are installed once and reused; `agents/skills/` installs into
  `~/.claude/skills/` and is mirrored (rsync --delete) into
  `~/.config/opencode/skills/`. The OpenCode plugin
  (`opencode/plugins/claude-hooks.ts`) shells out to `~/.claude/hooks/`.
- `update.sh` mirrors skills and plugins with `rsync --delete` (deleting on the
  host deletes here too) and excludes `*evg*`/`*evergreen*` skills:
  work-machine-only, not for the public repo.

## Gotchas

- `install.sh` fails up front when `podman` is installed but
  `~/github_token.sh` is missing or holds a classic (non-`github_pat_...`)
  token; the sandbox needs a fine-grained read-only PAT.
- Requirements: `install.sh` needs `jq`, `git`, `npm`; `update.sh` needs `jq`,
  `git`, `rsync`.
