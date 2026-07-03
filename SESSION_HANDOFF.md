> **SUPERSEDED (2026-07-02).** This handoff describes the February 2026 state and
> pre-reorg paths. Current truth: `docs/rebase/CURRENT_STATE.md` (state),
> `benchmarks/results/GENERATED_STATUS.md` (artifact-derived benchmark status),
> `CLAUDE.md` (skill index). Kept verbatim below as a historical record.

# Session Handoff - Agentic Science Worker

**Last Updated:** 2026-02-23
**Purpose:** Context for new Claude Code sessions continuing benchmark work

---

## Quick Start

```bash
# Navigate to project
cd /home/sf2/work/agents/science-agent/1-ScienceAgent

# Check current status
cat benchmarks/CURRENT_STATUS.md

# Run a benchmark
python benchmarks/evaluation/harness.py BENCH-T10-001

# Check VAST instances (important!)
vastai show instances
```

---

## Project Overview

**What:** AI-powered computational materials science assistant using Claude Code as the agent backbone. Benchmarks test autonomous simulation, analysis, and research capabilities.

**Architecture:**
```
Claude Code Agent → reads skills/ → executes tasks → graded by LLM
```

**Current State:** 78/86 active benchmarks passing (100% pass rate)

---

## Critical Files to Read

### Status & Planning
| File | Purpose | Priority |
|------|---------|----------|
| `benchmarks/CURRENT_STATUS.md` | Live dashboard, tier-by-tier scores | **Read First** |
| `benchmarks/NEXT_STEPS.md` | Immediate priorities | **Read First** |
| `benchmarks/GAP_ANALYSIS.md` | Coverage gaps, what to build | High |
| `benchmarks/IMPROVEMENT_METHODOLOGY.md` | How to fix failing benchmarks | High |
| `ROADMAP.md` | Overall vision and progress | Medium |

### Key Skills
| File | Purpose |
|------|---------|
| `skills/vast-cloud/SKILL.md` | VAST.ai cloud GPU usage |
| `skills/quantum-espresso/SKILL.md` | QE DFT (GPU paths) |
| `skills/lammps-simulation/SKILL.md` | MD simulations |
| `skills/mlip-simulation/SKILL.md` | MACE, CHGNet ML potentials |

### Benchmark Proposals
| File | Purpose |
|------|---------|
| `benchmarks/VASTAI_BENCHMARK_PROPOSAL.md` | T17 design (5 more to create) |
| `benchmarks/AUTHORING_GUIDE.md` | How to write new benchmarks |

---

## Current Benchmark Status

### Passing (100% of run)
| Tier | Benchmarks | Pass Rate | Notes |
|------|------------|-----------|-------|
| T1-T4 | 21 | 100% | Foundation |
| T7 | 1/3 | 33% | 2 need HPC |
| T8 | 6/7 | 86% | ML potentials |
| T9 | 3/5 | 60% | Autonomous research |
| T10 | 1/4 | 25% | Frontier DFT |
| T13-T16 | 43 | 100% | Quality/cognition |
| T17 | 3/3 | 100% | Cloud GPU (NEW) |
| T18 | 2/2 | 100% | Data analysis (NEW) |

### Archived (CURC Deferred)
- T5, T6: HPC Fundamentals/Scale
- T11: HPC+ML Hybrid
- Location: `skills/archive/hpc-cluster-curc/`

### Blocked
- T12: Theory Synthesis (needs Theorizer MCP)

---

## Immediate Next Steps

### 1. Run Remaining T10 Benchmarks
```bash
python benchmarks/evaluation/harness.py BENCH-T10-001  # Novel material discovery
python benchmarks/evaluation/harness.py BENCH-T10-002  # Cross-modal reasoning
python benchmarks/evaluation/harness.py BENCH-T10-003  # Open research question
```
- **Prerequisites:** QE GPU working (validated T10-004: 85)
- **Time:** 60-120 min each
- **Complexity:** High - frontier challenges

### 2. Create More T17 Benchmarks
Per `VASTAI_BENCHMARK_PROPOSAL.md`:
- T17-004: Cost-aware GPU selection
- T17-005: Multi-instance parallel jobs
- T17-006: Error recovery
- T17-007: Long job with checkpointing
- T17-008: Hybrid local-cloud pipeline

### 3. Create More T18 Benchmarks
Per `GAP_ANALYSIS.md`:
- T18-003: Publication-quality plots
- T18-004: Error propagation analysis

---

## Key Patterns Learned

