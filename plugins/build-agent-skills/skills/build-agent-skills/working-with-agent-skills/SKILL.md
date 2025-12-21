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

This skill guides you through creating, validating, and publishing **Agent Skills** — the open standard for packaging AI agent capabilities as portable, reusable modules.

## What Are Agent Skills?

**Agent Skills** are modular packages that extend AI agent capabilities. They are folders of instructions, scripts, and resources that agents can discover and use to perform tasks more accurately and efficiently.

Originally developed by Anthropic and released as an open standard, Agent Skills are now supported by major AI development tools including:
- **Claude Code** and **Claude** (Anthropic)
- **Cursor**
- **GitHub Copilot**
- **OpenAI** integrations
- **VS Code**
- Multiple specialized agents (Letta, Goose, Amp, etc.)

**Official Specification**: https://agentskills.io/specification
**Reference Implementation**: https://github.com/agentskills/agentskills

## Why Use Agent Skills?

Skills solve a fundamental problem: while AI agents are increasingly powerful, they often lack the specialized context needed for reliable real-world work. Skills bridge this gap by providing:

1. **Domain Expertise** — Package specialized knowledge (legal processes, data pipelines, security protocols) into reusable instructions
2. **New Capabilities** — Give agents abilities like presentation creation, dataset analysis, or infrastructure deployment
3. **Repeatable Workflows** — Convert multi-step tasks into consistent, auditable processes
4. **Interoperability** — Write once, use across multiple AI tools that support the standard
5. **Progressive Disclosure** — Load instructions efficiently, only when needed

## Agent Skills File Structure

Every skill must have a `SKILL.md` file with YAML frontmatter and Markdown content:

```
skill-name/
├── SKILL.md          # Required: Frontmatter + instructions
├── scripts/          # Optional: Executable scripts
├── references/       # Optional: Supporting documentation
└── assets/           # Optional: Images, templates, etc.
```

### Minimal Valid Skill

```yaml
---
name: example-skill
description: Brief description of what this skill does and when to use it.
---

# Example Skill

Instructions for the agent go here in Markdown format.
```

## YAML Frontmatter Schema

### Required Fields

- **`name`**: Skill identifier (1-64 characters, lowercase alphanumeric with hyphens)
  - No leading/trailing hyphens
  - No consecutive hyphens
  - Example: `pdf-processing`, `deploy-aws-lambda`, `security-audit`

- **`description`**: What the skill does and when to use it (1-1024 characters)
  - Include keywords for agent discovery
  - Describe use cases clearly
  - Example: "Extract text and tables from PDF files, fill forms, merge documents. Use when processing invoices, reports, or contracts."

### Optional Fields

- **`license`**: License designation (e.g., `Apache-2.0`, `MIT`, `Proprietary`)
- **`compatibility`**: Environment requirements (max 500 chars)
  - Example: "Requires Python 3.10+, AWS CLI configured, Docker installed"
- **`metadata`**: Key-value pairs for additional properties
  - Common: `author`, `version`, `tags`, `dependencies`
- **`allowed-tools`**: Space-delimited list of pre-approved tools (experimental)
  - Example: `allowed-tools: bash git docker kubectl`

### Complete Example

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
allowed-tools: bash aws docker python
---

# AWS Bedrock Deployment Skill

[Skill instructions continue here...]
```

## Writing Effective Skill Instructions

The Markdown content after frontmatter contains instructions for the agent. Follow these guidelines:

### 1. Clear Structure

Use headings to organize instructions logically:

```markdown
# Skill Name

Brief overview of what this skill accomplishes.

## Prerequisites

What needs to be in place before using this skill.

## Step-by-Step Instructions

1. First action...
2. Second action...
3. Third action...

## Expected Outputs

What the agent should produce.

## Error Handling

Common issues and how to resolve them.

## Examples

Concrete use cases demonstrating the skill.
```

### 2. Progressive Disclosure Strategy

Design skills for efficient context loading:

- **Metadata** (~100 tokens): Name and description loaded at agent startup
- **Primary Instructions** (<5000 tokens recommended): Full `SKILL.md` loaded when skill is activated
- **Supporting Resources** (on-demand): Referenced files loaded only when needed

Keep `SKILL.md` under 500 lines. Move detailed content to separate files in `references/`.

### 3. Reference External Files

Use relative paths from the skill root:

```markdown
## Detailed Configuration

For advanced configuration options, see [configuration guide](references/advanced-config.md).

## Code Templates

Use the starter template in [scripts/template.py](scripts/template.py).
```

**Best practice**: Keep references one level deep. Avoid nested chains (file1 → file2 → file3).

### 4. Concrete Examples

Include specific, actionable examples:

```markdown
## Example: Deploy a Customer Support Agent

**Input**:
- Agent definition in `agent.json`
- Environment: `production`
- AWS Region: `us-east-1`

**Steps**:
1. Validate agent configuration: `python scripts/validate.py agent.json`
2. Deploy to Bedrock: `aws bedrock create-agent --config agent.json --region us-east-1`
3. Test deployment: `python scripts/test-agent.py --endpoint <agent-arn>`

