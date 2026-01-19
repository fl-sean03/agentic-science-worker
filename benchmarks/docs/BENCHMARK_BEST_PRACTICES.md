# Benchmark Best Practices for Agentic Science Workers

Based on research of state-of-the-art LLM and agent benchmarks (AgentBench, SWE-bench,
ScienceAgentBench, ChemGraph, WebArena), this document outlines best practices tailored
for evaluating computational materials science agents.

---

## Research Summary

### Key Benchmarks Reviewed

| Benchmark | Domain | Key Innovation |
|-----------|--------|----------------|
| [AgentBench](https://github.com/THUDM/AgentBench) | General agent tasks | 8 diverse environments, multi-turn evaluation |
| [SWE-bench](https://www.swebench.com/) | Software engineering | Real GitHub issues, patch-based grading |
| [ScienceAgentBench](https://osu-nlp-group.github.io/ScienceAgentBench/) | Scientific discovery | 102 tasks from peer-reviewed papers |
| [ChemGraph](https://arxiv.org/abs/2506.06363) | Computational chemistry | 13 workflow tasks with foundation models |
| [WebArena](https://webarena.dev/) | Web automation | 812 templated tasks, functional correctness |

### Critical Insights

1. **Accuracy alone is insufficient**: The [CLEAR framework](https://arxiv.org/abs/2511.14136) showed
   agents optimized for accuracy alone are 4.4-10.8x more expensive than cost-aware alternatives

2. **Consistency matters**: Agent performance can drop from 60% (single run) to 25%
   (8-run consistency check)

3. **Multi-step tasks expose weaknesses**: Simple benchmarks don't capture planning,
   error recovery, and adaptive reasoning

4. **Domain expertise is essential**: ScienceAgentBench uses 9 subject matter experts
   to validate tasks from 44 peer-reviewed publications

---

## CLEAR Framework for Materials Science

We adopt the CLEAR framework, tailored for computational materials science:

### C - Cost

**What we measure:**
- API tokens consumed
- Compute time (CPU/GPU hours)
- Number of simulation restarts
- Total wall-clock time

**Why it matters:**
- Simulations are expensive (GPU hours, HPC allocation)
- Agents that waste compute are not production-ready
- Cost-aware agents are 4-10x more efficient

**Metrics:**
```yaml
cost_metrics:
  tokens_used: integer          # Total API tokens
  gpu_hours: float              # GPU compute time
  simulation_restarts: integer  # Number of failed runs
  api_calls: integer            # External API calls
```

### L - Latency

**What we measure:**
- Time to first useful output
- Total task completion time
- Time per simulation step
- Analysis turnaround time

**Why it matters:**
- Research has deadlines
- Iterative workflows need fast feedback
- Long latencies compound in multi-step tasks

**Metrics:**
```yaml
latency_metrics:
  time_to_first_output: seconds
  total_completion_time: seconds
  simulation_time: seconds
  analysis_time: seconds
```

### E - Efficacy

**What we measure:**
- Task completion rate
- Partial completion (milestone-based)
- Scientific correctness of results
- Output quality (plots, reports, files)

**Why it matters:**
- Can the agent actually do the science?
- Partial credit for complex workflows
- Wrong science is worse than no science

**Metrics:**
```yaml
efficacy_metrics:
  task_complete: boolean
  milestone_completion: float   # 0.0 - 1.0
  result_correct: boolean
  output_quality: float         # 0.0 - 1.0
```

### A - Assurance

**What we measure:**
- Parameter validation (are FF params from literature?)
- Simulation safety checks
- Data provenance tracking
- Reproducibility of results

**Why it matters:**
- Invented physics = wrong science
- Must cite sources for parameters
- Reproducibility is core to science

**Metrics:**
```yaml
assurance_metrics:
  parameters_validated: boolean
  sources_cited: boolean
  reproducible: boolean
  safety_checks_passed: boolean
```

### R - Reliability

**What we measure:**
- Consistency across multiple runs
- Error recovery success rate
- Graceful degradation under failures
- Variance in output quality

**Metrics:**
```yaml
reliability_metrics:
  consistency_rate: float       # Same result on N runs
  error_recovery_rate: float
  output_variance: float
```

---

## Task Design Principles

### 1. Tasks from Real Science

**Good:**
```yaml
prompt: |
  Calculate the self-diffusion coefficient of liquid argon at 94.4K
  using molecular dynamics with Lennard-Jones potential.
  Compare to the experimental value of 2.4 × 10⁻⁵ cm²/s.
```
*Based on: Verified experimental measurements, standard computational exercise*

**Bad:**
```yaml
prompt: |
  Run an MD simulation and analyze the results.
```
*Problem: Vague, no scientific context, no validation criteria*

### 2. Graded Difficulty Levels

Following ScienceAgentBench's approach:

| Level | Complexity | Example |
|-------|------------|---------|
| Tier 1 | Single skill, clear instructions | Run energy minimization |
| Tier 2 | 2-3 skills, some judgment | Find FF params + run simulation |
| Tier 3 | Full workflow, planning needed | Study diffusion (lit→sim→analysis) |
| Tier 4 | Open-ended research | Recommend materials for application |

**Calibration principle**: SOTA agents should achieve ~80% on Tier 1, ~50% on Tier 2,
<30% on Tier 3+. This ensures headroom for improvement.

### 3. Output Specification

Every task must specify:

```yaml
expected_outputs:
  files:
    - path: "result.data"
      format: "LAMMPS data file"
      validation: "contains N atoms with correct types"

    - path: "analysis/diffusion.png"
      format: "PNG image"
      validation: "MSD plot with linear fit"

  values:
    - name: "diffusion_coefficient"
      expected_range: [1.5e-5, 3.5e-5]
      unit: "cm²/s"
      tolerance: 0.5  # within 50% of experimental
```

### 4. Multi-Step Milestone Tracking

For complex tasks, define milestones:

```yaml
milestones:
  - id: M1
    description: "Literature search completed"
    validation: "Found 3+ relevant papers with parameters"
    weight: 0.15

  - id: M2
    description: "Simulation input created"
    validation: "Valid LAMMPS input file with correct parameters"
    weight: 0.25

  - id: M3
    description: "Simulation completed"
    validation: "Log file shows successful completion"
    weight: 0.30

  - id: M4
    description: "Analysis completed"
    validation: "Diffusion coefficient calculated correctly"
    weight: 0.30
```

### 5. Expert-Validated Reference Solutions

Every benchmark needs:

```yaml
reference_solution:
  location: "reference/solutions/BENCH-001/"
  files:
    - input.lmp      # Reference input file
    - log.lammps     # Expected output
    - analysis.py    # Reference analysis script

  expected_result:
    value: 2.43e-5
    unit: "cm²/s"
    source: "Rahman, A. Phys. Rev. 136, A405 (1964)"

  validation_notes: |
    Verified by domain expert (Dr. X, 2025-01-15).
    Result matches experimental value within 5%.
```

---

## Evaluation Methods

### 1. Programmatic Validation

For quantitative results:

```python
def validate_diffusion_result(agent_output, reference):
    """Validate diffusion coefficient calculation."""

    # Extract agent's reported value
    D_agent = extract_diffusion_value(agent_output)
    D_reference = reference['expected_value']
    tolerance = reference['tolerance']

    # Check if within acceptable range
    relative_error = abs(D_agent - D_reference) / D_reference

    return {
        'passed': relative_error <= tolerance,
        'agent_value': D_agent,
        'reference_value': D_reference,
        'relative_error': relative_error,
        'tolerance': tolerance
    }
```

### 2. LLM-as-Judge for Qualitative Assessment

For reports, reasoning, and decisions:

```python
JUDGE_PROMPT = """
You are evaluating an AI agent's scientific work.

Task: {task_description}
Agent's Output: {agent_output}

Evaluate on this rubric:
1. Scientific Accuracy (0-25): Are parameters, methods, and conclusions correct?
2. Completeness (0-25): Did the agent address all requirements?
3. Reasoning Quality (0-25): Is the scientific reasoning sound?
4. Communication (0-25): Is the output clear and well-documented?

Provide scores and brief justification for each category.
Format: JSON with keys accuracy, completeness, reasoning, communication, justification
"""
```

### 3. Functional Correctness (WebArena-style)

Check if the final state is correct, regardless of path:

```python
def validate_functional_correctness(workspace, expected_state):
    """Check if workspace matches expected final state."""

    checks = {}

    # Check files exist
    for expected_file in expected_state['files']:
        path = workspace / expected_file['path']
        checks[f"file:{expected_file['path']}"] = {
            'passed': path.exists(),
            'details': f"File {'exists' if path.exists() else 'missing'}"
        }

    # Check simulation completed
    log_file = workspace / "log.lammps"
    if log_file.exists():
        content = log_file.read_text()
        checks['simulation_completed'] = {
            'passed': "Loop time" in content,
            'details': "Simulation ran to completion"
        }

    return checks
```

### 4. Consistency Testing (Multi-Run)

Run each benchmark 3-5 times to measure reliability:

```python
def evaluate_consistency(benchmark_id, n_runs=3):
    """Run benchmark multiple times, measure consistency."""

    results = []
    for i in range(n_runs):
        result = run_benchmark(benchmark_id, seed=i)
        results.append(result)

    # Calculate consistency metrics
    success_rate = sum(r['passed'] for r in results) / n_runs

    if all(r.get('numeric_result') for r in results):
        values = [r['numeric_result'] for r in results]
        variance = np.var(values)
        cv = np.std(values) / np.mean(values)  # Coefficient of variation

    return {
        'success_rate': success_rate,
        'variance': variance,
        'coefficient_of_variation': cv,
        'all_runs': results
    }
```

---

## Common Pitfalls to Avoid

### 1. Insufficient Test Cases (SWE-bench Issue)

**Problem**: Using too few validation criteria allows false positives.

**Solution**: Multiple validation checks per task:
```yaml
validation:
  file_checks:
    - file exists
    - file format correct
    - file parseable
  content_checks:
    - correct number of atoms
    - parameters match specification
  result_checks:
    - value in expected range
    - units correct
```

### 2. Empty Response Counting as Success (τ-bench Issue)

**Problem**: Agent returns nothing, gets partial credit.

**Solution**: Explicit failure for empty/incomplete outputs:
```python
if not agent_output or len(agent_output.strip()) < 50:
    return {'passed': False, 'reason': 'Empty or trivial output'}
```

### 3. Overfitting to Benchmark

**Problem**: Agents learn benchmark patterns, not real skills.

**Solution**:
- Keep some tasks hidden
- Rotate task variants
- Use different parameter values than training examples

### 4. Ignoring Cost/Latency

**Problem**: Agent succeeds but uses 10x normal resources.

**Solution**: CLEAR metrics with cost thresholds:
```yaml
cost_limits:
  max_tokens: 50000
  max_simulation_time: 3600  # seconds
  max_api_calls: 20

scoring:
  within_limits: +10 bonus
  exceeds_2x: -20 penalty
  exceeds_5x: automatic_fail
```

---

## Materials Science-Specific Considerations

### 1. Parameter Provenance

Unlike general coding tasks, wrong parameters = wrong physics.

**Validation requirement:**
```yaml
parameter_validation:
  force_field:
    must_cite: true
    acceptable_sources:
      - peer-reviewed paper
      - established database (NIST, Materials Project)
      - textbook with ISBN
    unacceptable:
      - "typical values"
      - "reasonable estimate"
      - invented parameters
```

### 2. Simulation Sanity Checks

```yaml
simulation_sanity:
  energy_conservation:
    nve_drift: < 1e-4 eV/atom/ps
  temperature_stability:
    nvt_fluctuation: < 10% of target
  structure_integrity:
    no_atom_overlap: true
    no_bond_breaking: true (unless intended)
```

### 3. Unit Consistency

Different codes use different unit systems:
```yaml
unit_awareness:
  lammps_real:
    energy: kcal/mol
    distance: Angstrom
    time: femtosecond
  lammps_metal:
    energy: eV
    distance: Angstrom
    time: picosecond
  quantum_espresso:
    energy: Rydberg
    distance: Bohr

  validation: "Agent must report results in requested units"
```

### 4. Convergence Verification

```yaml
convergence_checks:
  scf_calculation:
    energy_converged: true
    forces_converged: true (if relaxation)
  md_equilibration:
    temperature_stable: true
    energy_drift_acceptable: true
```

---

## Benchmark Categories for Materials Science

Based on ChemGraph's 13 tasks and ScienceAgentBench's approach:

### Category 1: Structure & Setup
- Crystal structure retrieval
- Structure file conversion
- Force field parameter lookup
- Input file generation

### Category 2: Simulation Execution
- Energy minimization
- MD equilibration
- Property calculation runs
- DFT self-consistent field

### Category 3: Analysis & Processing
- Trajectory analysis
- Property extraction
- Statistical analysis
- Visualization/plotting

### Category 4: Literature & Knowledge
- Parameter search in papers
- Method comparison
- Result validation against literature

### Category 5: Integrated Workflows
- Structure → Simulation → Analysis
- Literature → Setup → Run → Report
- Multi-method comparison studies

---

## Implementation Roadmap

### Phase 1: Core Infrastructure
- Benchmark runner that sends prompts to Claude Code
- Basic grading framework (file checks, value validation)
- CLEAR metrics collection

### Phase 2: Tier 1-2 Benchmarks
- 10-15 single-skill tasks
- 10-15 multi-skill tasks
- Reference solutions and rubrics

### Phase 3: Advanced Evaluation
- LLM-as-Judge integration
- Consistency testing
- Cost/latency tracking

### Phase 4: Tier 3-4 Benchmarks
- Full research workflow tasks
- Open-ended evaluation with expert review
- Comparative analysis tools

---

## References

1. AgentBench: https://github.com/THUDM/AgentBench
2. SWE-bench: https://www.swebench.com/
3. ScienceAgentBench: https://osu-nlp-group.github.io/ScienceAgentBench/
4. ChemGraph: https://arxiv.org/abs/2506.06363
5. CLEAR Framework: https://arxiv.org/abs/2511.14136
6. WebArena: https://webarena.dev/
7. Agentic Benchmark Checklist: https://arxiv.org/pdf/2507.02825
