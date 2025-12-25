---
name: adversarial-coach
description: Adversarial implementation review based on Block's g3 dialectical autocoding research
---

# /coach - Adversarial Implementation Review

Invoke an adversarial coach to validate your implementation against requirements. Based on Block's g3 dialectical autocoding research.

## Usage

```
/coach [requirements-file]
```

**Examples:**
```
/coach                           # Coach reviews current work, infers requirements from context
/coach requirements.md           # Coach validates against specific requirements file
/coach SPEC.md                   # Coach validates against spec
```

## How This Works

You are the **orchestrator** of an adversarial coach-player loop:

```
┌─────────────────────────────────────────────────────────────────┐
│  COACH-PLAYER LOOP                                              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. You (player) implement features                             │
│                         ↓                                       │
│  2. /coach invokes adversarial review                           │
│                         ↓                                       │
│  3. Coach returns:                                              │
│     • IMPLEMENTATION_APPROVED → Done!                           │
│     • Specific fixes needed → Continue to step 4                │
│                         ↓                                       │
│  4. You address the feedback                                    │
│                         ↓                                       │
│  5. Loop back to step 2 until approved                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Your Task When /coach Is Invoked

### Step 1: Identify Requirements

First, establish what you're validating against:

1. If a requirements file is specified, read it
2. Otherwise, look for common requirement sources:
   - `requirements.md`, `REQUIREMENTS.md`
   - `SPEC.md`, `spec.md`
   - `TODO.md` with acceptance criteria
   - Recent conversation context about what should be built
3. If no requirements found, ask the user what they want validated

### Step 2: Perform Adversarial Review

Review the implementation with **fresh objectivity**. You are the coach now - discard any prior knowledge of implementation decisions or shortcuts.

**Check each of these systematically:**

1. **Requirements Compliance**
   - Go through each requirement item
   - Mark as ✅ implemented or ❌ missing/incomplete

2. **Compilation/Execution**
   - Does the code compile without errors?
   - Do tests pass?
   - Can the application actually run?

3. **Common Gaps** (things implementers often miss)
   - Authentication/authorization on all endpoints
   - HTTPS enforcement
   - Error handling for edge cases
   - Input validation
   - Missing tests for error paths
   - Incomplete UI flows

4. **Functional Verification**
   - If there's a UI, test the actual flows
   - If there's an API, test the endpoints
   - Verify the feature actually works, not just compiles

### Step 3: Return Your Verdict

#### If Implementation Is Complete (>95%):

```
IMPLEMENTATION_APPROVED

Summary of validation:
- [Requirement 1]: ✅ Verified
- [Requirement 2]: ✅ Verified
- Compilation: ✅ Success
- Tests: ✅ All passing
```

#### If Improvements Are Needed:

```
REQUIREMENTS COMPLIANCE:
- ✅ [Requirement]: Implemented correctly
- ❌ [Requirement]: Missing - [specific gap]

IMMEDIATE ACTIONS NEEDED:
1. [Specific, actionable fix]
2. [Specific, actionable fix]
3. [Specific, actionable fix]
```

## Key Principles

### Be Rigorous But Fair
- Catch real gaps, not style preferences
- Focus on functionality over aesthetics
- Security issues are always worth flagging

### Be Concise
- Bullet points, not essays
- Specific issues, not vague concerns
- No file contents in feedback
- No verbose analysis process

### Fresh Context Is Your Superpower
- Review as if you've never seen this code
- Don't rationalize shortcuts that were made
- Validate against requirements, not intentions

## The Magic Signal

The string `IMPLEMENTATION_APPROVED` is the termination signal. Only use it when:

- All requirements are genuinely met
- Code compiles and runs
- Tests pass
- No significant gaps remain

If in doubt, don't approve - provide specific feedback instead.

## Example Session

```
User: I just finished implementing the user auth feature. /coach SPEC.md

Claude: [Reads SPEC.md, reviews implementation]

REQUIREMENTS COMPLIANCE:
- ✅ User registration endpoint
- ✅ Login with JWT tokens
- ✅ Password hashing with bcrypt
- ❌ Logout endpoint - not implemented
- ❌ Token refresh - missing

IMMEDIATE ACTIONS NEEDED:
1. Add POST /auth/logout endpoint that invalidates tokens
2. Add POST /auth/refresh endpoint for token renewal
3. Add test coverage for auth error cases

---

User: [Implements the fixes] /coach SPEC.md

Claude: [Reviews again]

IMPLEMENTATION_APPROVED

All requirements verified:
- ✅ Registration, login, logout, refresh endpoints
- ✅ JWT token handling with proper expiry
- ✅ Password security with bcrypt
- ✅ 12 tests passing
```

## Research Background

This skill implements the coach role from Block's **dialectical autocoding** research:

- **Paper**: [Adversarial Cooperation in Code Synthesis](https://block.xyz/documents/adversarial-cooperation-in-code-synthesis.pdf)
- **Reference Implementation**: [g3](https://github.com/dhanji/g3)

Key insight: "Discard the implementing agent's self-report of success and perform an independent evaluation of compliance to requirements."
