---
name: github-issue-implementation
description: Use when starting work on a GitHub issue given its number or URL, before writing any code for it.
---

# GitHub Issue Implementation

**REQUIRED SUB-SKILL:** Use the `ticket-implementation` skill for the
shared workflow (reproduce, plan, implement, scope discipline, wrap up)
once this skill resolves the issue's details below.

## Overview

Resolves a GitHub issue number into title, description, and bug/feature
type via `gh`, instead of asking for them to be pasted in.

## Resolving the issue

1. **Input:** an issue number or URL. Ask for it if not given. If the
   repo isn't clear from the current directory's git remote, ask which
   `owner/repo` to use.
2. **Fetch it:** `gh issue view <number> [--repo owner/repo] --json
   title,body,labels,url`.
3. **Determine bug vs. feature/task** from labels (`bug` vs.
   `enhancement`/`feature`) first, falling back to the title/body if
   labels don't say. Ask only if genuinely ambiguous.
4. Hand off to `ticket-implementation` with the system set to GitHub (so
   its scope-discipline step offers a `github-issue` draft for anything
   unrelated found), plus the resolved type, title, and description.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Asking the user to paste title/description | Fetch them with `gh issue view` |
| Guessing the repo without checking the git remote or asking | Check the remote first, ask if still unclear |
| Treating "read the issue" as a downstream nice-to-have | Fetching it is step 1, before anything else |
| Skipping label inspection for bug/feature classification | Check labels before falling back to title/body |
