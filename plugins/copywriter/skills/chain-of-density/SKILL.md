---
name: chain-of-density
description: "Iteratively densify text summaries using Chain-of-Density technique. Use when compressing verbose documentation, condensing requirements, or creating executive summaries while preserving information density."
license: Apache-2.0
metadata:
  author: agentic-insights
  version: "1.0"
  paper: "From Sparse to Dense: GPT-4 Summarization with Chain of Density Prompting"
---

# Chain-of-Density Summarization

Compress text through iterative densification. Each pass adds entities and specificity while maintaining length.

## Quick Start

1. User provides text to summarize
2. You orchestrate 3-5 iterations via `cod-iteration` agent
3. Each iteration returns a denser summary
4. Return final summary + optional iteration history

## Orchestration Pattern

```
Iteration 1: Base summary (establish length)
     ↓
Iteration 2: Add entity density
     ↓
Iteration 3: Add specificity
     ↓
Iteration 4: Add context
     ↓
Iteration 5: Polish for nuance
     ↓
Final dense summary
```

## How to Orchestrate

For each iteration, invoke the `cod-iteration` agent via Task tool:

```
Task(subagent_type="cod-iteration", prompt="""
iteration: 1
target_words: 150
text: [INPUT TEXT HERE]
""")
```

Then pass output to next iteration:

```
Task(subagent_type="cod-iteration", prompt="""
iteration: 2
target_words: 150
text: [PREVIOUS SUMMARY HERE]
""")
```

**Critical**: Invoke serially, not parallel. Each iteration needs the previous output.

## Measuring Density

Use `scripts/text_metrics.py` for deterministic word counts:

```bash
echo "your summary text" | uv run scripts/text_metrics.py words
# Returns: 4

uv run scripts/text_metrics.py metrics "your summary text"
# Returns: {"words": 4, "chars": 22, "bytes": 22}
```

## Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| iterations | 5 | Number of density passes (3-5 recommended) |
| target_words | auto | Word count to maintain (derived from iteration 1) |
| return_history | false | Include all intermediate summaries |

## Output Format

### Minimal (default)
```
[Final dense summary text]
```

### With History (return_history=true)
```yaml
final_summary: |
  [Dense summary]
iterations:
  - turn: 1
    words: 152
    summary: |
      [Iteration 1 output]
  - turn: 2
    words: 148
    summary: |
      [Iteration 2 output]
  # ... etc
compression_ratio: 0.35
```

## When to Use

- Verbose skills exceeding 500 lines
- Documentation that repeats concepts
- Requirements documents needing condensation
- Creating quick-reference from detailed docs

## When NOT to Use

- Legal/compliance text (precision required)
- Tutorial content (beginners need explanation)
- Already concise content (<300 words)
- Specifications (don't compress specs)

## Example

**Input** (verbose skill excerpt, 180 words):
```
The name field is a required field that must be present in every skill.
The name field identifies the skill and must follow a specific format.
For the name field, you should use lowercase letters and hyphens only.
The name field can be 1 to 64 characters long. The description field
is also required and tells agents when to use your skill. The description
should include keywords for discovery. Try to include "Use when" in your
description so agents know when to activate your skill automatically...
```

**After 5 iterations** (~60 words):
```
Required fields: `name` (1-64 chars, lowercase alphanumeric-hyphens, pattern: ^[a-z0-9]+(-[a-z0-9]+)*$) and `description` (1-1024 chars). Description must include "Use when..." phrase + discovery keywords for agent auto-invocation in Claude Code, Cursor, GitHub Copilot.
```

## Architecture Note

This skill demonstrates **Claude Code orchestration**:
- Skill = orchestrator (this file)
- Agent = stateless worker (`cod-iteration`)
- Script = deterministic utility (`text_metrics.py`)

Sub-agents cannot call other sub-agents. Only skills/commands orchestrate via Task tool.
