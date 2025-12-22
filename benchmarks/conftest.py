"""
Agent Skills Benchmark - pytest fixtures and helpers

Wraps Claude Code CLI for programmatic testing of skills and subagents.
"""

import json
import subprocess
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest


@dataclass
class ClaudeResult:
    """Parsed result from claude -p with stream-json output."""

    raw_events: list[dict] = field(default_factory=list)
    tool_calls: list[dict] = field(default_factory=list)
    tool_results: list[dict] = field(default_factory=list)
    final_text: str = ""
    session_id: str | None = None
    cost_usd: float = 0.0
    duration_ms: int = 0
    exit_code: int = 0
    stderr: str = ""

    @property
    def tools_used(self) -> list[str]:
        """List of unique tool names that were called."""
        return list({tc.get("name", "") for tc in self.tool_calls})

    def has_tool_call(self, tool_name: str) -> bool:
        """Check if a specific tool was called."""
        return tool_name in self.tools_used

    def tool_call_contains(self, substring: str) -> bool:
        """Check if any tool call input contains a substring."""
        for tc in self.tool_calls:
            if substring in json.dumps(tc.get("input", {})):
                return True
        return False

    def output_contains(self, substring: str) -> bool:
        """Check if final output contains a substring."""
        return substring.lower() in self.final_text.lower()


def parse_stream_json(stdout: str) -> ClaudeResult:
    """Parse claude --output-format stream-json output."""
    result = ClaudeResult()
    text_chunks = []

    for line in stdout.strip().split("\n"):
        if not line:
            continue
        try:
            event = json.loads(line)
            result.raw_events.append(event)

            event_type = event.get("type", "")

            if event_type == "tool_use":
                result.tool_calls.append({
                    "name": event.get("name", ""),
                    "input": event.get("input", {}),
                })
            elif event_type == "tool_result":
                result.tool_results.append({
                    "name": event.get("name", ""),
                    "output": event.get("output", ""),
                })
            elif event_type == "result":
                result.final_text = event.get("result", "")
                result.session_id = event.get("session_id")
                result.cost_usd = event.get("cost_usd", 0.0)
                result.duration_ms = event.get("duration_ms", 0)
            elif event_type == "assistant":
                # Extract text from assistant message content
                msg = event.get("message", {})
                for block in msg.get("content", []):
                    if block.get("type") == "text":
                        text_chunks.append(block.get("text", ""))

        except json.JSONDecodeError:
            continue

    # If no result event, use accumulated text chunks
    if not result.final_text and text_chunks:
        result.final_text = "\n".join(text_chunks)

    return result


def run_claude(
    prompt: str,
    *,
    plugin_dir: str | Path | None = None,
    allowed_tools: list[str] | None = None,
    max_turns: int = 5,
    timeout: int = 120,
    model: str | None = None,
) -> ClaudeResult:
    """
    Run claude CLI in headless mode and return parsed results.

    Args:
        prompt: The prompt to send to Claude
        plugin_dir: Path to plugin directory for --plugin-dir
        allowed_tools: List of tools to allow (auto-approved)
        max_turns: Maximum conversation turns
        timeout: Timeout in seconds
        model: Model override (sonnet, opus, haiku)

    Returns:
        ClaudeResult with parsed tool calls and output
    """
    cmd = [
        "claude",
        "-p", prompt,
        "--output-format", "stream-json",
        "--max-turns", str(max_turns),
        "--verbose",
    ]

    if plugin_dir:
        cmd.extend(["--plugin-dir", str(plugin_dir)])

    if allowed_tools:
        cmd.extend(["--allowedTools", ",".join(allowed_tools)])

    if model:
        cmd.extend(["--model", model])

    start = time.time()
    proc = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=timeout,
        cwd=Path(__file__).parent.parent,  # Run from repo root
    )
    elapsed = int((time.time() - start) * 1000)

    result = parse_stream_json(proc.stdout)
    result.exit_code = proc.returncode
    result.stderr = proc.stderr
    result.duration_ms = elapsed

    return result


@pytest.fixture
def claude():
    """Fixture providing run_claude function."""
    return run_claude


@pytest.fixture
def repo_root() -> Path:
    """Path to the repository root."""
    return Path(__file__).parent.parent


@pytest.fixture
def plugins_dir(repo_root) -> Path:
    """Path to plugins directory."""
    return repo_root / "plugins"
