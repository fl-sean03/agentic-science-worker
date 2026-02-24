# ASW Capability Expansion Plan

**Created:** 2026-02-18
**Status:** In Progress
**Owner:** Claude Code Session
**Goal:** Increase ASW benchmark pass rate from 48% to 80%+ and enable "independent lab member" capabilities

---

## Executive Summary

This document outlines a phased approach to expanding the Agentic Science Worker's capabilities from reliable workflow execution (current state) to autonomous research (target state).

### Current State
- **Overall Pass Rate:** 50/104 (48%)
- **Tiers 1-6:** 100% (fundamentals solid)
- **Tiers 7-9:** 33-40% (autonomy struggling)
- **Tiers 10-16:** 0-29% (frontier/cognition weak)

### Target State
- **Overall Pass Rate:** 85/104 (80%+)
- **Behavioral Tiers (15-16):** 70%+
- **Robustness Tiers (13-14):** 60%+
- **Autonomy Tiers (7, 9):** 60%+

### Vision Alignment
Enable the agent to:
> "Take meeting transcripts, work independently for hours/days, produce results worth discussing at group meeting."

---

## Phase Overview

| Phase | Focus | Tiers | Current | Target | Duration |
|-------|-------|-------|---------|--------|----------|
| 1 | Consolidate | T15-T16 | 27% | 70% | 2-3 days |
| 2 | Robustness | T13-T14 | 0% | 60% | 1 week |
| 3 | Autonomy | T7, T9 | 37% | 60% | 2 weeks |
| 4 | Frontier | T10-T12 | 0% | 40% | 1+ month |

---

## Phase 1: CONSOLIDATE

### Objective
Fix agent cognition and scientific rigor issues. Make the agent think better before expanding what it can do.

### Benchmarks

#### Tier 15: Agent Cognition (14 benchmarks)
| ID | Name | Current | Notes |
|----|------|---------|-------|
| T15-001 | Approach Selection | ? | Choose between methods |
| T15-002 | Task Decomposition | ? | Break complex into steps |
| T15-003 | Plan Revision | 0% | **CRITICAL FAILURE** - fabrication |
| T15-004 | Self-Verification | 32% | Transcription errors |
| T15-005 | Meta-Learning | ? | Learn from task |
| T15-006 | Learning from Errors | 54% | Missing deliverables |
| T15-007 | Transfer Learning | ? | Apply across domains |
| T15-008 | Efficiency Optimization | ? | Improve over iterations |
| T15-009 | Novel Strategy | ? | Create new approaches |
| T15-010 | Reflection Quality | ? | Analyze own performance |
| T15-011 | Natural Validation | 100% | ✅ PASSING |
| T15-012 | Catch User Error | 92% | ✅ PASSING |
| T15-013 | Knowledge Boundaries | 93% | ✅ PASSING |
| T15-014 | ? | ? | Unknown |

#### Tier 16: Scientific Rigor (16 benchmarks)
| ID | Name | Current | Notes |
|----|------|---------|-------|
| T16-001 through T16-012 | Various | ? | Need to assess |
| T16-013 | Hidden Danger | 95% | ✅ PASSING |
| T16-014 | Natural Uncertainty | 93% | ✅ PASSING |
| T16-015 | Natural Citation | 73% | ⚠️ CLOSE |
| T16-016 | Conflicting Sources | 78% | ⚠️ CLOSE |

### Known Failure Modes (Already Fixed)

| Failure Mode | Benchmark | Fix Applied | Location |
|--------------|-----------|-------------|----------|
| Narrative without action | T15-003 | "CRITICAL: Narrative ≠ Execution" section | AGENTS.md:275-295 |
| Transcription errors | T15-004 | "VERIFY TRANSCRIPTION" section | AGENTS.md:334-349 |
| Missing deliverables | T15-006 | Pre-completion checklist | AGENTS.md:257-270 |

### Execution Steps

```
Step 1.1: Baseline Assessment
├── Run ALL T15 benchmarks (14 tests)
├── Run ALL T16 benchmarks (16 tests)
├── Document current scores in tracking spreadsheet
└── Identify new failure patterns

Step 1.2: Failure Analysis
├── For each failing benchmark:
│   ├── Read grading_audit.json for reasoning
│   ├── Read transcript.json for agent behavior
│   ├── Categorize failure mode
│   └── Document in FAILURE_MODE_ANALYSIS.md
└── Prioritize by frequency and severity

Step 1.3: Targeted Fixes
├── Update AGENTS.md with new guidance
├── Add examples to examples/ directory
├── Update relevant skill files
└── Document each fix with rationale

Step 1.4: Validation
├── Re-run failing benchmarks
├── Verify fixes don't break passing benchmarks
├── Update tracking with new scores
└── Iterate until 70% target reached
```

