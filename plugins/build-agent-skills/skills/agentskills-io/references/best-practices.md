# Agent Skills Best Practices

This guide covers advanced patterns, optimization techniques, and cross-platform compatibility strategies for creating robust Agent Skills.

## Writing Effective Skill Instructions

### 1. Use Clear, Imperative Language

Agents follow instructions literally. Be direct and unambiguous.

**❌ Avoid**:
```markdown
You might want to consider checking if the file exists before proceeding.
Perhaps try using the API endpoint to fetch data.
```

**✅ Better**:
```markdown
1. Check if the file exists: `test -f config.json`
2. If missing, create it: `touch config.json`
3. Fetch data from API: `curl https://api.example.com/data`
```

### 2. Provide Concrete Examples

Abstract instructions confuse agents. Show specific examples.

**❌ Avoid**:
```markdown
Deploy the application using appropriate configuration.
```

**✅ Better**:
```markdown
Deploy the application:

**Example 1: Development environment**
```bash
python scripts/deploy.py --env dev --region us-west-2
```

**Example 2: Production with custom domain**
```bash
python scripts/deploy.py --env prod --domain api.example.com --ssl-cert arn:aws:acm:...
```
```

### 3. Structure Instructions Hierarchically

Use headings to create scannable, navigable content:

```markdown
# Skill Name

Brief overview (2-3 sentences).

## Prerequisites

List requirements.

## Quick Start

Minimal example to get running fast.

## Complete Workflow

### Step 1: Preparation
Detailed first step.

### Step 2: Execution
Detailed second step.

### Step 3: Verification
How to confirm success.

## Advanced Usage

Optional advanced patterns.

## Troubleshooting

Common issues and solutions.
```

### 4. Anticipate Error Cases

Agents need guidance for when things go wrong.

**Include**:
- Common error messages and solutions
- Validation steps before destructive operations
- Recovery procedures
- Rollback instructions

**Example**:
```markdown
## Troubleshooting

**Error**: `Permission denied when writing to /var/log`
**Cause**: Insufficient filesystem permissions
**Solution**:
1. Check current permissions: `ls -la /var/log`
2. Add write permissions: `sudo chmod u+w /var/log/app.log`
3. Verify user ownership: `sudo chown $USER /var/log/app.log`

**Error**: `Connection timeout to database`
**Cause**: Network connectivity or firewall rules
**Solution**:
1. Test network connectivity: `ping db.example.com`
2. Check firewall rules: `sudo iptables -L`
3. Verify security group allows port 5432
4. Test connection: `psql -h db.example.com -U user -d database`
```

### 5. Use Progressive Disclosure

Keep main instructions concise, link to detailed resources.

**Main SKILL.md** (~200 lines):
```markdown
# Database Migration Skill

## Quick Start

Basic migration workflow: [detailed-workflow.md](references/detailed-workflow.md)

## Configuration

See [configuration-reference.md](references/configuration-reference.md) for all options.

## Examples

- [Simple migration](references/examples/simple.md)
- [Complex migration with data transformation](references/examples/complex.md)
- [Multi-database migration](references/examples/multi-db.md)
```

**references/detailed-workflow.md** (detailed, loaded on-demand)

### 6. Include Expected Outputs

Show agents what success looks like.

**Example**:
```markdown
### Step 3: Deploy Function

```bash
python scripts/deploy.py --function-name my-api
```

**Expected Output**:
```
Packaging dependencies... ✓
Creating deployment package... ✓
Uploading to AWS Lambda... ✓

Deployment successful!
Function ARN: arn:aws:lambda:us-east-1:123456789012:function:my-api
Version: $LATEST
Last Modified: 2024-01-15T10:30:00.000+0000
```

