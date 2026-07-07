# GENERATED Benchmark Status — artifact-derived, do not hand-edit

**Generated:** 2026-07-06 05:51 UTC by `benchmarks/evaluation/generate_status.py` (rebase-2026-07-02, model claude-fable-5)
**Source artifacts:** `/home/sf2/work/agents/science-agent/1-ScienceAgent/benchmarks/results/runs` (98 runs with result.json)

> This file is regenerated mechanically; every number is read from a
> `result.json` artifact. The human-maintained dashboard
> (`CURRENT_STATUS.md`) and the owner's uncommitted corrections to it
> remain the owner's record; where the two disagree, the divergence table
> below says so explicitly. Scores from runs without a `model` field are
> model-unattributed (pre-2026-07 era).

## Outcome tally

> Pass rate = passed / scored, where scored = total − void. VOID runs are
> infrastructure failures (agent_json.is_error: session-limit crash, CLI/
> transport error) that record a phantom score-0; they are NOT capability
> failures and are excluded from the denominator (see load_runs docstring).

| Passed | Failed | Timeout | Error | Void | Scored | Total | Pass rate |
|-------:|-------:|--------:|------:|-----:|-------:|------:|----------:|
| 88 | 9 | 0 | 0 | 1 | 97 | 98 | 90.7% |

## Per-tier results (latest run per task)

### Tier 1 — 7/7 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T1-001 | passed | 99 | 70 | claude-opus-4-8 | `BENCH-T1-001-20260705-202743` |
| T1-002 | passed | 99 | 70 | claude-opus-4-8 | `BENCH-T1-002-20260705-202743` |
| T1-003 | passed | 97 | 70 | claude-opus-4-8 | `BENCH-T1-003-20260705-202743` |
| T1-004 | passed | 99 | 70 | claude-opus-4-8 | `BENCH-T1-004-20260705-202743` |
| T1-005 | passed | 98 | 70 | claude-opus-4-8 | `BENCH-T1-005-20260705-202743` |
| T1-006 | passed | 96 | 70 | claude-opus-4-8 | `BENCH-T1-006-20260705-202743` |
| T1-007 | passed | 98 | 70 | claude-opus-4-8 | `BENCH-T1-007-20260705-202856` |

### Tier 2 — 3/4 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T2-001 | passed | 98 | 65 | claude-opus-4-8 | `BENCH-T2-001-20260705-233427` |
| T2-002 | passed | 99 | 65 | claude-opus-4-8 | `BENCH-T2-002-20260705-234005` |
| T2-003 | failed | 56 | 65 | claude-opus-4-8 | `BENCH-T2-003-20260706-015229` |
| T2-004 | passed | 92 | 65 | claude-opus-4-8 | `BENCH-T2-004-20260706-015229` |

### Tier 3 — 3/3 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T3-001 | passed | 85 | 60 | claude-opus-4-8 | `BENCH-T3-001-20260706-015229` |
| T3-002 | passed | 98 | 60 | claude-opus-4-8 | `BENCH-T3-002-20260706-015229` |
| T3-003 | passed | 64 | 60 | claude-opus-4-8 | `BENCH-T3-003-20260706-015649` |

### Tier 4 — 7/7 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T4-001 | passed | 97 | 60 | claude-opus-4-8 | `BENCH-T4-001-20260706-015921` |
| T4-002 | passed | 76 | 60 | claude-opus-4-8 | `BENCH-T4-002-20260706-020040` |
| T4-003 | passed | 98 | 60 | claude-opus-4-8 | `BENCH-T4-003-20260706-021028` |
| T4-004 | passed | 97 | 60 | claude-opus-4-8 | `BENCH-T4-004-20260706-021035` |
| T4-005 | passed | 89 | 60 | claude-opus-4-8 | `BENCH-T4-005-20260706-021308` |
| T4-006 | passed | 95 | 60 | claude-opus-4-8 | `BENCH-T4-006-20260706-022251` |
| T4-007 | passed | 65 | 60 | claude-opus-4-8 | `BENCH-T4-007-20260706-022440` |

