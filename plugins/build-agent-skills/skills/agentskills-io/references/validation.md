# Skills Validation Guide

This guide covers using the `skills-ref` validation tool, interpreting validation results, and troubleshooting common issues.

## Installation

The `skills-ref` tool is the official reference implementation for validating Agent Skills compliance. No installation is needed with `uvx`.

### Using uvx (Recommended)

Run validation without installing:

```bash
uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
  skills-ref validate path/to/skill
```

### Create Alias (Optional)

For convenience, create a shell alias:

```bash
# Add to ~/.bashrc or ~/.zshrc
alias skills-ref='uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref'

# Then use simply:
skills-ref validate ./my-skill
```

### Traditional Installation

If you prefer installing locally:

```bash
# Clone the repository
git clone https://github.com/agentskills/agentskills.git
cd agentskills/skills-ref

# Install with pip
pip install -e .

# Or with uv
uv pip install -e .
```

## Validation Commands

### 1. Validate Structure

The primary command checks frontmatter validity, naming conventions, and file structure:

```bash
skills-ref validate ./my-skill
```

**Success Output**:
```
✓ Valid skill: ./my-skill
```

**Failure Output**:
```
✗ Invalid skill: ./my-skill

Errors:
  - 'name' field contains invalid characters (must be lowercase alphanumeric with hyphens)
  - 'description' field exceeds 1024 characters

Warnings:
  - No 'license' field specified (recommended)
  - SKILL.md exceeds 500 lines (consider refactoring)
```

### 2. Read Properties

Extract frontmatter metadata as JSON:

```bash
skills-ref read-properties ./my-skill
```

**Output**:
```json
{
  "name": "aws-bedrock-deployment",
  "description": "Deploy LangGraph agents to AWS Bedrock AgentCore with memory, tools, and observability. Use when building AI agents on AWS with Claude models.",
  "license": "Apache-2.0",
  "compatibility": "Requires AWS CLI 2.x, Python 3.10+, valid AWS credentials with Bedrock access",
  "metadata": {
    "author": "agentic-insights",
    "version": "2.1.0",
    "category": "aws-deployment",
    "difficulty": "intermediate",
    "estimated-time": "30min"
  },
  "allowed-tools": "bash aws docker python"
}
```

**Use Cases**:
- CI/CD pipelines extracting version numbers
- Automated documentation generation
- Skill marketplace indexing
- Integration with skill management tools

### 3. Generate Agent Prompt

Create XML-formatted skill description for agent system prompts:

```bash
skills-ref to-prompt ./my-skill
```

**Output**:
```xml
<available_skills>
<skill>
<name>
aws-bedrock-deployment
</name>
<description>
Deploy LangGraph agents to AWS Bedrock AgentCore with memory, tools, and observability. Use when building AI agents on AWS with Claude models.
</description>
<location>
/path/to/my-skill/SKILL.md
</location>
</skill>
</available_skills>
```

