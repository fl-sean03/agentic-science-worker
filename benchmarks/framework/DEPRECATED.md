# DEPRECATED — superseded by `benchmarks/evaluation/`

Marker added 2026-07-02 (intelligence rebase, model `claude-fable-5`).

This directory (CLEAR metrics runner, `runner.py`/`metrics.py`) is a remnant of
the 2026-02-16 "Phase 1 refactor". All live harness activity — task loading,
backends, LLM grading, parallel running, artifact writing — happens in
`benchmarks/evaluation/`. Nothing imports from this directory.

It is deliberately **not deleted** (tidiness-only change, rejected this cycle as
U-R7; see `08_upgrades/upgrade-2026-07-02/uplift_opportunities.md`). If a future
correctness change touches these paths, bundle the removal then — with owner
awareness.
