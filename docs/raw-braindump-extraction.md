# JACDD Brain Dump - Raw Extraction

## Author: Yujan Shrestha

---

## DIAGRAM 1: The Process Flow (Top)

### Inputs (Left Side)
- "history of constraints + guidance" → feeds into "Constraints n"
- "history of WIP" → feeds into "WIP n"
- "Question and answers (to calibrate judgement model)"

### Central Engine
- Constraints n + WIP n → **queries** → **JACDD Judge**
- JACDD Judge → **estimates** → "1 - Potential solutions * acceptable solutions Dice score" (this is **Misalignment**)
- JACDD Judge → **infers** → "Space of acceptable solutions"
- JACDD Judge → **simulates** → "Space of potential solutions"

### Feedback Loop (Right Side)
- From Misalignment → "Judge suggests constraints to maximize Dice"
- Flow: "Judge consumes WIP and Constraints (and histories)" → "Misalignment Simulation" → "Constraints likely to reduce misalignment"

### Annotations
- Yellow sticky: "These can be deltas vs the current solution" — Yujan Shrestha

---

## DIAGRAM 2: The Ecosystem (Bottom)

### Human Role
- **Human** → "Asks clarifying questions" → updates "Constraints + Guidance"
- Yellow sticky on Constraints + Guidance: "These are probability density functions" — Yujan Shrestha

### JACDD Judge Role
- "Constraints + Guidance" → **updates** → **JACDD Judge**
- JACDD Judge → **infers** → "Space of acceptable solutions"
- JACDD Judge → **evaluates by** → "Space of potential solutions"
- JACDD Judge → **estimates** → "Potential solutions * acceptable solutions Dice score"

### Implementer Role
- "Space of all solutions" → **Implementer (Harness + people + team)** → **could produce** → "Space of potential solutions"
- Yellow sticky on Space of potential solutions: "These are probability density functions" — Yujan Shrestha

### Goal
- Yellow sticky: "The Dice score of potential vs acceptable is as high as possible" — Yujan Shrestha

---

## DEFINITIONS (Right side of bottom diagram)

**Scope Alignment** = Dice score of Potential solution space and Acceptable solution space

**Estimation** = act of estimating a space from a set of samples

**Solution** = A single point. One realization of constraints. One deliverable. One codebase. One product. A solution could in itself be a specification.

**Solution Space** = A boundary at which 95% of solutions lie

**Constraint** = a requirement, user need, acceptance criteria, verification test, or anything else that constrains the solution space

**Specification** = a list of constraints

**Implementation** = the act of transforming constraints into potential solution space

**Judgement** = something only a human can do. Act of making a decision with imperfect info. Most effectively defined by a bunch of example scenarios, possible choices, chosen choice, and reasoning.

**Judgement Interview** = the act of asking a bunch of questions to model judgement. A good interview is when the questions asked are right on decision boundaries and feel "hard" for the human but also "useful" for the specific problem at hand. Humans would say "good question."

---

## KEY INSIGHTS FROM THE DIAGRAMS

1. Solution spaces are modeled as **probability density functions**, not discrete sets
2. The Dice coefficient (set similarity metric) measures overlap between what's acceptable and what's producible
3. Misalignment = 1 - Dice(potential, acceptable) — the gap between what could be built and what should be built
4. The JACDD Judge actively **simulates** potential solutions and **infers** acceptable ones
5. The Judge's feedback loop suggests new constraints to **reduce misalignment**
6. Constraints can be expressed as **deltas vs the current solution** (not just absolute specs)
7. The Human's role is to calibrate the judgement model through Q&A and clarifying questions
8. The Implementer is the entire production apparatus: harness + people + team
9. The Judge sits between the Human (who defines acceptability) and the Implementer (who defines possibility)
10. History matters: both constraint history and WIP history feed into the Judge
