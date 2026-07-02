# Benchmark truth reconciliation — 2026-07-02 (additive record)

**Author:** intelligence rebase, model `claude-fable-5` (Slice A3, rebase-2026-07-02)
**Method:** every number below is derived from `benchmarks/results/runs/*/result.json`
by `benchmarks/evaluation/generate_status.py` (never retyped); see
`GENERATED_STATUS.md` for the full table and per-row divergences.

## Artifact truth (2026-02-24/25 fresh run, the latest full run)

- **80 passed / 12 failed / 5 timeout — 97 tasks with artifacts (82.5%).**
- One additional workspace exists without a result artifact (T7-001, stalled ~5 h and killed).
- No artifact records which model executed or graded these runs (fixed going
  forward by the 2026-07-02 model-identity pin, Slice A1).

## Committed claims vs artifact truth

- The **committed** `README.md` (as of `baaa4fd`) claims "81/86 benchmarks passing
  (100% pass rate)" — inconsistent with the artifacts above, and what GitHub
  currently shows.
- `benchmarks/CURRENT_STATUS.md` (committed) has a fresh-run summary but per-tier
  tables that predate the fresh run: 52 rows disagree with artifacts (both
  directions), including the confirmed set
  T10-003/004, T12-001/002/003, T7-002/003, T8-005, T15-007, T16-015/016.

## The owner's corrections exist and take precedence

The working tree contains **uncommitted owner edits** (dated 2026-02-25) to
`README.md`, `ROADMAP.md`, `benchmarks/CURRENT_STATUS.md`, `showcases/README.md`,
plus two deletions of superseded Jan-17 result summaries. Those edits already
contain the honest corrections (e.g. README → "80/97, 82%"). **This record does
not touch, restore, or supersede them** — they are the owner's; whether/how to
land them (and push the 3 unpushed commits) is owner decision **B-6** in
`08_upgrades/upgrade-2026-07-02/migration_plan.md` §3. A read-only snapshot of
those edits is preserved at
`08_upgrades/upgrade-2026-07-02/baseline/fenced-worktree-snapshot/`.

## Also on record

- The claimed pre-overhaul archive `benchmarks/results/archive/runs_20260224_pre_overhaul/`
  (3.2 GB) is **not on disk**; recovery from backup tiers is owner decision **B-7**.
- Historical result summaries under `results/` and `results/examples/` are
  artifacts of their era and are deliberately left byte-identical (some contain
  pre-2026-06-13 filesystem paths; see `docs/PATH_MIGRATION_2026-06-13.md`).
