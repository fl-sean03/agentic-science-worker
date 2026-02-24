#!/usr/bin/env python3
"""
Benchmark Harness for Agentic Science Worker

Spawns coding agents to execute benchmarks. Supports multiple backends:
- Claude Code (default)
- OpenAI Codex (planned)
- Aider (planned)

Usage:
    python harness.py BENCH-T1-001           # Run single benchmark
    python harness.py --tier 1               # Run all Tier 1
    python harness.py --list                 # List benchmarks
    python harness.py --verify               # Verify infrastructure
    python harness.py --backend claude       # Use specific backend
"""

import json
import os
import re
import shutil
import subprocess
import sys
import time
import yaml
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

# Import graders
from grader import BenchmarkGrader, GradingResult
from llm_grader import grade_with_llm, LLMGradeResult

# Import backends
try:
    from backends import get_backend, BACKENDS
except ImportError:
    # Fallback if backends not available
    BACKENDS = {'claude': None}
    def get_backend(name='claude'):
        return None


# ============================================================================
# Pass thresholds by tier
# ============================================================================

PASS_THRESHOLDS = {
    1: 70,  # Basic tasks should be mostly correct
    2: 65,  # Multi-skill allows some slack
    3: 60,  # Advanced workflows may have partial success
    4: 60,  # Research tasks reward partial progress
    5: 60,  # HPC fundamentals - new skill, allow learning
    6: 55,  # HPC-scale research - complex, async
    7: 50,  # Research campaigns - multi-day, partial credit
    8: 60,  # ML-powered materials - new capability
    9: 50,  # Autonomous research - complex workflows
    10: 40, # Frontier challenges - partial progress valuable
    11: 35, # HPC + ML hybrid - frontier, multi-resource coordination
    12: 50, # Theory synthesis - new Theorizer integration
    13: 60, # Robustness - agent should handle edge cases well
    14: 65, # Compute decision - agent should make good compute choices
    15: 60, # Agent cognition - planning, reasoning, self-reflection
    16: 70, # Scientific rigor - safety/reproducibility must be high
    17: 60, # Cloud GPU - VAST.ai instance management
    18: 60, # Data analysis - parsing and processing simulation output
}


# ============================================================================
# Configuration
# ============================================================================

PROJECT_ROOT = Path(__file__).parent.parent.parent
BENCHMARKS_DIR = PROJECT_ROOT / "benchmarks"
TASKS_DIR = BENCHMARKS_DIR / "tasks"
RESULTS_DIR = BENCHMARKS_DIR / "results" / "runs"
WORKSPACES_DIR = PROJECT_ROOT / "workspaces" / "benchmarks"

# Agent configuration
DEFAULT_MAX_TURNS = 50
DEFAULT_TIMEOUT_SECONDS = 1800  # 30 minutes
ALLOWED_TOOLS = [
    "Bash", "Read", "Write", "Edit", "Glob", "Grep",
    "WebSearch", "WebFetch", "TodoWrite"
]


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class BenchmarkResult:
    """Result from a benchmark run."""
    benchmark_id: str
    run_id: str
    timestamp: str
    status: str  # "passed", "failed", "timeout", "error"

    # Timing
    duration_seconds: float = 0.0

    # Agent output
    agent_output: str = ""
    agent_json: Dict = field(default_factory=dict)

    # Workspace
    workspace_path: str = ""
    files_created: List[str] = field(default_factory=list)

    # Grading results (NEW)
    score: float = 0.0
    max_score: float = 100.0
    pass_threshold: float = 70.0
    grading_details: Dict = field(default_factory=dict)

    # Errors
    error_message: Optional[str] = None
    stderr: str = ""
    exit_code: int = 0


# ============================================================================
# Benchmark Loader
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


# ============================================================================
# Workspace Management
# ============================================================================

