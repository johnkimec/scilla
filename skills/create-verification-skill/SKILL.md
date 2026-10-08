---
name: create-verification-skill
description: "Generate a project-local verification skill that drives a system the way a user does: a software app, firmware on a board, an FPGA or RTL design, a simulator, or a lab bench. Use for /create-verification-skill, \"make a control skill for this repo\", or when a project has no scripted way to prove behavior."
disable-model-invocation: true
---

# Create a verification skill

Every serious project needs a scripted way to drive the real system and prove behavior: launch it, exercise a feature the way a user would, and capture evidence. The system might be a software app, firmware on a board, an FPGA or RTL design, a simulator, or a lab bench. This skill generates that as a project-local skill (`.cursor/skills/verify-<target>/`) tailored to the repo. You write the generator's output for the next agent, not for a human: it will be read cold, mid-task, by an agent that has never seen the system.

## 1. Interview the repo, not the user

Answer these from the codebase and only ask the user what you cannot observe:

- **Surface:** what does a user actually touch? A web UI, a CLI/TUI, a desktop app, an API, a mobile app, a library, firmware on a board, an FPGA or RTL design, a simulator, or a lab bench? A repo can have several; pick the primary one and note the rest.
- **Run:** how does the system start locally? Prefer the repo's own documented command (package scripts, Makefile, README quickstart, flash or program step, simulator invocation). Note ports, env vars, seed data, auth, serial port, probe, bitstream, pin constraints, clock, and supply.
- **Drive:** how can an agent interact with it programmatically? Existing harnesses first: Playwright/Cypress specs, expect scripts, PTY helpers, curl-able endpoints, a debug port, OpenOCD, probe-rs, pyOCD, esptool, a cocotb or other testbench, a scripted instrument. Only then pick a generic recipe: browser/CDP for web and Electron, a tmux/PTY harness for CLI/TUI, plain HTTP for services, a serial console or JTAG/SWD session for firmware, the testbench for RTL, SCPI or the repo's fixture script for a bench.
- **Observe:** what evidence can be captured? Screenshots, terminal transcripts, response bodies, logs, exit codes, DB state, UART logs, register dumps, waveforms, logic-analyzer or scope captures, measured voltage or current, simulator logs.
- **Isolate:** can two instances run side by side (ports, data dirs, profiles, simulator processes, a second board)? A physical board, probe, or instrument usually cannot. Say so in the generated skill. Refusing to double-drive a shared board or session beats corrupting the user's setup. If only a simulator is available, the physical bench is unreachable until its prerequisite is present. Do not invent a board.

If the checkout doesn't build, flash, program, or start as-is, fix that first (or report it precisely) before generating; a skill written against a broken base teaches wrong steps. When an irrelevant missing asset blocks startup (a static dir the API never serves, a sample config, a missing constraints file the design never uses), the generated skill may create it, clearly marked as verification scaffolding, and remove it in cleanup.

## 2. Generate the skill

Write `.cursor/skills/verify-<target>/SKILL.md` with YAML frontmatter (`name: verify-<target>` and a `description` that names the system, the surface, and when to reach for it — without frontmatter the skill never registers) and these sections, each grounded in what the interview actually found (no placeholders left):

- **Launch:** the exact command that starts the system for verification, and how to tell it's ready (a log line, a port answering, a prompt, a UART banner, a DONE pin, a simulator prompt). Include teardown. For a short-lived CLI, TUI, or simulator run there is no server to keep alive: launch means build once, then start each drive in its own isolated session. For firmware or an FPGA, launch means build, flash or program, and wait for the ready signal. Name the safe state teardown leaves the board in.
- **Doctor:** one read-only check that answers "is this instance worth driving?" Software: process up, right version/build, port owned by us, auth valid. Hardware: probe claimed by this run, expected firmware hash or bitstream id, UART or debug link alive, and rail present when the harness can read it. An agent runs this first whenever anything looks off.
- **Drive:** the harness recipe with real selectors and commands from this repo, not examples. Prefer stable handles (ARIA labels, data attributes, prompt strings, route paths, register names, command strings, pin names, testbench entry points) over coordinates, tab order, and timing guesses.
- **Evidence:** what to capture for a proof and where it goes. State the proof standards: exercise the real user path (the screen, the command, the pin, the protocol, or the testbench's public interface), not an internal setter, a test-only endpoint, or a force that skips the design. Capture the stimulus and the resulting state, not just the final screen or a waveform with no cause. Verify side effects (files written, rows inserted, messages sent, a pin changed, a packet sent, a peripheral register moved) alongside what's visible. Mocks only where a production boundary already isolates the external system. When the safe path is a dry-run, test mode, or simulation, verify what it actually skips by observing (files, network, git refs, which pins the sim toggles) rather than trusting its name.
- **Cleanup:** how to tear down instances the run created. Never kill by process name; kill or release what you started, including a probe or serial port this run claimed. Cleanup removes instances and scratch state, never the evidence: proof artifacts survive the teardown, in a location the skill names. Do not power off a shared bench unless the skill says that is safe.
- **Helpers:** any script the skill ships is executable and its invocation is shown in the skill body. A helper the reader has to reverse-engineer is not a helper.

## 3. Seed the feature map

Create `.cursor/skills/verify-<target>/features/README.md` plus one file per user-facing feature you can identify (aim for the top 3-5 to start, from routes, commands, menus, pins, boot modes, protocols, or docs). Follow the shape in [`references/feature-map-example/`](references/feature-map-example/). That example is a software app. A firmware, FPGA, simulator, or bench map uses the same four headings, with the harness commands this repo actually runs. Each file answers, from the user's point of view: what the feature is, how to reach it, how to drive it with the harness, and what observable end state proves it works. The four H2s are `Sub-features`, `How to get to it (user POV)`, `Driving it with <harness>`, and `Gotchas`. The map is the repo's maintained verification source; a proof that drives one convenient entry point is incomplete when the map lists others.

## 4. Prove the generated skill before handing it over

Run its own instructions end to end once: launch, doctor, drive ONE mapped feature (one is enough; the map exists so later runs can cover the rest), capture evidence, clean up. After cleanup, confirm the evidence still exists at the named location. A cleanup that eats the proof fails this step. Fix what fails, and run the generated cleanup after every failed iteration too, so broken attempts don't strand processes, ports, probes, or simulator jobs. A generated skill that was never executed is a draft, not a deliverable. When the physical bench is absent, prove the simulator path and record the bench as unreachable with the missing prerequisite.

## 5. Offer the maintenance loop

Point the user at `/maintain-verification-skill` for keeping the map honest as the system changes. Suggest a cadence only if they ask.
