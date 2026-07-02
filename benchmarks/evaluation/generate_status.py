#!/usr/bin/env python3
"""
generate_status.py — artifact-derived benchmark status (Slice A3, rebase-2026-07-02).

Regenerates the benchmark dashboard MECHANICALLY from results/runs/*/result.json.
Every number in the output is pulled by reference from an artifact — nothing is
retyped by hand. Motivation: the human-maintained dashboard
(benchmarks/CURRENT_STATUS.md) was found to disagree with the artifacts on at
least nine rows, in both directions (see 08_upgrades/upgrade-2026-07-02/
current_system_audit.md §6). This script kills that transcription error class
and FLAGS every divergence against the human dashboard instead of silently
absorbing it.

The human dashboard is never modified (it is fenced, owner property). Output
goes to a NEW file: benchmarks/results/GENERATED_STATUS.md.

Usage:
    python generate_status.py                       # defaults
    python generate_status.py --results-dir PATH --dashboard PATH --out PATH

Provenance: written by claude-fable-5 (intelligence rebase 2026-07-02).
"""

import argparse
import json
import re
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DEFAULT_RESULTS = PROJECT_ROOT / "benchmarks" / "results" / "runs"
DEFAULT_DASHBOARD = PROJECT_ROOT / "benchmarks" / "CURRENT_STATUS.md"
DEFAULT_OUT = PROJECT_ROOT / "benchmarks" / "results" / "GENERATED_STATUS.md"

TASK_ID_RE = re.compile(r"BENCH-(T\d+-\d+)")
# Dashboard rows like: | T10-003 | 88 ✅ | notes |   or   | T7-002 | 67 | 41 min | notes |
DASH_ROW_RE = re.compile(r"^\|\s*(T\d+-\d+)\s*\|\s*(\d+(?:\.\d+)?)\s*(✅|❌|⏱)?")


def load_runs(results_dir: Path):
    """Latest result.json per task ID (dirs are BENCH-<id>-<YYYYmmdd-HHMMSS>)."""
    runs = {}
    for d in sorted(results_dir.iterdir()):
        rj = d / "result.json"
        if not rj.is_file():
            continue
        m = TASK_ID_RE.search(d.name)
        if not m:
            continue
        try:
            data = json.loads(rj.read_text())
        except Exception as e:
            print(f"WARN unreadable {rj}: {e}", file=sys.stderr)
            continue
        tid = m.group(1)
        # sorted() walks run dirs chronologically; keep the latest per task
        runs[tid] = {
            "dir": d.name,
            "status": data.get("status", "unknown"),
            "score": data.get("score"),
            "threshold": data.get("pass_threshold"),
            "timestamp": data.get("timestamp", ""),
            "model": data.get("model") or "unrecorded",
        }
    return runs


def parse_dashboard(dashboard: Path):
    """Extract {task_id: (score, mark)} from the human dashboard's tables."""
    rows = {}
    if not dashboard.is_file():
        return rows
    for line in dashboard.read_text().splitlines():
        m = DASH_ROW_RE.match(line.strip())
        if m:
            tid, score, mark = m.group(1), float(m.group(2)), m.group(3) or ""
            rows.setdefault(tid, (score, mark))  # first occurrence wins
    return rows


