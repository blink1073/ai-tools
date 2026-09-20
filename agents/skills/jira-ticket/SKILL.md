---
name: jira-ticket
description: Use when drafting a JIRA ticket for a bug, task, feature, or build/CI failure, before or while writing the ticket body.
---

# JIRA Ticket

**REQUIRED SUB-SKILL:** Use the `issue` skill first (which itself uses
`prose`), then apply the rules below.

## Overview

This skill supplies JIRA's template-resolution rule and JIRA-specific
markup for the `issue` skill's workflow. A bug, a task, and a broken
build want different fields, so the template is chosen per ticket rather
than fixed.

## Template resolution

**Check the repository first.** If the ticket's repository is
`drivers-evergreen-tools` or `drivers-github-tools` and the ticket is
*not* a build/CI failure, use `drivers-template.txt` and skip the
content-based table below — repo identity overrides what the ticket is
about for these two repos. A red CI job in either repo still gets
`build-failure-template.txt`; the repo override does not extend to
build failures.

Otherwise, four templates live in this skill's directory. Pick by what
the ticket is *about*, not by who reports it:

| Template | Use when |
|---|---|
| `task-template.txt` | New work, a change, or an improvement — nothing is broken |
| `bug-template.txt` | Shipped behavior is wrong for a user of the product |
| `build-failure-template.txt` | CI, the build, or the test pipeline is red — tooling, not product behavior |
| `drivers-template.txt` | Repo is `drivers-evergreen-tools` or `drivers-github-tools`, and it's not a build/CI failure (see above) |

1. **Infer** the best match from the conversation (repo check above takes
   priority over this step).
2. **State the recommendation and the signal you used** — one line, e.g.
   "Recommending `build-failure-template`: this is a red CI job, not a
   product defect." or "Recommending `drivers-template`: repo is
   `drivers-github-tools`."
3. **Ask** the user to confirm, pick a different one of the four, or
   supply their own template text (JIRA wiki markup) for this ticket.
   Skip this step when a calling skill states it has already resolved the
   template — steps 1–2 are then already settled, and re-asking spends
   the user's attention on a decision that skill made deliberately.
4. If the chosen file is empty or still just a placeholder comment, say
   so and ask for template text to use for this ticket instead.

The four files are starter templates — edit them in place to match your
org's conventions.

## Title

When presenting the draft, show the title alongside the body — not just
the body. If the ticket's repository is `drivers-evergreen-tools`
specifically (not `drivers-github-tools`), prefix the title with
`[Evergreen Tools] ` at draft time, ahead of the rest of the summary.

## Creating the ticket

Once the body is drafted and approved, ask whether to create the ticket now.
If the user declines, stop — the drafted body is the deliverable.

If they want it created, prompt for these fields before calling
`jira_create_issue`:

1. **Priority** — ask the user to pick one: `Minor - P4`, `Major - P3`, or
   `Unknown`.
2. **Component** — ask for a component name; an empty string is a valid
   answer (no component).
3. **Labels** — ask for a label; an empty string is a valid answer (no
   label).

### `drivers-evergreen-tools` override

If the ticket's repository is `drivers-evergreen-tools` specifically (not
`drivers-github-tools`), before calling `jira_create_issue`:

- Always use the **DRIVERS** project — don't ask.
- The title already carries the `[Evergreen Tools] ` prefix from the
  draft stage — use it as-is.
- Set Component to **Evergreen Tools** automatically — skip the Component
  prompt above.
- Ask for a **Driver Changes** field, defaulting to `Not Needed`; also
  offer `Needed - No Spec Changes` as an option.

Still ask Priority and Labels normally for this repo.

Use `jira_get_fields` to resolve the exact field IDs for Component,
Priority, and Driver Changes before calling `jira_create_issue`.

## Markup

- Wrap package, function, class, and other code-object names in
  `{{...}}` inline — not markdown backticks.
- Use a `{code}...{code}` block only for pasted artifacts (error
  messages, stack traces, config snippets), never to describe the fix.

## Formatting review

Before rendering, check for a blank line before every header — JIRA
renders a header wrong without one. No run-on paragraphs where the
template implies separate fields. No doubled blank lines.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Using markdown backticks (`` `foo` ``) for code names | Use `{{foo}}` |
| Header with no blank line before it | Add the blank line |
| Silently picking a template | State the recommendation and its signal, then ask |
| Asking which template when a calling skill already resolved it | Skip the ask — that decision is made |
| Listing the three and asking "which one?" with no recommendation | Infer first — an open question is not a recommendation |
| Filing a red CI job under `bug-template` | `bug-template` is for product behavior; a broken pipeline is `build-failure-template` |
| Inferring template from ticket content in `drivers-evergreen-tools`/`drivers-github-tools` for a non-failure ticket | Repo name overrides content — use `drivers-template` |
| Using `drivers-template` for a red CI job in `drivers-evergreen-tools`/`drivers-github-tools` | Build failures always use `build-failure-template`, even in these repos |
| Calling `jira_create_issue` without asking Priority/Component/Labels | Prompt for all three first (Component skipped only for `drivers-evergreen-tools`) |
| Prompting for Component in `drivers-evergreen-tools` | Auto-set to `Evergreen Tools`, don't ask |
| Filing a `drivers-evergreen-tools` ticket outside the DRIVERS project | Always DRIVERS for this repo |
| Dropping the `[Evergreen Tools]` title prefix for `drivers-evergreen-tools` | Prefix it at draft time, before presenting the title |
| Showing only the body when presenting a draft | Present the title alongside the body |
| Skipping the Driver Changes prompt for `drivers-evergreen-tools` | Ask, defaulting to `Not Needed` |
