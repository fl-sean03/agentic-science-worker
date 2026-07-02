# Post-mortem — the `CRASH` / `input_tmp.in` debris of 2026-01-17

**Written:** 2026-07-02 (intelligence rebase, model `claude-fable-5`; evidence in
`08_upgrades/upgrade-2026-07-02/current_system_audit.md` §12.3, verified against
the on-disk files).
**Status of debris:** left in place, untracked (`CRASH` is even `.gitignore`-d,
line 89). This record exists so the episode is machinery-visible instead of folklore.

## What happened

During the T1–T4 benchmark buildout night (2026-01-17), Quantum ESPRESSO's
`pw.x` was invoked at least twice with an **empty input file**:

- `benchmarks/input_tmp.in` — 0 bytes, 04:31
- `input_tmp.in` (repo root) — 0 bytes, 06:59
- `CRASH` (repo root, 06:59) — QE's abort report, verbatim:
  `read_namelists: error #2: could not find namelist &control`

`pw.x` writes its `CRASH` report into the current working directory — hence
debris at the repo root and in `benchmarks/`. Root cause: agent-side input
handling produced/served an empty temp input, and the invocation ran from the
repo root rather than an isolated workspace.

The mechanism was independently re-verified during the 2026-07-02 gate evals
(E-03): an infra test (`04_qe_binary.yaml`, "QE CPU responds to help") executed
by `framework/runner.py`'s `command_succeeds` branch **without a cwd** is the
producer of the repo-root twin.

## Why it matters

1. It recurred (≥2×) and was never structurally addressed — the debris was
   codified into `.gitignore` instead (decision D18 in the historical review).
2. The failure class is 100% catchable pre-run by a deterministic check; no
   model judgment required.

## What was done (2026-07-02)

- `scripts/lint_sim_input.py` (+ `tests/test_lint_sim_input.py`): deterministic
  pre-run lint; blocks empty/`&control`-less QE inputs (this exact class) and
  LAMMPS units/pair-style inconsistencies. Standalone prototype, EV-A5 green.
- **Not** wired into `.claude/hooks/validate_simulation.py` — that hook is the
  live session's operating surface; activation is staged as a proposal
  (owner decision B-2, `08_upgrades/upgrade-2026-07-02/proposals/`).
- The debris files themselves are owner property/fossils; removing them is a
  one-line owner action, not taken here.

## Prevention doctrine

Never run simulations from the repo root; always from an isolated workspace.
Pre-run, lint the input deterministically; the lint refusing a file is a
*cheap* failure. (Workspace hygiene is already benchmark-enforced; the lint
closes the input-validity half.)
