# Paper Reproduction Benchmarks

The ultimate test of a scientific agent: **Can it reproduce published research?**

---

## Why Paper Reproduction?

Paper reproduction is the gold standard for evaluating scientific agents because it tests:

1. **Literature Comprehension** - Can the agent find, read, and extract key information?
2. **Methodology Understanding** - Does it understand the scientific approach?
3. **Implementation Skills** - Can it translate methods into working code?
4. **Execution Capability** - Can it actually run the simulations?
5. **Analysis Ability** - Can it process results and compare to published values?
6. **Scientific Communication** - Can it explain what it did and why?

If an agent can successfully reproduce a classic paper, it demonstrates genuine
scientific capability - not just pattern matching.

---

## Selecting Papers for Reproduction

### Ideal Characteristics

| Criterion | Why It Matters |
|-----------|----------------|
| **Well-documented parameters** | Agent can extract what it needs |
| **Freely available** | No paywall barriers |
| **Uses our tools** | LAMMPS, QE, or Python analysis |
| **Moderate compute** | Can run in hours, not weeks |
| **Clear quantitative results** | Objective validation possible |
| **Previously reproduced** | Known to be reproducible |
| **Historical significance** | Showcases meaningful science |

### Warning Signs (Avoid)

| Red Flag | Problem |
|----------|---------|
| Missing parameters | "Standard values were used" |
| Proprietary software | Can't reproduce without license |
| Custom force fields | Parameters not published |
| HPC-scale compute | 10,000 CPU-hours not feasible |
| Vague methodology | "The system was equilibrated" |

---

## Current Paper Reproduction Benchmarks

### BENCH-T4-001: Rahman 1964 - Liquid Argon

**The "Hello World" of molecular dynamics**

| Aspect | Details |
|--------|---------|
| Paper | Rahman, Phys. Rev. 136, A405 (1964) |
| System | 864 Ar atoms, LJ potential |
| Result | D = 2.43 × 10⁻⁵ cm²/s |
| Difficulty | ★★★☆☆ (entry-level paper reproduction) |
| Compute | ~10 minutes |

Why this paper:
- First MD simulation of a realistic system
- All parameters documented
- Modern reproductions get D = 2.47 × 10⁻⁵ (2% error)
- Perfect introduction to paper reproduction

### BENCH-T4-002: Jorgensen 1983 - TIP4P Water

**One of the most cited papers in science**

| Aspect | Details |
|--------|---------|
| Paper | Jorgensen et al., J. Chem. Phys. 79, 926 (1983) |
| System | TIP4P water, NPT at 25°C |
| Result | Density ≈ 0.999 g/cm³ |
| Difficulty | ★★★★☆ (4-site model, more complex) |
| Compute | ~1 hour |
| Citations | 45,000+ |

Why this paper:
- Introduced TIP3P/TIP4P models used for 40 years
- All parameters in Table I
- Tests understanding of 4-site water model
- Historically significant

---

## Cutting-Edge Benchmarks (2024-2025)

These test the agent on state-of-the-art research:

### BENCH-T4-005: MLIP Systematic Softening (2025)

| Aspect | Details |
|--------|---------|
| Paper | Deng et al., npj Comp. Mat. 11, 9 (2025) |
| Finding | MLIPs systematically underpredict energies |
| Tests | Understanding of ML limitations, validation design |
| DOI | 10.1038/s41524-024-01500-6 |

Key insight: M3GNet, CHGNet, MACE all show "softening" - they
underpredict surface energies, defect energies, and barriers
because training data is biased toward equilibrium structures.

### BENCH-T4-006: Matbench Discovery (2025)

| Aspect | Details |
|--------|---------|
| Paper | Riebesell et al., Nature Machine Intelligence (2025) |
| Task | Analyze the crystal stability prediction benchmark |
| Tests | Understanding of ML benchmarks, critical analysis |
| URL | https://matbench-discovery.materialsproject.org/ |

This is THE benchmark for evaluating ML models for materials
discovery. Agent must understand metrics, analyze leaderboard,
and provide practical recommendations.

---

## Classic Papers (Historical Significance)

| Paper | Year | System | Key Result | Difficulty |
|-------|------|--------|------------|------------|
| Rahman | 1964 | Liquid Ar diffusion | D = 2.43×10⁻⁵ cm²/s | ★★★☆☆ |
| Jorgensen | 1983 | TIP4P water | ρ = 0.999 g/cm³ | ★★★★☆ |
| Verlet | 1967 | LJ RDF | g(r) structure | ★★★☆☆ |
| Parrinello-Rahman | 1981 | Pressure coupling | Crystal structure | ★★★★☆ |

