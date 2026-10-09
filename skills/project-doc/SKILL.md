---
name: project-doc
description: "Write a project doc with the user before any design is settled or any code is written: problem and scope, breakdown, decisions the user makes, then an implementation plan. Use for /project-doc, when starting a new project or design, when scoping a project before building, or when returning to an in-progress project doc in docs/."
---

# Project doc

The user scopes the problem and makes every architectural call. You ask, propose options, and teach. They weigh the reasoning and decide. You do not write implementation code.

A doc can take several sessions, up to about a week. A new chat does not remember the last one. The project doc is the memory.

## Files

- Template: [template.md](template.md), next to this skill.
- Project doc: `docs/<project-name>.md` in the project being designed. `<project-name>` is kebab-case. A project doc is a file there that has `## Decision log`.

The first time you create a project doc, add the rule below to that project's root `AGENTS.md` if it is not already there. Create `AGENTS.md` if the project has none. If the rule is already present, leave it.

## Rule

Do not implement a project until it has an approved project doc at `docs/<project-name>.md`. Read that doc before writing code. If the plan changes, update the decision log first: add a new entry, mark the old one superseded, and do not delete it. Then update the plan.

## Across sessions

Write the file in the same turn as the agreement, before you ask the next question. That includes an accepted answer, an options list, a decision entry, a sign-off, and a plan change.

On every write, set `## Progress` to the current phase and what is still open.

On resume, read the file and trust it over the chat. Summarize the phase, the last sign-off, and what is still open, then continue from the first open item.

## Start

1. If the user names a doc, or asks to continue, read that file. If more than one project doc exists and they did not name one, list the paths and ask which. Leave the choice to them.
2. **Resuming.** Summarize from the file: current phase, last sign-off, and what is still open (empty sections, a phase with no sign-off line, or a decision whose status is `open`). Continue from the first open item.
3. **New.** Confirm a short name. Copy the template to `docs/<project-name>.md`, set the title, set Status to `draft`, set Progress, and add a change-history line with today's date.

## Holds for every phase

- Stay on the current phase until the user signs off.
- Ask one or two questions at a time, then wait.
- These fields stay in the user's words: the problem, who it is for, constraints, non-goals, success criteria, My decision, My reasoning, and What I learned. Fix spelling. Leave their meaning alone. If you tighten a sentence, show the line and ask whether it still says what they meant.
- An answer is too vague to keep when a builder still could not tell what to build, who it is for, or how to know it worked. Name which of those is missing, and ask again. "Users", "make it better", "fast", "simple", and "robust" fail that test unless they name a check you could apply.
- Teach in a few sentences tied to their problem: what the choice means, what it costs, and what breaks if it is wrong.
- If they ask to start building, read Status. Building waits until they have set it to `approved`. Say what is still open, and stay on the doc.

## 1. Problem and scope

Fill Problem, Scope and non-goals, Constraints, and Success criteria.

This phase is open until the doc states, in their words:

- the problem
- who it is for
- the constraints
- the non-goals
- what done means

When those are filled, summarize them briefly and ask for a sign-off. On sign-off, add `YYYY-MM-DD — Phase 1 signed off.` to Change history.

## 2. Breakdown

Propose a split into subsystems or components, plus the interface between pieces that need to talk. Keep the proposal short enough to argue with.

Ask them to check the boundaries: one responsibility each, nothing important left out, nothing split across two pieces by accident.

Revise until they sign off. Write the agreed breakdown into the doc. On sign-off, add `YYYY-MM-DD — Phase 2 signed off.` to Change history.

## 3. Decisions

Walk every component in the breakdown, including nested pieces you agreed to split.

Log a decision when the other choice would change the breakdown, an interface, or what a later step has to build. Skip naming, formatting, and choices with one reasonable option. Under that component, record each skip in one line so it stays visible.

For each decision, in order:

1. Give two or three options. For each option: what it is, the tradeoff, and when it fits. Then one recommendation and the reasoning behind it. That recommendation is advice. Write the options and the recommendation into the log before you stop.
2. Stop. They supply their pick, why they picked it, and one line on what they learned.
3. Challenge weak reasoning. Weak means it only restates the option, ignores a tradeoff you named, or does not connect to their problem. Say which, and ask them to revise. Leave the replacement sentence to them.
4. Finish the log entry. You write Date, Context, Options, and AI recommendation. They own My decision, My reasoning, and What I learned. Set Status to `decided`. IDs are `D1`, `D2`, and never change.

Finish the current decision before opening the next one. Start the plan after every level of the breakdown has its decisions, or a one-line skip. If you are unsure a level is finished, ask.

On sign-off, add `YYYY-MM-DD — Phase 3 signed off.` to Change history.

## 4. Implementation plan

Write ordered steps. Each step names the decision IDs it depends on, or `none`, and how someone will know the step worked. The check is something a person can run or observe.

Read the plan back and ask them to sign off. On sign-off, add `YYYY-MM-DD — Phase 4 signed off.` to Change history, and restate the change rule in two sentences.

Status stays `draft` until they ask for `in review`. Set `approved` only after they say it is approved.

## 5. Change rule

Phase 5 is the rule for later edits. When the plan has to change after it was written:

1. Add a new decision-log entry for the new choice, including their reasoning and what they learned.
2. Set the old entry's status to `superseded by D<n>`. Leave the old decision text in place.
3. Update the plan so its steps point at the new ID.
4. Add a change-history line.

Put non-blocking unknowns in Open questions. An architectural choice stays in the decision log.

## Where to resume

Read the file before asking anything new.

| The doc shows | Continue in |
|---|---|
| Problem, users, constraints, non-goals, or done still missing, or no phase 1 sign-off | Phase 1 |
| Breakdown missing, or no phase 2 sign-off | Phase 2 |
| A component with neither decisions nor a one-line skip, or any entry still `open` | Phase 3 |
| Plan missing, a step without decision IDs and a check, or no phase 4 sign-off | Phase 4 |
| Phase 4 signed off, Status still `draft` or `in review` | Wait until they set `approved` |
| Status `approved`, and they want the plan to change | Phase 5, then edit the plan |
