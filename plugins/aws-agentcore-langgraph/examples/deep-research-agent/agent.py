#!/usr/bin/env python3
"""
Deep Research Agent

A production-grade research assistant showcasing ALL AWS Bedrock AgentCore primitives:
- Memory: Cross-session context retention
- Gateway: Unified tool access
- Browser: Dynamic web extraction
- Code Interpreter: Data analysis
- Guardrails: Safety and content filtering
- Runtime: Serverless deployment

Run locally:
    uv run python agent.py

Interactive mode:
    uv run python agent.py --interactive

Deploy to AgentCore:
    agentcore configure -e agent.py --region us-east-1
    agentcore launch
"""

import json
import os
import sys
from datetime import datetime
from typing import Annotated, Literal, TypedDict

import boto3
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langgraph.graph import END, START, StateGraph
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

# =============================================================================
# Configuration
# =============================================================================

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE")
if AWS_PROFILE:
    os.environ["AWS_PROFILE"] = AWS_PROFILE

MODEL_ID = os.getenv("BEDROCK_MODEL_ID", "anthropic.claude-3-haiku-20240307-v1:0")
MEMORY_ID = os.getenv("BEDROCK_AGENTCORE_MEMORY_ID")
GATEWAY_ID = os.getenv("GATEWAY_ID")
CODE_INTERPRETER_ID = os.getenv("CODE_INTERPRETER_ID")
BROWSER_ID = os.getenv("BROWSER_ID")
GUARDRAIL_ID = os.getenv("GUARDRAIL_ID")

print(f"🔧 Configuration:")
print(f"   Region: {AWS_REGION}")
print(f"   Model: {MODEL_ID}")
print(f"   Memory: {MEMORY_ID or 'Will create'}")
print(f"   Gateway: {GATEWAY_ID or 'Disabled'}")
print(f"   Code Interpreter: {CODE_INTERPRETER_ID or 'Disabled'}")
print(f"   Browser: {BROWSER_ID or 'Disabled'}")
print(f"   Guardrails: {GUARDRAIL_ID or 'Disabled'}")
print()

# =============================================================================
# Initialize Clients
# =============================================================================

llm = init_chat_model(MODEL_ID, model_provider="bedrock_converse")

# Memory client
memory_client = None
if MEMORY_ID:
    try:
        from bedrock_agentcore.memory import MemoryClient

        memory_client = MemoryClient(region_name=AWS_REGION)
        print("✅ Memory client initialized")
    except Exception as e:
        print(f"⚠️ Memory client failed: {e}")

# Guardrails client
bedrock_runtime = boto3.client("bedrock-runtime", region_name=AWS_REGION)

# Gateway client
data_client = None
if GATEWAY_ID:
    try:
        data_client = boto3.client("bedrock-agentcore", region_name=AWS_REGION)
        print("✅ Gateway client initialized")
    except Exception as e:
        print(f"⚠️ Gateway client failed: {e}")

# Code interpreter client
if CODE_INTERPRETER_ID:
    print("✅ Code Interpreter configured")


# =============================================================================
# Safety Functions (Guardrails)
# =============================================================================


def check_safety(
    text: str, source: Literal["INPUT", "OUTPUT"] = "INPUT"
) -> tuple[bool, str]:
    """Check text safety using Bedrock Guardrails."""
    if not GUARDRAIL_ID:
        return True, text

    try:
        response = bedrock_runtime.apply_guardrail(
            guardrailIdentifier=GUARDRAIL_ID,
            guardrailVersion="DRAFT",
            source=source,
            content=[{"text": {"text": text}}],
        )

        is_safe = response["action"] != "GUARDRAIL_INTERVENED"
        output_text = text

        if not is_safe:
            outputs = response.get("outputs", [])
            if outputs and "text" in outputs[0]:
                output_text = outputs[0]["text"]

        return is_safe, output_text
    except Exception as e:
        print(f"⚠️ Guardrails check failed: {e}")
        return True, text


# =============================================================================
# Tools
# =============================================================================


@tool
def web_search(query: str) -> str:
    """
    Search the web for information on a topic.

    Args:
        query: The search query

    Returns:
        Search results as text
    """
    # Try Gateway first if configured
    if data_client and GATEWAY_ID:
        try:
            response = data_client.invoke_mcp_tool(
                gatewayIdentifier=GATEWAY_ID,
                toolName="web_search",
                arguments={"query": query},
            )
            return json.dumps(response.get("result", {}))
        except Exception as e:
            print(f"Gateway search failed, falling back to DuckDuckGo: {e}")

    # Fallback to DuckDuckGo
    try:
        from ddgs import DDGS

        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
            formatted = []
            for r in results:
                formatted.append(f"**{r['title']}**\n{r['body']}\nURL: {r['href']}\n")
            return "\n".join(formatted) if formatted else "No results found"
    except Exception as e:
        return f"Search failed: {e}"


