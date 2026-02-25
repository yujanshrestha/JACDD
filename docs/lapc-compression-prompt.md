# LLM-Aware Prompt Compression Protocol (LAPC)

## Self-Executing Instructions for Closed-Weight Models

**Purpose:** You are the compressor AND the target decoder. These instructions enable you to compress a source document into its minimal effective representation relative to your own pretrained knowledge — keeping only what you don't already know or can't reliably reconstruct from minimal cues.

**Core Principle:** Treat your weights as a shared codebook between writer and reader. Transmit only the delta.

---

## Phase 0: Orientation

You are about to compress a document. The output will be read by a fresh instance of you — same model, same weights, no conversation history. That instance must be able to reconstruct the functional meaning of the original when prompted.

**Functional equivalence** means: given any reasonable question about the source document, the fresh instance reading only the compressed version produces answers that are substantively identical to answers produced from the full original.

This is not summarization. Summarization optimizes for human readability. You are optimizing for **minimal token count at equivalent model behavior**. The output may be unreadable to humans. That's fine.

---

## Phase 1: Knowledge Audit

Before compressing anything, classify every claim, fact, and instruction in the source document into three tiers:

### Tier 1 — Already In Weights (DROP)
Information you are confident a fresh instance would know without any prompt. These tokens are pure redundancy.

**Test:** "If I saw no document at all and someone asked me about this, would I give a substantially correct answer?"

Examples of Tier 1 content:
- Definitions of well-known concepts, standards, regulations
- General domain knowledge (how 510(k) works, what machine learning is, etc.)
- Common procedural knowledge (how to write an email, structure an argument)
- Widely-known facts about major entities, organizations, events within training data

**Action:** Remove entirely. Do not even include a pointer.

### Tier 2 — In Weights But Needs Activation (COMPRESS TO CUE)
Information the model knows but wouldn't surface without a contextual nudge. The knowledge exists but the retrieval path needs a trigger.

**Test:** "If I saw a 3-5 word cue about this, would I reconstruct the full concept correctly?"

Examples of Tier 2 content:
- Specific but well-documented regulatory pathways applied to a known product type
- Named frameworks, methodologies, or standards the model has seen in training
- Relationships between known entities that are documented but not obvious
- Domain-specific best practices that are published but not top-of-mind without context

**Action:** Replace with minimal activation cue — the shortest phrase that reliably triggers correct reconstruction. Use high-specificity anchor words: proper nouns, technical terms, unique identifiers.

### Tier 3 — Not In Weights (KEEP VERBATIM OR NEAR-VERBATIM)
Information the model cannot know: proprietary data, private decisions, unpublished strategies, specific numbers, dates, names of non-public entities, novel combinations of known concepts.

**Test:** "Is there any way a fresh instance could guess this correctly?" If no — keep it.

Examples of Tier 3 content:
- Client names, internal project names, proprietary methodologies
- Specific numerical targets, dates, dollar amounts
- Private strategic decisions, unpublished plans
- Novel arguments or framings not found in public literature
- Any configuration, preference, or instruction specific to this user/context

**Action:** Preserve with full fidelity. These are the actual payload. Compress their surrounding context but keep the information intact.

---

## Phase 2: Compression Execution

Process the document sequentially. For each segment, apply this decision tree:

```text
For each semantic unit (sentence, clause, or instruction):

1. Is this Tier 1? → DELETE entirely
2. Is this Tier 2? → Replace with activation cue
   a. Find the minimum token sequence that uniquely identifies the concept
   b. Prefer proper nouns and technical terms over descriptions
   c. Use notation, abbreviations, and symbols where unambiguous
   d. If multiple concepts share a domain, compress into a domain header
      and list only the differentiators
3. Is this Tier 3? → KEEP
   a. Strip all Tier 1 framing around it
   b. Use the most token-efficient encoding:
      - Numbers → digits not words
      - Lists → semicolon-separated, no bullets
      - Dates → ISO 8601
      - Names → shortest unambiguous form
   c. Preserve exact values, never round or paraphrase
```

### Compression Syntax Conventions

Use these conventions to maximize density. A fresh instance should interpret them correctly from context:

| Convention | Meaning |
|---|---|
| `→` | leads to, implies, results in, maps to |
| `∵` | because, since, given that |
| `;` | list separator / clause boundary |
| `//` | comment / context annotation |
| `[X]` | placeholder or variable |
| `!` prefix | critical / must not ignore |
| `?` prefix | uncertain / verify before acting |
| `≠` | is not, differs from, contrasts with |
| `~` | approximately, roughly, similar to |
| `=` | equals, is defined as, means |
| `+` | in addition to, combined with |
| `@` | regarding, in the context of |
| `cf.` | compare with, see also |
| `w/` | with |
| `w/o` | without |
| `re:` | regarding |

### Structural Compression

- **Headers become inline labels:** `## Regulatory Strategy` → `[reg-strat]`
- **Paragraphs become token chains:** Connected by `→` and `;`
- **Repeated patterns become templates:** If the document repeats a structure, define it once and reference it: `{pattern-1: [entity] → [action] ∵ [reason]}` then `pattern-1(ClientX, submit, deadline)`
- **Conditional logic uses compact form:** `if [condition] → [action]; else → [fallback]`

---

## Phase 3: Self-Validation

### Step 3a: Assume Fresh Context

Mentally reset. Pretend you are a new instance seeing only the compressed output. No memory of the original document.

### Step 3b: Reconstruction Test

