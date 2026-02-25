# JACDD: Judge-Aligned Constraint-Driven Development

A framework for quantifying and reducing the gap between what should be built and what will be built.

## The Problem

Software projects fail at alignment, not execution. A team builds a DICOM viewer for radiologists. The clinical lead wanted rapid scroll-through of a CT series with windowing adjustments in-flow. The engineers delivered a technically correct single-image viewer with a separate windowing dialog. The code works. The tests pass. The product is wrong.

This gap between stakeholder intent and delivered output is real but traditionally unmeasured. Requirements documents try to bridge it with words. JACDD bridges it with a measurable signal.

## The Core Insight

Every software project has two invisible regions. The **acceptable solution space** is the set of all outputs the stakeholder would accept -- inferred from their constraints, guidance, and revealed judgement. The **potential solution space** is the set of all outputs the implementer could actually produce, given their capabilities and context. These are not hard boundaries. They are probability distributions: constraints don't create binary in/out lines, they shift probability mass, making some solutions more likely than others.

The **Dice score** measures how much these two regions overlap -- the size of the intersection divided by the average size of both, yielding a value between 0 (no overlap) and 1 (perfect alignment). For the DICOM viewer: if the acceptable space is concentrated around fluid cine-loop workflows and the potential space is concentrated around click-per-image architectures, the Dice score is low. **Misalignment** is `1 - Dice(potential, acceptable)`. The goal is to drive it toward zero.

## How It Works

Three roles interact through a feedback loop.

The **Human** defines acceptability. They provide constraints -- requirements, acceptance criteria, user needs, verification tests, anything that narrows the solution space. Constraints can be expressed as **deltas against the current solution**, so the process is iterative, not big-bang. But constraints are imperfect proxies for intent -- written words never fully capture what a stakeholder means. That gap is where the **judgement interview** comes in: a structured conversation where questions sit right on decision boundaries. "Should the viewer allow windowing adjustments during scroll, or pause on a frame first?" If the Human's answer is immediate, the question was too easy. If they pause and say "good question" -- that's a decision boundary, and the system just learned something that no written constraint could have captured.

The **JACDD Judge** is the central engine. It ingests constraints, guidance, and work-in-progress -- including their histories. From this, it infers a model of the acceptable solution space and simulates a model of the potential solution space. It estimates the Dice score between these two models. When misalignment is detected, it suggests specific new constraints chosen to increase overlap. For the DICOM viewer, the Judge might surface: "The acceptable space strongly favors continuous scroll with inline windowing, but the potential space assumes a stop-and-adjust pattern. Suggest constraint: windowing controls must be operable without interrupting series navigation."

The **Implementer** is the entire production apparatus -- tooling, people, teams. The Judge models the implementer's capabilities to simulate what they would actually build.

## The Loop

1. The Judge ingests current constraints, guidance, and WIP (including histories).
2. It infers the acceptable space and simulates the potential space.
3. It estimates the Dice score and identifies where the spaces diverge.
4. It suggests constraints targeted at the divergence.
5. The Human applies judgement -- accepting, modifying, or rejecting the suggestions.
6. The cycle repeats. Each iteration narrows the gap.

History feeds forward. Prior constraints and prior WIP inform the next round. The system learns where alignment breaks down and targets those areas.

## What This Gets You

JACDD treats alignment as a continuous, measurable quantity rather than a binary hope. The Dice score is a concrete, directional signal -- not a feeling -- about whether you are building the right thing. Its reliability improves as the Judge ingests more constraints and judgement data; early scores are rough indicators, later scores carry more weight. The feedback loop does not just detect misalignment, it prescribes which constraints would fix it. And by modeling solution spaces as probability distributions rather than binary boundaries, the framework makes uncertainty a first-class concept -- neither what stakeholders want nor what teams can build is ever fully certain.

The Judge works with *models* of acceptability and capability, not the things themselves. The map is never the territory. That is why calibration is continuous, not one-shot -- every iteration refines the model, and the judgement interview exists precisely to surface the places where the model is wrong.

The Judge does not replace human judgement. It makes human judgement scalable. Humans calibrate; the Judge propagates.
