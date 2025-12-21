"""
AgentCore Runtime Demo - Calculator Agent

A simple LangGraph agent that can perform calculations.
Demonstrates the BedrockAgentCoreApp wrapper pattern.
"""

import os
from typing import Annotated, TypedDict

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

# Configure model
llm = init_chat_model(
    os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0"),
    model_provider=os.getenv("BEDROCK_MODEL_PROVIDER", "bedrock_converse"),
)


# Define tools
@tool
def calculate(expression: str) -> str:
    """
    Evaluate a mathematical expression.

    Args:
        expression: A math expression like "2 + 2" or "15 * 7"

    Returns:
        The result of the calculation
    """
    try:
        # Safe evaluation of math expressions
        allowed_names = {"abs": abs, "round": round, "min": min, "max": max}
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return f"The result of {expression} is {result}"
    except Exception as e:
        return f"Error calculating '{expression}': {e}"


@tool
def get_time() -> str:
    """Get the current time."""
    from datetime import datetime

    return f"The current time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"


# Bind tools to model
tools = [calculate, get_time]
llm_with_tools = llm.bind_tools(tools)


# Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]


# Build graph
def chatbot(state: State):
    """Main agent node - decides to respond or use tools."""
    return {"messages": [llm_with_tools.invoke(state["messages"])]}


graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("tools", ToolNode(tools=tools))

graph_builder.add_edge(START, "chatbot")
graph_builder.add_conditional_edges("chatbot", tools_condition)
graph_builder.add_edge("tools", "chatbot")

graph = graph_builder.compile()


# AgentCore Runtime wrapper
from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload, context):
    """
    Main entrypoint for AgentCore Runtime.

    Args:
        payload: Request body (e.g., {"prompt": "What is 2 + 2?"})
        context: Request context (headers, metadata)

    Returns:
        Response dict with "result" key
    """
    prompt = payload.get(
        "prompt", "Hello! I'm a calculator agent. Ask me to calculate something."
    )

    print(f"Received prompt: {prompt}")

    try:
        result = graph.invoke({"messages": [("user", prompt)]})
        response = result["messages"][-1].content
        print(f"Response: {response}")
        return {"result": response}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e), "status": "failed"}


# Run the app (starts HTTP server on port 8080)
if __name__ == "__main__":
    print("Starting Calculator Agent...")
    print("Endpoints:")
    print("  - GET  /ping         - Health check")
    print("  - POST /invocations  - Invoke agent")
    print()
    app.run()
