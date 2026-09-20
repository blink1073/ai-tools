---
name: pr-review-response
description: Use when addressing review comments on a pull request, before making any code changes in response to them.
---

# PR Review Response

## Overview

Review comments get validated before they get fixed, fixes get pushed
once as a single round, and responses only get drafted when asked —
never unprompted, and never posted.

## Workflow

**Given a direct link to a specific comment:** skip discovery entirely — no
fetching all comments, no filtering resolved/answered threads. Fetch only
that comment (its URL encodes the PR and comment/review ID; use `gh api
repos/{owner}/{repo}/pulls/comments/{id}` for an inline review comment,
`.../issues/comments/{id}` for a conversation comment, or `.../pulls/{pr}#pullrequestreview-{id}`'s
review body via `.../pulls/{pr}/reviews/{id}`, matching the URL shape). Go
straight to step 4 for that one comment, then step 5, then step 6. Steps
1-3 apply only when no specific comment link was given.

1. **Resolve the PR.** Infer from the current branch (`gh pr view --json
   number`). Ask for the PR number/URL if that fails.
2. **Fetch comments — all three sources.** Missing any of these silently
   drops feedback:
   - Inline review comments: `gh api repos/{owner}/{repo}/pulls/{pr}/comments`
   - General conversation comments: `gh api repos/{owner}/{repo}/issues/{pr}/comments`
   - **Review bodies:** `gh api repos/{owner}/{repo}/pulls/{pr}/reviews`,
     the `.body` field. A review can carry substantive feedback in its
     body with no inline comments at all, so it appears in neither of the
     first two sources. Reviewers that batch findings — Copilot puts them
     in a `<details><summary>Suppressed comments (N)</summary>` block —
     hide entire lists of issues here. Treat each finding inside a body
     as its own comment for steps 3-6.

   Merge chronologically. `gh api`'s `{owner}`/`{repo}` placeholders
   resolve automatically from the current directory's repository — no
   separate lookup needed, same as `gh pr view` in step 1.
3. **Filter out comments that don't need attention.**
   - Resolved review threads: check via GraphQL (`gh api graphql`
     querying `pullRequest.reviewThreads.nodes.isResolved`) and drop
     any comment in a resolved thread.
   - Comments that already have a reply (a later comment whose
     `in_reply_to_id` points to it, or a conversation comment already
     followed up on): drop them too.
   - Findings from a review body have no thread, so `isResolved` never
     applies and neither filter can clear them. Keep them unless a later
     comment or a change already on the branch addresses them — verify
     that against the code rather than assuming.
4. **Per remaining comment, in order:**
   - **Validate first.** Understand the concern. If it describes a code
     issue, confirm it's real before changing anything — add a test
     that demonstrates it if one doesn't exist and would help. **REQUIRED
     SUB-SKILL:** `test-driven-development` governs reproduce-before-fix;
     **REQUIRED SUB-SKILL:** `systematic-debugging` governs it for
     unexpected/buggy behavior specifically.
   - **Validated:** fix it locally. The validation test becomes
     regression coverage.
   - **Not valid:** make no code change. Note why — that's what a
     drafted response explains later.
5. **Ask once.** After every remaining comment is processed, ask
   whether to commit and push the accumulated fixes as one round.
   Confirm before the push. Before committing, if a justfile exists,
   run `just lint`. **REQUIRED SUB-SKILL:** `just-lint-retry` governs
   handling a failure (same rule `pr-creation` uses).
6. **Per remaining comment, in order, ask about a response.** "Want a
   drafted response to this one?" Only draft if yes — never unprompted.
   **REQUIRED SUB-SKILL:** `prose` governs the drafted text. Never post
   it; posting is always a separate, later, manual action outside this
   skill.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Applying a suggested fix without confirming the concern is real | Validate first; add a test if it would help confirm |
| Adding the confirming test after the fix instead of before | Test-first — it's the reproduction step, not an afterthought |
| Committing/pushing after each individual fix | One push, after all comments are processed |
| Posting a reply directly to a review thread | Never — draft only, and only when asked |
| Drafting a response before being asked | Ask per comment first; draft only on yes |
| Processing a resolved thread or an already-answered comment | Filter those out before validation |
| Fetching only the two comment endpoints and reporting "no comments" | Review bodies are a third source; check `pulls/{pr}/reviews` too |
| Trusting a review's own "generated no new comments" summary | Its body may still hide findings in a collapsed `<details>` block |
| Assuming a review body finding is handled because threads are resolved | Body findings have no thread to resolve; check the code instead |
