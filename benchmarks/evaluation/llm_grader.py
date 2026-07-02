#!/usr/bin/env python3
"""
Claude Code Agent Grader for Agentic Science Worker

Uses a full Claude Code agent (with tool access) to critically evaluate
benchmark results. The grader agent can read files, run analysis commands,
and verify outputs just like the main agent.
"""

import json
import os
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional
from dataclasses import dataclass, asdict


@dataclass
class LLMGradeResult:
    """Result from LLM grading."""
    benchmark_id: str
    total_score: float
    max_score: float = 100.0
    passed: bool = False
    pass_threshold: float = 70.0

    # Category scores
    categories: Dict[str, Dict[str, float]] = None

    # LLM reasoning
    reasoning: str = ""
    strengths: list = None
    weaknesses: list = None
    suggestions: list = None


# Tools available to the grading agent
GRADER_TOOLS = [
    "Bash",      # Run verification commands (grep, check values, etc.)
    "Read",      # Read files in workspace
    "Glob",      # Find files by pattern
    "Grep",      # Search file contents
]


def grade_with_llm(
    benchmark: Dict[str, Any],
    workspace: Path,
    agent_output: str,
    timeout: int = 300,  # 5 minutes for thorough grading
    max_retries: int = 2,
    model: str = None  # Slice A1 (rebase-2026-07-02): explicit grader-model pin
) -> LLMGradeResult:
    """
    Use a Claude Code agent to evaluate benchmark results.

    The grading agent has full tool access and can:
    - Read files in the workspace
    - Run bash commands to verify outputs
    - Search for patterns in logs
    - Perform numerical validation

    Args:
        benchmark: Benchmark definition from YAML
        workspace: Path to workspace directory
        agent_output: Full agent output text
        timeout: Timeout in seconds for grading (default 5 min)
        max_retries: Number of retry attempts on failure

    Returns:
        LLMGradeResult with scores and reasoning
    """
    import time

    benchmark_id = benchmark.get('id', 'unknown')
    tier = benchmark.get('tier', 1)

    # Build the grading prompt - agent will use tools to investigate
    grading_prompt = f"""You are a rigorous scientific reviewer grading an AI agent's work on a computational science benchmark.

## YOUR ROLE

You are evaluating whether a computational science agent worked like a real researcher.

**Core Evaluation Questions:**
1. Did the agent THINK before acting? (Plan, research, then execute)
2. Did the agent FIND its own resources? (Parameters, files, structures)
3. Did the agent VERIFY its work? (Check against literature, physical reasonableness)
4. Did the agent DOCUMENT properly? (Citations, methodology, reasoning)

**Use your tools to investigate thoroughly:**
- `Read` - Examine input files, logs, outputs, reports
- `Grep` - Search for citations, error messages, expected values
- `Bash` - Verify file integrity, check numerical values
- `Glob` - Find all relevant files in workspace

**Specific Evidence to Look For:**

*Citations and Sources:*
- Comments like "# Source: Rahman 1964" or "# From: Jorgensen et al., 1983"
- References with DOIs, journal names, or URLs
- Literature notes files (literature_notes.md, references.md, etc.)
- Mentioned database queries (Materials Project, PubChem, etc.)

*Verification Behavior:*
- Comparison of results to known/expected values
- Discussion of discrepancies or anomalies
- Physical reasonableness checks (order of magnitude, signs, units)
- Convergence testing or parameter sensitivity discussion

*Documentation Quality:*
- Clear methodology description
- Explained reasoning for choices
- Noted limitations or uncertainties
- Structured reports with sections

*Red Flags (penalize these):*
- Hardcoded values without sources
- "Typical" or "common" values without citation
- No verification against literature
- Missing error handling or blind acceptance of results

## BENCHMARK DEFINITION

**ID**: {benchmark_id}
**Tier**: {tier}
**Name**: {benchmark.get('name', 'Unknown')}

**Description**:
{benchmark.get('description', '')}

**Task Prompt Given to Agent**:
{benchmark.get('prompt', '')}

**Expected Outputs**:
{json.dumps(benchmark.get('expected_outputs', {}), indent=2)}

**Grading Rubric**:
{json.dumps(benchmark.get('grading', {}), indent=2)}

## WORKSPACE

The agent's work is in: {workspace}

Use your tools to explore this directory and verify the work.

## AGENT'S FINAL OUTPUT (for reference)

{agent_output[:6000] if len(agent_output) > 6000 else agent_output}

## YOUR GRADING TASK

1. **INVESTIGATE**: Use your tools to explore the workspace:
   - List files created
   - Read key input/output files
   - Check log files for errors or success messages
   - Verify numerical results are in expected ranges

2. **USE THE BENCHMARK-SPECIFIC RUBRIC** (Critical!):

   The rubric above in "Grading Rubric" section defines EXACTLY what to evaluate for THIS benchmark.
   Each benchmark has its own tailored criteria - USE THEM, not a generic rubric.

   **Read the rubric carefully and evaluate based on those specific categories and weights.**

   For example:
   - If the rubric has "input_setup" (35%) and "execution_success" (35%), evaluate those
   - If the rubric has "scientific_reasoning" (30%) and "independence" (25%), evaluate those
   - Do NOT add categories that aren't in the rubric
   - Do NOT change the weights specified in the rubric

3. **EVALUATE** based on the benchmark's rubric categories:

   For each category in the rubric:
   - Score 0-100 based on how well the agent met the criteria listed
   - Use the weight specified in the rubric
   - Provide specific notes about what was done well or poorly

   General scoring guide:
   - 90-100: Excellent - fully met all criteria with high quality
   - 70-89: Good - met most criteria with minor issues
   - 50-69: Adequate - met some criteria but notable gaps
   - 30-49: Poor - significant issues, many criteria not met
   - 0-29: Failed - did not meet criteria

4. **ADDITIONAL QUALITY CHECKS** (apply where relevant):

   If the benchmark required the agent to find its own parameters (not provided in prompt):
   - Did it search literature? Cite sources? Download resources?

   If parameters were PROVIDED in the prompt:
   - Did the agent use them correctly? (Don't penalize for not researching given parameters)

   Always check:
   - Are results physically reasonable?
   - Is documentation clear?
   - Were errors handled appropriately?

5. **SCORE**: Calculate weighted average based on the benchmark's rubric weights

6. **REPORT**: After your investigation, provide your final assessment in this EXACT JSON format:

```json
{{
    "total_score": <0-100>,
    "categories": {{
        "<category_from_rubric>": {{"score": <0-100>, "weight": <from_rubric>, "notes": "specific evaluation notes"}},
        "<another_category>": {{"score": <0-100>, "weight": <from_rubric>, "notes": "..."}}
    }},
    "reasoning": "Overall assessment in 2-3 sentences",
    "strengths": ["strength 1", "strength 2"],
    "weaknesses": ["weakness 1", "weakness 2"],
    "suggestions": ["suggestion for improvement"]
}}
```

**IMPORTANT**: Use the EXACT category names and weights from the benchmark's rubric, not generic categories.

**Grading Philosophy**:
- Be rigorous but fair
- Grade based on what the benchmark ASKED for
- If parameters were PROVIDED in the prompt, don't penalize for not researching them
- If the benchmark required finding parameters, evaluate how well the agent did that
- Focus on whether the agent accomplished the benchmark's specific goals

START by using your tools to explore the workspace, then provide your grading.
"""

    # Call Claude Code agent with full tool access
    cmd = [
        "claude",
        "-p",  # Print mode (non-interactive)
        "--output-format", "json",
        "--dangerously-skip-permissions",  # Full autonomy for grading
        "--allowedTools", ",".join(GRADER_TOOLS),
    ]
    if model:
        cmd += ["--model", model]  # Slice A1: pin grader model

    last_error = None

    for attempt in range(max_retries + 1):
        try:
            if attempt > 0:
                time.sleep(2)  # Brief pause before retry

            result = subprocess.run(
                cmd,
                input=grading_prompt,
                capture_output=True,
                text=True,
                timeout=timeout,
                cwd=str(workspace),  # Run from workspace directory
                env={**os.environ, "HOME": os.environ.get("HOME")}
            )

            if result.returncode != 0:
                last_error = f"Grading agent failed: {result.stderr}"
                continue

            # Parse the response
            response_json = json.loads(result.stdout)
            llm_response = response_json.get('result', '')

            # Extract JSON from agent response - try multiple patterns
            import re

            grade_data = None

            # Pattern 1: JSON in code block
            json_match = re.search(r'```json\s*(.*?)\s*```', llm_response, re.DOTALL)
            if json_match:
                try:
                    grade_data = json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass

            # Pattern 2: JSON object with total_score (nested structure)
            if grade_data is None:
                json_match = re.search(r'\{[^{}]*"total_score"[^{}]*"categories".*?\}(?=\s*$|\s*[^{])', llm_response, re.DOTALL)
                if json_match:
                    try:
                        # Try to find the complete JSON object
                        start = json_match.start()
                        brace_count = 0
                        end = start
                        for i, char in enumerate(llm_response[start:], start):
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    end = i + 1
                                    break
                        potential_json = llm_response[start:end]
                        grade_data = json.loads(potential_json)
                    except (json.JSONDecodeError, IndexError):
                        pass

            # Pattern 3: Simple JSON object with total_score
            if grade_data is None:
                json_match = re.search(r'\{\s*"total_score"\s*:\s*\d+', llm_response, re.DOTALL)
                if json_match:
                    try:
                        start = json_match.start()
                        brace_count = 0
                        for i, char in enumerate(llm_response[start:], start):
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                                if brace_count == 0:
                                    potential_json = llm_response[start:i+1]
                                    grade_data = json.loads(potential_json)
                                    break
                    except (json.JSONDecodeError, IndexError):
                        pass

            # Pattern 4: Try to parse whole response as JSON
            if grade_data is None:
                try:
                    grade_data = json.loads(llm_response)
                except json.JSONDecodeError:
                    # Last resort: extract just the score
                    score_match = re.search(r'"total_score"\s*:\s*(\d+(?:\.\d+)?)', llm_response)
                    if score_match:
                        grade_data = {"total_score": float(score_match.group(1))}
                    else:
                        raise json.JSONDecodeError("Could not find grade data", llm_response, 0)

            # Calculate pass/fail
            total_score = grade_data.get('total_score', 0)
            pass_thresholds = {1: 70, 2: 65, 3: 60, 4: 60}
            threshold = pass_thresholds.get(tier, 70)

            return LLMGradeResult(
                benchmark_id=benchmark_id,
                total_score=total_score,
                passed=total_score >= threshold,
                pass_threshold=threshold,
                categories=grade_data.get('categories', {}),
                reasoning=grade_data.get('reasoning', ''),
                strengths=grade_data.get('strengths', []),
                weaknesses=grade_data.get('weaknesses', []),
                suggestions=grade_data.get('suggestions', [])
            )

        except subprocess.TimeoutExpired:
            last_error = f"Grading agent timed out after {timeout}s (attempt {attempt + 1})"
        except json.JSONDecodeError as e:
            last_error = f"Failed to parse grading response: {e}"
        except Exception as e:
            last_error = f"Grading error: {e}"

    # All retries failed
    return LLMGradeResult(
        benchmark_id=benchmark_id,
        total_score=0,
        reasoning=f"Grading failed after {max_retries + 1} attempts. Last error: {last_error}"
    )


