#!/usr/bin/env python3
"""
AgentCore Memory Demo

Demonstrates AWS Bedrock AgentCore Memory for cross-session conversation persistence.

Features shown:
- Short-term memory (STM): Multi-turn conversation within a session
- Long-term memory (LTM): Cross-session knowledge retrieval
- Memory strategies: Automatic extraction of key information

Run locally:
    uv run python memory_demo.py

Environment variables:
    AWS_PROFILE - AWS profile to use (default: ag)
    AWS_REGION - AWS region (default: us-east-1)
    BEDROCK_AGENTCORE_MEMORY_ID - Memory ID (created if not provided)
"""

import os
import sys
import time
from datetime import datetime
from typing import Annotated

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

load_dotenv()

# Configure AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "ag")
os.environ["AWS_PROFILE"] = AWS_PROFILE

print(f"🔧 Using AWS Profile: {AWS_PROFILE}, Region: {AWS_REGION}")


def create_memory_if_needed() -> str:
    """Create a new AgentCore Memory if BEDROCK_AGENTCORE_MEMORY_ID not set."""
    import boto3

    memory_id = os.getenv("BEDROCK_AGENTCORE_MEMORY_ID")
    if memory_id:
        print(f"📦 Using existing memory: {memory_id}")
        return memory_id

    print("🆕 Creating new AgentCore Memory...")
    client = boto3.client('bedrock-agentcore-control', region_name=AWS_REGION)

    # Generate unique name
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    memory_name = f"memory_demo_{timestamp}"

    response = client.create_memory(
        name=memory_name,
        description="Demo memory for AgentCore Memory showcase",
        # Memory strategies control how information is extracted and stored
        memoryStrategies=[
            {
                "semanticMemoryStrategy": {
                    "name": "demo_semantic",
                    "description": "Extract key facts and preferences",
                    "namespaces": ["/demo/{actorId}/memories"]
                }
            }
        ],
        # Event expiration (in days)
        eventExpiryDuration=30
    )

    memory_id = response['memory']['id']
    print(f"✅ Created memory: {memory_id}")
    print(f"   Set BEDROCK_AGENTCORE_MEMORY_ID={memory_id} to reuse")

    # Wait for memory to be active
    print("⏳ Waiting for memory to become active...")
    for _ in range(30):
        status = client.get_memory(memoryId=memory_id)
        if status['memory']['status'] == 'ACTIVE':
            print("✅ Memory is active!")
            break
        time.sleep(2)

    return memory_id


def demonstrate_memory():
    """Main demo showing AgentCore Memory capabilities."""
    from bedrock_agentcore.memory import MemoryClient

    # Setup
    memory_id = create_memory_if_needed()
    memory_client = MemoryClient(region_name=AWS_REGION)

    # Demo user/session
    user_id = "demo-user-001"
    session_id = f"session-{datetime.now().strftime('%H%M%S')}"

    print(f"\n{'='*60}")
    print("📝 DEMO 1: Short-Term Memory (Conversation History)")
    print(f"{'='*60}")
    print(f"User: {user_id}, Session: {session_id}\n")

    # Simulate a conversation
    conversations = [
        ("What's my name?", "I don't know your name yet. What should I call you?"),
        ("My name is Alex", "Nice to meet you, Alex! I'll remember that."),
        ("What do I like?", "You haven't told me your preferences yet. What are you interested in?"),
        ("I love Python and AWS", "Great! I'll remember that you love Python and AWS."),
    ]

    for user_msg, assistant_msg in conversations:
        print(f"👤 User: {user_msg}")
        print(f"🤖 Assistant: {assistant_msg}")

        # Store in memory
        memory_client.create_event(
            memory_id=memory_id,
            actor_id=user_id,
            session_id=session_id,
            messages=[
                (user_msg, "USER"),
                (assistant_msg, "ASSISTANT")
            ]
        )
        print("   💾 Saved to memory\n")
        time.sleep(0.5)  # Small delay for API

    # Wait for eventual consistency (~10 seconds)
    print("⏳ Waiting for memory consistency (10s)...")
    time.sleep(10)

    # Retrieve conversation history
    print(f"\n{'='*60}")
    print("📖 DEMO 2: Retrieving Conversation History")
    print(f"{'='*60}\n")

    events = memory_client.list_events(
        memory_id=memory_id,
        actor_id=user_id,
        session_id=session_id
    )

    print(f"Found {len(events)} events in memory:\n")
    for i, event in enumerate(events, 1):
        print(f"Event {i}:")
        payload = event.get("payload", [])
        for msg in payload:
            if "conversational" in msg:
                conv = msg["conversational"]
                role = conv.get("role", "").upper()
                content = conv.get("content", {}).get("text", "")
                print(f"  {role}: {content}")
        print()

    # Demonstrate cross-session memory
    print(f"\n{'='*60}")
    print("🔄 DEMO 3: Cross-Session Memory Retrieval")
    print(f"{'='*60}")
    print("Starting NEW session but same user...\n")

    new_session_id = f"session-{datetime.now().strftime('%H%M%S')}-new"

    # In a real agent, you'd retrieve long-term memories to inform responses
    print("🔍 Retrieving memories for this user across all sessions...")

    try:
        memories = memory_client.retrieve_memories(
            memory_id=memory_id,
            namespace=f"/demo/{user_id}/memories",
            query="What does the user like?"
        )
        print(f"\n📚 Retrieved {len(memories) if memories else 0} long-term memories")
        if memories:
            for mem in memories[:3]:  # Show first 3
                print(f"  - {mem}")
    except Exception as e:
        print(f"  (Long-term memory retrieval: {e})")
        print("  Note: Semantic memories are extracted asynchronously")

    print(f"\n{'='*60}")
    print("✅ Memory Demo Complete!")
    print(f"{'='*60}")
    print(f"\nMemory ID: {memory_id}")
    print("This memory persists across agent restarts.")
    print("\nNext steps:")
    print("  1. Run this demo again - previous conversations are remembered!")
    print("  2. Use this memory ID with the langgraph-web-search agent")
    print(f"  3. Set: BEDROCK_AGENTCORE_MEMORY_ID={memory_id}")


