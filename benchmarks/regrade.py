#!/usr/bin/env python3
"""Re-grade benchmarks that failed due to rate limits."""

import json
import subprocess
import sys
from pathlib import Path

RESULTS_DIR = Path(__file__).parent / "results" / "runs"

def find_rate_limited():
    """Find all runs that need re-grading."""
    needs_regrade = []

    for run_dir in sorted(RESULTS_DIR.iterdir()):
        if not run_dir.is_dir():
            continue

        grading_file = run_dir / "grading_result.json"
        if not grading_file.exists():
            continue

        with open(grading_file) as f:
            data = json.load(f)

        raw = data.get("raw_response", "")
        if "hit your limit" in raw or "resets" in raw:
            needs_regrade.append(run_dir)

    return needs_regrade

def regrade(run_dir: Path):
    """Re-grade a single run."""
    # Import grading module
    sys.path.insert(0, str(Path(__file__).parent))
    from run import grade_results, load_benchmark

    benchmark_file = run_dir / "benchmark.yaml"
    transcript_file = run_dir / "transcript.md"

    if not benchmark_file.exists() or not transcript_file.exists():
        print(f"  Missing files in {run_dir.name}, skipping")
        return None

    # Load benchmark config
    benchmark = load_benchmark(benchmark_file)

    # Read transcript
    with open(transcript_file) as f:
        transcript = f.read()

    # Re-grade
    result = grade_results(
        benchmark=benchmark,
        transcript=transcript,
        workspace=run_dir / "workspace",
        grader=benchmark.get("grader", "llm"),
        threshold=benchmark.get("pass_threshold", 60)
    )

    # Save new grading result
    with open(run_dir / "grading_result.json", "w") as f:
        json.dump(result, f, indent=2)

    return result

def main():
    """Re-grade all rate-limited runs."""
    runs = find_rate_limited()

    if not runs:
        print("No runs need re-grading!")
        return

    print(f"Found {len(runs)} runs needing re-grading:\n")

    for run_dir in runs:
        print(f"Re-grading {run_dir.name}...")
        try:
            result = regrade(run_dir)
            if result:
                score = result.get("score", 0)
                status = "PASSED" if score >= 60 else "FAILED"
                print(f"  Score: {score}% - {status}")
        except Exception as e:
            print(f"  ERROR: {e}")

    print("\nDone!")

if __name__ == "__main__":
    main()
