# Contributing to Agentic Insights Plugin Marketplace

Thank you for your interest in contributing to the Agentic Insights Plugin Marketplace!

## Ways to Contribute

- **New Plugins** - Share plugins that encode reusable AI engineering patterns
- **Plugin Improvements** - Enhance existing plugins with better examples or documentation
- **Bug Reports** - Report issues with plugin functionality or documentation
- **Feature Requests** - Suggest new plugin ideas or improvements

## Plugin Submission Guidelines

### Before Submitting

1. Ensure your plugin solves a real problem encountered in production
2. Check that similar functionality doesn't already exist
3. Verify your plugin works with the latest Claude Code version
4. Test with multiple use cases

### Plugin Quality Standards

All plugins must meet these requirements:

**Documentation:**
- Clear README with purpose, installation, and usage examples
- Comprehensive SKILL.md for each skill
- Real-world usage examples
- Troubleshooting section

**Code Quality:**
- Follow existing plugin patterns (see superpowers for reference)
- Include proper error handling
- Add comments for complex logic
- Use descriptive variable/function names

**Testing:**
- Test all skills with real scenarios
- Verify examples work as documented
- Test error cases and edge conditions

**Licensing:**
- Use Apache-2.0 for corporate-friendly plugins
- Use MIT for general-purpose plugins
- Clearly state license in plugin README and LICENSE file

### Submission Process

1. **Fork the Repository**
   ```bash
   gh repo fork Agentic-Insights/claude-plugins-marketplace
   ```

2. **Create Plugin Directory**
   ```bash
   mkdir -p plugins/your-plugin-name
   cd plugins/your-plugin-name
   ```

3. **Add Plugin Structure**
   ```
   your-plugin-name/
   ├── .claude-plugin/
   │   └── plugin.json
   ├── README.md
   ├── CHANGELOG.md
   ├── LICENSE
   ├── skills/
   │   └── your-skill/
   │       └── SKILL.md
   └── examples/
   ```

4. **Create plugin.json**
   ```json
   {
     "name": "your-plugin-name",
     "version": "1.0.0",
     "description": "Clear, concise description of what your plugin does",
     "author": {
       "name": "Your Name"
     },
     "repository": "https://github.com/Agentic-Insights/claude-plugins-marketplace",
     "license": "Apache-2.0",
     "keywords": ["relevant", "tags", "here"]
   }
   ```

5. **Update Root README**
   Add your plugin to the "Available Plugins" section in the root README.md

6. **Commit with Conventional Commits**
   ```bash
   git add .
   git commit -m "feat(your-plugin): add initial plugin implementation"
   ```

7. **Submit Pull Request**
   - Provide clear description of what the plugin does
   - Explain the use case and value it provides
   - Link to any relevant documentation or examples
   - Note any dependencies or prerequisites

## Development Guidelines

### Conventional Commits

We use conventional commits for automated versioning:

- `feat(plugin-name): description` - New features (minor bump)
- `fix(plugin-name): description` - Bug fixes (patch bump)
- `docs(plugin-name): description` - Documentation only
- `chore(plugin-name): description` - Maintenance tasks

### Skill Structure

Follow this pattern for skills:

```markdown
---
name: skill-name
description: One-line description of what this skill does
---

# Skill Name

## Overview
What problem does this skill solve?

## When to Use
Specific scenarios where this skill should be invoked

## Usage
Step-by-step guide or examples

## Examples
Real-world usage patterns
```

### Documentation Style

- **Be concise** - Developers scan documentation, they don't read novels
- **Be practical** - Show real examples, not theoretical concepts
- **Be professional** - Remember this represents Agentic Insights consulting
- **Be complete** - Cover the happy path AND error cases

## Testing Your Plugin

Before submitting, test locally:

```bash
# Test skill invocation
/plugin marketplace add Agentic-Insights/claude-plugins-marketplace
/plugin install your-plugin-name@agentic-insights

# Verify skill appears
/help

# Test skill functionality
# (Follow usage examples from your SKILL.md)
```

## Code Review Process

1. **Automated Checks** - GitHub Actions will validate:
   - Plugin structure is valid
   - All required files exist
   - Links in documentation work

2. **Manual Review** - Maintainers will check:
   - Plugin quality and usefulness
   - Documentation clarity
   - Code follows best practices
   - Examples work as documented

3. **Feedback** - You may receive requests for changes:
   - Address all feedback
   - Update your PR
   - Request re-review

4. **Merge** - Once approved:
   - Your plugin will be merged
   - Semantic release will handle versioning
   - Plugin becomes available in marketplace

## Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create a GitHub Issue
- **Consulting**: Contact Agentic Insights at agenticinsights.com

## Community Guidelines

- **Be respectful** - Treat all contributors with respect
- **Be constructive** - Provide helpful feedback, not criticism
- **Be collaborative** - We're building this together
- **Be professional** - Remember this is a professional consulting brand

## License

By contributing, you agree that your contributions will be licensed under the same license as the plugin you're contributing to (Apache-2.0 or MIT as specified in the plugin's LICENSE file).

---

Thank you for helping make Claude Code more powerful for AI engineering! 🚀
