[LAPC v1 | source: docs/jacdd-reference.md + docs/raw-braindump-extraction.md | ratio: 1288/317 (wc-w proxy; ~4.06:1)]

// Context frame
requirements-alignment engine: model acceptable_space vs potential_space as PDFs; optimize overlap Dice(f,g)=∫min; misalignment=1-Dice; close via boundary interview→constraints loop.

// Tier 3 payload
!problem: acceptable/potential drift silently; late review discovers gap→waste.
spaces: acceptable=stakeholder constraints+judgement; potential=team capability+WIP+habits (team=people+harness+tools+codebase); both fuzzy/graded ≠ checklist.
alignment_bands: CRITICAL barely overlap/fundamental miss; LOW small overlap/major divergence; MODERATE meaningful overlap/gaps nameable; GOOD strong/refinement; HIGH near-complete/build-ready.
judge: only role modeling BOTH spaces; estimates band; asks boundary Qs on largest divergences; converts answers→constraints; suggests 2-4 constraints ranked by overlap impact; tracks accepted/modified/rejected.
loop: estimate→interview(3-5 Qs, one boundary at a time)→constrain(prefer delta vs current solution)→re-estimate→repeat until HIGH or "good enough".
bootstrap(iter0): max uncertainty; interview-heavy; initialize personality via team codebase+git inventory + stakeholder goal skeleton.
personality_file: jacdd-personality.md @project root; stakeholder section (preferences, judgement patterns, revealed priorities, decision tendencies)→acceptable model; team section (strengths, weaknesses, tools, habits, blind spots)→potential model; judge updates every iteration; human editable anytime.
history_inputs: full constraints + WIP + interview Q/A; enables trajectory/convergence, regression flags, !never re-suggest rejected constraints.
commit_archaeology: granularity→chunking style; message framing→priorities; co-location/separation→concept grouping; sequence→dependency thinking; principle=!commit w/ intention (judge learns team cognition from git).
?solution_space_def: boundary where ~95% candidate solutions lie.
example_dicom: goal cine-loop viewer; initial gap=lead wants inline windowing while team defaults separate dialog + single-image; iter0 alignment LOW; interview outputs inline windowing, frame latency <=200ms, multi-monitor deferred; constraints updated; iter1 MODERATE.

// Activation cues
judgement_interview quality: stakeholder pauses; says "good question"; forced choice between defensible options; concrete scenario not abstract; each answer narrows acceptable_space.
delta_constraint cue: "change relative to current state" composes better than absolute restatement.
definitions cue: scope_alignment=Dice(potential,acceptable); estimation=infer space from samples; solution=single point realization; spec=list of constraints.

// Behavioral constraints
!alignment layer only; pair w/ delivery process.
!not PM (no sprint/velocity), not BDD/Agile replacement, not spec language.
!amplifies human judgement; never automates authority.
!judge suggests; stakeholder decides; express uncertainty qualitatively (banded), avoid fabricated numeric score.
