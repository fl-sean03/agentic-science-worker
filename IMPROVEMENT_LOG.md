# Benchmarking Improvement Log

**Campaign Start**: 2026-01-18
**Purpose**: Track all fixes and improvements made during benchmark validation

---

## Summary Statistics

| Metric | Value |
|--------|-------|
| Total Fixes Applied | 5 |
| Benchmarks Fixed | 4 (T5-006, T6-003, T6-004, T7-002) |
| Proactive Fixes Applied | 1 (T6-005) |
| Skills Updated | 1 |
| CLAUDE.md Updates | 1 |
| Benchmark Prompts Fixed | 5 |

### Benchmark Results Summary

| Benchmark | Score | Status | Notes |
|-----------|-------|--------|-------|
| T8-001 | 91/100 | ✅ PASSED | MLIP setup |
| T5-001 | 94/100 | ✅ PASSED | HPC connection |
| T8-002 | 76/100 | ✅ PASSED | MLIP vs classical |
| T8-003 | 91/100 | ✅ PASSED | Phonon calculation |
| T8-004 | 82/100 | ✅ PASSED | Stability screening |
| T5-002 | 88/100 | ✅ PASSED | HPC migration |
| T5-004 | 88/100 | ✅ PASSED | HPC debugging |
| T5-006 | 95/100 | ✅ PASSED | Async job (after fix) |
| T5-003 | 90/100 | ✅ PASSED | Queue-aware partition |
| T5-005 | 96/100 | ✅ PASSED | GPU job submission |
| T5-007 | 81/100 | ✅ PASSED | Multi-job parameter sweep |
| T9-005 | 82/100 | ✅ PASSED | Debug MLIP failure |
| T8-005 | 92/100 | ✅ PASSED | MLIP MD (retry success) |
| T8-007 | 61/100 | ✅ PASSED | Matbench (after CLAUDE.md fix) |
| T9-004 | 65/100 | ✅ PASSED | Literature-to-Simulation |
| T6-001 | 68/100 | ✅ PASSED | System size convergence |
| T6-002 | 75/100 | ✅ PASSED | Long-timescale diffusion |
| T6-003 | 86/100 | ✅ PASSED | Large-scale phonons (after fix) |
| T6-004 | 75/100 | ✅ PASSED | High-throughput screening (after fix) |
| T6-005 | 81/100 | ✅ PASSED | Melting temperature (proactive fix) |
| T7-002 | 85/100 | ✅ PASSED | Autonomous error recovery (after fix) |

---

## Improvement Entries

<!-- Template for each improvement:

### [Date] - BENCH-XXX Fix #N

**Benchmark**: BENCH-XXX-NNN
**Run ID**: YYYYMMDD-HHMMSS
**Initial Score**: XX/100
**Status**: Failed

**Problem Observed**:
[What went wrong - be specific]

**Root Cause Analysis**:
[Why it happened]

**Category**: [Prompt Unclear | Missing Knowledge | Wrong Tool Usage | Scientific Error | Infrastructure Issue]

**Fix Applied**:
[What was changed]

**File(s) Modified**:
- `path/to/file.md` - [description of change]

**Result After Fix**:
- New Score: XX/100
- Status: [Passed | Still Failed]

**Lessons Learned**:
[What we learned that might apply to other benchmarks]

---

-->

## Phase 1: Infrastructure Validation

### 2026-01-18 - BENCH-T8-001 - Universal Potential Setup

**Benchmark**: BENCH-T8-001
**Run ID**: 20260118-112614
**Score**: 91/100
**Status**: PASSED

**Observations**:
- MACE-MP-0 works correctly on both CPU and GPU
- M3GNet requires DGL backend which is not installed
- CHGNet has float64/float32 dtype mismatch issues

**Agent Workarounds** (no fix needed, agent adapted):
- Used TensorNet-MatPES-PBE (PyG backend) instead of M3GNet
- Set `torch.set_default_dtype(torch.float32)` for CHGNet

**Recommendation**:
- Consider installing DGL for full M3GNet support (optional)
- Agent successfully adapted, no immediate action required

---

