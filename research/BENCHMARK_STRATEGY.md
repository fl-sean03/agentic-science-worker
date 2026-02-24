# ASW Benchmark Strategy

**Created:** 2026-02-19
**Purpose:** Define what we want from benchmarks and how to organize them

---

## The Core Question

**What is the Agentic Science Worker supposed to do?**

It's an AI agent that autonomously conducts computational materials science research:
- Runs simulations (LAMMPS MD, Quantum ESPRESSO DFT)
- Searches and uses scientific literature
- Makes decisions about compute resources
- Handles errors and unexpected situations
- Exhibits good scientific practices
- Works on multi-step research tasks

**What should benchmarks validate?**

That the agent can do these things correctly, reliably, and safely.

---

## Capability Hierarchy

### Level 1: Can It Execute? (Foundation)
> "Does the basic machinery work?"

- Run a LAMMPS simulation with given parameters
- Run a QE calculation with given input
- Search for a paper and extract information
- Query Materials Project for a structure
- Parse simulation output and compute properties

**Validation**: Did it produce correct output files with correct values?

### Level 2: Can It Decide? (Intelligence)
> "Does it make good choices?"

- Choose appropriate methods for a problem
- Select correct compute resources (local/cloud/HPC)
- Plan multi-step workflows
- Estimate resource requirements

**Validation**: Did it choose reasonably? Did it justify choices?

### Level 3: Can It Adapt? (Resilience)
> "Does it handle the unexpected?"

- Recover from simulation errors
- Work with missing/incomplete information
- Handle contradictory inputs
- Recognize when to ask for help

**Validation**: Did it recover? Did it escalate appropriately?

### Level 4: Is It Rigorous? (Scientific Quality)
> "Does it do good science?"

- Report uncertainties
- Cite sources
- Validate results
- Recognize unphysical values
- Document methodology

**Validation**: Would a scientist trust this output?

### Level 5: Can It Discover? (Autonomy)
> "Can it do real research?"

- Conduct multi-day research campaigns
- Make novel discoveries
- Iterate on results
- Learn from literature

**Validation**: Did it produce publishable-quality work?

---

## Mapping Tiers to Capabilities

| Level | Capability | Current Tiers | Status |
|-------|------------|---------------|--------|
| 1 | Execute | T1-T4 (basics) | ✅ Validated |
| 2 | Decide | T14 (compute), T15-partial | ✅ 100% |
| 3 | Adapt | T13 (robustness), T15-partial | ✅ 100%/93% |
| 4 | Rigorous | T16 (rigor) | ✅ 100% |
| 5 | Discover | T7, T9, T10 | ⏳ Partial |

### What's Actually Being Tested

**Well-Covered:**
- Basic simulation execution (T1-T4)
- Robustness to adversity (T13)
- Compute resource decisions (T14)
- Agent cognition/planning (T15)
- Scientific rigor (T16)

**Under-Covered:**
- ML/MLIP capabilities (T8) - status unclear
- Autonomous research (T9) - 2/5 run
- Frontier discovery (T10) - not run
- Long-running campaigns (T7) - 1/3 run

**Explicitly Postponed:**
- HPC remote execution (T5-T6, T11) - user requested delay

---

## What We Should Measure

### Primary Metrics (Must Have)

1. **Pass Rate**: % of benchmarks scoring ≥60
2. **Score Distribution**: Average score per tier
3. **Failure Modes**: What causes failures?

### Secondary Metrics (Nice to Have)

4. **Cost**: API tokens per benchmark
5. **Time**: Execution duration
6. **Reliability**: Score variance across runs

### Not Currently Measured

- CLEAR framework (Cost, Latency, Efficacy, Assurance, Reliability)
- Token usage tracking
- Multi-run consistency

---

## Reorganization Plan

### Current State (Messy)
```
benchmarks/
├── docs/           # 7 design docs (overlapping)
├── tasks/          # 16 tier directories
├── results/        # Run outputs
├── evaluation/     # Old harness
├── framework/      # Partial new framework
├── run.py          # Main runner
└── ...

research/
├── BENCHMARK_TRACKING.md    # Current status
├── IMPLEMENTATION_PLAN.md   # Execution plan
└── ...

internal/planning/
├── BENCHMARKING_CAMPAIGN.md # Original campaign plan
├── BENCHMARK_GAP_ANALYSIS.md
└── ...

docs/
├── BENCHMARK_*.md  # 4 more docs
└── ...
```

### Proposed State (Clean)
```
benchmarks/
├── README.md              # Single source of truth
├── CURRENT_STATUS.md      # Live status dashboard
├── run.py                 # Main runner
├── tasks/                 # Benchmark definitions
│   ├── tier01_basic/
│   ├── tier02_intermediate/
│   └── ...
├── results/               # Run outputs
└── evaluation/            # Grading code

docs/
├── architecture/
│   └── BENCHMARK_DESIGN.md    # How system works
└── archive/                    # Old docs (reference only)
```

---

## Immediate Next Steps

### 1. Consolidate Documentation
- Merge overlapping docs into single source of truth
- Archive outdated planning documents
- Create clean README

### 2. Validate Non-HPC Capabilities
- Check T8 (ML/MLIP) status
- Run remaining T9 benchmarks that don't need HPC
- Identify which T7/T9/T10 can run locally or on VAST

### 3. Fill Gaps
- Identify missing capability coverage
- Create new benchmarks if needed

### 4. Establish Baseline
- Document current state clearly
- Set targets for improvement

---

## Compute Resource Strategy

### Available Resources
| Resource | Use For | Cost | Speed |
|----------|---------|------|-------|
| Local CPU | Small MD, analysis | Free | Fast |
| Local GPU (RTX 5080) | MLIP, medium MD | Free | Fast |
| VAST.ai | Large MLIP, long runs | ~$0.50/hr | Medium |
| HPC (CURC) | DFT, very large MD | Free (allocation) | Queue delays |

### Benchmark Resource Requirements
| Tier | Primary Resource | Fallback |
|------|------------------|----------|
| T1-T4 | Local CPU/GPU | - |
| T7 | HPC (postponed) | VAST possible |
| T8 | Local GPU | VAST |
| T9 | Local GPU + VAST | HPC for DFT |
| T10 | Needs DFT | Postpone |
| T13-T16 | Local | - |

---

## Success Criteria

### Minimum Viable (Current Goal)
- T1-T4: ≥90% pass rate (validated)
- T13-T16: ≥90% pass rate (achieved: 98%)
- T8: ≥70% pass rate (to verify)
- T9: ≥50% pass rate (to verify/improve)

### Stretch Goals
- All non-HPC benchmarks passing
- Documented failure analysis for any failures
- Reproducible results across runs

---

*This document defines the "why" and "what". Implementation details in CURRENT_STATUS.md*
