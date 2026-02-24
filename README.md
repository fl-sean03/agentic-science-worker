# Agentic Science Worker

An autonomous AI researcher for computational materials science. Not a tool that executes commands—an independent lab member that takes ownership of research problems.

**Current Status:** 81/86 benchmarks passing (100% pass rate) | [View Dashboard](benchmarks/CURRENT_STATUS.md)

## Vision

**Today:** Handle defined workflows and research questions autonomously.

**Tomorrow:** Receive a group meeting transcript, work independently for hours or days, return with research contributions—hypotheses tested, literature synthesized, calculations completed.

The goal is not to help humans do science faster. It's to build a system that **does science**: forms hypotheses, tests them computationally, identifies what's interesting, and generates knowledge that didn't exist before.

## Recent Highlights

- **Novel Material Discovery**: Autonomously discovered 9 novel Li-ion cathode materials including Li₂Ni(PO₄)(SO₄) with 5.1V voltage (T10-001: 75)
- **Cross-Modal Reasoning**: Determined crystal structure from XRD pattern using computational methods (T10-002: 72)
- **Cloud GPU Integration**: Full VAST.ai lifecycle management - provision, execute, cleanup (T17: 97/91/92)
- **Publication-Ready Analysis**: MSD/diffusion calculations, thermodynamic parsing (T18: 92/92)

**See real examples:** [Showcases](showcases/) | [Novel Cathode Discovery](showcases/novel-cathode-discovery/) | [XRD Structure Determination](showcases/xrd-structure-determination/)

## Overview

The Agentic Science Worker can:

- **Run molecular dynamics simulations** (LAMMPS) with literature-sourced parameters
- **Perform DFT calculations** (Quantum ESPRESSO) for electronic structure
- **Use ML interatomic potentials** (MACE, CHGNet, M3GNet) for fast screening
- **Provision cloud GPUs** (VAST.ai) for overflow compute
- **Search scientific literature** and extract methodology/parameters
- **Query materials databases** (Materials Project) for structures and properties
- **Analyze results** with publication-quality figures and error propagation

Given a scientific question, it researches the methodology, finds parameters, runs simulations, verifies results against literature, and iterates until achieving physically reasonable results—like a competent graduate student working independently.

## Supported Coding Agents

