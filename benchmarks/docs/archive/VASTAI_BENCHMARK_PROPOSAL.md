# VAST.ai Cloud GPU Benchmark Proposal

**Created:** 2026-02-20
**Purpose:** Design benchmarks that test autonomous cloud GPU provisioning and usage

---

## Motivation

With CURC HPC deferred, VAST.ai becomes our primary cloud compute option. Current T14 benchmarks test compute *decisions* but don't exercise the full VAST.ai lifecycle:

| Current Coverage | Gap |
|------------------|-----|
| Decision-making (T14-001-005) | Actual instance provisioning |
| Cost estimation | Real cost tracking |
| Backend selection | Environment setup on cloud |
| Workflow design | File transfer and result retrieval |

**Goal:** Test the agent's ability to autonomously provision, use, and clean up cloud GPUs.

---

## Proposed Benchmarks

### Tier 17: Cloud GPU Operations

New tier specifically for cloud compute operations.

---

### BENCH-T17-001: Basic Instance Lifecycle

**Difficulty:** Easy | **Time:** 15 min | **Cost:** ~$0.10

**Task:** Complete the full instance lifecycle:
1. Search for cheapest RTX 3090/4090 under $0.40/hr
2. Create instance with appropriate image
3. Wait for SSH ready
4. Run `nvidia-smi` to verify GPU
5. Destroy instance

**Tests:**
- Instance selection logic
- SSH readiness handling
- Proper cleanup (no orphaned instances)

**Grading:**
- Instance created successfully (25%)
- GPU verified working (25%)
- Instance destroyed promptly (25%)
- Cost under $0.15 (25%)

---

### BENCH-T17-002: Environment Setup

**Difficulty:** Medium | **Time:** 30 min | **Cost:** ~$0.25

**Task:** Set up a complete simulation environment on VAST:
1. Provision RTX 4090 instance
2. Install: conda, ASE, MACE, CHGNet
3. Verify installation with test calculation
4. Document setup time and any issues
5. Destroy instance

**Tests:**
- Package installation in cloud environment
- Dependency resolution
- Environment verification
- Setup efficiency (time to first calculation)

**Grading:**
- All packages installed (30%)
- Test calculation succeeds (30%)
- Setup under 15 min (20%)
- Clean destruction (20%)

---

### BENCH-T17-003: File Transfer Workflow

**Difficulty:** Medium | **Time:** 45 min | **Cost:** ~$0.35

**Task:** Execute a complete local→cloud→local workflow:
1. Prepare LAMMPS input locally (NaCl melt simulation)
2. Provision instance and setup LAMMPS
3. Upload input files via SCP
4. Run simulation on cloud GPU
5. Download trajectory and log files
6. Analyze MSD locally
7. Destroy instance

**Tests:**
- Efficient file transfer
- Correct working directory management
- Result retrieval before destruction
- Local/cloud coordination

**Grading:**
- Simulation runs on cloud (25%)
- Results downloaded successfully (25%)
- MSD analysis completed locally (25%)
- Instance destroyed, cost tracked (25%)

---

### BENCH-T17-004: Cost-Aware GPU Selection

**Difficulty:** Medium | **Time:** 30 min | **Cost:** ~$0.30

**Task:** Make optimal GPU selection for a given workload:
1. Given: MACE relaxation of 500-atom system
2. Search available GPUs
3. Estimate job duration on different GPUs
4. Calculate total cost for each option
5. Select optimal GPU (balance speed vs cost)
6. Execute job, track actual cost
7. Compare estimate to actual

**Tests:**
- Performance estimation
- Cost calculation accuracy
- Decision justification
- Actual vs estimated comparison

**Expected Behavior:**
- RTX 4090 typically optimal for medium MACE jobs
- A100 faster but often not cost-effective for small jobs
- RTX 3090 cheapest but may be too slow

**Grading:**
- Selection justified with estimates (30%)
- Job completes successfully (25%)
- Actual cost within 50% of estimate (25%)
- Clear cost analysis in report (20%)

---

### BENCH-T17-005: Multi-Instance Parallel Jobs

**Difficulty:** Hard | **Time:** 60 min | **Cost:** ~$1.00

**Task:** Run parallel jobs across multiple VAST instances:
1. Task: Screen 5 metal surfaces for H adsorption (Cu, Ag, Au, Pt, Pd)
2. Provision 2-3 instances simultaneously
3. Distribute calculations across instances
4. Collect results from all instances
5. Aggregate and analyze
6. Destroy all instances

**Tests:**
- Multi-instance coordination
- Work distribution strategy
- Result aggregation
- Proper cleanup of all instances

**Grading:**
- All 5 calculations complete (30%)
- Parallel execution (not sequential) (25%)
- Results aggregated correctly (25%)
- All instances destroyed (20%)

---

### BENCH-T17-006: Error Recovery

**Difficulty:** Hard | **Time:** 45 min | **Cost:** ~$0.40

**Task:** Handle cloud compute failures gracefully:
1. Start LAMMPS simulation on VAST
2. **Injected failure:** Instance becomes unresponsive mid-job
3. Detect the failure
4. Decide: retry same instance, new instance, or local?
5. Recover and complete the job
6. Document lessons learned

**Implementation:** Use a small system with deliberate timeout.

