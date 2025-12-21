"""
AgentCore Policy Demo - Setup Script

Creates a Gateway with Policy Engine to demonstrate Cedar-based authorization.
The policy enforces a refund limit - allowing refunds under $1000 only.
"""

import json
import logging
import os
import time

import boto3
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
from bedrock_agentcore_starter_toolkit.operations.policy.client import PolicyClient
from bedrock_agentcore_starter_toolkit.utils.lambda_utils import create_lambda_function
from dotenv import load_dotenv

load_dotenv()

# Configuration
REGION = os.getenv("AWS_REGION", "us-west-2")
REFUND_LIMIT = int(os.getenv("REFUND_LIMIT", "1000"))


def setup_policy():
    """Setup Gateway with Policy Engine for refund authorization."""
    print("=" * 60)
    print("🛡️  AgentCore Policy Demo - Setup")
    print("=" * 60)
    print(f"Region: {REGION}")
    print(f"Refund Limit: ${REFUND_LIMIT}")
    print()

    # Initialize clients
    gateway_client = GatewayClient(region_name=REGION)
    gateway_client.logger.setLevel(logging.INFO)

    policy_client = PolicyClient(region_name=REGION)
    policy_client.logger.setLevel(logging.INFO)

    # Step 1: Create OAuth authorizer
    print("Step 1: Creating OAuth authorization server...")
    cognito_response = gateway_client.create_oauth_authorizer_with_cognito(
        "PolicyDemoGateway"
    )
    print("✅ Authorization server created\n")

    # Step 2: Create Gateway
    print("Step 2: Creating Gateway...")
    gateway = gateway_client.create_mcp_gateway(
        name=None,
        role_arn=None,
        authorizer_config=cognito_response["authorizer_config"],
        enable_semantic_search=False,
    )
    print(f"✅ Gateway created: {gateway['gatewayUrl']}\n")

    # Fix IAM permissions
    gateway_client.fix_iam_permissions(gateway)
    print("⏳ Waiting 30s for IAM propagation...")
    time.sleep(30)
    print("✅ IAM permissions configured\n")

    # Step 3: Create Lambda function with refund tool
    print("Step 3: Creating Lambda function with refund tool...")

    refund_lambda_code = '''
def lambda_handler(event, context):
    """Process a refund request."""
    amount = event.get("amount", 0)
    reason = event.get("reason", "Customer request")

    return {
        "status": "success",
        "message": f"Refund of ${amount} processed successfully",
        "amount": amount,
        "reason": reason,
        "transaction_id": f"REF-{context.aws_request_id[:8]}"
    }
'''

    session = boto3.Session(region_name=REGION)
    lambda_arn = create_lambda_function(
        session=session,
        logger=gateway_client.logger,
        function_name=f"RefundTool-{int(time.time())}",
        lambda_code=refund_lambda_code,
        runtime="python3.13",
        handler="lambda_function.lambda_handler",
        gateway_role_arn=gateway["roleArn"],
        description="Refund tool for Policy demo",
    )
    print("✅ Lambda function created\n")

    # Step 4: Add Lambda target with refund tool schema
    print("Step 4: Adding Lambda target with refund tool schema...")
    lambda_target = gateway_client.create_mcp_gateway_target(
        gateway=gateway,
        name="RefundAPI",
        target_type="lambda",
        target_payload={
            "lambdaArn": lambda_arn,
            "toolSchema": {
                "inlinePayload": [
                    {
                        "name": "process_refund",
                        "description": "Process a customer refund. Amount must comply with refund policies.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "amount": {
                                    "type": "integer",
                                    "description": "Refund amount in dollars",
                                },
                                "reason": {
                                    "type": "string",
                                    "description": "Reason for the refund",
                                },
                            },
                            "required": ["amount"],
                        },
                    }
                ]
            },
        },
        credentials=None,
    )
    print("✅ Lambda target added\n")

    # Step 5: Create Policy Engine
    print("Step 5: Creating Policy Engine...")
    engine = policy_client.create_or_get_policy_engine(
        name="RefundPolicyEngine", description="Policy engine for refund governance"
    )
    print(f"✅ Policy Engine: {engine['policyEngineId']}\n")

    # Step 6: Create Cedar policy
    print(f"Step 6: Creating Cedar policy (refund limit: ${REFUND_LIMIT})...")

    # Cedar policy: permit refunds under the limit
    cedar_statement = (
        f"permit(principal, "
        f'action == AgentCore::Action::"RefundAPI___process_refund", '
        f'resource == AgentCore::Gateway::"{gateway["gatewayArn"]}") '
        f"when {{ context.input.amount < {REFUND_LIMIT} }};"
    )

    print("\n📜 Cedar Policy:")
    print("-" * 40)
    print(cedar_statement)
    print("-" * 40 + "\n")

    policy = policy_client.create_or_get_policy(
        policy_engine_id=engine["policyEngineId"],
        name="refund_limit_policy",
        description=f"Allow refunds under ${REFUND_LIMIT}",
        definition={"cedar": {"statement": cedar_statement}},
    )
    print(f"✅ Policy created: {policy['policyId']}\n")

    # Step 7: Attach Policy Engine to Gateway in ENFORCE mode
    print("Step 7: Attaching Policy Engine to Gateway (ENFORCE mode)...")
    gateway_client.update_gateway_policy_engine(
        gateway_identifier=gateway["gatewayId"],
        policy_engine_arn=engine["policyEngineArn"],
        mode="ENFORCE",
    )
    print("✅ Policy Engine attached to Gateway\n")

    # Step 8: Save configuration
    config = {
        "gateway_url": gateway["gatewayUrl"],
        "gateway_id": gateway["gatewayId"],
        "gateway_arn": gateway["gatewayArn"],
        "policy_engine_id": engine["policyEngineId"],
        "policy_engine_arn": engine["policyEngineArn"],
        "policy_id": policy["policyId"],
        "region": REGION,
        "client_info": cognito_response["client_info"],
        "refund_limit": REFUND_LIMIT,
        "lambda_arn": lambda_arn,
    }

    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)

    print("=" * 60)
    print("✅ Setup Complete!")
    print("=" * 60)
    print()
    print(f"Gateway URL: {gateway['gatewayUrl']}")
    print(f"Policy Engine: {engine['policyEngineId']}")
    print(f"Refund Limit: ${REFUND_LIMIT}")
    print()
    print("Configuration saved to: config.json")
    print()
    print("Next steps:")
    print("  1. Run 'uv run python test_policy.py' to test policy enforcement")
    print("  2. Run 'uv run python cleanup_policy.py' when done")
    print("=" * 60)

    return config


if __name__ == "__main__":
    setup_policy()
