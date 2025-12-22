---
name: baml-philosophy
description: Foundation for BAML development - Vaibhav Gupta's reliability-first paradigm for type-safe LLM extraction. Use when starting BAML work, explaining BAML's approach, or making architectural decisions about structured LLM output.
license: "Apache-2.0"
---

# The BAML Philosophy

BAML (Boundary ML) represents a paradigm shift in AI engineering. This skill establishes the foundational principles that guide all BAML development.

**Source:** Vaibhav Gupta, BAML Co-creator

## The Core Problem

### The "Uncanny Valley" of AI Development

- **The Demo Trap:** Making an AI model work *once* or *mostly* (80-90% success) is easy.
- **The Production Reality:** In traditional software, if a database or API failed 5% of the time, the company would not exist. Yet in AI, we accept non-determinism as an excuse for fragility.
- **The Objective:** Treat AI components with the same rigor as standard software functions. An LLM call should be as predictable as a function call in Python or TypeScript.

## The Five Principles

### 1. Schema Is The Prompt

Traditional approach: Write a long text prompt describing what you want, then hope the model outputs JSON.

**BAML approach:** Define the **Data Model** first.
- Add descriptions to fields: `email: string @description("The user's personal email")`
- The BAML compiler *injects* type definitions into the prompt automatically via `{{ ctx.output_format }}`
- Instructions are co-located with the data structure they govern
- This reduces "prompt drift" - the schema IS the instruction

### 2. Types Over Strings

BAML simplifies "agentic" terminology into standard Computer Science concepts:

| "Agentic" Term | BAML / CS Equivalent | Explanation |
| :--- | :--- | :--- |
| **LLM Call** | **Function Signature** | Takes arguments (Inputs), ensures a return type (Output) |
| **Tool Calling** | **Union Types** | LLM returns a data structure representing intent: `SearchWeb \| Calculator` |
| **Parallel Tools** | **Array of Unions** | `[SearchWeb, Calculator]` - simple type definition |
| **Agent** | **While Loop + State** | Loop: call LLM, execute returned action, update state, repeat |

**Key insight:** By defining "Tools" as Union Types in the output schema, you strip away the complexity of "binding tools" via API parameters. The schema *is* the instruction.

### 3. Fuzzy Parsing Is BAML's Job

**The Problem:** LLMs are bad at outputting perfect JSON. They add markdown backticks, conversational filler ("Here is your JSON:"), or trailing commas.

**The Wrong Fix:** Writing retry logic (asking the LLM to fix itself) - slow and expensive.

**The BAML Fix:** A deterministic, robust **Fuzzy Parser** built into the transpiler.
- BAML's runtime assumes the LLM output *contains* the data but might be messy
- It parses the string heuristically to extract the valid JSON object matching the schema
- This fixes a massive percentage of "failures" without ever calling the LLM again

**Critical:** This is BAML's responsibility, not the app developer's. You define schemas; BAML generates the parsing code.

### 4. Transpiler, Not Library

BAML is not a Python library that adds runtime overhead. It is a **Transpiler**.

1. **Write:** Developers write `.baml` files (Schema + Prompt Templates)
2. **Generate:** The BAML compiler (`baml-cli generate`) converts this into native, dependency-free Python or TypeScript code
3. **Run:** The application imports these generated functions

**Benefits:**
- Language-agnostic source of truth
- Same BAML prompts generate Python client for backend, TypeScript for frontend
- No runtime dependency on BAML
- Type-safe generated code (Pydantic models, TypeScript interfaces)

### 5. Test-Driven Prompting

The feedback loop is critical.

- In standard coding, you write tests
- In BAML, the VS Code extension provides a **"Run" button** directly above every function
- Define test cases (e.g., a tricky resume text), hit run, see immediately if extraction works
- No need to spin up the entire application stack

For CI/CD: `baml-cli test` runs all tests programmatically.

## The Golden Rules

When working with BAML, always apply these rules:

1. **Don't Parse, Transpile:** Never write regex to extract JSON. Define a BAML `class` and let generated code handle it.

2. **Types over Strings:** If you want the model to choose between options, define an `enum`. If you want it to take an action, define a `class`.

3. **Assertions for Reliability:** Use `@assert` to enforce constraints that JSON Schema cannot capture.
   - Example: `quote_text string @assert(this.length < 100)`

4. **No Logic in Prompts:** Keep prompt text for *instruction* and *context*. Keep *structure* and *validation* in BAML Class definitions.

5. **Always `{{ ctx.output_format }}`:** Every function prompt must include this injection point for schema instructions.

## When to Use BAML

**Use BAML when extraction requires:**
- Type safety and validation (compile-time schema validation, runtime type checking)
- Hierarchical data (nested structures: invoices with line items, org charts, documents with sections)
- Reliability (automatic retries with exponential backoff, multi-provider fallbacks)
- Complex schemas (unions, enums, optional fields, calculated values)
- Production robustness (@assert/@check validation, observable workflows)

**Skip BAML for:**
- Simple one-off extractions
- Creative text generation
- When simple API calls suffice

## Applying These Principles

When I encounter a BAML task, I will:

1. **Think schema-first** - What data structure do I need? Define classes before writing prompts.
2. **Use type constraints** - Enums for choices, Union types for tool selection, @assert for invariants.
3. **Trust the parser** - Don't add app-layer JSON handling; BAML's generated code handles it.
4. **Test iteratively** - Use `baml-cli test` or VS Code playground to validate extraction.
5. **Detect context** - Check `generators.baml` for target language, load appropriate patterns.

This philosophy guides all BAML implementation work.
