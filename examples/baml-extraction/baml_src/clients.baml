// LLM Provider Configuration
// Local testing: Ollama | Production: Bedrock/Anthropic

// ============================================
// LOCAL TESTING (Ollama on Windows host)
// ============================================

// Primary local model - Qwen3 VL (good JSON compliance)
client<llm> OllamaQwen {
  provider "openai-generic"
  options {
    base_url "http://172.30.224.1:11434/v1"
    model "qwen3-vl:30b"
    api_key "ollama"
  }
}

// Alternative: GPT-OSS (latest - better JSON compliance)
client<llm> OllamaGPT {
  provider "openai-generic"
  options {
    base_url "http://172.30.224.1:11434/v1"
    model "gpt-oss:latest"
    api_key "ollama"
  }
}

// Fallback chain for local testing
client<llm> LocalExtractor {
  provider fallback
  options {
    strategy [OllamaQwen, OllamaGPT]
  }
}

// ============================================
// PRODUCTION (Bedrock/Anthropic)
// ============================================

// Anthropic Claude Haiku (fast + cheap)
client<llm> ClaudeHaiku {
  provider anthropic
  options {
    api_key env.ANTHROPIC_API_KEY
    model "claude-haiku-4-20250514"
    max_tokens 1024
  }
}

// Anthropic Claude Sonnet (complex extraction)
client<llm> ClaudeSonnet {
  provider anthropic
  options {
    api_key env.ANTHROPIC_API_KEY
    model "claude-sonnet-4-20250514"
    max_tokens 2048
  }
}

// Production fallback with Anthropic
client<llm> ProductionExtractor {
  provider fallback
  options {
    strategy [ClaudeHaiku, ClaudeSonnet]
  }
}

// ============================================
// ACTIVE CLIENT (change for deployment)
// ============================================

// For local testing, use Ollama
// For production, switch to ProductionExtractor or ClaudeHaiku
client<llm> Extractor {
  provider fallback
  options {
    strategy [OllamaQwen, OllamaGPT]
  }
}
