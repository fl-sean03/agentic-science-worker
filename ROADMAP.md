# Roadmap

**Last Updated:** 2026-01-19

This document tracks what we're building, what's done, and what's next.

---

## Grand Vision

### The Goal

Build an autonomous AI agent that can conduct computational materials science research at PhD level - finding parameters from literature, running simulations, verifying results, and iterating until correct.

### Why This Matters

- **Democratize computational science** - Not everyone has access to trained experts
- **Accelerate discovery** - Agents can run 24/7, explore more parameter space
- **Reduce human bottleneck** - The limit isn't compute, it's expertise

### Success Criteria

An agent that can:
1. Take a research question ("What's the diffusion coefficient of hydrogen in palladium?")
2. Find methodology and parameters from literature
3. Run appropriate simulations
4. Verify results against published values
5. Iterate if results don't match
6. Produce a report a scientist would accept

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
Tier 1  (Basic):           7/7   ████████████████████ 100%
Tier 2  (Intermediate):    4/4   ████████████████████ 100%
Tier 3  (Advanced):        3/3   ████████████████████ 100%
Tier 4  (Research):        7/7   ████████████████████ 100%
Tier 5  (HPC Fundamentals): 7/7   ████████████████████ 100%
Tier 6  (HPC Scale):       5/5   ████████████████████ 100%
Tier 7  (Campaigns):       1/3   ██████░░░░░░░░░░░░░░  33%
Tier 8  (ML Materials):    6/7   █████████████████░░░  86%
Tier 9  (Autonomous):      2/5   ████████░░░░░░░░░░░░  40%
Tier 10 (Frontier):        0/3   ░░░░░░░░░░░░░░░░░░░░   0%
Tier 11 (HPC+ML Hybrid):   0/7   ░░░░░░░░░░░░░░░░░░░░   0%

Total: 42/58 benchmarks (72%)
```

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
- [ ] IMPROVEMENT_LOG.md could use better indexing

---

## Research Directions

### Near-term (1-3 months)

1. **Complete all benchmarks** - Get to 100% pass rate across all tiers
2. **Real research tasks** - Have agent tackle actual research questions
3. **Paper writing** - Can the agent draft a methods section?

### Medium-term (3-6 months)

1. **Multi-agent collaboration** - Specialist agents (literature, simulation, analysis)
2. **Long-running campaigns** - Research projects spanning days/weeks
3. **Human-in-the-loop** - Agent proposes, human approves, agent executes

### Long-term (6-12 months)

1. **Novel discovery** - Agent finds something genuinely new
2. **Publication-ready output** - Full paper draft from agent
3. **Other domains** - Biology, chemistry, engineering

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

# If it fails, document in IMPROVEMENT_LOG.md
```

### Fix a Benchmark

Most failures are prompt issues, not code issues. See `CONTRIBUTING.md` for patterns that work.

### Add a Benchmark

See `benchmarks/AUTHORING_GUIDE.md` for how to write new benchmarks.

---

## Changelog

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
- See `IMPROVEMENT_LOG.md` for how past issues were solved
