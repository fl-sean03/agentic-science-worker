# Benchmark Results Cleanup Analysis

**Generated:** 2026-02-24
**Analysis Path:** `/home/sf2/LabWork/Workspace/29-AgenticScienceWorker/1-ScienceAgent/benchmarks/results/runs/`

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Disk Usage | 3.14 GB (3,219 MB) |
| Total Runs | 211 |
| Unique Benchmarks | 96 |
| Runs to Keep | 109 (1,676 MB / 52.1%) |
| Runs to Archive | 102 (1,543 MB / 47.9%) |
| **Potential Savings** | **1.5 GB** |

---

## Methodology

For each benchmark, we recommend keeping:
1. **Best Score Run** - The run with the highest score for that benchmark
2. **Most Recent Run** - The most recent run (even if score is lower)

All other runs are candidates for archival.

---

## Analysis by Tier

### Tier 1 (Basic LAMMPS)
| Benchmark | Total Runs | Best Score | Best Run | Size (MB) |
|-----------|------------|------------|----------|-----------|
| BENCH-T1-001 | 10 | 98 | BENCH-T1-001-20260216-180309 | 0.13 |
| BENCH-T1-002 | 6 | 97 | BENCH-T1-002-20260117-081354 | 0.09 |
| BENCH-T1-003 | 5 | 88 | BENCH-T1-003-20260117-231005 | 0.06 |
| BENCH-T1-004 | 5 | 97 | BENCH-T1-004-20260117-082455 | 0.07 |
| BENCH-T1-005 | 5 | 91 | BENCH-T1-005-20260117-231708 | 0.07 |
| BENCH-T1-006 | 5 | 100 | BENCH-T1-006-20260117-072923 | 0.07 |
| BENCH-T1-007 | 1 | 94 | BENCH-T1-007-20260117-232642 | 0.01 |

### Tier 2 (Intermediate LAMMPS)
| Benchmark | Total Runs | Best Score | Best Run | Size (MB) |
|-----------|------------|------------|----------|-----------|
| BENCH-T2-001 | 3 | 95 | BENCH-T2-001-20260117-093041 | 0.05 |
| BENCH-T2-002 | 3 | 91 | BENCH-T2-002-20260117-093538 | 0.08 |
| BENCH-T2-003 | 3 | 92 | BENCH-T2-003-20260117-234724 | 0.05 |
| BENCH-T2-004 | 1 | 93 | BENCH-T2-004-20260118-001315 | 0.02 |

### Tier 3 (Advanced LAMMPS)
| Benchmark | Total Runs | Best Score | Best Run | Size (MB) |
|-----------|------------|------------|----------|-----------|
| BENCH-T3-001 | 3 | 87 | BENCH-T3-001-20260118-002050 | 0.06 |
| BENCH-T3-002 | 3 | 88 | BENCH-T3-002-20260117-102131 | 0.06 |
| BENCH-T3-003 | 1 | 95 | BENCH-T3-003-20260118-004554 | 0.02 |

### Tier 4 (Multi-step LAMMPS)
| Benchmark | Total Runs | Best Score | Best Run | Size (MB) |
|-----------|------------|------------|----------|-----------|
| BENCH-T4-001 | 3 | 93 | BENCH-T4-001-20260118-005953 | 0.06 |
| BENCH-T4-002 | 3 | 93 | BENCH-T4-002-20260118-010715 | 0.06 |
| BENCH-T4-003 | 3 | 88 | BENCH-T4-003-20260117-113410 | 0.07 |
| BENCH-T4-004 | 3 | 88 | BENCH-T4-004-20260118-021821 | 0.06 |
| BENCH-T4-005 | 3 | 82 | BENCH-T4-005-20260117-114910 | 0.06 |
| BENCH-T4-006 | 3 | 82 | BENCH-T4-006-20260117-115715 | 0.06 |
| BENCH-T4-007 | 1 | 94 | BENCH-T4-007-20260118-024244 | 0.02 |

