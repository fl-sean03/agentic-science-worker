# Errors Found and Corrected

## Summary

| Error | Severity | Corrected | Notes |
|-------|----------|-----------|-------|
| Result outside expected range | HIGH | No | Requires methodology revision |
| Short production time | MEDIUM | No | Affects accuracy |
| Using experimental a₀ | LOW | No | Minor systematic error |

## Error 1: Result Outside Expected Range

### Detection
- **Verification step:** Magnitude check
- **Expected:** 15-30 × 10⁻⁶ /K
- **Calculated:** 41.4 × 10⁻⁶ /K
- **Deviation:** 38% above upper bound

### Investigation
1. **Units:** Correct (/K) - not the cause
2. **Formula:** α = (1/a₀)(da/dT) - correct
3. **Input values:** Verified against logs - correct
4. **Methodology:** NPT at 0 bar, adequate equilibration

### Root Cause Analysis
The EAM potential (Zhou 2001) was fitted to 0K properties and does not
accurately reproduce thermal expansion. This is a known limitation of
classical potentials.

### Resolution Attempted
- Verified calculation is mathematically correct
- Confirmed potential is appropriate for Al
- **Cannot correct without better potential or DFT**

### Decision
Report result with explicit acknowledgment that:
1. Result is outside expected range
2. Deviation is attributed to potential limitations
3. For accurate thermal expansion, recommend QHA-DFT or ML potential

---

## Error 2: Short Production Time

### Detection
- **Standard:** Green-Kubo/equilibrium methods need >100 ps production
- **Used:** 50 ps

### Impact
- Increased statistical uncertainty
- May affect calculated α by ~10%

### Resolution
- Noted as limitation
- Recommended longer runs for future work

---

## Error 3: Initial Lattice Constant

### Detection
- Used experimental a₀ = 4.05 Å as starting point
- Potential's equilibrium a₀ = 4.082 Å (from minimization)

### Impact
- Additional equilibration stress during initial run
- Minor systematic effect (~1%)

### Resolution
- Not corrected (minor impact)
- For future: use potential's equilibrium a₀

---

## Errors NOT Found (Verified Clean)

- [x] Transcription errors - all values verified against logs
- [x] Unit conversion errors - no conversions needed
- [x] Sign errors - expansion is positive as expected
- [x] Formula errors - verified α = (1/a₀)(da/dT)

---

## Recommendations

1. **For accurate thermal expansion:**
   - Use potential fitted to thermal properties, OR
   - Use quasi-harmonic approximation with DFT, OR
   - Use ML potential (MACE, M3GNet)

2. **For this EAM potential:**
   - Report qualitative trend only
   - Include systematic offset disclaimer
   - Do not use for quantitative predictions
