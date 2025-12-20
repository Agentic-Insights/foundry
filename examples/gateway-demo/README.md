# AgentCore Gateway Demo

Demonstrates AWS Bedrock AgentCore Gateway as a managed MCP (Model Context Protocol) server hub.

## What This Shows

1. **MCP Server Unification**: Aggregate multiple tool sources behind one endpoint
2. **Lambda → MCP Conversion**: Wrap Lambda functions as MCP-compatible tools
3. **Semantic Tool Discovery**: Search across 1000s of tools by meaning
4. **LangGraph Integration**: Use gateway tools in AI agents

## Quick Start

```bash
cd examples/gateway-demo
cp .env.example .env
# Edit .env with your AWS profile

uv sync
uv run python gateway_demo.py
```

## Gateway Concepts

### What is a Gateway?

A Gateway is a managed MCP server that:
- Converts various APIs into MCP-compatible tools
- Handles OAuth credential management
- Provides semantic tool discovery
- Unifies tool access behind a single endpoint

### Supported Target Types

| Target Type | Description |
|-------------|-------------|
| **Lambda** | Wrap Lambda functions as MCP tools |
| **OpenAPI** | Convert REST APIs via OpenAPI spec |
| **MCP Server** | Aggregate existing MCP servers |
| **Smithy** | AWS Smithy model definitions |
| **API Gateway** | Direct API Gateway integration |

### Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    AgentCore Gateway                     │
│                                                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  Lambda  │  │  OpenAPI │  │   MCP    │              │
│  │ Function │  │   Spec   │  │  Server  │              │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘              │
│       │             │             │                     │
│       └──────────┬──┴─────────────┘                     │
│                  │                                       │
│          ┌───────▼────────┐                             │
│          │   MCP Tools    │  ← Semantic Discovery       │
│          │   Endpoint     │  ← Credential Mgmt          │
│          └───────┬────────┘                             │
│                  │                                       │
└──────────────────┼───────────────────────────────────────┘
                   │
           ┌───────▼────────┐
           │  LangGraph     │
           │    Agent       │
           └────────────────┘
```

## API Patterns

### Create a Gateway

```python
import boto3

control = boto3.client('bedrock-agentcore-control', region_name='us-east-1')

response = control.create_gateway(
    name="my_gateway",
    description="My tool gateway",
    protocolType="MCP"
)
gateway_id = response['gatewayId']
```

### Add a Lambda Target

```python
control.create_gateway_target(
    gatewayIdentifier=gateway_id,
    name="WebSearch",
    targetConfiguration={
        "mcp": {
            "lambda": {
                "lambdaArn": "arn:aws:lambda:us-east-1:123:function:search",
                "toolSchema": {
                    "inlinePayload": [{
                        "name": "web_search",
                        "description": "Search the web",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "query": {"type": "string"}
                            },
                            "required": ["query"]
                        }
                    }]
                }
            }
        }
    },
    credentialProviderConfigurations=[
        {"credentialProviderType": "GATEWAY_IAM_ROLE"}
    ]
)
```

### Invoke a Gateway Tool

```python
data = boto3.client('bedrock-agentcore', region_name='us-east-1')

response = data.invoke_mcp_tool(
    gatewayIdentifier=gateway_id,
    toolName="web_search",
    arguments={"query": "AgentCore best practices"}
)
result = response.get('result', {})
```

### LangGraph Integration

```python
from langchain_core.tools import StructuredTool

def gateway_tool(tool_name: str):
    def invoke(**kwargs):
        return data.invoke_mcp_tool(
            gatewayIdentifier=gateway_id,
            toolName=tool_name,
            arguments=kwargs
        ).get('result', {})
    return invoke

# Create LangChain tool from gateway
search_tool = StructuredTool.from_function(
    func=gateway_tool("web_search"),
    name="web_search",
    description="Search the web for information"
)

# Use in LangGraph
tools = [search_tool]
llm_with_tools = llm.bind_tools(tools)
```

## One-Click Integrations

AgentCore Gateway provides pre-built integrations for:

- Salesforce
- Slack
- Jira
- Asana
- Zendesk

These integrations handle OAuth flows and credential management automatically.

## Why Gateway Matters

Before Gateway:
- Each MCP server = separate connection
- Credential management scattered
- No unified tool discovery
- Complex integration per service

With Gateway:
- Single MCP endpoint for all tools
- Centralized credential management
- Semantic search across all tools
- Simple integration pattern

## Next Steps

1. Create a Lambda function with your business logic
2. Add it as a gateway target
3. Use `invoke_mcp_tool()` in your LangGraph agent
4. Scale to 1000s of tools with semantic discovery
