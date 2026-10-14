### Runtime forensics

You own the diagnosis. The deliverable is a cited cause, not a fix.

Instrument the live process. A theory from the source, with no artifact, is not a diagnosis.

1. Capture a real artifact from the running process. A CPU profile for a spin, a heap snapshot for a leak, a trace for a glitch.
2. Reduce the artifact to the smoking gun: the function on the hot path, the chain holding the leaked object, or the loop that fires with no input. Keep the reduced finding. Leave the raw dump out of the reply.
3. Prove the mechanism on the live process before you believe it. A log, a probe, or a one-line change you can observe is enough. Revert that probe when the check is done.
4. Map the finding to a file, a symbol, and a line.

Reply: the signal you captured, the reduced finding, how you proved the mechanism, and the source location. No fix. If the user wants the fix, stop and match Bug fix.
