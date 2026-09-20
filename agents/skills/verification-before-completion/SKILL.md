---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs. Requires running verification commands and confirming output before making any success claim.
---

# Verification Before Completion

## Attribution

Adapted from [obra/superpowers](https://github.com/obra/superpowers) (MIT
License); repo tooling adapted to this setup.

## Overview

**Core principle:** evidence before claims, always. If you have not run
the verification command in this session, you cannot claim it passes.

**Violating the letter of this rule is violating the spirit of this
rule.**

## The Iron Law

```
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not run the verification command in this message, you cannot
claim it passes.

## The gate function

Before claiming any status or expressing satisfaction:

1. **Identify** the command that proves the claim.
2. **Run** the full command, fresh and complete.
3. **Read** the full output, check the exit code, count failures.
4. **Verify** the output confirms the claim.
5. **Only then** make the claim. If it does not confirm, state the actual
   status with evidence.

Skip any step and you are lying, not verifying.

## Common failures

| Claim | Requires | Not sufficient |
|---|---|---|
| Tests pass | `just test` output: 0 failures | A previous run, "should pass" |
| Lint clean | Lint output: 0 errors | A partial check, extrapolation |
| Bug fixed | Original symptom test passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | The test passes once |
| Agent completed | VCS diff shows the changes | The agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red flags: stop

- Using "should", "probably", "seems to"
- Expressing satisfaction before verifying ("Great!", "Perfect!",
  "Done!")
- About to commit, push, or open a PR without verification
- Trusting an agent's success report
- Relying on partial verification
- Thinking "just this once"
- Any wording implying success without having run verification

## Rationalizations

| Excuse | Reality |
|---|---|
| "Should work now" | Run the verification |
| "I'm confident" | Confidence is not evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Lint is not a compile or test check |
| "The agent said success" | Verify independently |
| "A partial check is enough" | Partial proves nothing |

## Key patterns

**Tests:** run `just test` (or `just test -- <path>` for one file), see
the pass count, then state it. Do not say "should pass now".

**Regression test (TDD red-green):** write it, run it (pass), revert the
fix, run it (must fail), restore the fix, run it (pass). Without the
red-green verification there is no regression test.

## Apply

Always, before: any success or completion claim, any expression of
satisfaction, any positive statement about the work, committing, opening
a PR, marking a task complete, moving to the next task, or delegating to
a sub-agent.
