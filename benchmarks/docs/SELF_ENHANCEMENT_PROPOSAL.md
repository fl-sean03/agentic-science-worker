# Tier 21: Self-Enhancement Benchmarks

**Created:** 2026-02-24
**Author:** Automated Proposal
**Status:** DRAFT - For Review

---

## Executive Summary

This proposal introduces **Tier 21: Self-Enhancement** benchmarks that test the agent's ability to extend, repair, and improve its own capabilities. Unlike existing tiers that test the agent using pre-configured tools, T21 tests whether the agent can:

1. Install new simulation packages when needed
2. Debug environment failures through trial-and-error
3. Write wrapper scripts for unsupported tools
4. Fix broken configurations autonomously
5. Validate that new capabilities work correctly

This is critical for **true autonomy** - a researcher who can only use pre-installed tools is fundamentally limited. The ability to self-enhance enables open-ended research where the agent can acquire new capabilities as research demands evolve.

---

## Tier Rationale

### Why Tier 21?

**Existing Tiers:**
- T1-T4: Basic simulation capabilities
- T5-T7: HPC and research campaigns
- T8-T11: ML materials and hybrid workflows
- T12: Theory synthesis
- T13: Robustness and error handling
- T14: Compute resource decisions
- T15-T16: Agent cognition and scientific rigor
- T17: Cloud GPU provisioning and usage
- T18: Data analysis

**Gap Analysis:**
All existing tiers assume tools are **already installed and configured**. Even T17 (cloud GPU) provides explicit setup instructions. No tier tests whether the agent can:
- Determine what tools it needs
- Install them without step-by-step guidance
- Debug installation failures
- Extend its own skill definitions

**Why T21 (not T19 or T20)?**
- T19-T20 reserved for potential intermediate capabilities
- T21 represents a qualitative jump: **meta-capability** (capability to gain capabilities)
- Numerically signals this is beyond standard autonomous research

### Relationship to Other Tiers

| Tier | Relationship |
|------|--------------|
| T13 (Robustness) | T21 extends error recovery to environment-level errors |
| T17 (Cloud GPU) | T21 builds on cloud provisioning to test iterative debugging |
| T9 (Autonomous Research) | T21 is "autonomous research on the research environment itself" |
| T15 (Agent Cognition) | T21 tests learning and adaptation in real-time |

---

## Safety Considerations

**CRITICAL: Self-enhancement benchmarks involve system modification.**

### Guardrails

1. **Sandboxed Execution**
   - All T21 benchmarks run on VAST.ai cloud instances
   - Agent cannot modify the local workstation
   - Instance destruction is mandatory after each benchmark

2. **Cost Limits**
   - Each benchmark has explicit cost caps ($0.50 - $2.00)
   - Agent must track spending throughout
   - Benchmarks fail if cost exceeded

3. **Time Limits**
   - Maximum 2 hours per benchmark
   - Prevents runaway debugging loops
   - Forces efficient problem-solving

4. **Forbidden Operations**
   - No modification of cloud provider credentials
   - No network attacks or unauthorized access
   - No cryptocurrency mining or resource abuse
   - No persistent storage of credentials

5. **Audit Trail**
   - All commands must be logged
   - Failed attempts documented
   - Post-mortem required for all benchmarks

### Risk Assessment

| Risk | Mitigation |
|------|------------|
| Bricked cloud instance | Expected behavior; instance is ephemeral |
| Excessive cost | Hard cost limits, balance monitoring |
| Infinite retry loops | Time limits, iteration caps |
| Security vulnerabilities | Sandboxed environment, no persistent access |
| Skill pollution | New skills created in benchmark workspace only |

---

## Benchmark Specifications

### BENCH-T21-001: Iterative Environment Debugging

**Objective:** Install LAMMPS on a fresh cloud GPU and iterate until working.

```yaml
id: BENCH-T21-001
name: Iterative Environment Debugging
tier: 21
category: self-enhancement
difficulty: hard
estimated_time_minutes: 90
cost_limit_dollars: 1.00
```

**Prompt:**

