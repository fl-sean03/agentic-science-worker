> **Historical record (2026-06-13).** Paths here predate the 2026-07-10 monorepo
> restructure; `benchmarks/` was carved out and the benchmark now lives under
> `caliber/`. Kept for provenance only.

# Path migration record — 2026-06-13 machine reorg (repairs applied 2026-07-02)

**Author:** intelligence rebase, model `claude-fable-5` (rebase-2026-07-02, Slice S5).

The machine was reorganized twice; both moves stranded absolute paths across this
repo (35 files found referencing dead roots on 2026-07-02):

| Dead root | Live root |
|---|---|
| `/home/sf2/LabWork/Workspace/29-AgenticScienceWorker/` | `/home/sf2/work/agents/science-agent/` |
| `/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/` | `/home/sf2/work/archive/gpu-tests-wsl/1-GPUTests/` |

> **Update 2026-07-03:** gpu-tests moved a second time — the 06-13 landing spot
> `~/work/compute/gpu-tests/1-GPUTests/` was archived to
> `~/work/archive/gpu-tests-wsl/1-GPUTests/` at the fleet close-out (compute M-3:
> WSL-era binaries do not run on bare-metal; working LAMMPS is
> `/home/sf2/builds/lammps/build/lmp`, QE pending toolchain rebuild — owner queue).
> The Live-root column above reflects the post-07-03 location.

## Repaired mechanically (2026-07-02, this branch)

Machinery/config files — old→new substitution only, every substituted target
verified to exist on disk:

- `benchmarks/infrastructure_tests/**/*.yaml` (13 files; `01_system_baseline.yaml`
  additionally retires its WSL2 check — the machine is bare-metal Ubuntu now)
- `benchmarks/scripts/validate_skills.py`
- `benchmarks/tasks/`: `BENCH-T10-004`, `BENCH-T16-003`, `BENCH-T16-013`
  (path constants inside task text only — prompts/thresholds/rubrics otherwise
  byte-identical; note for longitudinal comparisons)
- `scripts/run_lammps.sh`, `scripts/run_qe.sh` (also made env-overridable:
  `LMP`/`QE_CPU`/`QE_GPU`/`NVHPC_ENV`)
- `showcases/verify_all.py`, `showcases/theory-synthesis/{showcase.yaml,workspace/demo_theorizer.py}`
- `research/BENCHMARK_TRACKING.md` (self-declared historical, but contains
  copy-paste commands)

**Runnability caveat:** the gpu-tests binaries exist at the live root but
currently fail to execute (missing OpenMPI-4 runtime; see `harness.py --verify`
probe output and `config.yaml`). Path repair makes references *true*, not the
toolchain *healthy* — toolchain repair belongs to the gpu-tests project (owner
queue).

## Deliberately NOT repaired

- **Historical artifacts** (would falsify evidence): `benchmarks/results/examples/*.json`
  (5 files) and `benchmarks/docs/RESULTS_CLEANUP_ANALYSIS.md` — they record what
  ran/was analyzed in Jan–Feb at the paths of that era.
- **Fenced owner files:** `ROADMAP.md`, `benchmarks/CURRENT_STATUS.md` (dirty
  working tree; owner decision B-6).
- **Live agent operating surface** (owner sign-off required; exact diffs staged in
  `08_upgrades/upgrade-2026-07-02/proposals/`): `SESSION_HANDOFF.md`,
  `.claude/agents/simulation-runner.md`, `.claude/settings.json` (untracked),
  `.mcp.json` (untracked), `skills/quantum-espresso/SKILL.md`,
  `skills/compute-strategy/SKILL.md` + `backends/{polaris,crux}.md`, `AGENTS.md`.
