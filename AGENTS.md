# AGENTS.md - Subagent Patterns & Orchestration

Guidance for designing subagents in Claude plugins. Subagents extend agent capabilities beyond skills—they orchestrate, validate, and transform.

## When to Use Subagents

**Use skills** - Single focused task, atomic operation, reusable instruction set
**Use subagents** - Multi-step orchestration, parallel processing, conditional logic, error recovery, calling other skills in sequence

## Subagent Definition

Subagents are defined in `agents/<name>.md` with YAML frontmatter:

```yaml
---
name: subagent-name                          # Must be unique in plugin
description: What this subagent does         # Shown in agent discovery
capability: orchestration|validation|transform|review  # Category
input: { type: "description", schema: "..." }         # What it accepts
output: { type: "description", schema: "..." }        # What it produces
calls: [skill-name, other-subagent-name]             # Dependencies
parallelizable: true|false                           # Can run instances in parallel
---
```

## Core Patterns

### 1. Sequential Orchestrator
Subagent calls skills in order, passing output as input to next:

```
INPUT
  ↓
[Call Skill A] → Output A
  ↓
[Call Skill B] ← Input: Output A
  ↓
[Call Skill C] ← Input: Output B
  ↓
OUTPUT
```

**Example**: Database migration orchestrator
- Skill 1: Validate schema
- Skill 2: Generate migration script
- Skill 3: Create backup

### 2. Parallel Processor
Subagent spawns multiple instances of same skill with different inputs:

```
INPUT: [item1, item2, item3]
  ↓
[Skill instance 1] → Output 1   |
[Skill instance 2] → Output 2   | (parallel)
[Skill instance 3] → Output 3   |
  ↓
Aggregate results
  ↓
OUTPUT: [result1, result2, result3]
```

**Example**: Skill reviewer (validate N skills in parallel)
- Input: List of skill directories
- Each instance: Validate one skill
- Aggregate: Combined report

### 3. Conditional Router
Subagent examines input, decides which skill path to take:

```
INPUT
  ↓
[Analyze input]
  ↓
┌─ If condition A → [Call Skill A]
├─ If condition B → [Call Skill B]
└─ If condition C → [Call Skill C]
  ↓
OUTPUT
```

**Example**: Deployment selector
- Detect: AWS/Azure/GCP from config
- Route: Call appropriate deployment skill
- Result: Deployed application

### 4. Error Recovery
Subagent retries failed operations with fallback strategies:

```
INPUT
  ↓
[Try Primary Skill]
  ├─ Success → OUTPUT
  └─ Failure → [Try Fallback Skill 1]
      ├─ Success → OUTPUT
      └─ Failure → [Try Fallback Skill 2]
          ├─ Success → OUTPUT
          └─ Failure → [Log error, return status]
  ↓
OUTPUT
```

**Example**: Validation with recovery
- Skill 1: Validate with strict rules (fast)
- Skill 2: Validate with loose rules (slower)
- Skill 3: Manual review required (human loop)

## Example: Skill Reviewer Subagent

**File**: `agents/skill-reviewer.md`

```yaml
---
name: skill-reviewer
description: Validate individual skills for Agent Skills spec compliance. Use when reviewing multiple skills in parallel.
capability: validation
input:
  type: skill_directory_path
  schema: "/path/to/skill-name (directory containing SKILL.md)"
output:
  type: validation_report
  schema: "{ status: pass|warning|fail, issues: [], suggestions: [], metadata: {} }"
calls: [agentskills-io]
parallelizable: true
---
```

### Instructions

1. **Receive input**: Single skill directory path
2. **Read SKILL.md**: Extract frontmatter + content
3. **Invoke agentskills-io skill**: Use it to validate structure
4. **Check rules**:
   - Frontmatter: Required fields present (name, description)
   - Name format: `^[a-z0-9]+(-[a-z0-9]+)*$`
   - Directory match: Folder name == frontmatter `name`
   - File structure: Only scripts/, references/, assets/ allowed
   - Line count: SKILL.md should be <500 lines (warning if >)
   - References exist: Linked files in references/ must exist
5. **Generate report**:
   ```json
   {
     "status": "pass|warning|fail",
     "skill_name": "...",
     "issues": [
       { "field": "name", "severity": "error|warning", "message": "...", "fix": "..." }
     ],
     "suggestions": ["Consider adding metadata field", "..."],
     "metadata": { "lines": 245, "has_examples": true, "languages": ["python"] }
   }
   ```
6. **Return**: Structured report for aggregation

### Parallel Usage

```python
# Pseudo-code: Call skill-reviewer in parallel on multiple skills
skills = ["/path/to/skill1", "/path/to/skill2", "/path/to/skill3"]
results = run_parallel(skill_reviewer, skills)
aggregate_report = combine_reports(results)
```

## Example: Chain-of-Density Summarizer

**File**: `agents/chain-of-density.md`

```yaml
---
name: chain-of-density-summarizer
description: Iteratively compress text using 5-turn density-increasing summarization. Use when refactoring verbose skills or creating executive summaries.
capability: transform
input:
  type: text
  schema: "Long text or Markdown (skills, docs, requirements)"
output:
  type: summary_with_history
  schema: "{ final_summary, density_scores, iterations, compression_ratio }"
calls: []
parallelizable: false
---
```

### Instructions

**Process**: 5-turn summarization that progressively adds information density

