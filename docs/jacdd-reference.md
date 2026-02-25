# JACDD: Judgement-Aligned Constraint-Driven Development

## Comprehensive Reference

**Author:** Yujan Shrestha
**Version:** 0.1 (working draft)

---

## Abstract

Judgement-Aligned Constraint-Driven Development (JACDD) is a framework for continuously measuring and reducing the gap between what a team can build and what stakeholders would actually accept. It models both "potential solutions" and "acceptable solutions" as probability density functions over a solution space, measures their overlap using a generalization of the Dice coefficient, and uses that single metric — called **Scope Alignment** — to drive a feedback loop that suggests constraints most likely to bring those two spaces into convergence. The framework introduces a formal role called the **JACDD Judge** that sits between the human (who defines acceptability through judgement) and the implementer (who defines what is producible), continuously simulating misalignment and recommending corrective constraints.

---

## 1. Motivation and Problem Statement

Every project has two probability spaces that matter:

1. **The space of potential solutions** — the set of outcomes your team, tools, and processes could realistically produce given current capabilities and constraints.
2. **The space of acceptable solutions** — the set of outcomes your stakeholders would sign off on, given their needs, preferences, and judgement.

These spaces drift apart silently. Conventional development processes discover misalignment at review time — during demos, code reviews, acceptance testing, or (worst case) post-launch. By then, work has been invested in solutions that fall outside the acceptable space. This is not merely "building the wrong thing." It is a structural failure of the feedback loop between intent and execution.

JACDD addresses this by making the drift **measurable in real time**, giving teams a legible, single-number metric (Scope Alignment) that drives targeted corrective action through constraint suggestion. The loop runs continuously, not just at planning milestones.

### What JACDD is not

- It is not a project management methodology (no sprints, no velocity).
- It is not a specification language (constraints can take any form).
- It is not a replacement for human judgement — it is a framework for capturing and operationalizing that judgement.

---

## 2. Formal Definitions

### Solution

A single point in the solution space. One realization of constraints. One deliverable. One codebase. One product. Critically, a solution could in itself be a specification — this makes the framework recursive. A solution at one level of abstraction (e.g., an architecture document) can serve as the constraint input for another level (e.g., an implementation).

### Solution Space

A region of the abstract space of all possible solutions, defined as **the boundary within which 95% of the probability mass lies** (analogous to a confidence interval). This is a statistical definition, not a hard boundary — there are solutions outside the space with non-zero but negligible probability.

### Constraint

A requirement, user need, acceptance criterion, verification test, or anything else that narrows the solution space. Constraints reduce uncertainty by eliminating regions of the space.

**Example:** "The API must respond in under 200ms" is a constraint that excludes all architectures incapable of meeting this latency requirement, collapsing the solution space along the latency dimension.

Constraints can also be expressed as **deltas relative to the current solution** rather than absolute specifications. For example, "reduce the response time by 50%" is a delta constraint that operates relative to the current state rather than declaring an absolute target. This is particularly useful in iterative development where the current solution is the natural reference point.

### Specification

A list of constraints. A specification defines a solution space by intersection — each constraint removes some region of possibility, and the resulting space is what satisfies all constraints simultaneously. A specification does not need to be complete; it merely needs to be sufficient to constrain the space to a useful degree.

### Implementation

The act of transforming constraints into a potential solution space. This is not a single step but an ongoing process. The implementer (see Section 3) takes the current specification and produces outcomes that probabilistically cluster in some region of the space.

### Judgement

The act of making a decision with imperfect information. Judgement is what distinguishes acceptable from unacceptable solutions when the specification is ambiguous or incomplete — which it always is. The source material states that judgement is "something only a human can do," and this claim requires careful examination.

The stronger and more defensible reading is: judgement is the **authoritative source of acceptability**. Whether the mechanism is a human brain, a calibrated model, or a committee, the point is that acceptability is not derivable from constraints alone — it requires an evaluative capacity that can handle ambiguity, weigh competing concerns, and make calls in edge cases. In the current state of the art, this capacity is most reliably sourced from humans with domain expertise, but the framework does not structurally require that the Judge be a biological entity. What it does require is that the Judge be **calibrated against human judgement** — the human remains the ground truth even if a model performs the inference.

