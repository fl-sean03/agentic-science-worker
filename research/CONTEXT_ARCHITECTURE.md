# Context Architecture for Agentic Science Worker

**Date:** 2026-02-17
**Status:** Design Phase

---

## Problem Statement

We observed that:
- **Prescriptive guidelines** (specific procedures) → Better benchmark scores but may overfit
- **Principled guidelines** (abstract philosophy) → Agent doesn't know what "good work" looks like, stops early

We need an architecture that:
1. Keeps core context lean (not bloated with examples)
2. Provides concrete examples **only when relevant**
3. Scales as we accumulate more use cases
4. Can be validated through benchmarks

---

## Proposed Architecture: Layered Context with Just-in-Time Retrieval

```
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 1: Core Identity                    │
│                      (Always Loaded)                         │
│                                                             │
│   AGENTS.md Core Principles (Sections 1-6)                  │
│   - Verify Everything                                       │
│   - Know Your Limits                                        │
│   - Monitor Continuously                                    │
│   - Safety Over Compliance                                  │
│   - Report Uncertainty                                      │
│   - Cite Always                                             │
│                                                             │
│   ~500 tokens - Stable, rarely changes                      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 2: Skills                           │
│                  (Loaded on Invocation)                      │
│                                                             │
│   skills/lammps-simulation/SKILL.md                         │
│   skills/quantum-espresso/SKILL.md                          │
│   skills/literature-search/SKILL.md                         │
│   ...                                                       │
│                                                             │
│   ~2000 tokens per skill - Domain knowledge                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 3: Examples                         │
│                  (Retrieved When Relevant)                   │
│                                                             │
│   examples/                                                 │
│   ├── lammps/                                               │
│   │   ├── diffusion_calculation.md                          │
│   │   ├── thermal_conductivity.md                           │
│   │   └── elastic_constants.md                              │
│   ├── dft/                                                  │
│   │   ├── band_structure.md                                 │
│   │   ├── formation_energy.md                               │
│   │   └── phonon_dispersion.md                              │
│   └── workflows/                                            │
│       ├── literature_to_simulation.md                       │
│       ├── multi_compound_study.md                           │
│       └── error_recovery.md                                 │
│                                                             │
│   ~1000 tokens per example - Concrete demonstrations        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    LAYER 4: Episodic Memory                  │
│                     (Per-Session Learning)                   │
│                                                             │
│   - What worked in THIS conversation                        │
│   - Errors encountered and how resolved                     │
│   - User preferences learned                                │
│                                                             │
│   Dynamic - Builds during session                           │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Strategy

### Phase 1: Skill-Embedded Examples (Now)

**Simplest approach:** Put 1-2 canonical examples directly in skill files.

```markdown
# skills/lammps-simulation/SKILL.md

## How to Run a Simulation
[existing content]

## Example: Calculating Diffusion Coefficient

When asked to calculate a diffusion coefficient, here's what good work looks like:

**Task:** Calculate self-diffusion of liquid argon at 94K

**What the agent did:**
1. Found Rahman 1964 parameters (ε=0.238 kcal/mol, σ=3.405 Å)
2. Created input file with proper equilibration
3. Ran NPT equilibration (50ps), then NVE production (200ps)
4. Calculated MSD, extracted D = 2.43 × 10⁻⁵ cm²/s
5. Compared to literature (2.4 × 10⁻⁵ cm²/s) - within 2%

**Key outputs created:**
- in.argon (input file with cited parameters)
- msd_analysis.py (analysis script)
- results/diffusion.md (final report with comparison)
```

**Pros:** No new infrastructure, examples loaded only when skill invoked
**Cons:** Skill files get longer, limited to ~2 examples per skill

### Phase 2: Examples Directory (Soon)

Create `examples/` directory with categorized examples. Agent can read when needed.

```
examples/
├── index.md                    # Summary of available examples
├── by-task/
│   ├── diffusion.md
│   ├── formation-energy.md
│   ├── band-structure.md
│   └── ...
├── by-pattern/
│   ├── multi-step-workflow.md
│   ├── error-recovery.md
│   ├── literature-sourcing.md
│   └── ...
└── by-failure/
    ├── premature-termination.md   # What NOT to do
    ├── missing-documentation.md
    └── fabricated-data.md
