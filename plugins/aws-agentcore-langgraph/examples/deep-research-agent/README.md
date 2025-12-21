# Deep Research Agent

A production-grade research assistant showcasing **ALL AWS Bedrock AgentCore primitives** working together.

## What This Agent Does

Given a research topic, the agent:
1. **Searches** the web for relevant sources
2. **Browses** pages to extract detailed information
3. **Analyzes** data with code execution
4. **Remembers** context across sessions
5. **Accesses** enterprise tools via Gateway
6. **Operates safely** with Guardrails protection

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    AgentCore Runtime                            │
│  ┌─────────────────────────────────────────────────────────┐   │
│  │                   LangGraph Agent                        │   │
│  │                                                          │   │
│  │   ┌─────────┐    ┌─────────┐    ┌─────────────────┐    │   │
│  │   │ Planner │───▶│ Executor │───▶│ Synthesizer    │    │   │
│  │   └─────────┘    └────┬────┘    └─────────────────┘    │   │
│  │                       │                                  │   │
│  │         ┌─────────────┼─────────────┐                   │   │
│  │         ▼             ▼             ▼                   │   │
│  │   ┌─────────┐   ┌─────────┐   ┌─────────┐              │   │
│  │   │ Browser │   │  Code   │   │ Gateway │              │   │
│  │   │  Tool   │   │Interpret│   │  Tools  │              │   │
│  │   └─────────┘   └─────────┘   └─────────┘              │   │
│  │                                                          │   │
│  └──────────────────────────┬───────────────────────────────┘   │
│                             │                                    │
│         ┌───────────────────┼───────────────────┐               │
│         ▼                   ▼                   ▼               │
│   ┌─────────┐         ┌─────────┐         ┌─────────┐          │
│   │ Memory  │         │Guardrails│        │ Policy  │          │
│   │         │         │         │         │ Engine  │          │
│   └─────────┘         └─────────┘         └─────────┘          │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## AgentCore Primitives Used

| Primitive | Purpose in Agent |
|-----------|-----------------|
| **Memory** | Remember research context, user preferences, past queries |
| **Gateway** | Access unified MCP tools (search APIs, knowledge bases) |
| **Browser** | Navigate and extract from web pages dynamically |
| **Code Interpreter** | Analyze data, generate charts, run computations |
| **Guardrails** | Block prompt injections, sanitize memory, filter content |
| **Runtime** | Serverless deployment with session isolation |
| **Policy** | Fine-grained access control for tools (optional) |

## Quick Start

### Prerequisites

- AWS account with Bedrock AgentCore access
- Python 3.10+
- AWS credentials configured

### Local Development

```bash
cd examples/deep-research-agent
cp .env.example .env
# Edit .env with your configuration

uv sync
uv run python agent.py
```

### Interactive Mode

```bash
uv run python agent.py --interactive
```

### Deploy to AgentCore Runtime

```bash
# Configure
agentcore configure -e agent.py --region us-east-1 --name deep_research_agent

# Deploy
agentcore launch

# Test
agentcore invoke '{"prompt": "Research the latest developments in quantum computing"}'
```

## How It Works

### 1. Input Guard (Guardrails)

All user input is checked against Guardrails before processing:

```python
def input_guard(state):
    is_safe, _ = check_safety(state["messages"][-1].content)
    if not is_safe:
        return {"blocked": True, "messages": [SAFETY_RESPONSE]}
    return {"blocked": False}
```

### 2. Memory Loading

Previous conversations and extracted knowledge are loaded:

```python
def load_memory(state):
    # Short-term: conversation history
    events = memory_client.list_events(memory_id, user_id, session_id)

    # Long-term: semantic memories
    memories = memory_client.retrieve_memories(
        memory_id, namespace=f"/research/{user_id}",
        query="relevant research context"
    )
    return {"context": memories, "history": events}
```

### 3. Planning

The planner analyzes the research request and creates a plan:

```python
def planner(state):
    plan = llm.invoke([
        SystemMessage("Create a research plan with specific steps."),
        HumanMessage(state["query"])
    ])
    return {"plan": plan, "current_step": 0}
```

### 4. Tool Execution

The executor runs tools based on the plan:

```python
# Web search via Gateway
result = gateway_client.invoke_mcp_tool("web_search", {"query": topic})

# Deep page browsing
with browser_session() as client:
    page = connect_browser(client)
    page.goto(url)
    content = page.inner_text("body")

# Data analysis
result = code_interpreter.invoke("python", analysis_code)
```

### 5. Synthesis

The synthesizer compiles findings into a research report:

```python
def synthesizer(state):
    report = llm.invoke([
        SystemMessage("Synthesize research findings into a report."),
        HumanMessage(json.dumps(state["findings"]))
    ])
    return {"report": report}
```

### 6. Memory Persistence

Conversations and key insights are saved:

```python
def save_memory(state):
    # Save conversation
    memory_client.create_event(
        memory_id, user_id, session_id,
        messages=[(query, "USER"), (report, "ASSISTANT")]
    )
    return state
```

### 7. Output Guard (Guardrails)

Final output is checked before returning:

```python
def output_guard(state):
    is_safe, sanitized = check_safety(state["report"], "OUTPUT")
    if not is_safe:
        return {"report": sanitized}
    return state
```

## Configuration

### Environment Variables

```bash
# AWS
AWS_REGION=us-east-1
AWS_PROFILE=default

# Model
BEDROCK_MODEL_ID=us.anthropic.claude-haiku-4-5-20251001-v1:0

# Memory (auto-created if not set)
BEDROCK_AGENTCORE_MEMORY_ID=your-memory-id

# Gateway (optional - for enterprise tools)
GATEWAY_ID=your-gateway-id

# Code Interpreter (optional - for analysis)
CODE_INTERPRETER_ID=your-code-interpreter-id

# Browser (optional - for deep research)
BROWSER_ID=your-browser-id

# Guardrails (recommended for production)
GUARDRAIL_ID=your-guardrail-id
```

### Minimal Setup

For basic functionality, you only need:
- `AWS_REGION`
- `BEDROCK_MODEL_ID`

Other primitives are enabled when their IDs are provided.

## Example Interactions

### Simple Query
```
You: What are the key trends in AI agent development?

Agent: Based on my research, here are the key trends in AI agent development:

1. **Agentic AI Frameworks**: Tools like LangGraph, AutoGen, and CrewAI...
2. **Tool Use**: Agents increasingly use external tools...
3. **Memory Systems**: Long-term memory for personalization...
...

Sources:
- https://example.com/ai-trends
- https://example.com/agent-frameworks
```

### Deep Research with Analysis
```
You: Analyze the market share of cloud providers over the past 5 years

Agent: [Using web search to find market data...]
       [Browsing detailed reports...]
       [Running analysis code...]

       Here's my analysis:

       [Generated chart: cloud_market_share.png]

       AWS maintained leadership with 32% share...
       Azure grew from 15% to 23%...
       GCP reached 10%...
```

### Cross-Session Memory
```
Session 1:
You: I'm interested in renewable energy research

Session 2:
You: What should I research next?
Agent: Based on your interest in renewable energy, I suggest exploring...
```

## Customization

### Adding Custom Tools

```python
@tool
def company_knowledge_base(query: str) -> str:
    """Search internal company knowledge base."""
    # Your implementation
    pass

# Add to tools list
tools = [web_search, browse_page, execute_code, company_knowledge_base]
```

### Custom Memory Strategies

```python
memory_strategies = [
    {
        "semanticMemoryStrategy": {
            "name": "research_facts",
            "description": "Extract key research findings",
            "namespaces": ["/research/{actorId}/facts"]
        }
    },
    {
        "semanticMemoryStrategy": {
            "name": "user_preferences",
            "description": "Extract user interests and preferences",
            "namespaces": ["/research/{actorId}/preferences"]
        }
    }
]
```

### Custom Guardrails

Create a guardrail with specific policies for research:
- Block requests for harmful content generation
- Filter PII from research results
- Prevent jailbreak attempts

## Deployment Options

### Option 1: Local Development
```bash
uv run python agent.py
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Research quantum computing"}'
```

### Option 2: AgentCore Runtime
```bash
agentcore configure -e agent.py --region us-east-1
agentcore launch
agentcore invoke '{"prompt": "Research quantum computing"}'
```

### Option 3: Container Deployment
```bash
docker build -t deep-research-agent .
docker run -p 8080:8080 deep-research-agent
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Memory not persisting | Check BEDROCK_AGENTCORE_MEMORY_ID is set |
| Browser timeouts | Increase timeout or use simpler pages |
| Code interpreter errors | Check CODE_INTERPRETER_ID is valid |
| Guardrails blocking valid requests | Adjust filter strength |
| Gateway tool not found | Verify GATEWAY_ID and tool names |

## Cost Considerations

| Primitive | Pricing Model |
|-----------|--------------|
| Runtime | Per-session + compute time |
| Memory | Storage + API calls |
| Browser | Per-session time |
| Code Interpreter | Per-execution |
| Gateway | API calls |
| Guardrails | Per-evaluation |

For cost optimization:
- Use session reuse where possible
- Cache frequent queries
- Batch memory operations
- Use lighter models for simple tasks

## Security Best Practices

1. **Always enable Guardrails** for production
2. **Sanitize memory** before storage
3. **Use Policy Engine** for tool access control
4. **Rotate credentials** regularly
5. **Monitor CloudWatch** for anomalies
6. **Limit session duration** as needed

## References

- [AgentCore Documentation](https://docs.aws.amazon.com/bedrock-agentcore/)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Agentic Insights](https://agenticinsights.com)
