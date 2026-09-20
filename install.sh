#!/usr/bin/env bash
set -ex

# Every path below is relative to the repo root.
cd "$(dirname "$0")"

for cmd in jq git npm; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "error: '$cmd' is required but not found on PATH" >&2; exit 1; }
done

# Claude
mkdir -p ~/.claude/hooks
mkdir -p ~/.claude/skills
cp agents/AGENTS.md ~/.claude/CLAUDE.md
if [ -f ~/.claude/settings.json ]; then
  # Merge the repo's Bash allow/deny lists into the existing file, keeping
  # everything else already on this machine (env vars, model routing,
  # extra non-Bash entries, etc.) untouched.
  repo_bash_allow=$(jq -c '.permissions.allow' claude/settings.json)
  existing_non_bash_allow=$(jq -c '[.permissions.allow[]? | select(startswith("Bash") | not)]' ~/.claude/settings.json)
  repo_bash_deny=$(jq -c '.permissions.deny' claude/settings.json)
  existing_non_bash_deny=$(jq -c '[.permissions.deny[]? | select(startswith("Bash") | not)]' ~/.claude/settings.json)
  jq --argjson bash_allow "$repo_bash_allow" --argjson other "$existing_non_bash_allow" \
     --argjson bash_deny "$repo_bash_deny" --argjson other_deny "$existing_non_bash_deny" \
    '.permissions.allow = ($bash_allow + $other | unique)
     | .permissions.deny = ($bash_deny + $other_deny | unique)' \
    ~/.claude/settings.json > /tmp/claude_settings_merged.json
  mv /tmp/claude_settings_merged.json ~/.claude/settings.json
else
  cp claude/settings.json ~/.claude/settings.json
fi
cp agents/hooks/* ~/.claude/hooks/
cp -r agents/skills/* ~/.claude/skills/

# OpenCode
opencode_dir="$HOME/.config/opencode"
mkdir -p "$opencode_dir/plugins"
if [ -f "$opencode_dir/opencode.jsonc" ]; then
  tmp=$(mktemp)
  jq --slurpfile repo opencode/opencode.jsonc '
    .permission.bash = ($repo[0].permission.bash + ((.permission.bash // {}) | to_entries | map(select($repo[0].permission.bash[.key] == null)) | from_entries))
  ' "$opencode_dir/opencode.jsonc" > "$tmp"
  mv "$tmp" "$opencode_dir/opencode.jsonc"
else
  cp opencode/opencode.jsonc "$opencode_dir/opencode.jsonc"
fi
# Model settings are per-machine and not tracked in the repo.
missing=()
jq -e '.model' "$opencode_dir/opencode.jsonc" >/dev/null 2>&1 || missing+=("model")
jq -e '.agent.reviewer.model' "$opencode_dir/opencode.jsonc" >/dev/null 2>&1 || missing+=("agent.reviewer.model")
if [ ${#missing[@]} -gt 0 ]; then
  {
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
    echo "WARNING: opencode model settings are missing: ${missing[*]}"
    echo "Set them in $opencode_dir/opencode.jsonc. Each machine sets its own."
    echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
  } >&2
fi
mkdir -p "$opencode_dir/agent"
cp opencode/agent/reviewer.md "$opencode_dir/agent/reviewer.md"
cp opencode/agent/pr-review.md "$opencode_dir/agent/pr-review.md"
cp agents/AGENTS.md "$opencode_dir/AGENTS.md"
cp opencode/tui.json "$opencode_dir/tui.json"
cp opencode/package.json "$opencode_dir/package.json"
cp opencode/package-lock.json "$opencode_dir/package-lock.json"
cp -r opencode/plugins/* "$opencode_dir/plugins/"
npm ci --prefix "$opencode_dir"

# Sandbox CLI. Symlink it into PATH so edits here take effect immediately and
# update.sh never has to copy it back.
sandbox_bin="$HOME/.local/bin"
mkdir -p "$sandbox_bin"
repo="$(pwd)"
chmod +x sandbox/podbox sandbox/opencode-sandbox
ln -sfn "$repo/sandbox/podbox" "$sandbox_bin/podbox"

# opencode-sandbox drives podman, so link it whenever podman is present. A
# docker binary doesn't conflict: its name is distinct, and on some machines
# `docker` is a shim for podman anyway.
if command -v podman >/dev/null 2>&1; then
  ln -sfn "$repo/sandbox/opencode-sandbox" "$sandbox_bin/opencode-sandbox"
fi
