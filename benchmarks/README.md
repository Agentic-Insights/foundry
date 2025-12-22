# Agent Skills Benchmark

Minimal benchmark harness for testing Agent Skills plugins using Claude Code's headless mode.

## Quick Start

```bash
# Run all benchmarks
./benchmarks/run.sh

# Run fast (skip slow LLM calls)
./benchmarks/run.sh --fast

# Run specific plugin tests
./benchmarks/run.sh -k baml
./benchmarks/run.sh -k vhs

# Generate JSON report
./benchmarks/run.sh --json
```

## Architecture

```
benchmarks/
├── conftest.py      # pytest fixtures + run_claude() helper
├── test_skills.py   # Test cases for each plugin
├── pyproject.toml   # Dependencies (pytest, pytest-json-report)
├── run.sh           # Convenience runner
└── results/         # JSON reports from --json runs
```

## How It Works

1. **Wraps Claude CLI**: Uses `claude -p "<prompt>" --output-format stream-json`
2. **Parses Results**: Extracts tool calls, outputs, costs from stream
3. **Runs Assertions**: Verifies skills provide expected guidance
4. **Uses Haiku**: Fast model for cost-effective testing

## Writing Tests

```python
def test_my_skill(plugins_dir):
    result = run_claude(
        "Your test prompt here",
        plugin_dir=plugins_dir / "my-plugin",
        allowed_tools=["Read", "Bash"],
        max_turns=3,
        model="haiku",
    )

    # Assertions
    assert result.output_contains("expected phrase")
    assert result.has_tool_call("Bash")
    assert result.tool_call_contains("some-command")
```

## ClaudeResult API

| Property | Description |
|----------|-------------|
| `tools_used` | List of unique tool names called |
| `tool_calls` | Full tool call details with inputs |
| `final_text` | Claude's final response text |
| `cost_usd` | API cost for the run |
| `duration_ms` | Total runtime |
| `has_tool_call(name)` | Check if tool was used |
| `tool_call_contains(s)` | Check if any tool input contains string |
| `output_contains(s)` | Check if output contains string (case-insensitive) |

## Future Improvements

- [ ] Integrate with [Inspect AI](https://inspect.ai-safety-institute.org.uk/) for richer evals
- [ ] Add LLM-as-judge scoring for response quality
- [ ] Track benchmark results over time
- [ ] CI integration with GitHub Actions
