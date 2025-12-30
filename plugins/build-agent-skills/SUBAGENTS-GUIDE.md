# Subagents Guide - build-agent-skills Plugin

Quick reference for using the two new subagents to improve your skill development workflow.

## Overview

This plugin now includes two powerful subagents alongside the comprehensive `agentskills-io` teaching skill:

| Subagent | Purpose | Pattern | Time |
|----------|---------|---------|------|
| **skill-reviewer** | Validate skills for spec compliance | Parallel | ~30s per skill |

---

## Subagent 1: Skill Reviewer

**Use when:** You want to validate a skill or batch-validate all skills in a plugin.

### Quick Start

Validate a single skill:
```bash
/skill-reviewer /path/to/my-plugin/skills/my-skill
```

Output:
```json
{
  "status": "pass",
  "skill_name": "my-skill",
  "is_valid": true,
  "issues": [],
  "suggestions": [
    "Consider adding allowed-tools field for security"
  ],
  "metadata": {
    "lines": 245,
    "has_examples": true,
    "has_references": true,
    "languages": ["python", "bash"]
  }
}
```

### Batch Validation (Parallel)

Validate all skills in a plugin:

```bash
# Collect skill paths
find plugins/my-plugin/skills -name SKILL.md -type f | \
  xargs -I {} dirname {} | \
  xargs -P 4 -I {} /skill-reviewer {}
```

This runs 4 instances in parallel (adjust `-P 4` for your CPU cores).

### Understanding the Report

**Status meanings:**
- ✅ `pass` — Fully compliant, no issues
- ⚠️ `warning` — Valid but could be improved
- ❌ `fail` — Critical issues must be fixed

**Issues structure:**
```json
{
  "field": "name",
  "severity": "error|warning",
  "message": "Description of problem",
  "fix": "How to fix it"
}
```

**Suggestions:** Best-practice improvements (optional)

**Metadata:**
- `lines` — Total lines in SKILL.md
- `has_examples` — Contains code examples
- `has_references` — Uses references/ directory
- `has_scripts` — Includes scripts/ directory
- `languages` — Programming languages detected

### Common Issues & Fixes

**Issue:** "Directory name 'MySkill' doesn't match frontmatter name 'my-skill'"
```bash
# Fix: Rename directory to match
mv skills/MySkill skills/my-skill
```

**Issue:** "Referenced file not found: references/examples.md"
```bash
# Fix: Create the file or remove the reference
touch skills/my-skill/references/examples.md
# OR update SKILL.md to remove the link
```

**Issue:** "SKILL.md exceeds 500 lines (687)"
```bash
# Fix: Use progressive disclosure
# 1. Keep essentials in SKILL.md
# 2. Move detailed workflows to references/complete-workflow.md
# 3. Move templates to assets/
# 4. Move code to scripts/
```

---

## Subagent 2: Chain-of-Density Summarizer

**Use when:** Your skill documentation is verbose and needs condensing, or you want to understand where verbosity concentrates.

### Quick Start

Compress a verbose skill:
```bash
/chain-of-density-summarizer "$(cat plugins/my-plugin/skills/verbose-skill/SKILL.md)"
```

Output:
```json
{
  "final_summary": "Compressed high-density version...",
  "compression_ratio": 0.35,
  "original_size": 5200,
  "final_size": 1820,
  "iterations": [
    {
      "turn": 1,
      "description": "Remove Redundancy",
      "density_score": 0.4,
      "content": "v1 summary...",
      "size_bytes": 3100
    },
    { "turn": 2, "density_score": 0.6, ... },
    { "turn": 3, "density_score": 0.75, ... },
    { "turn": 4, "density_score": 0.85, ... },
    { "turn": 5, "density_score": 0.95, ... }
  ]
}
```

### Understanding the Output

**final_summary:** Your high-density skill body (ready to use)

**compression_ratio:** How much smaller is final vs original
- `0.35` = final is 35% of original size (65% compression)
- `0.50` = final is 50% of original size (50% compression)

**iterations:** The progression through 5 turns
- Shows density score at each step
- Shows how much content remains
- Reveals where density jumps most

