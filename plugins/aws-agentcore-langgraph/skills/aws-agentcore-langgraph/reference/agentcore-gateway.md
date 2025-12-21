# AgentCore Gateway Integration

Gateway transforms APIs, Lambda functions, and MCP servers into unified MCP-compatible tools.

## Quick Start: Lambda → MCP Tool

```bash
# 1. Create gateway (auto-creates IAM role + Cognito auth)
agentcore gateway create-mcp-gateway --name MyGateway --region us-east-1

# 2. Note the output: gateway_arn, gateway_url, role_arn

# 3. Add Lambda target
agentcore gateway create-mcp-gateway-target \
  --gateway-arn "arn:aws:bedrock-agentcore:us-east-1:123456789:gateway/abc123" \
  --gateway-url "https://gateway.bedrock-agentcore.us-east-1.amazonaws.com/abc123" \
  --role-arn "arn:aws:iam::123456789:role/AgentCoreGatewayRole" \
  --name OrderLookup --target-type lambda
```

## Supported Target Types

| Type | CLI `--target-type` | Use Case |
|------|---------------------|----------|
| **Lambda** | `lambda` | Custom code, DB queries, internal APIs |
| **OpenAPI** | `openApiSchema` | REST APIs with OpenAPI spec |
| **MCP Server** | `mcpServer` | Existing MCP servers (Nov 2025) |
| **Smithy** | `smithyModel` | AWS Smithy model definitions |
| **API Gateway** | SDK only | API Gateway stages directly |

## CLI Commands

```bash
# Gateway management
agentcore gateway create-mcp-gateway --name NAME --region REGION
agentcore gateway list-mcp-gateways --region REGION
agentcore gateway get-mcp-gateway --name NAME --region REGION
agentcore gateway delete-mcp-gateway --name NAME --region REGION

# Target management
agentcore gateway create-mcp-gateway-target \
  --gateway-arn ARN --gateway-url URL --role-arn ROLE \
  --name TARGET_NAME --target-type TYPE \
  [--target-payload JSON] [--credentials JSON]

agentcore gateway list-mcp-gateway-targets --gateway-arn ARN
agentcore gateway get-mcp-gateway-target --gateway-arn ARN --name NAME
agentcore gateway delete-mcp-gateway-target --gateway-arn ARN --name NAME
```

## Target Configuration (SDK)

### Lambda Target

```python
import boto3

control = boto3.client('bedrock-agentcore-control', region_name='us-east-1')

# IMPORTANT: Use "mcp" wrapper - this is the correct API structure
control.create_gateway_target(
    gatewayIdentifier="MyGateway",
    name="OrderLookup",
    targetConfiguration={
        "mcp": {
            "lambda": {
                "lambdaArn": "arn:aws:lambda:us-east-1:123456789:function:lookup-order",
                "toolSchema": {
                    "inlinePayload": [
                        {
                            "name": "lookup_order",
                            "description": "Look up order by ID",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "order_id": {
                                        "type": "string",
                                        "description": "The order identifier"
                                    }
                                },
                                "required": ["order_id"]
                            }
                        }
                    ]
                }
            }
        }
    },
    credentialProviderConfigurations=[
        {"credentialProviderType": "GATEWAY_IAM_ROLE"}
    ]
)
```

### OpenAPI Target

```python
control.create_gateway_target(
    gatewayIdentifier="MyGateway",
    name="WeatherAPI",
    targetConfiguration={
        "mcp": {
            "openApiSchema": {
                "s3": {
                    "uri": "s3://my-bucket/weather-api.yaml",
                    "bucketOwnerAccountId": "123456789012"
                }
            }
        }
    },
    credentialProviderConfigurations=[
        {
            "credentialProviderType": "API_KEY",
            "apiKeyCredentialProvider": {
                "providerArn": "arn:aws:bedrock-agentcore:...:api-key-provider/...",
                "credentialParameterName": "x-api-key",
                "credentialLocation": "HEADER"
            }
        }
    ]
)
```

### MCP Server Target (Nov 2025)

Unite multiple MCP servers behind a single gateway:

```python
control.create_gateway_target(
    gatewayIdentifier="MyGateway",
    name="ExternalMCP",
    targetConfiguration={
        "mcp": {
            "mcpServer": {
                "endpoint": "https://mcp.example.com/sse"
            }
        }
    },
    credentialProviderConfigurations=[
        {"credentialProviderType": "GATEWAY_IAM_ROLE"}
    ]
)
```

### API Gateway Stage Target

