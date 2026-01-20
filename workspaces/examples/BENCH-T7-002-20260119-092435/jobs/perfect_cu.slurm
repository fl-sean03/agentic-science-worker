#!/bin/bash
#SBATCH --job-name=cu_perfect
#SBATCH --partition=atesting
#SBATCH --qos=testing
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --time=00:30:00
#SBATCH --output=%x_%j.out
#SBATCH --error=%x_%j.err

# Cu Perfect Crystal Energy Minimization
# Using conda LAMMPS (conda-forge installation)

echo "=============================================="
echo "Job started: $(date)"
echo "Running on: $(hostname)"
echo "Working directory: $SLURM_SUBMIT_DIR"
echo "Job ID: $SLURM_JOB_ID"
echo "=============================================="

# Set up conda environment
LAMMPS_ENV="/scratch/alpine/$USER/conda_envs/lammps_env"
LAMMPS_BIN="$LAMMPS_ENV/bin/lmp"

# Check that LAMMPS exists
if [ ! -f "$LAMMPS_BIN" ]; then
    echo "ERROR: LAMMPS binary not found at $LAMMPS_BIN"
    exit 1
fi

echo "LAMMPS binary: $LAMMPS_BIN"
$LAMMPS_BIN -h 2>&1 | head -3

# Change to run directory
cd $SLURM_SUBMIT_DIR

# Check input file exists
if [ ! -f "perfect_cu.lmp" ]; then
    echo "ERROR: Input file perfect_cu.lmp not found"
    exit 1
fi

# Check for potential file
POTENTIALS_DIR="/curc/sw/install/lammps/2Aug23/impi/2021.5.0/intel/2022.1.2/share/lammps/potentials"
if [ ! -f "Cu_mishin1.eam.alloy" ]; then
    if [ -f "$POTENTIALS_DIR/Cu_mishin1.eam.alloy" ]; then
        cp $POTENTIALS_DIR/Cu_mishin1.eam.alloy .
        echo "Copied potential file from $POTENTIALS_DIR"
    else
        echo "ERROR: Potential file not found"
        exit 1
    fi
fi

# Show files before run
echo ""
echo "Files in directory:"
ls -la

echo ""
echo "Starting LAMMPS run..."
echo ""

# Run LAMMPS (serial for this small calculation)
$LAMMPS_BIN -in perfect_cu.lmp > perfect_cu.log 2>&1
EXIT_CODE=$?

echo ""
echo "=============================================="
echo "LAMMPS exit code: $EXIT_CODE"
echo "Job finished: $(date)"
echo "=============================================="

# Check for output
if [ -f "perfect_cu.log" ]; then
    echo ""
    echo "===== FULL OUTPUT ====="
    cat perfect_cu.log
fi

exit $EXIT_CODE
