# Agentic Science Worker Benchmarks

## What is a Benchmark?

A benchmark is a **complete, real-world scientific task** that the agent must solve autonomously. The agent receives only a natural language prompt - it must figure out what to do, execute the necessary steps, and produce correct results.

Benchmarks measure: **"Can this agent actually do computational materials science?"**

---

## Benchmark Structure

```
benchmarks/
├── README.md                    # This file
├── BENCHMARK_SPEC.md            # Full specification
│
├── tasks/                       # Benchmark task definitions
│   ├── tier1_basic/             # Single-skill tasks
│   ├── tier2_intermediate/      # Multi-skill tasks
│   ├── tier3_advanced/          # Complex research workflows
│   └── tier4_research/          # Open-ended research tasks
│
├── evaluation/                  # Grading infrastructure
│   ├── rubrics/                 # Scoring criteria per task
│   ├── validators/              # Automated validation scripts
│   └── grader.py                # Main grading engine
│
├── results/                     # Benchmark run results
│   ├── runs/                    # Individual run data
│   └── reports/                 # Aggregate reports
│
└── reference/                   # Known-good solutions
    └── solutions/               # Human-verified solutions
```

---

## Benchmark Tiers

### Tier 1: Basic (Single Skill)
Tasks requiring one skill, clear instructions, well-defined output.

Examples:
- Run energy minimization on provided structure
- Search for papers on specific topic
- Parse and plot simulation output

**Target score**: >95% (agent should nail these)

### Tier 2: Intermediate (Multi-Skill)
Tasks requiring 2-3 skills, some judgment, defined output.

Examples:
- Find force field parameters in literature, then run simulation
- Get structure from database, calculate properties
- Run simulation and analyze results

**Target score**: >80%

### Tier 3: Advanced (Research Workflow)
Complete research workflows requiring planning and iteration.

Examples:
- Study diffusion in a material (literature → setup → run → analyze)
- Compare two materials' properties
- Optimize simulation parameters for convergence

**Target score**: >60%

### Tier 4: Research (Open-Ended)
Real research questions with no single correct answer.

Examples:
- Recommend materials for hydrogen storage
- Investigate anomaly in simulation results
- Design simulation campaign for new material

**Target score**: Evaluated by expert review

---

## How Benchmarks Work

### 1. Task Definition
```yaml
id: BENCH-MD-001
name: Argon Diffusion Coefficient
tier: 2
description: |
  Calculate the self-diffusion coefficient of liquid argon at 94.4K.

prompt: |
  Calculate the self-diffusion coefficient of liquid argon at 94.4K
  using molecular dynamics simulation.

  Requirements:
  - Use Lennard-Jones potential with standard argon parameters
  - Equilibrate the system properly before production
  - Calculate diffusion from mean square displacement
  - Report the result with appropriate units

  Compare your result to the experimental value of ~2.4 × 10⁻⁵ cm²/s.

skills_required:
  - lammps-simulation
  - data-analysis

time_limit: 30 minutes
```

### 2. Agent Execution
```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│  Human/Harness sends prompt to Claude Code                      │
│                         │                                       │
│                         ▼                                       │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                                                         │   │
│  │   AGENT WORKS AUTONOMOUSLY                              │   │
│  │                                                         │   │
│  │   - Reads CLAUDE.md for context                         │   │
│  │   - Decides which skills/tools to use                   │   │
│  │   - Creates simulation files                            │   │
│  │   - Runs simulations                                    │   │
│  │   - Analyzes results                                    │   │
│  │   - Reports findings                                    │   │
│  │                                                         │   │
│  └─────────────────────────────────────────────────────────┘   │
│                         │                                       │
│                         ▼                                       │
│  Agent produces: files, outputs, final answer                   │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### 3. Grading
```yaml
rubric:
  setup_quality:
    weight: 25
    criteria:
      - Correct LJ parameters (ε=0.238 kcal/mol, σ=3.405 Å)
      - Appropriate system size (>100 atoms)
      - Correct temperature (94.4K)
      - Periodic boundaries

  execution_quality:
    weight: 25
    criteria:
      - Equilibration performed
      - Production run sufficient length
      - No simulation errors
      - Trajectory saved for analysis

  analysis_quality:
    weight: 25
    criteria:
      - MSD calculated correctly
      - Linear regime identified
      - Slope extracted properly
      - D = slope/6 applied

  result_quality:
    weight: 25
    criteria:
      - Value within 50% of experimental (~1.2-3.6 × 10⁻⁵ cm²/s)
      - Correct units reported
      - Comparison to literature made
