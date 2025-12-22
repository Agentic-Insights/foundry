# Pattern Matcher Module

**Version**: 1.0.0
**Purpose**: Match requirements to best BAML patterns from repository
**Dependencies**: mcp_interface.md, pattern_library.md, cache_manager.md

## Overview

The Pattern Matcher takes structured requirement specifications and finds the most similar patterns from the BAML repository. It queries MCP, scores candidates, and returns ranked matches for code generation.

## Core Matching Algorithm

```
FUNCTION find_patterns(requirement_spec):
  category = requirement_spec.category

  # Step 1: Check cache
  cache_key = generate_hash(requirement_spec)
  cached = cache_manager.get(cache_key, tier=2)
  IF cached:
    RETURN cached

  # Step 2: Query MCP for patterns
  patterns = query_patterns_from_mcp(category, requirement_spec)

  # Step 3: Score each pattern
  scored_patterns = []
  FOR pattern IN patterns:
    score = calculate_similarity(requirement_spec, pattern)
    scored_patterns.append((pattern, score))

  # Step 4: Filter by threshold
  matches = filter(scored_patterns, lambda x: x[1] > 0.7)

  # Step 5: Sort by score
  matches.sort(key=lambda x: x[1], reverse=True)

  # Step 6: Return top 3
  top_3 = matches[:3]

  # Step 7: Cache results
  cache_manager.set(cache_key, top_3, tier=2, ttl=900)

  RETURN top_3
```

## Similarity Scoring

```
FUNCTION calculate_similarity(requirement_spec, pattern):
  # Component match (40%)
  component_score = score_component_match(
    requirement_spec.entities,
    pattern.components
  ) * 0.4

  # Complexity match (30%)
  complexity_score = score_complexity_match(
    requirement_spec.complexity,
    pattern.metadata.complexity
  ) * 0.3

  # Recency (20%)
  recency_score = score_recency(pattern.last_used) * 0.2

  # Usage (10%)
  usage_score = score_usage(pattern.hit_count) * 0.1

  RETURN component_score + complexity_score + recency_score + usage_score
```

## Template Selection

```
FUNCTION select_template(requirement_spec, patterns):
  IF len(patterns) == 0:
    RETURN get_generic_template(requirement_spec.category)

  best_pattern = patterns[0][0]  # Highest scored

  # Determine adaptation strategy
  similarity = patterns[0][1]

  IF similarity > 0.9:
    RETURN {"strategy": "direct_use", "pattern": best_pattern}
  ELSE IF similarity > 0.7:
    RETURN {"strategy": "adapt", "pattern": best_pattern}
  ELSE:
    RETURN {"strategy": "hybrid", "pattern": best_pattern, "fallback": True}
```

## Fallback Handling

```
FUNCTION handle_mcp_unavailable(requirement_spec):
  # Load from persistent cache
  cached_patterns = cache_manager.get_all(tier=3)

  # Filter by category
  category_patterns = filter(cached_patterns,
    lambda p: p.category == requirement_spec.category)

  IF len(category_patterns) > 0:
    RETURN category_patterns[:3]

  # Ultimate fallback: generic template
  RETURN [get_generic_template(requirement_spec.category)]
```

---

**Status**: Pattern matching implemented with fallback
**Next**: code_generator.md
