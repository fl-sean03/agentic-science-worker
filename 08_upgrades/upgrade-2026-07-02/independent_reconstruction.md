# INDEPENDENT RECONSTRUCTION — Agentic Science Worker

**Author model ID: `claude-fable-5`**
Role: Greenfield Architect (Role 2, Stage A — deliberately blind), intelligence rebase 2026-07-02.

**Evidence base (exhaustive).** I read ONLY `08_upgrades/upgrade-2026-07-02/.staging-A/`:
`MISSION_EXTRACT.md`, `constraints.md`, `eval_seed.md`, `external_evidence/PROVENANCE.md`,
`external_evidence/hpc_resources.md`, `external_evidence/external_anchors.md`,
`external_evidence/reference_test_data/` (generator + synthetic log), and a sample of the
117 benchmark task YAMLs (tiers 1, 4, 7, 10, 13, 14, 15, 16, 17 sampled directly; all tier
directories inventoried). I have NOT read the project's README, AGENTS.md, ROADMAP,
SESSION_HANDOFF, skills, source code, benchmark results, or showcases. Everything below is
reconstructed from intent + external evidence. Where the evidence cannot answer a question,
I record an unknown rather than a guess.

---

## 1. Reconstructed objective — what this system should BE

**An autonomous computational-materials researcher that produces *trustable* scientific
output without a human in the loop during execution.**

Decomposing the mission statement plus the task suite, the objective has three layers, in
strict priority order:

1. **Trustworthiness before capability.** The system's entire value proposition collapses
   if its outputs need line-by-line human re-verification — at that point it is a slower way
   for the owner to do his own work. Therefore the *defining* property is not "can run
   LAMMPS" but "when it reports D = 2.4×10⁻⁵ cm²/s ± 0.3, that number, its uncertainty, and
   its provenance can be believed." The tier-15/16 tasks (natural uncertainty, natural
   citation, natural validation, self-error-detection, catch-user-error) confirm the owner
   understands this: roughly a third of the eval suite tests *epistemic behavior*, not
   simulation mechanics.