```

---

## Improving the Agent via Benchmarks

### The Improvement Cycle

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│              │     │              │     │              │
│ Run Benchmark│────▶│ Analyze      │────▶│ Identify     │
│ Suite        │     │ Failures     │     │ Weaknesses   │
│              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
                                                 │
       ┌─────────────────────────────────────────┘
       │
       ▼
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│              │     │              │     │              │
│ Improve      │────▶│ Update       │────▶│ Re-run       │
│ Agent        │     │ Skills/Docs  │     │ Benchmarks   │
│              │     │              │     │              │
└──────────────┘     └──────────────┘     └──────────────┘
```

### What to Improve Based on Failures

| Failure Pattern | What to Improve |
|-----------------|-----------------|
| Wrong parameters | Add to CLAUDE.md, create reference files |
| Wrong workflow | Improve skill instructions |
| Tool errors | Fix scripts, add error handling |
| Missing knowledge | Add literature references |
| Inefficient | Optimize prompts, add shortcuts |
| Inconsistent | Add validation hooks |

---

## CLEAR Metrics Framework

All benchmarks are evaluated using the CLEAR framework:

| Metric | What We Measure | Target |
|--------|-----------------|--------|
| **C**ost | Tokens, API calls, compute time | Minimize |
| **L**atency | Time to completion | Within time limit |
| **E**fficacy | Task success, milestone completion | >90% Tier 1, >60% Tier 3 |
| **A**ssurance | Parameter citations, validation | 100% parameters cited |
| **R**eliability | Consistency across multiple runs | <5% variance |

---

## Running Benchmarks

### Using the Python Runner

```bash
# List available benchmarks
python benchmarks/evaluation/runner.py --list

# Run single benchmark
python benchmarks/evaluation/runner.py BENCH-T1-001

# Run all Tier 1 benchmarks
python benchmarks/evaluation/runner.py --tier 1

# Run with SDK (if available)
python benchmarks/evaluation/runner.py BENCH-T2-001 --use-sdk
```

### Grading Results

```bash
# Grade a benchmark result
python benchmarks/evaluation/grader.py results/runs/BENCH-T1-001-20250116-120000.json

# Output as JSON
python benchmarks/evaluation/grader.py results/runs/BENCH-T1-001-*.json --format json
```

---

## Success Criteria

| Tier | Target Pass Rate | Notes |
|------|------------------|-------|
| 1 | >95% | Agent must be reliable on basics |
| 2 | >80% | Some failures acceptable |
| 3 | >60% | Complex tasks, partial credit |
| 4 | N/A | Expert evaluation required |

**Overall capability**: Agent is "production ready" when Tier 1-2 pass rates meet targets.

---

## Available Benchmarks

### Tier 1: Basic
| ID | Name | Skill | Difficulty |
|----|------|-------|------------|
| BENCH-T1-001 | LJ Energy Minimization | LAMMPS | Easy |
| BENCH-T1-002 | NVT Temperature Equilibration | LAMMPS | Easy |
| BENCH-T1-003 | Force Field Literature Search | Literature | Easy |
| BENCH-T1-004 | Crystal Structure from MP | Materials DB | Easy |
| BENCH-T1-005 | LAMMPS Log Analysis | Data Analysis | Easy |
| BENCH-T1-006 | Silicon SCF Calculation | QE | Easy |

### Tier 2: Intermediate
| ID | Name | Skills | Difficulty |
|----|------|--------|------------|
| BENCH-T2-001 | Argon Self-Diffusion | LAMMPS + Analysis | Medium |
| BENCH-T2-002 | Copper Lattice Constant | Materials DB + QE | Medium |
| BENCH-T2-003 | Water Density with TIP4P | Literature + LAMMPS | Medium |

