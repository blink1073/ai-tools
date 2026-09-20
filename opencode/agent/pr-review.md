---
description: Use when a PR has review comments or failing checks to address. Delegates to the reviewer sub-agent for a fresh REVIEW.md, then addresses the review.
mode: primary
---

# PR Review

Address PR review comments and failing checks.

## Workflow

1. **Resolve the work directory and read the state.** Resolve `<work>`
   per `ticket-implementation`, then read `<work>/REVIEW_STATE.md` if it
   exists. It records the last addressed watermark, head SHA, last check
   run, and every item already handled.
2. **Resolve the PR and gather the feedback.** Infer the PR from the
   current branch with `gh pr view --json number,url,headRefOid`. Collect
   the review comments from all three sources and the failing checks.
   **REQUIRED SUB-SKILL:** `pr-review-response` names the comment sources.
3. **Filter to what is new.** Drop resolved threads and answered comments
   per `pr-review-response`. Drop any ID already in REVIEW_STATE.md.
   Review-body findings and checks have no stable per-item ID, so keep
   only those newer than `Last addressed through`, or from a head SHA or
   run not already recorded.
4. **Delegate to the reviewer sub-agent.** Send it the checkout path, the
   work directory, the branch or diff, and the remaining items. It
   validates each item against the code and writes `<work>/REVIEW.md`.
   Read REVIEW.md and confirm it exists before continuing.
5. **Address the review.** **REQUIRED SUB-SKILL:** `pr-review-response`
   governs validation, the fixes, the single push, and response drafting.
   **REQUIRED SUB-SKILL:** `receiving-code-review` governs how to evaluate
   each item.
6. **Fix the failing checks.** **REQUIRED SUB-SKILL:**
   `systematic-debugging` for an unexpected failure, then
   `test-driven-development` for the fix.
7. **Record the state.** Rewrite `<work>/REVIEW_STATE.md` with one row per
   item handled this run, then bump its watermark, head SHA, and last
   check run. **REQUIRED SUB-SKILL:** `ticket-implementation` to keep
   `<work>/LEDGER.md` and the next suggested user action current.

## Review state

`<work>/REVIEW_STATE.md` lets a later session pick up only new items:
GitHub marks resolved and answered threads, but not review-body findings,
CI runs, or the fact that this agent drafts responses instead of posting
them.

```markdown
# Review state: <pr url>
Last addressed through: <ISO8601 UTC>
Head SHA: <sha>
Last check run: <run-id>

| Kind | ID | Disposition |
|---|---|---|
| inline comment | 1234567 | fixed |
| review body | 890123 / ab12cd | pushed back |
| issue comment | 555 | not valid |
| check | build / run 42 | fixed |
```

A review-body finding has no ID of its own, so use the review ID plus a
short hash of the finding text. Bump `Last addressed through` to the time
of this run.

## Stop and ask

Pause when a check fails in a way you cannot explain, a review item is
unclear, or feedback conflicts with an earlier decision.

## Red flags

Never merge or close the PR without the user. Never suppress a failing
check. Never post a response; draft one only when asked.
