---
name: chain-of-density-summarizer
description: Iteratively compress text using 5-turn chain-of-density summarization. Use when refactoring verbose skills to terse format, creating executive summaries, or condensing documentation while preserving key information density.
capability: transform
input:
  type: text
  description: "Long-form text: skill markdown, documentation, requirements, specifications"
  example: "---\nname: my-skill\ndescription: ...\n\n# My Skill\n\n[500+ lines of verbose instruction...]"
output:
  type: summary_with_history
  description: "High-density summary with iteration history and compression metrics"
  schema: |
    {
      "final_summary": "string (compressed text)",
      "compression_ratio": "number (0.0 to 1.0)",
      "original_size": "number (bytes)",
      "final_size": "number (bytes)",
      "iterations": [
        {
          "turn": "number (1-5)",
          "description": "string",
          "density_score": "number (0.0-1.0)",
          "content": "string",
          "size_bytes": "number"
        }
      ]
    }
calls: []
parallelizable: false
---

# Chain-of-Density Summarizer Subagent

Compress text from verbose to high-density format through 5-turn iterative summarization. Based on the chain-of-density prompting technique.

## Overview

This subagent applies a proven summarization technique that progressively increases information density across 5 iterations. Each turn removes bloat while adding specificity, entities, context, and nuance.

**Problem solved:**
- Verbose skills that could be terse and actionable
- Documentation that repeats concepts
- Long requirements documents that need condensing
- Skills exceeding 500 lines that need refactoring

**Typical use case:**
```
INPUT: SKILL.md file (600 lines, verbose)
  ↓
Turn 1: Remove redundancy (40% compression)
Turn 2: Add entity density (20% more compression)
Turn 3: Add specificity (15% more compression)
Turn 4: Add context (slight expansion)
Turn 5: Polish for nuance (final 1800-byte summary)
  ↓
OUTPUT: High-density summary (35% of original size, 95% density score)
```

## The Five Turns

### Turn 1: Remove Redundancy

**Goal**: Eliminate repetition without losing meaning

**Actions:**
1. Identify repeated phrases, concepts, examples
2. Replace repeated explanations with references
3. Consolidate similar points into single statement
4. Remove filler words ("very", "somewhat", "perhaps", "basically")
5. Remove introductory repetition ("As mentioned before...", "Again,...")
6. Collapse verbose examples to single representative example

**Expected compression**: 35-40% of original

**Density score**: 0.4

**Example:**

Before (verbose):
```
The name field is a required field that must be present in every skill.
The name field identifies the skill and must follow a specific format.
For the name field, you should use lowercase letters and hyphens only.
The name field can be 1 to 64 characters long.
```

After:
```
Required name field (1-64 chars): lowercase alphanumeric-hyphens only.
```

---

### Turn 2: Add Entity Density

**Goal**: Weave specific entities throughout to add context implicitly

**Actions:**
1. Extract key entities:
   - Names (person, system, tool: "Claude Code", "agentskills.io")
   - Constraints (numbers: "500 lines", "1-1024 chars")
   - Commands (tools: "skills-ref validate")
   - Concepts (categories: "Agent Skills", "frontmatter")
2. Weave entities into natural locations
3. Replace generic pronouns with entity names
4. Replace vague references with concrete nouns
5. Add tools/commands inline rather than in separate sections

**Expected compression**: 45-50% of original

**Density score**: 0.6

**Example:**

Before:
```
The skill description should be clear and useful. It should tell agents
when to use the skill. Try to include keywords for discovery.
```

After:
```
Description (1-1024 chars): Include "Use when..." phrase + keywords for agent discovery in Claude Code, Cursor, GitHub Copilot.
```

---

### Turn 3: Add Specificity

**Goal**: Replace vague terms with concrete examples and measurements

**Actions:**
1. Replace "error handling" with "catch FileNotFoundError, PermissionError"
2. Replace "example" with "python scripts/deploy.py --env prod"
3. Replace "documentation" with "references/api-reference.md"
4. Replace "file" with "SKILL.md" or "configuration.yaml"
5. Replace "field" with actual field name: "name field" → "name: my-skill"
6. Add URLs, version numbers, specific values
7. Include command outputs, not just command names

