#!/usr/bin/env python3
"""
AgentCore Code Interpreter Demo

Demonstrates AWS Bedrock AgentCore Code Interpreter for sandboxed code execution.

Features shown:
- Python/JS/TS execution: Run code in isolated sandboxes
- File handling: Upload files via S3 (up to 5GB)
- Terminal commands: Execute shell commands
- Data analysis: Generate charts and visualizations

Run locally:
    uv run python code_interpreter_demo.py

Environment variables:
    AWS_PROFILE - AWS profile to use (default: ag)
    AWS_REGION - AWS region (default: us-east-1)
"""

import json
import os
import time
from datetime import datetime

import boto3
from dotenv import load_dotenv

load_dotenv()

# Configure AWS
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
AWS_PROFILE = os.getenv("AWS_PROFILE", "ag")
os.environ["AWS_PROFILE"] = AWS_PROFILE

print(f"🔧 Using AWS Profile: {AWS_PROFILE}, Region: {AWS_REGION}")

# Initialize clients
control_client = boto3.client('bedrock-agentcore-control', region_name=AWS_REGION)
data_client = boto3.client('bedrock-agentcore', region_name=AWS_REGION)


def list_code_interpreters():
    """List existing code interpreter resources."""
    print("\n💻 Existing Code Interpreters:")
    try:
        response = control_client.list_code_interpreters()
        interpreters = response.get('codeInterpreterSummaries', [])

        if not interpreters:
            print("  (none found)")
            return []

        for ci in interpreters:
            print(f"  - {ci['name']} ({ci['codeInterpreterId']}) - {ci['status']}")

        return interpreters
    except Exception as e:
        print(f"  Error: {e}")
        return []


def create_code_interpreter() -> str | None:
    """Create a code interpreter resource or return existing one."""

    interpreters = control_client.list_code_interpreters().get('codeInterpreterSummaries', [])
    for ci in interpreters:
        if ci['status'] == 'READY':
            print(f"📦 Using existing code interpreter: {ci['codeInterpreterId']}")
            return ci['codeInterpreterId']

    # Create new code interpreter
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    ci_name = f"demo_code_interpreter_{timestamp}"

    print(f"\n🆕 Creating code interpreter: {ci_name}")

    try:
        response = control_client.create_code_interpreter(
            name=ci_name,
            description="Demo code interpreter for AgentCore showcase"
        )
        ci_id = response['codeInterpreterId']
        print(f"✅ Created code interpreter: {ci_id}")

        # Wait for it to be ready
        print("⏳ Waiting for code interpreter to be ready...")
        for _ in range(30):
            status = control_client.get_code_interpreter(codeInterpreterId=ci_id)
            if status['status'] == 'READY':
                print("✅ Code interpreter is ready!")
                return ci_id
            time.sleep(2)

        return ci_id
    except Exception as e:
        print(f"❌ Error creating code interpreter: {e}")
        return None


def execute_code_example(ci_id: str):
    """Show code execution example."""

    print("""
    Executing Python code in sandbox:

    ```python
    response = data_client.invoke_code_interpreter(
        codeInterpreterIdentifier=ci_id,
        sessionId="analysis-session-001",
        name="executeCode",
        arguments={
            "language": "python",
            "code": '''
import pandas as pd
import matplotlib.pyplot as plt

# Create sample data
data = {
    "month": ["Jan", "Feb", "Mar", "Apr"],
    "revenue": [1000, 1200, 1100, 1400]
}
df = pd.DataFrame(data)

# Analyze
print(df.describe())

# Visualize
plt.figure(figsize=(8, 5))
plt.bar(df["month"], df["revenue"])
plt.title("Monthly Revenue")
plt.savefig("/output/chart.png")
print("Chart saved to /output/chart.png")
'''
        }
    )
    ```

    Response includes:
    - stdout/stderr output
    - Generated files (accessible via session)
    - Execution status
    """)


def execute_terminal_example():
    """Show terminal command example."""

    print("""
    Executing terminal commands:

    ```python
    response = data_client.invoke_code_interpreter(
        codeInterpreterIdentifier=ci_id,
        sessionId="analysis-session-001",
        name="executeCommand",
        arguments={
            "command": "pip list && python --version"
        }
    )
    ```

    Available packages:
    - pandas, numpy, scipy
    - matplotlib, seaborn
    - scikit-learn
    - requests
    - And more common data science libraries
    """)


