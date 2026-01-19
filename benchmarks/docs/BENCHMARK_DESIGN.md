# Benchmark Design Documentation

## Overview: Two Types of Benchmarks

This benchmark suite contains two fundamentally different types of tests:

### 1. Infrastructure Benchmarks (Currently Implemented)

**Purpose**: Verify the tools, binaries, and environment work correctly.

**How they work**:
```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│                  │     │                  │     │                  │
│   YAML defines   │────▶│  Runner executes │────▶│  Check exit code │
│   a shell script │     │  script directly │     │  and outputs     │
│                  │     │                  │     │                  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
```

**Example**:
```yaml
type: command
command: |
  /path/to/lmp -in pre_written_input.lmp
validation:
  exit_code: 0
```

**What this tests**: "Does LAMMPS binary execute correctly?"
**What this does NOT test**: "Can an AI agent figure out how to use LAMMPS?"

---

### 2. Agentic Benchmarks (Planned/Partial Implementation)

**Purpose**: Test whether the AI agent can autonomously solve scientific problems.

**How they should work**:
```
┌──────────────────┐     ┌──────────────────┐     ┌──────────────────┐
│                  │     │                  │     │                  │
│   YAML defines   │────▶│  Send prompt to  │────▶│  Evaluate agent's│
│   a TASK/PROMPT  │     │  Claude Code CLI │     │  solution        │
│                  │     │                  │     │                  │
└──────────────────┘     └──────────────────┘     └──────────────────┘
                                  │
                                  ▼
                         ┌──────────────────┐
                         │  Agent decides:  │
                         │  - What tools    │
                         │  - What files    │
                         │  - What commands │
                         └──────────────────┘
```

**Example**:
```yaml
type: agent
prompt: |
  Create a LAMMPS simulation to minimize a 10-atom LJ system.
  Use epsilon=0.238 kcal/mol, sigma=3.405 Å.
  Report initial and final energies.
validation:
  files_created: [minimized.data]
  output_contains: [energy, minimize]
```

**What this tests**: "Can the agent autonomously complete a scientific task?"

---

## Current Benchmark Categories

| Category | Type | What It Tests |
|----------|------|---------------|
| `environment` | Infrastructure | System dependencies exist |
| `lammps` | Infrastructure | LAMMPS binary works |
| `qe` | Infrastructure | QE binary works |
| `literature` | Infrastructure | APIs are accessible |
| `materials` | Infrastructure | APIs are accessible |
| `analysis` | Infrastructure | Python scripts work |
| `workflows` | Infrastructure | Multi-step scripts work |
| `agent` | **Agentic** | Agent solves problems |

---

## How Grading Works

### Infrastructure Benchmarks (Current)

Simple pass/fail based on:

1. **Exit Code**: Did the command return 0?
2. **Output Contains**: Does stdout contain expected strings?
3. **Files Created**: Do expected output files exist?
4. **No Errors**: Is stderr empty (optional)?

```python
def _validate_results(self, test_def, result):
    validations = {}

    # Check return code
    if 'exit_code' in test_def['validation']:
        expected = test_def['validation']['exit_code']
        actual = result['returncode']
        validations['exit_code'] = {
            'passed': actual == expected
        }

    # Check output contains patterns
    if 'stdout_contains' in test_def['validation']:
        for pattern in test_def['validation']['stdout_contains']:
            validations[f'contains:{pattern}'] = {
                'passed': pattern in result['stdout']
            }

    # All validations must pass
    return validations
```

### Agentic Benchmarks (Proposed)

More sophisticated grading based on:

1. **Correctness**: Did the agent produce correct output?
2. **Completeness**: Did the agent complete all required steps?
3. **Efficiency**: How many tool calls / tokens used?
4. **Robustness**: Did the agent handle errors gracefully?

```python
def grade_agent_result(test_def, agent_output):
    score = 0
    rubric = test_def['grading']

    # Check each rubric item
    if file_is_valid('minimized.data'):
        score += rubric['correct_structure']

    if parameters_are_correct(agent_output):
        score += rubric['correct_forcefield']

    if lammps_ran_successfully(agent_output):
        score += rubric['successful_run']

    return score  # 0-100
```

---

## How to Execute Agent Benchmarks

### Option 1: Using Claude Code CLI (Headless)

```bash
# Send prompt to Claude Code and capture response
echo "$PROMPT" | claude --print --output-format json > response.json

# Parse response and evaluate
python evaluate_response.py response.json
```

### Option 2: Using Claude Agent SDK

```python
from claude_code_sdk import query, ClaudeAgentOptions

async def run_agent_benchmark(prompt: str, workspace: str):
    options = ClaudeAgentOptions(
        allowed_tools=["Bash", "Write", "Read"],
        max_turns=20,
        cwd=workspace
    )

    result = await query(prompt=prompt, options=options)

    return {
        'output': result.output,
        'tool_calls': result.tool_calls,
        'tokens_used': result.tokens_used,
        'success': result.success
    }
```

### Option 3: Interactive Evaluation

For complex benchmarks, human evaluation may be needed:

```yaml
type: agent
evaluation: manual

prompt: |
  Research hydrogen storage materials and recommend
  3 candidates for further DFT study.

manual_rubric:
  - Are the recommendations scientifically sound?
  - Did the agent cite sources?
  - Are the materials actually feasible?
```

---

## The CLEAR Framework

All benchmarks collect metrics following CLEAR:

| Metric | What We Measure | Target |
|--------|-----------------|--------|
| **C**ost | Tokens used, API calls | Minimize |
| **L**atency | Execution time | <60s for simple tasks |
| **E**fficacy | Task completion rate | >90% pass rate |
| **A**ssurance | Validation passes | 100% valid outputs |
| **R**eliability | Consistency across runs | <5% variance |

---

## Adding New Benchmarks

### Infrastructure Benchmark

```yaml
name: my-infrastructure-test
type: command
command: |
  # Pre-written script that tests something
  some_command --with args
validation:
  exit_code: 0
  stdout_contains: ["expected output"]
```

### Agentic Benchmark

```yaml
name: my-agent-test
type: agent
prompt: |
  Natural language description of the task
  the agent should complete autonomously.
expected_actions:
  - Description of what agent should do
validation:
  files_created: [expected_output.txt]
  functional_checks:
    - type: script
      script: validate_output.py
grading:
  task_complete: 50
  correct_output: 30
  efficient_solution: 20
```

---

## Current Limitations

1. **Agent tests not yet integrated**: The `type: agent` tests are defined but the runner doesn't yet call Claude Code CLI.

2. **Manual evaluation needed**: Complex scientific tasks may need human review.

3. **No token tracking**: We don't yet capture Claude API usage metrics.

4. **Single-run evaluation**: We don't yet test consistency across multiple runs.

---

## Roadmap

1. **Phase 1** (Current): Infrastructure benchmarks - verify tools work
2. **Phase 2**: Simple agent benchmarks - single-skill tasks
3. **Phase 3**: Complex agent benchmarks - multi-skill workflows
4. **Phase 4**: Adversarial benchmarks - edge cases and error recovery
5. **Phase 5**: Comparative benchmarks - compare against human performance
