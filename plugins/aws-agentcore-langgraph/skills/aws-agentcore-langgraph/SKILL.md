---
name: aws-agentcore-langgraph
description: Deploy LangGraph 1.0 agents on AWS Bedrock AgentCore for production. Use when (1) wrapping LangGraph StateGraph with BedrockAgentCoreApp runtime, (2) adding AgentCore Memory (short-term/long-term) to LangGraph agents, (3) connecting AgentCore Gateway MCP tools to LangGraph, (4) deploying agents via agentcore CLI (configure/launch/invoke/destroy), or (5) integrating LangGraph checkpointing with AgentCore services.
---

# AWS AgentCore + LangGraph Integration

## Quick Start: Minimal Runtime Integration

```python
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from typing import Annotated
from typing_extensions import TypedDict

# 1. Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]

# 2. Build LangGraph
builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_edge(START, "agent")
graph = builder.compile()

# 3. Wrap with AgentCore
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload, context):
    result = graph.invoke({"messages": [("user", payload.get("prompt", ""))]})
    return {"result": result["messages"][-1].content}

app.run()
```

## CLI Workflow

```bash
# Setup
pip install bedrock-agentcore bedrock-agentcore-starter-toolkit langgraph

# Deploy (interactive)
agentcore configure -e agent.py --region us-east-1
agentcore launch

# Deploy (non-interactive/scripted)
agentcore configure -e agent.py --region us-east-1 --name my_agent \
  --non-interactive --disable-memory --deployment-type container

# Test
agentcore invoke '{"prompt": "Hello"}'

# Cleanup
agentcore destroy
```

**Agent naming rules**: Must start with letter, contain only letters/numbers/underscores, 1-48 chars. Use `my_agent` not `my-agent`.

## Architecture Decision Tree

```
Need persistent memory across sessions?
├── Yes → Use AgentCore Memory (references/agentcore-memory.md)
│         - STM: turn-by-turn within session
│         - LTM: insights across sessions/agents
└── No → Use LangGraph checkpointing only

Need external API tools?
├── Yes → Use AgentCore Gateway (references/agentcore-gateway.md)
│         - Lambda → MCP tools (custom code, DB queries)
│         - OpenAPI → MCP tools (REST APIs)
│         - MCP Server → Unite existing MCPs (Nov 2025)
│         - API Gateway → Direct stage integration
└── No → Use LangGraph tools directly

Complex multi-step workflow?
├── Yes → Review LangGraph patterns (references/langgraph-patterns.md)
└── No → Use quick start above
```

## Key Concepts

**AgentCore Runtime**: Wraps any Python agent as HTTP service on port 8080. Handles `/invocations` and `/ping` endpoints.

**AgentCore Memory vs LangGraph Checkpointing**:
- AgentCore Memory: Managed service for cross-session/cross-agent memory
- LangGraph Checkpointing: In-graph state persistence per thread
- Use both together: AgentCore Memory for long-term facts, LangGraph checkpoints for conversation state

**AgentCore Gateway**: Transforms APIs/Lambda into MCP tools with auth handling.

## Reference Files

- **AgentCore CLI**: See [references/agentcore-cli.md](references/agentcore-cli.md) for all primitives + AWS CLI commands
- **AgentCore Runtime**: See [references/agentcore-runtime.md](references/agentcore-runtime.md) for streaming, async, tools examples
- **AgentCore Memory**: See [references/agentcore-memory.md](references/agentcore-memory.md) for STM/LTM patterns + env vars
- **AgentCore Gateway**: See [references/agentcore-gateway.md](references/agentcore-gateway.md) for MCP tool integration
- **LangGraph Patterns**: See [references/langgraph-patterns.md](references/langgraph-patterns.md) for StateGraph best practices

## Utility Scripts

Quick discovery scripts (run from skill directory):

