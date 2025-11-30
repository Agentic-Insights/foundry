# LangGraph 1.0 Patterns

## Table of Contents
- [State Definition](#state-definition)
- [Graph Building](#graph-building)
- [Tools and Routing](#tools-and-routing)
- [Checkpointing](#checkpointing)
- [Streaming](#streaming)
- [Migration Notes](#migration-notes)

## State Definition

### Basic State

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]  # Accumulates messages
    current_step: str                         # Overwritten each time
```

### With Custom Reducers

```python
import operator

class State(TypedDict):
    messages: Annotated[list, add_messages]      # Built-in message reducer
    search_results: Annotated[list, operator.add] # Concatenate lists
    error_count: Annotated[int, lambda a, b: a + b]  # Sum integers
    config: dict  # No reducer = overwrite
```

### Pydantic State (with validation)

```python
from pydantic import BaseModel, Field

class ValidatedState(BaseModel):
    messages: list = Field(default_factory=list)
    user_id: str
    temperature: float = Field(ge=0.0, le=2.0)
```

## Graph Building

### Basic Pattern

```python
from langgraph.graph import StateGraph, START, END

builder = StateGraph(State)

# Add nodes
builder.add_node("agent", agent_node)
builder.add_node("tools", tool_node)

# Add edges
builder.add_edge(START, "agent")
builder.add_edge("tools", "agent")

# Conditional routing
builder.add_conditional_edges(
    "agent",
    route_function,
    {"continue": "tools", "end": END}
)

graph = builder.compile()
```

### Node Functions

```python
def agent_node(state: State) -> dict:
    """Return partial state updates, don't mutate"""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}  # Merged via add_messages reducer

# Async node
async def async_agent_node(state: State) -> dict:
    response = await llm.ainvoke(state["messages"])
    return {"messages": [response]}
```

### Routing Functions

```python
from langgraph.graph import END

def route_agent(state: State) -> str:
    """Return node name or END"""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END
```

## Tools and Routing

### ToolNode + tools_condition (Standard Pattern)

```python
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool

@tool
def search(query: str) -> str:
    """Search the web."""
    return f"Results for: {query}"

tools = [search]
llm_with_tools = llm.bind_tools(tools)

def agent(state):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("agent", tools_condition)  # Routes to "tools" or END
builder.add_edge("tools", "agent")
builder.add_edge(START, "agent")
```

### Custom Tool Node (Full Control)

```python
from langchain_core.messages import ToolMessage

def custom_tool_node(state: State) -> dict:
    last_message = state["messages"][-1]
    results = []

    for tool_call in last_message.tool_calls:
        tool = tools_by_name[tool_call["name"]]
        result = tool.invoke(tool_call["args"])
        results.append(ToolMessage(
            content=str(result),
            tool_call_id=tool_call["id"]
        ))

    return {"messages": results}
```

### Command Pattern (State Updates from Tools)

New in LangGraph 1.0 - tools can update any state key:

```python
from langgraph.types import Command

@tool
def lookup_user(user_id: str) -> Command:
    """Look up user and store in state."""
    user_info = database.get_user(user_id)

    return Command(
        update={
            "user_info": user_info,  # Updates state["user_info"]
            "messages": [ToolMessage(content=f"Found user: {user_info['name']}", ...)]
        }
    )
```

**Important**: State keys updated via Command need reducers for concurrent tool calls.

## Checkpointing

### In-Memory (Testing)

```python
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()
graph = builder.compile(checkpointer=checkpointer)

config = {"configurable": {"thread_id": "user-123"}}
result = graph.invoke({"messages": [("user", "Hi")]}, config=config)
```

### PostgreSQL (Production)

```python
from langgraph.checkpoint.postgres import AsyncPostgresSaver

async with AsyncPostgresSaver.from_conn_string(DATABASE_URL) as checkpointer:
    graph = builder.compile(checkpointer=checkpointer)

    config = {"configurable": {"thread_id": "user-123"}}
    result = await graph.ainvoke({"messages": [("user", "Hi")]}, config=config)
```

### State Operations

```python
# Get current state
state = graph.get_state(config)
print(state.values)

# Get history
for snapshot in graph.get_state_history(config):
    print(snapshot.config["configurable"]["checkpoint_id"])

# Update state manually
graph.update_state(config, {"custom_field": "value"}, as_node="agent")

# Resume from checkpoint
old_config = {"configurable": {"thread_id": "user-123", "checkpoint_id": "abc123"}}
graph.invoke(None, config=old_config)
```

## Streaming

### Stream Modes

```python
# Updates only (recommended)
async for chunk in graph.astream(inputs, config, stream_mode="updates"):
    for node, output in chunk.items():
        print(f"{node}: {output}")

# Full state after each step
async for chunk in graph.astream(inputs, config, stream_mode="values"):
    print(chunk)

# Messages only
async for chunk in graph.astream(inputs, config, stream_mode="messages"):
    print(chunk)
```

### Token-by-Token Streaming

```python
from langchain_core.callbacks import StreamingStdOutCallbackHandler

llm = init_chat_model(
    "anthropic.claude-3-haiku-20240307-v1:0",
    model_provider="bedrock_converse",
    streaming=True,
    callbacks=[StreamingStdOutCallbackHandler()]
)
```

## Migration Notes

### LangGraph 1.0 Changes

| Old (Pre-1.0) | New (1.0) | Status |
|---------------|-----------|--------|
| `langgraph.prebuilt.create_react_agent` | `langchain.agents.create_agent` | Deprecated |
| `prompt=` parameter | `system_prompt=` parameter | Changed |
| Python 3.9 | Python 3.10+ | Required |
| `ToolNode`, `tools_condition` | Same | Still supported |
| `StateGraph`, nodes, edges | Same | Unchanged |

### Deprecation Warnings

```python
# OLD - Shows deprecation warning
from langgraph.prebuilt import create_react_agent
agent = create_react_agent(model, tools, prompt="...")

# NEW - Recommended
from langchain.agents import create_agent
agent = create_agent(model, tools, system_prompt="...")
```

### What Still Works

- `langgraph.prebuilt.ToolNode` - Still supported
- `langgraph.prebuilt.tools_condition` - Still supported
- `StateGraph`, `add_node`, `add_edge`, `add_conditional_edges` - Unchanged
- All checkpointing APIs - Unchanged

## Best Practices

1. **Compile once at startup** - Don't compile per-request
2. **Use async for production** - `ainvoke`, `astream`
3. **Keep state minimal** - Only persist what's needed
4. **Use reducers strategically** - Only where accumulation needed
5. **Pure node functions** - Return updates, don't mutate state
6. **Thread IDs for multi-tenancy** - Separate conversation contexts

```python
# Good: Compile once
graph = builder.compile(checkpointer=checkpointer)

@app.entrypoint
def invoke(payload, context):
    config = {"configurable": {"thread_id": payload["user_id"]}}
    return graph.invoke({"messages": [("user", payload["prompt"])]}, config)

# Bad: Compile per-request
@app.entrypoint
def invoke(payload, context):
    graph = builder.compile()  # Expensive!
    return graph.invoke(...)
```