def run_interactive_agent():
    """Run an interactive agent with memory-enabled conversation."""
    from bedrock_agentcore.memory import MemoryClient

    memory_id = create_memory_if_needed()
    memory_client = MemoryClient(region_name=AWS_REGION)

    # Initialize LLM
    llm = init_chat_model(
        os.getenv("BEDROCK_MODEL_ID", "us.anthropic.claude-haiku-4-5-20251001-v1:0"),
        model_provider="bedrock_converse",
    )

    user_id = "interactive-user"
    session_id = f"interactive-{datetime.now().strftime('%Y%m%d%H%M%S')}"

    print(f"\n{'='*60}")
    print("🤖 Interactive Agent with Memory")
    print(f"{'='*60}")
    print(f"Memory ID: {memory_id}")
    print(f"Session: {session_id}")
    print("Type 'quit' to exit, 'history' to see memory\n")

    # Load existing conversation from memory
    messages = []
    try:
        events = memory_client.list_events(
            memory_id=memory_id,
            actor_id=user_id,
            session_id=session_id
        )
        for event in events:
            for msg in event.get("payload", []):
                if "conversational" in msg:
                    conv = msg["conversational"]
                    role = conv.get("role", "").lower()
                    content = conv.get("content", {}).get("text", "")
                    if role in ("user", "assistant"):
                        messages.append({"role": role, "content": content})
        if messages:
            print(f"📚 Loaded {len(messages)} messages from previous conversation\n")
    except Exception as e:
        print(f"Note: Could not load history ({e})\n")

    while True:
        try:
            user_input = input("👤 You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n👋 Goodbye!")
            break

        if not user_input:
            continue

        if user_input.lower() == 'quit':
            print("👋 Goodbye!")
            break

        if user_input.lower() == 'history':
            print(f"\n📜 Conversation History ({len(messages)} messages):")
            for msg in messages:
                role = "👤 You" if msg["role"] == "user" else "🤖 Assistant"
                print(f"  {role}: {msg['content'][:100]}...")
            print()
            continue

        # Add user message
        messages.append({"role": "user", "content": user_input})

        # Get response from LLM
        response = llm.invoke(messages)
        assistant_message = response.content

        print(f"🤖 Assistant: {assistant_message}\n")

        # Add assistant message
        messages.append({"role": "assistant", "content": assistant_message})

        # Save to memory
        try:
            memory_client.create_event(
                memory_id=memory_id,
                actor_id=user_id,
                session_id=session_id,
                messages=[
                    (user_input, "USER"),
                    (assistant_message, "ASSISTANT")
                ]
            )
        except Exception as e:
            print(f"  ⚠️ Could not save to memory: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--interactive":
        run_interactive_agent()
    else:
        demonstrate_memory()
