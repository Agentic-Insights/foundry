---
name: working-with-agent-skills
description: Create, validate, and publish Agent Skills following the official open standard from agentskills.io. Use when (1) creating new skills for AI agents, (2) validating skill structure and metadata, (3) understanding the Agent Skills specification, (4) converting existing documentation into portable skills, or (5) ensuring cross-platform compatibility with Claude Code, Cursor, GitHub Copilot, and other tools.
license: Apache-2.0
metadata:
  author: agentic-insights
  version: "1.0"
  spec-url: https://agentskills.io/specification
  reference-repo: https://github.com/agentskills/agentskills
---

# Working with Agent Skills

Create, validate, and publish portable skills following the open standard for AI agent capabilities.

## What Are Agent Skills?

**Agent Skills** are modular packages that extend AI agent capabilities. Originally developed by Anthropic and released as an open standard, they are now supported by major AI development tools:

- **Claude Code** and **Claude** (Anthropic)
- **Cursor**
- **GitHub Copilot**
- **OpenAI** integrations
- **VS Code** and specialized agents

**Why use skills?**
- Package domain expertise as reusable instructions
- Enable new agent capabilities
- Ensure repeatable workflows
- Work across multiple AI tools
- Load instructions efficiently with progressive disclosure

**Official Resources**:
- Specification: https://agentskills.io/specification
- Reference Implementation: https://github.com/agentskills/agentskills

## Quick Start

### Creating Your First Skill

**1. Create directory structure**:
```bash
mkdir -p my-skill-name
cd my-skill-name
touch SKILL.md
```

**2. Add frontmatter and content**:

Use the [basic template](assets/skill-template.md) or start with this minimal example:

```yaml
---
name: my-skill-name
description: Clear description of what this skill does and when to use it.
license: Apache-2.0
---

# My Skill Name

## Prerequisites

- Python 3.10+
- Required tools or credentials

## Instructions

1. First step with concrete command
2. Second step with example
3. Verification step

## Example

Concrete example demonstrating the skill.
```

**3. Validate**:
```bash
uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
  skills-ref validate .
```

**4. Test with an AI agent** (Claude Code, Cursor, etc.)

**5. Iterate** based on agent behavior and refine instructions

### Validation Commands

**Validate structure**:
```bash
skills-ref validate ./my-skill
```

**Extract metadata**:
```bash
skills-ref read-properties ./my-skill
```

**Generate agent prompt format**:
```bash
skills-ref to-prompt ./my-skill
```

## File Structure

### Required

```
skill-name/
└── SKILL.md          # Frontmatter + instructions
```

### Recommended

```
skill-name/
├── SKILL.md          # Primary instructions (<500 lines)
├── scripts/          # Executable scripts
├── references/       # Supporting documentation (loaded on-demand)
└── assets/           # Templates, diagrams, examples
```

**Progressive disclosure**: Keep SKILL.md concise, move detailed content to `references/` and link as needed.

## Frontmatter Schema

### Required Fields

- **`name`**: Skill identifier (1-64 chars, lowercase alphanumeric with hyphens)
  - Format: `^[a-z0-9]+(-[a-z0-9]+)*$`
  - Example: `deploy-aws-lambda`, `postgres-migration`

- **`description`**: What the skill does and when to use it (1-1024 chars)
  - Include keywords for agent discovery
  - Start with capability, add "Use when..." for context
  - Example: "Deploy Python functions to AWS Lambda with dependencies and IAM roles. Use when creating serverless APIs, event processors, or scheduled tasks."

### Optional Fields

- **`license`**: SPDX identifier (e.g., `Apache-2.0`, `MIT`, `Proprietary`)
- **`compatibility`**: Environment requirements (max 500 chars)
- **`metadata`**: Key-value pairs (author, version, tags, etc.)
- **`allowed-tools`**: Space-delimited list of pre-approved tools (experimental)

### Complete Example

```yaml
---
name: aws-lambda-deploy
description: Deploy Python functions to AWS Lambda with dependencies, environment variables, and IAM roles. Use when creating serverless APIs or event processors.
license: Apache-2.0
compatibility: Requires AWS CLI 2.x, Python 3.9+, valid AWS credentials
metadata:
  author: agentic-insights
  version: "1.0.0"
  category: aws-deployment
  difficulty: intermediate
allowed-tools: bash aws python
---
```

## Writing Effective Instructions

### 1. Be Clear and Direct

Use imperative language:
```markdown
✅ 1. Check if file exists: `test -f config.json`
✅ 2. Create if missing: `touch config.json`

❌ You might want to check if the file exists...
```

### 2. Provide Concrete Examples

Show specific, runnable examples:
```markdown
## Example: Deploy to Production

```bash
python scripts/deploy.py --env prod --region us-east-1
```

**Expected Output**:
```
Deployment successful!
Function ARN: arn:aws:lambda:us-east-1:123:function:my-api
```
```

### 3. Handle Errors

Anticipate common failures:
```markdown
## Troubleshooting

**Error**: "Permission denied"
**Solution**: Grant permissions: `chmod +x scripts/deploy.py`

**Error**: Connection timeout
**Solution**:
1. Test connectivity: `ping api.example.com`
2. Check firewall rules
```

### 4. Use Progressive Disclosure

Link to detailed content:
```markdown
## Quick Start

Basic workflow: [complete-workflow.md](references/complete-workflow.md)

## Configuration

All options: [configuration-reference.md](references/configuration-reference.md)

## Examples

- [Simple example](references/examples.md#simple)
- [Advanced patterns](references/examples.md#advanced)
```

## Reference Documentation

This skill uses progressive disclosure. For detailed information, see:

| Topic | Reference | Description |
|-------|-----------|-------------|
| **YAML Schema** | [specification.md](references/specification.md) | Detailed frontmatter fields, validation rules, file structure requirements |
| **Examples** | [examples.md](references/examples.md) | Complete skill examples for database migrations, AWS Lambda, Kubernetes, etc. |
| **Validation** | [validation.md](references/validation.md) | Using skills-ref tool, troubleshooting validation errors, CI/CD integration |
| **Best Practices** | [best-practices.md](references/best-practices.md) | Advanced patterns, cross-platform compatibility, performance optimization |
| **Template** | [skill-template.md](assets/skill-template.md) | Basic skill template to copy and customize |

## Common Workflows

### Workflow: Create New Skill

1. **Identify capability**: What problem does this solve?
2. **Create structure**: `mkdir my-skill && cd my-skill && touch SKILL.md`
3. **Write frontmatter**: Add required `name` and `description`
4. **Draft instructions**: Clear, step-by-step guidance
5. **Add examples**: Concrete, runnable examples
6. **Validate**: `skills-ref validate .`
7. **Test**: Use with AI agent and iterate
8. **Publish**: Add README, LICENSE, push to repository

### Workflow: Validate Existing Skill

1. **Run validator**: `skills-ref validate ./skill-directory`
2. **Fix errors**: Address validation failures (see [validation.md](references/validation.md))
3. **Check structure**: Verify SKILL.md exists and is readable
4. **Test references**: Ensure linked files exist
5. **Verify cross-platform**: Test with multiple AI tools

### Workflow: Refactor Large Skill

If SKILL.md exceeds 500 lines:

1. **Create directories**: `mkdir -p references assets`
2. **Extract content**:
   - Detailed docs → `references/`
   - Templates → `assets/`
   - Extended examples → `references/examples.md`
3. **Update links**: Use relative paths from skill root
4. **Keep in main skill**: Overview, quick start, common examples
5. **Validate**: Ensure skill still works after refactoring

## Cross-Platform Compatibility

Skills work across multiple AI tools. Key points:

- **Claude Code**: Discovers skills in `.claude/plugins/*/skills/`
- **Cursor**: Looks in `.cursor/skills/` directory
- **GitHub Copilot**: Configurable locations, check documentation

**Best Practices**:
- Use platform-agnostic language
- Avoid tool-specific assumptions
- Test with at least 2 different agents
- Follow the open standard for maximum compatibility

## Validation Reference

### Quick Validation

```bash
# Using uvx (no installation)
uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
  skills-ref validate path/to/skill

# Create alias for convenience
alias skills-ref='uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref'
```

### Common Validation Errors

| Error | Fix |
|-------|-----|
| Invalid name format | Use lowercase alphanumeric with hyphens only |
| Missing description | Add `description:` field to frontmatter |
| Description too long | Keep under 1024 characters, move details to body |
| Invalid YAML | Check indentation, quote special characters |
| Missing SKILL.md | Filename must be exactly `SKILL.md` (all caps) |

For detailed troubleshooting, see [validation.md](references/validation.md).

## Examples

### Minimal Valid Skill

```yaml
---
name: example-skill
description: Brief description of what this skill does and when to use it.
---

# Example Skill

Instructions for the agent go here in Markdown format.
```

### Production Skill Structure

```
aws-lambda-deploy/
├── SKILL.md                    # Main instructions (200 lines)
├── README.md                   # Human-readable overview
├── LICENSE                     # Apache-2.0
├── CHANGELOG.md                # Version history
├── scripts/
│   ├── deploy.py              # Main deployment script
│   ├── validate.py            # Configuration validator
│   └── test.py                # Integration tests
├── references/
│   ├── complete-workflow.md   # Detailed deployment steps
│   ├── configuration.md       # All configuration options
│   ├── examples.md            # Extended examples
│   └── troubleshooting.md     # Common issues and solutions
└── assets/
    ├── config-template.yaml   # Configuration template
    └── iam-policy.json        # IAM policy example
```

For complete examples, see [examples.md](references/examples.md).

## Best Practices Summary

- ✅ Keep SKILL.md under 500 lines
- ✅ Use clear, imperative language
- ✅ Provide concrete examples with expected outputs
- ✅ Handle common error cases
- ✅ Use progressive disclosure (main skill + references)
- ✅ Validate before publishing
- ✅ Test with multiple AI agents
- ✅ Include README and LICENSE
- ✅ Use semantic versioning

For advanced patterns, see [best-practices.md](references/best-practices.md).

## When to Use This Skill

Use this skill when you need to:

1. **Create a new skill** from scratch following the open standard
2. **Validate existing skills** for spec compliance
3. **Convert documentation** (runbooks, SOPs) into portable Agent Skills
4. **Ensure cross-platform compatibility** across Claude Code, Cursor, GitHub Copilot
5. **Understand best practices** for effective skill design
6. **Publish skills** to marketplaces or internal repositories
7. **Debug skill loading issues** in AI agent environments

## Resources

- **Official Site**: https://agentskills.io
- **Specification**: https://agentskills.io/specification
- **Reference Repo**: https://github.com/agentskills/agentskills
- **Validation Tool**: https://github.com/agentskills/agentskills/tree/main/skills-ref
- **Community**: https://github.com/agentskills/agentskills/discussions
- **Marketplace**: https://github.com/Agentic-Insights/claude-plugins-marketplace

## Summary

Agent Skills provide a standardized way to extend AI agent capabilities:

- ✅ **Open Standard** — Interoperable across platforms
- ✅ **Portable** — Write once, use everywhere
- ✅ **Validated** — Use skills-ref for compliance checking
- ✅ **Efficient** — Progressive disclosure minimizes context usage
- ✅ **Community-Driven** — Contributions welcome

Start simple and iterate based on real-world usage. The specification is flexible while maintaining cross-platform compatibility.
