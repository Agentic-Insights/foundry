# Skills Validation Guide

## Installation

```bash
# Using uvx (recommended, no install needed)
uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref validate path/to/skill

# Shell alias
alias skills-ref='uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref'
```

## Commands

| Command | Purpose | Output |
|---------|---------|--------|
| `skills-ref validate ./skill` | Check structure/frontmatter | Pass/fail with errors |
| `skills-ref read-properties ./skill` | Extract metadata as JSON | Frontmatter fields |
| `skills-ref to-prompt ./skill` | Generate agent prompt XML | `<available_skills>` block |

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| Invalid name chars | Uppercase, underscores, special chars | Use `a-z`, `0-9`, `-` only |
| Missing required field | No `name` or `description` | Add to frontmatter |
| Description >1024 chars | Too long | Shorten, move detail to body |
| Invalid YAML | Bad indent, unquoted specials | Quote strings with `@#:`, use `"1.0"` for versions |
| SKILL.md not found | Wrong case or missing | Create `SKILL.md` (all caps) |

## Warnings

| Warning | Impact | Resolution |
|---------|--------|------------|
| No license field | Still valid | Add `license: Apache-2.0` |
| SKILL.md >500 lines | Context efficiency | Refactor to references/ |

## CI/CD Integration

```yaml
# GitHub Actions
- name: Validate skills
  run: |
    for skill in plugins/*/skills/*/; do
      uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref \
        skills-ref validate "$skill" || exit 1
    done
```

## Troubleshooting

| Issue | Check |
|-------|-------|
| Validates but won't load | File location, permissions, encoding (UTF-8) |
| Platform differences | Line endings (use LF), run `dos2unix` |
| Hangs on validate | File too large (>10MB), refactor |

## Resources

- Specification: https://agentskills.io/specification
- Examples: https://github.com/agentskills/agentskills/tree/main/skills
- Issues: https://github.com/agentskills/agentskills/issues