### 2026-01-18 - BENCH-T5-001 - HPC Connection Validation

**Benchmark**: BENCH-T5-001
**Run ID**: 20260118-112614
**Score**: 94/100
**Status**: PASSED

**Observations**:
- SSH connection to CURC Alpine working
- Test job submitted (ID: 22897817) and completed successfully
- Scratch space: ~9.3 TB available
- LAMMPS installations found in /curc/sw/install/lammps/

**No Issues** - HPC infrastructure fully operational

---

---

## Phase 2: Core ML Capabilities

### 2026-01-18 - BENCH-T8-002 - MLIP vs Classical Comparison

**Benchmark**: BENCH-T8-002
**Run ID**: 20260118-113509
**Score**: 76/100
**Status**: PASSED (threshold: 60)

**What Went Well**:
- EAM calculations excellent (95/100) with proper methodology and citations
- Comprehensive comparison report with experimental references
- Scientific analysis was solid (85/100)

**Weaknesses Identified**:
- M3GNet produced garbage values (C11=27499 GPa) - not properly diagnosed
- No visualization plot created despite being expected
- MLIP calculations scored 65/100 due to M3GNet issues

**Root Cause Analysis**:
- M3GNet has compatibility issues with current matgl version
- Agent didn't have guidance on validating MLIP output sanity

**Potential Improvement** (Optional - benchmark passed):
- Add to MLIP skill: "Always validate MLIP results against known values"
- Add sanity check: "Elastic constants should be 1-500 GPa for most materials"

**Decision**: Proceed (score above threshold), but note for future skill improvement

---

### 2026-01-18 - BENCH-T8-003 - Phonon Calculation with MLIPs

**Benchmark**: BENCH-T8-003
**Run ID**: 20260118-121703
**Score**: 91/100
**Status**: PASSED (threshold: 60)

**What Went Well**:
- Phonon methodology excellent (correct supercell, phonopy integration)
- Dispersion calculation correct with proper high-symmetry path
- Error quantification comprehensive (18.9% mean softening)
- Critical analysis outstanding - identified non-uniform error pattern

**Key Scientific Findings**:
- Γ optical: 384 cm⁻¹ vs 520 cm⁻¹ experimental = 26% softening
- Acoustic modes: ~14% softening
- Optical modes: ~24% softening
- Agent correctly noted this exceeds the commonly cited "~15%"

**Agent Strengths Demonstrated**:
- Deep scientific understanding of MLIP limitations
- Comprehensive report with practical recommendations
- Proper literature citations (Nilsson & Nelin 1972)
- Mode-dependent error analysis

**Decision**: Proceed - excellent scientific work, no fixes needed

---

---

## Phase 3: HPC Fundamentals

### 2026-01-18 - BENCH-T5-002 - Local-to-HPC Migration

**Benchmark**: BENCH-T5-002
**Run ID**: 20260118-113509
**Score**: 88/100
**Status**: PASSED (threshold: 60)

**What Went Well**:
- Local execution excellent (95/100)
- SLURM job script quality good (90/100)
- File transfer handled correctly (95/100)
- HPC execution successful (90/100)
- Agent handled KIM-API dependency issue intelligently

**Weaknesses Identified**:
- Result verification scored 75/100 - results differed by more than 0.1% tolerance

**Root Cause**:
- Different LAMMPS versions/builds between local and HPC
- Minor numerical differences in floating point results

**Decision**: Proceed - excellent score, minor numerical tolerance issue

---

### 2026-01-18 - BENCH-T5-004 - HPC Job Debugging

**Benchmark**: BENCH-T5-004
**Run ID**: 20260118-121703
**Score**: 88/100
**Status**: PASSED (threshold: 60)

**What Went Well**:
- Error identification outstanding - found 7 distinct issues (benchmark expected ~3)
- Iterative debugging approach (4 job submissions to find working solution)
- Comprehensive debug report with HPC path reference table
- Job completed successfully with physically valid results

