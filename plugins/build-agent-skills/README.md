# Build Agent Skills Plugin

> Build skills with the [Agent Skills](https://agentskills.io) open standard - create, validate, and publish portable skills for AI agents across Claude Code, Cursor, GitHub Copilot, and more.

## Overview

This plugin provides comprehensive guidance for working with **Agent Skills**, the open standard for packaging AI agent capabilities as modular, portable, and reusable components.

Originally developed by Anthropic and released as an open standard, Agent Skills are now supported by major AI development tools and provide interoperability across platforms.

## What Are Agent Skills?

Agent Skills are folders of instructions, scripts, and resources that AI agents can discover and use to perform tasks more accurately and efficiently. They solve a fundamental problem: while AI agents are powerful, they often lack specialized context for reliable real-world work.

**Official Resources**:
- 🌐 **Official Site**: [agentskills.io](https://agentskills.io)
- 📖 **Specification**: [agentskills.io/specification](https://agentskills.io/specification)
- 🔧 **Reference Implementation**: [github.com/agentskills/agentskills](https://github.com/agentskills/agentskills)

## Supported Platforms

Skills work across multiple AI development tools:
- **Claude Code** and **Claude** (Anthropic)
- **Cursor**
- **GitHub Copilot**
- **VS Code**
- **OpenAI** integrations
- Multiple specialized agents (Letta, Goose, Amp, etc.)

## Installation

Install this plugin in Claude Code:

```bash
# Clone the marketplace repository
git clone https://github.com/Agentic-Insights/claude-plugins-marketplace.git

# Link the agent-skills plugin
# Link the build-agent-skills plugin
cd claude-plugins-marketplace
claude-code plugins link plugins/build-agent-skills

# Verify installation
claude-code plugins list
```

## Skills Included

### 1. `working-with-agent-skills`

Comprehensive guide for creating, validating, and publishing Agent Skills following the official specification.

**Use this skill when**:
- Creating new skills from scratch
- Validating existing skills for compliance
- Converting documentation into portable skills
- Ensuring cross-platform compatibility
- Understanding best practices for skill development
- Publishing skills to marketplaces

**Key topics covered**:
- Agent Skills specification deep dive
- YAML frontmatter schema (required and optional fields)
- Writing effective skill instructions
- Progressive disclosure strategy
- Validation with `skills-ref` tool
- Complete skill creation workflow
- Cross-platform compatibility testing
- Real-world examples (database migrations, AWS Lambda deployment)

## Quick Start: Creating Your First Skill

### 1. Create Skill Directory

```bash
mkdir -p my-first-skill
cd my-first-skill
```

### 2. Create SKILL.md

```yaml
---
name: my-first-skill
description: Brief description of what this skill does and when to use it.
license: Apache-2.0
metadata:
  author: your-name
  version: "1.0"
---

# My First Skill

## Instructions

1. First step...
2. Second step...
3. Third step...

## Example

Concrete example demonstrating the skill.
```

### 3. Validate

```bash
uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
  skills-ref validate .
```

### 4. Test with Agent

Load the skill in Claude Code, Cursor, or another compatible agent and test functionality.

## Validation

This plugin includes the complete validation workflow using the official `skills-ref` tool.

### Install Validation Tool

No installation needed with `uvx`:

```bash
# Create convenience alias (optional)
alias skills-ref='uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref'
```

### Validation Commands

```bash
# Validate skill structure
skills-ref validate path/to/skill

# Extract metadata as JSON
skills-ref read-properties path/to/skill

# Generate agent prompt format
skills-ref to-prompt path/to/skill
```

## Key Concepts

### File Structure

Every skill requires a `SKILL.md` file with YAML frontmatter and Markdown instructions:

```
skill-name/
├── SKILL.md          # Required: Frontmatter + instructions
├── scripts/          # Optional: Executable scripts
├── references/       # Optional: Supporting documentation
└── assets/           # Optional: Templates, diagrams, etc.
```

### Required Frontmatter Fields

```yaml
---
name: skill-name                    # 1-64 chars, lowercase alphanumeric with hyphens
description: What it does and when  # 1-1024 chars, keyword-rich
---
```

### Progressive Disclosure

Skills are designed for efficient context loading:

1. **Metadata** (~100 tokens): Name and description loaded at startup
2. **Instructions** (<5000 tokens): Full `SKILL.md` loaded when activated
3. **Resources** (on-demand): Referenced files loaded only when needed

## Examples

### Example 1: Simple Python Script Skill

```yaml
---
name: python-data-analysis
description: Analyze CSV data with pandas, generate summary statistics, and create visualizations. Use when exploring datasets or generating reports.
license: MIT
metadata:
  author: data-team
  version: "1.0"
---

# Python Data Analysis Skill

## Prerequisites

- Python 3.9+
- pandas, matplotlib installed

## Instructions

1. Load CSV file: `df = pd.read_csv('data.csv')`
2. Generate summary: `df.describe()`
3. Create visualization: `df.plot(kind='bar')`
4. Save report: `df.to_html('report.html')`

## Example

```python
import pandas as pd
df = pd.read_csv('sales.csv')
print(df.groupby('region')['revenue'].sum())
```
```

### Example 2: Infrastructure Deployment Skill

```yaml
---
name: deploy-aws-ecs
description: Deploy containerized applications to AWS ECS Fargate with load balancing and auto-scaling. Use when launching production services on AWS.
license: Apache-2.0
compatibility: Requires AWS CLI 2.x, Docker, valid AWS credentials
metadata:
  author: devops-team
  version: "2.0"
allowed-tools: bash aws docker
---

# AWS ECS Deployment Skill

[Detailed deployment instructions...]
```

## Use Cases

### 1. Domain Expertise Packaging

Convert specialized knowledge into reusable skills:
- Legal document processing workflows
- Compliance audit procedures
- Security incident response playbooks
- Data pipeline orchestration patterns

### 2. Team-Specific Capabilities

Create organization-specific skills:
- Internal API integration patterns
- Custom deployment workflows
- Company-specific coding standards
- Proprietary tool usage guides

### 3. Repeatable Workflows

Encode multi-step processes:
- Database migration procedures
- Infrastructure provisioning sequences
- Release management checklists
- Testing and validation protocols

## Contributing to the Standard

Agent Skills is an open standard with community governance:

- **Specification Repository**: [github.com/agentskills/agentskills](https://github.com/agentskills/agentskills)
- **Submit Issues**: Report bugs or suggest improvements
- **Pull Requests**: Contribute to the spec or reference implementation
- **Discussions**: Join the community in GitHub Discussions

## Best Practices

1. **Clear Descriptions**: Include keywords for agent discovery
2. **Step-by-Step Instructions**: Make instructions unambiguous and actionable
3. **Concrete Examples**: Demonstrate real use cases
4. **Error Handling**: Cover common failure modes
5. **Progressive Disclosure**: Keep primary SKILL.md under 500 lines
6. **Validation**: Always validate with `skills-ref` before publishing
7. **Testing**: Test with actual agents before releasing
8. **Documentation**: Include README.md and CHANGELOG.md

## Troubleshooting

### Skill Not Discovered

**Issue**: Agent doesn't see the skill

**Solutions**:
- Verify `SKILL.md` exists in correct location
- Check YAML frontmatter is valid
- Ensure `name` field follows naming convention
- Restart the agent to reload skills

### Validation Fails

**Issue**: `skills-ref validate` reports errors

**Solutions**:
- Check `name` field: lowercase alphanumeric with hyphens only
- Verify `description` is 1-1024 characters
- Ensure YAML frontmatter is properly formatted
- Check for trailing spaces or special characters

### Instructions Unclear to Agent

**Issue**: Agent misinterprets instructions

**Solutions**:
- Add concrete examples
- Break complex steps into smaller substeps
- Include expected outputs
- Add troubleshooting section
- Test with multiple agents

## Resources

### Official Documentation
- [Agent Skills Official Site](https://agentskills.io)
- [Complete Specification](https://agentskills.io/specification)
- [Reference Implementation](https://github.com/agentskills/agentskills)

### Tools
- [skills-ref Validator](https://github.com/agentskills/agentskills/tree/main/skills-ref)

### Community
- [GitHub Discussions](https://github.com/agentskills/agentskills/discussions)
- [Issue Tracker](https://github.com/agentskills/agentskills/issues)

## License

This plugin is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

Agent Skills is an open standard governed by the community at [github.com/agentskills/agentskills](https://github.com/agentskills/agentskills).

## Author

Created by [Agentic Insights](https://agenticinsights.com) - AI engineering consulting for production-ready systems.

Part of the [Claude Plugins Marketplace](https://github.com/Agentic-Insights/claude-plugins-marketplace).
