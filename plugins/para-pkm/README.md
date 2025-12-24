# PARA PKM Plugin

> Manage PARA-based personal knowledge management (PKM) systems - create, organize, and maintain Projects, Areas, Resources, and Archives knowledge bases with AI-friendly navigation.

## Overview

This plugin provides comprehensive tools for implementing and managing the **PARA method**, a proven organizational framework that structures information by actionability rather than topic.

PARA organizes everything into four categories:
- **Projects** = Time-bound goals with deadlines
- **Areas** = Ongoing responsibilities to maintain
- **Resources** = Reference material and topics of interest
- **Archives** = Inactive items from other categories

## What is PARA?

The PARA method, created by Tiago Forte, solves a fundamental problem with traditional organizational systems: mixing active work with reference material makes it hard to focus on what matters now.

**Traditional organization** groups by topic (work, personal, hobbies), mixing urgent tasks with archived notes.

**PARA organization** groups by actionability, so you instantly see what needs attention:

```
projects/     ← What needs attention NOW
areas/        ← What needs regular maintenance
resources/    ← What might be useful later
archives/     ← What's done
```

This plugin makes it easy to create, maintain, and navigate PARA knowledge bases, with special attention to AI agent integration.

## Installation

Install this plugin in Claude Code:

```bash
# Clone the marketplace repository
git clone https://github.com/Agentic-Insights/claude-plugins-marketplace.git

# Link the para-pkm plugin
cd claude-plugins-marketplace
claude-code plugins link plugins/para-pkm

# Verify installation
claude-code plugins list
```

## Skills Included

<details>
<summary><strong>📁 para-pkm</strong> - Complete PARA knowledge management toolkit</summary>

<br>

**Use this skill when**:
- Creating a new PARA knowledge base from scratch
- Organizing existing notes/files into PARA structure
- Deciding where content belongs (Projects vs Areas vs Resources vs Archives)
- Creating AI-friendly navigation files for efficient agent access
- Archiving completed projects
- Validating PARA structure for common anti-patterns
- Learning PARA organizational patterns for specific use cases

**Key features**:
- Decision guide for categorizing content
- Python scripts for initialization, validation, and archiving
- Templates for projects, areas, and navigation files
- Common patterns by role (developers, consultants, researchers, product builders)
- Anti-pattern detection
- AI navigation best practices

</details>

## Quick Start

### Creating Your First PARA Knowledge Base

```bash
# Use the initialization script
cd ~/projects/claude-plugins-marketplace/plugins/para-pkm
python skills/para-pkm/scripts/init_para_kb.py my-knowledge-base
```

This creates:

```
my-knowledge-base/
├── projects/
│   ├── active/
│   └── stories/
├── areas/
├── resources/
├── archives/
├── README.md
└── AGENTS.md        # AI-friendly navigation file
```

### Decision Guide: Where Does Content Belong?

Use this decision tree when organizing content:

```
Is it completed or inactive?
└─ YES → Archives
└─ NO ↓

Does it have a deadline or clear end state?
└─ YES → Projects
└─ NO ↓

Is it an ongoing responsibility to maintain?
└─ YES → Areas
└─ NO → Resources
```

**Examples**:

| Content | Category | Reasoning |
|---------|----------|-----------|
| "Launch product by Q2" | Projects | Has deadline |
| "Product development" (ongoing R&D) | Areas | Continuous responsibility |
| "React documentation" | Resources | Reference material |
| "Completed migration project" | Archives | Inactive |

## Common Use Cases

### 1. Software Developers

```
projects/active/          # Features, bugs, migrations
areas/
  ├── professional-development/
  └── open-source/
resources/
  ├── coding-standards/
  ├── platform-configs/
  └── library-preferences/
archives/                 # Completed features, old projects
```

### 2. Consultants

```
projects/active/          # Client deliverables
areas/consulting/
  ├── operations/         # Repeatable processes
  └── clients/            # Relationship management
resources/
  └── templates/          # Proposals, contracts
archives/                 # Completed engagements
```

### 3. Product Builders

```
projects/active/          # Feature launches
areas/product-development/
  ├── active/             # Shipping products
  ├── research/           # Experiments
  ├── graduated/          # Ready to ship
  └── legacy/             # Historical
resources/
  ├── market-research/
  └── competitor-analysis/
```

## Python Scripts

The plugin includes powerful automation scripts:

### init_para_kb.py

Create new PARA knowledge base with proper structure.

```bash
python scripts/init_para_kb.py <kb-name> [--path <directory>]
```

### validate_para.py

Validate PARA structure and detect common anti-patterns.

```bash
python scripts/validate_para.py [path]
```

Checks for:
- Required PARA folders exist
- Anti-patterns (inbox/, todo/ folders)
- Navigation files present
- Structural issues

### archive_project.py

Move completed projects to archives with metadata.

```bash
python scripts/archive_project.py <project-file> [--kb-path <path>]
```

Automatically:
- Adds archive metadata (date, original location)
- Moves to `archives/` with timestamp
- Removes from `projects/active/`

### generate_nav.py

Generate or update AI agent navigation index.

