# Current System Audit — Agentic Science Worker (1-ScienceAgent)

**Role:** Cartographer (Stage B, intelligence rebase Opus 4.8 → Fable 5)
**Reviewing model:** `claude-fable-5`
**Date:** 2026-07-02
**Target:** `/home/sf2/work/agents/science-agent/1-ScienceAgent` (~1.8 GB; 358 git-tracked files)
**Stance:** READ-ONLY description. Evaluative itches are confined to §10 (flags). This
document inherits *evidence*, not the predecessor's conclusions.

---

## 1. Inventory — what is here, live vs. stale, and how you can tell

Staleness signals used throughout: file mtimes, git commit dates, string-search for
pre-reorg paths (`/home/sf2/LabWork/...`, `/home/sf2/Workspace/main/39-GPUTests/...` —
both directories **no longer exist**; the machine was reorganized to `~/work/` on
2026-06-13 per `/home/sf2/CLAUDE.md`), and internal cross-references.

### 1.1 Top-level layout

| Item | mtime | Live/Stale | Notes |
|---|---|---|---|
| `AGENTS.md` (27 KB) | 2026-02-20 | **Stale-ish** | The "primary agent context": researcher persona, 6 Core Principles, professional standards, failure-mode counters. Its skills table (lines 578–593) still lists `hpc-cluster` (archived) and omits every skill added after Feb (compute trio, project-update, iff-parameters). |
| `CLAUDE.md` (3.3 KB) | 2026-05-06 | **Live** | Most current top-level doc. Lists the "compute trio" (`compute-strategy`, `compute-validation`, `campaign-orchestration`) and says "read all three when driving a non-trivial compute campaign." |
| `README.md` | 2026-02-25 | **FENCED** (uncommitted edit) | Public-facing overview + benchmark table. Working-tree edit updates status 81/86 (100%) → 80/97 (82%). |
| `ROADMAP.md` | 2026-02-25 | **FENCED** (uncommitted edit) | Vision, tier progress bars, changelog through 2026-02-25. Header still says "Last Updated: 2026-02-23". |
| `SESSION_HANDOFF.md` | 2026-02-23 | **Stale** | Written for continuation sessions in the *old* path (`/home/sf2/LabWork/Workspace/29-AgenticScienceWorker/...`). Says T12 is blocked (superseded 2026-02-25) and "78/86 passing (100%)". Evidence of the predecessor era, not authority. |
| `CRASH` (269 B) | 2026-01-17 06:59 | **Debris** | Quantum ESPRESSO error dump: `read_namelists: could not find namelist &control`. See §12.3. |
| `input_tmp.in` (0 B) | 2026-01-17 06:59 | **Debris** | Empty QE input, same minute as CRASH. A twin exists at `benchmarks/input_tmp.in` (0 B, Jan 17 04:31). |
| `CONTRIBUTING.md` | 2026-01-29 | Stale-ish | Developer/benchmark-fixing guidance. |
| `config.example.yaml`, `.aider.conf.yml.example`, `.mcp.json.example` | Jan | Stale-ish | Templates. No actual `config.yaml` exists on disk. |
| `.mcp.json` | 2026-01-17 | **Rotted** | playwright + semantic-scholar + filesystem MCP servers; the filesystem server is rooted at the dead `/home/sf2/LabWork/Workspace/29-AgenticScienceWorker` path. |
| `.gitignore` | 2026-02-24 | Live | Ignores `workspaces/benchmarks/`, `benchmarks/results/runs/`, `config.yaml`, `.claude/settings.json`, and — notably — `CRASH` (line 89: someone codified the debris rather than removing it). |
| `logs/operations.log` | **2026-07-02 15:02** | **Live-session-owned** | 2 lines, written today by the PostToolUse hook: the live agentctl session wrote/edited `/home/sf2/work/ops/intelligence-rebase/projects/science-agent/status.md`. Confirms the live session is UP and has made **no project-file writes** today. Do not touch. |

### 1.2 Directories