Judgement is most effectively defined by a collection of **example scenarios**: possible choices, the chosen choice, and the reasoning behind it. This makes judgement an empirical, elicitable quantity rather than an abstract one.

### Judgement Interview

The act of asking targeted questions to model judgement. A good interview has a specific character: the questions fall right on **decision boundaries** and feel "hard" for the human but also "useful" for the specific problem at hand. The quality signal is the human saying "good question" — meaning the question forces them to articulate a distinction they hadn't previously made explicit.

**Example:** "If we can meet the latency requirement but only by caching aggressively, and caching introduces a 5-second staleness window, is that acceptable?" This question sits on the boundary between two constraints (latency vs. freshness) and forces the human to reveal which one dominates.

### Scope Alignment

The Dice coefficient between the potential solution space and the acceptable solution space:

```
Scope Alignment = Dice(Potential, Acceptable)
```

Ranges from 0 (no overlap — nothing buildable is acceptable) to 1 (perfect overlap — everything buildable is acceptable and vice versa).

### Misalignment

The complement of Scope Alignment:

```
Misalignment = 1 - Dice(Potential, Acceptable)
```

Ranges from 0 (perfect alignment) to 1 (total misalignment).

### Estimation

The act of estimating a continuous space from a finite set of samples. Since we cannot observe the entire solution space directly, we estimate the PDF from examples (past deliverables, prototypes, partial implementations).

---

## 3. The Three Actors and Their Responsibilities

JACDD identifies three distinct roles in the development process. These are roles, not people — a single person might fill multiple roles, or a role might be filled by a team or a tool.

### 3a. The Human

The Human is the source of **judgement** and the authority on **acceptability**. Their responsibilities:

- Define and refine the space of acceptable solutions through constraints and guidance.
- Calibrate the Judge's model of judgement through Q&A at decision boundaries (Judgement Interviews).
- Ask clarifying questions that tighten the specification.

The Human does not need to enumerate every acceptable outcome. They need to provide enough signal — through constraints, examples, and boundary-case answers — for the Judge to infer the acceptable space.

### 3b. The JACDD Judge

The Judge is the central engine of the framework. It sits between the Human and the Implementer, performing several functions:

- **Infers** the space of acceptable solutions from constraints, guidance, and calibration Q&A.
- **Simulates** the space of potential solutions from the implementer's capabilities, current WIP, and history.
- **Estimates** the Dice score between these two spaces (Scope Alignment).
- **Suggests constraints** most likely to increase the Dice score (reduce misalignment).
- **Consumes history**: both the history of constraints/guidance and the history of WIP.

The Judge is the only actor that holds a model of both spaces simultaneously. The Human knows what is acceptable but may not know what is buildable. The Implementer knows what is buildable but may not know what is acceptable. The Judge bridges this gap.

### 3c. The Implementer

The Implementer is the entire production apparatus: harness, people, and team. Their responsibilities:

- Transform constraints into actual solutions (code, products, deliverables).
- Produce the **space of potential solutions** — the distribution of outcomes that their process could realistically generate.

The Implementer is not a single engineer. It is the complete system that converts specification into output, including tooling, automation, team dynamics, and skill sets. The potential solution space is a function of the Implementer's capabilities, not just their intentions.

---

## 4. Solution Spaces as Probability Density Functions

This is one of JACDD's most important modeling choices. Solution spaces are not discrete sets of options. They are **probability density functions** (PDFs) over the abstract space of all possible solutions.

### Why PDFs?

A team does not have an equal chance of producing every possible outcome. Some outcomes are much more likely given their skills, tools, habits, and current trajectory. Similarly, stakeholders do not regard all technically-compliant solutions as equally acceptable — some are strongly preferred, others are barely tolerable. PDFs capture this gradation naturally.

### The 95% Boundary

JACDD defines a "solution space" operationally as the region containing 95% of the probability mass. This is analogous to a confidence interval. It acknowledges that:

- There are extremely unlikely but theoretically possible outcomes outside the boundary.
- The boundary is fuzzy, not sharp.
- The choice of 95% is a convention, not a physical law — teams could use 90% or 99% depending on their risk tolerance.

### Implications for the Dice Coefficient

The classical Dice coefficient is defined for sets:

```
Dice(A, B) = 2|A ∩ B| / (|A| + |B|)
```

When the solution spaces are PDFs rather than discrete sets, this requires generalization. The continuous analog uses integration over the minimum of the two density functions:

```
Dice(f, g) = 2 ∫ min(f(x), g(x)) dx / (∫ f(x) dx + ∫ g(x) dx)
```

Since `f` and `g` are proper PDFs (integrating to 1), the denominator simplifies to 2, giving:

```
Dice(f, g) = ∫ min(f(x), g(x)) dx
```

This is equivalent to the **intersection area** of the two distributions, which ranges from 0 (disjoint supports) to 1 (identical distributions). This formulation is sometimes called the **overlap coefficient** or **Ruzicka similarity** in the statistical literature.

### Why Not Other Divergence Measures?

Several alternatives exist for measuring distributional similarity, and the choice of Dice/overlap is deliberate:

| Measure | Why not for JACDD |
|---|---|
| **KL Divergence** | Asymmetric — KL(f\|\|g) ≠ KL(g\|\|f). Misalignment should be the same regardless of which space you start from. Also undefined when support of g doesn't cover f. |
| **Wasserstein Distance** | Measures the "cost" of transforming one distribution into another, not the degree of overlap. Two distributions could have low Wasserstein distance but poor overlap if they are narrow and slightly offset. |
| **Jaccard Index** | Equivalent to Dice for sets (monotonically related: J = D/(2-D)), but the Dice coefficient gives higher weight to overlap and is more sensitive to partial alignment, which is the quantity we want to optimize for. |
| **Cosine Similarity** | Treats distributions as vectors and measures angular similarity. Does not account for the magnitude/concentration of the distributions. |

The Dice/overlap formulation has the properties JACDD needs: it is **symmetric**, ranges from **0 to 1**, directly measures **overlap** (not distance or divergence), and degrades gracefully (a small improvement in alignment always produces a small improvement in score).

---

## 5. Process Architecture

### 5a. The Constraint-Judgement Loop (Diagram 1)

The core operational loop of JACDD:

```
                  ┌─────────────────────────────────┐
                  │          JACDD Judge             │
                  │                                  │
  Constraints_n ──┤──► infers acceptable space       │
  WIP_n ──────────┤──► simulates potential space     │
  Q&A ────────────┤──► calibrates judgement model    │
                  │                                  │
                  │    estimates Misalignment =      │
                  │    1 - Dice(potential, acceptable)│
                  │                                  │
                  │    suggests constraints to       │
                  │    maximize Dice score            │
                  └──────────────┬───────────────────┘
                                 │
                                 ▼
                  Constraints likely to reduce
                  misalignment
                                 │
                                 ▼
                  ┌──────────────────────────────────┐
                  │  Added to Constraints_(n+1)      │
                  │  History preserved                │
                  └──────────────────────────────────┘
```

**Inputs at each iteration n:**

1. **Constraints_n**: The current specification, plus the full history of how it evolved.
2. **WIP_n**: The current work in progress, plus the full history of prior deliverables.
3. **Q&A**: Question-and-answer pairs from Judgement Interviews that calibrate the Judge's model of acceptability.

**Process:**

1. The Judge consumes all three inputs.
2. It **infers** the space of acceptable solutions from constraints, guidance, and calibrated judgement.
3. It **simulates** the space of potential solutions from the implementer's track record, current WIP, and capabilities.
4. It **estimates** the Dice score between these two spaces.
5. It computes Misalignment = 1 - Dice.
6. It **suggests** new constraints — the ones most likely to push the two spaces toward convergence.

**Output:** A set of proposed constraints that, if adopted, would reduce misalignment. These are suggestions, not mandates — the Human reviews and refines them.