def tier_of(tid: str) -> int:
    return int(tid.split("-")[0][1:])


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    ap.add_argument("--dashboard", type=Path, default=DEFAULT_DASHBOARD,
                    help="human dashboard to diff against (READ-ONLY)")
    ap.add_argument("--out", type=Path, default=DEFAULT_OUT)
    args = ap.parse_args()

    runs = load_runs(args.results_dir)
    if not runs:
        print(f"No result.json artifacts under {args.results_dir}", file=sys.stderr)
        return 1
    dash = parse_dashboard(args.dashboard)

    tally = defaultdict(int)
    for r in runs.values():
        tally[r["status"]] += 1
    total = len(runs)
    passed = tally.get("passed", 0)

    # Divergences: artifact vs dashboard score, or dashboard marks pass while
    # artifact says failed/timeout (and vice versa).
    divergences = []
    for tid, r in sorted(runs.items(), key=lambda kv: (tier_of(kv[0]), kv[0])):
        if tid not in dash:
            continue
        d_score, d_mark = dash[tid]
        a_score = r["score"]
        notes = []
        if a_score is not None and abs(float(a_score) - d_score) >= 1.0:
            notes.append(f"score: dashboard {d_score:g} vs artifact {a_score:g}")
        art_pass = r["status"] == "passed"
        if d_mark == "✅" and not art_pass:
            notes.append(f"outcome: dashboard ✅ vs artifact {r['status']}")
        if d_mark == "❌" and art_pass:
            notes.append(f"outcome: dashboard ❌ vs artifact passed")
        if notes:
            divergences.append((tid, "; ".join(notes), r["dir"]))

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    L = []
    L.append("# GENERATED Benchmark Status — artifact-derived, do not hand-edit")
    L.append("")
    L.append(f"**Generated:** {now} by `benchmarks/evaluation/generate_status.py` "
             f"(rebase-2026-07-02, model claude-fable-5)")
    L.append(f"**Source artifacts:** `{args.results_dir}` ({total} runs with result.json)")
    L.append("")
    L.append("> This file is regenerated mechanically; every number is read from a")
    L.append("> `result.json` artifact. The human-maintained dashboard")
    L.append(f"> (`{args.dashboard.name}`) and the owner's uncommitted corrections to it")
    L.append("> remain the owner's record; where the two disagree, the divergence table")
    L.append("> below says so explicitly. Scores from runs without a `model` field are")
    L.append("> model-unattributed (pre-2026-07 era).")
    L.append("")
    L.append("## Outcome tally")
    L.append("")
    L.append("| Passed | Failed | Timeout | Error | Total | Pass rate |")
    L.append("|-------:|-------:|--------:|------:|------:|----------:|")
    L.append(f"| {passed} | {tally.get('failed', 0)} | {tally.get('timeout', 0)} "
             f"| {tally.get('error', 0)} | {total} | {100.0 * passed / total:.1f}% |")
    L.append("")

    L.append("## Per-tier results (latest run per task)")
    L.append("")
    tiers = defaultdict(list)
    for tid, r in runs.items():
        tiers[tier_of(tid)].append((tid, r))
    for tier in sorted(tiers):
        rows = sorted(tiers[tier])
        tp = sum(1 for _, r in rows if r["status"] == "passed")
        L.append(f"### Tier {tier} — {tp}/{len(rows)} passed")
        L.append("")
        L.append("| Task | Status | Score | Threshold | Model | Run dir |")
        L.append("|------|--------|------:|----------:|-------|---------|")
        for tid, r in rows:
            sc = "-" if r["score"] is None else f"{r['score']:g}"
            th = "-" if r["threshold"] is None else f"{r['threshold']:g}"
            L.append(f"| {tid} | {r['status']} | {sc} | {th} | {r['model']} | `{r['dir']}` |")
        L.append("")

    L.append("## Divergences vs human dashboard")
    L.append("")
    if not dash:
        L.append(f"_Dashboard not found/parsed at `{args.dashboard}` — no diff done._")
    elif not divergences:
        L.append("_None detected on parseable rows._")
    else:
        L.append(f"{len(divergences)} row(s) where `{args.dashboard.name}` disagrees "
                 "with the artifacts (artifact is authoritative for what RAN; the "
                 "dashboard row may predate the fresh run):")
        L.append("")
        L.append("| Task | Disagreement | Artifact |")
        L.append("|------|--------------|----------|")
        for tid, note, dirname in divergences:
            L.append(f"| {tid} | {note} | `{dirname}` |")
    L.append("")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("\n".join(L) + "\n")
    print(f"Wrote {args.out}: {passed}/{total} passed "
          f"({tally.get('failed', 0)} failed, {tally.get('timeout', 0)} timeout, "
          f"{tally.get('error', 0)} error); {len(divergences)} divergence(s) flagged.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