**Expected Output**:
```
Agent deployed successfully
ARN: arn:aws:bedrock:us-east-1:123456789012:agent/customer-support
Endpoint: https://bedrock-runtime.us-east-1.amazonaws.com
Status: ACTIVE
```
```

### 5. Edge Cases and Error Handling

Anticipate common failure modes:

```markdown
## Troubleshooting

**Issue**: "Permission denied" when deploying agent
**Solution**: Verify IAM role has `bedrock:CreateAgent` permission. Run: `aws iam get-role-policy --role-name MyRole --policy-name BedrockPolicy`

**Issue**: Agent fails to start after deployment
**Solution**: Check CloudWatch logs at `/aws/bedrock/agents/<agent-id>` for initialization errors.
```

## Validating Skills

Use the `skills-ref` reference implementation to validate skill structure before publishing.

### Installation

No installation needed with `uvx`:

```bash
# Validate a skill directory
uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref validate path/to/skill

# Create convenience alias (optional)
alias skills-ref='uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref'
```

### Validation Commands

**1. Validate Structure**

Checks frontmatter validity, naming conventions, and file structure:

```bash
skills-ref validate ./my-skill
```

**Output on success**:
```
Valid skill: ./my-skill
```

**Output on failure**:
```
Invalid skill: ./my-skill
- Error: 'name' field contains invalid characters (must be lowercase alphanumeric with hyphens)
- Error: 'description' field exceeds 1024 characters
- Warning: No 'license' field specified
```

**2. Read Properties**

Extract skill metadata as JSON:

```bash
skills-ref read-properties ./my-skill
```

**Output**:
```json
{
  "name": "aws-bedrock-deployment",
  "description": "Deploy LangGraph agents to AWS Bedrock AgentCore..."
}
```

**3. Generate Agent Prompt**

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
Deploy LangGraph agents to AWS Bedrock AgentCore with memory, tools, and observability...
</description>
<location>
/path/to/my-skill/SKILL.md
</location>
</skill>
</available_skills>
```

This format is used by Anthropic models and other agents to discover available skills.

## Workflow: Creating a New Skill

Follow this process to create a production-ready skill:

### 1. Identify the Capability

Define what the skill will do and when it should be used:

- What problem does it solve?
- What are the inputs and outputs?
- What tools or prerequisites are required?
- Who is the target user (developer, analyst, ops engineer)?

### 2. Create Directory Structure

```bash
mkdir -p my-skill-name
cd my-skill-name
touch SKILL.md
mkdir -p scripts references assets
```

### 3. Write YAML Frontmatter

Start with required fields, add optional as needed:

```yaml
---
name: my-skill-name
description: Clear, keyword-rich description of functionality and use cases.
license: Apache-2.0
metadata:
  author: your-org
  version: "1.0"
---
```

### 4. Draft Instructions

Write clear, step-by-step instructions in Markdown:

```markdown
# My Skill Name

Brief overview paragraph.

## Prerequisites

- Python 3.10+
- AWS CLI configured
- Docker installed

## Instructions

1. Clone the repository
2. Install dependencies
3. Configure environment
4. Run deployment script

## Examples

[Concrete example here]

## Troubleshooting

[Common issues here]
```

### 5. Validate

Check for spec compliance:

```bash
uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref validate .
```

Fix any errors, then validate again.

### 6. Test with Agent

Test the skill with an AI agent (Claude Code, Cursor, etc.):

1. Load the skill in your agent environment
2. Ask the agent to perform a task using the skill
3. Verify the agent follows instructions correctly
4. Refine based on observed behavior

### 7. Iterate

Based on testing:
- Clarify ambiguous instructions
- Add missing examples
- Document edge cases
- Improve error handling guidance

### 8. Publish

Once validated and tested:
- Add README.md with installation instructions
- Create CHANGELOG.md for version tracking
- Choose appropriate license (LICENSE file)
- Publish to GitHub or skill marketplace

## Advanced: Supporting Files

### scripts/

Executable scripts that agents can invoke:

```
scripts/
├── setup.sh              # Environment setup
├── deploy.py             # Main deployment script
├── validate.py           # Configuration validator
└── test-agent.py         # Integration testing
```

**Best Practice**: Make scripts idempotent and include `--help` flags.

### references/

Additional documentation loaded on-demand:

```
references/
├── api-reference.md      # API documentation
├── architecture.md       # System architecture
├── examples/             # Detailed examples
│   ├── basic.md
│   └── advanced.md
└── troubleshooting.md    # Extended troubleshooting
```

**Best Practice**: Keep each reference file focused on a single topic.

### assets/

Non-executable resources:

```
assets/
├── templates/            # Configuration templates
│   ├── agent-config.json
│   └── iam-policy.json
├── diagrams/             # Architecture diagrams
│   └── deployment-flow.png
└── examples/             # Example files
    └── sample-data.csv
```

## Cross-Platform Compatibility

