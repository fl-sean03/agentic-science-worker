# HPC Benchmark Proposal: Tier 5 and Beyond

> **STATUS: IMPLEMENTED**
>
> All 15 HPC benchmarks have been implemented:
> - Tier 5: 7 benchmarks in `tasks/tier5_hpc_fundamentals/`
> - Tier 6: 5 benchmarks in `tasks/tier6_hpc_scale/`
> - Tier 7: 3 benchmarks in `tasks/tier7_research_campaigns/`
>
> The benchmark harness has been updated to support tiers 5-7 with:
> - New pass thresholds (60%, 55%, 50%)
> - HPC infrastructure verification
> - `--include-hpc` flag for running HPC benchmarks
> - `--async-mode` flag for async job management

## What HPC Enables (That Local Can't Do)

| Capability | Local Workstation | HPC (Alpine) |
|------------|-------------------|--------------|
| Max atoms (practical) | ~10,000 | 100,000 - 1,000,000+ |
| Max simulation time | Minutes | Hours to days |
| Parallel cores | 8-16 | 64-128+ per node |
| GPU memory | 8-24 GB | 40 GB (A100) × 3 |
| Multi-node | No | Yes (100s of nodes) |
| Long queues | N/A | Days (must handle async) |

## New Skill Dimensions to Test

### 1. HPC Operations
- SSH connection and file transfer
- Module loading and environment setup
- SLURM job script creation
- Partition selection (testing → production)
- Queue awareness and wait time estimation
- Async job submission and monitoring
- Error recovery from failed HPC jobs

### 2. Scale-Up Reasoning
- When does a problem NEED HPC?
- System size convergence testing
- Parallel efficiency considerations
- Resource estimation (cores, memory, time)

### 3. Production Research Workflows
- Multi-day simulation campaigns
- Parameter sweeps with job arrays
- Checkpoint and restart strategies
- Data management at scale

---

## Proposed Benchmark Tiers

### Existing Tiers (Local Workstation)
- **Tier 1**: Basic skills (single tool)
- **Tier 2**: Intermediate (multi-skill workflows)
- **Tier 3**: Advanced (research workflows)
- **Tier 4**: Research-level (independent investigation)

### New Tiers (HPC-Enabled)

#### **Tier 5: HPC Fundamentals**
Test basic HPC operations - can the agent successfully use HPC?

#### **Tier 6: HPC-Scale Research**
Problems that REQUIRE HPC scale - can't be done locally.

#### **Tier 7: Production Campaigns**
Multi-job, multi-day research campaigns with async management.

---

## Tier 5: HPC Fundamentals (7 benchmarks)

### BENCH-T5-001: HPC Connection and Validation
**Goal**: Verify agent can connect to HPC and run a simple job

**Prompt**:
"Verify you can access the CURC Alpine HPC cluster. Connect via SSH, check your
scratch space quota, submit a simple 'hello world' job to the atesting partition,
wait for it to complete, and report the results."

**Skills Tested**:
- SSH connection
- Basic SLURM commands
- atesting partition usage
- Job monitoring

**Time Limit**: 15 min
**Difficulty**: Easy

---

### BENCH-T5-002: Local-to-HPC Migration
**Goal**: Take a working local LAMMPS simulation and run it on HPC

**Prompt**:
"You have a working LAMMPS simulation of liquid argon (input provided). Migrate this
simulation to run on HPC:
1. Create appropriate job script for atesting partition
2. Upload files to HPC
3. Submit and monitor the job
4. Download and verify results match local execution
5. Report any differences"

**Skills Tested**:
- Job script creation
- File transfer (scp/rsync)
- Module loading on HPC
- Result verification

**Time Limit**: 30 min
**Difficulty**: Easy-Medium

---

### BENCH-T5-003: Queue-Aware Partition Selection
**Goal**: Choose optimal partition based on job requirements and queue status

**Prompt**:
"You need to run a LAMMPS simulation that requires:
- 64 CPU cores
- ~4 hours runtime
- No GPU needed

Check the current queue status for amilan and amilan128c partitions. Based on
estimated wait times and job requirements, choose the optimal partition. Justify
your choice with queue statistics. Submit a test job to validate your choice."

**Skills Tested**:
- Queue analysis
- Partition comparison
- Resource matching
- Decision justification

