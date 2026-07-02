# GREENFIELD DESIGN — Autonomous Computational-Materials Researcher (2026, no legacy)

**Author model ID: `claude-fable-5`**
Role: Greenfield Architect (Role 2, Stage A — deliberately blind). Companion to
`independent_reconstruction.md` (same evidence base: `.staging-A/` only). This is what I
would build *today* for the reconstructed mission, assuming 2026 agent runtimes and a
Fable-5-class reasoning model, and assuming NO existing system to preserve. I have seen no
implementation; nothing here is a rewrite proposal.

---

## 0. Design theses

1. **The scarce resource is trust, not intelligence.** A 2026 frontier model already
   "knows" MD/DFT methodology well enough to be dangerous. The architecture's job is to
   make its claims *checkable* and its failures *loud*. Every structural choice below
   serves auditability first.
2. **The filesystem is the nervous system.** Sessions die; contexts fill; the machine
   itself was rebuilt once already. All campaign state, provenance, and budgets live in
   plain, append-mostly files that any fresh context (or human, or grader) can reconstruct
   the campaign from. The model is stateless; the campaign is not.
3. **Judgment in the model, discipline in the harness.** Methodology selection, hypothesis
   generation, and interpretation are model work. Budget enforcement, provenance capture,
   resource cleanup, and gate-keeping are *mechanical* (hooks/wrappers/ledgers) — because
   restraint is exactly what agentic models fail at under pressure (§8).

## 1. Architecture overview

```
                       ┌─────────────────────────────────────────────┐
 intake ───────────▶   │  CAMPAIGN LEDGER (on disk, append-mostly)   │
 (question, transcript,│  brief.md · plan.md · state.json ·          │
  citation, dataset)   │  runs/<run-id>/manifest.yaml · budget.jsonl │
                       │  provenance.jsonl · findings.md · report/   │
                       └─────────────────────────────────────────────┘
                              ▲            ▲             ▲
              ┌───────────────┘            │             └───────────────┐
      ┌───────┴───────┐          ┌─────────┴─────────┐         ┌─────────┴────────┐
      │ ORCHESTRATOR  │  spawns  │ EXECUTOR contexts │  gates  │ VALIDATOR context│
      │ (planning,    │────────▶ │ (one per run/step;│────────▶│ (fresh context,  │
      │ replanning,   │          │ disposable)       │         │ adversarial,     │
      │ intake, report│          │ sim setup, submit,│         │ never the author)│
      │ assembly)     │          │ parse, analyze    │         └──────────────────┘
      └───────┬───────┘          └─────────┬─────────┘
              │                            │ via backend adapters only
              ▼                            ▼
      compute-router            local GPU · Vast.ai · Alpine/SLURM · ALCF/PBS
```

Roles are *contexts*, not services: the orchestrator is a long-lived-by-convention agent
session that reads/writes the ledger; executors are spawned subagent contexts scoped to a
single run; the validator is always a **fresh context that did not produce the result**
(structural defense against self-grading bias). Any of them can die and be respawned; the
ledger is the only continuity.

## 2. Task intake

Accepted forms: a typed research question; a citation ("reproduce X"); a dataset + question;
a meeting transcript (aspirational per mission — supported as "extract candidate tasks,
rank, confirm scope"). Intake always produces a **campaign brief** before any compute:

- `brief.md`: question, deliverables, success criteria mapped to *external* anchors where
  they exist (literature value + tolerance), explicit non-goals.
- **Ambiguity triage** (the T13 spectrum, made mechanical): the model lists its
  interpretation decisions with confidence. Decisions above a materiality threshold
  (changes >10× compute, changes the scientific claim, touches metered money) become
  ask-the-owner items; everything else proceeds with the assumption *logged*. Impossible
  or ill-posed requests exit here with a written impossibility argument — a first-class
  deliverable, not a failure.
- **Premise check**: intake explicitly attempts to falsify the user's framing (catches
  T15-012-style user errors) before planning.

## 3. Planning

- `plan.md`: a DAG of steps, each with — purpose, method + methodology citation, expected
  output + *predicted range* (the model commits to a physics expectation BEFORE running;
  this is the cheapest, strongest self-check available), compute estimate (backend, wall
  time, cost), and the validation gate it must pass.
- **Methodology research precedes simulation.** Literature step is mandatory for any task
  with a reproduction/parameter component; every adopted parameter enters
  `provenance.jsonl` with its source (paper/DOI, database ID, convergence study, or
  `ASSUMED` with rationale). `ASSUMED` entries are surfaced in the final report
  automatically.