### Tier 7 — 3/3 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T7-001 | passed | 91 | 50 | claude-opus-4-8 | `BENCH-T7-001-20260706-022900` |
| T7-002 | passed | 90 | 50 | claude-opus-4-8 | `BENCH-T7-002-20260706-023740` |
| T7-003 | passed | 61 | 50 | claude-opus-4-8 | `BENCH-T7-003-20260706-024026` |

### Tier 8 — 5/7 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T8-001 | passed | 97 | 60 | claude-opus-4-8 | `BENCH-T8-001-20260706-024402` |
| T8-002 | passed | 96 | 60 | claude-opus-4-8 | `BENCH-T8-002-20260706-025614` |
| T8-003 | passed | 94 | 60 | claude-opus-4-8 | `BENCH-T8-003-20260706-030231` |
| T8-004 | passed | 95 | 60 | claude-opus-4-8 | `BENCH-T8-004-20260706-031057` |
| T8-005 | failed | 43 | 60 | claude-opus-4-8 | `BENCH-T8-005-20260706-031210` |
| T8-006 | failed | 46 | 60 | claude-opus-4-8 | `BENCH-T8-006-20260706-032149` |
| T8-007 | passed | 94 | 60 | claude-opus-4-8 | `BENCH-T8-007-20260706-032203` |

### Tier 9 — 3/4 passed (1 void/infra)

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T9-001 | failed | 48 | 50 | claude-opus-4-8 | `BENCH-T9-001-20260706-032735` |
| T9-002 | passed | 76 | 50 | claude-opus-4-8 | `BENCH-T9-002-20260706-033747` |
| T9-003 | void | 0 | 50 | claude-opus-4-8 | `BENCH-T9-003-20260705-234818` |
| T9-004 | passed | 89 | 50 | claude-opus-4-8 | `BENCH-T9-004-20260706-041548` |
| T9-005 | passed | 94 | 50 | claude-opus-4-8 | `BENCH-T9-005-20260706-041706` |

### Tier 10 — 3/4 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T10-001 | failed | 5 | 40 | unrecorded | `BENCH-T10-001-20260225-065909` |
| T10-002 | passed | 44 | 40 | claude-opus-4-8 | `BENCH-T10-002-20260705-215602` |
| T10-003 | passed | 92 | 40 | claude-opus-4-8 | `BENCH-T10-003-20260705-225708` |
| T10-004 | passed | 94 | 40 | claude-opus-4-8 | `BENCH-T10-004-20260705-215602` |

### Tier 12 — 3/3 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T12-001 | passed | 75 | 50 | claude-opus-4-8 | `BENCH-T12-001-20260705-215602` |
| T12-002 | passed | 72 | 50 | claude-opus-4-8 | `BENCH-T12-002-20260705-215602` |
| T12-003 | passed | 94 | 50 | claude-opus-4-8 | `BENCH-T12-003-20260705-225709` |

### Tier 13 — 8/8 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T13-001 | passed | 94 | 60 | claude-opus-4-8 | `BENCH-T13-001-20260705-202952` |
| T13-002 | passed | 94 | 60 | claude-opus-4-8 | `BENCH-T13-002-20260705-203015` |
| T13-003 | passed | 96 | 60 | claude-opus-4-8 | `BENCH-T13-003-20260705-221950` |
| T13-004 | passed | 93 | 60 | claude-opus-4-8 | `BENCH-T13-004-20260705-203056` |
| T13-005 | passed | 96 | 60 | claude-opus-4-8 | `BENCH-T13-005-20260705-203209` |
| T13-006 | passed | 94 | 60 | claude-opus-4-8 | `BENCH-T13-006-20260705-221953` |
| T13-007 | passed | 96 | 60 | claude-opus-4-8 | `BENCH-T13-007-20260705-203509` |
| T13-008 | passed | 96 | 60 | claude-opus-4-8 | `BENCH-T13-008-20260705-203551` |

### Tier 14 — 5/5 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T14-001 | passed | 94 | 65 | claude-opus-4-8 | `BENCH-T14-001-20260705-221034` |
| T14-002 | passed | 94 | 65 | claude-opus-4-8 | `BENCH-T14-002-20260705-221624` |
| T14-003 | passed | 90 | 65 | claude-opus-4-8 | `BENCH-T14-003-20260705-222113` |
| T14-004 | passed | 94 | 65 | claude-opus-4-8 | `BENCH-T14-004-20260705-222654` |
| T14-005 | passed | 70 | 65 | claude-opus-4-8 | `BENCH-T14-005-20260705-225709` |

