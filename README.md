# AWS Skills for Claude Code

Unofficial AWS integration skills for Claude Code.

## Install

```bash
/plugin marketplace add Agentic-Insights/aws-skills-cc
/plugin install aws-agentcore-langgraph@aws-skills-cc
```

## Skills

### aws-agentcore-langgraph

Deploy LangGraph agents on AWS Bedrock AgentCore.

| Reference | Coverage |
|-----------|----------|
| `agentcore-runtime.md` | BedrockAgentCoreApp, streaming, async |
| `agentcore-memory.md` | STM/LTM, env vars, sessions |
| `agentcore-gateway.md` | Lambda/OpenAPI/MCP tools |
| `agentcore-cli.md` | All primitives, AWS CLI |
| `langgraph-patterns.md` | StateGraph, checkpointing |

## Examples

Working agent implementations in `examples/` for developers who clone this repo.

## License

Apache 2.0
