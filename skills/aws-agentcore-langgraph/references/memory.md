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

# Create memory
memory = client.create_memory(
    name="AgentConversationMemory",
    description="Conversation history",
)
memory_id = memory["id"]

# Store conversation event
client.create_event(
    memory_id=memory_id,
    actor_id="user-123",
    session_id="session-abc",
    messages=[
        ("What's my order status?", "USER"),
        ("Let me check order #12345...", "ASSISTANT"),
        ("lookup_order(order_id='12345')", "TOOL"),
        ("Your order shipped yesterday.", "ASSISTANT")
    ]
)

# Retrieve events
events = client.list_events(
    memory_id=memory_id,
    actor_id="user-123",
    session_id="session-abc"
)
```

### Event Structure

```python
# Conversational event payload
{
    "conversational": {
        "content": {"text": "Hello"},
        "role": "USER"  # USER, ASSISTANT, or TOOL
    }
}

# Blob event (for checkpoints/binary data)
{
    "blob": {
        "content": base64_encoded_data,
        "mimeType": "application/json"
    }
}
```

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

### Pattern: Hybrid Memory

Use AgentCore Memory for cross-session facts, LangGraph checkpointing for conversation state.

```python
from langgraph.checkpoint.memory import InMemorySaver
from bedrock_agentcore.memory import MemoryClient
from bedrock_agentcore.runtime import BedrockAgentCoreApp

# AgentCore Memory for long-term facts
memory_client = MemoryClient(region_name="us-east-1")
memory_id = "your-memory-id"

# LangGraph checkpointer for conversation state
checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload, context):
    user_id = payload.get("user_id", "anonymous")
    session_id = payload.get("session_id", "default")
    prompt = payload.get("prompt", "")

    # 1. Load long-term memory
    user_facts = memory_client.list_events(
        memory_id=memory_id,
        actor_id=user_id
    )

    # 2. Build context with facts
    system_context = build_context_from_facts(user_facts)

    # 3. Run graph with LangGraph checkpointing
    config = {"configurable": {"thread_id": f"{user_id}-{session_id}"}}
    result = graph.invoke(
        {"messages": [("system", system_context), ("user", prompt)]},
        config=config
    )

    # 4. Store conversation to AgentCore Memory
    memory_client.create_event(
        memory_id=memory_id,
        actor_id=user_id,
        session_id=session_id,
        messages=[
            (prompt, "USER"),
            (result["messages"][-1].content, "ASSISTANT")
        ]
    )

    return {"result": result["messages"][-1].content}

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
