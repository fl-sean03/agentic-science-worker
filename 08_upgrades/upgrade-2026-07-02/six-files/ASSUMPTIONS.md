# Assumptions & Open Questions — Agentic Science Worker (1-ScienceAgent)

**Last reviewed:** 2026-07-02  ·  **Reviewing model:** claude-fable-5

## Assumption registry

| ID | Assumption | Type | Conf. | Blast radius if false | How to test | Owner | Status |
|----|-----------|------|-------|----------------------|-------------|-------|--------|
| A-01 | The February benchmark record measures agent capability (not mostly prompt fit + grader variance of one unrecorded model) | eng | L | **H** — every capability claim, the showcase narrative, and the "regression" story become unusable as a baseline; U-04 comparisons mislead | Slice A6 + grader study B-3b decompose model vs grader variance | rebase | open |
| A-02 | Fable 5 meets or exceeds Opus-era behavior on this project's task styles without the verbose-checklist prompt crutches | eng | M | **H** — if false, AGENTS.md counters are load-bearing and doc-trimming (B-1) would degrade the agent; A6 regression triggers the D2 ablation | Slice A6; then D2 ablation (counters present vs ablated, pinned model, N≥3) | rebase | open |
| A-03 | LLM-judge scores are comparable across runs/days (grader stability) | eng | L | **H** — all longitudinal comparisons, incl. "T10-001 regressed 75→5", are noise if false | U-05/B-3b: two-grader agreement + test-retest on preserved workspaces | rebase | open |
| A-04 | The gpu-tests binaries (`lmp`, `pw.x`) actually *execute* on the rebuilt bare-metal machine (driver 580-open/CUDA 12.8) | eng | M | **H** — Slices A2/A6/A7 and all local capability claims blocked; may need toolchain rebuild | A2 probe: run each binary on a 10-s input, not just `test -x` | rebase | **REFUTED 2026-07-02** (A2 probe executed them: `libmpi.so.40` missing; hang under ~/hpc-sdk hpcx env). Mitigation: LAMMPS via `/home/sf2/builds/lammps/build/lmp` (executes, smoke-verified); QE locally unavailable; gpu-tests toolchain repair → owner queue |
| A-05 | Alpine DTN key-only access is live today (key unexpired, machine on CU campus network, facility policy unchanged since 06-21) | eng | M | M — Track B-4 and the entire unattended-HPC story blocked; compute-strategy routing table wrong | Owner-sanctioned `ssh cu_alpine 'sinfo -p atesting_a100'` | owner | open — **incidental evidence 2026-07-02**: the harness's legacy auto-SSH check (since gated off) connected to `cu_alpine` and found `squeue`; connection-level liveness confirmed, partition/queue access still unverified |
| A-06 | ALCF account `sefl-alcf` has been approved since 2026-05-28 | eng | L | M — Polaris/Crux planning moot until approved; allocation clock (expires 2026-11-28) burns regardless | Portal check / `sbank-list-allocations` in first human session | owner | open |
| A-07 | Vast.ai account (balance ~$25 as of Feb), MP API key, S2 key, conda envs survived dormancy + rebuild | eng | M | M — cloud tier and literature/database skills fail at first use | A2 probe reports each (read-only checks) | rebase | open — **partially probed 2026-07-02**: conda env `science-tools` (per `environments/science-tools.yml`) no longer exists (harness ran under `dap4-showcase`); keys/Vast unverified (no external calls made) |
| A-08 | The vanished 3.2 GB pre-overhaul archive is recoverable from restic/ZFS backup tiers | eng | L | M — if false, Opus-era baseline artifacts are permanently lost; historical claims stay markdown-only | Backup catalog search (`~/work/ops/infra-consolidation/`) | owner | open |
| A-09 | Synthetic fixtures (seeded generator logs, injected queue statuses) predict behavior on live systems | eng | M | M — Ring-0-style evals could pass while live behavior fails | One paired task: same analysis on synthetic vs real LAMMPS log (after A2) | rebase | open |
| A-10 | `workspaces/` (1.6 GB, gitignored, this machine only) is a sufficient evidence base for the project's public claims | eng | L | M — single-disk loss destroys claim-to-evidence chain (already happened once: D11) | Hash manifest (done) + owner backup-policy decision | owner | open — partially mitigated 2026-07-02 |
| A-11 | Announced-vs-natural behavioral tasks: only *natural/hidden* variants measure real behavior in a 2026 model | domain/eng | M | L-M — headline behavioral scores inflated if announced tests kept in aggregate | Compare announced (T16-003) vs hidden (T16-013) pass patterns under Fable 5 | rebase | open |
| A-12 | Owner still wants multi-runtime portability (aider/codex/cursor) | eng | L | L — dead scaffolding either way; affects harness backend design | Ask (Track B-9) | owner | open |
| A-13 | The live agentctl session reads AGENTS.md/CLAUDE.md/skills from this repo as its operating surface (basis for Track A/B split) | eng | H | M — if it reads elsewhere, the Track boundary is miscalibrated (too conservative — safe direction) | Owner confirms session config | owner | open |
| A-14 | Physics anchors in eval_seed.md (Rahman D window, TIP4P density, Cu a=3.615 Å, Si gap character, Al α, H-in-Pd octahedral) are correct as stated | domain | H | M — eval grading wrong if any anchor wrong | Spot-check primaries before first gate run (curator already flagged #2's −213 kcal/mol estimate for direct recomputation) | rebase | open |
| A-15 | Compute trio doctrine (validated only in *other* projects' campaigns, e.g. hydrogenation post-incident) transfers to in-repo benchmark coverage | eng | M | M — B-4 task design may mis-specify what "good" looks like | First in-repo Alpine round-trip graded against the doctrine's own templates | rebase | open |

## Unresolved questions
- Q-01 — What model actually produced the February results? (Unrecorded; probably unanswerable — the permanent cost of D14.)
- Q-02 — Why did the pre-overhaul archive vanish — reorg casualty, disk cleanup, or moved off-machine? (Determines whether B-7 recovery is possible.)
- Q-03 — Was the 2026-05-09 hydrogenation runaway's Layer A′ response ever *exercised* — has ORCHESTRATION_CHECK.md caught anything since? (Evidence lives in the hydrogenation repo, not here.)
- Q-04 — Do the three undocumented `workspaces/projects/` side repos (parallel-lammps-hpc, allocation-scheduler, lammps-benchmarks) contain owner-valued work that should be surfaced or archived? (Post-doc discovery item; owner call.)
- Q-05 — What is the real cost (tokens + $ + hours) of a full suite run under Fable 5? (A6 slice extrapolates; needed before B-3 sign-off.)
- Q-06 — Is `benchmarks/framework/` truly superseded by `evaluation/`, or does anything still import it? (Low stakes; blocks nothing.)

## Confidence map (the beliefs the project leans on hardest)
- **"The agent IS the scaffolding" (D1)** → High for judgment-domain durability (survived two reorgs while all mechanism rotted) → but Low that it extends to *restraint* at the money/self-propagation boundary (2026-05-09 incident is a counterexample).
- **"The February suite proves the capability envelope"** → Low-Medium: artifact-backed for pass/fail counts, but model-unattributed, self-graded, and variance-confounded (A-01/A-03).
- **"Unattended multi-day campaigns work"** → Low: designed (D6), never certified; T7-001 is the only long-horizon datapoint and it stalled. Slice A7 is the test.
- **"Alpine DTN gives a real unattended HPC path" (D7)** → Medium-High on design and June verification; unknown liveness today (A-05).
- **"Doc claims can be trusted"** → **Refuted** as a class (D12): every load-bearing number must be re-derived from artifacts. This is the operative posture for all successor work.