### Tier 5-9 (QE and Mixed)
| Benchmark | Total Runs | Best Score | Size (MB) |
|-----------|------------|------------|-----------|
| BENCH-T5-001 | 1 | 94 | 0.01 |
| BENCH-T5-002 | 1 | 88 | 0.02 |
| BENCH-T5-003 | 1 | 90 | 0.02 |
| BENCH-T5-004 | 1 | 88 | 0.02 |
| BENCH-T5-005 | 2 | 96 | 0.03 |
| BENCH-T5-006 | 4 | 95 | 0.06 |
| BENCH-T5-007 | 1 | 81 | 0.02 |
| BENCH-T6-001 | 1 | 68 | 0.02 |
| BENCH-T6-002 | 1 | 75 | 0.02 |
| BENCH-T6-003 | 3 | 86 | 0.17 |
| BENCH-T6-004 | 2 | 75 | 0.04 |
| BENCH-T6-005 | 1 | 81 | 0.02 |
| BENCH-T7-001 | 2 | N/A | 0.14 |
| BENCH-T7-002 | 2 | 85 | 0.04 |
| BENCH-T8-001 | 1 | 91 | 0.02 |
| BENCH-T8-002 | 1 | 76 | 0.02 |
| BENCH-T8-003 | 1 | 91 | 0.02 |
| BENCH-T8-004 | 1 | 82 | 0.02 |
| BENCH-T8-005 | 2 | 92 | 0.03 |
| BENCH-T8-007 | 2 | 61 | 0.04 |
| BENCH-T9-003 | 4 | 62 | 10.54 |
| BENCH-T9-004 | 1 | 65 | 0.02 |
| BENCH-T9-005 | 1 | 82 | 0.02 |

### Tier 10 (Integration)
| Benchmark | Total Runs | Best Score | Size (MB) |
|-----------|------------|------------|-----------|
| BENCH-T10-001 | 1 | 75 | 0.03 |
| BENCH-T10-002 | 1 | 72 | 0.02 |
| BENCH-T10-003 | 1 | 78 | 0.02 |
| BENCH-T10-004 | 2 | 85 | 7.63 |

### Tier 13-14 (Literature/Advanced DFT)
| Benchmark | Total Runs | Best Score | Size (MB) |
|-----------|------------|------------|-----------|
| BENCH-T13-001 | 1 | 78 | 0.20 |
| BENCH-T13-002 | 4 | 62 | 206.72 |
| BENCH-T13-003 | 1 | 78 | 0.04 |
| BENCH-T13-004 | 1 | 72 | 2.15 |
| BENCH-T13-005 | 2 | 78 | 0.06 |
| BENCH-T13-006 | 1 | 67 | 0.10 |
| BENCH-T13-007 | 1 | 82 | 0.04 |
| BENCH-T13-008 | 1 | 88 | 0.04 |
| BENCH-T14-001 | 1 | 79 | 4.93 |
| BENCH-T14-002 | 2 | 68 | 0.08 |
| BENCH-T14-003 | 1 | 62 | 69.42 |
| BENCH-T14-004 | 1 | 72 | 0.05 |
| BENCH-T14-005 | 2 | 68 | 12.03 |

