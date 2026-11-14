---
name: eval
description: "Test how a skill, structure, or prompt change affects agent behavior before promoting it. Use for /eval, \"eval this skill\", or a blinded check of whether a variant changes what agents do. Do not use to run a product test suite, CI, or to grade application code. That stays a normal task."
disable-model-invocation: true
---

# Eval

You own the experiment. Plan it, blind it, run it, and synthesize it. The parent holds the rubric. Candidates do the task. One judge scores the outputs. You decide whether to promote the variant.

## Blinding

These rules apply to every directory, file, and prompt a candidate sees.

The word check is `scripts/scan-blind.py`. Run it. Do not scan the banned words from memory. Those words tell the candidate this is an experiment, and a missed one invalidates the run. From this skill's directory:

```bash
python3 scripts/scan-blind.py --help
python3 scripts/scan-blind.py <candidate-dir> <prompt-file>
```

Exit 0 means the names and file bodies are clean. Exit 1 means a hit. Stderr names the path, the line, and the word. Fix that path and run the scan again. Do not spawn while it exits 1. Exit 2 means the invocation was wrong. The script reads only, so a second run is safe. `--help` lists the words, the exit codes, and why there is no `--dry-run`.

- The candidate prompt looks like an organic user request. State the goal, not the meta.
- Do not ask the candidate to list which skills, principles, or files it applied. Ask for design notes generally. Grade chain-following from the files it opened and the shape of the work, not from its own claims.
- Directory and slug names look like names a user would pick for a real project.
- Do not tell a candidate that other candidates exist.
- The judge may know it is judging. It sees outputs by sanitized label only, never by model name.
- Comparing two variants: one judge scores both sets in a single pass on one scale, blind to which set each output came from.

The rubric stays with the parent. Do not write it into a candidate directory, including a hidden or cleverly named subfolder. A candidate can open any path it is given.

## Pass

1. **Frame.** State the variant under test and what behavior counts as success. Write 3–6 concrete criteria for the judge only. Concrete: `The generated skill names the launch command and the ready signal.` Vague: `The skill is good.` Hold the rubric back from candidates.

2. **Set up one directory per candidate.** Put the variant in place, plus any context an organic task would have: a project skeleton, and the skills the candidate would naturally read. Use a git worktree when the variant needs a real checkout. Give each directory a project-shaped name. Do not place the rubric, the judge prompt, or another candidate's output on any path the candidate can read. Run `scripts/scan-blind.py` on the directory before you leave this step.

3. **Write one prompt.** What a user would type. Every candidate gets that same prompt. No leakage of what is being measured. Run `scripts/scan-blind.py` on the prompt file after you write it.

4. **Spawn the candidates.** Spawn only after `scripts/scan-blind.py` exited 0 for every candidate directory and the shared prompt. Default to two, on different model families available in this session. Use the same model more than once only when the user asked for a generation-variance check. If the user named models, use those. If a slug is rejected, run that seat on the closest valid slug of the same family and say so. Spawn them all in one message with `run_in_background: true`. Each prompt contains the task, that candidate's own output path, and a request for short design notes. Nothing else. If a candidate produces no output, continue with the rest and record the dropout.

5. **Spawn one judge after every candidate has finished.** Do not spawn the judge while a candidate is still writing. Use one model from a different family than the parent when one is available. The judge is readonly. It receives the rubric and each output under a sanitized label. It scores every criterion and recommends whether the variant did the behavior. It never receives a model name. When two variants are under comparison, the judge scores both sets in that single pass and is not told which set is which.

6. **Check the chain from transcripts.** Read each candidate's transcript under this workspace's `agent-transcripts/` directory. The system prompt names that path. Do not glob `~/.cursor/projects/*/`. That crosses workspace boundaries and reads private chats from unrelated projects. Record which files each candidate actually opened.

7. **Read every output yourself.** Compare your reading with the judge's verdict. Agreement supports the recommendation. Disagreement means a model is biased or a criterion is ambiguous. Say which.

## Reply

Report the variant under test, the rubric, notes per candidate (including dropouts and which files were opened), the judge's verdict, your synthesis, and a recommendation to promote the variant or not.