**Time Limit**: 20 min
**Difficulty**: Medium

---

### BENCH-T5-004: HPC Job Debugging
**Goal**: Diagnose and fix a failing HPC job

**Prompt**:
"A LAMMPS job is failing on HPC. The job script and input files are provided, but
the job fails shortly after starting. Debug the issue:
1. Submit the job as-is and observe the failure
2. Examine error logs and output files
3. Identify the problem
4. Fix the job script or input
5. Resubmit and verify success

Common issues: wrong module versions, path errors, resource limits."

**Skills Tested**:
- Error log analysis
- HPC-specific debugging
- Module system understanding
- Iterative problem solving

**Time Limit**: 30 min
**Difficulty**: Medium

---

### BENCH-T5-005: GPU Job Submission
**Goal**: Run a GPU-accelerated simulation on HPC

**Prompt**:
"Run a LAMMPS simulation using GPU acceleration on HPC:
1. Check aa100 partition availability
2. Create a job script requesting 1 GPU
3. Configure LAMMPS for GPU execution (KOKKOS or GPU package)
4. Submit to atesting_a100 first to validate
5. If queue permits, submit to aa100 for full run
6. Compare GPU performance to CPU baseline"

**Skills Tested**:
- GPU partition usage
- LAMMPS GPU configuration
- Performance comparison
- Testing-first workflow

**Time Limit**: 45 min
**Difficulty**: Medium-Hard

---

### BENCH-T5-006: Async Job Management
**Goal**: Submit a long-running job and manage it asynchronously

**Prompt**:
"Submit a production LAMMPS job that will take 2+ hours to complete:
1. Estimate resource requirements
2. Check queue and choose partition
3. Submit job using async workflow (don't block waiting)
4. Save job tracking information
5. Demonstrate how to check job status later
6. Set up email notifications for completion

Since we can't wait for completion in this benchmark, focus on proper async
submission workflow and status checking."

**Skills Tested**:
- Async job submission
- Tracking file management
- Status monitoring
- Email notification setup

**Time Limit**: 30 min
**Difficulty**: Medium

---

### BENCH-T5-007: Multi-Job Parameter Sweep
**Goal**: Submit multiple jobs exploring different parameters

**Prompt**:
"Conduct a parameter sweep studying the effect of temperature on liquid argon
diffusion. Submit 5 separate jobs at temperatures: 85K, 95K, 105K, 115K, 125K.

Use SLURM job arrays OR submit as separate jobs. Each job should:
- Run independently
- Write results to separate directories
- Be tracked for async monitoring

Provide a summary of all submitted jobs and how to collect results when complete."

**Skills Tested**:
- Multi-job management
- Job arrays (optional)
- Organized output structure
- Result collection strategy

**Time Limit**: 45 min
**Difficulty**: Medium-Hard

---

## Tier 6: HPC-Scale Research (5 benchmarks)

### BENCH-T6-001: System Size Convergence Study
**Goal**: Determine converged system size for diffusion calculation

**Prompt**:
"Conduct a system size convergence study for liquid argon self-diffusion:

Run MD simulations with increasing system sizes:
- 256 atoms (local feasible)
- 1,000 atoms
- 4,000 atoms
- 10,000 atoms
- 32,000 atoms (HPC required)

For each size, calculate the diffusion coefficient. Plot D vs N^(-1/3) to
extrapolate the infinite-size limit. Determine the minimum system size needed
for converged results (<5% error from infinite limit).

This study requires HPC for the larger systems."

**Skills Tested**:
- Convergence study design
- Scale-up methodology
- Resource estimation per system size
- Scientific analysis of finite-size effects

**Time Limit**: 180 min (async jobs)
**Difficulty**: Hard

---

### BENCH-T6-002: Long-Timescale Diffusion Study
**Goal**: Study diffusion over nanosecond timescales

**Prompt**:
"Calculate the self-diffusion coefficient of a viscous liquid (glycerol or
a model thereof) at room temperature. This requires:

- System: ~5000 atoms of a viscous molecular liquid
- Challenge: Slow dynamics requires NANOSECONDS of simulation
- Expected: D ~ 10^-12 m²/s (1000× slower than argon)

