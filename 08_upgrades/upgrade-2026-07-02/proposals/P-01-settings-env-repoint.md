# P-01 — `.claude/settings.json`: repoint binary env vars (Track B-2)

**Status:** PROPOSED · **Author model:** claude-fable-5 · **Date:** 2026-07-02
**Target:** `.claude/settings.json` (UNTRACKED; contains the owner's MP API key —
this proposal shows only the path lines; the key lines are untouched and never
reproduced anywhere).

## Why
Every binary env var points at `/home/sf2/Workspace/main/39-GPUTests/...`, which
has not existed since the 2026-06-13 reorg. The live session inherits dead
`$LMP`/`$QE_CPU`/`$QE_GPU` and a dead Bash-permission path.

## Exact diff (path lines only; JSON keys/order preserved)

```diff
--- .claude/settings.json (current)
+++ .claude/settings.json (proposed)
@@ permissions.allow @@
-      "Bash(/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/*)",
+      "Bash(/home/sf2/work/compute/gpu-tests/1-GPUTests/*)",
+      "Bash(/home/sf2/builds/lammps/build/lmp*)",
@@ env @@
-    "LMP": "/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/md-lammps/install/bin/lmp",
-    "QE_CPU": "/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-cpu/bin",
-    "QE_GPU": "/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-gpu/bin",
-    "GPUTESTS_REPO": "/home/sf2/Workspace/main/39-GPUTests/1-GPUTests",
+    "LMP": "/home/sf2/builds/lammps/build/lmp",
+    "QE_CPU": "/home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/build-cpu/bin",
+    "QE_GPU": "/home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/build-gpu/bin",
+    "GPUTESTS_REPO": "/home/sf2/work/compute/gpu-tests/1-GPUTests",
```

**LMP choice, honestly:** the gpu-tests `lmp` exists at
`/home/sf2/work/compute/gpu-tests/1-GPUTests/md-lammps/install/bin/lmp` but
**does not run** (needs `libmpi.so.40`; hangs under the current `~/hpc-sdk`
hpcx env — probe evidence 2026-07-02, A-04 refuted). `/home/sf2/builds/lammps/build/lmp`
(22Jul2025-U4) executes and passed a smoke run. Proposed: point `LMP` at the
working binary now; repoint to gpu-tests after its toolchain repair if desired.
QE vars: both builds are currently non-runnable for the same reason — the paths
above are the correct on-disk locations, and `harness.py --verify` will report
their true state either way.

## Expected effect
Live sessions and hooks see truthful env; local LAMMPS work becomes possible in
interactive mode; no behavioral/prompt change.

## Eval plan
`python benchmarks/evaluation/harness.py --verify` (LAMMPS probe = EXECUTES) and
one interactive `$LMP -h` in a fresh session. Revert = restore the four prior
values (recorded in `baseline/hash_manifest.sha256`-covered snapshot of the file
hash; the old values are quoted in this diff).

## APPROVAL
- [ ] APPROVED ____________ (date / initials)   ·   [ ] REJECTED: ____________
