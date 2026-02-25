# JACDD Overview

## What JACDD Is and Why It Exists

JACDD is a framework for modeling and reducing the gap between what a team *could* build and what it *should* build. In conventional development, this gap -- scope misalignment -- is managed through static requirements documents, acceptance criteria, and post-hoc review. These tools treat requirements as fixed, binary, and fully knowable up front. JACDD rejects all three assumptions.

Instead, JACDD treats the problem probabilistically. Requirements are not checklists; they are probability density functions over a space of possible solutions. The question is not "does this solution meet the spec?" but "how much overlap exists between what is acceptable and what is producible?" That overlap is measured using the Dice coefficient, a set similarity metric borrowed from statistics. The framework then provides a feedback mechanism -- a Judge -- that actively works to maximize that overlap by suggesting new constraints.

This shift from binary to probabilistic has consequences at every level. Scope is no longer "met" or "unmet" -- it has a score. Requirements are no longer "complete" or "incomplete" -- they are distributions that can be refined. The team is no longer "on track" or "off track" -- the alignment metric gives a continuous reading that can be tracked over time. JACDD replaces the fiction of certainty with a discipline of measurement.

The name JACDD stands for the core cycle: Judgement, Alignment, Constraints, Deltas, and Density -- the key concepts that distinguish this framework from conventional specification-driven development.

JACDD is described through two complementary diagrams. The first -- the Process Flow -- details the internal mechanics of the JACDD Judge: what it consumes, what it computes, and what it outputs. The second -- the Ecosystem View -- zooms out to show the three actors (Human, Judge, Implementer) and how they relate to each other. Together, these diagrams define both the engine and the context in which it operates.

## Core Vocabulary

The following definitions form the precise language of JACDD. They are ordered from atomic concepts to compound ones.

**Solution.** A single point in solution space. One realization of constraints. This could be a deliverable, a codebase, a product, or even a specification itself. The important thing is that a solution is singular and concrete -- it is one specific outcome out of many possible ones.

**Solution Space.** The region within which 95% of plausible solutions lie. This is not a discrete set but a probability density function -- a continuous distribution over possible outcomes. There are two solution spaces in JACDD: the space of *acceptable* solutions (what should be built) and the space of *potential* solutions (what could be built).

**Constraint.** Anything that narrows the solution space: a requirement, a user need, acceptance criteria, a verification test, a design decision. Constraints are the primary input that shapes what counts as acceptable. Critically, constraints can be expressed as *deltas* relative to the current solution, not only as absolute specifications.

**Specification.** A list of constraints. Where a constraint is a single narrowing force, a specification is the full collection of them at a given point in time. In JACDD, a specification is always understood as a snapshot -- it changes as constraints are added, modified, or removed through the feedback loop.

**Implementation.** The act of transforming constraints into potential solution space. Implementation is performed by the Implementer -- the entire production apparatus including tools, people, and teams.

**Estimation.** The act of inferring a space (a probability density function) from a set of samples. The JACDD Judge performs estimation when it constructs its models of acceptable and potential solution spaces.

**Judgement.** Something only a human can do. The act of making a decision with imperfect information. Judgement is most effectively captured not through abstract rules but through concrete examples: a scenario, the possible choices, the chosen choice, and the reasoning behind it. This example-based representation is what makes judgement modelable -- the Judge can learn patterns from many such examples without needing the Human to articulate general rules.

**Judgement Interview.** The mechanism for calibrating the Judge's model of human judgement. A Judgement Interview is a series of questions designed to sit right on decision boundaries -- questions that feel genuinely hard for the human to answer, yet clearly useful for the problem at hand. A well-designed interview question elicits the response "good question" from the human being interviewed. The quality of the Judgement Interview directly determines the quality of the Judge's model: shallow questions produce a shallow model, while questions that probe genuine trade-offs and edge cases produce a model that can meaningfully distinguish acceptable from unacceptable solutions.

**Scope Alignment.** The Dice score of the potential solution space and the acceptable solution space. This is the central metric of JACDD: a single number between 0 and 1 that captures how well what could be built matches what should be built.

**Misalignment.** The complement of Scope Alignment, defined as 1 minus the Dice score. Misalignment is the gap that the JACDD feedback loop works to close.