def create_workspace(benchmark_id: str, run_id: str) -> Path:
    """Create a clean workspace for the benchmark run."""
    workspace = WORKSPACES_DIR / f"{benchmark_id}-{run_id}"
    if workspace.exists():
        shutil.rmtree(workspace)
    workspace.mkdir(parents=True)
    return workspace


def get_workspace_files(workspace: Path) -> List[str]:
    """List all files in workspace."""
    files = []
    for f in workspace.rglob("*"):
        if f.is_file():
            files.append(str(f.relative_to(workspace)))
    return files


# ============================================================================
# Agent Execution
# ============================================================================

def run_agent(
    prompt: str,
    workspace: Path,
    max_turns: int = DEFAULT_MAX_TURNS,
    timeout: int = DEFAULT_TIMEOUT_SECONDS,
    verbose: bool = False
) -> Dict[str, Any]:
    """
    Spawn a Claude Code agent to execute the task.

    Uses ~/.claude credentials (subscription-based auth).
    """

    # Build command
    # Note: No --cwd option in claude CLI - use subprocess cwd instead
    # Pass prompt via stdin to handle special characters
    cmd = [
        "claude",
        "-p",  # Print mode (non-interactive)
        "--output-format", "json",
        "--dangerously-skip-permissions",  # Full autonomy
        "--allowedTools", ",".join(ALLOWED_TOOLS),
    ]

    if verbose:
        print(f"  Command: {' '.join(cmd)}...")
        print(f"  Workspace: {workspace}")
        print(f"  Max turns: {max_turns}")
        print(f"  Timeout: {timeout}s")

    start_time = time.time()

    try:
        result = subprocess.run(
            cmd,
            input=prompt,  # Pass prompt via stdin
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(PROJECT_ROOT),
            env={**os.environ, "HOME": os.environ.get("HOME")}
        )

        elapsed = time.time() - start_time

        # Try to parse JSON output
        agent_json = {}
        try:
            agent_json = json.loads(result.stdout)
        except json.JSONDecodeError:
            pass

        return {
            "status": "success" if result.returncode == 0 else "failed",
            "stdout": result.stdout,
            "stderr": result.stderr,
            "exit_code": result.returncode,
            "elapsed": elapsed,
            "agent_json": agent_json
        }

    except subprocess.TimeoutExpired as e:
        elapsed = time.time() - start_time
        return {
            "status": "timeout",
            "stdout": e.stdout or "",
            "stderr": e.stderr or f"Timeout after {timeout}s",
            "exit_code": -1,
            "elapsed": elapsed,
            "agent_json": {}
        }

    except Exception as e:
        elapsed = time.time() - start_time
        return {
            "status": "error",
            "stdout": "",
            "stderr": str(e),
            "exit_code": -1,
            "elapsed": elapsed,
            "agent_json": {}
        }


# ============================================================================
# Benchmark Runner
# ============================================================================