### The Five Turns Explained

**Turn 1: Remove Redundancy** (density 0.4)
- Removes repeated phrases, concepts, examples
- Most aggressive compression
- Example: 5 paragraphs explaining "name field" → 1 bullet

**Turn 2: Add Entity Density** (density 0.6)
- Weaves specific entities throughout (tool names, constants, concepts)
- Replaces vague pronouns with concrete nouns
- Slight compression (v1 was already most redundancy removed)

**Turn 3: Add Specificity** (density 0.75)
- Replaces vague terms with concrete examples
- "error handling" → "catch FileNotFoundError, PermissionError"
- Good compression, more useful version

**Turn 4: Add Context** (density 0.85)
- Adds why/when each fact matters
- Adds prerequisites and dependencies
- Adds warnings for gotchas
- Adds back some size for clarity

**Turn 5: Polish for Nuance** (density 0.95)
- Distinguishes similar concepts
- Resolves ambiguities
- Final polish for readability
- Final compression pass

### How to Use the Output

**Option A: Adopt the Final Summary**
```bash
# Extract final_summary from JSON
# Replace SKILL.md body with it
# Update references/ with detailed sections
# Validate with skills-ref validate
```

**Option B: Study the Iterations**
```bash
# Don't adopt final summary directly
# Instead, understand WHERE density increased most
# If big jump from turn 1→2: original was redundant
# If big jump from turn 2→3: original was vague
# If big jump from turn 4→5: original was ambiguous

# Manually apply these insights to refactor
# Validate result
```

**Option C: Use as Refactoring Checklist**

The final_summary shows what a skilled technical writer would produce. Use it as reference:
- How dense can you make the body?
- What details belong in references/ vs body?
- Which examples can be moved to assets/?

### Compression Ratio Guidelines

