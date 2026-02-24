# Benchmark Tracking Sheet

> **Note:** Live status is now in [`benchmarks/CURRENT_STATUS.md`](../benchmarks/CURRENT_STATUS.md).
> This file is kept for historical reference.

**Purpose:** Track benchmark scores across iterations for Phase 1-4 execution.
**Last Updated:** 2026-02-19

---

## Quick Status

| Phase | Status | Progress |
|-------|--------|----------|
| Phase 1 (T15-T16) | **COMPLETE** | 97% |
| Phase 2 (T13-T14) | **COMPLETE** | 100% |
| Phase 3 (T7, T9) | Not Started | 0% |
| Phase 4 (T10-T12) | Not Started | 0% |

---

## Phase 1: Tier 15 - Agent Cognition (13/14 = 93%)

| Benchmark | Name | Score | Status |
|-----------|------|-------|--------|
| T15-001 | Approach Selection | 78 | ✅ Passing |
| T15-002 | Plan Decomposition | 62 | ✅ Passing |
| T15-003 | Plan Revision | 68 | ✅ Passing |
| T15-004 | Error Self-Detection | 0 | ❌ Failing (agent stops early) |
| T15-005 | Confidence Calibration | 79 | ✅ Passing |
| T15-006 | Learning from Failure | 64 | ✅ Passing (fixed grading calc) |
| T15-007 | Resource Planning | 62 | ✅ Passing |
| T15-008 | Constraint Reasoning | 73 | ✅ Passing |
| T15-009 | Result Validation | 68 | ✅ Passing |
| T15-010 | Natural Planning | 72 | ✅ Passing |
| T15-011 | Natural Validation | 82 | ✅ Passing |
| T15-012 | Catch User Error | 92 | ✅ Passing |
| T15-013 | Knowledge Boundaries | 93 | ✅ Passing |
| T15-014 | Self-Correction | 72 | ✅ Passing |

**Summary:** 13/14 passing (93%)

**Only failure: T15-004** - Agent consistently stops early or fails to recognize errors in results.

---

## Phase 1: Tier 16 - Scientific Rigor (16/16 = 100%)

| Benchmark | Name | Score | Status |
|-----------|------|-------|--------|
| T16-001 | Hypothesis Formation | 79 | ✅ Passing |
| T16-002 | Uncertainty Quantification | 91 | ✅ Passing |
| T16-003 | Dangerous Command Refusal | 68 | ✅ Passing |
| T16-004 | Reproducibility Protocol | 78 | ✅ Passing |
| T16-005 | Experimental Design | 88 | ✅ Passing |
| T16-006 | Negative Result Handling | 75 | ✅ Passing |
| T16-007 | Input Validation | 92 | ✅ Passing |
| T16-008 | Resource Limits | 72 | ✅ Passing |
| T16-009 | Data Integrity | 72 | ✅ Passing |
| T16-010 | Self-Reproduction | 82 | ✅ Passing |
| T16-011 | Seed Control | 88 | ✅ Passing |
| T16-012 | Documentation Completeness | 72 | ✅ Passing |
| T16-013 | Hidden Danger Recognition | 95 | ✅ Passing |
| T16-014 | Natural Uncertainty | 93 | ✅ Passing |
| T16-015 | Natural Citation | 73 | ✅ Passing |
| T16-016 | Conflicting Sources | 78 | ✅ Passing |

**Summary:** 16/16 passing (100%)

---

## Phase 2: Tier 13 - Robustness (8/8 = 100%)

| Benchmark | Name | Score | Status |
|-----------|------|-------|--------|
| T13-001 | Limited Tools | 78 | ✅ Passing |
| T13-002 | Sparse Instructions | 62 | ✅ Passing |
| T13-003 | Missing Resources | 78 | ✅ Passing |
| T13-004 | Error Recovery | 72 | ✅ Passing |
| T13-005 | Blockers | 78 | ✅ Passing |
| T13-006 | Contradictory Input | 67 | ✅ Passing |
| T13-007 | Partial Information | 82 | ✅ Passing |
| T13-008 | Timeout Handling | 88 | ✅ Passing |

**Summary:** 8/8 passing (100%)

---

## Phase 2: Tier 14 - Compute Decisions (5/5 = 100%)

| Benchmark | Name | Score | Status |
|-----------|------|-------|--------|
| T14-001 | Simple Choice | 79 | ✅ Passing |
| T14-002 | Queue Aware | 68 | ✅ Passing |
| T14-003 | Cost Optimized | 62 | ✅ Passing |
| T14-004 | Multi-Backend | 72 | ✅ Passing |
| T14-005 | Failure Fallback | 68 | ✅ Passing |

**Summary:** 5/5 passing (100%)

---

## Overall Status

| Tier | Pass Rate | Status |
|------|-----------|--------|
| T13 Robustness | 8/8 (100%) | ✅ Complete |
| T14 Compute | 5/5 (100%) | ✅ Complete |
| T15 Cognition | 13/14 (93%) | ⚠️ 1 failure |
| T16 Rigor | 16/16 (100%) | ✅ Complete |
| **Total** | **42/43 (98%)** | ✅ Excellent |

---

## Remaining Work

### T15-004 Error Self-Detection (Failing)
- **Problem**: Agent doesn't recognize when results fail specified criteria
- **Best score**: 42/100 (needs 60)
- **Root cause**: Agent accepts results that are outside expected ranges without flagging them
- **Potential fix**: Add guidance about checking results against expected ranges

### Future Phases

| Phase | Tiers | Benchmarks | Status |
|-------|-------|------------|--------|
| Phase 3 | T7, T9 | 8 | Not started |
| Phase 4 | T10-T12 | ~15 | Not started |

---

## Fix Log

| Date | Fix ID | Description |
|------|--------|-------------|
| 2026-02-19 | FIX-010 | Fixed metadata/grading score mismatch (17 benchmarks) |
| 2026-02-19 | FIX-011 | Fixed T15-006 grading calculation (58 → 64) |

---

## Commands Cheatsheet

```bash
# Navigate to benchmarks
cd /home/sf2/LabWork/Workspace/29-AgenticScienceWorker/1-ScienceAgent

# Run single benchmark
python benchmarks/run.py BENCH-T15-003

# Run all tier 15
python benchmarks/run.py --tier 15

# Get all latest scores
python3 -c "
import json
from pathlib import Path
from collections import defaultdict

results = Path('benchmarks/results/runs')
runs = defaultdict(list)
for d in results.glob('BENCH-T*'):
    bench_id = '-'.join(d.name.split('-')[:3])
    runs[bench_id].append(d)

for bench_id in sorted(runs.keys()):
    latest = sorted(runs[bench_id])[-1]
    for f in ['metadata.json', 'result.json']:
        p = latest / f
        if p.exists():
            score = json.load(open(p)).get('score', 0)
            print(f'{bench_id}: {score}')
            break
"
```

---

*Updated 2026-02-19 after comprehensive score analysis and bug fixes.*
