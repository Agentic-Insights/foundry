# Cache Structure Documentation

This directory contains the multi-tier caching system for the BAML Code Generation Skill.

## Cache Files

### patterns.json

**Purpose**: Stores discovered BAML patterns from the baml_Examples MCP server.

**Initial State**: Empty arrays and null values. After the first MCP query, the structure will be populated.

**Structure After First Query**:
```json
{
  "_comment": "Initial cache state. Timestamps and patterns will be updated automatically on first MCP query.",
  "version": "1.0.0",
  "last_updated": "2025-01-25T00:00:00Z",  // Updated on each refresh
  "repository_commit": "abc123def456...",  // Git commit hash from BoundaryML/baml-examples
  "patterns": {
    "extraction": [
      {
        "id": "uuid-v4",
        "name": "invoice_extraction",
        "description": "Extract structured data from invoices",
        "components": {
          "types": ["Invoice", "LineItem", "Address"],
          "functions": ["ExtractInvoice"],
          "clients": ["gpt-4o"]
        },
        "hit_count": 0,
        "last_used": "ISO-8601 timestamp"
      }
    ],
    "classification": [ /* Similar structure */ ],
    "rag": [ /* Similar structure */ ],
    "agents": [ /* Similar structure */ ]
  },
  "metadata": {
    "total_patterns": 150,  // Calculated dynamically
    "cache_size_bytes": 245678,
    "last_refresh": "2025-01-25T12:34:56Z"
  }
}
```

See `lib/pattern_library.md` lines 13-30 for the complete schema definition.

### query_cache.json

**Purpose**: Caches recent MCP query results to avoid redundant API calls.

**Initial State**: Empty queries array. Gets populated as MCP queries are made.

**Structure After Use**:
```json
{
  "version": "1.0.0",
  "queries": [
    {
      "query": "search_baml_documentation(\"enum syntax\")",
      "server": "baml_Docs",
      "result": { /* MCP response */ },
      "timestamp": "ISO-8601",
      "ttl": 900  // Time-to-live in seconds
    }
  ],
  "metadata": {
    "total_queries": 42,
    "cache_hits": 18,
    "cache_misses": 24,
    "hit_rate": 0.43
  }
}
```

### syntax.json

**Purpose**: Caches current BAML syntax specifications from baml_Docs MCP server.

**Initial State**: Empty syntax definitions. Populated on first validation query.

**Structure After Use**:
```json
{
  "version": "1.0.0",
  "last_updated": "2025-01-25T00:00:00Z",
  "syntax": {
    "types": {
      "class": { /* Syntax spec from BoundaryML/baml */ },
      "enum": { /* Syntax spec */ }
    },
    "functions": { /* Function syntax specs */ },
    "clients": { /* Client configuration specs */ },
    "tests": { /* Test syntax specs */ }
  },
  "repository_commit": "xyz789abc123...",  // Git commit hash from BoundaryML/baml
  "metadata": {
    "spec_version": "0.x.x",  // BAML language version
    "last_validated": "ISO-8601"
  }
}
```

## Cache Tiers

The caching system operates in 4 tiers (see `lib/cache_manager.md` for details):

- **Tier 1**: Session memory (loaded patterns, <1ms access)
- **Tier 2**: LRU memory cache (recent queries, <10ms access)
- **Tier 3**: File system (these JSON files, <50ms access)
- **Tier 4**: Live MCP queries (fallback, <500ms access)

## Maintenance

- **Automatic Updates**: Repository monitor runs daily at 00:00 UTC
- **Manual Refresh**: Delete cache files to force fresh MCP queries
- **Size Limits**: Tier 3 (disk) capped at 100MB total
- **TTL**: Query cache entries expire after 900 seconds (15 minutes)

## Troubleshooting

**Cache not populating?**
- Ensure MCP servers are configured (baml_Examples and baml_Docs)
- Check MCP connectivity with a test query
- Review logs for MCP query errors

**Stale patterns?**
- Delete `patterns.json` to force refresh
- Check `last_updated` timestamp in the file
- Verify repository_commit matches latest BoundaryML repos

**Large cache files?**
- Review `metadata.cache_size_bytes` in patterns.json
- Oldest/least-used patterns are auto-pruned at 100MB
- Manually delete query_cache.json if it grows too large

## Related Documentation

- **Pattern Library**: `lib/pattern_library.md` - Schema definitions
- **Cache Manager**: `lib/cache_manager.md` - Caching algorithms
- **MCP Interface**: `lib/mcp_interface.md` - MCP server integration
- **Repository Monitor**: `lib/repository_monitor.md` - Auto-update system
