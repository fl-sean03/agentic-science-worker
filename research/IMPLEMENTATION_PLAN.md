# ASW Full Implementation Plan

**Created:** 2026-02-19
**Status:** Phase 1-2 Complete, Phase 3-4 Ready
**Goal:** Complete Phase 1-4 benchmark improvements, reach 80%+ overall pass rate

---

## Current Status Summary (2026-02-19)

| Tier | Pass Rate | Status |
|------|-----------|--------|
| T13 Robustness | 8/8 (100%) | ✅ Complete |
| T14 Compute | 5/5 (100%) | ✅ Complete |
| T15 Cognition | 13/14 (93%) | ✅ Near-complete (1 hard failure) |
| T16 Rigor | 16/16 (100%) | ✅ Complete |
| T7 Campaigns | 1/3 (33%) | ⏳ 2 long benchmarks pending |
| T9 Autonomous | 2/5 (40%) | ⏳ 3 long benchmarks pending |

**Overall T13-T16:** 42/43 (98%)

---

## Completed Work

### Phase 1A: Investigate & Fix Error Benchmarks ✅

**Bug Fixed:** Metadata/grading score mismatch
- 17 benchmarks had score=0 in metadata.json but real scores (62-92) in grading_result.json
- Root cause: Grading re-run separately from main run, metadata not updated
- Fix: Synced all metadata.json files from grading_result.json

**Bug Fixed:** T15-006 grading calculation
- LLM grader arithmetic error: stored 58 but categories sum to 64
- Fix: Recalculated and updated to correct score (64 = passing)

### Phase 1B: Run Missing Benchmarks ✅

All T15 and T16 benchmarks have been run:
- T15: 14/14 run (13 passing, 1 failing)
- T16: 16/16 run (16 passing)

### Phase 1C: Fix Remaining Failures ⚠️

**T15-004 Error Self-Detection - NOT FIXED**
- Score: 0-42 across runs (needs 60)
- Issue: Agent doesn't recognize when results are outside expected ranges
- This is a genuinely difficult capability test
- Best run showed agent did the work but accepted wrong results
- Would need substantial guidance improvements to fix

### Phase 1D: Validation & Documentation ✅

- Updated BENCHMARK_TRACKING.md with accurate scores
- All T15/T16 scores verified and documented

### Phase 2: Robustness Verification ✅

- T13: 8/8 (100%)
- T14: 5/5 (100%)
- No action needed - already at target

---

## Remaining Work

### Phase 3: Autonomy Capabilities (T7/T9)

These are long-running (2-8 hour) benchmarks testing real research capabilities.

| Benchmark | Time | Status | Notes |
|-----------|------|--------|-------|
| T7-001 | 480 min | Not run | Multi-day HPC campaign |
| T7-002 | 240 min | 85 ✅ | Already passing |
| T7-003 | 360 min | Not run | Collaborative computation |
| T9-001 | 240 min | Not run | Active learning MLIP |
| T9-002 | 300 min | Not run | Multi-fidelity workflow |
| T9-003 | 180 min | Not run | Closed-loop optimization |
| T9-004 | 180 min | 65 ✅ | Already passing |
| T9-005 | 120 min | 82 ✅ | Already passing |

**Current:** 3/8 passing (38%)
**To reach 60%:** Need 2 more passing (T7-003, T9-001, T9-002, or T9-003)

### Phase 4: Frontier Capabilities (T10-T12)

Not yet started. These are the most challenging benchmarks.

---

## Success Criteria Status

| Phase | Metric | Target | Actual | Status |
|-------|--------|--------|--------|--------|
| 1 | T15 pass rate | ≥70% (10/14) | 93% (13/14) | ✅ Exceeded |
| 1 | T16 pass rate | ≥70% (11/16) | 100% (16/16) | ✅ Exceeded |
| 1 | Error benchmarks fixed | All 8 → 0 | Fixed (metadata sync) | ✅ Complete |
| 2 | T13-14 pass rate | ≥90% | 100% | ✅ Exceeded |
| 3 | T7 pass rate | ≥60% (2/3) | 33% (1/3) | ⏳ Pending |
| 3 | T9 pass rate | ≥60% (3/5) | 40% (2/5) | ⏳ Pending |
| 4 | T10-12 all run | Complete | Not started | ⏳ Pending |

---

## Execution Log

| Time | Action | Result |
|------|--------|--------|
| 2026-02-19 00:15 | Plan created | Ready to execute |
| 2026-02-19 ~10:00 | Phase 1A start | Investigating errors |
| 2026-02-19 ~10:30 | Found metadata bug | 17 benchmarks affected |
| 2026-02-19 ~10:35 | Fixed metadata sync | All scores corrected |
| 2026-02-19 ~10:40 | Fixed T15-006 calc | 58 → 64 (now passing) |
| 2026-02-19 ~10:50 | Updated tracking | BENCHMARK_TRACKING.md updated |
| 2026-02-19 ~11:00 | Phase 3 analysis | T7/T9 benchmarks are 2-8 hour runs |

---

## Commands Reference

```bash
# Run single benchmark
python benchmarks/run.py BENCH-T15-003

# Run with verbose
python benchmarks/run.py BENCH-T7-001 --verbose

# Get latest score for a benchmark
python3 -c "
import json
from pathlib import Path
results = Path('benchmarks/results/runs')
latest = sorted(results.glob('BENCH-T15-004-*'))[-1]
print(json.load(open(latest/'metadata.json')).get('score'))
"

# Run tier (careful - T7/T9 are very long!)
# python benchmarks/run.py --tier 7
```

---

## Key Insights

### What Worked
1. **Metadata sync fix** - Revealed 17 benchmarks were actually passing
2. **Grading calculation fix** - T15-006 was passing but marked as failed
3. **General principles** - "Genuine Revision" principle fixed T15-003

### What's Hard
1. **T15-004 Error Self-Detection** - Agent accepts wrong results without flagging
2. **T7/T9 Long benchmarks** - 2-8 hours each, real research campaigns
3. **Phase 4 Frontier** - T10-T12 are designed to be very difficult

### Architecture Notes
- Benchmarks use two JSON formats (old: result.json, new: metadata.json)
- LLM grader can make arithmetic errors (should verify category sum)
- Long benchmarks designed for real HPC campaigns, not quick testing

---

*This plan is actively maintained. Update after each significant action.*