### Tier 15 — 13/14 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T15-001 | passed | 64 | 60 | claude-opus-4-8 | `BENCH-T15-001-20260705-203739` |
| T15-002 | passed | 92 | 60 | claude-opus-4-8 | `BENCH-T15-002-20260705-203826` |
| T15-003 | failed | 8 | 60 | claude-opus-4-8 | `BENCH-T15-003-20260705-221955` |
| T15-004 | passed | 93 | 60 | claude-opus-4-8 | `BENCH-T15-004-20260705-203917` |
| T15-005 | passed | 91 | 60 | claude-opus-4-8 | `BENCH-T15-005-20260705-203948` |
| T15-006 | passed | 91 | 60 | claude-opus-4-8 | `BENCH-T15-006-20260705-204126` |
| T15-007 | passed | 95 | 60 | claude-opus-4-8 | `BENCH-T15-007-20260705-213048` |
| T15-008 | passed | 93 | 60 | claude-opus-4-8 | `BENCH-T15-008-20260705-204800` |
| T15-009 | passed | 93 | 60 | claude-opus-4-8 | `BENCH-T15-009-20260705-204933` |
| T15-010 | passed | 97 | 60 | claude-opus-4-8 | `BENCH-T15-010-20260705-205009` |
| T15-011 | passed | 97 | 60 | claude-opus-4-8 | `BENCH-T15-011-20260705-205237` |
| T15-012 | passed | 97 | 60 | claude-opus-4-8 | `BENCH-T15-012-20260705-205404` |
| T15-013 | passed | 95 | 60 | claude-opus-4-8 | `BENCH-T15-013-20260705-205559` |
| T15-014 | passed | 88 | 60 | claude-opus-4-8 | `BENCH-T15-014-20260705-205750` |

### Tier 16 — 15/16 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T16-001 | passed | 94 | 70 | claude-opus-4-8 | `BENCH-T16-001-20260705-223139` |
| T16-002 | passed | 96 | 70 | claude-opus-4-8 | `BENCH-T16-002-20260705-223614` |
| T16-003 | passed | 96 | 70 | claude-opus-4-8 | `BENCH-T16-003-20260705-223930` |
| T16-004 | passed | 80 | 70 | claude-opus-4-8 | `BENCH-T16-004-20260705-224130` |
| T16-005 | passed | 95 | 70 | claude-opus-4-8 | `BENCH-T16-005-20260705-225709` |
| T16-006 | passed | 97 | 70 | claude-opus-4-8 | `BENCH-T16-006-20260705-225709` |
| T16-007 | passed | 93 | 70 | claude-opus-4-8 | `BENCH-T16-007-20260705-230811` |
| T16-008 | passed | 87 | 70 | claude-opus-4-8 | `BENCH-T16-008-20260705-230826` |
| T16-009 | passed | 95 | 70 | claude-opus-4-8 | `BENCH-T16-009-20260705-231443` |
| T16-010 | passed | 97 | 70 | claude-opus-4-8 | `BENCH-T16-010-20260705-231806` |
| T16-011 | passed | 96 | 70 | claude-opus-4-8 | `BENCH-T16-011-20260705-231900` |
| T16-012 | passed | 93 | 70 | claude-opus-4-8 | `BENCH-T16-012-20260706-044412` |
| T16-013 | passed | 99 | 70 | claude-opus-4-8 | `BENCH-T16-013-20260705-232325` |
| T16-014 | passed | 98 | 70 | claude-opus-4-8 | `BENCH-T16-014-20260705-232502` |
| T16-015 | failed | 61 | 70 | claude-opus-4-8 | `BENCH-T16-015-20260705-232541` |
| T16-016 | passed | 83 | 70 | claude-opus-4-8 | `BENCH-T16-016-20260705-232615` |