Works with multiple coding agents ([Claude Code](https://claude.com/claude-code), [Aider](https://aider.chat), [Cursor](https://cursor.com)). Each reads `AGENTS.md` as primary context, gaining the knowledge and principles to work as an autonomous researcher.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Coding Agent                            │
│    Claude Code │ Aider │ OpenAI Codex │ Cursor              │
│     (AGENTS.md defines researcher behavior and methodology) │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        Skills                               │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │ LAMMPS   │ │ QE/DFT   │ │ VAST.ai  │ │ MLIP     │       │
│  │ Sim      │ │ Calc     │ │ Cloud    │ │ Potentials│      │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐       │
│  │Literature│ │Materials │ │ Data     │ │ Resource │       │
│  │ Search   │ │ Database │ │ Analysis │ │ Acquire  │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Tools                           │
│  LAMMPS │ Quantum ESPRESSO │ MACE/CHGNet │ VAST.ai │ Web   │
└─────────────────────────────────────────────────────────────┘
```

## Supported Agents

| Agent | Status | Configuration |
|-------|--------|---------------|
| [Claude Code](https://claude.com/claude-code) | Full Support | `AGENTS.md`, `.claude/` |
| [Aider](https://aider.chat) | Full Support | `AGENTS.md`, `configs/aider/` |
| [OpenAI Codex](https://openai.com/codex) | Planned | `AGENTS.md` |
| [Cursor](https://cursor.com) | Full Support | `AGENTS.md`, `.cursorrules` |

All agents read `AGENTS.md` (the [industry standard](https://github.com/AgenticAI-Foundation/AGENTS.md)) as their primary context file.

## Quick Start

### Prerequisites

- A supported coding agent:
  - [Claude Code CLI](https://claude.com/claude-code) with subscription, OR
  - [Aider](https://aider.chat) with API key, OR
  - [Cursor](https://cursor.com)
- Python 3.10+
- LAMMPS (with GPU support recommended)
- Quantum ESPRESSO (optional, for DFT)
- Materials Project API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/agentic-science-worker.git
cd agentic-science-worker
```

2. Copy and configure settings:
```bash
cp config.example.yaml config.yaml
cp .claude/settings.json.example .claude/settings.json
cp .mcp.json.example .mcp.json
```

3. Edit configuration files with your paths and API keys:
```yaml
# config.yaml
binaries:
  lammps: "/path/to/your/lammps/bin/lmp"
  qe_cpu: "/path/to/qe/bin"

api_keys:
  materials_project: "YOUR_MP_API_KEY"
```

4. Verify infrastructure:
```bash
cd benchmarks/evaluation
python harness.py --verify
```

### Running the Agent

**With Claude Code:**
```bash
cd /path/to/agentic-science-worker
claude
```

**With Aider:**
```bash
cd /path/to/agentic-science-worker
aider --read AGENTS.md
```

**With Cursor:**
```bash
cursor .
# Uses AGENTS.md and .cursorrules automatically
```

Example prompts (any agent):
```
Calculate the self-diffusion coefficient of liquid argon at 94K
Find the lattice constant of copper using the Mishin EAM potential
Calculate the band structure of silicon
```

## Benchmark Suite

The project includes a comprehensive benchmark suite to evaluate agent capabilities:

### Current Results (81/86 passing, 100% pass rate)

| Tier | Category | Benchmarks | Status |
|------|----------|------------|--------|
| T1-T4 | Foundation | 21 | 100% ✅ |
| T7 | Research Campaigns | 1/3 | 33% (2 need HPC) |
| T8 | ML/MLIP | 6/7 | 86% ✅ |
| T9 | Autonomous Research | 3/5 | 60% (2 need DFT data) |
| T10 | Frontier DFT | 4/4 | **100%** ✅ Novel discovery, XRD, phonon research |
| T13-T16 | Quality & Cognition | 43 | 100% ✅ |
| T17 | Cloud GPU (VAST.ai) | 3/3 | 100% ✅ Scores: 97, 91, 92 |
| T18 | Data Analysis | 2/2 | 100% ✅ Scores: 92, 92 |

*T5-T6, T11 archived (HPC deferred). T12 blocked on Theorizer MCP.*

### Running Benchmarks

```bash
cd benchmarks/evaluation

# List available benchmarks
python harness.py --list

# List available agent backends
python harness.py --list-backends

# Run a single benchmark
python harness.py BENCH-T1-001

# Run with a specific backend
python harness.py BENCH-T1-001 --backend claude
python harness.py BENCH-T1-001 --backend aider  # when implemented

# Run all benchmarks in a tier
python harness.py --tier 1

# Run with HPC tiers
python harness.py --all --include-hpc
```

### Benchmark Results

Results are saved to `benchmarks/results/runs/` with:
- `result.json` - Scores, grading details, agent output
- `benchmark.json` - Original benchmark definition
- `agent_output.txt` - Full agent transcript

## Configuration

### Environment Variables

| Variable | Description |
|----------|-------------|
| `LMP` / `LAMMPS_PATH` | Path to LAMMPS binary |
| `QE_CPU` / `QE_PATH` | Path to QE binaries directory |
| `QE_GPU` | Path to GPU-enabled QE (optional) |
| `MP_API_KEY` | Materials Project API key |
| `HPC_USER` | HPC cluster username |
| `HPC_HOST` | HPC login node hostname |

### Files

| File | Purpose |
|------|---------|
| `AGENTS.md` | **Primary** agent context (industry standard) |
| `CLAUDE.md` | Claude Code-specific wrapper |
| `skills/` | Skill definitions (LAMMPS, QE, HPC, etc.) |
| `configs/` | Agent-specific configurations |
| `.claude/settings.json` | Claude Code permissions |
| `.mcp.json` | MCP server configuration |
| `config.yaml` | User-specific configuration |

## Project Structure

```
agentic-science-worker/
├── AGENTS.md                 # Primary agent context (industry standard)
├── CLAUDE.md                 # Claude Code-specific wrapper
├── config.example.yaml       # Configuration template
├── skills/                   # Skill definitions (portable)
│   ├── lammps-simulation/    # Molecular dynamics
│   ├── quantum-espresso/     # DFT calculations
│   ├── vast-cloud/           # VAST.ai cloud GPU management
│   ├── mlip-simulation/      # ML potentials (MACE, CHGNet)
│   ├── literature-search/    # Paper search and extraction
│   ├── materials-database/   # Materials Project queries
│   ├── data-analysis/        # Property calculations, plotting
│   ├── resource-acquisition/ # Finding parameters, structures
│   └── archive/              # Archived skills (HPC, etc.)
├── benchmarks/
│   ├── CURRENT_STATUS.md     # Live dashboard
│   ├── tasks/                # Benchmark definitions (YAML)
│   │   ├── tier1_basic/      # Foundation tasks
│   │   ├── tier10_frontier/  # Novel discovery, XRD reasoning
│   │   ├── tier17_cloud_gpu/ # VAST.ai lifecycle tests
│   │   ├── tier18_data_analysis/  # MSD, plotting, errors
│   │   └── ...
│   ├── evaluation/           # Harness and graders
│   │   ├── harness.py
│   │   ├── grader.py
│   │   ├── llm_grader.py
│   │   └── vast_safety.py    # Cloud instance cleanup
│   └── results/              # Benchmark results
├── examples/                 # Canonical workflow examples
├── research/                 # Research methodology docs
└── workspaces/               # Agent work directories (gitignored)
```

## Cloud GPU Integration (VAST.ai)

The agent can provision and use cloud GPUs via VAST.ai for overflow compute:

1. Install VAST CLI and authenticate:
```bash
pip install vastai
vastai set api-key YOUR_API_KEY
```

2. The agent can then autonomously:
- Search for cost-effective GPUs (`vastai search offers`)
- Provision instances with appropriate images
- Transfer files via SCP, run calculations
- Monitor job progress remotely
- **Always clean up** - destroy instances after completion

3. Built-in safety:
- Instance labeling for tracking (BENCH-* prefix)
- Post-benchmark orphan detection
- Cost tracking and limits

Example workflow the agent handles:
```
Local: Prepare inputs → Cloud: Run GPU job → Local: Analyze results
```

*HPC cluster support archived - see `skills/archive/hpc-cluster-curc/` if needed.*

## ML Potentials (Optional)

For ML-accelerated simulations, install additional packages:

```bash
pip install mace-torch matgl chgnet ase phonopy
```

The agent can then use universal ML interatomic potentials (MACE, M3GNet, CHGNet) for:
- Fast property screening
- Large-scale MD simulations
- Phonon calculations

## Contributing

Contributions welcome! Areas of interest:
- New benchmark tasks
- Additional skills (VASP, CP2K, etc.)
- **New agent backends** (OpenAI Codex, etc.)
- Improved grading rubrics
- Documentation

See [CONTRIBUTING.md](CONTRIBUTING.md) for developer tips and [ROADMAP.md](ROADMAP.md) for planned features.

## License

MIT License - see LICENSE file.

## Acknowledgments

- Built on [Claude Code](https://claude.com/claude-code) by Anthropic
- Uses [Materials Project](https://materialsproject.org/) for structures
- Literature search via [Semantic Scholar](https://www.semanticscholar.org/)
