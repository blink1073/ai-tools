---
name: pr-creation
description: Use when preparing a GitHub pull request. The pr-creator sub-agent runs it; the conductor dispatches that agent rather than invoking this skill directly. Writes the body to .opencode/PR-BODY.md and hands the user the push and gh pr create commands to run from the host; never runs them here.
---

# PR Creation

Agents prepare pull requests, they don't open them. Write the body to
`.opencode/PR-BODY.md` and give the user the commands to run from the host.

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
   - If pre-flight checks modified any files, commit them with the rest of
     the change in step 3.
2. **Run the prose pass over the PR's prose.** **REQUIRED SUB-SKILL:**
   `prose` over every docstring, comment, and documentation file the PR
   adds or changes. Find the changed files with `git diff --name-only
   <merge-base>..HEAD` against the default branch, then read each one and
   fix prose that fails the `prose` checklist. Where the PR edits a
   docstring, **REQUIRED SUB-SKILL:** `docstrings` governs it.
3. **Commit, don't push.** Commit the work. Never push the branch and never
   run `gh pr create`.
4. **Write the body.** **REQUIRED SUB-SKILL:** `pr-description` finds the
   PR template and its structure. Keep it high-level and prose-governed.
   When the template has a changes section or a test
   section, give each **1 to 3 bullets**, no more. Write the result to
   `.opencode/PR-BODY.md`, creating `.opencode/` if needed.
5. **Resolve the target.**
   - A PR against **origin** exists for this branch: target **upstream**.
   - No fork PR for this branch and an `upstream` remote exists: stop and
     report the origin-versus-upstream question. A sub-agent cannot ask the
     user directly; the conductor relays.
   - No upstream remote: target **origin**.
6. **Verify the default branch** of the target repo: `gh repo view
   --json defaultBranchRef -q .defaultBranchRef.name`, adding `-R
   <upstream-owner>/<repo>` when targeting upstream.
7. **Prepare the commands.** Fill in the resolved values in the forms
   below, then print them for the user. Don't run any part of them.

   Target upstream:

   ```bash
   git push -u origin <branch>
   gh pr create --draft --repo <upstream-owner>/<repo> --base <default> \
     --head <fork-owner>:<branch> --title "<title>" \
     --body-file .opencode/PR-BODY.md
   ```

   Target origin: the same without `--repo`.
8. **Prompt the user to run them.** Print the commands and ask the user to
   run them from the host; this run ends here.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Running `gh pr create` | Write the body and hand the user the command |
| Pushing the branch | Put the push in the handed-over command instead |
| Writing `.opencode/pr-body.md` | Use `.opencode/PR-BODY.md` |
| More than 3 bullets in changes or test sections | Cap each at 1 to 3 bullets |
| Skipping the origin-PR check | Check first; an existing fork PR means target upstream |
| Asking the user directly from the sub-agent | Report the question; the conductor relays |
| Assuming `--base main` | Detect the actual default branch of the target repo |
| Treating a missing `just` recipe as a failure | Skip it silently; only a real failure stops the PR |
| Running `just lint`/`just typing` when there's no justfile | Skip pre-flight checks entirely |
| Retrying `just typing` after a failure | Don't; type errors aren't auto-fixed by re-running |
| Leaving pre-flight changes uncommitted | Commit them with the change in step 3 |
| Reformatting the body after drafting it | Apply the cap while drafting, then write the file once |
