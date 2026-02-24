# Benchmark Next Steps

**Last Updated:** 2026-02-23
**Status:** Strong foundation, expanding coverage

---

## Current State

| Metric | Value |
|--------|-------|
| Total active benchmarks | 86 |
| Passing | 78 (100% of run) |
| Not yet run | 8 (T10-001/002/003, T12-*, T7-001/003) |
| Archived (CURC) | T5, T6, T11 |

**Recent wins (2026-02-23):**
- T17 Cloud GPU: 3/3 passing (97, 91, 92) - VAST.ai integration validated
- T18 Data Analysis: 2/2 passing (92, 92) - new tier created
- T10-004 Basic DFT: 85 - QE GPU working

---

## Immediate Priorities

### 1. Run Remaining T10 Benchmarks (Frontier DFT)

```bash
python benchmarks/evaluation/harness.py BENCH-T10-001  # Novel material discovery
python benchmarks/evaluation/harness.py BENCH-T10-002  # Cross-modal reasoning
python benchmarks/evaluation/harness.py BENCH-T10-003  # Open research question
```

**Prerequisites:** QE GPU is working (validated via T10-004)
**Time:** 60-120 min each
**Complexity:** High - these are frontier challenges

### 2. Create More T17 Benchmarks (Cloud GPU)

Per VASTAI_BENCHMARK_PROPOSAL.md, implement:
- T17-004: Cost-aware GPU selection
- T17-005: Multi-instance parallel jobs
- T17-006: Error recovery
- T17-007: Long job with checkpointing
- T17-008: Hybrid local-cloud pipeline

**Location:** `benchmarks/tasks/tier17_cloud_gpu/`

### 3. Create More T18 Benchmarks (Data Analysis)

Per GAP_ANALYSIS.md:
- T18-003: Generate publication-quality plots
- T18-004: Error propagation through multi-step analysis

**Location:** `benchmarks/tasks/tier18_data_analysis/`

---

## Blocked / Deferred

| Item | Reason | When to Resume |
|------|--------|----------------|
| T5, T6, T11 | CURC HPC deferred | When CURC access restored |
| T7-001, T7-003 | Need HPC for multi-day runs | Use VAST.ai alternative? |
| T12-* | Needs Theorizer MCP | When ASTA integration ready |

---

## Key Patterns Learned

### Prompt Design (Critical!)

**Detailed prompts prevent early termination:**
```
**IMPORTANT: You must complete ALL steps below.**

1. Step one...
2. Step two...
3. Step three...

**Completion Checklist:**
- [ ] Item 1 done
- [ ] Item 2 done
- [ ] Item 3 done

Do NOT stop after step 1. ALL steps are required.
```

### VAST.ai Safety

Always include cleanup verification:
```bash
# After benchmark
vastai show instances | grep BENCH  # Should be empty
```

### Consistency Testing

For any flaky benchmark, run 3x before/after fixes:
- Mean ≥ 65 with 2/3 passing = acceptable
- All 3 pass = robust

---

## Files to Read for Context

| File | Purpose |
|------|---------|
| `benchmarks/CURRENT_STATUS.md` | Live dashboard |
| `benchmarks/GAP_ANALYSIS.md` | Coverage gaps |
| `benchmarks/IMPROVEMENT_METHODOLOGY.md` | How to fix failures |
| `benchmarks/VASTAI_BENCHMARK_PROPOSAL.md` | T17 design |
| `skills/vast-cloud/SKILL.md` | VAST.ai usage |
| `skills/quantum-espresso/SKILL.md` | QE GPU paths |

---

## Success Metrics

| Goal | Target | Current | Status |
|------|--------|---------|--------|
| Foundation (T1-T4) | ≥90% | 100% | ✅ |
| Quality (T13-T16) | ≥90% | 100% | ✅ |
| Cloud GPU (T17) | ≥80% | 100% | ✅ |
| Data Analysis (T18) | ≥80% | 100% | ✅ |
| Frontier DFT (T10) | ≥50% | 25% | ⏳ Run 3 more |
| Overall pass rate | 100% | 100% | ✅ |

---

*Next session: Run T10-001/002/003, create T17-004+, create T18-003+*