**Issues Agent Identified and Fixed**:
1. Missing QoS specification (CURC policy)
2. Generic "module load lammps" doesn't exist on CURC
3. mpirun not in PATH without Intel environment
4. GLIBC compatibility issues with newer LAMMPS (GLIBCXX_3.4.26)
5. KIM-API library not found
6. MPI task count mismatch
7. Input redirection vs -in flag

**Agent Solution**:
- Used older compatible LAMMPS version (29Sep21)
- Sourced Intel 2022 environment
- Set explicit LD_LIBRARY_PATH for all dependencies
- Changed mpirun to srun for SLURM integration

**Decision**: Proceed - excellent debugging demonstration, no fixes needed

---

### 2026-01-18 - BENCH-T5-006 - Async Job Management (FIX REQUIRED)

**Benchmark**: BENCH-T5-006
**Run IDs**: 20260118-123329 (failed), 20260118-124033 (failed), 20260118-124504 (failed), 20260118-124803 (passed)
**Initial Score**: 8/100, 8/100, 5/100
**Final Score**: 95/100 after fix
**Status**: PASSED (after 3 iterations)

**Problem Observed**:
- Agent completed queue analysis but terminated after ~40 seconds
- Zero files created in workspace
- Agent said "I'll pass this back to the main conversation"
- Agent treated task as "give recommendations" not "do the work"

**Root Cause Analysis**:
- Agent misinterpreted task scope
- Thought queue analysis was the complete task
- Did not understand it needed to create all deliverable files

**Category**: Prompt Unclear

**Fix Applied**:
Updated benchmark prompt to be extremely explicit:
1. Added "CRITICAL INSTRUCTIONS" header
2. Explicitly stated agent must CREATE ALL 5 FILES
3. Told agent to use Write tool specifically
4. Added workflow sequence with numbered steps
5. Told agent to verify all files exist before finishing
6. Encouraged use of TodoWrite for tracking

**File(s) Modified**:
- `benchmarks/tasks/tier5_hpc_fundamentals/BENCH-T5-006-async-job-management.yaml`

**Result After Fix**:
- New Score: 95/100
- Status: PASSED

**Lessons Learned**:
1. **Explicit file creation instructions are critical** for multi-deliverable tasks
2. **"Use Write tool" is more effective than "create files"**
3. **Numbered workflow steps help maintain task focus**
4. **Verify completion step prevents premature termination**

**Pattern Identified**:
When agent receives complex multi-step tasks, it may treat information-gathering
steps (like queue analysis) as the complete task. Fix by:
- Explicitly listing all deliverable files
- Specifying the exact tool to use (Write)
- Adding verification step at end

---

---

## Phase 4: Advanced ML Workflows

### 2026-01-18 - BENCH-T9-005 - Debug MLIP Failure for MgO

**Benchmark**: BENCH-T9-005
**Run ID**: 20260118-143541
**Score**: 82/100
**Status**: PASSED (threshold: 50)

**What Went Well**:
- Correctly identified root cause: wrong crystal structure (not MLIP limitation)
- Systematic 8-step investigation with multiple hypothesis testing
- Quantitative verification of fix (0.10 eV/atom final error vs 0.73 eV/atom original)
- Clear documentation with comprehensive diagnostic report

**Key Finding**:
The ~0.5 eV/atom error in CHGNet's MgO formation energy was caused by using incorrect
crystal structure - a 2-atom "primitive cell" with Mg-O distance 3.65 Å instead of proper
8-atom rock salt with Mg-O distance 2.11 Å.

**Weaknesses**:
- Did not follow expected directory structure (investigation/, diagnosis/, fix/)
- CSV output files not created as specified
- M3GNet import failed and was not debugged further

**Decision**: Passed - excellent scientific debugging, minor format issues

---

### 2026-01-18 - BENCH-T8-005 - MLIP-Accelerated MD (FAILED - Retry Needed)

**Benchmark**: BENCH-T8-005
**Run ID**: 20260118-143540
**Score**: 28/100
**Status**: FAILED (threshold: 60)

**Problem Observed**:
- Agent terminated after 98 minutes with "API Error: Connection error"
- Only equilibration (10 ps) completed, no production run (100 ps)
- No MSD analysis, no diffusion coefficient calculated
- No report generated