```bash
# List all AgentCore resources in region
./scripts/list-all.sh us-east-1 ag

# Get agent details
./scripts/agent-details.sh langgraph_agent_web_search-Fpc6MyE5Eh us-east-1 ag

# Tail runtime logs
./scripts/tail-logs.sh langgraph_agent_web_search-Fpc6MyE5Eh 5m us-east-1 ag

# Get memory details
./scripts/memory-details.sh langgraph_agent_web_search_mem-4DFwz46tZN us-east-1 ag
```

## Common Patterns

### With Web Search Tool

```python
from langchain_community.tools import DuckDuckGoSearchRun
from langchain.chat_models import init_chat_model
from langgraph.prebuilt import ToolNode, tools_condition

llm = init_chat_model("anthropic.claude-3-haiku-20240307-v1:0", model_provider="bedrock_converse")
tools = [DuckDuckGoSearchRun()]
llm_with_tools = llm.bind_tools(tools)

def agent(state):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
builder.add_edge(START, "agent")
```

### With Streaming Response

```python
@app.entrypoint
async def invoke(payload, context):
    async for chunk in graph.astream({"messages": [("user", payload["prompt"])]}):
        if "agent" in chunk:
            yield chunk["agent"]["messages"][-1].content
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `langgraph.prebuilt` deprecation warning | Still works in 1.0, but `create_react_agent` → `langchain.agents.create_agent` |
| Cold start slow | Use `agentcore launch --local` for testing first |
| Memory not persisting | Check if using AgentCore Memory vs LangGraph checkpointer |
| Tools not executing | Verify `tools_condition` routing and tool binding |
| `ValidationException: on-demand throughput isn't supported` | Claude 4.5 models require inference profiles. Use `us.anthropic.claude-*` not `anthropic.claude-*` |
| `ResourceNotFoundException: Model use case details not submitted` | Fill out Anthropic use case form in AWS Bedrock Console → Model access |
| `Invalid agent name` | Use underscores not hyphens: `my_agent` not `my-agent` |
| Platform mismatch warning (amd64 vs arm64) | Normal - CodeBuild handles cross-platform ARM64 builds automatically |
| Memory `list_events` returns empty | ~10s eventual consistency delay after `create_event`. Also check actor_id/session_id match |
| `'list' object has no attribute 'get'` | `list_events` returns list directly, and `event['payload']` is also a list. See agentcore-memory.md |
| Container not reading .env | Set env vars in Dockerfile ENV, not .env file (container doesn't load .env) |
| Memory not working after deploy | Check logs for "Memory enabled/disabled". Toolkit auto-injects `BEDROCK_AGENTCORE_MEMORY_ID` - don't hardcode in Dockerfile |
| "Memory disabled" in logs | Verify memory configured during `agentcore configure` and `.bedrock_agentcore.yaml` has `memory.memory_id` set |
| Gateway "Unknown tool" error | Lambda must strip `___` prefix from `bedrockAgentCoreToolName`. See agentcore-gateway.md |
| Gateway Lambda timeout | Lambda event format differs from API Gateway - flat dict of input properties only |

## Late 2025 Features (re:Invent)

| Feature | Description | Status |
|---------|-------------|--------|
| **MCP Server Targets** | Unite multiple MCP servers behind single Gateway (Nov 2025) | GA |
| **Policy** | Natural language guardrails (e.g., "allow refunds up to $100") | Preview |
| **Evaluations** | 13 pre-built metrics for correctness, safety, tool accuracy | Preview |
| **Bidirectional Streaming** | Voice agents: listen/respond simultaneously, handle interruptions | GA |
| **Episodic Memory** | Agents learn from experiences across sessions | GA |

## Documentation

**General Resources** (see topic-specific docs in each reference file):

| Resource | URL |
|----------|-----|
| AgentCore Docs | https://docs.aws.amazon.com/bedrock-agentcore/ |
| Starter Toolkit | https://aws.github.io/bedrock-agentcore-starter-toolkit/ |
| GitHub Samples | https://github.com/awslabs/amazon-bedrock-agentcore-samples |
| LangGraph Docs | https://langchain-ai.github.io/langgraph/ |
| CloudFormation | https://docs.aws.amazon.com/AWSCloudFormation/latest/TemplateReference/aws-resource-bedrockagentcore-runtime.html |
