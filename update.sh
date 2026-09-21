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

# Model values are tracked per profile in opencode/models.json. If the local
# config's models differ from the mapping for this machine's profile, the user
# edited them by hand, so adopt them into the mapping.
if command -v docker >/dev/null 2>&1; then
  model_profile=docker
else
  model_profile=no-docker
fi
local_default=$(jq -r '.model // empty' "$opencode_dir/opencode.json")
local_heavy=$(jq -r '.agent.plan.model // .agent.reviewer.model // empty' "$opencode_dir/opencode.json")
map_default=$(jq -r --arg p "$model_profile" '.[$p].default' opencode/models.json)
map_heavy=$(jq -r --arg p "$model_profile" '.[$p].heavy' opencode/models.json)
# Only adopt concrete values. A missing model or a leftover placeholder means
# the local config isn't the source of truth for this machine.
if [ -n "$local_default" ] && [ -n "$local_heavy" ] &&
   [ "${local_default#__}" = "$local_default" ] &&
   [ "${local_heavy#__}" = "$local_heavy" ] &&
   { [ "$local_default" != "$map_default" ] || [ "$local_heavy" != "$map_heavy" ]; }; then
  tmp=$(mktemp)
  jq --arg p "$model_profile" --arg default "$local_default" --arg heavy "$local_heavy" \
    '.[$p].default = $default | .[$p].heavy = $heavy' \
    opencode/models.json > "$tmp"
  mv "$tmp" opencode/models.json
fi

mkdir -p opencode/plugins
# Sync the repo template back with placeholders intact; the concrete values
# live only in opencode/models.json.
jq '{ "$schema": (."$schema"),
      model: "__DEFAULT_MODEL__",
      agent: { plan: { model: "__HEAVY_MODEL__" },
               reviewer: { model: "__HEAVY_MODEL__" } },
      permission: { bash: .permission.bash } }' \
  "$opencode_dir/opencode.json" > opencode/opencode.json
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
