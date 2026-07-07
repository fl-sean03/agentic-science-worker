# Agentic Science Worker

> An autonomous AI researcher for computational materials science — not a tool that runs commands, but an independent lab member that takes ownership of research problems.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Benchmarks](https://img.shields.io/badge/benchmarks-88%2F97%20(90.7%25)-brightgreen.svg)](benchmarks/results/GENERATED_STATUS.md)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Agents](https://img.shields.io/badge/agents-Claude%20Code%20%7C%20Aider%20%7C%20Cursor-8A2BE2.svg)](#supported-agents)

The Agentic Science Worker (ASW) turns a coding agent into a competent computational
researcher. Given a scientific question, it researches the methodology, finds parameters,
runs the simulations, verifies results against the literature, and iterates until the
physics is sound — the way a capable graduate student works independently.

- **What it is:** a portable capability layer — agent instructions (`AGENTS.md`), a library
  of domain **skills**, evaluation harness, and configuration — that rides on top of an
  existing coding agent.
- **What it is not:** a chat wrapper. The unit of work is a *research outcome* (a converged
  calculation, a verified property, a tested hypothesis), graded on real scientific criteria.

---

## Contents

- [Highlights](#highlights)
- [Benchmarks](#benchmarks)
- [How it works](#how-it-works)
- [Supported agents](#supported-agents)
- [Quick start](#quick-start)
- [Skills](#skills)
- [Repository structure](#repository-structure)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Citing](#citing)
- [License](#license)

## Highlights

- **Novel materials discovery** — autonomously proposed and screened Li-ion cathode
  candidates, including Li₂Ni(PO₄)(SO₄) at ~5.1 V.
- **Cross-modal reasoning** — determined a crystal structure from an XRD pattern using
  first-principles methods.
- **Durable long-horizon execution** — launches, detaches, and harvests multi-hour DFT/MD
  campaigns that outlive a single agent turn, resuming cleanly across interruptions.
- **Verifiable results** — every reported value is anchored to the exact inputs that
  produced it, and graded against sealed reference values rather than an LLM's say-so.
- **Cloud burst** — full VAST.ai GPU lifecycle (provision → execute → clean up) for overflow
  compute.

See it in action: **[Showcases »](showcases/)**

## Benchmarks

A held-out suite of **97 tasks** measures whether the agent can *do research*, not just run
commands — spanning molecular dynamics, DFT, ML-potential screening, autonomous multi-step
campaigns, literature synthesis, data analysis, and cloud-GPU execution. Each task is graded
on a real, checkable scientific outcome.

### Current results — 88/97 (90.7%) on the Opus-4.8 baseline

| Category | Tiers | Pass |
|----------|-------|-----:|
| Foundations | T1–T4 | 20/21 |
| Research campaigns | T7 | 3/3 |
| ML / MLIP screening | T8 | 5/7 |
| Autonomous research | T9 | 3/4 |
| Frontier DFT | T10 | 3/4 |
| Theory synthesis | T12 | 3/3 |
| Robustness & cognition | T13–T16 | 41/43 |
| Cloud GPU (VAST.ai) | T17 | 7/8 |
| Data analysis | T18 | 3/4 |
| **Total** | | **88/97 (90.7%)** |

*One task is excluded as an infrastructure VOID (98 tasks total). Full per-task run logs:
**[benchmark status »](benchmarks/results/GENERATED_STATUS.md)**.*

### How grading works

Scoring is **correctness-gated and judge-independent**:

- Each task defines **mechanical anchors** — numeric checks against sealed reference values
  (e.g. a formation energy within tolerance of DFT).
- A separate **frozen LLM judge** scores *process* quality — verification, uncertainty,
  provenance — but **can never overturn a failed anchor**.
- **Infrastructure failures are VOIDed** (unscored), never counted as capability failures.

As frontier models saturate correctness, two further axes keep the suite discriminating:

- **Reliability** — each task is run *k* times; we report pass^k (does it succeed *every*
  time, not just once).
- **Cost-efficiency** — spend and wall-time against a per-task reference budget, so a right
  answer that costs 15× more is scored differently from an efficient one.

## How it works

```
┌──────────────────────────────────────────────────────────────┐
│                         Coding Agent                         │
│         Claude Code  ·  Aider  ·  Cursor  ·  Codex           │
│      AGENTS.md defines researcher behavior & methodology     │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                            Skills                            │
│   simulation · DFT · MLIP · literature · databases · data    │
│   compute strategy · long-compute · campaign orchestration   │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                        External Tools                        │
│  LAMMPS · Quantum ESPRESSO · MACE/CHGNet/M3GNet · VAST · Web  │
└──────────────────────────────────────────────────────────────┘
```

The agent reads `AGENTS.md` as its primary context, then composes **skills** — self-contained
capability modules (`skills/<name>/SKILL.md`) — to plan and execute. Long-running work is
handled by a durable execution discipline: jobs are detached so they survive a turn ending,
their state lives in files (not the agent's context), and the agent re-enters to harvest
results. Everything the agent claims is recorded so it can be walked back to its inputs.

## Supported agents

| Agent | Status | Configuration |
|-------|--------|---------------|
| [Claude Code](https://claude.com/claude-code) | Full support | `AGENTS.md`, `.claude/` |
| [Aider](https://aider.chat) | Full support | `AGENTS.md`, `configs/aider/` |
| [Cursor](https://cursor.com) | Full support | `AGENTS.md`, `.cursorrules` |
| [OpenAI Codex](https://openai.com/codex) | Planned | `AGENTS.md` |

All agents read [`AGENTS.md`](AGENTS.md) — the [industry-standard](https://agents.md) agent
context file — as their primary instructions.

## Quick start

### Prerequisites

- A supported coding agent (Claude Code, Aider, or Cursor)
- Python 3.10+
- The `science-tools` conda environment (harness, MLIP, analysis):
  `conda env create -f environments/science-tools.yml`
- [LAMMPS](https://www.lammps.org/) (GPU build recommended) for molecular dynamics
- [Quantum ESPRESSO](https://www.quantum-espresso.org/) (optional) for DFT
- A [Materials Project](https://next-gen.materialsproject.org/api) API key

### Installation

```bash
git clone https://github.com/fl-sean03/agentic-science-worker.git
cd agentic-science-worker

# copy and fill in local configuration (paths + API keys stay out of git)
cp config.example.yaml config.yaml
cp .claude/settings.json.example .claude/settings.json
cp .mcp.json.example .mcp.json
```

Edit `config.yaml` with your binary paths and API keys:

```yaml
binaries:
  lammps: "/path/to/lammps/bin/lmp"
  qe_cpu: "/path/to/qe/bin"
api_keys:
  materials_project: "YOUR_MP_API_KEY"
```

Verify the setup:

```bash
cd benchmarks/evaluation && python harness.py --verify
```

### Run the agent

```bash
# Claude Code
claude

# Aider
aider --read AGENTS.md

# Cursor — uses AGENTS.md and .cursorrules automatically
cursor .
```

Example prompts (any agent):

```
Calculate the self-diffusion coefficient of liquid argon at 94 K.
Find the lattice constant of copper using the Mishin EAM potential.
Compute the band structure of silicon.
```

### Run benchmarks

```bash
cd benchmarks/evaluation
python harness.py --list                 # list available benchmarks
python harness.py BENCH-T1-001           # run one
python harness.py --tier 1               # run a whole tier
```

## Skills

Skills are self-contained capability modules under [`skills/`](skills/). Each has a
`SKILL.md` the agent reads on demand.

| Domain | Skills |
|--------|--------|
| Simulation | `lammps-simulation`, `quantum-espresso`, `mlip-simulation`, `torch-sim` |
| Compute discipline | `compute-strategy`, `compute-validation`, `long-compute`, `campaign-orchestration` |
| Knowledge | `literature-search`, `materials-database`, `iff-parameters`, `theory-synthesis` |
| Execution | `vast-cloud`, `resource-acquisition`, `data-analysis` |

The four compute-discipline skills compose: **strategy** picks the backend, **validation**
gates production behind smoke tests, **long-compute** detaches jobs that outlive a turn, and
**campaign-orchestration** manages long-running stateful execution.

## Repository structure

```
agentic-science-worker/
├── AGENTS.md            # primary agent context (methodology, conventions)
├── skills/              # capability modules (SKILL.md each)
├── benchmarks/          # evaluation suite, harness, and results
│   ├── evaluation/      # harness.py and grading
│   └── results/         # per-task run logs + GENERATED_STATUS.md
├── examples/            # canonical worked examples
├── showcases/           # highlight results with full write-ups
├── environments/        # conda environment specs
├── configs/             # per-agent configuration (aider, cursor, ...)
├── templates/           # scaffolding for new tasks/skills
├── docs/                # methodology and design notes
├── research/            # reference material
├── scripts/             # utilities
└── tests/               # harness tests
```

## Roadmap

See [ROADMAP.md](ROADMAP.md). In short: deepen durable long-horizon execution, expand the
verifiable-provenance substrate, and grow the benchmark suite toward multi-day reproduction
tasks where reliability and cost — not one-shot correctness — are the real frontier.

## Contributing

Contributions are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md) for how skills, benchmarks,
and grading are structured. Please open an issue to discuss substantial changes first.

## Citing

If you use the Agentic Science Worker in academic work, please cite it (see
[CITATION.cff](CITATION.cff)):

```bibtex
@software{florez_asw_2026,
  author  = {Florez, Sean},
  title   = {Agentic Science Worker: an autonomous AI researcher for
             computational materials science},
  year    = {2026},
  url      = {https://github.com/fl-sean03/agentic-science-worker}
}
```

## License

Released under the [MIT License](LICENSE).

## Acknowledgments

Built on the open computational-materials ecosystem — LAMMPS, Quantum ESPRESSO, the Materials
Project, and the MACE / CHGNet / M3GNet interatomic-potential communities.
