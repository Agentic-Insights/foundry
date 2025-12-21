from typing import Annotated

from langchain.chat_models import init_chat_model
from typing_extensions import TypedDict

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

import logging
import os
from dotenv import load_dotenv

load_dotenv()

langchain_logger = logging.getLogger("langchain")
langchain_logger.setLevel(logging.DEBUG)

print("Starting up...")
os.environ["LANGSMITH_OTEL_ENABLED"] = os.getenv("LANGSMITH_OTEL_ENABLED", "true")

llm = init_chat_model(
    os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0"),
    model_provider=os.getenv("BEDROCK_MODEL_PROVIDER", "bedrock_converse"),
)

## Define search tool
from langchain_community.tools import DuckDuckGoSearchRun
search = DuckDuckGoSearchRun()
tools = [search]
llm_with_tools = llm.bind_tools(tools)

print("Defining state...")
## Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]


graph_builder = StateGraph(State)


def chatbot(state: State):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

print("Configuring graph...")
graph_builder.add_node("chatbot", chatbot)

tool_node = ToolNode(tools=tools)

graph_builder.add_node("tools", tool_node)

graph_builder.add_conditional_edges(
    "chatbot",
    tools_condition,
)
# Any time a tool is called, we return to the chatbot to decide the next step
graph_builder.add_edge("tools", "chatbot")
graph_builder.add_edge(START, "chatbot")
graph = graph_builder.compile()
graph_configured = True

# Memory setup
from bedrock_agentcore.memory import MemoryClient

memory_id = os.getenv("BEDROCK_AGENTCORE_MEMORY_ID")
memory_client = None

if memory_id:
    print(f"Memory enabled: {memory_id}")
    memory_client = MemoryClient(region_name=os.getenv("AWS_REGION", "us-east-1"))
else:
    print("Memory disabled (BEDROCK_AGENTCORE_MEMORY_ID not set)")

from bedrock_agentcore.runtime import BedrockAgentCoreApp
app = BedrockAgentCoreApp()

@app.entrypoint
def agent_invocation(payload, context):

    print("received payload")
    print(payload)

    user_id = payload.get("user_id", "anonymous")
    session_id = payload.get("session_id", "default")
    prompt = payload.get("prompt", "No prompt found in input, please guide customer as to what tools can be used")

    # Load conversation history from memory
    messages = []
    if memory_client and memory_id:
        try:
            events = memory_client.list_events(
                memory_id=memory_id,
                actor_id=user_id,
                session_id=session_id
            )
            # events is a list directly
            event_list = events if isinstance(events, list) else events.get("events", [])
            for event in event_list:
                # payload is a LIST of message objects
                payload_list = event.get("payload", []) if isinstance(event, dict) else []
                for msg in payload_list:
                    if "conversational" in msg:
                        conv = msg["conversational"]
                        role = conv.get("role", "").lower()
                        content = conv.get("content", {}).get("text", "")
                        if role == "user":
                            messages.append({"role": "user", "content": content})
                        elif role == "assistant":
                            messages.append({"role": "assistant", "content": content})
            print(f"Loaded {len(messages)} messages from memory")
        except Exception as e:
            print(f"Error loading memory: {e}")

    # Add current prompt
    messages.append({"role": "user", "content": prompt})

    tmp_output = graph.invoke({"messages": messages})
    print(tmp_output)

    response_content = tmp_output['messages'][-1].content

    # Save conversation to memory
    if memory_client and memory_id:
        try:
            memory_client.create_event(
                memory_id=memory_id,
                actor_id=user_id,
                session_id=session_id,
                messages=[
                    (prompt, "USER"),
                    (response_content, "ASSISTANT")
                ]
            )
            print("Saved conversation to memory")
        except Exception as e:
            print(f"Error saving to memory: {e}")

    return {"result": response_content}

app.run()