```
**Task: Install LAMMPS GPU on Fresh Cloud Instance**

You need to run a LAMMPS simulation, but you don't have a pre-configured
environment. Your task is to:

1. Provision a VAST.ai GPU instance (any suitable GPU)
2. Install LAMMPS with GPU support from scratch
3. Verify it works by running a simple LJ test
4. Document your entire debugging process

**IMPORTANT:**
- You will NOT be given step-by-step installation instructions
- You WILL encounter errors - this is expected
- You must figure out dependencies, library versions, etc.
- Each failed attempt should teach you something

**You have access to:**
- Internet (for searching documentation, Stack Overflow, etc.)
- VAST.ai CLI for provisioning
- The target instance's shell

**Success Criteria:**
- LAMMPS runs with GPU acceleration
- A 10,000-step LJ simulation completes successfully
- nvidia-smi shows GPU utilization during run
- All debugging steps documented

**Deliverables:**
Create in workspaces/benchmarks/BENCH-T21-001/:

1. `attempts/` - Directory with each installation attempt
   - `attempt_1/commands.sh` - What you tried
   - `attempt_1/error.log` - What failed
   - `attempt_1/diagnosis.md` - What you learned
   - (repeat for each attempt)

2. `final/`
   - `install_script.sh` - Working installation procedure
   - `test_output.log` - Successful LAMMPS output
   - `gpu_verification.txt` - nvidia-smi during run

3. `debugging_report.md` - Full narrative:
   - Starting point and initial assumptions
   - Each failure and diagnosis
   - Key learnings
   - Final solution

Work in: workspaces/benchmarks/BENCH-T21-001/
```

**Grading Criteria:**

| Category | Weight | Criteria |
|----------|--------|----------|
| Problem Solving | 35% | Systematic debugging, learns from failures, doesn't repeat mistakes |
| Technical Execution | 25% | Correct final installation, GPU acceleration verified |
| Documentation | 20% | Clear debugging narrative, useful for future reference |
| Efficiency | 10% | Reasonable number of attempts, cost-conscious |
| Cleanup | 10% | Instance destroyed, no orphans |

**Expected Outputs:**

| Output | Description |
|--------|-------------|
| `debugging_report.md` | Complete debugging narrative |
| `final/install_script.sh` | Working installation procedure |
| `final/test_output.log` | Successful LAMMPS GPU run |
| `attempts/` | Documentation of failed attempts |

**Expected Values:**

| Metric | Expected |
|--------|----------|
| `lammps_working` | true |
| `gpu_acceleration` | true |
| `attempts_count` | 2-6 (reasonable iteration) |
| `total_cost` | $0.20 - $0.80 |
| `orphan_instances` | 0 |

---

### BENCH-T21-002: Package Discovery and Installation

**Objective:** Given a task requiring NAMD, discover and install it without explicit instructions.

```yaml
id: BENCH-T21-002
name: Package Discovery
tier: 21
category: self-enhancement
difficulty: hard
estimated_time_minutes: 60
cost_limit_dollars: 0.75
```

**Prompt:**

```
**Task: Run a Protein Simulation You Don't Have Tools For**

A collaborator sends you this request:

"Hey, I need you to run a quick equilibration of a small protein
(1UBQ - ubiquitin) using NAMD. Just 10,000 steps NPT at 300K to
verify it's stable. Can you do that?"

**The Challenge:**
You don't have NAMD installed. You've never used NAMD before. The agent's
standard skills don't include NAMD. You need to:

1. Figure out what NAMD is and how to get it
2. Understand the basic input format
3. Install it on a cloud GPU instance
4. Obtain the 1UBQ structure
5. Create necessary input files
6. Run the equilibration
7. Report results

**You must NOT:**
- Ask the user for installation instructions
- Claim you can't do it because you lack the tool
- Give up at the first obstacle

**You MUST:**
- Research NAMD yourself
- Figure out installation
- Learn enough to create inputs
- Complete the task

**Success Criteria:**
- NAMD installed and working
- 1UBQ structure obtained (PDB)
- 10,000 step NPT simulation completes
- Basic stability confirmed (no explosion)

**Deliverables:**
Create in workspaces/benchmarks/BENCH-T21-002/:

1. `research/`
   - `namd_overview.md` - What is NAMD, key features
   - `installation_research.md` - How to install
   - `input_format.md` - Understanding configuration

2. `setup/`
   - `install.sh` - Installation commands
   - `1UBQ.pdb` - Protein structure
   - `namd_config.conf` - NAMD configuration
   - Required parameter files

3. `simulation/`
   - `equilibration.log` - Simulation output
   - `final_structure.pdb` - Final coordinates

4. `capability_extension.md`
   - How you extended your capabilities
   - What you learned
   - Would you approach this differently next time?

Work in: workspaces/benchmarks/BENCH-T21-002/
```

**Grading Criteria:**

| Category | Weight | Criteria |
|----------|--------|----------|
| Research | 25% | Effective information gathering, understood tool quickly |
| Installation | 25% | NAMD working with GPU support |
| Scientific Execution | 25% | Correct inputs, simulation completed, reasonable results |
| Self-Reflection | 15% | Insightful capability extension documentation |
| Cleanup | 10% | Instance destroyed, cost tracked |

