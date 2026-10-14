---
name: scilla-mode
description: "Route a bug, a live diagnosis, a captured trace, or a behavior-preserving refactor through one playbook. Use for /scilla-mode, \"scilla mode\", a defect to reproduce and fix, a runtime or trace diagnosis, or a refactor that keeps behavior the same."
disable-model-invocation: true
---

# Scilla mode

`/scilla-mode` is the only command. The playbooks are files in `playbooks/`. Match one, copy its steps, and run them. Do not invent another playbook.

## Match

Read the request and open one file:

| The request | Playbook |
|---|---|
| A bug to reproduce and fix | `playbooks/bug-fix.md` |
| A live process, and the deliverable is a diagnosis (leak, spin, glitch) | `playbooks/runtime-forensics.md` |
| A capture they already have (profile, trace, heap snapshot, spindump) | `playbooks/trace-forensics.md` |
| A structure change, and behavior stays the same | `playbooks/refactoring.md` |

"new task" means match again. Leave the previous playbook.

A narrower playbook wins. A live symptom with no fix asked is runtime forensics. A file they handed you is trace forensics. "Fix it" after either diagnosis is bug fix. If none of the four fits, say so and ask which one it is.

These are other skills. Name the skill and stop:

- A new project or design, or new behavior before `docs/<project-name>.md` is `approved` → `/project-doc`
- How existing code works → `/walkthrough`
- Deepen a prompt before work → `/deepen`
- Whether a skill or prompt change alters what agents do → `/eval`
- One lasting lesson after a finished task → `/compound`

## Run

1. Read the matched playbook in full.
2. Put its steps in the todo list, in order, before any task-specific todos. Copy them as written. A step you will not do stays in the list with `skip:` and one line why.
3. Do the steps in order. A step that names another skill means run that skill.
4. End with the reply that playbook names.

Forensics stops at the diagnosis. Start bug fix only when the user asks for a fix.
