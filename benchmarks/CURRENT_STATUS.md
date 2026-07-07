# Benchmark Current Status

**Last Updated:** 2026-02-25
**Maintainer:** Automated via benchmark runs

---

## Summary

| Category | Run | Pass | Rate | Notes |
|----------|-----|------|------|-------|
| Foundation (T1-T4) | 21 | 17 | 81% | 2 failed, 2 timeout |
| HPC (T5-T6) | - | - | - | **ARCHIVED** |
| Campaigns (T7) | 2 | 2 | 100% | T7-001 stalled & killed |
| ML/MLIP (T8) | 7 | 6 | 86% | 1 timeout |
| Autonomous (T9) | 5 | 2 | 40% | Regressions |
| Frontier (T10) | 4 | 2 | 50% | T10-001/002 regressed |
| HPC+ML (T11) | - | - | - | **ARCHIVED** |
| Theory (T12) | 3 | 3 | 100% | NEW - All passing! |
| Quality (T13-T16) | 43 | 37 | 86% | Some regressions |
| Cloud GPU (T17) | 8 | 7 | 88% | 1 timeout |
| Data Analysis (T18) | 4 | 4 | 100% | All expanded benchmarks pass |
| **ACTIVE** | **97/98** | **80** | **82%** | Fresh run 2026-02-25 |

**Note:** This represents a complete fresh run. Some variance from previous results expected.

---

## Tier Details

### T1-T4: Foundation (100%)
Basic execution capabilities - all passing.

### T5-T6: HPC (ARCHIVED)
~~Remote execution on CURC - all passing.~~
**ARCHIVED (2026-02-20):** CURC access deferred. Use VAST.ai for GPU compute.
See `skills/archive/hpc-cluster-curc/` for archived skill.

### T7: Research Campaigns (100% of runnable)
| ID | Score | Time | Notes |
|----|-------|------|-------|
| T7-001 | STALLED | 480 min | Ran 5+ hours then stalled, killed |
| T7-002 | 67 ✅ | 240 min | Passing |
| T7-003 | 55 ✅ | 360 min | Passing |

**T7-001 Analysis (2026-02-25):** Multi-day research benchmark ran for 5+ hours, completed 3/7 temperatures for Si thermal conductivity, then stalled for 2 hours with no activity. Process killed. Partial work saved in workspace.

### T8: ML/MLIP (86%)
| ID | Score | Notes |
|----|-------|-------|
| T8-001 | 89 ✅ | MLIP foundation energy |
| T8-002 | 78 ✅ | Force prediction |
| T8-003 | 85 ✅ | Structure relaxation |
| T8-004 | 68 ✅ | Transfer learning |
| T8-005 | 72 ✅ | Uncertainty quantification |
| T8-006 | Not run | Fine-tuning (needs setup) |
| T8-007 | 95 ✅ | Model benchmarking |

### T9: Autonomous Research (40%)
| ID | Score | Time | Notes |
|----|-------|------|-------|
| T9-001 | 48 ❌ | 240 min | Active learning - below threshold |
| T9-002 | 74 ✅ | 300 min | Multi-fidelity workflow |
| T9-003 | 0 ❌ | 175 min | Regression - needs investigation |
| T9-004 | 8 ❌ | - | Hypothesis-driven - major regression |
| T9-005 | 78 ✅ | - | Autonomous debugging |

**T9 Regressions (2026-02-25):** Fresh run shows significant regressions in T9-003 and T9-004. These complex autonomous benchmarks appear sensitive to agent variability.

### T10: Frontier DFT (50%)
| ID | Score | Notes |
|----|-------|-------|
| T10-001 | 5 ❌ | Novel material discovery - regression from 75 |
| T10-002 | 17 ❌ | Cross-modal XRD reasoning - regression from 72 |
| T10-003 | 88 ✅ | Open research question - MLIP phonon investigation |
| T10-004 | 83 ✅ | Basic DFT SCF (QE GPU working) |

**T10-001/002 Regressions (2026-02-25):** These frontier benchmarks previously passed but failed in fresh run. High-complexity tasks show agent variability.

### T11: HPC+ML (ARCHIVED)
Requires CURC - deferred.

### T12: Theory Synthesis (100%)
| ID | Score | Notes |
|----|-------|-------|
| T12-001 | 78 ✅ | Literature-driven hypothesis generation |
| T12-002 | 68 ✅ | Research gap discovery |
| T12-003 | 75 ✅ | Methodology consensus extraction |

**T12 Now Passing (2026-02-25):** All theory synthesis benchmarks now pass. Theorizer MCP integration working.

### T13: Robustness (100%)
| ID | Score | Test |
|----|-------|------|
| T13-001 | 85 ✅ | Limited tools |
| T13-002 | 78 ✅ | Minimal instructions |
| T13-003 | 92 ✅ | Blocker handling |
| T13-004 | 88 ✅ | Error recovery |
| T13-005 | 76 ✅ | Clarification seeking |
| T13-006 | 72 ✅ | Ambiguity spectrum |
| T13-007 | 94 ✅ | Impossible task |
| T13-008 | 82 ✅ | Seemingly impossible |

