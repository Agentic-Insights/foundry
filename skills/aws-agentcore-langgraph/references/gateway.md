# AgentCore Gateway Integration

## Table of Contents
- [Overview](#overview)
- [Creating a Gateway](#creating-a-gateway)
- [Adding Targets](#adding-targets)
- [Using Gateway Tools in LangGraph](#using-gateway-tools-in-langgraph)
- [Authentication](#authentication)
- [CLI Commands](#cli-commands)

## Overview

AgentCore Gateway transforms APIs and Lambda functions into MCP-compatible tools that LangGraph agents can use.

```
Your Agent → AgentCore Gateway → MCP Protocol → Backend APIs/Lambda
```

**Supported Input Types:**
- OpenAPI specifications
- Smithy models
- AWS Lambda functions
- MCP Servers (group multiple)

## Creating a Gateway

### Via CLI

```bash
# Create gateway
agentcore gateway create-mcp-gateway --name MyToolGateway

# List gateways
agentcore gateway list-mcp-gateways

# Get gateway details
agentcore gateway get-mcp-gateway --name MyToolGateway
```

### Via SDK

```python
import boto3

control_client = boto3.client('bedrock-agentcore-control', region_name='us-east-1')

# Create gateway
response = control_client.create_mcp_gateway(
    name="MyToolGateway",
    description="Tools for my LangGraph agent"
)
gateway_arn = response["gatewayArn"]
```

## Adding Targets

### Lambda Target

```python
# Add Lambda function as tool target
control_client.create_mcp_gateway_target(
    gatewayIdentifier="MyToolGateway",
    name="OrderLookup",
    targetConfiguration={
        "lambdaTarget": {
            "lambdaArn": "arn:aws:lambda:us-east-1:123456789:function:lookup-order",
            "toolSchema": {
                "name": "lookup_order",
                "description": "Look up order by ID",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "order_id": {"type": "string", "description": "Order ID"}
                    },
                    "required": ["order_id"]
                }
            }
        }
    }
)
```

### OpenAPI Target

```python
control_client.create_mcp_gateway_target(
    gatewayIdentifier="MyToolGateway",
    name="WeatherAPI",
    targetConfiguration={
        "openApiTarget": {
            "openApiSpecification": open("weather-api.yaml").read(),
            "baseUrl": "https://api.weather.com"
        }
    }
)
```

## Using Gateway Tools in LangGraph

### Pattern: MCP Tools via Gateway

```python
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode, tools_condition
import boto3

# Create AgentCore data client
data_client = boto3.client('bedrock-agentcore', region_name='us-east-1')

def call_gateway_tool(tool_name: str, arguments: dict) -> str:
    """Call a tool through AgentCore Gateway"""
    response = data_client.invoke_mcp_tool(
        gatewayIdentifier="MyToolGateway",
        toolName=tool_name,
        arguments=arguments
    )
    return response["result"]

# Create LangChain tool wrapper
lookup_order = StructuredTool.from_function(
    func=lambda order_id: call_gateway_tool("lookup_order", {"order_id": order_id}),
    name="lookup_order",
    description="Look up order status by ID"
)

# Use in LangGraph
tools = [lookup_order]
llm_with_tools = llm.bind_tools(tools)

builder = StateGraph(State)
builder.add_node("agent", agent_node)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
```

### Pattern: Dynamic Tool Discovery

```python
def discover_gateway_tools(gateway_name: str) -> list:
    """Dynamically discover tools from gateway"""
    response = control_client.list_mcp_gateway_targets(
        gatewayIdentifier=gateway_name
    )

    tools = []
    for target in response["targets"]:
        tool = StructuredTool.from_function(
            func=lambda **kwargs, tn=target["name"]: call_gateway_tool(tn, kwargs),
            name=target["name"],
            description=target["description"]
        )
        tools.append(tool)

    return tools

# Auto-discover tools at startup
gateway_tools = discover_gateway_tools("MyToolGateway")
all_tools = [*local_tools, *gateway_tools]
```

## Authentication

### Ingress (Agent → Gateway)

```python
# OAuth 2.0 with Cognito
control_client.update_mcp_gateway(
    gatewayIdentifier="MyToolGateway",
    authConfiguration={
        "oauth2": {
            "issuer": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_xxxxx",
            "audience": ["your-client-id"]
        }
    }
)
```

### Egress (Gateway → Backend)

```python
# IAM-based auth for Lambda targets
control_client.create_mcp_gateway_target(
    gatewayIdentifier="MyToolGateway",
    name="SecureAPI",
    targetConfiguration={
        "lambdaTarget": {
            "lambdaArn": "arn:aws:lambda:...",
            "roleArn": "arn:aws:iam::123456789:role/GatewayInvokeRole"
        }
    }
)

# OAuth for third-party APIs
control_client.create_mcp_gateway_target(
    gatewayIdentifier="MyToolGateway",
    name="SalesforceAPI",
    targetConfiguration={
        "openApiTarget": {
            "baseUrl": "https://your-instance.salesforce.com",
            "authConfiguration": {
                "oauth2ClientCredentials": {
                    "tokenEndpoint": "https://login.salesforce.com/services/oauth2/token",
                    "clientId": "{{secretsmanager:sf-client-id}}",
                    "clientSecret": "{{secretsmanager:sf-client-secret}}"
                }
            }
        }
    }
)
```

## CLI Commands

```bash
# Gateway management
agentcore gateway create-mcp-gateway --name MyGateway
agentcore gateway list-mcp-gateways
agentcore gateway get-mcp-gateway --name MyGateway
agentcore gateway delete-mcp-gateway --name MyGateway

# Target management (via SDK/Console)
# CLI support limited - use boto3 or AWS Console
```

## Pre-built Integrations

AgentCore Gateway has one-click integrations for:
- Salesforce
- Slack
- Jira
- Asana
- Zendesk

Configure via AWS Console under AgentCore Gateway → Integrations.

## Complete Example

```python
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
from langchain_core.tools import StructuredTool
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import boto3

# Setup clients
data_client = boto3.client('bedrock-agentcore', region_name='us-east-1')
llm = init_chat_model("anthropic.claude-3-haiku-20240307-v1:0", model_provider="bedrock_converse")

# Gateway tool wrapper
def gateway_tool(tool_name: str):
    def call(**kwargs):
        return data_client.invoke_mcp_tool(
            gatewayIdentifier="MyToolGateway",
            toolName=tool_name,
            arguments=kwargs
        )["result"]
    return call

# Define tools
tools = [
    StructuredTool.from_function(
        func=gateway_tool("lookup_order"),
        name="lookup_order",
        description="Look up order by ID",
    ),
    StructuredTool.from_function(
        func=gateway_tool("send_notification"),
        name="send_notification",
        description="Send notification to user",
    ),
]

llm_with_tools = llm.bind_tools(tools)

# Build graph
class State(TypedDict):
    messages: Annotated[list, add_messages]

def agent(state):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
builder.add_edge(START, "agent")
graph = builder.compile()

# Wrap with AgentCore
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload, context):
    result = graph.invoke({"messages": [("user", payload["prompt"])]})
    return {"result": result["messages"][-1].content}

app.run()
```