**Tests:**
- Failure detection (SSH timeout, job stall)
- Recovery decision-making
- Checkpoint/restart awareness
- Cost accounting despite failure

**Grading:**
- Failure detected appropriately (25%)
- Recovery strategy reasonable (25%)
- Job eventually completes (25%)
- Orphaned instances cleaned up (25%)

---

### BENCH-T17-007: Long Job with Checkpointing

**Difficulty:** Hard | **Time:** 90 min | **Cost:** ~$0.75

**Task:** Run a longer job with checkpoint management:
1. Task: 1ns MD of ionic liquid (needs ~60 min on 4090)
2. Configure LAMMPS restart files every 10 min
3. Monitor job progress remotely
4. If interrupted, restore from checkpoint
5. Retrieve final results

**Tests:**
- Checkpoint configuration
- Progress monitoring
- Restart capability
- Long-running job management

**Grading:**
- Checkpoints created correctly (25%)
- Job monitored (progress tracked) (25%)
- Would survive interruption (checkpoint valid) (25%)
- Final results retrieved (25%)

---

### BENCH-T17-008: Hybrid Local-Cloud Pipeline

**Difficulty:** Expert | **Time:** 120 min | **Cost:** ~$1.50

**Task:** Complete research workflow spanning local and cloud:

**Phase 1 (Local):**
- Literature search for perovskite stability
- Download structures from Materials Project
- Prepare 10 input files

**Phase 2 (Cloud - VAST):**
- Provision A100 instance
- Setup QE environment
- Run 10 SCF calculations
- Download results

**Phase 3 (Local):**
- Parse all outputs
- Calculate stability metrics
- Generate comparison plot
- Write report

**Tests:**
- Seamless local↔cloud transitions
- Efficient batch processing on cloud
- Data pipeline integrity
- Cost-effective cloud usage

**Grading:**
- All 10 calculations complete (25%)
- Results correctly parsed (25%)
- Cloud time minimized (efficient batching) (25%)
- Total cost under $2.00 (25%)

---

## Implementation Notes

### Cost Safety

All benchmarks should:
1. Set hard cost limits in evaluation harness
2. Auto-destroy instances after timeout
3. Track and report actual spending
4. Fail gracefully if budget exceeded

```python
# In harness
MAX_COST_PER_BENCHMARK = {
    "T17-001": 0.25,
    "T17-002": 0.50,
    # ...
}
```

### Instance Cleanup Verification

After each benchmark:
```bash
vastai show instances --raw | grep -c "running"
# Should be 0 - fail if instances remain
```

### Grading Categories

| Category | Description |
|----------|-------------|
| provisioning | Instance selection and creation |
| execution | Job runs correctly on cloud |
| data_transfer | Files moved correctly |
| cleanup | Instances destroyed, no orphans |
| cost_efficiency | Reasonable spending |

---

## Tier Structure

```
benchmarks/tasks/tier17_cloud_gpu/
├── BENCH-T17-001-instance-lifecycle.yaml
├── BENCH-T17-002-environment-setup.yaml
├── BENCH-T17-003-file-transfer-workflow.yaml
├── BENCH-T17-004-cost-aware-selection.yaml
├── BENCH-T17-005-multi-instance-parallel.yaml
├── BENCH-T17-006-error-recovery.yaml
├── BENCH-T17-007-checkpoint-management.yaml
└── BENCH-T17-008-hybrid-pipeline.yaml
```

---

## Resource Requirements

| Benchmark | Est. Cost | GPU Type | Duration |
|-----------|-----------|----------|----------|
| T17-001 | $0.10 | RTX 3090/4090 | 15 min |
| T17-002 | $0.25 | RTX 4090 | 30 min |
| T17-003 | $0.35 | RTX 4090 | 45 min |
| T17-004 | $0.30 | Variable | 30 min |
| T17-005 | $1.00 | 2-3x RTX 4090 | 60 min |
| T17-006 | $0.40 | RTX 4090 | 45 min |
| T17-007 | $0.75 | RTX 4090 | 90 min |
| T17-008 | $1.50 | A100 | 120 min |
| **Total** | **~$4.65** | | ~7 hours |

Current balance: ~$25 → Can run full suite ~5 times

---

## Success Criteria

A passing T17 suite demonstrates:
1. Agent can autonomously provision cloud GPUs
2. Agent manages costs responsibly
3. Agent handles failures gracefully
4. Agent coordinates local/cloud compute effectively
5. Agent always cleans up resources

---

## Next Steps

1. [x] Create tier17_cloud_gpu directory ✅
2. [x] Implement T17-001 (simplest, validates infrastructure) → **97** ✅
3. [x] Implement T17-002 (environment setup) → **91** ✅
4. [x] Implement T17-003 (file transfer workflow) → **92** ✅
5. [ ] Add cost tracking to evaluation harness
6. [x] Implement T17-004 through T17-008 ✅ (created 2026-02-23)
7. [ ] Run T17-004 through T17-008
8. [ ] Document lessons learned

**Progress (2026-02-23):**
- Core benchmarks (T17-001, 002, 003) all passing on first run!
- T17-004 through T17-008 created (cost-aware, multi-instance, error recovery, checkpoint, hybrid pipeline)

---

*This proposal replaces the archived HPC benchmarks (T5, T6, T11) with cloud-native alternatives.*
