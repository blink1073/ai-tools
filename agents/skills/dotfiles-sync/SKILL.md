---
name: dotfiles-sync
description: Use when asked to commit or sync changes to ~/.claude, AGENTS.md, skills, or hooks in the dotfiles repo.
---

# Syncing to the dotfiles repo

`$HOME/workspace/dotfiles` holds the tracked copy of this config. It syncs by
copy, not symlink: `install.sh` writes the repo out to `~/.claude`, and
`update.sh` copies `~/.claude` back into the repo. Edits to `~/.claude` are
untracked until `update.sh` runs. AGENTS.md is stored there as
`agents/AGENTS.md`.

The repo is public. When asked to commit changes to `~/.claude`:

1. Review everything `update.sh` copies for content that should not be
   public: internal hostnames, wiki or ticket links, ticket IDs, email
   addresses, credentials, and descriptions of internal tooling or auth
   setup. Report what you find and let me decide rather than editing it out.
2. Run `update.sh` from the repo root.
3. Read `git status` and `git diff` before committing. The script copies
   whatever is currently on disk, so unrelated local edits ride along. Name
   them.
4. Ask before pushing to origin.