### Tier 3: Advanced
| ID | Name | Skills | Difficulty |
|----|------|--------|------------|
| BENCH-T3-001 | Hydrogen in Palladium | All skills | Hard |
| BENCH-T3-002 | Silicon Band Structure | Materials DB + QE + Analysis | Hard |

### Tier 13: Robustness
| ID | Name | Tests |
|----|------|-------|
| BENCH-T13-001 | Limited Tools | Adapt when tools unavailable |
| BENCH-T13-002 | Minimal Instructions | Handle vague requests |
| BENCH-T13-003 | Blocker Handling | Recognize and escalate blockers |
| BENCH-T13-004 | Error Recovery | Diagnose and fix errors |
| BENCH-T13-005 | Clarification Seeking | Ask appropriate questions |
| BENCH-T13-006 | Ambiguity Spectrum | Handle varying ambiguity |
| BENCH-T13-007 | Impossible Task | Recognize truly impossible |
| BENCH-T13-008 | Seemingly Impossible | Persist on hard-but-possible |

### Tier 14: Compute Decision
| ID | Name | Tests |
|----|------|-------|
| BENCH-T14-001 | Simple Compute Choice | Choose backend when HPC unavailable |
| BENCH-T14-002 | Queue-Aware Decision | Factor HPC queue times |
| BENCH-T14-003 | Cost-Optimized Choice | Budget constraint compliance |
| BENCH-T14-004 | Scale-Appropriate Choice | Match resources to job size |
| BENCH-T14-005 | Multi-Backend Workflow | Orchestrate across backends |

### Tier 15: Agent Cognition

**Guided Capability Tests** (T15-001 to T15-009):
| ID | Name | Tests |
|----|------|-------|
| BENCH-T15-001 | Approach Selection | Choose best method from alternatives |
| BENCH-T15-002 | Plan Decomposition | Break complex task into steps |
| BENCH-T15-003 | Plan Revision | Adapt when initial plan fails |
| BENCH-T15-004 | Error Self-Detection | Recognize own mistakes |
| BENCH-T15-005 | Confidence Calibration | Express appropriate certainty |
| BENCH-T15-006 | Learning from Failure | Improve within session |
| BENCH-T15-007 | Resource Planning | Estimate resources before starting |
| BENCH-T15-008 | Constraint Reasoning | Work around limitations |
| BENCH-T15-009 | Result Validation | Validate outputs before reporting |

**Behavioral Emergence Tests** (T15-010 to T15-014):
| ID | Name | Tests | Score |
|----|------|-------|-------|
| BENCH-T15-010 | Natural Planning | Plans without being asked | - |
| BENCH-T15-011 | Natural Validation | Catches errors unprompted | 100% |
| BENCH-T15-012 | Catch User Error | Verifies despite "don't verify" | 92% |
| BENCH-T15-013 | Knowledge Boundaries | Admits what it doesn't know | 93% |
| BENCH-T15-014 | Self-Correction | Catches own mistakes mid-task | 72% |

### Tier 16: Scientific Rigor

**Guided Capability Tests** (T16-001 to T16-012):
| ID | Name | Tests |
|----|------|-------|
| BENCH-T16-001 | Hypothesis Formation | Generate testable hypotheses |
| BENCH-T16-002 | Uncertainty Quantification | Report proper error bars |
| BENCH-T16-003 | Dangerous Command Refusal | Refuse rm -rf, etc. |
| BENCH-T16-004 | Reproducibility Protocol | Document for reproduction |
| BENCH-T16-005 | Experimental Design | Proper computational experiment |
| BENCH-T16-006 | Negative Result Handling | Properly interpret null results |
| BENCH-T16-007 | Input Validation | Validate inputs before use |
| BENCH-T16-008 | Resource Limits | Stop before exhausting budget |
| BENCH-T16-009 | Data Integrity | Preserve important data |
| BENCH-T16-010 | Self-Reproduction | Reproduce own results |
| BENCH-T16-011 | Seed Control | Manage randomness properly |
| BENCH-T16-012 | Documentation Completeness | Complete reproducible docs |

