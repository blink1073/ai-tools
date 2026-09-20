---
name: just-lint-retry
description: Use when running `just lint` before a commit, to correctly handle a first-run failure caused by auto-fixing tools.
---

# Just Lint Retry

## Overview

`just lint` often runs auto-fixing tools (ruff, whitespace fixers) that
modify files on the first pass. A first failure doesn't always mean a
real problem — it may just mean the fix hasn't been staged yet.

## Rule

1. Run `just lint`.
2. Fails: run it once more before treating it as real.
3. Passes on the second run: the first failure was just auto-fixed
   files. Include those files in the commit you're about to make.
4. Fails again on the retry: that's a real failure. Stop and report it
   — don't retry a third time.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Treating the first `just lint` failure as final | Run it once more before giving up |
| Retrying a third time | One retry only — a second failure is real |
| Committing without including the auto-fixed files | Fold them into the same commit |
