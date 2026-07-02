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
| ADR-101 | Pin + record model identity end-to-end | 2026-07-02 | Sean (proposed) | claude-fable-5 | Proposed (Slice A1) | H | Easy | below |
| ADR-102 | Status/dashboards generated from artifacts, never retyped | 2026-07-02 | Sean (proposed) | claude-fable-5 | Proposed (Slice A3) | H | Easy | below |
| ADR-103 | Restore runnability via new untracked config + live probe; live-session surface deferred to owner | 2026-07-02 | Sean (proposed) | claude-fable-5 | Proposed (Slice A2/B-2) | H | Easy | below |

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
