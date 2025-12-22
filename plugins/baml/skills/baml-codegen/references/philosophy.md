# BAML Philosophy

**Author**: Vaibhav Gupta (BoundaryML Founder)

## The Core Problem

Making AI work 80-90% is easy; production reliability (99%+) is hard. BAML treats LLM calls with the same rigor as database calls - structured, typed, and testable.

## The Five Principles

### 1. Schema Is The Prompt
Define data models first. Add `@description` to fields. The compiler automatically injects types via `{{ ctx.output_format }}` into your prompt template.

**Example**:
```baml
class Resume {
  name string @description("Candidate's full name")
  email string @description("Contact email")
  skills string[] @description("Technical skills")
}
```

The schema becomes the prompt structure - no manual JSON formatting needed.

### 2. Types Over Strings
Use enums for choices, classes for actions, unions for tool selection. No "tool binding" magic or string parsing.

**Why**: Type systems catch errors at compile time. String parsing catches them in production.

**Example**:
```baml
enum Sentiment { POSITIVE | NEGATIVE | NEUTRAL }
class Action { type ActionType, params json }
```

### 3. Fuzzy Parsing Is BAML's Job
BAML's runtime extracts valid JSON from messy LLM output. No retry logic needed. The parser handles:
- Markdown code blocks
- Trailing commas
- Missing quotes
- Mixed formats

**You write**: Clean type definitions
**BAML handles**: Dirty LLM output → clean typed objects

### 4. Transpiler Not Library
Write `.baml` files → generate native Python/TypeScript/Ruby/Go code. No runtime dependency means:
- Zero vendor lock-in
- Native IDE support
- Type safety at compile time
- Fast execution (no wrapper overhead)

**Workflow**:
```bash
# Edit source
vim baml_src/extractors.baml

# Generate client
baml-cli generate

# Use native code
from baml_client import b
result = await b.ExtractResume(resume_text)
```

### 5. Test-Driven Prompting
Use VS Code playground or `baml-cli test` to iterate without spinning up the full app.

**Benefits**:
- Instant feedback loop
- Test prompts in isolation
- Compare model outputs
- No deployment required

**Example**:
```bash
# Test single function
baml-cli test ExtractResume --input resume.txt

# Run full test suite
baml-cli test
```

## Golden Rules

### 1. Don't Parse, Transpile
Never write regex or manual JSON parsing. Define BAML classes and let the transpiler handle code generation.

❌ **Bad**: `json.loads(response)` + error handling
✅ **Good**: `b.ExtractData(input)` → typed object

### 2. Types Over Strings
Always prefer structured types over string manipulation.

❌ **Bad**: `"classify sentiment as positive/negative/neutral"`
✅ **Good**: `enum Sentiment { POSITIVE | NEGATIVE | NEUTRAL }`

### 3. @assert for Reliability
Use `@assert` to enforce constraints JSON Schema can't express.

```baml
class Product {
  price float @assert(this > 0, "Price must be positive")
  rating float @assert(this >= 0 && this <= 5, "Rating 0-5")
  stock int @assert(this >= 0, "Stock cannot be negative")
}
```

### 4. No Logic in Prompts
Keep business logic in code. Keep instructions in prompts. Keep structure in schemas.

❌ **Bad**: Complex conditional logic in prompt templates
✅ **Good**: Clear schema + simple instructions + logic in application code

### 5. Always {{ ctx.output_format }}
Every function must include `{{ ctx.output_format }}` in the prompt template. This injects the schema definition automatically.

```baml
function ExtractInvoice(invoice: string) -> Invoice {
  prompt #"
    Extract invoice details from this text:

    {{ invoice }}

    {{ ctx.output_format }}
  "#
}
```

## When to Use BAML

### ✅ Use BAML When You Need:

1. **Type Safety**: Compile-time guarantees for LLM outputs
2. **Hierarchical Data**: Nested objects, arrays, complex structures
3. **Reliability**: Built-in retries, fallbacks, validation
4. **Complex Schemas**: Many fields, constraints, relationships
5. **Production Robustness**: 99%+ reliability requirements
6. **Team Collaboration**: Multiple developers, shared types
7. **Testing**: Reproducible tests, regression prevention
8. **Multi-model**: Easy provider switching, fallbacks

### ❌ Skip BAML For:

1. **Simple Extractions**: Single-field, one-off data extraction
2. **Creative Generation**: Open-ended text, poetry, stories
3. **Prototyping**: Quick demos where types don't matter
4. **Simple API Calls**: When provider SDK is sufficient
5. **Streaming Text**: Real-time generation without structure

## Key Insights

**Reliability Gap**: The jump from 90% to 99%+ accuracy requires:
- Schema-driven prompts
- Type-safe outputs
- Automatic retries
- Validation assertions
- Testing infrastructure

BAML provides all of these out of the box.

**Developer Experience**: BAML treats LLM calls like any other typed API:
- Autocomplete
- Type checking
- Error messages
- Testing tools
- Documentation

**Performance**: By optimizing prompts and using efficient parsing:
- 50-70% token reduction vs manual prompts
- Faster responses (no retry loops)
- Lower costs
- Predictable latency

---

**References**:
- [BoundaryML Philosophy](https://github.com/BoundaryML/baml)
- [Test-Driven Prompting](https://docs.boundaryml.com/guides/testing)
- [Type System Deep Dive](https://docs.boundaryml.com/reference/types)
