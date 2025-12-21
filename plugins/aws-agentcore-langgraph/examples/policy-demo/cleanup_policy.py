"""
AgentCore Policy Demo - Cleanup Script

Removes all resources created by setup_policy.py:
- Policy Engine and policies
- Gateway and targets
- Lambda function
- Cognito User Pool
"""

import json
import os
import sys

import boto3
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient
from bedrock_agentcore_starter_toolkit.operations.policy.client import PolicyClient


def cleanup():
    """Clean up all demo resources."""
    print("=" * 60)
    print("🧹 AgentCore Policy Demo - Cleanup")
    print("=" * 60)
    print()

    # Load configuration
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Error: config.json not found!")
        print("Nothing to clean up.")
        sys.exit(1)

    region = config["region"]

    # Step 1: Clean up Policy Engine
    print("Step 1: Cleaning up Policy Engine...")
    try:
        policy_client = PolicyClient(region_name=region)
        policy_client.cleanup_policy_engine(config["policy_engine_id"])
        print("✅ Policy Engine cleaned up\n")
    except Exception as e:
        print(f"⚠️  Policy Engine cleanup failed: {e}\n")

    # Step 2: Clean up Gateway
    print("Step 2: Cleaning up Gateway...")
    try:
        gateway_client = GatewayClient(region_name=region)
        gateway_client.cleanup_gateway(config["gateway_id"], config["client_info"])
        print("✅ Gateway cleaned up\n")
    except Exception as e:
        print(f"⚠️  Gateway cleanup failed: {e}\n")

    # Step 3: Clean up Lambda function
    print("Step 3: Cleaning up Lambda function...")
    try:
        lambda_client = boto3.client("lambda", region_name=region)
        lambda_arn = config.get("lambda_arn", "")
        if lambda_arn:
            function_name = lambda_arn.split(":")[-1]
            lambda_client.delete_function(FunctionName=function_name)
            print("✅ Lambda function cleaned up\n")
        else:
            print("⚠️  No Lambda ARN found in config\n")
    except Exception as e:
        print(f"⚠️  Lambda cleanup failed: {e}\n")

    # Step 4: Remove config file
    print("Step 4: Removing config file...")
    try:
        os.remove("config.json")
        print("✅ Config file removed\n")
    except Exception as e:
        print(f"⚠️  Config file removal failed: {e}\n")

    print("=" * 60)
    print("✅ Cleanup Complete!")
    print("=" * 60)


if __name__ == "__main__":
    cleanup()
