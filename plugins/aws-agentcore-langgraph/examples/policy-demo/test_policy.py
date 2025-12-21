"""
AgentCore Policy Demo - Test Script

Tests the Policy Engine by making requests that should be:
1. ALLOWED - Refund under the limit
2. DENIED - Refund over the limit
"""

import json
import sys

import requests
from bedrock_agentcore_starter_toolkit.operations.gateway.client import GatewayClient


def test_refund(gateway_url: str, bearer_token: str, amount: int, reason: str = "Test"):
    """Test a refund request against the policy engine."""
    response = requests.post(
        gateway_url,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {bearer_token}",
        },
        json={
            "jsonrpc": "2.0",
            "id": 1,
            "method": "tools/call",
            "params": {
                "name": "RefundAPI___process_refund",
                "arguments": {"amount": amount, "reason": reason},
            },
        },
        timeout=30,
    )

    return response.status_code, response.json()


def main():
    print("=" * 60)
    print("🧪 AgentCore Policy Demo - Test")
    print("=" * 60)
    print()

    # Load configuration
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
    except FileNotFoundError:
        print("❌ Error: config.json not found!")
        print("Please run 'uv run python setup_policy.py' first.")
        sys.exit(1)

    gateway_url = config["gateway_url"]
    refund_limit = config["refund_limit"]

    print(f"Gateway: {gateway_url}")
    print(f"Refund Limit: ${refund_limit}")
    print()

    # Get access token
    print("🔑 Obtaining access token...")
    gateway_client = GatewayClient(region_name=config["region"])
    token = gateway_client.get_access_token_for_cognito(config["client_info"])
    print("✅ Token obtained\n")

    # Test cases
    test_cases = [
        {
            "name": "Small Refund (Should ALLOW)",
            "amount": 500,
            "reason": "Customer satisfaction",
            "expected": "ALLOW",
        },
        {
            "name": "Edge Case - Just Under Limit (Should ALLOW)",
            "amount": refund_limit - 1,
            "reason": "Product defect",
            "expected": "ALLOW",
        },
        {
            "name": "At Limit (Should DENY - not less than limit)",
            "amount": refund_limit,
            "reason": "Return request",
            "expected": "DENY",
        },
        {
            "name": "Over Limit (Should DENY)",
            "amount": 2000,
            "reason": "Large return",
            "expected": "DENY",
        },
    ]

    print("Running test cases...")
    print("-" * 60)

    results = []
    for i, test in enumerate(test_cases, 1):
        print(f"\n📝 Test {i}: {test['name']}")
        print(f"   Amount: ${test['amount']}")
        print(f"   Expected: {test['expected']}")

        status_code, response = test_refund(
            gateway_url, token, test["amount"], test["reason"]
        )

        # Determine if allowed or denied
        if status_code == 200 and "error" not in response:
            actual = "ALLOW"
            result_icon = "✅"
        else:
            actual = "DENY"
            result_icon = "🛡️"

        passed = actual == test["expected"]
        test_result = "PASS" if passed else "FAIL"

        print(f"   Actual: {actual}")
        print(f"   Result: {result_icon} {test_result}")

        if not passed:
            print(f"   Response: {json.dumps(response, indent=2)}")

        results.append({"test": test["name"], "passed": passed, "actual": actual})

    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)

    passed_count = sum(1 for r in results if r["passed"])
    total_count = len(results)

    for r in results:
        icon = "✅" if r["passed"] else "❌"
        print(f"  {icon} {r['test']}")

    print()
    print(f"Results: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print("\n🎉 All tests passed! Policy enforcement is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the policy configuration.")

    print("=" * 60)

    return passed_count == total_count


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
