# AWS AgentCore + LangGraph

Claude Code plugin for deploying LangGraph agents on AWS Bedrock AgentCore.

## Install Plugin

```bash
/plugin marketplace add Agentic-Insights/aws-skills-cc
/plugin install aws-agentcore-langgraph@aws-skills-cc
```

The skill auto-activates when working with AgentCore deployments, memory, or gateway integrations.

## What's Included

| Reference | Coverage |
|-----------|----------|
| `agentcore-runtime.md` | BedrockAgentCoreApp wrapper, streaming, async |
| `agentcore-memory.md` | STM/LTM patterns, env vars, session management |
| `agentcore-gateway.md` | Lambda/OpenAPI/MCP → unified MCP tools |
| `agentcore-cli.md` | All primitives, AWS CLI commands |
| `langgraph-patterns.md` | StateGraph, checkpointing, tools |

## For Developers

Clone and deploy the example agent:

```bash
git clone https://github.com/Agentic-Insights/aws-skills-cc.git
cd aws-skills-cc
uv sync

agentcore configure -e langgraph_agent_web_search.py --region us-east-1
agentcore launch
agentcore invoke '{"prompt": "What are the latest AI news?"}'
agentcore destroy
```

## Requirements

- Python 3.11+
- AWS account with Bedrock model access
- [uv](https://github.com/astral-sh/uv) package manager

## License

Apache 2.0 - See [LICENSE](LICENSE)
