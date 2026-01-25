# Contributing to Agentic Science Worker

Welcome! This document contains everything you need to know to contribute effectively.

## Table of Contents
- [Project Philosophy](#project-philosophy)
- [Development Setup](#development-setup)
- [Architecture Overview](#architecture-overview)
- [Developer Tips & Tricks](#developer-tips--tricks)
- [Common Pitfalls](#common-pitfalls)
- [Benchmark Development](#benchmark-development)
- [Testing Your Changes](#testing-your-changes)

---

## Project Philosophy

### Core Thesis

> **The best agentic system is the simplest one that works.**

We don't build complex orchestration. We give Claude:
1. Clear context (CLAUDE.md, skills)
2. Direct tool access (can run simulations, not just plan them)
3. Fast feedback (know when something fails)
4. Domain knowledge (what parameters to use, what's reasonable)

### What Makes This Different

Traditional approaches try to constrain and orchestrate AI agents. We take the opposite approach:

- **Trust the model** - Claude already knows computational science; we just give it tools
- **Minimal scaffolding** - Skills are just markdown files, not complex code
- **Fail fast, iterate** - Benchmarks reveal what's missing; we fix prompts, not code
- **Research-grade output** - The agent should produce work a PhD would accept

---

## Development Setup

### Prerequisites

```bash
# Required
- Claude Code CLI (subscription)
- Python 3.10+
- LAMMPS (GPU recommended)

# Optional
- Quantum ESPRESSO (for DFT benchmarks)
- HPC cluster access (for T5-T7 benchmarks)
- ML packages: mace-torch, matgl, chgnet (for T8+ benchmarks)
```

### Quick Start

```bash
git clone https://github.com/fl-sean03/agentic-science-worker.git
cd agentic-science-worker

# Configure
cp config.example.yaml config.yaml
cp .claude/settings.json.example .claude/settings.json
cp .mcp.json.example .mcp.json

# Edit configs with your paths/keys
vim config.yaml

# Verify
python benchmarks/evaluation/harness.py --verify

# Run a benchmark
python benchmarks/evaluation/harness.py BENCH-T1-001
```

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      CLAUDE.md                              │
│         (Researcher persona, methodology, mindset)          │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   .claude/skills/                           │
│  Each skill = SKILL.md file with:                          │
│  - When to use it                                          │
│  - Tool locations and commands                             │
│  - Domain-specific knowledge                               │
│  - Examples and patterns                                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│               benchmarks/evaluation/                        │
│  harness.py  - Spawns headless agents, captures output     │
│  grader.py   - Rule-based grading                          │
│  llm_grader.py - Claude-as-judge grading                   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                benchmarks/tasks/                            │
│  YAML files defining each benchmark:                       │
│  - prompt (what to do)                                     │
│  - expected_outputs (what files to create)                 │
│  - grading (evaluation criteria)                           │
└─────────────────────────────────────────────────────────────┘
```

### Key Files

| File | Purpose | When to Edit |
|------|---------|--------------|
| `CLAUDE.md` | Agent persona and methodology | Changing core behavior |
| `.claude/skills/*.md` | Domain-specific knowledge | Adding capabilities |
| `.claude/settings.json` | Permissions, env vars | New tools/paths |
| `benchmarks/tasks/*.yaml` | Test definitions | New benchmarks |
| `benchmarks/evaluation/harness.py` | Test runner | Changing execution |

---

## Developer Tips & Tricks

### Insight #1: Prompt Engineering > Code

Most "bugs" are actually unclear prompts. Before writing code, try:
1. Adding explicit instructions to the benchmark prompt
2. Adding examples to the skill file
3. Adding checklists the agent must complete

**Example fix that worked:**
```yaml
# Before (agent stopped after research):
prompt: |
  Calculate the melting temperature of copper.

# After (agent completed full workflow):
prompt: |
  **CRITICAL INSTRUCTIONS:**
  1. You are EXECUTING this task, not just planning it
  2. You must CREATE all output files listed below
  3. Use TodoWrite to track your checklist

  Calculate the melting temperature of copper.

  **Required outputs:**
  - [ ] simulation files created
  - [ ] simulation executed
  - [ ] results analyzed
  - [ ] report.md written
```

### Insight #2: The Agent is Smart, Just Misinterprets Scope

When benchmarks fail, it's usually because the agent:
- Thought "research and recommend" was the task (vs. "execute end-to-end")
- Optimized for efficiency (ran locally instead of HPC)
- Stopped at a reasonable checkpoint (after setup, before execution)

**Fix pattern:** Be explicit about what "done" means.

### Insight #3: LLM-as-Judge Grading is Powerful

The `llm_grader.py` spawns another Claude agent to evaluate results. This catches:
- Scientific errors a regex can't find
- Missing citations and methodology
- Physically unreasonable results

**Tip:** Grading prompts are in `llm_grader.py` around line 78. Customize for new domains.

### Insight #4: Skills are Just Context Injection

A skill file (`.claude/skills/*/SKILL.md`) is just markdown that gets injected when the agent invokes that skill. No code required.

**To add a new capability:**
1. Create `.claude/skills/new-skill/SKILL.md`
2. Write what the agent needs to know
3. Include examples and common patterns
4. That's it - the skill is now available

### Insight #5: Environment Variables for Portability

All paths should use environment variables:
```bash
# In .claude/settings.json
"env": {
  "LMP": "${LAMMPS_PATH:-/usr/local/bin/lmp}",
  "QE_CPU": "${QE_PATH:-/usr/local/qe/bin}"
}
```

The agent then uses `$LMP` in commands, making the system portable.

---

## Common Pitfalls

### Pitfall #1: Hardcoding Paths

**Wrong:**
```markdown
Run LAMMPS at `/home/myuser/lammps/bin/lmp`
```

**Right:**
```markdown
Run LAMMPS using `$LMP` (configured in settings.json)
```

### Pitfall #2: Vague Success Criteria

**Wrong:**
```yaml
prompt: |
  Analyze the simulation results.
```

**Right:**
```yaml
prompt: |
  Analyze the simulation results. Create:
  1. analysis.py - script that calculates diffusion coefficient
  2. results.txt - D value with units and uncertainty
  3. comparison.md - compare to literature value with citation
```

### Pitfall #3: Not Testing on Real Infrastructure

HPC benchmarks (T5-T7) require actual cluster access. The agent will find creative workarounds (run locally) if HPC isn't available. This isn't wrong - it's smart - but it bypasses what you're testing.

**Fix:** Add explicit requirements:
```yaml
prompt: |
  **CRITICAL: HPC EXECUTION REQUIRED**
  You MUST execute on the HPC cluster, NOT locally.
```

### Pitfall #4: Expecting Deterministic Output

The agent may:
- Use different file names
- Choose alternative methods
- Produce results in different formats

**Fix:** Grade on outcomes, not exact outputs:
```yaml
grading:
  - name: scientific_accuracy
    criteria:
      - Result within 10% of literature value
      - Method is physically appropriate
      - Sources are cited
```

---

## Benchmark Development

### Creating a New Benchmark

1. **Choose the right tier:**
   - T1-T2: Single tool, basic tasks
   - T3-T4: Multi-step, research reproduction
   - T5-T7: HPC execution
   - T8-T10: ML potentials, autonomous research
   - T11: Frontier challenges

2. **Write the YAML:**
```yaml
id: BENCH-T1-NEW
name: My New Benchmark
tier: 1
category: basic

description: |
  What this benchmark tests.

prompt: |
  **CRITICAL INSTRUCTIONS:**
  [Be explicit about what the agent must do]

  Your task:
  [The actual task]

  Required outputs:
  - [ ] file1.txt
  - [ ] file2.py

time_limit_minutes: 15

expected_outputs:
  files:
    - name: "file1.txt"
      description: "What this file should contain"

grading:
  categories:
    - name: execution
      weight: 50
      criteria:
        - Task was completed
        - Files were created
    - name: quality
      weight: 50
      criteria:
        - Results are correct
        - Sources are cited
```

3. **Run and iterate:**
```bash
python benchmarks/evaluation/harness.py BENCH-T1-NEW --verbose
```

### Benchmark Design Principles

1. **Test one thing well** - Don't combine HPC + ML + literature in one benchmark
2. **Have a ground truth** - Know what the correct answer is
3. **Allow multiple valid approaches** - Grade outcomes, not methods
4. **Include verification** - "Compare to literature" catches errors

---

## Testing Your Changes

### Running Single Benchmarks

```bash
# Basic run
python benchmarks/evaluation/harness.py BENCH-T1-001

# Verbose output
python benchmarks/evaluation/harness.py BENCH-T1-001 --verbose

# Run a whole tier
python benchmarks/evaluation/harness.py --tier 1
```

### Verifying Infrastructure

```bash
python benchmarks/evaluation/harness.py --verify
```

### Checking Results

Results are saved to `benchmarks/results/runs/BENCH-XXX-TIMESTAMP/`:
- `result.json` - Scores and grading
- `agent_output.txt` - Full agent transcript
- `benchmark.json` - Original benchmark definition

### Before Submitting a PR

1. Run affected benchmarks
2. Update `ROADMAP.md` if you completed a roadmap item
3. Ensure no hardcoded paths leaked in

---

## Questions?

- Check `docs/` for detailed guides
- See `ROADMAP.md` for what we're building toward

Welcome to the project!
