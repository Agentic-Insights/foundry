---
description: Initialize BAML in a Python or TypeScript project
argument-hint: [language] [provider]
---

# Initialize BAML Project

Set up BAML in an existing project or create a new one.

## Detection

First, detect the project context:
1. Check for existing `baml_src/` directory
2. Check for `pyproject.toml` (Python) or `package.json` (TypeScript)
3. Check for existing generators.baml

## Actions

### If No BAML Exists

**For Python projects:**
```bash
# Add baml-py dependency
uv add baml-py
# Or: pip install baml-py

# Create baml_src directory
mkdir -p baml_src
```

**For TypeScript projects:**
```bash
# Add BAML dependency
npm install @boundaryml/baml
# Or: pnpm add @boundaryml/baml

# Create baml_src directory
mkdir -p baml_src
```

### Create generators.baml

Detect language and create appropriate generator:

**Python:**
```baml
generator target {
  output_type python/pydantic
  output_dir "../baml_client"
  version "0.76.2"
}
```

**TypeScript:**
```baml
generator target {
  output_type typescript
  output_dir "../baml_client"
  version "0.76.2"
}
```

### Create clients.baml

```baml
// OpenAI client
client GPT4 {
  provider openai
  options {
    model "gpt-4"
    api_key env.OPENAI_API_KEY
  }
}

// Vision-capable model for images
client GPT4o {
  provider openai
  options {
    model "gpt-4o"
    api_key env.OPENAI_API_KEY
  }
}

// Default retry policy
retry_policy Default {
  max_retries 2
  strategy {
    type exponential_backoff
  }
}
```

### Create Example Function

```baml
// example.baml
class Person {
  name string
  email string @description("Email address if present")
  age int?
}

function ExtractPerson(text: string) -> Person {
  client GPT4
  prompt #"
    Extract person information from:
    {{ text }}

    {{ ctx.output_format }}
  "#
}

test BasicTest {
  functions [ExtractPerson]
  args {
    text "John Smith, john@example.com, 30 years old"
  }
}
```

## Generate Client (REQUIRED)

**After creating BAML files, generate the typed client:**
```bash
baml-cli generate
```

This creates the `baml_client/` directory with:
- Type definitions (Pydantic models or TypeScript interfaces)
- Client functions you import and call
- **This is 100% generated - never edit these files directly**

## Verify Setup

```bash
baml-cli test --filter "BasicTest"
```

## Environment Variables

Remind user to set API keys:
```bash
# .env
OPENAI_API_KEY=sk-...
# Or for Anthropic:
ANTHROPIC_API_KEY=sk-ant-...
```

## Output

Report what was created:
- `baml_src/generators.baml`
- `baml_src/clients.baml`
- `baml_src/example.baml`
- `baml_client/` (generated)

## Arguments

- `$ARGUMENTS` - Optional: specify language (python/typescript) or provider (openai/anthropic/ollama)

Example: `/baml-init typescript anthropic`