### 5b. The Human-Judge-Implementer Ecosystem (Diagram 2)

The broader ecosystem showing how the three actors relate:

```
  ┌──────────┐        Constraints        ┌──────────────┐
  │          │──── + Guidance ──────────► │              │
  │  Human   │                           │  JACDD Judge │
  │          │◄──── Clarifying ──────────│              │
  │          │      Questions            │              │
  └──────────┘                           │  infers      │
                                         │  acceptable  │
                                         │  space       │
                                         │              │
                                         │  evaluates   │
  ┌──────────────────┐                   │  against     │
  │   Implementer    │                   │  potential    │
  │ (harness+people  │ ── potential ───► │  space       │
  │  +team)          │    solutions      │              │
  └──────────────────┘                   │  estimates   │
       ▲                                 │  Dice score  │
       │                                 └──────────────┘
       │                                        │
       └──── constraint suggestions ◄───────────┘
```

The Human provides constraints and guidance (which are PDFs over the solution space). The Implementer produces the space of potential solutions (also a PDF). The Judge holds models of both, measures their overlap, and generates feedback that flows back to both the Human (as clarifying questions) and the process (as constraint suggestions).

The goal: **maximize the Dice score of potential vs. acceptable**.

---

## 6. The Feedback Mechanism

### 6a. Misalignment Simulation

The Judge does not merely measure current misalignment — it **simulates** what the misalignment would be under different constraint configurations. This is what enables the suggestion mechanism: the Judge can evaluate candidate constraints by their expected impact on the Dice score before they are actually adopted.

This simulation requires a model of how:

- Adding a constraint changes the acceptable space (typically narrows it).
- Adding a constraint changes the potential space (may narrow it, shift it, or leave it unchanged depending on whether the implementer can satisfy it).
- The Dice score responds to these changes.

### 6b. Constraint Suggestion

The Judge's primary output is **constraint suggestions**: specific constraints that, if adopted, would most effectively increase the Dice score. The suggestion mechanism works by identifying the dimensions of the solution space where the two distributions diverge most and proposing constraints that address those specific divergences.

