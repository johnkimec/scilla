---
name: walkthrough
description: "Explain a codebase in one linear document whose code snippets were printed by a command. Use Showboat note for commentary and Showboat exec with sed, grep, or cat for snippets. Use for /walkthrough, \"walk me through this code\", or \"how does this actually work\"."
disable-model-invocation: true
---

# Walkthrough

Explain the code in one pass, from the start of the story to the end. A snippet typed from memory is a miss. Commentary, then a command that prints the file, then the output that command produced.

## Pass

1. **Read, then plan.** Read the source. Plan one order a reader can follow from beginning to end, starting at the foundation or the entry point and moving outward. If the user named a file or an area, stay inside it.

2. **Learn the tool.** Run `uvx showboat --help` and use what it prints.

3. **Write `walkthrough.md` at the repo root.** If that file already exists, ask before replacing it. Create it with `uvx showboat init`.

4. **Alternate notes and printed code.** Commentary goes in with `uvx showboat note`. Every snippet is a `uvx showboat exec` of `sed`, `grep`, `cat`, `find`, or `wc` that prints the bytes on disk. A hand-copied snippet does not go in the note.

5. **Fix a bad command in the document.** If an exec fails or prints the wrong lines, `uvx showboat pop` that entry and run the corrected command.

6. **Check.** Run `uvx showboat verify walkthrough.md`. In the reply, give the path to the document.
