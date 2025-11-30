# AgentCore Runtime Patterns

## Table of Contents
- [Basic Entrypoint](#basic-entrypoint)
- [Async Streaming](#async-streaming)
- [With Tools](#with-tools)
- [Error Handling](#error-handling)
- [Local Testing](#local-testing)
- [CLI Reference](#cli-reference)

## Basic Entrypoint

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload, context):
    """
    payload: dict - Request body (e.g., {"prompt": "..."})
    context: dict - Request context (headers, metadata)
    """
    prompt = payload.get("prompt", "")
    result = graph.invoke({"messages": [("user", prompt)]})
    return {"result": result["messages"][-1].content}

app.run()  # Starts HTTP server on port 8080
```

## Async Streaming

```python
@app.entrypoint
async def invoke(payload, context):
    """Async generator for streaming responses"""
    async for chunk in graph.astream(
        {"messages": [("user", payload["prompt"])]},
        stream_mode="updates"
    ):
        for node_name, node_output in chunk.items():
            if "messages" in node_output:
                msg = node_output["messages"][-1]
                if hasattr(msg, "content"):
                    yield msg.content
```

### Stream Modes
- `"values"` - Full state after each step
- `"updates"` - Only changed keys per step (recommended)
- `"messages"` - Only message updates

## With Tools

```python
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import ToolNode, tools_condition

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Sunny in {city}"

llm = init_chat_model(
    "anthropic.claude-3-haiku-20240307-v1:0",
    model_provider="bedrock_converse"
)
tools = [get_weather]
llm_with_tools = llm.bind_tools(tools)

def agent_node(state):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
builder.add_edge(START, "agent")
graph = builder.compile()

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload, context):
    result = graph.invoke({"messages": [("user", payload["prompt"])]})
    return {"result": result["messages"][-1].content}

app.run()
```

## Error Handling

```python
@app.entrypoint
def invoke(payload, context):
    try:
        result = graph.invoke({"messages": [("user", payload.get("prompt", ""))]})
        return {"result": result["messages"][-1].content}
    except Exception as e:
        # AgentCore returns HTTP 500 for exceptions
        return {"error": str(e), "status": "failed"}
```

## Local Testing

```bash
# Run locally
python agent.py

# Test with curl
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the weather?"}'

# Health check
curl http://localhost:8080/ping
```

## CLI Reference

### Configure
```bash
agentcore configure -e agent.py \
  --name my-agent \
  --region us-east-1 \
  --disable-memory  # Skip memory setup if not needed
```

Creates `.bedrock_agentcore.yaml` config file.

### Launch
```bash
# Deploy to AWS
agentcore launch

# Local Docker testing
agentcore launch --local

# Or use deploy with CodeBuild (no local Docker needed)
agentcore deploy
```

### Invoke
```bash
# Basic
agentcore invoke '{"prompt": "Hello"}'

# With session
agentcore invoke '{"prompt": "Follow up"}' --session-id abc123

# Local
agentcore invoke '{"prompt": "Test"}' --local
```

### Status
```bash
agentcore status
agentcore status --verbose
```

### Destroy
```bash
agentcore destroy
agentcore destroy --dry-run  # Preview
agentcore destroy --force    # Skip confirmation
```

## Bedrock Models

Common model IDs for `init_chat_model`:

| Model | ID |
|-------|-----|
| Claude 3 Haiku | `anthropic.claude-3-haiku-20240307-v1:0` |
| Claude 3.5 Sonnet | `anthropic.claude-3-5-sonnet-20241022-v2:0` |
| Claude 3.5 Haiku | `anthropic.claude-3-5-haiku-20241022-v1:0` |
| Claude 4.5 Haiku (global) | `global.anthropic.claude-haiku-4-5-20251001-v1:0` |

```python
llm = init_chat_model(
    "anthropic.claude-3-5-sonnet-20241022-v2:0",
    model_provider="bedrock_converse"
)
```