**Root Cause Analysis**:
- Long-running MD simulation exceeded API connection stability
- Agent was waiting for Python subprocess (run_md.py using 323% CPU)
- No checkpointing or interim results saved

**Category**: Infrastructure Issue (API timeout)

**What Was Correct**:
- Structure preparation excellent (85/100) - proper Li3PS4 from Materials Project
- MD script well-designed with correct CHGNet/ASE setup
- Good literature citations and expected values documented

**Fix Required**: None - re-run benchmark

**Retry Result (20260118-163756)**: 92/100 PASSED
- 50 ps MD at 600K completed successfully
- D = 4.52 × 10⁻⁵ cm²/s calculated
- Full MSD analysis with plots
- Comprehensive report generated

**Lessons Learned**:
1. Long simulations need checkpointing for partial results
2. Consider running production MD in smaller chunks
3. Generate interim reports as work progresses
4. Retry can succeed if issue was transient (API connection)

---

### 2026-01-18 - BENCH-T8-007 - Matbench Discovery Evaluation

**Benchmark**: BENCH-T8-007
**Run ID**: 20260118-163757
**Score**: 52/100
**Status**: FAILED (threshold: 60)

**Problem Observed**:
- F1 score 0.11-0.21 vs expected 0.5-0.85
- Agent used simple energy ranking instead of proper convex hull construction
- WBM dataset download failed, used Materials Project instead

**Root Cause Analysis**:
- Proper Matbench Discovery evaluation requires computing convex hull positions
- Simple energy per atom ranking doesn't capture compositional stability
- Agent understood the issue but couldn't implement proper methodology

**Category**: Scientific Method Issue (incomplete implementation)

**What Was Correct**:
- Good benchmark understanding and leaderboard citations
- Correct published MACE-MP-0 values (F1=0.76, DAF=4.2x)
- Transparent about limitations
- Comprehensive error analysis

**Potential Fix**:
- Add guidance about convex hull construction for stability prediction
- Consider adding pymatgen phase diagram tools to standard knowledge

**Lessons Learned**:
1. Stability prediction requires compositional analysis, not just energies
2. Convex hull methodology is essential for thermodynamic stability
3. Agent should validate methodology against expected performance ranges

---

### 2026-01-18 - BENCH-T9-004 - Literature-to-Simulation Reproduction

**Benchmark**: BENCH-T9-004
**Run ID**: 20260118-182257
**Score**: 65/100
**Status**: PASSED (threshold: 50)

**What Went Well**:
- Found and correctly cited target paper on MLIP phonons
- Extracted methodology (4x4x4 supercell, 0.01 Å displacement, Phonopy)
- Successfully ran MACE-MP-0 phonon calculation on silicon
- Confirmed systematic softening finding (26% underestimation of optical phonon)
- Comprehensive report with proper scientific reasoning

**Result Achieved**:
- Si optical phonon: 11.49 THz (MACE) vs 15.53 THz (DFT reference)
- 26% softening - consistent with paper's systematic softening claims

**Weaknesses** (from grader):
- Did not reproduce a SPECIFIC numbered result from the paper
- General demonstration of softening rather than exact value matching
- Missing expected directory structure (literature/, reproduction/)

**Decision**: Passed - good autonomous research skills demonstrated

---

## Phase 4 Summary

**Results**: 3/4 passed (75%)
- T9-005 (Debug MLIP): 82 - PASSED
- T8-005 (MLIP MD): 92 - PASSED (after retry)
- T9-004 (Literature repro): 65 - PASSED
- T8-007 (Matbench): 52 - FAILED (methodology issue)

**Fixes Applied**: 0 (T8-005 retry was infrastructure, not prompt issue)

**Key Learnings**:
1. Long simulations can fail due to API timeouts - retry is valid strategy
2. Complex benchmarks (Matbench) require specific methodology knowledge
3. Agent shows strong scientific reasoning but sometimes misses exact requirements

---

### 2026-01-18 - CLAUDE.md Update: Research-First Methodology

**Purpose**: Address T8-007 failure pattern where agent used known-incorrect methodology