| Dir | Size | Freshest content | Assessment |
|---|---|---|---|
| `skills/` (17 entries) | 569 KB | **2026-06-21** | The live heart of the project post-February. Two generations: (a) Jan–Feb "researcher skills" (lammps-simulation, quantum-espresso, mlip-simulation, vast-cloud, literature-search, materials-database, data-analysis, resource-acquisition, theory-synthesis, ggen, torch-sim) and (b) Mar–Jun "operations skills" (iff-parameters 03-26; compute-strategy 05-05→06-21; compute-validation 05-06→05-10; campaign-orchestration 05-05; project-update + a full Python engine w/ tests 05-29). `skills/archive/hpc-cluster-curc/` holds the retired CURC skill. `.claude/skills → ../skills` symlink. |
| `benchmarks/` | 3.4 MB | 2026-02-25 | Harness (`evaluation/`), 117 task YAMLs under `tasks/tier{1-4,7-10,12-18}` + `tasks/archive`, rubrics, docs, fixtures, `results/runs/` (97 run dirs from the 2026-02-24/25 fresh run, gitignored), `results/examples/` (tracked). Frozen since Feb 25. Also contains an older, apparently parallel `framework/` (CLEAR metrics runner) beside the live `evaluation/`. `evaluation/rubrics/` and `evaluation/validators/` are empty; `benchmarks/rubrics/` is populated. `benchmarks/reports/` empty. |
| `workspaces/` | **1.6 GB** | 2026-02-25 | Bulk of repo size. `benchmarks/runs/` (agent work dirs from fresh run, 99 entries), `projects/` (3 undocumented mini-projects with their own `.git` — see §12.2), `examples/` (4 tracked exemplar runs), `phase0-tests/`, `copper_calc/`, `resources/` (potentials/pseudopotentials/structures caches). Gitignored except examples. |
| `showcases/` | 64 MB | 2026-02-25 | 6 showcases + `verify_all.py` (contains dead paths). `torch-sim-screening` is 63 MB of it. `showcases/README.md` is **dirty** (uncommitted note about run-to-run variability). |
| `internal/` | small | 2026-02-16 | Vision/strategy docs (`REAL_SCIENCE_VISION.md`, `ECOSYSTEM_AND_PARTNERSHIPS.md`), planning, validation results for ggen/torch-sim. |
| `research/` | small | 2026-02-19 | Benchmark strategy/tracking, failure-mode analysis, capability-expansion plan, context-architecture. |
| `docs/` | small | 2026-02-19 | `DESIGN_PHILOSOPHY.md` ("Intelligence as Scaffolding"), `BENCHMARK_OVERVIEW.md`, `HEADLESS_AGENT_GUIDE.md`, setup/integration docs. |
| `examples/` | small | 2026-02-18 | Canonical patterns (self-verification, error-recovery) and anti-patterns (narrative-without-action, premature-termination) that AGENTS.md points to. |
| `configs/` | small | Jan | Per-agent configs (claude, aider, cursor, codex). Aider/Codex backends never implemented (harness `backends/` has only `base.py` + `claude.py`). |
| `templates/`, `scripts/`, `environments/`, `resources/` | small | Jan–Feb | LAMMPS/QE templates; run scripts (dead paths inside `run_lammps.sh`/`run_qe.sh`); conda env YAMLs (`science-tools.yml`, `theorizer.yml`); `resources/pseudopotentials/` is **empty**. |
| `tests/` | 0 | 2026-01-17 | Empty since creation. |
| `.claude/` | small | Jan | `settings.json` (untracked, rotted env paths — §6), `settings.json.example` (tracked), hooks (`validate_simulation.py` PreToolUse-Bash; `format_output.py` PostToolUse-Write/Edit → `logs/operations.log`), 3 subagent defs (`data-analyst`, `literature-reviewer`, `simulation-runner` — the latter has dead paths). |

### 1.3 Git state

- Branch `main`, **3 commits ahead of `origin/main`** (github.com/fl-sean03/agentic-science-worker): `8e00ba8` (05-28 ALCF backends), `5c99011` (05-29 project-update), `baaa4fd` (06-21 Alpine→DTN repoint). Unpushed.
- **Dirty working tree (ALL FENCED, owner/live-session property):** modified `README.md`, `ROADMAP.md`, `benchmarks/CURRENT_STATUS.md`, `showcases/README.md`; deleted `benchmarks/results/BENCHMARK_RESULTS_20260117.md` and `benchmarks/results/BENCHMARK_RESULTS_VALIDATED_20260117.md`. All mtimes 2026-02-25 21:35–21:36 — this is the fresh-run documentation update, sitting uncommitted for four months. The deletions match recommendations in `benchmarks/docs/RESULTS_CLEANUP_ANALYSIS.md` (2026-02-25).
- Commit cadence: dense Jan 17–Feb 25 (benchmark era), then sparse single-purpose commits Mar 26 → Jun 21 (skills era), then dormant until today's wake.

---

## 2. Actual end-to-end behavior (exact scripts/configs)

There are **three distinct execution paths** through this system.

### 2.1 Interactive researcher mode (the product)

1. User runs `claude` (or aider/cursor) at repo root.
2. Context load: `CLAUDE.md` → defers to `AGENTS.md` (persona: "independent lab
   member"; 6 Core Principles: verify everything, know limits, monitor continuously,
   safety over compliance, report uncertainty, cite always; plus explicit
   anti-failure-mode sections "Narrative ≠ Execution", "Preparation ≠ Completion",
   "Genuine Revision ≠ Empirical Shortcuts").
3. Skills discovered via `.claude/skills → ../skills`. Domain knowledge is *pure
   markdown* — no orchestration code (deliberate: `docs/DESIGN_PHILOSOPHY.md`).
4. Tools: LAMMPS via `$LMP`, QE via `$QE_CPU`/`$QE_GPU` (env set in
   `.claude/settings.json`), `vastai` CLI, MP API (`$MP_API_KEY`), MCP servers
   (playwright, semantic-scholar, filesystem).
5. Hooks: `validate_simulation.py` blocks dangerous Bash patterns and warns on long
   LAMMPS runs pre-execution; `format_output.py` appends every Write/Edit to
   `logs/operations.log`.
6. Work products land in `workspaces/` (gitignored).

**Current operability caveat:** every binary path in `.claude/settings.json`
(`LMP=/home/sf2/Workspace/main/39-GPUTests/.../lmp`, `QE_CPU`, `QE_GPU`,
`GPUTESTS_REPO`) points to a directory that no longer exists. The real binaries are at
`/home/sf2/work/compute/gpu-tests/1-GPUTests/{md-lammps/install/bin/lmp,
dft-qe/build-{cpu,gpu}/bin/pw.x}` (verified present). As configured, local simulation
and `harness.py --verify` cannot find their binaries.

### 2.2 Benchmark harness mode (the evaluation machinery)

Flow, from `benchmarks/evaluation/harness.py`:

1. Load task YAML from `benchmarks/tasks/tierN_*/BENCH-Txx-yyy-*.yaml` (117 files;
   each has `prompt`, `expected_outputs` with value ranges, `grading` rubric with
   weighted categories, `time_limit_minutes`).
2. `create_workspace()` → `workspaces/benchmarks/<BENCH-ID>-<runid>/`.
3. Backend (`evaluation/backends/claude.py`) spawns
   `claude -p --output-format json --dangerously-skip-permissions --allowedTools
   Bash,Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,TodoWrite`
   with the task prompt, cwd = workspace, default 50 turns / 1800 s timeout.
   **The model is not pinned** — whatever the `claude` CLI defaults to.
