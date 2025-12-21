#!/bin/bash
# examples/runtime-demo/mock_lifecycle.sh

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[0;33m'
GRAY='\033[0;90m'
NC='\033[0m' # No Color

function type_cmd() {
    echo -e "${GRAY}$ $1${NC}"
    sleep 0.5
}

function spinner() {
    local pid=$1
    local delay=0.1
    local spinstr='|/-\'
    while [ "$(ps a | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        sleep $delay
        printf "\b\b\b\b\b\b"
    done
    printf "    \b\b\b\b"
}

# --- STEP 1: CONFIGURE ---
echo ""
type_cmd "agentcore configure -e agent.py --name calculator_agent"
sleep 1
echo "🔍 Analyzing project structure..."
sleep 0.5
echo "📦 Detected dependencies: langgraph, bedrock-agentcore"
sleep 0.5
echo -e "${GREEN}✅ Configuration created: .bedrock_agentcore.yaml${NC}"
sleep 0.5
echo "   - Entrypoint: agent.py:app"
echo "   - Runtime: python3.11"
echo "   - Architecture: arm64"
sleep 1

# --- STEP 2: LAUNCH ---
echo ""
type_cmd "agentcore launch"
sleep 1
echo "🚀 Launching agent: calculator_agent (us-east-1)"
echo "🏗️  Building container image..."
sleep 1.5
echo "   [+] Docker build complete (sha256:a1b2c3d4)"
echo "   [+] Pushed to ECR: 123456789012.dkr.ecr.us-east-1.amazonaws.com/calculator_agent:latest"
sleep 1
echo "☁️  Deploying infrastructure (CloudFormation)..."
# Simulate stack events
echo -e "${GRAY}   [10:00:01] CREATE_IN_PROGRESS  AWS::CloudFormation::Stack  calculator-agent-stack${NC}"
sleep 0.5
echo -e "${GRAY}   [10:00:05] CREATE_IN_PROGRESS  AWS::ECS::TaskDefinition    AgentTaskDef${NC}"
sleep 0.5
echo -e "${GRAY}   [10:00:12] CREATE_COMPLETE     AWS::ECS::TaskDefinition    AgentTaskDef${NC}"
sleep 0.5
echo -e "${GRAY}   [10:00:15] CREATE_IN_PROGRESS  AWS::Bedrock::AgentRuntime  AgentRuntime${NC}"
sleep 0.8
echo -e "${GRAY}   [10:00:25] CREATE_COMPLETE     AWS::Bedrock::AgentRuntime  AgentRuntime${NC}"
sleep 0.5
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "   Agent ID:    agent-runtime-07e4d8f2"
echo "   Endpoint:    https://runtime.us-east-1.bedrock-agentcore.aws.dev/invocations"
echo "   Status:      ACTIVE"
sleep 2

# --- STEP 3: INVOKE ---
echo ""
type_cmd "agentcore invoke '{\"prompt\": \"What is 25 * 4?\"}'"
sleep 1
echo "📨 Sending request to agent-runtime-07e4d8f2..."
sleep 1
echo "✅ Response (200 OK):"
echo -e "${BLUE}{"
echo -e "  \"result\": \"The result of 25 * 4 is 100\","
echo -e "  \"usage\": {"
echo -e "    \"input_tokens\": 42, "
echo -e "    \"output_tokens\": 12 "
echo -e "  }"
echo -e "}${NC}"
sleep 2

# --- STEP 4: CLEANUP ---
echo ""
type_cmd "agentcore destroy"
sleep 1
echo "🔥 Destroying resources for: calculator_agent"
echo "   [-] Deleting CloudFormation stack..."
sleep 1.5
echo -e "${GREEN}✅ Cleanup complete.${NC}"
echo ""
