<!-- CANONICAL LIVE COPY as of 2026-07-02: promoted from 08_upgrades/upgrade-2026-07-02/six-files/ (that copy is the frozen cycle record; update THIS one going forward). Promotion: rebase-2026-07-02 S7, model claude-fable-5. docs/ is gitignore-scoped; docs/rebase/ is explicitly tracked (ADR-106, owner review at B-6). -->
# Current State — Agentic Science Worker (1-ScienceAgent)

**Last reviewed:** 2026-07-02  ·  **Reviewing model:** claude-fable-5
**Source of truth for live status:** `CLAUDE.md` (2026-05-06) + git log. `AGENTS.md` is the agent persona/primary context but its status content is stale (2026-02-20; skills table lists archived `hpc-cluster`, omits all five post-February skills). `benchmarks/CURRENT_STATUS.md` is the dashboard, frozen 2026-02-25 with uncommitted fenced edits, and contains ≥9 artifact-divergent rows — do not treat it as a record without artifact cross-check.
*(Descriptive file. Ratified from the Stage-B audit §11 draft with Stage-C artifact corrections applied: T12 scores are 59/90/72, T7-002/003 are 64/58, T8-005 is a timeout.)*

## 2026-07-02 Track-A slice update (supervised execution, branch `rebase/upgrade-2026-07-02`)

Facts below supersede the matching statements later in this file (kept for the record):

- **Model identity is now pinned and recorded** (Slice A1): executor and grader spawns carry `--model`; `result.json` gains `model`/`grader_model`/`cli_version`. First attributed artifact: `BENCH-T13-007-20260702-162253` (claude-fable-5, 96/100 passed).
- **`harness.py --verify` passes again** (Slice A2) via untracked `config.yaml` + a live-execution probe (binaries are RUN, not stat-ed). Working LAMMPS: `/home/sf2/builds/lammps/build/lmp` (22Jul2025-U4; LJ smoke completes with `Loop time`).
- **A-04 refuted:** the gpu-tests binaries at `/home/sf2/work/compute/gpu-tests/1-GPUTests/` exist but DO NOT execute (missing OpenMPI-4 runtime; hang under ~/hpc-sdk hpcx env). QE (CPU+GPU) is therefore still unavailable locally. Toolchain repair = gpu-tests project, owner queue.
- **Status is now generatable from artifacts** (Slice A3): `benchmarks/evaluation/generate_status.py` → `benchmarks/results/GENERATED_STATUS.md` (80/12/5 of 97; 52 dashboard divergences flagged) + `RECONCILIATION_2026-07-02.md`. Fenced owner docs untouched.
- **CRASH class linted** (Slice A5): `scripts/lint_sim_input.py` + tests (8/8). Hook activation = proposal (B-2).
- **Machinery dead paths repaired** (22 files; `docs/PATH_MIGRATION_2026-06-13.md`). Still dead by design (operating surface → `08_upgrades/upgrade-2026-07-02/proposals/`): `.claude/settings.json`, `.mcp.json`, `SESSION_HANDOFF.md`, `.claude/agents/simulation-runner.md`, 4 skill pages, `AGENTS.md` skills table.
- **Model gate:** FAIL per the declared absolute bars as written; head-to-head favored the candidate 13.0 vs 12.5 (E-05 loss = suite authoring defect, fixed in EVALS v1.1; E-06 restraint miss shared identically by the incumbent → answered with `proposals/PROPOSAL_GATE.md`). Owner authorized supervised, fenced Track-A execution only.
- **Not executed this cycle:** A4 (validator replay), A6 (tier-slice re-baseline), A7 (forced-kill resume) — deferred to the owner queue with the gate story attached.

