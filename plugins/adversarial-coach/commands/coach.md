---
description: Adversarial code review - validates implementation against requirements with fresh context objectivity
argument-hint: [requirements-file]
---

# /coach - Adversarial Implementation Review

Validate the current implementation against requirements using an adversarial review approach from Block's g3 research.

## Arguments

- `requirements-file` (optional): Path to requirements document (e.g., `SPEC.md`, `requirements.md`)

## Your Task

### Step 1: Establish Requirements

**If a file is specified:**
- Read the specified requirements file

**If no file specified, search for:**
1. `requirements.md`, `REQUIREMENTS.md`
2. `SPEC.md`, `spec.md`
3. `TODO.md` with acceptance criteria
4. Recent conversation context about what should be built

**If nothing found:**
- Ask the user: "What requirements should I validate against?"

### Step 2: Perform Adversarial Review

You are now the **coach** - review with fresh objectivity. Discard any knowledge of implementation decisions or shortcuts.

**Systematic validation checklist:**

1. **Requirements Compliance**
   - Check each requirement item explicitly
   - Mark as ✅ implemented or ❌ missing/incomplete

2. **Build Verification**
   ```bash
   # For the appropriate language/framework:
   # Rust: cargo build && cargo test
   # Python: uv run pytest or python -m pytest
   # Node: npm run build && npm test
   # Go: go build && go test ./...
   ```

3. **Common Gaps to Check**
   - Authentication/authorization on all endpoints
   - HTTPS enforcement (if required)
   - Error handling for edge cases
   - Input validation at boundaries
   - Test coverage for error paths
   - Incomplete UI flows

4. **Functional Verification** (if applicable)
   - Test actual API endpoints
   - Verify UI flows work end-to-end
   - Check that features actually function, not just compile

### Step 3: Return Verdict

#### APPROVED (only if >95% complete):

```
IMPLEMENTATION_APPROVED

Validation summary:
- [Requirement 1]: ✅ Verified
- [Requirement 2]: ✅ Verified
- Build: ✅ Success
- Tests: ✅ Passing (N tests)
```

#### NEEDS WORK:

```
REQUIREMENTS COMPLIANCE:
- ✅ [Requirement]: Implemented correctly
- ❌ [Requirement]: [specific gap]

IMMEDIATE ACTIONS NEEDED:
1. [Specific, actionable fix]
2. [Specific, actionable fix]
3. [Specific, actionable fix]
```

## Key Rules

1. **Be rigorous but fair** - catch real gaps, not style preferences
2. **Be concise** - bullet points, no essays, no file dumps
3. **Be specific** - actionable fixes, not vague concerns
4. **Only approve when genuinely complete** - if in doubt, provide feedback
5. **The signal `IMPLEMENTATION_APPROVED` is sacred** - only use when truly done

## Example

```
User: /coach SPEC.md

Claude: [Reviews implementation against SPEC.md]

REQUIREMENTS COMPLIANCE:
- ✅ REST API with CRUD operations
- ✅ JWT authentication
- ❌ Rate limiting - not implemented
- ❌ API documentation - missing OpenAPI spec

IMMEDIATE ACTIONS NEEDED:
1. Add rate limiting middleware (requirement: 100 req/min per user)
2. Generate OpenAPI spec from route definitions
3. Add rate limit headers to responses
```

## Research Background

Based on Block's [Adversarial Cooperation in Code Synthesis](https://block.xyz/documents/adversarial-cooperation-in-code-synthesis.pdf) - the coach-player pattern that achieves 5/5 completeness vs 1-4/5 for single-agent approaches.