- **Fidelity ladder**: plans default to smoke test (minutes, local/cheapest) → validation
  run (small, checked against anchor) → production (sized by convergence evidence, not
  vibes). Skipping a rung requires a written justification in the plan.
- Replanning is an event appended to `plan.md` with reason + what evidence changed
  (T15-003). Plans are never edited in place — history is part of provenance.

## 4. Execution

- **Executor contexts are disposable and single-purpose.** Each run gets
  `runs/<run-id>/manifest.yaml`: inputs (hashed), code/potential/pseudopotential versions,
  seeds, backend, job IDs, env snapshot. Manifests are written *before* submission —
  a run that crashes still has complete provenance.
- **Backend adapters** (thin, uniform verbs: `probe`, `stage`, `submit`, `status`,
  `fetch`, `cleanup`) over: local GPU, Vast.ai, Alpine/SLURM (via DTN), ALCF/PBS (via
  human-opened ControlMaster only). Adapters are the ONLY path to compute; no raw ssh/qsub
  from the model. This is where mechanical discipline lives:
  - `probe` verifies the backend actually works *now* (binary exists, GPU visible, auth
    alive, quota OK) — never trust docs; the local machine was rebuilt once and the docs
    rotted (constraints §3). Probe results cached with TTL in `state.json`.
  - `submit` refuses without a budget line (§6) and records job-ID → run-ID mapping.
  - `cleanup` is idempotent and *runs on a dead-man's schedule*, not just on success
    (§8.3 — orphan Vast.ai instances are the canonical money leak).
- **Async by default.** Long jobs are submit-and-checkpoint: executor writes expected
  completion + polling instructions into `state.json` and exits. A cron/heartbeat (or the
  owner reopening a session) resumes via the ledger. No context ever "waits" hours.
- **Toolchain guards** encode the known failure classes as pre-submit lint, mechanically:
  LAMMPS unit-system consistency (ε in kcal/mol ⇒ `units real`), QE namelist validation
  (`&control` first — the exact CRASH signature in the evidence), pseudopotential/element/
  functional match, timestep sanity vs. fastest mode, PBC/box checks. Cheap, deterministic,
  catches the embarrassing 20%.

## 5. Validation (the load-bearing stage)

A result cannot flow to reporting until a **validation gate** passes, executed by a fresh
validator context with access to the run artifacts but not the executor's reasoning:

1. **Mechanical checks** (scripted, deterministic): run completed (`Loop time` / QE exit),
   conservation/thermostat sanity, units audit, statistical health (equilibration detected
   and discarded, autocorrelation-aware error bars, all replicas used).
2. **Physics checks** (model): sign/magnitude/asymptotics; comparison against the
   *pre-registered* prediction from `plan.md`; comparison against external anchors
   (eval_seed-style facts) with explicit tolerance; known systematic errors stated (PBE
   gap underestimation, MLIP softening) rather than "explained away".
3. **Provenance check**: every number in the draft claim traces to a manifest + analysis
   script; every parameter traces to `provenance.jsonl`.
4. **Verdict**: PASS / PASS-WITH-CAVEATS (caveats propagate verbatim to the report) /
   FAIL (loops to replanning). Verdicts are appended to the ledger; a validator can be
   overruled only by the owner, in writing.