### Tier 17 — 7/8 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T17-001 | passed | 98 | 60 | claude-opus-4-8 | `BENCH-T17-001-20260706-020927` |
| T17-002 | passed | 91 | 60 | claude-opus-4-8 | `BENCH-T17-002-20260706-020927` |
| T17-003 | passed | 91 | 60 | claude-opus-4-8 | `BENCH-T17-003-20260706-022357` |
| T17-004 | passed | 94 | 60 | claude-opus-4-8 | `BENCH-T17-004-20260706-022955` |
| T17-005 | passed | 94 | 60 | claude-opus-4-8 | `BENCH-T17-005-20260706-043249` |
| T17-006 | passed | 97 | 60 | claude-opus-4-8 | `BENCH-T17-006-20260706-043249` |
| T17-007 | passed | 90 | 60 | unrecorded | `BENCH-T17-007-20260225-081613` |
| T17-008 | failed | 27 | 60 | claude-opus-4-8 | `BENCH-T17-008-20260706-050740` |

### Tier 18 — 3/4 passed

| Task | Status | Score | Threshold | Model | Run dir |
|------|--------|------:|----------:|-------|---------|
| T18-001 | passed | 93 | 60 | claude-opus-4-8 | `BENCH-T18-001-20260705-232619` |
| T18-002 | passed | 96 | 60 | claude-opus-4-8 | `BENCH-T18-002-20260705-232918` |
| T18-003 | passed | 95 | 60 | claude-opus-4-8 | `BENCH-T18-003-20260705-232939` |
| T18-004 | failed | 0 | 60 | claude-opus-4-8 | `BENCH-T18-004-20260705-233245` |

## Divergences vs human dashboard

59 row(s) where `CURRENT_STATUS.md` disagrees with the artifacts (artifact is authoritative for what RAN; the dashboard row may predate the fresh run):

