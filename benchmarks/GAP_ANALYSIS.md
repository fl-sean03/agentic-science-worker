# Benchmark Suite Gap Analysis

**Created:** 2026-02-20
**Last Updated:** 2026-02-23
**Purpose:** Identify missing capabilities and propose improvements

---

## Current Coverage

### Tier Summary

| Tier | Name | Benchmarks | Status |
|------|------|------------|--------|
| T1-T4 | Foundation → Research | 21 | 100% passing |
| T5-T6 | HPC | 12 | **ARCHIVED** (CURC) |
| T7 | Research Campaigns | 3 | 1/3 passing, 2 archived |
| T8 | ML/MLIP | 7 | 86% passing |
| T9 | Autonomous Research | 5 | 80% passing |
| T10 | Frontier DFT | 4 | 1/4 passing (T10-004: 85 ✅) |
| T11 | HPC+ML | 7 | **ARCHIVED** (CURC) |
| T12 | Theory Synthesis | 3 | **NOT RUN** (needs Theorizer) |
| T13 | Robustness | 8 | 100% passing |
| T14 | Compute Decision | 5 | 100% passing |
| T15 | Agent Cognition | 14 | 100% passing |
| T16 | Scientific Rigor | 16 | 100% passing |
| T17 | Cloud GPU | 3 | **100% passing** (97, 91, 92) |
| T18 | Data Analysis | 2 | **100% passing** (92, 92) |

### Skills vs Benchmarks

| Skill | Benchmarks Testing It | Coverage |
|-------|----------------------|----------|
| lammps-simulation | T1-T4, T8, T9 | Good |
| mlip-simulation | T8, T9, T14 | Good |
| materials-database | T1, T4, T14 | Good |
| vast-cloud | T14-005, T17 (new) | Improving |
| quantum-espresso | T10 (not run) | **GAP** |
| data-analysis | Implicit in many | **GAP** - no dedicated |
| literature-search | Referenced but sparse | **GAP** |
| resource-acquisition | Referenced but sparse | **GAP** |
| theory-synthesis | T12 (not run) | Blocked |

---

## Identified Gaps

### Gap 1: DFT Workflow Benchmarks (HIGH PRIORITY)

**Status:** T10-004 (Basic SCF) passed with 85! QE GPU working. 5 more T10 benchmarks to run.

**Missing Tests:**
- SCF convergence verification
- Band structure calculation
- Structure relaxation with DFT
- Formation energy calculation
- Phonon calculation

**Proposed:** Run existing T10 benchmarks, add more if needed

---

### Gap 2: Data Analysis Benchmarks ✅ RESOLVED

**Status:** T18 tier created and passing!

**Implemented (2026-02-23):**
- T18-001: Parse LAMMPS thermo output, compute statistics → **92 ✅**
- T18-002: Calculate MSD and diffusion from trajectory → **92 ✅**

**Still Proposed:**
```yaml
BENCH-T18-003: Generate publication-quality plots
BENCH-T18-004: Error propagation through multi-step analysis
```

---

### Gap 3: Literature Search Benchmarks

**Status:** Skill exists, very sparse testing

**Missing Tests:**
- Find papers on specific topic
- Extract methodology from papers
- Verify citations are real
- Compare methods across papers
- Identify research gaps

**Proposed:** Create T19 - Literature Integration tier

```yaml
BENCH-T19-001: Find seminal papers on topic (e.g., "MLIP for thermal conductivity")
BENCH-T19-002: Extract simulation parameters from methods section
BENCH-T19-003: Verify that cited values match actual paper content
BENCH-T19-004: Synthesize methodology from multiple papers
```

---

### Gap 4: Resource Acquisition Benchmarks

**Status:** Skill exists, no dedicated testing

**Missing Tests:**
- Find appropriate force field for system
- Find pseudopotentials for DFT
- Find crystal structure from database
- Find experimental data for validation
- Handle "resource not found" gracefully

**Proposed:** Add to existing tiers or create focused benchmarks

```yaml
BENCH-T4-XXX: Find Tersoff parameters for novel ternary system
BENCH-T4-XXX: Acquire ONCV pseudopotentials for rare earth
BENCH-T4-XXX: Find experimental thermal conductivity for validation
```