## System map
- `AGENTS.md` (829 lines) — researcher persona, 6 Core Principles, anti-failure-mode sections; primary context for any coding agent. `CLAUDE.md` wraps it for Claude Code and indexes skills, including the "compute trio".
- `skills/` (symlinked at `.claude/skills`) — all domain capability as markdown, two generations:
  - Jan–Feb researcher skills: lammps-simulation, quantum-espresso, mlip-simulation, vast-cloud, literature-search, materials-database, data-analysis, resource-acquisition, theory-synthesis, ggen, torch-sim.
  - Mar–Jun operations skills: iff-parameters (03-26); compute-strategy w/ backends local/vast-ai/alpine/polaris/crux (05-05 → 06-21); compute-validation incl. Layer A′ orchestration safety (05-06/10); campaign-orchestration (05-05); project-update + stdlib Python engine w/ pytest suite (05-29, hosted here for use in *other* repos — no `.sync/` manifest exists here, by design).
  - `skills/archive/hpc-cluster-curc/` — retired CURC skill (archived 2026-02-20 for *access* reasons; blocker since removed by the Alpine DTN path).
- `benchmarks/` — 117 task YAMLs (98 active; tiers 1–4, 7–10, 12–18; 5/6/11 archived), harness `evaluation/harness.py` (spawns `claude -p --dangerously-skip-permissions`, **model unpinned**, no model field in artifacts), rule grader + LLM judge (`llm_grader.py`, also unpinned `claude -p`), per-tier pass thresholds 70→35, parallel runner (6 workers stable, 10 OOM), `vast_safety.py` postflight. Older `benchmarks/framework/` (CLEAR metrics) appears superseded by `evaluation/`. Frozen since 2026-02-25.
- `workspaces/` (1.6 GB, gitignored) — agent work dirs from the 2026-02-24/25 fresh run; 3 undocumented side projects with own `.git` under `projects/` (parallel-lammps-hpc, allocation-scheduler, lammps-benchmarks); resource caches; tracked `examples/`.
- `showcases/` (64 MB) — 6 curated best runs (novel-cathode discovery, XRD structure determination, etc.); fenced uncommitted README note adds a run-to-run variability disclaimer.
- `.claude/` — untracked `settings.json` (env for LAMMPS/QE binaries — **all paths dead post-2026-06-13 reorg**; also holds MP API key in plaintext), 2 hooks (pre-Bash safety regex; post-Write/Edit logging → `logs/operations.log`), 3 subagent defs. `.mcp.json`: playwright, semantic-scholar, filesystem (root = dead pre-reorg path).
- `internal/`, `research/`, `docs/`, `examples/` — vision/strategy, benchmark methodology, design philosophy ("the agent IS the scaffolding"), canonical behavior patterns/anti-patterns.
- Debris: `CRASH` + `input_tmp.in` (repo root and `benchmarks/`, 2026-01-17) — QE empty-input fossil, `.gitignore`-d rather than removed.
- Siblings (out of repo, fenced): `../asta-paper-finder`, `../asta-theorizer` (Theorizer drives T12 via CLI; its MCP server was never integrated despite doc claims).

## Current capabilities
- **Verified in the 2026-02-24/25 era** (model unpinned, presumed Opus-4-8-era; artifacts in `benchmarks/results/runs/`): LAMMPS MD, QE DFT on local RTX 5080, MLIP screening, Vast.ai full lifecycle, LAMMPS log/MSD analysis, theory synthesis via Theorizer (T12 3/3 at artifact scores 59/90/72), behavioral/rigor tiers largely passing. Fresh-run aggregate (artifact-verified): **80 passed / 12 failed / 5 timeout of 97 (82%)**. High variance on frontier tiers; the "regressed from 75/72" baselines are markdown-only (source artifacts lost with the vanished pre-overhaul archive).
- **Defined but NOT validated end-to-end in this repo:** compute-strategy routing to Alpine (DTN key-only) and ALCF Polaris/Crux (account pending as of 2026-05-28; OTP-gated); compute-validation smoke gates; campaign-orchestration WORKFLOW.md ticking; project-update engine (unit tests pass claim untested here). Zero benchmark coverage of the entire Mar–Jun operations layer.
- **NOT currently runnable as configured:** any local simulation and `harness.py --verify` — every binary env path in `.claude/settings.json` points to pre-reorg locations. The binaries exist at `/home/sf2/work/compute/gpu-tests/1-GPUTests/{md-lammps/install/bin/lmp, dft-qe/build-{cpu,gpu}/bin/pw.x}` (path existence re-verified 2026-07-02; post-rebuild *execution* unverified).

