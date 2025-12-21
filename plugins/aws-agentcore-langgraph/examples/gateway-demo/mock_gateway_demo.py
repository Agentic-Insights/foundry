#!/usr/bin/env python3
"""
AgentCore Gateway Mock Demo (for Recording)
"""
import os
import sys
import time
import json
from datetime import datetime

# Configure visual style
def print_header(text):
    print(f"\n{'='*60}")
    print(f"{text}")
    print(f"{'='*60}")

def simulate_typing(text, delay=0.02):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def main():
    print_header("📡 AgentCore Gateway: Tool Hub Demo")
    time.sleep(1)

    print("📡 Querying AWS Bedrock AgentCore...")
    time.sleep(2)
    print("📦 Found existing gateway: production-gateway (gw-8f2k9l1m)")
    time.sleep(1)

    print_header("🔧 Tool Discovery")
    print("🔍 Searching for available MCP tools in gateway...")
    time.sleep(2)
    
    tools = [
        {"name": "get_weather", "description": "Get current weather for a location", "target": "Lambda: us-east-1:weather-service"},
        {"name": "query_inventory", "description": "Check stock levels in ERP", "target": "OpenAPI: https://api.erp.internal"},
        {"name": "github_search", "description": "Search repositories via MCP", "target": "MCP: github-mcp-server"}
    ]

    for tool in tools:
        print(f"  ✨ Found Tool: {tool['name'].ljust(15)} | {tool['description']}")
        time.sleep(0.5)

    print_header("🤖 LangGraph Agent Integration")
    print("Initializing LangGraph agent with Gateway ToolNode...")
    time.sleep(2)

    print("\n🤖 Agent: Hello! I have access to your corporate tools via the AgentCore Gateway. How can I help?")
    
    # Interaction 1
    print("\n👤 You: Check the weather in Seattle and then tell me if we have 'Polka Dot Socks' in stock.")
    time.sleep(1)
    
    print("\n--- AgentCore Gateway Event Log ---")
    print("📡 [GATEWAY] Request: call_tool('get_weather', {'location': 'Seattle'})")
    time.sleep(1.5)
    print("✅ [GATEWAY] Response: {'temp': 62, 'condition': 'Cloudy'}")
    time.sleep(1)
    print("📡 [GATEWAY] Request: call_tool('query_inventory', {'item': 'Polka Dot Socks'})")
    time.sleep(1.5)
    print("✅ [GATEWAY] Response: {'in_stock': 142, 'warehouse': 'SEA-01'}")
    print("----------------------------------\n")

    time.sleep(1)
    simulate_typing("🤖 Assistant: The weather in Seattle is currently 62°F and cloudy. Good news! We have 142 pairs of Polka Dot Socks in stock at the SEA-01 warehouse.")
    
    time.sleep(2)
    print_header("✅ Demo Complete")
    print("AgentCore Gateway enables:")
    print("  1. Single endpoint for 1000s of tools")
    print("  2. Managed auth/credentials")
    print("  3. Real-time semantic tool search")
    print("  4. Secure connection to VPC/Private resources")

if __name__ == "__main__":
    main()