Design and execute a simulation campaign:
1. Estimate required simulation time to observe diffusive behavior
2. Plan HPC resources needed
3. Run equilibration (may take hours)
4. Run production (may take a day)
5. Analyze MSD to extract D
6. Compare to experimental values

This problem is IMPOSSIBLE on a local workstation due to timescale requirements."

**Skills Tested**:
- Timescale estimation
- Long simulation planning
- Checkpoint strategies
- Slow-dynamics analysis

**Time Limit**: 24 hours (async)
**Difficulty**: Expert

---

### BENCH-T6-003: Large-Scale Phonon Calculation
**Goal**: Calculate phonon dispersion for a large supercell

**Prompt**:
"Calculate the phonon dispersion of silicon using the finite-displacement method.
This requires:
- Large supercell (4×4×4 or larger, 512+ atoms)
- Many force calculations (6N displacements for N-atom cell)
- Parallel execution of many independent calculations

Use Quantum ESPRESSO or LAMMPS with appropriate force field.
Submit displacement calculations as a job array on HPC.
Post-process to obtain phonon dispersion and DOS.
Compare to experimental/literature phonon spectrum."

**Skills Tested**:
- Phonon methodology
- Job array for independent calculations
- Large-scale DFT or MD
- Post-processing workflows

**Time Limit**: 240 min
**Difficulty**: Expert

---

### BENCH-T6-004: High-Throughput Screening
**Goal**: Screen multiple materials for a target property

**Prompt**:
"Screen 10 different metal systems for hydrogen adsorption energy:
- Metals: Pd, Pt, Ni, Cu, Ag, Au, Fe, Co, Rh, Ir
- Calculate H adsorption energy on (111) surface

For each metal:
1. Get structure from Materials Project
2. Create (111) surface slab
3. Calculate clean surface energy
4. Add H atom and optimize
5. Calculate adsorption energy

Submit all calculations to HPC (can run in parallel).
Rank metals by H adsorption strength.
Identify candidates for hydrogen storage/catalysis."

**Skills Tested**:
- High-throughput workflow design
- Automated structure preparation
- Parallel job management
- Result aggregation and ranking

**Time Limit**: 300 min (async)
**Difficulty**: Expert

---

### BENCH-T6-005: Production-Quality Phase Diagram Point
**Goal**: Calculate a publication-quality free energy difference

**Prompt**:
"Calculate the melting temperature of aluminum using the solid-liquid
coexistence method (two-phase simulation):

1. Literature research: Find Al EAM potential and expected Tm (~933 K)
2. Create two-phase system: solid Al | liquid Al interface
3. Run NPT simulation at various temperatures
4. Identify temperature where interface is stable
5. Estimate Tm with uncertainty

This requires:
- Large system (10,000+ atoms for good interface)
- Long simulations (nanoseconds for equilibration)
- Multiple temperature runs

Report Tm with statistical uncertainty and comparison to experiment."

**Skills Tested**:
- Advanced simulation methodology
- Two-phase simulations
- Uncertainty quantification
- Publication-quality analysis

**Time Limit**: 480 min (async)
**Difficulty**: Expert

---

## Tier 7: Research Campaigns (3 benchmarks)

### BENCH-T7-001: Multi-Day Research Study
**Goal**: Conduct a complete research study over multiple days

**Prompt**:
"Conduct a systematic study of thermal conductivity in silicon as a function of
isotope mass disorder:

Phase 1 (Day 1): Literature + Setup
- Review thermal conductivity calculation methods
- Choose appropriate potential (Tersoff, Stillinger-Weber, ML)
- Design simulation protocol

Phase 2 (Day 2): Pure Si baseline
- Calculate thermal conductivity of pure Si-28
- Validate against experiment (~150 W/m·K at 300K)

Phase 3 (Day 3): Isotope study
- Natural Si (mixed isotopes)
- Pure Si-29
- Pure Si-30
- 50/50 Si-28/Si-30 mixture

Phase 4 (Day 4): Analysis + Report
- Analyze isotope mass effect
- Compare to theoretical predictions (Klemens model)
- Write publication-quality report

This is a MULTI-DAY campaign requiring proper async job management."

**Skills Tested**:
- Multi-day planning
- Campaign management
- Research methodology
- Publication-quality output