## Data / artifacts inventory
- `benchmarks/results/runs/` — 97 fresh-run dirs (result.json + benchmark.json + transcript) + parallel-run logs. Gitignored. Hash-manifested at `08_upgrades/upgrade-2026-07-02/baseline/hash_manifest.sha256`.
- `workspaces/benchmarks/` — corresponding agent work dirs (bulk of 1.6 GB). Gitignored.
- `benchmarks/results/examples/`, `workspaces/examples/` — small tracked exemplars.
- `showcases/*/outputs/` — curated evidence for headline claims (64 MB).
- **MISSING:** claimed pre-overhaul archive `benchmarks/results/archive/runs_20260224_pre_overhaul/` (3.2 GB, 211 runs) is not on disk anywhere — all pre-02-24 scores rest on markdown alone. Possibly recoverable from restic/ZFS backups (owner decision, Track B-7).
- `internal/validation/` — ggen/torch-sim validation results (2026-01-31).

## Active work (mirrored 2026-07-02, read-only)
- Dormant 2026-06-21 → 2026-07-02; woken for the intelligence rebase. A live agentctl session is UP; its only writes today were to the rebase ops area (per `logs/operations.log`). Do not interact.
- Fenced uncommitted owner edits (since 02-25): README/ROADMAP/CURRENT_STATUS fresh-run status corrections + showcases variability note + deletion of two Jan-17 result summaries. Snapshot preserved under `08_upgrades/upgrade-2026-07-02/baseline/`.
- 3 unpushed commits (`8e00ba8` ALCF backends, `5c99011` project-update, `baaa4fd` Alpine→DTN). GitHub shows none of the Mar–Jun era.
- Per ROADMAP TODOs (02-25): T9/T10 regression investigation, T17/T18 expansion, benchmark CI. Per the May–June commit arc: real compute campaigns (Alpine/ALCF) via the compute trio.

## Known failures (observed, reproducible)
- Local execution broken as configured (dead paths; 35 files reference pre-reorg roots incl. `.mcp.json`, `scripts/run_*.sh`, subagent defs).
- Frontier-tier run-to-run variance (T10-001 → 5, T10-002 → 17, T9-003 → 0, T9-004 → 8 on 02-25; earlier "passing" values unverifiable).
- T7-001 long-campaign stall at ~5 h (killed; partial workspace preserved).
- 5 fresh-run timeouts (T2-002, T4-005/006, T8-005, T17-004).
- Parallel runner OOM at 10 workers (6 stable).
- QE empty-input crash class (CRASH/input_tmp.in ×2, 2026-01-17) — never structurally addressed.
- Status-record drift: ≥9 dashboard rows diverge from artifacts (both directions); committed README overstates vs artifacts.

## External interfaces / dependencies
- `claude` CLI (executor AND grader; model unpinned — the central evidence-continuity defect), optional aider/cursor backends (never implemented beyond `claude.py`).
- LAMMPS + QE builds from `~/work/compute/gpu-tests/1-GPUTests/` (RTX 5080 local).
- Vast.ai CLI + prepaid account (~$25 as of Feb; unverified); Materials Project API (key in `.claude/settings.json`); Semantic Scholar MCP; Playwright MCP.
- CU Alpine via `dtn.rc.colorado.edu` (`ssh cu_alpine`, user `sefl7948`, key-only, no Duo; campus-network dependent).
- ALCF Polaris/Crux: account `sefl-alcf` pending as of 2026-05-28; MobilePASS+ OTP (no unattended login); allocation HydrogenStorage 5k+20k node-hours, **expires 2026-11-28**.
- Sibling ASTA Theorizer/paper-finder (CLI-level); conda envs per `environments/*.yml` (liveness unverified post-rebuild).
- IFF parameter tooling (`~/work/tools/iff/`) via iff-parameters skill.