If you see errors instead, check [Troubleshooting](#troubleshooting).
```

## Progressive Disclosure Strategy

### Context Budget Optimization

Design skills for efficient context loading:

| Stage | Content | Token Budget | Loading |
|-------|---------|--------------|---------|
| **Discovery** | Name + Description | ~100 tokens | Agent startup |
| **Activation** | Full SKILL.md | <5000 tokens | When skill invoked |
| **Deep Dive** | Referenced files | Variable | On-demand |

### When to Split Content

**Keep in main SKILL.md**:
- Overview and prerequisites
- Step-by-step workflow
- Common examples (1-3)
- Critical troubleshooting

**Move to references/**:
- Detailed API documentation
- Extended examples (4+)
- Architecture explanations
- Advanced configuration options
- Historical context or background

### Refactoring Example

**Before** (800 lines in SKILL.md):
```
my-skill/
└── SKILL.md
    ├── Overview (50 lines)
    ├── Prerequisites (30 lines)
    ├── Complete Workflow (200 lines)
    ├── 10 Examples (300 lines)
    ├── API Reference (150 lines)
    └── Troubleshooting (70 lines)
```

**After** (200 lines in SKILL.md):
```
my-skill/
├── SKILL.md
│   ├── Overview (50 lines)
│   ├── Prerequisites (30 lines)
│   ├── Quick Start (50 lines)
│   ├── Links to 3 key examples (20 lines)
│   ├── Common troubleshooting (30 lines)
│   └── Links to references (20 lines)
├── references/
│   ├── complete-workflow.md (200 lines)
│   ├── api-reference.md (150 lines)
│   ├── examples.md (300 lines)
│   └── troubleshooting.md (70 lines)
└── assets/
    └── config-template.json
```

**Implementation**:
```markdown
# My Skill

Brief overview.

## Quick Start

1. Basic workflow steps
2. Link to [complete workflow](references/complete-workflow.md) for details

## Examples

- [Basic usage](references/examples.md#basic-usage)
- [Advanced patterns](references/examples.md#advanced-patterns)

## API Reference

See [complete API reference](references/api-reference.md).

## Troubleshooting

**Common Issue**: Brief solution
For more issues, see [troubleshooting guide](references/troubleshooting.md).
```

### Reference File Linking Best Practices

**✅ Do**:
- Use relative paths from skill root
- Keep references one level deep
- Use descriptive filenames
- Create table of contents in main skill

**❌ Avoid**:
- Absolute paths
- Circular references
- Deep nesting (file1 → file2 → file3)
- Generic names like `doc.md`

## Cross-Platform Compatibility

### Supported Platforms

Agent Skills work across:
- **Claude Code** (Anthropic)
- **Cursor**
- **GitHub Copilot**
- **VS Code** with extensions
- **OpenAI** integrations
- Custom agents (Letta, Goose, Amp, etc.)

### Platform-Specific Considerations

#### Claude Code

**Skill Discovery**:
- Looks in `.claude/plugins/*/skills/`
- Loads metadata at startup
- Full content loaded when skill activated

**Best Practices**:
- Use clear descriptions for discovery
- Test with `claude code` command
- Skills appear in `<available_skills>` block

#### Cursor

**Skill Discovery**:
- Looks in `.cursor/skills/`
- Can also load from workspace `.skills/` directories

**Best Practices**:
- Include clear `description` for Cursor's AI to understand when to use
- Test in Cursor's AI chat interface

#### GitHub Copilot

**Skill Discovery**:
- Configurable locations (`.github/skills/`, workspace root)
- May require explicit configuration

**Best Practices**:
- Check GitHub Copilot documentation for latest integration
- Skills may be referenced as "agents" in Copilot

### Writing Platform-Agnostic Skills

**Avoid Platform-Specific Language**:
```markdown
❌ "Ask Claude to run this command"
✅ "Run this command: `python script.py`"

❌ "Use Cursor's search feature to find..."
✅ "Search the codebase for files matching..."
```

**Avoid Tool-Specific Assumptions**:
```markdown
❌ "Use the Bash tool to execute..."
✅ "Execute the following command: `...`"
```

**Test Across Platforms**:
Before publishing, test your skill with at least 2 different agents:
- [ ] Claude Code
- [ ] Cursor
- [ ] GitHub Copilot
- [ ] Custom agent

## Skill Versioning

### Semantic Versioning

Use semantic versioning in metadata:

```yaml
metadata:
  version: "2.1.3"
  # MAJOR.MINOR.PATCH
  # - MAJOR: Breaking changes to skill interface
  # - MINOR: New features, backward compatible
  # - PATCH: Bug fixes, clarifications
```

### Breaking Changes

When making breaking changes:

1. **Document migration path**:
   ```markdown
   ## Migration from v1.x to v2.0

   **Breaking Changes**:
   - Configuration format changed from JSON to YAML
   - `deploy.py` now requires `--region` argument

   **Migration Steps**:
   1. Convert config: `python scripts/migrate-config.py config.json config.yaml`
   2. Update deploy commands to include `--region us-east-1`
   ```

2. **Maintain backward compatibility when possible**:
   ```python
   # Support both old and new config formats
   if config_file.endswith('.json'):
       warnings.warn("JSON config deprecated, use YAML")
       config = load_json(config_file)
   else:
       config = load_yaml(config_file)
   ```

3. **Update version appropriately**: `1.5.2` → `2.0.0`

## Security Best Practices

### 1. Avoid Hardcoded Secrets

**❌ Never**:
```yaml
metadata:
  api_key: sk-1234567890abcdef
  database_password: mysecretpassword
```

**✅ Instead**:
```markdown
## Configuration

Store sensitive values in environment variables:
- `API_KEY`: Your API key from provider dashboard
- `DB_PASSWORD`: Database password

Or use a secrets manager:
- AWS Secrets Manager
- HashiCorp Vault
- Environment-specific `.env` files (add to `.gitignore`)
```

### 2. Validate Inputs

Guide agents to validate before executing:

```markdown
## Step 1: Validate Configuration

Before deploying, validate the configuration:

```bash
python scripts/validate-config.py config.yaml
```

This checks:
- All required fields are present
- Values are properly formatted
- References to external resources exist
- No common security misconfigurations
```

### 3. Prefer Least Privilege

```markdown
## Prerequisites

### IAM Permissions (AWS)

Create a role with minimal required permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "lambda:CreateFunction",
        "lambda:UpdateFunctionCode"
      ],
      "Resource": "arn:aws:lambda:*:*:function:my-app-*"
    }
  ]
}
```

**Do not use**: Admin policies or overly broad permissions.
```

### 4. Document Audit Trails

```markdown
## Deployment Process

All deployments are logged to:
- CloudWatch Logs: `/aws/lambda/my-app`
- Deployment history: `deployments.log`
- S3 bucket: `s3://my-app-deployments/history/`

View recent deployments:
```bash
aws s3 ls s3://my-app-deployments/history/ | tail -n 10
```
```

## Performance Optimization

### 1. Minimize Context Size

**Strategies**:
- Keep SKILL.md under 500 lines
- Move examples to separate files
- Use code templates instead of inline code
- Link to external documentation

### 2. Optimize File References

**Efficient**:
```markdown
For detailed configuration options, see [config reference](references/config.md).
```

**Inefficient**:
```markdown
## Configuration Options

### Option 1: connection_timeout
[500 lines of detailed documentation...]

### Option 2: retry_strategy
[300 lines of detailed documentation...]
```

### 3. Cache Heavy Operations

Guide agents to cache expensive operations:

```markdown
## Step 1: Download Dependencies

```bash
# Cache dependencies to avoid repeated downloads
if [ ! -d ".cache/dependencies" ]; then
  wget https://example.com/large-file.tar.gz -O .cache/large-file.tar.gz
  tar -xzf .cache/large-file.tar.gz -C .cache/dependencies
fi
```

Use cached dependencies:
```bash
export DEPS_PATH=.cache/dependencies
python script.py --deps $DEPS_PATH
```
```

## Testing Skills

### Manual Testing Checklist

Before publishing a skill:

- [ ] **Validation**: `skills-ref validate` passes
- [ ] **Fresh environment**: Test in clean directory
- [ ] **Prerequisites**: Document all dependencies
- [ ] **Happy path**: Main workflow completes successfully
- [ ] **Error cases**: Common failures handled gracefully
- [ ] **Documentation**: Links work, examples run
- [ ] **Cross-platform**: Works on Linux, macOS, Windows (if applicable)
- [ ] **Multiple agents**: Test with 2+ AI tools

### Automated Testing

**Basic Test Script**:
```bash
#!/bin/bash
# test-skill.sh

set -e

echo "Testing skill: my-skill"

# 1. Validate structure
echo "Validating skill structure..."
skills-ref validate ./my-skill

# 2. Check file references
echo "Checking file references..."
for ref in $(grep -o 'references/[^)]*\.md' my-skill/SKILL.md); do
  if [ ! -f "my-skill/$ref" ]; then
    echo "Error: Referenced file not found: $ref"
    exit 1
  fi
done

# 3. Test scripts are executable
echo "Checking script permissions..."
for script in my-skill/scripts/*; do
  if [ ! -x "$script" ]; then
    echo "Error: Script not executable: $script"
    exit 1
  fi
done

echo "All tests passed!"
```

**CI/CD Integration**:
```yaml
# .github/workflows/test-skills.yml
name: Test Skills
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Validate skills
        run: |
          for skill in skills/*/; do
            uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
              skills-ref validate "$skill"
          done
      - name: Run skill tests
        run: |
          bash test-skills.sh
```

## Documentation Standards

### README.md

Every publishable skill should include a README for human readers:

```markdown
# Skill Name

Brief description (copy from frontmatter).

## Installation

For Claude Code:
```bash
claude plugin add https://github.com/org/skill-repo
```

For Cursor:
```bash
git clone https://github.com/org/skill-repo.git ~/.cursor/skills/
```

## Quick Start

[Minimal example]

## Documentation

Full documentation in [SKILL.md](SKILL.md).

## License

Apache-2.0
```

### CHANGELOG.md

Track changes between versions:

```markdown
# Changelog

## [2.1.0] - 2024-01-15

### Added
- Support for Python 3.11
- Automatic rollback on deployment failure

### Changed
- Improved error messages for validation failures
- Updated dependencies to latest versions

### Fixed
- Fixed issue with large file uploads timing out

## [2.0.0] - 2024-01-01

### Breaking Changes
- Configuration format changed from JSON to YAML

### Migration Guide
See [MIGRATION.md](MIGRATION.md)
```

### LICENSE

Always include a LICENSE file:

```
Apache-2.0   - Best for commercial/enterprise use
MIT          - Permissive, simple
BSD-3-Clause - Similar to MIT with attribution
GPL-3.0      - Copyleft, derivatives must be open-source
Proprietary  - For internal/private skills
```

## Advanced Patterns

### Skill Composition

Skills can reference other skills:

```markdown
# Deploy Full Stack Application

This skill orchestrates multiple deployment skills:

1. Deploy database: Use [postgres-migration](../postgres-migration/SKILL.md) skill
2. Deploy API: Use [deploy-lambda-function](../deploy-lambda-function/SKILL.md) skill
3. Deploy frontend: Use [deploy-cloudfront](../deploy-cloudfront/SKILL.md) skill

## Prerequisites

All referenced skills must be installed.
```

### Conditional Workflows

Guide agents through decision trees:

```markdown
## Deployment Strategy

### If deploying to production:
1. Run full test suite: `pytest tests/`
2. Create backup: `python scripts/backup.py`
3. Deploy with blue-green strategy: `python scripts/deploy.py --strategy blue-green`

### If deploying to staging:
1. Deploy directly: `python scripts/deploy.py --env staging`
2. Run smoke tests: `python scripts/smoke-test.py`

### If deploying to development:
1. Deploy with hot reload: `python scripts/deploy.py --env dev --watch`
```

### Parameterized Templates

Provide reusable templates:

```markdown
## Configuration Template

Use the template in [assets/config-template.yaml](assets/config-template.yaml):

```yaml
app_name: {{APP_NAME}}
region: {{AWS_REGION}}
memory: {{MEMORY_MB}}
timeout: {{TIMEOUT_SECONDS}}
```

Fill in values:
- `{{APP_NAME}}`: Your application name
- `{{AWS_REGION}}`: Target AWS region
- `{{MEMORY_MB}}`: Memory allocation (128-10240)
- `{{TIMEOUT_SECONDS}}`: Function timeout (1-900)
```

### Multi-Environment Support

```markdown
## Environment Configuration

This skill supports multiple environments. Copy and customize:

**Development** (`config.dev.yaml`):
- Verbose logging
- Hot reload enabled
- Mock external services

**Staging** (`config.staging.yaml`):
- Production-like configuration
- Real external services
- Reduced logging

**Production** (`config.prod.yaml`):
- Optimized for performance
- All features enabled
- Minimal logging

Deploy to specific environment:
```bash
python scripts/deploy.py --config config.prod.yaml
```
```

## Common Antipatterns

### ❌ Vague Instructions

```markdown
Deploy the application to the cloud.
```

Why: Agent doesn't know which cloud, how to deploy, what to deploy.

### ❌ Assuming Context

```markdown
Run the deploy script.
```

Why: Which script? Where is it? What arguments?

### ❌ Implicit Dependencies

```markdown
Run the command to start the server.
```

Why: What command? What prerequisites? What server?

### ❌ No Error Handling

```markdown
1. Deploy to AWS
2. Verify it works
```

Why: What if deployment fails? How to verify? How to rollback?

### ❌ Over-complicated First Example

```markdown
## Example

Deploy a microservices architecture with 15 services, service mesh, observability stack, and multi-region failover...
```

Why: Start simple. Advanced examples come later.

## Quality Checklist

Before publishing a skill, verify:

**Structure**:
- [ ] Valid frontmatter with required fields
- [ ] SKILL.md under 500 lines (or justified if longer)
- [ ] Clear directory structure
- [ ] All referenced files exist

**Content**:
- [ ] Clear, imperative instructions
- [ ] Prerequisites listed explicitly
- [ ] At least one concrete example
- [ ] Error handling documented
- [ ] Expected outputs shown

**Testing**:
- [ ] Validates with `skills-ref validate`
- [ ] Tested with at least one AI agent
- [ ] All examples run successfully
- [ ] Error cases handled gracefully

**Documentation**:
- [ ] README.md included
- [ ] LICENSE file included
- [ ] CHANGELOG.md for versioned skills
- [ ] All links work

**Cross-Platform**:
- [ ] Platform-agnostic language
- [ ] Works on major AI tools
- [ ] No tool-specific assumptions

## Resources

- **Specification**: https://agentskills.io/specification
- **Examples**: https://github.com/agentskills/agentskills/tree/main/skills
- **Community**: https://github.com/agentskills/agentskills/discussions
- **Validation Tool**: https://github.com/agentskills/agentskills/tree/main/skills-ref
