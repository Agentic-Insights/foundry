#!/bin/bash
# Convenience wrapper for validate.py that sets up the environment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MARKETPLACE_ROOT="$(dirname "$SCRIPT_DIR")"

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo "❌ Error: uv not found"
    echo "Install with: curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

# Run validation with uv from marketplace root
cd "$MARKETPLACE_ROOT"
uv run --with click --with rich python "$SCRIPT_DIR/validate.py" "$@"
