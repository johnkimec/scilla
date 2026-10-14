### Trace forensics

You own the diagnosis from an artifact the user already has. The deliverable is a cited cause, not a fix.

The capture already exists. Read it. Do not re-run it to get a new one.

1. Name the format and open it with a tool that understands it. A CPU profile, a trace, a heap snapshot, or a spindump. If you cannot tell the format, say so and stop.
2. Turn the artifact into something you can query before you read it line by line. For a large file, reduce it first and keep the reduced finding.
3. Narrow to the cause. For time, find the frames that hold the most of it and walk to the hot path. For a leak, follow what keeps the object alive. For a spindump, find the thread that is stuck and why it waits.
4. Map the frame to a file, a symbol, and a line using the artifact's own symbols. A frame with no source mapping is not yet a diagnosis. Say so if the artifact has no symbols.
5. If the user gave a before and an after, compare them. If there is only one capture, label the finding as the strongest reading of that file.

Reply: the artifact and its format, the reduced finding, the source location, and whether a second capture confirmed it. No fix. If the user wants the fix, stop and match Bug fix.
