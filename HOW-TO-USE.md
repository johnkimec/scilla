# How to use these skills

Temporary. This file is a guide while the commands are still unfamiliar. Delete it when you no longer need it.

You install the skills into the project you are building. You then type a command in a new agent chat in that project. The agent reads the skill and does the steps. You stay in the chat and answer.

## Install them in a fresh project

Open a terminal in the fresh project, not in this repo.

```bash
npx skills add johnkimec/scilla#v0.2.0 --agent cursor -y
```

That installs every skill for Cursor. Swap `cursor` for `claude-code` or `codex` if that is the agent you use.

One skill only:

```bash
npx skills add johnkimec/scilla#v0.2.0 --skill project-doc --agent cursor -y
```

Every project on this machine:

```bash
npx skills add johnkimec/scilla#v0.2.0 -g --agent cursor -y
```

The `#v0.2.0` part pins this release. A later push to the repo will not change what you installed.

Start a new agent chat after installing. An old chat will not see the new skills.

## What to run, and when

Use them in this order on a new project.

1. `/project-doc` before any design or code. This can take several sessions.
2. Build only after that doc says `approved`.
3. `/build-from-example` when a working example already exists for the thing you are building.
4. `/walkthrough` when you are lost in code that already exists.
5. `/compound` at the end of a task, when the task taught you a fact the next task will need.
6. `/create-verification-skill` once the system actually runs and you want a scripted way to prove it.
7. `/maintain-verification-skill` later, when the system has changed and the verification notes may be stale.
8. `/eval` only when you are changing a skill or a prompt and you want to know whether agents behave differently. Skip it while you are building the product.

`/project-doc` can also start on its own when you say you are starting a project or a design. The other commands start when you type them.

## `/project-doc`

Writes the design for the whole project before any code: the problem, the boundaries, the decisions you make, and the plan.

**You type:** `/project-doc` and one sentence about the project. Example: `/project-doc I want to build a notes app for myself.`

**The agent does:** Confirms a short name. Creates `docs/<project-name>.md` from a template and sets Status to `draft`. The first time, it also adds a rule to the project's root `AGENTS.md`, and creates that file if the project has none. Then it asks you questions.

**You do:** Answer in your own words. Expect one or two questions at a time. Vague answers get sent back. You sign off on each phase before the next one starts. A full doc can take several chats across a week.

The phases, in order:

1. **Problem and scope.** The problem, who it is for, constraints, non-goals, and what done means. You sign off.
2. **Breakdown.** The agent proposes the pieces and how they talk to each other. You check the boundaries and sign off.
3. **Decisions.** For each real architectural choice, the agent gives two or three options, the tradeoff, and a recommendation. You record your pick, why, and one line on what you learned. A thin reason gets challenged. You rewrite it yourself.
4. **Plan.** Ordered steps. Each step names the decisions it depends on and how you will know it worked. You sign off.
5. **Later changes.** If the plan has to change, the agent adds a new decision and marks the old one superseded. The old text stays. Then it edits the plan.

Status stays `draft` until you say "mark it in review" or "this is approved." Only you set `approved`. If you ask the agent to start building before that, it should stop and tell you what is still open.

**Coming back another day.** Open a new chat and type `/project-doc continue docs/<project-name>.md`. The new chat does not remember the old one. The file does. The agent reads it, tells you the phase and what is still open, and continues there. Commit the doc when you stop for the day so the file is not only in your working copy.

**You get:** `docs/<project-name>.md`, and a short rule in `AGENTS.md`.

## `/build-from-example`

Builds a change by following code that already works, instead of inventing a new design.

**Use it when** you can point at a file, a path, a URL, another repo, or a behavior this repo already has. Example: "the export command" or "this GitHub file."

**You type:** `/build-from-example` plus the example and what you want. Example: `/build-from-example Add a delete command that works like the existing create command.`

**The agent does:** Opens the real source. For a URL, it fetches the raw file. If the example is another repository, it clones that repo into `/tmp`, follows the relevant part, and leaves the clone out of your commit. New files go where this repo already keeps that kind of file. If it cannot find a working example, it stops and says so.

**You do:** Name the example. If you have more than one, name all of them. Read the diff before you commit, and check that `/tmp` copies are not in `git status`.

**You get:** The new work in your repo, and a reply that names each example file it followed.

## `/walkthrough`

Explains a codebase in one document, in order, with every code snippet printed by a command from the files on disk.

**Use it when** you want to understand how the code actually works, or you want a tour of one file or one area.

**You type:** `/walkthrough`, or `/walkthrough the save path` if you want to stay inside one area.