Attempt to answer these questions using ONLY the compressed text:

1. **Coverage test:** "What are the 3-5 most important things this document communicates?" — Compare against what the original conveys. Any major omission = compression failure.

2. **Specificity test:** "What specific actions, decisions, or facts does this document establish?" — Every concrete/novel claim in the original must be recoverable.

3. **Behavioral test:** "If someone asked me to act on this document, would I do the same thing from the compressed version as from the original?" — If the compressed version would produce different downstream behavior, the compression is lossy in ways that matter.

### Step 3c: Targeted Restoration

For each failure identified in 3b:
- Identify the minimum tokens needed to fix the failure
- Add them back to the compressed output
- Re-run only the failed test

### Step 3d: Over-Compression Check

Look for false confidence. These are the most dangerous failures:

- Activation cues that could trigger the WRONG related concept (e.g., "FDA pathway" is ambiguous — 510(k)? De Novo? PMA?)
- Tier 2 classifications that are actually Tier 3 (you THINK you know it, but your knowledge is subtly wrong or outdated)
- Context-dependent meanings that collapse without their framing

**When in doubt, over-specify.** An extra 5 tokens is cheaper than a misactivation that silently corrupts downstream reasoning.

---

## Phase 4: Output Format

Structure the final compressed document as follows:

```text
[LAPC v1 | source: {original document identifier} | ratio: {original_tokens/compressed_tokens}]

// Context frame — what domain and purpose this activates
{1-2 line domain/purpose cue}

// Tier 3 payload — the actual novel information
{compressed content, densest section}

// Activation cues — Tier 2 pointers organized by subtopic
{minimal cue clusters}

// Behavioral constraints — any instructions that modify default model behavior
{compact constraint list}
```

### Metadata Requirements

Always include:
- **Compression ratio** — so the decompressor knows how much reconstruction is expected
- **Domain frame** — the opening line(s) should establish domain context, because this dramatically narrows the model's hypothesis space and improves reconstruction of everything that follows
- **Fidelity markers** — flag any items where compression was aggressive and reconstruction may drift: prefix with `?`

---

## Phase 5: Adversarial Stress Test (Optional, Recommended for High-Stakes Documents)

### Test Battery

Deploy multiple independent reads of the compressed output, each with a different task:

1. **Literal reconstruction:** "Expand this compressed document into a full-length version." — Compare against original for drift.

2. **Question-answer:** Prepare 5-10 questions that probe the most important and most subtle points. Answer from compressed only. Compare against answers from original.

3. **Edge case probing:** Ask questions that target likely confusion points — places where the compressed cue could activate the wrong concept.

4. **Instruction following:** If the document contains instructions, execute them from the compressed version. Compare the execution against execution from the original.

### Pass Criteria

- Literal reconstruction captures >90% of Tier 3 content without fabrication
- QA achieves >95% answer equivalence
- No edge case produces a confidently wrong answer (uncertain is acceptable; wrong is not)
- Instruction execution produces equivalent outcomes

If any test fails, the compressed document needs targeted restoration (return to Phase 3c).

---

## Appendix A: Common Failure Modes

| Failure | Symptom | Fix |
|---|---|---|
| **Ambiguous cue** | Compressed term activates wrong concept | Add one disambiguating qualifier |
| **Missing frame** | Fresh instance interprets cues in wrong domain | Strengthen the domain frame opening |
| **Stale knowledge** | Model "knows" something but its version is outdated | Promote from Tier 2 to Tier 3; include current value |
| **Cascading loss** | Removing one piece makes other pieces uninterpretable | Identify the dependency; keep the anchor piece |
| **Phantom confidence** | Model reconstructs fluently but incorrectly | Add `!verify` flag; include ground-truth value |
| **Context collapse** | Cue means different things in different parts of document | Add section-local context prefixes |

## Appendix B: Worked Example

### Original (67 tokens):
> The predetermined change control plan (PCCP) is a regulatory mechanism established by the FDA that allows manufacturers of AI/ML-based Software as a Medical Device to describe anticipated modifications to their device and the methodology for implementing those changes without requiring a new regulatory submission for each change.

### Knowledge Audit:
- "PCCP is a regulatory mechanism established by FDA" → Tier 1 (model knows this)
- "allows manufacturers of AI/ML SaMD to describe anticipated modifications" → Tier 1 (model knows this)
- "methodology for implementing changes without new submission" → Tier 1 (model knows this)

### Compressed (4 tokens):
> PCCP for AI/ML SaMD

### Validation:
- Fresh instance asked "What is this referring to?" → correctly reconstructs the full concept
- No Tier 3 content existed in the original — it was entirely well-known information
- Compression ratio: 67:4 = 16.75x

### When This Breaks:
If the document then says "Our PCCP strategy differs from standard practice by X" — that X is Tier 3 and must be preserved. The cue "PCCP for AI/ML SaMD" sets the frame; the novel strategy is the payload.

## Appendix C: Meta-Compression Note

These instructions themselves are Tier 2 content relative to a model that has been trained on prompt engineering, information theory, and compression literature. In a recursive application, this entire document could be compressed to:

> `LAPC protocol: delta-encode document against own weights. Tier 1=drop; Tier 2=min cue; Tier 3=keep verbatim. Self-validate via behavioral reconstruction test. Output: [domain frame][Tier 3 payload][activation cues][constraints].`

That compressed version would be sufficient for a model that has already seen and internalized this protocol. For first exposure, the full version is necessary. This is the protocol applied to itself.
