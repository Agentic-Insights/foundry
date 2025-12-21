# AgentCore Policy Demo

Demonstrate AgentCore Policy for fine-grained, natural language authorization rules that auto-convert to Cedar policies.

> **Note:** AgentCore Policy is currently in **PREVIEW**. APIs may change. Free during preview period.

## What This Demo Shows

- **Natural language policy authoring** - Write rules in plain English
- **Cedar auto-conversion** - Automatic conversion to Cedar policy language
- **Gateway integration** - Policies enforce tool access in real-time
- **Default-deny semantics** - All actions denied unless explicitly permitted

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     LangGraph Agent                         │
│                           │                                 │
│                           ▼                                 │
│                    Tool Invocation                          │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   AgentCore Gateway                         │
│  ┌───────────────────────────────────────────────────────┐ │
│  │                   Policy Engine                        │ │
│  │  ┌─────────────────────────────────────────────────┐  │ │
│  │  │ Cedar Policy: permit(...) when { amount < 1000 }│  │ │
│  │  └─────────────────────────────────────────────────┘  │ │
│  │                         │                              │ │
│  │            ┌────────────┴────────────┐                │ │
│  │            ▼                         ▼                │ │
│  │      ✅ ALLOW                    ❌ DENY              │ │
│  │    (amount: $500)             (amount: $2000)         │ │
│  └───────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Prerequisites

- AWS account with Bedrock AgentCore access
- Python 3.10+
- AWS credentials configured

## Quick Start

```bash
# Install dependencies
uv sync

# Copy environment template
cp .env.example .env

# Run setup (creates Gateway + Policy Engine + Lambda)
uv run python setup_policy.py

# Test the policy enforcement
uv run python test_policy.py

# Clean up resources
uv run python cleanup_policy.py
```

## Example Policies

### Natural Language to Cedar Conversion

| Natural Language | Cedar Policy |
|-----------------|--------------|
| "Allow refunds up to $1000" | `permit(...) when { context.input.amount < 1000 }` |
| "Only support role can access customer data" | `permit(...) when { principal.getTag("role") == "support" }` |
| "Deny tool access outside business hours" | `forbid(...) when { context.hour < 9 \|\| context.hour > 17 }` |

### Cedar Policy Patterns

```cedar
# Pattern 1: Multi-action permit
permit(
   principal is AgentCore::OAuthUser,
   action in [
     AgentCore::Action::"API__get_policy",
     AgentCore::Action::"API__get_claim_status"
   ],
   resource == AgentCore::Gateway::"<gateway-arn>"
);

# Pattern 2: Role-based with exception
forbid(
   principal is AgentCore::OAuthUser,
   action == AgentCore::Action::"API__update_coverage",
   resource == AgentCore::Gateway::"<gateway-arn>"
) unless {
   principal.hasTag("role") &&
   principal.getTag("role") == "manager"
};

# Pattern 3: Input validation
permit(
   principal is AgentCore::OAuthUser,
   action == AgentCore::Action::"API__file_claim",
   resource == AgentCore::Gateway::"<gateway-arn>"
) when {
   context.input has claimType &&
   context.input.claimType == "auto"
};

# Pattern 4: Amount limits
permit(
   principal is AgentCore::OAuthUser,
   action == AgentCore::Action::"API__process_refund",
   resource == AgentCore::Gateway::"<gateway-arn>"
) when {
   context.input.amount < 1000
};
```

## How It Works

### 1. Policy Engine Creation

```python
import boto3

client = boto3.client('bedrock-agentcore-control')

# Create policy engine
response = client.create_policy_engine(
    name='RefundPolicyEngine',
    description='Policy engine for refund governance'
)
policy_engine_id = response['policyEngineId']
policy_engine_arn = response['policyEngineArn']
```

### 2. Add Cedar Policy

```python
# Create policy with Cedar statement
cedar_policy = '''
permit(principal,
    action == AgentCore::Action::"RefundTarget___process_refund",
    resource == AgentCore::Gateway::"<gateway-arn>")
when { context.input.amount < 1000 };
'''

client.create_policy(
    policyEngineId=policy_engine_id,
    name='refund_limit_policy',
    validationMode='FAIL_ON_ANY_FINDINGS',
    description='Allow refunds under $1000',
    definition={'cedar': {'statement': cedar_policy}}
)
```

### 3. Attach to Gateway

```python
# Associate policy engine with gateway in ENFORCE mode
gateway_client.update_gateway(
    gatewayId=gateway_id,
    policyEngineConfiguration={
        'mode': 'ENFORCE',  # or 'OBSERVE' for logging only
        'arn': policy_engine_arn
    }
)
```

## Policy Enforcement Modes

| Mode | Behavior |
|------|----------|
| `ENFORCE` | Block requests that violate policies |
| `OBSERVE` | Log violations but allow all requests |

## Cedar Language Quick Reference

| Operator | Usage |
|----------|-------|
| `in` | Multiple action checks |
| `like` | Wildcard pattern matching |
| `has` | Field existence validation |
| `hasTag()` / `getTag()` | Principal attribute access |
| `\|\|` (OR) | Multiple acceptable values |
| `&&` (AND) | Combined conditions |
| `unless` | Exception logic |
| `when` | Conditional permit/forbid |

## Authorization Semantics

- **Default Deny** - No explicit permit = denied
- **Forbid Wins** - Any matching forbid policy overrides permit policies
- **Policy Layering** - Multiple policies can apply; all permits must pass

## What Gets Created

| Resource | Purpose |
|----------|---------|
| Policy Engine | Container for Cedar policies |
| Cedar Policy | Authorization rules |
| Gateway (with policy) | Enforces policies on tool calls |
| Lambda Function | Mock refund tool for testing |
| Cognito User Pool | OAuth authentication |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| AccessDeniedException | Check IAM permissions for `bedrock-agentcore:*` |
| Gateway not responding | Wait 30-60s after creation for DNS propagation |
| Policy not enforcing | Verify mode is `ENFORCE`, not `OBSERVE` |

## Cleanup

```bash
uv run python cleanup_policy.py
```

## Region Availability

US East (Ohio, N. Virginia), US West (Oregon), Asia Pacific (Mumbai, Singapore, Sydney, Tokyo), Europe (Frankfurt, Ireland)

## References

- [AgentCore Policy Docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/policy.html)
- [Example Policies](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/example-policies.html)
- [Cedar Language](https://www.cedarpolicy.com/)
