# AgentCore Browser Demo

Demonstrates AWS Bedrock AgentCore Browser for cloud-based web automation.

## What This Shows

1. **Cloud Browser Sessions**: Isolated Chrome instances in AWS
2. **Web Navigation**: Navigate, click, fill forms via Playwright
3. **Content Extraction**: Parse dynamic JavaScript-rendered content
4. **Session Recording**: Live view and replay capabilities

## Quick Start

```bash
cd examples/browser-demo
cp .env.example .env

uv sync
uv run playwright install chromium
uv run python browser_demo.py
```

## Browser Concepts

### Architecture

```
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
```

### Session Lifecycle

1. **Create session**: `browser_session()` context manager
2. **Connect**: Playwright connects via WebSocket
3. **Automate**: Navigate, interact, extract
4. **Cleanup**: Session auto-terminates on context exit

### Session Limits

| Parameter | Default | Maximum |
|-----------|---------|---------|
| Timeout | 15 min | 8 hours |
| Concurrent sessions | - | Account quota |

## API Patterns

### Basic Session

```python
from bedrock_agentcore.tools.browser_client import browser_session
from playwright.sync_api import sync_playwright

with browser_session('us-east-1') as client:
    ws_url, headers = client.generate_ws_headers()

    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(ws_url, headers=headers)
        page = browser.contexts[0].pages[0]

        page.goto("https://example.com")
        title = page.title()
        content = page.inner_text("body")
```

### As a LangGraph Tool

```python
from langchain_core.tools import tool

@tool
def browse_and_extract(url: str) -> str:
    """Navigate to a URL and extract page content."""
    with browser_session('us-east-1') as client:
        ws_url, headers = client.generate_ws_headers()

        with sync_playwright() as p:
            browser = p.chromium.connect_over_cdp(ws_url, headers=headers)
            page = browser.contexts[0].pages[0]

            page.goto(url)
            page.wait_for_load_state("networkidle")

            return page.inner_text("body")[:2000]

# Use in agent
tools = [browse_and_extract]
```

### Screenshot Capture

```python
page.goto("https://example.com")
page.screenshot(path="screenshot.png", full_page=True)
```

### Form Interaction

```python
page.fill("input#username", "myuser")
page.fill("input#password", "mypass")
page.click("button#submit")
page.wait_for_navigation()
```

## Use Cases

1. **Deep Research**: Navigate multiple sources, extract structured data
2. **Form Automation**: Fill out web forms programmatically
3. **Data Extraction**: Scrape JavaScript-rendered SPAs
4. **Monitoring**: Check website status, capture screenshots
5. **Testing**: Automated web testing with real browser behavior

## Required Permissions

```json
{
    "Effect": "Allow",
    "Action": [
        "bedrock-agentcore:StartBrowserSession",
        "bedrock-agentcore:StopBrowserSession",
        "bedrock-agentcore:GetBrowserSession",
        "bedrock-agentcore:ListBrowserSessions",
        "bedrock-agentcore:ConnectBrowserAutomationStream"
    ],
    "Resource": "*"
}
```

## Observability

- **Live View**: Real-time browser monitoring in AWS Console
- **Session Recording**: DOM changes, user actions, console logs, network events
- **S3 Storage**: Recordings stored for replay

## Next Steps

1. Install Playwright and browser binaries
2. Create browser sessions in your agent
3. Use Playwright to automate web research
4. Integrate extracted data into your LangGraph workflow
