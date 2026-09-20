---
name: designing
description: Use when turning an idea into a new ticket's requirements, before planning or implementation — from the orchestrator session when a ticket needs spawning, or when you have an idea of your own to file
---

# Designing

**REQUIRED SUB-SKILL:** Use `jira-ticket` or `github-issue` to render
the ticket (each uses `issue` and `prose`). This skill supplies the
design principles; those skills supply the format.

## Goal

Turn an idea into a ticket with clear, testable requirements and no
implementation details. The ticket states *what must be true*, never
*how to make it true*. The plan owns the how. This is the entry point
for any new ticket: an unrelated issue surfaced during orchestration, or
an idea you have on your own.

## Two entry modes

### From the orchestrator session (light)

The conductor does not design and does not write an artifact. On an
unrelated find, it prints the general requirements as a seed and hands
off:

- what was found and why it is out of scope
- the general requirement (the outcome, in one or two sentences)

Then stop. Do not draft the formal ticket or push heavy design reasoning
onto the light session. The user takes the seed to a filing session to
write up and file the ticket.

### From you, as your own idea (heavy)

Use this directly with an idea you want to file. This is design
reasoning, so run it in the heavy session. Work the requirements-only
rules below, then render and present the draft for filing.

## Inputs

- The need or problem, from the session or the user.
- The target system: JIRA or GitHub.
- Where the ticket lands (project/component/repo), if known.

## Before you write

1. Understand the need, not the fixing. Ask the questions a requirements
   reader needs answered, and ask only for what nothing in context can
   fill.

## The requirements-only rule

1. **State the requirement as an outcome.** A requirement says what
   must be true, in terms a reader can verify. "The form rejects an
   empty email" beats "validate the email field with a regex".
2. **Give acceptance criteria, not steps.** Each criterion is checkable:
   given a condition, the result satisfies the requirement.
3. **Move the how out of the ticket.** If you catch yourself writing an
   implementation approach, a function name, an algorithm, a library, or
   a migration plan, pull it out. Put it in the plan, or drop it. A
   missing plan means the implementation detail appears nowhere, not
   that it goes inline.
4. **Keep the ticket to one requirement.** If it spans unrelated
   subsystems, suggest splitting into separate tickets rather than
   writing one broad issue.

## Render

Hand the requirements and the target system to `jira-ticket` or
`github-issue`, which resolve the template, fill the body, propose a
title, and render a fenced draft. Finish there; filing the ticket is the
user's action.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Draining the light conductor into heavy design on a spawn | Print the general requirements and hand off; design in the filing session |
| Writing the fix approach into the ticket | Pull the how out; it belongs in the plan, not the ticket |
| Stating a step instead of an outcome | State what must be true, then give checkable criteria |
| Writing requirements that cannot be verified | Turn each into a criterion that can be tested |
| One ticket for several unrelated problems | Split into one ticket per requirement |
