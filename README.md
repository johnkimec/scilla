# scilla

[![tag](https://img.shields.io/github/v/tag/jvkec/scilla)](https://github.com/jvkec/scilla/tags)

Skills for Cursor agents. A skill is a folder in `skills/` with a `SKILL.md`. Run one by name.

Git tags are the installation record. Pin a tag when you install so a later push does not change an install that already shipped.

## Skills

| Command | When to use it |
|---|---|
| `/create-verification-skill` | Generate a project skill that launches a software app, firmware image, FPGA design, simulator, or lab bench, drives it the way a user would, and seeds a feature map. |
| `/maintain-verification-skill` | Check that feature map against the system and drive every feature once. |
| `/build-from-example` | Build a change from a working example's real source, and keep any downloaded copy out of the commit. |
| `/walkthrough` | Explain a codebase in order, with every snippet printed by a command and saved through Showboat. |
| `/compound` | After a task, write one lasting project lesson into `AGENTS.md` for the next agent. |
| `/eval` | Run a blinded check of whether a skill or prompt change actually changes what agents do. |

## Sources

- [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan. `/create-verification-skill`, `/maintain-verification-skill`, and `/eval` started there. The verification skills were generalized after that.
- [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/) by Simon Willison. `/build-from-example`, `/walkthrough`, and `/compound` come from that guide. The verification skills also took two rules from it: save the command with the output it produced, and turn a failed drive into a failing test when the project has a test suite.
