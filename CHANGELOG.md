# Changelog

All notable changes to this project are documented here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/).

## [0.2.0] — 2026-07

### Added
- **Durable long-horizon execution** — detach/harvest discipline for DFT/MD campaigns that
  outlive a single agent turn, with crash-safe resume (`skills/long-compute`,
  `skills/campaign-orchestration`).
- **Verifiable provenance** — reported values are anchored to the exact inputs that produced
  them.
- **Reliability & cost-efficiency benchmark axes** — pass^k over repeat runs and mechanical
  cost-efficiency against per-task reference budgets, alongside correctness.
- Standard open-source project files: `LICENSE` (MIT), `CHANGELOG.md`, `CITATION.cff`,
  `SECURITY.md`.

### Changed
- **Benchmark baseline refreshed to Opus-4.8: 88/97 (90.7%)**, with per-task run logs in
  `benchmarks/results/GENERATED_STATUS.md`.
- Professional README and repository restructure.
- Grading hardened: infrastructure failures are bucketed as VOID (unscored) rather than
  counted as capability failures.

### Removed
- Internal development scratch, superseded planning snapshots, and historical handoff notes
  are no longer part of the public tree.

## [0.1.0] — 2026-02

- Initial public release: skill-based agent for LAMMPS / Quantum ESPRESSO / MLIP workflows,
  literature and materials-database access, cloud-GPU execution, and a tiered benchmark suite.