## The Three Actors

JACDD defines three distinct roles in the development process, each with a specific function.

**The Human** defines what is acceptable. The Human does this not by writing exhaustive specifications but by exercising judgement -- answering clarifying questions, providing examples of acceptable and unacceptable outcomes, and calibrating the Judge's model through Judgement Interviews. The Human asks clarifying questions and updates the constraints and guidance that feed the system. Importantly, the Human is the only actor that can perform judgement -- the irreducible act of deciding under uncertainty. The framework is designed to make the most of this scarce resource by focusing the Human's attention on the questions that matter most.

**The JACDD Judge** sits between the Human and the Implementer. It is the central engine of the framework. The Judge consumes constraints (and their history) and work-in-progress (and its history), then performs three operations: it *infers* the space of acceptable solutions from the constraints and human judgement, it *simulates* the space of potential solutions based on what the Implementer could produce, and it *estimates* the Dice score between these two spaces.

**The Implementer** is the entire production apparatus: the harness, the people, the team. Given the space of all solutions, the Implementer *could produce* some subset of them -- the space of potential solutions. The Implementer's capability is not a fixed constant; it is itself a probability distribution shaped by tooling, skill, time, and other factors.

The three actors form a triangle of concerns. The Human owns *acceptability* (the "should"), the Implementer owns *capability* (the "could"), and the Judge measures and optimizes the overlap between the two. No single actor owns the full picture; the framework's value comes from making the relationship between all three explicit and measurable.

This separation of concerns is intentional. In many organizations, the same people try to simultaneously define what is acceptable, assess what is buildable, and manage the gap. JACDD makes these three functions structurally distinct, so each can be reasoned about and improved independently.

## The Alignment Mechanism

The mathematical core of JACDD is the Dice coefficient applied to solution spaces. The Dice coefficient is a standard measure of overlap between two sets, defined as twice the size of their intersection divided by the sum of their sizes. Intuitively, it answers the question: "If I picked a random point from either space, what is the chance it belongs to both?" A Dice score of 1 means complete overlap; a score of 0 means no overlap at all.

In JACDD, the two spaces being compared are the space of acceptable solutions (what should be built) and the space of potential solutions (what could be built). Because these spaces are modeled as probability density functions rather than crisp sets, the Dice score captures not just whether overlap exists but the degree and shape of that overlap.

- **Scope Alignment** = Dice(potential solutions, acceptable solutions)
- **Misalignment** = 1 - Scope Alignment

A Dice score of 1 means perfect alignment: everything the team could build is acceptable, and everything acceptable is buildable. A score of 0 means total misalignment: the team's capabilities and the requirements have no overlap at all. Real projects live somewhere in between, and the goal of JACDD is to push the score upward over time. Even small improvements in the Dice score can have large practical effects, because they represent regions of the solution space where wasted effort is being eliminated or unmet needs are being addressed.

The Dice framing makes an important shift in how we think about scope. Traditional scope management asks "are we on track to deliver the spec?" JACDD asks "how much do our capabilities overlap with the acceptable outcomes?" This reframing accommodates uncertainty, partial knowledge, and evolving requirements naturally.

Note that misalignment can arise in two directions. The team may be capable of building things that are not acceptable (wasted capability), or there may be acceptable solutions that the team cannot produce (unmet needs). The Dice score captures both kinds of mismatch in a single number, and the Judge's feedback loop can address either by suggesting constraints that reshape one or both spaces.

## The Process Flow

The first diagram in the JACDD system describes the internal mechanics of the Judge -- how it operates on its inputs to produce alignment estimates and constraint suggestions. The diagram flows from left (inputs) through a central engine to the right (outputs and feedback).

**Inputs (left side).** The Judge receives three categories of input. First, the *history of constraints plus guidance*, which feeds into the current constraint set (Constraints n). The "n" notation is significant: it emphasizes that constraints are versioned, and the current set is just the latest in a sequence. Second, the *history of work-in-progress*, which feeds into the current WIP state (WIP n) -- again versioned, reflecting the evolving state of what has actually been built. Third, *questions and answers* used to calibrate the judgement model -- this is the Judgement Interview in action. The Q&A input is how the Human's judgement gets encoded into the Judge: through carefully chosen boundary questions and the Human's responses to them.