- **0.10-0.30:** Aggressive (original very verbose)
- **0.30-0.50:** Good (standard refactoring)
- **0.50-0.70:** Moderate (could be terse, isn't required)
- **>0.70:** Light (already fairly dense)

If `compression_ratio > 0.70`, your skill is already terse. Don't force it shorter.

---

## Workflow Examples

### Workflow 1: Validate & Improve a Single Skill

```bash
# Step 1: Validate
/skill-reviewer plugins/my-plugin/skills/my-skill
# Output: warnings about missing license, no examples

# Step 2: Read suggestions
# Suggestion: "Add metadata field with author and version"

# Step 3: Edit SKILL.md frontmatter
# Add:
#   license: Apache-2.0
#   metadata:
#     author: your-name
#     version: "1.0"

# Step 4: Re-validate
/skill-reviewer plugins/my-plugin/skills/my-skill
# Output: status "pass", no issues
```

### Workflow 2: Batch Validate All Skills

```bash
# Collect all skills
skills=$(find plugins/my-plugin/skills -name SKILL.md -type f | \
  xargs -I {} dirname {})

# Run parallel validation
results=()
for skill in $skills; do
  result=$(/skill-reviewer "$skill")
  # Check status
  if echo "$result" | jq -e '.status != "pass"' > /dev/null; then
    results+=("$result")
  fi
done

# Print failed/warned skills
for result in "${results[@]}"; do
  echo "$result" | jq '.'
done
```

### Workflow 3: Refactor a Verbose Skill

```bash
# Step 1: Check if skill is verbose
lines=$(wc -l < plugins/my-plugin/skills/verbose-skill/SKILL.md)
if [ "$lines" -gt 500 ]; then
  echo "Skill is verbose ($lines lines)"
fi

# Step 2: Get compression insights
compression=$(/chain-of-density-summarizer "$(cat plugins/my-plugin/skills/verbose-skill/SKILL.md)")

# Step 3: Check compression ratio
ratio=$(echo "$compression" | jq '.compression_ratio')
if (( $(echo "$ratio < 0.5" | bc -l) )); then
  echo "Can compress to 50% of original - highly recommended"
fi

# Step 4: Extract high-density version
echo "$compression" | jq -r '.final_summary' > /tmp/condensed.md

# Step 5: Manually review and apply
# - Keep essentials in SKILL.md
# - Move detailed workflows to references/
# - Move templates to assets/
# - Move code to scripts/

# Step 6: Validate
/skill-reviewer plugins/my-plugin/skills/verbose-skill
```

### Workflow 4: Create New Skill from Verbose Spec

```bash
# Step 1: You have a verbose specification
spec=$(cat /tmp/verbose-spec.txt)

# Step 2: Compress it
condensed=$(/chain-of-density-summarizer "$spec")

# Step 3: Extract final summary
body=$(echo "$condensed" | jq -r '.final_summary')

# Step 4: Create SKILL.md with frontmatter
cat > plugins/my-plugin/skills/new-skill/SKILL.md <<EOF
---
name: new-skill
description: Clear description based on spec. Use when...
license: Apache-2.0
---

$body

## Examples

[Add 1-2 concrete examples]
EOF

# Step 5: Add supporting files
mkdir -p plugins/my-plugin/skills/new-skill/{references,assets,scripts}

# Step 6: Validate
/skill-reviewer plugins/my-plugin/skills/new-skill
```

---

## Integration with Other Tools

### With skills-ref Validator

```bash
# skill-reviewer uses skills-ref internally
# But you can also validate directly:

skills-ref validate plugins/my-plugin/skills/my-skill
# Checks: directory structure, YAML, format rules

/skill-reviewer plugins/my-plugin/skills/my-skill
# Checks: above + completeness + suggestions
```

### With marketplace-linter.py

```bash
# marketplace-linter.py analyzes all plugins
uv run scripts/marketplace-linter.py

# skill-reviewer validates individual skills
# Use skill-reviewer for targeted validation during development
# Use marketplace-linter for full marketplace compliance check
```

### With agentskills-io Skill

```bash
# agentskills-io: Teaching skill (what you should know)
# skill-reviewer: Validation tool (is your skill compliant?)

# Typical workflow:
# 1. Read agentskills-io to understand best practices
# 2. Write your skill
# 3. Use skill-reviewer to validate
# 4. If issues, read agentskills-io for guidance
# 5. Iterate until skill-reviewer reports "pass"
```

---

## Troubleshooting

### "Skill not found" Error

```bash
# Make sure path is correct
ls plugins/my-plugin/skills/my-skill/SKILL.md

# Make sure SKILL.md exists
touch plugins/my-plugin/skills/my-skill/SKILL.md
```

### "Invalid YAML" Error

```bash
# Check frontmatter syntax
# Look for:
# - Missing colons after keys
# - Inconsistent indentation
# - Unquoted special characters

# Example - WRONG:
---
name my-skill
description: What it does
---

# Example - RIGHT:
---
name: my-skill
description: What it does
---
```

### "Chain-of-density returns no compression"

```bash
# If compression_ratio > 0.90, text is already dense
# Don't force it shorter; it's well-written

# Or, text might be too short to meaningfully compress
# Minimum useful input: ~500 characters (one long paragraph)
```

---

## Quick Reference

| Task | Command | Time |
|------|---------|------|
| Validate one skill | `/skill-reviewer /path/to/skill` | 30s |
| Validate all skills | `find ... \| xargs -P 4 /skill-reviewer` | 2-3min |
| Compress verbose doc | `/chain-of-density-summarizer "$(cat file.md)"` | 2-3min |
| Check skill health | `/skill-reviewer` + read suggestions | 1min |
| Learn best practices | Read `agentskills-io` skill | varies |

---

## Next Steps

1. **Try it out**: Validate one of your skills with skill-reviewer
2. **Check the report**: Review issues and suggestions
3. **Fix issues**: Address any critical problems
4. **Improve quality**: Apply suggestions
5. **Learn more**: Read the full subagent definitions:
   - `agents/skill-reviewer.md` — Full validation spec
   - `agents/chain-of-density-summarizer.md` — Compression algorithm

---

For comprehensive guidance on creating Agent Skills, see the `agentskills-io` skill in this plugin.

For orchestration patterns and subagent design, see `AGENTS.md` in the repository root.
