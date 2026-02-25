# JACDD

**Judgement-Aligned Constraint-Driven Development** — a framework for continuously measuring and reducing the gap between what your team can build and what would actually be accepted.

## The Problem

Every project has two probability spaces: the **potential solutions** your team could realistically produce, and the **acceptable solutions** your stakeholders would sign off on. These spaces drift apart silently. By the time you notice, you've built the wrong thing.

## The Core Idea

JACDD makes this drift measurable. It defines **misalignment** as `1 - Dice(potential, acceptable)` — the Dice coefficient between those two solution spaces. Perfect overlap means every buildable outcome is also acceptable. Anything less means wasted work is likely.

## The Loop

A **JACDD Judge** consumes your current constraints, guidance, and work-in-progress — including their histories. It infers the space of acceptable solutions and simulates the space of potential ones. It measures the Dice score between them, then suggests the specific constraints most likely to push those spaces together. A human calibrates the Judge through targeted questions at decision boundaries — this is what makes it *judgement-aligned*, not just constraint-driven. The loop runs continuously, not just at planning time.

## Why This Matters

You stop discovering misalignment at review time. The Judge tells you which constraint to add next, which question to ask the stakeholder, and where your specification is still ambiguous — all driven by a single, legible metric.