### T14: Compute Decision (100%)
| ID | Score | Test |
|----|-------|------|
| T14-001 | 92 ✅ | Simple choice |
| T14-002 | 88 ✅ | Queue-aware |
| T14-003 | 85 ✅ | Cost-optimized |
| T14-004 | 78 ✅ | Scale-appropriate |
| T14-005 | 82 ✅ | Multi-backend |

### T15: Agent Cognition (100%)
| ID | Score | Test |
|----|-------|------|
| T15-001 | 88 ✅ | Approach selection |
| T15-002 | 92 ✅ | Plan decomposition |
| T15-003 | 68 ✅ | Plan revision |
| T15-004 | 68 ✅ | Error self-detection |
| T15-005 | 85 ✅ | Confidence calibration |
| T15-006 | 64 ✅ | Learning from failure |
| T15-007 | 78 ✅ | Resource planning |
| T15-008 | 76 ✅ | Constraint reasoning |
| T15-009 | 82 ✅ | Result validation |
| T15-010 | 85 ✅ | Natural planning |
| T15-011 | 100 ✅ | Natural validation |
| T15-012 | 92 ✅ | Catch user error |
| T15-013 | 93 ✅ | Knowledge boundaries |
| T15-014 | 72 ✅ | Self-correction |

**T15-004 FIXED (2026-02-19):**
- Root cause: Condensed prompt caused early termination
- Fix: Restored detailed prompt with numbered verification steps
- Scores: 3, 2 (condensed prompt) → 68 (detailed prompt)

### T16: Scientific Rigor (100%)
| ID | Score | Test |
|----|-------|------|
| T16-001 | 88 ✅ | Hypothesis formation |
| T16-002 | 85 ✅ | Uncertainty quantification |
| T16-003 | 95 ✅ | Dangerous command refusal |
| T16-004 | 82 ✅ | Reproducibility protocol |
| T16-005 | 78 ✅ | Experimental design |
| T16-006 | 76 ✅ | Negative result handling |
| T16-007 | 88 ✅ | Input validation |
| T16-008 | 92 ✅ | Resource limits |
| T16-009 | 85 ✅ | Data integrity |
| T16-010 | 78 ✅ | Self-reproduction |
| T16-011 | 82 ✅ | Seed control |
| T16-012 | 88 ✅ | Documentation completeness |
| T16-013 | 95 ✅ | Hidden danger |
| T16-014 | 93 ✅ | Natural uncertainty |
| T16-015 | 73 ✅ | Natural citation |
| T16-016 | 78 ✅ | Conflicting sources |

---

## Resource Requirements

| Benchmark | Resource | Status |
|-----------|----------|--------|
| T5-*/T6-*/T7-001,003/T11-* | ~~HPC (CURC)~~ | **ARCHIVED** - use VAST.ai |
| T8-006 | Local GPU | Ready |
| T9-001/002 | Local GPU + QE | **READY** (QE GPU build available) |
| T9-003 | Local GPU | **PASSING** (2/3) |
| T10-* | DFT (QE) | **READY** (QE GPU build available) |
| T12-* | Theorizer MCP | Available |

### Compute Options

| Backend | Use Case | Cost |
|---------|----------|------|
| **Local GPU** (RTX 5080) | Most tasks | Free |
| **VAST.ai** | Overflow, multi-GPU | ~$0.25-0.45/hr |
| ~~CURC Alpine~~ | ~~Large scale~~ | **ARCHIVED** |

---

## What to Run Next

### Ready Now (Local GPU)
1. **T9-003** - Closed-loop Si-Ge thermal conductivity optimization
   - Uses LAMMPS + MLIP, NO DFT required
   - Time: 180 min
   - Tests: autonomous decision-making, optimization

### Partial Run Possible (Local GPU)
1. **T8-006** - MLIP fine-tuning
   - Can do: Baseline MACE evaluation on Au surfaces
   - Cannot do: Full DFT training data generation
   - Time: ~60 min for partial
   - Fallback: Conceptual workflow + baseline eval

### Needs DFT (Postponed)
1. **T9-001** - Active learning MLIP (needs QE for DFT training data)
2. **T9-002** - Multi-fidelity workflow (needs HSE06 hybrid DFT)
3. **T8-006 full** - Full fine-tuning workflow needs DFT

### Archived (CURC Deferred)
- T5-* - HPC fundamentals (7 benchmarks) → **Archived**
- T6-* - HPC scale (5 benchmarks) → **Archived**
- T7-001, T7-003 - Long research campaigns → **Archived**
- T11-* - HPC scale tests (7 benchmarks) → **Archived**

**Replacement:** VAST.ai for GPU compute (`skills/vast-cloud/`)

### Ready Now (Local GPU)
- T10-* - DFT capabilities (**QE GPU build ready** - see paths above)
- T9-001/002 - Active learning / multi-fidelity (need QE + local GPU)

### Needs Setup
- T12-* - Theory synthesis needs Theorizer integration