def run_benchmark(
    benchmark_id: str,
    verbose: bool = False,
    save_results: bool = True,
    backend_name: str = "claude"
) -> BenchmarkResult:
    """Run a single benchmark."""

    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    timestamp = datetime.now().isoformat()

    print(f"\n{'='*60}")
    print(f"BENCHMARK: {benchmark_id}")
    print(f"Run ID: {run_id}")
    print(f"{'='*60}")

    # Load benchmark
    try:
        benchmark = load_benchmark(benchmark_id)
    except ValueError as e:
        return BenchmarkResult(
            benchmark_id=benchmark_id,
            run_id=run_id,
            timestamp=timestamp,
            status="error",
            error_message=str(e)
        )

    # Create workspace
    workspace = create_workspace(benchmark_id, run_id)
    print(f"Workspace: {workspace}")

    # Strip any hardcoded "Work in:" paths from the benchmark prompt
    # to avoid conflicts with our injected workspace
    task_prompt = benchmark['prompt']
    task_prompt = re.sub(r'\n\s*Work in:.*\n', '\n', task_prompt)
    task_prompt = re.sub(r'\n\s*Save.*to:.*workspaces/.*\n', '\n', task_prompt)

    # Build prompt with workspace context
    prompt = f"""You are executing benchmark task: {benchmark_id}

CRITICAL - WORKSPACE DIRECTORY: {workspace}
ALL files MUST be created directly in this directory or its subdirectories.
Do NOT use any other path. The workspace path is: {workspace}

TASK:
{task_prompt}

IMPORTANT REQUIREMENTS:
- Create ALL files in {workspace} (not any other directory)
- You may create subdirectories within the workspace if needed
- Complete the full task before finishing
- Report your results clearly at the end
"""

    # Get timeout from benchmark or use default
    timeout_minutes = benchmark.get('time_limit_minutes', 30)
    timeout_seconds = timeout_minutes * 60

    print(f"\nExecuting with {backend_name} backend (timeout: {timeout_minutes} min)...")
    print("-" * 40)

    # Get backend and run agent
    backend = get_backend(backend_name)
    if backend is None:
        # Fall back to legacy run_agent for Claude
        exec_result = run_agent(
            prompt=prompt,
            workspace=workspace,
            max_turns=benchmark.get('max_turns', DEFAULT_MAX_TURNS),
            timeout=timeout_seconds,
            verbose=verbose
        )
    else:
        exec_result = backend.run(
            prompt=prompt,
            workspace=workspace,
            max_turns=benchmark.get('max_turns', DEFAULT_MAX_TURNS),
            timeout=timeout_seconds,
            allowed_tools=ALLOWED_TOOLS,
            verbose=verbose
        )

    print("-" * 40)
    print(f"Execution: {exec_result['status']}")
    print(f"Duration: {exec_result['elapsed']:.1f}s")
    print(f"Exit code: {exec_result['exit_code']}")

    # Collect files
    files_created = get_workspace_files(workspace)
    print(f"Files created: {len(files_created)}")
    if verbose and files_created:
        for f in files_created[:10]:
            print(f"  - {f}")
        if len(files_created) > 10:
            print(f"  ... and {len(files_created) - 10} more")

    # === GRADING: Validate outputs against benchmark criteria ===
    tier = benchmark.get('tier', 1)
    pass_threshold = PASS_THRESHOLDS.get(tier, 70)

    grading_details = {}
    score = 0.0

    if exec_result['status'] in ('timeout', 'error'):
        # Execution failed - automatic fail
        status = exec_result['status']
        score = 0.0
    else:
        # Use LLM-as-Judge for grading (more robust than rule-based)
        print(f"\nGrading with Claude Code agent (threshold: {pass_threshold})...")
        try:
            llm_result = grade_with_llm(
                benchmark,
                workspace,
                exec_result['stdout'],
                timeout=300  # 5 minutes for thorough grading with tools
            )

            score = llm_result.total_score
            grading_details = {
                'grader': 'llm',
                'categories': llm_result.categories or {},
                'reasoning': llm_result.reasoning,
                'strengths': llm_result.strengths or [],
                'weaknesses': llm_result.weaknesses or [],
                'suggestions': llm_result.suggestions or []
            }

            # Determine pass/fail based on score vs threshold
            if score >= pass_threshold:
                status = "passed"
            else:
                status = "failed"

            print(f"Score: {score:.1f}/100")
            print(f"Status: {status.upper()}")
            if llm_result.reasoning:
                print(f"Assessment: {llm_result.reasoning[:200]}...")

        except Exception as e:
            # LLM grading failed - fall back to rule-based grader
            print(f"LLM grading error: {e}")
            print("Falling back to rule-based grader...")
            try:
                grader = BenchmarkGrader(BENCHMARKS_DIR)
                grading_result = grader.grade(
                    benchmark,
                    workspace,
                    exec_result['stdout']
                )
                score = grading_result.total_score
                grading_details = {
                    'grader': 'rule-based',
                    'categories': [
                        {
                            'name': c.name,
                            'weight': c.weight,
                            'score': c.score,
                            'weighted_score': c.weighted_score
                        }
                        for c in grading_result.categories
                    ]
                }
                status = "passed" if score >= pass_threshold else "failed"
                print(f"Score: {score:.1f}/100")
                print(f"Status: {status.upper()}")
            except Exception as e2:
                print(f"Rule-based grading also failed: {e2}")
                status = "failed" if exec_result['exit_code'] != 0 else "passed"
                grading_details = {'error': str(e), 'fallback_error': str(e2)}

    # Build result
    result = BenchmarkResult(
        benchmark_id=benchmark_id,
        run_id=run_id,
        timestamp=timestamp,
        status=status,
        duration_seconds=exec_result['elapsed'],
        agent_output=exec_result['stdout'],
        agent_json=exec_result['agent_json'],
        workspace_path=str(workspace),
        files_created=files_created,
        score=score,
        max_score=100.0,
        pass_threshold=pass_threshold,
        grading_details=grading_details,
        stderr=exec_result['stderr'],
        exit_code=exec_result['exit_code'],
        error_message=exec_result['stderr'] if exec_result['status'] == 'error' else None
    )

    # Save results
    if save_results:
        save_benchmark_result(result, benchmark)

    return result


