# Migration Plan — Agentic Science Worker (1-ScienceAgent)

**Role:** Migration Integrator (Role 4, Stage D)
**Author model:** `claude-fable-5`
**Date:** 2026-07-02
**Upgrade:** claude-opus-4-8 → claude-fable-5
**Inputs:** all Stage A–C package outputs in this directory (`current_system_audit.md`, `independent_reconstruction.md`, `greenfield_design.md`, `architecture_delta.md`, `historical_decision_review.md`, `uplift_opportunities.md`, `.staging-A/`), the read-only workspace, `machinery/templates/*`, `machinery/eval-template.md`.

**Dormancy framing.** This project slept 2026-06-21 → 2026-07-02 through the fleet rebase and a 2026-06-13 machine reorganization before that. The two top correctness items are therefore *state-truth restoration* (the system cannot currently execute anything locally: 35 dead-path files, dead `.claude/settings.json` env, dead `.mcp.json` root — while the binaries verifiably exist at `/home/sf2/work/compute/gpu-tests/1-GPUTests/`) and *doc-rot repair* (an agent booting today inherits a February worldview from AGENTS.md/SESSION_HANDOFF and an evidence record with nine confirmed artifact/doc divergences). Capability work is sequenced strictly behind those.

---

## 0. Gate status and standing rules

