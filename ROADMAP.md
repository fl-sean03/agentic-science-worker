# Roadmap

**Last Updated:** 2026-02-16

This document tracks what we're building, what's done, and what's next.

---

## Vision

### The Goal

Build an **AI-powered computational science assistant** that can autonomously run simulations, search literature, analyze data, and help researchers be more productive.

Starting with computational materials science, with potential expansion to other domains.

### The Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    INTELLIGENT AGENT                             │
│              (Claude Code / Coding Agent)                        │
│   Reasons about science, decides what tools to use, executes    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CAPABILITY TOOLKIT                            │
│   Each capability = a skill file the agent reads                 │
│   No orchestration. No abstractions. Just documentation.        │
│                                                                 │
│   Simulation │ Analysis │ Knowledge │ Compute │ (Future: Labs) │
└─────────────────────────────────────────────────────────────────┘
```

### The Principle

> **Expand the toolkit, not the complexity.**

### Why This Matters

- **Democratize computational science** - Not everyone has access to trained experts
- **Accelerate discovery** - Agents can run 24/7, explore more parameter space
- **Reduce human bottleneck** - The limit isn't compute, it's expertise
- **Compound value** - Each tool, integration, and success builds on the last

### Success Criteria

An agent that can:
1. Take a research question ("What's the diffusion coefficient of hydrogen in palladium?")
2. Find methodology and parameters from literature
3. Run appropriate simulations
4. Verify results against published values
5. Iterate if results don't match
6. Produce a report a scientist would accept

And eventually: discover something genuinely new.

---

## Current Status

### What Works (Validated)

| Capability | Status | Evidence |
|------------|--------|----------|
| LAMMPS simulations | Production | 42 benchmarks passed |
| Literature search | Production | Agent finds parameters autonomously |
| Parameter extraction | Production | Correct citations in outputs |
| Result verification | Production | Compares to published values |
| Error recovery | Production | T7-002: 4 HPC errors handled |
| HPC job submission | Production | T5-T6 tiers passing |
| ML potentials (MACE, CHGNet) | Production | T8 tier passing |
| Quantum ESPRESSO | Beta | T1-006 works, needs more testing |

### Benchmark Progress

```
Tier 1  (Basic):            7/7   ████████████████████ 100%
Tier 2  (Intermediate):     4/4   ████████████████████ 100%
Tier 3  (Advanced):         3/3   ████████████████████ 100%
Tier 4  (Research):         7/7   ████████████████████ 100%
Tier 5  (HPC Fundamentals): 7/7   ████████████████████ 100%
Tier 6  (HPC Scale):        5/5   ████████████████████ 100%
Tier 7  (Campaigns):        1/3   ██████░░░░░░░░░░░░░░  33%
Tier 8  (ML Materials):     6/7   █████████████████░░░  86%
Tier 9  (Autonomous):       2/5   ████████░░░░░░░░░░░░  40%
Tier 10 (Frontier):         0/3   ░░░░░░░░░░░░░░░░░░░░   0%
Tier 11 (HPC+ML Hybrid):    0/7   ░░░░░░░░░░░░░░░░░░░░   0%
Tier 12 (Theory Synthesis): 0/3   ░░░░░░░░░░░░░░░░░░░░   0%
Tier 13 (Robustness):       0/8   ░░░░░░░░░░░░░░░░░░░░   0%
Tier 14 (Compute Decision): 0/5   ░░░░░░░░░░░░░░░░░░░░   0%
Tier 15 (Agent Cognition):  4/14  █████░░░░░░░░░░░░░░░  29%  [9 guided + 5 behavioral]
Tier 16 (Scientific Rigor): 4/16  █████░░░░░░░░░░░░░░░  25%  [12 guided + 4 behavioral]

