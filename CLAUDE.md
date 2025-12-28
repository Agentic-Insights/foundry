# CLAUDE.md - Terse Marketplace Guidance

Guidance for Claude Code when working with the Agentic Insights Plugin Marketplace.

## Repository Structure

```
plugins/
├── <plugin-name>/
│   ├── .claude-plugin/plugin.json
│   ├── README.md
│   ├── CHANGELOG.md
│   ├── LICENSE (Apache-2.0)
│   ├── skills/
│   │   └── <skill-name>/SKILL.md (+ references/, assets/, scripts/)
│   ├── agents/
│   │   └── <subagent-name>.md
│   ├── examples/
│   └── recordings/
```

## Plugin Purpose

- **Lead generation** - Showcase AI engineering expertise
- **Client enablement** - Post-engagement momentum patterns
- **Product-ized solutions** - Repeatable consulting encoded as skills

## Skill Structure (Agent Skills Spec)

- **Required**: `SKILL.md` with YAML frontmatter (name, description) + Markdown instructions
- **Optional dirs**: `scripts/` (executable code), `references/` (detailed docs), `assets/` (static files)
- **No other subdirectories allowed**
- Keep SKILL.md under 500 lines (use progressive disclosure)
- Directory name MUST match frontmatter `name:` field

## Frontmatter Fields

- **Required**: `name` (1-64 chars, lowercase alphanumeric-hyphens), `description` (1-1024 chars, include "Use when...")
- **Optional**: `license` (SPDX), `compatibility` (environment reqs), `metadata` (author, version, tags), `allowed-tools` (space-delimited)

## Skill Writing Patterns

### Terse (Preferred for Action Skills)
- Bullet points, no prose
- "Do this", "Then this"
- Concrete examples only
- Reference detailed docs via links
- ~50-100 lines typical

### Comprehensive (For Teaching/Reference)
- Can exceed 500 lines if justified
- Multiple sections with explanations
- Extensive examples embedded
- Use for: tutorials, API docs, specifications

See `assets/` subdirectory for style examples.

## Quality Checklist

- [ ] Validate with `skills-ref validate path/to/skill`
- [ ] SKILL.md exists with valid frontmatter
- [ ] Description includes "Use when..."
- [ ] Examples are runnable/concrete
- [ ] No hardcoded paths (use relative paths)
- [ ] Progressive disclosure applied (refs → references/, assets/)
- [ ] Cross-platform compatible (test with multiple agents)
- [ ] Licensed under Apache-2.0
- [ ] Plugin has README.md with installation instructions

## Versioning

- Semantic versioning per plugin: MAJOR.MINOR.PATCH
- Auto-detect and bump only changed plugins: `bash scripts/bump-changed-plugins.sh`
- Or manually: `just bump-plugin <name> patch|minor|major`

## Commit Format

```
feat(plugin-name): Add feature description
fix(plugin-name): Fix bug description
docs: Update documentation
chore: Maintenance
```

## Git Workflow

1. Create feature branch: `git checkout -b feature/description`
2. Make changes + validate skills
3. Commit with conventional messages
4. Push feature branch
5. Semantic release auto-handles tags/versions
6. Plugins marked by marketplace.json

## Tools & Validation

- **skills-ref** - Validates Agent Skills spec: `uvx --from git+https://github.com/agentskills/agentskills#subdirectory=skills-ref skills-ref validate <path>`
- **Justfile** - Version management: `just bump`, `just validate <plugin>`, `just versions`, `just lint`
- **Linter** - Marketplace compliance: `uv run scripts/marketplace-linter.py` or `just lint`

## Brand & Tone

- Professional, technical, consulting-focused
- Real-world value over hype
- Highlight expertise, not features
- Target: practitioners, CTOs, engineering leaders
- Avoid: buzzwords, generic marketing, vague descriptions

## Key References

- Agent Skills spec: https://agentskills.io/specification
- Official validator: https://github.com/agentskills/agentskills
- Marketplace plugins: [plugins/](plugins/) directory
- Examples: See `build-agent-skills` plugin for teaching-skill patterns
