#!/usr/bin/env python3
"""
AgentCore Browser Demo

Demonstrates AWS Bedrock AgentCore Browser for cloud-based web automation.

Features shown:
- Cloud browser sessions: Isolated Chrome instances
- Web navigation: Navigate, click, fill forms
- Content extraction: Parse dynamic content
- Session recording: Live view and replay

Run locally:
    uv run python browser_demo.py

Environment variables:
    AWS_PROFILE - AWS profile to use (default: ag)
    AWS_REGION - AWS region (default: us-east-1)

Note: Requires Playwright installed: uv add playwright && uv run playwright install chromium
"""

import os
import time
from datetime import datetime

import boto3
from dotenv import load_dotenv

load_dotenv()

# Configure AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "ag")
os.environ["AWS_PROFILE"] = AWS_PROFILE

print(f"🔧 Using AWS Profile: {AWS_PROFILE}, Region: {AWS_REGION}")

# Initialize client
control_client = boto3.client('bedrock-agentcore-control', region_name=AWS_REGION)


def list_browsers():
    """List existing browser resources."""
    print("\n🌐 Existing Browsers:")
    try:
        response = control_client.list_browsers()
        browsers = response.get('browserSummaries', [])

        if not browsers:
            print("  (none found)")
            return []

        for browser in browsers:
            print(f"  - {browser['name']} ({browser['browserId']}) - {browser['status']}")

        return browsers
    except Exception as e:
        print(f"  Error: {e}")
        return []


def create_browser_resource() -> str | None:
    """Create a browser resource or return existing one."""

    browsers = control_client.list_browsers().get('browserSummaries', [])
    for browser in browsers:
        if browser['status'] == 'READY':
            print(f"📦 Using existing browser: {browser['browserId']}")
            return browser['browserId']

    # Create new browser resource
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    browser_name = f"demo_browser_{timestamp}"

    print(f"\n🆕 Creating browser resource: {browser_name}")

    try:
        response = control_client.create_browser(
            name=browser_name,
            description="Demo browser for AgentCore Browser showcase"
        )
        browser_id = response['browserId']
        print(f"✅ Created browser: {browser_id}")

        # Wait for browser to be ready
        print("⏳ Waiting for browser to be ready...")
        for _ in range(30):
            status = control_client.get_browser(browserId=browser_id)
            if status['status'] == 'READY':
                print("✅ Browser is ready!")
                return browser_id
            time.sleep(2)

        return browser_id
    except Exception as e:
        print(f"❌ Error creating browser: {e}")
        return None


def demonstrate_browser_api():
    """Show browser session API patterns."""

    print("""
    Browser Session Flow:

    1. Create a browser session:
       ```python
       from bedrock_agentcore.tools.browser_client import browser_session

       with browser_session('us-east-1') as client:
           ws_url, headers = client.generate_ws_headers()
           # ws_url is a WebSocket endpoint for browser control
       ```

    2. Connect with Playwright:
       ```python
       from playwright.sync_api import sync_playwright

       with sync_playwright() as p:
           browser = p.chromium.connect_over_cdp(ws_url, headers=headers)
           page = browser.contexts[0].pages[0]

           # Navigate
           page.goto("https://example.com")

           # Extract content
           title = page.title()
           content = page.content()

           # Interact
           page.click("button#submit")
           page.fill("input#search", "AgentCore")
       ```

    3. Session features:
       - Default timeout: 15 minutes (max 8 hours)
       - Live view for real-time monitoring
       - Session recording (stored in S3)
       - Complete isolation between sessions
    """)