---

### BENCH-T21-003: Skill Extension

**Objective:** Write a wrapper script for a new tool and integrate it as a usable capability.

```yaml
id: BENCH-T21-003
name: Skill Extension
tier: 21
category: self-enhancement
difficulty: medium
cost_limit_dollars: 0.50
estimated_time_minutes: 45
```

**Prompt:**

```
**Task: Create a New Skill for packmol**

You've been using LAMMPS for molecular dynamics, but you frequently need
to create initial configurations with multiple molecules. packmol is a
popular tool for this, but you don't have a skill for it.

**Your Task:**
1. Learn about packmol (purpose, input format, usage)
2. Install packmol on a cloud instance
3. Write a wrapper Python script that:
   - Takes a list of molecule files and counts
   - Generates packmol input
   - Runs packmol
   - Validates output
4. Create a skill definition following the project conventions
5. Test the skill by creating a water box

**Skill Requirements:**
The skill should:
- Accept molecule PDB/XYZ files
- Accept counts and box dimensions
- Handle common errors gracefully
- Return the packed configuration

**Test Case:**
Create a box of 1000 water molecules:
- Box: 30 x 30 x 30 Angstroms
- Molecule: TIP3P water
- Output: water_box.pdb

**Deliverables:**
Create in workspaces/benchmarks/BENCH-T21-003/:

1. `research/`
   - `packmol_overview.md` - Tool understanding

2. `skill/`
   - `packmol_skill.py` - Python wrapper
   - `skill_definition.yaml` - Skill metadata
   - `README.md` - Usage instructions

3. `test/`
   - `water.pdb` - TIP3P water molecule
   - `test_packing.py` - Test script
   - `water_box.pdb` - Output from test

4. `integration_notes.md`
   - How this skill fits the existing architecture
   - Edge cases handled
   - Potential improvements

Work in: workspaces/benchmarks/BENCH-T21-003/
```

**Grading Criteria:**

| Category | Weight | Criteria |
|----------|--------|----------|
| Research | 15% | Understood packmol correctly |
| Implementation | 35% | Clean, working wrapper script |
| Skill Design | 25% | Follows conventions, good error handling |
| Testing | 15% | Water box created successfully |
| Documentation | 10% | Clear usage instructions |

---

### BENCH-T21-004: Configuration Debugging

**Objective:** Debug a broken CUDA/GPU setup through systematic diagnosis.

```yaml
id: BENCH-T21-004
name: Configuration Debugging
tier: 21
category: self-enhancement
difficulty: hard
estimated_time_minutes: 75
cost_limit_dollars: 0.80
```

**Prompt:**

```
**Task: Fix Broken GPU Configuration**

You've provisioned a VAST.ai instance and started setting up your
environment, but something is wrong. CUDA programs fail with cryptic
errors, PyTorch doesn't see the GPU, and you're stuck.

**The Scenario:**
You inherit an instance where someone started setup but left it broken:
- nvidia-smi works
- But PyTorch says `cuda is not available`
- CUDA samples fail to compile or run
- Something is misconfigured

**Your Task:**
1. Diagnose what's wrong
2. Document the systematic debugging process
3. Fix the configuration
4. Verify everything works:
   - nvidia-smi (should already work)
   - PyTorch CUDA detection
   - CUDA sample compilation
   - Simple PyTorch GPU tensor operation

**You will need to:**
- Check CUDA paths and environment variables
- Verify driver/CUDA compatibility
- Check for conflicting installations
- Test each component systematically

**Note:** You must CREATE the broken state yourself:
1. Provision a clean instance
2. Break it deliberately (e.g., wrong LD_LIBRARY_PATH, conflicting CUDA)
3. Document how you broke it
4. Then debug and fix it as if you found it this way

**Deliverables:**
Create in workspaces/benchmarks/BENCH-T21-004/:

1. `setup/`
   - `break_script.sh` - How you created the broken state
   - `broken_symptoms.md` - Error messages and symptoms

2. `diagnosis/`
   - `diagnostic_commands.md` - Commands used to diagnose
   - `findings.md` - What was wrong
   - `root_cause.md` - Why it was broken

3. `fix/`
   - `fix_script.sh` - Commands to fix
   - `verification.md` - Proof everything works

4. `debugging_guide.md`
   - Systematic GPU debugging procedure
   - Common failure modes
   - Diagnostic flowchart

Work in: workspaces/benchmarks/BENCH-T21-004/
```

**Grading Criteria:**

