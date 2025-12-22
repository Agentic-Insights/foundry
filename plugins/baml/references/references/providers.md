# Provider Configuration Reference

Complete guide to configuring OpenAI, Anthropic, and Ollama providers with retry policies and fallback strategies.

## Provider Basics

```baml
client<llm> ClientName {
  provider PROVIDER_TYPE
  retry_policy RETRY_POLICY_NAME    // Optional
  options {
    // Provider-specific options
  }
}
```

## OpenAI Configuration

### Full Configuration

```baml
client<llm> GPT4 {
  provider openai
  options {
    api_key env.OPENAI_API_KEY
    model "gpt-4o"
    temperature 0.0
    max_tokens 2000
    base_url "https://api.openai.com/v1"  // Optional
  }
}
```

### Shorthand

```baml
client<llm> GPT4Mini {
  provider "openai/gpt-4o-mini"  // Uses env.OPENAI_API_KEY
}
```

### Supported Models

- `gpt-4o` - Most capable for complex extraction
- `gpt-4o-mini` - Fast and cost-effective
- `o1-mini`, `o1-preview` - Reasoning models (no temperature support)

### Temperature Guidelines

- **0.0** - Extraction, factual tasks (recommended)
- **0.3-0.5** - Balanced extraction with slight creativity
- **0.7-1.0** - Creative generation (not for extraction)

## Anthropic Configuration

### Full Configuration

```baml
client<llm> Claude {
  provider anthropic
  options {
    api_key env.ANTHROPIC_API_KEY
    model "claude-sonnet-4-20250514"
    temperature 0.0
    max_tokens 4096
  }
}
```

### Supported Models

- `claude-sonnet-4-20250514` - Best balance of capability and cost
- `claude-opus-4-20250514` - Most powerful
- `claude-haiku-4-20250514` - Fast and efficient

### Prompt Caching

```baml
client<llm> ClaudeWithCache {
  provider anthropic
  options {
    model "claude-sonnet-4-20250514"
    api_key env.ANTHROPIC_API_KEY
    allowed_role_metadata ["cache_control"]
  }
}

function Extract(doc: string) -> Data {
  client ClaudeWithCache
  prompt #"
    {{ _.role("system", cache_control={"type": "ephemeral"}) }}
    You are an expert extractor.

    {{ _.role("user") }}
    Extract from: {{ doc }}
    {{ ctx.output_format }}
  "#
}
```

## Ollama Configuration

Ollama uses `openai-generic` provider for OpenAI-compatible APIs.

### Local Development

```baml
client<llm> OllamaLocal {
  provider "openai-generic"
  options {
    base_url "http://localhost:11434/v1"
    model "llama3"
    temperature 0.7
  }
}
```

No API key required for local Ollama.

### Remote Ollama (e.g., Windows host from WSL)

```baml
client<llm> OllamaRemote {
  provider "openai-generic"
  options {
    base_url "http://172.30.224.1:11434/v1"
    model "llama3"
  }
}
```

### Supported Models

- `llama3` (8B, 70B) - General purpose
- `mistral` - Fast inference
- `mixtral` - Mixture of experts
- `qwen2` - Multilingual
- `codellama` - Code generation

## Retry Policies

```baml
retry_policy StandardRetry {
  max_retries 3
}

client<llm> ResilientClient {
  provider openai
  retry_policy StandardRetry
  options {
    model "gpt-4o"
  }
}
```

**Automatic exponential backoff**: ~100ms → ~200ms → ~400ms (with jitter)

**Retried**: Network timeouts, 5xx errors, 429 rate limits
**Not retried**: 4xx client errors, invalid keys, validation errors

## Fallback Strategies

### Basic Fallback Chain

```baml
client<llm> Primary {
  provider openai
  options { model "gpt-4o" }
}

client<llm> Secondary {
  provider anthropic
  options { model "claude-sonnet-4-20250514" }
}

client<llm> Tertiary {
  provider "openai-generic"
  options {
    base_url "http://localhost:11434/v1"
    model "llama3"
  }
}

client<llm> ResilientPipeline {
  provider fallback
  options {
    strategy [Primary, Secondary, Tertiary]
  }
}
```

### Cost-Optimized Pattern

```baml
client<llm> CostOptimized {
  provider fallback
  retry_policy StandardRetry
  options {
    strategy [
      GPT4,       // Tier 1: Expensive but accurate
      Claude,     // Tier 2: Balanced
      GPT4Mini,   // Tier 3: Cheap
      OllamaLocal // Tier 4: Free local
    ]
  }
}
```

## Environment Variables

### .env File

```env
OPENAI_API_KEY=sk-your-openai-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-key
OLLAMA_BASE_URL=http://localhost:11434/v1
```

### Reference in BAML

```baml
client<llm> GPT4 {
  provider openai
  options {
    api_key env.OPENAI_API_KEY
    base_url env.OPENAI_BASE_URL
  }
}
```

## Best Practices

**For Production:**
- Always use retry policies (3+ retries)
- Implement fallbacks for resilience
- Set temperature to 0.0 for extraction
- Separate dev/prod API keys

**For Development:**
- Use local Ollama for rapid iteration
- Use faster/cheaper models (GPT-4o-mini, Haiku)
- Smaller max_tokens to reduce costs

**For Reliability:**
- Chain cheap → expensive in fallbacks
- Combine retries + fallbacks
- Monitor latency with `_.latency_ms` in tests
