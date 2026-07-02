# Final Upgrade Record — Agentic Science Worker (1-ScienceAgent)

**Upgrade:** intelligence rebase, predecessor **claude-opus-4-8** → successor **claude-fable-5**
**Record author (Role 4, Migration Integrator):** `claude-fable-5`
**Date:** 2026-07-02
**Predecessor-era caveat:** no artifact in this repo records model identity for any pre-July work; "claude-opus-4-8" is the rebase brief's attribution for the recent era. January-era work may predate it (earlier Opus/Sonnet) — evidence cannot distinguish. This unrecorded provenance is itself finding D14 and is fixed going forward by Slice A1.

---

## 1. Scope and conduct

- **Target:** `/home/sf2/work/agents/science-agent/1-ScienceAgent` (~1.8 GB, 358 tracked files, 24 commits, 3 unpushed). Woken 2026-07-02 from dormancy (2026-06-21 →) specifically for this rebase; the fleet rebased on 2026-07-01 without it.
- **Conduct:** strictly read-only toward the project. All writes confined to `08_upgrades/upgrade-2026-07-02/`. The live agentctl session was never contacted (its hook log confirms zero project writes today). Fenced items (dirty working tree: README.md, ROADMAP.md, benchmarks/CURRENT_STATUS.md, showcases/README.md; two working-tree deletions; 3 unpushed commits; `logs/operations.log`; sibling asta dirs) were read but never modified, staged, restored, or pushed. No jobs submitted, no ssh, no external service mutated.
- **Stages completed:** A (blind reconstruction + greenfield), B (system audit/cartography), C (adversarial delta + historical decision review + uplift register), D (this integration: migration plan, six files, this record). All four roles ran as fresh Fable-5 contexts.

## 2. Evidence base and key findings

Package inventory (this directory): `stage-a-manifest.txt`, `.staging-A/` (curated intent/constraints/eval seed/external evidence), `independent_reconstruction.md`, `greenfield_design.md`, `current_system_audit.md`, `architecture_delta.md`, `historical_decision_review.md`, `uplift_opportunities.md`, `migration_plan.md`, `six-files/`, `baseline/`, this record.

Top findings (artifact-verified in Stage C unless noted):
1. **The system cannot currently run locally.** Every binary env path (`.claude/settings.json`), the MCP filesystem root, and run scripts point at pre-2026-06-13-reorg locations; 35 files carry dead paths. The binaries exist at `/home/sf2/work/compute/gpu-tests/1-GPUTests/` (execution post-rebuild unverified). Correctness item #1.
2. **State-truth rot.** Artifact truth for the last full run is **80 passed / 12 failed / 5 timeout of 97 (82%)**; the committed README claims 81/86 (100%); ≥9 dashboard rows diverge from artifacts in both directions; the honest corrections have sat uncommitted (fenced) since 2026-02-25. The claimed 3.2 GB pre-overhaul results archive **does not exist on disk** — all earlier baselines are markdown-only.
3. **Model identity was never pinned or recorded** in executor, judge, or artifacts — the February record is era-ambiguous at the exact moment a model swap makes that fatal for comparison.
4. **A post-February pivot the status docs never caught:** Mar–Jun commits built a compute-operations doctrine (compute-strategy/validation incl. post-incident Layer A′, campaign-orchestration, Alpine-DTN unattended path, ALCF onboarding; allocation HydrogenStorage expires 2026-11-28) with **zero benchmark coverage** — the suite still tests the February identity.
5. **Convergent validation of the incumbent's core:** the blind Fable-5 greenfield re-derived roughly half of the predecessor's Mar–Jun architecture (durable-file campaign state, smoke-first fidelity ladder, auth-tier honesty, validation gates). The skill-prose substrate survived two filesystem reorganizations that killed every mechanical artifact — "the agent IS the scaffolding" is validated for judgment, but **refuted for restraint** at the money/self-propagation boundary (2026-05-09 runaway: 8,366 jobs, ~16k emails).
6. **Endurance (the flagship claim) is designed but uncertified** — no recorded campaign death-and-resume exists; T7-001 stalled at 5 h.

## 3. Model gate

- **Incumbent:** presumed unavailable (verify `claude --model claude-opus-4-8` at execution; never fabricate head-to-head scores).
- **Gate instrument:** `six-files/EVALS.md` v1 — 15 tasks, absolute bars declared before running: ≥80% overall, **100% on restraint tasks E-06/E-07/E-13**, ≥80% on restraint/domain/tool-use/reasoning subtotals.
- **Fabrication check (already run):** `architecture_delta.md` §1 verified the Fable-5 Stage A/B outputs against artifacts — **no hallucinations**; three propagated doc-numbers were caught and corrected (discipline finding, not fabrication). PASS.
- **Gate run:** PENDING (Slice A0). The gate certifies "fit to operate this project," not "better than Opus 4.8."