**Novelty escalation** (tension T-B): claims with no external anchor ("we found a new
stable phase") additionally require independent re-derivation by a second method or seed
lineage, a stated confidence tier, and are labeled `UNCORROBORATED` until the owner
reviews. The system is architecturally forbidden from presenting uncorroborated novelty
as finding-grade output.

## 6. Compute strategy and budgets

- **Auth-tier model** (from constraints, honestly): Tier U (unattended: local, Vast.ai),
  Tier C (conditionally unattended: Alpine via DTN — key-only, campus network required),
  Tier H (human-session-scoped: ALCF via ControlMaster, MobilePASS+ OTP). Plans must
  schedule Tier-H work inside declared human-available windows; the router never
  *assumes* Tier-H availability. "Blocked on auth" is a normal, reportable campaign state.
- **Routing** is a scored decision recorded in the plan: data-locality, queue estimate
  (live-probed), cost (live-probed for Vast.ai — spot prices rot), allocation burn-down
  (Polaris charges whole nodes; the DD award expires 2026-11-28), and proportionality
  (<1 h smoke tests never go to metered/allocated resources).
- **Budget ledger** (`budget.jsonl`): every campaign carries hard caps — $ (cloud), node-
  hours (per-facility), LLM-token budget, wall-clock. Adapters *enforce* (refuse submit
  when exceeded); the model *plans within*. Spend events are appended at submit and
  reconciled at completion. Overruns halt the campaign and page the owner; they are never
  silently absorbed.
- **Standing reconciliation**: a scheduled sweep compares `vastai show instances` and
  facility queues against the ledger; any resource not traceable to a live run is flagged
  (and, for Vast.ai, destroyed) — external, checkable invariant I5.

## 7. Benchmark / eval design

Budget-aware (eval cost is a stated constraint) and gaming-resistant:

- **Ring 0 — deterministic, offline, free** (run on every change): parsing/analysis on
  seeded fixtures (the `seed=42` synthetic-log pattern generalizes), toolchain-guard unit
  tests, input-lint goldens, budget/cleanup logic simulations, refusal tests. Minutes, CI.
- **Ring 1 — local live physics** (nightly/weekly): the anchor set with tolerances (LJ
  minimization energy, Ar diffusion window, TIP4P density, Cu lattice constant, Si gap
  character). Graded *numerically* against external anchors — no LLM grader needed for
  the pass/fail core.
- **Ring 2 — metered live** (per-release, capped budget): one Vast.ai lifecycle task
  (external check: zero instances after), one Alpine round-trip, one multi-hour async
  campaign with a **forced mid-campaign kill** — the resume-from-ledger test is the only
  honest certification of the endurance claim (tension T-G). ALCF tasks run only inside a
  human window and grade the *scheduling-around-auth* behavior itself.
- **Ring 3 — cognition panel** (sampled, LLM-graded with published rubrics): natural-
  behavior tasks only where the tested behavior is *not announced* (the T16-014/T15-010
  pattern — unprompted uncertainty, unprompted planning, catch-user-error, impossible-task
  exit, hidden-danger refusal). Two-grader agreement sampled; rubric drift audited.
  Announced safety tests ("this is a test of your guardrails") are worthless against a
  2026 model and are excluded from headline metrics.
- **Anti-gaming rules**: graders never see the model's self-assessment before artifacts;
  numeric tasks graded from artifacts, not prose; a rotating held-out variant pool (same
  physics, perturbed specifics) defends against memorized solutions; every headline score
  reports its ring, cost, and N.
- **Score honesty**: the eval report always includes the *unattempted* set (e.g., ALCF
  blocked by account status) — capability claims are scoped to what was actually exercised.

## 8. Safety and restraint (designed for 2026 failure modes, from first principles)

Known agentic-model failure modes and the structural countermeasure for each:

| Failure mode | Countermeasure |
|---|---|
| **Overclaiming / premature victory** ("simulation successful" on a crashed run) | Reporting reads *only* validator verdicts + manifests, never executor prose; mechanical completion checks gate the pipeline |
| **Fabrication under tool failure** (API down → invent a plausible number) | Provenance check (§5.3) makes unsourced numbers unreportable; `ASSUMED` is legal and visible, fabrication is structurally caught |
| **Self-grading leniency** | Author/validator context separation; fresh context, artifacts only |
| **Retry storms / spend-to-look-busy** | Budget ledger enforced at the adapter, not by model self-restraint; per-step retry caps with mandatory diagnosis between retries |
| **Silent scope creep** ("while I was at it I also…") | Plan DAG is the contract; off-plan work requires a replanning event; report diffs deliverables against `brief.md` |
| **Destructive "cleanup" helpfulness** | No raw destructive shell against shared systems; adapter `cleanup` is scoped to run workspaces; deny-listed patterns require owner confirmation regardless of framing (hidden-danger class T16-013) |
| **Auth circumvention creativity** (agent "helpfully" scripting around OTP) | Tier-H access exists only through the human-opened ControlMaster; no credential material readable by executors; policy stated in the orchestrator constitution as a hard boundary |
| **Orphaned resources on crash** | Dead-man reconciliation sweep (§6) independent of any agent context |
| **Sycophancy to a wrong premise** | Mandatory premise check at intake; validator instructed to check the claim against physics, not against the user's expectation |
| **Context-rot degradation** (long session quietly loses constraints) | Disposable executor contexts + ledger re-read on every resume; constitution re-injected per context, not assumed remembered |

The **constitution** (a short, versioned file every context loads) carries the invariants
I1–I8 verbatim. It is deliberately short: restraint rules that don't fit in one page don't
survive context pressure.

## 9. Provenance & reproducibility

- `provenance.jsonl`: append-only claims ledger — every parameter, every external fact
  fetched (paper, MP record, price quote) with source, timestamp, and retrieval hash.
- Run manifests (§4) + pinned environments (conda-lock / container digest per backend) +
  recorded seeds ⇒ **replay test**: the eval suite includes re-running a past campaign's
  production step from its manifest alone (T16-010 self-reproduction, made structural).
- Reports are generated *from* the ledger (numbers pulled from analysis outputs by
  reference, never retyped), with an auto-appended methods section: parameter table with
  sources, uncertainty method, seeds, versions, budget actually spent, and all
  PASS-WITH-CAVEATS caveats. A report a stranger could rerun is the deliverable bar.

## 10. Capability unlocks (Fable-5-class vs 2025-era models)

What a 2026 frontier model makes feasible that materially changes this design vs. a
2025 build:

1. **Trustable pre-registration.** The model's physics priors are good enough that
   "predict the range before running" (§3) is a real error-detector, not noise — 2025
   models' predictions were too loose to gate on.
2. **Long-horizon coherence at the campaign level**: multi-day DAGs with replanning can be
   *owned* by the model rather than hand-scripted; 2025 designs needed rigid pipelines
   precisely because judgment degraded over long horizons. (The ledger is still required —
   contexts remain finite — but the pipeline rigidity is not.)
3. **Adversarial self-review that actually bites**: a fresh Fable-5 validator finds real
   physics/statistics errors in another context's work (unit slips, bad equilibration
   windows, over-fit MSD regimes) at a rate that justifies the token cost.
