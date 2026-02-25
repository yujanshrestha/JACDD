[LAPC v1 | source: docs/jacdd-reference.md + docs/raw-braindump-extraction.md | ratio: 1288/566 (wc-w proxy; ~2.28:1)]

// Context frame
JACDD (Yujan Shrestha, v0.2) = measure overlap(team_would_build, stakeholder_would_accept); close gap via boundary questions → constraints. Core problem: acceptable space & potential space drift apart silently; most processes discover gap at review time after wasted work. JACDD makes gap measurable + correctable throughout. !Not project mgmt, !not BDD/Agile replacement, !not automating judgement — amplifies it. Alignment layer only; pair w/ delivery process.

// Tier 3 payload
**Two spaces**: acceptable (PDF ← stakeholder constraints+judgement) & potential (PDF ← team capability+WIP+habits). Both fuzzy/graded/uncertain; !not checklists. Solution space = boundary where 95% of solutions lie. Misalignment = 1 - Dice(potential, acceptable). Dice(f,g) = ∫min(f(x),g(x))dx; symmetric; bounded 0-1; measures overlap not distance. Judge estimates qualitatively via five bands: CRITICAL (barely any overlap) → LOW → MODERATE → GOOD → HIGH (near-complete; ready to build).

**Judgement interview**: judge asks boundary questions where preference could go either way. Good signals: stakeholder pauses; says "good question"; forces choice between defensible options; concrete scenario-based !not abstract. Each answer → constraint narrowing gap. Ex: "Search returns 50ms but occasionally stale data (≤30s). Acceptable?" → forces latency-vs-freshness reveal.

**Delta constraints**: requirements as changes relative to current state; composes w/ iteration; reduces cognitive burden. Ex: "reduce response time by 50%" > absolute spec when system exists. Constraints written w/ implementor in mind.

**Roles**: stakeholder = source of judgement, defines acceptable. Judge = estimates alignment, asks boundary questions, suggests constraints, models both spaces, consumes personality file. Team/implementer = full production apparatus (people+tools+codebase); defines potential space. Judge sits between human (acceptability) & implementer (possibility).

**Personality file** (jacdd-personality.md @ project root): stakeholder section (preferences, judgement patterns, revealed priorities, decision tendencies ← interviews) feeds acceptable space. Team section (strengths, weaknesses, tools, habits, blind spots ← codebase+history) feeds potential space. Updated by judge after every iteration; human can edit anytime.

**Commit archaeology**: git history encodes team thought process — granularity (chunking), message framing (priorities), co-location vs separation (conceptual grouping), sequencing (dependency thinking) → feeds team personality → refines potential space. Commit w/ intention.

**Loop**: 1) estimate both spaces, identify divergences, estimate band → 2) 3-5 boundary questions targeting largest divergences → 3) suggest 2-4 constraints (prefer deltas) ranked by alignment impact; stakeholder accepts/modifies/rejects → 4) update, re-estimate, repeat until HIGH or good enough. Bootstrap (iter 0): dominate w/ interview; constraint suggestion grows as model matures; create initial personality from codebase inventory + stakeholder goal skeleton. History enables trajectory detection, regression flagging, no re-suggesting rejected constraints, convergence monitoring.

**Solution** = single point; one realization of constraints; one deliverable/codebase/product. ?Solution could itself be a specification. **Specification** = list of constraints. **Implementation** = transforming constraints into potential solution space.

// Activation cues
Trigger JACDD when: alignment unknown/untested; new stakeholder or domain; scope feels assumed not validated; team defaults diverge from stakeholder expectations; post-review rework pattern detected. ?Activation unclear when constraints are purely technical w/o stakeholder judgement dimension.

// Behavioral constraints
Judge must model both spaces — never collapse to one perspective. !Never automate judgement; amplify it. Prefer delta constraints over absolute when system exists. Interview questions must be concrete+scenario-based; reject abstract preference polling. Do not re-suggest rejected constraints w/o new evidence. Personality file is living artifact — update every iteration. Constraints can take any form (!not a specification language). Alignment estimation is qualitative (five bands); !do not claim numeric Dice computation. History (constraints+WIP+Q&A) is mandatory input; stateless judging is anti-pattern.
