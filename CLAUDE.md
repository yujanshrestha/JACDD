# JACDD — Judgement-Aligned Constraint-Driven Development

A framework that measures the overlap between what *should* be built and what *could* be built, then drives that overlap toward 1 through targeted constraints.

## Vocabulary

| Term | Definition |
|---|---|
| Solution Space | Region where 95% of plausible solutions lie (a probability density, not a list) |
| Acceptable Space | Solutions the Human would accept — inferred from constraints + judgement |
| Potential Space | Solutions the Implementer could produce — simulated from capability + WIP |
| Constraint | Anything that narrows a solution space (requirement, test, decision, delta) |
| Specification | A list of constraints at a given iteration |
| Dice Score | Overlap metric between potential and acceptable spaces (0 = none, 1 = perfect) |
| Scope Alignment | Dice(potential, acceptable) — the central metric |
| Misalignment | 1 − Scope Alignment — the gap JACDD works to close |
| Judgement Interview | Targeted questions on decision boundaries to calibrate acceptability |
| JACDD Judge | The engine that estimates alignment and suggests constraints |

## The Loop

1. Human states a goal and provides initial constraints.
2. Judge inventories the codebase and current WIP.
3. Judge infers the acceptable space from constraints + judgement data.
4. Judge simulates the potential space from Implementer capability + WIP.
5. Judge estimates the Dice score (qualitative band: CRITICAL / LOW / MODERATE / GOOD / HIGH).
6. Judge runs a Judgement Interview — 3-5 boundary questions per round.
7. Judge suggests 2-4 constraints ranked by expected Dice impact (prefer deltas).
8. Human accepts, modifies, or rejects. Constraints update. Repeat from step 3.

## Rules

1. Use `/agent:jacdd-judge` or say "start JACDD" to begin a session.
2. The Judge estimates alignment qualitatively — never fabricate numeric scores.
3. Interview questions must sit on decision boundaries ("good question" test).
4. Constraints can be deltas vs. current solution, not only absolutes.
5. History matters — the Judge consumes all prior constraints, WIP, and interviews.
6. State persists in `jacdd-state.md` at project root for cross-session continuity.
7. The Implementer = Claude Code + the Human. Potential space = what this team could plausibly produce.
8. The Judge suggests; the Human decides. Judgement is never automated away.

## Invocation

Run a full JACDD session: `/agent:jacdd-judge`

## Reference

Full theory and formal definitions: `docs/jacdd-reference.md`
