---
name: baml-implementation
description: Core BAML implementation patterns for type-safe LLM extraction. Use when writing BAML schemas, functions, tests, or configuring providers. Detects project language (Python/TypeScript/Go/Ruby) and framework (LangGraph) to load relevant references.
license: "Apache-2.0"
---

# BAML Implementation

This skill provides practical patterns for implementing BAML extraction pipelines. It works with the `baml-philosophy` skill which establishes the foundational principles.

## Context Detection

When starting BAML work, I first detect the project context:

1. **Check for `baml_src/generators.baml`** - Read `output_type` to determine target language
2. **Check dependencies** - Look for framework markers (langgraph imports, pyproject.toml/package.json)
3. **Load relevant references** - Based on detected context

## Quick Reference

| Need to... | Reference File |
|-----------|----------------|
| Configure providers | `references/providers.md` |
| Define types/schemas | `references/types-and-schemas.md` |
| Add validation | `references/validation.md` |
| Complex patterns | `references/advanced-patterns.md` |
| Python specifics | `references/languages-python.md` |
| TypeScript specifics | `references/languages-typescript.md` |
| Go/Ruby specifics | `references/languages-other.md` |
| LangGraph integration | `references/frameworks-langgraph.md` |
| Extract from images/forms | `references/usecase-image-forms.md` |
| Model workflows/events | `references/usecase-workflows.md` |

## The Generation Workflow

**BAML is a transpiler, not a runtime library.** You write `.baml` source files, then generate native code.

```
┌─────────────────┐     baml-cli generate     ┌─────────────────┐
│   baml_src/     │  ───────────────────────► │  baml_client/   │
│   (you edit)    │                           │  (GENERATED)    │
└─────────────────┘                           └─────────────────┘
```

### Critical Rules

1. **NEVER edit files in `baml_client/`** - They are regenerated on every `baml-cli generate`
2. **ALWAYS edit in `baml_src/`** - This is your source of truth
3. **Run `baml-cli generate` after changes** - Regenerates typed client code
4. **Generated code has full type safety** - Pydantic models (Python), TypeScript interfaces

### Generation Commands

```bash
# Generate client code (run after any .baml changes)
baml-cli generate

# Watch mode - auto-regenerate on file changes
baml-cli generate --watch

# Check version matches generator config
baml-cli --version
```

### generators.baml

This file configures what code gets generated:

```baml
generator target {
  output_type python/pydantic    # or: typescript, ruby/sorbet, go
  output_dir "../baml_client"    # Where generated code goes
  version "0.76.2"               # Must match baml-cli version!
}
```

## Project Structure

Standard BAML project layout:

```
project/
├── baml_src/                    # SOURCE - Edit these files
│   ├── generators.baml          # Code generation config
│   ├── clients.baml             # LLM provider configs
│   └── *.baml                   # Functions and types
├── baml_client/                 # GENERATED - Never edit!
│   ├── __init__.py / index.ts   # Entry point
│   ├── types.py / types.ts      # Generated type definitions
│   └── sync_client.py / client.ts
└── .env                         # API keys (not committed)
```

**The `baml_client/` directory is 100% generated.** If you need to change types or functions, edit the `.baml` source files and regenerate.

## Core Patterns

### 1. Defining Schemas

```baml
class Address {
  street string
  city string
  state string
  zip_code string @description("5-digit ZIP code")
}

class Person {
  name string
  email string @description("Personal email address")
  age int?                        // Optional
  address Address                 // Nested
}

enum Sentiment {
  POSITIVE
  NEGATIVE
  NEUTRAL
}
```

### 2. Writing Functions

Every BAML prompt is a typed function:

```baml
function ExtractPerson(text: string) -> Person {
  client GPT4
  prompt #"
    Extract person information from the following text:

    {{ text }}

    {{ ctx.output_format }}
  "#
}
```

**Critical:** Always include `{{ ctx.output_format }}` - this injects the schema instructions.

### 3. Provider Configuration

```baml
// OpenAI
client<llm> GPT4 {
  provider openai
  options {
    api_key env.OPENAI_API_KEY
    model "gpt-4o"
    temperature 0.0
  }
}

// Anthropic
client<llm> Claude {
  provider anthropic
  options {
    api_key env.ANTHROPIC_API_KEY
    model "claude-sonnet-4-20250514"
  }
}

// Ollama (local)
client<llm> OllamaLocal {
  provider "openai-generic"
  options {
    base_url "http://localhost:11434/v1"
    model "llama3"
  }
}
```

### 4. Validation

**@assert** - Strict validation (raises exception):
```baml
class Payment {
  amount float @assert(this > 0, "Amount must be positive")
  status string @assert(this in ["pending", "completed"])
}
```

**@check** - Monitoring (non-blocking):
```baml
class Citation {
  quote string @check(this|length > 0, citation_found)
}
```

### 5. Testing

```baml
test PersonTest {
  functions [ExtractPerson]
  args {
    text "John Smith, john@example.com, 30 years old"
  }
  @@assert({{ this.name == "John Smith" }})
  @@assert({{ this.email == "john@example.com" }})
}
```

Run tests:
```bash
baml-cli test
baml-cli test --filter "PersonTest"
baml-cli test --parallel 5
```

## Generated Code Usage

### Python

```python
from baml_client import b
from baml_client.types import Person

# Sync
person = b.ExtractPerson(text)
print(person.name)  # Type-safe

# Async
person = await b.ExtractPerson(text)

# Streaming
stream = b.stream.ExtractPerson(text)
for partial in stream:
    print(f"Got: {partial}")
final = stream.get_final_response()
```

### TypeScript

```typescript
import { b } from './baml_client'
import type { Person } from './baml_client/types'

// Async (default)
const person: Person = await b.ExtractPerson(text)
console.log(person.name)

// Streaming
const stream = b.stream.ExtractPerson(text)
for await (const partial of stream) {
  console.log('Got:', partial)
}
const final = await stream.getFinalResponse()
```

## Workflow

When implementing BAML extraction:

1. **Define the schema first** - What data structure do I need? (in `baml_src/`)
2. **Add field descriptions** - Guide the LLM with `@description`
3. **Add validation** - `@assert` for invariants, `@check` for monitoring
4. **Write the function** - Include `{{ ctx.output_format }}`
5. **Configure providers** - Set up clients with appropriate retry policies
6. **Write tests** - Cover happy path and edge cases
7. **Generate the client** - Run `baml-cli generate` to create typed code in `baml_client/`
8. **Run tests** - `baml-cli test` to verify extraction works
9. **Integrate** - Import from `baml_client` (generated) and use in application

**Remember:** After ANY change to `.baml` files, run `baml-cli generate` before using the client code.

## See Also

For detailed information on specific topics, read the appropriate reference:

- **Providers**: Complete OpenAI, Anthropic, Ollama configuration → `references/providers.md`
- **Types**: Full type system including unions, enums, maps → `references/types-and-schemas.md`
- **Validation**: @assert, @check, block-level validation → `references/validation.md`
- **Advanced**: Tool calling, dynamic types, complex extraction → `references/advanced-patterns.md`
- **Language-specific**: Python, TypeScript, Go, Ruby patterns → `references/languages-*.md`
- **Frameworks**: LangGraph integration → `references/frameworks-langgraph.md`
- **Use cases**: Image forms, workflow extraction → `references/usecase-*.md`