```python
control.create_gateway_target(
    gatewayIdentifier="MyGateway",
    name="MyRestAPI",
    targetConfiguration={
        "mcp": {
            "apiGateway": {
                "restApiId": "abc123xyz",
                "stage": "prod",
                "apiGatewayToolConfiguration": {
                    "toolFilters": [
                        {"filterPath": "/orders", "methods": ["GET", "POST"]}
                    ],
                    "toolOverrides": [
                        {
                            "path": "/orders",
                            "method": "GET",
                            "name": "list_orders",
                            "description": "List all orders"
                        }
                    ]
                }
            }
        }
    }
)
```

## Lambda Handler Requirements

**Critical:** Lambda handlers for AgentCore Gateway receive a different event format than API Gateway.

### Event Format

```python
# Event is a flat dict of input schema properties
event = {
    "order_id": "ORD-123",
    "include_history": True
}
```

### Context Properties

```python
context.client_context.custom = {
    "bedrockAgentCoreMessageVersion": "1.0",
    "bedrockAgentCoreAwsRequestId": "req-abc123",
    "bedrockAgentCoreMcpMessageId": "mcp-xyz789",
    "bedrockAgentCoreGatewayId": "gateway-id",
    "bedrockAgentCoreTargetId": "target-id",
    "bedrockAgentCoreToolName": "OrderLookup___lookup_order"  # Note prefix!
}
```

### Tool Name Prefix Handling

**Important:** Tool names include a target prefix in format `{target_name}___{tool_name}`. Strip it:

```python
def lambda_handler(event, context):
    # Get the full tool name (includes target prefix)
    full_tool_name = context.client_context.custom.get('bedrockAgentCoreToolName', '')

    # Strip the target prefix (format: "TargetName___actual_tool_name")
    if "___" in full_tool_name:
        tool_name = full_tool_name.split("___")[1]
    else:
        tool_name = full_tool_name

    # Route to appropriate handler
    if tool_name == "lookup_order":
        order_id = event.get("order_id")
        return {"status": "found", "order_id": order_id, "total": 99.99}

    return {"error": f"Unknown tool: {tool_name}"}
```

### Example: Multi-Tool Lambda

```python
import json

def lambda_handler(event, context):
    """Single Lambda serving multiple tools via AgentCore Gateway."""

    tool_name = context.client_context.custom.get('bedrockAgentCoreToolName', '')
    tool_name = tool_name.split("___")[-1]  # Strip prefix

    handlers = {
        "lookup_order": handle_lookup_order,
        "cancel_order": handle_cancel_order,
        "list_orders": handle_list_orders,
    }

    handler = handlers.get(tool_name)
    if not handler:
        return {"error": f"Unknown tool: {tool_name}"}

    return handler(event)

def handle_lookup_order(event):
    order_id = event["order_id"]
    # Query database...
    return {"order_id": order_id, "status": "shipped", "tracking": "1Z999AA10123456784"}

def handle_cancel_order(event):
    order_id = event["order_id"]
    reason = event.get("reason", "Customer request")
    # Cancel logic...
    return {"order_id": order_id, "cancelled": True, "reason": reason}

def handle_list_orders(event):
    customer_id = event["customer_id"]
    limit = event.get("limit", 10)
    # Query database...
    return {"orders": [{"id": "ORD-1"}, {"id": "ORD-2"}], "count": 2}
```

## Credential Provider Types

| Type | Use Case | Configuration |
|------|----------|---------------|
| `GATEWAY_IAM_ROLE` | Lambda, internal AWS | Uses gateway's execution role |
| `API_KEY` | Third-party APIs | Requires provider ARN, location, param name |
| `OAUTH` | OAuth2 APIs | Requires OAuth2 credential provider config |

## Authentication

### Ingress (Agent → Gateway)

Gateway uses OAuth2 with Cognito or custom JWT:

```python
# During gateway creation
auth_config = {
    "customJWTAuthorizer": {
        "allowedClients": ["your-client-id"],
        "discoveryUrl": "https://cognito-idp.us-east-1.amazonaws.com/us-east-1_xxxxx/.well-known/openid-configuration"
    }
}

control.create_gateway(
    name="MyGateway",
    roleArn="arn:aws:iam::...:role/...",
    protocolType="MCP",
    authorizerType="CUSTOM_JWT",
    authorizerConfiguration=auth_config
)
```

### Egress (Gateway → Backend)

Configured per-target via `credentialProviderConfigurations`.

## Using Gateway Tools in LangGraph

### Pattern: Gateway Tool Wrapper

