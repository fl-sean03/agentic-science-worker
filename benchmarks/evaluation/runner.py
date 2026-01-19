#!/usr/bin/env python3
"""
Benchmark Runner for Agentic Science Worker

Executes benchmarks by sending prompts to Claude Code and collecting results.
Supports both CLI-based and SDK-based execution.
"""

import asyncio
import json
import os
import subprocess
import sys
import time
import yaml
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class CLEARMetrics:
    """CLEAR framework metrics for benchmark evaluation."""
    # Cost
    tokens_used: int = 0
    api_calls: int = 0
    simulation_time_seconds: float = 0.0

    # Latency
    total_time_seconds: float = 0.0
    time_to_first_output: float = 0.0

    # Efficacy
    task_completed: bool = False
    milestones_achieved: List[str] = field(default_factory=list)
    milestone_completion: float = 0.0

    # Assurance
    parameters_validated: bool = False
    sources_cited: bool = False
    safety_checks_passed: bool = True

    # Reliability (filled by multi-run analysis)
    consistency_rate: Optional[float] = None


@dataclass
class BenchmarkResult:
    """Complete result from a benchmark run."""
    benchmark_id: str
    run_id: str
    timestamp: str

    # Execution info
    status: str  # "completed", "failed", "timeout", "error"
    error_message: Optional[str] = None

    # Agent outputs
    agent_response: str = ""
    files_created: List[str] = field(default_factory=list)
    extracted_values: Dict[str, Any] = field(default_factory=dict)

    # Grading
    score: float = 0.0
    max_score: float = 100.0
    grading_details: Dict[str, Any] = field(default_factory=dict)

    # CLEAR metrics
    clear_metrics: CLEARMetrics = field(default_factory=CLEARMetrics)


# ============================================================================
# Benchmark Loader
# ============================================================================

class BenchmarkLoader:
    """Load and validate benchmark definitions."""

    def __init__(self, benchmarks_dir: Path):
        self.benchmarks_dir = benchmarks_dir
        self.tasks_dir = benchmarks_dir / "tasks"

    def load_benchmark(self, benchmark_id: str) -> Dict[str, Any]:
        """Load a benchmark by ID."""
        # Search through tier directories
        for tier_dir in self.tasks_dir.iterdir():
            if not tier_dir.is_dir():
                continue
            for bench_file in tier_dir.glob("*.yaml"):
                with open(bench_file) as f:
                    bench = yaml.safe_load(f)
                if bench.get('id') == benchmark_id:
                    bench['_source_file'] = str(bench_file)
                    return bench

        raise ValueError(f"Benchmark not found: {benchmark_id}")

    def list_benchmarks(self, tier: Optional[int] = None) -> List[Dict[str, Any]]:
        """List all available benchmarks."""
        benchmarks = []

        for tier_dir in sorted(self.tasks_dir.iterdir()):
            if not tier_dir.is_dir():
                continue

            # Filter by tier if specified
            if tier is not None:
                tier_name = f"tier{tier}"
                if tier_name not in tier_dir.name:
                    continue

            for bench_file in sorted(tier_dir.glob("*.yaml")):
                with open(bench_file) as f:
                    bench = yaml.safe_load(f)
                bench['_source_file'] = str(bench_file)
                benchmarks.append(bench)

        return benchmarks


# ============================================================================
# Workspace Manager
# ============================================================================

class WorkspaceManager:
    """Manage benchmark workspaces."""

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir
        self.workspaces_dir = base_dir / "workspaces" / "benchmarks"

    def create_workspace(self, benchmark_id: str, run_id: str) -> Path:
        """Create a clean workspace for a benchmark run."""
        workspace = self.workspaces_dir / f"{benchmark_id}-{run_id}"

        # Clean up if exists
        if workspace.exists():
            import shutil
            shutil.rmtree(workspace)

        workspace.mkdir(parents=True)
        return workspace

    def get_created_files(self, workspace: Path) -> List[str]:
        """List all files created in workspace."""
        files = []
        for f in workspace.rglob("*"):
            if f.is_file():
                files.append(str(f.relative_to(workspace)))
        return files


# ============================================================================
# Agent Executor
# ============================================================================

class AgentExecutor:
    """Execute benchmarks by sending prompts to Claude Code."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def execute_cli(
        self,
        prompt: str,
        workspace: Path,
        timeout_seconds: int = 3600
    ) -> Dict[str, Any]:
        """Execute benchmark using Claude Code CLI."""

        # Build the full prompt with workspace context
        full_prompt = f"""
