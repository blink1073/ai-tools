---
name: executing-plans
description: Use when implementing a written plan (PLAN.md) in the conductor session, task by task with checkpoints.
---

# Executing Plans

## Goal

Work a written implementation plan task by task in the **conductor**
session (light model), verifying each step and stopping when blocked.
The plan is `<work>/PLAN.md` in the ticket work directory (resolve
`<work>` per `ticket-implementation`).

Say so at the start: "I'm using the executing-plans skill to implement
this plan."

## Step 1: Load and review the plan

1. Resolve `<work>` and read `<work>/PLAN.md`.
2. Review it critically. Name any questions or concerns.
3. If you have concerns, raise them with the user before starting. Do
   not guess past a gap.
4. If the plan is sound, create a todo list with one entry per task.
   The ticket ledger at `<work>/LEDGER.md` should already carry this
   ticket's metadata and a fresh session checklist (set up by the
   Planning session); if it does not exist, create it and `<work>/NOTES.md`
   now, using the `ticket-implementation` format. You may jot progress
   in `<work>/NOTES.md`, but leave the notes file's content to the user.

## Step 2: Execute the tasks

For each task:

1. Mark it in progress.
2. Follow each step exactly. The plan has bite-sized steps; run each
   verification it specifies.
3. Mark the task complete only after its verification passes.

## Step 3: Finish

When all tasks are complete and verified, check off **Implementing** in
the ticket ledger (`<work>/LEDGER.md`), stop coding, and hand off to the
review stage. Follow the staged review loop in
`ticket-implementation` (Review - Local Bot, then Self, then Automated
tools, then Team). Do not start the next phase on your own.

## Stop and ask

Stop immediately, and ask the user rather than guessing, when:

- You hit a blocker: missing dependency, test failure, unclear step.
- The plan has a gap that prevents starting.
- You do not understand an instruction.
- A verification fails repeatedly.

Return to step 1 to re-review the plan when the user updates it, or when
the approach needs rethinking. Do not force through a blocker.

## Remember

- Review the plan critically first; raise concerns, do not guess.
- Follow the plan steps exactly; do not skip verifications.
- Reference the skills the plan names, and use test-driven-development
  for each new feature or bug fix.
- Stop when blocked; the user owns the decision.
