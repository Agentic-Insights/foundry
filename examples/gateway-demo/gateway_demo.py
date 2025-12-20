#!/usr/bin/env python3
"""
AgentCore Gateway Demo

Demonstrates AWS Bedrock AgentCore Gateway as a managed MCP server hub that
unifies APIs, Lambda functions, and existing MCP servers into a single endpoint.

Features shown:
- Lambda → MCP: Wrap Lambda functions as MCP tools
- Tool discovery: Semantic search across gateway tools
- LangGraph integration: Use gateway tools in agents

Run locally:
    uv run python gateway_demo.py

Environment variables:
    AWS_PROFILE - AWS profile to use (default: ag)
    AWS_REGION - AWS region (default: us-east-1)
"""

import json
import os
import time
from datetime import datetime
from typing import Annotated

import boto3
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import StructuredTool
from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from typing_extensions import TypedDict

load_dotenv()

# Configure AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "ag")
os.environ["AWS_PROFILE"] = AWS_PROFILE

print(f"🔧 Using AWS Profile: {AWS_PROFILE}, Region: {AWS_REGION}")

# Initialize clients
control_client = boto3.client('bedrock-agentcore-control', region_name=AWS_REGION)
data_client = boto3.client('bedrock-agentcore', region_name=AWS_REGION)


def list_gateways():
    """List existing AgentCore Gateways."""
    print("\n📡 Existing Gateways:")
    response = control_client.list_gateways()
    gateways = response.get('items', [])

    if not gateways:
        print("  (none found)")
        return []

    for gw in gateways:
        print(f"  - {gw['name']} ({gw['gatewayId']}) - {gw['status']}")

    return gateways


def get_or_explain_gateway() -> str | None:
    """Get existing gateway or explain how to create one."""

    # Check for existing gateway
    gateways = control_client.list_gateways().get('items', [])
    for gw in gateways:
        if gw['status'] == 'READY':
            print(f"📦 Found existing gateway: {gw['name']} ({gw['gatewayId']})")
            return gw['gatewayId']

    # No gateway exists - show how to create one
    print("""
    ⚠️  No gateway found. Creating a gateway requires:

    1. An IAM role with gateway permissions
    2. Authorizer configuration (IAM or Custom JWT)

    Create a gateway with AWS CLI:

    ```bash
    # First, create an IAM role for the gateway
    aws iam create-role \\
      --role-name AgentCoreGatewayRole \\
      --assume-role-policy-document '{
        "Version": "2012-10-17",
        "Statement": [{
          "Effect": "Allow",
          "Principal": {"Service": "bedrock-agentcore.amazonaws.com"},
          "Action": "sts:AssumeRole"
        }]
      }'

    # Then create the gateway
    aws bedrock-agentcore-control create-gateway \\
      --name my-gateway \\
      --role-arn arn:aws:iam::YOUR_ACCOUNT:role/AgentCoreGatewayRole \\
      --protocol-type MCP \\
      --authorizer-type IAM \\
      --region us-east-1
    ```

    Or use the AgentCore console for guided setup.
    """)
    return None


def add_lambda_target(gateway_id: str, lambda_arn: str = None):
    """Add a Lambda function as an MCP tool target."""

    # If no Lambda provided, we'll create a simple echo tool
    # In production, you'd point this to your actual Lambda

    print(f"\n🔧 Adding Lambda target to gateway...")

    # For demo purposes, we'll show the API call structure
    # In production, you'd use an actual Lambda ARN

    print("""
    Example Lambda target configuration:

    control_client.create_gateway_target(
        gatewayIdentifier=gateway_id,
        name="WebSearchTool",
        targetConfiguration={
            "mcp": {
                "lambda": {
                    "lambdaArn": "arn:aws:lambda:us-east-1:123456789:function:web-search",
                    "toolSchema": {
                        "inlinePayload": [{
                            "name": "web_search",
                            "description": "Search the web for information",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "query": {
                                        "type": "string",
                                        "description": "Search query"
                                    }
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
    """)


def list_gateway_targets(gateway_id: str):
    """List tools available in a gateway."""
    print(f"\n🔧 Gateway targets for {gateway_id}:")

    try:
        response = control_client.list_gateway_targets(gatewayIdentifier=gateway_id)
        targets = response.get('items', [])

        if not targets:
            print("  (no targets configured)")
            return []

        for target in targets:
            print(f"  - {target['name']} ({target['status']})")

        return targets
    except Exception as e:
        print(f"  Error: {e}")
        return []


