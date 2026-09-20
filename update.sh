#!/usr/bin/env bash
set -ex

# Every path below is relative to the repo root.
cd "$(dirname "$0")"

for cmd in jq git rsync; do
  command -v "$cmd" >/dev/null 2>&1 || { echo "error: '$cmd' is required but not found on PATH" >&2; exit 1; }
done

# Claude
cp ~/.claude/CLAUDE.md agents/AGENTS.md
# Only the Bash allow/deny lists are synced into the committed settings.json.
# Never sync the whole file, which can carry env vars, API keys, or model
# routing that don't belong in a public repo. `unique` sorts as well as dedupes,
# matching install.sh, so repeated syncs are a no-op.
allow="$(jq -c '.permissions.allow | map(select(startswith("Bash"))) | unique' ~/.claude/settings.json)"
deny="$(jq -c '.permissions.deny | map(select(startswith("Bash"))) | unique' ~/.claude/settings.json)"
jq --argjson allow "$allow" --argjson deny "$deny" \
  '.permissions.allow = $allow | .permissions.deny = $deny' \
  claude/settings.json > claude/settings.json.tmp
mv claude/settings.json.tmp claude/settings.json
cp ~/.claude/hooks/* agents/hooks/
mkdir -p agents/skills
# Mirror, so a skill deleted from ~/.claude is deleted here too.
# Excludes evg/evergreen skills: they're work-machine-only, not for the public repo.
rsync -a --delete --exclude='*evg*' --exclude='*evergreen*' ~/.claude/skills/ agents/skills/

# OpenCode
opencode_dir="$HOME/.config/opencode"
mkdir -p opencode/plugins
jq '{ "$schema": (."$schema"), permission: { bash: .permission.bash } }' "$opencode_dir/opencode.jsonc" > opencode/opencode.jsonc
mkdir -p opencode/agent
cp "$opencode_dir/agent/reviewer.md" opencode/agent/reviewer.md
cp "$opencode_dir/agent/pr-review.md" opencode/agent/pr-review.md
cp "$opencode_dir/tui.json" opencode/tui.json
cp "$opencode_dir/package.json" opencode/package.json
cp "$opencode_dir/package-lock.json" opencode/package-lock.json
# Mirror, so a plugin deleted from ~/.config/opencode is deleted here too.
rsync -a --delete "$opencode_dir/plugins/" opencode/plugins/

# sandbox/ is intentionally NOT synced back. The CLI is authored here and is the
# source of truth; install.sh symlinks it into ~/.local/bin, so a local edit
# there is the repo file, not a copy.
