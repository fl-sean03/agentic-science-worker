# Historical Decision Review — Agentic Science Worker (1-ScienceAgent)

**Role:** Adversarial Reviewer (Role 3, Stage C)
**Reviewing model:** `claude-fable-5`
**Date:** 2026-07-02

Classification vocabulary: **validated** | **contextually-valid-outdated** | **weakly-supported** | **obsolete** | **incorrect** | **unresolved**. Every non-validated row carries the settling evidence that would move it. "History changed my view" notes are marked ▲.

Central rule applied: prior decisions are not correct merely because they are implemented — but several here carry *documented incident or benchmark evidence*, which is exactly the inheritance that counts.

---

## D1. Skill-based, no-orchestration architecture ("the agent IS the scaffolding")

**Where decided:** `docs/DESIGN_PHILOSOPHY.md` v1.0 (2026-01-29); `CONTRIBUTING.md`; ROADMAP principle "Expand the toolkit, not the complexity".
**Classification: validated** (as the core substrate; not as a ban on all mechanism).
**Evidence:** (a) 80/97 artifact-verified passes across 15 tiers with zero orchestration code; (b) survivability — through two filesystem reorganizations every mechanical artifact rotted (35 dead-path files, dead `.claude/settings.json`, dead `.mcp.json` root) while the markdown-skill layer remained fully live and was the only layer still growing in May–June; (c) independent convergence — the blind Fable-5 greenfield, given only mission + constraints, re-derived "judgment in the model" as thesis #3.
▲ History changed my view: before reading `DESIGN_PHILOSOPHY.md` and observing the rot asymmetry, I read the absence of orchestration code as immaturity. The evidence says it is the most durable part of the system.
**Caveat that keeps this honest:** the philosophy's implicit corollary — "mechanical gates are unnecessary" — is *not* validated. The 2026-05-09 runaway (D4) and the money-leak class show reasoning-only discipline has an unbounded failure tail. The correct reading is "no orchestration code for *judgment*", not "no mechanism for *restraint*".

## D2. AGENTS.md persona + anti-failure-mode prose engineering

**Where decided:** AGENTS.md (iterated through 2026-02-20); commit `60363a6` "validate Core Principles approach"; T15-004 fix history (score 3 → 68 by restoring a verbose prompt, per `benchmarks/docs/IMPROVEMENT_METHODOLOGY.md` and SESSION_HANDOFF "Key Patterns Learned").
**Classification: contextually-valid-outdated.**
The counters ("Narrative ≠ Execution", "Preparation ≠ Completion", verbose completion checklists) were empirical responses to a specific 2026-January/February model's failure modes, validated by before/after benchmark scores *of that model*. Under Fable 5 the failure-mode distribution is unknown; some counters may be dead weight (context cost, instruction dilution), others still load-bearing.
**Also factually rotten:** the skills table (lines 578–593) lists archived `hpc-cluster` and omits all five post-February skills — an agent booting from the "primary context file" gets a February worldview (incorrect fragment inside a contextually-valid doc).
**Settling evidence:** re-run the behavioral tiers (T13/T15/T16) under pinned Fable 5 twice — once with current AGENTS.md, once with the anti-failure-mode sections ablated. Score delta per section settles what stays.

## D3. Benchmark methodology — LLM-judge + rule grader, per-tier thresholds, self-graded

**Where decided:** `benchmarks/evaluation/{harness.py,grader.py,llm_grader.py}`; `PASS_THRESHOLDS` (70 → 35 by tier); `docs/BENCHMARK_GRADING.md`.
**Classification: weakly-supported.**
Defensible parts: hybrid rule+rubric grading; numeric `expected_outputs` ranges anchored to external literature values; `IMPROVEMENT_METHODOLOGY.md`'s explicit "generalization over specificity" rule is a real, written defense against teaching-to-the-test; a crude variance protocol existed (SESSION_HANDOFF: run 3×, mean ≥ 65 with 2/3 passing).
Unsupported parts, all confirmed against artifacts: executor and judge are the same **unpinned** model with no recorded identity; the judge explores the executor's own workspace; grader reliability never measured despite a documented grader-defect history (metadata score-0 desync across 17 benchmarks; rubric-sum arithmetic error, `CURRENT_STATUS.md` Known Issues); score transcription into dashboards drifts (nine confirmed row-level divergences including T12 78/68/75 vs artifact 59/90/72). The "T9/T10 regressions = agent variability" conclusion is confounded with grader variance and is currently undecidable.
**Settling evidence:** regrade ~15 preserved fresh-run workspaces twice with a pinned grader (two-grader agreement + test-retest); compare rule-based vs LLM verdicts on the numerically-anchored subset.

