"""
AgentCore Policy Demo - LangGraph Agent

A simple customer service agent that can process refunds.
Demonstrates how Policy Engine blocks unauthorized actions.
"""

import json
import os
import sys
from typing import Annotated, TypedDict

import requests
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
from dotenv import load_dotenv
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode

load_dotenv()


# Load configuration
def load_config():
    try:
        with open("config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ Error: config.json not found!")
        print("Please run 'uv run python setup_policy.py' first.")
        sys.exit(1)


config = load_config()
gateway_url = config["gateway_url"]
region = config["region"]

# Get access token
gateway_client = GatewayClient(region_name=region)
access_token = gateway_client.get_access_token_for_cognito(config["client_info"])


def process_refund(amount: int, reason: str = "Customer request") -> str:
    """
    Process a customer refund through the AgentCore Gateway.
    The Policy Engine will enforce refund limits.

    Args:
        amount: Refund amount in dollars
        reason: Reason for the refund

    Returns:
        Result of the refund request
    """
    response = requests.post(
        gateway_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {access_token}",
        },
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "RefundAPI___process_refund",
                "arguments": {"amount": amount, "reason": reason},
            },
        },
        timeout=30,
    )

    result = response.json()

    if "error" in result:
        return f"❌ POLICY DENIED: Refund of ${amount} was blocked. {result['error'].get('message', 'Authorization failed')}"

    if "result" in result:
        content = result["result"].get("content", [{}])
        if content and "text" in content[0]:
            return f"✅ {content[0]['text']}"

    return f"✅ Refund of ${amount} processed successfully"


# Define the agent state
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]


# Create tool node
tools = [process_refund]
tool_node = ToolNode(tools)


def agent_node(state: AgentState):
    """Simple agent that processes the last message."""
    import boto3

    bedrock = boto3.client("bedrock-runtime", region_name=region)

    # Format messages for Claude
    messages = []
    for msg in state["messages"]:
        if hasattr(msg, "content"):
            role = "user" if msg.type == "human" else "assistant"
            messages.append({"role": role, "content": msg.content})

    # System prompt
    system = f"""You are a helpful customer service agent.
You can process refunds using the process_refund tool.
Current refund policy: Refunds up to ${config['refund_limit']-1} are automatically approved.
Larger refunds require manager approval (which you cannot provide).

When asked to process a refund:
1. Extract the amount and reason
2. Use the process_refund tool
3. Report the result to the customer

Be helpful and professional."""

    # Call Claude
    response = bedrock.converse(
        modelId="anthropic.claude-3-haiku-20240307-v1:0",
        system=[{"text": system}],
        messages=messages,
        toolConfig={
            "tools": [
                {
                    "toolSpec": {
                        "name": "process_refund",
                        "description": "Process a customer refund",
                        "inputSchema": {
                            "json": {
                                "type": "object",
                                "properties": {
                                    "amount": {
                                        "type": "integer",
                                        "description": "Refund amount in dollars",
                                    },
                                    "reason": {
                                        "type": "string",
                                        "description": "Reason for the refund",
                                    },
                                },
                                "required": ["amount"],
                            }
                        },
                    }
                }
            ]
        },
    )

    # Process response
    from langchain_core.messages import AIMessage, ToolMessage

    output = response["output"]["message"]["content"]

    # Check for tool use
    for block in output:
        if "toolUse" in block:
            tool_use = block["toolUse"]
            tool_name = tool_use["name"]
            tool_input = tool_use["input"]

            # Execute the tool
            result = process_refund(**tool_input)

            # Return tool call and result
            return {
                "messages": [
                    AIMessage(
                        content="",
                        tool_calls=[
                            {
                                "id": tool_use["toolUseId"],
                                "name": tool_name,
                                "args": tool_input,
                            }
                        ],
                    ),
                    ToolMessage(content=result, tool_call_id=tool_use["toolUseId"]),
                ]
            }

    # Return text response
    text = ""
    for block in output:
        if "text" in block:
            text += block["text"]

    return {"messages": [AIMessage(content=text)]}


def should_continue(state: AgentState):
    """Check if we should continue or end."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return END


# Build the graph
workflow = StateGraph(AgentState)
workflow.add_node("agent", agent_node)
workflow.add_node("tools", tool_node)
workflow.add_edge(START, "agent")
workflow.add_conditional_edges("agent", should_continue, {"tools": "tools", END: END})
workflow.add_edge("tools", "agent")

graph = workflow.compile()


def main():
    """Interactive demo of the policy-protected agent."""
    print("=" * 60)
    print("🤖 Customer Service Agent (Policy-Protected)")
    print("=" * 60)
    print(f"Refund Limit: ${config['refund_limit']}")
    print()
    print("Try asking:")
    print('  - "I need a refund of $500 for a defective product"')
    print('  - "Please refund $2000 for my order"')
    print()
    print("Type 'quit' to exit")
    print("=" * 60)
    print()

    from langchain_core.messages import HumanMessage

    while True:
        try:
            user_input = input("You: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["quit", "exit", "q"]:
                print("Goodbye!")
                break

            # Run the agent
            result = graph.invoke({"messages": [HumanMessage(content=user_input)]})

            # Print the response
            for msg in result["messages"]:
                if hasattr(msg, "content") and msg.content:
                    if msg.type == "ai":
                        print(f"\nAgent: {msg.content}\n")
                    elif msg.type == "tool":
                        print(f"\n[Tool Result]: {msg.content}\n")

        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")


if __name__ == "__main__":
    main()
