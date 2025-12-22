# Pattern Library Module

**Version**: 1.0.0
**Purpose**: Central repository structure for BAML code patterns
**Storage**: cache/patterns.json (persistent), memory (session)

## Overview

The Pattern Library is the central data structure for storing, organizing, and retrieving BAML code patterns extracted from official repositories. It supports 1000+ pattern variations with efficient lookup and similarity matching.

## Data Structure

### Pattern Library Schema
```json
{
  "version": "1.0.0",
  "last_updated": "ISO-8601 timestamp",
  "repository_commit": "git commit hash",
  "total_patterns": "<number>",  // calculated dynamically from all patterns
  "patterns": {
    "extraction": [PatternCategory],
    "classification": [PatternCategory],
    "rag": [PatternCategory],
    "agents": [PatternCategory]
  },
  "metadata": {
    "cache_size_bytes": 0,
    "last_refresh": "ISO-8601 timestamp"
  }
}
```

### Pattern Category Structure
```json
{
  "category": "extraction | classification | rag | agents",
  "triggers": ["extract", "parse", "structure"],
  "examples": [Example],
  "templates": [Template],
  "optimizations": [OptimizationRule],
  "priority": 1-100,
  "hit_count": 0,
  "last_used": "ISO-8601 timestamp"
}
```

### Example Structure
```json
{
  "id": "uuid",
  "name": "invoice_extraction",
  "source_path": "extract-invoice/main.baml",
  "repository": "BoundaryML/baml",
  "components": {
    "types": [
      {
        "name": "Invoice",
        "definition": "class Invoice { ... }",
        "fields": ["invoice_number", "date", "items", "total"],
        "nested_types": ["LineItem"]
      }
    ],
    "functions": [
      {
        "name": "ExtractInvoice",
        "signature": "function ExtractInvoice(image: image) -> Invoice",
        "client": "openai/gpt-4o",
        "prompt_template": "Extract invoice data...",
        "has_multimodal": true
      }
    ],
    "clients": [
      {
        "name": "GPT4Vision",
        "provider": "openai",
        "model": "gpt-4o",
        "options": {"temperature": 0.0}
      }
    ],
    "tests": [
      {
        "name": "test_extract_invoice",
        "type": "happy_path",
        "framework": "pytest"
      }
    ]
  },
  "metadata": {
    "complexity": "moderate",
    "token_count": 1200,
    "success_rate": 0.98,
    "avg_latency_ms": 1500
  }
}
```

### Template Structure
```json
{
  "id": "uuid",
  "name": "base_extraction_template",
  "pattern_type": "extraction",
  "structure": {
    "base_code": "class {{OutputType}} { {{fields}} }\n\nfunction {{FunctionName}}({{params}}) -> {{OutputType}} { ... }",
    "variables": [
      {
        "name": "OutputType",
        "type": "string",
        "description": "Name of output class",
        "example": "Invoice"
      },
      {
        "name": "fields",
        "type": "array[string]",
        "description": "List of field definitions",
        "example": ["invoice_number string", "date string"]
      }
    ],
    "constraints": [
      {
        "rule": "OutputType must be PascalCase",
        "validation": "regex: ^[A-Z][a-zA-Z0-9]*$"
      }
    ]
  },
  "usage_stats": {
    "times_used": 150,
    "success_rate": 0.96,
    "average_tokens": 800
  }
}
```

### Optimization Rule Structure
```json
{
  "id": "uuid",
  "name": "token_reduction_for_prompts",
  "category": "token_optimization",
  "description": "Apply symbol tuning to compress verbose prompts",
  "applicability": {
    "pattern_types": ["extraction", "classification"],
    "min_prompt_tokens": 200
  },
  "algorithm": {
    "steps": [
      "Identify repeated phrases",
      "Replace with symbols or abbreviations",
      "Maintain semantic meaning"
    ]
  },
  "expected_savings": 0.30,  // 30% reduction
  "success_rate": 0.92
}
```

## Pattern Categories

### Extraction Patterns
**Triggers**: extract, parse, structure, data, document, form, ocr, vision
**Common Use Cases**:
- Invoice extraction
- Resume parsing
- Receipt processing
- Form extraction
- Document analysis

**Key Characteristics**:
- Often multimodal (image input)
- Complex nested output types
- Field validation rules
- High token counts (detailed prompts)

**Template Variables**:
- InputType: image | string | pdf
- OutputType: Complex class with nested types
- Validation: Business rules (e.g., subtotal + tax = total)

### Classification Patterns
**Triggers**: classify, categorize, label, identify, sentiment, intent
**Common Use Cases**:
- Sentiment analysis
- Intent detection
- Category assignment
- Priority classification

