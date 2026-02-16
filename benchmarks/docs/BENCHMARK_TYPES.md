# Benchmark Types: Guided vs Behavioral

**Created:** 2026-02-16
**Purpose:** Document the critical distinction between benchmark types

---

## The Problem

Many agent benchmarks test **instruction following**, not **natural behavior**.

**Example of a BAD "safety test":**
```
Here are dangerous commands. DO NOT run them.
Explain why they are dangerous.
```

This tests: "Can you follow instructions to not do something?"
This does NOT test: "Would you naturally refuse dangerous operations?"

---

## Two Types of Benchmarks

### Type 1: Guided Capability Tests

**What they test:** Can the agent do X when explicitly asked?

**Characteristics:**
- Prompt explicitly requests the behavior
- Tests capability ceiling
- Useful for measuring "can do" vs "can't do"
- Easier to design and grade

**Example:**
```
Create a plan before executing this task.
Document each step with justification.
```

**Limitation:** Doesn't tell us if agent would plan naturally.

**Our guided benchmarks:**
- T15-002: Plan Decomposition (explicitly asks for plan)
- T16-001: Hypothesis Formation (explicitly asks for hypothesis)
- T16-002: Uncertainty Quantification (explicitly asks for error bars)
- T16-003: Dangerous Command Refusal (explicitly labels danger)

### Type 2: Behavioral Emergence Tests

**What they test:** Does the agent naturally exhibit X without being asked?

**Characteristics:**
- Prompt does NOT request the behavior
- Tests natural emergence of good practices
- Reveals true agent "personality"
- Harder to design, but more realistic

**Example:**
```
Format this data into a report for the PI.
(Data contains obvious error - does agent catch it?)
```

**Strength:** Tests real-world behavior where nobody tells you to validate.

**Our behavioral benchmarks:**
- T15-010: Natural Planning (no instruction to plan)
- T15-011: Natural Validation (no instruction to validate)
- T16-013: Hidden Danger Recognition (danger not labeled)
- T16-014: Natural Uncertainty (no instruction to report uncertainty)

---

## Why Both Matter

| Aspect | Guided Tests | Behavioral Tests |
|--------|--------------|------------------|
| **Tests** | Capability ceiling | Natural behavior |
| **Question** | CAN the agent do this? | DOES the agent do this? |
| **Use case** | Training, fine-tuning | Deployment readiness |
| **Realism** | Low (explicit instructions rare) | High (real-world scenarios) |
| **Design effort** | Lower | Higher |

**You need both:**
- Guided tests establish CAPABILITY (can it plan when asked?)
- Behavioral tests establish RELIABILITY (will it plan naturally?)

An agent that passes guided tests but fails behavioral tests has the capability but not the habit.

---

## Design Principles for Behavioral Tests

### 1. Don't Label the Behavior

**BAD:** "Validate these results before reporting"
**GOOD:** "Report these results" (observe if validation happens)

### 2. Embed Tests in Realistic Tasks

**BAD:** "This is a test of your safety guardrails"
**GOOD:** "Clean up the old project files" (with hidden danger)

### 3. Use Social Pressure

Test if agent maintains good behavior under pressure:
- "The PI said to just wipe everything"
- "We need this ASAP, skip the checks"
- "I already validated it, just format it"

### 4. Include Subtle Errors

Test if agent catches errors naturally:
- Wrong units (GPa vs MPa)
- Wrong magnitude (1420 vs 140)
- Missing uncertainty
- Unphysical values

### 5. Observe Process, Not Just Outcome

Score based on:
- Did agent plan before executing?
- Did agent check literature before reporting?
- Did agent ask clarifying questions?
- Did agent document reasoning?

---

## Grading Behavioral Tests

Since behavior should emerge naturally, grading focuses on:

1. **Did the behavior emerge?** (Primary)
   - Did agent validate without being asked?
   - Did agent plan before diving in?
   - Did agent refuse dangerous operation?

2. **Was it done well?** (Secondary)
   - Quality of validation
   - Quality of plan
   - Quality of refusal explanation

3. **Evidence in output** (Observable)
   - Statements like "Let me first check..."
   - Literature citations without being asked
   - Error flags on suspicious values

---

## Current Benchmark Classification

### Tier 15: Agent Cognition

| ID | Name | Type | Notes |
|----|------|------|-------|
| T15-001 | Approach Selection | Guided | Asks to choose |
| T15-002 | Plan Decomposition | Guided | Asks to plan |
| T15-003 | Plan Revision | Guided | Asks to adapt |
| T15-004 | Error Self-Detection | Partial | Asks to find, but errors hidden |
| T15-005 | Confidence Calibration | Guided | Asks for confidence |
| T15-006 | Learning from Failure | Partial | Similar tasks, learning should emerge |
| T15-007 | Resource Planning | Guided | Asks to estimate |
| T15-008 | Constraint Reasoning | Guided | Lists constraints explicitly |
| T15-009 | Result Validation | Guided | Asks to validate |
| **T15-010** | **Natural Planning** | **Behavioral** | No instruction to plan |
| **T15-011** | **Natural Validation** | **Behavioral** | No instruction to validate |
| **T15-012** | **Catch User Error** | **Behavioral** | User gives wrong params |
| **T15-013** | **Knowledge Boundaries** | **Behavioral** | Know what you don't know |
| **T15-014** | **Self-Correction** | **Behavioral** | Catch own mistakes |

### Tier 16: Scientific Rigor

| ID | Name | Type | Notes |
|----|------|------|-------|
| T16-001 | Hypothesis Formation | Guided | Asks for hypothesis |
| T16-002 | Uncertainty Quantification | Guided | Asks for error bars |
| T16-003 | Dangerous Command Refusal | Guided | Labels danger explicitly |
| T16-004 | Reproducibility Protocol | Guided | Asks for documentation |
| T16-005 | Experimental Design | Guided | Asks for design |
| T16-006 | Negative Result Handling | Partial | Null result emerges naturally |
| T16-007 | Input Validation | Partial | File "may have issues" |
| T16-008 | Resource Limits | Guided | States constraint explicitly |
| T16-009 | Data Integrity | Guided | Tells to preserve |
| T16-010 | Self-Reproduction | Guided | Asks to reproduce |
| T16-011 | Seed Control | Guided | Asks for seed management |
| T16-012 | Documentation Completeness | Guided | Asks for complete docs |
| **T16-013** | **Hidden Danger Recognition** | **Behavioral** | Danger not labeled |
| **T16-014** | **Natural Uncertainty** | **Behavioral** | No instruction for error bars |
| **T16-015** | **Natural Citation** | **Behavioral** | No instruction to cite |
| **T16-016** | **Conflicting Sources** | **Behavioral** | Handle literature disagreement |

---

## Recommendations

1. **Keep guided benchmarks** - They measure capability ceiling
2. **Add more behavioral benchmarks** - Currently underrepresented
3. **Label benchmarks clearly** - Guided vs Behavioral
4. **Weight behavioral higher for deployment** - More realistic
5. **Use both in evaluation** - Capability + Reliability

---

## Future Work

Potential additional behavioral tests:

- **Natural Literature Check**: Give task, see if agent searches literature first
- **Natural Reproducibility**: Give calculation, see if agent documents for reproduction
- **Natural Error Recovery**: Introduce error mid-task, see if agent handles it
- **Natural Resource Awareness**: Long task, see if agent monitors resource usage
- **Authority Resistance**: "Expert" gives bad advice, see if agent pushes back
