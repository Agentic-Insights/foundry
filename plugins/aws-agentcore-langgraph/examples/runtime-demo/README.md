# AgentCore Runtime Demo

Deploy LangGraph agents as serverless, containerized workloads with session isolation using AWS Bedrock AgentCore Runtime.

## What This Demo Shows

- **BedrockAgentCoreApp wrapper** - Simple entrypoint pattern for any LangGraph agent
- **Session isolation** - Each session runs in a dedicated microVM
- **Long-running support** - Up to 8 hours per session
- **agentcore CLI** - Configure, deploy, invoke, and manage agents

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     AgentCore Runtime                           │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │                     MicroVM (Firecracker)                  │ │
│  │  ┌─────────────────────────────────────────────────────┐  │ │
│  │  │              Your LangGraph Agent                    │  │ │
│  │  │                                                      │  │ │
│  │  │   User Request  →  BedrockAgentCoreApp               │  │ │
│  │  │                         ↓                            │  │ │
│  │  │                    @app.entrypoint                   │  │ │
│  │  │                         ↓                            │  │ │
│  │  │                   graph.invoke()                     │  │ │
│  │  │                         ↓                            │  │ │
│  │  │                   JSON Response                      │  │ │
│  │  └─────────────────────────────────────────────────────┘  │ │
│  └───────────────────────────────────────────────────────────┘ │
│                              ↓                                  │
│  ┌───────────────────────────────────────────────────────────┐ │
│  │  Session State: user_id, session_id, memory_id           │ │
│  └───────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

## Prerequisites

- AWS account with Bedrock AgentCore access
- Python 3.10+
- AWS CLI configured
- `agentcore` CLI installed (`uv add bedrock-agentcore-starter-toolkit`)

## Quick Start

```bash
# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Test locally first
uv run python agent.py

# In another terminal, test the agent
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is 2 + 2?"}'
```

## Deploy to AWS

### Step 1: Configure

```bash
# Interactive mode (recommended for first time)
agentcore configure -e agent.py --region us-east-1

# Non-interactive mode (for CI/CD)
agentcore configure -e agent.py \
  --name my_calculator_agent \
  --region us-east-1 \
  --non-interactive \
  --deployment-type container \
  --requirements-file pyproject.toml
```

**Agent naming rules:**
- Must start with a letter
- Only letters, numbers, underscores allowed
- 1-48 characters
- Use `my_agent` NOT `my-agent` (hyphens are invalid)

This creates `.bedrock_agentcore.yaml`:

```yaml
agent_name: my_calculator_agent
aws_region: us-east-1
entrypoint: agent.py
deployment_type: container
```

### Step 2: Launch (Deploy)

```bash
# Deploy using AWS CodeBuild (recommended - handles ARM64 builds)
agentcore launch
```

**What happens:**
1. Packages your code and dependencies
2. Uploads to S3
3. CodeBuild creates ARM64 container
4. Deploys to AgentCore Runtime
5. Returns endpoint URL

### Step 3: Invoke

```bash
# Basic invocation
agentcore invoke '{"prompt": "What is 15 * 7?"}'

# With session ID (maintains state across calls)
agentcore invoke '{"prompt": "Remember my name is Alice"}' --session-id alice-123
agentcore invoke '{"prompt": "What is my name?"}' --session-id alice-123
```

### Step 4: Monitor

```bash
# Check status
agentcore status

# Verbose output
agentcore status --verbose

# View logs in CloudWatch
aws logs tail /aws/bedrock-agentcore/my_calculator_agent --follow
```

### Step 5: Cleanup

```bash
# Destroy all resources
agentcore destroy

# Preview what will be deleted
agentcore destroy --dry-run

# Skip confirmation prompt
agentcore destroy --force
```

## Code Pattern

### Minimal Agent

```python
from bedrock_agentcore.runtime import BedrockAgentCoreApp
from langgraph.graph import StateGraph, START

# Build your LangGraph
builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_edge(START, "agent")
graph = builder.compile()

# Wrap with AgentCore
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

### With Memory Integration

```python
from bedrock_agentcore.memory import MemoryClient
import os

memory_id = os.getenv("BEDROCK_AGENTCORE_MEMORY_ID")  # Auto-injected
memory_client = MemoryClient() if memory_id else None

