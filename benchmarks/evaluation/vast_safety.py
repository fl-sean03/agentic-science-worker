#!/usr/bin/env python3
"""
VAST.ai Instance Safety Utilities

Provides functions to ensure no orphaned instances remain after benchmarks.
Should be called by the evaluation harness before and after each T17 benchmark.
"""

import subprocess
import json
import time
from typing import List, Dict, Optional


def get_running_instances() -> List[Dict]:
    """Get all currently running VAST.ai instances."""
    try:
        result = subprocess.run(
            ["vastai", "show", "instances", "--raw"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            print(f"Warning: vastai command failed: {result.stderr}")
            return []

        if not result.stdout.strip():
            return []

        instances = json.loads(result.stdout)
        # Filter to running instances only
        return [i for i in instances if i.get("actual_status") == "running"]
    except subprocess.TimeoutExpired:
        print("Warning: vastai command timed out")
        return []
    except json.JSONDecodeError:
        print("Warning: Could not parse vastai output")
        return []
    except FileNotFoundError:
        print("Warning: vastai CLI not found")
        return []


def destroy_instance(instance_id: int) -> bool:
    """Destroy a specific instance."""
    try:
        result = subprocess.run(
            ["vastai", "destroy", "instance", str(instance_id)],
            capture_output=True,
            text=True,
            timeout=30
        )
        return result.returncode == 0
    except Exception as e:
        print(f"Error destroying instance {instance_id}: {e}")
        return False


def destroy_all_instances() -> int:
    """Destroy all running instances. Returns count destroyed."""
    instances = get_running_instances()
    destroyed = 0
    for inst in instances:
        inst_id = inst.get("id")
        if inst_id and destroy_instance(inst_id):
            destroyed += 1
            print(f"Destroyed instance {inst_id}")
    return destroyed


def get_balance() -> Optional[float]:
    """Get current VAST.ai account balance."""
    try:
        result = subprocess.run(
            ["vastai", "show", "user", "--raw"],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            return data.get("credit", 0.0)
    except Exception:
        pass
    return None


class VastSafetyContext:
    """
    Context manager for safe VAST.ai usage in benchmarks.

    Usage:
        with VastSafetyContext(max_cost=0.50) as ctx:
            # Run benchmark
            pass
        # Instances auto-cleaned up

    Features:
    - Records balance before/after
    - Destroys any orphaned instances on exit
    - Enforces cost limits
    - Provides audit trail
    """

    def __init__(self, max_cost: float = 1.0, auto_cleanup: bool = True):
        self.max_cost = max_cost
        self.auto_cleanup = auto_cleanup
        self.balance_before: Optional[float] = None
        self.balance_after: Optional[float] = None
        self.instances_before: List[int] = []
        self.instances_created: List[int] = []
        self.start_time: Optional[float] = None

    def __enter__(self):
        self.start_time = time.time()
        self.balance_before = get_balance()

        # Record existing instances (shouldn't interfere with those)
        existing = get_running_instances()
        self.instances_before = [i["id"] for i in existing]

        if existing:
            print(f"Warning: {len(existing)} instances already running before benchmark")

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.balance_after = get_balance()

        # Find any new instances that weren't cleaned up
        current = get_running_instances()
        current_ids = {i["id"] for i in current}
        before_ids = set(self.instances_before)

        orphans = current_ids - before_ids

        if orphans and self.auto_cleanup:
            print(f"Cleaning up {len(orphans)} orphaned instances: {orphans}")
            for inst_id in orphans:
                destroy_instance(inst_id)

        # Calculate cost
        if self.balance_before is not None and self.balance_after is not None:
            cost = self.balance_before - self.balance_after
            if cost > self.max_cost:
                print(f"Warning: Benchmark exceeded cost limit: ${cost:.2f} > ${self.max_cost:.2f}")

        return False  # Don't suppress exceptions

    def get_audit_report(self) -> Dict:
        """Generate audit report for logging."""
        return {
            "balance_before": self.balance_before,
            "balance_after": self.balance_after,
            "cost": (self.balance_before - self.balance_after)
                    if self.balance_before and self.balance_after else None,
            "instances_before": self.instances_before,
            "duration_seconds": time.time() - self.start_time if self.start_time else None,
        }


# Pre-flight check for T17 benchmarks
def preflight_vast_check() -> Dict:
    """
    Run before any T17 benchmark.
    Returns status dict with any issues found.
    """
    issues = []

    # Check CLI installed
    try:
        subprocess.run(["vastai", "--version"], capture_output=True, timeout=10)
    except FileNotFoundError:
        issues.append("vastai CLI not installed")
        return {"ok": False, "issues": issues}

    # Check balance
    balance = get_balance()
    if balance is None:
        issues.append("Could not get balance - API key issue?")
    elif balance < 0.10:
        issues.append(f"Low balance: ${balance:.2f}")

    # Check for orphan instances
    instances = get_running_instances()
    if instances:
        issues.append(f"{len(instances)} orphan instances found - will be billed!")
        for inst in instances:
            issues.append(f"  - Instance {inst['id']}: {inst.get('gpu_name', 'unknown')} @ ${inst.get('dph_total', 0):.2f}/hr")

    return {
        "ok": len(issues) == 0,
        "issues": issues,
        "balance": balance,
        "orphan_count": len(instances),
    }


# Post-flight check for T17 benchmarks
def postflight_vast_check(destroy_orphans: bool = True) -> Dict:
    """
    Run after any T17 benchmark.
    Optionally destroys any orphaned instances.
    """
    instances = get_running_instances()
    destroyed = []

    if instances and destroy_orphans:
        for inst in instances:
            inst_id = inst["id"]
            if destroy_instance(inst_id):
                destroyed.append(inst_id)

    return {
        "orphans_found": len(instances),
        "orphans_destroyed": destroyed,
        "balance": get_balance(),
    }


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "preflight":
            result = preflight_vast_check()
            print(json.dumps(result, indent=2))
            sys.exit(0 if result["ok"] else 1)

        elif cmd == "postflight":
            result = postflight_vast_check(destroy_orphans=True)
            print(json.dumps(result, indent=2))
            sys.exit(0 if result["orphans_found"] == 0 else 1)

        elif cmd == "cleanup":
            count = destroy_all_instances()
            print(f"Destroyed {count} instances")
            sys.exit(0)

        elif cmd == "status":
            instances = get_running_instances()
            balance = get_balance()
            print(f"Balance: ${balance:.2f}" if balance else "Balance: unknown")
            print(f"Running instances: {len(instances)}")
            for inst in instances:
                print(f"  - {inst['id']}: {inst.get('gpu_name')} @ ${inst.get('dph_total', 0):.2f}/hr")
            sys.exit(0)

    print("Usage: vast_safety.py [preflight|postflight|cleanup|status]")
    sys.exit(1)
