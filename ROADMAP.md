# Roadmap

This roadmap describes the direction of the Agentic Science Worker. It is intentionally
high-level; concrete work is tracked in issues.

## Now (v0.2)

- **Durable execution.** Long-horizon DFT/MD campaigns that survive interruptions — jobs are
  detached, state lives in files, and the agent re-enters to harvest. This removes the
  "agent parks and dies waiting on a long job" failure mode.
- **Verifiable provenance.** Every reported value can be walked back to the exact inputs that
  produced it, so results are auditable rather than asserted.
- **Rigorous benchmarking.** Correctness-gated, judge-independent grading, plus reliability
  (pass^k across repeat runs) and cost-efficiency axes that stay meaningful as models
  saturate one-shot correctness.

## Next

- **Long-horizon reproduction tier.** Benchmarks whose difficulty is *endurance* — staying
  coherent and in-budget across a multi-day campaign — not just knowing more physics.
- **Provenance tooling.** Query and export campaign provenance (e.g. as portable, citable
  research artifacts) so a completed study ships with its evidence.
- **Broader backends.** More scheduler and cloud targets behind the same compute-strategy
  interface.

## Later

- **Additional science domains** beyond the current materials focus.
- **Deeper multi-agent orchestration** for parallel sub-studies under a single research goal.

Have a use case or a benchmark you'd like to see? Open an issue.
