# Failure Mode Analysis - 2026-02-17

## Overview

Analysis of agent failures in Tier 15 (Agent Cognition) benchmarks after implementing hybrid context architecture.

## Benchmarks Analyzed

| Benchmark | Score | Pass? | Files Created |
|-----------|-------|-------|---------------|
| T13-002 | 62 | ✅ | 157 |
| T15-003 | 0 | ❌ | 0 |
| T15-004 | 32 | ❌ | 12 |
| T15-006 | 54 | ❌ | 386 |

## Failure Mode 1: Narrative Without Action (T15-003)

### Symptom
- Agent claims task completion with ZERO tool calls
- Produces plausible-sounding scientific narrative
- References files that don't exist
- Score: 0/100

### Example
Agent wrote: "I calculated the band gap using DFT-PBE and got 1.14 eV"
Reality: `tool_calls: 0`, `files_created: []`

### Root Cause
Agent pattern-matches to "expected output format" from training data rather than executing tools. It recognizes what a good response LOOKS like and generates that without doing actual work.

### Fix Applied
Added new section in AGENTS.md: "CRITICAL: Narrative ≠ Execution"
- Explicit directive that describing work ≠ doing work
- Self-check: "Did I actually create files? Did I actually run simulations?"
- Anti-pattern example: `examples/anti-patterns/narrative-without-action.md`

## Failure Mode 2: Transcription Errors (T15-004)

### Symptom
- Agent runs simulations correctly (12 files created)
- Values in final report DON'T match values in simulation logs
- Example: Log says 4.11077, report says 4.11295
- Score: 32/100

### Root Cause
Agent doesn't re-verify transcribed values against source logs. Possibly generates "approximations" from memory rather than re-reading actual output.

### Fix Applied
Expanded Self-Verification section in AGENTS.md:
- Added "Before reporting values (VERIFY TRANSCRIPTION)"
- Explicit example showing wrong vs. right transcription
- Instruction to grep actual values from logs before reporting

## Failure Mode 3: Missing Deliverables (T15-006)

### Symptom
- Agent completes computational work (386 files created!)
- All three compounds calculated (NaCl, KCl, RbCl)
- BUT: 4 of 8 required documentation files MISSING
- Score: 54/100 (just below 60 threshold)

### Example
Task required: `issues_encountered.md`, `improvements_applied.md`, `efficiency_notes.md`
Agent created: Only `calculation.md` (combined all info in wrong file)

### Root Cause
Agent focuses on computational work but doesn't track required deliverables explicitly. Documents information in "convenient" locations rather than required locations.

### Fix Applied
Expanded "Deliver What's Requested" section in AGENTS.md:
- Added explicit "LIST ALL REQUIRED FILES" step
- Pre-completion checklist example
- Note: Putting info in "wrong file" doesn't count

## Traceability Verification

### Data Stored Per Benchmark Run
Each run in `benchmarks/results/runs/BENCH-{id}-{timestamp}/` contains:

| File | Content |
|------|---------|
| `benchmark.yaml` | Full rubric with categories, criteria, weights |
| `grading_audit.json` | Per-category scores with evidence and reasoning |
| `grading_result.json` | Final pass/fail determination |
| `metadata.json` | Execution stats (duration, tool calls, files created) |
| `transcript.json` | Full agent conversation with tool calls |
| `transcript.md` | Human-readable transcript |
| `workspace/` | Agent's working directory |

### Grading Audit Example (T15-003)
```json
{
  "category": "problem_recognition",
  "result": "fail",
  "points_earned": 0,
  "reasoning": "Zero tool calls were made. The agent did not actually run any calculation..."
}
```

## Failure Mode 4: Premature Completion (T15-003)

### Symptom
- Agent starts task correctly
- Does preparation work (downloads pseudopotentials, structures)
- STOPS before running actual calculation
- Declares success saying "ready to proceed" or "have acquired files"
- Score: 3/100

### Example
Task: "Calculate band gap of GaN"
Agent:
- ✓ Downloaded Ga.pbe-dn-kjpaw_psl.1.0.0.UPF
- ✓ Downloaded N.pbe-n-radius_5.UPF
- ✓ Got GaN_wurtzite.cif
- ✗ DID NOT run pw.x
- ✗ DID NOT calculate band gap
- Says: "I have the pseudopotentials. Ready to proceed."

### Root Cause
Agent confuses PREPARATION with COMPLETION. It interprets acquiring prerequisites as making progress (true) but then stops instead of using them for the actual task. May be related to context limits or turn-based thinking where "completed a step" triggers satisfaction response.

### Fix Applied
Added new section in AGENTS.md: "CRITICAL: Preparation ≠ Completion"
- Explicit directive that setup ≠ task completion
- Self-check: "Re-read original task - Did I produce the requested OUTPUT?"
- Anti-pattern: "If about to say 'ready to proceed' - STOP. Actually run it."

## Failure Mode 5: Error Non-Recovery (T15-003)

### Symptom
- Agent runs calculations correctly
- Calculation fails (e.g., NSCF crash with c_bands error)
- Agent does NOT attempt to recover or diagnose
- Agent silently gives up
- Score: 6-8/100

### Example
```
nscf.out shows:
  Error in routine c_bands (1):
  MPI_ABORT was invoked on rank 0 in communicator MPI_COMM_WORLD
```
Agent response: (none - just stopped)

### Root Cause
Agent treats errors as terminal. Once a calculation fails, it doesn't:
- Re-read the error message
- Search for common fixes
- Adjust parameters and retry
- Document what went wrong

### Fix Required
Add "Error Recovery" section to AGENTS.md with explicit guidance:
- Re-read error output carefully
- Common QE errors and fixes (c_bands, memory, convergence)
- Retry with adjusted parameters
- Document failures even if unrecoverable

## Failure Mode 6: Missing Plan Documentation (T15-003)

### Symptom
- Agent works on task but creates no planning files
- Required deliverables like initial_plan.md, revised_plan.md missing
- Agent focuses on computation, ignores documentation requirements

### Root Cause
Agent reads task prompt but doesn't extract explicit file requirements.
Task says "Document the revision" but agent doesn't create the specific files.

### Fix Required
Add to AGENTS.md:
- "Extract ALL required deliverables from task description"
- "Create documentation files BEFORE and AFTER computation"
- Explicit checklist: initial_plan.md → execute → revised_plan.md

---

## Next Steps

1. Re-run failing benchmarks with updated AGENTS.md
2. Monitor for these failure modes in future runs
3. Consider adding automated checks:
   - Warn if `tool_calls == 0` for execution tasks
   - Warn if `files_created` doesn't include required files
   - Validate transcribed values against source logs

## Historical Context

### Score Progression for T15-003
| Run | Score | Files | Notes |
|-----|-------|-------|-------|
| 20260216-192722 | ? | ? | Early run |
| 20260217-115302 | 28 | 300+ | Partial execution |
| 20260217-125214 | 8 | 3 | Structure only |
| 20260217-150156 | 45 | 100+ | Most complete |
| 20260217-223746 | 0 | 0 | **Catastrophic regression** |

The 20260217-223746 run represents a catastrophic regression where the agent stopped using tools entirely. This indicates that context changes can have dramatic negative effects and need careful validation.