## D4. Layer A′ — orchestration safety as "agentic reasoning, not linting"

**Where decided:** commit `e814b4c` (2026-05-10), full rationale in the commit body; `skills/compute-validation/workflows/orchestration-safety.md`, `tools/slurm-orchestration.md`, priors schema (`class`, `related_questions`, `generalization`).
**Classification: validated as design response; unresolved in measured effectiveness.**
▲ History changed my view sharply. Blind, this looks like over-engineered prose. The commit message reveals it is a post-incident control for a real, quantified failure: 2026-05-09, hydrogenation project — NAMD config bug + in-script sbatch resubmit + mail-on-fail = 8,366 jobs and ~16,000 emails in 24 h, which physics verification and smoke both structurally missed. The "reasoning, not linting" argument (novel failure modes have no lint rule; priors seed reasoning) is coherent and the four-guardrails principle (bounded counter, rate ceiling, failure ceiling, notification cap) generalizes.
**But:** no artifact in this repo shows Layer A′ *catching* anything since (its consumers are other projects' campaigns), and the guardrails themselves are encoded as knowledge, not enforced. The greenfield's point stands narrowly: for self-propagating submissions and metered money, the guardrail should also exist mechanically — a reasoning layer that failed once at 8,366 jobs argues for, not against, a hard counter.
**Settling evidence:** hydrogenation-project campaign artifacts (ORCHESTRATION_CHECK.md instances, incident-free submission counts since 2026-05-10).

## D5. Compute-validation gate (Layer A physics verification + Layer B smoke-as-measurement)

**Where decided:** commit `ac2f6bc` (2026-05-06); `skills/compute-validation/SKILL.md`.
**Classification: weakly-supported (in this repo).**
The doctrine is thoughtful, converges with the blind greenfield's validation-gate design, and has explicit anti-scope rules ("don't use for one-off scripts"). But zero benchmarks exercise it (T5/T6/T11 were archived before it existed), and no in-repo campaign artifact demonstrates a smoke extrapolation predicting production behavior. Its validation, if any, lives in other projects' workspaces.
**Settling evidence:** one Ring-2-style eval task — smoke → SMOKE_ANALYSIS.md → production on `atesting_a100`/`aa100` — graded on whether the extrapolation was made and was accurate.

## D6. Campaign-orchestration — stateless agents over durable WORKFLOW.md

**Where decided:** commit `1e1e195` (2026-05-05); `skills/campaign-orchestration/SKILL.md`.
**Classification: weakly-supported, design validated by convergence.**
The pattern (file-is-the-state-machine, tick agents, escalation flags, budget fields) is exactly the blind greenfield's ledger, independently derived — strong structural endorsement. What is missing is the endurance proof: T7-001 stalled at 5 h and was killed; no recorded campaign has survived a genuine mid-run session death and resumed from `WORKFLOW.md` alone.
**Settling evidence:** the forced-kill resume test (uplift U-07). Until then the flagship "works independently for days" claim is uncertified.

## D7. Alpine access strategy — repoint to DTN, key-only, no Duo

**Where decided:** commit `baaa4fd` (2026-06-21), rationale in commit body: the prior page's "ask the user to refresh Duo" was wrong for autonomous work; canonical writeup external at `~/.claude/skills/cu-hpc-access`.
**Classification: validated** (as of its date; liveness today unverified).
This is the single decision that makes any unattended-HPC story real: login node = password+Duo (unusable by an agent), DTN = CILogon key, full SLURM + mounts. The correction replaced a factually wrong instruction — a correctness fix, properly documented. Rot risks: campus-network dependence, key expiry, facility policy drift.
**Settling evidence (cheap):** one `ssh cu_alpine 'sinfo -p atesting_a100'` round-trip in an owner-sanctioned session.

## D8. ALCF onboarding strategy — docs-first, account pending, OTP honesty

**Where decided:** commit `8e00ba8` (2026-05-28); `backends/{polaris,crux}.md`.
**Classification: validated in content, unresolved in status.**
The pages are honest where it matters: unattended login impossible by policy (MobilePASS+ per connection), whole-node accounting ("always pack 4 replicas/node"), `-A HydrogenStorage` on every qsub, ControlMaster as the only scripted path. The blind greenfield reproduced this auth-tier model from the same facts — convergent validation.
**Unresolved externals:** account `sefl-alcf` was pending 2026-05-28, current state unknown; 5,000 (Polaris) + 20,000 (Crux) node-hours expire **2026-11-28** regardless. That expiry is a stated external deadline; how to act on it is the owner's call.
**Settling evidence:** ALCF account portal status; `sbank-list-allocations -p HydrogenStorage` on first human-opened session.

## D9. CURC/HPC tier archiving (T5, T6, T11)

**Where decided:** changelog 2026-02-20; skills moved to `skills/archive/hpc-cluster-curc/`; SESSION_HANDOFF "CURC access deferred - use VAST.ai instead".
**Classification: contextually-valid-outdated.**
▲ History settles the blind reconstruction's open question #9 ("why archived — the reason changes whether revival is capability work or waste"): the reason was *access*, not capability failure. That blocker has since been removed by D7 (June: key-only DTN with full SLURM). The archival decision was right in February and is stale now; the HPC-scale capability axis is revivable and is where the compute trio would finally get in-repo coverage.
**Settling evidence:** one revived T5-class task through `cu_alpine` (uplift U-06).

## D10. The Tier-1 project-update engine hosted in this repo

**Where decided:** commit `5c99011` (2026-05-29); `skills/project-update/SKILL.md` + `engine/project_update/` + `engine/tests/`; isolation invariant referencing `36-LabSync/docs/ADR-001`.
**Classification: validated in design, weakly-supported operationally.**
Deliberate, documented choices: stdlib-only, deterministic, no-LLM floor, manifest-driven, explicit two-tier ADR. A pytest suite exists (`engine/tests/test_{manifest,bundle,synthesis_items,yaml_lite}.py`). No `.sync/manifest.yaml` exists *here* — by design (this repo hosts the skill for use inside other repos), so "untested against this repo" is not a defect, merely a fact.
**Settling evidence:** run its own pytest suite (safe, isolated) and one `orient` invocation inside a manifest-bearing repo (e.g. hydrogenation).

## D11. Fresh-run + results-cleanup operation (2026-02-24/25)

**Where decided:** commit `c20436f`; `RESULTS_CLEANUP_ANALYSIS.md` (211 runs, 3.14 GB, keep-109/archive-102); ROADMAP changelog "Archived 3.2GB… to `benchmarks/results/archive/runs_20260224_pre_overhaul/`"; uncommitted deletion of two Jan-17 summary MDs.
**Classification: decision contextually valid; execution outcome INCORRECT / unresolved.**
The fresh-run-with-archival plan was sound. The outcome on disk is not what the plan says: the archive directory **does not exist anywhere on this machine**, and `results/runs/` holds only the 97 fresh-run dirs — so not even the "keep best + latest" 109-run set survived. Every pre-02-24 score (the "regression from 75/72" baselines, the 40+ historical LAMMPS passes, T10-004's earlier 85, the showcase source runs) now rests on markdown alone. Most plausible mechanism: the archive was casualty of the 2026-06-13 machine reorg or a disk cleanup; undetermined.
**Settling evidence:** owner recollection; restic/ZFS snapshot catalogs from the backup tiers (`~/work/ops/infra-consolidation/`) — the archive may be recoverable from backup history.

## D12. Status/documentation practice — dashboards, README claims, SESSION_HANDOFF

**Classification: incorrect** (as a record-keeping system), with the fenced working-tree edit being the honest correction that never landed.
Artifact-confirmed: committed README "81/86 (100%)" vs artifact truth 80/97 (82%); dashboard tier tables contradict artifacts in at least nine rows (both directions); ROADMAP header says 02-23 atop a 02-25 changelog; SESSION_HANDOFF asserts "78/86 (100%)", dead paths, and prohibitions ("don't run T12") superseded two days after it was written. The uncommitted 02-25 edits fix the headline numbers correctly (I re-derived 80/97 exactly) but sat unpushed for four months while GitHub showed the rosier stale claim.
**Settling evidence:** none needed — reproduced. The structural fix is generation-from-artifacts (uplift U-03), and the pending commit decision belongs to the owner (fenced).

## D13. "Theorizer MCP integration validated" (ROADMAP/CURRENT_STATUS 2026-02-25)

**Classification: incorrect as stated.**
`skills/theory-synthesis/SKILL.md` marks the MCP server "Planned"; `.mcp.json` has no theorizer entry; T12 ran through CLI-level integration with the sibling `../asta-theorizer`. The *capability* is real (T12 3/3 passed at artifact scores 59/90/72 — note: not the 78/68/75 the docs repeat); the *mechanism claim* is wrong.
**Settling evidence:** reproduced (skill line vs. doc claim vs. artifacts).

## D14. Unpinned model in executor and grader; no identity in artifacts

**Classification: incorrect** (accidental-by-default, per the audit's reading of the code — no flag, no field, consistent with subscription-CLI usage).
This decision-by-omission now costs the project its entire longitudinal evidence base at exactly the moment (model swap) such a base matters most. Even the February scores' model identity is unrecorded anywhere in-repo ("Opus-4.8-era" comes from the rebase brief).
**Settling evidence:** reproduced from code. Fix is uplift U-01.

## D15. Benchmark-driven prompt-fixing ("most failures are prompt issues, not code issues")

**Where decided:** ROADMAP "How to Contribute"; IMPROVEMENT_METHODOLOGY; SESSION_HANDOFF "Don't use condensed prompts — causes early termination".
**Classification: contextually-valid-outdated.**
It worked, measurably, for the February model (T15-004 3 → 68). It also blurred capability measurement with prompt engineering — several "passes" certify the *prompt*, not the agent, and the generalization rule only partially mitigates this. Under Fable 5, the verbose-checklist doctrine is an untested prior; blindly keeping it re-tunes the new model to the old model's crutches, and blindly dropping it risks regressions.
**Settling evidence:** the D2 ablation experiment covers this (checklist vs. condensed prompts on a task sample, pinned model, N ≥ 3).

## D16. Multi-runtime portability (AGENTS.md standard; aider/codex/cursor backends)

**Where decided:** commit `8bd1d6a` (2026-01-22); `configs/`; harness `--backend` flag.
**Classification: weakly-supported, trending obsolete.**
Only `backends/claude.py` was ever implemented; aider "integration ready, needs testing" since January; nothing since. AGENTS.md-as-standard costs little and is harmless; the backend abstraction is dead scaffolding. The blind greenfield rated this the single highest-leverage owner question (its Q10) — correctly.
**Settling evidence:** an owner answer, not an experiment.

## D17. Showcases as curated capability evidence

**Where decided:** commit `c3ed9c9`; `showcases/` (64 MB); fenced README note adding a variability disclaimer.
**Classification: weakly-supported.**
The showcased runs happened (workspace outputs exist), but their scores' source artifacts vanished with D11, and the headline discovery benchmark (T10-001, showcased at 75) scored 5 on the very next full run. The owner's own uncommitted disclaimer ("These showcases demonstrate what the agent CAN achieve") is the honest frame. The novel-cathode candidates (e.g., Li2Ni(PO4)(SO4), 5.10 V) remain screening-level, un-re-derived claims — the greenfield's `UNCORROBORATED` category, avant la lettre.
**Settling evidence:** independent re-derivation of the top candidate via a second method (MLIP + DFT spot check) — a genuine Ring-2 style task.

## D18. Debris handling — `.gitignore`-ing `CRASH` instead of removing it; empty `tests/`; parallel `benchmarks/framework/`

**Classification: obsolete** (harmless fossils) with one **incorrect** habit: codifying debris (`.gitignore:89`) rather than cleaning it. The CRASH episode itself (2026-01-17, empty `input_tmp.in` fed to `pw.x` twice) was never structurally addressed — the reconstruction's N5 stands; a deterministic input lint (uplift U-11) is the 20-line answer the incident deserved.

---

## Summary table

| # | Decision | Verdict |
|---|---|---|
| D1 | Skill-only architecture | validated (substrate), with restraint caveat |
| D2 | AGENTS.md prose engineering | contextually-valid-outdated (+ stale table: incorrect fragment) |
| D3 | Benchmark grading methodology | weakly-supported |
| D4 | Layer A′ reasoning-not-linting | validated as response; effectiveness unresolved |
| D5 | Compute-validation gates | weakly-supported (in-repo) |
| D6 | WORKFLOW.md campaign pattern | weakly-supported; design convergence-validated |
| D7 | Alpine DTN access | validated (liveness to re-verify) |
| D8 | ALCF strategy | validated content; status unresolved |
| D9 | T5/6/11 archiving | contextually-valid-outdated (blocker since removed) |
| D10 | project-update engine | validated design; operationally thin |
| D11 | Results archive operation | execution incorrect/unresolved (evidence lost) |
| D12 | Status-doc practice | incorrect (self-corrupting record) |
| D13 | "Theorizer MCP validated" claim | incorrect as stated |
| D14 | Unpinned model | incorrect (by omission) |
| D15 | Prompt-fix doctrine | contextually-valid-outdated |
| D16 | Multi-runtime portability | weakly-supported → owner question |
| D17 | Showcases as evidence | weakly-supported |
| D18 | Debris codification | obsolete/incorrect habit |

**Where history most changed this reviewer's view:** D4 (incident-grounded, not over-engineering), D1 (rot asymmetry proves prose durability), D9 (archival reason was access, now removed — revival is capability work), and D11 (what looked like sloppy docs is actually a *lost evidence base*, a graver and different problem).
