# Benchmarking Campaign: Validation, Testing & Iteration Plan

**Created**: 2026-01-18
**Status**: Active Campaign
**Goal**: Systematically validate and improve the Agentic Science Worker across all capability tiers

---

## Executive Summary

We have 58 benchmarks across 11 tiers. Tiers 1-4 (21 benchmarks) have been run and validated.
**This campaign focuses on the remaining 37 benchmarks in Tiers 5-11**, which test:

- **Tiers 5-7**: HPC capabilities (SLURM, job management, multi-day workflows)
- **Tiers 8-10**: ML/AI capabilities (MLIPs, autonomous research, frontier challenges)
- **Tier 11**: HPC + ML hybrid (the cutting edge)

---

## Campaign Philosophy

### Principles

1. **Validate Before Advancing**: Don't rush to hard benchmarks. Ensure fundamentals work first.
2. **Fail Fast, Learn Fast**: Quick benchmarks first to surface issues early.
3. **Iterate Aggressively**: When a benchmark fails, diagnose and fix before moving on.
4. **Document Everything**: Every failure teaches us something. Record it.
5. **Parallel When Independent**: Use both local GPU and HPC simultaneously when possible.

### Success Metrics

| Tier | Target Pass Rate | Rationale |
|------|------------------|-----------|
| 5 | 80%+ | HPC fundamentals should be reliable |
| 6 | 60%+ | Complex workflows, allow partial success |
| 7 | 50%+ | Multi-day campaigns, partial credit valuable |
| 8 | 70%+ | ML basics should work well |
| 9 | 50%+ | Autonomous research is hard |
| 10 | 40%+ | Frontier - any success is meaningful |
| 11 | 35%+ | HPC+ML hybrid - cutting edge |

---

## Phase Structure

### Phase 1: Infrastructure Validation (Quick Wins)
**Duration**: ~1 hour
**Goal**: Confirm both ML and HPC infrastructure work with the agent

| Order | Benchmark | Time | Resource | Purpose |
|-------|-----------|------|----------|---------|
| 1a | BENCH-T8-001 | 30min | Local GPU | Validate MACE/CHGNet setup |
| 1b | BENCH-T5-001 | 15min | HPC | Validate SSH, SLURM, modules |

**Run in parallel** - these are independent.

**Exit Criteria**:
- T8-001: Agent successfully loads MLIP, runs calculation, gets energy
- T5-001: Agent connects to HPC, checks queue, identifies partitions

**If Failed**:
- T8-001 fails → Fix `.claude/skills/mlip-simulation/SKILL.md`
- T5-001 fails → Fix `.claude/skills/hpc-cluster/SKILL.md`

---

### Phase 2: Core ML Capabilities
**Duration**: ~2-3 hours
**Goal**: Validate agent can do meaningful work with MLIPs
**Prerequisite**: Phase 1 T8-001 passed

| Order | Benchmark | Time | Purpose |
|-------|-----------|------|---------|
| 2a | BENCH-T8-002 | 45min | MLIP vs classical FF comparison |
| 2b | BENCH-T8-003 | 60min | Phonon calculations with MLIP |
| 2c | BENCH-T8-004 | 90min | High-throughput stability screening |

**Run sequentially** - each builds on previous knowledge.

**Exit Criteria**:
- T8-002: Agent compares energies, discusses accuracy tradeoffs
- T8-003: Agent calculates phonons, acknowledges MLIP softening (~15%)
- T8-004: Agent screens 50+ materials, ranks by stability

**If Failed**:
- Scientific reasoning wrong → Update `CLAUDE.md` with guidance
- MLIP usage wrong → Update MLIP skill with examples
- Workflow issues → Add specific instructions to skill

---

### Phase 3: HPC Fundamentals
**Duration**: ~3-4 hours
**Goal**: Agent can reliably submit, monitor, and debug HPC jobs
**Prerequisite**: Phase 1 T5-001 passed

| Order | Benchmark | Time | Purpose |
|-------|-----------|------|---------|
| 3a | BENCH-T5-002 | 30min | Migrate local job to HPC |
| 3b | BENCH-T5-004 | 30min | Debug failing HPC job |
| 3c | BENCH-T5-006 | 30min | Async job management |
| 3d | BENCH-T5-003 | 25min | Queue-aware partition selection |
| 3e | BENCH-T5-005 | 45min | GPU job submission |
| 3f | BENCH-T5-007 | 45min | Multi-job parameter sweep |

**Run sequentially** - skills build on each other.

**Exit Criteria**:
- T5-002: Job runs on HPC, results retrieved
- T5-004: Agent identifies and fixes deliberate errors
- T5-006: Agent submits, does other work, checks status
- T5-003: Agent queries queue, selects appropriate partition
- T5-005: Agent submits GPU job with correct SLURM directives
- T5-007: Agent creates and manages job array

**If Failed**:
- SLURM syntax wrong → Add examples to HPC skill
- Module loading fails → Document CURC-specific modules
- Async handling poor → Add workflow guidance to skill

