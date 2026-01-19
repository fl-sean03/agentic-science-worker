#!/bin/bash
# Quantum ESPRESSO execution wrapper script
# Usage: ./run_qe.sh input.in output.out [gpu|cpu] [nprocs]

set -e

QE_CPU="/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-cpu/bin"
QE_GPU="/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/build-gpu/bin"
NVHPC_ENV="/home/sf2/Workspace/main/39-GPUTests/1-GPUTests/dft-qe/env/setup_nvhpc.sh"

if [ $# -lt 2 ]; then
    echo "Usage: $0 <input_file> <output_file> [gpu|cpu] [nprocs]"
    echo "  input_file: QE input file"
    echo "  output_file: Output file path"
    echo "  gpu|cpu: Execution mode (default: cpu)"
    echo "  nprocs: Number of MPI processes (default: 1)"
    exit 1
fi

INPUT_FILE="$1"
OUTPUT_FILE="$2"
MODE="${3:-cpu}"
NPROCS="${4:-1}"

if [ ! -f "$INPUT_FILE" ]; then
    echo "Error: Input file '$INPUT_FILE' not found"
    exit 1
fi

echo "=== Quantum ESPRESSO Execution ==="
echo "Input: $INPUT_FILE"
echo "Output: $OUTPUT_FILE"
echo "Mode: $MODE"
echo "Processes: $NPROCS"
echo "==================================="

if [ "$MODE" = "gpu" ]; then
    echo "Setting up NVHPC environment..."
    source "$NVHPC_ENV"
    QE_BIN="$QE_GPU"
else
    QE_BIN="$QE_CPU"
fi

if [ "$NPROCS" -gt 1 ]; then
    echo "Running with MPI ($NPROCS processes)..."
    mpirun -np "$NPROCS" "$QE_BIN/pw.x" < "$INPUT_FILE" > "$OUTPUT_FILE"
else
    echo "Running serial..."
    "$QE_BIN/pw.x" < "$INPUT_FILE" > "$OUTPUT_FILE"
fi

echo "=== Execution Complete ==="
echo "Output written to: $OUTPUT_FILE"