You are executing a benchmark task. Work in the directory: {workspace}

{prompt}

IMPORTANT:
- Create all files in the specified workspace directory
- Complete the task fully before responding
- Report your final results clearly
"""

        start_time = time.time()

        try:
            # Execute claude CLI with the prompt
            result = subprocess.run(
                [
                    "claude",
                    "--print",
                    "--output-format", "json",
                    "--max-turns", "50",
                    "--cwd", str(self.project_dir),
                    prompt
                ],
                capture_output=True,
                text=True,
                timeout=timeout_seconds,
                cwd=str(self.project_dir)
            )

            elapsed = time.time() - start_time

            # Parse output
            try:
                output_data = json.loads(result.stdout)
            except json.JSONDecodeError:
                output_data = {"raw_output": result.stdout}

            return {
                "status": "completed" if result.returncode == 0 else "failed",
                "output": output_data,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode,
                "elapsed_seconds": elapsed,
                "error": None
            }

        except subprocess.TimeoutExpired:
            elapsed = time.time() - start_time
            return {
                "status": "timeout",
                "output": None,
                "stdout": "",
                "stderr": f"Timeout after {timeout_seconds}s",
                "returncode": -1,
                "elapsed_seconds": elapsed,
                "error": "Execution timeout"
            }

        except Exception as e:
            elapsed = time.time() - start_time
            return {
                "status": "error",
                "output": None,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1,
                "elapsed_seconds": elapsed,
                "error": str(e)
            }

    async def execute_sdk(
        self,
        prompt: str,
        workspace: Path,
        timeout_seconds: int = 3600
    ) -> Dict[str, Any]:
        """Execute benchmark using Claude Agent SDK (if available)."""

        try:
            from claude_code_sdk import query, ClaudeCodeOptions

            start_time = time.time()

            # Configure options
            options = ClaudeCodeOptions(
                allowed_tools=["Bash", "Write", "Read", "Edit", "Glob", "Grep"],
                max_turns=50,
                cwd=str(workspace)
            )

            # Execute
            result = await query(prompt=prompt, options=options)

            elapsed = time.time() - start_time

            return {
                "status": "completed",
                "output": result.output if hasattr(result, 'output') else str(result),
                "tool_calls": result.tool_calls if hasattr(result, 'tool_calls') else [],
                "tokens_used": result.tokens_used if hasattr(result, 'tokens_used') else 0,
                "elapsed_seconds": elapsed,
                "error": None
            }

        except ImportError:
            return {
                "status": "error",
                "output": None,
                "elapsed_seconds": 0,
                "error": "Claude Code SDK not installed. Use CLI execution."
            }

        except Exception as e:
            return {
                "status": "error",
                "output": None,
                "elapsed_seconds": 0,
                "error": str(e)
            }


# ============================================================================
# Benchmark Runner
# ============================================================================

class BenchmarkRunner:
    """Main runner for executing benchmarks."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir
        self.benchmarks_dir = project_dir / "benchmarks"

        self.loader = BenchmarkLoader(self.benchmarks_dir)
        self.workspace_mgr = WorkspaceManager(project_dir)
        self.executor = AgentExecutor(project_dir)

        # Results directory
        self.results_dir = self.benchmarks_dir / "results" / "runs"
        self.results_dir.mkdir(parents=True, exist_ok=True)

    def run_benchmark(
        self,
        benchmark_id: str,
        use_sdk: bool = False,
        save_results: bool = True
    ) -> BenchmarkResult:
        """Run a single benchmark."""

        # Generate run ID
        run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
        timestamp = datetime.now().isoformat()

        print(f"\n{'='*60}")
        print(f"Running benchmark: {benchmark_id}")
        print(f"Run ID: {run_id}")
        print(f"{'='*60}\n")

        # Load benchmark definition
        try:
            benchmark = self.loader.load_benchmark(benchmark_id)
        except ValueError as e:
            return BenchmarkResult(
                benchmark_id=benchmark_id,
                run_id=run_id,
                timestamp=timestamp,
                status="error",
                error_message=str(e)
            )

        # Create workspace
        workspace = self.workspace_mgr.create_workspace(benchmark_id, run_id)
        print(f"Workspace: {workspace}")

        # Get timeout
        timeout_minutes = benchmark.get('time_limit_minutes', 30)
        timeout_seconds = timeout_minutes * 60

        # Execute
        print(f"\nExecuting benchmark (timeout: {timeout_minutes} min)...")
        print("-" * 40)

        if use_sdk:
            exec_result = asyncio.run(
                self.executor.execute_sdk(
                    benchmark['prompt'],
                    workspace,
                    timeout_seconds
                )
            )
        else:
            exec_result = self.executor.execute_cli(
                benchmark['prompt'],
                workspace,
                timeout_seconds
            )

        print("-" * 40)
        print(f"Execution status: {exec_result['status']}")
        print(f"Elapsed time: {exec_result['elapsed_seconds']:.1f}s")

        # Collect created files
        files_created = self.workspace_mgr.get_created_files(workspace)
        print(f"Files created: {len(files_created)}")

        # Build result
        result = BenchmarkResult(
            benchmark_id=benchmark_id,
            run_id=run_id,
            timestamp=timestamp,
            status=exec_result['status'],
            error_message=exec_result.get('error'),
            agent_response=exec_result.get('stdout', ''),
            files_created=files_created,
            clear_metrics=CLEARMetrics(
                total_time_seconds=exec_result['elapsed_seconds'],
                tokens_used=exec_result.get('tokens_used', 0)
            )
        )

        # Save results
        if save_results:
            self._save_result(result, benchmark)

        return result

    def run_tier(self, tier: int, use_sdk: bool = False) -> List[BenchmarkResult]:
        """Run all benchmarks in a tier."""
        benchmarks = self.loader.list_benchmarks(tier=tier)
        results = []

        print(f"\n{'#'*60}")
        print(f"Running Tier {tier} benchmarks ({len(benchmarks)} tasks)")
        print(f"{'#'*60}")

        for bench in benchmarks:
            result = self.run_benchmark(bench['id'], use_sdk=use_sdk)
            results.append(result)

        # Print summary
        self._print_tier_summary(tier, results)
        return results

    def _save_result(self, result: BenchmarkResult, benchmark: Dict):
        """Save benchmark result to disk."""
        result_file = self.results_dir / f"{result.benchmark_id}-{result.run_id}.json"

        data = {
            "result": asdict(result),
            "benchmark": benchmark
        }

        with open(result_file, 'w') as f:
            json.dump(data, f, indent=2, default=str)

        print(f"Result saved: {result_file}")

    def _print_tier_summary(self, tier: int, results: List[BenchmarkResult]):
        """Print summary of tier results."""
        print(f"\n{'='*60}")
        print(f"TIER {tier} SUMMARY")
        print(f"{'='*60}")

        completed = sum(1 for r in results if r.status == "completed")
        failed = sum(1 for r in results if r.status == "failed")
        errors = sum(1 for r in results if r.status in ("error", "timeout"))

        print(f"Total: {len(results)}")
        print(f"Completed: {completed}")
        print(f"Failed: {failed}")
        print(f"Errors/Timeouts: {errors}")
        print(f"Success rate: {completed/len(results)*100:.1f}%")


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Run benchmarks for the Agentic Science Worker"
    )
    parser.add_argument(
        "benchmark_id",
        nargs="?",
        help="Benchmark ID to run (e.g., BENCH-T1-001)"
    )
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
        help="Run all benchmarks in a tier"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available benchmarks"
    )
    parser.add_argument(
        "--use-sdk",
        action="store_true",
        help="Use Claude Agent SDK instead of CLI"
    )
    parser.add_argument(
        "--project-dir",
        type=Path,
        default=Path(__file__).parent.parent.parent,
        help="Project directory"
    )

    args = parser.parse_args()

    runner = BenchmarkRunner(args.project_dir)

    if args.list:
        # List benchmarks
        benchmarks = runner.loader.list_benchmarks(tier=args.tier)
        print(f"\nAvailable benchmarks ({len(benchmarks)} total):\n")
        for bench in benchmarks:
            tier = bench.get('tier', '?')
            name = bench.get('name', 'Unknown')
            difficulty = bench.get('metadata', {}).get('difficulty', 'unknown')
            print(f"  [{tier}] {bench['id']}: {name} ({difficulty})")
        return

    if args.tier:
        # Run tier
        runner.run_tier(args.tier, use_sdk=args.use_sdk)
    elif args.benchmark_id:
        # Run single benchmark
        result = runner.run_benchmark(args.benchmark_id, use_sdk=args.use_sdk)
        print(f"\nFinal status: {result.status}")
        if result.error_message:
            print(f"Error: {result.error_message}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