```python
from langchain_core.tools import StructuredTool
from langgraph.prebuilt import ToolNode, tools_condition
import boto3

data_client = boto3.client('bedrock-agentcore', region_name='us-east-1')

def call_gateway_tool(gateway_id: str, tool_name: str, arguments: dict) -> dict:
    """Invoke a tool through AgentCore Gateway."""
    response = data_client.invoke_mcp_tool(
        gatewayIdentifier=gateway_id,
        toolName=tool_name,
        arguments=arguments
    )
    return response.get("result", {})

# Create LangChain tool
lookup_order = StructuredTool.from_function(
    func=lambda order_id: call_gateway_tool("MyGateway", "lookup_order", {"order_id": order_id}),
    name="lookup_order",
    description="Look up order status by ID"
)

# Use in LangGraph
tools = [lookup_order]
llm_with_tools = llm.bind_tools(tools)
builder.add_node("tools", ToolNode(tools))
```

### Pattern: Dynamic Tool Discovery

```python
def discover_gateway_tools(gateway_id: str) -> list:
    """Auto-discover all tools from a gateway."""
    control = boto3.client('bedrock-agentcore-control', region_name='us-east-1')
    data = boto3.client('bedrock-agentcore', region_name='us-east-1')

    targets = control.list_gateway_targets(gatewayIdentifier=gateway_id)

    tools = []
    for target in targets.get("gatewayTargets", []):
        # Each target may expose multiple tools via its schema
        tool = StructuredTool.from_function(
            func=lambda **kwargs, gid=gateway_id, tn=target["name"]:
                call_gateway_tool(gid, tn, kwargs),
            name=target["name"],
            description=target.get("description", f"Tool from {target['name']}")
        )
        tools.append(tool)

    return tools

# Auto-discover at startup
gateway_tools = discover_gateway_tools("MyGateway")
all_tools = [*local_tools, *gateway_tools]
```

## Pre-built Integrations

One-click integrations via AWS Console:
- Salesforce
- Slack
- Jira
- Asana
- Zendesk

Configure under: AgentCore Gateway → Integrations in AWS Console.

## Complete Example: LangGraph + Gateway

```python
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain.chat_models import init_chat_model
from langchain_core.tools import StructuredTool
from bedrock_agentcore.runtime import BedrockAgentCoreApp
import boto3
import os

# Clients
data_client = boto3.client('bedrock-agentcore', region_name='us-east-1')
llm = init_chat_model(
    "us.anthropic.claude-3-5-haiku-20241022-v1:0",
    model_provider="bedrock_converse"
)

GATEWAY_ID = os.getenv("AGENTCORE_GATEWAY_ID", "MyGateway")

# Gateway tool helper
def gateway_tool(tool_name: str):
    def invoke(**kwargs):
        return data_client.invoke_mcp_tool(
            gatewayIdentifier=GATEWAY_ID,
            toolName=tool_name,
            arguments=kwargs
        ).get("result", {})
    return invoke

# Define tools
tools = [
    StructuredTool.from_function(
        func=gateway_tool("lookup_order"),
        name="lookup_order",
        description="Look up order by ID. Input: order_id (string)"
    ),
    StructuredTool.from_function(
        func=gateway_tool("cancel_order"),
        name="cancel_order",
        description="Cancel an order. Input: order_id (string), reason (string, optional)"
    ),
]

llm_with_tools = llm.bind_tools(tools)

# State
class State(TypedDict):
    messages: Annotated[list, add_messages]

def agent(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(State)
builder.add_node("agent", agent)
builder.add_node("tools", ToolNode(tools))
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")
builder.add_edge(START, "agent")
graph = builder.compile()

# AgentCore runtime wrapper
app = BedrockAgentCoreApp()

@app.entrypoint
def invoke(payload, context):
    result = graph.invoke({"messages": [("user", payload.get("prompt", ""))]})
    return {"result": result["messages"][-1].content}

app.run()
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Unknown tool" in Lambda | Strip `___` prefix from `bedrockAgentCoreToolName` |
| Lambda timeout | Increase timeout; Gateway waits for response |
| Auth errors on invoke | Check Cognito token, verify `allowedClients` |
| Tools not discoverable | Verify target status is ACTIVE |
| `SynchronizeGatewayTargets` permission error | Required for semantic search feature |

## Documentation

| Resource | URL |
|----------|-----|
| Gateway Overview | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway.html |
| Lambda Targets | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-add-target-lambda.html |
| Target Configuration | https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/gateway-add-target-api-target-config.html |
| MCP Server Targets | https://aws.amazon.com/blogs/machine-learning/transform-your-mcp-architecture-unite-mcp-servers-through-agentcore-gateway/ |
