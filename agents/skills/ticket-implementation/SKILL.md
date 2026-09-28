---
name: ticket-implementation
description: Use as a base for skills that implement a specific ticket or issue — invoked by jira-ticket-implementation, github-issue-implementation, and similar skills, not directly for a specific tracker. The `implementer` sub-agent runs it for the Implementing and Review - Local Bot phases.
---

# Ticket Implementation

## Overview

Shared workflow for implementing a ticket once its system, type (bug vs.
feature/task), title, and description are already resolved: reproduce
bugs before fixing them, use or build a plan before implementing, and
stay scoped to the ticket rather than drive-by fixing anything else. It
delegates to existing skills for the mechanics rather than
reimplementing them.

## Orchestration and model weight

Work runs in two top-level sessions plus two sub-agents. **Planning is a
dedicated top-level session** so the user can interact with it directly.
It runs on the **heavy model** (GLM 5.2); the user's long-running
**conductor** session runs the **light model** and never does the heavy
reasoning itself.

| Phase | Who does it | Model | Output to disk |
|---|---|---|---|
| Planning | Top-level session | Heavy | PLAN.md in the checkout root |
| Implementing | `implementer` sub-agent | Light | Working tree and commits |
| Review - Local Bot | `reviewer` sub-agent, invoked by `implementer` | Heavy | `.opencode/REVIEW.md` |
| Review - Self | Conductor | Light | Draft PR to the fork |
| Review - Automated tools | Conductor | Light | Push toward the upstream PR |
| Review - Team | Conductor | Light | Coordinate with the team |

The `reviewer` sub-agent cannot hand results through shared memory. The
`implementer` sub-agent runs it, then reads `.opencode/REVIEW.md`,
addresses the findings, and reports back; the conductor confirms the
report before continuing. Sessions end between the Planning session and
the Implementing session: the planning session writes PLAN.md and ends;
the conductor starts fresh, reads PLAN.md, and dispatches the
`implementer` sub-agent.

## Work file locations

Ticket work products live at fixed paths in the checkout — no directory
resolution, no per-branch subdirectories:

- `PLAN.md` (repo root) — the plan the dedicated Planning session drafts.
- `.opencode/REVIEW.md` — the review the `reviewer` sub-agent writes.
- `.opencode/LEDGER.md` — the ticket **ledger** (see below).
- `.opencode/NOTES.md` — your own notes. You write it; skills create it
  empty on first use.
- `.opencode/REVIEW_STATE.md` — the PR review state the `pr-review`
  agent maintains: the watermark and each handled comment or check. It
  carries across sessions, unlike the ledger, which resets per ticket.
  See `pr-review` for the format.

`.opencode/` is gitignored, and PLAN.md is excluded from git locally
(`.git/info/exclude`), so plans, reviews, ledgers, notes, and review
state are never committed. Never `git add` PLAN.md.

### Ticket ledger and notes

Each ticket keeps two files in `.opencode/` alongside the review:

- `.opencode/LEDGER.md` — the ticket **ledger**. Skills auto-manage it.
  It carries the ticket's metadata (branch, system, key, type, title), a
  **session checklist** with one item per phase of the workflow, and the
  **next suggested user action** so a fresh session knows what to do.
  Check an item off as its phase completes, so progress survives session
  boundaries; update the next action whenever a phase completes or
  blocks.
- `.opencode/NOTES.md` — your own note file. You write to it directly;
  skills leave it alone except to create it empty on first use.

The ledger is reset/re-initialized at the start of each ticket.

Ledger format:

```markdown
# Ledger: <checkout-dir>

Git checkout: `<abs path>`
Branch: `<branch>`
System: `JIRA`/`GitHub`
Key: `PROJ-1234`
Type: `bug`/`feature`
Title: `<title>`
Plan: `PLAN.md`
Review: `.opencode/REVIEW.md`
Ticket: `<URL>`
Fork PR: `<URL>`
Upstream PR: `<URL>`

## Next suggested user action

`<short, imperative next step>` — e.g. run the Planning phase, open the
draft fork PR, drive the upstream PR to merge.

## Session checklist
- [ ] Planning — PLAN.md written
- [ ] Implementing — tasks complete and verified
- [ ] Review - Local Bot — REVIEW.md written and addressed
- [ ] Review - Self — draft fork PR opened
- [ ] Review - Upstream and Team — PR driven to merge
```

Fill the link fields as each becomes available: **Ticket** from the
connector or `gh issue view` when the ticket is resolved, **Fork PR**
when the draft PR to your fork is opened, and **Upstream PR** when the
upstream PR is opened. Leave a field blank until its link exists; `n/a`
where there is no such artifact (e.g. no separate fork).

Keep **Next suggested user action** current: rewrite it whenever a phase
completes or the work pauses, so a later session (or the user) picks up
exactly there. Leave it blank on first initialization before the first
phase starts.

## Workflow