**Expected compression**: 40-45% of original

**Density score**: 0.75

**Example:**

Before:
```
You can validate your skills using a tool. The tool will check if your
skill follows the specification. Running the tool is important.
```

After:
```
Validate: `skills-ref validate ./skill-name` checks YAML, name format (^[a-z0-9]+(-[a-z0-9]+)*$), required fields, directory structure.
```

---

### Turn 4: Add Context

**Goal**: Include why/when each fact matters, prerequisites, and dependencies

**Actions:**
1. For each critical statement, add context: "because", "enables", "required for"
2. Identify prerequisite knowledge or setup
3. Explain consequences of decisions
4. Include warnings for gotchas
5. Note when something is optional vs critical
6. Add implementation notes

**Expected compression**: 50-55% of original (context adds back some size)

**Density score**: 0.85

**Example:**

Before:
```
SKILL.md must be under 500 lines.
```

After:
```
SKILL.md <500 lines required: agents load in context window. Exceeding wastes tokens. Move detailed docs to references/ (loaded on-demand), templates to assets/, code to scripts/.
```

---

### Turn 5: Polish for Nuance

**Goal**: Distinguish similar concepts, resolve ambiguities, add edge cases

**Actions:**
1. Distinguish similar terms that might confuse:
   - "deploy" vs "provision" vs "release"
   - "validate" vs "check" vs "verify"
   - "references/" (detailed docs) vs "assets/" (static files)
2. Resolve ambiguities from earlier turns
3. Add critical edge cases (if they affect 10%+ of use cases)
4. Improve readability: grammar, punctuation, flow
5. Ensure no contradictions between statements
6. Add cross-references for related concepts

**Expected final compression**: 30-40% of original

**Density score**: 0.95

**Example:**

Before (after turn 4):
```
SKILL.md <500 lines required: agents load in context window. Exceeding
wastes tokens. Move detailed docs to references/, templates to assets/,
code to scripts/.
```

After (turn 5):
```
SKILL.md <500 lines (critical): fits agent context window. Progressive disclosure:
- Detailed workflows → references/complete-workflow.md (loaded on-demand)
- Config templates → assets/config-template.yaml (static reference)
- Executable scripts → scripts/deploy.py (runnable code)
- Override prevents token waste and discovery.
```

---

## Processing Algorithm

```
INPUT: text
↓
[TURN 1: Remove Redundancy] → v1, density=0.4
↓
[TURN 2: Add Entity Density] → v2, density=0.6
↓
[TURN 3: Add Specificity] → v3, density=0.75
↓
[TURN 4: Add Context] → v4, density=0.85
↓
[TURN 5: Polish for Nuance] → v5, density=0.95
↓
OUTPUT: {final_summary: v5, iterations: [v1,v2,v3,v4,v5], ...}
```

## Output Schema Explained

```json
{
  "final_summary": "The compressed result (v5 from turn 5)",
  "compression_ratio": 0.35,  // final_size / original_size
  "original_size": 5200,      // bytes of input
  "final_size": 1820,         // bytes of output
  "iterations": [
    {
      "turn": 1,
      "description": "Remove Redundancy",
      "density_score": 0.4,
      "content": "The v1 summary...",
      "size_bytes": 3100
    },
    // ... turns 2-5 follow same structure
  ]
}
```

## Usage Patterns

### Pattern 1: Refactor Verbose Skill

**Use case**: Skill exceeds 500 lines; need to condense to terse format

```
INPUT: plugins/my-plugin/skills/verbose-skill/SKILL.md (600 lines)
↓
RUN: chain-of-density-summarizer
↓
OUTPUT: High-density summary suitable for body of refactored SKILL.md
↓
ACTION: User moves this summary to SKILL.md, extracts detailed sections to references/
```

**Decision point**: If compression_ratio < 0.4, the skill has significant verbosity that can be pruned.