### Files to Modify

| File | Purpose | Changes |
|------|---------|---------|
| `AGENTS.md` | Core principles | Add guidance for new failure modes |
| `examples/workflows/` | Positive examples | Add examples for failing patterns |
| `examples/anti-patterns/` | What to avoid | Document failure modes |
| `skills/*/SKILL.md` | Skill-specific | Add domain-specific guidance |

### Success Criteria
- [ ] T15 pass rate ≥ 70% (10/14)
- [ ] T16 pass rate ≥ 70% (11/16)
- [ ] No regressions in T15-011, T15-012, T15-013
- [ ] No regressions in T16-013, T16-014, T16-015, T16-016
- [ ] All failure modes documented with fixes

### Checkpoint
When Phase 1 is complete, update this document with:
- Final T15/T16 scores
- List of all fixes applied
- Remaining issues for Phase 2

---

## Phase 2: ROBUSTNESS

### Objective
Make the agent handle edge cases, unexpected situations, and resource constraints gracefully.

### Benchmarks

#### Tier 13: Robustness (8 benchmarks)
| ID | Name | Focus |
|----|------|-------|
| T13-001 | Limited Tools | Work with reduced capabilities |
| T13-002 | Sparse Instructions | Handle vague/minimal input |
| T13-003 | Missing Resources | Cope when files/data missing |
| T13-004 | Error Recovery | Recover from failures |
| T13-005 | Blockers | Handle unexpected obstacles |
| T13-006 | Contradictory Input | Resolve conflicts |
| T13-007 | Partial Information | Work with incomplete data |
| T13-008 | Timeout Handling | Manage long-running tasks |

#### Tier 14: Compute Decisions (5 benchmarks)
| ID | Name | Focus |
|----|------|-------|
| T14-001 | Simple Choice | Local vs HPC |
| T14-002 | Queue Aware | Factor in wait times |
| T14-003 | Cost Optimized | Minimize compute cost |
| T14-004 | Multi-Backend | Choose among options |
| T14-005 | Failure Fallback | Recover when resource fails |

### Execution Steps

```
Step 2.1: Run T13 Benchmarks
├── Execute all 8 T13 tests
├── Document failure patterns
└── Categorize by type (tools, resources, errors, etc.)

Step 2.2: Run T14 Benchmarks
├── Execute all 5 T14 tests
├── Document decision patterns
└── Note where agent makes wrong choices

Step 2.3: Robustness Fixes
├── Add error recovery patterns to AGENTS.md
├── Add graceful degradation guidance
├── Update hpc-cluster skill for queue awareness
├── Update vast-cloud skill for cost awareness
└── Add "when things go wrong" section

Step 2.4: Validation
├── Re-run T13 and T14
├── Verify no regressions in T1-T6, T15-T16
└── Document final scores
```

### Expected Challenges
1. **Tool limitations** - Agent may not know what to do without usual tools
2. **Ambiguity handling** - Need to make reasonable assumptions
3. **Cost/queue tradeoffs** - Need to teach decision framework

### Files to Modify

| File | Changes |
|------|---------|
| `AGENTS.md` | Add "Handling Difficult Situations" expansion |
| `skills/hpc-cluster/SKILL.md` | Queue awareness, fallback strategies |
| `skills/vast-cloud/SKILL.md` | Cost calculation, when to use |
| `examples/patterns/error-recovery.md` | Expand with more scenarios |
| `examples/patterns/graceful-degradation.md` | New file |

### Success Criteria
- [ ] T13 pass rate ≥ 60% (5/8)
- [ ] T14 pass rate ≥ 60% (3/5)
- [ ] No regressions in earlier tiers
- [ ] Clear decision framework for compute resources

---

## Phase 3: AUTONOMY

### Objective
Enable multi-hour/multi-day autonomous research with planning, tracking, and adaptation.

### Benchmarks

#### Tier 7: Research Campaigns (3 benchmarks)
| ID | Name | Focus |
|----|------|-------|
| T7-001 | Multi-Day Study | Extended research project |
| T7-002 | Error Recovery Campaign | Handle failures over time |
| T7-003 | Collaborative Research | Work with checkpoints |

