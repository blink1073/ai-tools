---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions, especially if the feedback seems unclear or technically questionable
---

# Receiving Code Review

## Attribution

Adapted from [obra/superpowers](https://github.com/obra/superpowers) (MIT
License); phrasing and prio references adapted to this setup.

## Overview

Code review is technical evaluation, not emotional performance. **Core
principle:** verify before implementing, ask before assuming, and prefer
technical correctness over social comfort. The user owns every PR
response but may ask the bot to review before answering; this skill
governs how to evaluate and address feedback.

## The response pattern

1. **Read** the full feedback without reacting.
2. **Understand** it: restate the requirement in your own words, or ask.
3. **Verify** it against the codebase reality.
4. **Evaluate** whether it is technically sound for this codebase.
5. **Respond** with a technical acknowledgment or a reasoned pushback.
6. **Implement** one item at a time, testing each.

## Forbidden responses

Never say "You're absolutely right!", "Great point!", "Excellent
feedback!", or "Let me implement that now" before verifying. Instead,
restate the technical requirement, ask a clarifying question, push back
with technical reasoning if it is wrong, or just start working.

## Handling unclear feedback

If any item is unclear, stop and ask before implementing anything. Items
may be related; partial understanding produces the wrong implementation.
Do not implement the items you understand and defer the rest.

## From the user vs. external reviewers

- **From the user:** trusted; implement after understanding. Still ask
  if the scope is unclear. No performative agreement; get to the action
  or a technical acknowledgment.
- **From external reviewers:** before implementing, check whether the
  suggestion is technically correct for this codebase, whether it breaks
  existing functionality, why the current implementation exists, whether
  it works across platforms and versions, and whether the reviewer has
  the full context. If it seems wrong, push back with reasoning. If you
  cannot verify it, say so and ask how to proceed. If it conflicts with
  the user's prior decisions, stop and discuss with the user first.

## YAGNI check for "professional" features

If a reviewer suggests implementing something "properly", search the
codebase for actual usage. If nothing calls it, ask whether to remove it
(YAGNI); if it is used, implement it properly.

## Implementation order

For multi-item feedback: clarify anything unclear first, then implement
blocking issues, then simple fixes, then complex fixes, testing each
individually and verifying no regressions.

## When to push back

Push back when the suggestion breaks existing functionality, the
reviewer lacks full context, it violates YAGNI, it is technically wrong
for the stack, legacy or compatibility reasons exist, or it conflicts
with the user's architectural decisions. Push back with technical
reasoning, reference working tests and code, and involve the user if it
is architectural.

## Acknowledging correct feedback

When feedback is correct, fix it and state what changed. Do not offer
gratitude expressions or performative praise; the code shows you heard
the feedback. If you catch yourself about to write "Thanks", delete it
and state the fix instead.

## Correcting your pushback

If you pushed back and were wrong, state the correction factually and
move on: "You were right; I checked X and it does Y. Implementing now."
No long apology, no defensiveness, no over-explaining.

## Common mistakes

| Mistake | Fix |
|---|---|
| Performative agreement | State the requirement, or just act |
| Blind implementation | Verify against the codebase first |
| Batching without testing | One at a time, test each |
| Assuming the reviewer is right | Check whether it breaks something |
| Avoiding pushback | Technical correctness over comfort |
| Partial implementation | Clarify all items first |
| Cannot verify, proceeding anyway | State the limitation, ask for direction |

## GitHub thread replies

Reply to inline review comments in their own thread
(`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as
top-level PR comments. See `pr-review-response` for the reply flow.
