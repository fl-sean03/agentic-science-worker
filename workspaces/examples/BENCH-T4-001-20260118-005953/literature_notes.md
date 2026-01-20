# Literature Notes: Rahman 1964 - Liquid Argon MD Simulation

## Reference
Rahman, A. (1964). "Correlations in the Motion of Atoms in Liquid Argon"
Physical Review, 136(2A), A405-A411.
DOI: 10.1103/PhysRev.136.A405

**Historical Significance**: This is the foundational paper of modern molecular dynamics simulation. It was the first MD simulation of a realistic system using the Lennard-Jones potential. Rahman is considered one of the founding fathers of molecular dynamics.

---

## Extracted Simulation Parameters

### System Size
- **Number of atoms**: 864 argon atoms
- **Initial configuration**: FCC lattice
- **Boundary conditions**: Periodic boundary conditions (cubic box)

### Thermodynamic Conditions
- **Temperature**: 94.4 K
- **Density**: 1.374 g/cm³ (equivalent to liquid argon at its triple point region)

### Box Size Calculation
From the density and number of atoms:
```
ρ = N × M / (V × N_A)
V = N × M / (ρ × N_A)
V = 864 × 39.948 g/mol / (1.374 g/cm³ × 6.022×10²³ mol⁻¹)
V = 34,499.3 / 8.274×10²³ cm³
V = 4.17 × 10⁻²⁰ cm³
V = 41,700 Å³

L = V^(1/3) = 34.68 Å
```
**Box dimension**: ~34.68 Å × 34.68 Å × 34.68 Å

### Lennard-Jones Potential Parameters
Rahman used the standard LJ parameters for argon:
- **σ (sigma)**: 3.4 Å (collision diameter)
- **ε/k_B**: 120 K (well depth in temperature units)

**Unit conversions for ε**:
- ε = 120 K × k_B = 120 × 1.380649×10⁻²³ J = 1.657×10⁻²¹ J
- ε = 0.238 kcal/mol (LAMMPS "real" units)
- ε = 0.997 kJ/mol (SI)
- ε = 0.0103 eV

### Cutoff Radius
Rahman did not explicitly state the cutoff, but the standard practice is:
- **Cutoff**: 2.5σ = 8.5 Å (conventional for LJ)
- Maximum practical cutoff for minimum image convention: L/2 = 17.34 Å

For this reproduction, I will use **rc = 8.5 Å** (2.5σ), which is the standard practice.

### Integration Method and Timestep
- **Original method**: Predictor-Corrector scheme
- **Original timestep**: 10 fs (~10⁻¹⁴ sec)
- **Modern practice**: Velocity Verlet with 1-2 fs timestep for better stability

### Simulation Duration
- Rahman ran ~10 ps of production (5,001 frames at 10 fs intervals)
- This corresponds to ~10⁻¹¹ seconds, sufficient to observe diffusion

---

## Reported Results

### Self-Diffusion Coefficient
- **Rahman's value**: D = 2.43 × 10⁻⁵ cm²/s
- **Experimental value** (from neutron scattering): ~2.86 × 10⁻⁵ cm²/s
- **Deviation**: Rahman's result was ~15% lower than experiment

Rahman calculated D using the Einstein relation from the mean square displacement:
```
D = lim(t→∞) <|r(t) - r(0)|²> / (6t)
```

### Other Results
- Pair correlation function g(r) agreed well with experiment
- Van Hove function Gs(r,t) showed maximum non-Gaussian behavior at t ≈ 3×10⁻¹² s
- System became diffusive (Gaussian displacement) after ~10⁻¹¹ s

---

## Modern Implementation Notes

### Deviations from Original Methodology
1. **Integrator**: Use velocity Verlet (more stable) instead of predictor-corrector
2. **Timestep**: Use 2 fs instead of 10 fs for better energy conservation
3. **Equilibration**: Use proper thermostat (NVT) for equilibration, then NVE for production
4. **Run length**: Extend production run to improve statistics
5. **Cutoff treatment**: Apply shift or long-range corrections

### Expected Accuracy
Modern implementations typically achieve D = 2.3-2.5 × 10⁻⁵ cm²/s, in good agreement with Rahman's original value.

---

## Sources
- Primary: Rahman, Phys. Rev. 136, A405 (1964)
- Parameters: Wikipedia - Lennard-Jones potential
- Verification: Hunter Heidenreich's blog post on modernizing Rahman's simulation
- Parameters: OpenMMTools documentation (ε = 0.238 kcal/mol for argon)
- McCarty Group Wiki - Simulation of Liquid Argon

## Key Equations

### Lennard-Jones Potential
```
V(r) = 4ε[(σ/r)¹² - (σ/r)⁶]
```

### Einstein Relation for Diffusion
```
D = (1/6) × d<r²>/dt   (in 3D)
```
where <r²> is the mean square displacement (MSD).

### Converting MSD slope to Diffusion Coefficient
```
MSD = 6Dt + constant
D = slope / 6
```
