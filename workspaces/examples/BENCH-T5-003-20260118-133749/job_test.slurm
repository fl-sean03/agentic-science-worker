#!/bin/bash
#SBATCH --job-name=lammps_test
#SBATCH --partition=atesting
#SBATCH --qos=testing
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --time=00:30:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

# ============================================
# LAMMPS Test Job - Validation on atesting
# Purpose: Verify job script works before production
# Using Intel 2022.1.2 and LAMMPS 29Sep21
# ============================================

echo "=== LAMMPS Test Job Started ==="
echo "Date: $(date)"
echo "Host: $(hostname)"
echo "Working directory: $(pwd)"
echo "Job ID: $SLURM_JOB_ID"
echo "Partition: $SLURM_JOB_PARTITION"
echo "Nodes: $SLURM_NNODES"
echo "Tasks: $SLURM_NTASKS"
echo ""

# Load Intel oneAPI 2022.1.2 environment
source /curc/sw/install/intel/2022.1.2/setvars.sh --force

# LAMMPS 29Sep21 built with Intel 2022.1.2
LAMMPS_ROOT="/curc/sw/install/lammps/29Sep21/impi/2021.5.0/intel/2022.1.2"
LAMMPS_BIN="${LAMMPS_ROOT}/bin/lmp"

echo "Using LAMMPS: $LAMMPS_BIN"
echo ""

# List LD_LIBRARY_PATH (Intel setvars should set this)
echo "LD_LIBRARY_PATH set by Intel setvars:"
echo "$LD_LIBRARY_PATH" | tr ':' '\n' | head -10
echo ""

# Verify LAMMPS is accessible
if [ -x "$LAMMPS_BIN" ]; then
    echo "LAMMPS binary found and executable"
    echo "Checking dependencies:"
    ldd $LAMMPS_BIN 2>&1 | grep "not found" || echo "All dependencies resolved"
else
    echo "ERROR: LAMMPS binary not found at $LAMMPS_BIN"
    exit 1
fi
echo ""

# Change to submission directory
cd $SLURM_SUBMIT_DIR

echo "Input files:"
ls -la *.lmp 2>/dev/null || echo "No .lmp files found"
echo ""

# Run LAMMPS test with Intel MPI
echo "=== Starting LAMMPS Test Run ==="
mpirun -np $SLURM_NTASKS $LAMMPS_BIN -in input_test.lmp

EXIT_CODE=$?
echo ""
echo "=== LAMMPS Test Completed ==="
echo "Exit code: $EXIT_CODE"
echo "Finished at: $(date)"

exit $EXIT_CODE
