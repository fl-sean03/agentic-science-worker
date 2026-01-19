# HPC + ML Hybrid Benchmarks

> **STATUS: IMPLEMENTED** - All 7 Tier 11 benchmarks have been created in
> `benchmarks/tasks/tier11_hpc_ml_hybrid/`. The harness has been updated
> to support Tier 11 with the `--include-hpc-ml` flag.

## The Gap: What's Missing

Current benchmarks test:
- **Tiers 5-7**: HPC operations with traditional simulations (LAMMPS, QE)
- **Tiers 8-10**: ML/AI on local GPU (MLIPs, autonomous workflows)

**Missing**: Combining ML/AI with HPC for problems that require BOTH:
- ML accuracy (near-DFT)
- HPC scale (100k+ atoms, multi-day simulations, massive parallelism)

## What HPC + ML Enables

| Capability | Local GPU | HPC + ML |
|------------|-----------|----------|
| MLIP system size | ~10,000 atoms | 100,000 - 1,000,000+ atoms |
| MLIP simulation time | Hours | Days to weeks |
| High-throughput screening | 100s of materials | 10,000+ materials |
| Active learning DFT | Limited by local resources | 1000s of DFT calculations |
| Multi-GPU inference | 1 GPU | 3× A100 per node, multi-node |
| Training large MLIPs | Limited | Full foundation model training |

## Proposed Benchmarks: Tier 11 - HPC-Scale ML Research

### BENCH-T11-001: Million-Atom MLIP Simulation
**Goal**: Run MLIP MD on a system too large for local GPU

**The Problem**:
- Local GPU: ~10-20k atoms practical limit (memory)
- Research need: Grain boundaries, dislocations, crack propagation need 100k+ atoms
- HPC A100s: 40GB memory, can handle 100k+ atoms

**Task**:
1. Create a polycrystalline copper system with grain boundaries (~100,000 atoms)
2. Submit MLIP MD job to HPC aa100 partition (GPU)
3. Run for 1 ns at 300K
4. Analyze grain boundary migration
5. This is IMPOSSIBLE on local 17GB GPU

**Skills Tested**: HPC GPU job submission, large-scale MLIP, async management

---

### BENCH-T11-002: Massive High-Throughput Screening
**Goal**: Screen 1000+ materials using HPC parallelism

**The Problem**:
- Local screening: 100-200 materials/day practical
- Research need: Comprehensive chemical space exploration
- HPC: 1000+ parallel jobs via job arrays

**Task**:
1. Generate 1000 candidate ternary oxide structures
2. Create SLURM job array to evaluate all with MLIP
3. Each job: relax structure, calculate formation energy
4. Collect results asynchronously
5. Rank all 1000 by stability
6. Identify top 50 for DFT validation

**Skills Tested**: Job arrays, result aggregation, high-throughput workflow

---

### BENCH-T11-003: Active Learning at Scale
**Goal**: Train accurate MLIP using HPC-scale DFT generation

**The Problem**:
- Active learning needs many DFT calculations
- Local: Limited to ~50-100 DFT calcs
- HPC: Can run 500-1000 DFT calculations in parallel

**Task**:
1. Goal: Train MLIP for high-entropy alloy (HEA) - 5 elements
2. Start with universal MLIP (poor for HEA)
3. Generate candidates, identify high-uncertainty configs
4. Submit 100 DFT calculations to HPC (job array)
5. Collect results, retrain MLIP
6. Iterate 3-5 times
7. Final model should have <30 meV/atom error

Budget: 500 DFT calculations total (only feasible on HPC)

**Skills Tested**: Active learning, HPC DFT, iterative campaigns

---

### BENCH-T11-004: Long-Timescale MLIP Dynamics
**Goal**: Run week-long MLIP simulation for rare event sampling

**The Problem**:
- Rare events (diffusion, nucleation) need long simulations
- Local: Hours of MD practical
- HPC: Days to weeks of continuous MD

**Task**:
1. Study Li-ion diffusion in solid electrolyte at LOW temperature (300K)
2. At 300K, diffusion is slow - need microsecond timescales
3. Submit multi-day MLIP MD job to HPC
4. Use checkpointing for job continuation
5. Analyze trajectory for diffusion events
6. Calculate diffusion coefficient with proper statistics

Required simulation time: ~10 microseconds (impossible locally)

**Skills Tested**: Long HPC jobs, checkpointing, rare event analysis

---

### BENCH-T11-005: Distributed MLIP Training
**Goal**: Train/fine-tune MLIP using multiple HPC GPUs