**Time Limit**: 96 hours (4 days, async)
**Difficulty**: Research-grade

---

### BENCH-T7-002: Autonomous Error Recovery
**Goal**: Complete a study despite encountering failures

**Prompt**:
"Complete a study of water viscosity at multiple temperatures. However, you will
encounter problems:
- Some jobs will fail (deliberately misconfigured)
- Some will timeout
- Some will produce unreasonable results

Your task:
1. Submit jobs for T = 280K, 300K, 320K, 340K, 360K
2. Monitor for completion
3. Identify and diagnose failures
4. Resubmit with fixes
5. Validate results against literature
6. Complete the study despite setbacks

This tests resilience and autonomous problem-solving."

**Skills Tested**:
- Error detection and diagnosis
- Autonomous recovery
- Result validation
- Persistence through failures

**Time Limit**: 180 min
**Difficulty**: Expert

---

### BENCH-T7-003: Collaborative Computation
**Goal**: Coordinate local and HPC resources efficiently

**Prompt**:
"Conduct a hybrid local/HPC study:

On LOCAL workstation:
- Literature research
- Small test calculations
- Data analysis and plotting
- Report writing

On HPC:
- Production simulations
- Large-scale calculations

Study: Compare EAM and ML potentials for copper diffusion

1. Run small validation tests locally
2. Submit production runs to HPC
3. While HPC jobs queue/run, continue local analysis
4. Pull results from HPC when ready
5. Synthesize into final report

Efficiently coordinate both resources without wasting time waiting."

**Skills Tested**:
- Multi-resource coordination
- Efficient workflow planning
- Parallel workstreams
- Resource-appropriate task assignment

**Time Limit**: 120 min
**Difficulty**: Hard

---

## Grading Considerations for HPC Benchmarks

### HPC-Specific Rubric Categories

1. **HPC Operations** (15-25%)
   - Correct SSH usage
   - Proper job scripts
   - Appropriate partition selection
   - Module loading

2. **Queue Awareness** (10-15%)
   - Checked queue before submitting
   - Reasonable partition choice given wait times
   - Async workflow for long waits

3. **Resource Estimation** (10-15%)
   - Appropriate core count
   - Reasonable time limits
   - Memory considerations

4. **Error Handling** (10-20%)
   - Graceful failure handling
   - Diagnostic approach
   - Recovery strategy

5. **Scientific Quality** (40-60%)
   - Same as existing benchmarks
   - Results physically reasonable
   - Proper documentation
   - Literature comparison

### Practical Considerations

1. **Async Benchmarks**:
   - Can't wait for completion in benchmark harness
   - Grade on: proper submission, tracking setup, methodology
   - Optional: manual verification of completed results

2. **Cost Awareness**:
   - HPC time is a shared resource
   - Benchmarks should not waste allocation
   - Prefer atesting for validation

3. **Queue Variability**:
   - Queue times vary day-to-day
   - Benchmarks should test queue-awareness, not assume specific wait

---

## Implementation Priority

### Phase 1: Foundation (Implement First)
- BENCH-T5-001: HPC Connection
- BENCH-T5-002: Local-to-HPC Migration
- BENCH-T5-004: Job Debugging
- BENCH-T5-006: Async Management

### Phase 2: Scale-Up
- BENCH-T5-003: Queue-Aware Selection
- BENCH-T5-005: GPU Jobs
- BENCH-T5-007: Parameter Sweeps
- BENCH-T6-001: Size Convergence

### Phase 3: Research-Grade
- BENCH-T6-002 through T6-005
- BENCH-T7-001 through T7-003

---

## Summary

| Tier | Focus | # Benchmarks | Typical Time | HPC Required |
|------|-------|--------------|--------------|--------------|
| 5 | HPC Fundamentals | 7 | 15-45 min | Yes (atesting) |
| 6 | HPC-Scale Research | 5 | 3-8 hours | Yes (production) |
| 7 | Research Campaigns | 3 | 1-4 days | Yes (multi-day) |

**Total new benchmarks: 15**

These benchmarks progressively test:
1. Can the agent USE HPC? (Tier 5)
2. Can the agent do things that REQUIRE HPC? (Tier 6)
3. Can the agent conduct SUSTAINED research campaigns? (Tier 7)
