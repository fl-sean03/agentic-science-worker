#!/usr/bin/env python3
"""
CLEAR Metrics Collection for Agentic Science Worker Benchmarks

Implements the CLEAR evaluation framework:
- Cost: Token usage, API calls, compute resources
- Latency: Execution time, responsiveness
- Efficacy: Task completion, output quality
- Assurance: Validation passes, safety checks
- Reliability: Consistency, error recovery
"""

import json
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List


@dataclass
class CostMetrics:
    """Cost-related metrics."""
    tokens_input: int = 0
    tokens_output: int = 0
    tokens_total: int = 0
    api_calls: int = 0
    tool_calls: int = 0
    compute_seconds: float = 0.0

    # Estimated costs (can be configured)
    cost_per_1k_input: float = 0.015  # Opus pricing
    cost_per_1k_output: float = 0.075

    @property
    def estimated_cost(self) -> float:
        """Estimate API cost in USD."""
        input_cost = (self.tokens_input / 1000) * self.cost_per_1k_input
        output_cost = (self.tokens_output / 1000) * self.cost_per_1k_output
        return input_cost + output_cost


@dataclass
class LatencyMetrics:
    """Latency-related metrics."""
    total_time: float = 0.0
    time_to_first_response: float = 0.0
    time_per_tool_call: List[float] = field(default_factory=list)
    time_waiting_for_user: float = 0.0

    @property
    def avg_tool_call_time(self) -> float:
        if not self.time_per_tool_call:
            return 0.0
        return sum(self.time_per_tool_call) / len(self.time_per_tool_call)


@dataclass
class EfficacyMetrics:
    """Efficacy-related metrics."""
    task_completed: bool = False
    partial_completion: float = 0.0  # 0.0 to 1.0
    output_quality_score: float = 0.0  # 0.0 to 1.0
    steps_to_completion: int = 0
    retries_needed: int = 0

    # Specific to scientific tasks
    simulation_converged: bool = False
    results_validated: bool = False
    scientifically_correct: bool = False


@dataclass
class AssuranceMetrics:
    """Assurance-related metrics."""
    validations_passed: int = 0
    validations_failed: int = 0
    safety_checks_passed: bool = True
    no_harmful_commands: bool = True
    data_integrity_maintained: bool = True

    @property
    def validation_pass_rate(self) -> float:
        total = self.validations_passed + self.validations_failed
        if total == 0:
            return 1.0
        return self.validations_passed / total


@dataclass
class ReliabilityMetrics:
    """Reliability-related metrics."""
    run_number: int = 1
    consistent_with_previous: bool = True
    errors_encountered: int = 0
    errors_recovered: int = 0
    graceful_degradation: bool = True

    @property
    def error_recovery_rate(self) -> float:
        if self.errors_encountered == 0:
            return 1.0
        return self.errors_recovered / self.errors_encountered


@dataclass
class CLEARMetrics:
    """Complete CLEAR metrics for a benchmark run."""
    benchmark_name: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    cost: CostMetrics = field(default_factory=CostMetrics)
    latency: LatencyMetrics = field(default_factory=LatencyMetrics)
    efficacy: EfficacyMetrics = field(default_factory=EfficacyMetrics)
    assurance: AssuranceMetrics = field(default_factory=AssuranceMetrics)
    reliability: ReliabilityMetrics = field(default_factory=ReliabilityMetrics)

    # Overall scores (0-100)
    @property
    def cost_score(self) -> float:
        """Lower cost = higher score. Normalized to 0-100."""
        # Baseline: 10000 tokens = 50 score
        baseline_tokens = 10000
        ratio = self.cost.tokens_total / baseline_tokens
        score = max(0, min(100, 100 - (ratio - 1) * 25))
        return score

    @property
    def latency_score(self) -> float:
        """Lower latency = higher score. Normalized to 0-100."""
        # Baseline: 60 seconds = 50 score
        baseline_time = 60
        ratio = self.latency.total_time / baseline_time
        score = max(0, min(100, 100 - (ratio - 1) * 25))
        return score

    @property
    def efficacy_score(self) -> float:
        """Higher efficacy = higher score."""
        base = 50 if self.efficacy.task_completed else 0
        base += self.efficacy.partial_completion * 30
        base += self.efficacy.output_quality_score * 20
        return min(100, base)

    @property
    def assurance_score(self) -> float:
        """Higher assurance = higher score."""
        base = self.assurance.validation_pass_rate * 50
        base += 25 if self.assurance.safety_checks_passed else 0
        base += 25 if self.assurance.data_integrity_maintained else 0
        return base

    @property
    def reliability_score(self) -> float:
        """Higher reliability = higher score."""
        base = 50 if self.reliability.consistent_with_previous else 25
        base += self.reliability.error_recovery_rate * 30
        base += 20 if self.reliability.graceful_degradation else 0
        return min(100, base)

    @property
    def overall_score(self) -> float:
        """Weighted average of all CLEAR scores."""
        weights = {
            'cost': 0.15,
            'latency': 0.15,
            'efficacy': 0.35,
            'assurance': 0.20,
            'reliability': 0.15
        }
        return (
            self.cost_score * weights['cost'] +
            self.latency_score * weights['latency'] +
            self.efficacy_score * weights['efficacy'] +
            self.assurance_score * weights['assurance'] +
            self.reliability_score * weights['reliability']
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'benchmark_name': self.benchmark_name,
            'timestamp': self.timestamp,
            'cost': asdict(self.cost),
            'latency': asdict(self.latency),
            'efficacy': asdict(self.efficacy),
            'assurance': asdict(self.assurance),
            'reliability': asdict(self.reliability),
            'scores': {
                'cost': self.cost_score,
                'latency': self.latency_score,
                'efficacy': self.efficacy_score,
                'assurance': self.assurance_score,
                'reliability': self.reliability_score,
                'overall': self.overall_score
            }
        }


