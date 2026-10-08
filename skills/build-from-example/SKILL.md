---
name: build-from-example
description: "Build a change by following working source instead of inventing a fresh implementation. Read the real files, keep any borrowed repo in /tmp, and leave that copy out of the commit. Use for /build-from-example, \"build this like that example\", or when a working example already exists."
disable-model-invocation: true
---

# Build from an example

A working example is the specification. Read it and follow it. Inventing a fresh design is a miss when an example was available.

## Pass

1. **Locate the example.** Use the file, path, URL, repo, or behavior the user named. A named behavior means the code that already implements it, such as an existing feed, command, or test. If they named nothing, search this repo for the closest working code. If you still cannot find a working example, stop and say so.

2. **Read the source.** Open the files. For a URL, fetch the raw file with curl. A GitHub blob page is HTML, and a summary of the page is not the example. When the user gives more than one example, read every one of them.

3. **Keep borrowed repos outside the project.** Clone or copy another repository to `/tmp`. Do not clone it into this repo, and do not commit it. An example that already lives in this repo stays where it is; read it in place.

4. **Follow the example.** Use every example you were given. Match its structure and the behavior the user asked to imitate. Put new files where this repo already keeps that kind of file. Carry over the part that does the job, and leave the rest of the example behind.

5. **Check the diff.** The change is the new work. The borrowed copy in `/tmp` is absent from `git status`. In the reply, name each example file you followed.