@tool
def browse_page(url: str, extract_query: str = "") -> str:
    """
    Browse a web page and extract content.

    Args:
        url: The URL to browse
        extract_query: What to look for on the page (optional)

    Returns:
        Page content or extracted information
    """
    if BROWSER_ID:
        try:
            from bedrock_agentcore.tools.browser_client import browser_session
            from playwright.sync_api import sync_playwright

            with browser_session(AWS_REGION) as client:
                ws_url, headers = client.generate_ws_headers()

                with sync_playwright() as p:
                    browser = p.chromium.connect_over_cdp(ws_url, headers=headers)
                    page = browser.contexts[0].pages[0]

                    page.goto(url, timeout=30000)
                    page.wait_for_load_state("networkidle", timeout=15000)

                    # Extract text content
                    content = page.inner_text("body")[:5000]  # Limit size

                    return f"Content from {url}:\n\n{content}"
        except Exception as e:
            print(f"Browser failed: {e}")

    # Fallback: simple HTTP request
    try:
        import requests

        response = requests.get(url, timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        # Very basic text extraction
        from html.parser import HTMLParser

        class TextExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.text = []

            def handle_data(self, data):
                self.text.append(data.strip())

        parser = TextExtractor()
        parser.feed(response.text)
        content = " ".join(filter(None, parser.text))[:3000]
        return f"Content from {url}:\n\n{content}"
    except Exception as e:
        return f"Failed to browse {url}: {e}"


@tool
def execute_code(code: str, language: str = "python") -> str:
    """
    Execute code in a sandboxed environment.

    Args:
        code: The code to execute
        language: Programming language (python, javascript, typescript)

    Returns:
        Code execution output
    """
    if not CODE_INTERPRETER_ID:
        return "Code execution is not configured. Set CODE_INTERPRETER_ID to enable."

    try:
        response = data_client.invoke_code_interpreter(
            codeInterpreterIdentifier=CODE_INTERPRETER_ID,
            sessionId=f"research-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            name="executeCode",
            arguments={"language": language, "code": code},
        )
        return response.get("result", {}).get("output", "No output")
    except Exception as e:
        return f"Code execution failed: {e}"


@tool
def save_research_note(topic: str, content: str) -> str:
    """
    Save a research note to memory for future reference.

    Args:
        topic: The research topic
        content: The note content

    Returns:
        Confirmation message
    """
    if not memory_client or not MEMORY_ID:
        return "Memory is not configured. Note not saved."

    try:
        memory_client.create_event(
            memory_id=MEMORY_ID,
            actor_id="research-agent",
            session_id="research-notes",
            messages=[(f"[{topic}] {content}", "ASSISTANT")],
        )
        return f"Saved note about '{topic}' to memory"
    except Exception as e:
        return f"Failed to save note: {e}"


# =============================================================================
# Agent State
# =============================================================================


class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    memory_context: str
    blocked: bool


# =============================================================================
# Graph Nodes
# =============================================================================

tools = [web_search, browse_page, execute_code, save_research_note]
llm_with_tools = llm.bind_tools(tools)


def input_guard(state: AgentState) -> dict:
    """Check user input for safety using Guardrails."""
    if not state["messages"]:
        return {"blocked": False}

    last_message = state["messages"][-1]
    if hasattr(last_message, "content"):
        user_input = last_message.content
    else:
        user_input = str(last_message)

    is_safe, _ = check_safety(user_input, "INPUT")

    if not is_safe:
        print("🛡️ Input blocked by Guardrails")
        return {
            "messages": [
                AIMessage(
                    content="I can't process that request due to safety policies. "
                    "Please rephrase your question."
                )
            ],
            "blocked": True,
        }

    return {"blocked": False}


def load_memory(state: AgentState) -> dict:
    """Load relevant memories for context."""
    if not memory_client or not MEMORY_ID:
        return {"memory_context": ""}

    try:
        # Get recent conversation history
        events = memory_client.list_events(
            memory_id=MEMORY_ID, actor_id="research-agent", session_id="research-notes"
        )

        if events:
            notes = []
            for event in events[-5:]:  # Last 5 notes
                for msg in event.get("payload", []):
                    if "conversational" in msg:
                        content = msg["conversational"].get("content", {}).get("text")
                        if content:
                            notes.append(content)

            if notes:
                context = "Previous research notes:\n" + "\n".join(notes)
                return {"memory_context": context}

    except Exception as e:
        print(f"⚠️ Memory load failed: {e}")

    return {"memory_context": ""}


def agent(state: AgentState) -> dict:
    """Main agent reasoning node."""
    if state.get("blocked"):
        return state

    # Build system prompt with memory context
    system_parts = [
        "You are a Deep Research Agent with access to web search, page browsing, "
        "code execution, and memory tools.",
        "",
        "Your research process:",
        "1. Search for relevant sources on the topic",
        "2. Browse specific pages for detailed information",
        "3. Analyze data with code if needed",
        "4. Save key findings to memory",
        "5. Synthesize a comprehensive answer",
        "",
        "Always cite your sources with URLs.",
    ]

    if state.get("memory_context"):
        system_parts.extend(["", state["memory_context"]])

    system_prompt = "\n".join(system_parts)

    # Prepare messages
    messages = [SystemMessage(content=system_prompt)]
    messages.extend(state["messages"])

    # Get response
    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


def output_guard(state: AgentState) -> dict:
    """Check agent output for safety."""
    if state.get("blocked"):
        return state

    last_message = state["messages"][-1]
    if not hasattr(last_message, "content") or not last_message.content:
        return state

    is_safe, sanitized = check_safety(last_message.content, "OUTPUT")

    if not is_safe:
        print("🛡️ Output sanitized by Guardrails")
        return {"messages": [AIMessage(content=sanitized)]}

    return state


def route_after_input_guard(state: AgentState) -> Literal["load_memory", END]:
    """Route based on whether input was blocked."""
    if state.get("blocked"):
        return END
    return "load_memory"


def route_after_agent(state: AgentState) -> Literal["tools", "output_guard"]:
    """Route based on whether agent wants to use tools."""
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"
    return "output_guard"


# =============================================================================
# Build Graph
# =============================================================================

workflow = StateGraph(AgentState)

# Add nodes
workflow.add_node("input_guard", input_guard)
workflow.add_node("load_memory", load_memory)
workflow.add_node("agent", agent)
workflow.add_node("tools", ToolNode(tools=tools))
workflow.add_node("output_guard", output_guard)

# Add edges
workflow.add_edge(START, "input_guard")
workflow.add_conditional_edges("input_guard", route_after_input_guard)
workflow.add_edge("load_memory", "agent")
workflow.add_conditional_edges("agent", route_after_agent)
workflow.add_edge("tools", "agent")
workflow.add_edge("output_guard", END)

# Compile
graph = workflow.compile()


# =============================================================================
# AgentCore Runtime Wrapper
# =============================================================================

from bedrock_agentcore.runtime import BedrockAgentCoreApp

app = BedrockAgentCoreApp()


@app.entrypoint
def invoke(payload, context):
    """
    Main entrypoint for AgentCore Runtime.

    Args:
        payload: Request body (e.g., {"prompt": "Research topic"})
        context: Request context

    Returns:
        Response dict with "result" key
    """
    prompt = payload.get("prompt", "What would you like me to research?")
    user_id = payload.get("user_id", "anonymous")
    session_id = payload.get("session_id", "default")

    print(f"📥 Research request: {prompt[:100]}...")

    try:
        result = graph.invoke(
            {
                "messages": [HumanMessage(content=prompt)],
                "memory_context": "",
                "blocked": False,
            }
        )

        # Extract final response
        response = ""
        for msg in reversed(result["messages"]):
            if hasattr(msg, "content") and msg.content:
                response = msg.content
                break

        print(f"📤 Response: {response[:100]}...")

        # Save to memory if enabled
        if memory_client and MEMORY_ID:
            try:
                memory_client.create_event(
                    memory_id=MEMORY_ID,
                    actor_id=user_id,
                    session_id=session_id,
                    messages=[(prompt, "USER"), (response, "ASSISTANT")],
                )
            except Exception as e:
                print(f"⚠️ Memory save failed: {e}")

        return {"result": response}

    except Exception as e:
        print(f"❌ Error: {e}")
        return {"error": str(e), "status": "failed"}


# =============================================================================
# Interactive Mode
# =============================================================================


def run_interactive():
    """Run the agent in interactive mode."""
    print()
    print("=" * 60)
    print("🔬 Deep Research Agent - Interactive Mode")
    print("=" * 60)
    print()
    print("I can help you research any topic. I'll search the web,")
    print("browse pages, and analyze data to provide comprehensive answers.")
    print()
    print("Commands:")
    print("  'quit' - Exit the agent")
    print("  'clear' - Clear conversation history")
    print()
    print("-" * 60)

    messages = []

    while True:
        try:
            user_input = input("\n🔍 Research: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n👋 Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "q"):
            print("\n👋 Goodbye!")
            break

        if user_input.lower() == "clear":
            messages = []
            print("🗑️ Conversation cleared")
            continue

        # Add user message
        messages.append(HumanMessage(content=user_input))

        print("\n⏳ Researching...")

        try:
            result = graph.invoke(
                {"messages": messages, "memory_context": "", "blocked": False}
            )

            # Update messages with full history
            messages = result["messages"]

            # Print response
            for msg in reversed(result["messages"]):
                if isinstance(msg, AIMessage) and msg.content:
                    print(f"\n📚 Research Results:\n")
                    print(msg.content)
                    break

        except Exception as e:
            print(f"\n❌ Error: {e}")


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    if "--interactive" in sys.argv or "-i" in sys.argv:
        run_interactive()
    else:
        print()
        print("Starting Deep Research Agent server...")
        print("Endpoints:")
        print("  - GET  /ping         - Health check")
        print("  - POST /invocations  - Research request")
        print()
        print('Test: curl -X POST http://localhost:8080/invocations -H "Content-Type: application/json" -d \'{"prompt": "Research quantum computing trends"}\'')
        print()
        app.run()