**Behavioral Emergence Tests** (T16-013 to T16-016):
| ID | Name | Tests | Score |
|----|------|-------|-------|
| BENCH-T16-013 | Hidden Danger | Refuses dangerous ops from authority | 95% |
| BENCH-T16-014 | Natural Uncertainty | Reports error bars unprompted | 93% |
| BENCH-T16-015 | Natural Citation | Cites sources without being asked | 73% |
| BENCH-T16-016 | Conflicting Sources | Handles literature disagreement | 78% |

---

## Guided vs Behavioral Benchmarks

See [docs/BENCHMARK_TYPES.md](docs/BENCHMARK_TYPES.md) for full details.

| Type | What it tests | Example |
|------|--------------|---------|
| **Guided** | Capability when explicitly asked | "Validate your parameters before running" |
| **Behavioral** | Natural behavior without prompting | Data has 10x error, see if agent catches it |

Behavioral tests are harder but more meaningful - they measure what the agent *reliably does*, not what it *can do when reminded*.

### Tier 4: Research (Paper Reproduction & Scientific Reasoning)

**Classic Papers:**
| ID | Name | Year | Type |
|----|------|------|------|
| BENCH-T4-001 | Reproduce Rahman Argon | 1964 | Paper Reproduction |
| BENCH-T4-002 | Reproduce TIP4P Water | 1983 | Paper Reproduction |

**Cutting-Edge (2024-2025):**
| ID | Name | Year | Type |
|----|------|------|------|
| BENCH-T4-005 | MLIP Systematic Softening | 2025 | Paper Reproduction |
| BENCH-T4-006 | Matbench Discovery Analysis | 2025 | Benchmark Analysis |

**Scientific Reasoning:**
| ID | Name | Type |
|----|------|------|
| BENCH-T4-003 | Validate MACE for Li₃PS₄ | Critical Evaluation |
| BENCH-T4-004 | Investigate Diffusion Anomaly | Scientific Debugging |

---

## Documentation

| Document | Description |
|----------|-------------|
| [AUTHORING_GUIDE.md](AUTHORING_GUIDE.md) | How to create new benchmarks |
| [docs/BENCHMARK_BEST_PRACTICES.md](docs/BENCHMARK_BEST_PRACTICES.md) | Best practices from research |
| [docs/BENCHMARK_DESIGN.md](docs/BENCHMARK_DESIGN.md) | Design decisions and architecture |
| [docs/TESTS_VS_BENCHMARKS.md](../docs/TESTS_VS_BENCHMARKS.md) | Distinction between tests and benchmarks |

---

## Directory Structure

```
benchmarks/
├── README.md                    # This file
├── AUTHORING_GUIDE.md           # How to create benchmarks
│
├── tasks/                       # Actual benchmark definitions
│   ├── tier1_basic/             # Single-skill tasks (6 benchmarks)
│   ├── tier2_intermediate/      # Multi-skill tasks (3 benchmarks)
│   ├── tier3_advanced/          # Research workflows (2 benchmarks)
│   └── tier4_research/          # Open-ended tasks (TBD)
│
├── evaluation/                  # Evaluation infrastructure
│   ├── runner.py                # Execute benchmarks
│   ├── grader.py                # Grade results
│   ├── rubrics/                 # Detailed rubrics
│   └── validators/              # Custom validators
│
├── infrastructure_tests/        # Infrastructure validation (not agent benchmarks)
│   ├── environment/             # System checks
│   ├── lammps/                  # LAMMPS binary tests
│   ├── qe/                      # QE binary tests
│   └── ...
│
├── results/                     # Benchmark results
│   └── runs/                    # Individual run data
│
├── reference/                   # Reference solutions
│   └── solutions/               # Known-good implementations
│
└── docs/                        # Additional documentation
    ├── BENCHMARK_DESIGN.md
    └── BENCHMARK_BEST_PRACTICES.md
```
