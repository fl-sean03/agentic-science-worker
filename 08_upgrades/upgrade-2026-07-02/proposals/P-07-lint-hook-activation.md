# P-07 — activate the sim-input lint inside the PreToolUse hook (Track B-2)

**Status:** PROPOSED · **Author model:** claude-fable-5 · **Date:** 2026-07-02
**Target:** `.claude/hooks/validate_simulation.py` (tracked; executed by the
live session on every Bash call → operating surface).

## Why
The 2026-01-17 CRASH class (empty QE input, ≥2 occurrences) is deterministic
and pre-catchable. Slice A5 built and tested the lint
(`scripts/lint_sim_input.py`, 8/8 tests, EV-A5); this proposal wires it in.

## Exact diff (insert into `validate_command`, after the existing pw.x check)

```diff
@@ def validate_command(command: str) -> tuple: @@
     # Check for QE runs without output redirect
     if 'pw.x' in command:
         if '>' not in command and 'tee' not in command:
             warnings.append("QE output not redirected. Consider: pw.x < input > output")
+
+    # Deterministic input lint (2026-01-17 CRASH class; see
+    # docs/rebase/CRASH_POSTMORTEM_20260117.md). Extract `< input` / `-in input`
+    # and lint it; a BLOCK becomes an error (hook exit 2).
+    m = re.search(r'(?:pw\.x[^|;&]*<\s*(\S+))|(?:\blmp\b[^|;&]*-in\s+(\S+))', command)
+    if m:
+        input_file = m.group(1) or m.group(2)
+        kind = 'qe' if m.group(1) else 'lammps'
+        lint = Path(__file__).resolve().parent.parent.parent / 'scripts' / 'lint_sim_input.py'
+        if lint.exists() and Path(input_file).exists():
+            r = subprocess.run([sys.executable, str(lint), kind, input_file],
+                               capture_output=True, text=True, timeout=10)
+            if r.returncode == 1:
+                errors.append(f"Input lint BLOCK: {r.stdout.strip()}")
```

(plus, at the top of the file: `import subprocess` and `from pathlib import Path`.)

Design choices: lint only fires when the command references an existing input
file (agent-generated temp inputs at invocation time are exactly the CRASH
case); lint failures other than BLOCK (missing lint script, timeout) stay
silent — the hook must never brick Bash.

## Expected effect
The CRASH class becomes impossible to execute silently; ~10 ms overhead on
matching commands only. This IS a behavioral change to the live session's tool
gating — hence owner sign-off.

## Eval plan
After applying: (1) hook unit check — feed the hook a synthetic
`pw.x < empty.in` tool call, expect exit 2 with the BLOCK message; (2) run
BENCH-T1-001 to confirm normal LAMMPS flows are not impeded; (3) watch
`logs/operations.log` for a week of sessions for false positives. Revert = git
revert (single commit).

## APPROVAL
- [ ] APPROVED ____________ (date / initials)   ·   [ ] REJECTED: ____________