1. **Set up the ledger and notes.** At the start of work on a ticket in
   a checkout, (re)write `.opencode/LEDGER.md` with the ticket's
   metadata (including the **Branch** and the **Ticket** link once
   resolved) and a fresh session checklist, and create
   `.opencode/NOTES.md` empty if it does not exist. Flip a checklist
   item to `[x]` as its phase completes, record the relevant PR link
   alongside (steps below), and update **Next suggested user action**
   to the next phase.
2. **Bug path — reproduce first.** If this is a bug, write a test that
   reproduces it and confirms it fails, before any other work.
   **REQUIRED SUB-SKILL:** `test-driven-development` governs the
   RED-GREEN-REFACTOR cycle from here on, for both the bug and feature
   paths. If the bug/feature determination is missing, ask before
   proceeding.
3. **Resolve the plan.** The plan is a local markdown file at the repo
   root, `PLAN.md`. It is not a gist.
   - PLAN.md exists: read it and treat it as the implementation plan.
   - PLAN.md is missing: in the **Planning** phase (the heavy top-level
     session), draft it and write it to the repo root. In the
     **Implementing** phase, do not draft a plan: **ask the user to
     create one** and pause until they do or supply a path. Say it
     plainly, for example:

      > No PLAN.md at the repo root. Run the Planning phase on the
      > heavy model (GLM 5.2) in a separate session, save the plan to
      > `PLAN.md` there, then resume here. I'll wait.
4. **Implement.** **REQUIRED SUB-SKILL:** `executing-plans` to work
   the plan task by task, with `test-driven-development` governing how
   each piece of code gets written. Where the work adds or edits a
   docstring, **REQUIRED SUB-SKILL:** `docstrings` governs it. For any
   other prose produced along the way (commit messages, code comments,
   status updates) not covered by a more specific skill, **REQUIRED
   SUB-SKILL:** `prose` governs it directly. When the plan is fully
   implemented and verified, check off **Implementing** in the ledger.
5. **Scope discipline.** If something unrelated to the ticket surfaces,
   don't fix it. Flag it: offer to draft a ticket for it. If a new
   ticket is needed, print the general requirements and hand off so the
   user can file it (see `designing`'s orchestrator mode). Keep working
   the original ticket regardless of the answer.
6. **Hand off for review.** Review is staged; this skill ends at the
   fork PR.
   - **Review - Local Bot (heavy).** The `implementer` sub-agent
     dispatches the `reviewer` sub-agent, which writes
     `.opencode/REVIEW.md`; the implementer reads it, addresses it, and
     reports back. The conductor confirms the report before moving on.
     When REVIEW.md is written and addressed, check off **Review -
     Local Bot** in the ledger and set the next action to open the
     draft fork PR.
   - **Review - Self (light).** Before opening the draft PR to the
     fork, offer to make a targeted evergreen patch build — ask the
     user rather than triggering a CI build unprompted. Then open a
     draft PR to the user's fork — for security bugs, a **private GHSA
     fork**. **REQUIRED SUB-SKILL:** `pr-creation` governs opening it
     (which uses `pr-description` for the content) — don't invoke
     `pr-description` directly and skip `pr-creation`'s mechanics. When
     the draft PR is open, record its **Fork PR** URL in the ledger,
     check off **Review - Self**, and set the next action to start the
     code-review session.
   - **Review - Upstream and Team (light).** After the fork PR, stop.
     The upstream PR, bots, automated tools, and team review run in a
     separate session: **REQUIRED SUB-SKILL:** `code-review`. Set the
     next action to start that session.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Fixing a bug before writing a failing reproduction test | Reproduce first, always |
| Starting to code before resolving a plan (PLAN.md or `writing-plans`) | Resolve the plan first |
| Fixing an unrelated issue found mid-work | Flag it, offer a ticket, keep scope |
| Auto-producing a plan in the Implementing phase when none exists | Ask the user to create it; pause until they do |
| Doing heavy reasoning in the conductor session | Run it in the dedicated heavy Planning session, or delegate to the sub-agents |
| Continuing before the reviewer sub-agent wrote REVIEW.md | Read `.opencode/REVIEW.md` and confirm it exists first |
| Treating the plan as a gist to publish | Plans live at the repo root as `PLAN.md`, not a gist |
| Re-explaining a sub-skill's process inline instead of invoking it | Invoke the sub-skill; don't duplicate its process here |
| Invoking `pr-description` directly to open the PR | Invoke `pr-creation` instead — it handles the description via `pr-description` itself |
| Skipping `/review` or addressing review comments without user sign-off | Run the staged review loop; the user owns responses |
| Writing PLAN.md anywhere but the repo root, or the other files outside `.opencode/` | PLAN.md at the root; REVIEW.md, LEDGER.md, NOTES.md, and REVIEW_STATE.md in `.opencode/` |
| Committing a work product | `.opencode/` is gitignored and PLAN.md is locally excluded; never `git add` either |
| Leaving the session checklist unchecked as phases finish | Flip each item to `[x]` when its phase completes; the ledger is the durable progress record |