#### Tier 9: Autonomous Research (5 benchmarks)
| ID | Name | Focus |
|----|------|-------|
| T9-001 | Active Learning | Self-directed exploration |
| T9-002 | Multi-Fidelity | Mix methods appropriately |
| T9-003 | Closed-Loop | Iterate on results |
| T9-004 | Self-Directed | No guidance given |
| T9-005 | Long Horizon | Plan far ahead |

### New Capabilities Required

1. **Progress Tracking**
   - Explicit todo lists / research journal
   - Checkpoint creation
   - State persistence

2. **Planning**
   - Break multi-day work into sessions
   - Prioritize tasks
   - Adapt plan based on results

3. **Memory**
   - Remember what worked/failed
   - Transfer learning across sessions
   - Build on previous results

### Implementation Approach

```
Step 3.1: Add Research Journal Pattern
├── Create examples/workflows/research-journal.md
├── Add guidance to AGENTS.md for long tasks
└── Test with T7-001

Step 3.2: Add Checkpointing
├── Define checkpoint format
├── Add to AGENTS.md
└── Test with T7-003

Step 3.3: Add Active Learning Pattern
├── Create examples/workflows/active-learning.md
├── Add exploration vs exploitation guidance
└── Test with T9-001

Step 3.4: Run Full T7 and T9
├── Execute all 8 benchmarks
├── Analyze failures
├── Iterate on fixes
└── Document patterns
```

### Architectural Considerations

**Option A: Prompt-Only (Preferred)**
- All guidance in AGENTS.md and examples
- No code changes
- Relies on agent following instructions

**Option B: Light Infrastructure**
- Add checkpointing scripts
- Add progress tracking tools
- Still prompt-driven

**Option C: Full Infrastructure**
- Episodic memory database
- State management system
- Significant engineering

**Recommendation:** Start with Option A, move to B if needed.

### Success Criteria
- [ ] T7 pass rate ≥ 60% (2/3)
- [ ] T9 pass rate ≥ 60% (3/5)
- [ ] Agent can work 2+ hours autonomously
- [ ] Clear research journal maintained

---

## Phase 4: FRONTIER

### Objective
Enable novel discovery and hypothesis generation — actual scientific contribution.

### Benchmarks

#### Tier 10: Frontier Research (3 benchmarks)
| ID | Name | Focus |
|----|------|-------|
| T10-001 | Material Discovery | Find new materials |
| T10-002 | Cross-Modal Reasoning | Connect different data types |
| T10-003 | Open Questions | Address unsolved problems |

#### Tier 11: HPC+ML Hybrid (7 benchmarks)
| ID | Name | Focus |
|----|------|-------|
| T11-001 | Million-Atom MLIP | Large-scale ML simulation |
| T11-002+ | Various | Advanced hybrid workflows |

#### Tier 12: Theory Synthesis (3 benchmarks)
| ID | Name | Focus |
|----|------|-------|
| T12-001 | Hypothesis Generation | Generate from literature |
| T12-002 | Gap Discovery | Find research gaps |
| T12-003 | Consensus Extraction | Synthesize methodology |

### Prerequisites
- Phase 1-3 complete
- Theorizer integration validated
- HPC access confirmed

### Execution Steps

```
Step 4.1: Theory Synthesis First (T12)
├── Verify Theorizer skill works
├── Run T12-001 (hypothesis generation)
├── Analyze quality of hypotheses
└── Iterate on prompting

Step 4.2: Frontier Research (T10)
├── Attempt T10-001 (material discovery)
├── This is genuinely hard - expect failures
├── Document what agent does well/poorly
└── May require multiple iterations

Step 4.3: Scale-Out (T11)
├── Requires HPC access
├── Test million-atom workflows
└── Validate performance at scale
```

### Success Criteria
- [ ] T12 pass rate ≥ 40% (1-2/3)
- [ ] T10 at least attempted with documented results
- [ ] Agent generates at least one novel, testable hypothesis
- [ ] Clear documentation of frontier capabilities and limitations

---

## Execution Tracking

### Progress Log