**The agent does:** Reads the code, picks one path from the start of the story to the end, and writes `walkthrough.md` at the repo root. Commentary and snippets alternate. Each snippet is produced by a command (`sed`, `grep`, `cat`, and similar) through Showboat, so the document shows the bytes on disk. It checks the document with `uvx showboat verify walkthrough.md`.

**You need:** `uv` installed, so `uvx showboat` can run. The first run may download Showboat.

**You do:** Read `walkthrough.md`. If a `walkthrough.md` is already in the repo, the agent will ask before replacing it.

**You get:** `walkthrough.md` at the repo root.

## `/compound`

After a task, saves one lasting lesson into `AGENTS.md` so the next agent starts with it.

**Use it when** a finished task revealed a command, a path, or a constraint that already caused a wrong change. Skip it when all you have is status or "here is where we stopped."

**You type:** `/compound` at the end of the task.

**The agent does:** Keeps one concrete sentence. Writes it to `AGENTS.md` at the repo root, or to a subdirectory `AGENTS.md` when the lesson is only true there. If the file already says it, it leaves the file alone. If there is no lasting lesson, it says so and stops. It does not create a skill or any other file.

**You do:** Read the sentence it quotes back. If it saved a status update instead of a fact the next task needs, say so.

**You get:** One new or replaced line in `AGENTS.md`, or a report that nothing was added.

## `/create-verification-skill`

Builds a project-local skill that launches your system and drives it the way a person would, then records how to prove each user-facing behavior.

**Use it when** the system runs: a software app, firmware on a board, an FPGA design, a simulator, or a lab bench. Use it after there is something real to drive. A repo that does not build or start yet gets that fixed first.

**You type:** `/create-verification-skill`

**The agent does:** Learns the system from the repo. It asks you only what it cannot see. It writes `.cursor/skills/verify-<target>/SKILL.md` with the launch command, a health check, how to drive the system, what evidence to capture, and how to clean up. It also writes a feature map: `.cursor/skills/verify-<target>/features/README.md` plus one file per user-facing behavior (it starts with the top few). Each feature file says what the behavior is, how a person reaches it, the commands that drive it, and the traps. Then it runs that skill once: launch, drive one mapped behavior, capture evidence, clean up, and check the evidence is still there.

**You do:** Answer the questions it cannot answer from the repo (a serial port, a login, a board that is not on the desk). Let it drive the real system once. Read the feature file it produced and correct anything a person would not actually do.

**You get:** A `verify-<target>` skill and a feature map inside the project. The map is a verification recipe. It is separate from `docs/<project-name>.md`, which is the design you wrote before building.

## `/maintain-verification-skill`

Checks the feature map against the current system and drives every mapped behavior once.

**Use it when** the system has changed and you want to know whether the verification skill is still true. Run `/create-verification-skill` first if the project has no verification skill.

**You type:** `/maintain-verification-skill`

**The agent does:** Reads every feature file, compares it with the source, then drives every feature on the running system. It only edits the verification skill's own files. If the product itself is broken, it does not fix the product in that run. When the repo has a test suite, it can add one failing test for that break, on a separate change. It finishes with one of three results: `clean` (nothing to change), `changed` (one set of proven corrections), or `blocked` (it says exactly what stopped it).

**You do:** Let it launch and drive the system. If it reports `blocked`, the message names the missing piece (auth, a probe, a cable, a board). Fix that, then run it again.

**You get:** An updated feature map, or a clear statement that it was already right, plus any failing test it added for a real product break.

## `/eval`

Runs a blinded check of whether a change to a skill, a file layout, or a prompt actually changes what agents do.

**Use it when** you are about to keep or reject a change to how agents work. Skip it for ordinary product work.

**You type:** `/eval` and what you want to compare. Example: `/eval Does the new project-doc skill make the agent ask me to decide, instead of writing the decision for me?`

**The agent does:** Writes a private rubric with a few concrete checks. Sets up a separate directory per candidate, with the change under test and a normal-looking task. The candidates do not see the rubric, and they are not told they are in a test. It runs two candidates on different model families, then one judge scores the outputs without being told which model wrote them. It also reads the transcripts to see which files each candidate opened. Then it compares the judge's verdict with its own reading.

**You do:** Say what behavior would count as success, in concrete terms. Read the final report before you keep the change. If the judge and the lead agent disagree, the report should say whether the rubric was fuzzy or the judge was biased.

**You get:** A report with the rubric, notes on each candidate, the judge's verdict, and a recommendation to keep the change or not. You do not get a product feature.