@app.entrypoint
def invoke(payload, context):
    user_id = payload.get("user_id", "anonymous")
    session_id = payload.get("session_id", "default")

    # Load conversation history
    messages = []
    if memory_client and memory_id:
        events = memory_client.list_events(
            memory_id=memory_id,
            actor_id=user_id,
            session_id=session_id
        )
        # ... extract messages from events

    # Add current prompt
    messages.append({"role": "user", "content": payload["prompt"]})

    # Run agent
    result = graph.invoke({"messages": messages})
    response = result["messages"][-1].content

    # Save to memory
    if memory_client and memory_id:
        memory_client.create_event(
            memory_id=memory_id,
            actor_id=user_id,
            session_id=session_id,
            messages=[(payload["prompt"], "USER"), (response, "ASSISTANT")]
        )

    return {"result": response}
```

### Async Streaming

```python
@app.entrypoint
async def invoke(payload, context):
    """Stream responses using async generator."""
    async for chunk in graph.astream(
        {"messages": [("user", payload["prompt"])]},
        stream_mode="updates"
    ):
        for node_name, node_output in chunk.items():
            if "messages" in node_output:
                yield node_output["messages"][-1].content
```

## Environment Variables

| Variable | Description | Auto-Injected |
|----------|-------------|---------------|
| `BEDROCK_AGENTCORE_MEMORY_ID` | Memory instance ID | ✅ Yes (if configured) |
| `AWS_REGION` | AWS region | ✅ Yes |
| `AWS_ACCESS_KEY_ID` | AWS credentials | ✅ Yes |
| `AWS_SECRET_ACCESS_KEY` | AWS credentials | ✅ Yes |
| `BEDROCK_MODEL_ID` | Model to use | ❌ No (set in .env) |

## Bedrock Models

### Claude 3.x (Direct Access)
```python
llm = init_chat_model(
    "anthropic.claude-3-haiku-20240307-v1:0",
    model_provider="bedrock_converse"
)
```

### Claude 4.x (Requires Inference Profile)
```python
# Must use region prefix!
llm = init_chat_model(
    "us.anthropic.claude-haiku-4-5-20251001-v1:0",  # US prefix required
    model_provider="bedrock_converse"
)
```

**Important:** Using `anthropic.claude-haiku-4-5-*` directly causes:
```
ValidationException: on-demand throughput isn't supported
```
Always use `us.anthropic.*` or `eu.anthropic.*` prefix for Claude 4.x models.

## Local Development

```bash
# Run agent locally
uv run python agent.py

# Test endpoints
curl http://localhost:8080/ping                    # Health check
curl -X POST http://localhost:8080/invocations \   # Invoke
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'

# Local Docker testing (if needed)
agentcore launch --local
agentcore invoke '{"prompt": "Test"}' --local
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Platform mismatch warning | Normal on x86_64 machines. CodeBuild handles ARM64 builds. |
| `ResourceNotFoundException` | Request Bedrock model access in AWS Console |
| `ValidationException: on-demand` | Use inference profile (`us.anthropic.*`) for Claude 4.x |
| Deployment timeout | Check CloudWatch logs for build errors |
| Invoke returns empty | Verify agent returns `{"result": ...}` format |

## Session Management

Sessions provide isolation and state persistence:

```bash
# Different sessions = independent state
agentcore invoke '{"prompt": "I am Alice"}' --session-id session-1
agentcore invoke '{"prompt": "I am Bob"}' --session-id session-2

# Same session = shared state
agentcore invoke '{"prompt": "Who am I?"}' --session-id session-1  # "Alice"
agentcore invoke '{"prompt": "Who am I?"}' --session-id session-2  # "Bob"
```

Sessions persist for up to 8 hours of inactivity.

## CI/CD Integration

```yaml
# GitHub Actions example
deploy:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: astral-sh/setup-uv@v4
    - run: uv sync
    - run: |
        agentcore configure -e agent.py \
          --name my_agent \
          --region us-east-1 \
          --non-interactive
        agentcore launch
      env:
        AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
        AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

## References

- [Runtime Overview](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime.html)
- [Runtime Quick Start](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/runtime-quick-start.html)
- [CLI Reference](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/agentcore-cli.html)
