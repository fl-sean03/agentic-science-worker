# Benchmark System Refactoring Plan

**Date:** 2026-02-16
**Status:** Phase 1 Complete

## Problem Statement

The current benchmark system has several critical issues that prevent effective evaluation and debugging:

1. **No traceability** - Can't see what agent did step-by-step
2. **Workspace deleted** - Can't inspect artifacts after run
3. **No grading audit** - Only final score, not per-check results
4. **Scattered rubrics** - Embedded in YAML, not reusable
5. **Two runners** - Confusion between harness.py and runner.py

## Goals

1. **Full Observability** - See every action the agent took
2. **Artifact Preservation** - Keep all files agent created
3. **Grading Transparency** - Audit trail for every scoring decision
4. **Standardized Rubrics** - Reusable, versioned grading criteria
5. **Single Entry Point** - One unified benchmark runner

---

## New Architecture

### Directory Structure

```
benchmarks/
├── README.md
├── run.py                      # Single entry point (replaces harness.py + runner.py)
│
├── tasks/                      # Benchmark definitions (unchanged)
│   ├── tier1_basic/
│   ├── tier2_intermediate/
│   └── ...
│
├── rubrics/                    # Standardized grading rubrics
│   ├── schema.yaml             # Rubric schema definition
│   ├── common/                 # Shared rubric components
│   │   ├── simulation_quality.yaml
│   │   ├── parameter_citation.yaml
│   │   └── documentation.yaml
│   └── tiers/                  # Tier-specific defaults
│       ├── tier1.yaml
│       └── tier2.yaml
│
├── evaluation/                 # Grading infrastructure
│   ├── executor.py             # Agent execution (extracted from harness)
│   ├── grader.py               # Unified grader (LLM + rules)
│   ├── audit.py                # Audit trail generation
│   └── validators/             # Validation primitives
│       ├── file.py
│       ├── simulation.py
│       ├── value.py
│       └── scientific.py
│
├── results/                    # Run results with full artifacts
│   └── {BENCH_ID}-{TIMESTAMP}/
│       ├── metadata.json       # Run metadata
│       ├── agent_transcript.md # Full agent conversation
│       ├── grading_audit.json  # Per-check grading results
│       ├── score_summary.json  # Final scores
│       └── workspace/          # Preserved agent workspace
│           ├── input/          # Input files provided
│           ├── output/         # Files agent created
│           └── logs/           # Simulation logs
│
└── docs/
    ├── AUTHORING_GUIDE.md
    ├── RUBRIC_GUIDE.md
    └── REFACTOR_PLAN.md        # This file
```

---

## Key Changes

### 1. Workspace Preservation

**Before:**
```python
# Workspace created, used, then deleted
workspace = create_workspace()
run_agent(workspace)
grade(workspace)
cleanup(workspace)  # DELETED!
```

**After:**
```python
# Workspace preserved in results directory
run_dir = results/BENCH-T1-001-20260216-120000/
workspace = run_dir / "workspace"
run_agent(workspace)
grade(workspace)
# Workspace stays in results directory forever
```

### 2. Grading Audit Trail

**Before:**
```json
{
  "score": 78,
  "status": "passed"
}
```

**After:**
```json
{
  "score": 78,
  "status": "passed",
  "audit": {
    "checks": [
      {
        "category": "setup_quality",
        "check": "lj_parameters_correct",
        "rule": "pair_coeff contains 0.238 3.405",
        "result": "PASS",
        "points": 10,
        "evidence": "Line 15: pair_coeff * * 0.238 3.405"
      },
      {
        "category": "setup_quality",
        "check": "atom_count_correct",
        "rule": "108 ± 10% atoms",
        "result": "FAIL",
        "points": 0,
        "evidence": "Found 96 atoms, expected ~108"
      }
    ],
    "grader": "rule_based",
    "grading_time_seconds": 2.3
  }
}
```

### 3. Agent Transcript

**Before:**
- `agent_output.txt` - Often empty, unstructured

**After:**
- `agent_transcript.md` - Structured markdown with:
  - Each tool call and result
  - Agent's reasoning
  - Timestamps
  - Token usage per turn

```markdown
# Agent Transcript: BENCH-T1-001

## Turn 1 (0:00)
**Agent Thinking:** I need to create a LAMMPS input file for LJ minimization...

**Tool Call:** Write
- File: input.lmp
- Content: [truncated, see workspace/output/input.lmp]

**Result:** File written successfully

## Turn 2 (0:05)
**Agent Thinking:** Now I'll run the simulation...

**Tool Call:** Bash
- Command: $LMP -in input.lmp
- Duration: 12.3s

**Result:** [Exit code 0, see workspace/logs/lammps.log]
```

### 4. Standardized Rubrics

**Before:** Rubrics embedded in each benchmark YAML

**After:** Rubrics in separate files, reusable

```yaml
# rubrics/common/simulation_quality.yaml
name: simulation_quality
description: Validates simulation execution quality
version: 1.0

checks:
  - id: simulation_completes
    description: Simulation runs to completion without errors
    type: file_contains
    file: "*.log"
    pattern: "Total wall time|Loop time"
    points: 20

  - id: no_warnings
    description: No critical warnings in output
    type: file_not_contains
    file: "*.log"
    patterns:
      - "ERROR"
      - "FATAL"
      - "nan"
    points: 10
```

### 5. Unified Runner

**Before:**
- `harness.py` (1002 lines)
- `runner.py` (520 lines)
- Different APIs, inconsistent behavior

**After:**
- `run.py` - Single entry point

```bash
# Run single benchmark
python benchmarks/run.py BENCH-T1-001

# Run tier
python benchmarks/run.py --tier 1

# Run with options
python benchmarks/run.py BENCH-T1-001 \
  --preserve-workspace \
  --grading-mode hybrid \
  --verbose
```

---

## Implementation Phases

### Phase 1: Foundation (COMPLETED 2026-02-16)
- [x] Create new directory structure (`rubrics/common/`, `rubrics/tiers/`)
- [x] Create rubric schema (`rubrics/schema.yaml`)
- [x] Create common rubrics (`simulation_quality.yaml`, `scientific_rigor.yaml`)
- [x] Create audit trail system (`evaluation/audit.py`)
- [x] Create transcript system (`evaluation/transcript.py`)
- [x] Create unified runner (`run.py`) with workspace preservation

### Phase 2: Core Refactor (Next)
- [ ] Extract executor from harness.py
- [ ] Implement unified grader
- [ ] Create agent transcript generator
- [ ] Migrate existing benchmarks to new rubric format

### Phase 3: Validation (Later)
- [ ] Run all benchmarks with new system
- [ ] Compare scores to old system
- [ ] Fix any regressions
- [ ] Document migration guide

---

## Migration Strategy

1. **Keep old system working** - Don't break existing functionality
2. **Build new system alongside** - New files, not modifications
3. **Gradual migration** - Convert benchmarks one tier at a time
4. **Validation** - Compare scores between old and new
5. **Cutover** - Once validated, deprecate old files

---

## Success Criteria

1. **Traceability:** Can answer "why did benchmark X fail?" in <1 minute
2. **Debugging:** Can reproduce any benchmark run exactly
3. **Auditability:** Every point in score has documented evidence
4. **Maintainability:** Adding new benchmark takes <15 minutes
5. **Performance:** Run time increase <10% from overhead

---

## Questions to Resolve

1. **Grading mode default:** LLM-only, rules-only, or hybrid?
2. **Workspace retention:** Keep forever, or prune after N days?
3. **Rubric versioning:** How to handle rubric updates for existing results?
4. **Cost tracking:** Include API costs in audit trail?