### Prompt Design (CRITICAL)
**Detailed prompts prevent early termination:**
```markdown
**IMPORTANT: You must complete ALL steps below.**

1. Step one...
2. Step two...
3. Step three...

**Completion Checklist:**
- [ ] Item 1 done
- [ ] Item 2 done

Do NOT stop after step 1. ALL steps are required.
```

### VAST.ai Safety
```bash
# ALWAYS check for orphans after benchmarks
vastai show instances | grep BENCH
# Should be empty - destroy any found

# Safety utility
python benchmarks/evaluation/vast_safety.py --postflight
```

### Consistency Testing
For flaky benchmarks, run 3x before/after fixes:
- Mean ≥ 65 with 2/3 passing = acceptable
- All 3 pass = robust

---

## Infrastructure

### Local GPU
- **GPU:** RTX 5080 (16GB VRAM)
- **QE GPU:** `/home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/build-gpu/bin/pw.x`
- **QE CPU:** `/home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/build-cpu/bin/pw.x`
- **NVHPC:** `~/hpc-sdk/` (for QE compilation)

### VAST.ai
- **CLI:** `vastai` (installed)
- **Balance:** ~$25 prepaid
- **Safety:** Always destroy instances after use
- **User's instances (DO NOT TOUCH):**
  - npt-tri-OH50-F50
  - shear-couple_xy-F100
  - stage5b-100ns-1000K (or similar labeled)

### Benchmark Harness
```bash
# List all benchmarks
python benchmarks/evaluation/harness.py --list

# Run single benchmark
python benchmarks/evaluation/harness.py BENCH-T10-001

# Run tier
python benchmarks/evaluation/harness.py --tier 17
```

---

## Directory Structure

```
/home/sf2/work/agents/science-agent/1-ScienceAgent/
├── AGENTS.md                 # Agent instructions (read by Claude)
├── ROADMAP.md                # Vision and progress
├── SESSION_HANDOFF.md        # This file
├── benchmarks/
│   ├── CURRENT_STATUS.md     # Live dashboard
│   ├── NEXT_STEPS.md         # Priorities
│   ├── GAP_ANALYSIS.md       # Coverage gaps
│   ├── IMPROVEMENT_METHODOLOGY.md  # Fix patterns
│   ├── VASTAI_BENCHMARK_PROPOSAL.md
│   ├── evaluation/
│   │   ├── harness.py        # Benchmark runner
│   │   ├── grader.py         # Rule-based grading
│   │   ├── llm_grader.py     # LLM-as-judge
│   │   └── vast_safety.py    # VAST cleanup utility
│   ├── tasks/
│   │   ├── tier1_basic/
│   │   ├── tier10_frontier/
│   │   ├── tier17_cloud_gpu/
│   │   ├── tier18_data_analysis/
│   │   └── ...
│   └── results/runs/         # Benchmark outputs
├── skills/
│   ├── vast-cloud/
│   ├── quantum-espresso/
│   ├── lammps-simulation/
│   ├── mlip-simulation/
│   └── archive/              # Archived skills (HPC)
└── workspaces/benchmarks/    # Agent work directories
```

---

## User Context

- **Other agents running:** User has other Claude sessions doing simulation work
- **VAST instances:** User has labeled instances - only destroy BENCH-* instances
- **HPC:** CURC access deferred - use VAST.ai instead
- **Time constraints:** User wants iterative progress, not perfection

---

## Commands Reference

```bash
# Benchmark operations
python benchmarks/evaluation/harness.py BENCH-XX-XXX  # Run one
python benchmarks/evaluation/harness.py --list         # List all
python benchmarks/evaluation/harness.py --tier 17      # Run tier

# VAST.ai operations
vastai show instances                    # List instances
vastai search offers "gpu_name=RTX_4090 dph<0.4"  # Find GPUs
vastai destroy instance <id>             # Destroy instance

# Status checks
cat benchmarks/CURRENT_STATUS.md | head -30
vastai show instances | grep BENCH       # Check orphans
```

---

## Success Metrics

| Goal | Target | Current |
|------|--------|---------|
| Overall pass rate | 100% | 100% |
| T10 Frontier | ≥50% | 25% (1/4) |
| T17 Cloud GPU | 100% | 100% (3/3) |
| T18 Data Analysis | 100% | 100% (2/2) |

---

## What NOT to Do

1. **Don't touch user's VAST instances** - Only destroy BENCH-* labeled ones
2. **Don't run T5/T6/T11** - These are archived (need CURC)
3. **Don't run T12** - Blocked on Theorizer MCP
4. **Don't use condensed prompts** - Causes early termination
5. **Don't forget to destroy VAST instances** - Bills until destroyed

---

*This handoff was created 2026-02-23. Read CURRENT_STATUS.md for latest.*
