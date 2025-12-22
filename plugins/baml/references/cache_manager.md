# Cache Manager Module

**Version**: 1.0.0
**Purpose**: Multi-tier caching system for MCP queries and patterns
**Storage**: Memory (Tier 1-2), File system (Tier 3), MCP (Tier 4)

## Overview

The Cache Manager implements a four-tier caching strategy to balance freshness with performance. It handles cache operations, TTL management, eviction policies, and cache invalidation.

## Cache Tiers

### Tier 1: Embedded Cache
**Location**: SKILL.md (embedded in skill file)
**Size**: 500 tokens
**TTL**: Never expires (skill-versioned)
**Content**: Core BAML syntax rules
**Hit Rate**: 60% (projected)

**Structure**:
```
Embedded directly in SKILL.md:
- Primitive types
- Basic class/enum/function syntax
- Common client configurations
- Essential directives
```

**Access**:
```
# No API needed - already in SKILL.md context
# Used automatically when skill loads
```

### Tier 2: Session Cache
**Location**: In-memory (conversation scope)
**Size**: 10 patterns, ~2MB
**TTL**: 15 minutes idle or conversation end
**Content**: Recent patterns and query results
**Eviction**: LRU (Least Recently Used)
**Hit Rate**: 25% (projected)

**Data Structure**:
```json
{
  "session_id": "uuid",
  "created": "ISO-8601",
  "last_access": "ISO-8601",
  "ttl_seconds": 900,
  "max_patterns": 10,
  "patterns": {
    "pattern_id": {
      "data": {Pattern},
      "last_accessed": "ISO-8601",
      "access_count": 5,
      "size_bytes": 1024
    }
  },
  "queries": {
    "query_hash": {
      "query": "search terms",
      "result": {MCP_Response},
      "cached_at": "ISO-8601",
      "expires_at": "ISO-8601",
      "hit_count": 3
    }
  },
  "statistics": {
    "total_accesses": 50,
    "cache_hits": 35,
    "cache_misses": 15,
    "hit_rate": 0.70
  }
}
```

### Tier 3: Persistent Cache
**Location**: cache/patterns.json, cache/syntax.json
**Size**: 20 patterns, ~100KB
**TTL**: 7 days
**Content**: Top patterns by usage, syntax rules
**Update**: Weekly promotion, commit hash validation
**Hit Rate**: 10% (projected)

**Data Structure**:
```json
{
  "version": "1.0.0",
  "created": "ISO-8601",
  "last_updated": "ISO-8601",
  "repository_commit": "git_hash",
  "ttl_days": 7,
  "patterns": [
    {
      "id": "uuid",
      "pattern": {Pattern},
      "hit_count": 150,
      "global_rank": 1,
      "cached_at": "ISO-8601"
    }
  ],
  "metadata": {
    "total_size_bytes": 102400,
    "pattern_count": 20,
    "last_promotion": "ISO-8601"
  }
}
```

### Tier 4: MCP Live Queries
**Location**: Remote (MCP servers)
**Size**: Unlimited (full repository)
**TTL**: 0 (real-time, no caching)
**Content**: All repository content, always fresh
**Hit Rate**: 5% (projected for novel/rare patterns)

**Access Pattern**:
```
Only query when:
  - Cache miss in Tier 1-3
  - Explicit refresh requested
  - Commit hash mismatch detected
  - Novel requirement (no similar pattern)
```

## Cache Operations

### Cache Lookup
```
FUNCTION cache_get(key, tier=null):
  # If tier specified, check only that tier
  IF tier:
    RETURN check_tier(key, tier)

  # Otherwise, check all tiers in order
  FOR tier IN [1, 2, 3]:
    result = check_tier(key, tier)
    IF result:
      update_access_stats(key, tier)
      RETURN {data: result, source: tier}

  # Cache miss - need MCP query (Tier 4)
  RETURN {data: null, source: 4}
```

