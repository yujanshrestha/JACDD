---
name: jacdd
description: Start a JACDD alignment session — measures overlap between what should be built and what could be built
user_invocable: true
---

# JACDD Session

Launch the JACDD Judge agent to run an alignment session.

Invoke the agent: `/agent:jacdd-judge`

If `jacdd-state.md` exists at the project root, resume from the last saved iteration.
Otherwise, start at iteration 0 (bootstrap).
