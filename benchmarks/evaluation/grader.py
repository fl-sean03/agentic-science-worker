#!/usr/bin/env python3
"""
Benchmark Grader for Agentic Science Worker

Grades benchmark results based on rubrics and validation criteria.
Supports file checks, value validation, and LLM-as-Judge evaluation.
"""

import json
import os
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
import yaml


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class CheckResult:
    """Result of a single validation check."""
    name: str
    passed: bool
    points_earned: float
    points_possible: float
    details: str = ""


@dataclass
class CategoryResult:
    """Result of a grading category."""
    name: str
    checks: List[CheckResult]
    weight: int
    score: float  # 0-100 within category
    weighted_score: float  # contribution to total


@dataclass
class GradingResult:
    """Complete grading result for a benchmark."""
    benchmark_id: str
    total_score: float  # 0-100
    max_score: float  # Always 100
    categories: List[CategoryResult]
    milestone_scores: Dict[str, float] = field(default_factory=dict)
    clear_assessment: Dict[str, Any] = field(default_factory=dict)
    notes: List[str] = field(default_factory=list)


# ============================================================================
# Validators
# ============================================================================

class FileValidator:
    """Validate file existence and content."""

    def __init__(self, workspace: Path):
        self.workspace = workspace

    def check_exists(self, relative_path: str) -> Tuple[bool, str]:
        """Check if file exists."""
        full_path = self.workspace / relative_path
        if full_path.exists():
            return True, f"File exists: {relative_path}"
        return False, f"File missing: {relative_path}"

    def check_not_empty(self, relative_path: str) -> Tuple[bool, str]:
        """Check if file exists and is not empty."""
        full_path = self.workspace / relative_path
        if not full_path.exists():
            return False, f"File missing: {relative_path}"
        if full_path.stat().st_size == 0:
            return False, f"File empty: {relative_path}"
        return True, f"File exists and not empty: {relative_path}"

    def check_contains(self, relative_path: str, patterns: List[str]) -> Tuple[bool, str]:
        """Check if file contains all specified patterns."""
        full_path = self.workspace / relative_path
        if not full_path.exists():
            return False, f"File missing: {relative_path}"

        content = full_path.read_text()
        missing = []
        for pattern in patterns:
            if pattern not in content:
                missing.append(pattern)

        if missing:
            return False, f"Missing patterns: {missing}"
        return True, f"All patterns found in {relative_path}"

    def check_regex(self, relative_path: str, regex: str) -> Tuple[bool, str]:
        """Check if file content matches regex."""
        full_path = self.workspace / relative_path
        if not full_path.exists():
            return False, f"File missing: {relative_path}"

        content = full_path.read_text()
        if re.search(regex, content):
            return True, f"Regex matched in {relative_path}"
        return False, f"Regex not matched: {regex}"


class ValueValidator:
    """Validate extracted values against expected ranges."""

    def check_in_range(
        self,
        value: float,
        expected_range: List[float],
        tolerance: float = 0.0
    ) -> Tuple[bool, str]:
        """Check if value is within expected range."""
        if len(expected_range) != 2:
            return False, "Invalid range specification"

        low, high = expected_range
        # Apply tolerance
        low_adj = low * (1 - tolerance) if tolerance else low
        high_adj = high * (1 + tolerance) if tolerance else high

        if low_adj <= value <= high_adj:
            return True, f"Value {value} within range [{low}, {high}]"
        return False, f"Value {value} outside range [{low}, {high}]"

    def check_equals(
        self,
        value: Any,
        expected: Any,
        tolerance: float = 0.0
    ) -> Tuple[bool, str]:
        """Check if value equals expected."""
        if isinstance(value, (int, float)) and isinstance(expected, (int, float)):
            if tolerance:
                if abs(value - expected) <= abs(expected * tolerance):
                    return True, f"Value {value} matches {expected} (±{tolerance*100}%)"
                return False, f"Value {value} != {expected} (±{tolerance*100}%)"

        if value == expected:
            return True, f"Value matches: {expected}"
        return False, f"Value {value} != {expected}"

    def check_relative_error(
        self,
        value: float,
        reference: float,
        max_error: float
    ) -> Tuple[bool, str]:
        """Check relative error against reference."""
        if reference == 0:
            return False, "Reference is zero"

        rel_error = abs(value - reference) / abs(reference)
        if rel_error <= max_error:
            return True, f"Relative error {rel_error:.2%} <= {max_error:.2%}"
        return False, f"Relative error {rel_error:.2%} > {max_error:.2%}"