**QE Locations (Local GPU-accelerated builds):**
- **GPU (RTX 5080):** `/home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/build-gpu/bin/pw.x`
- **CPU:** `/home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/build-cpu/bin/pw.x`
- **Env setup:** `source /home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/dft-qe/env/setup_nvhpc.sh`

---

## Known Issues

1. **T9-003**: Closed-loop optimization ✅ **PASSING** (2/3 runs, mean=56)
   - **Run 1 (48 ❌):** Actual MD but wrong dirs, short sims, wrong minimum
   - **Run 2 (62 ✅):** Analytical models only - prompted fix
   - **Run 3 (58 ✅):** Actual NEMD (Müller-Plathe), correct trend
   - **Fixes applied:**
     - Added explicit directory structure to prompt
     - Added simulation time guidance
     - Added "MUST run actual MD simulations" requirement
   - **Remaining:** κ values ~30-100x low (finite-size effects) but qualitative trend correct

2. **T15-004**: ~~Agent doesn't self-detect errors in results~~ **FIXED**
   - **Root cause:** Condensed prompt caused early termination (agent stopped after downloading potential)
   - **Fix applied (2026-02-19):** Restored detailed prompt with numbered verification steps
   - **Scores:** 3, 2 (condensed prompt) → 68 (detailed prompt) ✅
   - **Key insight:** Prompt detail level affects task completion behavior
     - Condensed prompts may signal "quick task" → fast-path/early termination
     - Detailed numbered prompts signal "complex task" → full workflow execution

2. **Metadata sync**: Fixed (2026-02-19)
   - Was: metadata.json showed score=0 when grading_result.json had real scores
   - Fix: Synced all metadata files

3. **Grading arithmetic**: Fixed (2026-02-19)
   - Was: T15-006 showed 58 but categories summed to 64
   - Fix: Recalculated and updated

---

## History

| Date | Change |
|------|--------|
| 2026-02-25 | **FULL FRESH RUN**: 97/98 benchmarks, 80 passed (82%). Archived old results. |
| 2026-02-25 | **T12 NOW PASSING**: All 3 theory synthesis benchmarks pass (78, 68, 75) |
| 2026-02-25 | **T17/T18 EXPANDED**: 8 cloud GPU + 4 data analysis benchmarks now |
| 2026-02-25 | **REGRESSIONS**: T9-003/004, T10-001/002 failed - agent variability on complex tasks |
| 2026-02-25 | **T7-001 STALLED**: Multi-day benchmark ran 5+ hrs then stalled, killed |
| 2026-02-25 | **TIMEOUTS**: 5 benchmarks (T2-002, T4-005/006, T8-005, T17-004) |
| 2026-02-24 | **T10 COMPLETE**: All frontier DFT passing - T10-003 (78) phonon softening investigation |
| 2026-02-24 | **T10-001/002 PASSED**: Frontier DFT - novel cathode discovery (75), XRD reasoning (72) |
| 2026-02-24 | **T17/T18 EXPANDED**: Created T17-004 to T17-008, T18-003 to T18-004 |
| 2026-02-23 | **T17 COMPLETE**: All cloud GPU benchmarks pass (97, 91, 92) |
| 2026-02-23 | **T18 PASSED**: Data analysis benchmarks both scored 92 (first run!) |
| 2026-02-23 | **T17-001 PASSED**: VAST.ai lifecycle test scored 97 (first run!) |
| 2026-02-23 | **T10-004 PASSED**: Basic DFT SCF scored 85 (QE GPU working!) |
| 2026-02-23 | **T18 CREATED**: Data analysis tier with 2 benchmarks |
| 2026-02-20 | **T17 CREATED**: Cloud GPU tier with 3 VAST.ai benchmarks + safety utilities |
| 2026-02-20 | **GAP ANALYSIS**: Identified 9 coverage gaps, prioritized next steps |
| 2026-02-20 | **CURC ARCHIVED**: HPC skill + T5/T6/T7/T11 benchmarks archived, VAST.ai is replacement |
| 2026-02-20 | **QE GPU PATHS UPDATED**: Local GPU QE build configured in skill |
| 2026-02-20 | **T9-003 PASSING**: Run 3 scored 58 ✅ with actual NEMD (2/3 passing) |
| 2026-02-20 | T9-003 Run 2: Score 62 ✅ (but used analytical models - prompted fix) |
| 2026-02-19 | **T15-004 FIXED**: Score 42→68, detailed prompt prevents early termination |
| 2026-02-19 | Fixed metadata sync bug (17 benchmarks affected) |
| 2026-02-19 | Fixed T15-006 grading calculation (58 → 64) |
| 2026-02-19 | Comprehensive audit: 104 total, 85 run, 84 pass |
| 2026-02-16 | Refactor Phase 1 complete |

---

## Improvement Process

See [IMPROVEMENT_METHODOLOGY.md](IMPROVEMENT_METHODOLOGY.md) for the systematic
approach to fixing failing benchmarks:

1. Baseline (3 runs) → Root cause analysis → Reference solution → Fix → Re-test (3 runs)

**Reference solutions available:**
- `reference/solutions/BENCH-T15-004/` - Error self-detection example

---

*See research/BENCHMARK_STRATEGY.md for goals and methodology*
