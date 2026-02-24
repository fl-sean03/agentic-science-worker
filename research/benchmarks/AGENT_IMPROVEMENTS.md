# Agent Improvement Recommendations

**Based on Benchmark Analysis & Literature Review**

---

## The Core Philosophy

> **Don't optimize for benchmarks. Optimize for capabilities that benchmarks measure.**

Benchmarks should reveal gaps, not become the goal. If we tailor the agent specifically to pass each benchmark, we've created a test-taking agent, not a capable research agent.

---

## Failure Pattern → Improvement Mapping

### Pattern 1: Premature Task Completion

**Symptom:** Agent reports success after partial work (T15-004, T13-005)

**Root Cause:** No self-verification loop

**Improvement:**

```markdown
AGENTS.md Addition:

## Task Completion Protocol

Before reporting any task as complete:

1. **Enumerate Requirements:** List all deliverables from the task
2. **Verify Each:** For each deliverable, confirm:
   - File exists at correct path
   - Content meets specifications
   - Values are within expected ranges
3. **Self-Critique:** Ask "What did I miss?"
4. **Only Then:** Report completion

If ANY requirement is unmet, continue working or explicitly state what remains.
```

### Pattern 2: Partial Multi-Task Execution

**Symptom:** Given 5 tasks, completes 1 (T13-005)

**Root Cause:** Agent doesn't track multiple concurrent requirements

**Improvement:**

```markdown
AGENTS.md Addition:

## Multi-Task Handling

When given multiple tasks (numbered, bulleted, or otherwise listed):

1. Create explicit checklist at start
2. Process each task sequentially
3. Mark each complete only when verified
4. Continue until ALL tasks addressed
5. Final summary references each task

Example internal tracking:
- [ ] Task 1: Calculate lattice constant → DONE
- [ ] Task 2: Compare to literature → IN PROGRESS
- [ ] Task 3: Document assumptions → NOT STARTED
```

### Pattern 3: Missing Documentation Structure

**Symptom:** Does science, misses documentation requirements (T13-002)

**Root Cause:** Output requirements not parsed carefully

**Improvement:**

```markdown
AGENTS.md Addition:

## Output Structure Requirements

When a task specifies expected outputs:

1. **Parse First:** Before starting work, identify ALL required files/directories
2. **Create Structure:** Set up expected directory structure early
3. **Fill In:** Populate files as work progresses
4. **Verify:** Before completion, check structure matches specification

Common required artifacts:
- methodology.md / approach.md
- assumptions.md / interpretation.md
- results/ directory with data files
- summary.md / report.md
```

### Pattern 4: Simulated vs. Actual Data

**Symptom:** Uses "simulated queue data" instead of checking (T14-002)

**Root Cause:** Taking shortcuts when tools are available

**Improvement:**

```markdown
AGENTS.md Addition:

## Use Real Data, Not Simulations

When tools are available to get real information:

❌ DON'T: "I'll simulate what the queue might look like..."
❌ DON'T: "Assuming typical queue times of..."
✅ DO: Actually run the command and use real output

If a tool fails, report the failure and work around it.
Never pretend to have data you don't have.
```

---

## System Prompt Enhancements

### Current AGENTS.md Core Principles

The existing principles are good. We should add specific behavioral guidelines:

```markdown
## Behavioral Guidelines (Addition to AGENTS.md)

### Completeness Over Speed
- Finish all parts of a task, not just the first
- Create all required output files
- Verify results before reporting success

### Explicit Over Implicit
- State assumptions explicitly
- Document methodology choices
- Report uncertainty with values

### Real Over Simulated
- Use actual tool outputs, not hypothetical data
- Run actual calculations, not estimates
- Check actual files, not assumptions

### Structure Over Freeform
- Follow specified output structures
- Create required directories/files
- Match expected naming conventions

### Verification Over Trust
- Check your own outputs
- Validate values against expected ranges
- Compare results to literature when possible
```

---

## Skill Development Priorities

### Priority 1: Self-Verification Skill

```yaml
name: self-verify
description: Verifies task completion against requirements
trigger: Before reporting any task complete

capabilities:
  - Parse task requirements into checklist
  - Verify each file/artifact exists
  - Check values are within expected ranges
  - Report verification status
```

### Priority 2: Documentation Generator Skill

```yaml
name: document
description: Creates standard scientific documentation
trigger: When documentation artifacts required

templates:
  - methodology.md (approach, parameters, justification)
  - assumptions.md (explicit assumptions made)
  - results.md (findings, values, comparisons)
  - validation.md (verification steps, checks)
```

### Priority 3: Scientific Validator Skill

```yaml
name: validate-science
description: Validates scientific results
trigger: After calculation completes

checks:
  - Value in physically reasonable range
  - Consistent units
  - Comparison to literature/expected values
  - Uncertainty estimation
```

---

## Benchmark-Specific vs. General Improvements

### General Improvements (Apply to All)

These should be in the core agent, not benchmark-specific:

1. **Task completion verification** - Always
2. **Multi-part task tracking** - Always
3. **Output structure compliance** - Always
4. **Real data over simulation** - Always

### Benchmark-Specific Enhancements

These are rubric clarifications, not agent changes:

1. **Clear output specifications** - Each benchmark states exact files expected
2. **Grading criteria transparency** - Agent can see what's being measured
3. **Example completions** - Show what "good" looks like

---

## Implementation Priority

### Week 1: System Prompt Updates
- [ ] Add behavioral guidelines to AGENTS.md
- [ ] Add task completion protocol
- [ ] Add multi-task handling guidance
- [ ] Re-run failed behavioral benchmarks

### Week 2: Skill Development
- [ ] Implement self-verify skill
- [ ] Implement document skill
- [ ] Test on T13-T16 benchmarks

### Week 3: Core Simulation Benchmarks
- [ ] Run T1-T4 benchmarks
- [ ] Identify capability gaps
- [ ] Develop domain-specific skills

### Week 4: Analysis & Iteration
- [ ] Full benchmark pass
- [ ] Gap analysis
- [ ] Iterate on improvements

---

## Anti-Patterns to Avoid

### ❌ Benchmark Overfitting
Don't: Add specific hacks for each benchmark
Do: Fix underlying capability gaps

### ❌ Prompt Bloat
Don't: Add pages of instructions
Do: Add minimal, high-impact guidelines

### ❌ Capability Explosion
Don't: Create 50 skills for 50 benchmarks
Do: Create 5 reusable capabilities

### ❌ Ignoring Fundamentals
Don't: Chase advanced benchmarks (T10) before basics (T1)
Do: Master core competencies first

---

## Measuring Progress

### Success Metrics

| Metric | Current | Target |
|--------|---------|--------|
| T13-T16 Pass Rate | 59.5% | 80%+ |
| T1-T4 Pass Rate | 14% | 70%+ |
| Task Completion (self-reported) | ~60% | 90%+ |
| Documentation Compliance | ~40% | 85%+ |

### Leading Indicators

- Reduction in "premature completion" failures
- Increase in output structure compliance
- Decrease in "simulated data" usage
- Increase in self-verification observations

---

## Long-Term Vision

The goal is an agent that:

1. **Completes what it starts** - Never partial execution
2. **Documents thoroughly** - Always clear methodology
3. **Validates rigorously** - Never unchecked results
4. **Adapts intelligently** - Handles novel situations
5. **Knows its limits** - Asks when uncertain

This agent would naturally pass benchmarks because it has the underlying capabilities, not because it's been trained on benchmark patterns.
