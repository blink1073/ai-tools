---
name: docstrings
description: Use when writing or editing a docstring for a function, method, class, or module, before or while drafting the docstring text.
---

# Docstrings

**REQUIRED SUB-SKILL:** Use the `prose` skill first for general writing
rules, then apply the rules below.

## Overview

A docstring documents behavior a reader can't get from the signature
alone: what it does, why it exists in its current form, and how to call
it. It is not a restatement of the parameter list in sentence form.

## Detect the convention before writing

1. Read 2-3 existing docstrings elsewhere in the same project.
2. Check `pyproject.toml` / `setup.cfg` / `conf.py` for `numpydoc`, Sphinx
   `napoleon_google_docstring` / `napoleon_numpy_docstring`, or similar
   config.
3. Follow whatever the project already does: style, section names, and
   level of detail.

If there's no existing convention, default to NumPy-style (numpydoc): a
one-line summary, a blank line, an extended summary only if there's
something non-obvious to say, then `Parameters` / `Returns` / `Raises` /
`Examples` sections as applicable. This is a default, not a mandate — use
Google-style or reST if the project leans that way once you check.

## Writing each part

- **Summary line:** one sentence, imperative mood ("Run the script," not
  "Runs the script" or "This function runs the script"), ends with a
  period, fits on one line.
- **Extended summary:** only add this if it says something the signature
  doesn't — a non-obvious side effect, why this differs from a similar
  method, a constraint the caller needs to know. If you can't say
  something the signature doesn't already show, skip it.
- **Parameters/Returns:** name, type, one line of what it means — not
  what its Python type already implies (don't write "an int representing
  the count" for a param called `count: int`).
- **Examples:** runnable and realistic, not a toy `foo(1, 2)`. Write them
  as doctests only if the project already runs `pytest
  --doctest-modules` (or equivalent) — check before assuming.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Extended summary just restates the signature in prose | Delete it, or add the actual rationale/gotcha |
| "Parameters" section repeats the type annotation as English | Describe what the value means, not its type |
| Docstring style doesn't match the rest of the file | Check existing docstrings first, match them |
| Example that doesn't run | Test it, or don't write it as a doctest |