def save_benchmark_result(result: BenchmarkResult, benchmark: Dict):
    """Save benchmark result to disk."""
    result_dir = RESULTS_DIR / f"{result.benchmark_id}-{result.run_id}"
    result_dir.mkdir(parents=True, exist_ok=True)

    # Save result metadata
    with open(result_dir / "result.json", 'w') as f:
        json.dump(asdict(result), f, indent=2, default=str)

    # Save benchmark definition
    with open(result_dir / "benchmark.json", 'w') as f:
        json.dump(benchmark, f, indent=2)

    # Save agent output separately for easy reading
    with open(result_dir / "agent_output.txt", 'w') as f:
        f.write(result.agent_output)

    if result.stderr:
        with open(result_dir / "stderr.txt", 'w') as f:
            f.write(result.stderr)

    print(f"Results saved: {result_dir}")


def run_tier(tier: int, verbose: bool = False, backend_name: str = "claude") -> List[BenchmarkResult]:
    """Run all benchmarks in a tier."""
    benchmarks = list_benchmarks(tier=tier)
    results = []

    print(f"\n{'#'*60}")
    print(f"TIER {tier} BENCHMARKS ({len(benchmarks)} tasks)")
    print(f"{'#'*60}")

    for bench in benchmarks:
        result = run_benchmark(bench['id'], verbose=verbose, backend_name=backend_name)
        results.append(result)

    # Print summary
    print_tier_summary(tier, results)
    return results


def print_tier_summary(tier: int, results: List[BenchmarkResult]):
    """Print summary of tier results."""
    print(f"\n{'='*60}")
    print(f"TIER {tier} SUMMARY")
    print(f"{'='*60}")

    passed = sum(1 for r in results if r.status == "passed")
    failed = sum(1 for r in results if r.status == "failed")
    errors = sum(1 for r in results if r.status in ("error", "timeout"))
    total_time = sum(r.duration_seconds for r in results)
    avg_score = sum(r.score for r in results) / len(results) if results else 0

    print(f"Total: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Errors/Timeouts: {errors}")
    print(f"Pass rate: {passed/len(results)*100:.1f}%")
    print(f"Average score: {avg_score:.1f}/100")
    print(f"Total time: {total_time:.1f}s")

    print(f"\nResults by benchmark:")
    for r in results:
        status_icon = "✓" if r.status == "passed" else "✗"
        print(f"  {status_icon} {r.benchmark_id}: {r.status} (score: {r.score:.1f}, time: {r.duration_seconds:.1f}s)")


