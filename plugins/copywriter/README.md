# Copywriter

Expert copywriting for UX, marketing, and product content.

## What This Skill Does

- **UX Writing** - Button labels, error messages, empty states, form fields, tooltips
- **Landing Pages** - Hero sections, feature descriptions, CTAs, social proof
- **Email Copy** - Welcome emails, transactional messages, campaigns
- **Microcopy** - Tooltips, confirmation dialogs, placeholder text, loading states

## Installation

```bash
claude plugin install agentic-insights/foundry --path plugins/copywriter
```

Or clone and install locally:

```bash
git clone https://github.com/agentic-insights/foundry
claude plugin install ./foundry/plugins/copywriter
```

## Usage

The skill activates when you ask about writing copy:

```
Write error messages for a signup form
```

```
Create hero section copy for a developer tool
```

```
Write a welcome email for new users
```

## Example Transformations

**Before (generic):**
```typescript
<Button>Submit</Button>
<Error>Invalid input</Error>
```

**After (specific, actionable):**
```typescript
<Button>Create Account</Button>
<Error>Please enter a valid email address</Error>
```

## Key Patterns

| Pattern | Formula |
|---------|---------|
| Error messages | What happened + How to fix it |
| Empty states | Headline + Explanation + Action |
| CTAs | Verb + Benefit + Remove friction |
| Hero copy | Benefit headline + How it works + CTA + Social proof |

## License

Apache-2.0