---

### Phase 4: Advanced ML Workflows
**Duration**: ~6-8 hours
**Goal**: Agent can do sophisticated ML-based research
**Prerequisite**: Phase 2 complete (T8-001 through T8-004)

| Order | Benchmark | Time | Purpose |
|-------|-----------|------|---------|
| 4a | BENCH-T8-005 | 120min | MLIP-accelerated MD |
| 4b | BENCH-T8-007 | 120min | Matbench evaluation |
| 4c | BENCH-T9-005 | 120min | Autonomous error diagnosis |
| 4d | BENCH-T9-004 | 180min | Literature-to-simulation |

**Run sequentially** - complex workflows need attention.

**Exit Criteria**:
- T8-005: Agent runs long MD, calculates diffusion coefficient
- T8-007: Agent evaluates against Matbench Discovery
- T9-005: Agent diagnoses simulation failure autonomously
- T9-004: Agent extracts parameters from paper, runs simulation

**If Failed**:
- Analysis wrong → Improve data-analysis skill
- Literature extraction fails → Improve literature-search skill
- Scientific methodology weak → Strengthen CLAUDE.md

---

### Phase 5: HPC-Scale Research
**Duration**: ~8-12 hours (can run overnight)
**Goal**: Agent handles complex HPC workflows
**Prerequisite**: Phase 3 complete (all T5 benchmarks)

| Order | Benchmark | Time | Purpose |
|-------|-----------|------|---------|
| 5a | BENCH-T6-001 | 180min | System size convergence |
| 5b | BENCH-T6-004 | 180min | High-throughput screening |
| 5c | BENCH-T6-005 | 300min | Melting temperature |
| 5d | BENCH-T7-002 | 240min | Autonomous error recovery |

**Can run T6 benchmarks in parallel** if HPC queue allows.

**Exit Criteria**:
- T6-001: Agent runs multiple system sizes, extracts converged value
- T6-004: Agent screens many materials via job arrays
- T6-005: Agent determines melting point via coexistence
- T7-002: Agent recovers from deliberate failures

---

### Phase 6: HPC + ML Integration
**Duration**: ~6-10 hours
**Goal**: Agent coordinates ML and HPC resources
**Prerequisite**: Phase 2 and Phase 3 complete

| Order | Benchmark | Time | Purpose |
|-------|-----------|------|---------|
| 6a | BENCH-T11-001 | 120min | Million-atom MLIP on HPC |
| 6b | BENCH-T11-002 | 90min | Massive screening with arrays |
| 6c | BENCH-T11-004 | 120min | Long-timescale dynamics |
| 6d | BENCH-T11-003 | 150min | Active learning at scale |

**Run sequentially** - each tests different integration pattern.

**Exit Criteria**:
- T11-001: Agent correctly determines HPC needed, runs large MLIP MD
- T11-002: Agent submits 500+ job array for ML screening
- T11-004: Agent implements checkpointing for long simulations
- T11-003: Agent coordinates MLIP with HPC DFT validation

---

### Phase 7: Frontier Challenges (Optional/Aspirational)
**Duration**: Variable (8+ hours each)
**Goal**: Push the limits of autonomous research
**Prerequisite**: Phases 1-6 substantially complete

| Benchmark | Time | Purpose |
|-----------|------|---------|
| BENCH-T8-006 | 180min | Fine-tuning universal potential |
| BENCH-T9-001 | 240min | Active learning for MLIP training |
| BENCH-T9-002 | 300min | Multi-fidelity workflow |
| BENCH-T9-003 | 180min | Closed-loop optimization |
| BENCH-T10-001 | 480min | Novel material discovery |
| BENCH-T10-002 | 180min | Cross-modal reasoning |
| BENCH-T10-003 | 480min | Open research question |
| BENCH-T11-005 | 180min | Distributed MLIP training |
| BENCH-T11-006 | 180min | Multi-fidelity HPC campaign |
| BENCH-T11-007 | 240min | Full autonomous discovery |

**These are research-grade challenges.** Any success here is significant.

---

## Iteration & Improvement Process

### When a Benchmark Fails

```
┌─────────────────────────────────────────────────────────────────┐
│                     BENCHMARK FAILED                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 1: READ THE GRADER OUTPUT                                 │
│  - What categories scored low?                                  │
│  - What specific criteria failed?                               │
│  - What did the grader say in reasoning?                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 2: EXAMINE AGENT OUTPUT                                   │
│  - Read workspaces/benchmarks/BENCH-XXX-YYY/                    │
│  - Look at files created                                        │
│  - Check agent_output.txt in results                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 3: DIAGNOSE ROOT CAUSE                                    │
│                                                                 │
│  A. Prompt Unclear?                                             │
│     → Benchmark YAML needs better instructions                  │
│                                                                 │
│  B. Missing Knowledge?                                          │
│     → CLAUDE.md or skill needs information                      │
│                                                                 │
│  C. Wrong Tool Usage?                                           │
│     → Skill needs examples or corrections                       │
│                                                                 │
│  D. Scientific Error?                                           │
│     → CLAUDE.md needs scientific guidance                       │
│                                                                 │
│  E. Infrastructure Issue?                                       │
│     → Fix environment, paths, or permissions                    │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 4: IMPLEMENT FIX                                          │
│  - Make minimal targeted change                                 │
│  - Document what was changed and why                            │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│  Step 5: RE-RUN BENCHMARK                                       │
│  - Same benchmark, fresh workspace                              │
│  - Compare scores before/after                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
               [PASSED]            [STILL FAILED]
                    │                   │
                    ▼                   ▼
            Record improvement    Iterate (back to Step 1)
            Proceed to next       Max 3 iterations, then
            benchmark             document and move on
```

