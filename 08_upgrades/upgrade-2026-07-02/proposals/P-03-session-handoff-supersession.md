# P-03 — `SESSION_HANDOFF.md`: supersession banner + dead-path fixes (Track B-1)

**Status:** APPROVED+APPLIED 2026-07-03 (owner sign-off: 2026-07-03 "apply the full fix" directive) · **Author model:** claude-fable-5 · **Date:** 2026-07-02
**Target:** `SESSION_HANDOFF.md` (tracked; on the new-session boot path — it
actively misdirects: dead `cd` path, "78/86 (100%)" claim, obsolete "don't run
T12" prohibition).

## Exact diff — part 1: banner (insert at very top, before line 1)

```diff
+> **SUPERSEDED (2026-07-02).** This handoff describes the February 2026 state and
+> pre-reorg paths. Current truth: `docs/rebase/CURRENT_STATE.md` (state),
+> `benchmarks/results/GENERATED_STATUS.md` (artifact-derived benchmark status),
+> `CLAUDE.md` (skill index). Kept verbatim below as a historical record.
+
 # Session Handoff - Agentic Science Worker
```

## Exact diff — part 2: path fixes (mechanical, verified targets exist)

```diff
@@ -9,7 +9,7 @@
 # Navigate to project
-cd /home/sf2/LabWork/Workspace/29-AgenticScienceWorker/1-ScienceAgent
+cd /home/sf2/work/agents/science-agent/1-ScienceAgent
@@ -153,8 +153,8 @@
-- **QE GPU:** `/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-gpu/bin/pw.x`
-- **QE CPU:** `/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-cpu/bin/pw.x`
+- **QE GPU:** `/home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/build-gpu/bin/pw.x`
+- **QE CPU:** `/home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/build-cpu/bin/pw.x`
@@ -183,7 +183,7 @@
-/home/sf2/LabWork/Workspace/29-AgenticScienceWorker/1-ScienceAgent/
+/home/sf2/work/agents/science-agent/1-ScienceAgent/
```

(Alternative considered: fix the stale status numbers inline — rejected; the
banner supersedes rather than rewrites history, and the numbers are the owner's
February prose.)

## Expected effect
A fresh session that opens the handoff is redirected to live truth instead of
February's; copy-paste commands stop failing.

## Eval plan
Fresh context asked "orient yourself in this project" must cite current paths
and the 80/97 artifact truth (E-01/E-02-style probe). Revert = git revert.

## APPROVAL
- [x] APPROVED 2026-07-03 — owner directive "apply the full fix" (fleet refresh close-out); applied by Fable 5 finalizer.
