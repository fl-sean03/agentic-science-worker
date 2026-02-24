"""
Audit Trail System for Benchmark Grading

Provides full traceability of grading decisions:
- Every check has documented evidence
- Every score has reasoning
- Full audit trail stored with results
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional
import json


class CheckResult(Enum):
    """Result of a single validation check."""
    PASS = "pass"
    FAIL = "fail"
    SKIP = "skip"      # Check not applicable
    ERROR = "error"    # Check couldn't be executed


@dataclass
class CheckEvidence:
    """Evidence collected during a check."""
    file_path: Optional[str] = None
    line_number: Optional[int] = None
    matched_text: Optional[str] = None
    extracted_value: Optional[Any] = None
    screenshot_path: Optional[str] = None
    additional_context: Optional[str] = None


@dataclass
class CheckAudit:
    """Complete audit record for a single validation check."""
    check_id: str
    check_description: str
    category: str

    # Validation details
    check_type: str
    validation_rule: str

    # Result
    result: CheckResult
    points_possible: int
    points_earned: int

    # Evidence
    evidence: Optional[CheckEvidence] = None
    reasoning: Optional[str] = None

    # Metadata
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    duration_ms: Optional[int] = None

    def to_dict(self) -> Dict:
        d = asdict(self)
        d['result'] = self.result.value
        return d


@dataclass
class CategoryAudit:
    """Audit record for a grading category."""
    name: str
    description: str
    weight: int

    checks: List[CheckAudit] = field(default_factory=list)

    @property
    def points_possible(self) -> int:
        return sum(c.points_possible for c in self.checks)

    @property
    def points_earned(self) -> int:
        return sum(c.points_earned for c in self.checks)

    @property
    def percentage(self) -> float:
        if self.points_possible == 0:
            return 0.0
        return (self.points_earned / self.points_possible) * 100

    @property
    def passed_checks(self) -> int:
        return sum(1 for c in self.checks if c.result == CheckResult.PASS)

    @property
    def failed_checks(self) -> int:
        return sum(1 for c in self.checks if c.result == CheckResult.FAIL)

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "description": self.description,
            "weight": self.weight,
            "points_possible": self.points_possible,
            "points_earned": self.points_earned,
            "percentage": round(self.percentage, 1),
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "checks": [c.to_dict() for c in self.checks]
        }


@dataclass
class GradingAudit:
    """Complete audit trail for a benchmark grading."""
    benchmark_id: str
    run_id: str

    # Grading metadata
    grader_type: str  # "llm", "rule_based", "hybrid"
    grader_version: str
    rubric_name: str
    rubric_version: str

    # Categories
    categories: List[CategoryAudit] = field(default_factory=list)

    # Timing
    started_at: str = field(default_factory=lambda: datetime.now().isoformat())
    completed_at: Optional[str] = None
    total_duration_seconds: Optional[float] = None

    # LLM grader details (if used)
    llm_model: Optional[str] = None
    llm_tokens_used: Optional[int] = None
    llm_cost_usd: Optional[float] = None

    # Errors
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)

    @property
    def total_score(self) -> float:
        """Calculate weighted total score."""
        total_weight = sum(c.weight for c in self.categories)
        if total_weight == 0:
            return 0.0

        weighted_sum = sum(c.percentage * c.weight for c in self.categories)
        return weighted_sum / total_weight

    @property
    def total_checks(self) -> int:
        return sum(len(c.checks) for c in self.categories)

    @property
    def passed_checks(self) -> int:
        return sum(c.passed_checks for c in self.categories)

    @property
    def failed_checks(self) -> int:
        return sum(c.failed_checks for c in self.categories)

    def add_check(self, category_name: str, check: CheckAudit):
        """Add a check to the appropriate category."""
        for cat in self.categories:
            if cat.name == category_name:
                cat.checks.append(check)
                return
        raise ValueError(f"Category '{category_name}' not found")

    def complete(self):
        """Mark grading as complete."""
        self.completed_at = datetime.now().isoformat()
        if self.started_at:
            start = datetime.fromisoformat(self.started_at)
            end = datetime.fromisoformat(self.completed_at)
            self.total_duration_seconds = (end - start).total_seconds()

    def to_dict(self) -> Dict:
        return {
            "benchmark_id": self.benchmark_id,
            "run_id": self.run_id,
            "grader_type": self.grader_type,
            "grader_version": self.grader_version,
            "rubric_name": self.rubric_name,
            "rubric_version": self.rubric_version,
            "total_score": round(self.total_score, 1),
            "total_checks": self.total_checks,
            "passed_checks": self.passed_checks,
            "failed_checks": self.failed_checks,
            "categories": [c.to_dict() for c in self.categories],
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "total_duration_seconds": self.total_duration_seconds,
            "llm_model": self.llm_model,
            "llm_tokens_used": self.llm_tokens_used,
            "llm_cost_usd": self.llm_cost_usd,
            "errors": self.errors,
            "warnings": self.warnings
        }

    def save(self, path: Path):
        """Save audit trail to JSON file."""
        with open(path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)

    @classmethod
    def load(cls, path: Path) -> 'GradingAudit':
        """Load audit trail from JSON file."""
        with open(path) as f:
            data = json.load(f)

        audit = cls(
            benchmark_id=data['benchmark_id'],
            run_id=data['run_id'],
            grader_type=data['grader_type'],
            grader_version=data['grader_version'],
            rubric_name=data['rubric_name'],
            rubric_version=data['rubric_version']
        )

        for cat_data in data.get('categories', []):
            cat = CategoryAudit(
                name=cat_data['name'],
                description=cat_data.get('description', ''),
                weight=cat_data['weight']
            )
            for check_data in cat_data.get('checks', []):
                evidence = None
                if check_data.get('evidence'):
                    evidence = CheckEvidence(**check_data['evidence'])

                check = CheckAudit(
                    check_id=check_data['check_id'],
                    check_description=check_data['check_description'],
                    category=cat_data['name'],
                    check_type=check_data['check_type'],
                    validation_rule=check_data['validation_rule'],
                    result=CheckResult(check_data['result']),
                    points_possible=check_data['points_possible'],
                    points_earned=check_data['points_earned'],
                    evidence=evidence,
                    reasoning=check_data.get('reasoning'),
                    timestamp=check_data.get('timestamp'),
                    duration_ms=check_data.get('duration_ms')
                )
                cat.checks.append(check)
            audit.categories.append(cat)

        audit.started_at = data.get('started_at')
        audit.completed_at = data.get('completed_at')
        audit.total_duration_seconds = data.get('total_duration_seconds')
        audit.llm_model = data.get('llm_model')
        audit.llm_tokens_used = data.get('llm_tokens_used')
        audit.llm_cost_usd = data.get('llm_cost_usd')
        audit.errors = data.get('errors', [])
        audit.warnings = data.get('warnings', [])

        return audit

    def to_markdown(self) -> str:
        """Generate human-readable markdown report."""
        lines = [
            f"# Grading Audit: {self.benchmark_id}",
            f"",
            f"**Run ID:** {self.run_id}",
            f"**Score:** {self.total_score:.1f}/100",
            f"**Checks:** {self.passed_checks}/{self.total_checks} passed",
            f"**Grader:** {self.grader_type} v{self.grader_version}",
            f"**Rubric:** {self.rubric_name} v{self.rubric_version}",
            f"",
            "---",
            ""
        ]

        for cat in self.categories:
            lines.append(f"## {cat.name} ({cat.weight}% weight)")
            lines.append(f"")
            lines.append(f"**Score:** {cat.points_earned}/{cat.points_possible} points ({cat.percentage:.1f}%)")
            lines.append(f"")
            lines.append("| Check | Result | Points |")
            lines.append("|-------|--------|--------|")

            for check in cat.checks:
                result_emoji = {
                    CheckResult.PASS: "PASS",
                    CheckResult.FAIL: "FAIL",
                    CheckResult.SKIP: "SKIP",
                    CheckResult.ERROR: "ERR"
                }[check.result]

                lines.append(
                    f"| {check.check_description} | {result_emoji} | "
                    f"{check.points_earned}/{check.points_possible} |"
                )

            lines.append("")

            # Add full reasoning for each check below the table
            for check in cat.checks:
                if check.reasoning:
                    lines.append(f"**{check.check_id}:** {check.reasoning}")
                    lines.append("")
                if check.evidence and check.evidence.matched_text:
                    lines.append(f"*Evidence:* {check.evidence.matched_text}")
                    lines.append("")

        if self.errors:
            lines.append("## Errors")
            for error in self.errors:
                lines.append(f"- {error}")
            lines.append("")

        if self.warnings:
            lines.append("## Warnings")
            for warning in self.warnings:
                lines.append(f"- {warning}")
            lines.append("")

        return "\n".join(lines)


def create_audit_from_benchmark(benchmark: Dict, run_id: str) -> GradingAudit:
    """Create an empty audit structure from a benchmark definition."""
    benchmark_id = benchmark.get('id', 'unknown')

    audit = GradingAudit(
        benchmark_id=benchmark_id,
        run_id=run_id,
        grader_type="hybrid",
        grader_version="1.0.0",
        rubric_name=benchmark.get('rubric', 'embedded'),
        rubric_version="1.0.0"
    )

    # Extract categories from benchmark grading spec
    grading = benchmark.get('grading', {})
    categories = grading.get('categories', [])

    if isinstance(categories, list):
        for cat in categories:
            if isinstance(cat, dict):
                audit.categories.append(CategoryAudit(
                    name=cat.get('name', 'unknown'),
                    description=cat.get('description', ''),
                    weight=cat.get('weight', 0)
                ))
    elif isinstance(categories, dict):
        for name, details in categories.items():
            weight = details.get('weight', 0) if isinstance(details, dict) else 0
            audit.categories.append(CategoryAudit(
                name=name,
                description='',
                weight=weight
            ))

    return audit
