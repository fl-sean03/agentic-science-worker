# P-06 — `AGENTS.md`: minimal factual skills-table refresh (Track B-1)

**Status:** PROPOSED · **Author model:** claude-fable-5 · **Date:** 2026-07-02
**Target:** `AGENTS.md` (tracked; THE primary live operating surface).

## Scope discipline (why this is so small)

This proposal is **factual repair only**: the skills table (AGENTS.md "Skills"
section) lists the archived `hpc-cluster` and omits six on-disk skills. It does
NOT touch persona, principles, counters, tone, or length — the behavioral
rewrite question is explicitly out of scope (U-R5 rejected; D2 ablation must
come first; see `docs/rebase/DECISIONS.md` ADR-105 and the E-06 gate story).

## Exact diff

```diff
@@ ## Skills table @@
 | Skill | Description |
 |-------|-------------|
 | `lammps-simulation` | Molecular dynamics with LAMMPS |
 | `quantum-espresso` | DFT calculations with QE |
-| `hpc-cluster` | Remote HPC execution via SSH/SLURM |
 | `vast-cloud` | On-demand GPU cloud (VAST AI) - no queues, pay per hour |
 | `literature-search` | Finding papers and extracting parameters |
 | `materials-database` | Querying Materials Project |
 | `mlip-simulation` | ML interatomic potentials |
 | `data-analysis` | Processing and visualizing results |
 | `theory-synthesis` | Literature-driven hypothesis generation (Theorizer) |
 | `ggen` | Crystal structure generation |
 | `torch-sim` | High-throughput MLIP simulations |
+| `resource-acquisition` | Sourcing potentials/pseudopotentials/structures |
+| `iff-parameters` | IFF force-field database access (search/export/compose) |
+| `compute-strategy` | Cross-backend job routing (local / Vast.ai / Alpine / ALCF) |
+| `compute-validation` | Verify-before-compute gates (physics + smoke + orchestration safety) |
+| `campaign-orchestration` | Durable WORKFLOW.md state + stateless tick agents for long campaigns |
+| `project-update` | Tier-1 in-repo update engine (hosted here for use in other repos) |
+
+Archived: `skills/archive/hpc-cluster-curc/` (CURC-era HPC skill, retired
+2026-02-20; Alpine/ALCF access now lives in `compute-strategy` backends).
```

## Expected effect
A booting agent sees the true skill inventory (16 live + archive) instead of the
February one; zero behavioral-instruction change.

## Eval plan
Fresh session: "list your available skills and what each is for" must match
`ls skills/` exactly. Behavioral tiers (T13/T15/T16) spot-run before/after if
the owner wants belt-and-suspenders (table content is not behavioral
instruction, so A/B is optional here). Revert = git revert.

## APPROVAL
- [ ] APPROVED ____________ (date / initials)   ·   [ ] REJECTED: ____________