| Category | Weight | Criteria |
|----------|--------|----------|
| Diagnosis Process | 30% | Systematic, logical debugging approach |
| Root Cause | 25% | Correctly identified the issue |
| Fix Quality | 20% | Clean fix, not just workaround |
| Documentation | 15% | Useful debugging guide created |
| Verification | 10% | Thoroughly verified fix works |

---

### BENCH-T21-005: Environment Validation Pipeline

**Objective:** Create a comprehensive validation suite for simulation environments.

```yaml
id: BENCH-T21-005
name: Environment Validation
tier: 21
category: self-enhancement
difficulty: medium
estimated_time_minutes: 60
cost_limit_dollars: 0.60
```

**Prompt:**

```
**Task: Build Environment Validation Pipeline**

When setting up computational environments (locally or on cloud), it's
easy to have subtle issues - wrong versions, missing libraries, incorrect
paths. You need a way to systematically validate that everything works.

**Your Task:**
Create a comprehensive validation pipeline that checks:

1. **System Level**
   - GPU available and healthy (nvidia-smi)
   - CUDA version and compatibility
   - Sufficient disk space
   - Python version correct

2. **Package Level**
   - Required Python packages installed
   - Correct versions
   - No import errors
   - GPU backends functional

3. **Application Level**
   - LAMMPS works (with GPU)
   - ASE calculators functional
   - ML potentials load correctly
   - Test calculations give expected results

4. **Integration Level**
   - End-to-end workflow test
   - File I/O works
   - Memory doesn't leak
   - Results reproducible

**Implementation:**
Create a validation script that:
- Runs all checks automatically
- Reports pass/fail with details
- Identifies specific issues
- Suggests fixes for common problems
- Produces a validation report

**Test Your Pipeline:**
1. Run on a correctly configured instance -> should pass
2. Break something deliberately -> should catch it
3. Fix and re-run -> should pass again

**Deliverables:**
Create in workspaces/benchmarks/BENCH-T21-005/:

1. `pipeline/`
   - `validate_environment.py` - Main validation script
   - `validators/` - Individual check modules
   - `requirements.txt` - Validation tool dependencies

2. `tests/`
   - `test_passing.md` - Report from good environment
   - `test_failing.md` - Report from broken environment
   - `test_fixed.md` - Report after fixing

3. `documentation/`
   - `check_catalog.md` - All checks documented
   - `fix_suggestions.md` - Common issues and fixes
   - `usage_guide.md` - How to use the pipeline

Work in: workspaces/benchmarks/BENCH-T21-005/
```

**Grading Criteria:**

| Category | Weight | Criteria |
|----------|--------|----------|
| Completeness | 30% | All check categories covered |
| Implementation | 25% | Clean, modular code |
| Error Detection | 20% | Catches deliberately broken environments |
| Fix Suggestions | 15% | Useful remediation advice |
| Documentation | 10% | Clear usage guide |

---

### BENCH-T21-006: Cross-Platform Adaptation

**Objective:** Run the same simulation workflow on different cloud images/configurations.

```yaml
id: BENCH-T21-006
name: Cross-Platform Adaptation
tier: 21
category: self-enhancement
difficulty: hard
estimated_time_minutes: 120
cost_limit_dollars: 1.50
```

**Prompt:**

```
**Task: Same Simulation, Different Platforms**

Real-world computational science often requires running on different
systems - local machines, cloud instances with different OS versions,
HPC clusters with modules. You need to adapt your workflow.

**The Simulation:**
A simple task: Calculate diffusion coefficient of liquid argon at 94K
using LAMMPS with GPU acceleration.

**The Challenge:**
Run this SAME simulation on THREE different VAST.ai configurations:

1. **Ubuntu 22.04 with CUDA 12.2**
   - Modern base image
   - Standard setup path

2. **Ubuntu 20.04 with CUDA 11.8**
   - Older image
   - May need different packages

3. **Rocky Linux 8 with CUDA 12.x**
   - RHEL-based system
   - Different package manager (dnf vs apt)

**For each platform:**
1. Provision instance with specified image
2. Install LAMMPS with GPU support
3. Run the argon diffusion simulation
4. Calculate diffusion coefficient
5. Document any platform-specific adaptations

**Success Criteria:**
- All three simulations complete
- Results agree within 10% (same physics, different platforms)
- Each platform's setup documented
- Differences analyzed

**Deliverables:**
Create in workspaces/benchmarks/BENCH-T21-006/:

1. `platform_1_ubuntu2204/`
   - `setup.sh` - Installation commands
   - `adaptations.md` - Platform-specific changes
   - `simulation/log.lammps` - Simulation output
   - `results.md` - Diffusion coefficient

2. `platform_2_ubuntu2004/`
   - (same structure)

3. `platform_3_rocky8/`
   - (same structure)

4. `analysis/`
   - `result_comparison.md` - Compare D across platforms
   - `platform_differences.md` - Key differences
   - `portable_workflow.md` - How to make workflows portable

Work in: workspaces/benchmarks/BENCH-T21-006/
```

