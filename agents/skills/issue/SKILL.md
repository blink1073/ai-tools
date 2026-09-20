---
name: issue
description: Use as a base for skills that draft an issue or ticket describing a problem or feature request — invoked by jira-ticket, github-issue, and similar skills, not directly for a specific ticket format.
---

# Issue

**REQUIRED SUB-SKILL:** Use the `prose` skill first for general writing
rules, then apply the rules below.

## Overview

An issue describes the problem and the desired state. It is not an
implementation plan — implementation detail belongs in a linked gist, or
gets dropped if there's no gist.

## Workflow

1. **Resolve the template.** How to find or choose a template is defined
   by whichever skill invoked you (its instructions follow this one). If
   you were invoked directly with no such rule available, ask the user
   for a template or whether to proceed without one.
2. **Pull content from the conversation.** Use the problem or feature
   already discussed. Ask only for fields nothing in context can fill.
3. **Resolve the gist.**
   - A gist already exists in the session for this work: ask whether to
     include it.
   - No gist exists: ask whether to create one (from whatever
     implementation plan/spec exists in context — show the content and
     get explicit confirmation before running `gh gist create --secret`,
     since creating a gist publishes content), link an existing gist by
     URL, or skip.
4. **Fill the template**, describing the problem and desired state only.
   Anything that describes "how to fix it" belongs in the gist (if any)
   or gets dropped — never write it into the issue body.
5. **Propose a title.** Short, specific, no ticket-type prefix.
6. **Render one fenced code block**: title on the first line, then the
   filled content.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Writing the fix approach into the body because there's no gist | Drop it — a missing gist means the plan doesn't appear anywhere, not that it goes inline |
| Skipping the gist question because none exists yet | Ask — "no gist yet" still gets a create/link/skip question |
| Guessing a template format when invoked with no calling skill | Ask the user instead |
