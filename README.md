# Agentic Science Worker

An autonomous AI agent system for computational materials science research. Designed to work with multiple coding agents ([Claude Code](https://claude.com/claude-code), [Aider](https://aider.chat), [OpenAI Codex](https://openai.com/codex), [Cursor](https://cursor.com)), this system enables AI to conduct scientific research like a PhD-level computational scientist.

## Overview

The Agentic Science Worker can:

- **Run molecular dynamics simulations** (LAMMPS) with literature-sourced parameters
- **Perform DFT calculations** (Quantum ESPRESSO) for electronic structure
- **Search scientific literature** and extract methodology/parameters
- **Query materials databases** (Materials Project) for structures and properties
- **Analyze results** and compare with published values
- **Execute on HPC clusters** for large-scale computations

The agent operates autonomously: given a scientific question, it researches the methodology, finds parameters, runs simulations, verifies results against literature, and iterates until achieving physically reasonable results.

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
│  │ LAMMPS   │ │ QE       │ │ HPC      │ │ MLIP     │       │
│  │ Skill    │ │ Skill    │ │ Skill    │ │ Skill    │       │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘       │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐                    │
│  │Literature│ │Materials │ │ Data     │                    │
│  │ Search   │ │ Database │ │ Analysis │                    │
│  └──────────┘ └──────────┘ └──────────┘                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    External Tools                           │
│  LAMMPS │ Quantum ESPRESSO │ Python │ HPC Cluster │ Web    │
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

### Tiers

| Tier | Category | Description |
|------|----------|-------------|
| 1-2 | Basic | Single-tool tasks (LAMMPS, QE, literature search) |
| 3-4 | Advanced | Multi-step workflows, paper reproduction |
| 5-7 | HPC | Remote cluster execution, async jobs, error recovery |
| 8-10 | ML/AI | Machine learning potentials, autonomous research |
| 11 | Frontier | HPC + ML hybrid, multi-fidelity campaigns |

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
│   ├── lammps-simulation/
│   ├── quantum-espresso/
│   ├── hpc-cluster/
│   ├── literature-search/
│   ├── materials-database/
│   ├── data-analysis/
│   ├── mlip-simulation/
│   └── resource-acquisition/
├── configs/                  # Agent-specific configurations
│   ├── claude/               # Claude Code settings
│   ├── aider/                # Aider configuration
│   ├── codex/                # OpenAI Codex settings
│   └── cursor/               # Cursor rules
├── .claude/
│   ├── settings.json.example # Settings template
│   ├── skills -> ../skills   # Symlink for compatibility
│   └── hooks/                # Pre/post tool hooks
├── benchmarks/
│   ├── tasks/                # Benchmark definitions (YAML)
│   │   ├── tier1_basic/
│   │   ├── tier2_intermediate/
│   │   └── ...
│   ├── evaluation/           # Harness and graders
│   │   ├── harness.py
│   │   ├── grader.py
│   │   ├── llm_grader.py
│   │   └── backends/         # Agent backend abstraction
│   └── results/              # Benchmark results
├── docs/                     # Project documentation
├── scripts/                  # Utility scripts
└── workspaces/               # Agent work directories (gitignored)
```

## HPC Integration

The agent can execute on remote HPC clusters via SSH:

1. Configure SSH access (passwordless with key):
```bash
# ~/.ssh/config
Host cu_alpine
    HostName login.rc.colorado.edu
    User your_username
    IdentityFile ~/.ssh/id_ed25519
```

2. Set HPC configuration in `config.yaml`:
```yaml
hpc:
  enabled: true
  ssh_alias: "cu_alpine"
  scratch_dir: "/scratch/alpine/$USER"
```

3. The agent can then:
- Submit SLURM jobs
- Monitor job status
- Handle queue-aware partition selection
- Recover from HPC errors automatically

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
