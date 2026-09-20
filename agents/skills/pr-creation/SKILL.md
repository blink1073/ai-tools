---
name: pr-creation
description: Use when preparing a GitHub pull request. Write the body to .opencode/pr-body.md and hand the user a gh pr create command to run from the host; never run gh pr create.
---

# PR Creation

Agents prepare pull requests, they don't open them. Write the body to
`.opencode/pr-body.md` and give the user the `gh pr create` command to run
from the host.

**REQUIRED SUB-SKILL:** Use the `pr-description` skill for the PR title and
body content.

## Workflow

1. **Pre-flight checks.** If `justfile` or `Justfile` exists in the repo
   root, run `just lint` then `just typing`.
   - Recipe doesn't exist (`just`'s stderr contains "Justfile does not
     contain recipe"): skip that check, not a failure.
   - `just lint` fails: **REQUIRED SUB-SKILL:** `just-lint-retry` governs
     handling the failure.
   - `just typing` fails: no retry. A type error isn't auto-fixed by
     re-running the check. Stop here and report it.
   - No justfile: skip pre-flight checks entirely.
   - If pre-flight checks modified any files, tell the user which files
     changed and leave them uncommitted. Agents don't commit.
2. **Get the PR content.** **REQUIRED SUB-SKILL:** `pr-description` produces
   the title and body.
3. **Write the body.** Write the body to `.opencode/pr-body.md` in the repo,
   creating `.opencode/` if needed. Write the `pr-description` output
   exactly; don't trim or reformat it.
4. **Resolve branch details.**
   - Default branch: `gh repo view --json defaultBranchRef -q
     .defaultBranchRef.name`.
   - Current branch: `git branch --show-current`.
   - Owner for `--head`: the fork/origin owner (`gh repo view --json owner -q
     .owner.login`, or the relevant fork's owner if working from one).
5. **Hand over the command.** Give the user this command, with the resolved
   values filled in, to run from the host:

   ```bash
   git push -u origin <branch> && \
   gh pr create --draft --base <default> --head <owner>:<branch> \
     --title <title> --body-file .opencode/pr-body.md
   ```

   Don't run any part of it. Don't push the branch from here.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Running `gh pr create` | Write the body and hand the user the command |
| Pushing the branch | Put the push in the handed-over command instead |
| Assuming `--base main` | Detect the actual default branch |
| Treating a missing `just` recipe as a failure | Skip it silently; only a real failure stops the PR |
| Running `just lint`/`just typing` when there's no justfile | Skip pre-flight checks entirely |
| Retrying `just typing` after a failure | Don't; type errors aren't auto-fixed by re-running |
| Committing pre-flight changes | Leave them for the user and report the files |
| Reformatting the body when writing the file | Write the `pr-description` output exactly |