| Date | Phase | Action | Result | Next Step |
|------|-------|--------|--------|-----------|
| 2026-02-18 | 0 | Created plan | Plan document complete | Start Phase 1 |
| 2026-02-18 | 1 | Gathered baseline | T15: 36%, T16: 50% | Run failing benchmarks |
| 2026-02-18 | 1 | Started T15-003,004,006 | Running in parallel | Wait for results |
| 2026-02-18 | 1 | Fixed harness context | AGENTS.md now in workspace | Re-run benchmarks |
| 2026-02-18 | 1 | FM-004 fix applied | T15-003: 0→3→8 | Discovered FM-005,006 |
| 2026-02-18 | 1 | FM-005,006 fixes applied | Error recovery, plan docs | Running T15-003 |
| 2026-02-18 | 1 | **T15-003 PASSED** | Score: 84/100 (0→84) | Validate other benchmarks |
| | | | | |

### Benchmark Score Tracking

| Tier | Baseline | After P1 | After P2 | After P3 | After P4 |
|------|----------|----------|----------|----------|----------|
| T13 | 0% | — | | | |
| T14 | 0% | — | | | |
| T15 | 29% | | | | |
| T16 | 25% | | | | |
| T7 | 33% | — | — | | |
| T9 | 40% | — | — | | |
| T10 | 0% | — | — | — | |
| T11 | 0% | — | — | — | |
| T12 | 0% | — | — | — | |

### Files Modified Tracking

| File | Phase | Change | Rationale |
|------|-------|--------|-----------|
| AGENTS.md | 1 | Added "Narrative ≠ Execution" | Fix fabrication |
| AGENTS.md | 1 | Added transcription verification | Fix T15-004 |
| AGENTS.md | 1 | Added pre-completion checklist | Fix T15-006 |
| examples/anti-patterns/narrative-without-action.md | 1 | Created | Document failure mode |
| benchmarks/evaluation/audit.py | 1 | Fixed truncation | Full reasoning visible |
| | | | |

---

## Recovery Instructions

### If Context Resets

1. **Read this document first:** `/research/ASW_CAPABILITY_EXPANSION_PLAN.md`

2. **Check progress log** (above) for last completed action

3. **Check benchmark results:**
   ```bash
   ls -lt benchmarks/results/runs/ | head -20
   ```

4. **Read latest failure analysis:** `/research/FAILURE_MODE_ANALYSIS.md`

5. **Resume from last checkpoint in progress log**

### Key Files

| File | Purpose |
|------|---------|
| `research/ASW_CAPABILITY_EXPANSION_PLAN.md` | This plan (master document) |
| `research/FAILURE_MODE_ANALYSIS.md` | Documented failure modes |
| `research/CONTEXT_ARCHITECTURE.md` | Context loading design |
| `AGENTS.md` | Core agent guidance |
| `ROADMAP.md` | Overall project roadmap |
| `benchmarks/README.md` | Benchmark documentation |

### Commands Reference

```bash
# Run single benchmark
cd benchmarks/evaluation
python harness.py BENCH-T15-003

# Run full tier
python harness.py --tier 15

# Check latest results
ls -lt ../results/runs/ | head -10

# Read grading audit
cat ../results/runs/BENCH-T15-003-*/grading_audit.md
```

---

## Appendix A: Benchmark Inventory

### Tier 13: Robustness (8)
- BENCH-T13-001 through BENCH-T13-008

### Tier 14: Compute Decisions (5)
- BENCH-T14-001 through BENCH-T14-005

### Tier 15: Agent Cognition (14)
- BENCH-T15-001 through BENCH-T15-014

### Tier 16: Scientific Rigor (16)
- BENCH-T16-001 through BENCH-T16-016

### Tier 7: Research Campaigns (3)
- BENCH-T7-001 through BENCH-T7-003

### Tier 9: Autonomous Research (5)
- BENCH-T9-001 through BENCH-T9-005

### Tier 10: Frontier Research (3)
- BENCH-T10-001 through BENCH-T10-003

### Tier 11: HPC+ML Hybrid (7)
- BENCH-T11-001 through BENCH-T11-007

### Tier 12: Theory Synthesis (3)
- BENCH-T12-001 through BENCH-T12-003

---

## Appendix B: Decision Log

| Decision | Rationale | Date |
|----------|-----------|------|
| Phase order: Consolidate → Robustness → Autonomy → Frontier | Build reliability before capability | 2026-02-18 |
| Prompt-only fixes first | Lower risk, faster iteration | 2026-02-18 |
| Target 70% not 100% | Diminishing returns, some benchmarks may be flawed | 2026-02-18 |
| Document everything | Enable recovery from context resets | 2026-02-18 |

---

*Last Updated: 2026-02-18*
*Next Action: Begin Phase 1 - Run baseline T15/T16 benchmarks*