**Key Characteristics**:
- Text input
- Enum output types
- Confidence scoring
- Low token counts (fast models)

**Template Variables**:
- InputType: string | Message
- OutputType: Enum with descriptions
- Temperature: 0.0-0.3 (deterministic)

### RAG Patterns
**Triggers**: search, retrieve, context, citation, source, reference
**Common Use Cases**:
- Citation-aware search
- Source-attributed responses
- Context-based generation
- Knowledge base querying

**Key Characteristics**:
- Context injection
- Citation tracking
- Array return types (multiple sources)
- Confidence per source

**Template Variables**:
- ContextType: Document | Chunk | Source
- OutputType: Class with citations
- RankingStrategy: relevance | recency | combined

### Agent Patterns
**Triggers**: agent, plan, execute, tool, workflow, action, decision
**Common Use Cases**:
- Planning agents
- Execution agents
- Multi-agent workflows
- Tool usage

**Key Characteristics**:
- Union return types (StopTool | ActionTool)
- State management
- Chain-of-thought prompts
- Function calling patterns

**Template Variables**:
- StateType: Planning | Execution | Decision
- ToolTypes: Union of available tools
- ReasoningStyle: chain-of-thought | react | reflexion

## Pattern Matching Algorithm

```
FUNCTION match_patterns(requirement, category):
  # Step 1: Extract key features
  features = {
    entities: extract_entities(requirement),
    actions: extract_verbs(requirement),
    constraints: extract_constraints(requirement),
    complexity: estimate_complexity(requirement)
  }

  # Step 2: Retrieve candidate patterns
  candidates = patterns[category].examples

  # Step 3: Score each candidate
  FOR pattern IN candidates:
    score = calculate_similarity(features, pattern)
    ranked_patterns.append((pattern, score))

  # Step 4: Filter by threshold
  matches = filter(ranked_patterns, score > 0.7)

  # Step 5: Sort by score descending
  matches.sort(key=lambda x: x[1], reverse=True)

  # Step 6: Return top 3
  RETURN matches[:3]
```

### Similarity Scoring Algorithm
```
FUNCTION calculate_similarity(features, pattern):
  scores = []

  # Component similarity (40% weight)
  entity_match = count_matching_entities(features.entities, pattern.types)
  component_score = entity_match / max(len(features.entities), 1)
  scores.append(component_score * 0.4)

  # Complexity match (30% weight)
  complexity_diff = abs(features.complexity - pattern.metadata.complexity)
  complexity_score = 1.0 - (complexity_diff / 3.0)  # normalize 0-3 scale
  scores.append(complexity_score * 0.3)

  # Recency (20% weight)
  days_since_use = (now - pattern.last_used).days
  recency_score = 1.0 / (1.0 + days_since_use / 30.0)  # decay over 30 days
  scores.append(recency_score * 0.2)

  # Community usage (10% weight)
  usage_score = min(pattern.hit_count / 100.0, 1.0)  # cap at 100 uses
  scores.append(usage_score * 0.1)

  RETURN sum(scores)
```

## Pattern Caching Strategy

### Tier 3 Cache (Persistent)
**Location**: cache/patterns.json
**Size**: Top 20 patterns by hit_count
**TTL**: 7 days
**Update**: Weekly promotion from global stats

```
FUNCTION update_tier3_cache():
  # Load all patterns with hit counts
  all_patterns = load_all_patterns()

  # Sort by hit_count descending
  all_patterns.sort(key=lambda p: p.hit_count, reverse=True)

  # Select top 20
  top_20 = all_patterns[:20]

  # Save to cache/patterns.json
  save_to_cache(top_20, "patterns.json")

  # Log update
  log("Tier 3 cache updated: {len(top_20)} patterns")
```

### Tier 2 Cache (Session)
**Location**: In-memory
**Size**: Last 5 patterns used in conversation
**TTL**: End of conversation (15 min idle)
**Update**: LRU eviction

```
session_cache = OrderedDict()  # max_size = 5

FUNCTION cache_pattern_session(pattern):
  IF pattern.id IN session_cache:
    # Move to end (most recent)
    session_cache.move_to_end(pattern.id)
  ELSE:
    # Add new pattern
    IF len(session_cache) >= 5:
      session_cache.popitem(last=False)  # Remove oldest
    session_cache[pattern.id] = pattern
```

## Pattern Validation