def demonstrate_browser_in_langgraph():
    """Show how to use browser as a LangGraph tool."""

    print("""
    LangGraph + Browser Integration:

    ```python
    from langchain_core.tools import tool
    from bedrock_agentcore.tools.browser_client import browser_session
    from playwright.sync_api import sync_playwright

    @tool
    def browse_and_extract(url: str, query: str) -> str:
        \"\"\"Navigate to a URL and extract information based on the query.\"\"\"

        with browser_session('us-east-1') as client:
            ws_url, headers = client.generate_ws_headers()

            with sync_playwright() as p:
                browser = p.chromium.connect_over_cdp(ws_url, headers=headers)
                page = browser.contexts[0].pages[0]

                page.goto(url)
                page.wait_for_load_state("networkidle")

                # Extract text content
                content = page.inner_text("body")

                # Or get specific elements
                # links = page.query_selector_all("a")
                # data = [{"text": l.inner_text(), "href": l.get_attribute("href")} for l in links]

                return content[:2000]  # Truncate for LLM context

    # Use in LangGraph
    tools = [browse_and_extract]
    llm_with_tools = llm.bind_tools(tools)
    ```
    """)


def demonstrate_browser():
    """Main demo showing AgentCore Browser capabilities."""

    print(f"\n{'='*60}")
    print("🌐 AgentCore Browser Demo")
    print(f"{'='*60}")

    # List existing browsers
    list_browsers()

    # Explain browser concepts
    print(f"\n{'='*60}")
    print("📖 DEMO 1: Browser Concepts")
    print(f"{'='*60}")

    print("""
    AgentCore Browser provides:

    ┌─────────────────────────────────────────────────────────┐
    │              AgentCore Browser Service                   │
    │                                                          │
    │  ┌──────────────────────────────────────────────────┐   │
    │  │        Cloud Chrome Instance (Isolated)           │   │
    │  │                                                    │   │
    │  │  • Full browser capabilities                      │   │
    │  │  • JavaScript execution                           │   │
    │  │  • Dynamic content rendering                      │   │
    │  │  • Form filling and clicks                        │   │
    │  │  • Screenshot/PDF generation                      │   │
    │  │                                                    │   │
    │  └──────────────────────────────────────────────────┘   │
    │                          │                               │
    │                   WebSocket API                          │
    │                          │                               │
    └──────────────────────────┼───────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  Playwright/CDP     │
                    │  (Your Agent Code)  │
                    └─────────────────────┘

    Key features:
    - Complete isolation from local systems
    - Session recording with replay
    - Live view for debugging
    - Web Bot Auth to reduce CAPTCHAs
    """)

    # Show API patterns
    print(f"\n{'='*60}")
    print("🔧 DEMO 2: Browser Session API")
    print(f"{'='*60}")

    demonstrate_browser_api()

    # Show LangGraph integration
    print(f"\n{'='*60}")
    print("🤖 DEMO 3: LangGraph Integration")
    print(f"{'='*60}")

    demonstrate_browser_in_langgraph()

    # Attempt to create a browser resource
    print(f"\n{'='*60}")
    print("🚀 DEMO 4: Creating Browser Resource")
    print(f"{'='*60}")

    browser_id = create_browser_resource()

    # Summary
    print(f"\n{'='*60}")
    print("✅ Browser Demo Complete!")
    print(f"{'='*60}")

    print(f"""
    Browser ID: {browser_id or 'Not created'}

    Use cases for AgentCore Browser:

    1. **Deep Research**: Navigate multiple sources, extract structured data
    2. **Form Automation**: Fill out web forms, submit applications
    3. **Data Extraction**: Scrape dynamic content (SPAs, JS-rendered pages)
    4. **Testing**: Automated web testing with real browser behavior
    5. **Monitoring**: Check website status, capture screenshots

    Required permissions:
    - bedrock-agentcore:StartBrowserSession
    - bedrock-agentcore:StopBrowserSession
    - bedrock-agentcore:GetBrowserSession
    - bedrock-agentcore:ConnectBrowserAutomationStream

    Next steps:
    1. Install Playwright: uv add playwright && uv run playwright install chromium
    2. Create a browser session using browser_session()
    3. Connect via Playwright and automate your research tasks
    """)


if __name__ == "__main__":
    demonstrate_browser()