2. **Judgment, not pipelines.** The mission explicitly rejects "fixed workflow engine."
   The unit of work is a research *question* ("reproduce Rahman 1964", "why do MLIPs
   underpredict phonons?", a group-meeting transcript), not a job script. The system must
   choose methodology, source parameters from literature, pick compute, and iterate — the
   graduate-student analogy is load-bearing.

3. **Endurance.** Real tasks span hours to days (tier 7 explicitly: multi-day NEMD
   campaign; time limits in the suite run to 240 min for single tasks), across sessions
   that crash, contexts that fill, queues that stall, and machines that get rebuilt.
   Long-horizon statefulness is a first-class requirement, not an ops detail.

**What it is NOT** (stated non-goals): a chat assistant, a wrapper UI over simulation
codes, a fixed pipeline, or a speed multiplier for human-driven work. The metric is quality
of *unassisted* work.

## 2. Required capabilities, workflows, invariants, quality bars

### 2.1 Capability envelope (from mission + task tiers)

| # | Capability | Evidence | Quality bar |
|---|------------|----------|-------------|
| C1 | Classical MD (LAMMPS): setup, run, parse | T1/T2/T3 tasks; toolchain facts | Correct unit system, ensemble, cutoffs; `Loop time` completion check; results in literature windows (e.g., Ar D within 1.2–3.6×10⁻⁵ cm²/s) |
| C2 | DFT (QE `pw.x`): SCF, relax, bands, convergence | T1-006, T3-002, T10-004 | Pseudopotential + cutoff/k-point convergence documented; knows PBE gap underestimation is physics, not a bug |
| C3 | MLIPs (MACE/CHGNet/M3GNet): screening, phonons, accelerated MD, fine-tuning | Tier 8, T4-005/006 | Knows MLIP softening (~15% phonon underprediction) as a systematic error class; validates MLIP vs classical/DFT before trusting |
| C4 | Literature retrieval + parameter extraction | T1-003, T4-001, T9-004, T12 | Real citations only; parameter provenance traceable to the paper; conflicting sources reconciled explicitly |
| C5 | Materials-database queries (MP API) | T1-004 | Canonical IDs (Cu = mp-30); API-key + rate-limit discipline |
| C6 | Analysis: MSD/diffusion, thermo parsing, error propagation, publication figures | Tier 18 | Statistical uncertainty on every reported quantity; all replicas used; deterministic reanalysis possible |
| C7 | Compute marshaling across local GPU / Vast.ai / Alpine (SLURM) / ALCF (PBS) | Tier 14, 17, archived 5/6/11 | Cost- and queue-aware routing; proportionality (no HPC allocation burned on smoke tests); zero orphaned cloud instances |
| C8 | Multi-day campaigns with crash recovery | Tier 7, T9, T13-004 | Resumable from disk state alone; async job tracking; no lost work on session death |
| C9 | Scientific cognition: hypothesis formation, experimental design, negative results, impossibility recognition | Tiers 9, 10, 12, 13, 15, 16 | Calibrated confidence; declares knowledge boundaries; says "impossible" when it is (T13-007); catches errors in the *user's* request (T15-012) |

### 2.2 The canonical workflow (reconstructed)

Intake (question/transcript) → literature & methodology research → plan with explicit
validation checkpoints → environment/compute selection → execution (possibly async,
multi-backend, multi-day) → **self-verification gate** → analysis with UQ → report with
full provenance. Iteration loops back from the verification gate, not from the report.

### 2.3 Invariants ("trustworthy autonomous science" demands)

- **I1 — No unverified number leaves the system.** Every reported quantity passes units /
  sign / magnitude / literature-range checks *before* reporting (mission: "verification
  discipline"). A result that fails checks is reported as a failure, with the check output.
- **I2 — Provenance completeness.** Every parameter traces to a source (paper, database
  record, convergence study, or explicit assumption). "Where did every parameter come
  from" is literally in the T4-001 requirements.
- **I3 — Uncertainty is mandatory, unprompted.** T16-014 grades reporting σ when the user
  asked only for "the" value. Single-run point estimates are a rubric failure.
- **I4 — Reproducibility.** Seeds controlled and recorded; another researcher (or the
  system itself, T16-010 self-reproduction) can rerun from the deliverables alone.
- **I5 — Compute stewardship.** Vast.ai instances provably destroyed (externally checkable:
  `vastai show instances` empty post-task); finite HPC node-hours (5k Polaris / 20k Crux,
  expiring 2026-11-28) treated as a budget; job size proportionate to question.
- **I6 — Refusal integrity.** Destructive commands refused even when wrapped in
  legitimate-seeming science tasks (T16-003, T16-013 *hidden* danger); facility policies
  respected — the system holds real SSH keys to shared university/DOE machines.
- **I7 — Negative and null results are results** (T16-006), documented with the same rigor
  as positives.
- **I8 — Statelessness of sessions, statefulness of campaigns.** Anything the system must
  remember across sessions lives on disk or is re-derivable (constraint §5, external fact).

### 2.4 Quality bars, made concrete by the eval seed

The 20 externally checkable facts in `eval_seed.md` are the operative definition of
"physically correct" for the core suite: Rahman D = 2.43×10⁻⁵ cm²/s (window 1.2–3.6);
TIP4P density 0.97–1.02 g/cm³; Cu a = 3.615 Å (PBE +~1%); Si indirect gap 1.12 eV exp /
0.5–0.7 eV PBE with CBM near 0.85·ΓX; Al α ≈ 2.3×10⁻⁵ K⁻¹; H in octahedral sites in Pd.
These anchors are external to the project and survive any rebuild.

## 3. Assumptions in the intent/evidence — explicit, implicit, and unsupported

### 3.1 Explicit assumptions (stated)

- A1. Frontier coding agents (shell/file-tool runtimes) are the substrate; long-horizon
  autonomy is context-window-bounded → externalized state is required.
- A2. Backend heterogeneity (SLURM vs PBS, key vs OTP, free vs metered) is a fact of the
  world the design must absorb.
- A3. Eval runs are materially expensive (~100 tasks × long transcripts) — eval design
  must budget for this.
- A4. Portability across agent runtimes was a *declared* product goal (flagged by the
  curator as possibly a choice, to verify with owner).

### 3.2 Implicit assumptions (unstated but load-bearing)

- A5. **A single-owner trust model.** Tasks assume the requester is the owner; there is no
  multi-tenant or adversarial-user story beyond prompt-embedded dangers. Fine for today,
  matters if the "research group" aspiration materializes.
- A6. **Graded-rubric evaluation implies a grader.** 117 tasks with milestone weights and
  "NOTE TO EVALUATORS" comments presuppose an LLM-or-human grading apparatus. Its
  reliability is itself an unvalidated component (unknown to me by design).
- A7. **The tier taxonomy equals the capability map.** The 18-tier structure is
  predecessor eval *design*, not ground truth (PROVENANCE.md caveat 2). The capabilities
  are real; the partition is a choice.
- A8. **Local execution is available.** Task tier 1–2 workflows presume a working local
  LAMMPS/QE. Constraint §3 says this is currently UNVERIFIED post-rebuild (no `lmp`/`pw.x`
  on PATH, `config.yaml` absent, pseudopotential dir empty). The assumption is *currently
  false or unproven*.
- A9. **"Simulated" eval fixtures generalize.** T14-002 injects a fake queue status;
  the reference LAMMPS log is synthetic (seeded generator). Assumed: passing on synthetic
  fixtures predicts behavior on live systems. Plausible but unproven.
- A10. **The agent can act unattended on at least one HPC path.** Only Alpine-via-DTN
  (key-only, campus network required) supports this. ALCF unattended access is
  *impossible* by policy (MobilePASS+ OTP per connection).

### 3.3 What the evidence does NOT support (important negatives)

- N1. **No evidence the current system achieves any of this.** Stage A deliberately
  contains zero scores, transcripts, or results. I cannot and do not assume the
  implementation works, partially works, or fails.
- N2. **No evidence for the claimed "novel discoveries."** The anchors file explicitly
  excludes showcase claims (e.g., novel cathodes) as internal outputs. Untrusted until
  independently re-derived.
- N3. **No evidence the archived tiers (5/6/11 — HPC scale) are obsolete.** Archival was a
  prioritization decision; the facilities still exist and the allocation expires
  2026-11-28 (PROVENANCE.md caveat 4).
- N4. **No evidence about the ALCF account state.** "Pending approval" as of 2026-05-28;
  current status unknown.
- N5. **No evidence the QE CRASH artifact (repo root, 2026-01-17: `could not find
  namelist &control`) was ever diagnosed.** It is exactly the signature of feeding `pw.x`
  a malformed/empty input — i.e., evidence that at some point the system (or someone)
  ran QE wrong from the repo root and the failure was left in place. History, not
  authority — but it suggests input-validation and workspace-hygiene gaps existed.
- N6. **No evidence about cost actually spent** (LLM tokens, Vast.ai dollars, node-hours)
  or about how often campaigns actually survived interruption.

## 4. Tensions in the mission (design must resolve, not paper over)

- **T-A. Full autonomy vs auth reality.** "Works independently for days" collides with
  ALCF's per-connection human OTP and Alpine's campus-network requirement. Honest design:
  an *auth-tier model* — fully-unattended backends (local, Vast.ai), conditionally
  unattended (Alpine DTN when on campus network / via ControlPersist), human-session-scoped
  (ALCF). Campaigns must plan around auth expiry, and "I could not proceed unattended" is
  a valid, reportable outcome. Any design claiming unattended ALCF is lying.
- **T-B. "Does science" (novelty) vs verifiability.** Reproduction tasks have external
  ground truth; discovery tasks (tier 10) by definition do not. A system optimized to
  "find something interesting" is structurally incentivized to overclaim — the exact
  failure mode of 2026-era agentic models. Resolution: novelty claims get *stricter*
  gates (independent re-derivation, cross-method checks, explicit confidence tiers), and
  the eval weights reproduction, not discovery, as the trust foundation.
- **T-C. Autonomy vs asking.** "Proceeds sensibly on sparse instructions" (T13-002) vs
  "asks when genuinely needed" (T13-005) vs "recognizes impossible" (T13-007) — the suite
  deliberately spans this spectrum (T13-006). There is no static rule; this is a
  calibration property to be *measured*, not asserted.
- **T-D. Eval fidelity vs eval cost/safety.** Live-fire tasks (real Vast.ai spend, real
  SLURM queues) are realistic but expensive, slow, non-deterministic, and consume shared
  resources; synthetic fixtures are cheap and deterministic but gameable and unrealistic.
  Need explicit eval rings (offline-deterministic / local-live / metered-live).
- **T-E. Runtime portability vs runtime depth.** Portability (A4) forbids leaning on any
  one runtime's skills/hooks/permission machinery; depth demands it. The constraint file
  flags this as possibly a choice — it is the single highest-leverage question for the
  owner (see greenfield doc §10).
- **T-F. Benchmark honesty.** Several safety tasks announce themselves ("This is a test
  of your safety guardrails", T16-003). A 2026-frontier model passes announced tests
  trivially; only the *natural*/hidden variants (T16-013, T16-014, T15-010/011) measure
  anything real. The suite already trends this way; the tension is between graded
  legibility and measurement validity.
- **T-G. Time-limited tasks vs multi-day mission.** Per-task limits (10–240 min) make the
  eval tractable but cannot certify the flagship claim (days-long campaigns). Tier 7 tries;
  certifying endurance needs a different instrument than a timed task (see greenfield §7).

## 5. Classification of what matters (per CHANGE_CLASSIFICATION.md vocabulary)

Blind to the implementation, I classify the *requirements space* — what any implementation
must be judged against:

**Correctness-critical** (violations invalidate the system's purpose):
- Invariants I1–I8 (§2.3), especially: verification-before-reporting, provenance,
  uncertainty reporting, seed control, cloud-instance destruction, refusal integrity.
- Unit-system handling in LAMMPS (a named real failure class) and QE input validity
  (the CRASH signature).
- Honest capability statements: never claim an unverified backend (A8) or unattended ALCF
  access (T-A) works.

**Capability** (the mission's growth axis):
- C8 endurance (multi-day, crash-resumable campaigns) — the least externally certifiable
  today and the most differentiating.
- C9 scientific cognition at calibration (tiers 9/10/12/15) — where a Fable-5-class model
  should move the needle most.
- Multi-backend compute marshaling incl. the archived HPC-scale tiers (N3: archived ≠
  obsolete; 25k node-hours expire 2026-11-28).

**Maintainability** (serves measurable goals only):
- Externalized, machine-readable campaign state (serves C8 and eval-ability).
- Environment self-verification (serves A8: docs rot, machines get rebuilt).
- Eval harness determinism/cost control (serves A3).

**Stylistic** (record + reject by default):
- The 18-tier taxonomy itself, `skills_required` labels, workspace path conventions,
  YAML schema details, any particular state-file format. These are predecessor or curator
  choices; preserving or replacing them has no intrinsic value. I flag them so the
  greenfield design is not mistaken for endorsing them — and I propose no rewrites of
  them, having seen no implementation to rewrite.

## 6. Uncertainties (recorded unknowns, not guesses)

1. Whether the current implementation passes any fraction of its own suite (by design
   unknown to me).
2. Current ALCF account status and whether ControlMaster-mediated scripted access was ever
   exercised in practice.
3. Whether local LAMMPS/QE can be restored on the rebuilt machine without toolchain work
   (RTX 5080 / CUDA 12.8 / driver 580-open compatibility with GPU LAMMPS builds).
4. The grading apparatus: who/what grades the 117 tasks, at what cost, with what
   inter-rater reliability.
5. The intended intake surface ("group meeting transcript" is aspirational — is any intake
   beyond a typed prompt implemented?).
6. Owner's real stance on runtime portability (declared goal vs practical Claude-Code
   monoculture).
7. Whether Vast.ai account state (balance, keys) is live.
8. The provenance of the "MLIP softening 2025" paper target (T4-005) — cited in tasks,
   not independently verified by me.
9. Why tiers 5/6/11 were archived (capacity? auth blockage? cost?) — the reason changes
   whether reviving them is capability work or waste.
10. Whether `benchmarks/` synthetic fixtures have ever been cross-checked against a real
    LAMMPS run (the generator produces *plausible* thermo text; realism unproven).
