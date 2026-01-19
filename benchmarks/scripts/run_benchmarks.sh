#!/bin/bash
# Benchmark Runner for Agentic Science Worker
# Usage: ./run_benchmarks.sh [options]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BENCH_DIR="$(dirname "$SCRIPT_DIR")"
AGENT_DIR="$(dirname "$BENCH_DIR")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default options
CATEGORY=""
VERBOSE=false
QUICK=false
REPORT=true
STOP_ON_FAILURE=false

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --category|-c)
            CATEGORY="$2"
            shift 2
            ;;
        --verbose|-v)
            VERBOSE=true
            shift
            ;;
        --quick|-q)
            QUICK=true
            CATEGORY="environment"
            shift
            ;;
        --full|-f)
            CATEGORY=""
            shift
            ;;
        --report|-r)
            REPORT=true
            shift
            ;;
        --no-report)
            REPORT=false
            shift
            ;;
        --stop-on-failure|-x)
            STOP_ON_FAILURE=true
            shift
            ;;
        --help|-h)
            echo "Agentic Science Worker Benchmark Runner"
            echo ""
            echo "Usage: $0 [options]"
            echo ""
            echo "Options:"
            echo "  -c, --category CATEGORY  Run only specific category"
            echo "  -q, --quick              Run quick environment checks only"
            echo "  -f, --full               Run full benchmark suite"
            echo "  -v, --verbose            Verbose output"
            echo "  -r, --report             Generate report (default)"
            echo "  --no-report              Skip report generation"
            echo "  -x, --stop-on-failure    Stop on first failure"
            echo "  -h, --help               Show this help"
            echo ""
            echo "Categories:"
            echo "  environment  System and dependency checks"
            echo "  lammps       LAMMPS simulation tests"
            echo "  qe           Quantum ESPRESSO tests"
            echo "  literature   Literature search tests"
            echo "  materials    Materials database tests"
            echo "  analysis     Data analysis tests"
            echo "  workflows    End-to-end workflow tests"
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════════╗"
echo "║     Agentic Science Worker Benchmark Suite                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Build arguments for Python runner
ARGS=""
if [ -n "$CATEGORY" ]; then
    ARGS="$ARGS --category $CATEGORY"
fi
if [ "$VERBOSE" = true ]; then
    ARGS="$ARGS --verbose"
fi
if [ "$REPORT" = true ]; then
    ARGS="$ARGS --report"
fi
if [ "$STOP_ON_FAILURE" = true ]; then
    ARGS="$ARGS --stop-on-failure"
fi

# Run the Python benchmark framework
cd "$BENCH_DIR"
python3 framework/runner.py $ARGS
EXIT_CODE=$?

# Summary
echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✓ All benchmarks passed${NC}"
else
    echo -e "${RED}✗ Some benchmarks failed${NC}"
fi

exit $EXIT_CODE
