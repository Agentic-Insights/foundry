#!/usr/bin/env bash
# Agent Skills Benchmark Runner
#
# Usage:
#   ./benchmarks/run.sh              # Run all tests
#   ./benchmarks/run.sh --fast       # Skip slow tests
#   ./benchmarks/run.sh -k baml      # Run only baml tests
#   ./benchmarks/run.sh --json       # Output JSON report

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"

cd "$SCRIPT_DIR"

# Parse args
PYTEST_ARGS=()
JSON_REPORT=false

for arg in "$@"; do
    case $arg in
        --fast)
            PYTEST_ARGS+=("-m" "not slow")
            ;;
        --json)
            JSON_REPORT=true
            ;;
        *)
            PYTEST_ARGS+=("$arg")
            ;;
    esac
done

# Add JSON report if requested
if $JSON_REPORT; then
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    PYTEST_ARGS+=("--json-report" "--json-report-file=results/benchmark_${TIMESTAMP}.json")
fi

# Ensure dependencies
if ! command -v uv &> /dev/null; then
    echo "Error: uv not found. Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Sync deps and run
echo "=== Agent Skills Benchmark ==="
echo "Running from: $SCRIPT_DIR"
echo ""

uv sync --quiet
uv run pytest "${PYTEST_ARGS[@]}"
