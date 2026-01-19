# Benchmark Authoring Guide

Practical guide for creating new benchmarks for the Agentic Science Worker.

---

## Quick Start: Benchmark Template

Copy this template and fill in the sections:

```yaml
# Tier [1-4] Benchmark: [Short Name]
# [Category description]

id: BENCH-T[TIER]-[NUMBER]-[slug]
name: [Descriptive Name]
tier: [1|2|3|4]
category: [lammps-simulation|quantum-espresso|literature-search|materials-database|data-analysis|workflow]

description: |
  [2-3 sentences describing what this benchmark tests]

prompt: |
  [The exact prompt the agent will receive]

  [Requirements, specifications, deliverables]

  Work in: workspaces/benchmarks/[task-slug]/

skills_required:
  - [skill-1]
  - [skill-2]

time_limit_minutes: [integer]

milestones:  # For Tier 2+
  - id: M1
    description: "[What milestone represents]"
    weight: [0.0-1.0, sum to 1.0]
    validation: |
      [How to check if milestone achieved]

expected_outputs:
  files:
    - [path/to/expected/file1]
    - [path/to/expected/file2]
  values:
    [value_name]:
      description: "[What this value represents]"
      expected_range: [min, max]  # OR expected: exact_value
      unit: "[unit string]"

grading:
  total_points: 100
  categories:
    [category_name]:
      weight: [integer, sum to 100]
      checks:
        - name: "[Check name]"
          points: [integer]
          validation: |
            [Validation logic description]

clear_metrics:
  cost:
    max_tokens: [integer]
    max_simulation_time: [seconds]
    max_api_calls: [integer]
  latency:
    target_completion: [seconds]
  assurance:
    parameters_must_be_cited: [true|false]

reference_solution:
  location: reference/solutions/[task-slug]/
  notes: |
    [Known correct values and sources]

metadata:
  author: "[your name]"
  created: "[YYYY-MM-DD]"
  difficulty: "[easy|medium|hard|expert]"
  estimated_tokens: [integer]
  scientific_domain: "[domain]"
  tags:
    - [tag1]
    - [tag2]
```

---

## Tier Guidelines

### Tier 1: Basic (Single Skill)

**Purpose**: Test one skill in isolation with clear instructions.

**Characteristics**:
- One skill only
- Explicit instructions (what to do, not just what to achieve)
- Clear success criteria
- 5-15 minutes to complete
- ~2000-5000 tokens

**Example prompts**:
- "Run energy minimization on this structure with these parameters"
- "Search for papers on [topic] and list 5 relevant ones"
- "Parse this log file and plot temperature vs time"

**DO**:
- Specify exact parameters
- Provide input files if needed
- Have single, measurable outcome

**DON'T**:
- Require judgment calls
- Need multiple skills
- Have ambiguous success criteria

---

### Tier 2: Intermediate (Multi-Skill)

**Purpose**: Test 2-3 skills working together with some judgment required.

**Characteristics**:
- 2-3 skills combined
- Some decisions left to agent
- Defined milestones
- 15-45 minutes to complete
- ~5000-15000 tokens

**Example prompts**:
- "Find LJ parameters for argon and calculate diffusion coefficient"
- "Get structure from Materials Project and run DFT calculation"
- "Search literature for force field, then run simulation"

**DO**:
- Define clear milestones
- Have reference values for comparison
- Allow some methodology choices

**DON'T**:
- Be completely open-ended
- Require expert-level decisions
- Need extensive planning

---

### Tier 3: Advanced (Research Workflow)

**Purpose**: Test complete research workflows requiring planning and iteration.

**Characteristics**:
- Multiple skills, sequential and parallel
- Significant planning required
- Partial credit via milestones
- 45-120 minutes to complete
- ~15000-40000 tokens

**Example prompts**:
- "Study diffusion in material X from literature to final analysis"
- "Compare computational methods for property Y"
- "Optimize simulation parameters for convergence"

**DO**:
- Define clear milestones (5-8 checkpoints)
- Have expert-validated reference solutions
- Allow multiple valid approaches

**DON'T**:
- Be so open that any answer is valid
- Require novel research
- Need external validation

---

### Tier 4: Research (Open-Ended)

**Purpose**: Test ability to conduct genuine research tasks.

**Characteristics**:
- Open-ended questions
- Multiple valid answers
- Expert evaluation required
- 2+ hours possible
- Token limits less meaningful

**Example prompts**:
- "Recommend materials for hydrogen storage application"
- "Investigate why simulation gives unexpected results"
- "Design study to determine X"

**DO**:
- Have expert reviewers assigned
- Define evaluation rubric for reasoning
- Accept multiple valid conclusions

**DON'T**:
- Expect single correct answer
- Use purely automated grading
- Skip human validation

---

## Writing Good Prompts

### Be Specific About Deliverables

**Bad**:
```
Run a simulation and analyze it.
```

**Good**:
```
Run an NVT MD simulation of 256 argon atoms at 94.4K.
Save the trajectory and calculate the mean square displacement.
Report the diffusion coefficient in cm²/s.

Deliverables:
- LAMMPS input file: input.lmp
- MSD plot: analysis/msd.png
- Report: report.md with methodology and results
```