- **Model gate:** incumbent claude-opus-4-8 presumed unavailable (`claude --model claude-opus-4-8` — check, don't assume, at execution time). Gating is therefore **absolute** per `machinery/eval-template.md`: candidate must score ≥80% overall on `six-files/EVALS.md` v1, **100% on restraint tasks (E-06, E-07, E-13)**, and meet the declared per-dimension bars. The adversarial-reviewer fabrication check is already in hand: `architecture_delta.md` §1 found **no hallucinations** in the Fable-5 Stage A/B outputs (three doc-number propagations were caught and corrected — a discipline finding, not fabrication). Gate FAIL ⇒ no slices execute; the six files and this package still land.
- **READ-ONLY fence (unchanged until owner approves execution):** no edits to any existing project file; all slice work happens on branch `rebase/upgrade-2026-07-02` or in new untracked/gitignored files; nothing below authorizes touching fenced items.
- **FENCED, permanently, regardless of track:** working-tree edits to `README.md`, `ROADMAP.md`, `benchmarks/CURRENT_STATUS.md`, `showcases/README.md`; the working-tree deletions of `benchmarks/results/BENCHMARK_RESULTS*_20260117.md` (never restore); the 3 unpushed commits (`8e00ba8`, `5c99011`, `baaa4fd` — never push/rebase); `logs/operations.log`; the live agentctl session; sibling `../asta-paper-finder`, `../asta-theorizer`.
- **No SLURM/ssh/job submission and no external-service mutation** except inside Track-B slices explicitly signed off by the owner, in an owner-sanctioned session.

## 1. Baseline preservation (partially DONE at plan time)

| Item | Status |
|---|---|
| **Hash manifest** of canonical artifacts: git HEAD, all 97 `results/runs/*/result.json`, fenced working-tree files, untracked owner files (hash only — `.claude/settings.json` contains an API key and is deliberately NOT snapshotted verbatim), governance docs, harness core | **DONE** → `baseline/hash_manifest.sha256` |
| **Verbatim snapshot of the fenced uncommitted edits** (they embody 4 months of unlanded owner intent; a reset would destroy them) | **DONE** → `baseline/fenced-worktree-snapshot/` (read-only copies; the originals remain untouched and uncommitted) |
| Untracked governance docs | None exist (checked: untracked set = `08_upgrades/`, `CRASH`, `input_tmp.in`, `.claude/settings.json`, `logs/operations.log`) |
| **Branch `rebase/upgrade-2026-07-02`** created at current HEAD (`baaa4fd`) | **PENDING EXECUTION** — first action of Slice A0. Branch creation does not touch the dirty working tree; all slice commits go only to this branch; `main` is never advanced by the rebase |
| Baseline eval scores | The February suite results are preserved by the manifest; the *pre-overhaul* archive is already lost (D11) — recovery from restic/ZFS backup catalogs is Track B-7, owner decision |

## 2. Track A — immediately executable (additive, reversible, no fenced contact, no external/HPC actions, no live-surface edits)

Every slice states: **hypothesis → measurable improvement → isolated prototype → named eval → merge/revert rule.** Slices execute in order; each is independently revertible.

### Slice A0 — Baseline branch + gate run
- **Hypothesis:** none (mechanical precondition).
- **Action:** create `rebase/upgrade-2026-07-02` at HEAD; verify `baseline/hash_manifest.sha256` still matches (detects any drift since plan time); run the EVALS.md v1 gate (15 tasks, fresh contexts, answer key withheld); record scores in `six-files/EVALS.md` § Historical results and `final_upgrade_record.md` §4.
- **Eval:** the gate itself. **Merge/revert:** gate FAIL ⇒ stop; package lands anyway.
- **Cost:** tokens only (~15 short fresh-context tasks).

### Slice A1 — Model pin + identity recording (U-01, correctness)
- **Hypothesis:** adding `--model` to executor and grader spawns and `model`/`grader_model`/`cli_version` fields to `result.json` restores evidence continuity at zero behavioral cost.
- **Measurable improvement:** 100% of new run artifacts carry model identity (February artifacts: 0%).
- **Prototype:** on branch, edit `benchmarks/evaluation/backends/claude.py` + `benchmarks/evaluation/llm_grader.py` (additive args/fields only; no task YAML, threshold, or rubric changes).
- **Named eval:** **EV-A1** = run one cheap non-compute task (BENCH-T13-007, impossible-task recognition) and assert the three fields present and pinned to `claude-fable-5`; plus EVALS E-12 (patch-spec correctness) already graded at gate time.
- **Merge/revert:** merge to branch head on pass; revert = `git revert` (two files).

### Slice A2 — Runnability restore via new, untracked config + live probe (U-02, correctness)
- **Hypothesis:** the system's local-execution brokenness is pure path rot; a fresh gitignored `config.yaml` (per `config.example.yaml`) pointing at `/home/sf2/work/compute/gpu-tests/1-GPUTests/{md-lammps/install/bin/lmp, dft-qe/build-{cpu,gpu}/bin/pw.x}` + a `probe` step in `harness.py --verify` (checks binaries/GPU/keys live instead of trusting configs) makes the harness runnable again.
- **Measurable improvement:** `harness.py --verify` passes (currently cannot); one local LAMMPS smoke (BENCH-T1-001) completes.
- **Prototype:** new `config.yaml` (untracked by design — `.gitignore` already covers it); `--verify` probe extension on branch. **Explicitly out of scope here:** `.claude/settings.json` and `.mcp.json` (live-session operating surface → Track B-2). The binaries exist on disk (re-verified 2026-07-02) but have never been *executed* post-rebuild — the probe must report, not assume, that they run (A-04 in ASSUMPTIONS.md).
- **Named eval:** **EV-A2** = `--verify` exit 0 + BENCH-T1-001 artifact with `Loop time` present; EVALS E-04/E-05 cover the parsing path.
- **Merge/revert:** revert = delete `config.yaml`, revert probe commit.

### Slice A3 — Artifact-derived status generation (U-03, correctness)
- **Hypothesis:** a script that regenerates the dashboard mechanically from `results/runs/*/result.json` (numbers pulled by reference, never retyped) kills the transcription-drift error class (nine confirmed divergent rows, both directions).
- **Measurable improvement:** generated table matches the Stage-C independent tally (80 pass / 12 fail / 5 timeout of 97) exactly; every divergence vs. the human-written dashboard is flagged, not silently absorbed.
- **Prototype:** new script `benchmarks/evaluation/generate_status.py` (or similar) writing to a **NEW** file (e.g. `benchmarks/results/GENERATED_STATUS.md`); fenced `CURRENT_STATUS.md` untouched.
- **Named eval:** **EV-A3** = diff of generated tally vs. `architecture_delta.md` §1.1 numbers = zero disagreement; divergence report lists ≥ the nine known rows (T10-003/004, T12-001/002/003, T7-002/003, T8-005, T15-007, T16-015/016, foundation counts).
- **Merge/revert:** pure addition; revert = delete script + output.

### Slice A4 — Validator-separation history replay (U-08, correctness→capability; also the cheapest Fable-5 uplift test)
- **Hypothesis:** a fresh Fable-5 validator context, given run *artifacts only* (never executor prose), independently flags known-failed runs without excess false alarms — testing the greenfield's "adversarial review now bites" claim (§10.3) before any larger grader study.
- **Measurable improvement:** catch-rate ≥5/6 on known-failed workspaces with ≤1/6 false alarm on known-passed.
- **Prototype:** driver script on branch; runs entirely against existing 2026-02 workspaces; writes verdicts under `08_upgrades/upgrade-2026-07-02/experiments/U-08/`.
- **Named eval:** **EV-A4** = the 6+6 replay itself, thresholds above declared *before* running.
- **Merge/revert:** nothing merges into the operating path this cycle; the result decides whether Track-B grader study (B-3b) is funded. Token cost only.

### Slice A5 — Deterministic toolchain lint, prototype only (U-11, correctness-minor)
- **Hypothesis:** a 20-line pre-run lint (QE: non-empty input, `&control` first; LAMMPS: units/pair-style consistency) catches the CRASH-file failure class (occurred ≥2× on 2026-01-17, never structurally addressed — D18).
- **Measurable improvement:** lint blocks a synthetic reproduction of the historical empty-input `pw.x` invocation.
- **Prototype:** standalone `scripts/lint_sim_input.py` + unit test on branch. **NOT wired into `.claude/hooks/validate_simulation.py`** — that hook is executed by the live session (operating surface → Track B-2 for activation).
- **Named eval:** **EV-A5** = unit test reproducing the CRASH signature is blocked; a valid QE input passes.
- **Merge/revert:** pure addition.

### Slice A6 — Fable-5 tier-slice re-baseline: T1 + T13 + T15 (U-04 first stage, capability — this is the project-level model gate)
- **Hypothesis:** under pinned Fable 5 with identical tasks/prompts/thresholds, foundation + behavioral tiers hold or improve vs. the February record (which is Opus-era and era-ambiguous); the slice bounds cost before the full suite.
- **Measurable improvement:** first model-attributed capability numbers in project history; per-task deltas vs. February artifacts with the caveat that the February model identity is unrecorded.
- **Prototype:** depends on A1+A2. Local only, no cloud, no HPC. Results land in gitignored `results/runs/` (additive) with pinned-model fields.
- **Named eval:** **EV-A6** = slice pass-rate ≥ February slice pass-rate on the same tasks (T1: 6/6 then; T13, T15 per artifact record), reported with replicate spread on the 3 known-variance behavioral tasks (T15-003, T13-003, T13-006 — 3× each).
- **Merge/revert:** runs are additive artifacts; no merge decision beyond recording. **If this slice shows Fable-5 regression on behavioral tiers, the D2 ablation (AGENTS.md counters) jumps the queue as the next experiment — the counters would then be load-bearing, not legacy.**
- **Cost note:** ~25–30 task executions, tokens + local GPU; no money spent beyond LLM usage.

### Slice A7 — Endurance certification, local forced-kill resume (U-07, capability)
- **Hypothesis:** a fresh context can resume a 2-stage local LAMMPS campaign from `WORKFLOW.md` alone after a `kill -9` between stages — certifying (or falsifying) the flagship "works independently for days" pattern (D6: designed, never proven; T7-001 stalled at 5 h historically).
- **Measurable improvement:** first recorded death+resume artifact trail, zero human hints.
- **Prototype:** isolated workspace under `workspaces/` (gitignored); uses existing `campaign-orchestration` skill *as documented* — no skill edits.
- **Named eval:** **EV-A7** = stage-2 completes after resume; the resume context's first actions are ledger reads (auditable in transcript); campaign artifacts complete.
- **Merge/revert:** additive; ~2 h wall + tokens; requires A2.

## 3. Track B — owner sign-off required (live operating surface, fenced-adjacent, external/HPC, benchmark-claim changes, standing automation)

| ID | Item | Why Track B | Prepared artifact (Track A side) |
|----|------|-------------|----------------------------------|
| B-1 | **Doc-rot repair on the agent boot path** (U-09): AGENTS.md skills-table refresh, SESSION_HANDOFF.md supersession banner, path corrections in the ~10 live-doc members of the 35-file dead-path set | AGENTS.md/CLAUDE.md/skills are the **live session's operating surface**; SESSION_HANDOFF and several candidates sit near fenced territory | Drafts staged on branch as `*.proposed.md` beside targets, never overwriting; diff summary for owner review |
| B-2 | **Environment repoint for the live session**: `.claude/settings.json` env vars (`LMP`, `QE_CPU`, `QE_GPU`), `.mcp.json` filesystem root; activation of the A5 lint inside `.claude/hooks/` | Same file the live session reads; also contains the owner's MP API key | Exact proposed values validated by A2's probe |
| B-3 | **Full-suite Fable-5 re-baseline** (U-04 full, ~98 tasks) incl. 3× replicates on the 8 known-variance tasks; **(b)** grader trust study (U-05: two-grader agreement + test-retest on ~15 preserved workspaces, artifact-only vs prose-visible) | Materially expensive (docs: ~7 h at 6 workers + LLM cost); B-3b funded only if A4 shows validator signal | A6 slice results + cost extrapolation from `parallel_run_*` logs |
| B-4 | **Alpine DTN round-trip + first in-repo HPC eval task** (U-06): `ssh cu_alpine 'sinfo -p atesting_a100'`, then one 10-min smoke through the compute-validation gate | External action: real SSH to a shared university machine; campus-network dependency; facility policy | Task definition + grading rubric drafted; D5/D7 doctrine cited |
| B-5 | **Standing money-boundary mechanism** (U-10): scheduled `vast_safety.py --postflight` sweep (dead-man), submit-side spend-cap check | Registers standing automation on the owner's machine; queries an external billed service | Dry-run sweep script (read-only `vastai show instances`) ready |
| B-6 | **Benchmark-claim / status-doc landing**: whether to commit the fenced 02-25 edits, push the 3 unpushed commits, adopt A3's generated status as the record | All fenced; committed README currently overstates (81/86, 100%) vs artifact truth (80/97, 82%) — GitHub-visible claim correction is an owner call | Stage-C verified tally + A3 generator |
| B-7 | **Evidence rescue**: attempt recovery of the vanished 3.2 GB pre-overhaul results archive (`runs_20260224_pre_overhaul`) from restic/ZFS tiers (`~/work/ops/infra-consolidation/`) | Backup-system operation outside the project; owner's infrastructure | D11 analysis; recovery would restore the only Opus-era baseline artifacts for U-04 comparison |
| B-8 | **ALCF status check + allocation plan** (`sefl-alcf` pending as of 05-28; HydrogenStorage 5k+20k node-hours **expire 2026-11-28** — external deadline) | OTP-gated human session by policy | polaris/crux backend pages verified content (D8) |
| B-9 | Owner questions that steer later cycles: runtime portability (D16 — dead aider/codex scaffolding), frontier-tier redesign (U-12, gated on B-3), showcase novelty re-derivation (D17) | Intent decisions, not engineering | Question list in `final_upgrade_record.md` §7 |

## 4. Explicitly REJECTED this cycle (stylistic attestation)

Per `CHANGE_CLASSIFICATION.md`, recorded and **rejected**; none appears in any slice:

- U-R1 WORKFLOW.md → JSONL ledger-suite migration (format churn; add fields instead, inside A7 only if evidence demands).
- U-R2 "Constitution" file (repackaged AGENTS.md).
- U-R3 Universal backend-adapter monopoly (new rot surface; contradicts D1/D4 evidence; only `probe` + spend-cap survive, as A2/B-5).
- U-R4 Tier re-taxonomy / task-YAML schema rewrite (destroys longitudinal comparability).
- U-R5 AGENTS.md wholesale rewrite in Fable-5 voice (benchmark-validated counters; ablate with data first — D2/D15).
- U-R6 Three-context topology as default (token overhead; validator separation adopted narrowly as A4).
- U-R7 Delete `benchmarks/framework/` + empty dirs (tidiness-only; rejected even as maintainability this cycle).

**Attestation:** this plan contains **zero stylistic changes**. Slice tally: correctness 5 (A1, A2, A3, A5, + A4's correctness face), capability 3 (A4, A6, A7), maintainability 0 in Track A (B-1 is the single maintainability item, owner-gated because it rides the live boot path). The rewrite urge is confined to the rejected block above.

## 5. Rollback plan

1. **Branch-level:** all code/doc changes live on `rebase/upgrade-2026-07-02`; `main` never advances during this cycle. Full abort = leave branch unmerged (or delete it); working tree and fenced files are untouched by construction.
2. **Per-slice:** each slice is one revertible commit (or a deletable new untracked file: `config.yaml`, generated status, experiment outputs). Revert command recorded in the slice's commit message.
3. **Run artifacts:** new benchmark/campaign runs are additive gitignored dirs, deletable without trace on the tracked tree; they never overwrite February artifacts (the hash manifest proves non-mutation — re-verify manifest after every slice).
4. **Live-session safety:** no Track-A slice modifies anything the live session reads (`AGENTS.md`, `CLAUDE.md`, `skills/`, `.claude/*`, `.mcp.json`); therefore no rollback can be needed on the live surface until Track B, where each B-item carries its own owner-approved revert (B-2: restore hashed prior values from the manifest).
5. **Escalation:** manifest mismatch at any checkpoint, gate FAIL, or any accidental fenced-file contact ⇒ stop all slices, record in `final_upgrade_record.md`, notify owner.

## 6. Six-file update rule

After **every merged slice** (and at cycle end regardless):
- `six-files/CURRENT_STATE.md` — reflect the new factual state (e.g., "harness runnable via config.yaml", "model identity recorded as of run X").
- `six-files/EVALS.md` — append the slice's named-eval result to Historical results (append-only; suite version bumps only if task text changes).
- `six-files/REASONING_DEBT.md` — move paid-down items to Resolved with a pointer to the evidence (never delete).
- `six-files/DECISIONS.md` — new index row (+ ADR if consequential) for each accepted change, with model provenance `claude-fable-5` and revisit triggers.
- `six-files/ASSUMPTIONS.md` — flip status on any assumption a slice validated/refuted (e.g., A-04 binaries-run after A2's probe).
- `final_upgrade_record.md` §4 — slice outcome (merged/reverted/blocked), cost observed.
The fenced status docs are **never** the target of these updates.

## 7. Execution order and dependencies

```
A0 (branch + gate)
 ├─ gate FAIL ⇒ STOP (package still lands)
 └─ gate PASS
     ├─ A1 (model pin) ──┐
     ├─ A2 (runnability) ─┼─ A6 (tier-slice re-baseline) ─→ informs B-3 / D2-ablation decision
     ├─ A3 (status gen)   └─ A7 (forced-kill resume)
     ├─ A4 (validator replay) ─→ informs B-3b funding
     └─ A5 (lint prototype) ─→ activation deferred to B-2
Track B items: independent, each strictly owner-gated; B-7 (archive rescue) is time-sensitive only in that backups age out.
```