4. Grading: rule-based `grader.py` + `llm_grader.py`, which spawns a *second*
   `claude -p --dangerously-skip-permissions` as an LLM-judge with tool access to
   explore the workspace and emit a rubric-keyed JSON score.
5. Pass thresholds per tier: 70 (T1), down to 40 (T10), 35 (T11), 50–70 elsewhere
   (dict `PASS_THRESHOLDS` in harness.py).
6. Results → `benchmarks/results/runs/<ID>-<runid>/{result.json, benchmark.json,
   agent_output.txt}` (+ full conversation capture per commit `0ce2cf6`).
7. `parallel_runner.py` fans out (fresh run used 6 workers; 10 caused OOM per
   ROADMAP). `vast_safety.py --postflight` hunts orphaned `BENCH-*` VAST instances.
8. `regrade.py`, `audit.py`, `preflight_checks.py`, `transcript.py` support tooling.

Last executed: 2026-02-24/25 ("fresh run", 97/98 completed, logs at
`benchmarks/results/parallel_run_20260225_resume.log`). Nothing has run since.

### 2.3 Real-compute campaign mode (the post-February direction, unbenchmarked)

Defined by the compute trio + campaign orchestration, all added May–June 2026:

- `skills/compute-strategy/SKILL.md` — 7-step decision tree routing jobs across
  backends: `backends/local.md`, `vast-ai.md`, `alpine.md` (CU Alpine via
  **DTN `dtn.rc.colorado.edu`, ssh alias `cu_alpine`, user `sefl7948`, key-only,
  no Duo**, partitions `atesting_a100`/`aa100`/etc., NAMD 3.0.2 pre-installed at
  `/projects/sefl7948/software/...`), `polaris.md` (ALCF Polaris, PBS Pro, account
  `sefl-alcf` **pending approval** as of 05-28, allocation `HydrogenStorage` 5,000
  node-hours expiring 2026-11-28, MobilePASS+ OTP ⇒ **no unattended login**),
  `crux.md` (ALCF CPU cluster).
- `skills/compute-validation/SKILL.md` — layered gate before expensive compute:
  Layer A (physics reasoning → VERIFICATION.md), Layer A′ (orchestration-safety
  reasoning over scripts/submission patterns, added commit `e814b4c`), Layer B
  (smoke run treated as a *measurement*, extrapolated → SMOKE_ANALYSIS.md), with
  templates and tool pages (`tools/namd.md`, `tools/slurm-orchestration.md`).
- `skills/campaign-orchestration/SKILL.md` — stateless-agent / durable-`WORKFLOW.md`
  tick pattern for N≥2 long campaigns; YAML frontmatter state machine (status,
  current_stage, escalation, budget caps, notify policy).
- `skills/project-update/` — "Tier-1" in-repo update engine (`engine/project_update/`,
  stdlib-only Python with a pytest suite) that mines git history + docs, driven by a
  `.sync/manifest.yaml`. **No `.sync/` exists in this repo** — the engine's
  prerequisite is absent here; the skill is hosted here for use inside other
  project repos (references `36-LabSync` ADRs).

No benchmark tier exercises this path (T5/T6/T11 HPC tiers were archived in the
CURC era, before these skills existed).

---

## 3. Architecture, dependencies, provenance pins

**Architecture** (deliberate, documented in `docs/DESIGN_PHILOSOPHY.md` v1.0):
"The agent IS the scaffolding." No mode selectors, no state machines, no
orchestration code. One flat layer of markdown skills + a coding-agent CLI +
external binaries. The only real *code* in the project is (a) the benchmark
harness/graders, (b) the project-update engine, (c) hooks and helper scripts.

**Dependency graph:**

| Dependency | Pin/provenance | Status |
|---|---|---|
| `claude` CLI + subscription | **Unpinned model, unpinned CLI version.** No result artifact records which model ran. | All recorded scores are era-specific (pre-Fable). |
| LAMMPS / QE binaries | External project `gpu-tests` (paths hardcoded in untracked `.claude/settings.json`) | Paths dead post-reorg; binaries verified to exist at `/home/sf2/work/compute/gpu-tests/1-GPUTests/`. |
| `vastai` CLI + account | ~$25 prepaid balance per SESSION_HANDOFF (Feb) | Unverified today. |
| Materials Project API | Key **hardcoded in `.claude/settings.json`** (untracked/gitignored, but plaintext on disk) | Unverified. |
| Semantic Scholar MCP | `npx @anthropic-ai/semantic-scholar-mcp`, `$SEMANTIC_SCHOLAR_API_KEY` | Unverified. |
| ASTA Theorizer / paper-finder | Sibling dirs `../asta-theorizer`, `../asta-paper-finder` (cloned 2026-01-31; conda env `theorizer`); theory-synthesis skill drives them. Theorizer's own MCP server marked "Planned" in the skill. | Sibling contains `api_keys.donotcommit.json`, `s2_key.donotcommit.txt`. |
| Conda envs | `environments/science-tools.yml`, `environments/theorizer.yml` | Version-pinned YAMLs exist; envs unverified. |
| CU Alpine | ssh alias `cu_alpine` in `~/.ssh/config`, key `~/.ssh/cu_alpine`, canonical writeup `~/.claude/skills/cu-hpc-access` (external to repo) | Requires CU campus network. |
| ALCF Polaris/Crux | Account pending as of 2026-05-28; OTP-gated | Cannot run unattended by design. |
| IFF database | Via `skills/iff-parameters` → Heinz-lab tooling under `~/work/tools/iff/` | External. |

