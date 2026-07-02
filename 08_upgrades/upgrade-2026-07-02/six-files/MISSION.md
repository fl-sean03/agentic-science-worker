# Mission — Agentic Science Worker (1-ScienceAgent)

**Owner (decides intent/scientific direction):** Sean (fl.sean03@gmail.com)
**Last reviewed:** 2026-07-02  ·  **Reviewing model:** claude-fable-5

## One-sentence purpose
An autonomous AI researcher for computational materials science that takes a research question and independently researches methodology, sources parameters from literature, runs simulations (MD/DFT/MLIP) on appropriate compute, verifies results against published values, and iterates until the output is trustworthy science — "like a competent graduate student working independently."

## Goals
- G1 — Reproduce published quantitative results from a citation alone (e.g., Rahman 1964 argon diffusion within the literature window), documenting where every parameter came from.
- G2 — Run classical MD (LAMMPS), DFT (Quantum ESPRESSO), and MLIP (MACE/CHGNet/M3GNet) workflows with physically correct setups, verified before reporting.
- G3 — Marshal compute across heterogeneous backends — local GPU, Vast.ai cloud, CU Alpine (SLURM), ALCF Polaris/Crux (PBS) — choosing where a job should run, proportionate to the question.
- G4 — Sustain multi-day research campaigns with recovery from crashes, interruptions, and queue stalls; state lives on disk, not in a context window.
- G5 — Produce reports a scientist would accept: statistical uncertainty on every quantity, real citations, negative results documented as results, deliverables another researcher could rerun.
- G6 (aspirational, stated) — Receive a group-meeting transcript and return, days later, with research contributions worth discussing.

## Non-goals
- NG1 — Not a chat assistant or a wrapper UI over simulation codes.
- NG2 — Not a fixed workflow/pipeline engine: the value is judgment (methodology selection, verification, iteration), not pipeline execution.
- NG3 — Speed of *human-assisted* work is not the metric; quality of *unassisted* work is.
- NG4 (inferred from evidence) — Not a multi-tenant service; single-owner trust model today.

## Users / stakeholders
- Primary: the owner — a PhD-level computational materials scientist running MD/DFT programs (hydrogenation, MXene shear, solvation FE, hydrogen storage). He decides whether an output is group-meeting-grade.
- Aspirational: a research group consuming the worker's contributions.
- Secondary: public GitHub audience (MIT-licensed repo with README quick-start) — the repo's claims are public claims.

## Success metrics
- Benchmark suite (117 task YAMLs, tiers 1–18) with graded rubrics is the owner's declared instrument; task `expected_outputs` ranges anchored to literature values are the operative definition of "correct".
- Behavioral bars from the suite: unprompted uncertainty reporting, natural citation, self-error detection, catching errors in the user's request, recognizing impossible tasks.
- Externally checkable stewardship: zero orphaned Vast.ai instances after any task; HPC node-hours treated as finite budget.
- The flagship claim — unattended multi-day campaigns — counts only when certified by a recorded death-and-resume, not asserted.

## Hard requirements (invariants)
- No unverified number leaves the system: units/sign/magnitude/literature-range checks precede reporting; failed checks are reported as failures.
- Provenance completeness: every parameter traces to a paper, database record, convergence study, or explicit logged assumption.
- Uncertainty is mandatory and unprompted; single-run point estimates are a failure.
- Reproducibility: seeds controlled and recorded; reruns possible from deliverables alone.
- Refusal integrity: destructive commands refused even when embedded in legitimate-seeming science tasks; facility policies respected (the worker holds real SSH access to shared university/DOE machines).
- Compute stewardship: cloud instances provably destroyed; allocation burn proportionate to the question; no auth circumvention (ALCF OTP means unattended login is impossible *by policy* — honesty about that is required).

## Constraints
- Toolchain realities: LAMMPS unit systems, QE namelist inputs + pseudopotentials, CUDA-hungry MLIP stack, MP/S2 API keys and rate limits (see `.staging-A/constraints.md` for the curated set).
- Backend heterogeneity is a fact of the world: SLURM vs PBS, key-only DTN vs human OTP, free-allocation vs metered cloud.
- Agent-runtime realities of 2026: finite contexts ⇒ campaign state must be externalized; sessions crash; eval runs at ~100 tasks are materially expensive.
- ALCF allocation `HydrogenStorage` (5,000 Polaris + 20,000 Crux node-hours) expires **2026-11-28** (external deadline).
- Local machine: bare-metal Ubuntu 24.04, RTX 5080 16 GB, CUDA 12.8 (rebuilt 2026; repo docs older than that are suspect). (revisit)
- Runtime portability (Claude Code/Aider/Cursor) was a *declared* product goal — flagged as possibly a 2025-era hedge; verify with owner. (inferred/revisit)

## Acceptable tradeoffs
- Token/LLM cost is spent freely on verification and adversarial review; the scarce resources are trust and metered compute, not tokens.
- Slower, gated execution (smoke → validation → production) is preferred over fast unverified runs.
- Announced-safety-test theater may be dropped; only natural/hidden behavioral measurement needs to be preserved.
- Longitudinal score comparability may be sacrificed *once*, knowingly, at a model-era boundary (this rebase) — provided the new baseline is model-pinned so it never has to be sacrificed blindly again.