**Example:** If the acceptable space strongly favors mobile-responsive designs but the potential space (based on the team's history) is concentrated around desktop-only implementations, the Judge might suggest: "All pages must render correctly on viewports from 320px to 1440px wide." This constraint narrows the potential space to the region that overlaps with the acceptable space along the responsiveness dimension.

Not all suggested constraints are equally valuable. The Judge should rank suggestions by **expected Dice improvement** — the predicted increase in Scope Alignment if the constraint is adopted.

### 6c. Delta-Based Constraints

Constraints can be expressed in two forms:

1. **Absolute constraints**: "The system must handle 1000 concurrent users." These define a fixed boundary in the solution space.
2. **Delta constraints**: "Increase concurrent user capacity by 3x relative to the current implementation." These define a boundary relative to the current solution.

Delta constraints are natural in iterative development. The source material explicitly annotates that suggested constraints "can be deltas vs the current solution." This is important because:

- The current solution is a known point in the space, making delta constraints easier to evaluate.
- Delta constraints compose naturally with iterative processes.
- They avoid the need to specify absolute targets when the current state is the most relevant reference point.

---

## 7. The Judgement Model

### 7a. What is Judgement?

Judgement in JACDD is the capacity to evaluate solutions under ambiguity. It answers questions that the specification cannot: "Is this acceptable?" when the spec is silent, contradictory, or underdetermined.

Judgement is not a binary function. It is a **distribution over evaluations** — a given solution might be judged acceptable with high confidence, acceptable with low confidence, or unacceptable. This fuzziness is what makes the PDF representation natural: the acceptable solution space has density that reflects the strength of the Judge's confidence in each region.

### 7b. Judgement Interviews

A Judgement Interview is the primary mechanism for calibrating the Judge's model of human judgement. The process:

1. The Judge identifies **decision boundaries** — regions of the solution space where its model is most uncertain about acceptability.
2. It formulates questions that target those boundaries, forcing the human to make a call.
3. The human answers, revealing which side of the boundary is acceptable and (critically) **why**.
4. The Judge updates its model, sharpening the boundary.

**What makes a good interview question:**

- It sits on a **decision boundary** — the answer could go either way.
- It feels "hard" for the human — forcing them to think, not just recall.
- It feels "useful" for the problem — the distinction matters for the actual solution.
- The human responds with "good question" — meaning the question surfaced a latent preference or tradeoff they hadn't explicitly considered.

**Example interview sequence:**

1. "If the search feature returns results in 50ms but occasionally shows stale data (up to 30 seconds old), is that acceptable?"
2. "What if the staleness window is 5 minutes instead of 30 seconds?"
3. "What if we can guarantee freshness but response time increases to 500ms?"

Each question probes a different facet of the latency-freshness tradeoff, progressively mapping the boundary of acceptability.

### 7c. Calibration Through Q&A

The source material lists "Question and answers (to calibrate judgement model)" as a distinct input to the Judge, separate from the constraints and WIP. This suggests a structured calibration process:

- The Q&A pairs form a **training set** for the judgement model.
- Each pair consists of a scenario (a point or region in the solution space) and an evaluation (acceptable, unacceptable, preferred, with reasoning).
- The Judge uses these pairs to interpolate its model of acceptability across the full space.

The relationship between Judgement Interviews and Q&A calibration can be understood as: Judgement Interviews are the **method** of generating Q&A pairs, while the Q&A corpus is the **data** that the Judge consumes for calibration. The interviews are active (the Judge chooses what to ask), while the Q&A input is passive (historical pairs that may come from any source).

---

## 8. History and Versioning

JACDD explicitly incorporates history as a first-class input. Both the "history of constraints + guidance" and the "history of WIP" feed into the Judge at each iteration. This has several implications:

### Why history matters

1. **Trajectory inference**: The Judge can estimate not just where the potential solution space is now, but where it is heading. A team that has been converging toward a particular architecture is likely to continue in that direction.
2. **Constraint evolution**: Understanding how constraints have changed reveals which dimensions of the problem are stable vs. volatile. Constraints that keep changing may indicate unresolved ambiguity in the acceptable space.
3. **Regression detection**: If a previously-satisfied constraint becomes violated in a new iteration, the Judge can flag this specifically.
4. **Convergence monitoring**: The history of Dice scores across iterations reveals whether the process is actually converging (alignment improving) or oscillating.

### Versioning scheme

Each iteration produces:

- `Constraints_n`: The constraint set at iteration n.
- `WIP_n`: The work-in-progress state at iteration n.
- `Dice_n`: The estimated Scope Alignment at iteration n.
- `Suggestions_n`: The constraints suggested by the Judge at iteration n.

The full history `{(Constraints_i, WIP_i, Dice_i, Suggestions_i) : i = 0..n}` is available to the Judge and can be used to detect trends, oscillations, and structural patterns in the alignment trajectory.

### The Bootstrap Problem

At iteration 0, there is no history. The Judge must operate with:

- An initial set of constraints (however rough) — `Constraints_0`.
- Either no WIP (greenfield project) or existing artifacts as `WIP_0`.
- Possibly zero Q&A pairs (no calibration data yet).

In this state, the Judge's estimates will be highly uncertain. The appropriate response is to **prioritize Judgement Interviews**: ask the Human the questions that would most rapidly reduce uncertainty about the acceptable space. The first few iterations of a JACDD loop should be dominated by calibration activity, with constraint suggestion becoming more prominent as the Judge's model matures.

---

## 9. Design Principles and Philosophical Notes

### Alignment is a continuous quantity, not a binary gate

Traditional development treats alignment as a gate: you pass review or you don't. JACDD treats it as a scalar that can be measured, tracked, and optimized at every point in the process. This shifts the conversation from "did we build the right thing?" (answered too late) to "how aligned are we right now, and what would improve it?" (answered continuously).

### Constraints are reductions of uncertainty, not mandates of form

A constraint does not dictate what the solution looks like. It eliminates what it cannot be. The solution space after applying constraints is everything that survives — there is still enormous freedom within it. This is why JACDD is constraint-driven rather than specification-driven: specifications tend to over-prescribe, while constraints merely prune.

### The Judge is an inference engine, not an oracle

The Judge estimates alignment — it does not determine it. Its model of the acceptable space is an approximation, calibrated by human input but never perfect. This is by design: the framework assumes that perfect knowledge of the acceptable space is unattainable (if it were attainable, you wouldn't need judgement — you'd just have a complete specification). The Judge's value is in making the best estimate possible from available information and identifying where more information would help most.

### Judgement is the scarce resource

The framework is designed around the assumption that human judgement is the bottleneck. The Judge's role is to make the most efficient use of that scarce resource by asking the right questions at the right time — targeting decision boundaries where the human's input will have the largest impact on the alignment estimate.

### Delta thinking over absolute thinking

The annotation that constraints "can be deltas vs the current solution" reveals a deeper principle: in iterative development, the most natural and actionable framing is often relative to the current state. "Make it faster" is more actionable than "make it fast" when you have a working system. Delta constraints compose well with iterative loops and avoid the need for complete upfront specification.

---

## 10. Open Questions and Future Directions

### How do you compute the Dice score in practice?

The framework defines Dice over continuous PDFs in a high-dimensional abstract solution space. In practice, you cannot evaluate this integral analytically. Possible approaches include:

- **Monte Carlo sampling**: Sample solutions from both distributions and estimate overlap from the samples.
- **Proxy metrics**: Define low-dimensional projections of the solution space (e.g., latency, coverage, UX scores) and compute Dice in the projected space.
- **Learned embeddings**: Train a model to embed solutions in a metric space where Dice can be approximated.

None of these are specified by the framework. The practical computation of Scope Alignment remains an open implementation question.

### What happens when constraints conflict?

If two constraints are mutually exclusive (e.g., "the system must be real-time" and "the system must run on a $5/month server"), the intersection of acceptable constraints is empty or near-empty. The Dice score with the potential space would collapse. How should the Judge handle this? Should it detect constraint conflicts explicitly? Should it report which constraints are in tension? The framework implies that the Judge would suggest relaxing one of the conflicting constraints, but the mechanism for this is not specified.

### Can the Judge model itself?

If the Judge is an inference engine, it has its own uncertainty about its estimates. Should the framework track not just the Dice score but the **confidence** in that score? A Dice score of 0.7 with high confidence is very different from 0.7 with massive uncertainty. Meta-uncertainty could drive different actions (more calibration vs. more implementation).

### How does JACDD interact with existing development processes?

The framework describes a loop but not an integration pattern. How does a JACDD Judge integrate with Scrum ceremonies? With CI/CD pipelines? With code review workflows? Is the Judge invoked at pull request time? At sprint planning? Continuously in the background? The framework is agnostic, but practical adoption requires specific integration guidance.

### Is the 95% boundary the right convention?

The definition of solution space as "the boundary at which 95% of solutions lie" is a convention. In safety-critical domains, you might want 99.9%. In exploratory prototyping, 80% might suffice. Should the boundary be configurable? Should different dimensions of the solution space use different thresholds?

### How does JACDD handle multi-stakeholder acceptability?

The framework models "acceptable solutions" as a single PDF. In reality, different stakeholders may have different — even contradictory — notions of acceptability. Should the Judge maintain separate acceptable-space models per stakeholder and compute alignment against each? Should there be an aggregation mechanism? Weighted Dice scores?

### What is the relationship between Judgement Interviews and Reinforcement Learning from Human Feedback (RLHF)?

The Judgement Interview mechanism — presenting boundary cases to humans and using their evaluations to refine a model — bears structural similarity to RLHF as used in training language models. Is there a formal connection? Can techniques from RLHF (reward modeling, preference learning) be directly applied to the Judge's calibration process?

### Can a JACDD loop be nested?

Since a solution can itself be a specification, can you run a JACDD loop at multiple levels of abstraction simultaneously? For example, a high-level JACDD loop aligning product strategy with market needs, feeding constraints into a lower-level JACDD loop aligning implementation with the product specification. How do the Dice scores at different levels relate?

---

## 11. Worked Example: Building a Search Feature

To make the framework concrete, consider a team building a search feature for an e-commerce platform.

**Iteration 0 (Bootstrap):**

- `Constraints_0`: "Users need to be able to search for products by name, category, and attributes."
- `WIP_0`: None (greenfield).
- The Judge has no history and no calibration. Its estimate of both spaces is highly uncertain.
- **Action:** Conduct Judgement Interviews.

**Judgement Interview:**

- Judge asks: "If search returns results in 200ms but doesn't support typo correction, is that acceptable?"
- Human: "No, typo correction is critical — many of our users misspell brand names."
- Judge asks: "What about phonetic matching? If a user searches for 'addidas' should they find 'Adidas'?"
- Human: "Yes, absolutely. Good question."
- Judge asks: "Should search results be personalized based on user history, or identical for all users?"
- Human: "Identical for now. Personalization is a separate feature."

**Iteration 1:**

- `Constraints_1`: Original constraint + "Must support typo correction and phonetic matching." + "Results must not be personalized."
- The Judge infers a narrower acceptable space (must handle misspellings, must not personalize).
- The Judge simulates the potential space based on the team's experience (they've built search before, using Elasticsearch).
- `Dice_1`: Estimated at 0.4 — moderate misalignment. The acceptable space requires fuzzy matching capabilities that the team's default Elasticsearch setup doesn't handle well.
- **Suggestion:** "Add a constraint specifying the minimum fuzzy matching accuracy on a standard typo dataset (e.g., correctly matching 90% of single-character typos)."