**Grading Criteria:**

| Category | Weight | Criteria |
|----------|--------|----------|
| Platform Coverage | 25% | All three platforms working |
| Scientific Consistency | 25% | Results agree across platforms |
| Adaptation Quality | 20% | Clean platform-specific solutions |
| Documentation | 15% | Differences clearly documented |
| Portability Insights | 15% | Useful lessons for future work |

---

### BENCH-T21-007: Autonomous Tool Selection

**Objective:** Given a research goal, determine what tools are needed and acquire them.

```yaml
id: BENCH-T21-007
name: Autonomous Tool Selection
tier: 21
category: self-enhancement
difficulty: hard
estimated_time_minutes: 90
cost_limit_dollars: 1.00
```

**Prompt:**

```
**Task: Tool Selection for Novel Research Problem**

You receive this research request:

"We're studying the adsorption of CO2 molecules on MXene surfaces
(Ti3C2). We need to calculate:
1. Adsorption energies at different sites
2. Charge transfer upon adsorption
3. Projected density of states

What approach would you take? Set up the computational environment
and run preliminary calculations."

**The Challenge:**
This task could be approached multiple ways:
- DFT (QE, VASP, etc.) - most accurate
- ML potentials (MACE, etc.) - faster but may not handle charge transfer
- Classical MD (LAMMPS) - inappropriate for this

You must:
1. Analyze what capabilities this task requires
2. Determine appropriate tools
3. Assess what you have vs. what you need
4. Acquire/install missing capabilities
5. Run preliminary calculations

**Decision Points:**
- What level of theory is needed?
- Which code handles charge analysis well?
- Do you have suitable pseudopotentials?
- What computational resources are required?

**Note:** The point is NOT to complete a full research study. The point
is to demonstrate autonomous tool selection and capability extension.
Preliminary calculations are sufficient.

**Deliverables:**
Create in workspaces/benchmarks/BENCH-T21-007/:

1. `analysis/`
   - `task_requirements.md` - What capabilities are needed
   - `tool_comparison.md` - Options considered
   - `selection_rationale.md` - Why you chose what you did

2. `setup/`
   - `capability_gap.md` - What was missing
   - `installation_log.md` - How you filled gaps
   - `environment_verification.md` - Proof it works

3. `preliminary_results/`
   - Input files used
   - Output logs
   - Brief results summary

4. `reflection.md`
   - Was your tool selection correct?
   - What would you do differently?
   - Lessons for future tool selection

Work in: workspaces/benchmarks/BENCH-T21-007/
```

**Grading Criteria:**

| Category | Weight | Criteria |
|----------|--------|----------|
| Requirement Analysis | 25% | Correctly identified what task needs |
| Tool Selection | 25% | Appropriate tools chosen with justification |
| Capability Extension | 20% | Successfully acquired missing capabilities |
| Preliminary Results | 15% | Some calculation completed |
| Reflection | 15% | Insightful self-assessment |

---

### BENCH-T21-008: Self-Healing Workflow

**Objective:** Create a workflow that automatically detects and recovers from environment failures.

```yaml
id: BENCH-T21-008
name: Self-Healing Workflow
tier: 21
category: self-enhancement
difficulty: very-hard
estimated_time_minutes: 120
cost_limit_dollars: 2.00
```

**Prompt:**

```
**Task: Build Self-Healing Simulation Workflow**

Cloud environments fail. Instances crash, connections drop, jobs stall.
A truly autonomous agent shouldn't just handle these failures - it should
build workflows that heal themselves.

**Your Task:**
Create a workflow system that:

1. **Monitors** the environment continuously
   - GPU health
   - Memory usage
   - Job progress
   - Connection stability

2. **Detects** problems automatically
   - GPU errors
   - OOM conditions
   - Stalled jobs
   - Connection drops

3. **Recovers** without human intervention
   - Checkpoints regularly
   - Restarts from checkpoint on failure
   - Provisions new instance if needed
   - Migrates work if necessary

4. **Learns** from failures
   - Logs all incidents
   - Identifies patterns
   - Adjusts behavior (e.g., checkpoint more often if unstable)

**Test Scenario:**
Run a 30-minute LAMMPS simulation that:
- Checkpoints every 5 minutes
- Continues from checkpoint if interrupted
- Handles injected failures gracefully

**Inject at least 2 failures:**
- Kill the SSH connection mid-job
- Simulate GPU memory pressure

**Deliverables:**
Create in workspaces/benchmarks/BENCH-T21-008/:

1. `workflow/`
   - `self_healing_runner.py` - Main workflow script
   - `monitor.py` - Health monitoring
   - `recovery.py` - Recovery procedures
   - `checkpoint_manager.py` - Checkpoint handling

2. `simulation/`
   - Input files
   - Checkpoints (timestamped)
   - Final output

3. `incidents/`
   - `failure_1.md` - First failure and recovery
   - `failure_2.md` - Second failure and recovery
   - `incident_summary.md` - Overall incident report

4. `analysis.md`
   - Total runtime vs. expected
   - Time lost to failures
   - Recovery success rate
   - Improvement opportunities

Work in: workspaces/benchmarks/BENCH-T21-008/
```