**Provenance of scientific parameters** is handled culturally, not mechanically:
AGENTS.md Principle 6 mandates citations in input-file comments; benchmark rubrics
grade for it. There is no lockfile-style pinning of pseudopotentials/potentials —
`workspaces/resources/{potentials,pseudopotentials,structures}` is a convention cache.

---

## 4. Requirements coverage vs. the project's own stated intent

Stated intent (README/ROADMAP/internal vision docs): an autonomous researcher that can
(1) take a research question, (2) find methodology/parameters from literature,
(3) run appropriate simulations, (4) verify against published values, (5) iterate,
(6) produce a report a scientist would accept — and eventually "receive a group
meeting transcript, work independently for days."

| Stated requirement | Coverage evidence | State |
|---|---|---|
| MD (LAMMPS) autonomously | T1–T4: 17/21 in fresh run; 40+ historical passes | Demonstrated (as of Feb; binaries currently mis-pathed) |
| DFT (QE, GPU) | T10-004 pass (artifact score 93); T10-003 pass (78) | Demonstrated |
| MLIP (MACE/CHGNet/M3GNet) | T8 6/7 | Demonstrated |
| Literature search + param extraction | Rubric-graded across tiers; T16-015 "natural citation" **failed fresh run (42)** | Partial |
| Materials Project queries | materials-database skill; used in showcases | Demonstrated |
| Cloud GPU (VAST.ai) lifecycle | T17 7/8 | Demonstrated |
| Data analysis / publication figures | T18 4/4 | Demonstrated |
| Theory synthesis | T12 3/3 (78/68/75) | Demonstrated (via Theorizer CLI-level integration; MCP "planned") |
| HPC (SLURM) execution | AGENTS.md still claims it as a capability; T5/T6/T11 archived; new Alpine/ALCF skill pages exist but **zero benchmarks and no recorded end-to-end campaign in this repo** | Claimed, not currently evidenced in-repo |
| Novel discovery (frontier) | T10-001/002 passed once (75/72 on 02-24), regressed to 5/17 on the 02-25 fresh run; showcases preserve the successful runs | Non-reproducible / high-variance |
| Multi-hour autonomy | T7-002/003 pass (67/55); T7-001 stalled at 5 h and was killed | Partial |
| Group-meeting-transcript workflow | Nothing implements it | Vision only |
| Multi-agent backends (aider/codex/cursor) | Configs + `--backend` flag exist; only `claude.py` backend implemented | Scaffolding only |

---

## 5. What the system actually optimizes for

Judged by where effort and artifacts accumulated, not by mission statements:

1. **Jan–Feb era: benchmark pass-rate and its documentation.** The densest artifact
   mass is benchmark tasks, graders, dashboards, improvement methodology, gap
   analyses, and prompt engineering. A recurring documented lesson: *detailed,
   checklist-style prompts prevent early termination* (T15-004 fix: score 3→68 by
   restoring a verbose prompt). Significant machinery exists to fix *benchmarks*
   (prompts/rubrics), which the project itself acknowledges: "Most failures are
   prompt issues, not code issues" (ROADMAP §How to Contribute).
2. **Behavior shaping of the agent via prose.** AGENTS.md is 829 lines of persona +
   anti-failure-mode instruction, iterated in response to specific benchmark failures
   (changelog 2026-02-16). The system's "code" is largely English.
3. **Demonstrability.** `showcases/` curates the best runs (novel cathode discovery,
   XRD structure determination) — the dirty `showcases/README.md` edit adds an honest
   variability disclaimer.
4. **Mar–Jun era pivot: compute-cost discipline on real infrastructure.** The five
   post-February commits all serve safe, cheap, resumable *real* compute (smoke-first
   iteration, verification gates, stateless campaign supervision, Alpine-DTN
   frictionless auth, ALCF onboarding). Optimization target shifted from "score well
   on our own suite" to "don't waste GPU-hours/queue position on real clusters."

---

## 6. Doc-vs-artifact divergences (paths cited; disagreeing numbers are gold)

1. **Dashboard scores vs. result artifacts** (`benchmarks/CURRENT_STATUS.md` vs.
   `benchmarks/results/runs/*/result.json`):
   - T10-003: dashboard **88** ✅ vs. artifact `BENCH-T10-003-20260224-233208/result.json` = **78**.
   - T10-004: dashboard **83** vs. artifact `BENCH-T10-004-20260224-233208/result.json` = **93**.
   (Both directions — not a uniform transcription offset. ROADMAP changelog agrees
   with the artifact for T10-003 ("T10-003 passed (78)") while README's highlights
   line says "T10-003: 78" but the header commit `e203c44` also says 78; only the
   dashboard says 88.)
2. **Fresh-run failures not propagated to tier tables.** `CURRENT_STATUS.md` summary
   row says Quality T13–T16 = 38/43 (88%), but the per-tier tables below it still
   show "T15: Agent Cognition (100%)" and every row ✅ — including T15-007 = "78 ✅"
   whereas `BENCH-T15-007-20260225-065909/result.json` = **46 (fail)**;
   T16-015 "73 ✅" vs. artifact **42 (fail)**; T16-016 "78 ✅" vs. artifact **58
   (fail)**. The tables are pre-fresh-run values under a post-fresh-run summary.
3. **Foundation-tier accounting.** Summary claims T1–T4 "2 failed, 2 timeout";
   `results/parallel_run_20260225_resume.log` shows 1 scored failure (T2-003 = 15)
   and 3 errored/timeout (T2-002, T4-005, T4-006).
4. **Vanished results archive.** `CURRENT_STATUS.md`/ROADMAP claim "Archived 3.2GB of
   old results to `benchmarks/results/archive/runs_20260224_pre_overhaul/`". That
   directory **does not exist** in the repo, and a filesystem-wide search found no
   `runs_20260224_pre_overhaul` anywhere. The pre-overhaul evidence base is gone or
   off-machine.
