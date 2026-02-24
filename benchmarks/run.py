#!/usr/bin/env python3
"""
Unified Benchmark Runner with Full Observability

Replaces harness.py and runner.py with a single entry point that provides:
- Full agent transcript (every tool call, every response)
- Preserved workspaces (never deleted)
- Grading audit trail (every check, every evidence)
- Multiple grading modes (LLM, rules, hybrid)

Usage:
    python run.py BENCH-T1-001              # Run single benchmark
    python run.py --tier 1                  # Run tier
    python run.py BENCH-T1-001 --verbose    # With detailed output
    python run.py BENCH-T1-001 --inspect    # Open results after run
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import time
import yaml
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# Add evaluation directory to path
sys.path.insert(0, str(Path(__file__).parent / "evaluation"))

from audit import GradingAudit, CategoryAudit, CheckAudit, CheckResult, CheckEvidence, create_audit_from_benchmark
from transcript import AgentTranscript, Turn, ToolCall, parse_claude_output


# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent
BENCHMARKS_DIR = PROJECT_ROOT / "benchmarks"
TASKS_DIR = BENCHMARKS_DIR / "tasks"
RESULTS_DIR = BENCHMARKS_DIR / "results" / "runs"

# Pass thresholds by tier
PASS_THRESHOLDS = {
    1: 70, 2: 65, 3: 60, 4: 60, 5: 60, 6: 55, 7: 50, 8: 60,
    9: 50, 10: 40, 11: 35, 12: 50, 13: 60, 14: 65, 15: 60, 16: 70
}

# Default configuration
DEFAULT_TIMEOUT_SECONDS = 1800  # 30 minutes
GRADING_TIMEOUT_SECONDS = 600  # 10 minutes for thorough grading

ALLOWED_TOOLS = [
    "Bash", "Read", "Write", "Edit", "Glob", "Grep",
    "WebSearch", "WebFetch", "TodoWrite"
]


# ============================================================================
# Result Data Structure
# ============================================================================

@dataclass
class BenchmarkRun:
    """Complete record of a benchmark run with full observability."""
    benchmark_id: str
    run_id: str
    timestamp: str

    # Status
    status: str  # "passed", "failed", "timeout", "error"
    score: float = 0.0
    pass_threshold: float = 70.0

    # Timing
    execution_duration_seconds: float = 0.0
    grading_duration_seconds: float = 0.0

    # Paths (all relative to run_dir)
    workspace_path: str = "workspace"
    transcript_path: str = "transcript.json"
    audit_path: str = "grading_audit.json"

    # Summary
    files_created: List[str] = field(default_factory=list)
    num_turns: int = 0
    num_tool_calls: int = 0

    # Errors
    error_message: Optional[str] = None
    exit_code: int = 0


# ============================================================================
# Benchmark Loading
# ============================================================================

def load_benchmark(benchmark_id: str) -> Dict[str, Any]:
    """Load a benchmark definition by ID."""
    for tier_dir in TASKS_DIR.iterdir():
        if not tier_dir.is_dir():
            continue
        for bench_file in tier_dir.glob("*.yaml"):
            with open(bench_file) as f:
                bench = yaml.safe_load(f)
            if bench.get('id') == benchmark_id:
                bench['_source_file'] = str(bench_file)
                return bench
    raise ValueError(f"Benchmark not found: {benchmark_id}")


def list_benchmarks(tier: Optional[int] = None) -> List[Dict]:
    """List all available benchmarks."""
    benchmarks = []
    for tier_dir in sorted(TASKS_DIR.iterdir()):
        if not tier_dir.is_dir():
            continue
        if tier is not None and f"tier{tier}" not in tier_dir.name:
            continue
        for bench_file in sorted(tier_dir.glob("*.yaml")):
            with open(bench_file) as f:
                bench = yaml.safe_load(f)
            benchmarks.append(bench)
    return benchmarks


def get_tier(benchmark: Dict) -> int:
    """Extract tier number from benchmark."""
    return benchmark.get('tier', 1)


# ============================================================================
# Execution
# ============================================================================

def execute_agent(
    prompt: str,
    workspace: Path,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Execute Claude Code agent and capture full output.

    Returns:
        Dict with: output, json, stderr, exit_code, duration
    """
    # Build command
    cmd = [
        "claude",
        "-p",  # Print mode
        "--output-format", "json",
        "--dangerously-skip-permissions",
        "--allowedTools", ",".join(ALLOWED_TOOLS)
    ]

    if verbose:
        print(f"  Command: {' '.join(cmd[:5])}...")
        print(f"  Workspace: {workspace}")
        print(f"  Timeout: {timeout}s")

    # Run agent
    start_time = time.time()
    try:
        result = subprocess.run(
            cmd,
            input=prompt,
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(workspace),
            env={**os.environ, 'CLICOLOR_FORCE': '0'}
        )
        duration = time.time() - start_time

        return {
            'status': 'success' if result.returncode == 0 else 'error',
            'output': result.stdout,
            'stderr': result.stderr,
            'exit_code': result.returncode,
            'duration': duration
        }

    except subprocess.TimeoutExpired:
        return {
            'status': 'timeout',
            'output': '',
            'stderr': f'Execution timed out after {timeout}s',
            'exit_code': -1,
            'duration': timeout
        }
    except Exception as e:
        return {
            'status': 'error',
            'output': '',
            'stderr': str(e),
            'exit_code': -1,
            'duration': time.time() - start_time
        }