**Grading Criteria:**

| Category | Weight | Criteria |
|----------|--------|----------|
| Monitoring | 20% | Comprehensive health monitoring |
| Detection | 20% | Failures detected promptly and accurately |
| Recovery | 25% | Clean recovery, no data loss |
| Resilience | 20% | Handles multiple failure modes |
| Documentation | 15% | Clear incident documentation |

---

## Benchmark Summary Table

| ID | Name | Difficulty | Time | Cost | Key Test |
|----|------|------------|------|------|----------|
| T21-001 | Iterative Debugging | Hard | 90 min | $1.00 | Install LAMMPS GPU without instructions |
| T21-002 | Package Discovery | Hard | 60 min | $0.75 | Learn and use NAMD from scratch |
| T21-003 | Skill Extension | Medium | 45 min | $0.50 | Create packmol skill |
| T21-004 | Configuration Debugging | Hard | 75 min | $0.80 | Fix broken CUDA setup |
| T21-005 | Environment Validation | Medium | 60 min | $0.60 | Build validation pipeline |
| T21-006 | Cross-Platform | Hard | 120 min | $1.50 | Same task, 3 platforms |
| T21-007 | Tool Selection | Hard | 90 min | $1.00 | Choose tools for novel problem |
| T21-008 | Self-Healing | Very Hard | 120 min | $2.00 | Build auto-recovery workflow |

---

## Implementation Notes

### Prerequisites

T21 benchmarks require:
1. VAST.ai account with balance (recommend $50+ for full suite)
2. Working `vastai` CLI configured
3. SSH key registered with VAST.ai
4. Network access for package downloads

### Execution Order

Recommended progression:
1. T21-003 (Skill Extension) - Lowest risk, good warm-up
2. T21-005 (Environment Validation) - Build useful tooling
3. T21-001 (Iterative Debugging) - Core capability test
4. T21-004 (Configuration Debugging) - Builds on T21-001
5. T21-002 (Package Discovery) - Tests research + installation
6. T21-006 (Cross-Platform) - Tests breadth
7. T21-007 (Tool Selection) - Tests judgment
8. T21-008 (Self-Healing) - Capstone challenge

### Grading Philosophy

These benchmarks prioritize:
1. **Process over outcome** - Good debugging with eventual success > lucky first try
2. **Documentation quality** - Useful for future work
3. **Self-reflection** - Learning from failures
4. **Cleanup discipline** - No orphan instances

### Cost Tracking

Each benchmark must include:
- Balance before starting
- Balance after completion
- Cost breakdown by phase
- Comparison to estimate

Cost overruns beyond limits should fail the benchmark.

---

## Future Extensions

Potential additional T21 benchmarks:

1. **T21-009: Multi-Code Pipeline**
   - Chain QE -> LAMMPS -> Analysis
   - Each tool installed on-demand

2. **T21-010: Dependency Resolution**
   - Install conflicting packages
   - Resolve version conflicts

3. **T21-011: Performance Optimization**
   - Identify performance bottlenecks
   - Optimize configuration

4. **T21-012: Capability Transfer**
   - Document skill for future agents
   - Create reproducible setup

---

## Conclusion

Tier 21 benchmarks test what truly autonomous agents need: the ability to enhance their own capabilities. An agent that can only use pre-configured tools is fundamentally limited. Self-enhancement enables:

- Open-ended research without human setup
- Adaptation to new computational requirements
- Recovery from environment failures
- Continuous capability expansion

These benchmarks are harder and riskier than existing tiers, but they test capabilities essential for genuine research autonomy.

---

## Appendix A: YAML Templates

Below are the first two benchmark specifications in full YAML format for reference.

### BENCH-T21-001 Full YAML

