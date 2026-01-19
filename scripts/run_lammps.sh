#!/bin/bash
# LAMMPS execution wrapper script
# Usage: ./run_lammps.sh input.lmp [gpu|cpu] [additional args...]

set -e

LMP="/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/md-lammps/install/bin/lmp"

if [ $# -lt 1 ]; then
    echo "Usage: $0 <input_file> [gpu|cpu] [additional_args...]"
    echo "  input_file: LAMMPS input script"
    echo "  gpu|cpu: Execution mode (default: cpu)"
    exit 1
fi

INPUT_FILE="$1"
MODE="${2:-cpu}"
shift 2 2>/dev/null || shift 1

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found"
    exit 1
fi

echo "=== LAMMPS Execution ==="
echo "Input: $INPUT_FILE"
echo "Mode: $MODE"
echo "========================"

if [ "$MODE" = "gpu" ]; then
    echo "Running with GPU acceleration..."
    $LMP -sf gpu -pk gpu 1 neigh yes -in "$INPUT_FILE" "$@"
else
    echo "Running on CPU..."
    $LMP -in "$INPUT_FILE" "$@"
fi

echo "=== Execution Complete ==="