---

### Gap 5: Multi-Skill Integration

**Status:** Some coverage in T14, T7, but limited

**Missing Tests:**
- Full research pipeline: Literature → Structure → Simulation → Analysis
- Graceful degradation when one skill fails
- Skill handoff (output of one = input of another)
- Cross-skill error recovery

**Proposed:** Enhance T7 or create integration-focused benchmarks

```yaml
BENCH-T7-004: Complete novice-to-expert research workflow
  - Start with only paper citation
  - Must find structure, force field, run simulation, analyze
  - Multi-day with checkpoints
```

---

### Gap 6: MLIP Training Benchmarks

**Status:** We test USING MLIPs, not training them

**Missing Tests:**
- Fine-tune MACE on new data
- Active learning: select structures for DFT
- Assess model uncertainty
- Domain adaptation

**Proposed:** Create T20 - MLIP Development tier

```yaml
BENCH-T20-001: Fine-tune MACE-MP on surface data
BENCH-T20-002: Active learning loop (MLIP → select → DFT → retrain)
BENCH-T20-003: Uncertainty-guided structure selection
BENCH-T20-004: Transfer learning across chemistries
```

Requires: QE for DFT data generation (now available)

---

### Gap 7: Visualization and Reporting

**Status:** Minimal coverage, often graded implicitly

**Missing Tests:**
- Generate ASE/VESTA structure visualizations
- Create property vs composition plots
- Write methods section for paper
- Generate SI tables

**Proposed:** Could add to T16 (Scientific Rigor) or new tier

```yaml
BENCH-T16-XXX: Generate publication-ready figure from trajectory
BENCH-T16-XXX: Write reproducible methods section
```

---

### Gap 8: Negative/Adversarial Testing

**Status:** Some in T13 (Robustness), could expand

**Missing Tests:**
- Deliberately broken inputs
- Contradictory instructions
- Resource exhaustion scenarios
- Malicious file injection attempts
- Prompt injection resistance

**Proposed:** Expand T13

```yaml
BENCH-T13-009: Handle corrupted input file gracefully
BENCH-T13-010: Detect and refuse impossible physical parameters
BENCH-T13-011: Maintain focus despite distractor instructions
```

---

## Priority Ranking

| Priority | Gap | Effort | Impact | Status |
|----------|-----|--------|--------|--------|
| 1 | DFT (T10) | Low | High | **PARTIAL** - T10-004 passed (85), 3 more to run |
| 2 | Data Analysis (T18) | Medium | High | **DONE** - T18-001/002 both passed (92) |
| 3 | VAST.ai (T17) | In progress | High | **DONE** - All 3 benchmarks pass (97, 91, 92) |
| 4 | Resource Acquisition | Low | Medium | Pending - Add to T4 |
| 5 | Literature Search (T19) | Medium | Medium | Pending - Create T19 tier |
| 6 | Multi-Skill Integration | High | High | Pending - Enhance T7 |
| 7 | MLIP Training (T20) | High | Medium | Pending - Create T20 (DFT now ready) |
| 8 | Visualization | Low | Low | Pending - Add to T16 |
| 9 | Adversarial | Medium | Low | Pending - Expand T13 |

---

## Immediate Actions

1. ~~**Run T10 Benchmarks**~~ → T10-004 passed (85), run remaining 3
2. ~~**Finish T17 Benchmarks**~~ → **DONE** (3/3 passing: 97, 91, 92)
3. ~~**Create T18-001**~~ → **DONE** (T18-001: 92, T18-002: 92)
4. **Run remaining T10** - T10-001, T10-002, T10-003 (complex frontier tasks)
5. **Create T17-004 through T17-008** - Advanced cloud benchmarks
6. **Add resource-acquisition to T4** - Practical coverage

---

## Skill Development Needs

| Skill | Current State | Improvement Needed |
|-------|---------------|-------------------|
| quantum-espresso | Good docs | Add GPU examples |
| data-analysis | Basic | Add property calculators |
| literature-search | Basic | Add paper parsing |
| resource-acquisition | Good | Add more sources |
| theory-synthesis | Exists | Needs Theorizer MCP |

---

*This analysis should be revisited quarterly to track progress.*
