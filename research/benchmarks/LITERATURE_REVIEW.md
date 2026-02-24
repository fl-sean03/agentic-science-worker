# Agentic Benchmark Literature Review

**Focus:** Scientific AI Agents & Research Automation

---

## Overview

This document surveys the landscape of LLM agent benchmarks as of 2025, with particular focus on scientific research agents. The field has evolved rapidly, with most papers published in 2024-2025.

---

## Key Benchmarks

### 1. ScienceAgentBench (ICLR 2025)

**Source:** [OSU-NLP-Group/ScienceAgentBench](https://github.com/OSU-NLP-Group/ScienceAgentBench)

**Focus:** Data-driven scientific discovery

**Structure:**
- 102 tasks from 44 peer-reviewed papers
- 4 disciplines: bioinformatics, geoscience, chemoinformatics, cognitive neuroscience
- Output: Self-contained Python programs
- Validation: 9 subject matter experts

**Evaluation Metrics:**
- Generated code quality (static analysis)
- Execution success
- Scientific output validity (GPT-4o as visual judge)
- Resource costs

**Key Design Decisions:**
- Password-protected gold solutions (prevent contamination)
- Containerized evaluation harness
- 30-minute parallel evaluation for full suite
- OpenHands integration for standardized comparison

**Performance:** ~30% success rate with GPT-4

**What We Can Learn:**
- Subject matter expert validation is valuable
- Containerized evaluation improves reproducibility
- Unified output format simplifies evaluation

---

### 2. CORE-Bench (NeurIPS 2024)

**Source:** [arxiv.org/abs/2409.11363](https://arxiv.org/abs/2409.11363)

**Focus:** Computational reproducibility of scientific papers

**Structure:**
- 270 tasks from 90 papers
- 3 disciplines: computer science, social science, medicine
- 3 difficulty levels
- Both language-only and vision-language tasks

**Key Insight:**
> "Having agents that can reproduce existing work is a necessary step towards building agents that can conduct novel research."

**Performance:** 21% on hardest tasks (GPT-4o)

**Agents Tested:**
- AutoGPT (general purpose)
- CORE-Agent (task-specific)

**What We Can Learn:**
- Reproducibility is foundational before novel research
- Multi-tier difficulty allows progressive testing
- Rapid parallelized evaluation is essential
- Even simple reproducibility is challenging (~20%)

---

### 3. MLAgentBench (ICML 2024)

**Source:** [github.com/snap-stanford/MLAgentBench](https://github.com/snap-stanford/MLAgentBench)

**Focus:** ML experimentation and model improvement

**Structure:**
- 13 tasks from Kaggle + custom ML tasks
- Range: CIFAR-10 improvement to BabyLM challenge
- Open-ended decision making
- Full pipeline access (data, architecture, training)

**Actions Available:**
- File system operations
- Code execution
- Output inspection
- Pipeline modification

**Performance:**
- 90% on well-established datasets
- 10% on recent Kaggle challenges
- 0% on newest research challenges

**Key Challenges Identified:**
- Long-term planning
- Hallucination
- Exploration vs. exploitation

**What We Can Learn:**
- Success rate varies dramatically with task novelty
- Long-term planning is a consistent weakness
- Baseline solutions help quantify improvement

---

### 4. MLE-bench (2024)

**Source:** [arxiv.org/abs/2410.07095](https://arxiv.org/abs/2410.07095)

**Focus:** ML engineering on Kaggle competitions

**Structure:**
- 75 ML engineering competitions
- Real-world skills: training, dataset prep, experiments
- Medal-based evaluation (bronze/silver/gold)

**Best Performance:** 16.9% achieve bronze (o1-preview + AIDE)

**What We Can Learn:**
- Competition format provides clear success metrics
- Scaffolding (AIDE) significantly improves performance
- Even "engineering" tasks are challenging

---

### 5. AgentBench (ICLR 2024)

**Source:** [github.com/THUDM/AgentBench](https://github.com/THUDM/AgentBench)

**Focus:** General LLM agent capabilities

**Structure:**
- 8 environments: OS, database, knowledge graph, card game, puzzles, household, web shopping, web browsing
- Multi-dimensional evaluation

**Key Findings:**
- Large gap between commercial and OSS models
- Main obstacles: long-term reasoning, decision-making, instruction following

**What We Can Learn:**
- Multi-environment testing reveals different capability gaps
- Commercial models significantly outperform open source
- Instruction following is a consistent weakness

---

### 6. SWE-bench

**Source:** [swebench.com](https://www.swebench.com/)

**Focus:** Software engineering (GitHub issue resolution)

**Structure:**
- 2,294 issue-commit pairs
- 12 Python repositories
- Variations: Lite (300), Verified, Multimodal

**Performance:** 20-45% depending on variant and model

**What We Can Learn:**
- Real codebase tasks are challenging
- Human verification (SWE-bench Verified) improves reliability
- Subsets allow focused evaluation

---

## Evaluation Frameworks

### KDD 2025 Tutorial Taxonomy

**Evaluation Objectives (What to Evaluate):**
1. Agent Behavior - Actions taken
2. Capabilities - What agent can do
3. Reliability - Consistency across runs
4. Safety - What agent avoids

**Evaluation Process (How to Evaluate):**
1. Interaction Modes - Single turn vs. multi-turn
2. Datasets & Benchmarks - Task collections
3. Metric Computation - How scores calculated
4. Tooling - Infrastructure for evaluation

### CLEAR Framework (Enterprise AI)

| Dimension | Metrics |
|-----------|---------|
| **C**ost | Token usage, API costs, infrastructure overhead |
| **L**atency | Response time, total duration, time-to-first-token |
| **E**fficacy | Task completion, accuracy, quality |
| **A**ssurance | Safety, security, compliance, auditability |
| **R**eliability | Consistency, error recovery, degradation handling |

**Key Insight:** 85% of companies experiment with AI, but most abandon after POC due to misalignment between benchmark performance and enterprise needs.

---

## Common Metrics Across Benchmarks

| Metric | Description | Used In |
|--------|-------------|---------|
| Success Rate (SR) | Binary task completion | Most benchmarks |
| Pass@k | Success with k attempts | Code generation |
| Task Goal Completion (TGC) | Partial credit | AgentBench |
| Execution Success | Code runs without error | ScienceAgentBench |
| Result Correctness | Output matches expected | CORE-Bench |
| Cost Efficiency | Tokens/API calls per task | CLEAR |
| Error Recovery | Handling of failures | AgentBench |

---

## Design Patterns for Improving Agents

### ReAct (Reasoning + Acting)

**Pattern:** Thought → Action → Observation → Thought → ...

**Benefits:**
- 34% improvement on ALFWorld
- Reduces hallucination
- Improves interpretability

**Implementation:**
```
Thought: I need to find the lattice constant of copper
Action: Run LAMMPS with EAM potential
Observation: Simulation complete, a = 3.615 Å
Thought: This matches literature value of 3.61 Å, task complete
```

### Plan-then-Execute

**Pattern:** Generate plan → Execute steps → Verify

**Benefits:**
- Avoids repetitive loops
- Maintains focus on goal
- Enables checkpoint recovery

**Key Insight:** Decoupling planning from execution prevents getting stuck.

### Tree of Thoughts

**Pattern:** Explore multiple reasoning paths explicitly

**Benefits:**
- Game of 24: 4% → 74% accuracy
- Enables backtracking
- Considers alternatives

---

## Gaps in Current Benchmarks

### What's Missing

1. **Long-horizon tasks:** Most benchmarks < 1 hour
2. **Multi-day research:** No benchmarks for sustained campaigns
3. **Physical simulation:** Most focus on code, not computation
4. **Resource management:** Limited cost/compute awareness
5. **Collaboration:** Few multi-agent benchmarks

### Our Unique Contributions

Our benchmark system addresses several gaps:

| Gap | Our Approach |
|-----|--------------|
| Physical simulation | Actual LAMMPS/QE execution |
| Resource management | T14 compute decision benchmarks |
| Multi-backend | Local/HPC/Cloud workflows |
| Behavioral testing | T13-T16 agent cognition |
| Full observability | Workspace preservation, audits |

---

## Recommendations for Our System

### Adopt from Literature

1. **Containerized evaluation** (ScienceAgentBench)
   - Reproducible runs
   - Isolated environments
   - Parallelizable

2. **Difficulty tiers** (CORE-Bench)
   - We already have 16 tiers
   - Could consolidate to 3-4 main levels

3. **Expert validation** (ScienceAgentBench)
   - Have domain experts validate benchmark tasks
   - Especially for T8-T12 advanced tasks

4. **Baseline solutions** (MLAgentBench)
   - Provide reference solutions for comparison
   - Enables "improvement over baseline" metrics

### Innovate Beyond Literature

1. **Full observability** (unique to us)
   - Keep workspace artifacts
   - Complete grading audits
   - Agent transcripts

2. **Behavioral benchmarks** (T13-T16)
   - Tests cognition, not just completion
   - No equivalent in literature

3. **Multi-compute** (T5, T14)
   - Tests compute resource decisions
   - Real HPC integration

4. **Scientific rigor** (T16)
   - Tests methodology, not just results
   - Reproducibility, uncertainty, safety

---

## References

### Primary Sources

- [ScienceAgentBench](https://github.com/OSU-NLP-Group/ScienceAgentBench) - ICLR 2025
- [CORE-Bench](https://arxiv.org/abs/2409.11363) - NeurIPS 2024
- [MLAgentBench](https://arxiv.org/abs/2310.03302) - ICML 2024
- [AgentBench](https://arxiv.org/abs/2308.03688) - ICLR 2024
- [MLE-bench](https://arxiv.org/abs/2410.07095) - 2024
- [SWE-bench](https://arxiv.org/abs/2310.06770) - 2023

### Surveys & Tutorials

- [KDD 2025: Evaluation & Benchmarking of LLM Agents](https://sap-samples.github.io/llm-agents-eval-tutorial/)
- [Evaluation and Benchmarking of LLM Agents: A Survey](https://arxiv.org/html/2507.21504v1)
- [10 AI Agent Benchmarks](https://www.evidentlyai.com/blog/ai-agent-benchmarks)

### Design Patterns

- [ReAct Prompting](https://www.promptingguide.ai/techniques/react)
- [LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)
- [CLEAR Framework](https://arxiv.org/html/2511.14136v1)
