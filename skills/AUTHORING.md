# Writing a skill

Read this before you add or change a skill in `skills/`. [AUDIT.md](AUDIT.md) scores the current skills against the same bar.

A skill is a folder with a `SKILL.md`. Agents load it in three steps. Write each step so the one that is always in context stays small, and the one that runs the task stays exact.

## What loads when

| Tier | What | When it loads | Keep it |
|---|---|---|---|
| Catalog | `name` and `description` | Every session, for every installed skill | The trigger. About 100 tokens. |
| Instructions | `SKILL.md` body | After the description matches, or the user types the command | The steps for a normal run. Under 500 lines. |
| Resources | `references/`, `assets/`, `scripts/` | When a step says to read or run that file | The branch, the template, or the check. |

```
skill-name/
├── SKILL.md          # required
├── references/       # read on a named branch
├── assets/           # copy into the output (templates)
└── scripts/          # run; the source stays out of context
```

`name` matches the folder. Lowercase letters, numbers, and single hyphens. It does not start or end with a hyphen, and it has no `--`. Sixty-four characters is the limit.

`description` is 1–1024 characters. It says what the skill does and when to use it.

The body stays under 500 lines, and under about 5,000 tokens, because the whole file sits in context once the skill starts. Move a section out when a run needs it only on one branch, and name the condition in `SKILL.md`: "Read `references/aws.md` when the target is AWS." A file you only mention as "see references/" gets skipped, or it gets loaded every time.

Link one level deep from `SKILL.md`. A reference that points at another reference gets half-read.

`scripts/` are for running. Say "run `scripts/check.py`" when the agent should execute it. Say "read it" only when the agent has to change the script. The useful output is the script's stdout. The source does not need to enter context.

`assets/` holds a file the skill copies, such as a template. `references/` holds a document the agent reads. A short template that every run needs can live in the body.

The user-facing page for a command is `HOW-TO-USE.md`, plus the tables in `README.md` and `skills/README.md`. A skill folder is for the agent. Leave README, changelog, and install notes out of it.

`disable-model-invocation: true` is a Cursor field. It makes the skill a slash command there. Claude Code and Codex do not read that field, and the description is the trigger on those hosts. Write the description so a host that ignores the flag still starts the skill on the right requests. In this repo, `/project-doc` and `/socratic-tutor` are meant to start from the user's words. The others set the flag. Their descriptions still have to stand alone.

Put a real environment requirement in `compatibility` (`Requires uv`). Skip the field when the skill runs with ordinary tools.

## The description

The body is not loaded yet. A "When to use" section under the heading cannot fix a description that missed.

Write third person, and tell the agent when to act. The description is inserted into the system prompt. "I can help you process PDFs" and "You can use this to process PDFs" both drift. "Extracts text from PDFs. Use when the user has a PDF or asks to pull text out of one" is the shape.

Front-load the words a person would type. Codex keeps a short budget for the whole skill list and shortens descriptions when many skills are installed. The slash name and the trigger phrases belong in the first sentence, so a shortened description still matches. Procedure belongs in the body.

Name the command and two or three real phrasings. Include a case where the user needs the skill and never says its name, when that case is one you want.

Add "Do not use when..." for a near miss only: a request that shares the keywords and belongs to a different skill, or to a normal answer. `socratic-tutor` does this for a one-off "explain X" or "what is X". A negative nobody would confuse with the skill spends the 1024 characters on a boundary that does not bite.

One skill is one job, with one kind of input and one way to know it is done. `create-verification-skill` and `maintain-verification-skill` are split because "there is no verifier yet" and "the verifier is stale" are different requests.

## How much freedom

Match the tightness of each step to how badly a wrong step fails.

| Freedom | The step is like | What you write |
|---|---|---|
| High | Several approaches work, and the context picks | The goal and how to tell it worked |
| Medium | One pattern is the default, and some variation is fine | A template, or a script with flags |
| Low | The sequence is the result, or a slip is expensive | The exact command, and the instruction to leave the flags alone |

A skill mixes these. `deepen` is free on the four answers and tight on stopping before it runs the rewrite. `eval` is tight on blinding, because a leaked rubric ends the experiment, and looser on how the task is worded.

Give one default. A menu of equal tools makes the agent try all of them.

On a flexible step, the reason does the work. Write "do X because Y causes Z." The agent can then handle a case you did not list. A bare NEVER belongs on a step that is unsafe to improvise: killing a process by name, powering off a shared bench, putting a rubric on a path the candidate can open. Those stay absolute, with the failure named in the same sentence when you have the room.

## Scripts

Leave a step as instructions when the agent can do it with the tools it already has and a miss is obvious in the result. Add `scripts/` when the same check gets rewritten on every run, or a wrong answer is quiet.

Calling a tool that already exists is the instruction-only path. `walkthrough` runs `uvx showboat`. Rebundling Showboat would only drift from the tool.

A bundled script:

- Takes every input as a flag, an environment variable, or stdin. A prompt waits forever. The agent has no TTY.
- Prints `--help`: one line on what it does, the flags, an example, and the exit codes. That text is how the agent learns the interface. Keep it short. It enters context.
- Supports `--dry-run` when it writes, deletes, or sends.
- Writes structured records to stdout (JSON or TSV) and writes the diagnosis to stderr: what failed, what was expected, and what to try. "Field `signature_date` not found. Available: customer_name, order_total."
- Uses exit codes that differ by failure, and lists them in `--help`.
- Is safe to run twice. Create-if-missing beats create-and-fail.
- Defaults to a short summary. A harness that cuts a tool result around 10–30k characters will drop the line that mattered. Offer `--offset` or require `--output` when the full dump is the point.
- Pins its dependencies. A Python script declares them with PEP 723 and runs under `uv run`. A one-off tool is `npx eslint@9`, not a floating package. State a hard runtime need in `compatibility`.

For a step that changes a lot of state, use plan, then validate, then execute, then verify. The agent writes a plan file. A script checks that plan against the source of truth. The agent runs the change only after the check exits 0. A second command confirms the result. Validate before the destructive command, not after.

List each script in `SKILL.md` with the condition that runs it. An unlisted file is invisible.

Test the script once yourself before you point the skill at it. A script the agent has to debug on the first real run is an instruction with extra steps.

## Don'ts and gotchas

Put the allowed action, the action that fails, and the failure in one place:

> Clone the other repo into `/tmp` and leave it out of the commit. A clone inside this repo shows up in `git status` and ships with the change.

A wall of bare NEVERs gets skipped, or it gets applied to a case you would have allowed. Keep the absolute form for the unsafe steps above.

Keep a `## Gotchas` section in `SKILL.md` when the skill has a trap that a careful reading of the happy path would still miss. The agent does not go looking for a trap it has not recognized, so a gotcha in `references/` arrives late. When a real run fails in a new way, add one line here: the preferred action, and what the wrong action produced. That list is the skill's memory. Skip the heading until the first real trap. A made-up gotcha is noise.

The feature maps from `/create-verification-skill` already require a `Gotchas` heading. Hold a skill in this repo to the same standard once it has a trap worth recording. A gotcha that belongs to a single step can sit on that step instead of in the section. `build-from-example` does this for a GitHub blob page: the page is HTML, and a summary of it is not the example.

## Queries, then `/eval`

Two checks. They answer different questions.

**Does the description fire on the right requests?** Write about 20 prompts. Eight to ten should load the skill. Eight to ten should not. The failures that teach you something are near misses: same words, different job. "Write a fibonacci function" does not test a PDF skill. Mix a formal ask, a casual one, a typo, and a request that never names the skill. One-line prompts that already say the command only test that the agent can read.

Run each prompt a few times. One run is noise. Treat a should-trigger prompt as passing when it loads the skill on more than half the runs, and a should-not-trigger prompt as passing when it stays under that.

Change the description from a train subset (about 60%). Hold the rest out. A description that only passes the prompts you edited against will miss the next phrasing. Broaden a description that missed real work. Add a near-miss boundary when a neighbor skill, or a normal answer, got the request. Add the general case, not the exact words of the failed prompt. Keep the result under 1024 characters. Pick the wording that holds up on the held-out prompts.

**Does the skill change what the agent does?** Opening the file is not the same as doing the job. Use `/eval` (`skills/eval/SKILL.md`). The parent writes a few concrete checks and keeps them off any path a candidate can read. Run the same task with the skill and without it, or with the old text and the new text. One judge scores both without being told which is which. Then read the transcripts yourself.

Read those transcripts for repeated work. If every candidate built the same helper, that helper belongs in `scripts/`.

Stop when a fresh handful of prompts still triggers cleanly, and the blinded check says the new text is the one that does the job.

## Checklist

- `name` matches the folder and follows the character rules.
- The description is third person, front-loads the trigger words, and fits in 1024 characters.
- A real near miss is named, with "Do not use when..." or by pointing at the other skill.
- The body is under 500 lines. Any other file says when to read or run it, one level from `SKILL.md`.
- A repeated or quiet check is a script with the interface above, or the skill says why the step stays prose.
- A tight rule names the preferred action and the failure. A bare absolute is reserved for a step that is unsafe to improvise.
- `## Gotchas` holds traps a real run has hit.
- Trigger prompts have been run. If the output is the thing that matters, `/eval` has been run too.

## Sources

The bar above is the overlap of these, as they stood when this guide was written:

- [Agent Skills specification](https://agentskills.io/specification), plus the skill-creation guides on [best practices](https://agentskills.io/skill-creation/best-practices), [descriptions](https://agentskills.io/skill-creation/optimizing-descriptions), [evaluation](https://agentskills.io/skill-creation/evaluating-skills), and [scripts](https://agentskills.io/skill-creation/using-scripts)
- [Anthropic, skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) and the [skill-creator skill](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)
- [OpenAI, building Codex skills](https://developers.openai.com/plugins/build/skills) and the [Codex skill-creator](https://github.com/openai/skills/blob/main/skills/.system/skill-creator/SKILL.md)
- [Cursor Agent Skills](https://cursor.com/docs/skills)
