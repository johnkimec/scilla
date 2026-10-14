---
name: deepen
description: "Rewrite a task into a deeper version, not a bigger one: name the professional move, the raw starting material, the methods and tools, and the external check for correctness. Use for /deepen or when the user wants their prompt deepened before work starts."
disable-model-invocation: true
---

# Deepen

I want a deeper version of this task, not a bigger one. Before rewriting it: (1) say what a top professional in this field would do here that I'm not asking for; (2) name the rawest material they would start from instead of what has already been digested for me; (3) name the specific methods and tools they would use; (4) say what, other than you or me, would show the result is right. Then rewrite my prompt to ask for exactly that.

## Pass

1. **Read the task.** Use the user's current ask as the task. If they have not named one, ask for it and stop.

2. **Answer (1)–(4) first.** Do not rewrite yet. Keep each answer concrete and short. Depth means a harder cut on the same job: primary sources, named methods, and a check outside the chat. It does not mean a longer scope, extra features, or adjacent work.

3. **Rewrite the prompt.** One prompt that asks for exactly that deeper version. No preamble. No options menu. No offer to do the original shallow version instead.

4. **Stop.** Do not run the rewritten prompt unless the user says to.
