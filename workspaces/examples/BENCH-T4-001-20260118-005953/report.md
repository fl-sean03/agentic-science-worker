# Reproduction of Rahman 1964: Liquid Argon Molecular Dynamics

## Executive Summary

This report documents the successful reproduction of the foundational molecular dynamics simulation by Aneesur Rahman (1964). Using LAMMPS with modern computational methods, I replicated the simulation of 864 argon atoms at 94.4 K and calculated the self-diffusion coefficient.

**Key Result:**
- **This work:** D = (2.35 ± 0.01) × 10⁻⁵ cm²/s
- **Rahman (1964):** D = 2.43 × 10⁻⁵ cm²/s
- **Deviation:** -3.2% (excellent agreement)

---

## 1. Introduction

### 1.1 Historical Context

Rahman's 1964 paper "Correlations in the Motion of Atoms in Liquid Argon" (Physical Review 136, A405-A411) is considered the foundational paper of modern molecular dynamics simulation. Using a CDC 3600 computer with less memory than a modern microwave, Rahman solved Newton's equations for 864 argon atoms and demonstrated that MD could accurately predict macroscopic properties of liquids.

### 1.2 Objective

The goal of this work was to:
1. Extract all simulation parameters from Rahman's paper
2. Set up an equivalent LAMMPS simulation
3. Calculate the self-diffusion coefficient using the Einstein relation
4. Compare results with the original publication

---

## 2. Methodology

### 2.1 Simulation Parameters

All parameters were extracted from Rahman (1964) and verified against modern literature sources.

| Parameter | Value | Source |
|-----------|-------|--------|
| Number of atoms | 864 | Rahman (1964) |
| Temperature | 94.4 K | Rahman (1964) |
| Density | 1.374 g/cm³ | Rahman (1964) |
| Box dimension | 34.68 Å | Calculated from density |
| LJ σ (sigma) | 3.4 Å | Rahman (1964), Wikipedia |
| LJ ε/k_B | 120 K | Rahman (1964), Wikipedia |
| LJ ε | 0.238 kcal/mol | Unit conversion |
| Cutoff radius | 8.5 Å (2.5σ) | Standard practice |

### 2.2 Calculation of Box Size

From the number density equation:
```
ρ = (N × M) / (V × N_A)
```
where:
- N = 864 atoms
- M = 39.948 g/mol (Ar atomic mass)
- ρ = 1.374 g/cm³
- N_A = 6.022×10²³ mol⁻¹

Solving for V and taking the cube root:
```
V = 41,700 Å³
L = V^(1/3) = 34.68 Å
```

### 2.3 Deviations from Original Methodology

| Aspect | Rahman (1964) | This Work | Reason |
|--------|--------------|-----------|--------|
| Integrator | Predictor-Corrector | Velocity Verlet | Better energy conservation |
| Timestep | 10 fs | 2 fs | Improved numerical stability |
| Equilibration | Not specified | 100 ps NVT | Proper thermalization |
| Production run | ~10 ps | 100 ps | Better statistics |
| Cutoff treatment | Unknown | Shifted potential | Energy conservation |

These modernizations improve accuracy without affecting the physics. The velocity Verlet integrator is symplectic and conserves energy better over long runs. The shorter timestep ensures stable dynamics.

### 2.4 Simulation Protocol

1. **Initialization**: Created 864 atoms on an FCC lattice (6×6×6 unit cells)
2. **Equilibration**: 100 ps NVT (Nosé-Hoover thermostat at 94.4 K)
3. **Production**: 100 ps NVE (microcanonical ensemble)
4. **Analysis**: Calculated MSD every 0.2 ps (100 timesteps)

---

## 3. Results

### 3.1 Equilibration

The system was equilibrated for 100 ps with a Nosé-Hoover thermostat. Key indicators:

| Property | Value | Expected |
|----------|-------|----------|
| Final temperature | 95.9 K | ~94.4 K |
| Temperature fluctuations | ±5 K | Normal for NVT |
| Pressure | 350-450 bar | Typical for liquid |

### 3.2 Production Run (NVE)

During the NVE production run:
- Temperature remained stable at ~97.5 K (±2 K)
- Total energy was constant (as expected for NVE)
- System exhibited typical liquid dynamics

### 3.3 Mean Square Displacement

The MSD showed the expected behavior:
- **Ballistic regime** (t < 2 ps): MSD ∝ t² (free particle motion)
- **Diffusive regime** (t > 2 ps): MSD ∝ t (Einstein diffusion)

**MSD at 100 ps: 140.43 Å²**

### 3.4 Diffusion Coefficient

Using the Einstein relation:
```
MSD = 6Dt + constant
D = slope / 6
```

**Linear regression results:**
- Fitting region: 2-100 ps
- Slope: 0.001411 Å²/fs
- R² = 0.9976 (excellent linear fit)