class MetricsCollector:
    """Collect and aggregate metrics across benchmark runs."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.output_dir = output_dir or Path(".")
        self.metrics_history: List[CLEARMetrics] = []
        self._current_metrics: Optional[CLEARMetrics] = None
        self._start_time: Optional[float] = None

    def start_benchmark(self, name: str) -> CLEARMetrics:
        """Start collecting metrics for a new benchmark."""
        self._current_metrics = CLEARMetrics(benchmark_name=name)
        self._start_time = time.time()
        return self._current_metrics

    def end_benchmark(self) -> CLEARMetrics:
        """End the current benchmark and finalize metrics."""
        if self._current_metrics and self._start_time:
            self._current_metrics.latency.total_time = time.time() - self._start_time

        if self._current_metrics:
            self.metrics_history.append(self._current_metrics)

        result = self._current_metrics
        self._current_metrics = None
        self._start_time = None
        return result

    def record_tool_call(self, tool_name: str, duration: float):
        """Record a tool call."""
        if self._current_metrics:
            self._current_metrics.cost.tool_calls += 1
            self._current_metrics.latency.time_per_tool_call.append(duration)

    def record_tokens(self, input_tokens: int, output_tokens: int):
        """Record token usage."""
        if self._current_metrics:
            self._current_metrics.cost.tokens_input += input_tokens
            self._current_metrics.cost.tokens_output += output_tokens
            self._current_metrics.cost.tokens_total = (
                self._current_metrics.cost.tokens_input +
                self._current_metrics.cost.tokens_output
            )

    def record_validation(self, passed: bool):
        """Record a validation result."""
        if self._current_metrics:
            if passed:
                self._current_metrics.assurance.validations_passed += 1
            else:
                self._current_metrics.assurance.validations_failed += 1

    def record_error(self, recovered: bool = False):
        """Record an error occurrence."""
        if self._current_metrics:
            self._current_metrics.reliability.errors_encountered += 1
            if recovered:
                self._current_metrics.reliability.errors_recovered += 1

    def set_task_completed(self, completed: bool,
                          partial: float = 0.0,
                          quality: float = 0.0):
        """Set task completion status."""
        if self._current_metrics:
            self._current_metrics.efficacy.task_completed = completed
            self._current_metrics.efficacy.partial_completion = partial
            self._current_metrics.efficacy.output_quality_score = quality

    def save_metrics(self, filename: Optional[str] = None):
        """Save collected metrics to file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"metrics_{timestamp}.json"

        output_path = self.output_dir / filename

        data = {
            'collection_time': datetime.now().isoformat(),
            'total_benchmarks': len(self.metrics_history),
            'metrics': [m.to_dict() for m in self.metrics_history]
        }

        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        return output_path

    def get_summary(self) -> Dict[str, Any]:
        """Get summary statistics across all collected metrics."""
        if not self.metrics_history:
            return {}

        scores = [m.overall_score for m in self.metrics_history]
        times = [m.latency.total_time for m in self.metrics_history]
        tokens = [m.cost.tokens_total for m in self.metrics_history]

        return {
            'total_benchmarks': len(self.metrics_history),
            'avg_overall_score': sum(scores) / len(scores),
            'min_overall_score': min(scores),
            'max_overall_score': max(scores),
            'avg_time': sum(times) / len(times),
            'total_tokens': sum(tokens),
            'avg_tokens': sum(tokens) / len(tokens)
        }


# Convenience function for one-off metrics
def quick_metrics(name: str,
                  completed: bool,
                  time_seconds: float,
                  tokens: int = 0,
                  validations_passed: int = 0,
                  validations_failed: int = 0) -> CLEARMetrics:
    """Create metrics quickly for simple benchmarks."""
    metrics = CLEARMetrics(benchmark_name=name)
    metrics.efficacy.task_completed = completed
    metrics.latency.total_time = time_seconds
    metrics.cost.tokens_total = tokens
    metrics.assurance.validations_passed = validations_passed
    metrics.assurance.validations_failed = validations_failed
    return metrics
