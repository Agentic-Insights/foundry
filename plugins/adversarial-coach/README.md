# Adversarial Coach

**Version**: 0.1.0
**Status**: Beta
**Based on**: [Block AI Research - Adversarial Cooperation in Code Synthesis](https://block.xyz/documents/adversarial-cooperation-in-code-synthesis.pdf)

## Overview

An adversarial code review subagent that validates implementations against requirements with fresh context objectivity. Based on Block's g3 dialectical autocoding research, which demonstrates how a coach-player feedback loop significantly improves code quality by catching gaps that implementers miss.

## The Problem This Solves

> "Agents often elide instructions in longer prompts... The key insight in the adversarial dyad is to discard the implementing agent's self-report of success and have the coach perform an independent evaluation of compliance to requirements."

Studies show AI coding agents frequently declare success while gaps remain:
- Missing authentication enforcement
- Incomplete error handling
- Skipped HTTPS requirements
- Untested edge cases

The coach provides an **independent, adversarial review** from a fresh context.

## How It Works

```
┌─────────────────────────────────┐
│  YOU (or Claude) implements     │
│  a feature or fixes a bug       │
└──────────────┬──────────────────┘
               │
               ▼ invoke coach subagent
┌─────────────────────────────────┐
│  COACH (Fresh Context)          │
│  • Reviews against requirements │
│  • Tests compilation/execution  │
│  • Finds gaps and issues        │
│  • Returns actionable feedback  │
└──────────────┬──────────────────┘
               │
               ▼
  IMPLEMENTATION_APPROVED or specific fixes needed
```

The coach starts with a **clean context window** - it has no knowledge of the implementation process, decisions made, or shortcuts taken. This objectivity helps catch what the implementer missed.

## Installation

```bash
/plugin install adversarial-coach@agentic-insights
```

## Usage

### The `/coach` Command

```bash
/coach                    # Review current work, infer requirements from context
/coach requirements.md    # Validate against specific requirements file
/coach SPEC.md           # Validate against spec document
```

### Workflow

1. Implement your feature with Claude
2. Run `/coach` to get adversarial review
3. Address the feedback
4. Repeat until you get `IMPLEMENTATION_APPROVED`

```
┌─────────────────────────────────────────────────────────────────┐
│  COACH-PLAYER LOOP                                              │
├─────────────────────────────────────────────────────────────────┤
│  1. You implement features                                      │
│                    ↓                                            │
│  2. /coach performs adversarial review                          │
│                    ↓                                            │
│  3. IMPLEMENTATION_APPROVED? → Done!                            │
│     Specific fixes needed?   → Go to step 4                     │
│                    ↓                                            │
│  4. Address the feedback, loop to step 2                        │
└─────────────────────────────────────────────────────────────────┘
```

### Using the Coach Subagent Directly

You can also invoke the coach as a subagent:

```
User: "Use the coach subagent to validate my implementation"
User: "Have the coach review this against SPEC.md"
```

## Example Output

### Approval
```
IMPLEMENTATION_APPROVED

Validated:
- REST API endpoints: All 5 endpoints functional
- Authentication: JWT middleware on protected routes
- Database: Migrations and models complete
- Tests: 23 passing, 0 failing
```

### Needs Work
```
REQUIREMENTS COMPLIANCE:
- REST API endpoints: Implemented
- JWT authentication: MISSING on /api/health endpoint
- HTTPS enforcement: NOT IMPLEMENTED
- Error handling: Division by zero not caught

IMMEDIATE ACTIONS NEEDED:
1. Add auth middleware to health endpoint or document exemption
2. Add HTTPS redirect middleware
3. Handle division by zero in calculator service
4. Add tests for error cases
```

## Key Principles

1. **Fresh Context**: Coach reviews from blank slate - no implementation bias
2. **Requirements-Anchored**: Always validates against stated requirements
3. **Concise Feedback**: Bullet points, not essays
4. **Actionable**: Specific issues, not vague concerns
5. **Rigorous but Fair**: Catches real gaps, not style preferences

## Research Background

This plugin implements the coach role from Block's **dialectical autocoding** research:

- **Paper**: [Adversarial Cooperation in Code Synthesis](https://block.xyz/documents/adversarial-cooperation-in-code-synthesis.pdf)
- **Reference Implementation**: [g3](https://github.com/dhanji/g3)
- **Key Finding**: Coach-player adversarial loops achieve 5/5 completeness vs 1-4/5 for single-agent approaches

The g3 system uses:
- Separate coach and player agents with fresh contexts per turn
- Coach at `temperature=0.1` for consistency
- Explicit `IMPLEMENTATION_APPROVED` termination signal
- Requirements document as the source of truth

## Roadmap

- [ ] Multi-turn coach-player loop automation
- [ ] Integration with claude-code-sdk for non-interactive mode
- [ ] Specialized coaches (security, performance, accessibility)
- [ ] Requirements extraction from conversation context

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) in the marketplace root.

## License

Apache-2.0