**Turn 1: Remove Redundancy**
- Read input text
- Identify repeated concepts, examples, phrasing
- Condense to essentials (remove 40% bloat)
- Output: ~60% of original length
- Density score: 0.4

**Turn 2: Add Entity Density**
- Input: Turn 1 output
- Extract key entities (person, place, concept, tool, command)
- Weave entities throughout summary
- Reduce generic phrasing ("This" → "This command")
- Output: ~50% of original length
- Density score: 0.6

**Turn 3: Add Specificity**
- Input: Turn 2 output
- Replace vague terms with concrete examples
- Add quantities, numbers, commands where possible
- Replace "error handling" with "catch permission-denied errors"
- Output: ~45% of original length
- Density score: 0.75

**Turn 4: Add Context**
- Input: Turn 3 output
- Include why/when each fact matters
- Add prerequisites and dependencies
- Include warnings for gotchas
- Output: ~50% of original (context adds back size)
- Density score: 0.85

**Turn 5: Polish for Nuance**
- Input: Turn 4 output
- Distinguish similar concepts ("deploy" vs "provisioning")
- Resolve ambiguities
- Add edge cases if critical
- Final polish: readability, grammar, flow
- Output: Final summary
- Density score: 0.95

### Return Format

```json
{
  "final_summary": "High-density version of input",
  "compression_ratio": 0.35,
  "iterations": [
    { "turn": 1, "density": 0.4, "summary": "...", "size_bytes": 2400 },
    { "turn": 2, "density": 0.6, "summary": "...", "size_bytes": 2200 },
    { "turn": 3, "density": 0.75, "summary": "...", "size_bytes": 1900 },
    { "turn": 4, "density": 0.85, "summary": "...", "size_bytes": 2100 },
    { "turn": 5, "density": 0.95, "summary": "...", "size_bytes": 1800 }
  ],
  "original_length": 5200,
  "final_length": 1800
}
```

## Subagent Calling Convention

### From Claude (in conversation)

```
/invoke-subagent skill-reviewer /path/to/skill
```

### From another subagent (orchestration)

```
Call subagent: skill-reviewer
Input: skill_directory_path = "/path/to/skill"
Wait for: validation_report
```

### From scripts (programmatic)

```python
import json
result = claude_code.call_subagent(
    name="skill-reviewer",
    input="/path/to/skill"
)
report = json.loads(result)
```

## Design Guidelines

### Single Responsibility
- Subagent does ONE thing well
- If doing 3+ different transformations, split into separate subagents
- Each subagent is independently testable

### Idempotency
- Running same subagent twice with same input should produce same output
- Exception: time-based operations (get current date, fetch live data)

### Error Handling
- Subagent must handle skill failures gracefully
- Return structured error in output (don't crash)
- Include recovery suggestions

### Naming
- Descriptive: `skill-reviewer`, not `agent1` or `check`
- Action verb preferred: `validate`, `deploy`, `summarize`, not `task-runner`
- Lowercase-hyphenated: `chain-of-density-summarizer`

### Documentation
- 3-4 line description including "Use when..."
- Section per major workflow step
- Concrete example workflow
- Clear input/output schemas

## Parallelization Considerations

**Safe to parallelize**:
- Same skill called N times with different inputs
- Independent validation tasks
- Read-only operations
- Embarrassingly parallel problems

**NOT safe to parallelize**:
- Tasks with shared state (modify same file)
- Conditional logic dependent on sibling results
- Resource-constrained operations (too many GPU tasks)
- API rate-limited calls

**Parallelization pattern**:
```
Input: [item1, item2, ..., itemN]
  ↓
Spawn N instances of same subagent
  ↓
[Instance 1] → Result 1
[Instance 2] → Result 2
[Instance N] → Result N
  ↓
Aggregate + return combined result
```

## Key Differences: Skill vs Subagent

| Aspect | Skill | Subagent |
|--------|-------|----------|
| **Scope** | Single focused task | Multi-step orchestration |
| **Reusability** | Any agent can load + use | Plugin-specific orchestration |
| **State** | Stateless instruction set | May maintain state across calls |
| **Dependencies** | Standalone or light | Calls other skills/subagents |
| **SKILL.md** | Required, follows Agent Skills spec | Not required (uses .md) |
| **Execution** | Direct invocation | Via agent/framework dispatcher |
| **Parallelization** | Inherent (multiple agent instances) | Explicit (framework-managed) |

## Example Plugin Structure

```
my-plugin/
├── .claude-plugin/plugin.json
├── skills/
│   ├── skill-a/SKILL.md
│   ├── skill-b/SKILL.md
│   └── skill-c/SKILL.md
├── agents/
│   ├── orchestrator-subagent.md        (calls skill-a, skill-b, skill-c in order)
│   ├── parallel-validator.md           (calls skill-a N times in parallel)
│   └── conditional-router.md           (decides which skill to call)
└── examples/
    ├── orchestration-example.md
    ├── parallelization-example.md
    └── error-recovery-example.md
```

## Real-World Reference

See `build-agent-skills` plugin:
- **Skill**: `agentskills-io` (comprehensive teaching skill)
- **Subagent** (planned): `skill-reviewer` (validates skills in parallel)
- **Subagent** (planned): `chain-of-density-summarizer` (refactor verbose docs)

---

**Key Principle**: Skills teach and do; subagents orchestrate and decide.