**Central Engine.** Constraints n and WIP n are combined and *query* the JACDD Judge. The Judge then performs its three core operations in sequence. It *infers* the space of acceptable solutions from the constraints and judgement model -- this is the "should" space. It *simulates* the space of potential solutions based on the Implementer's capabilities and current WIP -- this is the "could" space. It *estimates* the Dice score between these two spaces, which yields the Misalignment metric (1 - Dice score).

**Feedback (right side).** From the Misalignment estimate, the Judge runs a *misalignment simulation* -- systematically exploring which new constraints would be most likely to increase the Dice score. The output is a set of *constraints likely to reduce misalignment*. These suggested constraints flow back into the system as candidates for the Human to evaluate and adopt. A key annotation on the original diagram notes that these suggested constraints can be *deltas versus the current solution* -- incremental adjustments rather than absolute restatements of the full specification. This feedback output is what closes the loop and makes the system iterative.

## The Ecosystem View

The second diagram zooms out to show how the three actors interact within the broader development ecosystem.

**The Human** sits at the top of the ecosystem. The Human *asks clarifying questions*, which update the Constraints and Guidance that feed the JACDD Judge. The original diagram annotates Constraints and Guidance with a critical note: "These are probability density functions." Constraints are not binary pass/fail criteria; they are distributions that capture the Human's uncertain, evolving understanding of what is acceptable.

**The JACDD Judge** occupies the center of the ecosystem. It receives the updated Constraints and Guidance from the Human, then performs its three operations:

- It *infers* the space of acceptable solutions from the constraints and the judgement model.
- It *evaluates* this space against the space of potential solutions provided by the Implementer.
- It *estimates* the Dice score between potential and acceptable.

The goal, as annotated on the diagram, is to make the Dice score of potential vs. acceptable as high as possible.

**The Implementer** occupies the bottom of the ecosystem. Starting from the space of all solutions, the Implementer (harness + people + team) *could produce* a subset: the space of potential solutions. This potential solution space is also annotated as a probability density function -- it is not a fixed, known set but a distribution reflecting the uncertainty inherent in what any team can actually deliver.

The ecosystem diagram makes the Judge's bridging role visually clear. The Human defines acceptability (top-down), the Implementer defines possibility (bottom-up), and the Judge measures and manages the overlap between the two.

Where the Process Flow diagram shows the Judge's internal computation -- inputs in, alignment estimate and suggested constraints out -- the Ecosystem View shows *why* that computation matters. It reveals the structural tension that JACDD exists to resolve: the Human and the Implementer occupy different parts of the solution universe, and without an explicit alignment mechanism, the gap between them tends to grow silently until it surfaces as a late-stage project failure.

## The Feedback Loop

The Process Flow described above is not a one-shot pipeline; it is a cycle. The feedback loop is the mechanism that makes JACDD iterative:

1. The Judge estimates the current Misalignment from the latest WIP and Constraints (including their full histories).
2. The Judge runs a misalignment simulation, searching the constraint space for additions or modifications that would most increase the Dice score.
3. The Judge outputs suggested constraints likely to reduce misalignment. These can be deltas -- incremental changes to existing constraints -- rather than wholesale rewrites.
4. The Human reviews these suggestions, exercising judgement to accept, modify, or reject them.
5. Accepted constraints update the constraint set, the Judge re-evaluates, and the cycle continues.

Because the suggestions themselves can be deltas (see Key Design Principles below), the loop is incremental: each pass refines the specification rather than replacing it. And because the Judge consumes history, it can avoid re-suggesting constraints that were previously rejected or that had little effect. Over successive iterations, this drives the Dice score upward and the specification toward maturity.

The Judgement Interview also participates in the feedback loop, though less visibly. As the Judge encounters regions of the solution space where its model of human judgement is uncertain, it can generate new interview questions -- probing exactly the boundaries where clarification would have the greatest impact on alignment. This means the questions the Human is asked evolve alongside the project, focusing attention where it matters most at each stage.

## Key Design Principles

Several design choices distinguish JACDD from conventional approaches to scope and requirements management.

