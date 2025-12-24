---
name: baml-codegen
description: "Use when generating BAML code for type-safe LLM extraction, classification, RAG, or agent workflows - creates complete .baml files with types, functions, clients, tests, and framework integrations from natural language requirements. Queries official BoundaryML repositories via MCP for real-time patterns. Supports multimodal inputs (images, audio), Python/TypeScript/Ruby/Go, 10+ frameworks, 50-70% token optimization, 95%+ compilation success."
license: "Apache-2.0"
compatibility: "Requires MCP servers: baml_Docs (required), baml_Examples (optional). Works offline with 80% functionality using cached patterns."
---

# BAML Code Generation Skill

**Version**: 2.0.0
**Status**: Production (Unified BAML Plugin)
**Token Budget**: ~3500 tokens (validated, 12KB)

## Overview

Generate BAML applications by querying official BoundaryML repositories through MCP servers. This skill extracts patterns, validates syntax, and synthesizes complete solutions including types, functions, tests, and integrations.

**BAML treats LLM calls with the same rigor as database calls** - structured, typed, and testable. It transpiles `.baml` files into native Python/TypeScript/Ruby/Go code with zero runtime dependencies.

## Quick Start

### Activation Triggers
- Keywords: BAML, LLM, structured output, code generation, extraction, classification
- User requests to generate BAML code
- Questions about BAML syntax or patterns

### Critical Transpiler Rules
- **NEVER edit `baml_client/`** - 100% generated, overwritten on every `baml-cli generate`
- **ALWAYS edit `baml_src/`** - Source of truth for all BAML code
- **Run `baml-cli generate` after changes** - Regenerates typed client code

### Context Detection
Before generating code, detect project context:
1. Check `baml_src/generators.baml` - Read `output_type` for target language
2. Check dependencies - Look for framework markers (langgraph, fastapi, next.js)
3. Detect existing patterns - Scan existing .baml files for conventions

## Core Workflow

```
User Request → Analyze Requirements → Pattern Matching (MCP) → Syntax Validation (MCP)
    ↓
Generate Code → Generate Tests → Generate Integration → Validate & Optimize
    ↓
[IF ERRORS] Error Recovery (MCP) → Retry Validation
    ↓
Deliver Artifacts
```

### Step 1: Analyze Requirements
- Parse natural language text
- Identify pattern category (extraction/classification/rag/agents)
- Extract entities and constraints

### Step 2: Pattern Matching 🔍 **MCP REQUIRED**
- Execute: `mcp__baml_Examples__search_baml_examples_code`
- Fetch: `mcp__baml_Docs__fetch_generic_url_content`
- Parse: Extract types/functions/prompts from real code
- Rank by similarity (>0.7 threshold)
- Output: "🔍 Found {X} patterns from BoundaryML/baml-examples"

### Step 3: Syntax Validation 🔍 **baml_Docs**
- Query: `mcp__baml_Docs__search_baml_documentation("syntax {feature}")`
- Compare: Example syntax vs canonical docs
- Modernize: Update deprecated patterns to current spec
- Output: "✅ Validated against BoundaryML/baml" OR "🔧 Modernized {N} patterns"

### Step 4: Code Generation
Generate complete .baml files:
- **Types**: Classes and enums with `@description` and `@assert`
- **Functions**: Signature, prompt template with `{{ ctx.output_format }}`
- **Clients**: Provider configuration (openai, anthropic, etc.)

### Step 5: Test & Integration Generation
- Tests: pytest/Jest with 100% function coverage
- Integration: Framework-specific code (FastAPI, Next.js, LangChain)
- Deployment: Docker/K8s configs

### Step 6: Error Recovery 🔧 **IF ERRORS**
- Query: `mcp__baml_Docs__search_baml_documentation("{error}")`
- Fetch: Current syntax spec from BoundaryML/baml
- Fix: Update code to match canonical specification
- Retry: Re-validate (max 2 attempts)
- Output: "🔧 Fixed {N} errors using BoundaryML/baml docs"

## BAML Philosophy (TL;DR)

**The Core Problem**: Making AI work 80-90% is easy; production reliability (99%+) is hard.

**The Five Principles**:
1. **Schema Is The Prompt** - Define data models first, compiler injects types
2. **Types Over Strings** - Use enums/classes/unions, not string parsing
3. **Fuzzy Parsing Is BAML's Job** - BAML extracts valid JSON from messy LLM output
4. **Transpiler Not Library** - Write `.baml` → generate native code, no runtime dependency
5. **Test-Driven Prompting** - Use VS Code playground or `baml-cli test` to iterate

