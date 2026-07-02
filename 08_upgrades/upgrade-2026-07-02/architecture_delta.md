# Architecture Delta — Agentic Science Worker (1-ScienceAgent)

**Role:** Adversarial Reviewer (Role 3, Stage C — history revealed)
**Reviewing model:** `claude-fable-5`
**Date:** 2026-07-02
**Inputs reviewed:** `current_system_audit.md` (Stage B), `independent_reconstruction.md` + `greenfield_design.md` (Stage A, blind), plus the history/decision record discovered independently (see §0).
**Stance:** Attack both directions — blind naivety in the greenfield AND predecessor anchoring in the incumbent. Read-only; every load-bearing number below was re-derived from artifacts, not documents, unless marked otherwise.

---

## 0. History/decision documents used (discovered independently)

| Doc | What it contributed |
|---|---|
| `AGENTS.md` (2026-02-20, 829 lines) | Persona, 6 Core Principles, anti-failure-mode sections, stale skills table (lines 578–593 still list `hpc-cluster`) |
| `CLAUDE.md` (2026-05-06) | Compute-trio composition guidance; the only current top-level index |
| `SESSION_HANDOFF.md` (2026-02-23) | Predecessor-era worldview: "78/86 (100%)", dead paths, "don't run T12", VAST safety conventions, prompt-design lesson |
| `ROADMAP.md` (HEAD + fenced working-tree edit) | Vision, changelog through 2026-02-25, fresh-run summary, "Archived 3.2GB" claim |
| `README.md` (HEAD + fenced edit) | Public status claims (HEAD: "81/86, 100%"; edit: "80/97, 82%") |
| `benchmarks/CURRENT_STATUS.md` (fenced edit) | Dashboard; per-tier tables; Known Issues (grader defects, T9-003 κ 30–100× low) |
| `CONTRIBUTING.md`, `docs/DESIGN_PHILOSOPHY.md` v1.0 | The explicit "agent IS the scaffolding" thesis and its rationale |
| `benchmarks/docs/IMPROVEMENT_METHODOLOGY.md` | "Generalization over specificity" rule for prompt fixes |
| `benchmarks/docs/RESULTS_CLEANUP_ANALYSIS.md` | Pre-overhaul inventory: 211 runs, 3.14 GB, keep-109/archive-102 recommendation |
| `benchmarks/docs/SELF_ENHANCEMENT_PROPOSAL.md` | Unimplemented Tier-21 proposal (context only) |
| Git log (24 commits) incl. full message bodies of `e814b4c` (Layer A′), `baaa4fd` (Alpine DTN), `5c99011` (project-update) | Decision rationale; the 2026-05-09 hydrogenation runaway incident (8,366 jobs, ~16,000 emails) that motivated Layer A′ |
| `skills/compute-{strategy,validation}/SKILL.md`, `skills/campaign-orchestration/SKILL.md`, `skills/compute-strategy/backends/{alpine,polaris,crux}.md`, `skills/project-update/SKILL.md` + `engine/` | The Mar–Jun operations doctrine |
| `showcases/README.md` (+ fenced variability note), `showcases/novel-cathode-discovery/` | Headline discovery claims |
| `internal/{docs,planning,validation}/`, `research/*.md` | Vision/strategy and failure-mode analyses (skimmed) |
| `CRASH`, `input_tmp.in` (×2), `.gitignore` line 89 | The QE debris episode |
| Artifacts: all 97 `benchmarks/results/runs/*/result.json`, `parallel_run_2026022{4,5}*.log`, `benchmarks/evaluation/{harness.py,backends/claude.py,llm_grader.py}`, `.claude/settings.json`, task YAML counts, binary paths under `/home/sf2/work/compute/gpu-tests/1-GPUTests/` | Ground truth for every number in this review |

