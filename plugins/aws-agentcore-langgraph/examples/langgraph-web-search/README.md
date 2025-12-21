# LangGraph Web Search Agent

A ReAct-style LangGraph agent with DuckDuckGo search, deployable to AWS Bedrock AgentCore.

## Setup

```bash
cp .env.example .env
# Edit .env with your AWS credentials

uv sync
```

## Run Locally

```bash
uv run python agent.py
```

The agent starts an HTTP server on port 8080.

```bash
curl -X POST http://localhost:8080/invocations \
  -H "Content-Type: application/json" \
  -d '{"prompt": "What is the weather in Seattle?"}'
```

## Deploy to AgentCore

```bash
# Install starter toolkit
uv add --dev bedrock-agentcore-starter-toolkit

# Configure and deploy
agentcore configure -e agent.py --region us-east-1
agentcore launch
agentcore invoke '{"prompt": "Search for latest AI news"}'
```

## Architecture

```
User Request -> BedrockAgentCoreApp -> StateGraph -> Bedrock Claude
                    (HTTP :8080)          |   ^
                                    ToolNode (DuckDuckGo)
```

The agent uses a ReAct loop:
1. **chatbot** node: LLM decides to respond or use tools
2. **tools_condition**: Routes to tools if tool_calls present, else END
3. **tools** node: Executes DuckDuckGo search, returns to chatbot

## Memory Integration

When deployed with AgentCore Memory, the toolkit auto-injects `BEDROCK_AGENTCORE_MEMORY_ID`. The agent loads conversation history and persists new exchanges.

## License

Apache 2.0