Total: 50/104 benchmarks (48%)
```

**Behavioral Benchmark Results (T15-T16):**
All 8 behavioral tests passing (87% avg score). Core Principles validated.

---

## Immediate TODOs

### High Priority

- [ ] **Complete T7 tier** - Research campaigns
  - [ ] T7-001: Multi-day research study
  - [ ] T7-003: Collaborative computation

- [ ] **Complete T8 tier** - ML materials
  - [ ] T8-006: Fine-tuning ML potentials

- [ ] **Complete T9 tier** - Autonomous research
  - [ ] T9-001: Active learning loop
  - [ ] T9-002: Multi-fidelity optimization
  - [ ] T9-003: Closed-loop optimization

### Medium Priority

- [ ] **T10 Frontier Benchmarks**
  - [ ] T10-001: Novel material discovery
  - [ ] T10-002: Cross-modal reasoning
  - [ ] T10-003: Open research question

- [ ] **T11 HPC+ML Hybrid Benchmarks**
  - [ ] T11-001: Million-atom MLIP simulation
  - [ ] T11-002: Massive screening campaign
  - [ ] T11-003: Active learning at scale
  - [ ] T11-004: Long timescale dynamics
  - [ ] T11-005: Distributed training
  - [ ] T11-006: Multi-fidelity campaign
  - [ ] T11-007: Autonomous discovery

- [ ] **T12 Theory Synthesis Benchmarks** [NEW - uses ASTA Theorizer]
  - [ ] T12-001: Literature-driven hypothesis generation
  - [ ] T12-002: Research gap discovery and exploitation
  - [ ] T12-003: Methodology consensus extraction

- [ ] **T13 Robustness Benchmarks** [agent resilience]
  - [ ] T13-001: Operation with limited tools
  - [ ] T13-002: Minimal/unclear instructions
  - [ ] T13-003: Blocker handling and escalation
  - [ ] T13-004: Error recovery and diagnosis
  - [ ] T13-005: Appropriate clarification seeking

- [ ] **T15 Agent Cognition Benchmarks** [NEW - planning/reasoning]
  - [ ] T15-001: Approach selection (choose best method)
  - [ ] T15-002: Plan decomposition (break complex tasks)
  - [ ] T15-003: Plan revision (adapt when plan fails)
  - [ ] T15-004: Error self-detection (recognize mistakes)
  - [ ] T15-005: Confidence calibration (appropriate certainty)
  - [ ] T15-006: Learning from failure (in-session improvement)
  - [ ] T15-007: Resource planning (estimate before starting)
  - [ ] T15-008: Constraint reasoning (work around limits)
  - [ ] T15-009: Result validation (verify before reporting)

- [ ] **T16 Scientific Rigor Benchmarks** [NEW - scientific method/safety]
  - [ ] T16-001: Hypothesis formation
  - [ ] T16-002: Uncertainty quantification
  - [ ] T16-003: Dangerous command refusal (rm -rf, etc.)
  - [ ] T16-004: Reproducibility protocol
  - [ ] T16-005: Experimental design
  - [ ] T16-006: Negative result handling
  - [ ] T16-007: Input validation
  - [ ] T16-008: Resource limits (graceful stop)
  - [ ] T16-009: Data integrity (preserve important files)
  - [ ] T16-010: Self-reproduction (reproduce own results)
  - [ ] T16-011: Seed control (manage randomness)
  - [ ] T16-012: Documentation completeness

### Low Priority / Nice to Have

- [ ] Add VASP support (requires license)
- [ ] Add CP2K support
- [ ] Add more water models (SPC/E, TIP3P)
- [ ] Add polymer simulation examples
- [ ] Add surface/interface benchmarks
- [x] ~~Multi-agent support (AGENTS.md standard)~~ **DONE 2026-01-22**
- [ ] Add OpenAI Codex backend
- [ ] Add Aider backend (integration ready, needs testing)

---

## Enhancements Needed

### Benchmark Improvements

| Issue | Description | Priority |
|-------|-------------|----------|
| Async HPC handling | Agent completes before long jobs finish | Medium |
| Better error messages | Some failures are cryptic | Low |
| Checkpoint/resume | Long benchmarks can't resume | Medium |
| Parallel execution | Run independent benchmarks in parallel | Low |

### Skill Improvements

| Skill | Enhancement Needed | Priority |
|-------|-------------------|----------|
| `hpc-cluster` | Add more partition guidance | Medium |
| `mlip-simulation` | Add fine-tuning examples | High |
| `quantum-espresso` | Add band structure workflow | Medium |
| `literature-search` | Add PDF parsing capability | Low |

### Infrastructure

| Item | Description | Priority | Status |
|------|-------------|----------|--------|
| Multi-agent support | AGENTS.md, backend abstraction | High | **DONE** |
| CI/CD | Auto-run benchmarks on PR | Medium | TODO |
| Dashboard | Visualize benchmark results over time | Low | TODO |
| Cost tracking | Track API costs per benchmark | Low | TODO |
| Multi-model support | Test with different models | Low | TODO |

---

## Technical Debt

- [ ] Some benchmarks have duplicate runs in results/ (cleanup needed)
- [ ] `phase0-tests/` directory still has test artifacts
- [ ] Some skill files have outdated examples

---

## Research Directions

### Near-term

1. **Complete all benchmarks** - Improve pass rate across all tiers
2. **Real research tasks** - Have agent tackle actual research questions
3. **Documentation** - Improve skill files based on usage

### Medium-term

1. **Workflow improvements** - Better handling of multi-step tasks
2. **Error recovery** - More robust handling of simulation failures
3. **Human-in-the-loop** - Agent proposes, human approves, agent executes

### Long-term

1. **Expanded capabilities** - Support for more simulation codes
2. **Community contributions** - Skills from external contributors
3. **Other domains** - Potential expansion beyond materials

---

## Integrations

The agent supports various external tools through skill files.

### Current Integrations

| Tool | Purpose | Status |
|------|---------|--------|
| ggen | Structure generation | Skill + showcase |
| torch-sim | High-throughput ML sims | Skill + showcase |
| VAST AI | On-demand cloud GPU | Skill + tested |

### Integration Pattern

Every new capability follows the same pattern:
1. Add a skill file explaining the tool
2. Document when/why to use it
3. Let the agent decide

No special infrastructure. Just skills.

### Showcases

Demonstrations of tool integrations: `showcases/`

---

## How to Contribute

### Pick a TODO

1. Check the "Immediate TODOs" section above
2. Comment on the issue or create one
3. Follow the patterns in `CONTRIBUTING.md`

### Run a Benchmark

```bash
# See what's not passing
python benchmarks/evaluation/harness.py --list

