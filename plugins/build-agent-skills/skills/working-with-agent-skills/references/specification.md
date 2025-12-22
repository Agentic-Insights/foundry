# Agent Skills Specification

This document provides detailed information about the Agent Skills YAML frontmatter schema, validation rules, and file structure requirements.

**Official Specification**: https://agentskills.io/specification

## YAML Frontmatter Schema

Every skill must include YAML frontmatter at the top of its `SKILL.md` file, delimited by triple dashes (`---`).

### Required Fields

#### `name`
- **Type**: String
- **Length**: 1-64 characters
- **Format**: Lowercase alphanumeric characters and hyphens only
- **Rules**:
  - No leading or trailing hyphens
  - No consecutive hyphens (`--`)
  - Must be unique within your skill collection
- **Examples**:
  - ✅ `pdf-processing`
  - ✅ `deploy-aws-lambda`
  - ✅ `security-audit`
  - ❌ `PDF_Processing` (uppercase)
  - ❌ `-my-skill` (leading hyphen)
  - ❌ `my--skill` (consecutive hyphens)

#### `description`
- **Type**: String
- **Length**: 1-1024 characters
- **Purpose**: Helps agents discover when to use the skill
- **Best Practices**:
  - Start with what the skill does
  - Include specific use cases after "Use when..."
  - Add relevant keywords for discoverability
  - Be specific about capabilities
- **Example**:
  ```yaml
  description: Extract text and tables from PDF files, fill forms, merge documents. Use when processing invoices, reports, or contracts.
  ```

### Optional Fields

#### `license`
- **Type**: String
- **Format**: SPDX license identifier or "Proprietary"
- **Common Values**: `Apache-2.0`, `MIT`, `BSD-3-Clause`, `GPL-3.0`, `Proprietary`
- **Purpose**: Clearly communicates usage rights
- **Example**:
  ```yaml
  license: Apache-2.0
  ```

#### `compatibility`
- **Type**: String
- **Length**: Maximum 500 characters
- **Purpose**: Describes environment requirements and prerequisites
- **Best Practices**:
  - List required software versions
  - Mention platform requirements (OS, architecture)
  - Specify credential/configuration needs
  - Keep concise but complete
- **Example**:
  ```yaml
  compatibility: Requires Python 3.10+, AWS CLI configured, Docker installed
  ```

#### `metadata`
- **Type**: Object (key-value pairs)
- **Purpose**: Extensible properties for custom information
- **No Length Limit**: But keep reasonable for context efficiency
- **Common Keys**:
  - `author`: Creator or organization name
  - `version`: Semantic version string (e.g., "1.2.0")
  - `category`: Classification tag
  - `tags`: Array of keywords
  - `dependencies`: Required libraries or tools
  - `difficulty`: Complexity level (beginner, intermediate, advanced)
  - `estimated-time`: Expected duration to complete
- **Example**:
  ```yaml
  metadata:
    author: agentic-insights
    version: "2.1.0"
    category: aws-deployment
    difficulty: intermediate
    estimated-time: 30min
    tags: [aws, bedrock, langgraph, deployment]
    dependencies: ["boto3>=1.26.0", "langchain>=0.1.0"]
  ```

#### `allowed-tools` (Experimental)
- **Type**: String
- **Format**: Space-delimited list of tool names
- **Purpose**: Pre-authorize specific command-line tools for agent use
- **Status**: Experimental feature, support varies by platform
- **Security Note**: Only list tools safe for automated execution
- **Example**:
  ```yaml
  allowed-tools: bash git docker kubectl aws
  ```

### Complete Schema Example

```yaml
---
name: aws-bedrock-deployment
description: Deploy LangGraph agents to AWS Bedrock AgentCore with memory, tools, and observability. Use when building production-ready AI agents on AWS with Claude models.
license: Apache-2.0
compatibility: Requires AWS CLI 2.x, Python 3.10+, valid AWS credentials with Bedrock access
metadata:
  author: agentic-insights
  version: "2.1.0"
  category: aws-deployment
  difficulty: intermediate
  estimated-time: 30min
  tags: [aws, bedrock, langgraph, deployment]
  dependencies: ["boto3>=1.26.0", "langchain>=0.1.0"]
allowed-tools: bash aws docker python
---

# AWS Bedrock Deployment Skill

[Markdown content follows...]
```

## File Structure Requirements

### Mandatory Structure

```
skill-name/
├── SKILL.md          # Required: Frontmatter + instructions
```

That's it! A valid skill only needs `SKILL.md` with proper frontmatter.

### Recommended Structure

```
skill-name/
├── SKILL.md          # Primary instructions
├── scripts/          # Executable scripts
│   ├── setup.sh
│   ├── deploy.py
│   └── validate.py
├── references/       # Supporting documentation
│   ├── api-reference.md
│   ├── troubleshooting.md
│   └── examples/
└── assets/           # Non-executable resources
    ├── templates/
    └── diagrams/
```