### Cache Set
```
FUNCTION cache_set(key, value, tier, ttl=null):
  IF tier == 1:
    # Tier 1 is embedded, cannot be modified
    RETURN error("Tier 1 is read-only")

  ELSE IF tier == 2:
    # Session cache - in memory
    session_cache[key] = {
      data: value,
      cached_at: now(),
      expires_at: now() + ttl,
      access_count: 0
    }
    # Check capacity, evict if needed
    IF len(session_cache) > max_size:
      evict_lru(session_cache)

  ELSE IF tier == 3:
    # Persistent cache - file system
    patterns = load_from_file("cache/patterns.json")
    patterns[key] = {
      data: value,
      cached_at: now(),
      hit_count: 0
    }
    # Keep only top 20 by hit_count
    patterns = sort_and_trim(patterns, 20)
    save_to_file(patterns, "cache/patterns.json")

  RETURN success
```

### Cache Invalidate
```
FUNCTION cache_invalidate(key=null, tier=null):
  IF key AND tier:
    # Invalidate specific key in specific tier
    delete(tier_cache[tier], key)

  ELSE IF tier:
    # Invalidate entire tier
    clear(tier_cache[tier])

  ELSE IF key:
    # Invalidate key across all tiers
    FOR tier IN [2, 3]:  # Can't invalidate Tier 1
      delete(tier_cache[tier], key)

  ELSE:
    # Invalidate all caches (except Tier 1)
    FOR tier IN [2, 3]:
      clear(tier_cache[tier])

  log("Cache invalidated: key={key}, tier={tier}")
```

## TTL Management

### TTL Checking
```
FUNCTION is_expired(cache_entry):
  IF cache_entry.ttl == null:
    RETURN False  # Never expires

  current_time = now()
  expires_at = cache_entry.cached_at + cache_entry.ttl

  RETURN current_time > expires_at
```

### Automatic Cleanup
```
FUNCTION cleanup_expired_entries():
  # Run periodically (every 5 minutes)

  # Tier 2: Session cache
  FOR key, entry IN session_cache.items():
    IF is_expired(entry):
      delete(session_cache, key)
      log(f"Expired session cache: {key}")

  # Tier 3: Persistent cache
  patterns = load_from_file("cache/patterns.json")
  patterns = filter(patterns, lambda p: not is_expired(p))
  save_to_file(patterns, "cache/patterns.json")
```

## Eviction Policies

### LRU Eviction (Tier 2)
```
FUNCTION evict_lru(cache):
  # Find entry with oldest last_accessed
  oldest_key = None
  oldest_time = now()

  FOR key, entry IN cache.items():
    IF entry.last_accessed < oldest_time:
      oldest_time = entry.last_accessed
      oldest_key = key

  # Remove oldest entry
  IF oldest_key:
    delete(cache, oldest_key)
    log(f"LRU evicted: {oldest_key}")
```

### Hit Count Eviction (Tier 3)
```
FUNCTION evict_low_usage(patterns, max_count=20):
  # Sort by hit_count descending
  patterns.sort(key=lambda p: p.hit_count, reverse=True)

  # Keep top max_count
  kept = patterns[:max_count]
  evicted = patterns[max_count:]

  FOR pattern IN evicted:
    log(f"Evicted low usage pattern: {pattern.id}")

  RETURN kept
```

## Commit Hash Validation

### Check Repository Freshness
```
FUNCTION validate_cache_freshness(tier=3):
  # Get current repository commit hash
  current_commit = get_repository_commit_hash()

  # Load cached commit hash
  cache_data = load_from_file(f"cache/patterns.json")
  cached_commit = cache_data.repository_commit

  # Compare
  IF current_commit == cached_commit:
    RETURN {fresh: True, action: "use_cache"}
  ELSE:
    RETURN {fresh: False, action: "invalidate_and_refresh"}
```