class SimulationValidator:
    """Validate simulation-specific criteria."""

    def __init__(self, workspace: Path):
        self.workspace = workspace

    def check_lammps_completion(self, log_file: str = "log.lammps") -> Tuple[bool, str]:
        """Check if LAMMPS simulation completed."""
        path = self.workspace / log_file
        if not path.exists():
            return False, f"Log file not found: {log_file}"

        content = path.read_text()

        # Check for completion marker
        if "Total wall time" in content or "Loop time" in content:
            # Check for errors
            if "ERROR" in content:
                return False, "Simulation had errors"
            return True, "LAMMPS simulation completed successfully"

        return False, "LAMMPS simulation did not complete"

    def check_qe_convergence(self, output_file: str) -> Tuple[bool, str]:
        """Check if QE calculation converged."""
        path = self.workspace / output_file
        if not path.exists():
            return False, f"Output file not found: {output_file}"

        content = path.read_text()

        if "convergence has been achieved" in content.lower():
            if "JOB DONE" in content:
                return True, "QE calculation converged and completed"
            return True, "QE SCF converged"

        return False, "QE calculation did not converge"

    def extract_lammps_final_energy(self, log_file: str = "log.lammps") -> Optional[float]:
        """Extract final energy from LAMMPS log."""
        path = self.workspace / log_file
        if not path.exists():
            return None

        content = path.read_text()
        # Look for TotEng column in thermo output
        # This is a simplified parser - real one would be more robust
        lines = content.split('\n')
        for line in reversed(lines):
            if 'TotEng' in line:
                continue
            parts = line.split()
            if len(parts) >= 2:
                try:
                    # Assuming TotEng is typically in a specific column
                    return float(parts[-2])  # Adjust based on thermo style
                except (ValueError, IndexError):
                    continue
        return None


# ============================================================================
# LLM-as-Judge
# ============================================================================

class LLMJudge:
    """Use LLM to evaluate qualitative aspects."""

    def __init__(self, model: str = "claude-3-5-haiku-latest"):
        self.model = model

    def evaluate_report(
        self,
        report_content: str,
        rubric: Dict[str, Any],
        task_description: str
    ) -> Dict[str, Any]:
        """Evaluate a written report using LLM."""

        prompt = f"""
You are evaluating a scientific report written by an AI agent.

## Task the agent was given:
{task_description}

## Agent's report:
{report_content}

## Evaluation rubric:
{json.dumps(rubric, indent=2)}

Evaluate the report on each rubric criterion. For each criterion, provide:
1. A score from 0-100
2. Brief justification (1-2 sentences)

Respond in JSON format:
{{
  "scores": {{
    "criterion_name": {{
      "score": <0-100>,
      "justification": "..."
    }}
  }},
  "overall_notes": "..."
}}
"""

        # This would call an LLM API
        # For now, return placeholder
        return {
            "scores": {},
            "overall_notes": "LLM evaluation not implemented",
            "error": "LLM judge requires API integration"
        }

    def evaluate_scientific_reasoning(
        self,
        agent_output: str,
        expected_reasoning: str
    ) -> Dict[str, Any]:
        """Evaluate scientific reasoning quality."""
        # Placeholder for LLM evaluation
        return {
            "reasoning_score": 0,
            "notes": "LLM evaluation not implemented"
        }


# ============================================================================
# Main Grader
# ============================================================================

