# ML/AI for Materials Science Benchmarks

> **STATUS: IMPLEMENTED**
>
> All 15 ML/AI benchmarks have been implemented:
> - Tier 8: 7 benchmarks in `tasks/tier8_ml_materials/`
> - Tier 9: 5 benchmarks in `tasks/tier9_autonomous_research/`
> - Tier 10: 3 benchmarks in `tasks/tier10_frontier/`
>
> ML packages installed: mace-torch, matgl, chgnet, phonopy
> GPU verified: RTX 5080 (17.1 GB) with CUDA support
>
> The benchmark harness supports tiers 8-10 with:
> - New pass thresholds (60%, 50%, 40%)
> - ML infrastructure verification
> - `--include-ml` flag for running ML benchmarks

## Vision: Testing Autonomous AI-Assisted Research

This proposal outlines benchmarks that test the agent's ability to leverage modern ML tools for materials science - specifically Machine Learning Interatomic Potentials (MLIPs) and autonomous research workflows.

These benchmarks push toward the frontier of **AI-assisted scientific discovery**.

---

## What's Now Possible (That Wasn't 2 Years Ago)

| Capability | Traditional MD | With Universal MLIPs |
|------------|---------------|---------------------|
| Accuracy | Empirical potentials | Near-DFT accuracy |
| Element coverage | Limited to fitted systems | 89 elements |
| Property prediction | Basic thermodynamics | Formation energy, stability |
| Simulation cost | Fast but inaccurate | DFT accuracy at MD cost |
| Training requirement | N/A | Pre-trained, ready to use |

**Key Tools Available:**
- **MACE-MP-0**: 4.7M parameters, trained on Materials Project
- **CHGNet**: Charge-aware, great for batteries
- **M3GNet**: Fast, good generalization
- **SevenNet**: Best for phonons
- **MatGL**: Python library for all of the above

---

## Proposed Benchmark Structure

### Tier 8: ML-Powered Materials Science (7 benchmarks)
Test: Can the agent use modern ML tools for materials science?

### Tier 9: Autonomous Research Workflows (5 benchmarks)
Test: Can the agent conduct autonomous, closed-loop research?

### Tier 10: Frontier Challenges (3 benchmarks)
Test: Can the agent tackle open research problems?

---

## Tier 8: ML-Powered Materials Science

### BENCH-T8-001: Universal Potential Setup
**Goal**: Install and validate MACE/CHGNet/M3GNet

**Prompt**:
"Set up the MatGL and MACE Python packages on this workstation. Validate the installation by:
1. Loading the pre-trained MACE-MP-0 model
2. Loading the pre-trained CHGNet model
3. Creating a simple Si diamond structure
4. Running a single-point energy calculation with each model
5. Comparing energies to verify models are working

Report versions installed and any issues encountered."

**Skills Tested**:
- Python environment management
- MLIP framework installation
- Model loading and basic inference

**Time Limit**: 30 min
**Difficulty**: Easy

---

### BENCH-T8-002: MLIP vs Classical Comparison
**Goal**: Compare MLIP accuracy against classical potentials

**Prompt**:
"Compare universal MLIPs against classical potentials for copper:
1. Calculate lattice constant using:
   - EAM potential (classical)
   - MACE-MP-0 (universal MLIP)
   - CHGNet (universal MLIP)
2. Calculate elastic constants (C11, C12, C44) with each method
3. Compare all results to experimental values
4. Create a comparison table and discuss accuracy differences

Use ASE for calculations. Document which model is most accurate and why."

**Skills Tested**:
- Multi-model comparison
- Elastic constant calculation
- Critical evaluation of ML models
- Scientific writing

**Time Limit**: 45 min
**Difficulty**: Medium

---

### BENCH-T8-003: Phonon Calculation with MLIPs
**Goal**: Calculate phonon dispersion using universal potentials

**Prompt**:
"Calculate the phonon dispersion of silicon using MACE-MP-0:
1. Create Si diamond supercell (3×3×3 conventional)
2. Use finite displacement method (phonopy integration or manual)
3. Calculate force constants
4. Compute phonon dispersion along Γ-X-K-Γ-L path
5. Compare to experimental phonon spectrum

**Important**: Universal MLIPs have a known ~15% frequency softening. Quantify this systematic error in your results."

**Skills Tested**:
- Phonon methodology with MLIPs
- Understanding of MLIP limitations
- Quantitative error analysis

**Time Limit**: 60 min
**Difficulty**: Medium-Hard

---

### BENCH-T8-004: High-Throughput Stability Screening
**Goal**: Screen materials for thermodynamic stability

**Prompt**:
"Use universal MLIPs to screen candidate materials for stability:

Target: Find stable ternary oxides in the Li-Mn-O system

1. Generate candidate structures:
   - LiMnO2 (various polymorphs)
   - Li2MnO3
   - LiMn2O4 (spinel)
   - Other reasonable compositions

2. For each candidate:
   - Relax structure with MACE-MP-0 or CHGNet
   - Calculate formation energy
   - Assess stability vs decomposition

3. Rank candidates by stability
4. Compare your ranking to Materials Project data
5. Identify any disagreements and discuss possible causes

This is a realistic battery materials screening workflow."

**Skills Tested**:
- Structure generation
- Formation energy calculation
- Phase stability analysis
- Validation against database

**Time Limit**: 90 min
**Difficulty**: Hard

---

### BENCH-T8-005: MLIP-Accelerated MD
**Goal**: Run long MD simulations enabled by MLIP speed

**Prompt**:
"Calculate the self-diffusion coefficient of Li+ in Li3PS4 solid electrolyte:

1. Get Li3PS4 structure from Materials Project
2. Create supercell (at least 200 atoms)
3. Run NVT MD at 600K using CHGNet (charge-aware, good for Li)
4. Simulate for at least 100 ps (would take weeks with DFT)
5. Calculate Li+ MSD and extract diffusion coefficient
6. Compare to experimental/literature values

This problem is ONLY feasible with MLIPs - DFT-MD would be too expensive."

**Skills Tested**:
- Solid electrolyte simulation
- Long-timescale MD with MLIPs
- Diffusion analysis
- Understanding of when MLIPs enable new science

**Time Limit**: 120 min
**Difficulty**: Hard

---

### BENCH-T8-006: Fine-Tuning Universal Potential
**Goal**: Improve MLIP accuracy for specific chemistry via fine-tuning

**Prompt**:
"Fine-tune MACE-MP-0 for improved accuracy on gold surfaces:

Background: Universal MLIPs have larger errors for surfaces. Fine-tuning on a small dataset can dramatically improve accuracy.

1. Generate training data:
   - Create Au(111), Au(100), Au(110) surface slabs
   - Run DFT single-point calculations (5-10 configurations each)
   - Include some with adatoms/vacancies

2. Fine-tune MACE-MP-0:
   - Use MACE fine-tuning workflow
   - Small learning rate, few epochs
   - Monitor validation loss

3. Evaluate improvement:
   - Compare surface energies before/after fine-tuning
   - Test on held-out configurations

4. Document: Training data size, fine-tuning parameters, accuracy improvement

This demonstrates transfer learning for domain adaptation."

**Skills Tested**:
- DFT data generation
- MLIP fine-tuning workflow
- Transfer learning concepts
- Validation methodology

**Time Limit**: 180 min (DFT calculations take time)
**Difficulty**: Expert

---

### BENCH-T8-007: Matbench Discovery Evaluation
**Goal**: Reproduce a Matbench Discovery evaluation

**Prompt**:
"Participate in the Matbench Discovery benchmark:

1. Download the Matbench Discovery test set
2. For each structure:
   - Relax with your chosen MLIP
   - Predict formation energy
   - Classify as stable/unstable

3. Calculate metrics:
   - F1 score for stability prediction
   - MAE for formation energy
   - Discovery Acceleration Factor (DAF)

4. Compare your results to the leaderboard
5. Discuss where your model succeeds and fails

This is a real ML benchmark used by the community."

**Skills Tested**:
- Standard ML benchmark methodology
- Metric calculation
- Community tool usage
- Critical analysis of model performance

**Time Limit**: 120 min
**Difficulty**: Hard

---

## Tier 9: Autonomous Research Workflows

### BENCH-T9-001: Active Learning for MLIP Training
**Goal**: Use active learning to efficiently train an MLIP

**Prompt**:
"Train an MLIP for a new chemistry using active learning:

Target System: Ag-Cu alloys (not well-represented in universal potentials)

Workflow:
1. Start with universal MLIP (MACE-MP-0)
2. Run MD to explore configuration space
3. Identify high-uncertainty configurations
4. Run DFT on selected configurations (limit: 50 DFT calculations)
5. Fine-tune MLIP on new data
6. Iterate until convergence

Success Metric: Achieve <50 meV/atom error on mixing enthalpy using only 50 DFT calculations.

This demonstrates intelligent data acquisition vs. random sampling."

**Skills Tested**:
- Active learning workflow
- Uncertainty quantification
- Efficient DFT usage
- Iterative model improvement

**Time Limit**: 240 min
**Difficulty**: Expert

---

### BENCH-T9-002: Multi-Fidelity Workflow
**Goal**: Combine cheap and expensive calculations intelligently

**Prompt**:
"Design a multi-fidelity workflow for band gap prediction:

Problem: You need accurate band gaps, but hybrid DFT (HSE) is 100x more expensive than PBE.

Workflow:
1. Screen 20 candidate semiconductors
2. Run PBE (cheap) on all 20
3. Use PBE results to select top 5 candidates
4. Run HSE (expensive) only on top 5
5. Train a correction model: HSE ≈ f(PBE)
6. Apply correction to remaining candidates
7. Validate on 2-3 additional HSE calculations

Compare cost vs. running HSE on everything.
Quantify accuracy loss from multi-fidelity approach."

**Skills Tested**:
- Multi-fidelity strategy
- Cost-aware computation
- Transfer learning for properties
- Quantitative cost-benefit analysis

**Time Limit**: 300 min
**Difficulty**: Expert

---

### BENCH-T9-003: Closed-Loop Optimization
**Goal**: Optimize a property through iterative simulation

**Prompt**:
"Optimize the thermal conductivity of a silicon-germanium alloy:

Goal: Find the Si(x)Ge(1-x) composition with LOWEST thermal conductivity (for thermoelectrics).

Closed-Loop Workflow:
1. Start: Calculate κ for pure Si and pure Ge
2. Propose: Suggest next composition to test
3. Calculate: Run MD with MLIP, compute thermal conductivity
4. Analyze: Update your model of κ(x)
5. Iterate: Propose next composition based on what you've learned

Constraints:
- Maximum 10 compositions tested
- Each MD run: 10,000 atoms, 100 ps

Find the minimum κ composition within 10 iterations.
Compare to literature (minimum near x ≈ 0.5)."

**Skills Tested**:
- Bayesian-style optimization
- Thermal conductivity calculation
- Iterative decision making
- Efficient exploration vs exploitation

**Time Limit**: 180 min
**Difficulty**: Expert

---

### BENCH-T9-004: Autonomous Literature-to-Simulation
**Goal**: Reproduce a computational result from a paper autonomously

**Prompt**:
"Reproduce a key result from a recent MLIP paper:

Paper: 'Universal machine learning interatomic potentials are ready for phonons' (npj Comp. Mat., 2025)

Task:
1. Find and read the paper
2. Identify a key figure or table to reproduce
3. Set up the exact same calculation (structure, model, method)
4. Run the calculation
5. Compare your result to the published result
6. Quantify agreement/disagreement

You must autonomously:
- Find the paper
- Extract methodology
- Implement the calculation
- Validate against published results"

**Skills Tested**:
- Literature comprehension
- Methodology extraction
- Exact reproduction
- Scientific validation

**Time Limit**: 180 min
**Difficulty**: Expert

---

### BENCH-T9-005: Autonomous Error Diagnosis
**Goal**: Diagnose and fix ML model failures

**Prompt**:
"Debug why an MLIP is giving wrong results:

Scenario: A collaborator reports that CHGNet gives unreasonable results for MgO. The formation energy is wrong by 0.5 eV/atom.

Your Task:
1. Reproduce the error
2. Investigate possible causes:
   - Wrong structure?
   - Model limitation?
   - Calculation setup error?
   - Known chemistry gap?
3. Determine root cause
4. Propose and test a fix (different model, fine-tuning, etc.)
5. Document findings

This tests diagnostic reasoning when ML models fail."

**Skills Tested**:
- Debugging ML models
- Root cause analysis
- Knowledge of MLIP limitations
- Problem-solving

**Time Limit**: 120 min
**Difficulty**: Hard

---

## Tier 10: Frontier Challenges

### BENCH-T10-001: Novel Material Discovery Campaign
**Goal**: Propose and validate a new material

**Prompt**:
"Conduct an autonomous materials discovery campaign:

Target: Find a new Li-ion battery cathode material with:
- High voltage (> 4V vs Li/Li+)
- Good stability (formation energy < -1 eV/atom)
- Novel composition (not in Materials Project)

Campaign Phases:

Phase 1: Literature Survey
- What compositions have been explored?
- What makes a good cathode?
- Identify under-explored chemical spaces

Phase 2: Computational Screening
- Generate 100+ candidate structures
- Screen with MLIP for stability
- Rank by predicted voltage

Phase 3: Validation
- Select top 5 candidates
- Run DFT validation (or MLIP with error bars)
- Assess novelty vs existing databases

Phase 4: Report
- Propose 1-3 candidates for experimental synthesis
- Justify with computational evidence
- Discuss uncertainties and risks

This is real autonomous discovery research."

**Skills Tested**:
- Research strategy
- Creative hypothesis generation
- High-throughput workflow
- Scientific judgment
- Publication-quality analysis

**Time Limit**: 480 min (8 hours, async)
**Difficulty**: Research-Grade