### Pattern Completeness Check
```
FUNCTION validate_pattern(pattern):
  required_components = ["types", "functions", "clients"]

  FOR component IN required_components:
    IF component NOT IN pattern.components:
      RETURN False, f"Missing {component}"

  # Validate type definitions
  FOR type_def IN pattern.components.types:
    IF not is_valid_baml_type(type_def.definition):
      RETURN False, f"Invalid type: {type_def.name}"

  # Validate function signatures
  FOR function IN pattern.components.functions:
    IF not is_valid_baml_function(function.signature):
      RETURN False, f"Invalid function: {function.name}"

  RETURN True, "Pattern valid"
```

### Pattern Compilation Test
```
FUNCTION test_pattern_compiles(pattern):
  # Generate full BAML code
  baml_code = synthesize_code(pattern)

  # Attempt to parse with BAML grammar
  TRY:
    ast = parse_baml(baml_code)
    RETURN True, "Compilation successful"
  CATCH error:
    RETURN False, f"Compilation error: {error}"
```

## Pattern Discovery

### Query MCP for New Patterns
```
FUNCTION discover_patterns(category):
  # Query MCP for category examples
  mcp_results = mcp_interface.search_code(category_queries[category])

  # Parse each result
  new_patterns = []
  FOR result IN mcp_results.items[:10]:  # Top 10 results
    # Fetch file content
    content = mcp_interface.fetch_url_content(result.path)

    # Parse BAML code
    parsed = parse_baml_file(content)

    # Create pattern structure
    pattern = build_pattern_from_parsed(parsed, result)

    # Validate
    is_valid, error = validate_pattern(pattern)
    IF is_valid:
      new_patterns.append(pattern)

  RETURN new_patterns
```

### Pattern Enrichment
```
FUNCTION enrich_pattern(pattern):
  # Add metadata
  pattern.metadata.token_count = count_tokens(pattern)
  pattern.metadata.complexity = estimate_complexity(pattern)

  # Generate test template
  pattern.components.tests = generate_test_template(pattern)

  # Extract optimization opportunities
  pattern.optimizations = identify_optimizations(pattern)

  # Calculate initial quality score
  pattern.metadata.quality_score = assess_quality(pattern)

  RETURN pattern
```

## Usage Statistics

### Tracking Pattern Usage
```
FUNCTION track_pattern_usage(pattern_id, success):
  pattern = get_pattern(pattern_id)

  # Increment hit count
  pattern.hit_count += 1

  # Update success rate
  total_uses = pattern.hit_count
  success_count = pattern.metadata.success_count + (1 if success else 0)
  pattern.metadata.success_rate = success_count / total_uses

  # Update last used
  pattern.last_used = now()

  # Save updated pattern
  save_pattern(pattern)
```

### Global Statistics
```
global_stats = {
  "total_generations": 0,
  "pattern_usage": {
    "extraction": 450,
    "classification": 320,
    "rag": 180,
    "agents": 50
  },
  "top_patterns": [
    {"id": "uuid", "name": "invoice_extraction", "count": 150},
    {"id": "uuid", "name": "sentiment_classification", "count": 120},
    ...
  ]
}
```

## Pattern Adaptation

### Adaptation Strategies
```
FUNCTION adapt_pattern(base_pattern, new_requirement):
  adaptation_type = determine_adaptation_type(base_pattern, new_requirement)

  IF adaptation_type == "partial_match":
    # Keep matching components, generate missing ones
    adapted = base_pattern.copy()
    missing = identify_missing_components(new_requirement, base_pattern)
    adapted.components.update(generate_components(missing))

  ELSE IF adaptation_type == "weak_match":
    # Use as skeleton, replace core components
    adapted = create_skeleton(base_pattern)
    adapted.components = generate_components(new_requirement)

  ELSE:  # no_match
    # Ground-up generation with generic template
    adapted = generate_from_generic_template(new_requirement)

  RETURN adapted
```

## Performance Optimization

### Pattern Loading
- **Lazy Loading**: Load patterns on-demand, not all at startup
- **Indexing**: Index patterns by triggers for O(1) category lookup
- **Compression**: Store patterns in compressed format, decompress on access

### Search Optimization
- **Inverted Index**: Trigger keywords → Pattern IDs
- **Bloom Filters**: Quick negative checks before full similarity calculation
- **Parallel Matching**: Score candidates in parallel

## Integration Points

### With MCP Interface
- Pattern library requests pattern discovery via MCP
- MCP returns raw examples, pattern library structures them

### With Code Generator
- Code generator requests patterns by category
- Pattern library returns top matches with metadata

### With Cache Manager
- Pattern library uses cache manager for Tier 2/3 caching
- Cache manager handles TTL and eviction

---

**Status**: Data structure defined
**Next**: Implement in code_generator.md usage
**Scale**: Supports 1000+ patterns efficiently
