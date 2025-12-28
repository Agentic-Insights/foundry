# Copywriter

Expert copywriting for UX, marketing, and product content with Chain-of-Density summarization.

## Skills

| Skill | Purpose |
|-------|---------|
| `copywriter` | Write compelling UX copy, landing pages, emails, microcopy |
| `chain-of-density` | Iteratively compress verbose text while preserving meaning |

## Components

```
copywriter/
├── skills/
│   ├── copywriter/SKILL.md        # UX/marketing copy patterns
│   └── chain-of-density/
│       ├── SKILL.md               # Summarization orchestrator
│       └── scripts/text_metrics.py
└── agents/
    └── cod-iteration.md           # Single-iteration density worker
```

## Installation

```bash
claude plugin install agentic-insights/foundry --path plugins/copywriter
```

## Usage

### Copywriting

```
Write error messages for a signup form
```

```
Create hero section copy for a developer tool
```

### Chain-of-Density Summarization

```
Use chain-of-density to compress this 500-word description to 150 words
```

The CoD skill orchestrates the `cod-iteration` agent serially across 5 turns, each adding density while maintaining length.

## Copywriting Patterns

| Pattern | Formula |
|---------|---------|
| Error messages | What happened + How to fix it |
| Empty states | Headline + Explanation + Action |
| CTAs | Verb + Benefit + Remove friction |
| Hero copy | Benefit headline + How it works + CTA + Social proof |

## Chain-of-Density Flow

```
Turn 1: Base summary (establish length)
Turn 2: Add entity density (names, numbers, commands)
Turn 3: Add specificity (concrete examples)
Turn 4: Add context (why/when it matters)
Turn 5: Polish for nuance (resolve ambiguities)
```

## License

Apache-2.0
