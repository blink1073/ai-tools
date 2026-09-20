---
name: prose
description: Use when writing or reviewing any prose for a human reader — docstrings, PR descriptions, comments, README text, commit messages, error messages — before or while drafting the text.
---

# Prose

## Overview

Default LLM prose habits — hedging, restating the obvious, decorative
punctuation, marketing adjectives — make writing harder to read, not
easier. This skill is a checklist of concrete, checkable rules that other
writing skills (docstrings, pr-description, ...) build on. Invoke it
first, then apply whatever format-specific rules the calling skill adds.

## Drafting

Draft directly, then review the result against every section below and fix
what it missed before using the text.

## Checklist

Apply every item below to any prose you write. Read the draft back
against this list before finishing.

- **Write Simplified Technical English.** Follow ASD-STE100: short
  sentences, one instruction per sentence, the active voice, a consistent
  term for each thing, and simple tenses. Approved-sense common words over
  jargon or elegant variation.
- **Lead with the point.** State the conclusion or the point of the
  paragraph in its first sentence. Don't wind up to it.
- **Cut restatement.** Delete any sentence whose only job is to describe
  what the reader can already see (the code, the diff, the filename, the
  obvious context).
- **Active voice, concrete verbs.** "The parser rejects malformed input,"
  not "malformed input is rejected by the parser" or "may not be handled
  correctly."
- **One idea per sentence.** Split sentences joined by "and" or "which"
  when they carry two separate claims.
- **No filler transitions.** Delete "It's worth noting that," "In order
  to," "It should be mentioned that" — say the thing directly.
- **No marketing adjectives.** "Powerful," "seamless," "robust," "simply,"
  "just" describe a feeling, not a fact. State what the thing does
  instead.
- **No em dashes, "--", "via", or arrow characters ("->", "→").** Spell
  out the connecting logic in words: "through," "using," "results in,"
  "then," "so."
- **Match the register to the reader.** A docstring reader wants
  mechanics; a PR reviewer wants judgment and risk; end-user docs want
  plain language. Don't write all three the same way.
- **Cut every sentence that doesn't change what the reader does or
  knows.** For comments, docstrings, and PR descriptions specifically:
  if deleting a sentence loses no information the reader needs to act or
  understand, delete it. Prefer a fragment or a short list item over a
  full sentence when either carries the same information.
- **Comments describe the code as it stands.** Write for a reader with
  zero context on how the code was written. No references to prior
  versions, bugs fixed, or changes made — including what you just worked
  out while debugging. State the lesson as a property or constraint ("end
  is exclusive"), not as history ("this used to be off-by-one"). If a
  comment only makes sense to someone who watched the code evolve,
  rewrite or remove it.
- **Keep comments proportional to the code.** Usually one line. Don't
  restate what the code says, and don't justify one line of configuration
  with a paragraph of rationale. Reasoning that needs more than a line or
  two belongs in a commit message or README, not the source. A ticket or
  issue number replaces the story: cite it, don't summarize it.
- **One line beats one paragraph.** Comments: one line, no more, unless
  a non-obvious invariant genuinely needs two. PR descriptions: state
  what changed and why in as few sentences as the reviewer needs to
  approve — skip background they already have, skip restating the
  diff, skip a closing summary that repeats the opening.
- **No throat-clearing before the answer.** Don't preface a comment or
  PR description with context-setting ("This PR adds...", "This change
  is needed because...") when the fact itself can open the sentence
  ("Adds retry to..."). Start with the verb or the noun that matters.
- **Don't hard-wrap text.** Let lines run long and let the reader's
  client wrap them; don't insert your own line endings to force a
  narrow column width. Two exceptions. Editing a documentation file
  that already hard-wraps by hand (existing lines manually broken at a
  fixed width): match its existing convention. Writing a git commit
  body: wrap at 72, because git never reflows a body and `git log`
  indents it by four spaces. Never impose manual wrapping on prose that
  doesn't already have it.

## Budgets

Every piece of prose has a size. Write to the size below, then stop.

| Thing | Budget |
|---|---|
| Inline comment | 1 line; 2 only for a non-obvious invariant |
| Docstring summary line | 1 sentence |
| Docstring extended summary | none by default; at most 2 sentences, and only for a constraint or gotcha the body doesn't show |
| Parameter, return, or raises entry | 1 clause |
| Commit message body | none if the subject carries it; at most 3 sentences, wrapped at 72 |
| PR summary | 2 sentences |
| PR or ticket bullet | 1 line, 1 claim |
| Ticket problem statement | 3 sentences; more only when the problem has separate symptoms the reader must tell apart |
| Error message | 1 sentence, naming what failed and what to do; when the cause is genuinely ambiguous, 1 sentence naming the failure plus 1 listing the remedies |

Over budget means cut a claim. Splitting one long sentence into two short
ones is not a cut, and neither is packing the same claims onto fewer,
longer lines: budgets in sentences are about content, not line count, so
keep the wrapping the format calls for. Reaching a budget is not a
requirement to fill it: the best extended summary is usually no extended
summary, and the best comment is usually the one you didn't need because
the code says it.

## Depth

Give the reader the fact at one level of detail and stop. Depth is the
habit of explaining the fact, then justifying it, then restating its
consequence.

- **Don't explain what the code shows.** A docstring that walks through
  the precedence order of a five-line function, or a bullet that
  paraphrases the diff, is telling the reader something they are already
  looking at. Say what they can't see: the constraint, the gotcha, the
  reason for the choice.
- **Answer the reader's one question.** A reviewer is asking "should I
  approve this?" A docstring reader is asking "how do I call this?" History
  of the old behavior, mechanism visible in the diff, and background they
  already have are different questions. Leave them out unless the answer
  depends on them.
- **No second sentence propping up the first.** If a bullet needs a
  follow-up sentence to explain it, rewrite the bullet. Don't append.
- **Skip the sections with nothing to say.** An empty-by-convention
  Parameters block, a "Motivation" that restates the summary, a "Notes"
  section holding one obvious remark: omit them rather than filling them.

## Common Mistakes

| Habit | Instead |
|---|---|
| "This function will iterate through the list and, for each item, check if it matches — then it will return the result." | "It returns the first matching item." |
| "It's important to note that this may cause issues in some cases." | Name the actual case, or cut the sentence. |
| "This powerful utility seamlessly handles..." | "This handles..." |
| "Data flows from the parser -> validator -> writer." | "The parser hands data to the validator, which hands it to the writer." |
| Docstring longer than the function it documents | Cut to the summary line; add back only what the body doesn't show. |
| Parameters section restating the type annotation for every argument | Keep entries that say what the value *means*; drop the rest. |
| A "Changes" bullet that runs four sentences | One line, one claim. Split into separate bullets or cut. |
| PR summary that explains the mechanism the diff already shows | State what changed and why the reviewer should approve. |
| "// Fixed the off-by-one here — was using <= before" | "// end is exclusive" |
| A one-line config change under a paragraph explaining the incident that prompted it | One line, or nothing; put the rationale in the commit message. |