def invoke_gateway_tool(gateway_id: str, tool_name: str, arguments: dict):
    """Invoke a tool through the gateway."""
    print(f"\n🚀 Invoking tool: {tool_name}")
    print(f"   Arguments: {json.dumps(arguments)}")

    try:
        response = data_client.invoke_mcp_tool(
            gatewayIdentifier=gateway_id,
            toolName=tool_name,
            arguments=arguments
        )

        result = response.get('result', {})
        print(f"   Result: {json.dumps(result, indent=2)}")
        return result
    except Exception as e:
        print(f"   Error: {e}")
        return None


def create_gateway_langgraph_agent(gateway_id: str):
    """Create a LangGraph agent that uses gateway tools."""

    print(f"\n🤖 Creating LangGraph agent with gateway tools...")

    # Create a tool wrapper for gateway invocation
    def gateway_tool_wrapper(tool_name: str):
        def invoke(**kwargs):
            try:
                response = data_client.invoke_mcp_tool(
                    gatewayIdentifier=gateway_id,
                    toolName=tool_name,
                    arguments=kwargs
                )
                return response.get('result', {})
            except Exception as e:
                return {"error": str(e)}
        return invoke

    # In a real scenario, you'd dynamically discover tools from the gateway
    # For this demo, we'll show the pattern

    print("""
    LangGraph + Gateway Integration Pattern:

    # 1. Discover tools from gateway
    targets = control_client.list_gateway_targets(gatewayIdentifier=gateway_id)

    # 2. Create LangChain tools from gateway targets
    tools = []
    for target in targets:
        for tool in target.get('tools', []):
            tools.append(StructuredTool.from_function(
                func=gateway_tool_wrapper(tool['name']),
                name=tool['name'],
                description=tool['description']
            ))

    # 3. Build LangGraph with these tools
    llm = init_chat_model("claude-haiku-4-5", model_provider="bedrock_converse")
    llm_with_tools = llm.bind_tools(tools)

    # 4. Standard LangGraph ReAct pattern
    builder = StateGraph(State)
    builder.add_node("agent", agent_node)
    builder.add_node("tools", ToolNode(tools=tools))
    builder.add_conditional_edges("agent", tools_condition)
    graph = builder.compile()
    """)


def demonstrate_gateway():
    """Main demo showing AgentCore Gateway capabilities."""

    print(f"\n{'='*60}")
    print("📡 AgentCore Gateway Demo")
    print(f"{'='*60}")

    # Step 1: List existing gateways
    list_gateways()

    # Step 2: Show gateway creation
    print(f"\n{'='*60}")
    print("🆕 DEMO 1: Gateway Creation")
    print(f"{'='*60}")

    print("""
    A Gateway acts as a managed MCP server that can:

    1. Convert Lambda functions → MCP tools
    2. Convert OpenAPI specs → MCP tools
    3. Aggregate multiple MCP servers → Single endpoint
    4. Handle OAuth credentials for external APIs

    Key benefits:
    - Semantic tool discovery across 1000s of tools
    - Centralized credential management
    - Unified MCP endpoint for all tools
    """)

    # Get existing gateway or explain how to create one
    gateway_id = get_or_explain_gateway()

    if not gateway_id:
        print("\n💡 Once you have a gateway, re-run this demo to see full capabilities.")
        return

    # Step 3: Show target configuration
    print(f"\n{'='*60}")
    print("🔧 DEMO 2: Adding Tool Targets")
    print(f"{'='*60}")

    add_lambda_target(gateway_id)
    list_gateway_targets(gateway_id)

    # Step 4: Show LangGraph integration
    print(f"\n{'='*60}")
    print("🤖 DEMO 3: LangGraph Integration")
    print(f"{'='*60}")

    create_gateway_langgraph_agent(gateway_id)

    # Summary
    print(f"\n{'='*60}")
    print("✅ Gateway Demo Complete!")
    print(f"{'='*60}")

    print(f"""
    Gateway ID: {gateway_id}

    What AgentCore Gateway enables:

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

    Next steps:
    1. Create a Lambda function for your tool
    2. Add it as a gateway target
    3. Use invoke_mcp_tool() in your LangGraph agent
    """)


if __name__ == "__main__":
    demonstrate_gateway()