# ============================================================================
# Grading
# ============================================================================

def grade_with_llm_agent(
    workspace: Path,
    benchmark: Dict,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Use Claude Code agent to grade the benchmark result.

    Returns grading details with audit trail.
    """
    # Build grading prompt
    grading_prompt = f"""You are a CRITICAL GRADER evaluating a benchmark result. Your job is to thoroughly explore this workspace and rigorously grade the work against specific criteria.

## Benchmark Being Graded
ID: {benchmark.get('id')}
Name: {benchmark.get('name')}

## Original Task Given to Agent
{benchmark.get('description', '')}

## Expected Outputs
{yaml.dump(benchmark.get('expected_outputs', {}), default_flow_style=False)}

## Grading Rubric (Use This!)
{yaml.dump(benchmark.get('grading', {}), default_flow_style=False)}

## YOUR GRADING PROCESS (Follow These Steps)

### Step 1: Explore the Workspace
Use Glob to find ALL files created:
- `Glob pattern="**/*"` to see everything
- Note what was created vs what was expected

### Step 2: Read Key Artifacts
For each important file:
- Read the content
- Check if it meets the criteria
- Note specific evidence (quote lines, values, etc.)

### Step 3: Check for Errors
Look for:
- Error messages in logs
- Incomplete outputs
- Missing required files
- Scientific errors (wrong values, missing units, etc.)

### Step 4: Evaluate Against Each Criterion
For EACH grading criterion in the rubric:
- State what you found (with file:line evidence)
- Determine if it passes, partially passes, or fails
- Assign points accordingly

### Step 5: Return Your Grading

```json
{{
    "total_score": <0-100>,
    "categories": {{
        "<category_name>": {{
            "score": <0-100>,
            "weight": <from rubric>,
            "evidence": "<specific files/lines that support your score>",
            "notes": "<what you found, be specific>"
        }}
    }},
    "reasoning": "<overall critical assessment>",
    "strengths": ["<specific things done well with evidence>"],
    "weaknesses": ["<specific issues found with evidence>"],
    "suggestions": ["<concrete improvements>"]
}}
```

## GRADING STANDARDS
- Be RIGOROUS - don't give points for incomplete work
- Require EVIDENCE - cite specific files and content
- Check CORRECTNESS - wrong values = low score even if file exists
- Penalize MISSING ITEMS - if rubric requires it and it's missing, deduct points
- Award PARTIAL CREDIT fairly - 50% complete = ~50% of points

DO NOT be lenient. Scientific work requires precision.
"""

    # Run grading agent
    cmd = [
        "claude",
        "-p",
        "--output-format", "json",
        "--dangerously-skip-permissions",
        "--allowedTools", "Read,Bash,Glob,Grep"
    ]

    try:
        result = subprocess.run(
            cmd,
            input=grading_prompt,
            capture_output=True,
            text=True,
            timeout=GRADING_TIMEOUT_SECONDS,
            cwd=str(workspace),
            env={**os.environ, 'CLICOLOR_FORCE': '0'}
        )

        # Parse response
        output = result.stdout
        try:
            data = json.loads(output)
            result_text = data.get('result', output)
        except json.JSONDecodeError:
            result_text = output

        # Extract JSON from response
        import re
        json_match = re.search(r'```json\s*(.*?)\s*```', result_text, re.DOTALL)
        if json_match:
            grading_json = json.loads(json_match.group(1))
        else:
            # Try parsing entire response as JSON
            try:
                grading_json = json.loads(result_text)
            except:
                grading_json = {'total_score': 0, 'reasoning': 'Failed to parse grading response'}

        return {
            'score': grading_json.get('total_score', 0),
            'categories': grading_json.get('categories', {}),
            'reasoning': grading_json.get('reasoning', ''),
            'strengths': grading_json.get('strengths', []),
            'weaknesses': grading_json.get('weaknesses', []),
            'suggestions': grading_json.get('suggestions', []),
            'grader': 'llm',
            'raw_response': result_text[:2000]  # Keep first 2000 chars
        }

    except subprocess.TimeoutExpired:
        return {
            'score': 0,
            'reasoning': 'Grading timed out',
            'grader': 'timeout'
        }
    except Exception as e:
        return {
            'score': 0,
            'reasoning': f'Grading error: {str(e)}',
            'grader': 'error'
        }


# ============================================================================
# Main Run Function
# ============================================================================

def run_benchmark(
    benchmark_id: str,
    verbose: bool = False,
    grading_mode: str = "llm"  # "llm", "rules", "hybrid"
) -> BenchmarkRun:
    """
    Run a benchmark with full observability.

    Creates:
    - results/{benchmark_id}-{run_id}/
        - metadata.json      # Run metadata
        - transcript.json    # Full agent transcript
        - transcript.md      # Human-readable transcript
        - grading_audit.json # Detailed grading results
        - grading_audit.md   # Human-readable grading
        - workspace/         # Preserved agent workspace
    """
    # Load benchmark
    benchmark = load_benchmark(benchmark_id)
    tier = get_tier(benchmark)
    pass_threshold = PASS_THRESHOLDS.get(tier, 60)

    # Create run ID and directories
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    run_dir = RESULTS_DIR / f"{benchmark_id}-{run_id}"
    run_dir.mkdir(parents=True, exist_ok=True)

    # Workspace is INSIDE results directory (preserved!)
    workspace = run_dir / "workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    # Copy AGENTS.md and CLAUDE.md to workspace so agent has context
    agents_md = PROJECT_ROOT / "AGENTS.md"
    claude_md = PROJECT_ROOT / "CLAUDE.md"
    if agents_md.exists():
        shutil.copy(agents_md, workspace / "AGENTS.md")
    if claude_md.exists():
        shutil.copy(claude_md, workspace / "CLAUDE.md")

    # Also copy skills directory (symlink to save space)
    skills_src = PROJECT_ROOT / "skills"
    skills_dst = workspace / "skills"
    if skills_src.exists() and not skills_dst.exists():
        skills_dst.symlink_to(skills_src)

    # Copy examples directory (symlink)
    examples_src = PROJECT_ROOT / "examples"
    examples_dst = workspace / "examples"
    if examples_src.exists() and not examples_dst.exists():
        examples_dst.symlink_to(examples_src)

    print(f"\n{'='*60}")
    print(f"BENCHMARK: {benchmark_id}")
    print(f"Run ID: {run_id}")
    print(f"{'='*60}")
    print(f"Results: {run_dir}")

    # Get timeout from benchmark or use default
    timeout_minutes = benchmark.get('time_limit_minutes', 30)
    timeout_seconds = timeout_minutes * 60

    # Build prompt
    prompt = benchmark.get('prompt', '')
    if not prompt:
        prompt = f"Complete this benchmark task:\n\n{benchmark.get('description', '')}"

    # Execute agent
    print(f"\nExecuting agent (timeout: {timeout_minutes} min)...")
    print("-" * 40)
    exec_result = execute_agent(
        prompt=prompt,
        workspace=workspace,
        timeout=timeout_seconds,
        verbose=verbose
    )

    print(f"Execution: {exec_result['status']}")
    print(f"Duration: {exec_result['duration']:.1f}s")
    print(f"Exit code: {exec_result['exit_code']}")

    # Get files created
    files_created = []
    for f in workspace.rglob("*"):
        if f.is_file():
            files_created.append(str(f.relative_to(workspace)))
    print(f"Files created: {len(files_created)}")

    # Generate transcript
    transcript = parse_claude_output(
        output=exec_result['output'],
        benchmark_id=benchmark_id,
        run_id=run_id,
        prompt=prompt,
        workspace=str(workspace)
    )
    transcript.complete(
        files_created=files_created,
        exit_code=exec_result['exit_code'],
        final_result=exec_result['output'][:5000] if exec_result['output'] else None
    )

    # Save transcript
    transcript.save(run_dir / "transcript.json")
    with open(run_dir / "transcript.md", 'w') as f:
        f.write(transcript.to_markdown())

    # Grade the result
    print(f"\nGrading with {grading_mode} grader (threshold: {pass_threshold})...")
    grading_start = time.time()

    if grading_mode == "llm":
        grading_result = grade_with_llm_agent(workspace, benchmark, verbose)
    else:
        # Fallback to simple grading
        grading_result = {
            'score': 50,  # Placeholder
            'reasoning': 'Rule-based grading not implemented',
            'grader': 'rules'
        }

    grading_duration = time.time() - grading_start
    score = grading_result.get('score', 0)
    status = "passed" if score >= pass_threshold else "failed"

    if exec_result['status'] == 'timeout':
        status = 'timeout'
    elif exec_result['status'] == 'error':
        status = 'error'

    print(f"Score: {score:.1f}/100")
    print(f"Status: {status.upper()}")

    # Create grading audit
    audit = create_audit_from_benchmark(benchmark, run_id)
    audit.grader_type = grading_mode

    # Add grading results to audit categories
    categories = grading_result.get('categories', {})
    for cat in audit.categories:
        if cat.name in categories:
            cat_result = categories[cat.name]
            # Create a summary check for this category
            check = CheckAudit(
                check_id=f"{cat.name}_overall",
                check_description=f"Overall {cat.name} assessment",
                category=cat.name,
                check_type="llm_evaluate",
                validation_rule="LLM assessment",
                result=CheckResult.PASS if cat_result.get('score', 0) >= 60 else CheckResult.FAIL,
                points_possible=cat.weight,
                points_earned=int(cat_result.get('score', 0) * cat.weight / 100),
                reasoning=cat_result.get('notes', '')
            )
            cat.checks.append(check)

    audit.complete()

    # Save audit
    audit.save(run_dir / "grading_audit.json")
    with open(run_dir / "grading_audit.md", 'w') as f:
        f.write(audit.to_markdown())

    # Save overall grading result
    with open(run_dir / "grading_result.json", 'w') as f:
        json.dump(grading_result, f, indent=2)

    # Create run metadata
    run = BenchmarkRun(
        benchmark_id=benchmark_id,
        run_id=run_id,
        timestamp=datetime.now().isoformat(),
        status=status,
        score=score,
        pass_threshold=pass_threshold,
        execution_duration_seconds=exec_result['duration'],
        grading_duration_seconds=grading_duration,
        files_created=files_created,
        num_turns=len(transcript.turns),
        num_tool_calls=sum(len(t.tool_calls) for t in transcript.turns),
        error_message=exec_result.get('stderr') if status in ('error', 'timeout') else None,
        exit_code=exec_result['exit_code']
    )

    # Save metadata
    with open(run_dir / "metadata.json", 'w') as f:
        json.dump(asdict(run), f, indent=2)

    # Save benchmark definition
    with open(run_dir / "benchmark.yaml", 'w') as f:
        yaml.dump(benchmark, f, default_flow_style=False)

    # Print assessment
    if grading_result.get('reasoning'):
        print(f"Assessment: {grading_result['reasoning'][:200]}...")

    print(f"Results saved: {run_dir}")
    print(f"\nFinal status: {status}")

    return run


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="Run benchmarks with full observability")
    parser.add_argument("benchmark", nargs="?", help="Benchmark ID (e.g., BENCH-T1-001)")
    parser.add_argument("--tier", type=int, help="Run all benchmarks in tier")
    parser.add_argument("--list", action="store_true", help="List available benchmarks")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--grading-mode", choices=["llm", "rules", "hybrid"],
                       default="llm", help="Grading mode")
    parser.add_argument("--inspect", action="store_true", help="Open results directory after run")

    args = parser.parse_args()

    if args.list:
        benchmarks = list_benchmarks(tier=args.tier)
        print(f"Available benchmarks ({len(benchmarks)} total):\n")
        current_tier = None
        for b in benchmarks:
            tier = b.get('tier', 0)
            if tier != current_tier:
                print(f"\n--- Tier {tier} ---")
                current_tier = tier
            print(f"  {b['id']}: {b.get('name', 'Unnamed')}")
        return

    if args.tier:
        benchmarks = list_benchmarks(tier=args.tier)
        print(f"Running {len(benchmarks)} benchmarks in Tier {args.tier}")
        results = []
        for b in benchmarks:
            result = run_benchmark(
                b['id'],
                verbose=args.verbose,
                grading_mode=args.grading_mode
            )
            results.append(result)

        # Summary
        passed = sum(1 for r in results if r.status == "passed")
        print(f"\n{'='*60}")
        print(f"TIER {args.tier} SUMMARY: {passed}/{len(results)} passed")
        print(f"{'='*60}")
        return

    if args.benchmark:
        result = run_benchmark(
            args.benchmark,
            verbose=args.verbose,
            grading_mode=args.grading_mode
        )

        if args.inspect:
            run_dir = RESULTS_DIR / f"{result.benchmark_id}-{result.run_id}"
            print(f"\nOpening: {run_dir}")
            subprocess.run(["xdg-open", str(run_dir)])
        return

    parser.print_help()


if __name__ == "__main__":
    main()