5. **HEAD-vs-working-tree status split.** Committed README says "81/86 benchmarks
   passing (100% pass rate)"; the uncommitted edit says "80/97 (82%)". Anyone reading
   GitHub sees a claim four months stale *and* directionally rosier. Origin is
   additionally 3 commits behind local.
6. **AGENTS.md vs. skills/ reality.** AGENTS.md skills table lists `hpc-cluster`
   (now `skills/archive/hpc-cluster-curc/`) and lacks `compute-strategy`,
   `compute-validation`, `campaign-orchestration`, `project-update`,
   `iff-parameters`, `vast-cloud`'s current framing. CLAUDE.md (05-06) is the
   accurate index. The "primary context file" is the stale one.
7. **Theorizer MCP.** ROADMAP/CURRENT_STATUS: "Theorizer MCP integration validated"
   (2026-02-25). `skills/theory-synthesis/SKILL.md` line 318: "MCP server | Planned".
   `.mcp.json` contains no theorizer server. T12 evidently ran through non-MCP
   integration.
8. **Dead paths, 35 files.** `grep -rl 'LabWork|Workspace/main/39-GPUTests'` hits 35
   files incl. `.mcp.json` (filesystem MCP root), `.claude/settings.json` (all
   binary env vars), `SESSION_HANDOFF.md`, `ROADMAP.md`, `benchmarks/CURRENT_STATUS.md`
   (QE paths §"QE Locations"), `scripts/run_lammps.sh`, `scripts/run_qe.sh`,
   `.claude/agents/simulation-runner.md`, `showcases/verify_all.py`,
   `skills/quantum-espresso/SKILL.md`, `skills/compute-strategy/SKILL.md` +
   `backends/{polaris,crux}.md` (these last reference `39-GPUTests` for QE builds).
   Note: `coldseed-lint.sh` reported only "2 path tokens; 0 dead" — its scan is much
   narrower than reality here.
9. **SESSION_HANDOFF.md** claims "Current State: 78/86 active benchmarks passing
   (100% pass rate)" and "Don't run T12 — blocked on Theorizer MCP"; both superseded
   two days later by the fresh run. It also anchors all commands to the dead
   `/home/sf2/LabWork/...` path.
10. **README project tree** omits `internal/`, `research/` beyond one line,
    `showcases/` (present), and the entire post-Feb skills generation.

---

## 7. Implicit embedded assumptions

- **The agent-under-test and the judge are the same unpinned model.** `claude -p`
  is invoked for both execution and LLM-grading with no `--model` flag; nothing in
  `result.json` records model identity. Every historical score silently assumes
  "whatever `claude` resolved to that day" — and the fleet just moved to Fable 5,
  so re-running the suite measures a different system than the one documented.
- **Repo location stability.** Absolute paths are baked into configs, skills, docs,
  and the MCP filesystem root. This assumption has now been violated twice
  (LabWork → Workspace/main → work/) and each move strands ~dozens of files.
