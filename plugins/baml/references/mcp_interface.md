# MCP Interface Module

**Version**: 1.0.0
**Purpose**: Interface for querying BAML repositories via MCP servers
**Dependencies**: MCP tools (baml_Docs)

## Overview

This module provides a structured interface for interacting with BAML repositories through MCP (Model Context Protocol) servers. It handles query construction, response parsing, caching, and error handling.

## Available MCP Tools

### 1. fetch_baml_documentation
**Purpose**: Fetch complete BAML README
**Cost**: ~3000 tokens
**Use Case**: General context, fallback queries
**Tool**: `mcp__baml_Docs__fetch_baml_documentation`

### 2. search_baml_documentation
**Purpose**: Semantic search within documentation
**Cost**: 200-1000 tokens
**Use Case**: Finding specific syntax, features
**Tool**: `mcp__baml_Docs__search_baml_documentation`
**Input**: `{"query": "search terms"}`

### 3. search_baml_code
**Purpose**: GitHub code search (exact match)
**Cost**: ~500 tokens per page
**Use Case**: Finding implementation examples
**Tool**: `mcp__baml_Docs__search_baml_code`
**Input**: `{"query": "search terms", "page": 1}`
**Returns**: 30 results per page

### 4. fetch_generic_url_content
**Purpose**: Fetch specific file content
**Cost**: 500-2000 tokens
**Use Case**: Detailed reference retrieval
**Tool**: `mcp__baml_Docs__fetch_generic_url_content`
**Input**: `{"url": "absolute URL"}`

## Query Patterns

### Pattern 1: Syntax Lookup
**Objective**: Find BAML syntax rules
```
Query Type: search_baml_documentation
Query: "class enum function type definition syntax"
Expected Results: fern/03-reference/baml/*.mdx files
Cache Strategy: Tier 1 (embedded) or Tier 3 (7-day cache)
```

### Pattern 2: Example Discovery
**Objective**: Find code examples for a pattern
```
Query Type: search_baml_code
Query: "function Extract" OR "class Invoice" OR specific pattern
Expected Results: File paths with matching code
Cache Strategy: Tier 2 (session) or Tier 3 (7-day)
Follow-up: fetch_generic_url_content for file details
```

### Pattern 3: Pattern Category Search
**Objective**: Find all examples for a category
```
Extraction:
  - Query: "extract invoice resume receipt"
  - Paths: extract-*/**, */extract*.baml

Classification:
  - Query: "classify intent sentiment category"
  - Paths: classify-*/**, */classify*.baml

RAG:
  - Query: "rag search citation context retrieve"
  - Paths: rag-*/**, */rag*.baml

Agents:
  - Query: "agent plan execute tool workflow"
  - Paths: agent-*/**, */agent*.baml
```

### Pattern 4: Client Configuration
**Objective**: Find client setup examples
```
Query Type: search_baml_code
Query: "client provider openai anthropic gemini"
Expected Results: Client configuration blocks
Cache Strategy: Tier 3 (providers change rarely)
```

### Pattern 5: Specific Example Paths
**Objective**: Directly fetch known examples
```
Known Paths:
  - extract-receipt/
  - extract-resume/
  - extract-invoice/
  - classify-intent/
  - classify-sentiment/
  - rag-citations/
  - rag-search/
  - agent-planning/
  - multi-agent/

Method: Use search_baml_code with specific path, then fetch
```

## Query Construction Algorithm

```
FUNCTION construct_query(requirement, pattern_type):
  # Step 1: Determine query type
  IF pattern_type IN ['extraction', 'classification', 'rag', 'agents']:
    query_type = 'search_baml_code'
  ELSE IF looking_for_syntax:
    query_type = 'search_baml_documentation'
  ELSE:
    query_type = 'fetch_baml_documentation'  # Fallback

  # Step 2: Build search terms
  base_terms = PATTERN_KEYWORDS[pattern_type]
  entities = extract_entities(requirement)
  search_terms = combine(base_terms, entities)

  # Step 3: Check cache
  cache_key = hash(query_type + search_terms)
  IF cache_has(cache_key) AND not_expired(cache_key):
    RETURN cache_get(cache_key)

  # Step 4: Execute MCP query
  result = execute_mcp_query(query_type, search_terms)

  # Step 5: Cache result
  cache_set(cache_key, result, TTL=900)  # 15 min

  RETURN result
```

## Response Parsing

### Code Search Response
```
{
  "items": [
    {
      "path": "engine/baml-lib/example.baml",
      "repository": "BoundaryML/baml",
      "score": 0.95,
      "highlights": ["function ExtractInvoice"]
    },
    ...
  ],
  "total_count": 436,
  "incomplete_results": false,
  "page": 1
}

Parsing Algorithm:
1. Extract top 5 paths by score
2. For each path, construct GitHub raw URL
3. Fetch content using fetch_generic_url_content
4. Parse BAML code blocks
5. Extract types, functions, clients
```

### Documentation Search Response
```
{
  "results": [
    {
      "title": "Class Definition",
      "content": "...",
      "relevance_score": 0.92,
      "source_path": "fern/03-reference/baml/class.mdx"
    },
    ...
  ],
  "total_results": 12
}

Parsing Algorithm:
1. Sort by relevance_score (descending)
2. Extract code examples from content
3. Store in syntax cache (Tier 3)
4. Return structured syntax rules
```

## Connection Validation

