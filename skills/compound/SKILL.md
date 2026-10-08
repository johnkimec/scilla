---
name: compound
description: "After a task, write one standing project lesson into AGENTS.md so the next agent starts with it. Use for /compound or when a finished task revealed a command, path, or constraint the next task will need. Skip notes that only describe where this task stopped."
disable-model-invocation: true
---

# Compound

A finished task can leave one standing lesson in the project's `AGENTS.md`. Where this task stopped does not belong there.

## Pass

1. **Keep only a standing lesson.** A standing lesson is a fact the next task in this repo will need: a command, a path, or a constraint that already caused a wrong change. Status, remaining work, and decisions that apply only to this change stay out of the file. If there is no standing lesson, say so and stop.

2. **Choose the file.** Use `AGENTS.md` at the repo root. If the lesson is only true inside a subdirectory that already has its own `AGENTS.md`, use that file. If none exists, create `AGENTS.md` at the repo root.

3. **Make the smallest edit.** If the file already says it, leave it. If a line is now wrong, replace that line. Add a line only when nothing in the file covers the lesson. One concrete sentence. Do not create a skill, and do not add any other file.

4. **Report the line.** Quote what you added or changed, and name the file. If you changed nothing, say that the file already had it or that there was no standing lesson.
