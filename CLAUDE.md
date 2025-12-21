# CLAUDE.md

This file provides guidance to Claude Code when working with the Agentic Insights Plugin Marketplace.

## Project Overview

A professional Claude Code plugin marketplace for Agentic Insights consulting. This repository contains production-ready plugins that serve three purposes:
1. **Lead generation** - Showcase AI engineering expertise to potential clients
2. **Client enablement** - Tools and patterns for post-engagement momentum
3. **Product-ized solutions** - Repeatable consulting patterns encoded as plugins

## Repository Structure

```
claude-plugins-marketplace/
├── plugins/
│   └── aws-agentcore-langgraph/    # Individual plugin directories
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── README.md
│       ├── CHANGELOG.md
│       ├── LICENSE
│       ├── skills/
│       ├── examples/
│       └── recordings/
├── README.md                        # Marketplace landing page
├── CLAUDE.md                        # This file
├── CONTRIBUTING.md                  # Contribution guidelines
└── .github/
    └── workflows/
        └── release.yml              # Semantic release automation
```

## Plugin Development Standards

### Quality Requirements

- All skills must have clear descriptions and use cases
- Follow superpowers plugin patterns for structure
- Include comprehensive README with examples
- Test skills with real scenarios before publishing
- Use conventional commits for semantic versioning

### Skill Structure

Each skill in a plugin should follow this pattern:

```
skills/
└── plugin-name/
    └── skill-name/
        ├── SKILL.md       # Complete documentation
        └── prompt.md      # Optional: additional context
```

### Plugin Metadata (plugin.json)

Each plugin must include:
- Accurate description (appears in marketplace)
- Relevant keywords for discoverability
- Repository URL (github.com/Agentic-Insights/claude-plugins-marketplace)
- Author: agentic-insights or killerapp
- Appropriate license (Apache-2.0 for corporate-friendly, MIT otherwise)

### Target Audience

Write documentation for three audiences:
1. **Potential clients** - Clear value proposition, professional tone
2. **Current/past clients** - Practical implementation guidance
3. **Development teams** - Technical details and integration patterns

## Development Workflow

### Adding New Plugins

1. Create plugin directory in `plugins/<plugin-name>/`
2. Add `.claude-plugin/plugin.json` with metadata
3. Create comprehensive README.md
4. Add skills, examples, documentation
5. Update root README.md with plugin listing
6. Test locally before pushing

### Versioning

- Use semantic versioning (MAJOR.MINOR.PATCH)
- Each plugin tracks its own version independently
- Marketplace infrastructure has separate versioning
- Automated releases via semantic-release on conventional commits

### Commit Messages

Follow conventional commits:
- `feat:` - New features (minor version bump)
- `fix:` - Bug fixes (patch version bump)
- `docs:` - Documentation (no version bump)
- `chore:` - Maintenance (no version bump)

Example:
```bash
git commit -m "feat(aws-agentcore): add memory persistence skill"
git commit -m "fix(aws-agentcore): correct CLI invocation pattern"
git commit -m "docs: update marketplace installation instructions"
```

## Plugin Lifecycle

1. **Alpha** - Private/client-specific, not in marketplace
2. **Beta** - In marketplace, marked as beta in description
3. **Stable** - Production-ready, documented, tested
4. **Deprecated** - Marked but still available

## Available Tools

Use these Claude Code skills when developing plugins:
- `plugin-dev:create-plugin` - Guided plugin creation
- `plugin-dev:skill-reviewer` - Quality review for skills
- `plugin-dev:plugin-validator` - Validate plugin structure
- `superpowers:writing-skills` - Create skills following best practices

## Skill Validation

### Agent Skills Open Standard

All skills in this repository follow the **[Agent Skills](https://agentskills.io)** open standard - an interoperable format for packaging AI agent capabilities supported by Claude Code, Cursor, GitHub Copilot, and more.

**For comprehensive guidance on creating and validating skills**, use the `build-agent-skills` plugin included in this marketplace:

```bash
# The build-agent-skills plugin provides:
# - Complete Agent Skills specification documentation
# - Validation workflow with skills-ref tool
# - Best practices for skill development
# - Cross-platform compatibility guidance
# - Real-world examples and templates
```

See [plugins/build-agent-skills/](plugins/build-agent-skills/) for complete documentation.

### Quick Validation

Validate any skill using `uvx`:

```bash
# Validate skill structure
uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
  skills-ref validate path/to/skill

# Convenience alias
alias skills-ref='uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref'
```

**Important**: Always validate skills before committing to ensure compliance with the [Agent Skills specification](https://agentskills.io/specification).

## Testing Locally

Before pushing changes:

1. **Validate skills** - Run `skills-ref validate` on all modified skills
2. Test plugin installation locally
3. Verify skill descriptions are clear
4. Run through examples in documentation
5. Check that all links work

## Git Workflow

- Work on feature branches
- Use conventional commits
- Push to GitHub
- Semantic release handles versioning automatically
- Tag releases for individual plugins as needed

## Brand Guidelines

- Professional, technical tone
- Focus on practical value and real-world usage
- Reference agenticinsights.com appropriately
- Highlight consulting expertise without overselling
