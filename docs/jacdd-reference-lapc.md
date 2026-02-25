[LAPC v1 | jacdd-reference.md v0.2 — Yujan Shrestha | 671/213 (~3.15:1)]
// requirements-alignment framework: Dice overlap of 2 solution-space PDFs; iterative closure via boundary interviews → actionable constraints
!problem: spaces drift silently; gap discovered at review→wasted work; JACDD=measurable+correctable throughout

[T3 payload]
model: acceptable=PDF(stakeholder constraints+judgement); potential=PDF(team capability+WIP+habits); fuzzy/graded ≠ checklists; alignment=overlap
judge: !only role modeling BOTH spaces; estimates alignment band; asks boundary Qs; suggests constraints; consumes+updates personality_file
personality_file: jacdd-personality.md
  stakeholder→acceptable: preferences;judgement patterns;revealed priorities;decision tendencies ←interviews
  team→potential: strengths;weaknesses;tools;habits;blind spots ←codebase+git history
  update: judge every iteration; human anytime
commit→personality→potential: git(granularity→chunking;framing→priorities;co-location→grouping;sequencing→dependency thinking)→team section→potential space; !commit w/ intention
bands: CRITICAL ~0 overlap,misunderstand; LOW small,direction gaps; MODERATE meaningful,gaps nameable; GOOD strong,refinement; HIGH ~complete,build-ready
!metric design choice: qualitative only; Dice integral never computed; judge estimates via bands

[T3 process]
loop: estimate both spaces→interview(3-5 boundary Qs @largest divergences)→constrain(2-4 actionable constraints ranked by alignment impact;accept/modify/reject)→re-estimate→repeat→HIGH
bootstrap iter0: interview-dominant; constraint weight grows w/ model maturity; init personality: team←codebase inventory; stakeholder←goal skeleton
history: full constraint+WIP+Q&A trail→trajectory detection;regression flagging;!never re-suggest rejected;convergence monitoring

[T2 cues]
interview quality signals: pause;"good question";forced choice between defensible options;concrete not abstract; each answer→constraint
constraints: actionable > format; use as few constraints as possible for max overlap gain
roles: stakeholder=judgement source→acceptable; team=full production apparatus→potential

[behavioral constraints]
!alignment layer only—pair w/ delivery; not PM/velocity; not BDD/Agile replacement; amplifies judgement ≠ automates; constraints=any form
