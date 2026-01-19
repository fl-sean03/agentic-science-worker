# Agent Improvement Plan: From Zero to Discovery

A comprehensive, detailed plan for iteratively improving the Agentic Science Worker
until it passes all benchmarks and is ready for real scientific discovery.

---

## Table of Contents

1. [Current State Assessment](#1-current-state-assessment)
2. [The Iteration Methodology](#2-the-iteration-methodology)
3. [Phase 0: Infrastructure Validation](#3-phase-0-infrastructure-validation)
4. [Phase 1: Tier 1 Mastery](#4-phase-1-tier-1-mastery)
5. [Phase 2: Tier 2 Integration](#5-phase-2-tier-2-integration)
6. [Phase 3: Tier 3 Research Workflows](#6-phase-3-tier-3-research-workflows)
7. [Phase 4: Tier 4 Scientific Reasoning](#7-phase-4-tier-4-scientific-reasoning)
8. [Phase 5: Discovery Readiness](#8-phase-5-discovery-readiness)
9. [Failure Diagnosis Guide](#9-failure-diagnosis-guide)
10. [Success Metrics](#10-success-metrics)

---

## 1. Current State Assessment

### What Exists

```
1-ScienceAgent/
├── CLAUDE.md                    ✅ Created - needs validation
├── .claude/
│   ├── settings.json            ✅ Created - needs testing
│   ├── skills/                  ✅ 5 skills created
│   │   ├── lammps-simulation/
│   │   ├── quantum-espresso/
│   │   ├── literature-search/
│   │   ├── materials-database/
│   │   └── data-analysis/
│   └── hooks/                   ✅ Basic hooks created
├── scripts/                     ✅ Utility scripts
├── benchmarks/                  ✅ Framework + 15 benchmarks
│   ├── tasks/
│   │   ├── tier1_basic/         6 benchmarks
│   │   ├── tier2_intermediate/  3 benchmarks
│   │   ├── tier3_advanced/      2 benchmarks
│   │   └── tier4_research/      6 benchmarks
│   └── evaluation/
│       ├── runner.py            ✅ Created
│       └── grader.py            ✅ Created
└── docs/                        ✅ Documentation
```

### What's Untested

- [ ] CLAUDE.md paths actually work
- [ ] Skills provide useful guidance
- [ ] Settings.json permissions are correct
- [ ] Hooks catch errors appropriately
- [ ] Agent can actually run simulations
- [ ] Benchmark runner executes correctly
- [ ] Grader produces meaningful scores

### Known Gaps

1. **No baseline measurement** - We don't know current pass rate
2. **Untested integrations** - Skills haven't been used in practice
3. **Missing reference solutions** - Benchmarks need validated answers
4. **No iteration history** - No log of what's been tried

---

## 2. The Iteration Methodology

### The Core Loop

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│   ┌─────────┐    ┌─────────┐    ┌─────────┐    ┌─────────┐        │
│   │  RUN    │───▶│ ANALYZE │───▶│ DIAGNOSE│───▶│  FIX    │        │
│   │Benchmark│    │ Results │    │ Failures│    │ (Small) │        │
│   └─────────┘    └─────────┘    └─────────┘    └─────────┘        │
│        ▲                                            │              │
│        │                                            │              │
│        └────────────────────────────────────────────┘              │
│                                                                     │
│   Repeat until pass rate meets target                              │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Key Principles

1. **Measure before changing** - Always know your baseline
2. **One fix at a time** - Isolate what works
3. **Smallest fix first** - CLAUDE.md before new tools
4. **Document everything** - Keep iteration log
5. **Validate fixes** - Re-run failed benchmark after fix

### The Fix Priority Stack

When a benchmark fails, try fixes in this order:

```
Priority 1: CLAUDE.md
   └── Add missing path, clarify capability
   └── Effort: 1 minute, Impact: High

Priority 2: Skill content
   └── Add example, clarify instructions
   └── Effort: 5 minutes, Impact: High

Priority 3: Settings/Permissions
   └── Allow blocked command
   └── Effort: 1 minute, Impact: Medium

Priority 4: Hooks
   └── Add validation, catch error earlier
   └── Effort: 15 minutes, Impact: Medium

Priority 5: Scripts/Tools
   └── Add helper script, wrapper
   └── Effort: 30 minutes, Impact: Medium

Priority 6: New Capability
   └── Add MCP server, new tool
   └── Effort: Hours, Impact: Varies

ONLY go to Priority N+1 after exhausting Priority N
```

---

## 3. Phase 0: Infrastructure Validation

**Goal:** Verify the system actually works before running benchmarks

**Duration:** 1-2 hours

### Step 0.1: Verify Tool Access

```bash
# Test LAMMPS
/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/md-lammps/install/bin/lmp -h

# Test QE
/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-cpu/bin/pw.x --help

# Test Python environment
python3 -c "import numpy; import matplotlib; print('OK')"

# Test GPU
nvidia-smi
```

**Pass criteria:** All commands execute without error

**If fails:** Fix paths in CLAUDE.md and settings.json

### Step 0.2: Verify Permissions

```bash
# From project directory, test allowed commands
cd /home/sf2/LabWork/Workspace/29-AgenticScienceWorker/1-ScienceAgent

# Check settings.json is valid JSON
python3 -c "import json; json.load(open('.claude/settings.json'))"

# Verify paths in settings match reality
grep -o '/[^"]*' .claude/settings.json | head -20 | while read p; do
  if [[ -e "${p%%:*}" ]] || [[ -e "${p%%\**}" ]]; then
    echo "✓ $p"
  else
    echo "✗ MISSING: $p"
  fi
done
```

**Pass criteria:** All paths exist

**If fails:** Update settings.json with correct paths

### Step 0.3: Verify Skills Load

```bash
# Check all skills have valid SKILL.md
for skill in .claude/skills/*/; do
  if [[ -f "${skill}SKILL.md" ]]; then
    echo "✓ $(basename $skill)"
  else
    echo "✗ MISSING: ${skill}SKILL.md"
  fi
done
```

**Pass criteria:** All 5 skills have SKILL.md

### Step 0.4: Test Benchmark Runner

```bash
# List benchmarks
python3 benchmarks/evaluation/runner.py --list

# Verify all benchmark YAML files parse
python3 -c "
import yaml
from pathlib import Path
for f in Path('benchmarks/tasks').rglob('*.yaml'):
    try:
        yaml.safe_load(open(f))
        print(f'✓ {f.name}')
    except Exception as e:
        print(f'✗ {f.name}: {e}')
"
```

**Pass criteria:** All benchmarks listed, all YAML valid

### Step 0.5: Manual Smoke Test

Before automated benchmarks, manually test one simple task:

```bash
# Start Claude Code in this directory
cd /home/sf2/LabWork/Workspace/29-AgenticScienceWorker/1-ScienceAgent
claude

# Give it a simple task:
# "Create a 10-atom LJ argon system and run a 100-step energy minimization.
#  Use epsilon=0.238 kcal/mol, sigma=3.405 Å. Work in workspaces/test/"
```

**Pass criteria:**
- Agent finds LAMMPS binary
- Creates valid input file
- Runs minimization
- Reports result

**If fails:** Note exactly where it failed, fix before proceeding

### Phase 0 Checklist

- [ ] LAMMPS binary works
- [ ] QE binary works (CPU at minimum)
- [ ] Python environment has numpy, matplotlib
- [ ] settings.json is valid and paths exist
- [ ] All 5 skills have SKILL.md
- [ ] Benchmark YAML files parse correctly
- [ ] Manual smoke test passes

**Only proceed to Phase 1 when ALL items checked**

---

## 4. Phase 1: Tier 1 Mastery

**Goal:** >95% pass rate on single-skill benchmarks

**Duration:** 1-3 days of iteration

### Tier 1 Benchmarks

| ID | Name | Skill | Expected Difficulty |
|----|------|-------|---------------------|
| T1-001 | LJ Minimization | LAMMPS | Easy |
| T1-002 | NVT Equilibration | LAMMPS | Easy |
| T1-003 | Literature Search | Literature | Easy |
| T1-004 | Materials Query | Materials DB | Easy |
| T1-005 | Log Analysis | Data Analysis | Easy |
| T1-006 | Si SCF | QE | Medium |

### Step 1.1: Run All Tier 1 Benchmarks

```bash
# Create results directory
mkdir -p benchmarks/results/phase1

# Run all Tier 1
python3 benchmarks/evaluation/runner.py --tier 1 2>&1 | tee benchmarks/results/phase1/run1.log

# Or run individually to see details
python3 benchmarks/evaluation/runner.py BENCH-T1-001
python3 benchmarks/evaluation/runner.py BENCH-T1-002
# ... etc
```

### Step 1.2: Record Baseline

Create iteration log:

```markdown
# benchmarks/results/ITERATION_LOG.md

## Phase 1, Run 1 - [DATE]

### Results
| Benchmark | Status | Notes |
|-----------|--------|-------|
| T1-001 | ? | |
| T1-002 | ? | |
| T1-003 | ? | |
| T1-004 | ? | |
| T1-005 | ? | |
| T1-006 | ? | |

**Pass rate:** X/6 (Y%)

### Failure Analysis
[Details for each failure]

### Changes Made
[None yet - this is baseline]
```

### Step 1.3: Analyze Each Failure

For each failed benchmark, determine:

1. **Where did it fail?**
   - Didn't attempt task?
   - Tool error?
   - Wrong output?
   - Timeout?

2. **Why did it fail?**
   - Missing information?
   - Wrong approach?
   - Tool problem?
   - Analysis error?

3. **What's the minimal fix?**
   - Add to CLAUDE.md?
   - Update skill?
   - Fix permission?
   - Add hook?

### Step 1.4: Fix Pattern Guide

**Pattern: "Couldn't find binary"**
```markdown
# Add to CLAUDE.md:
## Tool Paths
- LAMMPS: `/full/path/to/lmp`
- QE pw.x: `/full/path/to/pw.x`
```

**Pattern: "Used wrong parameters"**
```markdown
# Add to relevant skill:
## Standard Parameters
| System | ε | σ | Source |
|--------|---|---|--------|
| Argon | 0.238 kcal/mol | 3.405 Å | Allen & Tildesley |
```

**Pattern: "Simulation crashed"**
```markdown
# Add to skill:
## Common Errors and Fixes
- "Unknown atom style" → Use `atom_style atomic` for LJ
- "Illegal ... command" → Check LAMMPS version compatibility
```

**Pattern: "Analysis gave wrong value"**
```markdown
# Add to data-analysis skill:
## Formulas
- Diffusion: D = MSD_slope / (2 * dimensions)
- 3D: D = slope / 6
```

**Pattern: "Took too long"**
```markdown
# Add to skill:
## Recommended Settings
- LJ minimization: 1000 steps usually sufficient
- NVT equilibration: 10,000 steps for small systems
```

### Step 1.5: Iterate Until >95%

```
While pass_rate < 95%:
    1. Run failed benchmarks
    2. Analyze top failure
    3. Make ONE small fix
    4. Re-run that benchmark
    5. If passes, run all Tier 1 again
    6. Update iteration log
```

### Step 1.6: Document What Worked

After achieving >95%:

```markdown
## Phase 1 Complete - [DATE]

### Final Results
| Benchmark | Status | Attempts |
|-----------|--------|----------|
| T1-001 | ✓ | 2 |
| T1-002 | ✓ | 3 |
| ... | | |

**Final pass rate:** 6/6 (100%)

### Key Fixes Made
1. Added LAMMPS path to CLAUDE.md
2. Added LJ parameters to lammps-simulation skill
3. Fixed temperature units in NVT example
4. Added pseudopotential path for QE

### Lessons Learned
- Agent didn't know X, now knows Y
- Skill needed more explicit Z
```

### Phase 1 Exit Criteria

- [ ] All 6 Tier 1 benchmarks passing
- [ ] Pass rate >95% (allow 1 flaky failure)
- [ ] Iteration log complete
- [ ] Fixes documented

---

## 5. Phase 2: Tier 2 Integration

**Goal:** >80% pass rate on multi-skill benchmarks

**Duration:** 3-5 days of iteration

### Tier 2 Benchmarks

| ID | Name | Skills | Challenge |
|----|------|--------|-----------|
| T2-001 | Argon Diffusion | LAMMPS + Analysis | Run then analyze |
| T2-002 | Cu Lattice Constant | Materials DB + QE | Get structure then calculate |
| T2-003 | Water TIP4P | Literature + LAMMPS | Find params then simulate |

### Step 2.1: Baseline Measurement

```bash
# Run all Tier 2
python3 benchmarks/evaluation/runner.py --tier 2 2>&1 | tee benchmarks/results/phase2/run1.log
```

Record in iteration log.

### Step 2.2: Integration Failure Patterns

Multi-skill tasks fail differently than single-skill:

**Pattern: "First skill worked, second didn't use output"**
```markdown
# Add to CLAUDE.md or skill:
## Workflow: Literature → Simulation
1. Search for parameters, save to notes.md
2. Read notes.md before creating input file
3. Cite source in simulation comments
```

**Pattern: "Got structure but wrong format"**
```markdown
# Add to materials-database skill:
## Output Formats
- For LAMMPS: save as .data file
- For QE: save as .in format (ATOMIC_POSITIONS)
- Always verify atom count matches
```

**Pattern: "Simulation ran but analysis wrong"**
```markdown
# Add to data-analysis skill:
## Post-Simulation Workflow
1. First verify simulation completed (check log)
2. Identify output files (log.lammps, dump.*, etc.)
3. Parse correct columns from thermo output
4. Apply appropriate formulas
```

**Pattern: "Lost context between steps"**
```markdown
# Add to relevant skills:
## Multi-Step Tasks
- Save intermediate results to files
- Read previous outputs before next step
- Document what was done at each stage
```

### Step 2.3: Create Reference Solutions

For Tier 2+, create validated reference solutions:

```bash
# For each Tier 2 benchmark:
mkdir -p benchmarks/reference/solutions/t2-001-argon-diffusion

# Include:
# - input.lmp (known-good input file)
# - expected_output.txt (what success looks like)
# - analysis.py (reference analysis script)
# - README.md (notes on correct values)
```

### Step 2.4: Iterate

Same loop as Phase 1, but expect:
- More complex failures
- Need for workflow documentation
- Possible skill cross-references

### Phase 2 Exit Criteria

- [ ] All 3 Tier 2 benchmarks passing
- [ ] Pass rate >80%
- [ ] Reference solutions created
- [ ] Workflow patterns documented

---

## 6. Phase 3: Tier 3 Research Workflows

**Goal:** >60% pass rate on complex research tasks

**Duration:** 1-2 weeks of iteration

### Tier 3 Benchmarks

| ID | Name | Complexity |
|----|------|------------|
| T3-001 | H in Pd Diffusion | Full research workflow |
| T3-002 | Si Band Structure | DFT workflow with analysis |

### Step 3.1: Understand Why Tier 3 is Hard

Tier 3 requires:
- **Planning** - What steps, in what order?
- **Judgment** - What parameters are reasonable?
- **Recovery** - What to do when something fails?
- **Validation** - Is the result sensible?

These aren't just "more skills" - they require reasoning.

### Step 3.2: Add Planning Support

```markdown
# Add to CLAUDE.md:
## Research Workflow Pattern

For complex tasks, use this structure:

1. **Literature Phase**
   - Search for relevant papers
   - Extract parameters and methods
   - Document sources

2. **Setup Phase**
   - Get structures from databases
   - Create simulation inputs
   - Validate inputs before running

3. **Execution Phase**
   - Run simulations
   - Monitor for errors
   - Save all outputs

4. **Analysis Phase**
   - Parse output files
   - Calculate target properties
   - Compare to literature

5. **Reporting Phase**
   - Summarize methodology
   - Present results with uncertainties
   - Discuss any discrepancies
```

### Step 3.3: Add Checkpoints

For long workflows, add intermediate validation:

```markdown
# Add to skills:
## Checkpoint: After Literature Search
Before proceeding, verify:
- [ ] Found at least 2 relevant papers
- [ ] Extracted specific parameter values
- [ ] Have experimental comparison value

## Checkpoint: After Structure Setup
Before running:
- [ ] Structure file exists and is readable
- [ ] Atom count matches expectations
- [ ] Simulation input file syntax valid

## Checkpoint: After Simulation
Before analysis:
- [ ] Log file shows completion
- [ ] No ERROR messages
- [ ] Output files exist
```

### Step 3.4: Add Recovery Patterns

```markdown
# Add to skills:
## If Simulation Fails

1. Read error message carefully
2. Check common causes:
   - Wrong path?
   - Missing file?
   - Parameter out of range?
3. Fix and retry (max 3 attempts)
4. If still failing, report what was tried

## If Analysis Gives Unreasonable Result

1. Verify simulation actually ran correctly
2. Check units (common source of 10x errors)
3. Compare intermediate values to expectations
4. If stuck, report partial progress
```

### Step 3.5: Iterate with Partial Credit

Tier 3 uses milestones for partial credit:

```yaml
# In benchmark definition:
milestones:
  - id: M1
    description: "Literature search completed"
    weight: 0.15
  - id: M2
    description: "Simulation input created"
    weight: 0.25
  # etc.
```

Track which milestones are achieved even if final result is wrong.

### Phase 3 Exit Criteria

- [ ] Both Tier 3 benchmarks show progress
- [ ] At least 60% of milestones achieved
- [ ] Planning patterns documented
- [ ] Recovery patterns documented

---

## 7. Phase 4: Tier 4 Scientific Reasoning

**Goal:** Demonstrate genuine scientific capability

**Duration:** 2-4 weeks

### Tier 4 Benchmarks

| ID | Name | Type |
|----|------|------|
| T4-001 | Rahman 1964 | Paper reproduction |
| T4-002 | TIP4P 1983 | Paper reproduction |
| T4-003 | MACE Validation | Critical evaluation |
| T4-004 | Anomaly Investigation | Scientific debugging |
| T4-005 | MLIP Softening 2025 | Recent paper |
| T4-006 | Matbench Discovery | Benchmark analysis |

### Step 4.1: Paper Reproduction Track

For T4-001, T4-002, T4-005:

```markdown
# Add to CLAUDE.md:
## Paper Reproduction Workflow

1. **Find the Paper**
   - Search Semantic Scholar
   - Get full text if possible
   - Note DOI for citation

2. **Extract Methodology**
   - System: size, composition
   - Conditions: T, P, density
   - Force field: all parameters
   - Methods: integration, thermostat

3. **Note What's NOT in Paper**
   - Assumed knowledge
   - "Standard" values
   - Implementation details

4. **Reproduce with Modern Tools**
   - May need to adapt (better timestep, etc.)
   - Document any deviations
   - Justify choices

5. **Compare Results**
   - Quantitative comparison
   - Discuss sources of difference
   - Assess agreement quality
```

### Step 4.2: Scientific Reasoning Track

For T4-003, T4-004:

```markdown
# Add to CLAUDE.md:
## Scientific Evaluation Workflow

When asked to evaluate or debug:

1. **Understand the Question**
   - What exactly is being asked?
   - What would a good answer look like?

2. **Gather Evidence**
   - Search literature
   - Find data/benchmarks
   - Note what's known vs unknown

3. **Form Hypotheses**
   - What could explain observations?
   - What are alternative explanations?
   - What would distinguish them?

4. **Test Hypotheses**
   - Design diagnostic tests
   - Run calculations if needed
   - Compare results to predictions

5. **Draw Conclusions**
   - What does evidence support?
   - What remains uncertain?
   - What would change your conclusion?
```

### Step 4.3: Evaluation Approach

Tier 4 requires different grading:

```python
# Not just: did it get the right number?
# But: did it reason correctly?

evaluation_criteria = {
    "methodology_sound": "Did it use appropriate approach?",
    "evidence_gathered": "Did it find relevant information?",
    "reasoning_valid": "Does conclusion follow from evidence?",
    "uncertainty_acknowledged": "Does it know what it doesn't know?",
    "communication_clear": "Can a human understand and verify?"
}
```

### Step 4.4: Expert Review

For Tier 4, automated grading is insufficient:

```markdown
## Expert Review Checklist

For each Tier 4 result:

- [ ] Methodology is scientifically sound
- [ ] Parameters have valid sources
- [ ] Analysis is correct
- [ ] Conclusions are justified
- [ ] Limitations are acknowledged
- [ ] A domain expert would find this credible
```

### Phase 4 Exit Criteria

- [ ] At least 2 paper reproductions successful
- [ ] At least 1 scientific reasoning task shows good judgment
- [ ] Expert review indicates "credible work"
- [ ] Clear path to improvement for remaining tasks

---

## 8. Phase 5: Discovery Readiness

**Goal:** Ready for real scientific contribution

**Duration:** Ongoing

### Step 5.1: Validate at Scale

Run systematic tests:

```bash
# Run each benchmark 3x to check consistency
for bench in BENCH-T1-001 BENCH-T1-002 ...; do
  for run in 1 2 3; do
    python3 benchmarks/evaluation/runner.py $bench
  done
done

# Calculate consistency rate
# (Same result on N runs)
```

### Step 5.2: Measure Efficiency

Track resources:

```python
metrics = {
    "tokens_per_benchmark": [],
    "time_per_benchmark": [],
    "retries_per_benchmark": [],
    "human_interventions": [],
}
```

Goal: Decreasing resource usage over time.

### Step 5.3: Discovery Pilot

Run first real discovery task:

**Pilot Project:** MLIP Failure Analysis
```
1. Get 100 structures from Materials Project
2. Calculate energies with MACE
3. Compare to MP DFT values
4. Identify outliers
5. Analyze patterns
6. Document findings
```

This is real science - the results don't exist yet.

### Step 5.4: Human-in-Loop for Discovery

For discovery, the loop becomes:

```
Agent proposes → Human reviews → Agent refines → Human validates
       │                                              │
       └──────── Real scientific contribution ◀───────┘
```

### Phase 5 Exit Criteria

- [ ] Consistent pass rates across runs
- [ ] Efficient resource usage
- [ ] Successful pilot project
- [ ] Process for discovery validated

---

## 9. Failure Diagnosis Guide

### Quick Reference

| Symptom | Likely Cause | Check | Fix |
|---------|--------------|-------|-----|
| "Can't find X" | Missing path | CLAUDE.md | Add path |
| "Permission denied" | Blocked command | settings.json | Add to allow |
| "Unknown command" | Wrong syntax | Skill | Add example |
| "Wrong answer" | Bad formula/units | Skill | Add formula |
| "Simulation crashed" | Bad input | Skill | Add validation |
| "Timeout" | Too slow | Skill | Add limits |
| "Gave up" | Didn't know how | Skill | Add workflow |

### Deep Diagnosis

For persistent failures:

1. **Reproduce manually**
   - Can YOU complete the task with the same tools?
   - If not, it's an infrastructure problem

2. **Check the transcript**
   - What did the agent actually try?
   - Where did reasoning go wrong?

3. **Compare to success**
   - What's different from passing benchmarks?
   - Is it missing specific knowledge?

4. **Simplify the task**
   - Can it do half the task?
   - Which half fails?

---

## 10. Success Metrics

### Quantitative Targets

| Phase | Metric | Target |
|-------|--------|--------|
| 0 | Infrastructure tests | 100% pass |
| 1 | Tier 1 pass rate | >95% |
| 2 | Tier 2 pass rate | >80% |
| 3 | Tier 3 milestone completion | >60% |
| 4 | Tier 4 expert review | "Credible" |
| 5 | Consistency (3-run) | >90% |
| 5 | Token efficiency | <20k/benchmark |

### Qualitative Indicators

**Good signs:**
- Failures are rare and edge cases
- Agent self-corrects on retry
- Reasoning is sound even when wrong
- Asks for help appropriately

**Bad signs:**
- Same failures repeatedly
- Bizarre approaches
- Doesn't learn from errors
- Never asks, or always asks

### The Ultimate Test

The system is ready when:

> A domain expert, reviewing the agent's work, says:
> "This is the quality I'd expect from a competent graduate student."

Not perfect. Not superhuman. But competent and trustworthy.

---

## Summary: The Full Roadmap

```
Week 1:
├── Day 1-2: Phase 0 (Infrastructure)
└── Day 3-7: Phase 1 (Tier 1 → >95%)

Week 2-3:
├── Phase 2 (Tier 2 → >80%)
└── Begin Phase 3

Week 4-6:
├── Phase 3 (Tier 3 → >60%)
└── Begin Phase 4

Week 7+:
├── Phase 4 (Tier 4 - Scientific Reasoning)
└── Phase 5 (Discovery Readiness)

Ongoing:
└── Discovery projects, continuous improvement
```

---

## Appendix: Commands Reference

```bash
# Infrastructure validation
./scripts/run_infrastructure_tests.sh

# Run specific benchmark
python3 benchmarks/evaluation/runner.py BENCH-T1-001

# Run all benchmarks in tier
python3 benchmarks/evaluation/runner.py --tier 1

# List all benchmarks
python3 benchmarks/evaluation/runner.py --list

# Grade a result
python3 benchmarks/evaluation/grader.py results/runs/BENCH-*.json

# View iteration log
cat benchmarks/results/ITERATION_LOG.md
```

---

## Appendix: Files to Edit

| File | When to Edit |
|------|--------------|
| `CLAUDE.md` | Missing paths, capabilities, domain knowledge |
| `.claude/settings.json` | Permission issues |
| `.claude/skills/*/SKILL.md` | Wrong approach, missing examples |
| `.claude/hooks/*.py` | Need earlier error catching |
| `scripts/*.py` | Need helper tools |

---

## Final Note

This plan is comprehensive but not rigid. The iteration loop is what matters:

1. Measure
2. Analyze
3. Fix (small)
4. Repeat

Every improvement teaches us something. The goal isn't to follow this plan perfectly - it's to systematically improve until the agent can do real science.

**Let's begin.**
