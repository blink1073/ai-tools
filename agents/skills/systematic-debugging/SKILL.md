---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
---

# Systematic Debugging

## Attribution

Adapted from [obra/superpowers](https://github.com/obra/superpowers) (MIT
License); method kept, tool and workflow references adapted to this
setup.

## Overview

**Core principle:** find the root cause before attempting any fix. A
symptom fix is a failure.

**Violating the letter of this process is violating the spirit of
debugging.**

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you have not completed Phase 1, you cannot propose a fix.

## When to use

Use for any technical issue: test failures, bugs, unexpected behavior,
performance problems, build failures, integration issues. Use it
especially when time is short, a fix "just" seems obvious, you have
already tried several fixes, or you do not fully understand the issue.
Do not skip it because the issue looks simple.

## The four phases

Complete each phase before the next.

### Phase 1: root cause investigation

Before attempting any fix:

1. **Read the error messages carefully.** Read stack traces to the end.
   Note line numbers, file paths, and error codes.
2. **Reproduce consistently.** Trigger it reliably, identify the exact
   steps, check it happens every time. If you cannot reproduce it,
   gather more data; do not guess.
3. **Check recent changes.** Git diff and recent commits, new
   dependencies, config changes, environment differences.
4. **Gather evidence in multi-component systems.** When the system has
   more than one component, add diagnostics at each boundary before
   proposing a fix: log what enters and exits each component, verify
   environment and config propagation, check state at each layer. Run
   once to show where it breaks, then investigate that component.
5. **Trace data flow.** Find where the bad value originates, what called
   it, and keep tracing upward to the source. Fix at the source, not at
   the symptom.

### Phase 2: pattern analysis

1. **Find a working example.** Locate similar code that works.
2. **Compare against a reference.** Read the reference implementation
   fully, not skimmed.
3. **Identify the differences.** List every difference between working
   and broken; do not assume any "cannot matter".
4. **Understand the dependencies.** Know what settings, config, and
   environment the code needs and assumes.

### Phase 3: hypothesis and testing

1. **Form one hypothesis.** State it clearly: "X is the root cause
   because Y". Be specific.
2. **Test minimally.** Make the smallest possible change, one variable at
   a time. Do not fix multiple things at once.
3. **Verify before continuing.** Worked? Go to Phase 4. Did not work?
   Form a new hypothesis; do not stack more fixes.
4. **When you do not know,** say so, ask for help, and research more. Do
   not pretend.

### Phase 4: implementation

1. **Create a failing test.** Use the `test-driven-development` skill to
   write a proper failing test before fixing.
2. **Implement one fix.** Address the root cause; one change at a time;
   no "while I'm here" improvements or bundled refactoring.
3. **Verify the fix.** Use the `verification-before-completion` skill
   before claiming success.
4. **If the fix does not work,** stop. Count attempts. Under three,
   return to Phase 1 with the new information. At three or more, stop
   and question the architecture (below), do not attempt a fourth fix
   without that discussion.

### When three or more fixes fail: question the architecture

A pattern that signals a wrong architecture: each fix reveals new shared
state or coupling; fixes need massive refactoring; each fix creates new
symptoms elsewhere. Stop and question whether the approach is sound, or
whether refactoring beats continuing to fix symptoms. Discuss it with
the user before attempting more fixes. This is not a failed hypothesis;
it is a wrong architecture.

## Red flags: stop and follow the process

Stop and return to Phase 1 when you catch yourself thinking:

- "Quick fix for now, investigate later"
- "Just try changing X and see"
- "Add several changes and run the tests"
- "Skip the test, I'll verify manually"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- Naming fixes before tracing the data flow
- "One more fix attempt" after two or more have failed

## Common rationalizations

| Excuse | Reality |
|---|---|
| "Issue is simple, no process needed" | Simple issues have root causes too. The process is fast for simple bugs. |
| "Emergency, no time" | Systematic debugging is faster than guess-and-check thrashing. |
| "I'll test after confirming the fix" | Untested fixes do not stick; test first proves it. |
| "Multiple fixes at once saves time" | You cannot isolate what worked, and it causes new bugs. |
| "I see the problem, let me fix it" | Seeing a symptom is not understanding a root cause. |
| "One more fix attempt" after 2+ failures | Three or more failures means an architectural problem. |

## Quick reference

| Phase | Key activities | Success |
|---|---|---|
| 1. Root cause | Read errors, reproduce, check changes, gather evidence | Understand what and why |
| 2. Pattern | Find working examples, compare | Identify differences |
| 3. Hypothesis | Form theory, test minimally | Confirmed or new hypothesis |
| 4. Implementation | Create test, fix, verify | Bug resolved, tests pass |
