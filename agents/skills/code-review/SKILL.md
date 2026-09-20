---
name: code-review
description: Use when a ticket has a fork PR and you are carrying it to the upstream PR and through team review, after ticket-implementation's fork PR
---

# Code Review

**REQUIRED SUB-SKILL:** `pr-review-response` governs addressing review
comments. `receiving-code-review` governs how to evaluate feedback.
This skill orchestrates the post-fork review phase.

## Goal

Carry a ticket from the fork PR to a merged, reviewed change. Invoked in
a new session after `ticket-implementation` ends at the fork PR. Runs on
the light model; the user owns every PR response. Do not invoke the
local bot reviewer (`reviewer` sub-agent, `<work>/REVIEW.md`) unless the
user asks; let the team review stand on its own.

## Inputs

- The ticket. Infer the PR rather than asking: get the upstream repo
  with `git remote get-url origin`, the branch with
  `git rev-parse --abbrev-ref HEAD`, then `gh pr view --json
  url,number,headRefName,baseRefName` for the PR by branch. Prefer the
  **upstream PR** if one exists for the branch; otherwise use the
  **draft fork PR** — carry whichever exists into the rest of the
  workflow, rather than re-opening a PR that is already there.
- The upstream target branch.

## Workflow

1. **Open a PR against upstream, or reuse the upstream PR if one already
   exists.** If the upstream PR for this branch is already open, use it;
   otherwise push the fork branch (or the draft PR) toward upstream and
   open the PR. Use `pr-description` for the content. Record the
   **Upstream PR** URL in the ticket ledger at `<work>/LEDGER.md`
   (resolving `<work>` and creating the ledger if it does not exist,
   using the `ticket-implementation` format) and check off the relevant
   item, per `ticket-implementation`.
2. **Clear bots and automated tools.** Address the CI and bot comments
   as they arrive, using `pr-review-response`. Fix what fails; do not
   suppress a real failure.
3. **Present for review.** Once the automated checks are clear, mark the
   PR ready for review and update the JIRA ticket to Code Review with
   the PR link (see `jira-ticket` for the transition).
4. **Coach team review.** The team reviews; the user coordinates with
   the bot. `pr-review-response` governs each reply. The user decides
   on every response. Only run the local bot reviewer (`reviewer`
   sub-agent, producing `<work>/REVIEW.md`) if the user explicitly asks;
   otherwise leave team review to the team.
5. **Close.** Comments addressed, PR merged, JIRA to Closed.

## Stop and ask

Pause and ask rather than guessing when: the upstream PR cannot be
opened, an automated check fails in a way you cannot explain, or a team
comment conflicts with the user's earlier decision.

## Red flags

Never merge or close without the user. Never suppress a failing check.
Never answer a review comment in a way the user has not approved.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Continuing the implementing session into upstream review | Start a new session; this skill is the entry point |
| Asking the user for the PR link | Infer it from the branch with `gh pr view` |
| Opening a second upstream PR when one already exists for the branch | Use the existing upstream PR; only open one if none exists |
| Suppressing or "fixing" an automated failure by weakening the test | Address the real cause; keep the check honest |
| Marking the PR ready before checks are clear | Clear bots and automated tools first |
| Answering a review comment without user approval | The user owns every response; you draft, they decide |
