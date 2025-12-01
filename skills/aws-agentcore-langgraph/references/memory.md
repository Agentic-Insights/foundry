# AgentCore Memory Integration

## Table of Contents
- [Memory Types](#memory-types)
- [Short-Term Memory (STM)](#short-term-memory-stm)
- [Long-Term Memory (LTM)](#long-term-memory-ltm)
- [LangGraph + AgentCore Memory](#langgraph--agentcore-memory)
- [CLI Memory Commands](#cli-memory-commands)

## Memory Types

| Type | Scope | Use Case |
|------|-------|----------|
| **Short-Term (STM)** | Within session | Turn-by-turn conversation context |
| **Long-Term (LTM)** | Across sessions/agents | User preferences, facts, summaries |
| **LangGraph Checkpointing** | Per thread | Graph state persistence |

**Key Insight**: AgentCore Memory is a managed AWS service. LangGraph checkpointing is in-process. Use both together for full-featured agents.

## Short-Term Memory (STM)

Stores conversation turns within a session.

```python
from bedrock_agentcore.memory import MemoryClient

client = MemoryClient(region_name="us-east-1")

# Create memory (via CLI is easier)
# agentcore memory create my_memory -r us-east-1 --wait

# Store conversation event
client.create_event(
    memory_id=memory_id,
    actor_id="user-123",
    session_id="session-abc",
    messages=[
        ("What's my order status?", "USER"),
        ("Your order shipped yesterday.", "ASSISTANT")
    ]
)

# Retrieve events - returns LIST directly (not dict with "events" key)
events = client.list_events(
    memory_id=memory_id,
    actor_id="user-123",      # REQUIRED
    session_id="session-abc"  # REQUIRED
)
# events = [{'memoryId': '...', 'payload': [...], ...}, ...]
```

### Event Structure

**IMPORTANT**: `list_events` returns a list directly. Each event's `payload` is also a LIST of messages.

```python
# list_events returns:
[
    {
        'memoryId': 'my_memory-abc123',
        'actorId': 'user-123',
        'sessionId': 'session-abc',
        'eventId': '0000001234567890#hash',
        'eventTimestamp': datetime(...),
        'payload': [  # <-- LIST of messages, not a dict!
            {'conversational': {'content': {'text': 'Hello'}, 'role': 'USER'}},
            {'conversational': {'content': {'text': 'Hi there!'}, 'role': 'ASSISTANT'}}
        ],
        'branch': {'name': 'main'}
    },
    # ... more events
]
```

### Parsing Events Correctly

```python
# CORRECT way to parse events
messages = []
for event in events:  # events is a list
    payload_list = event.get("payload", [])  # payload is a LIST
    for msg in payload_list:
        if "conversational" in msg:
            conv = msg["conversational"]
            role = conv.get("role", "").lower()
            content = conv.get("content", {}).get("text", "")
            if role == "user":
                messages.append({"role": "user", "content": content})
            elif role == "assistant":
                messages.append({"role": "assistant", "content": content})
```

### Eventual Consistency

**CRITICAL**: Events are not immediately available after `create_event`. There's ~10 second eventual consistency delay before events appear in `list_events`. Design your agent to handle this gracefully.

## Long-Term Memory (LTM)

Automatically extracts and stores insights across sessions.

```python
# LTM is typically configured during agentcore configure
# It extracts facts like:
# - "User prefers window seats"
# - "Customer has premium account"
# - "Last discussed topic: refund policy"
```

## LangGraph + AgentCore Memory

### Passing Memory ID to Container

Memory ID must be set in the **Dockerfile** ENV, not just .env (container doesn't read .env):

```dockerfile
ENV AGENTCORE_MEMORY_ID=my_memory-abc123
```

Or add to your generated Dockerfile at `.bedrock_agentcore/<agent_name>/Dockerfile`.

### Pattern: Full Working Example

```python
import os
from bedrock_agentcore.memory import MemoryClient
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# Memory setup at module level
memory_id = os.getenv("AGENTCORE_MEMORY_ID")
memory_client = None
if memory_id:
    memory_client = MemoryClient(region_name=os.getenv("AWS_REGION", "us-east-1"))

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload, context):
    user_id = payload.get("user_id", "anonymous")
    session_id = payload.get("session_id", "default")
    prompt = payload.get("prompt", "")

    # 1. Load conversation history from memory
    messages = []
    if memory_client and memory_id:
        try:
            events = memory_client.list_events(
                memory_id=memory_id,
                actor_id=user_id,
                session_id=session_id
            )
            # Parse events correctly (list of events, each with payload list)
            for event in events:
                for msg in event.get("payload", []):
                    if "conversational" in msg:
                        conv = msg["conversational"]
                        role = conv.get("role", "").lower()
                        content = conv.get("content", {}).get("text", "")
                        if role in ("user", "assistant"):
                            messages.append({"role": role, "content": content})
        except Exception as e:
            print(f"Error loading memory: {e}")

    # 2. Add current prompt and invoke graph
    messages.append({"role": "user", "content": prompt})
    result = graph.invoke({"messages": messages})
    response = result["messages"][-1].content

    # 3. Save conversation to memory
    if memory_client and memory_id:
        try:
            memory_client.create_event(
                memory_id=memory_id,
                actor_id=user_id,
                session_id=session_id,
                messages=[(prompt, "USER"), (response, "ASSISTANT")]
            )
        except Exception as e:
            print(f"Error saving memory: {e}")

    return {"result": response}

app.run()
```

### Pattern: Agent with Memory Node

```python
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    messages: Annotated[list, add_messages]
    user_facts: list
    user_id: str

def load_memory_node(state):
    """Load user facts from AgentCore Memory"""
    events = memory_client.list_events(
        memory_id=memory_id,
        actor_id=state["user_id"]
    )
    facts = extract_facts(events)
    return {"user_facts": facts}

def agent_node(state):
    """Agent with access to user facts"""
    context = f"User facts: {state['user_facts']}"
    messages = [("system", context)] + state["messages"]
    response = llm.invoke(messages)
    return {"messages": [response]}

def save_memory_node(state):
    """Save conversation to AgentCore Memory"""
    memory_client.create_event(
        memory_id=memory_id,
        actor_id=state["user_id"],
        session_id="current",
        messages=format_messages(state["messages"][-2:])
    )
    return {}

builder = StateGraph(State)
builder.add_node("load_memory", load_memory_node)
builder.add_node("agent", agent_node)
builder.add_node("save_memory", save_memory_node)

builder.add_edge(START, "load_memory")
builder.add_edge("load_memory", "agent")
builder.add_edge("agent", "save_memory")
builder.add_edge("save_memory", END)

graph = builder.compile()
```

## CLI Memory Commands

```bash
# Create memory
agentcore memory create --name MyMemory --strategy STM

# List memories
agentcore memory list

# Get memory details
agentcore memory get --memory-id mem-123

# Delete memory
agentcore memory delete --memory-id mem-123

# Check status
agentcore memory status --memory-id mem-123
```

## Production Checkpointers

For production LangGraph deployments, use persistent checkpointers:

```python
# PostgreSQL (recommended for production)
from langgraph.checkpoint.postgres import AsyncPostgresSaver

async with AsyncPostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)

# SQLite (local development)
from langgraph.checkpoint.sqlite import SqliteSaver
checkpointer = SqliteSaver.from_conn_string("checkpoints.db")

# Redis (high-performance)
from langgraph.checkpoint.redis import AsyncRedisSaver
checkpointer = AsyncRedisSaver(redis_client)
```

Install with:
```bash
pip install langgraph-checkpoint-postgres  # or -sqlite, -redis
```
