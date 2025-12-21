# AgentCore CLI Reference

Quick reference for AgentCore primitives. Use `scripts/` utilities for common discovery tasks.

## Primitives Overview

| Primitive | Purpose | agentcore CLI | AWS CLI |
|-----------|---------|---------------|---------|
| **Runtime** | Deploy/manage agents | `agentcore status/deploy/invoke` | `list-agent-runtimes` |
| **Memory** | STM/LTM persistence | `agentcore memory` | `list-memories` |
| **Gateway** | API→MCP tools | `agentcore gateway` | `list-gateways` |
| **Identity** | OAuth/credentials | `agentcore identity` | `list-workload-identities` |
| **Code Interpreter** | Sandboxed code execution | - | `list-code-interpreters` |
| **Browser** | Web browsing capability | - | `list-browsers` |
| **Observability** | Traces/logs | `agentcore obs` | CloudWatch |
| **Policy** | Guardrails (preview) | - | `list-policies` |
| **Evaluator** | Quality metrics (preview) | - | `list-evaluators` |

## agentcore CLI

### Runtime
```bash
agentcore status                    # Current agent status
agentcore deploy                    # Deploy (CodeBuild, recommended)
agentcore deploy --local            # Local dev server
agentcore invoke '{"prompt":"Hi"}'  # Test invocation
agentcore destroy                   # Cleanup all resources
agentcore dev                       # Hot-reload dev server
```

### Memory
```bash
agentcore memory list               # List all memories
agentcore memory create NAME        # Create new memory
agentcore memory get --memory-id ID # Get memory details
agentcore memory delete --memory-id ID
```

### Gateway
```bash
agentcore gateway list              # List gateways
agentcore gateway create NAME       # Create gateway
agentcore gateway target list       # List targets
```

### Identity
```bash
agentcore identity list             # List credential providers
agentcore identity create NAME      # Create provider
```

### Observability
```bash
agentcore obs traces                # View recent traces
agentcore obs logs                  # View logs
agentcore obs spans                 # View spans
```

## AWS CLI (bedrock-agentcore-control)

### List All Resources
```bash
# Runtimes (agents)
aws bedrock-agentcore-control list-agent-runtimes --region us-east-1

# Memory
aws bedrock-agentcore-control list-memories --region us-east-1

# Gateway
aws bedrock-agentcore-control list-gateways --region us-east-1
aws bedrock-agentcore-control list-gateway-targets --gateway-id GW_ID --region us-east-1

# Identity
aws bedrock-agentcore-control list-workload-identities --region us-east-1
aws bedrock-agentcore-control list-api-key-credential-providers --region us-east-1
aws bedrock-agentcore-control list-oauth2-credential-providers --region us-east-1

# Policy (preview)
aws bedrock-agentcore-control list-policies --region us-east-1
aws bedrock-agentcore-control list-policy-engines --region us-east-1

# Evaluators (preview)
aws bedrock-agentcore-control list-evaluators --region us-east-1
aws bedrock-agentcore-control list-online-evaluation-configs --region us-east-1

# Other
aws bedrock-agentcore-control list-browsers --region us-east-1
aws bedrock-agentcore-control list-code-interpreters --region us-east-1
```

### Get Resource Details
```bash
aws bedrock-agentcore-control get-agent-runtime --agent-runtime-id ID --region us-east-1
aws bedrock-agentcore-control get-memory --memory-id ID --region us-east-1
aws bedrock-agentcore-control get-gateway --gateway-id ID --region us-east-1
aws bedrock-agentcore-control get-policy --policy-id ID --region us-east-1
```

### CloudWatch Logs
```bash
# Runtime logs
aws logs tail /aws/bedrock-agentcore/runtimes/AGENT_ID-DEFAULT \
  --log-stream-name-prefix "$(date +%Y/%m/%d)/[runtime-logs]" \
  --region us-east-1 --since 1h

# Memory logs
aws logs tail /aws/vendedlogs/bedrock-agentcore/memory/APPLICATION_LOGS/MEMORY_ID \
  --region us-east-1 --since 1h
```

## Environment Variables

Auto-injected by toolkit during `agentcore launch`:
- `BEDROCK_AGENTCORE_MEMORY_ID` - Memory resource ID
- `BEDROCK_AGENTCORE_MEMORY_NAME` - Memory name
- `AWS_REGION` - Deployment region

Pass custom env vars:
```bash
agentcore launch --env GUARDRAIL_ID="xyz" --env KB_ID="abc"
```

## Quick Discovery Scripts

See `scripts/` directory:
- `list-all.sh` - List all AgentCore resources in region
- `agent-status.sh` - Detailed status of current agent
- `tail-logs.sh` - Stream runtime logs

## Documentation

| Resource | URL |
|----------|-----|
| CLI Reference | https://aws.github.io/bedrock-agentcore-starter-toolkit/api-reference/cli.html |
| AWS CLI bedrock-agentcore-control | https://awscli.amazonaws.com/v2/documentation/api/latest/reference/bedrock-agentcore-control/index.html |