### Get Repository Commit Hash
```
FUNCTION get_repository_commit_hash():
  # Query GitHub API for latest commit
  # Note: Lightweight query, minimal cost

  TRY:
    # Use MCP to fetch commit info
    result = mcp_interface.fetch_url_content(
      "https://api.github.com/repos/BoundaryML/baml/commits/main"
    )
    commit_hash = result.sha[:8]  # First 8 chars
    RETURN commit_hash

  CATCH error:
    # If unavailable, assume cache is fresh
    log("Unable to check commit hash, assuming fresh")
    RETURN null
```

## Cache Statistics

### Tracking Metrics
```
cache_stats = {
  "tier_1": {
    "hits": 0,
    "misses": 0,
    "hit_rate": 0.0,
    "avg_access_time_ms": 1
  },
  "tier_2": {
    "hits": 0,
    "misses": 0,
    "hit_rate": 0.0,
    "avg_access_time_ms": 5,
    "evictions": 0,
    "current_size": 0,
    "max_size": 10
  },
  "tier_3": {
    "hits": 0,
    "misses": 0,
    "hit_rate": 0.0,
    "avg_access_time_ms": 20,
    "last_refresh": "ISO-8601",
    "patterns_count": 0
  },
  "tier_4": {
    "queries": 0,
    "avg_latency_ms": 250,
    "errors": 0
  },
  "overall": {
    "total_requests": 0,
    "total_hits": 0,
    "overall_hit_rate": 0.0,
    "cache_savings_percent": 0.0
  }
}
```

### Update Statistics
```
FUNCTION update_cache_stats(tier, hit, latency_ms):
  cache_stats[f"tier_{tier}"]["hits" if hit else "misses"] += 1
  total = cache_stats[f"tier_{tier}"]["hits"] + cache_stats[f"tier_{tier}"]["misses"]
  cache_stats[f"tier_{tier}"]["hit_rate"] = cache_stats[f"tier_{tier}"]["hits"] / total

  # Update average latency (exponential moving average)
  alpha = 0.2  # Smoothing factor
  old_avg = cache_stats[f"tier_{tier}"]["avg_access_time_ms"]
  cache_stats[f"tier_{tier}"]["avg_access_time_ms"] = (
    alpha * latency_ms + (1 - alpha) * old_avg
  )

  # Update overall stats
  cache_stats["overall"]["total_requests"] += 1
  IF hit:
    cache_stats["overall"]["total_hits"] += 1

  cache_stats["overall"]["overall_hit_rate"] = (
    cache_stats["overall"]["total_hits"] / cache_stats["overall"]["total_requests"]
  )
```

## Cache Warming

### Preload Common Patterns
```
FUNCTION warm_cache():
  # Called on skill activation
  # Preload top 10 patterns into Tier 2

  # Load from Tier 3 (persistent)
  patterns = load_from_file("cache/patterns.json")

  # Sort by hit_count and take top 10
  top_patterns = sort(patterns, key="hit_count", reverse=True)[:10]

  # Load into Tier 2 (session)
  FOR pattern IN top_patterns:
    cache_set(pattern.id, pattern, tier=2, ttl=900)

  log(f"Cache warmed with {len(top_patterns)} patterns")
```

### Prefetching
```
FUNCTION prefetch_related_patterns(current_pattern):
  # Predict and prefetch patterns user might need next
  # Based on common workflows

  IF current_pattern.category == "extraction":
    # Likely to need test patterns next
    prefetch_patterns(category="extraction", type="test")

  ELSE IF current_pattern.category == "classification":
    # May need integration patterns
    prefetch_patterns(category="classification", type="integration")
```

## Cache Maintenance

