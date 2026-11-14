# Skill audit

Reviewed 2026-11-13 against `main` at `e1c14ab` (the merge that added `socratic-tutor`). Updated 2026-11-14, after the four items in Done were implemented. The bar is [AUTHORING.md](AUTHORING.md). The counts table is current and includes frontmatter. Paragraphs under Per skill keep the original reading. A Done line says what changed. Every description is under the 1024-character limit, third person, and paired with a `name` that matches its folder.

## Done

Implemented 2026-11-14. `disable-model-invocation: true` is still set on the eight slash commands, for Cursor.

1. **Descriptions stand alone.** Each of those eight descriptions keeps the slash phrasing and adds a near-miss boundary, on the pattern of `socratic-tutor`. `scilla-mode` does not start on an ordinary bug, code question, new feature, or refactor. `walkthrough` does not start on a one-off "how does this work." Create and maintain name each other. `/eval` does not start for a product suite, CI, or grading application code. The maintain description opens on the trigger. The old "A product gap leaves as..." clause is gone. Procedure stays in the body.
2. **`/eval` runs `scripts/scan-blind.py`.** The word list lives in the script. Stdout is JSON. Stderr names the path. Exit 0 is clean, 1 is a hit, 2 is a bad invocation. Judgment (the rubric, the prompt's tone, the judge) stays prose.
3. **Shape check, copied into both skills.** `scripts/check-feature-map.py` is the same file in `create-verification-skill` and `maintain-verification-skill`. It checks `name`, `description`, and the four feature H2s in order. `features/README.md` is the index and is not a feature file. The live drive stays prose.
4. **Checklists, same files.** The evidence standards in `create-verification-skill` and the live pass in `maintain-verification-skill` are checklists. The rules are the same rules. They were not split into `references/`.

## Do later

- `project-doc`: say to read `template.md` only when creating a doc. Add why decision IDs never change (later steps and `superseded by` links point at them). A README or a code tour is `/walkthrough`.
- `walkthrough`: set `compatibility: Requires uv`. The dependency is in `HOW-TO-USE.md` and absent from the skill. The description boundary is done.
- `create-verification-skill`: link `references/feature-map-example/create-note.md` from `SKILL.md`. Today the filled example is a second hop through the example README.
- On the cleanup rule "Never kill by process name," add the failure in the same sentence: a shared name matches processes this run did not start. That line is copied into generated skills, so the reason travels.
- `maintain-verification-skill`: an index diff (README entries against files on disk) is still prose. The triage paragraph is still one block. The shape check does not cover either.

## Leave as they are

`compound`, `deepen`, and `build-from-example` stay short. Their 2026-11-14 edit is the description boundary only. The steps were not rewritten. `socratic-tutor` was already the description to copy and was not changed. `scilla-mode`'s playbooks were not changed. None of the ten skills is over 500 lines.

## Counts

| Skill | Lines | Auto-starts in Cursor | Description | Extra files |
|---|---:|---|---:|---|
| `build-from-example` | 21 | No | 335 | — |
| `compound` | 19 | No | 319 | — |
| `create-verification-skill` | 64 | No | 439 | `references/feature-map-example/`, `scripts/check-feature-map.py` |
| `deepen` | 19 | No | 325 | — |
| `eval` | 51 | No | 289 | `LICENSE`, `scripts/scan-blind.py` |
| `maintain-verification-skill` | 63 | No | 321 | `scripts/check-feature-map.py` |
| `project-doc` | 115 | Yes | 330 | `template.md` |
| `scilla-mode` | 42 | No | 279 | 4 playbooks, 12–14 lines each |
| `socratic-tutor` | 72 | Yes | 300 | `LICENSE` |
| `walkthrough` | 23 | No | 208 | — |

"Auto-starts" means `disable-model-invocation` is absent. On Claude Code and Codex, treat every row as able to auto-start.

## Per skill

### `build-from-example`

The file is one pass of five steps. Disclosure is already right: nothing here is a branch long enough to move, and the git check at the end is one command, so a bundled script would be a wrapper around `git status`.

The description names the job, the command, and "build this like that example." It also spends characters on `/tmp`. That detail belongs in step 3. The near miss, on a host that ignores the flag, is a green-field design with no example. That request is `/project-doc`. The step already stops when no example exists. The description can say the same in one clause.

Freedom matches the work. Locating and following the example is judgment. Keeping the clone out of the repo is tight, and the sentence says why a clone inside the repo is a miss. The GitHub-blob gotcha sits on step 2, which is the moment it matters: a blob page is HTML, and a summary of the page is not the example.

**Done:** the description says a design with no example is `/project-doc`, and an ordinary implementation with no example stays a normal answer. `/tmp` is out of the description and still in step 3. Nothing else.

### `compound`

Nineteen lines, one edit, one sentence. A script would only reimplement "is this sentence already in the file."

The description is specific, and "Skip notes that only describe where this task stopped" is a real near miss rather than a decorative negative. The same boundary is in the opening line and in step 1, with the reason: status is not a fact the next task needs.

"Do not create a skill, and do not add any other file" is absolute and slightly bare. The reason is in the line above it (one sentence, in `AGENTS.md`). A future edit can attach that reason to the prohibition. Low priority.

**Done:** the description says a status recap does not start the skill. Optional wording on "do not create a skill" is still open.

### `create-verification-skill`

Forty-four lines plus a reference example. The example is the right split: a software shape the agent opens while writing a map, with the four headings named in `SKILL.md`. The body stays on the main path, which is correct, because the evidence rules have to be copied into the generated skill.

Two disclosure nits. The evidence bullet and the seed paragraph are long enough to drop clauses (1,426 and 876 characters). And the filled example, `create-note.md`, is reached from the example README, a second hop. Link it from `SKILL.md`.

The description lists the surfaces and the command. It does not separate this skill from `maintain-verification-skill`. "Make a control skill for this repo" is also wide: a control skill can mean an MCP server or a device driver.

No `scripts/`. The live interview has to stay prose. The shape of the output does not. A checker for `name`, `description`, and the four H2s in order would catch the failure the skill already names (no frontmatter, the skill never registers). Confirming that evidence survived cleanup is one file check. Leave that as a command.

The hard rules are mostly in the right form. "Do not invent a board" follows the reason: a missing bench stays unreachable until its prerequisite is present. "Never kill by process name" is the kind of absolute that should stay absolute. Add the reason beside it so generated skills inherit the reason. "A written claim about the result is not an artifact" already says why. There is no Gotchas section for the generator itself. The traps that are known (broken checkout teaches wrong steps, cleanup that deletes the proof, a blob of a skill that was never run) are in the steps. A section would repeat them. Add one when a new trap shows up.

Freedom is high on discovering the system and low on the file shape. That mix is right. The evidence bullet is low-freedom content packed as a paragraph, which reads as looser than it is.

**Done:** `scripts/check-feature-map.py`, the evidence checklist, and the maintain boundary in the description. Still open: link `create-note.md` from `SKILL.md`.

### `deepen`

The whole skill is four questions and a stop. High freedom on the answers, low freedom on "do not run the rewrite." The reason for the stop is the contract of the skill: the user gets a prompt, and the work happens only if they ask.

The description already says "a deeper version, not a bigger one," which is the near miss (more features, a longer list). On a host that auto-starts skills, "deepen this" during product work can still grab a task the user wanted done. The slash-only flag is what prevents that in Cursor. One "Do not use when the user wants the task done, or a larger scope" covers the other hosts.

Step 2 states the same boundary with a reason: depth is a harder cut on the same job, and a longer scope is a miss. No script. No extra file.

**Done:** the description says not to start when the user wants the task done, or a larger scope.

### `eval`

The skill is the repo's functional eval. Use it for the behavior half of [AUTHORING.md](AUTHORING.md). Trigger-query sets (about 20 prompts, half of them near misses) are a separate check this skill does not run. A future skill author follows both.

Forty-three lines, all of them on the main path. The blinding rules have to be in the body. Moving them to a reference would only help if the agent could forget them, and it must not.

The description is the tightest in the set after `socratic-tutor`: a skill, a structure, or a prompt, before promoting it. The remaining near miss is the word "test" next to product tests and CI. "Do not use to run a product test suite" is the sentence. Lower priority than `scilla-mode` and `walkthrough`, because the first clause already says the subject is agent behavior.

The deterministic gap is the blinding scan in "Do these first." The rest of the pass is judgment: the rubric, the organic prompt, the comparison with the judge. A scoring script would freeze a check that the skill wants a person to read. The transcript rule is already a good don't: globbing `~/.cursor/projects/*/` crosses workspace boundaries and reads other projects' chats. The rubric rule is the other one that should stay absolute, and it already says why: a candidate can open any path it is given.

Freedom is calibrated. Blinding is low. Framing the variant is higher. The spawn steps are specific because the order is the experiment (judge only after every candidate has finished).

**Done:** `scripts/scan-blind.py` is the word check, and the description excludes a product suite, CI, and grading application code.

### `maintain-verification-skill`

Thirty-nine lines, and two of them are doing too much work. The edit-scope paragraph is 505 characters. The live pass is 2,016. The triage paragraph is 1,029. Nothing is missing from `references/` for length. The file is hard to follow because three checklists are written as prose. Rewrite them as checklists in this file. A `references/live-pass.md` would be the wrong split: the pass is the main path, and a 39-line file is cheap once it is readable.

The description leads with mechanism ("parallel source readers," "one PR") and puts "audit the verify skill" last. A host that shortens descriptions will cut that trigger first. The awkward clause is "A product gap leaves as its own failing test." Say what ships, in the body, and open the description with the trigger. Add "Do not use when the project has no verification skill; that is `/create-verification-skill`."

Index hygiene (README entries against files on disk) is a diff a script can print. Worth bundling beside the shape checker from the create skill, as a copy in this folder. The source wave and the live drive stay instruction-only. A generic driver cannot know the board.

"Never change product behavior" is the right absolute. The next sentence is the reason, in the form the agent can apply: a behavior the system dropped is either doc drift (fix the map) or a regression (keep the map, file the failing test elsewhere). "Never put a second agent on a board" has its reason in the same breath. The instruction to keep run notes out of the commit is bare. Low priority. Say they are scratch because a committed note rots into a second map.

The outcome enum (`clean`, `changed`, `blocked`) is good low freedom. The coordinator owning the drive is good low freedom. Both are buried in the long paragraphs.

**Done:** the live pass is a checklist, the description opens on the trigger and names `/create-verification-skill`, and this skill has its own copy of `scripts/check-feature-map.py`. Still open: the index diff, and the triage paragraph, which is still one block.

### `project-doc`

The longest skill, at 115 lines, and still a third of the limit. The phase table at the end is the kind of branch table that earns its place in the body: every resume uses it. `template.md` (65 lines) is a template. The convention puts those in `assets/`. Leaving it beside `SKILL.md` works, because the link is one level deep. The real nit is when it loads. The opening points at the template on every run, including a resume that only needs `docs/<project-name>.md`. Say to read it when creating a doc.

The description matches the intended auto-start: a new project or design, or a return to `docs/`. The near misses are "write the README," "document this code" (`/walkthrough`), and "plan this refactor" (`/scilla-mode` refactoring). One sentence covers that set. This skill is allowed to start without a slash, so the sentence matters in Cursor too.

No script. The resume table is short enough to follow, and a script that prints the phase would miss "this answer is too vague to keep," which is a judgment the skill defines well: a builder still could not tell what to build, who it is for, or how to know it worked.

The don'ts carry reasons. Write the file in the same turn, because a new chat does not remember. Building waits on `approved`, and the reply says what is still open. Decision IDs "never change" with no reason on the line. Add one: plan steps and `superseded by` links point at the ID. The user's own sentences stay in their words, with a test for when you may propose a tighter line. That is the right amount of freedom for a skill whose product is a decision the user made.

There is no Gotchas heading. The known traps are the phase rules. Add a heading when a resume goes wrong in a way the table did not cover.

**Next:** the description sentence, the "read the template only when creating" line, and the ID reason. Moving the template to `assets/` can wait.

### `scilla-mode`

The best disclosure in the repo. Forty-two lines route to one playbook. The playbooks are 12–14 lines. The spec's usual directory name is `references/`. `playbooks/` is allowed, and the name tells the agent what the file is. Keep it. The match table says which file to open. That is the condition the spec asks for.

The description is the widest in the set: a defect to reproduce and fix, a diagnosis, or a refactor that keeps behavior. That is the skill's job once someone has typed `/scilla-mode`. As an automatic trigger it swallows ordinary debugging and ordinary refactors, and it also overlaps `/walkthrough`, `/project-doc`, `/deepen`, `/eval`, `/compound`, and `/socratic-tutor`. Those boundaries are in the body, under "These are other skills." The body loads after the trigger, so they cannot prevent a false start. Put the near misses in the description, or keep the skill slash-only on every host you ship to.

Inside a matched playbook the freedom is right. Bug fix is low freedom on "a line ships because a run justified it," and the reply shape is specified. The unit-test gotcha is on the verify step: a test that does not run the repro does not show the bug is gone. Trace forensics says why you do not re-capture: the artifact in hand is the assignment. Runtime forensics stops at the diagnosis and names the switch to bug fix. Refactoring pins behavior before the move.

A script that picks the playbook would be a worse matcher than the table. Leave the match as instructions.

**Done:** the description keeps `/scilla-mode` and "scilla mode", and an ordinary bug, code question, new feature, or refactor stays a normal answer. The playbooks were not changed.

### `socratic-tutor`

Seventy-two lines, all on the main path. The skill map is rendered every level change, so it belongs in the body. No script, and none is called for. The levels are a judgment.

This is the description to copy. It is third person, it front-loads "teach me / tutor me / quiz me / drill me / help me master," and it names the near miss that would otherwise false-start the skill: a one-off "explain X" or "what is X" stays a normal answer. The skill is allowed to auto-start, and the description is written for that. The Guard section repeats the boundary with the reason a false start is costly: the user gets a quiz they did not ask for, and the confirmation is one short question.

The teaching rules are medium freedom with reasons attached. One question, then wait, because a hint in the same message answers it. Explain only after two or three misses, then re-test from another angle. "Do not flatter" comes with the line to use instead. Levels move on two independent checks, one of them unprompted, because a level given on the turn after you told them the answer is not a level. That is a gotcha written as a rule. A `## Gotchas` heading would help a human scanning the file and would not change the agent's behavior. Optional.

The skill map characters and the command list are templates. They are short and used every session. Keep them inline.

**Next:** none required.

### `walkthrough`

Twenty-three lines. Showboat is the deterministic tool, invoked with `--help` first and `verify` at the end. Bundling a wrapper would fork that tool. This is the instruction-only case the guide tells you to keep.

The description's second sentence is implementation: Showboat, `sed`, `grep`, `cat`. Those words do not help a person get the skill, and they compete with the trigger. "How does this actually work" is the broad phrase. A question about one function becomes a `walkthrough.md` at the repo root, which is a heavy answer to a light question. The same shape as `socratic-tutor`'s guard belongs here: a one-off question stays a normal answer; this skill writes the linear document when the user wants a tour.

`uv` is a real prerequisite and is missing from the skill. `compatibility: Requires uv` puts it where a host can see it. A gotcha line for "if `uvx` is not found, stop and say so" beats a failed `exec` halfway through the document.

The memory-snippet rule is already in the right form. A snippet typed from memory is a miss, because the document has to show the bytes on disk. Asking before replacing an existing `walkthrough.md` is the other trap, and it is on the step.

**Done:** the description drops the Showboat sentence, and a one-off "how does this work" stays a normal answer. Still open: `compatibility: Requires uv`, and a stop when `uvx` is missing. The steps were not changed.