---

## Proposed Future Benchmarks

### More Recent Papers to Add

| Paper | Year | Topic | Why It's Good |
|-------|------|-------|---------------|
| CHGNet (Deng) | 2023 | Universal potential | Well-documented, reproducible |
| MACE-MP-0 | 2023 | Foundation model | Benchmark-ready |
| Short-range order in HEAs | 2025 | ML for alloys | Tests complex systems |
| Li₃PS₄ conductivity | 2024 | Solid electrolyte | Practical application |

---

## Evaluation Approach

### What We Grade

1. **Parameter Extraction (25%)**
   - Did agent find correct paper?
   - Are all parameters correctly extracted?
   - Are sources properly cited?

2. **Simulation Quality (30%)**
   - Is the setup scientifically correct?
   - Were modern best practices applied?
   - Did simulation complete successfully?

3. **Analysis Quality (25%)**
   - Was the target quantity correctly calculated?
   - Is statistical uncertainty estimated?
   - Are units correct?

4. **Scientific Communication (20%)**
   - Is the result compared to the paper?
   - Are deviations explained?
   - Is the report clear and complete?

### Acceptable Deviations

| Aspect | Acceptable | Problematic |
|--------|------------|-------------|
| Result deviation | ±20% from paper | >50% |
| Modern improvements | Smaller timestep, better thermostat | Complete methodology change |
| System size | Slightly larger for statistics | 10x larger |
| Missing parameters | Search literature | Invent values |

---

## Implementation Notes

### Agent Workflow

```
1. SEARCH: Find paper in Semantic Scholar / arXiv / publisher
           ↓
2. READ: Extract methodology section, tables, parameters
           ↓
3. PLAN: Design simulation matching paper's approach
           ↓
4. SETUP: Create input files with documented parameters
           ↓
5. RUN: Execute simulation with proper equilibration
           ↓
6. ANALYZE: Calculate target quantity from output
           ↓
7. COMPARE: Validate against published value
           ↓
8. REPORT: Document methodology, results, deviations
```

### Common Failure Modes

| Failure | Cause | Solution |
|---------|-------|----------|
| Wrong parameters | Used different source | Always cite paper directly |
| Order of magnitude off | Unit conversion error | Double-check unit systems |
| Simulation crashes | Bad timestep/cutoff | Check LAMMPS warnings |
| No linear MSD regime | Insufficient run time | Extend production run |
| Density way off | Wrong box size | Verify density calculation |

---

## Adding New Paper Reproduction Benchmarks

### Template

```yaml
id: BENCH-T4-XXX
name: Reproduce [Author] [Year] [System]
tier: 4
category: paper-reproduction

prompt: |
  Reproduce results from:
  [Full citation]

  Your objective:
  1. Find and read the paper
  2. Extract simulation parameters from [specific section/table]
  3. Set up [simulation type] matching the methodology
  4. Calculate [target quantity]
  5. Compare to published value: [value with units]

skills_required:
  - literature-search
  - [simulation-skill]
  - data-analysis

expected_outputs:
  values:
    [quantity_name]:
      expected_range: [min, max]
      unit: "[units]"

reference_solution:
  notes: |
    Published value: [value]
    Key parameters: [list]
    DOI: [doi]

metadata:
  benchmark_type: "paper-reproduction"
  paper_doi: "[doi]"
  paper_year: [year]
```

### Checklist

- [ ] Paper is freely accessible (or common enough agent can find it)
- [ ] All parameters are documented in paper
- [ ] Result has been independently reproduced
- [ ] Computation fits within time limits
- [ ] Uses tools available to the agent
- [ ] Clear quantitative target for validation

---

## Resources

### Paper Databases
- [Semantic Scholar](https://www.semanticscholar.org/)
- [arXiv](https://arxiv.org/) (preprints)
- [APS Physics](https://journals.aps.org/) (Physical Review)
- [AIP Publishing](https://pubs.aip.org/) (J. Chem. Phys.)

### Potential Databases
- [NIST Interatomic Potentials](https://www.ctcms.nist.gov/potentials/)
- [OpenKIM](https://openkim.org/)

### Classic Papers
- [Nature's 100 Most Cited Papers](https://www.nature.com/news/the-top-100-papers-1.16224)
- MD Papers: Rahman 1964, Verlet 1967, Parrinello-Rahman 1981
- Water Models: Jorgensen 1983, Berendsen 1987
- DFT: Kohn-Sham 1965, Perdew-Burke-Ernzerhof 1996