### Pattern 2: Create Executive Summary

**Use case**: Documentation that needs quick-reference version

```
INPUT: Full API specification (1500 lines)
↓
RUN: chain-of-density-summarizer
↓
OUTPUT: 400-line executive summary with entities and specificity
↓
ACTION: User publishes summary as references/quick-start.md
```

### Pattern 3: Convert Requirements to Instructions

**Use case**: PRD or specification needs to become actionable instructions

```
INPUT: Product requirements document (800 lines)
↓
RUN: chain-of-density-summarizer
↓
OUTPUT: High-density step-by-step instructions
↓
ACTION: User creates SKILL.md based on compressed instructions
```

## Quality Metrics

### Compression Ratio
- **0.10-0.30**: Aggressive compression (50-90% reduction)
- **0.30-0.50**: Good compression (50-70% reduction)
- **0.50-0.70**: Moderate compression (30-50% reduction)
- **>0.70**: Light compression (<30% reduction)

### Density Score
- **0.95+**: Excellent (almost every word carries meaning)
- **0.85-0.95**: Very good (professional technical writing)
- **0.75-0.85**: Good (readable technical content)
- **0.60-0.75**: Moderate (some verbose phrasing remains)
- **<0.60**: Low (too much explanation, not dense enough)

### Iteration Analysis

If you see large jumps between turns:
- **Turn 1→2 big drop**: Original had lots of redundancy
- **Turn 2→3 big drop**: Original was vague; specificity helps compression
- **Turn 3→4 slight increase**: Context is important; added back for clarity
- **Turn 4→5 small change**: Mostly polish; density nearly maxed out

## Integration with build-agent-skills

### As Part of Skill Development Workflow

```
1. Draft verbose skill (don't worry about length)
2. Run chain-of-density-summarizer on SKILL.md body
3. Review compressed version
4. Adopt if quality is good; refine if needed
5. Apply progressive disclosure (detailed sections → references/)
6. Validate with skills-ref
```

### As Part of Documentation Refactoring

```
1. Identify verbose documentation
2. Run chain-of-density-summarizer on section
3. Preview iterations to see where density increases most
4. Extract insights: what made it denser?
5. Manually refactor remaining prose using same techniques
```

## Limitations & Constraints

- **Complex structured content**: Markdown with code blocks, tables, lists. Handles these but may compress sub-optimally.
- **Narrative context**: Stories, analogies are hard to compress. Removes them in early turns.
- **Domain expertise required**: Output is compressed but assumes reader has context. Not for intro-level docs.
- **Single-direction**: Can compress but can't expand. Always start with verbose version.
- **Language-specific**: Works best with English technical writing. Other languages may need adjustment.

## When NOT to Use

- **Specifications**: Don't compress specs; they need precision
- **Legal/compliance**: Don't compress contractual language
- **User-facing documentation**: End users need explanations; don't over-compress
- **Tutorial/intro material**: Beginners need step-by-step; don't compress
- **Short content**: Already <300 lines? Probably doesn't need compression

## When to Use

- **Action skills**: Instructions for experienced practitioners
- **API references**: For people who know the domain
- **Internal documentation**: For engineers who have context
- **Technical specifications** (non-legal): For developers
- **Requirements documents**: For teams familiar with the problem space
- **Post-mortems/runbooks**: For on-call engineers

## Real-World Example

**Original SKILL.md** (544 lines, agentskills-io skill):
- Multiple overview sections
- Extensive tutorial content
- Full YAML schema
- Many examples
- Best practices lists
- References to external docs

**After chain-of-density** (estimated):
- ~180-220 lines (33-40% compression)
- High density score (~0.9)
- Suitable for experienced skill developers
- Would need accompanying teaching skill (agentskills-io does this)

**Key insight**: Teaching skills intentionally break the 500-line rule. A "high-density" version would serve as quick reference; the original is the teaching material.

---

**Key principle**: Density ≠ deletion. Density = every word counts. Some content is worth keeping compressed; some is bloat.
