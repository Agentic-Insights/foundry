# LangGraph Web Search Agent

A LangGraph agent with web search capabilities, deployed on AWS Bedrock AgentCore.

## Quick Start

```bash
# Install dependencies
uv sync

# Configure environment
cp .env.example .env
# Edit .env with your settings

# Deploy to AgentCore
agentcore configure -e langgraph_agent_web_search.py --region us-east-1
agentcore launch

# Test
agentcore invoke '{"prompt": "What is the tallest mountain in Africa?"}'

# Cleanup
agentcore destroy
```

## Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `AWS_PROFILE` | AWS CLI profile | - |
| `AWS_REGION` | AWS region | `us-east-1` |
| `BEDROCK_MODEL_ID` | Bedrock model | `us.anthropic.claude-haiku-4-5-20251001-v1:0` |
| `BEDROCK_MODEL_PROVIDER` | Model provider | `bedrock_converse` |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AgentCore Runtime                     │
│  ┌───────────────────────────────────────────────────┐  │
│  │              LangGraph StateGraph                 │  │
│  │  ┌─────────┐    tools_condition    ┌──────────┐  │  │
│  │  │ chatbot │ ──────────────────────▶│  tools   │  │  │
│  │  └─────────┘ ◀─────────────────────└──────────┘  │  │
│  │       │                                  │        │  │
│  │       ▼                                  ▼        │  │
│  │  Claude 4.5 Haiku              DuckDuckGo Search  │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Requirements

- Python 3.11+
- AWS account with Bedrock access
- Model access enabled for Claude models in Bedrock console
