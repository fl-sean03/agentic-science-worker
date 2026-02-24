# Self-Verification Checklist

## Pre-Calculation Expectations

Based on task description and literature:
- **Expected α:** 15-30 × 10⁻⁶ /K
- **Literature value:** 23.1 × 10⁻⁶ /K (NIST, 300K)
- **Method:** NPT MD at two temperatures

## Raw Data Extraction

Values extracted directly from log files (not manually transcribed):

```bash
$ grep "Final lattice" log_300K.txt
Final lattice constant: 4.11077 Angstrom

$ grep "Final lattice" log_600K.txt
Final lattice constant: 4.16188 Angstrom
```

## Verification Steps

### 1. Units Check
- **Expected:** /K (per Kelvin)
- **Calculation:** α = (1/Å) × (Å/K) = /K
- **Status:** ✓ PASS

### 2. Magnitude Check
- **Expected range:** 15-30 × 10⁻⁶ /K
- **Calculated:** 41.4 × 10⁻⁶ /K
- **Status:** ❌ FAIL - Result is 38% above expected range

### 3. Sign Check
- **Expected:** Positive (materials expand when heated)
- **a(300K):** 4.11077 Å
- **a(600K):** 4.16188 Å
- **Expansion:** Yes (4.16188 > 4.11077)
- **Status:** ✓ PASS

### 4. Literature Comparison
- **Experimental:** 23.1 × 10⁻⁶ /K (NIST, 300K)
- **Calculated:** 41.4 × 10⁻⁶ /K
- **Deviation:** 79% higher than experiment
- **Status:** ❌ FAIL - Deviation exceeds acceptable threshold (20%)

### 5. Methodology Check
- **Equilibration:** 50 ps (adequate)
- **Production:** 50 ps (marginal - should be longer)
- **System size:** 864 atoms (adequate)
- **Status:** ⚠️ MARGINAL - Production time should be longer

## Transcription Verification

| Source | Value | Report Value | Match |
|--------|-------|--------------|-------|
| log_300K.txt:332 | 4.11077 | 4.11077 | ✓ |
| log_600K.txt:332 | 4.16188 | 4.16188 | ✓ |

## Overall Verification Status

| Check | Status |
|-------|--------|
| Units | ✓ PASS |
| Magnitude | ❌ FAIL |
| Sign | ✓ PASS |
| Literature | ❌ FAIL |
| Methodology | ⚠️ MARGINAL |

**Result requires investigation before reporting.**
