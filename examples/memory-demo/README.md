# AgentCore Memory Demo

Demonstrates AWS Bedrock AgentCore Memory for cross-session conversation persistence.

## What This Shows

1. **Short-Term Memory (STM)**: Multi-turn conversation within a session
2. **Long-Term Memory (LTM)**: Cross-session knowledge retrieval
3. **Memory Strategies**: Automatic extraction of key information (semantic, summary, user preferences)

## Quick Start

```bash
cd examples/memory-demo
cp .env.example .env
# Edit .env with your AWS profile

uv sync
uv run python memory_demo.py
```

## Modes

### Demo Mode (default)
Shows the memory API in action with a simulated conversation:

```bash
uv run python memory_demo.py
```

Output:
```
🔧 Using AWS Profile: ag, Region: us-east-1
🆕 Creating new AgentCore Memory...
✅ Created memory: memory_demo_20251220-abc123

============================================================
📝 DEMO 1: Short-Term Memory (Conversation History)
============================================================
User: demo-user-001, Session: session-143025

👤 User: What's my name?
🤖 Assistant: I don't know your name yet. What should I call you?
   💾 Saved to memory
...
```

### Interactive Mode
Chat with an LLM that remembers your conversation:

```bash
uv run python memory_demo.py --interactive
```

## Memory Concepts

### Short-Term Memory (Events)
- Stored via `create_event()`
- Contains conversation messages
- Scoped by `actor_id` (user) and `session_id`
- Expires after configured duration (default: 30 days)

### Long-Term Memory (Semantic)
- Extracted automatically by memory strategies
- Searchable via `retrieve_memories()`
- Stores key facts, preferences, and summaries
- Persists across sessions

### Memory Strategies

| Strategy | Purpose |
|----------|---------|
| `SEMANTIC` | Extract key concepts and relationships |
| `SUMMARY` | Maintain conversation summaries |
| `USER_PREFERENCE` | Track user preferences and interests |

## API Patterns

```python
from bedrock_agentcore.memory import MemoryClient

client = MemoryClient(region_name="us-east-1")

# Store conversation
client.create_event(
    memory_id="your-memory-id",
    actor_id="user-123",
    session_id="session-abc",
    messages=[
        ("What's the weather?", "USER"),
        ("It's sunny in Seattle.", "ASSISTANT")
    ]
)

# Retrieve events (short-term)
events = client.list_events(
    memory_id="your-memory-id",
    actor_id="user-123",
    session_id="session-abc"
)

# Retrieve memories (long-term, semantic search)
memories = client.retrieve_memories(
    memory_id="your-memory-id",
    namespace="/user-preferences",
    query="What does the user like?"
)
```

## Important Notes

- **Eventual Consistency**: Events have ~10 second delay before they're retrievable
- **Event Expiry**: Configure 1-365 days retention
- **Namespace**: Use custom namespaces to organize long-term memories

## Next Steps

After running this demo:
1. Note the Memory ID printed at the end
2. Set `BEDROCK_AGENTCORE_MEMORY_ID` in your `.env`
3. Try the `langgraph-web-search` example with memory enabled