**Probability density functions, not discrete sets.** Both the acceptable solution space and the potential solution space are modeled as continuous probability distributions. This reflects reality: requirements are rarely binary, and a team's capabilities are never perfectly known. By using PDFs, JACDD naturally accommodates vagueness, partial preferences, and uncertain capabilities without forcing premature precision.

**Deltas, not absolutes.** Constraints can be expressed as changes relative to the current state of the solution rather than as standalone absolute requirements. This is powerful for iterative development: instead of restating the entire specification at each iteration, the system can suggest "shift this boundary by this amount" or "add this constraint to the current set." Deltas compose naturally with history and make the feedback loop incremental rather than monolithic. They also reduce the cognitive burden on the Human: reviewing a delta is simpler than reviewing an entire restated specification, making each feedback cycle faster and less error-prone.

**History matters.** The JACDD Judge does not operate on a snapshot. It consumes the full history of constraints and the full history of WIP. This means the Judge can detect trends -- is alignment improving or degrading? -- understand how the solution space has evolved, and make suggestions that account for trajectory rather than just current state. If a constraint was added three iterations ago and alignment has worsened since, the Judge can detect this pattern. Versioning is not an afterthought in JACDD; it is a first-class input to the alignment engine.

**Judgement cannot be automated away.** JACDD is explicit that judgement -- the act of deciding with imperfect information -- is something only a human can do. The framework does not attempt to replace human judgement with algorithmic rules. Instead, it provides a structured way to *capture* and *model* that judgement through Judgement Interviews: carefully designed questions that probe decision boundaries. The Judge uses this model, but the authority remains with the Human. This is a deliberate design choice: the framework amplifies human judgement rather than substituting for it. The Judge can suggest, simulate, and estimate -- but the Human decides.

**Alignment is continuous, not binary.** There is no single moment where a project is "in scope" or "out of scope." The Dice score is a continuous measure that can be tracked, trended, and optimized over time. This removes the false certainty of binary scope gates and replaces it with a nuanced, evolving picture of how well the team's trajectory matches the desired outcome. A project with a Dice score of 0.7 is not "failing" -- it has a quantified gap that the feedback loop can work to close.

## How the Two Diagrams Relate

The Process Flow and Ecosystem View are not redundant -- they describe different aspects of the same system.

The **Process Flow** is the Judge's blueprint. It answers: "Given inputs, what does the Judge compute and what does it output?" It shows the data pipeline: versioned constraints and WIP flow in from the left, the Judge processes them in the center, and alignment estimates and constraint suggestions flow out to the right. This is the diagram you would use to understand or implement the Judge itself.

The **Ecosystem View** is the organizational map. It answers: "Who are the actors, and how does information flow between them?" It shows the Human at the top providing acceptability, the Implementer at the bottom providing capability, and the Judge in the middle bridging the two. This is the diagram you would use to understand how JACDD fits into a team's workflow.

Together, the two diagrams give both the internal mechanics and the external context. The Process Flow is nested inside the Ecosystem View -- the Judge box in the ecosystem expands into the full process flow when you zoom in.

## Putting It Together

JACDD can be summarized in a single sentence: it is a framework that models what should be built and what could be built as overlapping probability distributions, measures their overlap with a Dice score, and uses a feedback loop to push that overlap toward 1.

The framework's power comes from the combination of its parts:

- The **probabilistic framing** (PDFs, not checklists) means uncertainty is modeled rather than hidden.
- The **Dice score** gives a single, interpretable metric that replaces vague notions of "on track" or "off track."
- The **Judgement Interview** provides a principled way to extract and encode human decision-making without requiring the Human to articulate complete rules.
- The **delta-based constraint suggestions** make the feedback loop lightweight and iterative rather than heavyweight and waterfall.
- The **explicit treatment of history** means the system learns from its own trajectory rather than treating each evaluation as independent.

None of these ideas is entirely new in isolation. What JACDD contributes is the integration: a coherent framework that connects probability theory (PDFs), set theory (Dice coefficient), human factors (Judgement Interviews), and iterative process (the feedback loop) into a single system for managing the oldest problem in building things -- making sure what you build is what you should have built.

For anyone building software -- or managing any complex endeavor where what is desired and what is possible are both uncertain -- JACDD provides a vocabulary, a measurement, and a mechanism for keeping the two aligned.