# ============================================================================
# Infrastructure Verification
# ============================================================================

def verify_infrastructure() -> bool:
    """Verify all required infrastructure is available."""
    print("Verifying infrastructure...")
    print("-" * 40)

    all_ok = True

    # Check Claude CLI
    try:
        result = subprocess.run(["claude", "--version"], capture_output=True, text=True)
        print(f"✓ Claude CLI: available")
    except FileNotFoundError:
        print(f"✗ Claude CLI: NOT FOUND")
        all_ok = False

    # Check LAMMPS (from environment or common locations)
    lmp_path = os.environ.get("LMP") or os.environ.get("LAMMPS_PATH")
    if lmp_path and Path(lmp_path).exists():
        print(f"✓ LAMMPS: {lmp_path}")
    elif shutil.which("lmp"):
        print(f"✓ LAMMPS: {shutil.which('lmp')} (from PATH)")
    else:
        print(f"✗ LAMMPS: NOT FOUND (set LMP or LAMMPS_PATH env var)")
        all_ok = False

    # Check QE (from environment or common locations)
    qe_path = os.environ.get("QE_CPU") or os.environ.get("QE_PATH")
    if qe_path:
        pw_path = Path(qe_path) / "pw.x" if Path(qe_path).is_dir() else Path(qe_path)
        if pw_path.exists():
            print(f"✓ QE: {pw_path}")
        else:
            print(f"✗ QE: NOT FOUND at {qe_path}")
            all_ok = False
    elif shutil.which("pw.x"):
        print(f"✓ QE: {shutil.which('pw.x')} (from PATH)")
    else:
        print(f"⚠ QE: NOT FOUND (set QE_CPU or QE_PATH env var) - DFT benchmarks unavailable")

    # Check Python packages
    try:
        import numpy
        import matplotlib
        print(f"✓ Python packages: numpy, matplotlib")
    except ImportError as e:
        print(f"✗ Python packages: {e}")
        all_ok = False

    # Check directories
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    WORKSPACES_DIR.mkdir(parents=True, exist_ok=True)
    print(f"✓ Directories: results, workspaces")

    # Check benchmarks exist
    benchmarks = list_benchmarks()
    print(f"✓ Benchmarks: {len(benchmarks)} tasks found")

    # Check HPC access (optional)
    print(f"\nHPC Infrastructure (optional):")
    try:
        hpc_result = subprocess.run(
            ["ssh", "-o", "BatchMode=yes", "-o", "ConnectTimeout=5", "cu_alpine", "echo HPC_OK"],
            capture_output=True,
            text=True,
            timeout=10
        )
        if "HPC_OK" in hpc_result.stdout:
            print(f"✓ HPC SSH: cu_alpine accessible")
            # Check for SLURM
            slurm_result = subprocess.run(
                ["ssh", "cu_alpine", "which squeue"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if slurm_result.returncode == 0:
                print(f"✓ HPC SLURM: squeue available")
            else:
                print(f"⚠ HPC SLURM: not found (HPC benchmarks may fail)")
        else:
            print(f"⚠ HPC SSH: connection failed (HPC benchmarks unavailable)")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print(f"⚠ HPC SSH: not configured (HPC benchmarks unavailable)")

    # Check ML packages (optional for ML tiers)
    print(f"\nML Infrastructure (optional):")
    ml_packages = {
        'mace': 'MACE universal potential',
        'matgl': 'MatGL (M3GNet, CHGNet)',
        'chgnet': 'CHGNet model',
        'phonopy': 'Phonon calculations',
        'ase': 'Atomic Simulation Environment'
    }
    ml_available = True
    for pkg, desc in ml_packages.items():
        try:
            __import__(pkg)
            print(f"✓ {pkg}: {desc}")
        except ImportError:
            print(f"⚠ {pkg}: NOT INSTALLED ({desc})")
            ml_available = False

    # Check GPU for ML
    try:
        import torch
        if torch.cuda.is_available():
            gpu_name = torch.cuda.get_device_name(0)
            gpu_mem = torch.cuda.get_device_properties(0).total_memory / 1e9
            print(f"✓ GPU: {gpu_name} ({gpu_mem:.1f} GB)")
        else:
            print(f"⚠ GPU: CUDA not available (ML benchmarks will be slow)")
    except ImportError:
        print(f"⚠ PyTorch: NOT INSTALLED")

    print("-" * 40)
    if all_ok:
        print("Infrastructure verification PASSED")
        print("Note: HPC access is optional for Tiers 1-4")
    else:
        print("Infrastructure verification FAILED")

    return all_ok


# ============================================================================
# CLI Interface
# ============================================================================

def cleanup_old_workspaces(keep_latest: int = 3, dry_run: bool = True):
    """Clean up old benchmark workspaces, keeping the N most recent per benchmark."""
    from collections import defaultdict

    # Group workspaces by benchmark ID
    workspaces_by_bench = defaultdict(list)
    for ws in WORKSPACES_DIR.iterdir():
        if ws.is_dir() and ws.name.startswith("BENCH-"):
            # Extract benchmark ID (e.g., BENCH-T1-001 from BENCH-T1-001-20260117-101100)
            parts = ws.name.split('-')
            if len(parts) >= 3:
                bench_id = '-'.join(parts[:3])
                workspaces_by_bench[bench_id].append(ws)

    removed_count = 0
    freed_bytes = 0

    for bench_id, workspaces in workspaces_by_bench.items():
        # Sort by modification time, newest first
        workspaces.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        # Remove old ones beyond keep_latest
        for ws in workspaces[keep_latest:]:
            # Calculate size
            size = sum(f.stat().st_size for f in ws.rglob('*') if f.is_file())

            if dry_run:
                print(f"  Would remove: {ws.name} ({size / 1024 / 1024:.1f} MB)")
            else:
                shutil.rmtree(ws)
                print(f"  Removed: {ws.name} ({size / 1024 / 1024:.1f} MB)")

            removed_count += 1
            freed_bytes += size

    print(f"\nTotal: {removed_count} workspaces, {freed_bytes / 1024 / 1024:.1f} MB")
    if dry_run and removed_count > 0:
        print("Run with --cleanup --force to actually remove")


def generate_summary_report(all_results: Dict[int, List[BenchmarkResult]]) -> str:
    """Generate a detailed markdown summary report."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines = [
        "# Benchmark Summary Report",
        f"\n**Generated**: {timestamp}\n",
        "---\n",
        "## Overall Statistics\n"
    ]

    total_passed = 0
    total_count = 0
    total_score = 0
    tier_stats = {}

    for tier, results in all_results.items():
        passed = sum(1 for r in results if r.status == "passed")
        avg_score = sum(r.score for r in results) / len(results) if results else 0
        total_passed += passed
        total_count += len(results)
        total_score += sum(r.score for r in results)
        tier_stats[tier] = {"passed": passed, "total": len(results), "avg": avg_score}

    overall_avg = total_score / total_count if total_count else 0
    pass_rate = (total_passed / total_count * 100) if total_count else 0

    lines.extend([
        f"| Metric | Value |",
        f"|--------|-------|",
        f"| Total Benchmarks | {total_count} |",
        f"| Passed | {total_passed} |",
        f"| Pass Rate | {pass_rate:.1f}% |",
        f"| Average Score | {overall_avg:.1f}/100 |",
        "\n## Results by Tier\n",
        "| Tier | Passed | Total | Pass Rate | Avg Score |",
        "|------|--------|-------|-----------|-----------|"
    ])

    for tier in sorted(tier_stats.keys()):
        stats = tier_stats[tier]
        rate = (stats["passed"] / stats["total"] * 100) if stats["total"] else 0
        lines.append(f"| Tier {tier} | {stats['passed']} | {stats['total']} | {rate:.1f}% | {stats['avg']:.1f} |")

    lines.append("\n## Detailed Results\n")

    for tier in sorted(all_results.keys()):
        lines.append(f"### Tier {tier}\n")
        for result in all_results[tier]:
            status_icon = "✅" if result.status == "passed" else "❌"
            lines.append(f"#### {status_icon} {result.benchmark_id}\n")
            lines.append(f"- **Status**: {result.status.upper()}")
            lines.append(f"- **Score**: {result.score:.1f}/100 (threshold: {result.pass_threshold})")
            lines.append(f"- **Duration**: {result.duration_seconds:.1f}s")

            if result.grading_details:
                if 'reasoning' in result.grading_details:
                    lines.append(f"- **Assessment**: {result.grading_details['reasoning']}")

                if 'categories' in result.grading_details and result.grading_details['categories']:
                    lines.append("\n**Category Scores:**\n")
                    lines.append("| Category | Score | Weight |")
                    lines.append("|----------|-------|--------|")
                    for cat, data in result.grading_details['categories'].items():
                        if isinstance(data, dict):
                            score = data.get('score', 0)
                            weight = data.get('weight', 0)
                            lines.append(f"| {cat} | {score:.0f} | {weight}% |")

                if 'strengths' in result.grading_details and result.grading_details['strengths']:
                    lines.append("\n**Strengths:**")
                    for s in result.grading_details['strengths']:
                        lines.append(f"- {s}")

                if 'weaknesses' in result.grading_details and result.grading_details['weaknesses']:
                    lines.append("\n**Weaknesses:**")
                    for w in result.grading_details['weaknesses']:
                        lines.append(f"- {w}")

            lines.append("")

    return "\n".join(lines)


def run_all_tiers(verbose: bool = False, save_report: bool = True,
                  include_hpc: bool = False, include_ml: bool = False,
                  include_hpc_ml: bool = False, backend_name: str = "claude"):
    """Run all benchmarks across all tiers.

    Args:
        verbose: Enable verbose output
        save_report: Save summary report to disk
        include_hpc: Include HPC tiers (5, 6, 7) - requires HPC access
        include_ml: Include ML tiers (8, 9, 10) - requires MLIP packages
        include_hpc_ml: Include HPC+ML hybrid tier (11) - requires both
        backend_name: Agent backend to use (default: claude)
    """
    all_results = {}

    # Core tiers (local execution)
    tiers = [1, 2, 3, 4]

    # Add HPC tiers if requested
    if include_hpc:
        tiers.extend([5, 6, 7])

    # Add ML tiers if requested
    if include_ml:
        tiers.extend([8, 9, 10])

    # Add HPC+ML hybrid tier if requested (requires both HPC and ML)
    if include_hpc_ml:
        tiers.append(11)

    for tier in tiers:
        results = run_tier(tier, verbose=verbose, backend_name=backend_name)
        all_results[tier] = results

    # Print overall summary
    print(f"\n{'#'*60}")
    print("OVERALL BENCHMARK SUMMARY")
    print(f"{'#'*60}")

    total_passed = 0
    total_failed = 0
    total_errors = 0
    total_score = 0
    total_count = 0

    for tier, results in all_results.items():
        passed = sum(1 for r in results if r.status == "passed")
        failed = sum(1 for r in results if r.status == "failed")
        errors = sum(1 for r in results if r.status in ("error", "timeout"))
        avg_score = sum(r.score for r in results) / len(results) if results else 0

        total_passed += passed
        total_failed += failed
        total_errors += errors
        total_score += sum(r.score for r in results)
        total_count += len(results)

        print(f"\nTier {tier}: {passed}/{len(results)} passed ({avg_score:.1f} avg)")

    print(f"\n{'='*60}")
    overall_avg = total_score / total_count if total_count else 0
    print(f"TOTAL: {total_passed}/{total_count} passed ({total_passed/total_count*100:.1f}%)")
    print(f"Average Score: {overall_avg:.1f}/100")
    print(f"{'='*60}")

    # Save summary report
    if save_report:
        report = generate_summary_report(all_results)
        report_path = RESULTS_DIR / f"summary-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"
        report_path.parent.mkdir(parents=True, exist_ok=True)
        with open(report_path, 'w') as f:
            f.write(report)
        print(f"\nSummary report saved: {report_path}")


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Benchmark Harness for Agentic Science Worker"
    )
    parser.add_argument(
        "benchmark_id",
        nargs="?",
        help="Benchmark ID to run (e.g., BENCH-T1-001)"
    )
    parser.add_argument(
        "--tier",
        type=int,
        choices=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
        help="Run all benchmarks in a tier"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all benchmarks across all tiers"
    )
    parser.add_argument(
        "--list",
        action="store_true",
        help="List available benchmarks"
    )
    parser.add_argument(
        "--verify",
        action="store_true",
        help="Verify infrastructure"
    )
    parser.add_argument(
        "--cleanup",
        action="store_true",
        help="Clean up old workspaces (keeps 3 most recent per benchmark)"
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Actually remove files (with --cleanup)"
    )
    parser.add_argument(
        "--keep",
        type=int,
        default=3,
        help="Number of recent workspaces to keep (default: 3)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--include-hpc",
        action="store_true",
        help="Include HPC tiers (5, 6, 7) when running --all (requires HPC access)"
    )
    parser.add_argument(
        "--include-ml",
        action="store_true",
        help="Include ML tiers (8, 9, 10) when running --all (requires MLIP packages)"
    )
    parser.add_argument(
        "--include-hpc-ml",
        action="store_true",
        help="Include HPC+ML hybrid tier (11) when running --all (requires both HPC and MLIP)"
    )
    parser.add_argument(
        "--async-mode",
        action="store_true",
        help="Enable async mode for HPC benchmarks (check job status, don't wait)"
    )
    parser.add_argument(
        "--backend",
        type=str,
        default="claude",
        choices=list(BACKENDS.keys()),
        help="Agent backend to use (default: claude)"
    )
    parser.add_argument(
        "--list-backends",
        action="store_true",
        help="List available agent backends"
    )

    args = parser.parse_args()

    if args.list_backends:
        print("\nAvailable backends:")
        for name, backend_cls in BACKENDS.items():
            if backend_cls:
                backend = backend_cls()
                status = "ready" if backend.verify() else "not configured"
                print(f"  {name}: {backend.description} ({status})")
            else:
                print(f"  {name}: not implemented")
        return

    if args.verify:
        success = verify_infrastructure()
        sys.exit(0 if success else 1)

    if args.cleanup:
        cleanup_old_workspaces(keep_latest=args.keep, dry_run=not args.force)
        return

    if args.list:
        benchmarks = list_benchmarks(tier=args.tier)
        print(f"\nAvailable benchmarks ({len(benchmarks)} total):\n")
        for bench in benchmarks:
            tier = bench.get('tier', '?')
            name = bench.get('name', 'Unknown')
            difficulty = bench.get('metadata', {}).get('difficulty', 'unknown')
            print(f"  [T{tier}] {bench['id']}: {name} ({difficulty})")
        return

    if args.all:
        run_all_tiers(verbose=args.verbose, include_hpc=args.include_hpc,
                      include_ml=args.include_ml, include_hpc_ml=args.include_hpc_ml,
                      backend_name=args.backend)
    elif args.tier:
        run_tier(args.tier, verbose=args.verbose, backend_name=args.backend)
    elif args.benchmark_id:
        result = run_benchmark(args.benchmark_id, verbose=args.verbose, backend_name=args.backend)
        print(f"\nFinal status: {result.status}")
        if result.error_message:
            print(f"Error: {result.error_message}")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