### Server Availability Check
```
FUNCTION validate_mcp_connection():
  TRY:
    # Lightweight query to test connection
    result = mcp__baml_Docs__fetch_baml_documentation()
    IF result contains "BAML":
      RETURN {status: "connected", server: "baml_Docs"}
    ELSE:
      RETURN {status: "error", message: "Unexpected response"}

  CATCH error:
    RETURN {status: "unavailable", error: error, fallback: "Use embedded cache"}
```

### Fallback Strategy
```
IF mcp_unavailable:
  1. Load Tier 1 cache (embedded syntax in SKILL.md)
  2. Load Tier 3 cache (persistent patterns.json)
  3. Warn user: "Operating in offline mode with cached patterns"
  4. Use generic templates for novel patterns
  5. Suggest: "Retry when MCP connection restored"
```

## Error Handling

### Connection Errors
```
Error: "MCP server timeout"
Recovery:
  1. Retry with exponential backoff (1s, 2s, 4s)
  2. Max 3 retries
  3. Fall back to cache
  4. Log error for monitoring
```

### Query Errors
```
Error: "No results found"
Recovery:
  1. Broaden search terms
  2. Try alternative query type
  3. Use generic template
  4. Ask user for more specific requirements
```

### Rate Limiting
```
Error: "Rate limit exceeded"
Recovery:
  1. Use cached results
  2. Queue additional queries
  3. Implement exponential backoff
  4. Notify user of delay
```

## Optimization Techniques

### Query Batching
```
Instead of:
  query("class syntax")
  query("enum syntax")
  query("function syntax")

Batch:
  query("class enum function syntax")

Then parse and categorize results locally
Savings: 2 fewer MCP calls
```

### Pagination Strategy
```
For code search with many results:
  1. Fetch page 1 (30 results)
  2. Check if top results (score > 0.8) are sufficient
  3. If yes, stop (save queries)
  4. If no, fetch page 2
  5. Max 3 pages (90 results)
```

### Commit Hash Tracking
```
On first query:
  1. Store repository commit hash with result
  2. On subsequent queries, check current commit
  3. If same, use cache
  4. If different, invalidate cache and re-query

Benefits:
  - Ensures freshness
  - Avoids unnecessary queries
  - Minimal overhead (just hash check)
```

## Performance Metrics

### Target Latencies
- cache_lookup: <10ms
- search_documentation: ~250ms
- search_code: ~200ms
- fetch_url_content: ~150ms
- full_pattern_fetch: <500ms (1 search + 1-3 fetches)

### Cache Hit Rates (Projected)
- Tier 1 (syntax): 60%
- Tier 2 (session): 25%
- Tier 3 (persistent): 10%
- Tier 4 (MCP): 5%

### Cost Optimization
- Without caching: 6000 tokens/generation
- With caching: 4500 tokens/generation
- Savings: 25% average

## Integration Points

### With pattern_matcher.md
```
pattern_matcher calls mcp_interface to:
  1. Query examples for category
  2. Fetch specific pattern files
  3. Validate pattern structure
```

### With cache_manager.md
```
mcp_interface uses cache_manager to:
  1. Check cache before queries
  2. Store results after queries
  3. Manage TTL and eviction
```

### With validator.md
```
mcp_interface provides syntax rules to:
  1. Validate generated code
  2. Check type definitions
  3. Verify function signatures
```

## Usage Examples

### Example 1: Find Extraction Pattern
```
Input: "extract invoice data"

Process:
1. construct_query("extract invoice data", "extraction")
2. Query: search_baml_code("extract invoice")
3. Results: ["extract-invoice/main.baml", ...]
4. Fetch: fetch_generic_url_content(top results)
5. Parse and return structured pattern

Output:
{
  pattern_type: "extraction",
  examples: [
    {
      name: "invoice_extraction",
      path: "extract-invoice/main.baml",
      types: ["Invoice", "LineItem"],
      functions: ["ExtractInvoice"]
    }
  ]
}
```

### Example 2: Get Syntax Rules
```
Input: Need class syntax

Process:
1. Check Tier 1 cache (embedded) → Hit!
2. Return cached syntax

Output:
{
  syntax: "class Name { field type }",
  attributes: ["@alias", "@description"],
  examples: [...]
}
```

### Example 3: MCP Unavailable
```
Input: "classify sentiment"

Process:
1. Try MCP query → Timeout
2. Fall back to Tier 3 (persistent cache)
3. Find cached classification patterns
4. Return with warning

Output:
{
  pattern_type: "classification",
  examples: [...],  # From cache
  warning: "Operating offline, patterns may be outdated"
}
```

## Monitoring & Logging

### Metrics to Track
- mcp_query_count: Total queries
- mcp_query_latency: Average response time
- mcp_cache_hit_rate: Cache effectiveness
- mcp_error_rate: Connection failures
- mcp_fallback_count: Times cache was used

### Debug Mode
```
When debug enabled:
  - Log all query construction
  - Log MCP request/response
  - Log cache operations
  - Log parsing steps
  - Output detailed timing
```

## Future Enhancements

### Phase 2 (Optional)
- WebSocket connection for real-time updates
- Streaming responses for large queries
- Parallel query execution
- Query result pre-fetching
- Machine learning for query optimization

### baml_Examples Integration
- When server available, query for additional patterns
- Merge with baml_Docs patterns
- Prioritize baml_Examples for code patterns
- Use baml_Docs for syntax documentation

---

**Status**: Core implementation ready
**Next Module**: pattern_library.md (data structure)
**Dependencies**: cache_manager.md (to be implemented)