```bash
python scripts/generate_nav.py [--kb-path <path>] [--output <file>]
```

Creates efficient `AGENTS.md` file with:
- Current active context
- Path navigation (not file lists)
- Under 100 lines for minimal tokens

## Templates

Use templates as starting points:

- `assets/AGENTS.md.template` - AI navigation index
- `assets/project.md.template` - Project file structure
- `assets/area-overview.md.template` - Area overview format
- `assets/README.md.template` - Knowledge base README

Copy and customize:

```bash
cp assets/project.md.template projects/active/my-project.md
```

## AI Agent Integration

The plugin is designed for seamless AI agent navigation:

### AGENTS.md Best Practices

1. **Keep it minimal** - Under 100 lines, minimal tokens
2. **Point to paths** - Don't list all files, let agents use grep/glob
3. **Include active context** - What's currently being worked on
4. **Update regularly** - As projects/areas change

Example `AGENTS.md`:

```markdown
# AI Agent Navigation

## Current Focus
Working on: Feature X launch (projects/active/feature-x.md)

## Structure
- projects/active/ - Current work with deadlines
- areas/ - Ongoing responsibilities
- resources/ - Reference material
- archives/ - Completed/inactive items

## Recent Updates
- 2025-01-15: Archived Project Y
- 2025-01-10: Started Feature X
```

### Efficient Agent Queries

Agents can efficiently navigate PARA structure:

```bash
# Find all active projects
grep -r "status: active" projects/active/

# Find specific resource
glob "resources/**/*authentication*"

# Review recent archives
ls -lt archives/ | head -10
```

## Key Principles

### 1. Organize by Actionability, Not Topic

Traditional systems organize by subject (work, personal, hobbies), mixing active and inactive content.

PARA organizes by actionability, making it immediately clear what needs attention.

### 2. Content Flows Through Categories

Content naturally moves through PARA:

```
Resources → Projects → Archives
  (research)  (active work)  (completed)

Areas → Archives
  (ongoing)  (no longer responsible)

Projects ⟺ Areas
  (goal becomes ongoing or vice versa)
```

### 3. Keep Structure Flat

Avoid deep nesting:
- ✅ Max 2-3 levels
- ❌ Deep hierarchies (4+ levels)

Flat structures are easier to navigate and maintain.

### 4. Move Freely, Don't Overthink

Wrong location is better than no organization. Move items as understanding evolves.

## Anti-Patterns to Avoid

❌ **Inbox folder** - PARA doesn't need inbox. Capture directly into appropriate category.

❌ **Deep nesting** - Keep max 2-3 levels. Flat is better than nested.

❌ **Topic-based organization** - Don't split by "work" vs "personal". Split by actionability.

❌ **Perfectionism** - "Wrong" location is better than no organization.

❌ **Todo folders** - Tasks should live with their projects/areas, not separately.

❌ **Duplicated content** - One home per item. Use links to reference across categories.

## Reference Documentation

The skill includes comprehensive reference guides:

- `references/para-principles.md` - Complete PARA method explanation
- `references/decision-guide.md` - Detailed decision tree with examples
- `references/common-patterns.md` - Proven patterns for different roles
- `references/ai-navigation.md` - Best practices for AI-friendly navigation

## Tips for Success

1. **Start simple** - Begin with basic Projects/Areas/Resources/Archives
2. **Projects first** - Identify current work, put everything else in Resources temporarily
3. **Move freely** - Items naturally migrate between categories
4. **Review regularly** - Monthly review to archive and reassess
5. **One home per item** - Avoid duplicating content
6. **Keep it shallow** - Max 2-3 levels of nesting
7. **Let patterns emerge** - Structure becomes clear through use

## Troubleshooting

### "I can't decide if something is a Project or an Area"

Ask: **Does it have a clear end state?**

- Clear end state = Project
- Ongoing indefinitely = Area

Examples:
- "Get promoted" = Project (clear end)
- "Career development" = Area (ongoing)

### "My structure feels too complex"

Signs of over-organization:
- More than 3 levels of nesting
- Difficulty finding content
- Hesitation when filing new items

**Solution**: Flatten structure, combine similar categories, archive unused folders.

### "I have both project and relationship work with a client"

**Use both categories**:

```
projects/active/
  └── client-x-deliverable.md    # Technical work

areas/consulting/clients/
  └── client-x-relationship.md   # Relationship notes
```

Cross-reference between files.

## Resources

### PARA Method
- [Building a Second Brain](https://www.buildingasecondbrain.com/) - Tiago Forte's book
- [Forte Labs Blog](https://fortelabs.com/blog/) - Official PARA resources

### Community
- [GitHub Discussions](https://github.com/Agentic-Insights/claude-plugins-marketplace/discussions) - Ask questions, share patterns

## License

This plugin is licensed under the Apache License 2.0. See [LICENSE](LICENSE) for details.

## Author

Created by [Agentic Insights](https://agenticinsights.com) - AI engineering consulting.

Part of the [Claude Plugins Marketplace](https://github.com/Agentic-Insights/claude-plugins-marketplace).