This format is used by:
- Claude (Anthropic's models)
- Claude Code
- Other agents following Anthropic's prompt conventions

**Use Case**: Building custom agent systems that need to dynamically load skills.

### 4. Batch Validation

Validate multiple skills at once:

```bash
# Validate all skills in a directory
for skill_dir in skills/*/; do
  echo "Validating $skill_dir"
  skills-ref validate "$skill_dir"
done
```

**CI/CD Example** (GitHub Actions):
```yaml
- name: Validate all skills
  run: |
    for skill in plugins/*/skills/*/; do
      echo "::group::Validating $skill"
      uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
        skills-ref validate "$skill" || exit 1
      echo "::endgroup::"
    done
```

## Common Validation Errors

### Error: Invalid Name Format

**Message**: `'name' field contains invalid characters (must be lowercase alphanumeric with hyphens)`

**Causes**:
- Uppercase letters: `My-Skill`
- Underscores: `my_skill`
- Leading/trailing hyphens: `-my-skill` or `my-skill-`
- Consecutive hyphens: `my--skill`
- Special characters: `my@skill`, `my.skill`

**Fix**:
```yaml
# ❌ Invalid
name: My_Skill-Name
name: -my-skill
name: my--skill

# ✅ Valid
name: my-skill-name
name: my-skill
name: deploy-aws-lambda
```

### Error: Missing Required Fields

**Message**: `'description' field is required`

**Fix**: Add the missing field to frontmatter:
```yaml
---
name: my-skill
description: Clear description of what this skill does and when to use it.
---
```

### Error: Description Too Long

**Message**: `'description' field exceeds 1024 characters`

**Fix**: Shorten the description to focus on core functionality:

```yaml
# ❌ Too long (1200 chars)
description: This skill provides comprehensive functionality for deploying applications to AWS Lambda including support for Python, Node.js, and Go runtimes with automatic dependency packaging, environment variable management, VPC configuration, IAM role creation, CloudWatch logging setup, API Gateway integration, custom domain configuration, and much more...

# ✅ Concise (150 chars)
description: Deploy serverless functions to AWS Lambda with dependencies, environment variables, and IAM roles. Use for APIs, event processors, or scheduled tasks.
```

Move detailed information to the skill body instead.

### Error: Invalid YAML Syntax

**Message**: `Invalid YAML syntax in frontmatter`

**Common Causes**:
1. **Unquoted special characters**:
   ```yaml
   # ❌ Invalid
   description: Deploy apps with @special #characters

   # ✅ Valid
   description: "Deploy apps with @special #characters"
   ```

2. **Incorrect indentation**:
   ```yaml
   # ❌ Invalid (2 space indent, then 4 space)
   metadata:
     author: example
       version: "1.0"

   # ✅ Valid (consistent 2 space indent)
   metadata:
     author: example
     version: "1.0"
   ```

3. **Missing quotes for version numbers**:
   ```yaml
   # ❌ Invalid (YAML interprets as float)
   version: 1.0

   # ✅ Valid (string)
   version: "1.0"
   ```

### Error: Missing SKILL.md

**Message**: `SKILL.md not found in skill directory`

**Fix**: Ensure file exists with exact name (all caps):
```bash
# Check filename
ls -la my-skill/

# Rename if needed
mv my-skill/skill.md my-skill/SKILL.md
mv my-skill/Skill.md my-skill/SKILL.md
```

### Warning: No License Field

**Message**: `No 'license' field specified (recommended)`

**Impact**: Warning only, skill is still valid

**Fix**: Add license to frontmatter:
```yaml
---
name: my-skill
description: My skill description
license: Apache-2.0  # or MIT, BSD-3-Clause, etc.
---
```

### Warning: Large SKILL.md

**Message**: `SKILL.md exceeds 500 lines (consider refactoring)`

**Impact**: Warning only, but affects context efficiency

**Fix**: Use progressive disclosure:
1. Keep main workflow in SKILL.md
2. Move detailed content to `references/`
3. Link to references from main skill

See [best-practices.md](best-practices.md#progressive-disclosure) for refactoring guidance.

## Troubleshooting Validation Issues

### Validation Passes But Skill Doesn't Load

**Symptom**: `skills-ref validate` succeeds, but agent doesn't recognize skill

**Checks**:
1. **File location**: Ensure skill is in agent's expected directory
   - Claude Code: `.claude/plugins/*/skills/`
   - Cursor: `.cursor/skills/`
   - Check platform documentation

2. **File permissions**: Ensure SKILL.md is readable
   ```bash
   chmod 644 my-skill/SKILL.md
   ```

3. **Character encoding**: Verify UTF-8 encoding
   ```bash
   file -i my-skill/SKILL.md
   # Should show: charset=utf-8
   ```

4. **YAML parsing**: Test YAML manually
   ```bash
   # Extract and validate YAML
   sed -n '/^---$/,/^---$/p' my-skill/SKILL.md | head -n -1 | tail -n +2 | python3 -c "import yaml, sys; yaml.safe_load(sys.stdin)"
   ```

### Validation Hangs or Crashes

**Symptom**: `skills-ref validate` doesn't complete

**Causes**:
1. **Extremely large files**: Skills with massive content
2. **Circular references**: If custom validation added

**Fix**:
```bash
# Check file size
du -h my-skill/SKILL.md

# If > 10MB, skill is likely too large
# Refactor into smaller files
```

### Different Results on Different Platforms

**Symptom**: Validates on Linux but fails on Windows (or vice versa)

**Causes**:
1. **Line endings**: CRLF vs LF
2. **Path separators**: `\` vs `/`
3. **File permissions**

**Fix**:
```bash
# Normalize line endings to LF
dos2unix my-skill/SKILL.md

# Or with git
git config core.autocrlf input
```

## Integration Examples

### Pre-commit Hook

Validate skills before committing:

```bash
#!/bin/bash
# .git/hooks/pre-commit

SKILLS=$(git diff --cached --name-only --diff-filter=ACM | grep 'skills/.*/SKILL.md$' | xargs dirname | sort -u)

if [ -n "$SKILLS" ]; then
  echo "Validating modified skills..."
  for skill in $SKILLS; do
    echo "Checking $skill..."
    uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
      skills-ref validate "$skill" || exit 1
  done
fi
```

### CI/CD Pipeline

GitHub Actions example:

```yaml
name: Validate Skills

on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install uv
        run: pip install uv

      - name: Validate all skills
        run: |
          EXIT_CODE=0
          for skill in plugins/*/skills/*/; do
            if [ -f "$skill/SKILL.md" ]; then
              echo "::group::Validating $skill"
              if ! uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
                skills-ref validate "$skill"; then
                EXIT_CODE=1
              fi
              echo "::endgroup::"
            fi
          done
          exit $EXIT_CODE
```

### Makefile Target

```makefile
.PHONY: validate-skills
validate-skills:
	@echo "Validating all skills..."
	@for skill in $$(find . -name "SKILL.md" -type f -exec dirname {} \;); do \
		echo "Validating $$skill..."; \
		uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
			skills-ref validate "$$skill" || exit 1; \
	done
	@echo "All skills validated successfully!"
```

Usage: `make validate-skills`

## Advanced Validation

### Custom Validation Rules

For organization-specific requirements, extend validation:

```python
# custom_validate.py
import sys
from pathlib import Path

def validate_custom_rules(skill_path):
    """Add organization-specific validation."""
    skill_md = Path(skill_path) / "SKILL.md"
    content = skill_md.read_text()

    # Example: Require "Security Considerations" section
    if "## Security Considerations" not in content:
        print(f"❌ Missing required section: Security Considerations")
        return False

    # Example: Check for required metadata
    if '"author": "agentic-insights"' not in content:
        print(f"❌ Author must be 'agentic-insights'")
        return False

    return True

if __name__ == "__main__":
    skill_path = sys.argv[1]
    if not validate_custom_rules(skill_path):
        sys.exit(1)
```

Run both standard and custom validation:
```bash
skills-ref validate ./my-skill && python custom_validate.py ./my-skill
```

### Validation in Development Workflow

Recommended workflow:

1. **During development**: Run validation frequently
   ```bash
   # Watch for changes and validate
   while inotifywait -e modify my-skill/SKILL.md; do
     skills-ref validate my-skill
   done
   ```

2. **Before committing**: Pre-commit hook (see above)

3. **In CI/CD**: Block merges on validation failures

4. **Before publishing**: Final validation check
   ```bash
   skills-ref validate ./my-skill && \
   echo "✅ Skill ready to publish"
   ```

## Getting Help

If validation issues persist:

1. **Check specification**: https://agentskills.io/specification
2. **Review examples**: https://github.com/agentskills/agentskills/tree/main/skills
3. **Report issues**: https://github.com/agentskills/agentskills/issues
4. **Community discussion**: https://github.com/agentskills/agentskills/discussions

Include in bug reports:
- Output of `skills-ref validate`
- Your `SKILL.md` frontmatter
- Platform/OS information
- Python version: `python --version`