- **Benchmarks run with `--dangerously-skip-permissions` in Sean's real
  environment.** Safety rests on prompt discipline, the PreToolUse regex hook, and
  conventions like "only destroy `BENCH-*` VAST instances" (SESSION_HANDOFF lists
  Sean's untouchable instances by name).
- **Pass thresholds encode capability tiers** (40 for frontier vs. 70 for basics) —
  i.e., "partial progress counts more the harder the task". Aggregate "pass rate"
  numbers inherit that definition without restating it.
- **LLM-judge scores are comparable across runs/days/models** — the regression
  narrative ("agent variability on complex tasks") assumes grader stability that was
  never separately measured.
- **VAST.ai billing hygiene depends on label conventions + a postflight script**
  running after every session.
- **Alpine DTN key-only access assumes the machine is on the CU campus network**
  (stated in `backends/alpine.md`); Polaris assumes a human with a phone.
- **`workspaces/` (1.6 GB) is the real evidence base but is gitignored** — the
  project's claims are reproducible only on this one machine.
- **The compute trio assumes projects it operates on carry their own AGENTS.md
  authority** ("Project-level rules win") — this repo is a skill *host*, and its own
  benchmark suite never validates the trio.

---

## 8. Accidental vs. deliberate (evidence only)

| Observation | Reading | Evidence |
|---|---|---|
| Skill-only, no-orchestration architecture | **Deliberate** | `docs/DESIGN_PHILOSOPHY.md` argues it explicitly; ROADMAP principle "Expand the toolkit, not the complexity." |
| CURC/HPC tier archiving | **Deliberate** | Changelog 2026-02-20 with rationale (access deferred, VAST replacement); skills moved to `archive/`. |
| Dirty working tree (docs + 2 deletions) | **Deliberate edits, accidental permanence** | Contents are the coherent fresh-run update + cleanup recommended in `RESULTS_CLEANUP_ANALYSIS.md`; sitting uncommitted since 02-25 with 3 unpushed commits stacked after — looks like a session ended before commit and the project went dormant. |
| `CRASH` + `input_tmp.in` at root and in `benchmarks/` | **Accidental debris, then codified** | Empty QE input + the exact pw.x error for an empty input, timestamped 2026-01-17 during the T1–T4 buildout; later someone added `CRASH` to `.gitignore` (line 89) rather than deleting the file. |
| `benchmarks/framework/` (CLEAR runner/metrics) beside `evaluation/` | **Likely superseded remnant** | `framework/` untouched since the 02-16 "Phase 1 refactor"; all activity (harness, backends, parallel runner) is in `evaluation/`. |
| Empty dirs: `tests/`, `benchmarks/reports/`, `evaluation/{rubrics,validators}/`, `resources/pseudopotentials/` | **Aspirational scaffolding** | Created, never populated; no references that depend on them. |
| `workspaces/projects/*` with own `.git` repos | **Deliberate side-projects, undocumented** | See §12.2; READMEs and design docs inside, never mentioned by any top-level doc. |
| Model unpinned in harness | **Accidental-by-default** | No flag, no recorded model field; consistent with subscription-CLI usage rather than a considered choice. |
| MP API key + CURC creds in `.claude/settings.json` | **Deliberate convenience** | File is gitignored (`settings.json.example` is the sanitized twin); the plaintext-on-disk exposure is the accepted cost. |
| ROADMAP "Last Updated 2026-02-23" atop a 02-25 changelog | **Accidental** | Header not bumped in the uncommitted edit. |

---

## 9. Known + suspected failure points

**Known (observed, documented, or reproducible):**

1. Local execution is broken as configured: `$LMP`, `$QE_CPU`, `$QE_GPU`,
   MCP-filesystem root, and `scripts/run_*.sh` all point to nonexistent paths
   (§6.8). `harness.py --verify` cannot pass today.
2. High-variance frontier benchmarks: T10-001 75→5, T10-002 72→17, T9-003 58→0,
   T9-004 65→8 between 02-24 and 02-25 runs (same suite, days apart).
3. Long-horizon stall: T7-001 ran 5+ h, completed 3/7 temperatures, stalled 2 h,
   was killed (CURRENT_STATUS §T7).
4. Timeouts: T2-002, T4-005, T4-006, T8-005, T17-004 (fresh run).
5. Parallel runner OOM at 10 workers (6 stable) — ROADMAP 02-25 infra note.
6. Historical grader defects, fixed but indicative: metadata.json score=0 desync
   (17 benchmarks), rubric-sum arithmetic error (T15-006 58→64) — CURRENT_STATUS
   §Known Issues.
7. T9-003 κ values 30–100× low (finite-size effects) even in passing runs.
8. QE namelist crash mode (the CRASH file) — agent-side input handling produced an
   empty input file at least twice (root + benchmarks/).

**Suspected (uncertain, flagged honestly):**

9. All pass-rate claims are void under Fable 5 until re-measured (model unpinned;
   scores are Opus-era artifacts).
10. Judge-executor coupling: the same model family grading itself may compress
    observed "regressions"/"passes" in unknown ways; no human-graded calibration
    set exists in-repo (`benchmarks/rubrics/` provides structure, not calibration).
11. The vanished 3.2 GB results archive means pre-overhaul scores can no longer be
    re-audited; historical comparisons rest on markdown summaries alone.
12. VAST balance/API keys/conda envs may have rotted during dormancy (unverified —
    read-only audit).
13. ALCF Polaris account was "pending approvals" on 2026-05-28; current state
    unknown; allocation clock (expires 2026-11-28) is running regardless.
14. `project-update` engine is untested against this repo (no `.sync/manifest.yaml`
    here) — fine for its intended use in other repos, but nothing here exercises it.

---

## 10. Flags for the reviewer (evaluative itches, one line each — NOT proposals)

- Unpinned model in both executor and grader; no model field in result.json — biggest single threat to evidence continuity across the rebase.
- Absolute-path brittleness (35 files) suggests the reviewer weigh a single env/config indirection (correctness-class, since the system currently can't run).
- Dashboard/table/artifact score disagreements (§6.1–6.3) mean CURRENT_STATUS.md cannot be trusted as a source of record without artifact cross-checks.
- Self-grading loop (claude judges claude) with no human-calibrated anchor set.
- The benchmark suite tests the *old* identity (local/VAST researcher); the post-Feb compute trio — now the live direction — has zero coverage.
- "Fixing benchmarks by fixing prompts" blurs capability measurement and prompt engineering; regressions may be prompt-sensitivity artifacts.
- Two parallel benchmark frameworks (`benchmarks/framework/` vs `evaluation/`) invite confusion.
- Secrets in plaintext on disk (`.claude/settings.json` MP key; sibling asta-theorizer key files) — worth an owner decision, not an agent one.
- 1.6 GB of gitignored evidence and a vanished 3.2 GB archive: claim-to-evidence chain is fragile.
- AGENTS.md (the primary context) is the stalest of the three context docs; an agent booting from it gets a February worldview.
- SESSION_HANDOFF.md actively misdirects new sessions (dead paths, superseded status, obsolete prohibitions).
- `showcases/` (64 MB) and `workspaces/benchmarks/` blur exemplar vs. evidence; the uncommitted variability disclaimer is the owner already flagging this.

---

## 11. DRAFT CURRENT_STATE.md (per machinery/templates/CURRENT_STATE.md)

```markdown
# Current State — Agentic Science Worker (1-ScienceAgent)

**Last reviewed:** 2026-07-02  ·  **Reviewing model:** claude-fable-5
**Source of truth for live status:** CLAUDE.md (2026-05-06) + git log; AGENTS.md is
the agent persona/context but its status content is stale (2026-02-20);
benchmarks/CURRENT_STATUS.md is the benchmark dashboard, frozen 2026-02-25 with
uncommitted edits (fenced).

## System map
- `AGENTS.md` — researcher persona + principles; primary context for any coding agent
  (claude/aider/cursor). `CLAUDE.md` wraps it for Claude Code and indexes skills.
- `skills/` (symlinked at `.claude/skills`) — all domain capability as markdown:
  Jan–Feb researcher skills (lammps-simulation, quantum-espresso, mlip-simulation,
  vast-cloud, literature-search, materials-database, data-analysis,
  resource-acquisition, theory-synthesis, ggen, torch-sim) + Mar–Jun operations
  skills (iff-parameters; compute-strategy w/ backends local/vast-ai/alpine/polaris/
  crux; compute-validation; campaign-orchestration; project-update w/ Python engine).
  `skills/archive/hpc-cluster-curc/` retired.
- `benchmarks/` — 117 task YAMLs (tiers 1–4, 7–10, 12–18), harness
  (`evaluation/harness.py` → spawns `claude -p` per benchmark, LLM-judge grading via
  a second `claude -p`, per-tier pass thresholds 40–70), parallel runner,
  VAST-orphan safety tool, dashboards and methodology docs. Older `framework/`
  (CLEAR metrics) appears superseded.
- `workspaces/` (1.6 GB, gitignored) — agent work dirs: 2026-02-24/25 fresh-run
  outputs, plus three self-contained side projects under `projects/`.
- `showcases/` (64 MB) — curated successful runs (novel cathode discovery, XRD
  structure determination, cloud-GPU automation, theory synthesis, ggen, torch-sim).
- `.claude/` — settings (env for LAMMPS/QE binaries — currently dead paths),
  2 hooks (pre-Bash safety regex; post-Write/Edit operation logging to
  `logs/operations.log`), 3 subagent definitions. `.mcp.json`: playwright,
  semantic-scholar, filesystem (dead root).
- Siblings (out of repo): `../asta-paper-finder`, `../asta-theorizer` (Theorizer
  used by theory-synthesis / T12).

## Current capabilities
- Verified in the 2026-02-24/25 era (Opus-era model, results in
  `benchmarks/results/runs/`): LAMMPS MD, QE DFT on local RTX 5080 (GPU build),
  MLIP screening (MACE/CHGNet), VAST.ai full lifecycle, LAMMPS log/MSD analysis,
  theory synthesis via Theorizer (T12 3/3), behavioral/rigor tiers largely passing.
  Fresh-run aggregate: 80/97 passing (82%) with high variance on frontier tiers
  (T10-001/002 and T9-003/004 regressed to failing).
- Defined but NOT validated end-to-end in this repo: compute-strategy routing to
  CU Alpine (DTN key-only access) and ALCF Polaris/Crux (account pending as of
  2026-05-28; OTP-gated); compute-validation smoke-gates; campaign-orchestration
  WORKFLOW.md ticking; project-update engine (has unit tests; no manifest here).
- NOT currently runnable as configured: any local simulation and
  `harness.py --verify` — all binary env paths in `.claude/settings.json` point to
  pre-reorg locations that no longer exist (actual binaries:
  `/home/sf2/work/compute/gpu-tests/1-GPUTests/...`).

## Data / artifacts inventory
- `benchmarks/results/runs/` — 97 fresh-run dirs (result.json + benchmark.json +
  agent transcript each) + parallel-run summary JSON/logs. Gitignored.
- `workspaces/benchmarks/` — corresponding agent work dirs (1.6 GB). Gitignored.
- `benchmarks/results/examples/`, `workspaces/examples/` — small tracked exemplars.
- `showcases/*/outputs/` — curated evidence for headline claims (64 MB).
- Claimed pre-overhaul archive `benchmarks/results/archive/runs_20260224_pre_overhaul/`
  (3.2 GB) is NOT on disk — pre-Feb-24 raw evidence unavailable.
- `internal/validation/` — ggen/torch-sim validation results (2026-01-31).

## Active work (mirrored 2026-07-02, read-only)
- Project was dormant 2026-06-21 → 2026-07-02; woken for the intelligence rebase.
  A live agentctl session is UP (its only writes today are to the rebase status file,
  per logs/operations.log).
- Uncommitted owner edits (fenced): README/ROADMAP/CURRENT_STATUS fresh-run status
  update + showcases variability note + deletion of two Jan-17 result summaries.
- 3 unpushed commits (ALCF backends; project-update skill; Alpine→DTN repoint).
- Per ROADMAP TODOs (2026-02-25): investigate T9/T10 regressions, expand T17/T18,
  T8-006 fine-tuning, CI/CD for benchmarks. Per the May–June commit arc: driving
  real compute campaigns (Alpine/ALCF) via the compute trio.

## Known failures (observed, reproducible)
- Frontier-tier run-to-run variance (T10-001: 75→5; T10-002: 72→17; T9-003: 58→0;
  T9-004: 65→8 across 02-24→02-25 runs).
- T7-001 long-campaign stall at ~5 h (killed; partial workspace preserved).
- 5 fresh-run timeouts (T2-002, T4-005/006, T8-005, T17-004).
- Parallel runner OOM at 10 workers (6 stable).
- Dead binary/config paths post-2026-06-13 reorg (35 files reference old roots).
- QE empty-input crash debris (CRASH, input_tmp.in ×2) from 2026-01-17.

## External interfaces / dependencies
- `claude` CLI (model unpinned — executor AND grader), optional aider/cursor.
- LAMMPS + QE GPU/CPU builds from the gpu-tests project (RTX 5080 local).
- VAST.ai CLI + prepaid account; Materials Project API (key on disk);
  Semantic Scholar MCP; Playwright MCP.
- CU Alpine via dtn.rc.colorado.edu (`cu_alpine`, user sefl7948, key-only,
  campus-network dependent); ALCF Polaris/Crux (acct sefl-alcf pending 05-28,
  MobilePASS+ OTP, allocation HydrogenStorage 5,000 node-hr, expires 2026-11-28).
- Sibling ASTA Theorizer/paper-finder + conda envs (environments/*.yml).
- IFF parameter tooling (~/work/tools/iff/) via iff-parameters skill.
```

## 12. POST-DOC DISCOVERY + fenced files

### 12.1 Work on disk newer than the status docs (status docs freeze at 2026-02-25)

All of the following is **absent from README/ROADMAP/CURRENT_STATUS/SESSION_HANDOFF**;
only CLAUDE.md (05-06) partially reflects it. This is the actual latest era of the
project:

| Date | Artifact | What it is |
|---|---|---|
| 2026-03-26 | `skills/iff-parameters/` (commit `b9b1ecc`) | IFF force-field DB access skill (search/export/compose; ties to ~/work/tools/iff) |
| 2026-05-05 | `skills/compute-strategy/` (`fa4856f`), `skills/campaign-orchestration/` (`1e1e195`) | Cross-backend job routing meta-skill; stateless multi-campaign supervision over WORKFLOW.md files |
| 2026-05-06→10 | `skills/compute-validation/` (`ac2f6bc`, `e814b4c`) | Verify-before-compute gates incl. Layer A′ orchestration safety |
| 2026-05-28 | `skills/compute-strategy/backends/{polaris,crux}.md` (`8e00ba8`) | ALCF onboarding: acct sefl-alcf pending, HydrogenStorage allocation, PBS Pro, OTP auth |
| 2026-05-29 | `skills/project-update/` + `engine/` (`5c99011`) | Tier-1 in-repo update engine, stdlib Python + pytest suite (LabSync ADR-001 companion) |
| 2026-06-21 | `backends/alpine.md` rewrite (`baaa4fd`) | Alpine access repointed to the DTN: key-only, **no Duo**, `ssh cu_alpine`; NAMD 3.0.2 path on /projects |
| 2026-05-06 | `CLAUDE.md` rewrite | Introduces the "compute trio" composition guidance |
| 2026-07-02 | `logs/operations.log` | Live session hook log (2 writes, both to the rebase ops area — no project edits today) |

Interpretation (evidence-level): between March and June the project quietly became the
*fleet-wide home of compute-operations doctrine* (used by hydrogenation/NAMD campaigns
on Alpine, ALCF prep) while its own benchmark/status apparatus stayed frozen at the
February identity. The three newest commits are unpushed, so GitHub shows none of it.

### 12.2 Undocumented on-disk work (older, but in no doc)

- `workspaces/projects/parallel-lammps-hpc/` (Jan 29; own `.git`) — parallel LAMMPS
  fan-out + "mini partition" design (`mini_partition.py`, `MINI_PARTITION_DESIGN.MD`,
  `submit_mini_partition.sh`) targeting SLURM.
- `workspaces/projects/allocation-scheduler/` (Jan 29; own `.git`) — pilot allocation
  scheduler with CURC `amilan`/`atesting` submit scripts, tests, DEPLOY.md.
- `workspaces/projects/lammps-benchmarks/` (Feb 9) — LAMMPS benchmark/analysis runs.
- `benchmarks/docs/SELF_ENHANCEMENT_PROPOSAL.md` (2026-02-25, 37 KB) — drafted
  "Tier 21: self-enhancement" benchmark tier (agent installs/debugs its own tools);
  never implemented; not referenced by ROADMAP TODOs.
- `benchmarks/docs/RESULTS_CLEANUP_ANALYSIS.md` (2026-02-25) — the analysis behind
  the (uncommitted) deletion of the two Jan-17 result summaries.

### 12.3 The CRASH file's story

`CRASH` (2026-01-17 06:59) is a verbatim Quantum ESPRESSO abort report:
`read_namelists: error #2: could not find namelist &control` — exactly what `pw.x`
emits when its input lacks the `&control` block. `input_tmp.in` (0 bytes, same
minute, repo root) and `benchmarks/input_tmp.in` (0 bytes, 04:31 the same night) show
the mechanism: during the T1–T4 buildout night (changelog: "2026-01-17 Completed
T1–T4 benchmarks"), a QE invocation was made from the repo root (and once from
`benchmarks/`) with an empty temp input file; QE wrote its CRASH report into the cwd.
The debris was never cleaned — instead `CRASH` was added to `.gitignore` (line 89).
It is a fossil of an early agent error-recovery episode, not an unresolved incident.
(Both files are untracked; per rebase rules they are left in place.)

### 12.4 FENCED files — never edit, stage, restore, or commit

The dirty set (owner/live-session property, uncommitted since 2026-02-25):

1. `README.md` (modified)
2. `ROADMAP.md` (modified)
3. `benchmarks/CURRENT_STATUS.md` (modified)
4. `showcases/README.md` (modified — **present in `git status` beyond the four items
   named in the rebase brief; treated as fenced on the same basis**)
5. `benchmarks/results/BENCHMARK_RESULTS_20260117.md` (deleted in working tree — do not restore)
6. `benchmarks/results/BENCHMARK_RESULTS_VALIDATED_20260117.md` (deleted in working tree — do not restore)

Additionally fenced by this audit:

7. `logs/operations.log` — actively written by the live session's PostToolUse hook.
8. The 3 unpushed commits (`8e00ba8`, `5c99011`, `baaa4fd`) — do not push, rebase, or
   otherwise disturb; publication is an owner decision.
9. `../asta-paper-finder/`, `../asta-theorizer/` — siblings, out of rebase scope
   (listed only as context; asta-theorizer contains owner API-key files).
10. The live agentctl session itself — never interact.

### 12.5 Uncertainty register (honest gaps in this audit)

- I did not execute any harness, binary, or network call (read-only mandate); "runs"
  claims are inferred from artifacts, not re-verified.
- The fate of the 3.2 GB pre-overhaul results archive is unknown (deleted vs. moved
  off-machine); I searched the local filesystem only to depth 6.
- I sampled, not exhaustively read, the 97 result.json files; the §6 score
  divergences are confirmed for the cited IDs, and others may exist.
- Whether Alpine DTN access and the ALCF account are functional *today* is unknown.
- The precise model identity behind the February results is not recorded anywhere in
  the artifacts; "Opus-4.8-era" comes from the rebase brief, not from evidence in
  this repo.
