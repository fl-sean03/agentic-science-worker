#!/usr/bin/env python3
"""
Pre-flight checks for benchmark grading.

These run BEFORE expensive LLM grading to catch obvious failures fast.
"""

from pathlib import Path
from typing import Dict, Any, List, Tuple
from dataclasses import dataclass


@dataclass
class PreflightResult:
    """Result of pre-flight checks."""
    passed: bool
    warnings: List[str]
    failures: List[str]
    auto_fail: bool = False  # If True, skip LLM grading entirely
    auto_fail_reason: str = ""


def check_tool_usage(
    num_tool_calls: int,
    benchmark: Dict[str, Any]
) -> Tuple[bool, str]:
    """Check if agent used tools when required."""
    # These tiers/categories require tool usage
    execution_tiers = {13, 14, 15, 16}  # Tiers that require actual execution
    tier = benchmark.get('tier', 1)

    if tier in execution_tiers and num_tool_calls == 0:
        return False, f"CRITICAL: Zero tool calls for Tier {tier} benchmark (requires execution)"

    return True, ""


def check_required_files(
    workspace: Path,
    benchmark: Dict[str, Any]
) -> Tuple[List[str], List[str]]:
    """Check if required output files exist."""
    warnings = []
    failures = []

    expected = benchmark.get('expected_outputs', {}).get('files', [])

    for file_spec in expected:
        if isinstance(file_spec, dict):
            filename = file_spec.get('name', '')
        else:
            filename = str(file_spec)

        if not filename:
            continue

        # Check if file/directory exists
        file_path = workspace / filename
        if not file_path.exists():
            # Check if it's a pattern (ends with /)
            if filename.endswith('/'):
                failures.append(f"Required directory missing: {filename}")
            else:
                failures.append(f"Required file missing: {filename}")

    return warnings, failures


def check_files_created(
    files_created: List[str],
    benchmark: Dict[str, Any]
) -> Tuple[bool, str]:
    """Check if any files were created for execution benchmarks."""
    execution_tiers = {13, 14, 15, 16}
    tier = benchmark.get('tier', 1)

    if tier in execution_tiers and len(files_created) == 0:
        return False, "CRITICAL: No files created for execution benchmark"

    return True, ""


def run_preflight_checks(
    workspace: Path,
    benchmark: Dict[str, Any],
    num_tool_calls: int,
    files_created: List[str]
) -> PreflightResult:
    """
    Run all pre-flight checks before LLM grading.

    Returns PreflightResult with warnings, failures, and auto_fail flag.
    """
    warnings = []
    failures = []
    auto_fail = False
    auto_fail_reason = ""

    # Check 1: Tool usage
    passed, msg = check_tool_usage(num_tool_calls, benchmark)
    if not passed:
        failures.append(msg)
        auto_fail = True
        auto_fail_reason = "Agent made zero tool calls for an execution benchmark (fabrication detected)"

    # Check 2: Files created
    passed, msg = check_files_created(files_created, benchmark)
    if not passed:
        failures.append(msg)
        if not auto_fail:
            auto_fail = True
            auto_fail_reason = "Agent created no files for an execution benchmark"

    # Check 3: Required files exist
    file_warnings, file_failures = check_required_files(workspace, benchmark)
    warnings.extend(file_warnings)
    failures.extend(file_failures)

    return PreflightResult(
        passed=len(failures) == 0,
        warnings=warnings,
        failures=failures,
        auto_fail=auto_fail,
        auto_fail_reason=auto_fail_reason
    )


def format_preflight_report(result: PreflightResult) -> str:
    """Format pre-flight results for display."""
    lines = ["Pre-flight Checks:"]

    if result.auto_fail:
        lines.append(f"  AUTO-FAIL: {result.auto_fail_reason}")

    if result.failures:
        lines.append("  Failures:")
        for f in result.failures:
            lines.append(f"    ✗ {f}")

    if result.warnings:
        lines.append("  Warnings:")
        for w in result.warnings:
            lines.append(f"    ⚠ {w}")

    if result.passed and not result.warnings:
        lines.append("  ✓ All checks passed")

    return "\n".join(lines)