### Where to Make Fixes

| Problem | File to Edit | Example Fix |
|---------|--------------|-------------|
| Agent doesn't know MACE API | `.claude/skills/mlip-simulation/SKILL.md` | Add code examples |
| Agent uses wrong SLURM syntax | `.claude/skills/hpc-cluster/SKILL.md` | Add CURC-specific examples |
| Agent makes bad scientific choices | `CLAUDE.md` | Add verification checklist |
| Agent doesn't cite sources | `CLAUDE.md` | Strengthen citation requirements |
| Benchmark prompt is ambiguous | `benchmarks/tasks/.../BENCH-*.yaml` | Clarify prompt text |
| Agent needs specific workflow | Add hook in `.claude/settings.json` | Add pre/post tool hooks |
| Grader too harsh/lenient | `benchmarks/evaluation/llm_grader.py` | Adjust grading prompts |

### Improvement Documentation

After each fix, add entry to improvement log:

```markdown
## Improvement Log

### [Date] - BENCH-XXX Fix #N

**Problem**: [What failed]
**Root Cause**: [Why it failed]
**Fix Applied**: [What was changed]
**File Modified**: [Which file]
**Result**: [Pass/Fail after fix, score change]
```

---

## Execution Commands

### Running Individual Benchmarks

```bash
cd benchmarks/evaluation

# Run single benchmark
python harness.py BENCH-T8-001

# Run with verbose output
python harness.py BENCH-T8-001 --verbose

# Run entire tier
python harness.py --tier 8

# List available benchmarks
python harness.py --list
python harness.py --list --tier 11
```

### Checking Results

```bash
# Latest results
ls -lt benchmarks/results/runs/ | head -20

# Read specific result
cat benchmarks/results/runs/BENCH-T8-001-*/result.json | jq '.score, .status'

# Read agent output
cat benchmarks/results/runs/BENCH-T8-001-*/agent_output.txt

# Check workspace files
ls benchmarks/../workspaces/benchmarks/BENCH-T8-001-*/
```

### Parallel Execution

```bash
# Terminal 1: ML benchmark (local GPU)
python harness.py BENCH-T8-001

# Terminal 2: HPC benchmark (remote)
python harness.py BENCH-T5-001
```

---

## Timeline Estimate

| Phase | Duration | Cumulative |
|-------|----------|------------|
| Phase 1: Infrastructure | 1 hour | 1 hour |
| Phase 2: Core ML | 3 hours | 4 hours |
| Phase 3: HPC Fundamentals | 4 hours | 8 hours |
| Phase 4: Advanced ML | 8 hours | 16 hours |
| Phase 5: HPC-Scale | 12 hours | 28 hours |
| Phase 6: HPC+ML | 8 hours | 36 hours |
| Phase 7: Frontier | 20+ hours | 56+ hours |

**Note**: These are execution times. Add iteration time for fixes.
**Realistic total with iteration**: 60-80 hours over multiple sessions.

---

## Risk Mitigation

### Known Risks

| Risk | Mitigation |
|------|------------|
| HPC queue congestion | Run HPC benchmarks during off-peak hours |
| Long benchmark timeout | Use `--timeout` flag, implement checkpointing |
| API rate limits | Space out benchmarks, use caching |
| GPU memory issues | Monitor with `nvidia-smi`, restart if needed |
| Agent gets stuck | Set reasonable timeouts, manual intervention |

### Stopping Points

Safe places to pause the campaign:
- After Phase 1 (infrastructure validated)
- After Phase 3 (all fundamentals done)
- After Phase 4 (ML capabilities validated)
- After any complete tier

---

## Definition of Done

The campaign is complete when:

1. **All Phase 1-4 benchmarks pass** (or have documented reasons for failure)
2. **70%+ of Phase 5-6 benchmarks pass**
3. **At least 3 Phase 7 (frontier) benchmarks attempted**
4. **Improvement log documents all fixes made**
5. **Final summary report generated**

---

## Next Action

**Proceed to Phase 1: Infrastructure Validation**

Run in parallel:
- `python harness.py BENCH-T8-001` (Local GPU - ML validation)
- `python harness.py BENCH-T5-001` (HPC - connection validation)

Monitor both, collect results, diagnose any failures, iterate as needed.
