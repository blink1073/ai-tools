---
name: github-issue
description: Use when drafting a GitHub issue for a bug, feature, or task, before or while writing the issue body.
---

# GitHub Issue

**REQUIRED SUB-SKILL:** Use the `issue` skill first (which itself uses
`prose`), then apply the rules below.

## Overview

This skill supplies GitHub's template-resolution rule, markup, and AI
attribution fallback for the `issue` skill's workflow.

## Template resolution

1. Look for `.github/ISSUE_TEMPLATE/` (a directory of templates) or the
   legacy single `.github/ISSUE_TEMPLATE.md`.
2. Exactly one template found: use it, no question asked.
3. Multiple templates found: infer the best match from the conversation
   (bug report vs. feature request vs. other), state the recommendation,
   and ask the user to confirm or pick a different one.
4. No template found: use a plain problem/desired-state structure and
   add an AI attribution line (see below) — there's no template to omit
   it from.

## Markup

Standard markdown backticks for code-object names — GitHub renders
markdown natively, no special inline syntax needed.

## AI attribution (no-template case only)

Add a line near the end of the issue: who/what generated the content
(e.g., "Drafted with AI assistance (Claude); reviewed by a human before
posting") and that a human reviewed it. Omit this if a template was
used — don't add fields a template doesn't define.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Asking which template when only one exists | Just use it |
| Silently picking a template with multiple candidates | State the recommendation, then ask |
| Adding AI attribution when a template was used | Only add it in the no-template fallback |
