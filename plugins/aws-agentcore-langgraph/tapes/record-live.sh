#!/bin/bash
# Record live terminal demos using VHS
#
# Usage:
#   ./tapes/record-live.sh hero     # Record the hero/deployment demo
#   ./tapes/record-live.sh memory   # Record memory demo
#   ./tapes/record-live.sh all      # Record all demos

set -e

PROJECT_DIR="/home/vaskin/projects/agentcore-lg"
RECORDINGS_DIR="$PROJECT_DIR/recordings"
TAPES_DIR="$PROJECT_DIR/tapes"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

mkdir -p "$RECORDINGS_DIR"

# Generate a tape that runs a script
generate_tape() {
    local name="$1"
    local script="$2"
    local tape_file="$TAPES_DIR/live-${name}.tape"

    cat > "$tape_file" << EOF
# Live recording: $name
Output "${RECORDINGS_DIR}/live-${name}.gif"
Output "${RECORDINGS_DIR}/live-${name}.mp4"

Set Width 1200
Set Height 676
Set FontSize 16
Set FontFamily "JetBrainsMono Nerd Font"
Set LineHeight 1.3
Set Theme "Dracula"
Set Padding 15
Set Margin 10
Set MarginFill "#282a36"
Set BorderRadius 8
Set WindowBar Colorful
Set TypingSpeed 30ms
Set Framerate 30
Set Shell bash

$script
EOF
    echo "$tape_file"
}

# Hero demo - invoke already deployed agent
record_hero() {
    echo -e "${BLUE}Recording: Hero Demo (Invoke Live Agent)${NC}"

    local script='
Env AWS_PROFILE "ag"

Type "cd /home/vaskin/projects/agentcore-lg/examples/langgraph-web-search"
Enter
Sleep 500ms

Type "head -50 agent.py"
Enter
Sleep 3s

Type "uv run agentcore status"
Enter
Sleep 3s

Type `uv run agentcore invoke {"prompt": "What are the top AI trends in 2024?"}`
Enter
Sleep 15s
'

    local tape=$(generate_tape "hero" "$script")
    echo -e "${YELLOW}Running VHS...${NC}"
    vhs "$tape"
    echo -e "${GREEN}✓ Hero demo recorded${NC}"
}

# Memory demo
record_memory() {
    echo -e "${BLUE}Recording: Memory Demo${NC}"

    local script='
Type "cd /home/vaskin/projects/agentcore-lg/examples/memory-demo"
Enter
Sleep 500ms

Type "cat memory_demo.py | head -50"
Enter
Sleep 3s

Type "uv run python memory_demo.py"
Enter
Sleep 15s
'

    local tape=$(generate_tape "memory" "$script")
    vhs "$tape"
    echo -e "${GREEN}✓ Memory demo recorded${NC}"
}

# Browser demo
record_browser() {
    echo -e "${BLUE}Recording: Browser Demo${NC}"

    local script='
Type "cd /home/vaskin/projects/agentcore-lg/examples/browser-demo"
Enter
Sleep 500ms

Type "uv run python browser_demo.py"
Enter
Sleep 10s
'

    local tape=$(generate_tape "browser" "$script")
    vhs "$tape"
    echo -e "${GREEN}✓ Browser demo recorded${NC}"
}

# Code interpreter demo
record_code_interpreter() {
    echo -e "${BLUE}Recording: Code Interpreter Demo${NC}"

    local script='
Type "cd /home/vaskin/projects/agentcore-lg/examples/code-interpreter-demo"
Enter
Sleep 500ms

Type "uv run python code_interpreter_demo.py"
Enter
Sleep 10s
'

    local tape=$(generate_tape "code-interpreter" "$script")
    vhs "$tape"
    echo -e "${GREEN}✓ Code interpreter demo recorded${NC}"
}

# Guardrails demo
record_guardrails() {
    echo -e "${BLUE}Recording: Guardrails Demo${NC}"

    local script='
Type "cd /home/vaskin/projects/agentcore-lg/examples/guardrails-demo"
Enter
Sleep 500ms

Type "uv run python guardrails_demo.py"
Enter
Sleep 10s
'

    local tape=$(generate_tape "guardrails" "$script")
    vhs "$tape"
    echo -e "${GREEN}✓ Guardrails demo recorded${NC}"
}

# Deep research demo (interactive)
record_deep_research() {
    echo -e "${BLUE}Recording: Deep Research Agent${NC}"

    local script='
Type "cd /home/vaskin/projects/agentcore-lg/examples/deep-research-agent"
Enter
Sleep 500ms

Type "head -80 agent.py"
Enter
Sleep 3s

Type "uv run python agent.py --interactive"
Enter
Sleep 3s

Type "What are the latest trends in AI agents?"
Enter
Sleep 15s

Type "quit"
Enter
Sleep 1s
'

    local tape=$(generate_tape "deep-research" "$script")
    vhs "$tape"
    echo -e "${GREEN}✓ Deep research demo recorded${NC}"
}

# Quick overview
record_overview() {
    echo -e "${BLUE}Recording: Overview${NC}"

    local script='
Type "cd /home/vaskin/projects/agentcore-lg"
Enter
Sleep 500ms

Type "ls examples/"
Enter
Sleep 2s

Type "cat examples/deep-research-agent/README.md | head -50"
Enter
Sleep 4s
'

    local tape=$(generate_tape "overview" "$script")
    vhs "$tape"
    echo -e "${GREEN}✓ Overview recorded${NC}"
}

# Main
case "${1:-}" in
    hero)
        record_hero
        ;;
    memory)
        record_memory
        ;;
    browser)
        record_browser
        ;;
    code|code-interpreter)
        record_code_interpreter
        ;;
    guardrails)
        record_guardrails
        ;;
    deep|deep-research)
        record_deep_research
        ;;
    overview)
        record_overview
        ;;
    all)
        record_overview
        record_memory
        record_browser
        record_code_interpreter
        record_guardrails
        record_deep_research
        record_hero
        ;;
    *)
        echo "Usage: $0 {hero|memory|browser|code|guardrails|deep|overview|all}"
        echo ""
        echo "Demos:"
        echo "  hero          Deploy LangGraph to AgentCore and invoke"
        echo "  memory        AgentCore Memory demo"
        echo "  browser       AgentCore Browser demo"
        echo "  code          Code Interpreter demo"
        echo "  guardrails    Guardrails safety demo"
        echo "  deep          Deep Research Agent interactive"
        echo "  overview      Quick project overview"
        echo "  all           Record all demos"
        exit 1
        ;;
esac

echo ""
echo -e "${GREEN}Recordings saved to: $RECORDINGS_DIR/${NC}"
ls -lh "$RECORDINGS_DIR"/live-*.gif 2>/dev/null || true
