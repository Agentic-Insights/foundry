#!/bin/bash
# Render all VHS tape files to GIF/MP4
#
# Usage:
#   ./tapes/render.sh          # Render all tapes
#   ./tapes/render.sh 01       # Render specific tape (e.g., 01-memory)
#   ./tapes/render.sh hero     # Render hero demo only
#   ./tapes/render.sh --clean  # Clean recordings directory first

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"
TAPES_DIR="$PROJECT_DIR/tapes"
RECORDINGS_DIR="$PROJECT_DIR/recordings"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   AgentCore Demo Renderer              ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════╝${NC}"
echo

# Check dependencies
check_deps() {
    local missing=()

    if ! command -v vhs &> /dev/null; then
        missing+=("vhs")
    fi

    if ! command -v ffmpeg &> /dev/null; then
        missing+=("ffmpeg")
    fi

    if [ ${#missing[@]} -ne 0 ]; then
        echo -e "${RED}Error: Missing dependencies: ${missing[*]}${NC}"
        echo "Install with: brew install ${missing[*]}"
        exit 1
    fi
}

# Clean recordings directory
clean_recordings() {
    echo -e "${YELLOW}Cleaning recordings directory...${NC}"
    rm -rf "$RECORDINGS_DIR"/*.gif "$RECORDINGS_DIR"/*.mp4 2>/dev/null || true
    echo -e "${GREEN}✓ Cleaned${NC}"
}

# Render a single tape
render_tape() {
    local tape="$1"
    local name=$(basename "$tape" .tape)

    echo -e "${BLUE}Rendering: ${name}${NC}"

    # Change to project directory for relative paths
    cd "$PROJECT_DIR"

    if vhs "$tape" 2>&1; then
        echo -e "${GREEN}✓ ${name} complete${NC}"

        # Show output files
        if [ -f "$RECORDINGS_DIR/${name}.gif" ]; then
            local size=$(du -h "$RECORDINGS_DIR/${name}.gif" | cut -f1)
            echo -e "  ${GREEN}→ ${name}.gif (${size})${NC}"
        fi
        if [ -f "$RECORDINGS_DIR/${name}.mp4" ]; then
            local size=$(du -h "$RECORDINGS_DIR/${name}.mp4" | cut -f1)
            echo -e "  ${GREEN}→ ${name}.mp4 (${size})${NC}"
        fi
    else
        echo -e "${RED}✗ ${name} failed${NC}"
        return 1
    fi

    echo
}

# Main logic
main() {
    check_deps

    # Create recordings directory
    mkdir -p "$RECORDINGS_DIR"

    # Handle arguments
    case "$1" in
        --clean)
            clean_recordings
            shift
            ;;
        --help|-h)
            echo "Usage: $0 [options] [tape-pattern]"
            echo
            echo "Options:"
            echo "  --clean    Clean recordings directory first"
            echo "  --help     Show this help"
            echo
            echo "Examples:"
            echo "  $0              # Render all tapes"
            echo "  $0 01           # Render 01-memory.tape"
            echo "  $0 hero         # Render 09-hero.tape"
            echo "  $0 --clean all  # Clean and render all"
            exit 0
            ;;
    esac

    # Find tapes to render
    local tapes=()
    local pattern="${1:-}"

    if [ -z "$pattern" ]; then
        # Render all (except _settings)
        for tape in "$TAPES_DIR"/[0-9]*.tape; do
            if [ -f "$tape" ]; then
                tapes+=("$tape")
            fi
        done
    else
        # Render matching pattern
        for tape in "$TAPES_DIR"/*"$pattern"*.tape; do
            if [ -f "$tape" ] && [[ ! "$tape" == *"_settings"* ]]; then
                tapes+=("$tape")
            fi
        done
    fi

    if [ ${#tapes[@]} -eq 0 ]; then
        echo -e "${YELLOW}No tapes found matching pattern: $pattern${NC}"
        exit 1
    fi

    echo -e "${BLUE}Found ${#tapes[@]} tape(s) to render${NC}"
    echo

    # Render each tape
    local success=0
    local failed=0

    for tape in "${tapes[@]}"; do
        if render_tape "$tape"; then
            ((success++))
        else
            ((failed++))
        fi
    done

    # Summary
    echo -e "${BLUE}════════════════════════════════════════${NC}"
    echo -e "${GREEN}✓ Rendered: $success${NC}"
    if [ $failed -gt 0 ]; then
        echo -e "${RED}✗ Failed: $failed${NC}"
    fi
    echo
    echo -e "Recordings saved to: ${BLUE}$RECORDINGS_DIR/${NC}"

    # List all recordings
    if [ "$(ls -A "$RECORDINGS_DIR" 2>/dev/null)" ]; then
        echo
        echo "Files:"
        ls -lh "$RECORDINGS_DIR"/*.gif "$RECORDINGS_DIR"/*.mp4 2>/dev/null | awk '{print "  " $9 " (" $5 ")"}'
    fi
}

main "$@"