### Daily Refresh (Tier 3)
```
FUNCTION daily_refresh_schedule():
  # Runs at 00:00 UTC daily

  log("Starting daily cache refresh...")

  # Check repository for updates
  freshness = validate_cache_freshness()

  IF not freshness.fresh:
    log("Repository updated, refreshing cache...")

    # Query MCP for latest patterns
    FOR category IN ["extraction", "classification", "rag", "agents"]:
      new_patterns = discover_patterns(category)
      update_tier3_cache(category, new_patterns)

    # Update commit hash
    cache_data = load_from_file("cache/patterns.json")
    cache_data.repository_commit = get_repository_commit_hash()
    cache_data.last_updated = now()
    save_to_file(cache_data, "cache/patterns.json")

    log("Cache refresh complete")
  ELSE:
    log("Cache is fresh, no refresh needed")
```

### Weekly Promotion (Tier 3)
```
FUNCTION weekly_promotion():
  # Runs every Sunday

  log("Starting weekly pattern promotion...")

  # Load all patterns with global hit counts
  all_patterns = load_all_patterns_with_stats()

  # Sort by hit_count descending
  all_patterns.sort(key=lambda p: p.hit_count, reverse=True)

  # Take top 20
  top_20 = all_patterns[:20]

  # Update Tier 3 cache
  cache_data = {
    "patterns": top_20,
    "last_promotion": now(),
    "repository_commit": get_repository_commit_hash()
  }
  save_to_file(cache_data, "cache/patterns.json")

  log(f"Promoted {len(top_20)} patterns to Tier 3")
```

## Integration with Other Modules

### With MCP Interface
```
# mcp_interface calls cache_manager before querying
result = cache_manager.get(query_hash, tier=2)
IF not result:
  result = mcp_interface.query(params)
  cache_manager.set(query_hash, result, tier=2, ttl=900)
```

### With Pattern Library
```
# pattern_library uses cache_manager for pattern storage
pattern = cache_manager.get(pattern_id, tier=2)
IF not pattern:
  pattern = cache_manager.get(pattern_id, tier=3)
  IF pattern:
    # Promote to Tier 2 for fast access
    cache_manager.set(pattern_id, pattern, tier=2, ttl=900)
```

### With Code Generator
```
# code_generator checks cache before generating
cached_code = cache_manager.get(requirement_hash, tier=2)
IF cached_code:
  RETURN cached_code  # Instant response

# Otherwise, generate and cache
code = generate_code(requirement)
cache_manager.set(requirement_hash, code, tier=2, ttl=900)
```

## Performance Targets

### Latency Goals
- Tier 1: <1ms (already loaded)
- Tier 2: <10ms (memory lookup)
- Tier 3: <50ms (file read + parse)
- Tier 4: <500ms (MCP query)

### Hit Rate Goals (Projected Targets)
- Tier 1: 60% (projected)
- Tier 2: 25% (projected)
- Tier 3: 10% (projected)
- Tier 4: 5% (projected)
- **Overall**: 95% cached (target, pending production validation)

*Note: These are performance targets based on analysis of common BAML patterns. Actual hit rates will be measured and reported post-deployment.*

### Storage Limits
- Tier 2: Max 2MB in memory
- Tier 3: Max 100MB on disk

## Error Handling

### File System Errors
```
TRY:
  patterns = load_from_file("cache/patterns.json")
CATCH FileNotFoundError:
  # Initialize empty cache
  patterns = init_empty_cache()
  save_to_file(patterns, "cache/patterns.json")
CATCH PermissionError:
  log("Cannot write cache, using memory only")
  # Fall back to Tier 2 only
```

### Corruption Handling
```
TRY:
  cache_data = json.parse(read_file("cache/patterns.json"))
CATCH JSONDecodeError:
  log("Cache file corrupted, rebuilding...")
  # Backup corrupted file
  backup_file("cache/patterns.json", "cache/patterns.json.bak")
  # Initialize fresh cache
  cache_data = init_empty_cache()
  save_to_file(cache_data, "cache/patterns.json")
```

---

**Status**: Cache strategy defined
**Next**: Integrate with mcp_interface.md and pattern_library.md
**Performance**: Projected 95% cache hit rate, 25% cost savings