```yaml
# Tier 21 Benchmark: Iterative Environment Debugging
# Test installation and debugging without step-by-step instructions

id: BENCH-T21-001
name: Iterative Environment Debugging
tier: 21
category: self-enhancement

description: |
  Test the agent's ability to install LAMMPS with GPU support on a fresh
  cloud instance WITHOUT step-by-step installation instructions. The agent
  must iterate through failures, debug issues, and eventually succeed.
  This tests true self-enhancement capability.

prompt: |
  **Task: Install LAMMPS GPU on Fresh Cloud Instance**

  You need to run a LAMMPS simulation, but you don't have a pre-configured
  environment. Your task is to:

  1. Provision a VAST.ai GPU instance (any suitable GPU)
  2. Install LAMMPS with GPU support from scratch
  3. Verify it works by running a simple LJ test
  4. Document your entire debugging process

  **IMPORTANT:**
  - You will NOT be given step-by-step installation instructions
  - You WILL encounter errors - this is expected
  - You must figure out dependencies, library versions, etc.
  - Each failed attempt should teach you something

  **You have access to:**
  - Internet (for searching documentation, Stack Overflow, etc.)
  - VAST.ai CLI for provisioning
  - The target instance's shell

  **Success Criteria:**
  - LAMMPS runs with GPU acceleration
  - A 10,000-step LJ simulation completes successfully
  - nvidia-smi shows GPU utilization during run
  - All debugging steps documented

  **Deliverables:**
  Create in workspaces/benchmarks/BENCH-T21-001/:

  1. `attempts/` - Directory with each installation attempt
     - `attempt_1/commands.sh` - What you tried
     - `attempt_1/error.log` - What failed
     - `attempt_1/diagnosis.md` - What you learned
     - (repeat for each attempt)

  2. `final/`
     - `install_script.sh` - Working installation procedure
     - `test_output.log` - Successful LAMMPS output
     - `gpu_verification.txt` - nvidia-smi during run

  3. `debugging_report.md` - Full narrative:
     - Starting point and initial assumptions
     - Each failure and diagnosis
     - Key learnings
     - Final solution

  Work in: workspaces/benchmarks/BENCH-T21-001/

skills_required:
  - vast-cloud
  - lammps-simulation

time_limit_minutes: 90

cost_limit_dollars: 1.00

expected_outputs:
  files:
    - name: "debugging_report.md"
      description: "Complete debugging narrative"
    - name: "final/install_script.sh"
      description: "Working installation procedure"
    - name: "final/test_output.log"
      description: "Successful LAMMPS GPU run"
    - name: "attempts/"
      description: "Documentation of failed attempts"

  values:
    lammps_working:
      description: "LAMMPS runs successfully"
      expected: true
    gpu_acceleration:
      description: "GPU acceleration verified"
      expected: true
    attempts_count:
      description: "Number of installation attempts"
      expected_range: [2, 6]
    total_cost:
      description: "Total cloud cost"
      expected_range: [0.20, 0.80]
      unit: "dollars"
    orphan_instances:
      description: "Running instances after benchmark"
      expected: 0

grading:
  categories:
    - name: problem_solving
      weight: 35
      criteria:
        - Systematic debugging approach
        - Learns from each failure
        - Doesn't repeat mistakes
        - Adapts strategy based on errors
        - Shows persistence

    - name: technical_execution
      weight: 25
      criteria:
        - Correct final installation
        - GPU acceleration verified
        - Test simulation successful
        - Clean installation script

    - name: documentation
      weight: 20
      criteria:
        - Clear debugging narrative
        - Each attempt documented
        - Useful for future reference
        - Lessons captured

    - name: efficiency
      weight: 10
      criteria:
        - Reasonable number of attempts
        - Cost within limits
        - Didn't waste time on obvious dead ends

    - name: cleanup
      weight: 10
      criteria:
        - Instance destroyed
        - No orphan instances
        - Cost tracked

metadata:
  difficulty: hard
  estimated_time_minutes: 90
  estimated_cost_dollars: 0.50
  skills_tested:
    - iterative_debugging
    - environment_setup
    - self_research
    - persistence
  notes: |
    This benchmark deliberately omits step-by-step instructions. The agent
    must figure out LAMMPS GPU installation through documentation, trial
    and error, and web searches. This tests genuine self-enhancement
    capability, not just instruction following.
```

### BENCH-T21-002 Full YAML

