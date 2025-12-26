---
name: skill-reviewer
description: Validate individual skills for Agent Skills specification compliance. Use when reviewing multiple skills in parallel or batch-validating a plugin's skill library.
capability: validation
input:
  type: skill_directory_path
  description: "Absolute path to skill directory containing SKILL.md"
  example: "/home/user/my-plugin/skills/my-skill"
output:
  type: validation_report
  description: "Structured validation report with status, issues, and suggestions"
  schema: |
    {
      "status": "pass|warning|fail",
      "skill_name": "string",
      "skill_path": "string",
      "is_valid": "boolean",
      "frontmatter": { "name": "...", "description": "...", ... },
      "issues": [
        { "field": "string", "severity": "error|warning", "message": "string", "fix": "string" }
      ],
      "suggestions": ["string"],
      "metadata": {
        "lines": "number",
        "has_examples": "boolean",
        "has_references": "boolean",
        "has_scripts": "boolean",
        "has_assets": "boolean",
        "languages": ["string"]
      }
    }
calls: ["agentskills-io"]
parallelizable: true
---

# Skill Reviewer Subagent

Validate individual Agent Skills for specification compliance. Design supports parallel execution for batch validation.

## Overview

This subagent examines a single skill directory and produces a structured validation report. It can run multiple instances in parallel to validate entire plugin skill libraries.

**Typical use case:**
```
INPUT: skill_directories = [skill1_path, skill2_path, skill3_path, ...]
  ↓
Run 3 parallel instances of skill-reviewer
  ↓
Aggregate reports into combined summary
  ↓
OUTPUT: { total: 3, passed: 2, failed: 1, warnings: 1, ... }
```

## Validation Workflow

### Step 1: Verify SKILL.md Exists

- Check: `<input_path>/SKILL.md` exists
- **Error if**: File missing or inaccessible
- Severity: Critical (skill is invalid without it)

### Step 2: Parse Frontmatter

- Extract YAML frontmatter between `---` delimiters
- Extract required fields: `name`, `description`
- Extract optional fields: `license`, `compatibility`, `metadata`, `allowed-tools`
- **Error if**: YAML is invalid (syntax error)
- **Error if**: Required fields missing

### Step 3: Validate Required Fields

**Name field:**
- Pattern: `^[a-z0-9]+(-[a-z0-9]+)*$` (lowercase alphanumeric-hyphens)
- Length: 1-64 characters
- Constraint: MUST match parent directory name
- **Error if**: Pattern invalid or name doesn't match directory
- Severity: Critical

**Description field:**
- Length: 1-1024 characters
- **Error if**: Too short (<10 chars) or too long (>1024)
- **Warning if**: Missing "Use when..." phrase (important for agent discovery)
- Severity: Error or Warning

### Step 4: Check File Structure

Check for allowed subdirectories:
- `scripts/` — Executable code
- `references/` — Supporting documentation
- `assets/` — Static resources

**Error if**: Other subdirectories found
- Examples of violations: `examples/`, `docs/`, `tests/`, `__pycache__/`

Severity: Warning (allowed but not spec-compliant)

### Step 5: Analyze SKILL.md Content

- Count lines in SKILL.md
- **Warning if**: Exceeds 500 lines (suggests need for progressive disclosure)
- Detect: Presence of code examples, references, diagrams
- Detect: Programming languages used

### Step 6: Validate References & Assets

If `references/` exists:
- List all `.md` files
- Check: Links in SKILL.md point to existing files
- **Error if**: Referenced file missing
- Severity: Error (broken link)

If `assets/` exists:
- List all files (no specific requirements)
- Verify: Not empty

If `scripts/` exists:
- List all executable files
- Check: Shebang or extension indicates executable type
- Note: Executability in report metadata

### Step 7: Use agentskills-io Skill for Validation

Invoke the `agentskills-io` skill for final spec validation:
- Use `skills-ref validate <path>` logic
- Capture any errors or warnings from official validator
- If official validator passes, mark as valid
- If official validator fails, report those errors

### Step 8: Generate Suggestions

Based on findings, suggest improvements:
- "Consider adding `license` field to frontmatter" (if missing)
- "Description could include 'Use when...' for better discovery"
- "SKILL.md has 550 lines; consider moving details to `references/`"
- "Add `metadata` with author and version for professional presentation"
- "No examples found; include at least one concrete example in body"

### Step 9: Return Validation Report