### Directory Purposes

#### `scripts/`
Executable scripts that agents can invoke directly:
- Shell scripts (`.sh`)
- Python scripts (`.py`)
- Any other executable files
- **Best Practice**: Make scripts idempotent and include `--help` flags

#### `references/`
Additional documentation loaded on-demand:
- Extended API documentation
- Architecture guides
- Detailed examples
- Troubleshooting guides
- **Best Practice**: Keep each file focused on a single topic

#### `assets/`
Non-executable resources:
- Configuration templates
- Diagrams and images
- Example data files
- Sample configurations
- **Best Practice**: Use descriptive subdirectories

## Validation Rules

Skills must pass these validation checks:

### Frontmatter Validation

1. **YAML Syntax**: Must be valid YAML
2. **Delimiter Format**: Must use `---` on separate lines
3. **Required Fields**: `name` and `description` must be present
4. **Field Types**: All fields must match expected types
5. **Field Lengths**: Must respect character limits
6. **Name Format**: Must match regex `^[a-z0-9]+(-[a-z0-9]+)*$`

### Content Validation

1. **Markdown After Frontmatter**: Content after `---` must be valid Markdown
2. **No Empty Skills**: Must have at least one heading or paragraph
3. **File Encoding**: Must be UTF-8 encoded

### File Structure Validation

1. **SKILL.md Present**: Must exist in skill directory
2. **Case Sensitive**: Filename must be exactly `SKILL.md` (all caps)
3. **File Permissions**: Must be readable

### Common Validation Errors

**Error**: `'name' field contains invalid characters`
- **Fix**: Use only lowercase letters, numbers, and hyphens
- **Example**: Change `My_Skill` to `my-skill`

**Error**: `'description' field is required`
- **Fix**: Add description field to frontmatter
- **Example**: `description: Brief description of what this skill does.`

**Error**: `'description' field exceeds 1024 characters`
- **Fix**: Shorten description, move details to skill body
- **Example**: Keep description focused on what and when

**Error**: `Invalid YAML syntax`
- **Fix**: Check for proper indentation and quoting
- **Example**: Quote strings containing special characters

## Progressive Disclosure Design

Skills should be designed for efficient context loading:

### Context Budget Strategy

1. **Metadata (~100 tokens)**
   - Name and description loaded at agent startup
   - Helps agent decide which skills to load
   - Keep description keyword-rich and concise

2. **Primary Instructions (<5000 tokens recommended)**
   - Full `SKILL.md` loaded when skill is activated
   - Should provide complete workflow
   - Keep under 500 lines for optimal loading

3. **Supporting Resources (on-demand)**
   - Referenced files loaded only when needed
   - Agent requests these explicitly
   - No practical size limit, but stay focused

### Refactoring Large Skills

If your `SKILL.md` exceeds 500 lines:

1. **Extract detailed content** to `references/`
2. **Move code templates** to `assets/templates/`
3. **Separate examples** to `references/examples/`
4. **Link from main skill** using relative paths

Example refactoring:

**Before** (800 lines in SKILL.md):
```
my-skill/
└── SKILL.md  # Contains everything
```

**After** (200 lines in SKILL.md):
```
my-skill/
├── SKILL.md            # Core workflow
├── references/
│   ├── api-docs.md     # Detailed API reference
│   └── examples.md     # Extended examples
└── assets/
    └── template.json   # Configuration template
```

## Platform-Specific Notes

### Claude Code
- Skills discovered automatically from `.claude/plugins/*/skills/`
- Frontmatter loaded during initialization
- Full skill loaded on first use

### Cursor
- Skills in `.cursor/skills/` directory
- Metadata cached for quick access
- Content loaded on-demand

### GitHub Copilot
- Skills in workspace `.github/skills/` or configured location
- Progressive loading based on context relevance

### Custom Implementations
The specification is intentionally flexible. Custom platforms may:
- Add platform-specific metadata keys
- Implement custom validation rules
- Support additional file types

Always test skills with your target platform(s).

## Schema Evolution

The Agent Skills specification evolves through community input:

- **Backward Compatibility**: New versions maintain compatibility with existing skills
- **Deprecation Policy**: Features deprecated with 6-month notice period
- **Extension Mechanism**: Custom fields allowed in `metadata` object
- **RFC Process**: Major changes go through public review

Track specification changes at: https://github.com/agentskills/agentskills

## Minimal Valid Skill

The absolute minimum for a valid skill:

```yaml
---
name: example-skill
description: Brief description of what this skill does and when to use it.
---

# Example Skill

Instructions for the agent go here in Markdown format.
```

This minimal skill:
- ✅ Passes validation
- ✅ Loads in all platforms
- ✅ Can be discovered by agents
- ✅ Provides basic functionality

From here, add optional fields and structure as needed.