**The Problem**:
- Training large MLIPs needs multiple GPUs
- MACE foundation model: trained on 100s of GPUs
- Fine-tuning can benefit from multi-GPU

**Task**:
1. Prepare dataset of 10,000 configurations for a specific chemistry
2. Set up distributed MACE training across multiple GPUs
3. Submit training job to HPC (request 2-4 GPUs)
4. Monitor training loss
5. Evaluate final model accuracy

**Skills Tested**: Distributed training, HPC GPU allocation, ML training workflows

---

### BENCH-T11-006: Multi-Fidelity Campaign on HPC
**Goal**: Run comprehensive multi-fidelity study using HPC resources

**The Problem**:
- Multi-fidelity needs: cheap MLIP (fast) + expensive DFT/hybrid (slow)
- Local: Can't run many expensive calculations
- HPC: Can parallelize expensive tier

**Task**:
1. Screen 500 perovskite compositions with MLIP (fast, local or HPC)
2. Select top 100 for PBE DFT (submit to HPC CPU nodes)
3. Select top 20 for HSE hybrid DFT (submit to HPC, expensive)
4. Build multi-fidelity model
5. Predict HSE-quality band gaps for all 500

Cost model:
- MLIP: 1 minute each (local)
- PBE: 1 hour each (HPC CPU)
- HSE: 24 hours each (HPC CPU)

**Skills Tested**: Multi-fidelity, resource allocation, HPC DFT campaigns

---

### BENCH-T11-007: Autonomous Discovery Campaign with HPC
**Goal**: Full autonomous discovery loop using both local and HPC resources

**The Problem**:
- Real discovery needs iteration: screen → validate → refine → repeat
- Each iteration may need HPC for validation
- Must coordinate local ML with HPC DFT

**Task**:
1. **Day 1**: Literature survey, hypothesis generation (local)
2. **Day 1**: Initial MLIP screening of 1000 candidates (local GPU)
3. **Day 2**: Submit DFT validation for top 50 to HPC
4. **Day 2**: While waiting, refine screening criteria (local)
5. **Day 3**: Collect DFT results, identify false positives
6. **Day 3**: Retrain/adjust model, screen remaining space
7. **Day 4**: Final DFT validation of best candidates
8. **Day 5**: Write discovery report

This requires coordinating:
- Local: Fast ML screening, analysis, writing
- HPC: DFT validation batches (async)

**Skills Tested**: Full autonomous research, local/HPC coordination, multi-day campaigns

---

## Implementation Considerations

### HPC ML Environment on CURC

```bash
# On Alpine, need to set up ML environment
module load anaconda
conda create -n mlip python=3.10
conda activate mlip
pip install torch --index-url https://download.pytorch.org/whl/cu118
pip install mace-torch matgl chgnet ase
```

### SLURM Script for MLIP on GPU

```bash
#!/bin/bash
#SBATCH --partition=aa100
#SBATCH --gres=gpu:1
#SBATCH --time=24:00:00
#SBATCH --output=mlip_%j.out

module load anaconda cuda/11.8
conda activate mlip

python run_mlip_md.py --atoms 100000 --steps 1000000
```

### Job Arrays for Screening

```bash
#!/bin/bash
#SBATCH --partition=amilan
#SBATCH --array=0-999
#SBATCH --time=00:30:00

# Each task processes one structure
python evaluate_structure.py --index $SLURM_ARRAY_TASK_ID
```

---

## Relationship to Existing Tiers

```
Tiers 1-4:   Traditional computational science (local)
Tiers 5-7:   HPC + traditional simulations
Tiers 8-10:  ML/AI on local GPU
Tier 11:     HPC + ML/AI hybrid (NEW)
```

Tier 11 represents the frontier - combining:
- Scale of HPC
- Intelligence of ML
- Autonomy of AI agents

---

## Summary

| Benchmark | Key Challenge | HPC Resource | ML Component |
|-----------|---------------|--------------|--------------|
| T11-001 | Million-atom simulation | A100 GPU | MACE inference |
| T11-002 | 1000+ material screening | Job arrays | MLIP evaluation |
| T11-003 | Active learning at scale | DFT job arrays | MLIP training |
| T11-004 | Microsecond dynamics | Long GPU job | MLIP MD |
| T11-005 | Distributed training | Multi-GPU | MACE training |
| T11-006 | Multi-fidelity campaign | DFT tiers | ML screening |
| T11-007 | Full discovery loop | Mixed | Full autonomous |

**Total: 7 new HPC+ML benchmarks**

These represent the cutting edge of computational materials science -
where AI agents coordinate ML models and HPC resources for discoveries
that neither could achieve alone.