**Root Cause Analysis**:
The agent understood WHAT to do (convex hull) but not HOW. Instead of researching
the implementation, it fell back to a simplified approach it knew was wrong, then
documented why the results were wrong instead of fixing them.

**Changes Made to CLAUDE.md**:

1. **Strengthened "When Something Seems Wrong"**:
   - Added step 5: "Assume YOUR methodology is wrong first"
   - Added step 6: "Iterate until resolved"
   - Added critical warning: Do not submit results 5x off from published values
   - Removed "document discrepancy" as an acceptable endpoint

2. **Added "When You Don't Know How to Implement Something"**:
   - Research methodology first (search, docs, papers, GitHub)
   - Validate on simple cases before scaling
   - Understand before implementing
   - Explicit prohibition on using known-incorrect approaches

3. **Added "Methods and Implementation" to Finding What You Need**:
   - Library documentation
   - Web search patterns
   - Methods sections of papers
   - GitHub examples

4. **Strengthened "The Mindset"**:
   - Added "Research what you don't know"
   - Added "Iterate until correct"
   - Added explicit list: research it, iterate, fix methodology, never submit wrong results

**Philosophy**: These are general behavioral principles, not specific knowledge.
They apply to any analysis the agent doesn't know how to implement.

**Retry Result (20260118-191754)**: 61/100 PASSED

The fix worked! Key improvements:
- Agent researched proper methodology (formation energies, elemental references)
- F1 improved from 0.11 to 0.47 (4x better)
- Formation energy MAE: 0.156 eV/atom (excellent)
- DFT correlation: 0.97 (excellent)
- DAF: 1.82x (actually accelerates discovery now)

The agent still didn't implement full convex hull, but the methodology improvement
was substantial. The CLAUDE.md changes successfully guided better behavior.

---

## Phase 4 Final Summary (After Fixes)

**Results**: 4/4 passed (100%)
- T9-005 (Debug MLIP): 82 - PASSED
- T8-005 (MLIP MD): 92 - PASSED (after retry)
- T9-004 (Literature repro): 65 - PASSED
- T8-007 (Matbench): 61 - PASSED (after CLAUDE.md fix)

**Fixes Applied**: 1 (CLAUDE.md research-first methodology)
**Key Validation**: General guidance changes improved agent behavior

---

### 2026-01-18 - Data Analysis Skill Update: Methodology Section

**Purpose**: Apply same research-first methodology principles to data-analysis skill

**Changes Made**:
Added "Analysis Methodology" section with:
1. **Before Implementing Analysis**: Know what you're measuring, research unfamiliar methods, understand physics
2. **Validation**: Test on known systems, check literature, verify convergence
3. **When Results Seem Wrong**: Check implementation, check input data, research alternatives, iterate

**File Modified**: `.claude/skills/data-analysis/SKILL.md`

**Rationale**: The skill was pure code templates with no methodology guidance.
This aligns with the successful CLAUDE.md pattern - teach principles, not just provide tools.

---

## Phase 5: HPC-Scale Research

### 2026-01-18 - BENCH-T6-001 - System Size Convergence

**Benchmark**: BENCH-T6-001
**Run ID**: 20260118-194444
**Score**: 68/100
**Status**: PASSED (threshold: 55)

**No Issues** - Benchmark passed on first attempt.

---

### 2026-01-18 - BENCH-T6-002 - Long-Timescale Diffusion

**Benchmark**: BENCH-T6-002
**Run ID**: 20260118-194444
**Score**: 75/100
**Status**: PASSED (threshold: 55)

**No Issues** - Benchmark passed on first attempt.

---

### 2026-01-19 - BENCH-T6-003 - Large-Scale Phonons (FIX REQUIRED)

**Benchmark**: BENCH-T6-003
**Run ID**: 20260118-194950
**Initial Score**: 10/100
**Status**: FAILED (threshold: 55)

**Problem Observed**:
- Agent completed only Step 1 (literature research) and partial Step 2 (structure setup)
- No supercell created despite explicit requirement
- No displacement files, no HPC jobs, no phonon analysis
- Same pattern as T5-006 - agent treated research as complete task

