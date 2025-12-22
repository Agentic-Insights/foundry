# LangGraph + BAML Integration

**Source**: Validated from Hekmatica research agent, BAML docs, community implementations
**Philosophy**: LangGraph orchestrates WHEN/WHERE, BAML defines WHAT/HOW

Using BAML for type-safe extraction within LangGraph workflows.

## Complementary Architecture

**LangGraph's Role**: Orchestration engine for complex agent workflows
- `StateGraph` coordinates data flow between processing steps
- Manages state transitions and conditional routing
- Handles cycles, loops, and multi-agent coordination

**BAML's Role**: Reliable LLM interaction layer
- Defines all LLM calls as typed functions
- Provides structured output parsing with fuzzy matching
- Manages retries, fallbacks, and multi-provider resilience
- Separates prompts from orchestration code

**Integration Pattern**:
```
LangGraph manages: WHEN to call LLMs, WHERE in the workflow
BAML defines: WHAT those LLM calls look like, HOW outputs are validated
```

## Why BAML + LangGraph

| LangGraph Provides | BAML Provides |
|-------------------|---------------|
| Graph orchestration | Type-safe LLM calls |
| State management | Schema validation |
| Conditional routing | Fuzzy JSON parsing |
| Cycles and loops | Retry/fallback handling |

**Key Benefit**: Clean separation of concerns
- `agent.py` (LangGraph) stays focused on workflow logic
- `baml_src/` contains all LLM prompts and schemas
- Type safety across the entire pipeline

## Integration Pattern

### State Definition

```python
from typing import TypedDict
from baml_client.types import ToolCall, ExtractedData

class AgentState(TypedDict):
    messages: list[dict]
    extracted: ExtractedData | None
    tool_calls: list[ToolCall]
    iteration: int
```

### BAML for Node Functions

```python
from langgraph.graph import StateGraph
from baml_client import b

def extract_node(state: AgentState) -> AgentState:
    """Use BAML for structured extraction."""
    result = b.ExtractData(state["messages"][-1]["content"])
    return {"extracted": result}

def route_node(state: AgentState) -> AgentState:
    """Use BAML union types for tool selection."""
    tools = b.SelectTools(state["messages"][-1]["content"])
    return {"tool_calls": tools}

# Build graph
graph = StateGraph(AgentState)
graph.add_node("extract", extract_node)
graph.add_node("route", route_node)
```

### Conditional Routing with BAML Types

```python
from baml_client.types import GetWeather, SearchWeb, Calculator

def route_by_tool(state: AgentState) -> str:
    """Route based on BAML union type."""
    if not state["tool_calls"]:
        return "end"

    tool = state["tool_calls"][0]
    if isinstance(tool, GetWeather):
        return "weather_node"
    elif isinstance(tool, SearchWeb):
        return "search_node"
    elif isinstance(tool, Calculator):
        return "calc_node"
    return "end"

graph.add_conditional_edges("route", route_by_tool)
```

## BAML Schema for LangGraph Agents

### Tool Selection Schema

```baml
class GetWeather {
  type "get_weather"
  location string
  @@stream.done
}

class SearchWeb {
  type "search"
  query string
  @@stream.done
}

class MessageToUser {
  type "message"
  content string @stream.with_state
}

class Resume {
  type "resume"
  @@stream.done
}

function SelectAction(
  state: AgentState,
  query: string
) -> (GetWeather | SearchWeb | MessageToUser | Resume)[] {
  client GPT4
  prompt #"
    {{ Instructions() }}
    Current state: {{ state }}
    Query: {{ query }}
    {{ ctx.output_format }}
  "#
}
```

### State Extraction

```baml
class AgentState {
  context string?
  last_tool_result string?
  iteration int
}

function ParseState(messages: string[]) -> AgentState {
  client GPT4
  prompt #"
    Extract agent state from conversation:
    {% for msg in messages %}
    {{ msg }}
    {% endfor %}
    {{ ctx.output_format }}
  "#
}
```

## Best Practices

1. **BAML for LLM Nodes** - Use BAML functions for any node that calls an LLM
2. **Type Guards for Routing** - Use `isinstance()` with BAML union types
3. **State Types Aligned** - Keep LangGraph state types aligned with BAML types
4. **Stream for UX** - Use `b.stream.FunctionName()` for long-running extractions

## Example Projects

See agent patterns in:
- `baml-examples/python-chatbot/server/baml_src/agent.baml` - Full agent with tool selection and state
- `baml-examples/form-filler/baml_src/form_filler.baml` - Multi-turn form extraction with union actions

## Streaming in LangGraph

```python
async def streaming_node(state: AgentState):
    """Stream BAML responses through LangGraph."""
    stream = b.stream.GenerateResponse(state["messages"])

    async for partial in stream:
        # Yield partial results for real-time UI
        yield {"partial_response": partial.content}

    final = await stream.get_final_response()
    return {"response": final}
```

## Real-World Example: Hekmatica Research Agent

**10-Step Research Workflow** (source: github.com/kargarisaac/Hekmatica):

1. **Clarification** (BAML) - Extract user intent and constraints
2. **User Interaction** (LangGraph) - Conditional routing based on clarity
3. **Query Decomposition** (BAML) - Break complex questions into sub-queries
4. **Planning** (BAML) - Generate research plan with typed steps
5. **Information Gathering** (Python tools) - Web search, API calls
6. **Filtering** (BAML) - Rank/filter results by relevance
7. **Answer Synthesis** (BAML) - Generate structured response with citations
8. **Self-Critique** (BAML) - Evaluate answer quality
9. **Refinement** (LangGraph conditional) - Iterate if quality insufficient
10. **Completion** (LangGraph) - Return final result