### Tier 15-16 (Complex Workflows - LARGEST DISK USAGE)
| Benchmark | Total Runs | Best Score | Size (MB) | Notes |
|-----------|------------|------------|-----------|-------|
| BENCH-T15-001 | 1 | 78 | 7.57 | |
| BENCH-T15-002 | 1 | 62 | 9.13 | |
| **BENCH-T15-003** | **12** | **78** | **1,228.60** | **Largest consumer** |
| BENCH-T15-004 | 11 | 68 | 10.03 | |
| BENCH-T15-005 | 1 | 79 | 0.03 | |
| **BENCH-T15-006** | **7** | **64** | **735.56** | **Second largest** |
| BENCH-T15-007 | 1 | 62 | 2.46 | |
| BENCH-T15-008 | 2 | 73 | 17.71 | |
| BENCH-T15-009 | 1 | 68 | 0.03 | |
| BENCH-T15-010 | 1 | 72 | 0.03 | |
| BENCH-T15-011 | 2 | 100 | 0.04 | |
| BENCH-T15-012 | 2 | 92 | 0.03 | |
| BENCH-T15-013 | 1 | 93 | 0.02 | |
| BENCH-T15-014 | 1 | 72 | 0.01 | |
| BENCH-T16-001 | 1 | 79 | 0.14 | |
| **BENCH-T16-002** | **2** | **91** | **554.96** | **Third largest** |
| BENCH-T16-003 | 1 | 68 | 0.03 | |
| BENCH-T16-004 | 2 | 78 | 8.37 | |
| BENCH-T16-005 | 2 | 88 | 66.34 | |
| BENCH-T16-006 | 2 | 75 | 30.67 | |
| BENCH-T16-007 | 1 | 92 | 0.75 | |
| **BENCH-T16-008** | **3** | **72** | **139.63** | |
| BENCH-T16-009 | 1 | 72 | 0.06 | |
| BENCH-T16-010 | 2 | 82 | 0.16 | |
| BENCH-T16-011 | 1 | 88 | 0.06 | |
| **BENCH-T16-012** | **3** | **72** | **85.18** | |
| BENCH-T16-013 | 1 | 95 | 0.01 | |
| BENCH-T16-014 | 1 | 93 | 0.01 | |
| BENCH-T16-015 | 2 | 73 | 0.02 | |
| BENCH-T16-016 | 2 | 78 | 0.03 | |

### Tier 17-18 (Latest)
| Benchmark | Total Runs | Best Score | Size (MB) |
|-----------|------------|------------|-----------|
| BENCH-T17-001 | 1 | 97 | 0.06 |
| BENCH-T17-002 | 2 | 98 | 0.03 |
| BENCH-T17-003 | 1 | 92 | 0.02 |
| BENCH-T18-001 | 1 | 92 | 0.30 |
| BENCH-T18-002 | 1 | 92 | 4.70 |

---

## Benchmarks with Most Runs (Cleanup Priority)

| Rank | Benchmark | Runs | Best Score | Archivable Runs | Archivable Size |
|------|-----------|------|------------|-----------------|-----------------|
| 1 | BENCH-T15-003 | 12 | 78 | 10 | 629 MB |
| 2 | BENCH-T15-004 | 11 | 68 | 10 | 8.7 MB |
| 3 | BENCH-T1-001 | 10 | 98 | 9 | 0.1 MB |
| 4 | BENCH-T15-006 | 7 | 64 | 6 | 518 MB |
| 5 | BENCH-T1-002 | 6 | 97 | 4 | 0.06 MB |
| 6 | BENCH-T1-003 | 5 | 88 | 4 | 0.05 MB |
| 7 | BENCH-T1-004 | 5 | 97 | 3 | 0.04 MB |
| 8 | BENCH-T1-005 | 5 | 91 | 4 | 0.06 MB |
| 9 | BENCH-T1-006 | 5 | 100 | 3 | 0.04 MB |
| 10 | BENCH-T13-002 | 4 | 62 | 3 | 190 MB |

---

## Runs by Date

| Date | Runs |
|------|------|
| 2026-01-17 | 61 |
| 2026-01-18 | 35 |
| 2026-01-19 | 7 |
| 2026-02-16 | 48 |
| 2026-02-17 | 27 |
| 2026-02-18 | 11 |
| 2026-02-19 | 10 |
| 2026-02-20 | 1 |
| 2026-02-23 | 11 |

---

## Top 10 Largest Archivable Runs

These runs contribute the most to disk usage and are safe to archive:

| Directory | Size (MB) | Score |
|-----------|-----------|-------|
| BENCH-T15-003-20260217-115302 | 383.67 | 28 |
| BENCH-T15-006-20260217-115303 | 284.51 | 32 |
| BENCH-T15-006-20260217-223746 | 230.60 | 54 |
| BENCH-T13-002-20260217-125212 | 190.43 | 52 |
| BENCH-T15-003-20260217-150156 | 146.45 | 45 |
| BENCH-T16-008-20260217-115316 | 121.02 | 54 |
| BENCH-T15-003-20260218-195907 | 72.33 | 8 |
| BENCH-T16-012-20260217-115317 | 41.77 | 0 |
| BENCH-T15-003-20260218-222754 | 23.93 | 52 |
| BENCH-T16-002-20260216-192742 | 12.67 | 42 |

**Archiving just these 10 runs would save 1,507 MB (1.47 GB)**

---

## Recommended Actions

### 1. High Priority - Archive Large Failed/Low-Score Runs

Archive these directories first (over 100 MB each, low scores):

```bash
# Create archive directory
mkdir -p /home/sf2/LabWork/Workspace/29-AgenticScienceWorker/1-ScienceAgent/benchmarks/results/archive/

# Archive large low-scoring runs
cd /home/sf2/LabWork/Workspace/29-AgenticScienceWorker/1-ScienceAgent/benchmarks/results/runs/

# Compress and move (example for top 3)
tar -czf ../archive/BENCH-T15-003-20260217-115302.tar.gz BENCH-T15-003-20260217-115302 && rm -rf BENCH-T15-003-20260217-115302
tar -czf ../archive/BENCH-T15-006-20260217-115303.tar.gz BENCH-T15-006-20260217-115303 && rm -rf BENCH-T15-006-20260217-115303
tar -czf ../archive/BENCH-T15-006-20260217-223746.tar.gz BENCH-T15-006-20260217-223746 && rm -rf BENCH-T15-006-20260217-223746
```

### 2. Medium Priority - Archive All Non-Best Runs

Full list of 102 directories recommended for archival (sorted by size, descending):

```
BENCH-T15-003-20260217-115302 (383.67 MB, score=28)
BENCH-T15-006-20260217-115303 (284.51 MB, score=32)
BENCH-T15-006-20260217-223746 (230.60 MB, score=54)
BENCH-T13-002-20260217-125212 (190.43 MB, score=52)
BENCH-T15-003-20260217-150156 (146.45 MB, score=45)
BENCH-T16-008-20260217-115316 (121.02 MB, score=54)
BENCH-T15-003-20260218-195907 (72.33 MB, score=8)
BENCH-T16-012-20260217-115317 (41.77 MB, score=0)
BENCH-T15-003-20260218-222754 (23.93 MB, score=52)
BENCH-T16-002-20260216-192742 (12.67 MB, score=42)
BENCH-T16-006-20260216-192749 (11.39 MB, score=15)
BENCH-T15-003-20260218-195123 (2.52 MB, score=3)
BENCH-T15-006-20260217-150156 (2.37 MB, score=2)
BENCH-T9-003-20260219-231712 (2.30 MB, score=N/A)
BENCH-T15-004-20260219-141526 (1.72 MB, score=42)
BENCH-T16-005-20260216-192748 (1.62 MB, score=18)
BENCH-T16-012-20260216-192804 (1.61 MB, score=2)
BENCH-T10-004-20260223-003205 (1.50 MB, score=8)
BENCH-T9-003-20260219-151249 (1.29 MB, score=48)
BENCH-T15-004-20260217-125214 (1.20 MB, score=42)
BENCH-T15-004-20260217-150156 (0.98 MB, score=32)
BENCH-T15-004-20260217-223746 (0.92 MB, score=32)
BENCH-T15-004-20260219-142809 (0.80 MB, score=5)
BENCH-T15-004-20260219-222128 (0.80 MB, score=2)
BENCH-T15-008-20260216-192733 (0.80 MB, score=32)
BENCH-T15-004-20260219-221805 (0.80 MB, score=3)
BENCH-T15-004-20260216-192729 (0.77 MB, score=2)
BENCH-T15-004-20260218-193634 (0.70 MB, score=3)
```

