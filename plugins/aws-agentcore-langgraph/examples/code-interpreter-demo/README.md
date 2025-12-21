# AgentCore Code Interpreter Demo

Demonstrates AWS Bedrock AgentCore Code Interpreter for sandboxed code execution.

## What This Shows

1. **Sandboxed Execution**: Run Python/JS/TS code in isolated environments
2. **Data Analysis**: Agents can analyze datasets dynamically
3. **File Handling**: Upload files via S3 (up to 5GB)
4. **Terminal Commands**: Execute shell commands in sandbox

## Quick Start

```bash
cd examples/code-interpreter-demo
cp .env.example .env

uv sync
uv run python code_interpreter_demo.py
```

## Code Interpreter Concepts

### Architecture

```
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
                └─────────────────────┘
```

### Supported Languages

| Language | Use Case |
|----------|----------|
| **Python** | Data analysis, ML, visualization |
| **JavaScript** | Data transformation, API calls |
| **TypeScript** | Type-safe scripting |

### File Limits

| Method | Maximum Size |
|--------|--------------|
| Inline upload | 100 MB |
| S3 upload | 5 GB |

## API Patterns

### Execute Python Code

```python
import boto3

data_client = boto3.client('bedrock-agentcore', region_name='us-east-1')

response = data_client.invoke_code_interpreter(
    codeInterpreterIdentifier="aws.codeinterpreter.v1",
    sessionId="analysis-session-001",
    name="executeCode",
    arguments={
        "language": "python",
        "code": """
import pandas as pd
import matplotlib.pyplot as plt

data = {"month": ["Jan", "Feb", "Mar"], "revenue": [1000, 1200, 1400]}
df = pd.DataFrame(data)

print(df.describe())

plt.bar(df["month"], df["revenue"])
plt.savefig("/output/chart.png")
"""
    }
)
```

### Execute Terminal Commands

```python
response = data_client.invoke_code_interpreter(
    codeInterpreterIdentifier="aws.codeinterpreter.v1",
    sessionId="analysis-session-001",
    name="executeCommand",
    arguments={
        "command": "pip list | head -20"
    }
)
```

### LangGraph Integration

```python
from langchain_core.tools import tool

@tool
def execute_python(code: str) -> str:
    """Execute Python code in a sandboxed environment."""
    response = data_client.invoke_code_interpreter(
        codeInterpreterIdentifier=CI_ID,
        sessionId="agent-session",
        name="executeCode",
        arguments={"language": "python", "code": code}
    )
    return response.get('result', {}).get('output', '')

# Use in agent
tools = [execute_python]
llm_with_tools = llm.bind_tools(tools)
```

## Pre-installed Libraries

The Python environment includes:
- pandas, numpy, scipy
- matplotlib, seaborn
- scikit-learn
- requests
- Beautiful Soup
- And more common data science libraries

## Use Cases

1. **Data Analysis**: Agents dynamically analyze CSV/JSON data
2. **Chart Generation**: Create visualizations based on data
3. **Mathematical Computation**: Complex calculations
4. **Data Transformation**: ETL operations
5. **Script Execution**: Run agent-generated code safely

## Security

- **Complete isolation**: Sandbox prevents access to host systems
- **No direct AWS access**: Use S3 references for files
- **Session-based**: Automatic cleanup after session ends
- **Resource limits**: Prevent abuse

## Next Steps

1. Create a code interpreter resource
2. Use `invoke_code_interpreter()` in your LangGraph agent
3. Let your agent dynamically generate and execute analysis code