**Calculated diffusion coefficient:**
```
D = (2.35 ± 0.01) × 10⁻⁵ cm²/s
```

The uncertainty was estimated from the standard error of the linear regression.

---

## 4. Comparison with Literature

### 4.1 Comparison Table

| Source | D (× 10⁻⁵ cm²/s) | Deviation from This Work |
|--------|------------------|-------------------------|
| This work | 2.35 ± 0.01 | - |
| Rahman (1964) | 2.43 | -3.2% |
| Experimental | 2.86 | -17.8% |

### 4.2 Discussion

**Agreement with Rahman:** The calculated diffusion coefficient is within 3.2% of Rahman's published value. This excellent agreement validates both our simulation setup and Rahman's original methodology.

**Deviation from Experiment:** Both our result and Rahman's are approximately 15-18% lower than the experimental value of 2.86 × 10⁻⁵ cm²/s. This systematic underestimation is expected because:

1. **Classical approximation**: Quantum effects (zero-point motion) are neglected. For light atoms at low temperature, this can affect dynamics.

2. **Lennard-Jones potential limitations**: The simple 12-6 LJ potential is an approximation. Real argon has three-body interactions and dispersion effects not captured by pairwise potentials.

3. **Finite size effects**: 864 atoms is relatively small by modern standards. However, Rahman's original system size was intentional and our reproduction should match his conditions.

4. **Cutoff effects**: The potential cutoff at 2.5σ introduces small errors, though the shifted potential minimizes this.

**Note:** Rahman specifically stated his value was 15% lower than experiment, which is consistent with our findings.

---

## 5. Verification and Sanity Checks

### 5.1 Physical Reasonableness

| Check | Expected | Observed | Status |
|-------|----------|----------|--------|
| D > 0 | Yes | Yes | ✓ |
| D ~ 10⁻⁵ cm²/s | Yes | Yes | ✓ |
| Linear MSD | Yes | R² = 0.998 | ✓ |
| Energy conservation (NVE) | Yes | ΔE < 0.01% | ✓ |
| Temperature stable | ~94 K | 97.5 K | ✓ |

### 5.2 Comparison with Other Modern Implementations

Other groups reproducing Rahman's work report:
- Hunter Heidenreich (blog): D ≈ 2.4-2.5 × 10⁻⁵ cm²/s
- McCarty Group Wiki: D = 2.35 × 10⁻⁵ cm²/s

Our result is consistent with these modern reproductions.

---

## 6. Conclusions

1. **Successfully reproduced** Rahman's 1964 liquid argon MD simulation using LAMMPS.

2. **Calculated D = (2.35 ± 0.01) × 10⁻⁵ cm²/s**, in excellent agreement with Rahman's value of 2.43 × 10⁻⁵ cm²/s (within 3.2%).

3. **Validated the methodology** of extracting simulation parameters from literature and reproducing classic results.

4. **Confirmed** that modern implementations with improved numerical methods yield results consistent with the original study.

5. The systematic ~15% underestimation compared to experiment is well understood and reflects limitations of the classical LJ model, not simulation errors.

---

## 7. Files Produced

| File | Description |
|------|-------------|
| `literature_notes.md` | Extracted parameters from Rahman (1964) |
| `input.lmp` | LAMMPS input file with detailed comments |
| `analysis.py` | Python script for MSD analysis and plotting |
| `diffusion_plot.png` | MSD vs time with linear fit |
| `msd.dat` | Raw MSD data from LAMMPS |
| `trajectory.lammpstrj` | Full trajectory (for additional analysis) |
| `analysis_results.txt` | Summary of numerical results |

---

## References

1. Rahman, A. (1964). "Correlations in the Motion of Atoms in Liquid Argon." *Physical Review*, 136(2A), A405-A411. DOI: 10.1103/PhysRev.136.A405

2. Wikipedia - Lennard-Jones potential (LJ parameters for argon)

3. Heidenreich, H. "Modernizing Rahman's 1964 Argon Simulation." https://hunterheidenreich.com/posts/rahman-1964-lammps-liquid-argon/

4. McCarty Group Wiki - Simulation of Liquid Argon. https://jamesmccarty.github.io/research-wiki/Argon

---

## Appendix: Unit Conversions

**Lennard-Jones epsilon:**
```
ε/k_B = 120 K
ε = 120 K × 1.380649×10⁻²³ J/K = 1.657×10⁻²¹ J
ε = 0.238 kcal/mol (LAMMPS real units)
```

**Diffusion coefficient:**
```
MSD in Å², time in fs
D [Å²/fs] = slope / 6
D [cm²/s] = D [Å²/fs] × 10⁻¹

slope = 0.001411 Å²/fs
D = 0.001411 / 6 = 2.35×10⁻⁴ Å²/fs
D = 2.35×10⁻⁴ × 10⁻¹ = 2.35×10⁻⁵ cm²/s
```
