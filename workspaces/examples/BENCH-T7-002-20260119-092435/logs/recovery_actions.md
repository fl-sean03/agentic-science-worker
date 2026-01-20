# Recovery Actions Log - Cu Vacancy Formation Energy Calculation

## Overview
This log documents how each error was diagnosed and resolved.

---

## Recovery Timeline

### Recovery 1: Add QoS to SLURM Scripts
**Timestamp:** 2026-01-19 09:28 UTC
**Related Error:** Error 1 - Missing QoS Specification

**Diagnosis:**
- Read SLURM error message indicating QoS is required
- Checked CURC documentation for valid QoS options
- For `atesting` partition, the QoS should be `testing`

**Solution:**
Added `#SBATCH --qos=testing` directive to SLURM scripts for testing partition.

**Verification:** Will resubmit job and verify successful queue entry.

---

### Recovery 2: Fix Intel Environment Setup
**Timestamp:** 2026-01-19 09:30 UTC
**Related Error:** Error 2 - Module Not Found

**Diagnosis:**
- Checked module availability - intel/2024.2 does not exist as a module
- Found Intel installations directly in /curc/sw/install/intel/
- LAMMPS 2Aug23 was compiled with Intel 2022.1.2
- Need to source the Intel setvars.sh instead of using modules

**Solution:**
Modified SLURM script to:
1. Use LAMMPS 2Aug23 build (intel/2022.1.2)
2. Source Intel environment directly: `source /curc/sw/install/intel/2022.1.2/setvars.sh`
3. Set I_MPI environment variables for proper MPI execution

**Verification:** Will resubmit job and verify successful execution.

---

### Recovery 3: Alternative - Use Conda LAMMPS
**Timestamp:** 2026-01-19 09:35 UTC
**Related Error:** Error 3 - Missing Shared Library (libkim-api)

**Diagnosis:**
- The kim-api library is not installed on the cluster
- All existing LAMMPS builds have this dependency
- Need to either find a build without kim-api or use conda to install LAMMPS

**Solution:**
Create a SLURM script that:
1. Loads anaconda module (available only on compute nodes)
2. Creates a conda environment with LAMMPS from conda-forge
3. Runs the simulation using conda LAMMPS

Alternative solution if conda doesn't work: Build minimal LAMMPS from source without kim-api support.

**Verification:** Will submit a job that installs and uses conda LAMMPS.

---

### Recovery 4: Accept Conda TOS and Install LAMMPS
**Timestamp:** 2026-01-19 09:50 UTC
**Related Error:** Error 4 - Conda Terms of Service Not Accepted

**Diagnosis:**
- Batch jobs cannot interactively accept TOS
- Need to pre-accept TOS before job submission

**Solution:**
1. Ran `conda tos accept` for both main and r channels
2. Created conda environment in /scratch/alpine/$USER/conda_envs/lammps_env
3. Installed LAMMPS 2024.08.29 from conda-forge

**Result:** LAMMPS successfully installed and verified working:
```
Large-scale Atomic/Molecular Massively Parallel Simulator - 29 Aug 2024
```

**Verification:** LAMMPS binary works. Now updating SLURM scripts to use this installation.

---

## Final Successful Runs

### Perfect Crystal Job (22907181)
**Timestamp:** 2026-01-19 09:55 UTC
- Used conda LAMMPS from /scratch/alpine/$USER/conda_envs/lammps_env/bin/lmp
- Completed in 9 seconds
- Result: E(perfect) = -906.295892532314 eV

### Vacancy Crystal Job (22907182)
**Timestamp:** 2026-01-19 09:57 UTC
- Used same conda LAMMPS installation
- Completed in 2 seconds
- Result: E(vacancy) = -901.483938298065 eV

---

## Summary

| Recovery | Time | Successful |
|----------|------|------------|
| QoS Addition | 1 min | Yes |
| Intel Environment | 2 min | No (led to Error 3) |
| Conda LAMMPS | 10 min | Yes (after TOS fix) |
| Conda TOS Accept | 5 min | Yes |

**Total recovery time:** ~18 minutes
**Final workflow:** Conda-installed LAMMPS from conda-forge

---

## Lessons Learned

1. **Check QoS requirements** - CURC Alpine requires explicit QoS for all partitions
2. **Module availability varies** - Not all expected modules exist; check with `module spider`
3. **Pre-built software has dependencies** - The KIM API dependency was not obvious
4. **Conda TOS must be accepted** - Run `conda tos accept` interactively before batch jobs
5. **conda-forge is reliable** - Provides self-contained LAMMPS without complex dependencies

