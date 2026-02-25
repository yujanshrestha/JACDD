# JACDD

JACDD is an alignment method for reducing the gap between:
- what a team will likely build (`potential_space`)
- what stakeholders will actually accept (`acceptable_space`)

It does this through iterative boundary interviews and constraint updates.

## Canonical Docs
- Unified source ("what gets compiled down"): [docs/jacdd-source.md](/Users/yshrestha/work/jacdd/docs/jacdd-source.md)
- Structured reference: [docs/jacdd-reference.md](/Users/yshrestha/work/jacdd/docs/jacdd-reference.md)
- Raw extraction from diagrams: [docs/raw-braindump-extraction.md](/Users/yshrestha/work/jacdd/docs/raw-braindump-extraction.md)
- Compressed artifacts:
  - [docs/jacdd-reference-lapc.md](/Users/yshrestha/work/jacdd/docs/jacdd-reference-lapc.md)
  - [docs/jacdd-gpt-5.3-codex.md](/Users/yshrestha/work/jacdd/docs/jacdd-gpt-5.3-codex.md)
  - [docs/jacdd-claude-opus-4.6.md](/Users/yshrestha/work/jacdd/docs/jacdd-claude-opus-4.6.md)

## How Engineers Use JACDD In a Project

### 1) Create Persistent Project Files
At project root, create:
- `jacdd-personality.md`
- `jacdd-state.md`

Purpose:
- `jacdd-personality.md` stores stakeholder + team behavior signals.
- `jacdd-state.md` stores iteration state, accepted constraints, Q/A log, and suggestion outcomes.

### 2) Run Iteration 0 (Bootstrap)
Do this once at project start:
1. Write a one-sentence goal.
2. Inventory current codebase/WIP and recent git history.
3. Estimate initial alignment band (`CRITICAL/LOW/MODERATE/GOOD/HIGH`).
4. Ask 3-5 boundary questions (one at a time).
5. Convert answers into 2-4 actionable constraints with highest expected Dice impact.
6. Have stakeholder accept/modify/reject each constraint.
7. Update `jacdd-state.md` and `jacdd-personality.md`.

### 3) Run Ongoing Iterations
Each iteration:
1. Load full history (`state`, `personality`, prior interviews/constraints, WIP changes).
2. Re-estimate alignment and largest divergences.
3. Choose:
   - run boundary interview (if key uncertainty exists), or
   - propose constraints (if uncertainty is already localized).
4. Record decisions and never re-suggest rejected constraints without new evidence.
5. Continue until `HIGH` alignment or explicit "good enough."

### 4) Write Constraints as Actionable Dice Levers
Prefer constraints that change likely implementation behavior and close the largest divergences.
Use as few constraints as possible to maximize Dice gain per constraint.

Prefer:
- "Windowing controls must remain operable during scroll"
- "Multi-monitor layout is out of scope for launch"

Over:
- broad or redundant constraints that do not change team decisions
- large bundles of low-impact constraints that overconstrain delivery

If a delta or an absolute form is more actionable for a specific divergence, use that form.

### 5) Keep Commits Legible to the Judge
JACDD treats git history as team-thinking evidence.

Commit principles:
- Group by intention (why), not only by file.
- Encode decision rationale in messages.
- Sequence commits to expose dependency thinking.

## Optional: Generate Model-Specific LAPC Artifacts

You can generate a Claude Opus 4.6 compressed artifact with blind validation loops via OpenRouter.

### Setup
1. Put API key in [`.env`](/Users/yshrestha/work/jacdd/.env):
   - `OPENROUTER_API_KEY=...`
2. Optional override:
   - `OPENROUTER_MODEL=anthropic/claude-opus-4.6`

### Run
```bash
cd /Users/yshrestha/work/jacdd
./scripts/lapc_openrouter_opus46.py
```

Outputs:
- `docs/jacdd-claude-opus-4.6.md`
- `docs/jacdd-claude-opus-4.6-validation.json`

Validation protocol separates:
- oracle (source-aware),
- evaluator (compressed-only),
- scorer (compares outputs),
to prevent source leakage during evaluation.

## Minimal Adoption Checklist
- [ ] Team understands five alignment bands.
- [ ] Iteration loop is running and persisted.
- [ ] Boundary interviews are concrete and decision-boundary focused.
- [ ] Constraints are actionable, sparse, and ranked by expected Dice impact.
- [ ] Rejected constraints are tracked and not re-proposed blindly.
- [ ] `jacdd-personality.md` is updated every iteration.
- [ ] Commits are intention-structured for history-based inference.
