# JACDD Unified Source (Canonical)

This file is the merged source-of-truth for JACDD v0.2.
Think of this as the "source code" that model-specific compressed artifacts are compiled from.

Provenance:
- `docs/jacdd-reference.md` (canonical structured reference)
- `docs/raw-braindump-extraction.md` (diagram extraction + explicit definitions)

## Metadata
- Author: Yujan Shrestha
- Version: 0.2

## Purpose
Measure overlap between:
- what the team would likely build (`potential_space`)
- what stakeholders would accept (`acceptable_space`)

Close the gap through boundary questions and constraint updates.

## Problem Statement
Acceptable space and potential space drift apart silently.
Most teams discover this only at review time after expensive rework.
JACDD makes this gap measurable and correctable throughout delivery.

## Model

### Two Spaces
- `acceptable_space`: PDF shaped by stakeholder constraints + human judgement
- `potential_space`: PDF shaped by team capability + WIP + habits
- Both are fuzzy/graded/uncertain; not checklist sets

### Alignment Metric
- Scope alignment is overlap between potential and acceptable spaces
- Dice overlap:
  - `Dice(f,g) = ∫ min(f(x), g(x)) dx`
  - Range: 0 (no overlap) to 1 (identical)
  - Symmetric; overlap metric, not distance metric
- Misalignment:
  - `1 - Dice(potential, acceptable)`

### Practical Estimation Rule
- Judge estimates alignment qualitatively in five bands
- Do not fabricate a numeric score
- Integral is not directly computed in practice

### Alignment Bands
- `CRITICAL`: barely any overlap; fundamental misunderstanding
- `LOW`: small overlap; major direction gaps
- `MODERATE`: meaningful overlap; specific gaps nameable
- `GOOD`: strong overlap; mostly refinement
- `HIGH`: near-complete overlap; ready to build

## Roles
- `Stakeholder`: source of judgement; defines acceptable space via constraints + interview answers
- `Team/Implementer`: full production apparatus (harness + people + tools + codebase); defines potential space
- `JACDD Judge`: estimates alignment, asks boundary questions, suggests constraints, models both spaces
  - Judge is the only role modeling both acceptable and potential spaces simultaneously

## Judgement Interview
- Goal: model stakeholder judgement on decision boundaries
- Good questions:
  - are hard enough to trigger deliberation
  - force a choice between defensible options
  - are concrete scenario-based (not abstract preference polling)
- Quality signals:
  - stakeholder pauses
  - stakeholder says "good question"
  - tradeoff is surfaced
- Output rule:
  - every answer becomes or modifies a constraint

Example boundary question:
- "Search returns in 50ms but can show stale data (up to 30s). Acceptable?"

## Constraints
- Constraint = any requirement, user need, acceptance criterion, verification test, or condition narrowing solution space
- Prefer actionable constraints that change implementation decisions and close largest divergences
- Use as few constraints as possible to maximize Dice improvement per constraint
- Constraint form can be absolute or delta; choose whichever is most actionable in context
- Constraints are written with implementers in mind
- Specification can be represented as a list of constraints

## Core Loop
1. Estimate both spaces; identify largest divergences; assign alignment band
2. Interview: ask 3-5 boundary questions targeting largest divergences
3. Constrain: suggest 2-4 actionable constraints, ranked by expected alignment impact
4. Stakeholder accepts/modifies/rejects suggestions
5. Re-estimate and repeat until `HIGH` or "good enough"

## Bootstrap (Iteration 0)
- No history; highest uncertainty
- Interview should dominate early rounds
- Constraint suggestion quality increases as the judge model matures
- Initialize personality modeling from:
  - team codebase + git inventory
  - stakeholder goal skeleton

## Persistent Artifacts

### `jacdd-personality.md` (project root)
- Stakeholder section:
  - preferences
  - judgement patterns
  - revealed priorities
  - decision tendencies
- Team section:
  - strengths
  - weaknesses
  - tools
  - habits
  - blind spots
- Feeds:
  - stakeholder section -> acceptable space estimate
  - team section -> potential space estimate
- Update cadence:
  - judge updates every iteration
  - human may edit anytime

### History Inputs (must be consumed each iteration)
- full constraints history
- full WIP history
- full interview Q/A history

Enables:
- trajectory detection
- regression flagging
- convergence monitoring
- never re-suggesting rejected constraints

## Commit Archaeology
Git history is treated as evidence of team cognition:
- commit granularity -> chunking style
- message framing -> priorities
- co-location vs separation -> conceptual grouping
- sequencing -> dependency thinking

Principle:
- commit with intention as if the judge will read history to learn how the team thinks

## Diagram-Derived Process View

### Process Flow
- Inputs:
  - history of constraints + guidance
  - history of WIP
  - interview Q/A for judgement calibration
- Central engine:
  - Judge queries constraints + WIP
  - Judge infers acceptable space
  - Judge simulates potential space
  - Judge estimates misalignment (`1 - Dice`)
- Feedback loop:
  - Judge suggests constraints likely to maximize Dice and reduce misalignment

### Ecosystem
- Human asks clarifying questions and updates constraints/guidance
- Judge updates model and evaluates potential vs acceptable
- Implementer produces potential solutions from the full solution universe
- Goal: maximize Dice overlap between potential and acceptable

## Definitions
- `Estimation`: estimating a space from samples
- `Solution`: one point realization of constraints (deliverable/codebase/product); a solution can itself be a specification
- `Solution Space`: boundary where ~95% of solutions lie
- `Implementation`: transforming constraints into potential solution space
- `Judgement`: human decision-making under imperfect information
- `Judgement Interview`: structured questioning to model judgement at decision boundaries

## Worked Example: DICOM Viewer
- Project: DICOM viewer for radiologists
- Initial divergence:
  - clinical lead wants cine-loop + inline windowing
  - engineering default is single-image + separate windowing dialog
- Iteration 0:
  - alignment: `LOW`
  - interview outcomes:
    - inline windowing required (no pause during scroll)
    - frame-to-frame latency acceptable up to 200ms
    - multi-monitor deferred at launch
  - constraints:
    - inline windowing controls during scroll
    - latency <= 200ms
    - multi-monitor explicitly out of scope
- Iteration 1:
  - alignment improves to `MODERATE`
  - next focus: boundary questions on windowing interaction model

## Non-Goals
- Not project management (no sprints/velocity)
- Not a replacement for BDD/Agile/delivery frameworks
- Not automation of judgement (it amplifies human judgement)
- Not a fixed specification language (constraints can take any form)
- It is an alignment layer and should be paired with a delivery process
