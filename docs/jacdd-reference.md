meta:
  author: Yujan Shrestha
  version: "0.2"

what: measure overlap(team_would_build, stakeholder_would_accept); close gap via boundary questions → constraints

problem: acceptable space and potential space drift apart silently; most processes discover gap at review time after wasted work; JACDD makes gap measurable + correctable throughout

concepts:
  two_spaces:
    desc: acceptable + potential are fuzzy/graded/uncertain; not checklists
    acceptable: PDF shaped by stakeholder constraints + judgement
    potential: PDF shaped by team capability + WIP + habits

  alignment_bands:
    CRITICAL: barely any overlap; fundamental misunderstanding
    LOW: small overlap; major direction gaps
    MODERATE: meaningful overlap; specific gaps nameable
    GOOD: strong overlap; refinement phase
    HIGH: near-complete overlap; ready to build

  judgement_interview:
    desc: judge asks questions on decision boundaries where preference could go either way
    good_question_signals:
      - stakeholder pauses (not obvious)
      - says "good question" (surfaced latent tradeoff)
      - forces choice between two defensible options
      - concrete scenario-based; not abstract
    example: "Search returns results in 50ms but occasionally shows stale data (up to 30s). Acceptable?" → forces latency-vs-freshness reveal
    output: each answer becomes constraint narrowing gap

  delta_constraints:
    desc: requirements as changes relative to current state
    why: composes with iteration; reduces cognitive burden
    example: "reduce response time by 50%" > "response time must be under 200ms" when system exists

  personality_file:
    desc: persistent profile sharpening both space estimates
    stakeholder_section: preferences; judgement patterns; revealed priorities; decision tendencies (extracted from interviews)
    team_section: strengths; weaknesses; tools; habits; blind spots (extracted from codebase + history)
    feeds: acceptable space ← stakeholder section; potential space ← team section
    update_cadence: judge updates after every iteration; human can edit anytime
    file: jacdd-personality.md at project root

  roles:
    stakeholder: source of judgement; defines acceptable via constraints + interview answers
    judge: estimates alignment; asks boundary questions; suggests constraints; consumes personality file to sharpen both space estimates; only role modeling both spaces
    team: full production apparatus (people + tools + codebase); defines potential space

loop:
  1_estimate: model both spaces; identify divergences; estimate alignment band
  2_interview: 3-5 boundary questions targeting largest divergences; each reveals unwritten preference
  3_constrain: suggest 2-4 constraints (prefer deltas) ranked by alignment impact; stakeholder accepts/modifies/rejects
  4_repeat: update constraints; re-estimate; continue until HIGH or "good enough"

bootstrap:
  desc: iteration 0; no history; maximum uncertainty
  action: dominate with interview questions; constraint suggestion grows as model matures; create initial personality file from codebase inventory (team) + goal (stakeholder skeleton)

history:
  inputs: full history of constraints + WIP + interview Q&A
  enables: trajectory detection; regression flagging; no re-suggesting rejected constraints; convergence monitoring
  commit_archaeology:
    desc: git history encodes team thought process — what they group, separate, name, and sequence reveals how they think about changes
    signals: commit granularity (chunking style); message framing (priorities); co-location vs separation (conceptual grouping); sequencing (dependency thinking)
    feeds: team section of personality file; refines potential space model
    principle: commit with intention — structure git history as if the judge will read it to learn how you think

example:
  project: DICOM viewer for radiologists
  gap: clinical lead wants cine-loop scroll + inline windowing; engineers default to single-image viewer + separate windowing dialog
  iteration_0:
    goal: "Build DICOM viewer with cine-loop scrolling"
    alignment: LOW
    interview:
      - q: "Windowing adjustments pause scroll or work inline?"
        a: "Inline. Pausing breaks clinical workflow."
      - q: "200ms frame-to-frame latency acceptable?"
        a: "Yes, up to 200ms. Above that radiologists lose spatial context."
      - q: "Multi-monitor layouts at launch?"
        a: "Not at launch. Good question — matters eventually."
    constraints:
      - "Windowing controls operable during scroll (delta: add inline controls)"
      - "Frame-to-frame latency ≤200ms"
      - "Multi-monitor deferred (explicit out-of-scope)"
  iteration_1:
    alignment: MODERATE
    next: boundary questions on windowing interaction model

theory:
  model: solution spaces as PDFs over abstract outcome space
  metric: "Dice(f,g) = ∫ min(f(x),g(x)) dx"
  range: 0 (no overlap) to 1 (identical)
  properties: symmetric; bounded 0-1; measures overlap not distance
  practice: judge estimates qualitatively (five bands); integral not directly computable

not:
  - no project management (no sprints; no velocity)
  - no replacement for BDD/Agile/delivery frameworks
  - no automating judgement — amplifies it
  - no specification language — constraints take any form
  - alignment layer only; pair with delivery process
