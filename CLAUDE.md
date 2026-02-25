name: JACDD
desc: Measure overlap(team_would_build, stakeholder_would_accept); close gap via boundary questions → constraints

vocab:
  acceptable_space: what stakeholder would accept
  potential_space: what team would likely build
  alignment: overlap of both (CRITICAL/LOW/MODERATE/GOOD/HIGH)
  judge: estimates alignment; suggests questions + constraints
  judgement_interview: boundary questions where answer could go either way
  delta_constraint: requirement as change from current state

loop:
  1: estimate what team would build vs stakeholder would accept
  2: ask boundary question (answer could go either way)
  3: constrain — turn answer into requirement; prefer deltas
  4: repeat until aligned

rules:
  invoke: `/agent:jacdd-judge` or "start JACDD"
  alignment: qualitative only; never fabricate numeric scores
  questions: must sit on decision boundaries ("good question" test)
  constraints: can be deltas vs current solution
  history: judge consumes all prior constraints, WIP, interviews
  state: persists in jacdd-state.md at project root
  implementer: Claude Code + Human; potential space = what team could plausibly produce
  authority: judge suggests; human decides; no automating judgement

ref: docs/jacdd-reference.md
source: docs/raw-braindump-extraction.md
