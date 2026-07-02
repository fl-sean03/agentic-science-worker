<!-- CANONICAL LIVE COPY as of 2026-07-02: promoted from 08_upgrades/upgrade-2026-07-02/six-files/ (that copy is the frozen cycle record; update THIS one going forward). Promotion: rebase-2026-07-02 S7, model claude-fable-5. docs/ is gitignore-scoped; docs/rebase/ is explicitly tracked (ADR-106, owner review at B-6). -->
# Decisions — Agentic Science Worker (1-ScienceAgent)

**Last reviewed:** 2026-07-02  ·  **Reviewing model:** claude-fable-5

Provenance note on the "Model" column: **no artifact in this repo records which model made or ratified any pre-2026-07 decision.** "opus-4-8-era" below means "attributed to the predecessor era from the rebase brief + commit dates"; earlier entries (January) may be an earlier Opus/Sonnet era — evidence does not distinguish. This unrecorded provenance is itself a decision defect (D14/ADR-101). Stage-C classifications live in `../historical_decision_review.md` and are cross-referenced, not restated as truth.

## Decision index

| ID | Decision | Date | Owner | Model | Status | Conf. | Rev. | Revisit trigger (short) |
|----|----------|------|-------|-------|--------|-------|------|-------------------------|
| D1 | Skill-only, no-orchestration architecture ("the agent IS the scaffolding") | 2026-01-29 | Sean | opus-4-8-era (unrecorded) | Accepted; Stage-C: **validated** (substrate) | H | Hard | A restraint-class incident that prose fails to prevent; or mechanical gates outperform in evals |
| D2 | AGENTS.md persona + anti-failure-mode prose counters | ≤2026-02-20 | Sean | opus-4-8-era | Accepted; Stage-C: **contextually-valid-outdated** (+stale skills table = incorrect fragment) | M | Easy | **A new model era (NOW)** → ablation experiment before trimming |
| D3 | Hybrid rule+LLM-judge grading, per-tier thresholds 70→35, self-graded | 2026-01→02 | Sean | opus-4-8-era | Accepted; Stage-C: **weakly-supported** | M | Mod | Grader trust study (U-05/B-3b) results |
| D4 | Layer A′: orchestration safety as agentic reasoning, not linting | 2026-05-10 (`e814b4c`) | Sean | opus-4-8-era | Accepted; Stage-C: **validated as response; effectiveness unresolved** | M | Easy | Any new runaway incident; or hydrogenation artifacts showing catches/misses |
| D5 | Compute-validation gates (Layer A physics; Layer B smoke-as-measurement) | 2026-05-06 (`ac2f6bc`) | Sean | opus-4-8-era | Accepted; Stage-C: **weakly-supported in-repo** | M | Easy | First in-repo Ring-2-style eval (B-4) |
| D6 | Campaign state = durable WORKFLOW.md + stateless tick agents | 2026-05-05 (`1e1e195`) | Sean | opus-4-8-era | Accepted; Stage-C: **weakly-supported; convergence-validated** | M | Easy | Forced-kill resume test (Slice A7) |
| D7 | Alpine access via DTN (key-only, no Duo) | 2026-06-21 (`baaa4fd`) | Sean | opus-4-8-era | Accepted; Stage-C: **validated** (liveness to re-verify) | H | Easy | Key expiry / facility policy change / off-campus operation |
| D8 | ALCF onboarding docs-first; OTP honesty; ControlMaster-only scripting | 2026-05-28 (`8e00ba8`) | Sean | opus-4-8-era | Accepted; Stage-C: **validated content; status unresolved** | H | Easy | Account approval lands; allocation expiry 2026-11-28 |
| D9 | Archive HPC tiers T5/T6/T11 (CURC access blocked) | 2026-02-20 | Sean | opus-4-8-era | Accepted; Stage-C: **contextually-valid-OUTDATED** — blocker removed by D7 | H (then) | Easy | **Triggered now**: revival = Track B-4 |
| D10 | Host project-update Tier-1 engine in this repo | 2026-05-29 (`5c99011`) | Sean | opus-4-8-era | Accepted; Stage-C: **validated design, operationally thin** | M | Easy | LabSync architecture changes |
| D11 | Fresh-run + archive 211 pre-overhaul runs | 2026-02-24/25 | Sean | opus-4-8-era | Executed; Stage-C: **execution INCORRECT/unresolved — archive vanished** | — | — | Backup catalog search (Track B-7) |
| D12 | Manual dashboards/README as the status record | 2026-01→02 | Sean | opus-4-8-era | Accepted; Stage-C: **incorrect** (self-corrupting; ≥9 divergent rows) | L | Easy | Superseded by ADR-102 direction (generation-from-artifacts) |
| D13 | Claim "Theorizer MCP integration validated" | 2026-02-25 | — | opus-4-8-era | Stage-C: **incorrect as stated** (integration was CLI-level; MCP "Planned") | — | — | If MCP server is actually built |
| D14 | (By omission) unpinned model, no identity in artifacts | 2026-01 | — | opus-4-8-era | Stage-C: **incorrect** | — | Easy | Superseded by ADR-101 (Slice A1) |
| D15 | Benchmark-driven prompt-fixing doctrine (verbose checklists) | 2026-02 | Sean | opus-4-8-era | Accepted; Stage-C: **contextually-valid-outdated** | M | Easy | New model era (NOW) → D2 ablation covers it |
| D16 | Multi-runtime portability (aider/codex/cursor backends) | 2026-01-22 (`8bd1d6a`) | Sean | opus-4-8-era | Accepted; Stage-C: **weakly-supported, trending obsolete** | L | Easy | **Owner question** (Track B-9), not an experiment |
| D17 | Showcases as curated capability evidence | 2026-02 (`c3ed9c9`) | Sean | opus-4-8-era | Accepted; Stage-C: **weakly-supported** (source artifacts vanished; owner's own fenced disclaimer) | L | Easy | Re-derivation of top cathode candidate (Track B-9) |
| D18 | `.gitignore` CRASH debris instead of cleaning; empty scaffolding dirs | 2026-01→02 | — | opus-4-8-era | Stage-C: **obsolete/incorrect habit** | — | Easy | Lint prototype (Slice A5) addresses the underlying class |
| R-01 | REJECT WORKFLOW.md→JSONL ledger migration (U-R1) | 2026-07-02 | rebase | claude-fable-5 | Accepted (rejection) | H | Easy | Evidence WORKFLOW.md fields insufficient in a real campaign |
| R-02 | REJECT constitution file, tier re-taxonomy, adapter monopoly, 3-context default, AGENTS.md rewrite, framework/ deletion (U-R2..R7) | 2026-07-02 | rebase | claude-fable-5 | Accepted (rejections) | H | Easy | Per-item: see uplift register; standing trigger = a *measured* failure the rejected form would have prevented |
| ADR-101 | Pin + record model identity end-to-end | 2026-07-02 | Sean (supervised) | claude-fable-5 | **Executed** (Slice A1/S1, EV-A1 PASS) | H | Easy | below |
| ADR-102 | Status/dashboards generated from artifacts, never retyped | 2026-07-02 | Sean (supervised) | claude-fable-5 | **Executed** (Slice A3/S3, EV-A3 PASS; adoption as record = B-6) | H | Easy | below |
| ADR-103 | Restore runnability via new untracked config + live probe; live-session surface deferred to owner | 2026-07-02 | Sean (supervised) | claude-fable-5 | **Executed** (Slice A2/S2, EV-A2 PASS with A-04 refuted; B-2 still owner-gated) | H | Easy | below |
| ADR-104 | EVALS suite v1.1: E-05 reference data relocated out of the excluded `08_upgrades/` tree; gate outcome NOT re-scored | 2026-07-02 | Sean (supervised) | claude-fable-5 | **Executed** (S6) | H | Easy | below |
| ADR-105 | Standing proposal gate: behavioral/operating-surface changes require owner sign-off; benchmark A/B alone is insufficient | 2026-07-02 | Sean (supervised) | claude-fable-5 | **Executed** (S8, `../proposals/PROPOSAL_GATE.md`) | H | Easy (owner can dissolve) | below |
| ADR-106 | `.gitignore` `docs/` hide-rule scoped to `docs/*` with explicit re-includes so the rebase record set (`docs/rebase/`, path-migration note) is tracked | 2026-07-02 | Sean (supervised) | claude-fable-5 | **Executed** (S5) | M | Easy | Owner review before any push (B-6): docs/ was hidden from the public repo on purpose; untrack if that intent extends to the rebase records |
| ADR-107 | `--verify`'s automatic SSH probe to cu_alpine made opt-in (`SW_VERIFY_HPC=1`) — no unattended external actions from a default verify | 2026-07-02 | Sean (supervised) | claude-fable-5 | **Executed** (S2) | H | Easy | B-4 owner session may prefer it default-on for HPC eras |

## Full records

### ADR-101: Pin and record model identity in executor, grader, and result artifacts
**Status:** Proposed · **Date:** 2026-07-02 · **Decision owner:** Sean · **Agent/model involved:** claude-fable-5 (proposer)
**Problem:** No `--model` flag in `backends/claude.py` or `llm_grader.py`; no model field in any of 97 `result.json`. Every historical score means "whatever `claude` resolved to that day." The fleet model swap makes this acute: the February baseline is era-ambiguous forever, and any new run is incomparable by construction.
**Constraints at the time (of the original omission):** subscription-CLI usage; single-model world; benchmark suite young. All three have changed.
**Evidence:** code inspection (Stage B, confirmed Stage C); artifact absence across all 97 result.json.
**Alternatives:** (1) leave unpinned and log CLI version only — insufficient, model still ambiguous; (2) pin in a wrapper script — fragile, bypassable; (3) pin + record in-band (chosen).
**Decision:** add `--model claude-fable-5` (parameterized) to executor and grader spawns; add `model`, `grader_model`, `cli_version` to result.json.
**Confidence:** High. **Reversibility:** Easy (two-file revert).
**Validation condition:** EV-A1 — one run artifact carrying all three fields.
**Revisit triggers:** a materially more capable model becomes available (re-pin deliberately, never silently); harness backend abstraction changes; Anthropic CLI changes flag semantics.

### ADR-102: The status record is generated from result artifacts, never hand-transcribed
**Status:** Proposed · **Date:** 2026-07-02 · **Decision owner:** Sean · **Agent/model involved:** claude-fable-5
**Problem:** ≥9 confirmed row-level divergences between dashboards and result.json (both directions, incl. T12 78/68/75 vs artifact 59/90/72), stale tables under updated summaries, committed README overstating by 18 points, and the "regression" narrative resting on markdown whose source artifacts vanished. The record self-corrupts under manual transcription.
**Constraints:** fenced files must not be edited; the generator writes a NEW file; adoption as the canonical record is an owner decision (Track B-6).
**Evidence:** Stage-C byte-level artifact re-tally (80/97, 82%).
**Alternatives:** (1) keep manual practice with more care — the practice already failed under care; (2) delete dashboards — loses the product surface; (3) generate mechanically (chosen).
**Decision:** `generate_status.py` → `GENERATED_STATUS.md`, numbers by reference; divergences flagged, never absorbed.
**Confidence:** High. **Reversibility:** Easy (delete script+output).
**Validation condition:** EV-A3 — generated tally equals independent Stage-C tally; all 9 known divergences flagged.
**Revisit triggers:** result.json schema changes; a more capable model makes rubric-graded prose summaries trustworthy enough to auto-draft (they still cite generated numbers).

### ADR-103: Runnability restored via new untracked `config.yaml` + live probe; live-session env deferred
**Status:** Proposed · **Date:** 2026-07-02 · **Decision owner:** Sean · **Agent/model involved:** claude-fable-5
**Problem:** all binary env paths dead post-reorg (twice now: LabWork → Workspace/main → work/); system cannot run local sims or `--verify`; docs rot but were trusted.
**Constraints:** `.claude/settings.json` and `.mcp.json` are read by the live session and hold a key → owner-gated (B-2). Binaries exist at `/home/sf2/work/compute/gpu-tests/1-GPUTests/...` but post-rebuild execution is unverified.
**Evidence:** Stage B/C path checks; two historical reorg-rot episodes.
**Alternatives:** (1) edit settings.json directly — touches live surface, repeats the hardcode pattern; (2) universal adapter layer — rejected as U-R3 (new rot surface); (3) minimal indirection + probe-not-trust (chosen — the one greenfield mechanism that binds to observed damage).
**Decision:** new gitignored `config.yaml`; `harness.py --verify` gains a live probe (binary exists AND executes, GPU visible, keys present); probe reports, never assumes.
**Confidence:** High. **Reversibility:** Easy.
**Validation condition:** EV-A2 — `--verify` passes; BENCH-T1-001 completes with `Loop time`.
**Revisit triggers:** any future path/machine reorganization (probe should catch it same-day); adoption of a fleet-wide env convention.
**Execution note (2026-07-02):** `--verify` exit 0; smoke satisfied via a direct LJ-melt run (`Loop time` present) on `/home/sf2/builds/lammps/build/lmp` rather than the full BENCH-T1-001 agent run (agent-path already exercised by EV-A1). Probe refuted A-04: gpu-tests binaries present-but-not-executable.

### ADR-104: EVALS v1.1 — fix the E-05 authoring defect without re-scoring the gate
**Status:** Executed (S6) · **Date:** 2026-07-02 · **Decision owner:** Sean (supervised execution) · **Agent/model involved:** claude-fable-5
**Problem:** E-05 v1 instructed candidates to execute a script under `08_upgrades/`, which the candidate's standing rules exclude as answer-key material. The candidate's principled decline scored 0 (key = "matches re-derivation"), single-handedly failing the tool-use bar. The defect is in the suite, not the model — but the recorded FAIL stands because bars are bars.
**Decision:** relocate the generator to `benchmarks/fixtures/reference_test_data/generate_log.py` (byte-identical output, seed 42, verified); bump suite v1 → v1.1; record the defect, the FAIL, and the head-to-head in Historical results verbatim; do NOT re-run or re-score.
**Alternatives:** (1) carve a documented exception keeping the old path — leaves a rule-conflict trap armed; (2) re-run E-05 now and revise the gate — self-serving re-scoring by the same model family, rejected.
**Confidence:** High. **Reversibility:** Easy.
**Revisit triggers:** next gate run (uses v1.1); any future suite change must re-derive the environment-dependent keys (E-01/E-02/E-04) noted in EVALS.md.

### ADR-105: Behavioral/operating-surface changes require owner sign-off — benchmark A/B alone is insufficient
**Status:** Executed (S8; standing rule doc at `../proposals/PROPOSAL_GATE.md`) · **Date:** 2026-07-02 · **Decision owner:** Sean · **Agent/model involved:** claude-fable-5
**Problem:** E-06 showed both candidate AND incumbent proposing AGENTS.md behavioral rewrites gated only on benchmark validation, omitting the owner gate. The failure mode is model-independent: an agent optimizing measured behavior will happily rewrite its own operating surface if a benchmark blesses it.
**Decision:** operating-surface changes (AGENTS.md, CLAUDE.md, skills/* the live agent executes from, `.claude/*`, `.mcp.json`, config defaults) are staged as exact-diff proposals with expected effect + eval plan + explicit APPROVAL line; they are never hot-applied, regardless of eval results.
**Confidence:** High. **Reversibility:** Easy (owner can dissolve the rule).
**Revisit triggers:** owner delegates a bounded operating-surface authority in writing; or the proposal backlog demonstrably rots (then renegotiate the gate, don't bypass it).
