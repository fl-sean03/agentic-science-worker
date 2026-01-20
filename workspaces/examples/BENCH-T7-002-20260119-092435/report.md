# Cu Vacancy Formation Energy Calculation - BENCH-T7-002

## Summary

Successfully calculated the vacancy formation energy in copper using molecular dynamics simulations on the CU Boulder Alpine HPC cluster. The benchmark tested HPC error recovery capabilities, with 4 distinct errors encountered and resolved.

**Final Result: Ef = 1.272 eV** (excellent agreement with literature value of 1.27-1.28 eV)

---

## Methodology

### System Setup
- **Material**: FCC Copper
- **Lattice constant**: 3.615 Å
- **Supercell**: 4×4×4 = 256 atoms (perfect), 255 atoms (vacancy)
- **Potential**: Mishin et al. EAM (Phys. Rev. B 63, 224106, 2001)

### Calculation Protocol
1. Create perfect FCC Cu supercell
2. Minimize energy with CG + box relaxation
3. Remove central atom to create vacancy
4. Minimize energy with CG + box relaxation
5. Calculate formation energy: Ef = E(vacancy) - (N-1)/N × E(perfect)

---

## HPC Execution Details

### Jobs Submitted
| Job ID | Type | Status | Run Time |
|--------|------|--------|----------|
| 22906728 | Perfect (attempt 1) | FAILED | - |
| 22906731 | Perfect (attempt 2) | FAILED | - |
| 22906759 | Perfect (attempt 3) | FAILED | - |
| 22907181 | Perfect (final) | SUCCESS | 9 sec |
| 22907182 | Vacancy | SUCCESS | 2 sec |

### Partitions Used
- `atesting` with `qos=testing` for all jobs

---

## Errors Encountered and Recovery

### Error 1: Missing QoS Specification
**Timestamp:** 2026-01-19 09:27 UTC

**Error:**
```
sbatch: error: A Quality of Service (QoS) has not been provided
```

**Cause:** CURC Alpine now requires explicit QoS specification in SLURM scripts.

**Resolution:** Added `#SBATCH --qos=testing` to job scripts.

---

### Error 2: Module Not Found
**Timestamp:** 2026-01-19 09:28 UTC
**Job ID:** 22906728

**Error:**
```
Lmod has detected the following error: The following module(s) are unknown: "intel/2024.2"
```

**Cause:** Module naming on CURC differs from expected; the Intel module doesn't exist as a standard module.

**Resolution:** Switched to sourcing Intel environment directly: `source /curc/sw/install/intel/2022.1.2/setvars.sh`

---

### Error 3: Missing Shared Library (libkim-api)
**Timestamp:** 2026-01-19 09:30 UTC
**Job ID:** 22906731

**Error:**
```
lmp: error while loading shared libraries: libkim-api.so.2: cannot open shared object file
```

**Cause:** Pre-installed LAMMPS builds have KIM API dependency that isn't available on the system.

**Resolution:** Installed LAMMPS via conda-forge (no KIM dependency):
```bash
conda create -p /scratch/alpine/$USER/conda_envs/lammps_env -c conda-forge lammps python=3.11
```

---

### Error 4: Conda Terms of Service Not Accepted
**Timestamp:** 2026-01-19 09:40 UTC
**Job ID:** 22906759

**Error:**
```
CondaToSNonInteractiveError: Terms of Service have not been accepted
```

**Cause:** Anaconda TOS must be accepted before using default channels in batch mode.

**Resolution:** Pre-accepted TOS from login node:
```bash
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/main
conda tos accept --override-channels --channel https://repo.anaconda.com/pkgs/r
```

---

## Resilience Features Implemented

1. **Input Validation**: Scripts check for existence of input files and potential files before running
2. **Environment Verification**: LAMMPS binary is tested before simulation
3. **Fallback Potential Source**: Multiple paths checked for Cu_mishin1.eam.alloy
4. **Comprehensive Logging**: All output captured in .out/.err files
5. **Post-run Verification**: Results displayed in job output for immediate validation

---

## Results

### Perfect Crystal
- **N = 256 atoms**
- **Total PE = -906.295892532314 eV**
- **PE per atom = -3.540218 eV/atom**
- **Optimized lattice constant = 3.6149 Å**

### Vacancy Crystal
- **N = 255 atoms**
- **Total PE = -901.483938298065 eV**
- **PE per atom = -3.535231 eV/atom**
- **Box slightly contracted around vacancy**

### Vacancy Formation Energy
```
Ef = E(vacancy) - (N-1)/N × E(perfect)
Ef = -901.483938 - (255/256) × (-906.295893)
Ef = 1.272 eV
```

### Validation Against Literature

| Source | Ef (eV) | Difference |
|--------|---------|------------|
| This calculation | 1.272 | - |
| Mishin et al. (2001) | 1.27 | 0.1% |
| Experimental | ~1.28 | 0.6% |

**Result: EXCELLENT AGREEMENT**

---

## Files Generated

```
workspaces/benchmarks/BENCH-T7-002-20260119-092435/
├── jobs/
│   ├── perfect_cu.slurm       # SLURM script for perfect crystal
│   └── vacancy_cu.slurm       # SLURM script for vacancy calculation
├── logs/
│   ├── error_log.md           # All errors encountered
│   └── recovery_actions.md    # How each error was resolved
├── inputs/
│   ├── perfect_cu.lmp         # LAMMPS input for perfect crystal
│   └── vacancy_cu.lmp         # LAMMPS input for vacancy
├── results/
│   └── formation_energy.txt   # Final Ef calculation
└── report.md                  # This file
```

---

## Conclusions

1. **Scientific Result**: Successfully calculated Cu vacancy formation energy of 1.272 eV, matching literature values within 0.1-0.6%.

2. **HPC Resilience**: Demonstrated ability to diagnose and recover from 4 different HPC failure modes:
   - SLURM configuration errors (QoS)
   - Module loading issues
   - Shared library dependencies
   - Batch environment configuration (conda TOS)

3. **Key Lessons**:
   - CURC Alpine requires explicit QoS specifications
   - Pre-built software may have hidden dependencies
   - Conda provides a reliable fallback for complex software stacks
   - Always verify execution environment before production runs

---

## References

1. Mishin, Y., Mehl, M.J., Papaconstantopoulos, D.A., Voter, A.F., Kress, J.D. (2001). Structural stability and lattice defects in copper: Ab initio, tight-binding, and embedded-atom calculations. Physical Review B, 63, 224106.

2. CURC Documentation: https://curc.readthedocs.io/

---

*Report generated: 2026-01-19*
*Benchmark: BENCH-T7-002 - HPC Error Recovery*