# Run one
python benchmarks/evaluation/harness.py BENCH-T7-001 --verbose
```

### Fix a Benchmark

Most failures are prompt issues, not code issues. See `CONTRIBUTING.md` for patterns that work.

### Add a Benchmark

See `benchmarks/AUTHORING_GUIDE.md` for how to write new benchmarks.

---

## Changelog

### 2026-02-16
- **Behavioral Benchmark Validation**
  - Ran 8 behavioral benchmarks on real agent
  - All passing (87% average score)
  - T15-011 Natural Validation: 100% (catches errors unprompted)
  - T15-012 Catch User Error: 92% (verifies despite "don't verify")
  - T15-013 Knowledge Boundaries: 93% (admits uncertainty)
  - T15-014 Self-Correction: 72% (catches own mistakes)
  - T16-013 Hidden Danger: 95% (refuses dangerous ops)
  - T16-014 Natural Uncertainty: 93% (reports error bars)
  - T16-015 Natural Citation: 73% (cites sources)
  - T16-016 Conflicting Sources: 78% (handles disagreement)
- **AGENTS.md Core Principles**
  - Added 6 Core Principles governing all agent work
  - Strengthened Principle 5 (conflict handling) based on T16-016 failure
  - Strengthened Principle 6 (citation completeness) based on T16-015 failure
  - Re-ran failed benchmarks - both passed after improvements
- **Benchmark Bug Fixes**
  - Fixed T15-012: Prompt now contains actual error (0.238 eV vs 0.0103 eV)
- **Documentation**
  - Created BENCHMARK_TYPES.md (guided vs behavioral distinction)
  - Updated benchmark README with behavioral test information
- **Total benchmarks run: 50/104 (48%)**

### 2026-02-15
- **VAST AI Integration**
  - Created `skills/vast-cloud/` with full documentation
  - Implemented `vast_client.py` Python wrapper
  - Added job templates for MACE, LAMMPS GPU
  - Tested with real instance (working)
- **Tier 14: Compute Decision Benchmarks** (5 benchmarks)
  - T14-001: Simple compute choice (local vs VAST when HPC unavailable)
  - T14-002: Queue-aware decision (factor in HPC wait times)
  - T14-003: Cost-optimized choice ($0 budget constraint)
  - T14-004: Scale-appropriate choice (recognize large jobs)
  - T14-005: Multi-backend workflow orchestration
- **Tier 15: Agent Cognition Benchmarks** (9 benchmarks) [NEW]
  - T15-001 to T15-009: Planning, reasoning, self-reflection, learning
  - Tests approach selection, plan decomposition/revision
  - Tests error detection, confidence calibration, result validation
- **Tier 16: Scientific Rigor Benchmarks** (12 benchmarks) [NEW]
  - T16-001 to T16-012: Scientific method and safety
  - Tests hypothesis formation, experimental design, uncertainty
  - Tests safety (dangerous command refusal, data integrity)
  - Tests reproducibility (seed control, self-reproduction, documentation)
- **Comprehensive Gap Analysis**
  - Researched agent benchmark best practices (SWE-bench, GAIA, KDD 2025)
  - Created `internal/planning/BENCHMARK_GAP_ANALYSIS.md`
  - Identified missing evaluation dimensions and created new tiers
- **Infrastructure Updates**
  - Updated harness.py to support Tiers 12-16
  - Updated AGENTS.md with vast-cloud skill
  - Total benchmarks: 74 → 104

### 2026-01-31
- **Showcase Setup & Validation**
  - Installed and validated ggen (structure generation) - demo works in 8.2s
  - Installed and validated torch-sim (high-throughput screening) - 15+ structures/sec
  - Installed ASTA Theorizer (literature-driven theory synthesis)
    - Cloned asta-theorizer and asta-paper-finder
    - Created theorizer conda environment (Python 3.12)
    - API keys configured (placeholder - user to fill in)
  - Created `theory-synthesis` showcase with demo script
  - Created verification script: `showcases/verify_all.py` (3/3 showcases ready)
- **Environment Management**
  - Created `environments/science-tools.yml` (ggen + torch-sim)
  - Created `environments/theorizer.yml` (ASTA Theorizer)
  - Set up shared model cache at `~/.cache/science-agent/`
- **Documentation Updates**
  - Updated `showcases/README.md` with environment setup instructions
  - Updated skill files with verification commands and cache locations
  - Updated theory-synthesis skill with correct installation instructions

### 2026-01-29
- **New Tiers & Benchmarks**
  - Added Tier 12: Theory Synthesis (3 benchmarks)
    - T12-001: Literature-driven hypothesis generation
    - T12-002: Research gap discovery
    - T12-003: Methodology consensus extraction
  - Added Tier 13: Robustness (8 benchmarks)
    - T13-001: Limited tool operation
    - T13-002: Minimal instructions handling
    - T13-003: Blocker handling and escalation
    - T13-004: Error recovery and debugging
    - T13-005: Clarification seeking calibration
    - T13-006: Ambiguity spectrum response
    - T13-007: Impossible task recognition
    - T13-008: Seemingly impossible task persistence
- **New Skill**
  - Added `skills/theory-synthesis/` for ASTA Theorizer integration
- **Design Philosophy Documentation**
  - Created `docs/DESIGN_PHILOSOPHY.md` - "Intelligence as Scaffolding"
  - Created `docs/BENCHMARK_OVERVIEW.md` - comprehensive coverage analysis
- **AGENTS.md Enhancement**
  - Added Autonomy & Judgment section
  - Added Handling Difficult Situations section
  - Added Communication Style section
  - Added Working with Limited Resources section
- **Infrastructure**
  - Updated harness.py with T12/T13 pass thresholds

### 2026-01-23
- **New Integrations**
  - Created `showcases/` directory for tool demonstrations
  - Added ggen integration (structure generation)
  - Added torch-sim integration (high-throughput ML sims)
  - Added `skills/ggen/` and `skills/torch-sim/`
  - Updated `skills/mlip-simulation/` to reference torch-sim for scale

### 2026-01-22
- **Multi-agent generalization**
  - Adopted AGENTS.md as primary context (industry standard)
  - Created backend abstraction for benchmark harness
  - Added `--backend` flag to harness.py
  - Moved skills/ to project root (symlinked for Claude Code)
  - Added configs/ for agent-specific settings (claude, aider, cursor, codex)
  - Updated README for multi-agent usage

### 2026-01-19
- Published to GitHub
- Added benchmark results summary
- Added example workspaces
- Created CONTRIBUTING.md and ROADMAP.md

### 2026-01-18
- Completed T5, T6 HPC benchmarks
- Fixed "agent stops after research" pattern
- Added CRITICAL INSTRUCTIONS fix

### 2026-01-17
- Completed T1-T4 benchmarks
- Established LLM-as-judge grading
- Created benchmark harness

---

## Contact

Questions? Issues? Ideas?

- Open an issue on GitHub
- Check existing docs in `docs/`
