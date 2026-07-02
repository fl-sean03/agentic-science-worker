# Reasoning Debt — Agentic Science Worker (1-ScienceAgent)

**Last reviewed:** 2026-07-02  ·  **Reviewing model:** claude-fable-5

Ranked by leverage = (blast radius) × (likelihood prior reasoning is wrong) × (how much a stronger model/experiment could improve it).

## Open reasoning debt (ranked)

| ID | The under-justified reasoning | Kind | Where it lives | Blast | Leverage | What would pay it down |
|----|------------------------------|------|----------------|-------|----------|------------------------|
| RD-01 | "T9/T10 score collapses = agent variability on complex tasks" — concluded without ever measuring grader variance, with an unpinned model grading itself, and with the before-run artifacts now lost | weak-evidence | ROADMAP/CURRENT_STATUS regression narrative; D3 | **H** | **H** | U-05/B-3b grader study (two-grader agreement + test-retest on preserved workspaces) + Slice A6 replicates; decomposes model vs grader vs task variance |
| RD-02 | The entire February capability record implicitly attributed to "the agent" without recording which model ran or judged | weak-evidence | all 97 result.json (absence); D14 | **H** | **H** (for the future; past likely unrecoverable) | Slice A1 (pin+record) stops the bleeding — **landed 2026-07-02** (EV-A1 green); the past half stays open pending B-7 archive recovery |
| RD-03 | Verbose-checklist prompts + AGENTS.md anti-failure counters treated as "how to run agents" when they were tuned to one older model's failure distribution | under-evaluated | AGENTS.md; IMPROVEMENT_METHODOLOGY.md; D2/D15 | **H** | **H** | D2 ablation: behavioral tiers (T13/T15/T16) under pinned Fable 5, counters present vs ablated, N≥3 — decides what is load-bearing vs dead weight |
| RD-04 | "Works independently for days" claimed from design plausibility; never derived from a demonstrated death-and-resume; the one long-horizon datapoint (T7-001) stalled | unreconstructed | campaign-orchestration SKILL.md; README vision; D6 | **H** | **H** | Slice A7 forced-kill resume test — first empirical certification either way |
| RD-05 | Self-grading validity: judge = executor's model family, judge explores executor's own workspace, calibration never measured despite a documented grader-defect history | under-evaluated | llm_grader.py; D3 | **H** | M-H | A4 validator-separation replay (cheap) → B-3b full study; artifacts-only grading variant |
| RD-06 | "Archived 3.2 GB of results" believed executed because docs say so; the archive does not exist — the claim-to-evidence chain was never re-checked after the machine reorg | weak-evidence | ROADMAP changelog; D11 | M-H | M-H | Backup catalog search (B-7); henceforth: hash manifests at every operation (started 2026-07-02) |
| RD-07 | "The agent IS the scaffolding" silently extended from judgment (where evidence supports it) to *restraint* (where the 2026-05-09 runaway refutes it); the boundary was never drawn explicitly until this rebase | under-evaluated | DESIGN_PHILOSOPHY.md; D1/D4 | M-H | M | B-5 mechanical money/self-propagation bounds + a written boundary statement in the philosophy doc (owner-gated, B-1 adjacent) |
| RD-08 | Per-tier pass thresholds (70→35) encode "partial progress counts more on harder tasks" — chosen without recorded justification; aggregate "pass rate" claims inherit the definition invisibly | under-evaluated | harness.py PASS_THRESHOLDS; D3 | M | M | Either justify from rubric semantics or report threshold-free score distributions alongside pass rates (A3 generator can do both) |
| RD-09 | Showcase "novel discovery" headline (9 cathode candidates, Li2Ni(PO4)(SO4) 5.10 V) presented as capability evidence; screening-level, never re-derived, source run's benchmark scored 5/100 the next day | weak-evidence | showcases/novel-cathode-discovery; D17 | M | M | Second-method re-derivation of top candidate (MLIP + DFT spot check) with UNCORROBORATED labeling until then (B-9) |
| RD-10 | Synthetic fixtures (seeded logs, injected queue states) assumed to predict live behavior; never cross-checked against a real run | under-evaluated | benchmarks fixtures; A-09 | M | M | One paired synthetic-vs-real task after A2 restores local execution |
| RD-11 | T5/6/11 "archived" read as "obsolete" ever since; the archival reason (CURC access) was removed in June but nobody re-examined the archive decision until this rebase | under-evaluated | skills/archive; D9 | M | M | B-4: one revived Alpine round-trip task — also gives the compute trio its first coverage |
| RD-12 | `benchmarks/framework/` vs `evaluation/` duality: superseded-ness inferred from mtimes, never verified (imports, references) | undetermined-necessity | benchmarks/framework/ | L | L | 20-min import/reference audit; no action otherwise (U-R7 rejected) |
| RD-13 | Empty-input QE crash class diagnosed post-hoc by this rebase; the original incident was never root-caused at the time — unknown whether the agent's input-generation bug still exists in the current skill prompts | unreconstructed | CRASH; quantum-espresso skill; D18 | L-M | M | Slice A5 lint **landed 2026-07-02** (prototype + tests; post-mortem at `docs/rebase/CRASH_POSTMORTEM_20260117.md`); still owed: hook activation (B-2) + one QE task observation (blocked on QE runnability, A-04) |

## Suspected blind spots (no one has looked hard)
- **Cost accounting**: no artifact anywhere records LLM token/dollar spend of benchmark runs or campaigns; "materially expensive" is a guess. First pinned runs (A6) should record wall+tokens as first-class fields.
- **Security posture**: benchmarks run `--dangerously-skip-permissions` on the owner's real machine with real `~/.ssh` keys reachable; safety rests on a regex hook + prompt discipline. Never threat-modeled. Owner-level decision; flagged, not proposed.
- **`.mcp.json` silently broken**: the filesystem MCP server roots at a dead path — meaning MCP-dependent behaviors may have been no-ops for weeks without any error surfacing. Whether anything relied on it is unexamined.
- **The three undocumented side repos** under `workspaces/projects/` (own `.git`, Jan–Feb): potentially valuable HPC fan-out/scheduler prototypes invisible to every status doc (Q-04).
- **Grader prompt-injection surface**: the LLM judge explores agent-authored workspaces with tool access; a benchmark run could (even accidentally) leave judge-steering text in its workspace. Never audited; artifacts-only grading (A4/B-3b) reduces it.
- **Backup coverage of gitignored evidence**: whether restic/ZFS tiers actually capture `workspaces/` and `results/runs/` (1.6 GB gitignored evidence) is unverified — the D11 loss suggests assumed-covered may be wrong.

## Resolved (paid-down debt)
| ID | Was | Resolved by | Date | Outcome |
|----|-----|-------------|------|---------|
| RD-14 | Fresh-run headline numbers ("100%"? "82%"?) disagreed across docs; truth unknown | Stage-C byte-level re-tally of all 97 result.json (`architecture_delta.md` §1.1) | 2026-07-02 | 80/12/5 of 97 (82%) is artifact truth; committed README overstates; fenced edit is correct |
| RD-15 | "Why were HPC tiers archived" (capability vs access) | git/changelog forensics (`historical_decision_review.md` D9) | 2026-07-02 | Access, not capability — revival is legitimate capability work (B-4) |
| RD-16 | CRASH file: unresolved incident or debris? | Stage-B forensics (audit §12.3) | 2026-07-02 | Fossil of a 2026-01-17 empty-input QE invocation; structural fix still owed (→RD-13/A5) |
