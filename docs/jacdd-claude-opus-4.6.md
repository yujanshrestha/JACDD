[LAPC v1 | source: docs/jacdd-reference.md + docs/raw-braindump-extraction.md | ratio: 1303/514 (wc-w proxy; ~2.54:1)]

// Context frame
JACDD measures overlap(team_would_build, stakeholder_would_accept) as Dice score; closes gap via boundary questions → constraints. Core problem: acceptable space & potential space drift apart silently; most processes discover gap at review time after wasted work. JACDD makes gap measurable + correctable throughout. !Not project mgmt, !not BDD/Agile replacement, !not automating judgement — amplifies it. Alignment layer only; pair w/ delivery process.

// Tier 3 payload
**Spaces**: acceptable (PDF ← stakeholder constraints+judgement) & potential (PDF ← team capability+WIP+habits). Both fuzzy/graded/uncertain; !not checklists. Solution space = boundary containing 95% of solutions. Single solution = one point/realization/deliverable.

**Metric**: Dice(f,g) = ∫min(f(x),g(x))dx; range 0→1; symmetric. Misalignment = 1 − Dice. Judge estimates qualitatively via five bands: CRITICAL (barely overlap) → LOW → MODERATE (gaps nameable) → GOOD (refinement) → HIGH (build-ready).

**Roles**: Stakeholder = source of judgement, defines acceptable. Judge = estimates alignment, asks boundary Qs, suggests constraints, consumes personality file; only role modeling both spaces. Team/Implementer = full production apparatus (people+tools+codebase); defines potential space. Constraints written w/ implementer in mind.

**Loop**: 1) estimate both spaces + alignment band → 2) 3-5 boundary Qs targeting largest divergences → 3) suggest 2-4 constraints ranked by Dice impact; stakeholder accepts/modifies/rejects → 4) re-estimate; repeat until HIGH or good-enough.

**Bootstrap** (iter 0): no history, max uncertainty; dominate w/ interview Qs; constraint suggestion grows as model matures; create initial personality file from codebase inventory (team) + goal (stakeholder skeleton).

**Judgement interview signals**: stakeholder pauses; says "good question"; forces choice between defensible options; concrete scenario-based !not abstract. Each answer → constraint narrowing gap.

**Personality file** (jacdd-personality.md @ project root): stakeholder section (preferences, judgement patterns, revealed priorities) feeds acceptable space; team section (strengths, weaknesses, tools, habits, blind spots) feeds potential space. Updated every iteration; human editable anytime.

**Commit archaeology**: git history encodes team thinking — granularity, message framing, co-location, sequencing → feeds team personality → refines potential space. Commit w/ intention.

**History**: full constraint + WIP + Q&A history enables trajectory detection, regression flagging, no re-suggesting rejected constraints, convergence monitoring.

**Constraint form**: absolute or delta vs current solution, whichever more actionable for the divergence. ?Constraints can also be expressed as specifications (list of constraints).

// Activation cues
Judge activates loop when: new project/feature (bootstrap), alignment band ≤ MODERATE, new WIP diverges from constraints, stakeholder signals changed preference, ?post-review regression detected. Interview dominates early; constraints dominate later. ?Personality file absence → treat as bootstrap.

// Behavioral constraints
1. Maximize Dice improvement per constraint; prefer fewer, higher-impact constraints over exhaustive lists.
2. Never re-suggest rejected constraints; track rejection in history.
3. Boundary Qs must be concrete+scenario-based; if stakeholder doesn't pause or engage, Q is too obvious — reformulate.
4. Always estimate alignment band before suggesting constraints; band frames constraint urgency.
5. Constraints take any form (requirement, acceptance criteria, delta, out-of-scope declaration) — !no specification language enforced.
6. Judge must consume personality file to sharpen both space estimates; !do not model spaces from constraints alone.
7. ?When Dice estimation is ambiguous between adjacent bands, report both w/ reasoning rather than false precision.