**Architecture Split**:
- **LangGraph (agent.py)**: Orchestration (steps 2, 5, 9, 10)
- **BAML (baml_src/)**: Cognitive tasks (steps 1, 3, 4, 6, 7, 8)
- **Python Tools**: External actions (step 5)

**Key Insight**: BAML handles 6/10 steps, all involving LLM reasoning. LangGraph handles state, routing, and tool execution.

## Migration Strategies

### From Pure LangGraph to BAML Integration

**Before** (string prompts):
```python
def planning_node(state: dict) -> dict:
    response = llm.invoke([
        SystemMessage("You are a planner. Output JSON with fields: steps, priority"),
        HumanMessage(state["query"])
    ])
    # Fragile parsing
    plan = json.loads(response.content)
    return {"plan": plan}
```

**After** (BAML):
```python
# In baml_src/planner.baml
class Plan {
  steps string[]
  priority "high" | "medium" | "low"
}

function CreatePlan(query: string) -> Plan {
  client GPT4
  prompt #"
    Create a research plan for: {{ query }}
    {{ ctx.output_format }}
  "#
}

# In agent.py
from baml_client import b

def planning_node(state: dict) -> dict:
    plan = b.CreatePlan(state["query"])  # Type-safe!
    return {"plan": plan}
```

**Benefits**:
- Type safety: `plan.steps` is guaranteed to be `list[str]`
- Fuzzy parsing: Handles messy LLM output automatically
- Centralized prompts: All in `baml_src/`, versioned
- Testable: `baml-cli test` without running full graph

### Migration Checklist

- [ ] Identify all LLM calls in LangGraph nodes
- [ ] Extract prompts to `.baml` files with type definitions
- [ ] Replace `llm.invoke()` with `b.FunctionName()`
- [ ] Keep LangGraph for orchestration (don't change graph structure)
- [ ] Run `baml-cli generate` to create client
- [ ] Update imports: `from baml_client import b`
- [ ] Test nodes individually with `baml-cli test`
- [ ] Test full graph integration

### Common Migration Patterns

**1. Message Formatting**
```baml
class Message {
  role "user" | "assistant" | "system"
  content string
}

function FormatMessages(history: Message[]) -> string {
  client GPT4
  prompt #"
    Summarize conversation:
    {% for msg in history %}
    {{ msg.role }}: {{ msg.content }}
    {% endfor %}
    {{ ctx.output_format }}
  "#
}
```

**2. State Updates**
```baml
class StateUpdate {
  new_context string?
  iteration_complete bool
  next_action "continue" | "stop" | "retry"
}

function UpdateState(
  current_state: AgentState,
  latest_result: string
) -> StateUpdate {
  client GPT4
  prompt #"
    Current: {{ current_state }}
    Result: {{ latest_result }}
    Decide next action.
    {{ ctx.output_format }}
  "#
}
```

**3. Tool Call Decisions**
```baml
function SelectNextTool(
  state: AgentState
) -> GetWeather | SearchWeb | Calculator | None {
  client GPT4
  prompt #"
    State: {{ state }}
    Choose tool or None to finish.
    {{ ctx.output_format }}
  "#
}
```

## Performance Considerations

### When to Use BAML in LangGraph

**✅ Use BAML for**:
- Any LLM call requiring structured output
- Tool selection/routing decisions
- State parsing/updates
- Multi-step reasoning with validation

**⚠️ Keep in LangGraph**:
- Simple string responses (no structure needed)
- State management (TypedDict is fine)
- Conditional routing logic (Python isinstance checks)
- External tool execution (web search, DB queries)

### Optimization Tips

**1. Cache BAML Client Initialization**:
```python
from baml_client import b  # Initialize once at module level

def node_function(state):
    return b.Extract(state["data"])  # Reuse client
```

**2. Async for Parallel Nodes**:
```python
async def parallel_extraction(state):
    results = await asyncio.gather(
        b.ExtractA(state["doc_a"]),
        b.ExtractB(state["doc_b"]),
        b.ExtractC(state["doc_c"])
    )
    return {"results": results}
```

**3. Stream for Long-Running Operations**:
```python
async def long_running_node(state):
    stream = b.stream.ComplexExtraction(state["large_doc"])

    async for partial in stream:
        # Update state incrementally
        yield {"progress": partial}

    final = await stream.get_final_response()
    return {"result": final}
```

## Troubleshooting

### Issue: BAML Types Don't Match LangGraph State

**Problem**: `TypedDict` vs Pydantic mismatch

**Solution**: Convert at boundaries
```python
from baml_client.types import ExtractedData

def baml_node(state: TypedDict) -> dict:
    result: ExtractedData = b.Extract(state["text"])

    # Convert Pydantic → dict for LangGraph
    return {"extracted": result.model_dump()}
```

### Issue: Streaming Not Working in Graph

**Problem**: LangGraph requires generators for streaming

**Solution**: Use `yield` with BAML streams
```python
async def node(state):
    stream = b.stream.Function(state["input"])

    async for partial in stream:
        yield {"partial": partial.model_dump()}  # Must yield

    final = await stream.get_final_response()
    yield {"final": final.model_dump()}
```

---

**References**:
- [Hekmatica Research Agent](https://github.com/kargarisaac/Hekmatica)
- [BAML LangGraph Examples](https://github.com/BoundaryML/baml-examples)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
