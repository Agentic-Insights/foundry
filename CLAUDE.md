# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

```bash
# Install dependencies
uv sync

# Run agent locally (starts HTTP server on port 8080)
uv run python langgraph_agent_web_search.py

# Test agent endpoint
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is 2+2?"}'

# Deploy to AWS AgentCore
agentcore configure -e langgraph_agent_web_search.py --region us-east-1
agentcore launch
agentcore invoke '{"prompt": "Hello"}'
agentcore destroy
```

## Environment

- Always use `uv` instead of pip/python directly
- AWS credentials: `export AWS_PROFILE=ag` if credential issues arise
- Python 3.11+ required (LangGraph 1.0 dropped Python 3.9)

## Architecture

**LangGraph + AgentCore Integration Pattern:**

```
User Request → BedrockAgentCoreApp → LangGraph StateGraph → Bedrock LLM
                   (HTTP :8080)           ↓    ↑
                                      ToolNode (DuckDuckGo)
```

The agent uses a ReAct-style loop:
1. `chatbot` node: LLM decides to respond or use tools
2. `tools_condition`: Routes to tools node if tool_calls present, else END
3. `tools` node: Executes tools, returns to chatbot

**Key Components:**
- `BedrockAgentCoreApp`: Wraps graph as HTTP service with `/invocations` and `/ping` endpoints
- `StateGraph`: LangGraph 1.0 graph with message accumulation via `add_messages` reducer
- `init_chat_model`: Initializes Bedrock Claude model with `bedrock_converse` provider

## Skills

The `skills/aws-agentcore-langgraph/` directory contains a redistributable skill documenting AgentCore + LangGraph integration patterns. Reference files cover runtime, memory, gateway, and LangGraph 1.0 patterns.
