# Plugin Validation Scripts

Validation tools for Claude Code plugins in the marketplace.

## Quick Start

```bash
# Validate entire marketplace
./scripts/validate.sh

# Validate specific plugin
./scripts/validate.sh --plugin plugins/baml

# Fast mode (skip skills validation)
./scripts/validate.sh --skip-skills

# JSON output for CI/CD
./scripts/validate.sh --output json
```

## What It Validates

### plugin.json Schema
- ✅ JSON syntax validity
- ✅ Required fields (`name`)
- ✅ Field types (especially `author` must be object, not string)
- ✅ Naming conventions (kebab-case, lowercase)
- ✅ Semantic versioning (MAJOR.MINOR.PATCH)
- ✅ Path validation (relative, exists)
- ✅ SPDX license identifiers

### marketplace.json
- ✅ JSON syntax validity
- ✅ Required fields (`name`, `owner`, `plugins`)
- ✅ Plugin references exist
- ✅ Version consistency with plugin.json
- ✅ No duplicate plugin names
- ✅ Author field format

### Skills (via skills-ref)
- ✅ Integrates with [skills-ref](https://agentskills.io) tool
- ✅ Validates all skills in `skills/` directories
- ✅ Checks SKILL.md exists
- ✅ Reports Agent Skills compliance

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) for dependency management
- [skills-ref](https://agentskills.io) (installed via uvx automatically)

## CLI Options

```
--plugin PATH       Validate specific plugin directory
--skip-skills       Skip skills validation (faster)
--output {text|json} Output format (default: text with colors)
--verbose, -v       Show detailed validation steps
--no-color          Disable colored output for CI/CD
```

## Exit Codes

- `0` - All validations passed
- `1` - One or more validations failed

## CI/CD Integration

The validation runs automatically on:
- Pull requests affecting plugins/** or .claude-plugin/**
- Pushes to main branch
- Manual workflow dispatch

See `.github/workflows/validate.yml` for configuration.

## Common Issues

### Author Field Error
```
❌ Error: Author must be object with "name" field, not string
```

**Fix:** Change `"author": "name"` to `"author": {"name": "name"}`

### Path Validation Error
```
❌ Error: Path "skills/my-skill" does not exist
```

**Fix:** Ensure the path exists and uses `./` prefix: `"./skills/my-skill"`

### Version Mismatch
```
❌ Error: Plugin version mismatch: marketplace=2.1.0, plugin.json=1.0.2
```

**Fix:** Update marketplace.json to match actual plugin.json version

## Development

```bash
# Install dependencies
cd scripts
uv sync

# Run tests (when available)
uv run pytest

# Lint code
uv run ruff check validate.py
```

## Validation Rules

Based on [Claude Code plugin specification](https://docs.anthropic.com/claude-code/plugins):

1. **Plugin name**: kebab-case, lowercase, no spaces
2. **Author field**: MUST be object `{"name": "..."}`, NOT string
3. **Version**: Semantic versioning (MAJOR.MINOR.PATCH)
4. **Paths**: Relative, start with `./`, must exist
5. **Marketplace versions**: Must match plugin.json versions

## Files

- `validate.py` - Main validation script (Python)
- `validate.sh` - Bash wrapper for convenience
- `pyproject.toml` - Python dependencies
- `.github/workflows/validate.yml` - CI/CD workflow
