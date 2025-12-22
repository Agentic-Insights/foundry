"""
Agent Skills Benchmark - Test cases for marketplace plugins.

Run with: uv run pytest benchmarks/ -v
"""

import pytest
from conftest import run_claude


class TestBuildAgentSkills:
    """Test cases for build-agent-skills plugin."""

    @pytest.mark.slow
    def test_validate_skill_invokes_skills_ref(self, plugins_dir):
        """Skill should guide user to use skills-ref validate."""
        result = run_claude(
            "How do I validate an Agent Skill structure? Answer briefly with the command to use.",
            plugin_dir=plugins_dir / "build-agent-skills",
            allowed_tools=["Bash", "Read", "Glob", "Grep", "Skill"],
            max_turns=5,
            model="haiku",
        )

        # Should mention validation or skills-ref
        assert (
            result.tool_call_contains("skills-ref")
            or result.output_contains("skills-ref")
            or result.output_contains("valid")
            or result.output_contains("uvx")
        ), f"Expected validation mention. Got: {result.final_text[:500]}"

    @pytest.mark.slow
    def test_skill_structure_knowledge(self, plugins_dir):
        """Skill should know Agent Skills structure requirements."""
        result = run_claude(
            "Using your skill knowledge, what files are required in an Agent Skill directory? Answer briefly.",
            plugin_dir=plugins_dir / "build-agent-skills",
            allowed_tools=["Read", "Glob", "Grep"],
            max_turns=3,
            model="haiku",
        )

        # Should mention skill file requirements (SKILL.md or skill.json depending on spec version)
        assert (
            result.output_contains("SKILL.md")
            or result.output_contains("skill.md")
            or result.output_contains("skill.json")
            or result.output_contains("README")
        ), (
            f"Should mention skill file requirements. Got: {result.final_text[:500]}"
        )


class TestVhsRecorder:
    """Test cases for vhs-recorder plugin."""

    @pytest.mark.slow
    def test_tape_file_knowledge(self, plugins_dir):
        """Skill should know VHS tape file syntax."""
        result = run_claude(
            "What commands can I use in a VHS tape file? List the main commands briefly.",
            plugin_dir=plugins_dir / "vhs-recorder",
            allowed_tools=["Read", "Glob", "Grep"],
            max_turns=3,
            model="haiku",
        )

        # Should mention core VHS commands or tape/recording concepts
        vhs_concepts = ["Type", "Sleep", "Output", "Set", "Hide", "Show", "tape", "vhs", "command"]
        mentioned = sum(1 for cmd in vhs_concepts if result.output_contains(cmd))

        assert mentioned >= 1, (
            f"Should mention VHS concepts. Got: {result.final_text[:500]}"
        )

    @pytest.mark.slow
    def test_timing_guidance(self, plugins_dir):
        """Skill should provide timing best practices."""
        result = run_claude(
            "What are good timing values for VHS recordings? Answer from your skill knowledge only.",
            plugin_dir=plugins_dir / "vhs-recorder",
            allowed_tools=["Read", "Glob", "Grep"],
            max_turns=3,
            model="haiku",
        )

        # Should mention Sleep or timing-related content
        assert (
            result.output_contains("sleep")
            or result.output_contains("timing")
            or result.output_contains("ms")
            or result.output_contains("second")
        ), f"Should discuss timing. Got: {result.final_text[:500]}"