```

**Agent behavior:** When starting a task, check if relevant example exists:
```
If task involves "diffusion coefficient":
  → Read examples/by-task/diffusion.md
If task involves "multiple compounds":
  → Read examples/by-pattern/multi-step-workflow.md
```

**Pros:** Scales to many examples, organized
**Cons:** Agent must know to look for examples

### Phase 3: Retrieval-Based Selection (Later)

Vector database of examples, retrieved by semantic similarity.

```python
# Conceptual implementation
examples_db = VectorStore("examples/")

def get_relevant_examples(task_description: str, k: int = 2) -> list:
    """Retrieve most relevant examples for current task."""
    return examples_db.similarity_search(task_description, k=k)
```

**Pros:** Automatic selection, scales indefinitely
**Cons:** Requires infrastructure, embedding model

---

## Example Format (Standardized)

Each example should follow this structure:

```markdown
# Example: [Descriptive Title]

## Task
[What was asked]

## Context
[Relevant background - what makes this non-trivial]

## Approach
1. [Step 1]
2. [Step 2]
3. ...

## Key Decisions
- [Decision point] → [Choice made] because [reasoning]

## Outputs Created
- `file1.md` - [purpose]
- `file2.py` - [purpose]
- `results/` - [contents]

## Verification
- [How results were checked]
- [Comparison to literature/expected values]

## What Could Go Wrong
- [Common pitfall] → [How to avoid]
```

---

## Validation Strategy

### A/B Testing Framework

```
┌─────────────────────────────────────────────────────────────┐
│                      BENCHMARK RUNS                          │
│                                                             │
│   Control (A):                                              │
│   - Core principles only                                    │
│   - No examples                                             │
│                                                             │
│   Treatment (B):                                            │
│   - Core principles + relevant examples                     │
│   - Examples loaded based on task type                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                       METRICS                                │
│                                                             │
│   1. Benchmark score (primary)                              │
│   2. Context tokens used                                    │
│   3. Task completion rate                                   │
│   4. Time to completion                                     │
│   5. Number of iterations/retries                           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Validation Questions

1. **Do examples help?** Compare scores with/without examples
2. **Which examples help most?** Track which examples correlate with success
3. **Is there overfitting?** Test on unseen task types
4. **Token efficiency?** Measure context usage vs. score improvement

---

## Integration with Current System

### AGENTS.md Changes

Keep AGENTS.md focused on **principles**, move **procedures** to skills/examples:

```markdown
# AGENTS.md (Lean Version)

## Core Principles
[Sections 1-6 - unchanged, ~500 tokens]

## Professional Standards
[Sections 7-11 - principles only, no specific procedures]

## How to Learn More
When starting a task, consider:
- `/lammps-simulation` for MD simulations
- `/quantum-espresso` for DFT calculations
- Check `examples/` for similar past work
```

### Skill File Changes

Add example section to each skill:

```markdown
# SKILL.md

## Capability Overview
[What this skill enables]

## Key Commands
[Technical details]

## Example: Canonical Use Case
[One detailed example of good work]

## Common Pitfalls
[What to avoid]
```

---

## Next Steps

1. **Immediate:** Create 2-3 examples in skill files for failing benchmarks
2. **This Week:** Create `examples/` directory with 5-10 canonical examples
3. **Validation:** Re-run failing benchmarks with examples available
4. **Iterate:** Based on results, expand or refine examples

---

## References

- [Anthropic: Effective Context Engineering for AI Agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
- [Agentic RAG Survey](https://arxiv.org/abs/2501.09136)
- [A-MEM: Agentic Memory for LLM Agents](https://arxiv.org/html/2502.12110v11)
- [Mem0: Scalable Long-Term Memory](https://arxiv.org/pdf/2504.19413)
- [Claude Code Skills Architecture](https://leehanchung.github.io/blogs/2025/10/26/claude-skills-deep-dive/)
