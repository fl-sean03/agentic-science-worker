# Agentic Science Worker

> An autonomous AI researcher for computational materials science — not a tool that runs commands, but an independent lab member that takes ownership of research problems.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![Agents](https://img.shields.io/badge/agents-Claude%20Code%20%7C%20Aider%20%7C%20Cursor-8A2BE2.svg)](#supported-agents)

The Agentic Science Worker (ASW) turns a coding agent into a competent computational
researcher. Given a scientific question, it researches the methodology, finds parameters,
runs the simulations, verifies results against the literature, and iterates until the
physics is sound — the way a capable graduate student works independently.

This repository is the **project monorepo** — the single home for ongoing development:

- **The capability core** — agent instructions (`AGENTS.md`) and a library of domain
  **skills** that ride on top of an existing coding agent, turning it into a research worker.
- **[Caliber](caliber/)** — the benchmark that measures autonomous materials-science agents
  on three axes (correctness × reliability × cost), with its runners/"harnesses" and
  versioned task generations. Public methodology, private answers.
- **What it is not:** a chat wrapper. The unit of work is a *research outcome* (a converged
  calculation, a verified property, a tested hypothesis), graded on real scientific criteria.

---

## Contents

- [Highlights](#highlights)
- [Caliber — the benchmark](#caliber--the-benchmark)
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

## Caliber — the benchmark

Measuring the agent is a first-class part of this project, kept as its own product:
**[Caliber »](caliber/)**. It grades autonomous materials-science agents on whether they
can *do research* — choose a sound method, run the real calculation, verify their own
numbers, and report honestly — across molecular dynamics, DFT, ML-potential work,
multi-step campaigns, and robustness traps.

Every run is scored on **three orthogonal axes**, because a frontier agent can be
correct-but-unreliable or correct-but-ruinously-expensive:

- **Correctness gate** — mechanical numeric checks against a sealed, high-compute reference
  the *grader* computes (oracle-escrow); a frozen process judge scores method/uncertainty/
  provenance but can never overturn the gate.
- **Reliability (pass^k)** — each task run *k* times; we report the probability it passes
  *every* trial, not just one lucky run.
- **Cost-efficiency** — dollars and tokens per correct solution, on an accuracy-vs-cost
  Pareto frontier.

Difficulty is a **dial, not a fixed bar** (a coupled-stage *horizon* from trivial to
end-to-end paper reproduction), so the benchmark degrades gracefully instead of saturating.
Public methodology lives in [caliber/METHODOLOGY.md](caliber/METHODOLOGY.md); sealed answers
stay in a separate private store. No leaderboard numbers are published until a generation is
frozen with pass^k + cost.

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
python -m pytest caliber/scoring -q     # scoring/evidence/provenance tests
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

### Run the benchmark (Caliber)

```bash
# sweep a model across the sealed task set on its native harness
python caliber/suite/native_sweep.py --reps 3 --lanes 3

# audit a completed run (wake pattern, cost anatomy, artifact integrity)
python caliber/suite/native_audit.py <run_dir> --brief
```

Sealed answer keys are injected from a separate private store at grade time; see
[caliber/METHODOLOGY.md](caliber/METHODOLOGY.md).

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
agentic-science-worker/          # the project monorepo
├── AGENTS.md            # primary agent context (methodology, conventions)
├── skills/              # capability modules (SKILL.md each) — the capability core
├── caliber/             # the benchmark (its own product)
│   ├── METHODOLOGY.md   # three-axis scoring, oracle-escrow grading, difficulty horizon
│   ├── harnesses/       # per-model native runners (native-claude/; more added over time)
│   ├── scoring/         # scoring, frozen judge, evidence store, provenance graph
│   └── suite/           # versioned task generations (batch1/, ...) + sweep/audit tooling
├── examples/            # canonical worked examples
├── showcases/           # highlight results with full write-ups
├── environments/        # conda environment specs
├── configs/             # per-agent configuration (aider, cursor, ...)
├── templates/           # scaffolding for new tasks/skills
├── docs/                # methodology and design notes
├── research/            # reference material
├── scripts/             # utilities
└── tests/               # tests
```
Sealed benchmark answers live in a separate private store, never in this repo.

## Roadmap

See [ROADMAP.md](ROADMAP.md). In short: deepen durable long-horizon execution, expand the
verifiable-provenance substrate, and grow **Caliber** toward its next generation — oracle-
escrowed, procedurally-generated task families reaching multi-day reproduction, where
reliability and cost (not one-shot correctness) are the real frontier.

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
