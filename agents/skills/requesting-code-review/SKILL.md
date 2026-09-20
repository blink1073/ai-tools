---
name: requesting-code-review
description: Use when completing tasks, implementing a major feature, or before opening a PR to upstream, to have work reviewed against requirements
---

# Requesting Code Review

## Attribution

Adapted from [obra/superpowers](https://github.com/obra/superpowers) (MIT
License); adapted to the reviewer sub-agent and the staged review loop.

## Overview

Get the work reviewed before issues cascade. The reviewer gets precisely
crafted context, never your session history. **Core principle:** review
early, review often.

In this workflow, review runs in the `reviewer` sub-agent (heavy model)
during the **Review - Local Bot** phase, which produces `<work>/REVIEW.md`
in the ticket work directory and precedes the draft PR. Do not skip it
because the change looks simple.

## What to hand the reviewer

1. **Get the git shas:**
   ```bash
   BASE_SHA=$(git rev-parse HEAD~1)   # or origin/main
   HEAD_SHA=$(git rev-parse HEAD)
   ```
2. **Dispatch the `reviewer` sub-agent** with focused context only:
   - `{DESCRIPTION}`: a brief summary of what was built.
   - `{PLAN_OR_REQUIREMENTS}`: what it should do, from `<work>/PLAN.md`
     or the ticket.
   - `{BASE_SHA}` and `{HEAD_SHA}`: the change to review.
   - The checkout path and `<work>`, so it can write `<work>/REVIEW.md`.
3. **Act on the feedback** in REVIEW.md:
   - Fix anything critical immediately.
   - Fix anything important before proceeding.
   - Note minor items for later.
   - If the reviewer is wrong, push back with technical reasoning, but
     verify first (see `receiving-code-review`).

## Why dispatch a sub-agent, not review inline

You are the conductor; reviewing the diff inline burns the context you
need to keep driving the work. The reviewer's context holds the diff and
the evaluation; only the findings return to you. Hand it crafted context,
never your whole session history, so it judges the work, not your
thought process.

## Red flags

Never skip review because "it is simple". Never ignore a critical issue,
proceed past an unfixed important issue, or argue with valid technical
feedback.
