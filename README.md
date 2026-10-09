# scilla

[![tag](https://img.shields.io/github/v/tag/johnkimec/scilla)](https://github.com/johnkimec/scilla/tags)

A collection of skills for coding agents. Some I took from people who publish how they work. Some I wrote after a session turned into a step worth repeating.

Git tags are what you install. Pin a tag so a later push does not change an install you already have. The badge above is the current tag.

## Install

The same commands work for Cursor, Claude Code, and Codex. Set `--agent` to `cursor`, `claude-code`, or `codex`.

Install every skill in the project you are in:

```bash
npx skills add johnkimec/scilla#v0.2.0 --agent cursor -y
npx skills add johnkimec/scilla#v0.2.0 --agent claude-code -y
npx skills add johnkimec/scilla#v0.2.0 --agent codex -y
```

Install one skill:

```bash
npx skills add johnkimec/scilla#v0.2.0 --skill walkthrough --agent cursor -y
```

Install for every project on this machine:

```bash
npx skills add johnkimec/scilla#v0.2.0 -g --agent cursor -y
```

Replace `v0.2.0` with the tag on the badge. On the one-skill and global commands, swap `cursor` for `claude-code` or `codex`.

## Skills

| Command | When to use it |
|---|---|
| `/create-verification-skill` | Generate a project skill that launches a software app, firmware image, FPGA design, simulator, or lab bench, drives it the way a user would, and seeds a feature map. |
| `/maintain-verification-skill` | Check that feature map against the system and drive every feature once. |
| `/build-from-example` | Build a change from a working example's real source, and keep any downloaded copy out of the commit. |
| `/walkthrough` | Explain a codebase in order, with every snippet printed by a command and saved through Showboat. |
| `/compound` | After a task, write one lasting project lesson into `AGENTS.md` for the next agent. |
| `/eval` | Run a blinded check of whether a skill or prompt change actually changes what agents do. |
| `/project-doc` | Scope a project in a written doc, and make the architectural decisions, before any code. |

## Sources

- [pstack](https://github.com/cursor/plugins/tree/main/pstack) by Lauren Tan.
- [Agentic Engineering Patterns](https://simonwillison.net/guides/agentic-engineering-patterns/) by Simon Willison.