---

### BENCH-T10-002: Cross-Modal Scientific Reasoning
**Goal**: Integrate computational and experimental data

**Prompt**:
"A collaborator provides experimental XRD data for a synthesized material. Determine its structure:

Provided: XRD pattern (simulated from unknown structure)

Your Task:
1. Analyze XRD peaks to identify crystal system
2. Propose candidate structures
3. Simulate XRD for each candidate using MLIP-relaxed structures
4. Match to experimental pattern
5. Refine structure to improve fit
6. Report final structure with confidence assessment

This requires integrating:
- Crystallography knowledge
- MLIP calculations
- Pattern matching algorithms
- Uncertainty quantification"

**Skills Tested**:
- Cross-modal reasoning
- Structure determination
- Experimental data analysis
- Integration of ML and traditional methods

**Time Limit**: 180 min
**Difficulty**: Expert

---

### BENCH-T10-003: Open Research Question
**Goal**: Make progress on an unsolved problem

**Prompt**:
"Investigate why universal MLIPs systematically underpredict phonon frequencies by ~15%:

This is a KNOWN but UNSOLVED problem in the MLIP community.

Your Investigation:
1. Reproduce the systematic error for 3 materials (Si, Cu, MgO)
2. Hypothesize causes:
   - Training data bias?
   - Architecture limitation?
   - Energy vs force weighting?
   - Something else?
3. Design experiments to test your hypotheses
4. Run experiments within your capabilities
5. Report findings with scientific rigor

You may not solve this, but make measurable progress and propose next steps.

This is how real research works - tackling open questions."

**Skills Tested**:
- Research methodology
- Hypothesis generation
- Experimental design
- Scientific writing
- Acknowledging limitations

**Time Limit**: 480 min (8 hours, async)
**Difficulty**: Research-Grade

---

## Implementation Notes

### Prerequisites for ML Benchmarks

**Software Stack:**
```bash
# Core MLIP packages
pip install mace-torch  # MACE
pip install matgl       # M3GNet, CHGNet
pip install ase         # Atomic Simulation Environment

# Supporting tools
pip install phonopy     # Phonon calculations
pip install pymatgen    # Structure manipulation

# GPU requirements
# CUDA 11.8+ for MACE GPU acceleration
# PyTorch with CUDA support
```

**Hardware:**
- GPU: RTX 3090/4090 or better (16GB+ VRAM)
- RAM: 32GB+ recommended
- Storage: 50GB+ for models and data

### Benchmark Harness Updates Needed

1. **New Tier Support**: Add tiers 8, 9, 10
2. **ML Environment Validation**: Check MACE/MatGL installation
3. **GPU Verification**: Ensure CUDA is available
4. **Longer Timeouts**: Tier 10 may need 8+ hours
5. **Async Support**: Long-running ML training

### Grading Considerations

**ML-Specific Rubric Categories:**

1. **Model Usage** (20-30%)
   - Correct model loading
   - Appropriate model selection
   - Proper inference setup

2. **Scientific Validity** (30-40%)
   - Results physically reasonable
   - Limitations acknowledged
   - Comparison to references

3. **Methodology** (20-30%)
   - Reproducible workflow
   - Clear documentation
   - Error quantification

4. **Innovation** (10-20%, for Tier 10)
   - Novel approaches
   - Creative problem-solving
   - Research insight

---

## Summary

| Tier | Focus | # Benchmarks | GPU Required | Key Challenge |
|------|-------|--------------|--------------|---------------|
| 8 | ML-Powered Materials Science | 7 | Yes | Using modern MLIP tools |
| 9 | Autonomous Research Workflows | 5 | Yes | Closed-loop, multi-fidelity |
| 10 | Frontier Challenges | 3 | Yes | Open research problems |

**Total new benchmarks: 15**

These benchmarks test whether the agent can:
1. **Use ML tools** (Tier 8): Load models, run calculations, interpret results
2. **Conduct autonomous research** (Tier 9): Active learning, optimization loops
3. **Tackle open problems** (Tier 10): Real research methodology

---

## Relationship to Existing Benchmarks

```
Tiers 1-4: Traditional computational materials science (LAMMPS, QE)
Tiers 5-7: HPC-enabled research (large scale, async)
Tiers 8-10: ML/AI-powered research (MLIPs, autonomous workflows)
```

The full benchmark suite now tests:
- **Can the agent do basic simulations?** (T1-T4)
- **Can the agent use HPC?** (T5-T7)
- **Can the agent use modern ML?** (T8-T10)
- **Can the agent conduct autonomous research?** (T9-T10)

This progression mirrors how computational materials science is evolving: from manual simulations → HPC scale-up → ML acceleration → autonomous discovery.