Structure follows the schema above:
```json
{
  "status": "pass|warning|fail",
  "skill_name": "my-skill",
  "skill_path": "/path/to/my-skill",
  "is_valid": true,
  "frontmatter": {
    "name": "my-skill",
    "description": "Do something useful. Use when creating X or solving Y.",
    "license": "Apache-2.0"
  },
  "issues": [],
  "suggestions": [
    "Add metadata field with author and version",
    "Consider expanding examples with error handling section"
  ],
  "metadata": {
    "lines": 245,
    "has_examples": true,
    "has_references": false,
    "has_scripts": true,
    "has_assets": false,
    "languages": ["python", "bash"]
  }
}
```

## Error Severity Levels

**CRITICAL** (status = fail)
- SKILL.md missing
- Frontmatter invalid YAML
- Required field missing (name or description)
- Name format invalid
- Directory name ≠ frontmatter name
- Referenced file missing

**WARNING** (status = warning)
- Description too short (<10 chars)
- SKILL.md exceeds 500 lines
- Missing optional fields (license, metadata)
- Unknown subdirectory present
- No examples provided
- Missing "Use when..." in description

**INFO** (included in suggestions)
- Could improve clarity
- Best practice opportunities
- Enhancement suggestions

## Parallelization

This subagent is designed for parallel execution:

```python
from concurrent.futures import ThreadPoolExecutor
import json

# List of skills to validate
skills = [
  "/path/to/skill1",
  "/path/to/skill2",
  "/path/to/skill3"
]

# Run validation in parallel
results = []
with ThreadPoolExecutor(max_workers=3) as executor:
  futures = [executor.submit(validate_skill, skill) for skill in skills]
  results = [f.result() for f in futures]

# Aggregate results
aggregate_report = {
  "total_skills": len(results),
  "valid": sum(1 for r in results if r["status"] == "pass"),
  "warnings": sum(1 for r in results if r["status"] == "warning"),
  "errors": sum(1 for r in results if r["status"] == "fail"),
  "details": results
}

print(json.dumps(aggregate_report, indent=2))
```

## Integration with build-agent-skills Plugin

### Standalone Usage

Validate a single skill:
```bash
# Assume plugin is loaded in Claude Code
/skill-reviewer /path/to/skill
```

### Batch Validation (Sequential)

Validate all skills in a plugin:
```bash
for skill_dir in plugins/my-plugin/skills/*/; do
  /skill-reviewer "$skill_dir"
done
```

### Marketplace Linting

The `marketplace-linter.py` script (in repo scripts/) can be updated to use this subagent:
```python
# Current: Direct validation
# Future: Invoke skill-reviewer subagent for each skill

from concurrent.futures import ThreadPoolExecutor
results = executor.map(invoke_skill_reviewer, skill_paths)
```

## Related Tools

- **Skill**: `agentskills-io` — Comprehensive Agent Skills guidance
- **CLI**: `skills-ref validate` — Official validator (called internally)
- **Script**: `scripts/validate-skills-repo.sh` — Batch validation wrapper
- **Linter**: `scripts/marketplace-linter.py` — Marketplace compliance checker
- **Browser**: `scripts/marketplace-browser.html` — Visual linting dashboard

## Example Report Output

Valid skill:
```json
{
  "status": "pass",
  "skill_name": "aws-lambda-deploy",
  "is_valid": true,
  "issues": [],
  "suggestions": [
    "Consider adding allowed-tools field to whitelist bash, aws, python"
  ]
}
```

Skill with warnings:
```json
{
  "status": "warning",
  "skill_name": "data-analysis",
  "is_valid": true,
  "issues": [
    {
      "field": "description",
      "severity": "warning",
      "message": "Description lacks 'Use when...' phrase for agent discovery",
      "fix": "Add context: 'Use when exploring datasets or generating reports.'"
    },
    {
      "field": "frontmatter",
      "severity": "warning",
      "message": "Missing optional license field",
      "fix": "Add: license: Apache-2.0"
    }
  ],
  "suggestions": [
    "Consider moving extended examples to references/examples.md",
    "Add metadata field with author, version, and category tags"
  ]
}
```

Skill with errors:
```json
{
  "status": "fail",
  "skill_name": "invalid-skill",
  "is_valid": false,
  "issues": [
    {
      "field": "name",
      "severity": "error",
      "message": "Directory name 'InvalidSkill' doesn't match frontmatter name 'invalid-skill'",
      "fix": "Rename directory to 'invalid-skill' to match frontmatter"
    },
    {
      "field": "references/api.md",
      "severity": "error",
      "message": "Referenced file not found",
      "fix": "Create references/api.md or remove the link from SKILL.md"
    }
  ]
}
```

---

**Key insight**: This subagent validates the *structure* of skills. The `agentskills-io` skill provides the *guidance* for writing better skills. Use subagent for QA; use skill for education.