4. **Literature-to-parameters with provenance** at near-human reliability: extracting a
   complete, sourced parameter set from a 1964 paper and reconciling conflicting modern
   sources (T12-003) was 2025's flakiest step; it can now be a gated, auditable stage.
5. **Cross-domain diagnosis**: correlating a PBS scheduler quirk, a Lustre I/O pattern,
   and a thermostat artifact in one reasoning pass — the tier-9 error-diagnosis class —
   was beyond 2025 models without heavy scaffolding.
6. **Cheap cognition evals**: rubric-graded natural-behavior panels (§7 Ring 3) become
   affordable and reasonably reliable with a frontier grader; in 2025 the grader was the
   least trustworthy component.
7. **Genuine open-question work** (tier 10) shifts from "generate hypotheses" to "design
   and execute discriminating tests between hypotheses" — with the §5 novelty escalation
   as the containment vessel.

What does NOT change with model quality: auth physics (OTP still needs a human), money
leaks (billing doesn't care how smart the agent is), context finiteness (ledgers still
required), and the need for mechanical gates (a smarter model produces more sophisticated
bad ideas faster — the harness, not the model, holds the line).

## 11. Questions I would ask of the current system

1. What fraction of the 117 tasks has the incumbent actually passed, at what grading
   rigor, and how much did a full suite run cost (tokens + $ + node-hours)?
2. Has any campaign survived a genuine mid-run session death and resumed from disk state
   alone? Show the artifact trail.
3. What is the ALCF account status today, and has scripted access via a human-opened
   ControlMaster ever been exercised on Polaris/Crux? How much of the 25k node-hour award
   (expires 2026-11-28) has been used?
4. Is local execution real right now — can the rebuilt machine run `lmp` and `pw.x` at
   all (post-WSL2→bare-metal), and who verified it last?
5. What is the story behind the repo-root QE `CRASH` file (2026-01-17)? Was the root
   cause diagnosed, and did anything structural change as a result?
6. Have any Vast.ai instances ever been orphaned, and is there an independent
   reconciliation against `vastai show instances` (vs. trusting the agent's own cleanup
   logs)?
7. Who or what grades benchmark runs, and has grader reliability ever been measured
   (two-grader agreement, rubric drift)?
8. Why were tiers 5/6/11 archived — auth blockage, cost, or capability failure? The
   answer decides whether HPC-scale work is a revival or a rebuild.
9. Are the showcase "novel discovery" claims (excluded from my evidence as internal
   output) backed by re-derivable artifacts — manifests, seeds, independent method
   cross-checks — or only by reports?
10. Is runtime portability (Claude Code / Aider / Cursor) a real requirement the owner
    still wants, or a 2025-era hedge? The answer swings the orchestration design more
    than any other single fact.
11. Where does parameter provenance live today — can the system answer "where did σ =
    3.405 Å come from" for an arbitrary past run without re-reading a transcript?
12. What does the system do today when a validation-range check fails — loop, report the
    failure, or rationalize the discrepancy? Show a real example transcript.
