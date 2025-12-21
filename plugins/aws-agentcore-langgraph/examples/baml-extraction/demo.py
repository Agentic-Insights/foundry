#!/usr/bin/env python3
"""
BAML Extraction Demo

Demonstrates type-safe LLM extraction using BAML for parsing
AWS Bedrock AgentCore memory events.

Usage:
    uv sync
    uv run baml-cli generate
    uv run python demo.py
"""

import os
import json
from dotenv import load_dotenv

load_dotenv()

# Import BAML generated client (after running `baml-cli generate`)
try:
    from baml_client.baml_client.sync_client import b
    from baml_client.baml_client.types import Conversation, AgentResponse, ConversationMessage
    BAML_READY = True
except ImportError:
    BAML_READY = False
    print("BAML client not generated yet. Run: uv run baml-cli generate")


def demo_extract_conversation():
    """Demo: Extract conversation from AgentCore memory events."""
    print("\n" + "="*60)
    print("Demo 1: Extract Conversation from Memory Events")
    print("="*60)

    # Simulated AgentCore memory events (nested structure)
    raw_events = json.dumps([
        {
            "event_id": "evt-001",
            "timestamp": "2025-12-17T10:00:00Z",
            "payload": [
                {
                    "conversational": {
                        "role": "USER",
                        "content": {"text": "What's the latest news about Python 3.13?"}
                    }
                }
            ]
        },
        {
            "event_id": "evt-002",
            "timestamp": "2025-12-17T10:00:05Z",
            "payload": [
                {
                    "conversational": {
                        "role": "ASSISTANT",
                        "content": {"text": "I searched for Python 3.13 news. Python 3.13 introduces several exciting features including improved error messages, a new REPL, and experimental JIT compiler support."}
                    }
                }
            ]
        },
        {
            "event_id": "evt-003",
            "timestamp": "2025-12-17T10:01:00Z",
            "payload": [
                {
                    "conversational": {
                        "role": "USER",
                        "content": {"text": "Tell me more about the JIT compiler."}
                    }
                }
            ]
        }
    ])

    print(f"\nInput: Raw memory events ({len(raw_events)} chars)")
    print("-" * 40)

    # Type-safe extraction with BAML
    conversation: Conversation = b.ExtractConversation(raw_events)

    print(f"\nExtracted Conversation:")
    print(f"  Turn count: {conversation.turn_count}")
    print(f"  Has tool calls: {conversation.has_tool_calls}")
    print(f"  Messages ({len(conversation.messages)}):")

    for i, msg in enumerate(conversation.messages):
        print(f"    [{i+1}] {msg.role}: {msg.content[:50]}...")

    return conversation


def demo_extract_response():
    """Demo: Extract structured info from agent response."""
    print("\n" + "="*60)
    print("Demo 2: Extract Agent Response with Tool Metadata")
    print("="*60)

    raw_response = """Based on my DuckDuckGo search, I found several relevant results about Python 3.13's JIT compiler:

1. The JIT compiler is experimental and opt-in via the --enable-experimental-jit flag
2. It uses a copy-and-patch approach for code generation
3. Performance improvements are promising but still being refined

The search returned results from python.org, Real Python, and several technical blogs. Would you like me to search for more specific benchmarks?"""

    print(f"\nInput: Agent response ({len(raw_response)} chars)")
    print("-" * 40)

    # Type-safe extraction
    response: AgentResponse = b.ExtractAgentResponse(
        raw_response=raw_response,
        tool_names="DuckDuckGo, Calculator, WebBrowser"
    )

    print(f"\nExtracted Response Metadata:")
    print(f"  Main response: {response.main_response[:80]}...")
    print(f"  Tools used: {response.tools_used}")
    print(f"  Confidence: {response.confidence}")
    print(f"  Requires followup: {response.requires_followup}")

    return response


def demo_analyze_tone():
    """Demo: Analyze response tone for monitoring."""
    print("\n" + "="*60)
    print("Demo 3: Response Tone Analysis (Monitoring)")
    print("="*60)

    responses = [
        "I found exactly what you were looking for! Here are the top results.",
        "I'm sorry, but I couldn't find any information about that topic.",
        "Error: Service unavailable. Please try again later.",
    ]

    for i, response in enumerate(responses):
        print(f"\n[{i+1}] Response: {response[:50]}...")
        analysis = b.AnalyzeResponseTone(response)
        print(f"    Tone: {analysis.tone}")
        print(f"    Is error: {analysis.is_error_message}")
        if analysis.suggested_improvement:
            print(f"    Suggestion: {analysis.suggested_improvement}")


def main():
    """Run all demos."""
    print("\n" + "#"*60)
    print("# BAML Extraction Demo for AWS Bedrock AgentCore")
    print("# Testing the baml-dev plugin capabilities")
    print("#"*60)

    if not BAML_READY:
        print("\nSetup required:")
        print("  1. cd examples/baml-extraction")
        print("  2. cp .env.example .env  # Add your ANTHROPIC_API_KEY")
        print("  3. uv sync")
        print("  4. uv run baml-cli generate")
        print("  5. uv run python demo.py")
        return

    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("\nWarning: ANTHROPIC_API_KEY not set.")
        print("Set it in .env or export ANTHROPIC_API_KEY=...")
        print("Falling back to Ollama (if available)")

    # Run demos
    demo_extract_conversation()
    demo_extract_response()
    demo_analyze_tone()

    print("\n" + "="*60)
    print("Demo complete! BAML provides:")
    print("  - Type-safe extraction with Pydantic models")
    print("  - 60% token reduction via optimized prompts")
    print("  - Built-in retry and fallback strategies")
    print("  - Validation at extraction boundaries")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
