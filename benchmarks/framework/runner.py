#!/usr/bin/env python3
"""
Benchmark Runner for Agentic Science Worker

This framework runs benchmarks following the CLEAR evaluation principles:
- Cost: Token usage, API calls
- Latency: Execution time
- Efficacy: Task completion rate
- Assurance: Validation passes
- Reliability: Consistency across runs
"""

import json
import os
import subprocess
import sys
import time
import yaml
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class BenchmarkResult:
    """Result of a single benchmark run."""
    name: str
    category: str
    passed: bool
    execution_time: float
    error_message: Optional[str] = None
    validation_results: dict = field(default_factory=dict)
    metrics: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class BenchmarkSuite:
    """Collection of benchmark results."""
    name: str
    total_tests: int = 0
    passed_tests: int = 0
    failed_tests: int = 0
    skipped_tests: int = 0
    total_time: float = 0.0
    results: list = field(default_factory=list)

    @property
    def pass_rate(self) -> float:
        if self.total_tests == 0:
            return 0.0
        return (self.passed_tests / self.total_tests) * 100


class BenchmarkRunner:
    """Main benchmark execution engine."""

    def __init__(self, base_dir: str):
        self.base_dir = Path(base_dir)
        self.tests_dir = self.base_dir / "tests"
        self.fixtures_dir = self.base_dir / "fixtures"
        self.reports_dir = self.base_dir / "reports"
        self.reports_dir.mkdir(exist_ok=True)

    def discover_tests(self, category: Optional[str] = None) -> list:
        """Discover all test files in the tests directory."""
        tests = []

        if category:
            search_dirs = [self.tests_dir / category]
        else:
            search_dirs = [d for d in self.tests_dir.iterdir() if d.is_dir()]

        for test_dir in search_dirs:
            if not test_dir.exists():
                continue
            for test_file in test_dir.glob("*.yaml"):
                tests.append(test_file)
            for test_file in test_dir.glob("*.yml"):
                tests.append(test_file)

        return sorted(tests)

    def load_test(self, test_path: Path) -> dict:
        """Load a test definition from YAML."""
        with open(test_path, 'r') as f:
            return yaml.safe_load(f)

    def run_test(self, test_def: dict, verbose: bool = False) -> BenchmarkResult:
        """Execute a single benchmark test."""
        name = test_def.get('name', 'unnamed')
        category = test_def.get('category', 'unknown')

        start_time = time.time()

        try:
            # Determine test type and run appropriate handler
            test_type = test_def.get('type', 'command')

            if test_type == 'command':
                result = self._run_command_test(test_def, verbose)
            elif test_type == 'script':
                result = self._run_script_test(test_def, verbose)
            elif test_type == 'validation':
                result = self._run_validation_test(test_def, verbose)
            elif test_type == 'agent':
                result = self._run_agent_test(test_def, verbose)
            else:
                raise ValueError(f"Unknown test type: {test_type}")

            execution_time = time.time() - start_time

            # Run validations
            validation_results = self._validate_results(test_def, result)
            passed = all(v['passed'] for v in validation_results.values())

            return BenchmarkResult(
                name=name,
                category=category,
                passed=passed,
                execution_time=execution_time,
                validation_results=validation_results,
                metrics=result.get('metrics', {})
            )

        except Exception as e:
            execution_time = time.time() - start_time
            return BenchmarkResult(
                name=name,
                category=category,
                passed=False,
                execution_time=execution_time,
                error_message=str(e)
            )

    def _run_command_test(self, test_def: dict, verbose: bool) -> dict:
        """Run a command-based test."""
        command = test_def.get('command', '')
        timeout = test_def.get('timeout', 120)
        env = os.environ.copy()
        env.update(test_def.get('env', {}))

        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
            cwd=test_def.get('cwd', str(self.base_dir.parent))
        )

        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode,
            'metrics': {
                'exit_code': result.returncode
            }
        }

    def _run_script_test(self, test_def: dict, verbose: bool) -> dict:
        """Run a script-based test."""
        script = test_def.get('script', '')
        script_path = self.base_dir / "scripts" / script

        if not script_path.exists():
            raise FileNotFoundError(f"Script not found: {script_path}")

        result = subprocess.run(
            ['python3', str(script_path)],
            capture_output=True,
            text=True,
            timeout=test_def.get('timeout', 300),
            cwd=str(self.base_dir.parent)
        )

        return {
            'stdout': result.stdout,
            'stderr': result.stderr,
            'returncode': result.returncode
        }

    def _run_validation_test(self, test_def: dict, verbose: bool) -> dict:
        """Run a validation-only test (check existing state)."""
        checks = test_def.get('checks', [])
        results = []

        for check in checks:
            check_type = check.get('type', 'file_exists')

            if check_type == 'file_exists':
                path = Path(check['path']).expanduser()
                results.append({
                    'check': check.get('name', check['path']),
                    'passed': path.exists()
                })
            elif check_type == 'command_succeeds':
                try:
                    result = subprocess.run(
                        check['command'],
                        shell=True,
                        capture_output=True,
                        timeout=30
                    )
                    results.append({
                        'check': check.get('name', check['command']),
                        'passed': result.returncode == 0,
                        'output': result.stdout.decode()[:500]
                    })
                except Exception as e:
                    results.append({
                        'check': check.get('name', check['command']),
                        'passed': False,
                        'error': str(e)
                    })
            elif check_type == 'contains':
                path = Path(check['path']).expanduser()
                if path.exists():
                    content = path.read_text()
                    results.append({
                        'check': check.get('name', f"{check['path']} contains {check['pattern']}"),
                        'passed': check['pattern'] in content
                    })
                else:
                    results.append({
                        'check': check.get('name', check['path']),
                        'passed': False,
                        'error': 'File not found'
                    })

        all_passed = all(r['passed'] for r in results)

        return {
            'checks': results,
            'all_passed': all_passed,
            'returncode': 0 if all_passed else 1
        }

    def _run_agent_test(self, test_def: dict, verbose: bool) -> dict:
        """Run an agent-based test (sends prompt to Claude Code)."""
        # This would integrate with Claude Code CLI
        # For now, return a placeholder
        prompt = test_def.get('prompt', '')

        # In a real implementation, this would:
        # 1. Start a Claude Code session
        # 2. Send the prompt
        # 3. Capture the response and tool usage
        # 4. Return metrics

        return {
            'agent_test': True,
            'prompt': prompt,
            'note': 'Agent tests require Claude Code integration',
            'returncode': 0
        }

    def _validate_results(self, test_def: dict, result: dict) -> dict:
        """Validate test results against criteria."""
        validations = test_def.get('validation', {})
        validation_results = {}

        # Check return code
        if 'exit_code' in validations:
            expected = validations['exit_code']
            actual = result.get('returncode', -1)
            validation_results['exit_code'] = {
                'expected': expected,
                'actual': actual,
                'passed': actual == expected
            }

        # Check output contains
        if 'stdout_contains' in validations:
            patterns = validations['stdout_contains']
            if isinstance(patterns, str):
                patterns = [patterns]
            stdout = result.get('stdout', '')
            for pattern in patterns:
                validation_results[f'stdout_contains:{pattern[:30]}'] = {
                    'pattern': pattern,
                    'passed': pattern in stdout
                }

        # Check output not contains
        if 'stdout_not_contains' in validations:
            patterns = validations['stdout_not_contains']
            if isinstance(patterns, str):
                patterns = [patterns]
            stdout = result.get('stdout', '')
            for pattern in patterns:
                validation_results[f'stdout_not_contains:{pattern[:30]}'] = {
                    'pattern': pattern,
                    'passed': pattern not in stdout
                }

        # Check stderr is empty (no errors)
        if validations.get('no_errors', False):
            stderr = result.get('stderr', '')
            # Filter out common non-error output
            error_lines = [l for l in stderr.split('\n')
                         if l.strip() and not l.startswith('Warning')]
            validation_results['no_errors'] = {
                'passed': len(error_lines) == 0,
                'error_count': len(error_lines)
            }

        # Check file was created
        if 'files_created' in validations:
            for file_path in validations['files_created']:
                path = Path(file_path).expanduser()
                validation_results[f'file_created:{file_path}'] = {
                    'path': file_path,
                    'passed': path.exists()
                }

        # If no validations specified, default to checking return code
        if not validation_results:
            validation_results['default_exit_code'] = {
                'expected': 0,
                'actual': result.get('returncode', -1),
                'passed': result.get('returncode', -1) == 0
            }

        return validation_results

    def run_suite(self, category: Optional[str] = None,
                  verbose: bool = False,
                  stop_on_failure: bool = False) -> BenchmarkSuite:
        """Run a full benchmark suite."""
        suite = BenchmarkSuite(name=category or "full")
        tests = self.discover_tests(category)

        print(f"\n{'='*60}")
        print(f"Running {len(tests)} benchmarks" +
              (f" in category '{category}'" if category else ""))
        print(f"{'='*60}\n")

        for test_path in tests:
            test_def = self.load_test(test_path)
            name = test_def.get('name', test_path.stem)

            # Check if test should be skipped
            if test_def.get('skip', False):
                suite.skipped_tests += 1
                print(f"  SKIP  {name}")
                continue

            print(f"  RUN   {name}...", end=" ", flush=True)

            result = self.run_test(test_def, verbose)
            suite.results.append(result)
            suite.total_tests += 1
            suite.total_time += result.execution_time

            if result.passed:
                suite.passed_tests += 1
                print(f"PASS ({result.execution_time:.2f}s)")
            else:
                suite.failed_tests += 1
                print(f"FAIL ({result.execution_time:.2f}s)")
                if result.error_message:
                    print(f"        Error: {result.error_message}")
                if verbose:
                    for val_name, val_result in result.validation_results.items():
                        if not val_result.get('passed', True):
                            print(f"        - {val_name}: {val_result}")

                if stop_on_failure:
                    break

        print(f"\n{'='*60}")
        print(f"Results: {suite.passed_tests}/{suite.total_tests} passed " +
              f"({suite.pass_rate:.1f}%)")
        print(f"Time: {suite.total_time:.2f}s")
        if suite.skipped_tests:
            print(f"Skipped: {suite.skipped_tests}")
        print(f"{'='*60}\n")

        return suite

    def generate_report(self, suite: BenchmarkSuite,
                       output_path: Optional[Path] = None) -> str:
        """Generate a detailed report of benchmark results."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        if output_path is None:
            output_path = self.reports_dir / f"report_{timestamp}.json"

        report = {
            'timestamp': timestamp,
            'suite_name': suite.name,
            'summary': {
                'total_tests': suite.total_tests,
                'passed': suite.passed_tests,
                'failed': suite.failed_tests,
                'skipped': suite.skipped_tests,
                'pass_rate': suite.pass_rate,
                'total_time': suite.total_time
            },
            'results': [asdict(r) for r in suite.results]
        }

        with open(output_path, 'w') as f:
            json.dump(report, f, indent=2)

        return str(output_path)


def main():
    """CLI entry point for benchmark runner."""
    import argparse

    parser = argparse.ArgumentParser(description='Run Agentic Science Worker benchmarks')
    parser.add_argument('--category', '-c',
                       help='Run only specific category')
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Verbose output')
    parser.add_argument('--quick', '-q', action='store_true',
                       help='Run quick validation only')
    parser.add_argument('--report', '-r', action='store_true',
                       help='Generate detailed report')
    parser.add_argument('--stop-on-failure', '-x', action='store_true',
                       help='Stop on first failure')

    args = parser.parse_args()

    # Determine base directory
    script_dir = Path(__file__).parent.parent
    runner = BenchmarkRunner(script_dir)

    # Run appropriate suite
    if args.quick:
        suite = runner.run_suite(category='environment',
                                verbose=args.verbose,
                                stop_on_failure=args.stop_on_failure)
    else:
        suite = runner.run_suite(category=args.category,
                                verbose=args.verbose,
                                stop_on_failure=args.stop_on_failure)

    # Generate report if requested
    if args.report:
        report_path = runner.generate_report(suite)
        print(f"Report saved to: {report_path}")

    # Exit with appropriate code
    sys.exit(0 if suite.failed_tests == 0 else 1)


if __name__ == '__main__':
    main()