**Iteration 2:**

- The team implements a prototype with fuzzy matching.
- `WIP_2`: Working prototype with Elasticsearch fuzzy queries.
- `Dice_2`: Estimated at 0.65 — improving. The fuzzy matching works but the acceptable space also includes response time expectations that the prototype doesn't yet meet.
- **Suggestion:** "Clarify maximum acceptable response time. Current prototype averages 450ms; is this acceptable?"

This triggers another Judgement Interview round, and the loop continues.

---

## 12. Mathematical Summary

For reference, the core mathematical objects in JACDD:

| Symbol | Meaning |
|---|---|
| S | The abstract space of all possible solutions |
| f: S → R≥0 | PDF over S representing the potential solution space |
| g: S → R≥0 | PDF over S representing the acceptable solution space |
| Dice(f, g) | ∫ min(f(x), g(x)) dx (Scope Alignment) |
| M(f, g) | 1 - Dice(f, g) (Misalignment) |
| C_n | Constraint set at iteration n |
| W_n | Work-in-progress state at iteration n |
| g(· \| C_n) | Acceptable space conditioned on constraints at iteration n |
| f(· \| W_n) | Potential space conditioned on WIP at iteration n |

The JACDD loop optimizes:

```
max  Dice(f(· | W_n), g(· | C_n))
 C_n
```

subject to the constraint that C_n is achievable (the Human agrees to the constraints) and W_n is producible (the Implementer can generate it).

---

## 13. Glossary Quick Reference

| Term | Short Definition |
|---|---|
| **JACDD** | Judgement-Aligned Constraint-Driven Development |
| **Scope Alignment** | Dice(potential, acceptable) — the overlap metric |
| **Misalignment** | 1 - Scope Alignment |
| **Solution** | A single point in solution space |
| **Solution Space** | 95% probability mass boundary of a PDF over solutions |
| **Constraint** | Anything that narrows the solution space |
| **Specification** | A list of constraints |
| **Judgement** | Evaluative capacity under ambiguity; the authority on acceptability |
| **Judgement Interview** | Targeted questions at decision boundaries to calibrate the Judge |
| **JACDD Judge** | The inference engine that estimates alignment and suggests constraints |
| **Human** | The source of judgement and authority on acceptability |
| **Implementer** | The full production apparatus (harness + people + team) |
| **Delta Constraint** | A constraint expressed relative to the current solution |
| **Estimation** | Inferring a continuous space from finite samples |