## 4. Executed migration slices — **PENDING EXECUTION**

No slice has been executed. Baseline preservation is partially complete at plan time (hash manifest `baseline/hash_manifest.sha256`; verbatim snapshot of the fenced working-tree edits under `baseline/fenced-worktree-snapshot/`; branch `rebase/upgrade-2026-07-02` NOT yet created — first act of Slice A0). Slice outcomes, gate scores, and observed costs will be recorded here as they land, per the six-file update rule (migration_plan.md §6).

| Slice | Status |
|---|---|
| A0 branch + gate · A1 model pin · A2 runnability+probe · A3 status generation · A4 validator replay · A5 lint prototype · A6 tier-slice re-baseline · A7 forced-kill resume | **PENDING EXECUTION** |
| B-1 … B-9 | awaiting owner sign-off |

## 5. Change classification summary and stylistic attestation

- Accepted into plan: **correctness 5** (A1 model pin; A2 runnability/probe; A3 artifact-derived status; A5 input lint; B-5 mechanical money bounds), **capability 5** (A4/B-3b validator+grader studies; A6/B-3 Fable-5 re-baseline; A7 endurance certification; B-4 HPC revival; U-12 deferred), **maintainability 1** (B-1 doc-rot repair, owner-gated because it rides the live boot path).
- **Rejected stylistic (recorded, per CHANGE_CLASSIFICATION.md):** U-R1 ledger-format migration, U-R2 constitution file, U-R3 universal adapter monopoly, U-R4 tier re-taxonomy/schema rewrite, U-R5 AGENTS.md rewrite-in-new-voice, U-R6 three-context default topology; plus U-R7 (maintainability-only tidying) rejected this cycle.
- **Attestation:** the migration plan contains **zero stylistic changes**; the greenfield's ideas were adopted only where they bind to observed damage (unpinned model, self-corrupting record, money tail, uncertified endurance) or a removed blocker (Alpine DTN). The rewrite urge was considered and declined, visibly.

## 6. Six files

All six landed under `08_upgrades/upgrade-2026-07-02/six-files/` (this rebase's writes are fenced out of the project root; **promotion of the six files into the project proper is a Track-B owner decision**, since the project's own AGENTS.md/status docs are live-surface or fenced):
- `MISSION.md` — intent only, non-goals explicit, invariants I1-class hard requirements, allocation deadline 2026-11-28 recorded as external fact.
- `CURRENT_STATE.md` — descriptive, artifact-corrected (T12 = 59/90/72 etc.), runnability truth, MISSING-archive flagged.
- `DECISIONS.md` — D1–D18 index with model-era provenance caveat + Stage-C classifications cross-referenced; new ADR-101/102/103 (fable-5 provenance) with revisit triggers incl. the standing "more capable model arrives".
- `ASSUMPTIONS.md` — 15 registered assumptions with blast radius (headline: A-01 record validity, A-02 prompt-counter transfer, A-04 binaries execute, A-05/A-06 HPC liveness).
- `EVALS.md` — 15 tasks, separated answer key, declared absolute bars; ≥2 real-tool tasks (E-04, E-05, E-15); 3 restraint probes incl. live-operating-surface (E-06) and compute-discipline (E-07, expensive-HPC-when-cheap-exists scores 0).
- `REASONING_DEBT.md` — 13 open items ranked by leverage (top: regression-narrative confound, unattributed record, prompt-counter transfer, uncertified endurance), 6 suspected blind spots, 3 resolved this cycle.

## 7. Handoff — owner decisions and open items

1. **Approve/deny Track A execution** (branch-only, additive, no fenced contact — migration_plan.md §2) and the gate run (A0).
2. **Track B sign-offs**, each independent (plan §3): B-1 boot-path doc repair; B-2 live env repoint (.claude/settings.json, .mcp.json, hook activation); B-3 full re-baseline + grader study; B-4 Alpine round-trip (first in-repo HPC coverage); B-5 standing Vast.ai dead-man sweep + spend caps; B-6 landing the fenced status corrections / pushing 3 commits (GitHub currently shows a 4-month-stale, rosier claim); B-7 attempt archive recovery from restic/ZFS; B-8 ALCF account status + allocation plan (expires 2026-11-28); B-9 intent questions — runtime portability (dead aider/codex scaffolding), showcase novelty re-derivation, frontier-tier redesign.
3. **Standing rule inherited by the successor:** doc claims in this repo are not evidence; every load-bearing number gets re-derived from artifacts (the practice that produced findings #2–#3 above).
4. If the gate FAILS: no slices execute; this package and the six files stand as model-independent value; escalate with specific failed tasks.

**Record status:** sections 1–3, 5–7 complete; §4 pending execution.
