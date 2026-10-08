---
name: pr-body
description: Use when asked to create or draft just a pull request body or PR description file (PR-BODY.md), without the full PR preparation flow of linting, committing, and handing over push commands.
---

# PR Body

## Overview

One deliverable: the PR body, written to `PR-BODY.md` at the repo root.
Everything else — lint runs, commits, push, `gh pr create` — belongs to
`pr-creation`; this skill starts at the diff and ends at the file.

## Workflow

1. **Read the change.** Diff the branch against its merge base with the
   default branch and read the full diff before writing a word.
2. **Pick the structure.** **REQUIRED SUB-SKILL:** `pr-description`
   governs finding the PR template and filling its sections.
3. **Write high level.** State what changed and why in terms a reviewer
   can approve at a glance, never a file-by-file restatement of the
   diff. Cap every bulleted section at three bullets, two when two
   carry it; merge small claims into one bullet rather than giving
   each file or each tweak its own.
4. **Prose pass, then write once.** **REQUIRED SUB-SKILL:** run the
   `prose` checklist over every word of the draft — headings, bullets,
   sentences — fix what fails, and only then create `PR-BODY.md`.
   Write the finished body in one pass; don't draft into the file and
   edit it there.

Stop after the file exists. Report its path and hand the user the
push and PR commands; don't run them.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Four-plus bullets because the diff is big | Cap at three; merge or cut claims |
| Bullets naming files or parameters | Describe the outcome the reviewer cares about |
| Skipping the prose pass on a short body | Prose runs on every draft, before the file is written |
| Writing to `.opencode/PR-BODY.md` or `pr-body.md` | `PR-BODY.md` at the repo root, exact name |
| Running lint or `gh pr create` | That is `pr-creation`; stop at the file |