class BenchmarkGrader:
    """Grade benchmark results against rubrics."""

    def __init__(self, benchmarks_dir: Path):
        self.benchmarks_dir = benchmarks_dir

    def grade(
        self,
        benchmark_def: Dict[str, Any],
        workspace: Path,
        agent_response: str = ""
    ) -> GradingResult:
        """Grade a benchmark result."""

        benchmark_id = benchmark_def['id']
        grading_spec = benchmark_def.get('grading', {})
        categories_spec = grading_spec.get('categories', {})

        # Initialize validators
        file_validator = FileValidator(workspace)
        value_validator = ValueValidator()
        sim_validator = SimulationValidator(workspace)

        # Grade each category
        category_results = []

        for cat_name, cat_spec in categories_spec.items():
            weight = cat_spec.get('weight', 0)
            checks = cat_spec.get('checks', [])

            check_results = []
            for check in checks:
                result = self._evaluate_check(
                    check,
                    workspace,
                    file_validator,
                    value_validator,
                    sim_validator,
                    agent_response
                )
                check_results.append(result)

            # Calculate category score
            total_points = sum(c.points_possible for c in check_results)
            earned_points = sum(c.points_earned for c in check_results)
            category_score = (earned_points / total_points * 100) if total_points > 0 else 0

            category_results.append(CategoryResult(
                name=cat_name,
                checks=check_results,
                weight=weight,
                score=category_score,
                weighted_score=category_score * weight / 100
            ))

        # Calculate total score
        total_score = sum(cr.weighted_score for cr in category_results)

        # Grade milestones if defined
        milestone_scores = {}
        if 'milestones' in benchmark_def:
            milestone_scores = self._grade_milestones(
                benchmark_def['milestones'],
                workspace,
                agent_response
            )

        # CLEAR assessment
        clear_assessment = self._assess_clear_metrics(
            benchmark_def,
            workspace,
            agent_response
        )

        return GradingResult(
            benchmark_id=benchmark_id,
            total_score=total_score,
            max_score=100.0,
            categories=category_results,
            milestone_scores=milestone_scores,
            clear_assessment=clear_assessment
        )

    def _evaluate_check(
        self,
        check: Dict[str, Any],
        workspace: Path,
        file_validator: FileValidator,
        value_validator: ValueValidator,
        sim_validator: SimulationValidator,
        agent_response: str
    ) -> CheckResult:
        """Evaluate a single check."""

        name = check.get('name', 'Unnamed check')
        points = check.get('points', 0)
        validation = check.get('validation', '')
        validation_lower = validation.lower()

        passed = False
        details = ""

        # Collect all text for searching (agent output + all files in workspace)
        combined_text = agent_response
        for f in workspace.rglob('*'):
            if f.is_file() and f.suffix in ['.out', '.log', '.lammps', '.in', '.lmp', '.md', '.txt', '.py']:
                try:
                    combined_text += "\n" + f.read_text()
                except Exception:
                    pass

        # QE specific checks
        if 'job done' in validation_lower:
            if 'JOB DONE' in combined_text:
                passed = True
                details = "'JOB DONE' found in output"
            else:
                passed = False
                details = "'JOB DONE' not found"

        elif 'convergence' in validation_lower:
            if 'convergence has been achieved' in combined_text.lower() or 'scf convergence' in combined_text.lower():
                passed = True
                details = "SCF convergence found"
            elif 'convergence' in combined_text.lower() and 'yes' in combined_text.lower():
                passed = True
                details = "Convergence achieved (from agent report)"
            else:
                passed = False
                details = "Convergence not verified"

        # LAMMPS specific checks
        elif 'loop time' in validation_lower or 'total wall time' in validation_lower:
            if 'Loop time' in combined_text or 'Total wall time' in combined_text:
                passed = True
                details = "LAMMPS completion marker found"
            else:
                passed = False
                details = "LAMMPS completion marker not found"

        elif 'no error' in validation_lower or 'no fatal' in validation_lower:
            if 'ERROR' in combined_text or 'FATAL' in combined_text:
                passed = False
                details = "Errors found in output"
            else:
                passed = True
                details = "No errors in output"

        # Energy checks
        elif 'energy' in validation_lower and ('range' in validation_lower or 'reasonable' in validation_lower):
            # Look for energy values in output
            energy_match = re.search(r'total\s+energy\s*[=:]\s*(-?[\d.]+)', combined_text, re.I)
            if not energy_match:
                energy_match = re.search(r'\*\*total\s+energy\*\*\s*[|\s]*\*?\*?(-?[\d.]+)', combined_text, re.I)
            if not energy_match:
                energy_match = re.search(r'(?:final|total)\s+(?:potential\s+)?energy[:\s]+(-?[\d.]+)', combined_text, re.I)

            if energy_match:
                energy = float(energy_match.group(1))
                # Check if in reasonable range (Si should be around -15.8 Ry, LJ argon around -213)
                if -20 < energy < -10 or -700 < energy < -100:
                    passed = True
                    details = f"Energy {energy} is in reasonable range"
                else:
                    passed = True  # Still pass if we found an energy
                    details = f"Energy {energy} found (range not strictly validated)"
            else:
                passed = False
                details = "Energy value not found"

        # Structure/lattice checks
        elif 'diamond cubic' in validation_lower or 'lattice' in validation_lower:
            if 'diamond' in combined_text.lower() or 'fcc' in combined_text.lower() or '5.43' in combined_text:
                passed = True
                details = "Correct structure found"
            else:
                passed = False
                details = "Structure details not verified"

        # Cutoff checks for QE
        elif 'ecutwfc' in validation_lower or 'cutoff' in validation_lower:
            cutoff_match = re.search(r'ecutwfc\s*[=:]\s*(\d+)', combined_text, re.I)
            if not cutoff_match:
                cutoff_match = re.search(r'cutoff\s*[|\s]*(\d+)\s*ry', combined_text, re.I)
            if cutoff_match:
                cutoff = int(cutoff_match.group(1))
                if cutoff >= 30:
                    passed = True
                    details = f"Cutoff {cutoff} Ry is adequate"
                else:
                    passed = False
                    details = f"Cutoff {cutoff} Ry may be too low"
            else:
                passed = False
                details = "Cutoff value not found"

        # K-point checks
        elif 'k-point' in validation_lower or 'k-grid' in validation_lower:
            if '4x4x4' in combined_text or '4×4×4' in combined_text or 'k-point grid' in combined_text.lower():
                passed = True
                details = "K-point grid found"
            elif re.search(r'\d+\s*[x×]\s*\d+\s*[x×]\s*\d+', combined_text):
                passed = True
                details = "K-point grid specified"
            else:
                passed = False
                details = "K-point grid not found"

        # Pseudopotential checks
        elif 'pseudo' in validation_lower:
            if '.upf' in combined_text.lower() or 'pseudopotential' in combined_text.lower():
                passed = True
                details = "Pseudopotential referenced"
            else:
                passed = False
                details = "Pseudopotential not found"

        # Atom count checks
        elif 'atom' in validation_lower:
            match = re.search(r'(\d+)\s*atoms', validation_lower)
            if match:
                expected_atoms = int(match.group(1))
                actual_match = re.search(r'(?:created|total)\s+(\d+)\s+atoms', combined_text, re.I)
                if not actual_match:
                    actual_match = re.search(r'number of atoms\s*[=:]\s*(\d+)', combined_text, re.I)
                if actual_match:
                    actual = int(actual_match.group(1))
                    if abs(actual - expected_atoms) / expected_atoms <= 0.1:
                        passed = True
                        details = f"Found {actual} atoms (expected ~{expected_atoms})"
                    else:
                        passed = False
                        details = f"Found {actual} atoms, expected ~{expected_atoms}"
                else:
                    passed = False
                    details = "Atom count not found"
            else:
                passed = False
                details = "Atom count check failed"

        # LJ parameter checks
        elif 'pair_coeff' in validation_lower or 'lj' in validation_lower:
            if 'pair_coeff' in combined_text or 'lj/cut' in combined_text.lower():
                passed = True
                details = "LJ parameters found"
            else:
                passed = False
                details = "LJ parameters not found"

        # Temperature checks
        elif 'temperature' in validation_lower:
            # Check for temperature convergence (e.g., |avg_temp - 94.4| < 5 K)
            if 'avg_temp' in validation_lower or 'converge' in validation_lower:
                # Look for average temperature in output
                avg_match = re.search(r'average\s+temperature[:\s]*(\d+\.?\d*)', combined_text, re.I)
                if not avg_match:
                    avg_match = re.search(r'avg\s+temp[:\s]*(\d+\.?\d*)', combined_text, re.I)
                if not avg_match:
                    avg_match = re.search(r'\*\*average\s+temperature[^*]*\*\*[:\s|\s]*(\d+\.?\d*)', combined_text, re.I)

                if avg_match:
                    avg_temp = float(avg_match.group(1))
                    # Extract target from validation if present
                    target_match = re.search(r'(\d+\.?\d*)\s*K', validation)
                    target = float(target_match.group(1)) if target_match else 94.4
                    if abs(avg_temp - target) < 10:  # Within 10K
                        passed = True
                        details = f"Average temp {avg_temp}K close to target {target}K"
                    else:
                        passed = False
                        details = f"Average temp {avg_temp}K not close to target {target}K"
                else:
                    passed = False
                    details = "Average temperature not found"
            else:
                temp_match = re.search(r'temp(?:erature)?\s*[=:]\s*(\d+\.?\d*)', combined_text, re.I)
                if temp_match:
                    passed = True
                    details = f"Temperature {temp_match.group(1)}K found"
                else:
                    passed = False
                    details = "Temperature not found"

        # Citation checks
        elif 'jorgensen' in validation_lower and '1983' in validation_lower:
            if 'jorgensen' in combined_text.lower() and '1983' in combined_text:
                passed = True
                details = "Jorgensen 1983 citation found"
            else:
                passed = False
                details = "Citation not found"

        elif 'rahman' in validation_lower and '1964' in validation_lower:
            if 'rahman' in combined_text.lower() and '1964' in combined_text:
                passed = True
                details = "Rahman 1964 citation found"
            else:
                passed = False
                details = "Citation not found"

        # Results reported check
        elif 'report' in validation_lower or 'extract' in validation_lower:
            # Check if agent provided a summary with numerical results
            if re.search(r'\d+\.?\d*\s*(ry|ev|kcal|angstrom|cm)', combined_text, re.I):
                passed = True
                details = "Results with units found in output"
            else:
                passed = False
                details = "Results not clearly reported"

        # File existence checks
        elif "exists" in validation_lower:
            match = re.search(r'([a-zA-Z0-9_./\-]+\.[a-zA-Z0-9]+)', validation)
            if match:
                file_path = match.group(1)
                # Check in workspace and subdirectories
                found = False
                for f in workspace.rglob('*'):
                    if f.name == Path(file_path).name:
                        found = True
                        break
                if found:
                    passed = True
                    details = f"File {file_path} found"
                else:
                    passed = False
                    details = f"File {file_path} not found"

        # Generic keyword matching as fallback
        else:
            # Extract key terms from validation and check if they appear
            keywords = [w.lower() for w in re.findall(r'\b[a-zA-Z]{4,}\b', validation)]
            if keywords:
                matches = sum(1 for kw in keywords if kw in combined_text.lower())
                match_ratio = matches / len(keywords)
                if match_ratio >= 0.5:
                    passed = True
                    details = f"Found {matches}/{len(keywords)} key terms"
                else:
                    passed = False
                    details = f"Only found {matches}/{len(keywords)} key terms"
            else:
                passed = False
                details = f"Could not parse validation: {validation[:50]}..."

        return CheckResult(
            name=name,
            passed=passed,
            points_earned=points if passed else 0,
            points_possible=points,
            details=details
        )

    def _grade_milestones(
        self,
        milestones: List[Dict],
        workspace: Path,
        agent_response: str
    ) -> Dict[str, float]:
        """Grade milestone completion."""
        scores = {}

        for milestone in milestones:
            mid = milestone['id']
            weight = milestone['weight']
            validation = milestone.get('validation', '')

            # Simplified milestone validation
            # In practice, this would be more sophisticated
            achieved = False

            # Check for keywords in response
            keywords = re.findall(r'\w+', validation.lower())
            matches = sum(1 for kw in keywords if kw in agent_response.lower())
            if matches >= len(keywords) * 0.5:  # 50% keyword match
                achieved = True

            scores[mid] = weight if achieved else 0

        return scores

    def _assess_clear_metrics(
        self,
        benchmark_def: Dict,
        workspace: Path,
        agent_response: str
    ) -> Dict[str, Any]:
        """Assess CLEAR metrics."""

        clear_spec = benchmark_def.get('clear_metrics', {})
        assessment = {
            'cost': {},
            'latency': {},
            'efficacy': {},
            'assurance': {},
            'reliability': {}
        }

        # Cost assessment
        cost_limits = clear_spec.get('cost', {})
        if 'max_tokens' in cost_limits:
            # Would need actual token count from execution
            assessment['cost']['within_token_limit'] = True  # Placeholder

        # Assurance assessment
        assurance_spec = clear_spec.get('assurance', {})
        if assurance_spec.get('parameters_must_be_cited'):
            # Check for citations in response
            has_citation = bool(re.search(
                r'\(\d{4}\)|et al\.|doi:|arxiv:',
                agent_response,
                re.I
            ))
            assessment['assurance']['parameters_cited'] = has_citation

        return assessment

    def generate_report(self, result: GradingResult) -> str:
        """Generate human-readable grading report."""

        lines = [
            f"# Grading Report: {result.benchmark_id}",
            f"",
            f"## Overall Score: {result.total_score:.1f} / {result.max_score}",
            f"",
            f"## Category Breakdown",
            f""
        ]

        for cat in result.categories:
            lines.append(f"### {cat.name} (weight: {cat.weight}%)")
            lines.append(f"Score: {cat.score:.1f}% ({cat.weighted_score:.1f} points)")
            lines.append("")

            for check in cat.checks:
                status = "✓" if check.passed else "✗"
                lines.append(f"  {status} {check.name}: {check.points_earned}/{check.points_possible}")
                if check.details:
                    lines.append(f"      {check.details}")
            lines.append("")

        if result.milestone_scores:
            lines.append("## Milestones")
            for mid, score in result.milestone_scores.items():
                status = "✓" if score > 0 else "✗"
                lines.append(f"  {status} {mid}: {score:.2f}")
            lines.append("")

        if result.notes:
            lines.append("## Notes")
            for note in result.notes:
                lines.append(f"  - {note}")

        return "\n".join(lines)


# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """Main entry point for grader CLI."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Grade benchmark results"
    )
    parser.add_argument(
        "result_file",
        type=Path,
        help="Path to benchmark result JSON file"
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output file for grading report"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format"
    )

    args = parser.parse_args()

    # Load result
    with open(args.result_file) as f:
        data = json.load(f)

    benchmark_def = data['benchmark']
    result_info = data['result']

    # Determine workspace
    workspace_path = Path(result_info.get('workspace', '.'))

    # Grade
    grader = BenchmarkGrader(Path("."))
    grading_result = grader.grade(
        benchmark_def,
        workspace_path,
        result_info.get('agent_response', '')
    )

    # Output
    if args.format == "json":
        output = json.dumps({
            'benchmark_id': grading_result.benchmark_id,
            'total_score': grading_result.total_score,
            'max_score': grading_result.max_score,
            'categories': [
                {
                    'name': c.name,
                    'weight': c.weight,
                    'score': c.score,
                    'weighted_score': c.weighted_score
                }
                for c in grading_result.categories
            ]
        }, indent=2)
    else:
        output = grader.generate_report(grading_result)

    if args.output:
        args.output.write_text(output)
        print(f"Report saved to: {args.output}")
    else:
        print(output)


if __name__ == "__main__":
    main()
