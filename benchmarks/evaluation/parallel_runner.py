#!/usr/bin/env python3
"""
Parallel Benchmark Runner

Runs multiple benchmarks in parallel using subprocess workers.
Each benchmark runs in its own Claude Code instance.

Usage:
    # Run all benchmarks with 5 parallel workers
    python parallel_runner.py --all --workers 5

    # Run specific tier with 10 workers
    python parallel_runner.py --tier 15 --workers 10

    # Run specific benchmarks
    python parallel_runner.py BENCH-T1-001 BENCH-T1-002 BENCH-T1-003 --workers 3
"""

import argparse
import subprocess
import sys
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from datetime import datetime
import json

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent))
from harness import list_benchmarks, RESULTS_DIR


def run_single_benchmark(benchmark_id: str, verbose: bool = False) -> dict:
    """Run a single benchmark in a subprocess."""
    start_time = time.time()

    cmd = [
        sys.executable,
        str(Path(__file__).parent / "harness.py"),
        benchmark_id
    ]
    if verbose:
        cmd.append("--verbose")

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=86400  # 24 hours max
        )

        elapsed = time.time() - start_time

        # Try to extract score from output
        score = None
        status = "unknown"
        for line in result.stdout.split('\n'):
            if 'Score:' in line:
                try:
                    score = float(line.split('Score:')[1].split('/')[0].strip())
                except:
                    pass
            if 'Status:' in line:
                status = line.split('Status:')[1].strip().lower()

        return {
            "benchmark_id": benchmark_id,
            "status": status,
            "score": score,
            "elapsed": elapsed,
            "returncode": result.returncode,
            "stdout_preview": result.stdout[-500:] if len(result.stdout) > 500 else result.stdout
        }

    except subprocess.TimeoutExpired:
        return {
            "benchmark_id": benchmark_id,
            "status": "timeout",
            "score": None,
            "elapsed": time.time() - start_time,
            "returncode": -1,
            "error": "Timeout after 24 hours"
        }
    except Exception as e:
        return {
            "benchmark_id": benchmark_id,
            "status": "error",
            "score": None,
            "elapsed": time.time() - start_time,
            "returncode": -1,
            "error": str(e)
        }


def print_progress(completed: int, total: int, results: list):
    """Print progress bar and summary."""
    bar_width = 40
    filled = int(bar_width * completed / total)
    bar = '█' * filled + '░' * (bar_width - filled)

    passed = sum(1 for r in results if r.get('status') == 'passed')
    failed = sum(1 for r in results if r.get('status') == 'failed')
    errors = sum(1 for r in results if r.get('status') in ('error', 'timeout'))

    print(f"\r[{bar}] {completed}/{total} | ✅ {passed} ❌ {failed} ⚠️ {errors}", end='', flush=True)


def main():
    parser = argparse.ArgumentParser(
        description="Parallel Benchmark Runner - Run multiple benchmarks simultaneously"
    )
    parser.add_argument(
        "benchmarks",
        nargs="*",
        help="Specific benchmark IDs to run"
    )
    parser.add_argument(
        "--tier",
        type=int,
        help="Run all benchmarks in a tier"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all benchmarks"
    )
    parser.add_argument(
        "--workers", "-w",
        type=int,
        default=5,
        help="Number of parallel workers (default: 5)"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--exclude-archived",
        action="store_true",
        default=True,
        help="Exclude archived HPC tiers (5, 6, 11)"
    )

    args = parser.parse_args()

    # Collect benchmarks to run
    benchmark_ids = []

    if args.benchmarks:
        benchmark_ids = args.benchmarks
    elif args.tier:
        benchmarks = list_benchmarks(tier=args.tier)
        benchmark_ids = [b['id'] for b in benchmarks]
    elif args.all:
        benchmarks = list_benchmarks()
        benchmark_ids = [b['id'] for b in benchmarks]

        # Exclude archived HPC tiers
        if args.exclude_archived:
            archived_prefixes = ['BENCH-T5-', 'BENCH-T6-', 'BENCH-T11-']
            benchmark_ids = [
                bid for bid in benchmark_ids
                if not any(bid.startswith(p) for p in archived_prefixes)
            ]
    else:
        parser.print_help()
        return

    if not benchmark_ids:
        print("No benchmarks to run!")
        return

    print(f"\n{'='*60}")
    print(f"PARALLEL BENCHMARK RUN")
    print(f"{'='*60}")
    print(f"Benchmarks: {len(benchmark_ids)}")
    print(f"Workers: {args.workers}")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")

    # Run benchmarks in parallel
    results = []
    start_time = time.time()

    with ProcessPoolExecutor(max_workers=args.workers) as executor:
        # Submit all jobs
        future_to_benchmark = {
            executor.submit(run_single_benchmark, bid, args.verbose): bid
            for bid in benchmark_ids
        }

        # Collect results as they complete
        for future in as_completed(future_to_benchmark):
            result = future.result()
            results.append(result)
            print_progress(len(results), len(benchmark_ids), results)

    total_time = time.time() - start_time

    # Print summary
    print(f"\n\n{'='*60}")
    print("RESULTS SUMMARY")
    print(f"{'='*60}")

    passed = [r for r in results if r.get('status') == 'passed']
    failed = [r for r in results if r.get('status') == 'failed']
    errors = [r for r in results if r.get('status') in ('error', 'timeout', 'unknown')]

    print(f"\nTotal: {len(results)}")
    print(f"Passed: {len(passed)} ({len(passed)/len(results)*100:.1f}%)")
    print(f"Failed: {len(failed)}")
    print(f"Errors: {len(errors)}")
    print(f"Total time: {total_time/60:.1f} minutes")

    if passed:
        avg_score = sum(r['score'] for r in passed if r['score']) / len([r for r in passed if r['score']])
        print(f"Avg score (passed): {avg_score:.1f}")

    # List failures
    if failed:
        print(f"\n❌ Failed benchmarks:")
        for r in failed:
            print(f"  - {r['benchmark_id']}: score={r.get('score', 'N/A')}")

    if errors:
        print(f"\n⚠️ Errors:")
        for r in errors:
            print(f"  - {r['benchmark_id']}: {r.get('error', r.get('status'))}")

    # Save results
    report_path = RESULTS_DIR / f"parallel-run-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    with open(report_path, 'w') as f:
        json.dump({
            "run_time": datetime.now().isoformat(),
            "total_benchmarks": len(benchmark_ids),
            "workers": args.workers,
            "total_seconds": total_time,
            "passed": len(passed),
            "failed": len(failed),
            "errors": len(errors),
            "results": results
        }, f, indent=2)

    print(f"\nResults saved: {report_path}")


if __name__ == "__main__":
    main()
