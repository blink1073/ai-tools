---
name: test-driven-development
description: Use when implementing any feature or bug fix, before writing implementation code.
---

# Test-Driven Development (TDD)

## Core principle

Write the test first. Watch it fail. Write the minimal code to pass. If
you did not watch the test fail, you do not know it tests the right
thing. This repo is Python with pytest; run tests through the repo's
`just` recipes (`just test`, or `just test -- <path>` for one file).

Say so at the start: "I'm using the test-driven-development skill."

## The Iron Law

```
NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST
```

Write code before the test? Delete it and start over. No exceptions: do
not keep it as reference, do not adapt it while writing tests, do not
look at it. Delete means delete.

Exceptions, ask the user first: throwaway prototypes, generated code,
configuration files.

## Red-Green-Refactor

### Red: write the failing test

One test, one behavior, a clear name that states the behavior. Use real
code; use a mock only when unavoidable.

Good example (pytest):

```python
def test_retries_failed_operations_three_times():
    calls = 0

    def operation():
        nonlocal calls
        calls += 1
        if calls < 3:
            raise RuntimeError("transient")
        return "success"

    assert retry(operation, attempts=3) == "success"
    assert calls == 3
```

Prefer plain assertions with the repo's style. Name the production
change that would make the test fail, before writing it.

### Verify Red: watch it fail

Run the test. Confirm it fails for the reason you expect: the feature is
missing, not a typo or an import error. If it passes, you are testing
existing behavior; fix the test. If it errors, fix the error and rerun.
Never skip this.

### Green: write the minimal code

Write the simplest code that passes the test. Do not add features,
refactor unrelated code, or "improve" past the test (YAGNI). Run the
test, confirm it passes and the other tests still pass.

### Refactor: clean up

Only after green. Remove duplication, improve names, extract helpers.
Keep the tests green. Do not change behavior.

## Verify

Before marking work complete, confirm every item:

- Every new function or method has a test.
- Each test was watched to fail before implementing.
- Each failure was for the expected reason.
- Minimal code was written to pass each test.
- All tests pass, output clean (no errors, warnings).
- Tests use real code; mocks only where unavoidable.
- Edge cases and errors are covered.

Cannot check every item? You skipped TDD. Start over.

## When stuck

| Problem | Solution |
|---|---|
| Do not know how to test | Write the wished-for output, write the assertion, ask the user |
| Test too complicated | The design is too complicated; simplify the interface |
| Must mock everything | The code is too coupled; use dependency injection |
| Huge test setup | Extract a helper; if still complex, simplify the design |

## Debugging

A bug found? Write the failing test that reproduces it, then follow the
cycle. The test proves the fix and prevents regression. Never fix a bug
without a test.

## Rationalizations to reject

"Too simple to test", "I'll test after", "I already tested manually",
"Deleting hours of work is wasteful", "Keep it as reference", "TDD is
dogmatic, I'm being pragmatic", "Just this once". All of these mean:
delete the code and start over with TDD.

## Final rule

Production code exists only when a test failed first. No exceptions
without the user's permission.