**Root Cause Analysis**:
- Agent misinterpreted task scope despite 7 explicit steps
- Returned after basic setup without completing core workflow

**Category**: Prompt Unclear (same pattern as T5-006)

**Fix Applied**:
Updated benchmark prompt with same pattern as successful T5-006 fix:
1. Added "CRITICAL INSTRUCTIONS - READ CAREFULLY" header
2. Explicit warning: "Do NOT stop after literature research - that is only Step 1 of 7"
3. TodoWrite checklist of all 7 steps
4. Added "BEFORE FINISHING - VERIFY ALL DELIVERABLES EXIST" checklist
5. Explicit instruction: "If any are missing, GO BACK and complete them"

**File(s) Modified**:
- `benchmarks/tasks/tier6_hpc_scale/BENCH-T6-003-large-scale-phonons.yaml`

**Result After Fix**:
- Run 1 (20260119-080501): 21/100 - Still failed (better setup but stopped after Step 2)
- Run 2 (20260119-080557): **86/100 - PASSED** ✅

**Detailed Score Comparison**:
| Category | Original | Run 1 | Run 2 |
|----------|----------|-------|-------|
| System setup | 40 | 85 | 95 |
| Displacement generation | 0 | 0 | 95 |
| Parallel execution | 0 | 0 | 80 |
| Phonon analysis | 0 | 0 | 85 |
| Scientific quality | 30 | 70 | 75 |
| **TOTAL** | **10** | **21** | **86** |

**Key Achievements**:
- Agent created 1,296 displacement files
- Generated complete phonon dispersion and DOS
- Wrote comprehensive report with experimental comparison
- Created both HPC SLURM script and local execution option

**Lessons Learned**:
1. Complex multi-step HPC benchmarks need same explicit structure as T5-006
2. "Step 1, Step 2..." format is not sufficient - need CRITICAL header
3. Verification checklist at end prevents premature termination

**Pattern Confirmed**:
This is now the second occurrence of the "stops after research" pattern.
Adding to Systematic Patterns table.

---

### 2026-01-19 - BENCH-T6-004 - High-Throughput Screening (FIX REQUIRED)

**Benchmark**: BENCH-T6-004
**Run ID**: 20260119-082128
**Initial Score**: 15/100
**Status**: FAILED (threshold: 55)

**Problem Observed**:
- Same "stops after research" pattern as T5-006 and T6-003
- Agent completed literature research and partial setup but didn't execute screening workflow
- No LAMMPS calculations performed, no ranking generated

**Root Cause Analysis**:
- Agent treated information gathering as complete task
- Third occurrence of same pattern

**Category**: Prompt Unclear (same systematic pattern)

**Fix Applied**:
Same pattern as T5-006/T6-003:
1. Added "CRITICAL INSTRUCTIONS - READ CAREFULLY" header
2. Explicit warning not to stop after research
3. TodoWrite checklist of all 7 steps
4. Verification checklist at end

**File(s) Modified**:
- `benchmarks/tasks/tier6_hpc_scale/BENCH-T6-004-high-throughput-screening.yaml`

**Result After Fix**:
- New Score: 75/100
- Status: PASSED ✅

**Execution Details**:
- Agent screened 10 FCC metals (Pd, Pt, Ni, Cu, Ag, Au, Rh, Ir, Al, Pb)
- Generated 110 LAMMPS input files programmatically
- Correctly identified Pt, Pd, Ir as best HER catalysts
- Recognized limitation: only Ni and Pd have validated M-H potentials

**Pattern Confirmed**: Third occurrence of "stops after research" pattern

---

### 2026-01-19 - BENCH-T6-005 - Melting Temperature (PROACTIVE FIX)

**Benchmark**: BENCH-T6-005
**Run ID**: 20260119-084153
**Score**: 81/100
**Status**: PASSED (first run)

**Proactive Fix Applied**:
Applied same CRITICAL INSTRUCTIONS pattern BEFORE running benchmark based on
pattern identified in T5-006, T6-003, T6-004.