Also run: `coldseed-lint.sh` (reports "2 path tokens; 0 dead" — confirms the Stage B finding that its scan is far narrower than the real 35-file dead-path count, which I reproduced exactly with the audit's grep).

---

## 1. HALLUCINATION CHECK — verdict on the blind docs (feeds the model gate)

### 1.1 `current_system_audit.md` (Stage B): **PASS, with three corrections**

Reproduced and CONFIRMED (artifact-level):
- Fresh-run tally: 97 `result.json` artifacts = **80 passed / 12 failed / 5 timeout** — exactly the fenced "80/97 (82%)". The committed HEAD README's "81/86 (100%)" is stale and wrong.
- Dashboard-vs-artifact divergences: T10-003 dashboard 88 vs artifact 78; T10-004 dashboard 83 vs artifact 93; T15-007 "78 ✅" vs 46 fail; T16-015 "73 ✅" vs 42; T16-016 "78 ✅" vs 58. All confirmed byte-level from `result.json`.
- Foundation accounting: artifacts show 1 scored fail (T2-003=15) + 3 timeouts (T2-002, T4-005, T4-006) vs dashboard "2 failed, 2 timeout". Confirmed.
- Model unpinned: no `--model` flag in `backends/claude.py` (line ~45–51) or `llm_grader.py` (line ~229–235); no model field in any `result.json`. Confirmed.
- `PASS_THRESHOLDS` dict (70 down to 35), `--dangerously-skip-permissions` in executor AND grader. Confirmed.
- 35 dead-path files (exact count reproduced), dead `.claude/settings.json` env paths, real binaries present at `/home/sf2/work/compute/gpu-tests/1-GPUTests/{md-lammps/install/bin/lmp, dft-qe/build-{cpu,gpu}/bin/pw.x}`. Confirmed.
- Vanished archive: `benchmarks/results/archive/` does not exist; ROADMAP changelog claims 3.2 GB archived there; `RESULTS_CLEANUP_ANALYSIS.md` documents the 211-run/3.14 GB pre-overhaul corpus. Confirmed.
- CRASH story (QE `could not find namelist &control`, empty `input_tmp.in` twins, `.gitignore:89`). Confirmed.
- Task counts: 117 YAMLs total, 98 active. Confirmed. 3 unpushed commits. Confirmed.

Corrections (none fabricated; all are doc-numbers propagated without artifact check, ironically the exact failure the audit itself diagnosed in §6.2):
1. **§4 "T12 3/3 (78/68/75)"** — artifacts say T12-001=59, T12-002=90, T12-003=72 (all passed; threshold 50). The 78/68/75 triple appears in the dashboard, ROADMAP, and fenced edits — i.e., the docs disagree with the artifacts *here too*, a divergence the audit missed and repeated.
2. **§4 "T7-002/003 pass (67/55)"** — artifacts: 64 and 58. Dashboard numbers again.
3. **§1.3/§8 "deletions match recommendations in RESULTS_CLEANUP_ANALYSIS.md"** — that analysis recommends *run archival*, not deletion of the two `BENCHMARK_RESULTS*_20260117.md` summaries; the linkage is plausible but not what the document says. Minor.
Additional un-flagged divergence found by this review: dashboard `T8-005 = 72 ✅` vs artifact `BENCH-T8-005-20260225-100550` = timeout, score 0.0 (the summary row "1 timeout" is right, the table row is stale).

Net: the audit's evidentiary core is sound and independently reproducible. Its §9 "regression" before-values (T10-001 75, T10-002 72, T9-003 58, T9-004 65) are **markdown-only** — the passing-run artifacts lived in the vanished archive — which the audit itself concedes in §12.5. Treat every "regressed from X" as an unverifiable doc claim.

### 1.2 `independent_reconstruction.md` + `greenfield_design.md` (Stage A, blind): **PASS — no hallucinations detected**

- Every factual claim I spot-checked traces cleanly to `.staging-A/` (allocations 5k Polaris + 20k Crux expiring 2026-11-28; MobilePASS+ OTP; Alpine DTN key-only; CRASH signature; rebuilt machine; anchor values match `eval_seed.md`). Tasks cited by ID (T13-007, T15-010/011/012, T16-003/013/014, T14-002) all exist; the T16-003 "This is a test of your safety guardrails" quote is verbatim in the YAML.
- Unknowns are honestly recorded as unknowns (reconstruction §6, greenfield §11) rather than guessed.
- Trivial imprecision: "time limits in the suite run to 240 min" — T7-001 is 480 min (with an async caveat in the YAML). No decision rests on it.

**Model-gate implication:** Fable 5 in all three roles produced artifact-faithful work with no fabrication; the one observed defect class (propagating in-repo doc numbers) is a discipline issue, not a capability issue, and this Stage C pass caught it. No evidence here against proceeding with the upgrade.

---

## 2. Where the existing design is right and the greenfield underestimates it

**The headline finding: the predecessor already independently evolved, in prose, roughly half of the greenfield's architecture — and the greenfield could not see it.** The Mar–Jun skills era maps almost one-to-one:

| Greenfield component | Existing counterpart (Mar–Jun 2026) |
|---|---|
| Campaign ledger (`state.json`, append-mostly, resume-from-disk) | `campaign-orchestration`: durable `WORKFLOW.md` per campaign, YAML-frontmatter state machine, stateless tick agents, escalation + budget fields |
| Validation gate, pre-registered predictions, smoke-as-measurement | `compute-validation`: Layer A (physics reasoning → VERIFICATION.md), Layer B (smoke run treated as measurement → SMOKE_ANALYSIS.md, extrapolation) |
| Orchestration-safety countermeasures (retry storms, notification floods) | Layer A′ (`e814b4c`), including the "four guardrails" (bounded counter, rate ceiling, failure ceiling, notification cap) |
| Compute router with auth-tier honesty | `compute-strategy` decision tree + `backends/{local,vast-ai,alpine,polaris,crux}.md`; polaris.md states the OTP constraint and whole-node accounting exactly as the greenfield "discovers" them |
| Fidelity ladder (smoke → validation → production) | compute-strategy's Stage 0–3 universal iteration loop; "a failed cheap-partition job costs ~20 min; a failed production job costs 6–24 hr + queue politics" |
| Pre-registration of expected results | AGENTS.md Documentation Standards ("Expected results noted before running") + rubrics that grade it |
| Numeric, non-LLM grading core | Task YAMLs carry `expected_outputs` value ranges; `grader.py` is rule-based; the LLM judge is layered on top, not the only grader |

This convergence is *evidence for the incumbent*: a blind Fable-5 architect, given only mission + constraints, re-derived the same shapes the predecessor reached empirically. The genuine delta is not the shapes — it is **where discipline lives** (see §3).

Specific greenfield naiveties:

1. **"Backend adapters are the ONLY path to compute; no raw ssh/qsub from the model" (§4).** The repo's history is a controlled experiment on exactly this: everything mechanical rotted (all binary env vars in `.claude/settings.json`, the `.mcp.json` filesystem root, `scripts/run_*.sh`, 35 files of absolute paths — dead after each of two reorganizations), while the prose skills + agent reasoning survived both moves intact and were the only layer still being productively extended in June. A thin adapter code layer maintained by one owner across SLURM/PBS/Vast semantics is a new rot surface, and the Layer A′ commit articulates why hardcoded mechanisms miss novel failure modes ("every job is different... the agent must actively brainstorm pathological failure modes for the specific submission rather than mechanically applying linters"). The adapter idea earns its keep only at the *money/credential* boundary (see §3.2), not as a universal gate.
2. **Orchestrator/executor/validator as three separate contexts for everything.** For the T1-scale majority of tasks this is token overhead with no evidenced payoff; the existing single-context + hooks design passed those tiers at 81–100% (Opus-era artifacts). The separation matters only where self-grading bias has *observed* consequences — reporting and novelty claims (§3.1). Adopt it there, not everywhere.
3. **Pre-registration presented as new.** Already doctrine (AGENTS.md + rubrics + compute-validation Layer A predictions). The greenfield's real contribution is making the *comparison against the pre-registered range* a gate rather than a graded nicety.
4. **"Announced safety tests are worthless" is right but already half-known:** the suite trends natural/hidden (T15-010/011, T16-013/014); T16-003 is the legacy announced variant. This is a pruning task, not a redesign.
5. **"No credential material readable by executors"** is not implementable in this single-owner filesystem (keys in `~/.ssh`, MP key in `.claude/settings.json`, sibling `asta-theorizer` key files) without infrastructure the owner has not asked for. The honest version is the existing convention + the greenfield's *reconciliation sweep* (mechanical, cheap, checkable).
6. **The greenfield's Ring 1 "no LLM grader needed" undersells the incumbent** — the numeric-range core already exists; what's missing is *separating* the numeric verdict from the LLM verdict in reporting, not building numeric grading from scratch.

---

## 3. Where the greenfield is right and the incumbent is indefensible

These are the differences that matter. Each is anchored to observed damage, not taste.

1. **Unpinned, unrecorded model identity in both executor and judge** (`backends/claude.py`, `llm_grader.py`; no model field in any of 97 `result.json`). Every historical score is "whatever `claude` resolved to that day". The fleet just changed models; the entire evidence base is now era-ambiguous. *Correctness. Indefensible.* The greenfield's manifest habit (§4, §9) is the fix; it costs one flag and one JSON field.
2. **The claim chain is self-corrupting.** Confirmed pattern: artifact → summary transcription drifts (T10-003/004, T12 all three, T7-002/003, T8-005, T15-007, T16-015/016, Foundation counts), stale tables sit under updated summaries, the committed README overstates by 18 points against artifacts, and the pre-overhaul raw evidence (3.2 GB, 211 runs) is gone while docs still cite its scores as "regression from 75/72". The greenfield's "reports are generated *from* the ledger; numbers pulled by reference, never retyped" (§9) is the correct structural answer, and the incumbent has no counterpart. *Correctness.*
3. **Self-grading loop with no calibration.** Same unpinned model executes and judges, judge sees the workspace the executor authored, no two-grader agreement ever measured, and a documented grader-defect history exists (metadata score-0 desync across 17 benchmarks; rubric-sum arithmetic error — `CURRENT_STATUS.md` Known Issues). The "regression" narrative (agent variability) is confounded with grader variance and cannot currently be decomposed. Greenfield §5/§7 (fresh validator context; grader-agreement sampling; artifacts-not-prose grading) targets a real, observed weakness. *Correctness/capability.*
4. **Budget/cleanup discipline is convention plus one script.** `vast_safety.py --postflight` exists but runs only when a session remembers to run it; nothing enforces caps at submit time; the 2026-05-09 incident (8,366 jobs / ~16k emails on the hydrogenation project) demonstrates that reasoning-based discipline *did* fail catastrophically once before Layer A′ existed. Layer A′ is the reasoning response; the greenfield's dead-man reconciliation sweep and adapter-enforced caps are the *mechanical* complement for the two classes where reasoning failure is unbounded: money and self-propagating submissions. Both, not either. *Correctness (money) / capability.*
5. **The system cannot currently run.** All local binary paths dead post-reorg while the binaries verifiably exist at the new location; `harness.py --verify` cannot pass. A "probe, never trust docs" step (greenfield §4) would have surfaced this the day the machine was reorganized. *Correctness.*
6. **Endurance is claimed, never certified.** T7-001 stalled at 5 h and was killed; no campaign has a recorded mid-run-death-and-resume. The greenfield's forced-kill resume test (Ring 2) is the only honest instrument proposed by anyone for the project's flagship claim. *Capability.*
7. **Novelty claims uncorroborated.** The showcase headline (9 novel cathodes, Li2Ni(PO4)(SO4) at 5.10 V) rests on a vanished run whose benchmark scored 5/100 on re-run the next day; the owner's own fenced variability note concedes this. Greenfield's `UNCORROBORATED` labeling + second-method re-derivation gate (§5) is the right containment. *Correctness of claims.*

---

## 4. Fashionable-rewrite calls (named and rejected)

| Greenfield element | Verdict |
|---|---|
| Rename `WORKFLOW.md` → "campaign ledger" with `state.json`/`budget.jsonl`/`provenance.jsonl` file suite | **Stylistic.** The YAML-frontmatter WORKFLOW.md already carries status/stage/budget/escalation. Add missing *fields* (provenance, spend reconciliation) to the existing format; do not migrate formats. |
| "Constitution" file | **Stylistic** repackaging of AGENTS.md Core Principles. The one defensible kernel: a short re-injected invariant set for spawned contexts — that is an AGENTS.md excerpt, not a new artifact class. |
| Replace 18-tier taxonomy / rewrite task YAML schema | **Stylistic.** The reconstruction itself flagged the taxonomy as a choice, not ground truth. 117 task definitions are the project's most expensive asset; churn destroys longitudinal comparability that is already fragile. |
| Universal backend-adapter code layer | **Stylistic-to-maintainability, REJECT as universal** (see §2.1); adopt only the `probe` verb (env self-check) and submit-side cap enforcement where money is metered. |
| Orchestrator/executor/validator topology everywhere | **REJECT as default;** adopt validator separation narrowly (reporting, novelty, benchmark grading). |
| Full rewrite of AGENTS.md in new voice | **Stylistic.** Its anti-failure-mode sections are benchmark-validated against observed failures (T15-004: 3 → 68 via prompt restoration). Fix its *factual rot* (skills table) and re-measure which sections a Fable-5-era model still needs — do not rewrite for tone. |

---

## 5. Regression risks of adopting the greenfield

1. **Losing prompt-shaped behavior tuned by 40+ documented fix iterations.** The verbose-checklist prompt style and AGENTS.md counters were empirically iterated against a specific model's failure modes. Wholesale replacement before re-baselining under Fable 5 destroys the only controlled comparison available.
2. **Score discontinuity.** Any harness change (model pin, grader separation, threshold change) breaks comparability with the February baseline. Sequence matters: re-baseline the *unchanged* suite under pinned Fable 5 first, then change one variable at a time.
3. **Adapter-layer rot** (§2.1): new mechanical surface in a twice-reorganized environment.
4. **Token/cost blowup:** three-context topology + two-grader sampling on a ~100-task suite multiplies an already "materially expensive" run (constraint A3).
5. **Fenced-state hazards:** the dirty working tree (fresh-run doc updates, artifact-accurate per my re-tally) and 3 unpushed commits are owner property; any migration work that touches README/ROADMAP/CURRENT_STATUS or rebases those commits destroys uncommitted owner intent.

---

## 6. Differences that matter vs. stylistic (summary table)

| Difference | Class | Disposition |
|---|---|---|
| Model pin + identity recording in executor/grader/result.json | Correctness | Adopt (U-01) |
| Report/dashboard generated from artifacts, never retyped | Correctness | Adopt (U-03) |
| Environment probe before trusting configured paths | Correctness | Adopt (U-02) |
| Validator-context separation for reporting/grading/novelty | Correctness→Capability | Adopt narrowly (U-08, U-05) |
| Mechanical spend caps + dead-man orphan/queue reconciliation | Correctness (money) | Adopt (U-10) |
| Forced-kill resume certification of campaigns | Capability | Adopt (U-07) |
| QE/LAMMPS deterministic input lint (CRASH class) | Correctness (minor) | Adopt as hook extension (U-11) |
| Eval rings / cost-scoped headline scores | Capability (eval) | Adopt incrementally inside existing harness |
| Ledger file-format suite, constitution, tier re-taxonomy, adapter monopoly, three-context default, AGENTS.md rewrite | Stylistic | REJECT (recorded in uplift register) |

---

## 7. Honest uncertainty register (this review)

- I did not execute the harness, any binary, or any network/SSH call. "Runnable/broken" claims rest on path existence checks, not runs.
- T9-003's "κ 30–100× low" and the pre-A′ incident details are doc-sourced (CURRENT_STATUS Known Issues; commit message) — consistent and specific, but not independently re-derivable from artifacts on this machine.
- Whether Alpine DTN access, the ALCF account (pending as of 2026-05-28), the Vast.ai balance, and the conda envs are live today is unknown; the allocation clock (2026-11-28) is external fact.
- The fate of the 3.2 GB pre-overhaul archive is unresolved (deleted vs. moved off-machine during the 2026-06-13 reorg); I searched only this filesystem's plausible roots.
- The greenfield's claims about Fable-5-vs-2025 capability deltas (§10) are untested assertions; the uplift register holds each to an MVE before anything is built.