**When to Use BAML**: Type safety, hierarchical data, reliability (retries/fallbacks), complex schemas, production robustness.

**When to Skip**: Simple one-off extractions, creative text generation, quick prototypes.

*Full philosophy: [references/philosophy.md](references/philosophy.md)*

## Pattern Library

| Category | Use Case | Model Choice | Latency |
|----------|----------|--------------|---------|
| **Extraction** | Parse unstructured → structured data | GPT-5 / GPT-5-mini | 2-5s |
| **Classification** | Categorize into predefined classes | GPT-5-mini | <1s |
| **RAG** | Generate answers with citations | GPT-5 | 4-6s |
| **Agents** | Multi-step reasoning and planning | GPT-5 | 5-10s |
| **Vision** | Extract data from images | GPT-5-Vision | 5-7s |

*Complete patterns with code: [references/patterns.md](references/patterns.md)*

## MCP Query Strategy

**Observable Indicators** (user sees MCP usage):
- 🔍 "Found {X} patterns from BoundaryML/baml-examples"
- ✅ "Fetched {file} from BoundaryML/baml"
- ✅ "Validated against BoundaryML/baml - syntax current"
- 🔧 "Modernized {N} deprecated patterns"
- 🔧 "Fixed {N} errors using BoundaryML/baml docs"
- 📦 "Using cached pattern (MCP unavailable)"
- ⚠️ "MCP unavailable, using fallback templates"

**Execution Order**:
1. Check MCP availability first
2. Execute queries for pattern category
3. Parse real code examples
4. Adapt to requirements
5. Fall back to cache only if MCP fails

*Complete MCP workflow: [references/mcp-interface.md](references/mcp-interface.md)*

## BAML Syntax Reference

**Core Blocks**: `class`, `enum`, `function`, `client`

**Type System**: `string`, `int`, `float`, `bool`, `Type[]`, `Type?`, `Type|Type`

**Key Patterns**:
- `@description("...")` - Field documentation (becomes prompt context)
- `@assert(this > 0)` - Runtime validation
- `{{ param }}` - Variable injection
- `{{ ctx.output_format }}` - Auto-inject schema (required in all functions)

**Providers**: `openai`, `anthropic`, `gemini`, `vertex`, `bedrock`, `ollama`

**Example**:
```baml
class Invoice {
  total float @description("Total amount") @assert(this > 0)
}

function ExtractInvoice(text: string) -> Invoice {
  client GPT5
  prompt #"
    Extract invoice data: {{ text }}
    {{ ctx.output_format }}
  "#
}

client<llm> GPT5 {
  provider openai
  options { model gpt-5, temperature 0.0 }
}
```

*Query MCP for complete syntax: `mcp__baml_Docs__search_baml_documentation("syntax")`*

## Output Format

Always deliver:
1. **BAML Code**: Complete `.baml` files ready for `baml_src/`
2. **Tests**: pytest/Jest tests with 100% coverage
3. **Integration**: Framework-specific client code
4. **Deployment**: Docker/K8s configuration (if needed)
5. **Metadata**: Pattern used, token count, cost estimate, optimization notes

## Performance Targets

- Simple function (<50 lines): <5s
- Complex system (>500 lines): <30s
- Compilation success: >95%
- Token optimization: >50% reduction vs manual prompts
- Cost per generation: <$0.02

## Reference Documentation

| Topic | File | Description |
|-------|------|-------------|
| **Philosophy** | [references/philosophy.md](references/philosophy.md) | BAML principles, golden rules, when to use |
| **Patterns** | [references/patterns.md](references/patterns.md) | Pattern library by category with code examples |
| **MCP Interface** | [references/mcp-interface.md](references/mcp-interface.md) | Query workflow, caching strategy, error handling |
| **Examples** | [references/examples.md](references/examples.md) | Complete code generation examples with tests |

## Error Handling

**MCP Unavailable**: Fall back to embedded cache → warn user
**Pattern Not Found**: Use generic template → ask for clarification
**Validation Failure**: Auto-query docs → auto-fix → retry (max 2 attempts)
**Generation Timeout**: Show progress → stream partial results → allow cancellation

---

**Token Count**: ~3500 tokens (12KB, validated)
**Last Updated**: 2025-12-21
**Version**: 2.0.0 - Unified BAML plugin with progressive disclosure
**Ready for Production**: Yes