def print_grade_report(result: LLMGradeResult):
    """Print a formatted grading report."""
    print(f"\n{'='*60}")
    print(f"GRADING REPORT: {result.benchmark_id}")
    print(f"{'='*60}")

    status = "PASSED" if result.passed else "FAILED"
    print(f"\nTotal Score: {result.total_score:.0f}/100 ({status})")
    print(f"Pass Threshold: {result.pass_threshold:.0f}")

    if result.categories:
        print(f"\nCategory Scores:")
        for cat, data in result.categories.items():
            score = data.get('score', 0)
            weight = data.get('weight', 25)
            notes = data.get('notes', '')[:80]
            print(f"  {cat}: {score:.0f}/100 (weight: {weight}%)")
            if notes:
                print(f"    → {notes}")

    if result.reasoning:
        print(f"\nOverall Assessment:")
        print(f"  {result.reasoning}")

    if result.strengths:
        print(f"\nStrengths:")
        for s in result.strengths:
            print(f"  + {s}")

    if result.weaknesses:
        print(f"\nWeaknesses:")
        for w in result.weaknesses:
            print(f"  - {w}")

    if result.suggestions:
        print(f"\nSuggestions:")
        for s in result.suggestions:
            print(f"  → {s}")


if __name__ == "__main__":
    import argparse
    import yaml

    parser = argparse.ArgumentParser(description="Claude Code Agent Grader")
    parser.add_argument("benchmark_yaml", help="Path to benchmark YAML")
    parser.add_argument("workspace", help="Path to workspace directory")
    parser.add_argument("--output", help="Path to agent output file")
    parser.add_argument("--timeout", type=int, default=300, help="Grading timeout in seconds")

    args = parser.parse_args()

    with open(args.benchmark_yaml) as f:
        benchmark = yaml.safe_load(f)

    workspace = Path(args.workspace)

    agent_output = ""
    if args.output:
        agent_output = Path(args.output).read_text()

    result = grade_with_llm(benchmark, workspace, agent_output, timeout=args.timeout)
    print_grade_report(result)

    # Save result
    output_file = workspace / "grading_result.json"
    with open(output_file, 'w') as f:
        json.dump(asdict(result), f, indent=2)
    print(f"\nResult saved to: {output_file}")
