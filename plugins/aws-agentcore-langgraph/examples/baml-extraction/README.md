# BAML Extraction Demo

Type-safe LLM extraction for AWS Bedrock AgentCore memory events using [BAML](https://docs.boundaryml.com/).

## What This Demo Shows

This example demonstrates BAML's capabilities for parsing and validating structured data from LLM responses:

1. **Memory Event Extraction** - Parse nested AgentCore memory events into typed `Conversation` objects
2. **Response Metadata Extraction** - Extract tool usage, confidence, and follow-up flags from agent responses
3. **Tone Analysis** - Monitor agent response quality with structured analysis

## Quick Start

```bash
cd examples/baml-extraction

# Setup
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY

# Install dependencies
uv sync

# Generate BAML client (creates baml_client/)
uv run baml-cli generate

# Run demo
uv run python demo.py
```

## Running BAML Tests

```bash
# Run all tests
uv run baml-cli test

# Run specific test
uv run baml-cli test --filter "ExtractSimpleConversation"

# Run tests in parallel
uv run baml-cli test --parallel 3
```

## Project Structure

```
baml-extraction/
├── baml_src/               # BAML source files
│   ├── generators.baml     # Code generation config (Python/Pydantic)
│   ├── clients.baml        # LLM providers (Anthropic + Ollama)
│   ├── memory_extraction.baml  # Types and functions
│   └── tests.baml          # BAML tests
├── baml_client/            # Generated client (don't edit)
├── demo.py                 # Demo script
├── pyproject.toml          # Dependencies
└── .env.example            # Environment template
```

## Key BAML Features Demonstrated

### Type-Safe Extraction
```python
from baml_client.baml_client import b
from baml_client.baml_client.types import Conversation

# Fully typed - IDE autocomplete works!
conversation: Conversation = b.ExtractConversation(raw_events)
print(conversation.messages[0].role)  # MessageRole enum
print(conversation.turn_count)        # int
```

### Fallback Providers
```baml
client<llm> ExtractorWithFallback {
  provider fallback
  options {
    strategy [ClaudeHaiku, OllamaLocal]
  }
}
```

### Built-in Validation
```baml
class Conversation {
  messages ConversationMessage[]
  turn_count int @description("Number of conversation turns (non-negative)")
}
```

## Providers Configured

| Provider | Model | Use Case |
|----------|-------|----------|
| ClaudeHaiku | claude-haiku-4-20250514 | Fast, cost-effective extraction |
| ClaudeSonnet | claude-sonnet-4-20250514 | Complex extraction |
| OllamaLocal | llama3.2 | Local fallback (no API key) |

Ollama is configured to use `http://172.30.224.1:11434` (Windows host from WSL).