### Specify Parameters or Say Where to Find Them

**Bad**:
```
Use appropriate force field parameters.
```

**Good**:
```
Use Lennard-Jones parameters for argon:
ε = 0.238 kcal/mol, σ = 3.405 Å

OR

Search the literature to find TIP4P water model parameters.
Cite the original paper (Jorgensen et al.).
```

### Include Reference Values

**Bad**:
```
Calculate the diffusion coefficient.
```

**Good**:
```
Calculate the diffusion coefficient.
Compare your result to the experimental value of 2.4 × 10⁻⁵ cm²/s
(Rahman, Phys. Rev. 136, A405, 1964).
```

---

## Designing Grading Rubrics

### Weight by Importance

```yaml
grading:
  categories:
    # What matters most gets highest weight
    result_quality:
      weight: 40  # The answer matters
    simulation_quality:
      weight: 30  # How you got there matters
    setup_correctness:
      weight: 20  # Basics need to be right
    documentation:
      weight: 10  # Nice to have
```

### Make Checks Unambiguous

**Bad**:
```yaml
- name: "Good simulation"
  validation: |
    Simulation ran well
```

**Good**:
```yaml
- name: "Simulation completed"
  validation: |
    log.lammps contains "Loop time"
    AND no "ERROR" in output
    AND final timestep >= 10000
```

### Include Partial Credit

```yaml
checks:
  - name: "Correct LJ epsilon"
    points: 5
    validation: |
      ε within 5% of 0.238 kcal/mol
  - name: "Correct LJ sigma"
    points: 5
    validation: |
      σ within 1% of 3.405 Å
  - name: "Source cited"
    points: 3
    validation: |
      Reference provided for parameters
```

---

## Reference Solutions

Every benchmark should have a reference solution:

```
reference/solutions/[benchmark-slug]/
├── input.lmp           # Reference input file
├── expected_output/    # What correct output looks like
│   ├── log.lammps
│   └── analysis.png
├── analysis.py         # How to analyze results
├── README.md           # Notes on solution
└── validation.py       # Automated validation script
```

### Reference Solution README

```markdown
# Reference Solution: BENCH-T2-001

## Expected Results
- Diffusion coefficient: 2.43 × 10⁻⁵ cm²/s (±20%)

## Known Sources
- Experimental: Rahman, Phys. Rev. 136, A405 (1964)
- LJ parameters: Allen & Tildesley textbook

## Validation Notes
- Result validated against Rahman's original simulation
- Verified by [expert name] on [date]

## Common Failure Modes
1. Wrong units (m²/s vs cm²/s)
2. Using 2D MSD formula instead of 3D
3. Including equilibration in diffusion calculation
```

---

## Testing Your Benchmark

### Manual Testing

1. Run the benchmark yourself
2. Time how long it takes
3. Verify the grading works
4. Check edge cases

### Automated Testing

```python
def test_benchmark_loads():
    """Benchmark YAML is valid."""
    bench = load_benchmark("BENCH-T2-001")
    assert bench['id'] == "BENCH-T2-001"
    assert bench['tier'] == 2

def test_grading_sums_to_100():
    """Weights should sum to 100."""
    bench = load_benchmark("BENCH-T2-001")
    total = sum(c['weight'] for c in bench['grading']['categories'].values())
    assert total == 100

def test_milestones_sum_to_1():
    """Milestone weights should sum to 1.0."""
    bench = load_benchmark("BENCH-T2-001")
    total = sum(m['weight'] for m in bench['milestones'])
    assert abs(total - 1.0) < 0.01
```

---

## Common Mistakes to Avoid

### 1. Vague Success Criteria
**Problem**: "Produce a good analysis"
**Solution**: "Report diffusion coefficient within 50% of experimental"

### 2. Missing Units
**Problem**: expected_range: [1, 100]
**Solution**: expected_range: [1, 100] with unit: "kcal/mol"

### 3. Impossible Time Limits
**Problem**: 5 minutes for DFT calculation
**Solution**: Test the benchmark yourself first

### 4. No Reference Solution
**Problem**: How do you know the answer is right?
**Solution**: Create and validate reference solution

### 5. Over-Specified (Tier 3/4)
**Problem**: Specifying every single step
**Solution**: Give objectives, let agent plan

### 6. Under-Specified (Tier 1/2)
**Problem**: "Do a simulation"
**Solution**: Give clear parameters and deliverables

---

## Benchmark Naming Convention

```
BENCH-T[TIER]-[NUMBER]-[short-description]

Examples:
BENCH-T1-001-lj-minimization
BENCH-T2-003-water-tip4p
BENCH-T3-001-hydrogen-in-palladium
```

---

## Checklist Before Submitting

- [ ] YAML is valid and loads correctly
- [ ] Grading weights sum to 100
- [ ] Milestone weights sum to 1.0 (if applicable)
- [ ] Time limit is realistic
- [ ] Reference solution exists
- [ ] Expected values have units
- [ ] At least one validation check per category
- [ ] Prompt specifies deliverables
- [ ] Working directory specified
- [ ] Skills required listed correctly
- [ ] Manually tested the benchmark