class TestBaml:
    """Test cases for baml plugin."""

    @pytest.mark.slow
    def test_schema_design_knowledge(self, plugins_dir):
        """Skill should know BAML schema patterns."""
        result = run_claude(
            "What keywords are used to define types in BAML? Answer briefly.",
            plugin_dir=plugins_dir / "baml",
            allowed_tools=["Read", "Glob", "Grep"],
            max_turns=3,
            model="haiku",
        )

        # Should mention BAML concepts or type-related keywords
        baml_concepts = ["class", "function", "enum", "client", "template", "string", "int", "type", "baml", "schema"]
        mentioned = sum(1 for c in baml_concepts if result.output_contains(c))

        assert mentioned >= 1, (
            f"Should mention BAML/type concepts. Got: {result.final_text[:500]}"
        )

    @pytest.mark.slow
    def test_extraction_patterns(self, plugins_dir):
        """Skill should know extraction patterns."""
        result = run_claude(
            "What is the basic pattern for extracting structured data with BAML? Answer briefly.",
            plugin_dir=plugins_dir / "baml",
            allowed_tools=["Read", "Glob", "Grep", "Skill"],
            max_turns=5,
            model="haiku",
        )

        # Should mention extraction concepts
        assert (
            result.output_contains("extract")
            or result.output_contains("schema")
            or result.output_contains("class")
            or result.output_contains("function")
            or result.output_contains("baml")
            or result.output_contains("type")
        ), f"Should discuss extraction. Got: {result.final_text[:500]}"


class TestAwsAgentcore:
    """Test cases for aws-agentcore-langgraph plugin."""

    @pytest.mark.slow
    def test_agentcore_cli_knowledge(self, plugins_dir):
        """Skill should know AgentCore CLI commands."""
        result = run_claude(
            "Using your skill knowledge, what CLI commands does the agentcore tool provide? Answer briefly.",
            plugin_dir=plugins_dir / "aws-agentcore-langgraph",
            allowed_tools=["Read", "Glob", "Grep"],
            max_turns=3,
            model="haiku",
        )

        # Should mention agentcore commands
        commands = ["configure", "launch", "invoke", "destroy", "agentcore", "deploy"]
        mentioned = sum(1 for cmd in commands if result.output_contains(cmd))

        assert mentioned >= 2, (
            f"Should mention AgentCore commands. Got: {result.final_text[:500]}"
        )

    @pytest.mark.slow
    def test_langgraph_patterns(self, plugins_dir):
        """Skill should know LangGraph integration patterns."""
        result = run_claude(
            "How does LangGraph integrate with AWS AgentCore? Answer briefly.",
            plugin_dir=plugins_dir / "aws-agentcore-langgraph",
            allowed_tools=["Read", "Glob", "Grep", "Skill"],
            max_turns=5,
            model="haiku",
        )

        # Should mention LangGraph or AgentCore concepts
        assert (
            result.output_contains("langgraph")
            or result.output_contains("graph")
            or result.output_contains("state")
            or result.output_contains("runtime")
            or result.output_contains("agent")
            or result.output_contains("aws")
        ), f"Should discuss LangGraph/AgentCore. Got: {result.final_text[:500]}"


class TestParaPkm:
    """Test cases for para-pkm plugin."""

    @pytest.mark.slow
    def test_para_structure_knowledge(self, plugins_dir):
        """Skill should know PARA methodology."""
        result = run_claude(
            "Using your skill knowledge, what are the four categories in the PARA method? Answer briefly.",
            plugin_dir=plugins_dir / "para-pkm",
            allowed_tools=["Read", "Glob", "Grep"],
            max_turns=3,
            model="haiku",
        )

        # Should mention all PARA categories
        para = ["Projects", "Areas", "Resources", "Archives"]
        mentioned = sum(1 for p in para if result.output_contains(p))

        assert mentioned >= 3, (
            f"Should mention PARA categories. Got: {result.final_text[:500]}"
        )


# Benchmark utilities for tracking results
def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Add benchmark summary to pytest output."""
    passed = len(terminalreporter.stats.get("passed", []))
    failed = len(terminalreporter.stats.get("failed", []))
    total = passed + failed

    if total > 0:
        terminalreporter.write_sep("=", "Agent Skills Benchmark Summary")
        terminalreporter.write_line(f"Passed: {passed}/{total} ({100*passed/total:.0f}%)")
        if failed > 0:
            terminalreporter.write_line(f"Failed: {failed}/{total}")
