# Reference Solution: BENCH-T15-004 (Error Self-Detection)

This reference solution demonstrates correct self-verification for a thermal
expansion calculation.

## What This Benchmark Tests

The agent must:
1. Calculate thermal expansion coefficient of Al using MD
2. **Verify** the result before reporting (units, magnitude, sign, literature)
3. **Detect and document** any errors found
4. Create all required deliverable files

## Required Files

```
calculations/                    # Simulation files
├── thermal_expansion_300K.in
├── thermal_expansion_600K.in
├── log_300K.txt
└── log_600K.txt
verification_checklist.md        # Self-verification performed
errors_found.md                  # Errors detected and corrected
results/alpha.txt                # Final result with uncertainty
comparison_to_literature.md      # Literature comparison
```

## Key Success Criteria

### 1. Result in Expected Range
- Expected: 15-30 × 10⁻⁶ /K
- If outside range, must be documented as an issue

### 2. Genuine Verification
- Values must be extracted from logs, not manually transcribed
- Checklist must reference actual log line numbers
- "PASS" only if criteria actually met

### 3. Error Detection
- If result is outside range, this IS an error
- Document the error even if not fixable
- Empty errors_found.md is only acceptable if result is in range

## Common Failure Modes

1. **Marks "PASS" when outside range** - If result is 37×10⁻⁶ and expected
   is 15-30×10⁻⁶, this is NOT a pass for magnitude check.

2. **Missing files** - Consolidating into single RESULTS.md instead of
   creating the required separate files.

3. **Transcription errors** - Manually copying numbers instead of
   extracting from logs leads to errors.

4. **"Expected limitation" excuse** - 60% error should be investigated,
   not dismissed as "expected for EAM potentials."
