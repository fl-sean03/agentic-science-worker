# P-04 — `.claude/agents/simulation-runner.md`: binary path fixes (Track B-1/B-2)

**Status:** APPROVED+APPLIED 2026-07-03 (owner sign-off: 2026-07-03 "apply the full fix" directive) · **Author model:** claude-fable-5 · **Date:** 2026-07-02
**Target:** `.claude/agents/simulation-runner.md` (tracked; a live-session
subagent definition → operating surface).

## Exact diff

```diff
@@ -23,9 +23,9 @@
 
 ## Binary Paths
 
-- LAMMPS: `/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/md-lammps/install/bin/lmp`
-- QE CPU: `/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-cpu/bin/pw.x`
-- QE GPU: `/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-gpu/bin/pw.x`
+- LAMMPS: `$LMP` (see `.claude/settings.json`; working build 2026-07-02: `/home/sf2/builds/lammps/build/lmp`)
+- QE CPU: `/home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/build-cpu/bin/pw.x` (present; NOT runnable as of 2026-07-02 — MPI runtime rot, see `harness.py --verify`)
+- QE GPU: `/home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/build-gpu/bin/pw.x` (same caveat)
```

## Why / expected effect
The subagent currently instructs simulation runs against nonexistent binaries;
after the fix it points at env-truth and carries the honest runnability caveat.

## Eval plan
Spawn the subagent on a trivial LAMMPS task; it must use the working binary and
flag QE as unavailable rather than failing blind. Revert = git revert.

## APPROVAL
- [x] APPROVED 2026-07-03 — owner directive "apply the full fix" (fleet refresh close-out); applied by Fable 5 finalizer.