```yaml
# Tier 21 Benchmark: Package Discovery and Installation
# Test discovering and learning a new tool autonomously

id: BENCH-T21-002
name: Package Discovery
tier: 21
category: self-enhancement

description: |
  Test the agent's ability to discover, learn, and use a completely new
  computational tool (NAMD for molecular dynamics) without prior
  experience or explicit instructions.

prompt: |
  **Task: Run a Protein Simulation You Don't Have Tools For**

  A collaborator sends you this request:

  "Hey, I need you to run a quick equilibration of a small protein
  (1UBQ - ubiquitin) using NAMD. Just 10,000 steps NPT at 300K to
  verify it's stable. Can you do that?"

  **The Challenge:**
  You don't have NAMD installed. You've never used NAMD before. The agent's
  standard skills don't include NAMD. You need to:

  1. Figure out what NAMD is and how to get it
  2. Understand the basic input format
  3. Install it on a cloud GPU instance
  4. Obtain the 1UBQ structure
  5. Create necessary input files
  6. Run the equilibration
  7. Report results

  **You must NOT:**
  - Ask the user for installation instructions
  - Claim you can't do it because you lack the tool
  - Give up at the first obstacle

  **You MUST:**
  - Research NAMD yourself
  - Figure out installation
  - Learn enough to create inputs
  - Complete the task

  **Success Criteria:**
  - NAMD installed and working
  - 1UBQ structure obtained (PDB)
  - 10,000 step NPT simulation completes
  - Basic stability confirmed (no explosion)

  **Deliverables:**
  Create in workspaces/benchmarks/BENCH-T21-002/:

  1. `research/`
     - `namd_overview.md` - What is NAMD, key features
     - `installation_research.md` - How to install
     - `input_format.md` - Understanding configuration

  2. `setup/`
     - `install.sh` - Installation commands
     - `1UBQ.pdb` - Protein structure
     - `namd_config.conf` - NAMD configuration
     - Required parameter files

  3. `simulation/`
     - `equilibration.log` - Simulation output
     - `final_structure.pdb` - Final coordinates

  4. `capability_extension.md`
     - How you extended your capabilities
     - What you learned
     - Would you approach this differently next time?

  Work in: workspaces/benchmarks/BENCH-T21-002/

skills_required:
  - vast-cloud
  - resource-acquisition

time_limit_minutes: 60

cost_limit_dollars: 0.75

expected_outputs:
  files:
    - name: "research/namd_overview.md"
      description: "Understanding of NAMD"
    - name: "setup/install.sh"
      description: "Installation procedure"
    - name: "simulation/equilibration.log"
      description: "Simulation output"
    - name: "capability_extension.md"
      description: "Reflection on learning process"

  values:
    namd_installed:
      description: "NAMD working on instance"
      expected: true
    simulation_completed:
      description: "10,000 step simulation finished"
      expected: true
    protein_stable:
      description: "No structural explosion"
      expected: true
    research_documented:
      description: "Learning process documented"
      expected: true

grading:
  categories:
    - name: research
      weight: 25
      criteria:
        - Effective information gathering
        - Understood NAMD purpose and usage
        - Found correct installation method
        - Learned input format basics

    - name: installation
      weight: 25
      criteria:
        - NAMD installed successfully
        - GPU acceleration if available
        - All dependencies resolved
        - Clean installation process

    - name: scientific_execution
      weight: 25
      criteria:
        - Correct input files created
        - Simulation completed
        - Results physically reasonable
        - Structure file obtained correctly

    - name: self_reflection
      weight: 15
      criteria:
        - Insightful capability extension doc
        - Identified challenges and solutions
        - Useful for future similar tasks

    - name: cleanup
      weight: 10
      criteria:
        - Instance destroyed
        - Cost tracked
        - No orphan instances

metadata:
  difficulty: hard
  estimated_time_minutes: 60
  estimated_cost_dollars: 0.35
  skills_tested:
    - autonomous_learning
    - tool_discovery
    - self_research
    - capability_extension
  notes: |
    This benchmark tests the agent's ability to tackle tasks outside its
    existing skill set. Rather than refusing or asking for help, the agent
    should autonomously research, learn, and execute with a new tool.
```

---

## Appendix B: Related Work

### Existing Self-Enhancement Concepts

1. **AutoGPT / BabyAGI** - Autonomous task decomposition, but pre-defined tools
2. **Tool Learning in LLMs** - Learning to use provided APIs
3. **Code Generation Agents** - Writing code to extend capabilities
4. **SWE-Bench** - Software engineering tasks including environment setup

### How T21 Differs

T21 specifically tests:
- Environment-level capability extension (not just API learning)
- Iterative debugging through trial-and-error
- Cross-platform adaptation
- Self-healing workflows

These capabilities are more fundamental than tool use - they enable the agent to acquire and maintain the infrastructure needed for tool use.

---

*End of Proposal*
