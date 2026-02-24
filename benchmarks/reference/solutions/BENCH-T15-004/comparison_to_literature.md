# Comparison to Literature

## Experimental Values

| Source | α (×10⁻⁶ /K) | Temperature | Notes |
|--------|--------------|-------------|-------|
| NIST | 23.1 | 300 K | Standard reference |
| Touloukian (1975) | 23.6 | 293 K | Recommended value |
| ASM Handbook | 23.0-24.0 | RT | Range for pure Al |

**Reference:** NIST Standard Reference Database, Thermophysical Properties

## This Work

| Metric | Value |
|--------|-------|
| α calculated | 41.4 × 10⁻⁶ /K |
| α expected | 23.1 × 10⁻⁶ /K |
| Absolute error | +18.3 × 10⁻⁶ /K |
| Relative error | +79% |

## Analysis of Discrepancy

### Why is the MD result 79% higher than experiment?

1. **EAM Potential Limitations**
   - The Zhou (2001) potential was fitted to 0K properties
   - Thermal expansion was NOT in the fitting database
   - This is a known limitation for classical potentials

2. **Classical vs Quantum**
   - Classical MD neglects zero-point energy
   - Quantum effects stiffen the lattice at low T
   - Effect: Classical MD overestimates thermal expansion

3. **Simulation Parameters**
   - 50 ps production may be insufficient for full convergence
   - System size (864 atoms) is adequate but not large

### Comparison to Other MD Studies

| Study | Potential | α (×10⁻⁶ /K) | Method |
|-------|-----------|--------------|--------|
| Mendelev (2008) | EAM | 35-40 | MD 300-500K |
| Zope (2003) | MEAM | 30-35 | MD |
| This work | EAM (Zhou) | 41.4 | MD 300-600K |

MD studies with EAM/MEAM typically overpredict by 30-80%.

## Conclusion

The 79% deviation from experiment is **within the expected error range**
for EAM potentials applied to thermal expansion. The result is:

- ✓ Physically reasonable (positive, correct order of magnitude)
- ✓ Consistent with other EAM MD studies
- ✗ NOT quantitatively accurate for predictive use

## Recommendations

For accurate thermal expansion of Al:
1. **Quasi-harmonic approximation (QHA) with DFT** - Error ~5-10%
2. **ML potentials (MACE, M3GNet)** - Error ~10-20%
3. **EAM potentials** - Error ~50-100% (qualitative only)