(Plus 74 more small runs <0.1 MB each)

### 3. Directories to KEEP (109 total)

These are the best-score and most-recent runs that should be preserved:

```
BENCH-T1-001-20260216-180309 (best score: 98)
BENCH-T1-002-20260117-081354 (best score: 97)
BENCH-T1-002-20260117-230631 (most recent)
BENCH-T1-003-20260117-231005 (best score: 88)
BENCH-T1-004-20260117-082455 (best score: 97)
BENCH-T1-004-20260117-231358 (most recent)
BENCH-T1-005-20260117-231708 (best score: 91)
BENCH-T1-006-20260117-072923 (best score: 100)
BENCH-T1-006-20260117-232105 (most recent)
BENCH-T1-007-20260117-232642 (best score: 94)
BENCH-T15-003-20260218-213714 (best score: 78)
BENCH-T15-003-20260218-234346 (most recent)
BENCH-T15-006-20260218-221458 (best score: 64)
BENCH-T16-002-20260217-115305 (best score: 91)
... (95 more)
```

---

## Bulk Archive Script

To archive all recommended runs at once:

```bash
#!/bin/bash
RUNS_DIR="/home/sf2/LabWork/Workspace/29-AgenticScienceWorker/1-ScienceAgent/benchmarks/results/runs"
ARCHIVE_DIR="/home/sf2/LabWork/Workspace/29-AgenticScienceWorker/1-ScienceAgent/benchmarks/results/archive"

mkdir -p "$ARCHIVE_DIR"

# List of directories to archive (102 total)
ARCHIVE_LIST=(
"BENCH-T15-003-20260217-115302"
"BENCH-T15-006-20260217-115303"
"BENCH-T15-006-20260217-223746"
"BENCH-T13-002-20260217-125212"
"BENCH-T15-003-20260217-150156"
"BENCH-T16-008-20260217-115316"
"BENCH-T15-003-20260218-195907"
"BENCH-T16-012-20260217-115317"
"BENCH-T15-003-20260218-222754"
"BENCH-T16-002-20260216-192742"
"BENCH-T16-006-20260216-192749"
"BENCH-T15-003-20260218-195123"
"BENCH-T15-006-20260217-150156"
"BENCH-T9-003-20260219-231712"
"BENCH-T15-004-20260219-141526"
"BENCH-T16-005-20260216-192748"
"BENCH-T16-012-20260216-192804"
"BENCH-T10-004-20260223-003205"
"BENCH-T9-003-20260219-151249"
"BENCH-T15-004-20260217-125214"
"BENCH-T15-004-20260217-150156"
"BENCH-T15-004-20260217-223746"
"BENCH-T15-004-20260219-142809"
"BENCH-T15-004-20260219-222128"
"BENCH-T15-008-20260216-192733"
"BENCH-T15-004-20260219-221805"
"BENCH-T15-004-20260216-192729"
"BENCH-T15-004-20260218-193634"
"BENCH-T7-001-20260219-105156"
"BENCH-T15-006-20260217-125215"
"BENCH-T16-010-20260216-192801"
"BENCH-T15-003-20260218-234114"
"BENCH-T15-004-20260218-221457"
"BENCH-T16-004-20260216-192745"
"BENCH-T14-002-20260216-184223"
"BENCH-T13-002-20260217-150156"
"BENCH-T2-002-20260117-003453"
"BENCH-T15-006-20260218-193641"
"BENCH-T13-005-20260216-184746"
"BENCH-T13-002-20260216-184221"
"BENCH-T15-003-20260217-125214"
"BENCH-T15-003-20260217-223746"
"BENCH-T3-001-20260117-101100"
"BENCH-T4-001-20260117-103126"
"BENCH-T15-003-20260218-193628"
"BENCH-T8-007-20260118-163757"
"BENCH-T4-002-20260117-104054"
"BENCH-T4-004-20260117-114117"
"BENCH-T15-006-20260216-192731"
"BENCH-T7-002-20260119-091802"
"BENCH-T4-003-20260117-021843"
"BENCH-T4-001-20260117-010840"
"BENCH-T2-003-20260117-094307"
"BENCH-T4-006-20260117-024112"
"BENCH-T4-004-20260117-022601"
"BENCH-T4-005-20260117-023422"
"BENCH-T1-005-20260117-082853"
"BENCH-T5-005-20260118-125424"
"BENCH-T14-005-20260216-192720"
"BENCH-T4-002-20260117-012218"
"BENCH-T1-003-20260117-082123"
"BENCH-T1-006-20260117-083247"
"BENCH-T1-002-20260117-081838"
"BENCH-T3-001-20260117-010414"
"BENCH-T1-005-20260117-072527"
"BENCH-T1-002-20260117-071729"
"BENCH-T1-002-20260117-070050"
"BENCH-T5-006-20260118-124504"
"BENCH-T2-003-20260117-004128"
"BENCH-T1-001-20260117-230427"
"BENCH-T1-006-20260117-071145"
"BENCH-T6-003-20260119-080501"
"BENCH-T3-002-20260117-010735"
"BENCH-T2-001-20260117-002954"
"BENCH-T5-006-20260118-124033"
"BENCH-T6-004-20260119-082128"
"BENCH-T1-005-20260117-070953"
"BENCH-T15-012-20260216-093829"
"BENCH-T1-001-20260117-065927"
"BENCH-T1-001-20260117-230126"
"BENCH-T1-001-20260117-071613"
"BENCH-T1-004-20260117-070542"
"BENCH-T1-001-20260117-081659"
"BENCH-T5-006-20260118-123329"
"BENCH-T1-004-20260117-072206"
"BENCH-T16-016-20260216-094532"
"BENCH-T6-003-20260118-194950"
"BENCH-T1-002-20260117-001526"
"BENCH-T8-005-20260118-143540"
"BENCH-T16-008-20260216-192759"
"BENCH-T1-003-20260117-070248"
"BENCH-T15-003-20260216-192722"
"BENCH-T1-004-20260117-002042"
"BENCH-T1-003-20260117-071955"
"BENCH-T1-001-20260117-001235"
"BENCH-T1-005-20260117-002357"
"BENCH-T1-006-20260117-002752"
"BENCH-T1-001-20260117-001420"
"BENCH-T16-015-20260216-095118"
"BENCH-T1-003-20260117-001758"
"BENCH-T1-001-20260117-001212"
"BENCH-T1-001-20260117-001143"
)

echo "Archiving ${#ARCHIVE_LIST[@]} directories..."

for dir in "${ARCHIVE_LIST[@]}"; do
    if [ -d "$RUNS_DIR/$dir" ]; then
        echo "Archiving: $dir"
        tar -czf "$ARCHIVE_DIR/$dir.tar.gz" -C "$RUNS_DIR" "$dir"
        # Uncomment to actually remove after archiving:
        # rm -rf "$RUNS_DIR/$dir"
    fi
done

echo "Done. Check $ARCHIVE_DIR for archived runs."
```

---

## Summary

- **Current Usage:** 3.14 GB across 211 runs
- **After Cleanup:** ~1.68 GB across 109 runs
- **Space Saved:** ~1.5 GB (47.9%)

The primary disk consumers are Tier 15-16 benchmarks (complex DFT/workflow tests) where each run can generate hundreds of MB of output files. Focusing cleanup on these tiers will yield the greatest space savings.