**Result**:
- Benchmark passed on first attempt
- Agent executed complete workflow autonomously

**Scientific Quality**:
- Calculated Tm = 932.6 K vs experimental 933 K (0.04% error!)
- Proper two-phase coexistence method with 16,000 atoms
- 6 temperature simulations (880-960 K)
- Linear interpolation to find melting point
- Comprehensive report with proper citations

**Grading Deductions**:
- Used local GPU instead of HPC cluster (expected for Tier-6) - scored 65/100 on HPC execution
- 200 ps production runs instead of suggested 500+ ps

**Lessons Learned**:
1. Proactive application of known fix patterns works!
2. Agent chose efficiency (local GPU) over expected method (HPC)
3. Plot display issue: agent used `plt.show()` which popped up windows

**Minor Issue Noted**:
Agent's analysis script called `plt.show()` which displayed plots interactively.
For benchmark scenarios, should use `matplotlib.use('Agg')` or avoid `plt.show()`.

---

### 2026-01-19 - BENCH-T7-002 - Autonomous Error Recovery (FIX REQUIRED)

**Benchmark**: BENCH-T7-002
**Run IDs**: 20260119-091802 (failed), 20260119-092435 (passed)
**Initial Score**: 49/100
**Final Score**: 85/100
**Status**: PASSED (after fix)

**Problem Observed**:
- First run: Agent executed locally (local GPU) instead of HPC
- Only encountered 1 error (atom selection) instead of expected 2-7 HPC errors
- Benchmark tests HPC error recovery - local execution bypasses the test objective

**Root Cause Analysis**:
- Benchmark prompt mentioned HPC errors but didn't explicitly require HPC execution
- Agent optimized for efficiency by running locally

**Category**: Environment Requirement Not Explicit

**Fix Applied**:
Added explicit HPC requirement at top of prompt:
```yaml
**CRITICAL: HPC EXECUTION REQUIRED**

This benchmark tests your ability to handle HPC failures. You MUST:
1. Execute calculations on the HPC cluster (cu_alpine), NOT locally
2. Submit jobs via SLURM and handle real HPC failure modes
3. Document all errors in logs/error_log.md and logs/recovery_actions.md
4. Create SLURM job scripts in jobs/ directory

Running locally defeats the purpose of this benchmark.
```

Also added explicit output structure requirement.

**File(s) Modified**:
- `benchmarks/tasks/tier7_research_campaigns/BENCH-T7-002-autonomous-error-recovery.yaml`

**Result After Fix**:
- New Score: 85/100
- Status: PASSED ✅

**HPC Errors Handled**:
| Error | Type | Resolution |
|-------|------|------------|
| 1 | Missing QoS | Added `--qos=testing` to SLURM |
| 2 | Module not found | Sourced Intel setvars.sh directly |
| 3 | Missing libkim-api | Installed LAMMPS via conda-forge |
| 4 | Conda TOS | Pre-accepted TOS from login node |

**Scientific Result**:
- Ef = 1.272 eV (99.4% agreement with experimental ~1.28 eV)
- 158 turns, 35 minutes of execution

**Pattern Identified**:
New pattern: "Agent optimizes for efficiency, bypasses test objective"
- When a benchmark tests a specific execution environment (HPC), explicitly require it
- Add "CRITICAL" header with explicit environment requirements

---

## Phase 6: HPC + ML Integration

*Pending earlier phases*

---

## Phase 7: Frontier Challenges

*Pending earlier phases*

---

## Systematic Patterns Identified

| Pattern | Occurrences | Standard Fix |
|---------|-------------|--------------|
| Agent stops after research/setup step | T5-006, T6-003, T6-004, T6-005 (proactive) | Add "CRITICAL INSTRUCTIONS" header, explicit file checklist, TodoWrite step list, verification checklist at end |
| Agent optimizes for efficiency, bypasses test objective | T7-002 | Add "CRITICAL" header with explicit environment requirements (HPC, specific tools, etc.) |

---

## Files Modified During Campaign

| File | Times Modified | Last Modified |
|------|----------------|---------------|
| - | - | - |
