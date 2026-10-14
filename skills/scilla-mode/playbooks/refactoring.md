### Refactoring

You own a structure change. The deliverable is the same behavior, in a shape that is easier to follow.

Pin the current behavior before you move anything. A change the user can see is a bug fix or a new project, not this playbook.

1. Name the behavior that must stay the same, and the check that proves it. If the project has a verification skill, use it. If it does not, name a command a user would run and keep its output.
2. Run that check and keep the output. That output is the pin.
3. If the area is unclear, run `/walkthrough` on it before editing.
4. Change structure only. If a working example of the shape you want already exists, run `/build-from-example`. If the move changes a decision in `docs/<project-name>.md`, add a new decision-log entry and mark the old one superseded before you change the plan or the code.
5. Run the same check as step 1. The result matches the pin. A different surface is not a pass.
6. If the work revealed a command, a path, or a constraint the next task will need, run `/compound`.

Reply: what moved, what behavior you pinned, and the before and after output of the same check.