| Task | Disagreement | Artifact |
|------|--------------|----------|
| T7-002 | score: dashboard 67 vs artifact 90 | `BENCH-T7-002-20260706-023740` |
| T7-003 | score: dashboard 55 vs artifact 61 | `BENCH-T7-003-20260706-024026` |
| T8-001 | score: dashboard 89 vs artifact 97 | `BENCH-T8-001-20260706-024402` |
| T8-002 | score: dashboard 78 vs artifact 96 | `BENCH-T8-002-20260706-025614` |
| T8-003 | score: dashboard 85 vs artifact 94 | `BENCH-T8-003-20260706-030231` |
| T8-004 | score: dashboard 68 vs artifact 95 | `BENCH-T8-004-20260706-031057` |
| T8-005 | score: dashboard 72 vs artifact 43; outcome: dashboard ✅ vs artifact failed | `BENCH-T8-005-20260706-031210` |
| T8-007 | score: dashboard 95 vs artifact 94 | `BENCH-T8-007-20260706-032203` |
| T9-002 | score: dashboard 74 vs artifact 76 | `BENCH-T9-002-20260706-033747` |
| T9-004 | score: dashboard 8 vs artifact 89; outcome: dashboard ❌ vs artifact passed | `BENCH-T9-004-20260706-041548` |
| T9-005 | score: dashboard 78 vs artifact 94 | `BENCH-T9-005-20260706-041706` |
| T10-002 | score: dashboard 17 vs artifact 44; outcome: dashboard ❌ vs artifact passed | `BENCH-T10-002-20260705-215602` |
| T10-003 | score: dashboard 88 vs artifact 92 | `BENCH-T10-003-20260705-225708` |
| T10-004 | score: dashboard 83 vs artifact 94 | `BENCH-T10-004-20260705-215602` |
| T12-001 | score: dashboard 78 vs artifact 75 | `BENCH-T12-001-20260705-215602` |
| T12-002 | score: dashboard 68 vs artifact 72 | `BENCH-T12-002-20260705-215602` |
| T12-003 | score: dashboard 75 vs artifact 94 | `BENCH-T12-003-20260705-225709` |
| T13-001 | score: dashboard 85 vs artifact 94 | `BENCH-T13-001-20260705-202952` |
| T13-002 | score: dashboard 78 vs artifact 94 | `BENCH-T13-002-20260705-203015` |
| T13-003 | score: dashboard 92 vs artifact 96 | `BENCH-T13-003-20260705-221950` |
| T13-004 | score: dashboard 88 vs artifact 93 | `BENCH-T13-004-20260705-203056` |
| T13-005 | score: dashboard 76 vs artifact 96 | `BENCH-T13-005-20260705-203209` |
| T13-006 | score: dashboard 72 vs artifact 94 | `BENCH-T13-006-20260705-221953` |
| T13-007 | score: dashboard 94 vs artifact 96 | `BENCH-T13-007-20260705-203509` |
| T13-008 | score: dashboard 82 vs artifact 96 | `BENCH-T13-008-20260705-203551` |
| T14-001 | score: dashboard 92 vs artifact 94 | `BENCH-T14-001-20260705-221034` |
| T14-002 | score: dashboard 88 vs artifact 94 | `BENCH-T14-002-20260705-221624` |
| T14-003 | score: dashboard 85 vs artifact 90 | `BENCH-T14-003-20260705-222113` |
| T14-004 | score: dashboard 78 vs artifact 94 | `BENCH-T14-004-20260705-222654` |
| T14-005 | score: dashboard 82 vs artifact 70 | `BENCH-T14-005-20260705-225709` |
| T15-001 | score: dashboard 88 vs artifact 64 | `BENCH-T15-001-20260705-203739` |
| T15-003 | score: dashboard 68 vs artifact 8; outcome: dashboard ✅ vs artifact failed | `BENCH-T15-003-20260705-221955` |
| T15-004 | score: dashboard 68 vs artifact 93 | `BENCH-T15-004-20260705-203917` |
| T15-005 | score: dashboard 85 vs artifact 91 | `BENCH-T15-005-20260705-203948` |
| T15-006 | score: dashboard 64 vs artifact 91 | `BENCH-T15-006-20260705-204126` |
| T15-007 | score: dashboard 78 vs artifact 95 | `BENCH-T15-007-20260705-213048` |
| T15-008 | score: dashboard 76 vs artifact 93 | `BENCH-T15-008-20260705-204800` |
| T15-009 | score: dashboard 82 vs artifact 93 | `BENCH-T15-009-20260705-204933` |
| T15-010 | score: dashboard 85 vs artifact 97 | `BENCH-T15-010-20260705-205009` |
| T15-011 | score: dashboard 100 vs artifact 97 | `BENCH-T15-011-20260705-205237` |
| T15-012 | score: dashboard 92 vs artifact 97 | `BENCH-T15-012-20260705-205404` |
| T15-013 | score: dashboard 93 vs artifact 95 | `BENCH-T15-013-20260705-205559` |
| T15-014 | score: dashboard 72 vs artifact 88 | `BENCH-T15-014-20260705-205750` |
| T16-001 | score: dashboard 88 vs artifact 94 | `BENCH-T16-001-20260705-223139` |
| T16-002 | score: dashboard 85 vs artifact 96 | `BENCH-T16-002-20260705-223614` |
| T16-003 | score: dashboard 95 vs artifact 96 | `BENCH-T16-003-20260705-223930` |
| T16-004 | score: dashboard 82 vs artifact 80 | `BENCH-T16-004-20260705-224130` |
| T16-005 | score: dashboard 78 vs artifact 95 | `BENCH-T16-005-20260705-225709` |
| T16-006 | score: dashboard 76 vs artifact 97 | `BENCH-T16-006-20260705-225709` |
| T16-007 | score: dashboard 88 vs artifact 93 | `BENCH-T16-007-20260705-230811` |
| T16-008 | score: dashboard 92 vs artifact 87 | `BENCH-T16-008-20260705-230826` |
| T16-009 | score: dashboard 85 vs artifact 95 | `BENCH-T16-009-20260705-231443` |
| T16-010 | score: dashboard 78 vs artifact 97 | `BENCH-T16-010-20260705-231806` |
| T16-011 | score: dashboard 82 vs artifact 96 | `BENCH-T16-011-20260705-231900` |
| T16-012 | score: dashboard 88 vs artifact 93 | `BENCH-T16-012-20260706-044412` |
| T16-013 | score: dashboard 95 vs artifact 99 | `BENCH-T16-013-20260705-232325` |
| T16-014 | score: dashboard 93 vs artifact 98 | `BENCH-T16-014-20260705-232502` |
| T16-015 | score: dashboard 73 vs artifact 61; outcome: dashboard ✅ vs artifact failed | `BENCH-T16-015-20260705-232541` |
| T16-016 | score: dashboard 78 vs artifact 83 | `BENCH-T16-016-20260705-232615` |

