---
name: pr-description
description: Use when writing or drafting a pull request description, before or while filling out the PR body.
---

# PR Description

**REQUIRED SUB-SKILL:** Use the `prose` skill first for general writing
rules, then apply the rules below.

## Overview

A PR description tells a reviewer what changed and why they should
approve it. Prose sections carry the *why*; a bullet list carries the
*what*. Don't let a restated diff leak into the prose.

## Find the template first

Look for, in order: `.github/pull_request_template.md`,
`.github/PULL_REQUEST_TEMPLATE.md`, `.github/PULL_REQUEST_TEMPLATE/` (any
file inside). Match case-insensitively.

- **Template exists:** fill it section by section, in its own structure.
  Don't add or remove sections, don't rename them. Where the content goes
  depends on whether the template has a prose section at all:
  - **It has one** (Summary, Description, Motivation, What/Why, or any
    heading meant for narrative): write into it. Nothing goes outside the
    template.
  - **It's only a checklist, boilerplate, or HTML comments:** write the
    summary and change bullets above the template's first line, then
    reproduce the template below them unchanged. No separator line between
    them, no invented headings, nothing appended after the template.
  - Leave a checkbox unchecked when you have no evidence it's done. What's
    missing goes on that checkbox's own line, after the existing text. Not
    in a note below the template, which would put content after it.
- **No template:** use this fallback structure:
  - **Summary** — what and why, 1-2 sentences.
  - **Motivation** — the problem being solved.
  - **Changes** — terse bullet list of what changed.
  - **Testing** — what was actually run. Not "N/A" unless nothing could
    be run — say why.
  - **Breaking changes** — only include this section if there are any;
    omit it rather than writing "None."

## Writing each part

- **Summary/Motivation:** why this change exists, the problem, not the
  diff. If you find yourself listing filenames here, that content
  belongs in Changes instead.
- **Changes:** a flat bullet list, one bullet per claim, no prose. A
  bullet holding an "and", an "as well as", or a comma series of things
  you did is holding more than one claim, so split it. Three claims in one
  bullet:

  > - Documented the new cache eviction policy, why it replaces the LRU
  >   one, and that it applies only to read-through caches.

  The same content, one claim per bullet:

  > - Replaced LRU eviction with a size-and-age policy.
  > - Scoped the new policy to read-through caches only.
  > - Recorded why LRU was insufficient for large entries.

  Describe each change by its outcome or behavior, not its
  implementation — skip parameter names, function signatures, and
  internal identifiers unless a reviewer needs one to find the change.
  "Added a configurable retry limit," not "Added `max_retries` parameter
  to `fetch_page(url, max_retries=3)`."
- **Testing:** the actual command(s) run and their result, not a
  placeholder.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Summary restates the diff ("Changed X.py to add a new function") | Say why the function needed to exist |
| Changes bullet reads like a diff line ("Added `max_retries` param to `fetch_page(url, max_retries=3)`") | Describe the outcome ("Added a configurable retry limit to page fetches") |
| One bullet carrying a series of claims joined by "and" or commas | One bullet per claim, even when they touch the same file |
| "Testing: N/A" with no explanation | State what was run, or why nothing could be |
| Writing "Breaking changes: None" | Omit the section entirely if there are none |
| Filling a template's sections out of order or renaming them | Match the template's exact structure |
| Appending the summary after a checklist-only template, or fencing it off with `---` | Summary and bullets go above the template's first line, template unchanged below |
| Inventing "Changes" and "Testing" headings the template doesn't have | Use the template's own sections; a checklist-only template gets bare bullets above it |
| Checking every box so the template looks complete | Uncheck what you can't evidence, and say what's missing on that box's line |
| Explaining the unchecked boxes in a trailing note below the template | Put the explanation on the checkbox line itself |
