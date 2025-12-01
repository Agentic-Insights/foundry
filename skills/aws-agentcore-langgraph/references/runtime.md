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
# Interactive mode (prompts for options)
agentcore configure -e agent.py --region us-east-1

# Non-interactive mode (scripted deployments)
agentcore configure -e agent.py \
  --name my_agent \
  --region us-east-1 \
  --non-interactive \
  --disable-memory \
  --deployment-type container \
  --requirements-file pyproject.toml
```

**Agent naming rules**:
- Must start with a letter
- Only letters, numbers, underscores allowed
- 1-48 characters
- Use `my_agent` NOT `my-agent` (hyphens invalid)

Creates `.bedrock_agentcore.yaml` config file.

### Launch
```bash
# Deploy to AWS (uses CodeBuild for ARM64 container - recommended)
agentcore launch

# Local Docker testing (requires Docker/Podman)
agentcore launch --local

# Alternative: explicit deploy command
agentcore deploy              # CodeBuild (default, recommended)
agentcore deploy --local      # Local development
agentcore deploy --local-build  # Build locally, deploy to cloud
```

**Platform note**: AgentCore requires ARM64 containers. If your machine is x86_64/amd64, you'll see a "platform mismatch" warning - this is normal. CodeBuild (default) handles cross-platform builds automatically. No action needed.

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

### Model ID Format

**Claude 3.x models** support direct on-demand access:
```
anthropic.claude-3-haiku-20240307-v1:0
anthropic.claude-3-5-sonnet-20241022-v2:0
```

**Claude 4.x models** require inference profiles (region prefix):
```
us.anthropic.claude-haiku-4-5-20251001-v1:0      # US inference profile
eu.anthropic.claude-haiku-4-5-20251001-v1:0      # EU inference profile
```

**CRITICAL**: Using `anthropic.claude-haiku-4-5-*` directly causes `ValidationException: on-demand throughput isn't supported`. Always use `us.anthropic.*` or `eu.anthropic.*` prefix for Claude 4.x models.

### Recommended Models

| Model | ID | Notes |
|-------|-----|-------|
| Claude 3 Haiku | `anthropic.claude-3-haiku-20240307-v1:0` | Fast, cheap, on-demand |
| Claude 3.5 Haiku | `anthropic.claude-3-5-haiku-20241022-v1:0` | Better quality, on-demand |
| Claude 3.5 Sonnet | `anthropic.claude-3-5-sonnet-20241022-v2:0` | High quality, on-demand |
| Claude 4.5 Haiku | `us.anthropic.claude-haiku-4-5-20251001-v1:0` | Latest, requires inference profile |

### Example

```python
# Claude 3.5 (on-demand - simpler)
llm = init_chat_model(
    "anthropic.claude-3-5-haiku-20241022-v1:0",
    model_provider="bedrock_converse"
)

# Claude 4.5 (requires US inference profile)
llm = init_chat_model(
    "us.anthropic.claude-haiku-4-5-20251001-v1:0",
    model_provider="bedrock_converse"
)
```

### Model Access Errors

If you get `ResourceNotFoundException: Model use case details have not been submitted`:
1. Go to AWS Bedrock Console → Model access
2. Request access for the Anthropic model
3. Fill out the Anthropic use case form
4. Wait ~15 minutes for approval
