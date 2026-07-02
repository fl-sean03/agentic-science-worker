# P-05 — skill pages: dead-path fixes (Track B-1)

**Status:** PROPOSED · **Author model:** claude-fable-5 · **Date:** 2026-07-02
**Targets (all tracked, all live operating surface — skills the live agent
executes from):** `skills/quantum-espresso/SKILL.md`,
`skills/compute-strategy/SKILL.md`,
`skills/compute-strategy/backends/polaris.md`,
`skills/compute-strategy/backends/crux.md`.

Mechanical substitutions only; every new target verified to exist on disk
(2026-07-02): gpu-tests tree, `~/work/compute/alcf/` hub (AGENTS.md +
docs/POLARIS_PLAYBOOK.md present), `~/work/research/hydrogenation/simulations/
surfaces/HPC_PLAYBOOK.md`. No prose/doctrine changes.

**Caveat carried, not hidden:** the QE binaries referenced by
`quantum-espresso/SKILL.md` are at the correct new location but are NOT
currently runnable (MPI runtime rot; A-04 refuted). If desired, an extra
caveat line can be added under "Local GPU-accelerated QE" — flagged here as an
owner option because it is a content (not path) edit.

## Exact diff — skills/quantum-espresso/SKILL.md

```diff
@@ -174,32 +174,32 @@
 **Local GPU-accelerated QE (RTX 5080):**
 ```
-QE_GPU="/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-gpu/bin"
+QE_GPU="/home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/build-gpu/bin"
-QE_CPU="/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-cpu/bin"
+QE_CPU="/home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/build-cpu/bin"
-QE_ENV="/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/env/setup_nvhpc.sh"
+QE_ENV="/home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/env/setup_nvhpc.sh"
@@ execution examples @@
-/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-cpu/bin/pw.x < input.in > output.out
+/home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/build-cpu/bin/pw.x < input.in > output.out
-mpirun -np 4 /home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-cpu/bin/pw.x < input.in > output.out
+mpirun -np 4 /home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/build-cpu/bin/pw.x < input.in > output.out
-source /home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/env/setup_nvhpc.sh
+source /home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/env/setup_nvhpc.sh
-/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-gpu/bin/pw.x < input.in > output.out
+/home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/build-gpu/bin/pw.x < input.in > output.out
@@ -207,8 +207,8 @@
-bash /home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/scripts/run_example01_cpu.sh
-bash /home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/scripts/run_example01_gpu.sh
+bash /home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/scripts/run_example01_cpu.sh
+bash /home/sf2/work/compute/gpu-tests/1-GPUTests/dft-qe/scripts/run_example01_gpu.sh
```

## Exact diff — skills/compute-strategy/SKILL.md

```diff
@@ -228,7 +228,7 @@
-A canonical example of the project-level layer (slab Thrust 4 in the Pt-NEC LOHC project): `~/LabWork/Workspace/31-Hydrogenation/simulations/surfaces/HPC_PLAYBOOK.md`.
+A canonical example of the project-level layer (slab Thrust 4 in the Pt-NEC LOHC project): `~/work/research/hydrogenation/simulations/surfaces/HPC_PLAYBOOK.md`.
```

## Exact diff — skills/compute-strategy/backends/polaris.md

```diff
@@ -174,4 +174,4 @@
-ALCF/Polaris is operated from a dedicated hub: **`~/LabWork/Workspace/35-ALCF/`**. The applied playbook is `35-ALCF/docs/POLARIS_PLAYBOOK.md` — bring-up checklist, stage tracking, NAMD launch examples, validation-gate artifacts, lessons learned; `35-ALCF/AGENTS.md` has hub boundaries; `35-ALCF/deploy/templates/` has PBS job templates. This page is the cross-project backend reference; the hub is where Polaris operational state lives. There is no CCM-style wrapper for Polaris yet — drive it through `ssh polaris` + PBS directly.
+ALCF/Polaris is operated from a dedicated hub: **`~/work/compute/alcf/`**. The applied playbook is `alcf/docs/POLARIS_PLAYBOOK.md` — bring-up checklist, stage tracking, NAMD launch examples, validation-gate artifacts, lessons learned; `alcf/AGENTS.md` has hub boundaries; `alcf/deploy/templates/` has PBS job templates. This page is the cross-project backend reference; the hub is where Polaris operational state lives. There is no CCM-style wrapper for Polaris yet — drive it through `ssh polaris` + PBS directly.
```

## Exact diff — skills/compute-strategy/backends/crux.md

```diff
@@ -137,4 +137,4 @@
-ALCF is operated from the hub at `~/LabWork/Workspace/35-ALCF/` — see `35-ALCF/AGENTS.md` and `STATUS.md` for the full multi-resource allocation. There is no CCM-style wrapper for Crux — drive it through `ssh crux` + PBS directly.
+ALCF is operated from the hub at `~/work/compute/alcf/` — see `alcf/AGENTS.md` and `STATUS.md` for the full multi-resource allocation. There is no CCM-style wrapper for Crux — drive it through `ssh crux` + PBS directly.
```

## Expected effect
Skill-driven sessions stop being routed to nonexistent trees; compute-strategy's
cross-project references resolve again.

## Eval plan
Fresh session invoking each skill must resolve every referenced path
(`test -e` per token — coldseed-lint-style). Revert = git revert.

## APPROVAL
- [ ] APPROVED ____________ (date / initials)   ·   [ ] REJECTED: ____________
