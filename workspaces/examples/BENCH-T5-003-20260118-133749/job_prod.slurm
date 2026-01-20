#!/bin/bash
#SBATCH --job-name=lammps_prod
#SBATCH --partition=amilan
#SBATCH --qos=normal
#SBATCH --nodes=1
#SBATCH --ntasks=64
#SBATCH --time=03:00:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err
#SBATCH --mail-type=END,FAIL

# ============================================
# LAMMPS Production Job - 64 cores on amilan
#
# Partition Decision Rationale:
# - amilan chosen over amilan128c due to:
#   * 40 idle nodes vs 0 idle nodes on amilan128c
#   * 2302 pending jobs on amilan vs 597 on amilan128c
#   * BUT amilan has 387 nodes vs only 16 on amilan128c
#   * Estimated wait: minutes (amilan) vs hours (amilan128c)
# - 64-core job fits perfectly on 1 amilan node
# - Higher memory per core (3.75 GB vs 2 GB on 128c)
#
# Job Details:
# - Liquid Argon MD simulation
# - 32768 atoms, 550000 timesteps total
# - Estimated runtime: ~2 hours
# ============================================

echo "=== LAMMPS Production Job Started ==="
echo "Date: $(date)"
echo "Host: $(hostname)"
echo "Working directory: $(pwd)"
echo "Job ID: $SLURM_JOB_ID"
echo "Partition: $SLURM_JOB_PARTITION"
echo "Nodes: $SLURM_NNODES"
echo "Tasks: $SLURM_NTASKS"
echo ""

# Load Intel oneAPI 2022.1.2 environment (matched to LAMMPS build)
source /curc/sw/install/intel/2022.1.2/setvars.sh --force

# LAMMPS path (Note: requires kim-api library to be available)
LAMMPS_ROOT="/curc/sw/install/lammps/29Sep21/impi/2021.5.0/intel/2022.1.2"
LAMMPS_BIN="${LAMMPS_ROOT}/bin/lmp"

echo "Using LAMMPS: $LAMMPS_BIN"
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

echo "Input files present:"
ls -la input_prod.lmp
echo ""

# Run LAMMPS production
echo "=== Starting LAMMPS Production Run ==="
echo "Start time: $(date)"
START_TIME=$(date +%s)

mpirun -np $SLURM_NTASKS $LAMMPS_BIN -in input_prod.lmp

EXIT_CODE=$?
END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo ""
echo "=== LAMMPS Production Completed ==="
echo "Exit code: $EXIT_CODE"
echo "Elapsed time: $ELAPSED seconds ($((ELAPSED/60)) minutes)"
echo "Finished at: $(date)"

# List output files
echo ""
echo "Output files generated:"
ls -la *.dat *.data *.lammps *.lammpstrj 2>/dev/null || echo "No output files found"

exit $EXIT_CODE
