### Bug fix

You own the fix. The deliverable is a change that makes the original repro pass, and the run that shows it.

Every shipped line traces to a run you did. A guess that might help does not ship. When a run kills a hypothesis, revert the edit that hypothesis caused. Ship the smallest change the evidence justifies.

1. Reproduce it yourself on the real surface. If the project has a verification skill, use its launch and drive. If it does not, drive the surface a user would use and keep the command together with the output. Ask the user to reproduce only after that path cannot reach the bug, and say why.
2. Find the cause. If the path through the code is unclear, run `/walkthrough` on that area. State the candidate causes, then rule them out with a run. Each pass, take the check that removes the most remaining causes. When the program state is unclear, add a log or a probe and read it while the code runs.
3. Make the smallest fix that surviving cause justifies. If a working example of the same behavior exists, run `/build-from-example` on it. If the fix changes a decision in `docs/<project-name>.md`, add a new decision-log entry and mark the old one superseded before you change the plan or the code.
4. Verify on the same surface as step 1. The original repro now passes. A run that did not reach that surface is not a pass. A unit test that does not run the repro does not show the bug is gone.
5. If the hunt revealed a command, a path, or a constraint the next task will need, run `/compound`.

Reply: what was broken, the cause, the fix, and how you verified. Include the failing run and the passing run.
