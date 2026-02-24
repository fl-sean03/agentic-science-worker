# Showcases

Real examples of autonomous research conducted by the Agentic Science Worker. Each showcase demonstrates end-to-end capability on a challenging scientific task.

## Featured Showcases

### 1. [Novel Li-Ion Cathode Discovery](novel-cathode-discovery/)
**Benchmark:** T10-001 | **Score:** 75/100 | **Time:** 22 min

The agent autonomously discovered **9 novel high-voltage cathode materials** not in the Materials Project database. The top discovery, Li2Ni(PO4)(SO4), achieves 5.1V with excellent stability.

**What it demonstrates:**
- Literature-driven hypothesis generation
- High-throughput computational screening (88 candidates)
- MLIP-based stability filtering
- Novelty verification against databases
- Publication-quality research report

---

### 2. [XRD Structure Determination](xrd-structure-determination/)
**Benchmark:** T10-002 | **Score:** 72/100 | **Time:** 8 min

Given only an XRD pattern, the agent determined the crystal structure is **layered R-3m LiNiO2** through systematic analysis and pattern matching against 23 candidate structures.

**What it demonstrates:**
- Cross-modal scientific reasoning (experimental -> computational)
- Bragg's law calculations and systematic absence analysis
- Database queries and structure comparison
- Publication-quality figures

---

### 3. [Cloud GPU Automation](cloud-gpu-automation/)
**Benchmark:** T17-001 | **Score:** 97/100 | **Time:** 5 min

The agent autonomously provisioned a cloud GPU (VAST.ai), verified functionality, and properly cleaned up resources - demonstrating infrastructure management capability.

**What it demonstrates:**
- Autonomous cloud resource provisioning
- Cost-aware GPU selection
- Proper resource cleanup (no orphaned instances)
- Infrastructure reliability

---

## How to Explore

Each showcase includes:
- `README.md` - Summary and key findings
- `outputs/` or `images/` - Key files and visualizations
- Links to full benchmark results

## Running Your Own

```bash
# Run any benchmark to see the agent in action
python benchmarks/evaluation/harness.py BENCH-T10-001

# Results saved to: benchmarks/results/runs/
# Workspace created at: workspaces/benchmarks/
```

## Benchmark Scores Explained

| Score | Meaning |
|-------|---------|
| 90-100 | Exceptional - exceeds expectations |
| 70-89 | Good - solid scientific work |
| 50-69 | Adequate - meets basic requirements |
| <50 | Needs improvement |

All showcases achieved **passing scores** (threshold: 40) on first attempt.