Skills work across multiple AI tools. Test compatibility:

### Claude Code

```bash
# Skills discovered automatically from .claude/plugins/*/skills/
claude code
# Agent sees skill in <available_skills> block
```

### Cursor

```
# Add skill to .cursor/skills/ directory
# Cursor AI discovers skills at startup
```

### GitHub Copilot

```
# GitHub Copilot reads skills from workspace
# Skills appear in agent context when needed
```

### Testing Checklist

- [ ] Skill validates with `skills-ref validate`
- [ ] Description includes clear keywords for discovery
- [ ] Instructions are unambiguous and actionable
- [ ] Examples demonstrate concrete use cases
- [ ] Error handling covers common failure modes
- [ ] File references use relative paths (one level deep)
- [ ] Primary SKILL.md is under 500 lines
- [ ] Tested with at least one AI agent
- [ ] README.md explains installation and usage
- [ ] License file included

## Real-World Examples

### Example 1: Database Migration Skill

```yaml
---
name: postgres-migration
description: Create and run database migrations for PostgreSQL with rollback support. Use when adding tables, modifying schemas, or seeding data in PostgreSQL databases.
license: MIT
metadata:
  author: example-org
  version: "1.2.0"
---

# PostgreSQL Migration Skill

## Prerequisites

- PostgreSQL 14+ installed and running
- `psql` client available
- Database connection string in `DATABASE_URL` environment variable

## Instructions

### Creating a Migration

1. Generate migration file:
   ```bash
   python scripts/create-migration.py --name add_users_table
   ```

2. Edit generated file in `migrations/YYYYMMDD_HHMMSS_add_users_table.sql`

3. Write UP migration (changes to apply):
   ```sql
   -- UP
   CREATE TABLE users (
     id SERIAL PRIMARY KEY,
     email VARCHAR(255) UNIQUE NOT NULL,
     created_at TIMESTAMP DEFAULT NOW()
   );
   ```

4. Write DOWN migration (rollback):
   ```sql
   -- DOWN
   DROP TABLE IF EXISTS users;
   ```

### Running Migrations

Apply all pending migrations:
```bash
python scripts/migrate.py up
```

Rollback last migration:
```bash
python scripts/migrate.py down
```

### Expected Output

```
Running migrations...
✓ 20240101_120000_add_users_table.sql
✓ 20240102_140000_add_posts_table.sql
Applied 2 migrations successfully
```

## Troubleshooting

**Issue**: "Permission denied for database"
**Solution**: Grant necessary permissions: `GRANT ALL ON DATABASE mydb TO myuser;`

**Issue**: Migration fails partway through
**Solution**: Wrap DDL in transactions. Check `migrations/.applied` for state.
```

### Example 2: AWS Lambda Deployment Skill

```yaml
---
name: deploy-lambda-function
description: Package and deploy Python functions to AWS Lambda with dependencies, environment variables, and IAM roles. Use when creating serverless APIs, event processors, or scheduled tasks on AWS.
license: Apache-2.0
compatibility: Requires AWS CLI 2.x, Python 3.9+, valid AWS credentials
metadata:
  author: agentic-insights
  version: "1.0.0"
  category: aws-deployment
allowed-tools: bash aws zip python
---

# AWS Lambda Deployment Skill

[Instructions continue...]
```

## Skill Governance and Contributions

Agent Skills is an **open standard** governed by the community:

- **Specification Repository**: https://github.com/agentskills/agentskills
- **Discussions**: GitHub Issues and Discussions
- **Contributions Welcome**: Submit PRs to improve the spec or reference implementation

The standard remains open to ecosystem contributions while maintaining compatibility across platforms.

## Resources

- **Official Site**: https://agentskills.io
- **Specification**: https://agentskills.io/specification
- **Reference Repo**: https://github.com/agentskills/agentskills
- **Validation Tool**: https://github.com/agentskills/agentskills/tree/main/skills-ref
- **Community Examples**: Check the agentskills GitHub for community-contributed skills

## When to Use This Skill

Use this skill when you need to:

1. **Create a new skill** from scratch following the open standard
2. **Validate existing skills** for compliance with the specification
3. **Convert documentation** (runbooks, SOPs) into portable Agent Skills
4. **Ensure cross-platform compatibility** with Claude Code, Cursor, GitHub Copilot, etc.
5. **Understand best practices** for writing effective, discoverable skills
6. **Publish skills** to marketplaces or internal repositories
7. **Debug skill loading issues** in AI agent environments

## Summary

Agent Skills provide a standardized way to extend AI agent capabilities:

- ✅ **Open Standard** — Interoperable across platforms
- ✅ **Portable** — Write once, use everywhere
- ✅ **Validated** — Use skills-ref for compliance checking
- ✅ **Efficient** — Progressive disclosure minimizes context usage
- ✅ **Community-Driven** — Contributions welcome at https://github.com/agentskills/agentskills

Start by creating simple skills and iterate based on real-world usage. The specification is designed to be flexible while maintaining cross-platform compatibility.