def demonstrate_langgraph_integration():
    """Show LangGraph integration pattern."""

    print("""
    LangGraph + Code Interpreter Integration:

    ```python
    from langchain_core.tools import tool
    import boto3

    data_client = boto3.client('bedrock-agentcore', region_name='us-east-1')
    CI_ID = "your-code-interpreter-id"

    @tool
    def execute_python(code: str) -> str:
        \"\"\"Execute Python code in a sandboxed environment.\"\"\"
        response = data_client.invoke_code_interpreter(
            codeInterpreterIdentifier=CI_ID,
            sessionId="agent-session",
            name="executeCode",
            arguments={
                "language": "python",
                "code": code
            }
        )
        return response.get('result', {}).get('output', '')

    @tool
    def analyze_data(file_s3_uri: str, analysis_prompt: str) -> str:
        \"\"\"Load data from S3 and perform analysis.\"\"\"
        code = f'''
import pandas as pd
import boto3

# Load from S3
s3 = boto3.client("s3")
# Parse S3 URI and download...

# Analysis based on prompt
df = pd.read_csv("/data/file.csv")
print(df.describe())
print(df.head())
'''
        return execute_python(code)

    # Use in LangGraph
    tools = [execute_python, analyze_data]
    llm_with_tools = llm.bind_tools(tools)
    ```
    """)


def demonstrate_code_interpreter():
    """Main demo showing AgentCore Code Interpreter capabilities."""

    print(f"\n{'='*60}")
    print("💻 AgentCore Code Interpreter Demo")
    print(f"{'='*60}")

    # List existing interpreters
    list_code_interpreters()

    # Explain concepts
    print(f"\n{'='*60}")
    print("📖 DEMO 1: Code Interpreter Concepts")
    print(f"{'='*60}")

    print("""
    AgentCore Code Interpreter provides:

    ┌─────────────────────────────────────────────────────────┐
    │           AgentCore Code Interpreter                     │
    │                                                          │
    │  ┌──────────────────────────────────────────────────┐   │
    │  │         Isolated Sandbox Environment              │   │
    │  │                                                    │   │
    │  │  ┌────────┐  ┌────────┐  ┌────────────────┐      │   │
    │  │  │ Python │  │  JS/TS │  │ Terminal Cmds  │      │   │
    │  │  └────────┘  └────────┘  └────────────────┘      │   │
    │  │                                                    │   │
    │  │  • pandas, numpy, matplotlib pre-installed        │   │
    │  │  • File I/O within sandbox                        │   │
    │  │  • S3 file access (up to 5GB)                     │   │
    │  │                                                    │   │
    │  └──────────────────────────────────────────────────┘   │
    │                          │                               │
    │                     Session API                          │
    │                          │                               │
    └──────────────────────────┼───────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │   LangGraph Agent   │
                    │   (invoke_code_     │
                    │    interpreter)     │
                    └─────────────────────┘

    Supported languages:
    - Python (with data science libraries)
    - JavaScript
    - TypeScript

    File limits:
    - Inline upload: 100 MB
    - S3 upload: 5 GB
    """)

    # Show code execution
    print(f"\n{'='*60}")
    print("🐍 DEMO 2: Python Execution")
    print(f"{'='*60}")

    execute_code_example("example-ci-id")

    # Show terminal commands
    print(f"\n{'='*60}")
    print("🖥️ DEMO 3: Terminal Commands")
    print(f"{'='*60}")

    execute_terminal_example()

    # Show LangGraph integration
    print(f"\n{'='*60}")
    print("🤖 DEMO 4: LangGraph Integration")
    print(f"{'='*60}")

    demonstrate_langgraph_integration()

    # Try to create a code interpreter
    print(f"\n{'='*60}")
    print("🚀 DEMO 5: Creating Code Interpreter")
    print(f"{'='*60}")

    ci_id = create_code_interpreter()

    # Summary
    print(f"\n{'='*60}")
    print("✅ Code Interpreter Demo Complete!")
    print(f"{'='*60}")

    print(f"""
    Code Interpreter ID: {ci_id or 'Not created'}

    Use cases for AgentCore Code Interpreter:

    1. **Data Analysis**: Agents analyze CSV/JSON data dynamically
    2. **Chart Generation**: Create visualizations on the fly
    3. **Mathematical Computation**: Complex calculations
    4. **Data Transformation**: Clean and process datasets
    5. **Script Execution**: Run agent-generated code safely

    Security benefits:
    - Complete sandbox isolation
    - No access to AWS resources directly (use S3 for files)
    - Session-based with automatic cleanup
    - Resource limits prevent abuse

    Next steps:
    1. Create a code interpreter resource
    2. Use invoke_code_interpreter() in your agent
    3. Let your agent dynamically generate and execute code
    """)


if __name__ == "__main__":
    demonstrate_code_interpreter()
