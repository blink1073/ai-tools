---
name: github-actions-security
description: Use when editing GitHub Actions workflow files (.github/workflows/*.yml).
---

# GitHub Actions Security

When editing GitHub Actions workflow files (`.github/workflows/*.yml`):
- Always include `persist-credentials: false` in every `actions/checkout` step
- Apply this to all jobs, not just specific ones
- When a third-party action is pinned to a SHA (e.g. `owner/action@abc1234 # v1.2.3`),
  verify that the SHA actually corresponds to the version in the comment — look up the
  action's tags/releases to confirm they match before accepting or making changes
